"""Golden-Referenz für Chunk-Generierung (M22e)."""

from __future__ import annotations

from dataclasses import dataclass

from game_core.collision_catalog import CollisionCatalog
from game_core.collision_grid import CHUNK_SOLID_GRID_BYTES
from game_core.content_registry import ContentRegistry
from game_core.tile_ids import stable_tile_id
from game_core.world import CHUNK_SIZE_TILES, TILE_SIZE_PX, World
from game_core.world_gen import generate_chunk, populate_chunk_decorations


@dataclass(frozen=True, slots=True)
class ReferenceDecoration:
    wx: int
    wy: int
    decoration_id: str
    procedural: bool = True


@dataclass(frozen=True, slots=True)
class ReferenceChunkState:
    coord: tuple[int, int]
    layer0: tuple[int, ...]
    layer1: tuple[int, ...]
    procedural_decorations: tuple[ReferenceDecoration, ...]
    solid_grid: bytes


def _decorations_in_chunk(
    world: World,
    cx: int,
    cy: int,
) -> tuple[ReferenceDecoration, ...]:
    wx_min = cx * CHUNK_SIZE_TILES
    wx_max = wx_min + CHUNK_SIZE_TILES - 1
    wy_min = cy * CHUNK_SIZE_TILES
    wy_max = wy_min + CHUNK_SIZE_TILES - 1
    found: list[ReferenceDecoration] = []
    for placed in world.decorations:
        if not placed.procedural:
            continue
        wx = int(placed.world_x // TILE_SIZE_PX)
        wy = int(placed.world_y // TILE_SIZE_PX)
        if wx_min <= wx <= wx_max and wy_min <= wy <= wy_max:
            found.append(
                ReferenceDecoration(
                    wx=wx,
                    wy=wy,
                    decoration_id=placed.decoration_id,
                    procedural=True,
                )
            )
    return tuple(sorted(found, key=lambda item: (item.wy, item.wx, item.decoration_id)))


def sequential_reference_chunk(
    coord: tuple[int, int],
    content: ContentRegistry,
    collision: CollisionCatalog,
) -> ReferenceChunkState:
    """Heutiger Sequential-Pfad — Wahrheitsquelle für Golden-Tests."""
    cx, cy = coord
    chunk = generate_chunk(cx, cy)
    world = World(chunks={coord: chunk})
    populate_chunk_decorations(world, content, cx, cy)
    world.rebuild_chunk_solid(coord, content, collision)
    solid_grid = chunk.solid_grid
    assert solid_grid is not None
    assert len(solid_grid) == CHUNK_SOLID_GRID_BYTES

    layer0 = tuple(
        stable_tile_id(chunk.get_key(tx, ty, 0))
        for ty in range(CHUNK_SIZE_TILES)
        for tx in range(CHUNK_SIZE_TILES)
    )
    layer1 = tuple(
        stable_tile_id(chunk.get_key(tx, ty, 1))
        for ty in range(CHUNK_SIZE_TILES)
        for tx in range(CHUNK_SIZE_TILES)
    )

    return ReferenceChunkState(
        coord=coord,
        layer0=layer0,
        layer1=layer1,
        procedural_decorations=_decorations_in_chunk(world, cx, cy),
        solid_grid=bytes(solid_grid),
    )


REFERENCE_TEST_COORDS: tuple[tuple[int, int], ...] = (
    (0, 0),
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (-2, 3),
    (4, -2),
    (3, 3),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
)
