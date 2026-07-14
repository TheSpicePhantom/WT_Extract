"""Tests — M25d CPU Full-Frame Bilanz v4."""

from __future__ import annotations

import pytest

from game_core.perf.cpu_balance import (
    cpu_attributed_ms,
    cpu_attributed_ms_v4,
    has_v4_attribution,
    reconcile_cpu_balance,
)
from game_core.perf.models import FrameMetrics
from game_core.perf.run_analysis.fps_killers import attribution_incompatible_v4, phase_ms_buckets
from game_core.perf.run_analysis.load import load_run
from game_core.perf.run_analysis.models import FrameRecord
from game_core.perf.run_analysis.phase_enum import ATTRIBUTION_VERSION
from game_core.perf.config import load_profiling_config
from game_core.perf.models import ExtractStepMetrics, StreamStepMetrics
from game_core.perf.session import PerfSession, TickCallbacks
from tools import gate_perf_run


class _DummyCallbacks(TickCallbacks):
    def on_scenario_step(self, focus_x, focus_y, zoom, move_dx, move_dy) -> None:
        pass

    def on_stream_update(self, step_metrics: StreamStepMetrics) -> tuple[int, int]:
        return 0, 0

    def on_deco_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        return 1.0

    def on_tile_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        return 2.0

    @property
    def chunk_count(self) -> int:
        return 10

    @property
    def deco_sprite_count(self) -> int:
        return 5


def _frame_metrics(**kwargs) -> FrameMetrics:
    base = dict(
        schema_version=1,
        frame_index=0,
        scenario_id="test",
        frame_ms=10.0,
        stream_ms=3.0,
        stream_apply_ms=2.0,
        stream_unload_ms=0.0,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=10,
        focus_x=0.0,
        focus_y=0.0,
        zoom=0.35,
    )
    base.update(kwargs)
    return FrameMetrics(**base)


def test_v4_balance_closes() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=40.0,
        frame_ms=10.0,
        cpu_input_ms=1.0,
        cpu_framework_pre_tick_ms=2.0,
        cpu_framework_post_tick_ms=15.0,
        cpu_render_submit_ms=10.0,
        cpu_present_cpu_ms=2.0,
        cpu_framework_post_present_ms=0.0,
    )
    assert has_v4_attribution(frame)
    assert cpu_attributed_ms_v4(frame) == 40.0
    delta, residual = reconcile_cpu_balance(frame)
    assert delta is not None and abs(delta) < 0.05
    assert residual == 0.0


def test_v4_child_fields_not_double_counted() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=30.0,
        frame_ms=10.0,
        cpu_input_ms=1.0,
        cpu_framework_pre_tick_ms=1.0,
        cpu_framework_post_tick_ms=10.0,
        cpu_render_submit_ms=6.0,
        cpu_present_cpu_ms=2.0,
        cpu_sim_ms=5.0,
        cpu_camera_ms=3.0,
        cpu_extract_render_ms=4.0,
    )
    assert cpu_attributed_ms(frame) == 30.0


def test_v4_negative_delta_exported() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=10.0,
        frame_ms=20.0,
        cpu_input_ms=1.0,
        cpu_framework_pre_tick_ms=1.0,
        cpu_framework_post_tick_ms=5.0,
        cpu_render_submit_ms=6.0,
    )
    delta, residual = reconcile_cpu_balance(frame)
    assert delta is not None and delta < 0.0
    assert residual == 0.0


def test_phase_ms_buckets_v4() -> None:
    frame = FrameRecord(
        frame_index=0,
        frame_ms=10.0,
        stream_ms=3.0,
        stream_apply_ms=2.0,
        stream_unload_ms=0.0,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=10,
        focus_x=0.0,
        focus_y=0.0,
        zoom=0.35,
        cpu_full_frame_ms=30.0,
        extra={
            "cpu_input_ms": 1.0,
            "cpu_framework_pre_tick_ms": 2.0,
            "cpu_framework_post_tick_ms": 12.0,
            "cpu_render_submit_ms": 5.0,
            "cpu_present_cpu_ms": 0.0,
            "cpu_measurement_residual_ms": 0.01,
        },
    )
    buckets = phase_ms_buckets(frame)
    assert buckets["canonical_tick"] == 10.0
    assert buckets["cpu_render_submit"] == 5.0
    assert "cpu_sim" not in buckets


def test_full_frame_timer_scope() -> None:
    config = load_profiling_config()
    session = PerfSession(config=config, scenario_id="steady", run_mode="test", extract_enabled=True)
    session.full_frame_enabled = True
    session._warmup_frames = 0

    session.begin_full_frame()
    session.record_full_frame_phase("cpu_input_ms", 1.0)
    session.record_app_phase("cpu_sim_ms", 2.0)
    frame = session.run_canonical_tick(
        _DummyCallbacks(), focus_x=0.0, focus_y=0.0, zoom=1.0, move_dx=0.0, move_dy=0.0
    )
    assert frame is not None
    session.record_full_frame_phase("cpu_framework_post_tick_ms", 3.0)
    session.record_render_timing("render_pack_ms", 2.0)
    session.record_render_timing("pre_render_ms", 1.0)
    full_ms = session.end_full_frame()
    finalized = session.finalize_pending_frame(cpu_full_frame_ms=full_ms)
    assert finalized is not None
    assert finalized.cpu_render_submit_ms is not None
    assert finalized.cpu_measurement_residual_ms is not None

    with pytest.raises(AssertionError):
        session.record_app_phase("cpu_sim_ms", 1.0)


def test_record_before_begin_fails() -> None:
    config = load_profiling_config()
    session = PerfSession(config=config, scenario_id="steady", run_mode="test")
    session.full_frame_enabled = True
    with pytest.raises(AssertionError):
        session.record_full_frame_phase("cpu_input_ms", 1.0)


def test_loader_v3_run_attribution_incompatible() -> None:
    run_dir = (
        __import__("pathlib").Path(__file__).resolve().parents[1]
        / "docs/benchmarks/perf/runs/20260714T090831Z_demo_a9aaa9e"
    )
    loaded = load_run(run_dir)
    assert loaded.attribution_version == 3
    assert attribution_incompatible_v4(loaded.frames)


def test_gate_overhead_ab_helper() -> None:
    def _frames(value: float, n: int = 50):
        return [
            FrameRecord(
                frame_index=i,
                frame_ms=10.0,
                stream_ms=3.0,
                stream_apply_ms=2.0,
                stream_unload_ms=0.0,
                stream_loaded=0,
                stream_unloaded=0,
                chunk_count=10,
                focus_x=0.0,
                focus_y=0.0,
                zoom=0.35,
                cpu_full_frame_ms=value,
                extra={},
            )
            for i in range(n)
        ]

    checks = gate_perf_run.gate_cpu_full_frame_overhead_ab(
        _frames(20.0),
        _frames(20.2),
        p50_delta_max_ms=0.5,
        p95_delta_max_ms=1.5,
        p95_delta_max_pct=0.03,
        mean_delta_max_ms=0.3,
    )
    assert all(ok for ok, _ in checks)


def test_attribution_version_is_4() -> None:
    assert ATTRIBUTION_VERSION == 4


def test_no_cpu_other_named_in_v4_frame() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=20.0,
        frame_ms=10.0,
        cpu_input_ms=1.0,
        cpu_framework_pre_tick_ms=1.0,
        cpu_framework_post_tick_ms=5.0,
        cpu_render_submit_ms=3.0,
    )
    assert not hasattr(frame, "cpu_other_named_ms") or getattr(frame, "cpu_other_named_ms", None) is None
