"""Tests — Dirty-Chunk-Render-Cache (M17) + M23d Batch-Registry."""

from __future__ import annotations

from unittest.mock import patch

from bridge.chunk_extractor import ChunkRenderExtractor
from game_core.world import CHUNK_SIZE_PX, CHUNK_SIZE_TILES, CHUNK_TILE_COUNT, Chunk, World
from game_core.world_gen import KEY_GRASS, KEY_STONE
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import CameraData


def _catalog() -> SpriteCatalog:
    return SpriteCatalog(key_to_id={"wt:tiles/grass": 1, "wt:tiles/stone": 2})


def _camera_at(chunk_x: int, chunk_y: int, *, zoom: float = 0.5) -> CameraData:
    center_x = chunk_x * CHUNK_SIZE_PX + CHUNK_SIZE_PX * 0.5
    center_y = chunk_y * CHUNK_SIZE_PX + CHUNK_SIZE_PX * 0.5
    return CameraData(
        position_x=center_x,
        position_y=center_y,
        zoom=zoom,
        viewport_width=1280,
        viewport_height=720,
    )


def _world_with_chunks(coords: tuple[tuple[int, int], ...]) -> World:
    chunks: dict[tuple[int, int], Chunk] = {}
    for coord in coords:
        terrain = [KEY_GRASS] * CHUNK_TILE_COUNT
        chunks[coord] = Chunk.from_terrain(coord, terrain)
    return World(chunks=chunks)


def _tile_count(frame) -> int:
    return sum(
        len(layer.tile_ids)
        for chunk in frame.tile_chunks
        for layer in chunk.layers
    )


def test_cache_hit_avoids_rebuild() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    with patch.object(extractor, "_build_full_layer_batch", wraps=extractor._build_full_layer_batch) as rebuild:
        first = extractor.extract(camera)
        second = extractor.extract(camera)

    assert _tile_count(first) > 0
    assert _tile_count(second) == _tile_count(first)
    assert rebuild.call_count == 2


def test_dirty_tile_triggers_rebuild() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    extractor.extract(camera)
    world.set_tile(0, 0, KEY_STONE)

    with patch.object(extractor, "_build_full_layer_batch", wraps=extractor._build_full_layer_batch) as rebuild:
        frame = extractor.extract(camera)

    assert rebuild.call_count == 1
    cached = extractor._batch_registry[(0, 0), 0, 0]
    assert int(cached.tile_ids[0]) == 2
    assert _tile_count(frame) > 0


def test_off_screen_dirty_stays_lazy() -> None:
    world = _world_with_chunks(((0, 0), (5, 5)))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    extractor.extract(camera)
    world.set_tile(5 * CHUNK_SIZE_TILES, 5 * CHUNK_SIZE_TILES, KEY_STONE)
    assert (5, 5) in world.dirty_chunks

    with patch.object(extractor, "_build_full_layer_batch", wraps=extractor._build_full_layer_batch) as rebuild:
        extractor.extract(camera)

    assert rebuild.call_count == 0
    assert (5, 5) in world.dirty_chunks

    camera_far = _camera_at(5, 5)
    with patch.object(extractor, "_build_full_layer_batch", wraps=extractor._build_full_layer_batch) as rebuild:
        extractor.extract(camera_far)

    assert rebuild.call_count == 2
    assert (5, 5) not in world.dirty_chunks


def test_invalidate_all_forces_rebuild() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    extractor.extract(camera)
    extractor.invalidate_all()

    with patch.object(extractor, "_build_full_layer_batch", wraps=extractor._build_full_layer_batch) as rebuild:
        extractor.extract(camera)

    assert rebuild.call_count == 2


def test_set_world_clears_cache() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    extractor.extract(camera)
    assert ((0, 0), 0, 0) in extractor._batch_registry

    new_world = _world_with_chunks(((0, 0),))
    extractor.set_world(new_world)
    assert not extractor._batch_registry


def test_view_cull_reduces_visible_tiles() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    zoomed = _camera_at(0, 0, zoom=8.0)

    frame = extractor.extract(zoomed)
    full_batch = extractor._batch_registry[(0, 0), 0, 0]
    full_count = len(full_batch.tile_ids)
    visible_count = _tile_count(frame)

    assert full_count == CHUNK_TILE_COUNT
    assert visible_count < full_count
