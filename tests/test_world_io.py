"""Tests — Welt Save/Load (M16)."""

from __future__ import annotations

from pathlib import Path

from game_core.character import AnimClip, Character
from game_core.world import CHUNK_TILE_COUNT, Chunk, World
from game_core.world_gen import KEY_GRASS, KEY_STONE, KEY_WATER
from game_core.world_io import (
    DEFAULT_WORLD_SAVE_PATH,
    load_world,
    save_world,
    world_from_dict,
    world_to_dict,
)


def _demo_world() -> tuple[World, Character]:
    terrain = [KEY_GRASS] * CHUNK_TILE_COUNT
    overlay = [""] * CHUNK_TILE_COUNT
    overlay[0] = KEY_STONE
    chunk = Chunk.from_terrain((0, 0), terrain, overlay)
    world = World(chunks={(0, 0): chunk})
    world.place_decoration(1, 1, "trees/apple/summer/apple_1")
    player = Character(world_x=32.0, world_y=48.0, direction=2, clip=AnimClip.WALK, anim_time=0.25)
    return world, player


def test_world_roundtrip_dict() -> None:
    world, player = _demo_world()
    restored = world_from_dict(world_to_dict(world, player))
    assert len(restored.world.chunks) == 1
    assert restored.world.get_tile(0, 0) == KEY_GRASS
    assert restored.world.get_tile(0, 0, layer=1) == KEY_STONE
    assert len(restored.world.decorations) == 1
    assert restored.player.world_x == 32.0
    assert restored.player.clip == AnimClip.WALK


def test_save_and_load_file(tmp_path: Path) -> None:
    world, player = _demo_world()
    path = tmp_path / "world.json"
    save_world(path, world, player)
    loaded = load_world(path)
    assert loaded.world.get_tile(1, 1) is not None
    assert loaded.player.direction == 2
    assert path.is_file()


def test_modified_tile_persists(tmp_path: Path) -> None:
    world, player = _demo_world()
    world.set_tile(2, 2, KEY_WATER)
    path = tmp_path / "wet.json"
    save_world(path, world, player)
    loaded = load_world(path)
    assert loaded.world.get_tile(2, 2) == KEY_WATER


def test_default_save_path_parent_exists() -> None:
    assert DEFAULT_WORLD_SAVE_PATH.parent.name == "saves"
