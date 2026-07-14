"""Bildschirm → Weltkoordinaten — für Input in Demos (keine GPU-Abhängigkeit)."""

from __future__ import annotations

import math

from game_core.world import TILE_SIZE_PX
from render_scene.types import CameraData


def screen_to_world_px(
    camera: CameraData,
    screen_x: float,
    screen_y: float,
) -> tuple[float, float]:
    """Framebuffer-Pixel → Welt-Pixel (Y-up, Anker unten links)."""
    zoom = max(camera.zoom, 1e-6)
    vp_w = max(camera.viewport_width, 1)
    vp_h = max(camera.viewport_height, 1)
    half_w = (vp_w / zoom) * 0.5
    half_h = (vp_h / zoom) * 0.5

    left = camera.position_x - half_w
    right = camera.position_x + half_w
    bottom = camera.position_y - half_h
    top = camera.position_y + half_h

    u = screen_x / vp_w
    v = screen_y / vp_h
    world_x = left + u * (right - left)
    world_y = top - v * (top - bottom)
    return world_x, world_y


def screen_to_world_tile(
    camera: CameraData,
    screen_x: float,
    screen_y: float,
) -> tuple[int, int]:
    """Framebuffer-Pixel → Welt-Tile-Index (floor)."""
    world_x, world_y = screen_to_world_px(camera, screen_x, screen_y)
    return math.floor(world_x / TILE_SIZE_PX), math.floor(world_y / TILE_SIZE_PX)
