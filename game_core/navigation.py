"""Navigation — Walkability und Charakterbewegung mit Pixel-Kollision."""

from __future__ import annotations

import math

from game_core.character import (
    CHARACTER_SPRITE_PX,
    AnimClip,
    Character,
    direction_from_delta,
    move_speed_for_clip,
)
from game_core.collision_catalog import CollisionCatalog
from game_core.collision_grid import world_cell_solid
from game_core.content_registry import ContentRegistry
from game_core.world import (
    CHUNK_SIZE_PX,
    EMPTY_OVERLAY_KEY,
    OVERLAY_LAYER_ID,
    TERRAIN_LAYER_ID,
    TILE_SIZE_PX,
    World,
)

FOOTPRINT_TILES = max(1, int(math.ceil(CHARACTER_SPRITE_PX / TILE_SIZE_PX)))


def _chunk_coord_for_world_px(world_px: float, world_py: float) -> tuple[int, int]:
    return (
        int(math.floor(world_px / CHUNK_SIZE_PX)),
        int(math.floor(world_py / CHUNK_SIZE_PX)),
    )


def _collision_sample_chunk_coords(
    world_x: float,
    world_y: float,
    collision: CollisionCatalog,
    character: Character,
) -> set[tuple[int, int]]:
    char_mask = collision.character_mask(character.direction)
    coords: set[tuple[int, int]] = set()
    for local_x, local_y in collision.solid_offsets(char_mask):
        sample_x = world_x + local_x + 0.5
        sample_y = world_y + local_y + 0.5
        coords.add(_chunk_coord_for_world_px(sample_x, sample_y))
    return coords


def footprint_tile_coords(world_x: float, world_y: float) -> tuple[tuple[int, int], ...]:
    """2×2-Tiles unter dem Sprite-Anker (unten links) — M14-Fallback."""
    tx0 = int(math.floor(world_x / TILE_SIZE_PX))
    ty0 = int(math.floor(world_y / TILE_SIZE_PX))
    coords: list[tuple[int, int]] = []
    for dy in range(FOOTPRINT_TILES):
        for dx in range(FOOTPRINT_TILES):
            coords.append((tx0 + dx, ty0 + dy))
    return tuple(coords)


def tile_blocks_movement(world: World, content: ContentRegistry, wx: int, wy: int) -> bool:
    """True wenn Welt-Tile oder Decoration die Bewegung blockiert — M14-Fallback."""
    terrain_key = world.get_tile(wx, wy, layer=TERRAIN_LAYER_ID)
    if terrain_key is None:
        return True
    if not content.tile_walkable(terrain_key):
        return True

    overlay_key = world.get_tile(wx, wy, layer=OVERLAY_LAYER_ID)
    if overlay_key and overlay_key != EMPTY_OVERLAY_KEY:
        if not content.tile_walkable(overlay_key):
            return True

    placed = world.decoration_at_tile(wx, wy)
    if placed is not None and content.decoration_blocks(placed.decoration_id):
        return True

    return False


def _anchor_position_blocked_tiles(
    world: World,
    content: ContentRegistry,
    world_x: float,
    world_y: float,
) -> bool:
    for wx, wy in footprint_tile_coords(world_x, world_y):
        if tile_blocks_movement(world, content, wx, wy):
            return True
    return False


def mask_position_blocked(
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
    character: Character,
    world_x: float,
    world_y: float,
) -> bool:
    """Pixel-Kollision — Charaktermaske gegen Chunk-Solid-Grid."""
    sample_coords = _collision_sample_chunk_coords(
        world_x, world_y, collision, character
    )
    world.ensure_collision_fresh_for_coords(sample_coords, content, collision)
    char_mask = collision.character_mask(character.direction)
    for local_x, local_y in collision.solid_offsets(char_mask):
        sample_x = world_x + local_x + 0.5
        sample_y = world_y + local_y + 0.5
        if world_cell_solid(world, sample_x, sample_y):
            return True
    return False


def anchor_position_blocked(
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
    character: Character,
    world_x: float,
    world_y: float,
) -> bool:
    """Blockiert wenn Charaktermaske gegen Solid-Grid kollidiert."""
    return mask_position_blocked(world, content, collision, character, world_x, world_y)


def find_walkable_anchor(
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
    character: Character,
    *,
    near_x: float,
    near_y: float,
    search_radius_tiles: int = 64,
) -> tuple[float, float]:
    """Begehbaren Anker (unten links) nahe near_x/y — tile-snapped."""
    if not anchor_position_blocked(world, content, collision, character, near_x, near_y):
        return near_x, near_y

    start_tx = int(math.floor(near_x / TILE_SIZE_PX))
    start_ty = int(math.floor(near_y / TILE_SIZE_PX))
    for radius in range(1, search_radius_tiles + 1):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if max(abs(dx), abs(dy)) != radius:
                    continue
                wx = start_tx + dx
                wy = start_ty + dy
                anchor_x = float(wx * TILE_SIZE_PX)
                anchor_y = float(wy * TILE_SIZE_PX)
                if not anchor_position_blocked(
                    world, content, collision, character, anchor_x, anchor_y
                ):
                    return anchor_x, anchor_y
    return near_x, near_y


def spawn_character_at_center(
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
    center_x: float,
    center_y: float,
) -> Character:
    """Charakter mit Sprite-Mitte nahe center — auf begehbarem Terrain."""
    half = CHARACTER_SPRITE_PX * 0.5
    character = Character(world_x=center_x - half, world_y=center_y - half)
    anchor_x, anchor_y = find_walkable_anchor(
        world,
        content,
        collision,
        character,
        near_x=character.world_x,
        near_y=character.world_y,
    )
    character.world_x = anchor_x
    character.world_y = anchor_y
    return character


def apply_character_movement(
    character: Character,
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
    dt: float,
    move_x: float,
    move_y: float,
    *,
    force_run: bool = False,
) -> None:
    """Bewegung mit Axis-Slide — Pixel-Kollision via Solid-Grid."""
    sample_coords = _collision_sample_chunk_coords(
        character.world_x, character.world_y, collision, character
    )
    world.ensure_collision_fresh_for_coords(sample_coords, content, collision)
    character.force_run = force_run
    dx = float(move_x)
    dy = float(move_y)
    speed_len = math.hypot(dx, dy)

    if speed_len > 1e-6:
        dx /= speed_len
        dy /= speed_len
        character.direction = direction_from_delta(dx, dy, character.direction)
        if force_run:
            character.clip = AnimClip.RUN
            scalar_speed = move_speed_for_clip(AnimClip.RUN)
        else:
            character.clip = AnimClip.WALK
            scalar_speed = move_speed_for_clip(AnimClip.WALK)

        step_x = dx * scalar_speed * dt
        step_y = dy * scalar_speed * dt

        candidate_x = character.world_x + step_x
        if not mask_position_blocked(
            world, content, collision, character, candidate_x, character.world_y
        ):
            character.world_x = candidate_x

        candidate_y = character.world_y + step_y
        if not mask_position_blocked(
            world, content, collision, character, character.world_x, candidate_y
        ):
            character.world_y = candidate_y
    else:
        character.clip = AnimClip.IDLE

    character.tick_animation(dt)
