"""Chunk-Solid-Grid — 8×8 px Zellen für Broad-Phase-Kollision."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

from game_core.collision_catalog import CollisionCatalog, CollisionMask
from game_core.content_registry import ContentRegistry
from game_core.tile_ids import stable_tile_id
from game_core.worker_content_snapshot import WorkerContentSnapshot
from game_core.world import (
    CHUNK_SIZE_PX,
    CHUNK_SIZE_TILES,
    EMPTY_OVERLAY_KEY,
    OVERLAY_LAYER_ID,
    TERRAIN_LAYER_ID,
    TILE_SIZE_PX,
    Chunk,
    World,
    tile_to_world_anchor,
)
from game_core.world_gen_result import DecorationPlacement

COLLISION_CELL_PX = 8
CHUNK_CELLS_PER_AXIS = CHUNK_SIZE_PX // COLLISION_CELL_PX
CHUNK_SOLID_GRID_BYTES = (CHUNK_CELLS_PER_AXIS * CHUNK_CELLS_PER_AXIS + 7) // 8


def _empty_solid_grid() -> bytearray:
    return bytearray(CHUNK_SOLID_GRID_BYTES)


def _set_cell(grid: bytearray, cell_x: int, cell_y: int, solid: bool) -> None:
    if not (0 <= cell_x < CHUNK_CELLS_PER_AXIS and 0 <= cell_y < CHUNK_CELLS_PER_AXIS):
        return
    bit_index = cell_y * CHUNK_CELLS_PER_AXIS + cell_x
    byte_index = bit_index >> 3
    bit_mask = 1 << (bit_index & 7)
    if solid:
        grid[byte_index] |= bit_mask
    else:
        grid[byte_index] &= ~bit_mask


def _cell_solid(grid: bytes, cell_x: int, cell_y: int) -> bool:
    if not (0 <= cell_x < CHUNK_CELLS_PER_AXIS and 0 <= cell_y < CHUNK_CELLS_PER_AXIS):
        return True
    bit_index = cell_y * CHUNK_CELLS_PER_AXIS + cell_x
    return bool(grid[bit_index >> 3] & (1 << (bit_index & 7)))


def _fill_tile_rect(grid: bytearray, chunk: Chunk, tx: int, ty: int) -> None:
    base_x = tx * (TILE_SIZE_PX // COLLISION_CELL_PX)
    base_y = ty * (TILE_SIZE_PX // COLLISION_CELL_PX)
    cells_per_tile = TILE_SIZE_PX // COLLISION_CELL_PX
    for dy in range(cells_per_tile):
        for dx in range(cells_per_tile):
            _set_cell(grid, base_x + dx, base_y + dy, True)


def _stamp_mask_in_chunk(
    grid: bytearray,
    chunk: Chunk,
    mask: CollisionMask,
    offsets: tuple[tuple[int, int], ...],
    anchor_world_x: float,
    anchor_world_y: float,
) -> None:
    chunk_origin_x = chunk.coord[0] * CHUNK_SIZE_PX
    chunk_origin_y = chunk.coord[1] * CHUNK_SIZE_PX

    for local_x, local_y in offsets:
        world_px = anchor_world_x + local_x
        world_py = anchor_world_y + local_y
        local_px = world_px - chunk_origin_x
        local_py = world_py - chunk_origin_y
        if not (0 <= local_px < CHUNK_SIZE_PX and 0 <= local_py < CHUNK_SIZE_PX):
            continue
        cell_x = int(local_px // COLLISION_CELL_PX)
        cell_y = int(local_py // COLLISION_CELL_PX)
        _set_cell(grid, cell_x, cell_y, True)


def rebuild_chunk_solid(
    chunk: Chunk,
    world: World,
    content: ContentRegistry,
    collision: CollisionCatalog,
) -> bytes:
    """Baut 8×8-Solid-Grid für einen Chunk — Terrain, Overlay, Decorations."""
    grid = _empty_solid_grid()

    cx, cy = chunk.coord
    for ty in range(CHUNK_SIZE_TILES):
        for tx in range(CHUNK_SIZE_TILES):
            wx = cx * CHUNK_SIZE_TILES + tx
            wy = cy * CHUNK_SIZE_TILES + ty
            terrain_key = world.get_tile(wx, wy, layer=TERRAIN_LAYER_ID)
            if terrain_key is None or not content.tile_walkable(terrain_key):
                _fill_tile_rect(grid, chunk, tx, ty)

            overlay_key = world.get_tile(wx, wy, layer=OVERLAY_LAYER_ID)
            if overlay_key and overlay_key != EMPTY_OVERLAY_KEY:
                if not content.tile_walkable(overlay_key):
                    _fill_tile_rect(grid, chunk, tx, ty)

    chunk_origin_x = cx * CHUNK_SIZE_PX
    chunk_origin_y = cy * CHUNK_SIZE_PX
    chunk_max_x = chunk_origin_x + CHUNK_SIZE_PX
    chunk_max_y = chunk_origin_y + CHUNK_SIZE_PX

    for placed in world.decorations:
        definition = content.decoration_by_id(placed.decoration_id)
        if definition is None or not definition.blocks_movement:
            continue
        mask = collision.decoration_mask(definition.sprite_key)
        if mask is None:
            if definition.blocks_movement:
                wx = int(placed.world_x // TILE_SIZE_PX)
                wy = int(placed.world_y // TILE_SIZE_PX)
                local_wx = wx - cx * CHUNK_SIZE_TILES
                local_wy = wy - cy * CHUNK_SIZE_TILES
                if 0 <= local_wx < CHUNK_SIZE_TILES and 0 <= local_wy < CHUNK_SIZE_TILES:
                    _fill_tile_rect(grid, chunk, local_wx, local_wy)
            continue
        anchor_x = placed.world_x
        anchor_y = placed.world_y
        max_x = anchor_x + mask.width
        max_y = anchor_y + mask.height
        if max_x <= chunk_origin_x or max_y <= chunk_origin_y:
            continue
        if anchor_x >= chunk_max_x or anchor_y >= chunk_max_y:
            continue
        offsets = collision.solid_offsets(mask)
        _stamp_mask_in_chunk(grid, chunk, mask, offsets, anchor_x, anchor_y)

    return bytes(grid)


def build_chunk_solid_grid(
    chunk: Chunk,
    decorations: Sequence[DecorationPlacement],
    *,
    walkable_by_tile_id: Mapping[int, bool],
    snapshot: WorkerContentSnapshot,
    collision: CollisionCatalog,
) -> bytes:
    """Pure Solid-Grid — Terrain, Overlay, chunk-lokale prozedurale Deko (M22e)."""
    grid = _empty_solid_grid()
    cx, cy = chunk.coord

    for ty in range(CHUNK_SIZE_TILES):
        for tx in range(CHUNK_SIZE_TILES):
            terrain_key = chunk.get_key(tx, ty, layer=TERRAIN_LAYER_ID)
            terrain_id = stable_tile_id(terrain_key or "")
            if not walkable_by_tile_id.get(terrain_id, True):
                _fill_tile_rect(grid, chunk, tx, ty)

            overlay_key = chunk.get_key(tx, ty, layer=OVERLAY_LAYER_ID)
            if overlay_key and overlay_key != EMPTY_OVERLAY_KEY:
                overlay_id = stable_tile_id(overlay_key)
                if not walkable_by_tile_id.get(overlay_id, True):
                    _fill_tile_rect(grid, chunk, tx, ty)

    chunk_origin_x = cx * CHUNK_SIZE_PX
    chunk_origin_y = cy * CHUNK_SIZE_PX
    chunk_max_x = chunk_origin_x + CHUNK_SIZE_PX
    chunk_max_y = chunk_origin_y + CHUNK_SIZE_PX

    for placement in decorations:
        deco_int = stable_tile_id(placement.decoration_id)
        if not snapshot.decoration_blocks_by_id.get(deco_int, False):
            continue
        sprite_key = snapshot.decoration_sprite_key_by_id.get(deco_int)
        if sprite_key is None:
            continue
        mask = collision.decoration_mask(sprite_key)
        anchor_x, anchor_y = tile_to_world_anchor(placement.wx, placement.wy)
        if mask is None:
            local_wx = placement.wx - cx * CHUNK_SIZE_TILES
            local_wy = placement.wy - cy * CHUNK_SIZE_TILES
            if 0 <= local_wx < CHUNK_SIZE_TILES and 0 <= local_wy < CHUNK_SIZE_TILES:
                _fill_tile_rect(grid, chunk, local_wx, local_wy)
            continue
        max_x = anchor_x + mask.width
        max_y = anchor_y + mask.height
        if max_x <= chunk_origin_x or max_y <= chunk_origin_y:
            continue
        if anchor_x >= chunk_max_x or anchor_y >= chunk_max_y:
            continue
        offsets = collision.solid_offsets(mask)
        _stamp_mask_in_chunk(grid, chunk, mask, offsets, anchor_x, anchor_y)

    return bytes(grid)


def world_cell_solid(world: World, world_px: float, world_py: float) -> bool:
    """Globaler Solid-Check — True wenn blockiert oder außerhalb."""
    cell_x = int(math.floor(world_px / COLLISION_CELL_PX))
    cell_y = int(math.floor(world_py / COLLISION_CELL_PX))
    if cell_x < 0 or cell_y < 0:
        return True

    chunk_x = cell_x // CHUNK_CELLS_PER_AXIS
    chunk_y = cell_y // CHUNK_CELLS_PER_AXIS
    chunk = world.get_chunk((chunk_x, chunk_y))
    if chunk is None or chunk.solid_grid is None:
        return True

    local_x = cell_x - chunk_x * CHUNK_CELLS_PER_AXIS
    local_y = cell_y - chunk_y * CHUNK_CELLS_PER_AXIS
    return _cell_solid(chunk.solid_grid, local_x, local_y)


def chunk_coords_for_mask_stamp(
    anchor_world_x: float,
    anchor_world_y: float,
    mask: CollisionMask,
) -> set[tuple[int, int]]:
    """Chunk-Koordinaten, die eine Maske berühren kann."""
    min_x = anchor_world_x
    min_y = anchor_world_y
    max_x = anchor_world_x + mask.width
    max_y = anchor_world_y + mask.height
    min_cx = int(math.floor(min_x / CHUNK_SIZE_PX))
    min_cy = int(math.floor(min_y / CHUNK_SIZE_PX))
    max_cx = int(math.floor((max_x - 1e-9) / CHUNK_SIZE_PX))
    max_cy = int(math.floor((max_y - 1e-9) / CHUNK_SIZE_PX))
    coords: set[tuple[int, int]] = set()
    for cy in range(min_cy, max_cy + 1):
        for cx in range(min_cx, max_cx + 1):
            coords.add((cx, cy))
    return coords
