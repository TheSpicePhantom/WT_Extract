"""Tests — Walkability und Kollision (M14 + M15)."""

from __future__ import annotations

from game_core.character import Character
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.navigation import (
    apply_character_movement,
    mask_position_blocked,
    spawn_character_at_center,
    tile_blocks_movement,
)
from game_core.world import CHUNK_SIZE_PX, CHUNK_SIZE_TILES, CHUNK_TILE_COUNT, Chunk, World
from game_core.world_gen import KEY_DEEP_WATER, KEY_GRASS, KEY_WATER, generate_demo_world


def _single_grass_world() -> World:
    chunk = Chunk.from_terrain((0, 0), [KEY_GRASS] * CHUNK_TILE_COUNT)
    return World(chunks={(0, 0): chunk})


def _world_with_water_at(wx: int, wy: int) -> World:
    keys = [KEY_GRASS] * CHUNK_TILE_COUNT
    index = wy * CHUNK_SIZE_TILES + wx
    keys[index] = KEY_DEEP_WATER
    chunk = Chunk.from_terrain((0, 0), keys)
    return World(chunks={(0, 0): chunk})


def _load_collision_or_skip():
    try:
        return load_collision_catalog()
    except FileNotFoundError:
        import pytest

        pytest.skip("Collision manifest missing — run python tools/bake_collision.py")


def test_water_tile_blocks() -> None:
    world = _world_with_water_at(2, 2)
    content = load_content_registry()
    assert tile_blocks_movement(world, content, 2, 2)
    assert not tile_blocks_movement(world, content, 0, 0)


def test_movement_blocked_by_water() -> None:
    collision = load_collision_catalog()
    world = _world_with_water_at(2, 0)
    content = load_content_registry()
    world.rebuild_all_solid(content, collision)
    player = Character(world_x=0.0, world_y=0.0)
    start_x = player.world_x
    for _ in range(40):
        apply_character_movement(player, world, content, collision, 0.05, 1.0, 0.0)
    assert player.world_x < 32.0
    assert start_x == 0.0


def test_axis_slide_along_water() -> None:
    collision = load_collision_catalog()
    world = _world_with_water_at(2, 0)
    content = load_content_registry()
    world.rebuild_all_solid(content, collision)

    player_east = Character(world_x=0.0, world_y=0.0)
    for _ in range(40):
        apply_character_movement(player_east, world, content, collision, 0.05, 1.0, 0.0)
    assert player_east.world_x < 32.0

    player_north = Character(world_x=0.0, world_y=0.0)
    for _ in range(20):
        apply_character_movement(player_north, world, content, collision, 0.05, 0.0, 1.0)
    assert player_north.world_y > 0.0


def test_spawn_finds_grass_near_demo_center() -> None:
    collision = load_collision_catalog()
    world = generate_demo_world(16, 16)
    content = load_content_registry()
    world.rebuild_all_solid(content, collision)
    center_x = 16 * CHUNK_SIZE_PX * 0.5
    center_y = center_x
    player = spawn_character_at_center(world, content, collision, center_x, center_y)
    assert not mask_position_blocked(
        world, content, collision, player, player.world_x, player.world_y
    )
