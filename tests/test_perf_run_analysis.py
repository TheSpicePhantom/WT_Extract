"""Tests für Profiling-Run-Analyse."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from game_core.perf.export_schema import SCHEMA_VERSION, write_run_export
from game_core.perf.models import FrameMetrics, HitchEvent, RunSummary
from game_core.perf.run_analysis.diagnose import analyze_run, load_budget_caps
from game_core.perf.run_analysis.hitch import (
    CAUSE_APPLY,
    CAUSE_MIXED,
    CAUSE_UNLOAD,
    PATTERN_BACKLOG,
    PATTERN_ISOLATED,
    classify_hitch_cause,
    analyze_hitches,
)
from game_core.perf.run_analysis.load import RunLoadError, load_run
from game_core.perf.run_analysis.reconstruct import check_summary, recompute_summary
from game_core.perf.run_analysis.report import write_all_reports


def _frame(
    index: int,
    *,
    frame_ms: float = 2.0,
    stream_apply_ms: float = 0.5,
    stream_unload_ms: float = 0.1,
    stream_loaded: int = 1,
    stream_unloaded: int = 0,
    pending: int | None = None,
    deco: float | None = None,
    tile: float | None = None,
) -> FrameMetrics:
    stream_ms = stream_apply_ms + stream_unload_ms
    return FrameMetrics(
        schema_version=SCHEMA_VERSION,
        frame_index=index,
        scenario_id="test",
        frame_ms=frame_ms,
        stream_ms=stream_ms,
        stream_apply_ms=stream_apply_ms,
        stream_unload_ms=stream_unload_ms,
        stream_loaded=stream_loaded,
        stream_unloaded=stream_unloaded,
        chunk_count=100,
        focus_x=10.0,
        focus_y=20.0,
        zoom=1.0,
        deco_extract_ms=deco,
        tile_extract_ms=tile,
        pending_unload_count=pending,
    )


def _hitch(
    index: int,
    *,
    frame_ms: float,
    stream_apply_ms: float,
    stream_unload_ms: float = 0.1,
    tags: tuple[str, ...] = ("frame_slow",),
    pending: int | None = None,
) -> HitchEvent:
    return HitchEvent(
        schema_version=SCHEMA_VERSION,
        frame_index=index,
        scenario_id="test",
        tags=tags,
        frame_ms=frame_ms,
        stream_ms=stream_apply_ms + stream_unload_ms,
        stream_apply_ms=stream_apply_ms,
        stream_unload_ms=stream_unload_ms,
        stream_loaded=4,
        stream_unloaded=0,
        chunk_count=100,
        focus_x=10.0,
        focus_y=20.0,
        zoom=1.0,
    )


def _write_synthetic_run(tmp_path: Path, *, with_m23a: bool = True) -> Path:
    run_dir = tmp_path / "run_test"
    pending_kw = {"pending": 0 if with_m23a else None}
    frames = [
        _frame(i, frame_ms=2.0, stream_apply_ms=0.4, **pending_kw)
        for i in range(10)
    ]
    frames.append(
        _frame(
            10,
            frame_ms=40.0,
            stream_apply_ms=38.0,
            stream_loaded=4,
            pending=5 if with_m23a else None,
        )
    )
    frames.append(_frame(11, frame_ms=3.0, stream_apply_ms=0.5, pending=2 if with_m23a else None))
    frames.extend(
        _frame(i, frame_ms=2.0, stream_apply_ms=0.3, **pending_kw)
        for i in range(12, 20)
    )

    hitches = [
        _hitch(10, frame_ms=40.0, stream_apply_ms=38.0, tags=("frame_slow", "stream_slow", "load_burst")),
    ]

    summary = RunSummary(
        schema_version=SCHEMA_VERSION,
        run_id="run_test",
        scenario_id="test",
        run_mode="synthetic",
        recorded_frames=len(frames),
        frame_ms_mean=4.0,
        frame_ms_p95=10.0,
        frame_ms_max=40.0,
        stream_ms_mean=2.0,
        stream_ms_p95=5.0,
        stream_ms_max=38.1,
        stream_unload_ms_p95=0.1,
        stream_unload_ms_max=0.1,
        hitch_count=1,
        hitch_frame_count=1,
        hitch_stream_count=1,
        hitch_load_count=1,
        hitch_unload_count=0,
        max_loaded_per_frame=4,
        max_unloaded_per_frame=0,
        chunk_count_mean=100.0,
    )

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": "run_test",
        "recorded_at": "2026-01-01T00:00:00+00:00",
        "scenario_id": "test",
        "run_mode": "synthetic",
        "extract_enabled": True,
        "warmup_frames": 2,
        "recorded_frames": len(frames),
        "git_commit": "test",
        "config_fingerprint": {"profiling": "1", "streaming": "2", "world_gen": "3"},
    }

    write_run_export(run_dir, manifest=manifest, frames=frames, hitches=hitches, summary=summary)
    return run_dir


def test_load_run_validates_schema_version(tmp_path: Path) -> None:
    run_dir = _write_synthetic_run(tmp_path)
    loaded = load_run(run_dir)
    assert loaded.manifest["run_id"] == "run_test"
    assert len(loaded.frames) == 20
    assert len(loaded.hitches) == 1
    if loaded.optional_fields:
        assert "pending_unload_count" in loaded.optional_fields


def test_load_run_rejects_bad_schema(tmp_path: Path) -> None:
    run_dir = _write_synthetic_run(tmp_path)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["schema_version"] = 99
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(RunLoadError, match="schema_version"):
        load_run(run_dir)


def test_recompute_summary_matches_export(tmp_path: Path) -> None:
    run_dir = _write_synthetic_run(tmp_path)
    loaded = load_run(run_dir)
    recomputed = recompute_summary(
        loaded.frames,
        loaded.hitches,
        run_id="run_test",
        scenario_id="test",
        run_mode="synthetic",
        schema_version=SCHEMA_VERSION,
    )
    checks = check_summary(loaded.summary, recomputed)
    int_checks = [check for check in checks if check.field in {"recorded_frames", "hitch_count", "hitch_load_count"}]
    assert all(check.ok for check in int_checks)
    assert recomputed["frame_ms_max"] == pytest.approx(40.0)


def test_summary_mismatch_detected() -> None:
    summary = {"recorded_frames": 10, "frame_ms_mean": 5.0}
    recomputed = {"recorded_frames": 12, "frame_ms_mean": 5.0}
    checks = check_summary(summary, recomputed)
    frame_check = next(check for check in checks if check.field == "recorded_frames")
    assert not frame_check.ok


def test_hitch_classification_apply_dominant() -> None:
    from game_core.perf.run_analysis.models import HitchRecord

    hitch = HitchRecord(
        frame_index=1,
        frame_ms=100.0,
        stream_ms=90.0,
        stream_apply_ms=85.0,
        stream_unload_ms=1.0,
        stream_loaded=4,
        stream_unloaded=0,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("frame_slow", "load_burst"),
    )
    cause = classify_hitch_cause(hitch)
    assert cause.cause_id == CAUSE_APPLY
    assert cause.reasons


def test_hitch_classification_mixed() -> None:
    from game_core.perf.run_analysis.models import HitchRecord

    hitch = HitchRecord(
        frame_index=1,
        frame_ms=100.0,
        stream_ms=50.0,
        stream_apply_ms=35.0,
        stream_unload_ms=35.0,
        stream_loaded=4,
        stream_unloaded=2,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("frame_slow",),
    )
    cause = classify_hitch_cause(hitch)
    assert cause.cause_id == CAUSE_MIXED


def test_backlog_pattern_detection() -> None:
    from game_core.perf.run_analysis.models import FrameRecord, HitchRecord

    frames = [
        FrameRecord(
            frame_index=i,
            frame_ms=2.0,
            stream_ms=0.5,
            stream_apply_ms=0.4,
            stream_unload_ms=0.1,
            stream_loaded=1,
            stream_unloaded=0,
            chunk_count=100,
            focus_x=0.0,
            focus_y=0.0,
            zoom=1.0,
            pending_unload_count=count,
        )
        for i, count in enumerate([10, 20, 30])
    ]
    hitch = HitchRecord(
        frame_index=2,
        frame_ms=30.0,
        stream_ms=5.0,
        stream_apply_ms=2.0,
        stream_unload_ms=3.0,
        stream_loaded=2,
        stream_unloaded=2,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("unload_backlog",),
        pending_unload_count=40,
    )
    analyses = analyze_hitches(frames, [hitch], context_radius=2)
    assert analyses[0].context_pattern.pattern_id == PATTERN_BACKLOG


def test_isolated_spike_pattern() -> None:
    from game_core.perf.run_analysis.models import FrameRecord, HitchRecord

    frames = [
        FrameRecord(
            frame_index=i,
            frame_ms=2.0,
            stream_ms=0.5,
            stream_apply_ms=0.4,
            stream_unload_ms=0.1,
            stream_loaded=1,
            stream_unloaded=0,
            chunk_count=100,
            focus_x=0.0,
            focus_y=0.0,
            zoom=1.0,
        )
        for i in range(5)
    ]
    frames[2] = FrameRecord(
        frame_index=2,
        frame_ms=80.0,
        stream_ms=75.0,
        stream_apply_ms=74.0,
        stream_unload_ms=1.0,
        stream_loaded=4,
        stream_unloaded=0,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
    )
    hitch = HitchRecord(
        frame_index=2,
        frame_ms=80.0,
        stream_ms=75.0,
        stream_apply_ms=74.0,
        stream_unload_ms=1.0,
        stream_loaded=4,
        stream_unloaded=0,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("frame_slow",),
    )
    analyses = analyze_hitches(frames, [hitch], context_radius=2)
    assert analyses[0].context_pattern.pattern_id == PATTERN_ISOLATED


def test_analyze_run_without_optional_fields(tmp_path: Path) -> None:
    run_dir = _write_synthetic_run(tmp_path, with_m23a=False)
    loaded = load_run(run_dir)
    diagnosis = analyze_run(loaded, caps=load_budget_caps(max_applies=4, max_unloads=2))
    assert diagnosis.problem_ranking
    assert "pending_unload_count" not in diagnosis.optional_fields
    assert any("Backlog" in item for item in diagnosis.budget_insights + diagnosis.open_questions)


def test_report_outputs(tmp_path: Path) -> None:
    run_dir = _write_synthetic_run(tmp_path)
    loaded = load_run(run_dir)
    diagnosis = analyze_run(loaded)
    out_dir = tmp_path / "out"
    paths = write_all_reports(diagnosis, out_dir)
    assert paths["markdown"].is_file()
    assert paths["json"].is_file()
    assert paths["hitches_csv"].is_file()
    assert paths["notable_frames_csv"].is_file()
    md = paths["markdown"].read_text(encoding="utf-8")
    assert "Hitch-Analyse" in md


def test_unload_dominant_classification() -> None:
    from game_core.perf.run_analysis.models import HitchRecord

    hitch = HitchRecord(
        frame_index=1,
        frame_ms=20.0,
        stream_ms=18.0,
        stream_apply_ms=1.0,
        stream_unload_ms=17.0,
        stream_loaded=0,
        stream_unloaded=2,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("unload_burst",),
    )
    assert classify_hitch_cause(hitch).cause_id == CAUSE_UNLOAD
