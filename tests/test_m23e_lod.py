"""Tests — M23e Visibility LOD / Map-Mode."""

from __future__ import annotations

from bridge.chunk_extractor import ChunkRenderExtractor
from game_core.perf.models import ExtractStepMetrics
from game_core.visibility_lod_config import LOD0, LOD1, LOD2, VisibilityLodConfig, resolve_lod_level
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


def test_resolve_lod_level_deterministic() -> None:
    config = VisibilityLodConfig(map_mode=False, lod1_zoom_max=0.4, lod2_zoom_max=0.2)
    assert resolve_lod_level(0.8, config) == LOD0
    assert resolve_lod_level(0.35, config) == LOD1
    assert resolve_lod_level(0.05, config) == LOD2


def test_map_mode_forces_lod2() -> None:
    config = VisibilityLodConfig(
        lod_enabled=True, map_mode=True, lod1_zoom_max=0.4, lod2_zoom_max=0.2
    )
    assert resolve_lod_level(1.0, config) == LOD2


def test_lod_disabled_always_lod0() -> None:
    config = VisibilityLodConfig(
        lod_enabled=False, map_mode=True, lod1_zoom_max=0.4, lod2_zoom_max=0.2
    )
    assert resolve_lod_level(0.05, config) == LOD0
    assert resolve_lod_level(1.0, config) == LOD0

    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog(), lod_config=config)
    metrics = ExtractStepMetrics()
    extractor.extract(_camera_at(0, 0, zoom=0.05), step_metrics=metrics)
    assert metrics.tile_lod0_groups >= 1
    assert metrics.tile_lod2_groups == 0
    assert metrics.tile_map_mode_active == 0


def test_lod0_matches_legacy_at_normal_zoom() -> None:
    world = _world_with_chunks(((0, 0), (1, 0)))
    camera = _camera_at(0, 0, zoom=0.8)
    batch_extractor = ChunkRenderExtractor(
        world, _catalog(), extract_mode="batch", lod_mode="detail_only"
    )
    legacy_extractor = ChunkRenderExtractor(world, _catalog(), extract_mode="per_chunk")

    def _sig(frame):
        parts = []
        for chunk in frame.tile_chunks:
            for layer in chunk.layers:
                parts.append((chunk.chunk_coord, int(layer.layer), len(layer.tile_ids)))
        return tuple(parts)

    assert _sig(batch_extractor.extract(camera)) == _sig(legacy_extractor.extract(camera))


def test_lod2_fewer_tiles_than_lod0() -> None:
    world = _world_with_chunks(((0, 0),))
    config = VisibilityLodConfig(map_mode=False, lod1_zoom_max=0.4, lod2_zoom_max=0.2)
    lod0_extractor = ChunkRenderExtractor(
        world, _catalog(), lod_config=config, lod_mode="detail_only"
    )
    lod2_extractor = ChunkRenderExtractor(world, _catalog(), lod_config=config)
    camera = _camera_at(0, 0, zoom=0.05)

    lod0_count = sum(
        len(layer.tile_ids)
        for chunk in lod0_extractor.extract(camera).tile_chunks
        for layer in chunk.layers
    )
    lod2_count = sum(
        len(layer.tile_ids)
        for chunk in lod2_extractor.extract(camera).tile_chunks
        for layer in chunk.layers
    )
    assert lod2_count < lod0_count


def test_lod_metrics_on_zoom_out() -> None:
    world = _world_with_chunks(tuple((x, 0) for x in range(8)))
    config = VisibilityLodConfig(map_mode=False, lod1_zoom_max=0.4, lod2_zoom_max=0.2)
    extractor = ChunkRenderExtractor(world, _catalog(), lod_config=config)
    metrics = ExtractStepMetrics()

    extractor.extract(_camera_at(0, 0, zoom=0.05), step_metrics=metrics)
    assert metrics.tile_lod2_groups >= 1
    assert metrics.tile_lod0_groups == 0


def test_lod_switch_counted() -> None:
    world = _world_with_chunks(((0, 0),))
    config = VisibilityLodConfig(map_mode=False, lod1_zoom_max=0.4, lod2_zoom_max=0.2)
    extractor = ChunkRenderExtractor(world, _catalog(), lod_config=config)
    metrics = ExtractStepMetrics()

    extractor.extract(_camera_at(0, 0, zoom=0.8), step_metrics=metrics)
    metrics.reset()
    extractor.extract(_camera_at(0, 0, zoom=0.05), step_metrics=metrics)
    assert metrics.tile_lod_switches == 1


def test_invalidate_clears_all_lod_levels() -> None:
    world = _world_with_chunks(((0, 0),))
    config = VisibilityLodConfig(map_mode=False, lod1_zoom_max=0.4, lod2_zoom_max=0.2)
    extractor = ChunkRenderExtractor(world, _catalog(), lod_config=config)
    extractor.extract(_camera_at(0, 0, zoom=0.8))
    extractor.extract(_camera_at(0, 0, zoom=0.05))
    assert extractor._batch_registry
    extractor.invalidate((0, 0))
    assert not any(key[0] == (0, 0) for key in extractor._batch_registry)


def test_lod_metrics_zero_overhead_without_profile() -> None:
    world = _world_with_chunks(((0, 0),))
    extractor = ChunkRenderExtractor(world, _catalog())
    frame = extractor.extract(_camera_at(0, 0, zoom=0.05))
    assert len(frame.tile_chunks) == 1
