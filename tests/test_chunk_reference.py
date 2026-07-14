"""Tests — Golden-Referenzpfad (M22e Phase 0)."""

from __future__ import annotations

from game_core.collision_catalog import load_collision_catalog
from game_core.collision_grid import CHUNK_SOLID_GRID_BYTES
from game_core.world import CHUNK_TILE_COUNT
from game_core.content_registry import load_content_registry
from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def test_sequential_reference_chunk_stable() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    for coord in REFERENCE_TEST_COORDS:
        first = sequential_reference_chunk(coord, content, collision)
        second = sequential_reference_chunk(coord, content, collision)
        assert first == second
        assert len(first.layer0) == CHUNK_TILE_COUNT
        assert len(first.solid_grid) == CHUNK_SOLID_GRID_BYTES


def test_reference_decorations_sorted() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ref = sequential_reference_chunk((3, 3), content, collision)
    order = [(d.wy, d.wx, d.decoration_id) for d in ref.procedural_decorations]
    assert order == sorted(order)
