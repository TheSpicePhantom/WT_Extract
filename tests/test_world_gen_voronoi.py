"""Tests — Voronoi-Biomregion (M21)."""

from __future__ import annotations

import math

from game_core.world_gen import hash_cell, sample_biome_region, sample_sub_biome, seed_point_in_cell


def test_hash_cell_stable() -> None:
    assert hash_cell(3, 7, 42) == hash_cell(3, 7, 42)
    assert hash_cell(3, 7, 42) != hash_cell(3, 8, 42)


def test_seed_point_in_cell_bounds() -> None:
    cell_size = 96.0
    x, y = seed_point_in_cell(2, -1, cell_size, 99)
    assert 2 * cell_size <= x < 3 * cell_size
    assert -1 * cell_size <= y < 0 * cell_size


def test_biome_region_blend_range() -> None:
    region = sample_biome_region(150.0, 220.0)
    assert region.distance_1 <= region.distance_2
    assert 0.0 <= region.blend_t <= 1.0
    assert region.border_distance >= 0.0


def test_voronoi_seam_stable() -> None:
    wx, wy = 64.0, 128.0
    a = sample_biome_region(wx, wy)
    b = sample_biome_region(wx, wy)
    assert a.nearest_biome == b.nearest_biome
    assert math.isclose(a.blend_t, b.blend_t)


def test_sub_biome_sample_range() -> None:
    value = sample_sub_biome(10.0, 20.0)
    assert 0.0 <= value <= 1.0
    assert sample_sub_biome(10.0, 20.0) == sample_sub_biome(10.0, 20.0)
