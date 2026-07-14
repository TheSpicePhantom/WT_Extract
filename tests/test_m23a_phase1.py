"""Tests — M23a Phase 1: Pending-Queue, Mark, Revive, Ghost-Semantik."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, World
from game_core.world_gen import generate_chunk


def _setup() -> tuple[ChunkStreamer, World, object, object, MagicMock]:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=2,
        unload_radius=3,
        max_applies_per_frame=0,
    )
    streamer = ChunkStreamer(config=config)
    return streamer, world, content, collision, extractor


def test_mark_removes_from_world_chunks() -> None:
    streamer, world, content, collision, extractor = _setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    initial = world.chunk_count
    assert initial > 0
    far_x = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, 0.0, content, collision, extractor)
    assert (0, 0) not in world.chunks
    assert streamer.pending_unload.count() > 0


def test_revive_before_load() -> None:
    streamer, world, content, collision, extractor = _setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    original_count = world.chunk_count
    assert (0, 0) in world.chunks
    original_tile = world.get_tile(4, 4)

    config = streamer.config
    streamer2 = ChunkStreamer(
        config=StreamingConfig(
            mode="radius",
            load_radius=2,
            unload_radius=3,
            max_applies_per_frame=0,
        )
    )
    streamer2.update(world, 0.0, 0.0, content, collision, extractor)
    far_x = 40 * CHUNK_SIZE_PX
    streamer2.update(world, far_x, 0.0, content, collision, extractor)
    assert (0, 0) not in world.chunks
    assert streamer2.pending_unload.contains((0, 0))

    streamer2.update(world, 0.0, 0.0, content, collision, extractor)
    assert (0, 0) in world.chunks
    assert world.get_tile(4, 4) == original_tile


def test_pending_not_in_chunk_count() -> None:
    streamer, world, content, collision, extractor = _setup()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.chunks[(1, 0)] = generate_chunk(1, 0)
    assert world.chunk_count == 2
    streamer._mark_pending_unload(world, (0, 0), extractor)
    assert world.chunk_count == 1
    assert streamer.pending_unload.contains((0, 0))


def test_ghost_deco_not_queryable_when_pending() -> None:
    streamer, world, content, collision, extractor = _setup()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(2, 2, "trees/oak", procedural=True)
    streamer._mark_pending_unload(world, (0, 0), extractor)
    assert world.decoration_at_tile(2, 2) is None


def test_unmodified_drain_no_delta() -> None:
    streamer, world, content, collision, extractor = _setup()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    streamer._mark_pending_unload(world, (0, 0), extractor)
    streamer._drain_pending(world, max_count=0)
    assert (0, 0) not in streamer.persistent_deltas
    assert not streamer.pending_unload.contains((0, 0))


def test_modified_drain_creates_delta() -> None:
    streamer, world, content, collision, extractor = _setup()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.set_tile(1, 1, "wt:tiles/stone")
    streamer._mark_pending_unload(world, (0, 0), extractor)
    streamer._drain_pending(world, max_count=0)
    assert (0, 0) in streamer.persistent_deltas
