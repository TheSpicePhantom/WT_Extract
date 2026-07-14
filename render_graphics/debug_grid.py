"""Welt-Raster als GPU-Vertexdaten — zur Visualisierung der orthographischen Kamera."""

from __future__ import annotations

import struct

# Vertex: vec2 position + vec4 color (24 bytes)
VERTEX_STRIDE = 24


def _vertex(x: float, y: float, r: float, g: float, b: float, a: float = 1.0) -> tuple[float, ...]:
    return (x, y, r, g, b, a)


def _append_quad(
    vertices: list[tuple[float, ...]],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: tuple[float, float, float, float],
) -> None:
    r, g, b, a = color
    vertices.extend(
        [
            _vertex(x0, y0, r, g, b, a),
            _vertex(x1, y0, r, g, b, a),
            _vertex(x1, y1, r, g, b, a),
            _vertex(x0, y0, r, g, b, a),
            _vertex(x1, y1, r, g, b, a),
            _vertex(x0, y1, r, g, b, a),
        ]
    )


def _append_line_quad(
    vertices: list[tuple[float, ...]],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    thickness: float,
    color: tuple[float, float, float, float],
) -> None:
    """Achsenparallele oder schräge Linie als gefülltes Quad (GPU-Dreiecke)."""
    half = thickness * 0.5
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return

    # Horizontal/vertikal: _append_quad braucht unterschiedliche x0!=x1 und y0!=y1.
    if abs(dy) < 1e-6:
        left = min(x0, x1)
        right = max(x0, x1)
        y = y0
        _append_quad(vertices, left, y - half, right, y + half, color)
        return

    if abs(dx) < 1e-6:
        bottom = min(y0, y1)
        top = max(y0, y1)
        x = x0
        _append_quad(vertices, x - half, bottom, x + half, top, color)
        return

    length = (dx * dx + dy * dy) ** 0.5
    nx = -dy / length * half
    ny = dx / length * half
    r, g, b, a = color
    vertices.extend(
        [
            _vertex(x0 + nx, y0 + ny, r, g, b, a),
            _vertex(x1 + nx, y1 + ny, r, g, b, a),
            _vertex(x1 - nx, y1 - ny, r, g, b, a),
            _vertex(x0 + nx, y0 + ny, r, g, b, a),
            _vertex(x1 - nx, y1 - ny, r, g, b, a),
            _vertex(x0 - nx, y0 - ny, r, g, b, a),
        ]
    )


append_line_quad = _append_line_quad


def build_world_grid_vertices(
    span: float = 512.0,
    step: float = 32.0,
    line_thickness: float = 1.5,
) -> bytes:
    """Erzeugt ein Weltkoordinaten-Raster (GPU-Vertex-Bytes)."""
    vertices: list[tuple[float, ...]] = []
    grid_color = (0.45, 0.48, 0.52, 1.0)
    axis_x_color = (0.95, 0.25, 0.25, 1.0)
    axis_y_color = (0.25, 0.85, 0.35, 1.0)
    marker_color = (0.98, 0.82, 0.15, 1.0)

    pos = -span
    while pos <= span + 1e-6:
        color = grid_color
        thickness = line_thickness
        if abs(pos) < 1e-6:
            pos += step
            continue
        _append_line_quad(vertices, -span, pos, span, pos, thickness, color)
        _append_line_quad(vertices, pos, -span, pos, span, thickness, color)
        pos += step

    _append_line_quad(vertices, -span, 0.0, span, 0.0, line_thickness * 1.5, axis_x_color)
    _append_line_quad(vertices, 0.0, -span, 0.0, span, line_thickness * 1.5, axis_y_color)

    _append_quad(vertices, 80.0, 40.0, 140.0, 100.0, marker_color)
    _append_quad(vertices, -200.0, -120.0, -120.0, -60.0, (0.35, 0.55, 0.95, 1.0))

    flat: list[float] = [value for vertex in vertices for value in vertex]
    return struct.pack(f"{len(flat)}f", *flat)


def vertex_count(vertex_bytes: bytes) -> int:
    return len(vertex_bytes) // VERTEX_STRIDE
