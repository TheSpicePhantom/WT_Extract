"""Tests — Chunk-Streaming (M18)."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.chunk_streaming import ChunkStreamer, coords_in_radius, focus_to_chunk
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.stream_view import StreamViewParams
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, CHUNK_SIZE_TILES, TILE_SIZE_PX, World
from game_core.world_gen import (
    generate_chunk,
    populate_chunk_decorations,
    remove_decorations_in_chunk,
    remove_procedural_decorations_in_chunk,
)


def _streamer_setup(*, mode: str = "radius") -> tuple[ChunkStreamer, World, object, object, MagicMock]:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode=mode,
        load_radius=8,
        unload_radius=10,
        max_applies_per_frame=0,
        max_unloads_per_frame=0,
    )
    streamer = ChunkStreamer(config=config)
    return streamer, world, content, collision, extractor


def test_load_radius() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    expected = len(coords_in_radius((0, 0), 8))
    assert world.chunk_count == expected
    assert world.chunk_count == 17 * 17


def test_unload_distant_chunks() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert (0, 0) in world.chunks

    far_x = 40 * CHUNK_SIZE_PX
    far_y = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, far_y, content, collision, extractor)
    assert (0, 0) not in world.chunks
    center = focus_to_chunk(far_x, far_y)
    assert center in world.chunks


def test_deterministic_chunk_decorations() -> None:
    content = load_content_registry()
    if not content.decorations:
        return

    world_a = World()
    world_b = World()
    world_a.chunks[(0, 0)] = generate_chunk(0, 0)
    world_b.chunks[(0, 0)] = generate_chunk(0, 0)
    populate_chunk_decorations(world_a, content, 0, 0)
    populate_chunk_decorations(world_b, content, 0, 0)

    ids_a = [placed.decoration_id for placed in world_a.decorations]
    ids_b = [placed.decoration_id for placed in world_b.decorations]
    assert ids_a == ids_b
    assert ids_a


def test_unload_removes_decorations() -> None:
    content = load_content_registry()
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    if not content.decorations:
        return
    world.place_decoration(1, 1, content.decorations[0].id)
    assert len(world.decorations) == 1

    remove_decorations_in_chunk(world, (0, 0))
    assert len(world.decorations) == 0


def test_invalidate_on_unload() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    extractor.reset_mock()

    far_x = 40 * CHUNK_SIZE_PX
    far_y = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, far_y, content, collision, extractor)
    assert extractor.invalidate.call_count > 0


def test_loaded_chunk_has_solid_grid() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    chunk = world.chunks[(0, 0)]
    assert chunk.solid_grid is not None


def test_dirty_chunk_persisted_on_unload() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    from game_core.chunk_delta import apply_terrain_delta
    from game_core.world_gen import KEY_STONE, generate_chunk

    world.set_tile(4, 4, KEY_STONE)
    assert (0, 0) in world.dirty_chunks

    far_x = 40 * CHUNK_SIZE_PX
    far_y = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, far_y, content, collision, extractor)
    assert streamer.pending_unload.contains((0, 0)) or (0, 0) in streamer.persistent_deltas

    for _ in range(30):
        if (0, 0) in streamer.persistent_deltas:
            break
        streamer.update(world, far_x, far_y, content, collision, extractor)

    assert (0, 0) in streamer.persistent_deltas
    baseline = generate_chunk(0, 0)
    restored = apply_terrain_delta(baseline, streamer.persistent_deltas[(0, 0)])
    assert restored.get_key(4, 4) == KEY_STONE


def test_override_used_on_reload() -> None:
    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    from game_core.world_gen import KEY_STONE

    world.set_tile(2, 2, KEY_STONE)
    streamer._flush_modified_chunk(world, (0, 0))
    world.chunks.pop((0, 0))
    streamer._decorated_chunks.discard((0, 0))

    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert world.chunks[(0, 0)].get_key(2, 2) == KEY_STONE


def test_reload_after_unload_restores_procedural_decorations() -> None:
    content = load_content_registry()
    if not content.decorations:
        return

    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    deco_count_loaded = len(world.decorations)
    assert deco_count_loaded > 0

    far_x = 40 * CHUNK_SIZE_PX
    far_y = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, far_y, content, collision, extractor)
    # Same-Frame-Marks werden beim Drain übersprungen (M23a) — zweiter Tick räumt auf.
    streamer.update(world, far_x, far_y, content, collision, extractor)
    assert len(world.decorations) < deco_count_loaded

    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert (0, 0) in world.chunks
    wx_min, wx_max = 0, CHUNK_SIZE_TILES - 1
    wy_min, wy_max = 0, CHUNK_SIZE_TILES - 1
    origin_deco = [
        placed
        for placed in world.decorations
        if placed.procedural
        and wx_min <= int(placed.world_x // TILE_SIZE_PX) <= wx_max
        and wy_min <= int(placed.world_y // TILE_SIZE_PX) <= wy_max
    ]
    assert len(origin_deco) > 0


def test_override_reload_restores_procedural_decorations() -> None:
    content = load_content_registry()
    if not content.decorations:
        return

    streamer, world, content, collision, extractor = _streamer_setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    baseline_deco = len(world.decorations)
    assert baseline_deco > 0

    from game_core.world_gen import KEY_STONE

    world.set_tile(2, 2, KEY_STONE)
    streamer._flush_modified_chunk(world, (0, 0))
    world.chunks.pop((0, 0))
    streamer._decorated_chunks.discard((0, 0))
    remove_procedural_decorations_in_chunk(world, (0, 0))

    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert world.chunks[(0, 0)].get_key(2, 2) == KEY_STONE
    chunk_deco = sum(
        1
        for placed in world.decorations
        if 0 <= int(placed.world_x) < CHUNK_SIZE_TILES * TILE_SIZE_PX
        and 0 <= int(placed.world_y) < CHUNK_SIZE_TILES * TILE_SIZE_PX
    )
    assert chunk_deco > 0


def test_steady_update_does_not_rebuild_all_solids() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=1,
        unload_radius=2,
        max_applies_per_frame=0,
        max_unloads_per_frame=0,
    )
    streamer = ChunkStreamer(config=config)
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    world.collision_dirty_chunks.clear()

    rebuild_calls = 0
    original = world.rebuild_chunk_solid

    def counting_rebuild(coord, content_arg, collision_arg):
        nonlocal rebuild_calls
        rebuild_calls += 1
        return original(coord, content_arg, collision_arg)

    world.rebuild_chunk_solid = counting_rebuild  # type: ignore[method-assign]
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert rebuild_calls == 0


def test_procedural_deco_removed_user_deco_kept() -> None:
    content = load_content_registry()
    if not content.decorations:
        return

    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    deco_id = content.decorations[0].id
    world.place_decoration(1, 1, deco_id, procedural=True)
    world.place_decoration(2, 2, deco_id, procedural=False)

    remove_procedural_decorations_in_chunk(world, (0, 0))
    assert len(world.decorations) == 1
    assert world.decorations[0].procedural is False


def test_hybrid_loads_fewer_chunks_than_radius() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    view = StreamViewParams(
        focus_x=float(CHUNK_SIZE_PX),
        focus_y=float(CHUNK_SIZE_PX),
        player_x=float(CHUNK_SIZE_PX),
        player_y=float(CHUNK_SIZE_PX),
        zoom=0.35,
        viewport_w=1280,
        viewport_h=720,
    )
    hybrid = ChunkStreamer(
        config=StreamingConfig(mode="hybrid", max_applies_per_frame=0),
    )
    hybrid.update(world, float(CHUNK_SIZE_PX), float(CHUNK_SIZE_PX), content, collision, extractor, view=view)
    hybrid.shutdown_chunk_gen_pool()
    assert world.chunk_count < 17 * 17
    assert world.chunk_count > 0
