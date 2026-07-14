"""Tests — M23c Extract-Microprofile und Cache-Vertrag."""

from __future__ import annotations

import time
from unittest.mock import patch

from bridge.chunk_extractor import ChunkRenderExtractor
from bridge.decoration_extractor import decorations_to_sprites
from game_core.perf.models import ExtractStepMetrics
from game_core.world import CHUNK_SIZE_PX, CHUNK_TILE_COUNT, Chunk, World
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


def test_extract_metrics_cache_hit_after_warmup() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)
    metrics = ExtractStepMetrics()

    extractor.extract(camera, step_metrics=metrics)
    metrics.reset()
    extractor.extract(camera, step_metrics=metrics)

    assert metrics.tile_visible_chunks == 1
    assert metrics.tile_cache_hits == 1
    assert metrics.tile_cache_misses == 0
    assert metrics.tile_full_rebuild_ms == 0.0


def test_extract_metrics_miss_on_dirty() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)
    metrics = ExtractStepMetrics()

    extractor.extract(camera, step_metrics=metrics)
    world.set_tile(0, 0, KEY_STONE)
    metrics.reset()
    extractor.extract(camera, step_metrics=metrics)

    assert metrics.tile_cache_misses == 1
    assert metrics.tile_full_rebuild_ms > 0.0


def test_extract_no_overhead_without_metrics() -> None:
    world = _world_with_chunks(((0, 0), (1, 0), (2, 0)))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(1, 0)

    with patch("bridge.chunk_extractor.time.perf_counter", side_effect=[0.0, 0.001] * 20):
        frame = extractor.extract(camera)

    assert len(frame.tile_chunks) >= 1


def test_invalidate_causes_miss_not_dirty_flag() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)
    metrics = ExtractStepMetrics()

    extractor.extract(camera, step_metrics=metrics)
    extractor.invalidate((0, 0))
    assert (0, 0) not in world.dirty_chunks

    metrics.reset()
    extractor.extract(camera, step_metrics=metrics)
    assert metrics.tile_cache_misses == 1


def test_deco_metrics_populated() -> None:
    world = _world_with_chunks(((0, 0),))
    metrics = ExtractStepMetrics()
    camera = _camera_at(0, 0)

    class _Content:
        @staticmethod
        def decoration_by_id(_decoration_id: str):
            return None

    decorations_to_sprites(_Content(), _catalog(), world, camera=camera, step_metrics=metrics)
    assert metrics.deco_scanned_count == 0
    assert metrics.deco_visible_count == 0


def test_materials_cache_reused() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    chunk = world.chunks[(0, 0)]

    batch_a = extractor._build_full_layer_batch(chunk, 0)
    batch_b = extractor._build_full_layer_batch(chunk, 0)
    assert batch_a is not None and batch_b is not None
    assert batch_a.materials is batch_b.materials
