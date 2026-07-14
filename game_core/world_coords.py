"""Welt-Koordinaten — Chunk/Region-Zuordnung mit floor_div (M24).

Persistenz-Semantik: 1 Tile = 1 m. Legacy-Code mappt Welt-Z auf tile wy.
"""

from __future__ import annotations

CHUNK_TILES = 64
REGION_CHUNKS = 8
REGION_SLOT_COUNT = REGION_CHUNKS * REGION_CHUNKS
TILE_METERS = 1.0


def floor_div(a: int, b: int) -> int:
    """Euklidische Floor-Division — identisch zu Python // für ints."""
    if b <= 0:
        raise ValueError("floor_div divisor must be positive")
    return a // b


def world_tile_to_chunk(tx: int, tz: int) -> tuple[int, int, int, int]:
    """Welt-Tile (tx, tz) → Chunk (cx, cz), lokales (local_tx, local_tz)."""
    cx = floor_div(tx, CHUNK_TILES)
    cz = floor_div(tz, CHUNK_TILES)
    local_tx = tx - cx * CHUNK_TILES
    local_tz = tz - cz * CHUNK_TILES
    return cx, cz, local_tx, local_tz


def chunk_to_region(
    cx: int,
    cz: int,
) -> tuple[int, int, int, int, int]:
    """Chunk → Region (rx, rz), Slot-Offset (slot_cx, slot_cz), slot_index 0..63."""
    rx = floor_div(cx, REGION_CHUNKS)
    rz = floor_div(cz, REGION_CHUNKS)
    slot_cx = cx - rx * REGION_CHUNKS
    slot_cz = cz - rz * REGION_CHUNKS
    slot_index = slot_cz * REGION_CHUNKS + slot_cx
    return rx, rz, slot_cx, slot_cz, slot_index


def region_filename(rx: int, rz: int) -> str:
    """Dateiname für Region-Blob: regions/r_<rx>_<rz>.bin"""
    return f"r_{rx}_{rz}.bin"
