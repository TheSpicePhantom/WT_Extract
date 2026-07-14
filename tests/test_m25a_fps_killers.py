"""Tests — M25a FPS Killer Attribution v2."""

from __future__ import annotations

from game_core.perf.run_analysis.fps_killers import (
    build_ab_comparison,
    build_quantile_dominance,
    classify_dominant_phase,
    decision_cpu_vs_present_vs_gpu,
    fps_killers_payload,
    phase_shares,
    pick_quantile_frame,
)
from game_core.perf.run_analysis.models import FrameRecord


def _frame(
    frame_index: int,
    cpu_full: float,
    *,
    pool: float = 0.0,
    apply: float = 0.0,
    tile: float = 0.0,
    deco: float = 0.0,
    render: float = 0.0,
    present: float = 0.0,
) -> FrameRecord:
    apply_total = apply + pool
    return FrameRecord(
        frame_index=frame_index,
        frame_ms=cpu_full * 0.5,
        stream_ms=apply_total,
        stream_apply_ms=apply_total,
        stream_unload_ms=0.0,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=8,
        focus_x=0.0,
        focus_y=0.0,
        zoom=0.35,
        cpu_full_frame_ms=cpu_full,
        apply_pool_ms=pool,
        tile_extract_ms=tile,
        deco_extract_ms=deco,
        render_cpu_ms=render,
        present_wait_cpu_ms=present,
    )


def test_classify_stream_pool_dominant() -> None:
    frame = _frame(0, 100.0, pool=40.0)
    shares = phase_shares(frame)
    assert shares is not None
    phase, share = classify_dominant_phase(shares)
    assert phase == "stream_pool"
    assert share == 0.4


def test_classify_mixed_when_top_two_close() -> None:
    shares = {
        "stream_pool": 0.30,
        "extract_deco": 0.28,
        "stream_apply": 0.0,
        "extract_tiles": 0.0,
        "render_cpu": 0.0,
        "present_wait": 0.0,
        "gpu": 0.0,
    }
    phase, _ = classify_dominant_phase(shares)
    assert phase == "mixed"


def test_classify_unclear_when_all_small() -> None:
    shares = {phase: 0.05 for phase in shares_keys()}
    phase, _ = classify_dominant_phase(shares)
    assert phase == "unclear"


def shares_keys() -> tuple[str, ...]:
    return (
        "stream_apply",
        "stream_pool",
        "extract_tiles",
        "extract_deco",
        "render_cpu",
        "present_wait",
        "gpu",
    )


def test_decision_present_wait_dominant() -> None:
    frames = [_frame(i, 100.0, present=50.0, pool=10.0) for i in range(10)]
    decision = decision_cpu_vs_present_vs_gpu(frames)
    assert decision["decision"] == "present_wait_dominant"
    assert "reason_cpu_vs_present" in decision


def test_decision_cpu_dominant() -> None:
    frames = [_frame(i, 100.0, pool=45.0) for i in range(10)]
    decision = decision_cpu_vs_present_vs_gpu(frames)
    assert decision["decision"] == "cpu_dominant"


def test_quantile_picks_different_frames() -> None:
    frames = [
        _frame(0, 10.0, pool=4.0),
        _frame(1, 20.0, pool=8.0),
        _frame(2, 30.0, pool=12.0),
        _frame(3, 40.0, pool=16.0),
        _frame(4, 50.0, pool=20.0),
    ]
    quantiles, same = build_quantile_dominance(frames)
    assert quantiles["p95"]["frame_index"] != quantiles["p99"]["frame_index"]
    assert same is False


def test_quantile_same_frame_flag_when_only_one_candidate() -> None:
    frames = [_frame(0, 50.0, pool=20.0)]
    quantiles, same = build_quantile_dominance(frames)
    assert quantiles["p95"]["frame_index"] == quantiles["p99"]["frame_index"]
    assert same is True


def test_pick_quantile_excludes_p95_frame_for_p99() -> None:
    frames = [
        _frame(0, 40.0),
        _frame(1, 41.0),
        _frame(2, 42.0),
    ]
    p95 = pick_quantile_frame(frames, 41.0)
    p99 = pick_quantile_frame(frames, 42.0, exclude_indices={p95.frame_index})
    assert p95.frame_index == 1
    assert p99.frame_index == 2


def test_payload_includes_scenario_context() -> None:
    manifest = {
        "scenario_id": "steady",
        "run_id": "test_run",
        "run_mode": "cli",
        "extract_enabled": True,
        "stream_enabled": True,
        "deco_extract_enabled": True,
        "tile_extract_enabled": True,
    }
    frames = [_frame(i, 50.0, pool=20.0) for i in range(20)]
    payload = fps_killers_payload(frames, manifest=manifest)
    assert payload["scenario_id"] == "steady"
    assert payload["run_id"] == "test_run"
    assert payload["attribution_version"] == 2
    assert payload["quantiles"]["p95"]["dominant_phase"] == "stream_pool"
    assert payload["decision"]["decision"] == "cpu_dominant"


def test_ab_comparison_structure() -> None:
    baseline = fps_killers_payload(
        [_frame(i, 60.0, pool=25.0) for i in range(20)],
        manifest={"scenario_id": "steady", "run_id": "base", "extract_enabled": True},
    )
    variant = fps_killers_payload(
        [_frame(i, 40.0, pool=10.0) for i in range(20)],
        manifest={"scenario_id": "steady", "run_id": "var", "extract_enabled": False},
    )
    ab = build_ab_comparison(baseline, variant, causal_feature="extract_enabled")
    assert ab["causal_feature"] == "extract_enabled"
    assert ab["baseline"]["run_id"] == "base"
    assert ab["variant"]["run_id"] == "var"
    assert ab["delta"]["cpu_full_frame_ms_p95"] is not None
