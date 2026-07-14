"""Kompakte Chunk-Generierungsergebnisse für IPC (M22b/M22c/M22e/M24a)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game_core.decorations import PlacedDecoration
from game_core.tile_ids import stable_tile_id
from game_core.world import CHUNK_TILE_COUNT, Chunk, tile_to_world_anchor

if TYPE_CHECKING:
    from game_core.collision_catalog import CollisionCatalog
    from game_core.content_registry import ContentRegistry
    from game_core.world import World


@dataclass(frozen=True, slots=True)
class ProceduralDecoration:
    """Pure Deko-Platzierung — String-IDs (Worker-Berechnung)."""

    wx: int
    wy: int
    decoration_id: str


# Alias für bestehende Pure-Pfade.
DecorationPlacement = ProceduralDecoration


@dataclass(frozen=True, slots=True)
class IpcDecorationPlacement:
    """IPC-Deko — FNV-int-IDs (M22e)."""

    wx: int
    wy: int
    decoration_id: int


@dataclass(frozen=True, slots=True)
class ChunkGenResult:
    coord: tuple[int, int]
    layer0: tuple[int, ...]
    layer1: tuple[int, ...]
    decorations: tuple[IpcDecorationPlacement, ...] | None = None
    solid_grid: bytes | None = None


def is_worker_complete(result: ChunkGenResult) -> bool:
    return result.decorations is not None and result.solid_grid is not None


def is_terrain_only(result: ChunkGenResult) -> bool:
    return result.decorations is None and result.solid_grid is None


def validate_chunk_gen_result(result: ChunkGenResult) -> None:
    if len(result.layer0) != CHUNK_TILE_COUNT or len(result.layer1) != CHUNK_TILE_COUNT:
        raise ValueError(
            f"ChunkGenResult {result.coord}: erwartet {CHUNK_TILE_COUNT} IDs pro Layer, "
            f"erhalten layer0={len(result.layer0)} layer1={len(result.layer1)}"
        )
    deco_set = result.decorations is not None
    solid_set = result.solid_grid is not None
    if deco_set != solid_set:
        raise ValueError(
            f"ChunkGenResult {result.coord}: decorations/solid_grid müssen beide gesetzt "
            f"oder beide None sein (deco={deco_set}, solid={solid_set})"
        )
    if result.solid_grid is not None and len(result.solid_grid) != _expected_solid_grid_bytes():
        raise ValueError(
            f"ChunkGenResult {result.coord}: solid_grid Länge {len(result.solid_grid)}, "
            f"erwartet {_expected_solid_grid_bytes()}"
        )


def _expected_solid_grid_bytes() -> int:
    from game_core.collision_grid import CHUNK_SOLID_GRID_BYTES

    return CHUNK_SOLID_GRID_BYTES


def chunk_from_result(result: ChunkGenResult, content: ContentRegistry) -> Chunk:
    if len(result.layer0) != CHUNK_TILE_COUNT or len(result.layer1) != CHUNK_TILE_COUNT:
        raise ValueError(
            f"ChunkGenResult {result.coord}: erwartet {CHUNK_TILE_COUNT} IDs pro Layer, "
            f"erhalten layer0={len(result.layer0)} layer1={len(result.layer1)}"
        )
    layer0 = [content.tile_id_to_key(tile_id) for tile_id in result.layer0]
    layer1 = [content.tile_id_to_key(tile_id) for tile_id in result.layer1]
    return Chunk.from_terrain(result.coord, layer0, layer1)


def procedural_to_ipc(
    placements: tuple[ProceduralDecoration, ...],
) -> tuple[IpcDecorationPlacement, ...]:
    return tuple(
        IpcDecorationPlacement(
            wx=placement.wx,
            wy=placement.wy,
            decoration_id=stable_tile_id(placement.decoration_id),
        )
        for placement in placements
    )


def _worker_placed_decorations(
    result: ChunkGenResult,
    content: ContentRegistry,
) -> list[PlacedDecoration]:
    assert result.decorations is not None
    batch: list[PlacedDecoration] = []
    for placement in result.decorations:
        try:
            deco_key = content.decoration_id_to_key(placement.decoration_id)
        except KeyError:
            continue
        if content.decoration_by_id(deco_key) is None:
            continue
        world_x, world_y = tile_to_world_anchor(placement.wx, placement.wy)
        batch.append(
            PlacedDecoration(
                world_x=world_x,
                world_y=world_y,
                decoration_id=deco_key,
                procedural=True,
            )
        )
    return batch


def apply_worker_complete_result(
    world: World,
    result: ChunkGenResult,
    content: ContentRegistry,
) -> Chunk:
    """Reine Datenübernahme — kein Main-Rebuild, kein place_decoration-O(D×N)."""
    if not is_worker_complete(result):
        raise ValueError(
            f"apply_worker_complete_result erfordert WORKER_COMPLETE, "
            f"erhalten coord={result.coord}"
        )
    validate_chunk_gen_result(result)
    chunk = chunk_from_result(result, content)
    coord = result.coord
    assert result.solid_grid is not None
    world.chunks[coord] = chunk
    chunk.solid_grid = result.solid_grid
    world.mark_semantically_active(coord)
    world.decorations.extend(_worker_placed_decorations(result, content))
    world.collision_dirty_chunks.discard(coord)
    return chunk


def apply_chunk_result(
    world: World,
    result: ChunkGenResult,
    content: ContentRegistry,
    collision: CollisionCatalog | None = None,
) -> Chunk:
    """Backward-compat — delegiert an apply_worker_complete_result (M24a)."""
    _ = collision
    return apply_worker_complete_result(world, result, content)
