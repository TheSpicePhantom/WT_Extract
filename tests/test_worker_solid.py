"""Tests — Worker-Solid Pure-Funktion (M22e Phase 2)."""

from __future__ import annotations

from game_core.collision_catalog import load_collision_catalog
from game_core.collision_grid import build_chunk_solid_grid
from game_core.content_registry import load_content_registry
from game_core.tile_ids import stable_tile_id
from game_core.worker_content_snapshot import WorkerContentSnapshot
from game_core.world import Chunk
from game_core.world_gen import compute_procedural_decorations
from game_core.world_gen_context import WorldGenContext
from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def _walkable_by_tile_id(content) -> dict[int, bool]:
    mapping: dict[int, bool] = {0: True}
    for tile in content.tiles:
        mapping[stable_tile_id(tile.sprite_key)] = tile.walkable
    return mapping


def test_snapshot_walkable_matches_registry() -> None:
    content = load_content_registry()
    snapshot = WorkerContentSnapshot.from_registry(content)
    for tile in content.tiles:
        tile_id = stable_tile_id(tile.sprite_key)
        assert snapshot.tile_walkable_by_id(tile_id) == content.tile_walkable(tile.sprite_key)


def test_build_solid_matches_rebuild() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = WorldGenContext.from_active()
    snapshot = WorkerContentSnapshot.from_registry(content)
    walkable = _walkable_by_tile_id(content)
    known_ids = frozenset(content.decoration_ids())

    for coord in REFERENCE_TEST_COORDS:
        ref = sequential_reference_chunk(coord, content, collision)
        cx, cy = coord
        layer0 = [content.tile_id_to_key(tile_id) for tile_id in ref.layer0]
        layer1 = [content.tile_id_to_key(tile_id) for tile_id in ref.layer1]
        chunk = Chunk.from_terrain(coord, layer0, layer1)
        decorations = compute_procedural_decorations(
            cx, cy, ctx=ctx, known_decoration_ids=known_ids
        )
        built = build_chunk_solid_grid(
            chunk,
            decorations,
            walkable_by_tile_id=walkable,
            snapshot=snapshot,
            collision=collision,
        )
        assert built == ref.solid_grid
