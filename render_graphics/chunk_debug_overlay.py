"""Optionale Chunk-Grenzen für Debug — erweiterbar via ChunkOverlayLayer."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Iterable, Sequence

from game_core.world import CHUNK_SIZE_PX
from render_graphics.debug_grid import VERTEX_STRIDE, append_line_quad

Coord = tuple[int, int]
Rgba = tuple[float, float, float, float]

# Standard: geladene Chunks (Option C)
LOADED_CHUNK_COLOR: Rgba = (0.95, 0.35, 0.85, 0.95)
DEFAULT_SCREEN_LINE_PX = 2.5


@dataclass(frozen=True, slots=True)
class ChunkOverlayLayer:
    """Eine überlagerte Chunk-Menge — mehrere Layer kombinierbar (z. B. loaded + wanted)."""

    chunks: frozenset[Coord]
    color: Rgba = LOADED_CHUNK_COLOR
    screen_line_px: float = DEFAULT_SCREEN_LINE_PX
    name: str = "loaded"


def loaded_chunks_layer(chunks: Iterable[Coord]) -> ChunkOverlayLayer:
    return ChunkOverlayLayer(chunks=frozenset(chunks), name="loaded")


def chunk_world_rect(cx: int, cy: int) -> tuple[int, int, int, int]:
    """Chunk-Rechteck in Welt-Pixeln: (x0, y0, x1, y1), identisch zur Tile-Platzierung."""
    x0 = cx * CHUNK_SIZE_PX
    y0 = cy * CHUNK_SIZE_PX
    return x0, y0, x0 + CHUNK_SIZE_PX, y0 + CHUNK_SIZE_PX


def world_line_thickness(screen_px: float, zoom: float) -> float:
    """Konstante Bildschirmbreite — world_thickness * zoom ≈ screen_px."""
    return max(screen_px, 0.5) / max(zoom, 1e-6)


def _append_chunk_outline(
    vertices: list[tuple[float, ...]],
    cx: int,
    cy: int,
    *,
    thickness: float,
    color: Rgba,
) -> None:
    x0, y0, x1, y1 = chunk_world_rect(cx, cy)
    fx0, fy0, fx1, fy1 = float(x0), float(y0), float(x1), float(y1)
    append_line_quad(vertices, fx0, fy0, fx1, fy0, thickness, color)
    append_line_quad(vertices, fx1, fy0, fx1, fy1, thickness, color)
    append_line_quad(vertices, fx1, fy1, fx0, fy1, thickness, color)
    append_line_quad(vertices, fx0, fy1, fx0, fy0, thickness, color)


def build_overlay_vertices(
    layers: Sequence[ChunkOverlayLayer],
    *,
    zoom: float = 1.0,
) -> bytes:
    """Kombiniert alle Layer zu GPU-Vertex-Bytes (leer wenn keine Chunks)."""
    vertices: list[tuple[float, ...]] = []
    for layer in layers:
        if not layer.chunks:
            continue
        thickness = world_line_thickness(layer.screen_line_px, zoom)
        for cx, cy in sorted(layer.chunks):
            _append_chunk_outline(
                vertices,
                cx,
                cy,
                thickness=thickness,
                color=layer.color,
            )
    if not vertices:
        return b""
    flat: list[float] = [value for vertex in vertices for value in vertex]
    return struct.pack(f"{len(flat)}f", *flat)


def vertex_count(vertex_bytes: bytes) -> int:
    if not vertex_bytes:
        return 0
    return len(vertex_bytes) // VERTEX_STRIDE
