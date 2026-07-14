"""GLFW-Fenster ohne OpenGL — Surface wird von Vulkan (GPU) erstellt."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import glfw


@dataclass(frozen=True, slots=True)
class WindowConfig:
    title: str = "WT Extract"
    width: int = 1280
    height: int = 720
    resizable: bool = True


class Window:
    """OS-Fenster; Rendering erfolgt ausschließlich über Vulkan auf der GPU."""

    def __init__(self, config: WindowConfig | None = None) -> None:
        self._config = config or WindowConfig()
        self._owns_glfw = False
        self._window = self._create_window()
        self._fullscreen = False
        self._windowed_x = 100
        self._windowed_y = 100
        self._windowed_w = self._config.width
        self._windowed_h = self._config.height
        self._resize_callbacks: list[Callable[[int, int], None]] = []
        glfw.set_framebuffer_size_callback(self._window, self._on_framebuffer_resize)

    def _create_window(self):
        if not glfw.init():
            raise RuntimeError("GLFW konnte nicht initialisiert werden.")

        self._owns_glfw = True
        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE if self._config.resizable else glfw.FALSE)

        window = glfw.create_window(
            self._config.width,
            self._config.height,
            self._config.title,
            None,
            None,
        )
        if window is None:
            glfw.terminate()
            raise RuntimeError("GLFW-Fenster konnte nicht erstellt werden.")

        return window

    def _on_framebuffer_resize(self, _window, width: int, height: int) -> None:
        fb_w, fb_h = int(width), int(height)
        if fb_w < 1 or fb_h < 1:
            return
        for callback in self._resize_callbacks:
            callback(fb_w, fb_h)

    def on_framebuffer_resized(self, callback: Callable[[int, int], None]) -> None:
        """Registriert Callback bei Framebuffer-Größenänderung (Resize, HiDPI, Vollbild)."""
        self._resize_callbacks.append(callback)

    def set_window_title(self, title: str) -> None:
        glfw.set_window_title(self._window, title)

    def request_close(self) -> None:
        glfw.set_window_should_close(self._window, True)

    @property
    def handle(self):
        return self._window

    @property
    def is_fullscreen(self) -> bool:
        return self._fullscreen

    @property
    def framebuffer_size(self) -> tuple[int, int]:
        width, height = glfw.get_framebuffer_size(self._window)
        return int(width), int(height)

    @property
    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self._window))

    def poll_events(self) -> None:
        glfw.poll_events()

    def focus(self) -> None:
        glfw.focus_window(self._window)

    def toggle_fullscreen(self) -> bool:
        """Wechselt Fenster- ↔ borderless Vollbild. Returns neuer Modus."""
        if self._window is None:
            return self._fullscreen

        if self._fullscreen:
            glfw.set_window_monitor(
                self._window,
                None,
                self._windowed_x,
                self._windowed_y,
                self._windowed_w,
                self._windowed_h,
                glfw.DONT_CARE,
            )
            self._fullscreen = False
        else:
            self._windowed_x, self._windowed_y = glfw.get_window_pos(self._window)
            self._windowed_w, self._windowed_h = glfw.get_window_size(self._window)
            monitor = glfw.get_primary_monitor()
            if monitor is None:
                return self._fullscreen
            mode = glfw.get_video_mode(monitor)
            if mode is None:
                return self._fullscreen
            monitor_x, monitor_y = glfw.get_monitor_pos(monitor)
            glfw.set_window_monitor(
                self._window,
                None,
                monitor_x,
                monitor_y,
                mode.size.width,
                mode.size.height,
                glfw.DONT_CARE,
            )
            self._fullscreen = True

        self._wait_for_framebuffer_stable()
        return self._fullscreen

    def _wait_for_framebuffer_stable(self, max_polls: int = 64) -> tuple[int, int]:
        """Poll bis Framebuffer-Größe nach Resize stabil ist (Windows/HiDPI)."""
        last = (-1, -1)
        stable_reads = 0
        for _ in range(max_polls):
            glfw.poll_events()
            current = self.framebuffer_size
            if current[0] >= 1 and current[1] >= 1 and current == last:
                stable_reads += 1
                if stable_reads >= 2:
                    return current
            else:
                stable_reads = 0
            last = current
        return self.framebuffer_size

    def destroy(self) -> None:
        if self._window is not None:
            glfw.destroy_window(self._window)
            self._window = None
        if self._owns_glfw:
            glfw.terminate()
            self._owns_glfw = False

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.destroy()
