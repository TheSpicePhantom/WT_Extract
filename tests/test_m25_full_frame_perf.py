"""Tests — M25 Full-Frame Profiling Contract."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.perf.config import load_profiling_config
from game_core.perf.models import ExtractStepMetrics, StreamStepMetrics
from game_core.perf.session import PerfSession, TickCallbacks


class _DummyCallbacks(TickCallbacks):
    def __init__(self) -> None:
        self._chunk_count = 0
        self._deco_sprite_count = 0

    def on_scenario_step(self, focus_x, focus_y, zoom, move_dx, move_dy) -> None:
        self._chunk_count = 1

    def on_stream_update(self, step_metrics: StreamStepMetrics) -> tuple[int, int]:
        return 0, 0

    def on_deco_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        return 0.0

    def on_tile_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        return 0.0

    @property
    def chunk_count(self) -> int:
        return self._chunk_count

    @property
    def deco_sprite_count(self) -> int:
        return self._deco_sprite_count


def test_full_frame_fields_present_when_enabled() -> None:
    config = load_profiling_config()
    session = PerfSession(config=config, scenario_id="steady", run_mode="test", extract_enabled=False)
    session.full_frame_enabled = True
    session._warmup_frames = 0

    cb = _DummyCallbacks()
    session.begin_full_frame()
    frame = session.run_canonical_tick(cb, focus_x=0.0, focus_y=0.0, zoom=1.0, move_dx=0.0, move_dy=0.0)
    assert frame is not None

    # Simuliere Renderer-Timings.
    session.record_render_timing("wait_fence_ms", 1.0)
    session.record_render_timing("acquire_ms", 2.0)
    session.record_render_timing("pre_render_ms", 3.0)
    session.record_render_timing("record_ms", 4.0)
    session.record_render_timing("submit_ms", 5.0)
    session.record_render_timing("present_ms", 6.0)

    full_ms = session.end_full_frame()
    finalized = session.finalize_pending_frame(cpu_full_frame_ms=full_ms)
    assert finalized is not None
    assert finalized.cpu_full_frame_ms is not None
    assert finalized.render_cpu_ms is not None
    assert finalized.present_wait_cpu_ms is not None
    assert finalized.render_wait_fence_ms == 1.0
    assert finalized.render_acquire_ms == 2.0
    assert finalized.render_pre_render_ms == 3.0
    assert finalized.render_record_ms is not None
    assert finalized.cpu_balance_delta_ms is not None
    assert finalized.cpu_residual_ms is not None
    assert finalized.cpu_scenario_ms is not None


