"""M24b — Stage-Daten, IPC-Results, build/apply (kein Discard in Apply)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game_core.chunk_build import BuildKey, ChunkBuildState, DecoState, TerrainState
from game_core.decorations import PlacedDecoration
from game_core.tile_ids import stable_tile_id
from game_core.world import CHUNK_TILE_COUNT, Chunk, tile_to_world_anchor
from game_core.world_gen_result import (
    IpcDecorationPlacement,
    procedural_to_ipc,
)

if TYPE_CHECKING:
    from game_core.collision_catalog import CollisionCatalog
    from game_core.content_registry import ContentRegistry
    from game_core.world import World
    from game_core.world_gen import ChunkFieldCache
    from game_core.world_gen_context import WorldGenContext
    from game_core.world_gen_result import ProceduralDecoration


@dataclass(slots=True)
class TerrainStageData:
    build_key: BuildKey
    layer0: tuple[str, ...]
    layer1: tuple[str, ...]
    field_cache: ChunkFieldCache


@dataclass(slots=True)
class DecoStageData:
    build_key: BuildKey
    placements: tuple[ProceduralDecoration, ...]
    solid_grid: bytes


@dataclass(frozen=True, slots=True)
class TerrainResult:
    build_key: BuildKey
    layer0: tuple[int, ...]
    layer1: tuple[int, ...]

    @property
    def coord(self) -> tuple[int, int]:
        return self.build_key.coord


@dataclass(frozen=True, slots=True)
class DecoResult:
    build_key: BuildKey
    placements: tuple[IpcDecorationPlacement, ...]
    solid_grid: bytes

    @property
    def coord(self) -> tuple[int, int]:
        return self.build_key.coord


def to_terrain_result(stage: TerrainStageData) -> TerrainResult:
    layer0_ids = tuple(stable_tile_id(key) for key in stage.layer0)
    layer1_ids = tuple(stable_tile_id(key) for key in stage.layer1)
    return TerrainResult(build_key=stage.build_key, layer0=layer0_ids, layer1=layer1_ids)


def to_deco_result(stage: DecoStageData) -> DecoResult:
    return DecoResult(
        build_key=stage.build_key,
        placements=procedural_to_ipc(stage.placements),
        solid_grid=stage.solid_grid,
    )


def build_terrain_stage(
    build_key: BuildKey,
    ctx: WorldGenContext,
    *,
    field_cache: ChunkFieldCache | None = None,
) -> TerrainStageData:
    from game_core.world_gen import build_terrain_layers_and_field_cache

    cx, cy = build_key.coord
    layer0, layer1, cache = build_terrain_layers_and_field_cache(cx, cy, ctx)
    if field_cache is not None:
        cache = field_cache
    return TerrainStageData(
        build_key=build_key,
        layer0=layer0,
        layer1=layer1,
        field_cache=cache,
    )


def build_deco_stage(terrain_stage: TerrainStageData, ctx: WorldGenContext) -> DecoStageData:
    from game_core.collision_catalog import load_collision_catalog
    from game_core.collision_grid import build_chunk_solid_grid
    from game_core.content_registry import load_content_registry
    from game_core.terrain_gen_profile import profile_section
    from game_core.world_gen import compute_procedural_decorations
    from game_core.worker_content_snapshot import WorkerContentSnapshot

    cx, cy = terrain_stage.build_key.coord
    if ctx._worker_snapshot is not None and ctx._worker_collision is not None:
        snapshot = ctx._worker_snapshot
        collision = ctx._worker_collision
        walkable = _walkable_from_snapshot(snapshot)
        known_ids = snapshot.known_decoration_ids
    else:
        content = load_content_registry()
        collision = load_collision_catalog()
        snapshot = WorkerContentSnapshot.from_registry(content)
        walkable = _walkable_from_content(content)
        known_ids = snapshot.known_decoration_ids

    with profile_section("deco_procedural"):
        procedural = compute_procedural_decorations(
            cx,
            cy,
            ctx=ctx,
            known_decoration_ids=known_ids,
            field_cache=terrain_stage.field_cache,
        )
    with profile_section("deco_solid_grid"):
        chunk = Chunk.from_terrain((cx, cy), list(terrain_stage.layer0), list(terrain_stage.layer1))
        solid_grid = build_chunk_solid_grid(
            chunk,
            procedural,
            walkable_by_tile_id=walkable,
            snapshot=snapshot,
            collision=collision,
        )
    return DecoStageData(
        build_key=terrain_stage.build_key,
        placements=procedural,
        solid_grid=solid_grid,
    )


def _walkable_from_content(content) -> dict[int, bool]:
    mapping: dict[int, bool] = {0: True}
    for tile in content.tiles:
        mapping[stable_tile_id(tile.sprite_key)] = tile.walkable
    return mapping


def _walkable_from_snapshot(snapshot) -> dict[int, bool]:
    mapping: dict[int, bool] = {0: True}
    for tile_id in snapshot.non_walkable_tile_ids:
        mapping[tile_id] = False
    return mapping


def chunk_from_terrain_result(result: TerrainResult, content: ContentRegistry) -> Chunk:
    if len(result.layer0) != CHUNK_TILE_COUNT or len(result.layer1) != CHUNK_TILE_COUNT:
        raise ValueError(f"TerrainResult {result.coord}: ungültige Layer-Länge")
    layer0 = [content.tile_id_to_key(tile_id) for tile_id in result.layer0]
    layer1 = [content.tile_id_to_key(tile_id) for tile_id in result.layer1]
    return Chunk.from_terrain(result.coord, layer0, layer1)


def _deco_batch(result: DecoResult, content: ContentRegistry) -> list[PlacedDecoration]:
    batch: list[PlacedDecoration] = []
    for placement in result.placements:
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


def apply_terrain_stage(
    world: World,
    result: TerrainResult,
    content: ContentRegistry,
    build_state: ChunkBuildState,
) -> Chunk:
    """Nur nach positivem can_apply_terrain_result — kein Discard hier."""
    chunk = chunk_from_terrain_result(result, content)
    coord = result.coord
    world.chunks[coord] = chunk
    world.mark_semantically_active(coord)
    build_state.terrain_build_key = result.build_key
    build_state.terrain_state = TerrainState.APPLIED
    build_state.pending_terrain_build_key = None
    if build_state.deco_state != DecoState.SUPPRESSED:
        build_state.deco_state = DecoState.NONE
    return chunk


def apply_deco_stage(
    world: World,
    result: DecoResult,
    content: ContentRegistry,
    build_state: ChunkBuildState,
) -> None:
    """Nur nach positivem can_apply_deco_result — kein Discard hier."""
    coord = result.coord
    chunk = world.chunks.get(coord)
    if chunk is None:
        raise ValueError(f"apply_deco_stage: Chunk fehlt für {coord}")
    chunk.solid_grid = result.solid_grid
    world.decorations.extend(_deco_batch(result, content))
    world.collision_dirty_chunks.discard(coord)
    build_state.last_applied_deco_build_key = result.build_key
    build_state.deco_state = DecoState.APPLIED
    build_state.deco_incomplete = False


def terrain_result_to_chunk_gen(result: TerrainResult) -> "ChunkGenResult":
    from game_core.world_gen_result import ChunkGenResult

    return ChunkGenResult(
        coord=result.coord,
        layer0=result.layer0,
        layer1=result.layer1,
        decorations=None,
        solid_grid=None,
    )


def deco_result_to_chunk_gen(terrain: TerrainResult, deco: DecoResult) -> "ChunkGenResult":
    from game_core.world_gen_result import ChunkGenResult

    return ChunkGenResult(
        coord=terrain.coord,
        layer0=terrain.layer0,
        layer1=terrain.layer1,
        decorations=deco.placements,
        solid_grid=deco.solid_grid,
    )
