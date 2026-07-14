"""Demo: Texture Atlas — texturierte Sprites auf 32px-Tile-Grid."""

from __future__ import annotations

import sys

import glfw

from wt_platform.window import Window, WindowConfig
from render_core.policy import assert_gpu_only
from render_graphics.camera import camera_from_viewport
from render_graphics.instancing import demo_sprite_field
from render_graphics.ortho_renderer import OrthoFrameRenderer
from render_scene.types import RenderFrame, TILE_SIZE_PX

MOVE_SPEED = 480.0
ZOOM_SPEED = 1.8
WINDOW_TITLE_BASE = "WT Extract — Texture Atlas (GPU)"
FPS_UPDATE_INTERVAL = 0.5


class FpsCounter:
    """Glätteter FPS-Zähler für Fenstertitel."""

    def __init__(self, update_interval: float = FPS_UPDATE_INTERVAL) -> None:
        self._update_interval = update_interval
        self._elapsed = 0.0
        self._frames = 0
        self.fps = 0.0

    def tick(self, dt: float) -> bool:
        self._elapsed += dt
        self._frames += 1
        if self._elapsed < self._update_interval:
            return False
        self.fps = self._frames / self._elapsed
        self._elapsed = 0.0
        self._frames = 0
        return True

# Minecraft-Style Keys — stabil über Atlas-Rebakes
DEMO_SPRITE_KEYS = (
    "wt:tiles/grass",
    "wt:tiles/dirt",
    "wt:tiles/stone",
    "wt:items/gear",
    "wt:decoration/trees/pine",
    "wt:decoration/trees/oak",
    "wt:buildings/small",
    "wt:buildings/large",
    "wt:tiles/water",
    "wt:buildings/large",
    "wt:decoration/trees/oak",
    "wt:tiles/grass",
    "wt:decoration/trees/pine",
    "wt:buildings/small",
    "wt:tiles/stone",
    "wt:items/gear",
    "wt:tiles/dirt",
    "wt:tiles/water",
    "wt:buildings/large",
    "wt:decoration/trees/oak",
    "wt:tiles/grass",
    "wt:decoration/trees/pine",
    "wt:buildings/small",
    "wt:tiles/water",
    "wt:tiles/stone",
    "wt:items/gear",
    "wt:tiles/dirt",
    "wt:buildings/large",
    "wt:decoration/trees/oak",
    "wt:tiles/grass",
)


def main() -> int:
    assert_gpu_only("atlas_demo")

    window = Window(WindowConfig(title=WINDOW_TITLE_BASE, width=1280, height=720))
    window.focus()

    scroll_y = 0.0

    def on_scroll(_window, _xoffset: float, yoffset: float) -> None:
        nonlocal scroll_y
        scroll_y += yoffset

    glfw.set_scroll_callback(window.handle, on_scroll)

    try:
        renderer = OrthoFrameRenderer.create(window)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        print("Bake ausführen: python tools/bake_atlas.py --generate-placeholders", file=sys.stderr)
        window.destroy()
        return 1

    catalog = renderer.sprite_catalog
    sprites = demo_sprite_field(
        cols=6,
        rows=5,
        spacing=float(TILE_SIZE_PX) * 3,
        origin_x=-float(TILE_SIZE_PX) * 9,
        origin_y=-float(TILE_SIZE_PX) * 4,
        sprite_keys=DEMO_SPRITE_KEYS,
        catalog=catalog,
    )

    cam_x = 0.0
    cam_y = float(TILE_SIZE_PX) * 2
    zoom = 1.0
    last_time = glfw.get_time()
    fps_counter = FpsCounter()

    try:
        while not window.should_close:
            glfw.poll_events()

            now = glfw.get_time()
            dt = min(now - last_time, 0.05)
            last_time = now

            width, height = window.framebuffer_size
            if width < 1 or height < 1:
                continue

            if glfw.get_key(window.handle, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(window.handle, True)

            move = MOVE_SPEED * dt / max(zoom, 0.1)

            if _key(window, glfw.KEY_W, glfw.KEY_UP):
                cam_y += move
            if _key(window, glfw.KEY_S, glfw.KEY_DOWN):
                cam_y -= move
            if _key(window, glfw.KEY_A, glfw.KEY_LEFT):
                cam_x -= move
            if _key(window, glfw.KEY_D, glfw.KEY_RIGHT):
                cam_x += move

            if _key(window, glfw.KEY_E, glfw.KEY_PAGE_UP, glfw.KEY_KP_ADD):
                zoom *= ZOOM_SPEED ** dt
            if _key(window, glfw.KEY_Q, glfw.KEY_PAGE_DOWN, glfw.KEY_KP_SUBTRACT):
                zoom /= ZOOM_SPEED ** dt
            if _key(window, glfw.KEY_EQUAL):
                zoom *= ZOOM_SPEED ** dt
            if _key(window, glfw.KEY_MINUS):
                zoom /= ZOOM_SPEED ** dt

            if scroll_y != 0.0:
                zoom *= ZOOM_SPEED ** (scroll_y * 0.25)
                scroll_y = 0.0

            zoom = max(0.05, min(zoom, 32.0))

            camera = camera_from_viewport(cam_x, cam_y, zoom, width, height)
            renderer.draw(
                RenderFrame(
                    camera=camera,
                    sprites=sprites,
                    clear_color=(0.12, 0.13, 0.16, 1.0),
                )
            )

            if fps_counter.tick(dt):
                glfw.set_window_title(
                    window.handle,
                    f"{WINDOW_TITLE_BASE} | {fps_counter.fps:.0f} FPS",
                )
    finally:
        renderer.destroy()
        window.destroy()

    return 0


def _key(window: Window, primary: int, *alternatives: int) -> bool:
    handle = window.handle
    if glfw.get_key(handle, primary) == glfw.PRESS:
        return True
    return any(glfw.get_key(handle, key) == glfw.PRESS for key in alternatives)


if __name__ == "__main__":
    sys.exit(main())
