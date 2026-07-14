"""Data-driven Tile-Pinsel — Input → Tile-Key aus Content-Registry."""

from __future__ import annotations

from game_core.content_registry import ContentRegistry, TileBrushPalette
from game_core.world import World
from wt_platform.input import InputFrame, key_held


def apply_tile_brush_palette(
    world: World,
    palette: TileBrushPalette,
    input_frame: InputFrame,
    wx: int,
    wy: int,
) -> bool:
    """Wendet alle aktiven Pinsel-Inputs der Palette auf (wx, wy) an."""
    changed = False

    if palette.mouse_left and input_frame.mouse_left:
        if world.set_tile(wx, wy, palette.mouse_left, layer=palette.layer):
            changed = True

    if palette.mouse_right and input_frame.mouse_right:
        if world.set_tile(wx, wy, palette.mouse_right, layer=palette.layer):
            changed = True

    for key_name, sprite_key in palette.key_bindings:
        if key_held(input_frame, key_name):
            if world.set_tile(wx, wy, sprite_key, layer=palette.layer):
                changed = True

    return changed


def apply_paint_at_cursor(
    world: World,
    content: ContentRegistry,
    paint_mode: str,
    camera,
    input_frame: InputFrame,
) -> bool:
    """Free-Cam-Pinsel — Modus wählt Palette aus der Registry."""
    from bridge.screen_to_world import screen_to_world_tile

    palette = content.brush_palette(paint_mode)
    if palette is None:
        return False

    screen_x, screen_y = input_frame.cursor_fb
    wx, wy = screen_to_world_tile(camera, screen_x, screen_y)
    return apply_tile_brush_palette(world, palette, input_frame, wx, wy)


def palette_label(content: ContentRegistry, palette: TileBrushPalette) -> str:
    """Kurzbeschreibung für Fenstertitel — z. B. L0 stone/grass R=dirt."""
    parts: list[str] = [f"L{palette.layer}"]
    if palette.mouse_left:
        parts.append(f"LMB={content.tile_label(palette.mouse_left)}")
    if palette.mouse_right:
        parts.append(f"RMB={content.tile_label(palette.mouse_right)}")
    for key_name, sprite_key in palette.key_bindings:
        label = "clear" if not sprite_key else content.tile_label(sprite_key)
        parts.append(f"{key_name}={label}")
    return " ".join(parts)
