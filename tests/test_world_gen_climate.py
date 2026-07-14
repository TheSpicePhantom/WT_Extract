"""Tests — Klima-Sampling und Chunk-Naht-Stabilität (M21)."""

from __future__ import annotations

from game_core.biomes import WaterClass
from game_core.world import CHUNK_SIZE_TILES
from game_core.world_gen import classify_water, generate_chunk, sample_climate, sample_height
from game_core.world_gen import (
    build_chunk_field_cache,
    generate_chunk_terrain,
    resolve_tile,
    resolve_tile_cached,
)


def test_sample_climate_fields() -> None:
    sample = sample_climate(100.0, 200.0)
    assert 0.0 <= sample.height <= 1.0
    assert 0.0 <= sample.temperature <= 1.0
    assert 0.0 <= sample.moisture <= 1.0
    assert 0.0 <= sample.continentalness <= 1.0


def test_height_deterministic() -> None:
    assert sample_height(10.0, 20.0) == sample_height(10.0, 20.0)


def test_water_classification() -> None:
    assert classify_water(0.1) == WaterClass.DEEP
    assert classify_water(0.40) == WaterClass.SHALLOW
    assert classify_water(0.55) == WaterClass.LAND


def test_chunk_seam_stable() -> None:
    """Gleicher Welt-Tile an Chunk-Grenze — identisches Sample von beiden Chunks."""
    cx, cy = 2, 3
    tx = CHUNK_SIZE_TILES - 1
    ty = 4
    wx = cx * CHUNK_SIZE_TILES + tx
    wy = cy * CHUNK_SIZE_TILES + ty

    left = generate_chunk(cx, cy)
    right = generate_chunk(cx + 1, cy)
    right_tx = 0
    assert left.get_key(tx, ty) == right.get_key(right_tx, ty)


def test_chunk_reload_identical() -> None:
    a = generate_chunk(5, -2)
    b = generate_chunk(5, -2)
    assert a.layer_keys == b.layer_keys


def test_chunk_field_cache_matches_resolve_tile() -> None:
    cx, cy = 3, 4
    cache = build_chunk_field_cache(cx, cy)
    for ty in range(CHUNK_SIZE_TILES):
        for tx in range(CHUNK_SIZE_TILES):
            wx = cx * CHUNK_SIZE_TILES + tx
            wy = cy * CHUNK_SIZE_TILES + ty
            direct = resolve_tile(wx, wy)
            cached = resolve_tile_cached(tx, ty, cache)
            assert direct.tile_key_layer0 == cached.tile_key_layer0
            assert direct.tile_key_layer1 == cached.tile_key_layer1
            assert direct.biome_id == cached.biome_id


def test_generate_chunk_terrain_matches_cache_path() -> None:
    layers = generate_chunk_terrain(2, 2)
    chunk = generate_chunk(2, 2)
    assert layers[0] == chunk.layer_keys[0]
    assert layers[1] == chunk.layer_keys[1]
