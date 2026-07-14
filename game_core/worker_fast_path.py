"""Worker-Complete-Fast-Path — Predicates und Guards (M24a)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from game_core.world import CHUNK_SIZE_TILES, TILE_SIZE_PX
from game_core.world_gen_result import ChunkGenResult, is_worker_complete, validate_chunk_gen_result

if TYPE_CHECKING:
    from game_core.world import World
    from game_core.world_gen import DebugMode


class _PendingUnloadCheck(Protocol):
    def contains(self, coord: tuple[int, int]) -> bool: ...


class _StreamerFastPathContext(Protocol):
    pending_unload: _PendingUnloadCheck
    persistent_deltas: dict[tuple[int, int], object]
    persistent_overrides: dict[tuple[int, int], object]


def has_user_decorations_in_chunk(world: World, coord: tuple[int, int]) -> bool:
    cx, cy = coord
    wx_min = cx * CHUNK_SIZE_TILES
    wx_max = wx_min + CHUNK_SIZE_TILES - 1
    wy_min = cy * CHUNK_SIZE_TILES
    wy_max = wy_min + CHUNK_SIZE_TILES - 1
    for placed in world.decorations:
        if placed.procedural:
            continue
        wx = int(placed.world_x // TILE_SIZE_PX)
        wy = int(placed.world_y // TILE_SIZE_PX)
        if wx_min <= wx <= wx_max and wy_min <= wy <= wy_max:
            return True
    return False


def is_worker_complete_result(
    result: ChunkGenResult,
    *,
    worker_apply_enabled: bool,
    debug_mode: DebugMode | None,
) -> bool:
    if not worker_apply_enabled:
        return False
    if debug_mode is not None:
        return False
    if not is_worker_complete(result):
        return False
    try:
        validate_chunk_gen_result(result)
    except ValueError:
        return False
    return True


def can_apply_worker_complete_fast_path(
    world: World,
    streamer: _StreamerFastPathContext,
    result: ChunkGenResult,
    *,
    worker_apply_enabled: bool,
    debug_mode: DebugMode | None,
) -> bool:
    if not is_worker_complete_result(
        result,
        worker_apply_enabled=worker_apply_enabled,
        debug_mode=debug_mode,
    ):
        return False
    coord = result.coord
    if streamer.pending_unload.contains(coord):
        return False
    if coord in streamer.persistent_deltas:
        return False
    if coord in streamer.persistent_overrides:
        return False
    if coord in world.dirty_chunks:
        return False
    if has_user_decorations_in_chunk(world, coord):
        return False
    return True
