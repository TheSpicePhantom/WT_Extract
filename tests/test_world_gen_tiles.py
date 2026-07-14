"""Tests — Tile-Auflösung und generate_chunk (M21)."""

from __future__ import annotations

from game_core.world import CHUNK_SIZE_TILES, CHUNK_TILE_COUNT
from game_core.world_gen import (
    KEY_DEEP_WATER,
    KEY_GRASS,
    KEY_SHALLOW_WATER,
    generate_chunk,
    generate_chunk_terrain,
    resolve_tile,
)


def test_generate_chunk_terrain_layers() -> None:
    layers = generate_chunk_terrain(0, 0)
    assert len(layers[0]) == CHUNK_TILE_COUNT
    assert len(layers[1]) == CHUNK_TILE_COUNT


def test_generate_chunk_has_tile_keys() -> None:
    chunk = generate_chunk(1, 1)
    assert chunk.get_key(0, 0)
    assert all(key.startswith("wt:tiles/") for key in chunk.layer_keys[0])


def test_resolve_tile_water_or_land() -> None:
    resolved = resolve_tile(500, 500)
    assert resolved.tile_key_layer0.startswith("wt:tiles/")
    if resolved.tile_key_layer0 in (KEY_DEEP_WATER, KEY_SHALLOW_WATER):
        assert resolved.is_walkable is False
    else:
        assert resolved.is_walkable is True


def test_start_area_prefers_land() -> None:
    resolved = resolve_tile(256, 256)
    assert resolved.tile_key_layer0 != KEY_DEEP_WATER
    assert resolved.tile_key_layer0 != KEY_SHALLOW_WATER or resolved.biome_id.value == "shallow_water"
