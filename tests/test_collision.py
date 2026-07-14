"""Tests — Pixel-Kollision (M15)."""

from __future__ import annotations

from game_core.character import Character
from game_core.collision_catalog import load_collision_catalog
from game_core.collision_grid import rebuild_chunk_solid
from game_core.content_registry import load_content_registry
from game_core.navigation import mask_position_blocked, spawn_character_at_center
from game_core.world import CHUNK_SIZE_PX, CHUNK_SIZE_TILES, CHUNK_TILE_COUNT, Chunk, World
from game_core.world_gen import KEY_DEEP_WATER, KEY_GRASS, KEY_WATER, generate_demo_world


def _single_grass_world() -> World:
    chunk = Chunk.from_terrain((0, 0), [KEY_GRASS] * CHUNK_TILE_COUNT)
    return World(chunks={(0, 0): chunk})


def _world_with_water_at(wx: int, wy: int) -> World:
    keys = [KEY_GRASS] * CHUNK_TILE_COUNT
    keys[wy * CHUNK_SIZE_TILES + wx] = KEY_DEEP_WATER
    chunk = Chunk.from_terrain((0, 0), keys)
    return World(chunks={(0, 0): chunk})


def test_character_masks_differ_by_direction() -> None:
    collision = load_collision_catalog()
    mask_a = collision.character_mask(0)
    mask_b = collision.character_mask(3)
    assert mask_a.solid_pixel_count() > 0
    assert mask_b.solid_pixel_count() > 0
    assert mask_a.bits != mask_b.bits


def test_tree_trunk_has_fewer_pixels_than_full_height() -> None:
    collision = load_collision_catalog()
    content = load_content_registry()
    tree_key = next(
        entry.sprite_key for entry in content.decorations if entry.category == "tree"
    )
    tree_mask = collision.decoration_mask(tree_key)
    assert tree_mask is not None
    max_y = max(local_y for _, local_y in collision.solid_offsets(tree_mask))
    assert max_y < tree_mask.height - 1


def test_water_blocks_via_solid_grid() -> None:
    world = _world_with_water_at(2, 2)
    content = load_content_registry()
    collision = load_collision_catalog()
    world.rebuild_all_solid(content, collision)
    player = Character(world_x=0.0, world_y=0.0)
    assert mask_position_blocked(world, content, collision, player, 64.0, 64.0)


def test_spawn_finds_walkable_on_demo_world() -> None:
    world = generate_demo_world(16, 16)
    content = load_content_registry()
    collision = load_collision_catalog()
    world.rebuild_all_solid(content, collision)
    center = 16 * CHUNK_SIZE_PX * 0.5
    player = spawn_character_at_center(world, content, collision, center, center)
    assert not mask_position_blocked(
        world, content, collision, player, player.world_x, player.world_y
    )


def test_decoration_stamps_narrower_than_full_tile() -> None:
    world = _single_grass_world()
    content = load_content_registry()
    collision = load_collision_catalog()
    tree_id = next(entry.id for entry in content.decorations if entry.category == "tree")
    world.place_decoration(2, 2, tree_id)
    chunk = world.get_chunk((0, 0))
    assert chunk is not None
    chunk.solid_grid = rebuild_chunk_solid(chunk, world, content, collision)
    solid_cells = sum(byte.bit_count() for byte in chunk.solid_grid)
    assert solid_cells < 16


def test_east_of_tree_is_walkable() -> None:
    world = _single_grass_world()
    content = load_content_registry()
    collision = load_collision_catalog()
    tree_id = next(entry.id for entry in content.decorations if entry.category == "tree")
    wx, wy = 2, 2
    world.place_decoration(wx, wy, tree_id)
    world.rebuild_all_solid(content, collision)
    player = Character(world_x=0.0, world_y=0.0)
    tree_def = content.decoration_by_id(tree_id)
    assert tree_def is not None
    tree_mask = collision.decoration_mask(tree_def.sprite_key)
    assert tree_mask is not None
    anchor_x = float(wx * 32 + tree_mask.width + 8)
    anchor_y = float(wy * 32)
    assert not mask_position_blocked(world, content, collision, player, anchor_x, anchor_y)
