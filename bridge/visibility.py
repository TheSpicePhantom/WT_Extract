"""Kamera-basierte Chunk- und Tile-Sichtbarkeit — keine GPU-Abhängigkeiten."""

from __future__ import annotations

import math

from game_core.stream_view import StreamViewParams, viewport_world_bounds as core_viewport_bounds
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, CHUNK_SIZE_TILES, TILE_SIZE_PX, World
from render_scene.types import CameraData


def camera_world_bounds(camera: CameraData) -> tuple[float, float, float, float]:
    """Sichtbares Welt-Rechteck: left, right, bottom, top (Y-up)."""
    params = StreamViewParams(
        focus_x=camera.position_x,
        focus_y=camera.position_y,
        player_x=camera.position_x,
        player_y=camera.position_y,
        zoom=camera.zoom,
        viewport_w=camera.viewport_width,
        viewport_h=camera.viewport_height,
    )
    policy = StreamingConfig(max_half_chunks_cap=10_000)
    return core_viewport_bounds(params, policy)


def visible_chunk_coords(
    camera: CameraData,
    world: World,
    padding_chunks: int = 1,
) -> tuple[tuple[int, int], ...]:
    """Chunk-Indizes die das Kamera-Fenster schneiden (+ Padding)."""
    left, right, bottom, top = camera_world_bounds(camera)

    cx_min = math.floor(left / CHUNK_SIZE_PX) - padding_chunks
    cx_max = math.floor(right / CHUNK_SIZE_PX) + padding_chunks
    cy_min = math.floor(bottom / CHUNK_SIZE_PX) - padding_chunks
    cy_max = math.floor(top / CHUNK_SIZE_PX) + padding_chunks

    visible: list[tuple[int, int]] = []
    for cy in range(cy_min, cy_max + 1):
        for cx in range(cx_min, cx_max + 1):
            if (cx, cy) in world.chunks:
                visible.append((cx, cy))
    return tuple(visible)


def visible_tile_range_in_chunk(
    chunk_coord: tuple[int, int],
    camera: CameraData,
) -> tuple[int, int, int, int] | None:
    """Tile-Indizes (tx_min, tx_max, ty_min, ty_max) im Chunk die das Kamera-Fenster schneiden.

    None wenn kein Tile sichtbar ist (Chunk kann trotzdem per Padding in visible_chunk_coords sein).
    """
    left, right, bottom, top = camera_world_bounds(camera)
    cx, cy = chunk_coord
    chunk_origin_x = cx * CHUNK_SIZE_PX
    chunk_origin_y = cy * CHUNK_SIZE_PX

    if chunk_origin_x + CHUNK_SIZE_PX <= left or chunk_origin_x >= right:
        return None
    if chunk_origin_y + CHUNK_SIZE_PX <= bottom or chunk_origin_y >= top:
        return None

    tx_min = max(0, math.floor((left - chunk_origin_x) / TILE_SIZE_PX))
    tx_max = min(
        CHUNK_SIZE_TILES - 1,
        math.floor((right - chunk_origin_x - 1e-9) / TILE_SIZE_PX),
    )
    ty_min = max(0, math.floor((bottom - chunk_origin_y) / TILE_SIZE_PX))
    ty_max = min(
        CHUNK_SIZE_TILES - 1,
        math.floor((top - chunk_origin_y - 1e-9) / TILE_SIZE_PX),
    )

    if tx_min > tx_max or ty_min > ty_max:
        return None
    return tx_min, tx_max, ty_min, ty_max
