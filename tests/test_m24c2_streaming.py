"""Tests — M24c.2 Streaming-Scheduler & Combined Worker."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from game_core.chunk_gen_pool import ChunkGenPool, _JobState
from game_core.chunk_stage import DecoResult, TerrainResult
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.collision_grid import CHUNK_SOLID_GRID_BYTES
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


def _deco_result(coord: tuple[int, int]) -> DecoResult:
    key = _build_key(coord)
    return DecoResult(
        build_key=key,
        placements=(),
        solid_grid=b"\x00" * CHUNK_SOLID_GRID_BYTES,
    )


def _make_pool() -> ChunkGenPool:
    return ChunkGenPool(WorldGenContext.from_active(), workers=1)


def test_terrain_submit_list_is_filtered() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=2,
        unload_radius=4,
        max_applies_per_frame=4,
        max_sync_applies_per_frame=0,
        sync_fallback_only_when_pool_disabled=True,
        pipeline_mode="split",
    )
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.coordinator = _make_pool().coordinator
    pool.poll_terrain_ready.return_value = []
    pool.poll_deco_ready.return_value = []
    pool.terrain_in_flight_count.return_value = 0
    pool.terrain_running_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.is_in_flight.return_value = False
    pool.has_ready_results.return_value = False
    pool.submit_terrain.return_value = []
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=pool):
        streamer.update(world, 0.0, 0.0, content, collision, extractor, step_metrics=metrics)
    pool.submit_terrain.assert_called_once()
    submitted_coords = pool.submit_terrain.call_args[0][0]
    assert isinstance(submitted_coords, list)


def test_sync_blocked_when_coord_submitted_this_step() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=2,
        unload_radius=4,
        max_applies_per_frame=4,
        max_sync_applies_per_frame=0,
        sync_fallback_only_when_pool_disabled=True,
        pipeline_mode="combined",
    )
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.coordinator = _make_pool().coordinator
    key = pool.coordinator.next_terrain_build_key((1, 0))
    pool.poll_terrain_ready.return_value = []
    pool.poll_deco_ready.return_value = []
    pool.terrain_in_flight_count.return_value = 0
    pool.terrain_running_count.return_value = 0
    pool.deco_in_flight_count.return_value = 0
    pool.has_pending_result.return_value = False
    pool.is_in_flight.return_value = False
    pool.has_ready_results.return_value = False
    pool.submit_chunk_pipeline.return_value = [key]
    metrics = StreamStepMetrics()
    with patch.object(streamer, "ensure_chunk_gen_pool", return_value=pool):
        with patch.object(streamer, "_load_chunk") as load_chunk:
            streamer.update(world, 0.0, 0.0, content, collision, extractor, step_metrics=metrics)
    assert load_chunk.call_count == 0
    assert metrics.sync_skipped_worker_submitted > 0


def test_combined_pipeline_populates_both_ready_queues() -> None:
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
    pool = ChunkGenPool(WorldGenContext.from_active(), workers=2)
    coord = (-777, -777)
    keys = pool.submit_chunk_pipeline(
        [coord],
        max_in_flight=4,
        parallelism_cap=2,
    )
    assert len(keys) == 1
    build_key = keys[0]
    deadline = __import__("time").perf_counter() + 60.0
    while __import__("time").perf_counter() < deadline:
        pool.poll_terrain_ready()
        pool.poll_deco_ready()
        if build_key in pool._terrain_ready and build_key in pool._deco_ready:
            break
        __import__("time").sleep(0.05)
    assert build_key in pool._terrain_ready
    assert build_key in pool._deco_ready
    terrain, deco = pool._terrain_ready[build_key], pool._deco_ready[build_key]
    assert terrain.coord == coord
    assert deco.coord == coord
    pool.shutdown()


def test_pipeline_task_returns_pair() -> None:
    from dataclasses import replace

    from game_core.world_gen import configure_world_gen, get_world_gen_config
    from game_core.world_gen_parallel import (
        _generate_chunk_pipeline_task,
        _pool_worker_init,
        shutdown_parallel_pool,
    )

    shutdown_parallel_pool()
    config = replace(get_world_gen_config(), parallel_prefetch=True, parallel_workers=1)
    configure_world_gen(config)
    from game_core.world_gen import get_biomes_config

    _pool_worker_init(config, get_biomes_config())
    key = _build_key((2, 2))
    terrain, deco = _generate_chunk_pipeline_task(key)
    assert terrain.coord == (2, 2)
    assert deco.coord == (2, 2)
    shutdown_parallel_pool()


def test_warmup_combined_pipeline() -> None:
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
    config = StreamingConfig(pipeline_mode="combined")
    streamer = ChunkStreamer(config=config)
    try:
        assert streamer.warmup_chunk_gen_pool(coord=(-666, -666), timeout_s=60.0)
    finally:
        streamer.shutdown_chunk_gen_pool()
