"""Tests — M23d Chunk-Render-Batching."""

from __future__ import annotations

from bridge.chunk_extractor import ChunkRenderExtractor
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


def _frame_signature(frame) -> tuple:
    parts: list[tuple] = []
    for chunk in frame.tile_chunks:
        for layer in chunk.layers:
            parts.append(
                (
                    chunk.chunk_coord,
                    int(layer.layer),
                    layer.tile_ids,
                    layer.world_x,
                    layer.world_y,
                )
            )
    return tuple(parts)


def test_batch_and_legacy_paths_match() -> None:
    world = _world_with_chunks(((0, 0), (1, 0)))
    camera = _camera_at(0, 0, zoom=0.5)
    batch_extractor = ChunkRenderExtractor(world, _catalog(), extract_mode="batch")
    legacy_extractor = ChunkRenderExtractor(world, _catalog(), extract_mode="per_chunk")
    assert _frame_signature(batch_extractor.extract(camera)) == _frame_signature(
        legacy_extractor.extract(camera)
    )


def test_registry_hit_after_warmup() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)
    metrics = ExtractStepMetrics()

    extractor.extract(camera, step_metrics=metrics)
    metrics.reset()
    extractor.extract(camera, step_metrics=metrics)

    assert metrics.tile_registry_hits >= 1
    assert metrics.tile_registry_misses == 0
    assert metrics.tile_cache_hits == 1


def test_cull_cache_hit_on_repeated_camera() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0, zoom=8.0)
    metrics = ExtractStepMetrics()

    extractor.extract(camera, step_metrics=metrics)
    metrics.reset()
    extractor.extract(camera, step_metrics=metrics)

    assert metrics.tile_cull_cache_hits >= 1
    assert metrics.tile_cull_cache_misses == 0


def test_invalidate_clears_registry_and_cull() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0, zoom=8.0)

    extractor.extract(camera)
    assert extractor._batch_registry
    assert extractor._cull_cache
    extractor.invalidate((0, 0))
    assert not any(key[0] == (0, 0) for key in extractor._batch_registry)
    assert not any(key[0] == (0, 0) for key in extractor._cull_cache)


def test_dirty_rebuilds_only_affected_layer() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)

    extractor.extract(camera)
    world.set_tile(0, 0, KEY_STONE, layer=0)
    metrics = ExtractStepMetrics()
    extractor.extract(camera, step_metrics=metrics)

    assert metrics.tile_registry_misses == 1
    assert (0, 0, 0) not in extractor._batch_registry or (0, 0, 0) in extractor._registry_empty


def test_batching_metrics_zero_overhead_without_profile() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    camera = _camera_at(0, 0)
    frame = extractor.extract(camera)
    assert len(frame.tile_chunks) == 1
