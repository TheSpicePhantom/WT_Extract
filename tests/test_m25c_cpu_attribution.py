"""Tests — M25c CPU Full-Frame Attribution & Burst-Klassifikation."""

from __future__ import annotations

from game_core.perf.cpu_balance import cpu_attributed_ms, reconcile_cpu_balance
from game_core.perf.models import FrameMetrics
from game_core.perf.run_analysis.burst_classify import classify_stream_burst, is_burst_frame
from game_core.perf.run_analysis.diagnose import build_cpu_balance, build_stream_burst_table
from game_core.perf.run_analysis.fps_killers import phase_ms_buckets
from game_core.perf.run_analysis.load import load_run
from game_core.perf.run_analysis.models import FrameRecord
from game_core.perf.run_analysis.phase_enum import ATTRIBUTION_VERSION
from game_core.perf.session import PerfSession, TickCallbacks
from game_core.perf.config import load_profiling_config
from game_core.perf.models import ExtractStepMetrics, StreamStepMetrics
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


def test_cpu_balance_closes() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=40.0,
        frame_ms=10.0,
        cpu_input_ms=1.0,
        cpu_app_ui_ms=2.0,
        cpu_sim_ms=5.0,
        cpu_camera_ms=3.0,
        cpu_extract_render_ms=6.0,
        cpu_tile_render_ms=4.0,
        cpu_render_prep_ms=2.0,
        cpu_framework_ms=3.0,
        render_cpu_ms=3.0,
        present_wait_cpu_ms=1.0,
    )
    delta, residual = reconcile_cpu_balance(frame)
    assert delta is not None
    assert residual is not None
    assert abs(delta) < 0.05
    assert residual == 0.0
    assert cpu_attributed_ms(frame) == 40.0


def test_cpu_balance_negative_delta_exported() -> None:
    frame = _frame_metrics(
        cpu_full_frame_ms=10.0,
        frame_ms=20.0,
        render_cpu_ms=1.0,
    )
    delta, residual = reconcile_cpu_balance(frame)
    assert delta is not None and delta < 0.0
    assert residual == 0.0


def test_classify_stream_burst_pool_idle_refresh() -> None:
    frame = FrameRecord(
        frame_index=20,
        frame_ms=42.0,
        stream_ms=38.0,
        stream_apply_ms=33.0,
        stream_unload_ms=0.0,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=16,
        focus_x=2048.0,
        focus_y=2048.0,
        zoom=0.35,
        cpu_full_frame_ms=50.0,
        apply_pool_ms=10.0,
        extra={
            "apply_pool_idle_refresh": 1,
            "apply_pool_poll_ms": 8.0,
        },
    )
    assert is_burst_frame(frame)
    assert classify_stream_burst(frame) == "pool_idle_refresh"


def test_classify_stream_burst_poll_collect() -> None:
    frame = FrameRecord(
        frame_index=3,
        frame_ms=15.0,
        stream_ms=10.0,
        stream_apply_ms=8.0,
        stream_unload_ms=0.0,
        stream_loaded=1,
        stream_unloaded=0,
        chunk_count=16,
        focus_x=0.0,
        focus_y=0.0,
        zoom=0.35,
        apply_pool_ms=7.0,
        extra={"apply_pool_poll_ms": 6.0},
    )
    assert classify_stream_burst(frame) == "pool_poll_collect"


def test_build_stream_burst_table_has_both_time_domains() -> None:
    frames = [
        FrameRecord(
            frame_index=20,
            frame_ms=42.334,
            stream_ms=37.941,
            stream_apply_ms=33.484,
            stream_unload_ms=0.0,
            stream_loaded=0,
            stream_unloaded=0,
            chunk_count=16,
            focus_x=2048.0,
            focus_y=2048.0,
            zoom=0.35,
            cpu_full_frame_ms=48.0,
            apply_pool_ms=33.0,
            extra={"apply_pool_poll_ms": 30.0},
        )
    ]
    table = build_stream_burst_table(frames)
    assert len(table) == 1
    row = table[0]
    assert row["canonical_tick_ms"] == 42.334
    assert row["cpu_full_frame_ms"] == 48.0
    assert "burst_cause_id" in row


def test_build_cpu_balance_from_frames() -> None:
    frames = [
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
            cpu_full_frame_ms=30.0,
            extra={
                "cpu_input_ms": 1.0,
                "cpu_residual_ms": 2.0,
                "cpu_balance_delta_ms": 0.01,
            },
        )
        for i in range(30)
    ]
    balance = build_cpu_balance(frames)
    assert "phases" in balance
    assert balance["phases"]["canonical_tick_ms"]["mean"] == 10.0
    assert "cpu_balance_delta_ms" in balance


def test_phase_ms_buckets_m25c() -> None:
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
        render_cpu_ms=1.0,
        extra={
            "cpu_input_ms": 1.0,
            "cpu_sim_ms": 5.0,
            "cpu_residual_ms": 2.0,
        },
    )
    buckets = phase_ms_buckets(frame)
    assert buckets["canonical_tick"] == 10.0
    assert buckets["cpu_input"] == 1.0
    assert buckets["cpu_sim"] == 5.0


def test_gate_cpu_balance_delta() -> None:
    frames = [
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
            cpu_full_frame_ms=30.0,
            extra={"cpu_balance_delta_ms": 0.01},
        )
        for i in range(50)
    ]
    ok, _msg = gate_perf_run.gate_cpu_balance_delta_p95_max_ms(frames, max_ms=0.05)
    assert ok


def test_loader_backward_compat_old_run() -> None:
    run_dir = (
        __import__("pathlib").Path(__file__).resolve().parents[1]
        / "docs/benchmarks/perf/runs/20260714T084714Z_demo_a9aaa9e"
    )
    loaded = load_run(run_dir)
    assert loaded.frames
    assert "cpu_full_frame_ms" in loaded.optional_fields


def test_session_exports_balance_fields() -> None:
    config = load_profiling_config()
    session = PerfSession(config=config, scenario_id="steady", run_mode="test", extract_enabled=True)
    session.full_frame_enabled = True
    session._warmup_frames = 0
    session.begin_full_frame()
    session.record_full_frame_phase("cpu_input_ms", 1.0)
    session.record_full_frame_phase("cpu_framework_pre_tick_ms", 0.5)
    session.record_app_phase("cpu_sim_ms", 2.0)
    frame = session.run_canonical_tick(
        _DummyCallbacks(), focus_x=0.0, focus_y=0.0, zoom=1.0, move_dx=0.0, move_dy=0.0
    )
    assert frame is not None
    session.record_full_frame_phase("cpu_framework_post_tick_ms", 3.0)
    full_ms = session.end_full_frame()
    finalized = session.finalize_pending_frame(cpu_full_frame_ms=full_ms)
    assert finalized is not None
    assert finalized.cpu_balance_delta_ms is not None
    assert finalized.cpu_measurement_residual_ms is not None
    assert finalized.cpu_framework_pre_tick_ms is not None


def test_attribution_version_is_4() -> None:
    assert ATTRIBUTION_VERSION == 4
