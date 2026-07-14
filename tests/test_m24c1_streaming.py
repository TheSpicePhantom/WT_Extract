"""Tests — M24c.1 Streaming-Integrationsfixes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from game_core.chunk_gen_pool import ChunkGenPool, _JobState
from game_core.chunk_stage import TerrainResult
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.models import StreamStepMetrics
from game_core.streaming_config import StreamingConfig
from game_core.world import World
from game_core.world_gen_context import WorldGenContext


def _build_key(coord: tuple[int, int], revision: int = 1) -> object:
    from game_core.chunk_build import BuildKey, deco_config_version, terrain_config_version

    return BuildKey(
        coord=coord,
        terrain_revision=revision,
        terrain_config_version=terrain_config_version(),
        deco_config_version=deco_config_version(),
        build_epoch=0,
    )


def _terrain_result(coord: tuple[int, int]) -> TerrainResult:
    key = _build_key(coord)
    return TerrainResult(build_key=key, layer0=(0,) * 4096, layer1=(0,) * 4096)


def _make_pool() -> ChunkGenPool:
    return ChunkGenPool(WorldGenContext.from_active(), workers=1)


def test_is_terrain_in_flight_includes_ready() -> None:
    pool = _make_pool()
    key = pool.coordinator.next_terrain_build_key((3, 3))
    pool._terrain_states[key] = _JobState.READY
    assert pool.is_terrain_in_flight((3, 3))
    assert not pool.is_terrain_in_flight((4, 4))


def test_is_deco_in_flight_includes_ready() -> None:
    pool = _make_pool()
    key = _build_key((7, 7))
    pool._deco_states[key] = _JobState.READY
    assert pool.is_deco_in_flight((7, 7))


def test_has_pending_result() -> None:
    pool = _make_pool()
    coord = (2, 2)
    key = pool.coordinator.next_terrain_build_key(coord)
    pool._terrain_ready[key] = _terrain_result(coord)
    assert pool.has_pending_result(coord)


def test_is_in_flight_covers_terrain_and_deco() -> None:
    pool = _make_pool()
    terrain_key = pool.coordinator.next_terrain_build_key((1, 0))
    deco_key = _build_key((0, 1))
    pool._terrain_states[terrain_key] = _JobState.RUNNING
    pool._deco_states[deco_key] = _JobState.SUBMITTED
    assert pool.is_in_flight((1, 0))
    assert pool.is_in_flight((0, 1))


def test_sync_fallback_not_triggered_when_pending_result() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=1,
        unload_radius=3,
        max_applies_per_frame=0,
        max_sync_applies_per_frame=4,
    )
    streamer = ChunkStreamer(config=config)
    pool = _make_pool()
    coord = (0, 0)
    key = pool.coordinator.next_terrain_build_key(coord)
    pool._terrain_ready[key] = _terrain_result(coord)
    pool._terrain_states[key] = _JobState.READY
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=pool):
        with patch.object(streamer, "_load_chunk") as load_chunk:
            streamer.update(world, 0.0, 0.0, content, collision, extractor, step_metrics=metrics)
    loaded_coords = [call.args[1] for call in load_chunk.call_args_list]
    assert coord not in loaded_coords


def test_sync_fallback_counter_on_last_resort() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=1,
        unload_radius=3,
        max_applies_per_frame=0,
        max_sync_applies_per_frame=4,
        sync_fallback_in_flight_ms=0.0,
    )
    streamer = ChunkStreamer(config=config)
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=None):
        with patch.object(streamer, "_load_chunk") as load_chunk:
            loaded, _ = streamer.update(
                world, 0.0, 0.0, content, collision, extractor, step_metrics=metrics
            )
    assert load_chunk.called
    assert metrics.sync_fallback_triggered >= 1
    assert loaded >= 1


def test_warmup_exercises_terrain_and_deco_pipeline() -> None:
    from dataclasses import replace

    from game_core.world_gen import configure_world_gen, get_world_gen_config
    from game_core.world_gen_parallel import resolve_worker_count, shutdown_parallel_pool

    shutdown_parallel_pool()
    configure_world_gen(
        replace(
            get_world_gen_config(),
            parallel_prefetch=True,
            parallel_workers=2,
        )
    )
    if resolve_worker_count(get_world_gen_config().parallel_workers) <= 0:
        pytest.skip("parallel_workers=0")
    streamer = ChunkStreamer()
    try:
        assert streamer.warmup_chunk_gen_pool(coord=(-888, -888), timeout_s=60.0)
    finally:
        streamer.shutdown_chunk_gen_pool()
