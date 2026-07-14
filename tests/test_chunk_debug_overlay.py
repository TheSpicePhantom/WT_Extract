"""Tests für optionale Chunk-Grenzen-Overlays."""

from __future__ import annotations

from render_graphics.chunk_debug_overlay import (
    ChunkOverlayLayer,
    build_overlay_vertices,
    loaded_chunks_layer,
    vertex_count,
    world_line_thickness,
)
from render_graphics.debug_grid import VERTEX_STRIDE

VERTICES_PER_CHUNK_EDGE = 6
EDGES_PER_CHUNK = 4


def test_empty_layers_produce_no_vertices() -> None:
    assert build_overlay_vertices([]) == b""
    assert build_overlay_vertices([loaded_chunks_layer([])]) == b""


def test_one_chunk_outline_vertex_count() -> None:
    layer = loaded_chunks_layer([(0, 0)])
    data = build_overlay_vertices([layer])
    expected = EDGES_PER_CHUNK * VERTICES_PER_CHUNK_EDGE
    assert vertex_count(data) == expected
    assert len(data) == expected * VERTEX_STRIDE


def test_multiple_layers_stack_vertices() -> None:
    layers = (
        ChunkOverlayLayer(chunks=frozenset({(0, 0)}), color=(1.0, 0.0, 0.0, 1.0), name="a"),
        ChunkOverlayLayer(chunks=frozenset({(1, 0)}), color=(0.0, 1.0, 0.0, 1.0), name="b"),
    )
    data = build_overlay_vertices(layers)
    assert vertex_count(data) == 2 * EDGES_PER_CHUNK * VERTICES_PER_CHUNK_EDGE


def test_duplicate_coords_in_one_layer_draw_once() -> None:
    layer = ChunkOverlayLayer(chunks=frozenset({(0, 0)}))
    data = build_overlay_vertices([layer, layer])
    assert vertex_count(data) == EDGES_PER_CHUNK * VERTICES_PER_CHUNK_EDGE * 2


def test_zoom_scales_world_line_thickness() -> None:
    layer = loaded_chunks_layer([(0, 0)])
    near = build_overlay_vertices([layer], zoom=1.0)
    far = build_overlay_vertices([layer], zoom=0.1)
    assert world_line_thickness(2.5, 1.0) == 2.5
    assert world_line_thickness(2.5, 0.1) == 25.0
    assert len(near) == len(far)
    assert near != far
