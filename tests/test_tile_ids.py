"""Tests — stabile FNV-Tile-IDs (M22c)."""

from __future__ import annotations

import pytest

from game_core.content_registry import load_content_registry
from game_core.tile_ids import (
    EMPTY_TILE_ID,
    build_tile_key_by_id,
    normalize_tile_key,
    stable_tile_id,
)


def test_empty_key_maps_to_empty_tile_id() -> None:
    assert stable_tile_id("") == EMPTY_TILE_ID
    assert EMPTY_TILE_ID == 0


def test_stable_tile_id_is_deterministic() -> None:
    key = "wt:tiles/grass"
    assert stable_tile_id(key) == stable_tile_id(key)
    assert stable_tile_id(key) != EMPTY_TILE_ID


def test_normalize_tile_key_matches_sprite_rules() -> None:
    assert normalize_tile_key("WT:Tiles/Grass") == "wt:tiles/grass"
    assert normalize_tile_key("") == ""


def test_registry_ids_match_stable_hash() -> None:
    content = load_content_registry()
    for tile in content.tiles:
        assert content.tile_key_to_id(tile.sprite_key) == stable_tile_id(tile.sprite_key)
    assert content.tile_key_to_id("") == EMPTY_TILE_ID


def test_build_tile_key_by_id_detects_collision(monkeypatch) -> None:
    key_by_id = build_tile_key_by_id(["wt:tiles/grass", ""])
    assert key_by_id[stable_tile_id("wt:tiles/grass")] == "wt:tiles/grass"
    assert key_by_id[EMPTY_TILE_ID] == ""

    def fake_stable(key: str) -> int:
        if key:
            return 999
        return EMPTY_TILE_ID

    monkeypatch.setattr("game_core.tile_ids.stable_tile_id", fake_stable)
    with pytest.raises(ValueError, match="Kollision"):
        build_tile_key_by_id(["wt:tiles/grass", "wt:tiles/dirt"])
