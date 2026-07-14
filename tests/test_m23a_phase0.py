"""Tests — M23a Phase 0: PersistenzFlags, TerrainDelta, Dirty-Entkopplung."""

from __future__ import annotations

from game_core.persistenz import PersistenzFlags, is_persistenz_relevant
from game_core.chunk_delta import (
    OVERLAY_DELTA_SCHEMA_VERSION,
    OverlayDelta,
    TerrainDelta,
    TileOverride,
    apply_terrain_delta,
    compute_terrain_delta,
    terrain_delta_from_dict,
    terrain_delta_to_dict,
)
from game_core.world import OVERLAY_LAYER_ID, TERRAIN_LAYER_ID, World
from game_core.world_gen import generate_chunk


def test_unmodified_chunk_not_persistenz_relevant() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    assert not world.is_persistenz_relevant((0, 0))


def test_set_tile_sets_persistenz_not_only_dirty() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.dirty_chunks.clear()
    assert world.set_tile(4, 4, "wt:tiles/stone")
    assert (0, 0) not in world.dirty_chunks or world.is_persistenz_relevant((0, 0))
    assert world.get_persistenz_flags((0, 0)) & PersistenzFlags.TILE_MODIFIED
    overrides = world.get_persistenz_tile_overrides((0, 0))
    assert len(overrides) == 1
    assert overrides[0].tile_key == "wt:tiles/stone"


def test_runtime_dirty_without_persistenz_change() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.mark_dirty((0, 0))
    assert (0, 0) in world.dirty_chunks
    assert not world.is_persistenz_relevant((0, 0))


def test_user_deco_sets_persistenz_flag() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(2, 2, "trees/oak", procedural=False)
    assert world.get_persistenz_flags((0, 0)) & PersistenzFlags.USER_DECO_IN_BOUNDS


def test_procedural_deco_does_not_set_persistenz() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(2, 2, "trees/oak", procedural=True)
    assert not world.is_persistenz_relevant((0, 0))


def test_procedural_removal_sets_suppression() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(2, 2, "trees/oak", procedural=True)
    assert world.remove_decoration_at(2, 2)
    assert world.get_persistenz_flags((0, 0)) & PersistenzFlags.SUPPRESSION
    suppressions = world.get_persistenz_suppressions((0, 0))
    assert len(suppressions) == 1


def test_terrain_delta_roundtrip() -> None:
    baseline = generate_chunk(0, 0)
    delta = TerrainDelta(
        coord=(0, 0),
        tile_overrides=(TileOverride(TERRAIN_LAYER_ID, 1, 1, "wt:tiles/stone"),),
    )
    restored = apply_terrain_delta(baseline, delta)
    assert restored.get_key(1, 1, TERRAIN_LAYER_ID) == "wt:tiles/stone"
    payload = terrain_delta_to_dict(delta)
    parsed = terrain_delta_from_dict(payload)
    assert parsed == delta


def test_compute_terrain_delta_from_flags() -> None:
    snapshot = generate_chunk(1, 2)
    flags = PersistenzFlags.TILE_MODIFIED
    overrides = (TileOverride(TERRAIN_LAYER_ID, 0, 0, "wt:tiles/stone"),)
    delta = compute_terrain_delta(snapshot, flags, tile_overrides=overrides)
    assert delta is not None
    assert delta.coord == (1, 2)
    assert not is_persistenz_relevant(PersistenzFlags.NONE)
    assert compute_terrain_delta(snapshot, PersistenzFlags.NONE) is None


def test_overlay_delta_schema_slot() -> None:
    overlay = OverlayDelta(coord=(0, 0))
    assert overlay.schema_version == OVERLAY_DELTA_SCHEMA_VERSION


def test_semantically_inactive_queries_return_none() -> None:
    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(1, 1, "trees/oak", procedural=True)
    world.mark_semantically_inactive((0, 0))
    assert world.get_tile(1, 1) is None
    assert world.decoration_at_tile(1, 1) is None
