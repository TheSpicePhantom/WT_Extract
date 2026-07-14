"""Tests — M24b Pipeline-Vertrag (Failure-Modes)."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock

import pytest

from game_core.chunk_build import (
    BuildCoordinator,
    BuildKey,
    ChunkBuildState,
    DecoState,
    TerrainState,
    terrain_config_version,
)
from game_core.chunk_build_guards import (
    can_apply_deco_result,
    can_apply_terrain_result,
    submit_deco_allowed,
)
from game_core.chunk_build import deco_config_version
from game_core.chunk_gen_pool import ChunkGenPool
from game_core.chunk_stage import (
    DecoResult,
    TerrainResult,
    apply_deco_stage,
    apply_terrain_stage,
)
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.streaming_config import StreamingConfig
from game_core.world import World
from game_core.collision_grid import CHUNK_SOLID_GRID_BYTES


def _build_key(coord: tuple[int, int], revision: int = 1, epoch: int = 0) -> BuildKey:
    return BuildKey(
        coord=coord,
        terrain_revision=revision,
        terrain_config_version=terrain_config_version(),
        deco_config_version=deco_config_version(),
        build_epoch=epoch,
    )


def _terrain_result(coord: tuple[int, int], revision: int = 1, epoch: int = 0) -> TerrainResult:
    key = _build_key(coord, revision, epoch)
    return TerrainResult(build_key=key, layer0=(0,) * 4096, layer1=(0,) * 4096)


def _deco_result(key: BuildKey) -> DecoResult:
    return DecoResult(
        build_key=key,
        placements=(),
        solid_grid=b"\x00" * CHUNK_SOLID_GRID_BYTES,
    )


class _MockStreamer:
    pending_unload = MagicMock()
    persistent_deltas: dict = {}
    persistent_overrides: dict = {}

    def __init__(self) -> None:
        self.pending_unload.contains.return_value = False


def test_terrain_before_deco_applyable() -> None:
    content = load_content_registry()
    world = World()
    streamer = _MockStreamer()
    coordinator = BuildCoordinator()
    build_state = ChunkBuildState()
    result = _terrain_result((0, 0))
    build_state.pending_terrain_build_key = result.build_key
    assert can_apply_terrain_result(world, streamer, result, build_state, coordinator)
    apply_terrain_stage(world, result, content, build_state)
    assert build_state.terrain_state == TerrainState.APPLIED


def test_deco_discard_on_build_key_mismatch() -> None:
    world = World()
    streamer = _MockStreamer()
    coordinator = BuildCoordinator()
    build_state = ChunkBuildState()
    terrain = _terrain_result((0, 0), revision=1)
    build_state.terrain_build_key = terrain.build_key
    build_state.terrain_state = TerrainState.APPLIED
    world.chunks[(0, 0)] = MagicMock()
    stale = _deco_result(_build_key((0, 0), revision=0))
    assert not can_apply_deco_result(world, streamer, stale, build_state, coordinator)


def test_deco_suppressed_on_dirty() -> None:
    world = World()
    world.dirty_chunks.add((0, 0))
    streamer = _MockStreamer()
    build_state = ChunkBuildState()
    build_state.terrain_state = TerrainState.APPLIED
    build_state.terrain_build_key = _build_key((0, 0))
    world.chunks[(0, 0)] = MagicMock()
    assert not submit_deco_allowed(
        world,
        streamer,
        (0, 0),
        build_state,
        wanted=True,
        in_flight_room=True,
        visible_terrain_pending=0,
    )


def test_deco_only_after_terrain_applied() -> None:
    world = World()
    streamer = _MockStreamer()
    build_state = ChunkBuildState()
    build_state.terrain_state = TerrainState.IN_FLIGHT
    assert not submit_deco_allowed(
        world,
        streamer,
        (0, 0),
        build_state,
        wanted=True,
        in_flight_room=True,
        visible_terrain_pending=0,
    )


def test_terrain_stale_after_resubmit() -> None:
    world = World()
    streamer = _MockStreamer()
    coordinator = BuildCoordinator()
    build_state = ChunkBuildState()
    stale_key = coordinator.next_terrain_build_key((0, 0))
    stale = replace(_terrain_result((0, 0), revision=1, epoch=0), build_key=stale_key)
    key_new = coordinator.next_terrain_build_key((0, 0))
    build_state.pending_terrain_build_key = key_new
    assert not can_apply_terrain_result(world, streamer, stale, build_state, coordinator)


def test_terrain_stale_after_epoch_bump() -> None:
    world = World()
    streamer = _MockStreamer()
    coordinator = BuildCoordinator()
    coordinator.bump_epoch()
    build_state = ChunkBuildState()
    stale = _terrain_result((0, 0), revision=1, epoch=0)
    build_state.pending_terrain_build_key = stale.build_key
    assert not can_apply_terrain_result(world, streamer, stale, build_state, coordinator)


def test_duplicate_deco_apply_discarded() -> None:
    from game_core.world import Chunk
    from game_core.world_gen import KEY_GRASS

    content = load_content_registry()
    world = World()
    streamer = _MockStreamer()
    coordinator = BuildCoordinator()
    key = _build_key((0, 0))
    build_state = ChunkBuildState()
    build_state.terrain_build_key = key
    build_state.terrain_state = TerrainState.APPLIED
    world.chunks[(0, 0)] = Chunk.from_terrain((0, 0), [KEY_GRASS] * 4096, [KEY_GRASS] * 4096)
    deco = _deco_result(key)
    assert can_apply_deco_result(world, streamer, deco, build_state, coordinator)
    apply_deco_stage(world, deco, content, build_state)
    assert not can_apply_deco_result(world, streamer, deco, build_state, coordinator)


def test_build_epoch_only_from_coordinator() -> None:
    coord = BuildCoordinator()
    assert coord.read_build_epoch() == 0
    key = coord.next_terrain_build_key((1, 1))
    assert key.build_epoch == 0
    coord.bump_epoch()
    assert coord.read_build_epoch() == 1
    key2 = coord.next_terrain_build_key((1, 1))
    assert key2.build_epoch == 1
    assert key2.terrain_revision == 1


def test_visible_terrain_pending_blocks_deco_submit() -> None:
    world = World()
    streamer = _MockStreamer()
    cs = ChunkStreamer(config=StreamingConfig(mode="radius"))
    cs._build_tracker.get((0, 0)).terrain_state = TerrainState.EMPTY
    assert cs._visible_terrain_pending({(0, 0)}) == 1
    build_state = cs._build_tracker.get((0, 0))
    build_state.terrain_build_key = _build_key((0, 0))
    build_state.terrain_state = TerrainState.APPLIED
    world.chunks[(0, 0)] = MagicMock()
    assert not submit_deco_allowed(
        world,
        streamer,
        (0, 0),
        build_state,
        wanted=True,
        in_flight_room=True,
        visible_terrain_pending=1,
    )


def test_deco_incomplete_revive_flow() -> None:
    from game_core.pending_unload import PendingUnloadEntry
    from game_core.persistenz import PersistenzFlags
    from game_core.world import Chunk

    from game_core.world_gen import KEY_GRASS

    world = World()
    streamer = ChunkStreamer(config=StreamingConfig(mode="radius"))
    chunk = Chunk.from_terrain((0, 0), [KEY_GRASS] * 4096, [KEY_GRASS] * 4096)
    entry = PendingUnloadEntry(
        coord=(0, 0),
        snapshot=chunk,
        persistenz_flags=PersistenzFlags(0),
        deco_incomplete=True,
    )
    streamer.pending_unload.mark(entry)
    assert streamer._revive_pending(world, (0, 0))
    bs = streamer._build_tracker.get((0, 0))
    assert bs.deco_incomplete is True
    assert bs.deco_state == DecoState.NONE


def test_router_discards_stale_terrain() -> None:
    content = load_content_registry()
    world = World()
    config = StreamingConfig(mode="radius", max_applies_per_frame=0)
    streamer = ChunkStreamer(config=config)
    pool = MagicMock(spec=ChunkGenPool)
    pool.coordinator = BuildCoordinator()
    stale_key = pool.coordinator.next_terrain_build_key((0, 0))
    stale = replace(_terrain_result((0, 0), revision=1), build_key=stale_key)
    key_new = pool.coordinator.next_terrain_build_key((0, 0))
    streamer._build_tracker.get((0, 0)).pending_terrain_build_key = key_new
    pool.poll_terrain_ready.return_value = [stale]
    pool.poll_deco_ready.return_value = []
    from game_core.perf.models import StreamStepMetrics

    metrics = StreamStepMetrics()
    loaded, _ = streamer._route_pool_results(
        pool,
        world,
        content,
        {(0, 0)},
        budget=0,
        unlimited=True,
        step_metrics=metrics,
    )
    assert loaded == 0
    assert metrics.terrain_discarded_stale == 1
    pool.discard_terrain.assert_called_once()
