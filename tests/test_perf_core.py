"""Tests — game_core/perf Kern (M23 Phase 0)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from game_core.perf.aggregate import PerfAggregator
from game_core.perf.config import load_profiling_config
from game_core.perf.export_schema import (
    SCHEMA_VERSION,
    assert_supported_schema_version,
    validate_frame_line,
    validate_hitch_line,
    validate_manifest,
    validate_summary,
    write_run_export,
)
from game_core.perf.hitch import classify_hitch
from game_core.perf.models import FrameMetrics, HitchEvent, RunSummary, StreamStepMetrics
from game_core.perf.session import PerfSession


def _sample_frame(**overrides) -> FrameMetrics:
    base = dict(
        schema_version=SCHEMA_VERSION,
        frame_index=0,
        scenario_id="steady",
        frame_ms=5.0,
        stream_ms=2.0,
        stream_apply_ms=1.0,
        stream_unload_ms=0.5,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=10,
        focus_x=256.0,
        focus_y=256.0,
        zoom=0.35,
    )
    base.update(overrides)
    return FrameMetrics(**base)


def test_classify_hitch_multiple_tags_ordered() -> None:
    config = load_profiling_config()
    frame = _sample_frame(
        frame_ms=100.0,
        stream_ms=100.0,
        stream_loaded=10,
        stream_unloaded=10,
    )
    tags = classify_hitch(frame, config.hitch)
    assert tags == ("frame_slow", "stream_slow", "load_burst", "unload_burst")


def test_classify_hitch_no_tags() -> None:
    config = load_profiling_config()
    frame = _sample_frame()
    assert classify_hitch(frame, config.hitch) == ()


def test_schema_validation_rejects_unknown_version() -> None:
    with pytest.raises(ValueError, match="Unsupported schema_version"):
        assert_supported_schema_version(99)


def test_write_run_export_empty_hitches(tmp_path: Path) -> None:
    aggregator = PerfAggregator()
    frame = _sample_frame()
    aggregator.record_frame(frame)
    summary = aggregator.build_summary(
        schema_version=SCHEMA_VERSION,
        run_id="test_run",
        scenario_id="steady",
        run_mode="cli",
    )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": "test_run",
        "recorded_at": "2026-01-01T00:00:00+00:00",
        "scenario_id": "steady",
        "run_mode": "cli",
        "extract_enabled": True,
        "warmup_frames": 0,
        "recorded_frames": 1,
        "git_commit": "test",
        "config_fingerprint": {},
    }
    write_run_export(
        tmp_path,
        manifest=manifest,
        frames=aggregator.frames,
        hitches=[],
        summary=summary,
    )
    assert (tmp_path / "manifest.json").is_file()
    assert (tmp_path / "frames.jsonl").is_file()
    assert (tmp_path / "hitches.jsonl").is_file()
    assert (tmp_path / "summary.json").is_file()
    validate_manifest(json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8")))
    frame_line = json.loads((tmp_path / "frames.jsonl").read_text(encoding="utf-8").strip())
    validate_frame_line(frame_line)
    summary_data = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    validate_summary(summary_data)


def test_hitch_event_serializable() -> None:
    event = HitchEvent(
        schema_version=SCHEMA_VERSION,
        frame_index=1,
        scenario_id="pan",
        tags=("unload_burst",),
        frame_ms=10.0,
        stream_ms=9.0,
        stream_apply_ms=1.0,
        stream_unload_ms=8.0,
        stream_loaded=0,
        stream_unloaded=5,
        chunk_count=20,
        focus_x=512.0,
        focus_y=256.0,
        zoom=0.35,
    )
    payload = event.to_dict()
    validate_hitch_line(payload)


def test_perf_session_warmup_excluded() -> None:
    config = load_profiling_config()
    session = PerfSession(
        config=config,
        scenario_id="steady",
        run_mode="cli",
    )
    session._warmup_frames = 2

    class _Cb:
        chunk_count = 5
        deco_sprite_count = 0

        def on_scenario_step(self, *_args) -> None:
            pass

        def on_stream_update(self, step: StreamStepMetrics):
            step.total_ms = 1.0
            return 0, 0

        def on_deco_extract(self, _extract_metrics=None) -> float:
            return 0.1

        def on_tile_extract(self, _extract_metrics=None) -> float:
            return 0.1

    cb = _Cb()
    assert session.run_canonical_tick(cb, focus_x=256, focus_y=256, zoom=0.35, move_dx=0, move_dy=0) is None
    assert session.run_canonical_tick(cb, focus_x=256, focus_y=256, zoom=0.35, move_dx=0, move_dy=0) is None
    frame = session.run_canonical_tick(cb, focus_x=256, focus_y=256, zoom=0.35, move_dx=0, move_dy=0)
    assert frame is not None
    assert frame.frame_index == 0
