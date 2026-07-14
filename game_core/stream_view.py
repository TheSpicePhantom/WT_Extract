"""Viewport-/Streaming-Mengen — reine Mathe in game_core (M22d)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX

Coord = tuple[int, int]


def focus_to_chunk(focus_x: float, focus_y: float) -> Coord:
    """Welt-Pixel → Chunk-Index (cx, cy)."""
    cx = math.floor(focus_x / CHUNK_SIZE_PX)
    cy = math.floor(focus_y / CHUNK_SIZE_PX)
    return int(cx), int(cy)


def coords_in_radius(center: Coord, radius: int) -> set[Coord]:
    """Chebyshev-Radius — max(|dx|, |dy|) <= radius."""
    cx, cy = center
    coords: set[Coord] = set()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if max(abs(dx), abs(dy)) <= radius:
                coords.add((cx + dx, cy + dy))
    return coords


def chebyshev_distance(a: Coord, b: Coord) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


@dataclass(frozen=True, slots=True)
class StreamViewParams:
    focus_x: float
    focus_y: float
    player_x: float
    player_y: float
    zoom: float
    viewport_w: int
    viewport_h: int
    move_dx: float = 0.0
    move_dy: float = 0.0


@dataclass(frozen=True, slots=True)
class StreamSets:
    visible: frozenset[Coord]
    wanted: frozenset[Coord]
    keep: frozenset[Coord]
    prefetch: frozenset[Coord]


def viewport_world_bounds(
    params: StreamViewParams,
    policy: StreamingConfig,
) -> tuple[float, float, float, float]:
    """Sichtbares Welt-Rechteck: left, right, bottom, top (Y-up)."""
    zoom = max(params.zoom, policy.min_zoom)
    vp_w = max(params.viewport_w, 1)
    vp_h = max(params.viewport_h, 1)
    half_w = (vp_w / zoom) * 0.5
    half_h = (vp_h / zoom) * 0.5
    max_half_px = policy.max_half_chunks_cap * CHUNK_SIZE_PX
    half_w = min(half_w, max_half_px)
    half_h = min(half_h, max_half_px)
    left = params.focus_x - half_w
    right = params.focus_x + half_w
    bottom = params.focus_y - half_h
    top = params.focus_y + half_h
    return left, right, bottom, top


def chunks_in_aabb(cx_min: int, cx_max: int, cy_min: int, cy_max: int) -> set[Coord]:
    coords: set[Coord] = set()
    for cy in range(cy_min, cy_max + 1):
        for cx in range(cx_min, cx_max + 1):
            coords.add((cx, cy))
    return coords


def chunks_in_viewport(params: StreamViewParams, policy: StreamingConfig) -> set[Coord]:
    left, right, bottom, top = viewport_world_bounds(params, policy)
    pad = policy.viewport_padding_chunks
    cx_min = math.floor(left / CHUNK_SIZE_PX) - pad
    cx_max = math.floor(right / CHUNK_SIZE_PX) + pad
    cy_min = math.floor(bottom / CHUNK_SIZE_PX) - pad
    cy_max = math.floor(top / CHUNK_SIZE_PX) + pad
    return chunks_in_aabb(cx_min, cx_max, cy_min, cy_max)


def player_safety_ring(params: StreamViewParams, policy: StreamingConfig) -> set[Coord]:
    player_chunk = focus_to_chunk(params.player_x, params.player_y)
    return coords_in_radius(player_chunk, policy.player_safety_ring)


def expand_aabb(coords: set[Coord], padding: int) -> set[Coord]:
    if not coords or padding <= 0:
        return set(coords)
    cx_min = min(coord[0] for coord in coords)
    cx_max = max(coord[0] for coord in coords)
    cy_min = min(coord[1] for coord in coords)
    cy_max = max(coord[1] for coord in coords)
    return chunks_in_aabb(
        cx_min - padding,
        cx_max + padding,
        cy_min - padding,
        cy_max + padding,
    )


def cap_by_distance(
    coords: set[Coord],
    center: Coord,
    max_count: int,
) -> set[Coord]:
    if max_count <= 0 or len(coords) <= max_count:
        return set(coords)
    ranked = sorted(coords, key=lambda coord: (chebyshev_distance(coord, center), coord))
    return set(ranked[:max_count])


def prefetch_strip(
    keep: set[Coord],
    params: StreamViewParams,
    policy: StreamingConfig,
) -> set[Coord]:
    if policy.prefetch_chunks <= 0 or not keep:
        return set()
    if math.hypot(params.move_dx, params.move_dy) < policy.prefetch_min_speed_px:
        return set()

    cx_min = min(coord[0] for coord in keep)
    cx_max = max(coord[0] for coord in keep)
    cy_min = min(coord[1] for coord in keep)
    cy_max = max(coord[1] for coord in keep)
    strip: set[Coord] = set()

    if abs(params.move_dx) >= abs(params.move_dy):
        step = 1 if params.move_dx >= 0 else -1
        edge_cx = cx_max if step > 0 else cx_min
        for offset in range(1, policy.prefetch_chunks + 1):
            cx = edge_cx + step * offset
            for cy in range(cy_min, cy_max + 1):
                strip.add((cx, cy))
    else:
        step = 1 if params.move_dy >= 0 else -1
        edge_cy = cy_max if step > 0 else cy_min
        for offset in range(1, policy.prefetch_chunks + 1):
            cy = edge_cy + step * offset
            for cx in range(cx_min, cx_max + 1):
                strip.add((cx, cy))
    return strip


def compute_stream_sets(
    params: StreamViewParams,
    policy: StreamingConfig,
) -> StreamSets:
    if policy.mode == "radius":
        center = focus_to_chunk(params.focus_x, params.focus_y)
        wanted = coords_in_radius(center, policy.load_radius)
        keep = coords_in_radius(center, policy.unload_radius)
        frozen_wanted = frozenset(wanted)
        return StreamSets(
            visible=frozen_wanted,
            wanted=frozen_wanted,
            keep=frozenset(keep),
            prefetch=frozenset(),
        )

    visible = chunks_in_viewport(params, policy)
    safety = player_safety_ring(params, policy)
    focus_chunk = focus_to_chunk(params.focus_x, params.focus_y)
    wanted = cap_by_distance(visible | safety, focus_chunk, policy.max_loaded_chunks)
    keep = expand_aabb(wanted, policy.keep_padding_chunks)
    prefetch = prefetch_strip(keep, params, policy) - wanted
    return StreamSets(
        visible=frozenset(visible),
        wanted=frozenset(wanted),
        keep=frozenset(keep),
        prefetch=frozenset(prefetch),
    )
