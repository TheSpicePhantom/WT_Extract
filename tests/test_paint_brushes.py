"""Tests — data-driven Tile-Pinsel (M12b)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from game_core.content_registry import load_content_registry
from game_core.paint_brushes import palette_label


def test_brush_palettes_loaded() -> None:
    content = load_content_registry()
    terrain = content.brush_palette("terrain")
    overlay = content.brush_palette("overlay")
    assert terrain is not None
    assert overlay is not None
    assert terrain.layer == 0
    assert overlay.layer == 1
    assert terrain.mouse_left == "wt:tiles/stone"
    assert terrain.mouse_right == "wt:tiles/grass"
    assert dict(terrain.key_bindings) == {"R": "wt:tiles/dirt", "T": "wt:tiles/water"}
    assert dict(overlay.key_bindings) == {"X": ""}


def test_tile_labels() -> None:
    content = load_content_registry()
    assert content.tile_label("wt:tiles/grass") == "grass"
    assert content.tile_label("") == "clear"


def test_palette_label_includes_bindings() -> None:
    content = load_content_registry()
    terrain = content.brush_palette("terrain")
    assert terrain is not None
    label = palette_label(content, terrain)
    assert "LMB=stone" in label
    assert "R=dirt" in label


def test_unknown_brush_key_rejected(tmp_path: Path) -> None:
    tiles_path = tmp_path / "tiles.json"
    tiles_path.write_text(
        json.dumps(
            {
                "version": 1,
                "tiles": {"wt:tiles/grass": {"layer": 0, "walkable": True}},
                "brushes": {
                    "terrain": {
                        "layer": 0,
                        "mouse_left": "wt:tiles/missing",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unbekannter Tile-Key"):
        load_content_registry(tiles_config=tiles_path)
