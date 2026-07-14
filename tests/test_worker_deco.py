"""Tests — Deko-Extraktion (M22e Phase 1)."""

from __future__ import annotations

from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.world_gen import compute_procedural_decorations
from game_core.world_gen_context import WorldGenContext
from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def test_compute_deco_matches_populate() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = WorldGenContext.from_active()
    known_ids = frozenset(content.decoration_ids())

    for coord in REFERENCE_TEST_COORDS:
        ref = sequential_reference_chunk(coord, content, collision)
        cx, cy = coord
        computed = compute_procedural_decorations(
            cx, cy, ctx=ctx, known_decoration_ids=known_ids
        )
        computed_sorted = tuple(
            sorted(computed, key=lambda item: (item.wy, item.wx, item.decoration_id))
        )
        ref_sorted = tuple(
            (d.wx, d.wy, d.decoration_id)
            for d in ref.procedural_decorations
        )
        assert len(computed_sorted) == len(ref.procedural_decorations)
        for placement, ref_deco in zip(computed_sorted, ref.procedural_decorations, strict=True):
            assert placement.wx == ref_deco.wx
            assert placement.wy == ref_deco.wy
            assert placement.decoration_id == ref_deco.decoration_id


def test_known_decoration_filter_equivalent() -> None:
    content = load_content_registry()
    ctx = WorldGenContext.from_active()
    known_ids = frozenset(content.decoration_ids())
    placements = compute_procedural_decorations(0, 0, ctx=ctx, known_decoration_ids=known_ids)
    for placement in placements:
        assert content.decoration_by_id(placement.decoration_id) is not None
