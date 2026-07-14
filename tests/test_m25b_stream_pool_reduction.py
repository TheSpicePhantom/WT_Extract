"""Tests — M25b Stream Pool Load/Apply FPS-Killer Reduktion."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from game_core.chunk_gen_pool import ChunkGenPool
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.models import StreamStepMetrics
from game_core.perf.run_analysis.diagnose import build_stream_pool_breakdown
from game_core.perf.run_analysis.models import FrameRecord
from game_core.stream_view import StreamViewParams
from game_core.streaming_config import StreamingConfig
from game_core.world import World
from game_core.world_gen import generate_chunk
from tools import gate_perf_run


def _steady_view() -> StreamViewParams:
    return StreamViewParams(
        focus_x=2048.0,
        focus_y=2048.0,
        player_x=2048.0,
        player_y=2048.0,
        zoom=0.35,
        viewport_w=1280,
        viewport_h=720,
        move_dx=0.0,
        move_dy=0.0,
    )


def _frame(
    frame_index: int,
    *,
    cpu_full: float = 25.0,
    pool: float = 8.0,
    pool_poll: float = 3.0,
    route_passes: int = 1,
    idle_skip: int = 1,
) -> FrameRecord:
    return FrameRecord(
        frame_index=frame_index,
        frame_ms=cpu_full * 0.5,
        stream_ms=pool,
        stream_apply_ms=pool,
        stream_unload_ms=0.0,
        stream_loaded=0,
        stream_unloaded=0,
        chunk_count=14,
        focus_x=2048.0,
        focus_y=2048.0,
        zoom=0.35,
        cpu_full_frame_ms=cpu_full,
        apply_pool_ms=pool,
        extra={
            "apply_pool_poll_ms": pool_poll,
            "apply_pool_route_passes": route_passes,
            "apply_pool_idle_skip": idle_skip,
        },
    )


def test_pool_idle_skip_eligible_when_steady() -> None:
    world = World()
    coord = (32, 32)
    world.chunks[coord] = generate_chunk(32, 32)
    config = StreamingConfig(
        mode="radius",
        load_radius=0,
        unload_radius=2,
        pool_idle_skip_enabled=True,
    )
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.terrain_in_flight_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.has_pending_result.return_value = False
    pool.has_ready_results.return_value = False
    wanted = {coord}
    assert streamer._pool_idle_skip_eligible(pool, wanted, _steady_view(), world)


def test_pool_idle_skip_not_eligible_on_movement() -> None:
    world = World()
    coord = (32, 32)
    world.chunks[coord] = generate_chunk(32, 32)
    streamer = ChunkStreamer()
    pool = MagicMock(spec=ChunkGenPool)
    pool.terrain_in_flight_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.has_pending_result.return_value = False
    pool.has_ready_results.return_value = False
    view = StreamViewParams(
        focus_x=2048.0,
        focus_y=2048.0,
        player_x=2048.0,
        player_y=2048.0,
        zoom=0.35,
        viewport_w=1280,
        viewport_h=720,
        move_dx=10.0,
        move_dy=0.0,
    )
    assert not streamer._pool_idle_skip_eligible(pool, {coord}, view, world)


def test_single_route_when_no_submit() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=0,
        unload_radius=2,
        pool_idle_skip_enabled=False,
        pipeline_mode="combined",
    )
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.coordinator = ChunkGenPool.__new__(ChunkGenPool)
    pool.poll_terrain_ready.return_value = []
    pool.poll_deco_ready.return_value = []
    pool.terrain_in_flight_count.return_value = 0
    pool.terrain_running_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.is_in_flight.return_value = False
    pool.has_ready_results.return_value = False
    pool.submit_chunk_pipeline.return_value = []
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=pool):
        streamer.update(
            world,
            2048.0,
            2048.0,
            content,
            collision,
            extractor,
            view=_steady_view(),
            step_metrics=metrics,
        )
    assert metrics.apply_pool_route_passes == 1


def test_second_route_only_after_submit() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=2,
        unload_radius=4,
        pool_idle_skip_enabled=False,
        pipeline_mode="combined",
    )
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.coordinator = ChunkGenPool.__new__(ChunkGenPool)
    key = MagicMock()
    key.coord = (99, 99)
    pool.poll_terrain_ready.return_value = []
    pool.poll_deco_ready.return_value = []
    pool.terrain_in_flight_count.return_value = 0
    pool.terrain_running_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.is_in_flight.return_value = False
    pool.has_ready_results.return_value = False
    pool.submit_chunk_pipeline.return_value = [key]
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=pool):
        streamer.update(world, 0.0, 0.0, content, collision, extractor, step_metrics=metrics)
    assert metrics.apply_pool_route_passes == 2
    assert metrics.terrain_submitted == 1


def test_stream_pool_breakdown() -> None:
    frames = [_frame(i) for i in range(20)]
    breakdown = build_stream_pool_breakdown(frames)
    assert "apply_pool_ms" in breakdown
    assert breakdown["apply_pool_poll_ms"]["mean"] == pytest.approx(3.0)
    assert breakdown["apply_pool_idle_skip_rate"] == pytest.approx(1.0)


def test_gate_stream_pool_p95_share_pass() -> None:
    frames = [_frame(i, cpu_full=20.0, pool=6.0) for i in range(50)]
    ok, msg = gate_perf_run.gate_stream_pool_p95_share(frames, max_share=0.40)
    assert ok, msg


def test_gate_stream_pool_p95_share_fail() -> None:
    frames = [_frame(i, cpu_full=20.0, pool=12.0) for i in range(50)]
    ok, _msg = gate_perf_run.gate_stream_pool_p95_share(frames, max_share=0.40)
    assert not ok
