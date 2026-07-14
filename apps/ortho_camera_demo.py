"""Demo: Orthographische GPU-Kamera mit pan/zoom (WASD + Mausrad)."""

from __future__ import annotations

import sys

import glfw

from wt_platform.window import Window, WindowConfig
from render_core.policy import assert_gpu_only
from render_graphics.camera import camera_from_viewport
from render_graphics.ortho_renderer import OrthoFrameRenderer
from render_scene.types import RenderFrame

MOVE_SPEED = 480.0
ZOOM_SPEED = 1.8


def main() -> int:
    assert_gpu_only("ortho_camera_demo")

    window = Window(WindowConfig(title="WT Extract — Ortho Camera (GPU)", width=1280, height=720))
    window.focus()

    scroll_y = 0.0

    def on_scroll(_window, _xoffset: float, yoffset: float) -> None:
        nonlocal scroll_y
        scroll_y += yoffset

    glfw.set_scroll_callback(window.handle, on_scroll)

    renderer = OrthoFrameRenderer.create(window)

    cam_x = 0.0
    cam_y = 0.0
    zoom = 1.0
    last_time = glfw.get_time()

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
            renderer.draw(RenderFrame(camera=camera, clear_color=(0.12, 0.13, 0.16, 1.0)))
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
