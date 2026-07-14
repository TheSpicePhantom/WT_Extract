"""M24b — Apply- und Submit-Guards (symmetrisch, kein Discard)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from game_core.chunk_build import (
    BuildCoordinator,
    BuildKey,
    ChunkBuildState,
    DecoState,
    TerrainState,
)
from game_core.chunk_stage import DecoResult, TerrainResult
from game_core.worker_fast_path import has_user_decorations_in_chunk

if TYPE_CHECKING:
    from game_core.world import World


class _StreamerGuardContext(Protocol):
    pending_unload: object
    persistent_deltas: dict[tuple[int, int], object]
    persistent_overrides: dict[tuple[int, int], object]

    def pending_unload_contains(self, coord: tuple[int, int]) -> bool: ...


def _pending_unload_contains(streamer: _StreamerGuardContext, coord: tuple[int, int]) -> bool:
    checker = streamer.pending_unload
    if hasattr(checker, "contains"):
        return checker.contains(coord)
    return False


def _is_suppressed(build_state: ChunkBuildState) -> bool:
    return build_state.deco_state == DecoState.SUPPRESSED


def can_apply_terrain_result(
    world: World,
    streamer: _StreamerGuardContext,
    result: TerrainResult,
    build_state: ChunkBuildState,
    coordinator: BuildCoordinator,
    *,
    wanted: bool = True,
) -> bool:
    coord = result.coord
    if not wanted:
        return False
    if _pending_unload_contains(streamer, coord):
        return False
    if coord in streamer.persistent_deltas:
        return False
    if coord in streamer.persistent_overrides:
        return False
    if coord in world.dirty_chunks:
        return False
    if result.build_key.build_epoch != coordinator.read_build_epoch():
        return False
    pending = build_state.pending_terrain_build_key
    if pending is not None and result.build_key != pending:
        return False
    active = build_state.terrain_build_key
    if active is not None:
        if result.build_key.terrain_revision < active.terrain_revision:
            return False
        if coord in world.chunks and result.build_key != active:
            return False
    if coord in world.chunks and build_state.terrain_state == TerrainState.APPLIED:
        if active is not None and result.build_key != active:
            return False
    return True


def can_apply_deco_result(
    world: World,
    streamer: _StreamerGuardContext,
    result: DecoResult,
    build_state: ChunkBuildState,
    coordinator: BuildCoordinator,
    *,
    wanted: bool = True,
) -> bool:
    coord = result.coord
    if not wanted:
        return False
    if _pending_unload_contains(streamer, coord):
        return False
    if coord in streamer.persistent_deltas:
        return False
    if coord in streamer.persistent_overrides:
        return False
    if coord in world.dirty_chunks:
        return False
    if has_user_decorations_in_chunk(world, coord):
        return False
    if _is_suppressed(build_state):
        return False
    if build_state.terrain_state != TerrainState.APPLIED:
        return False
    if result.build_key.build_epoch != coordinator.read_build_epoch():
        return False
    active_terrain = build_state.terrain_build_key
    if active_terrain is None or result.build_key != active_terrain:
        return False
    if build_state.last_applied_deco_build_key is not None:
        if result.build_key == build_state.last_applied_deco_build_key:
            return False
    if coord not in world.chunks:
        return False
    return True


def submit_terrain_allowed(
    world: World,
    streamer: _StreamerGuardContext,
    coord: tuple[int, int],
    build_state: ChunkBuildState,
    *,
    wanted: bool,
    in_flight_room: bool,
) -> bool:
    if not wanted:
        return False
    if not in_flight_room:
        return False
    if _pending_unload_contains(streamer, coord):
        return False
    if coord in streamer.persistent_overrides:
        return False
    if coord in streamer.persistent_deltas:
        return False
    if coord in world.chunks and build_state.terrain_state == TerrainState.APPLIED:
        return False
    if build_state.terrain_state == TerrainState.IN_FLIGHT:
        return False
    return True


def submit_deco_allowed(
    world: World,
    streamer: _StreamerGuardContext,
    coord: tuple[int, int],
    build_state: ChunkBuildState,
    *,
    wanted: bool,
    in_flight_room: bool,
    visible_terrain_pending: int,
) -> bool:
    if not wanted:
        return False
    if not in_flight_room:
        return False
    if visible_terrain_pending > 0:
        return False
    if _is_suppressed(build_state):
        return False
    if build_state.terrain_state != TerrainState.APPLIED:
        return False
    if build_state.deco_state in (DecoState.IN_FLIGHT, DecoState.APPLIED):
        return False
    if build_state.deco_incomplete and build_state.deco_state == DecoState.APPLIED:
        return False
    if _pending_unload_contains(streamer, coord):
        return False
    if coord in streamer.persistent_overrides:
        return False
    if coord in streamer.persistent_deltas:
        return False
    if coord in world.dirty_chunks:
        return False
    if has_user_decorations_in_chunk(world, coord):
        return False
    if build_state.terrain_build_key is None:
        return False
    if coord not in world.chunks:
        return False
    return True


def should_suppress_deco(
    world: World,
    streamer: _StreamerGuardContext,
    coord: tuple[int, int],
    *,
    wanted: bool,
) -> str | None:
    if not wanted:
        return "not_wanted"
    if _pending_unload_contains(streamer, coord):
        return "pending_unload"
    if coord in streamer.persistent_overrides:
        return "override"
    if coord in streamer.persistent_deltas:
        return "delta"
    if coord in world.dirty_chunks:
        return "dirty"
    if has_user_decorations_in_chunk(world, coord):
        return "user_deco"
    return None
