"""Tests — Welt-Koordinaten floor_div / Chunk / Region (M24 Phase 1)."""

from __future__ import annotations

import pytest

from game_core.world_coords import (
    CHUNK_TILES,
    REGION_CHUNKS,
    REGION_SLOT_COUNT,
    chunk_to_region,
    floor_div,
    region_filename,
    world_tile_to_chunk,
)


def test_floor_div_negative() -> None:
    assert floor_div(-1, 64) == -1
    assert floor_div(-64, 64) == -1
    assert floor_div(-65, 64) == -2
    assert floor_div(0, 64) == 0
    assert floor_div(63, 64) == 0
    assert floor_div(64, 64) == 1


def test_world_tile_negative_corner() -> None:
    cx, cz, lx, lz = world_tile_to_chunk(-1, -1)
    assert (cx, cz) == (-1, -1)
    assert (lx, lz) == (63, 63)


def test_world_tile_negative_boundary() -> None:
    cx, cz, lx, lz = world_tile_to_chunk(-64, 0)
    assert (cx, cz) == (-1, 0)
    assert (lx, lz) == (0, 0)

    cx, cz, lx, lz = world_tile_to_chunk(-65, 0)
    assert (cx, cz) == (-2, 0)
    assert (lx, lz) == (63, 0)


def test_chunk_to_region_negative() -> None:
    rx, rz, scx, scz, idx = chunk_to_region(-8, 0)
    assert (rx, rz) == (-1, 0)
    assert (scx, scz) == (0, 0)
    assert idx == 0


@pytest.mark.parametrize(
    ("slot_cx", "slot_cz", "expected_index"),
    [(cx, cz, cz * REGION_CHUNKS + cx) for cz in range(REGION_CHUNKS) for cx in range(REGION_CHUNKS)],
)
def test_all_region_slot_indices(slot_cx: int, slot_cz: int, expected_index: int) -> None:
    cx = slot_cx
    cz = slot_cz
    _, _, out_scx, out_scz, idx = chunk_to_region(cx, cz)
    assert (out_scx, out_scz) == (slot_cx, slot_cz)
    assert idx == expected_index
    assert 0 <= idx < REGION_SLOT_COUNT


def test_quadrants_around_origin() -> None:
    cases = [
        ((64, 64), (1, 1)),
        ((-1, 64), (-1, 1)),
        ((-1, -1), (-1, -1)),
        ((64, -1), (1, -1)),
    ]
    for (tx, tz), (exp_cx, exp_cz) in cases:
        cx, cz, _, _ = world_tile_to_chunk(tx, tz)
        assert (cx, cz) == (exp_cx, exp_cz)


def test_region_filename_negative() -> None:
    assert region_filename(-1, 0) == "r_-1_0.bin"
    assert region_filename(3, -2) == "r_3_-2.bin"
