"""Zentraler Input-State — GLFW-Abstraktion für Apps (kein Gameplay)."""

from __future__ import annotations

from dataclasses import dataclass

import glfw

from wt_platform.window import Window

# A–Z
_LETTER_KEYS: dict[str, int] = {chr(code): getattr(glfw, f"KEY_{chr(code)}") for code in range(ord("A"), ord("Z") + 1)}

_NAMED_KEYS: dict[str, int] = {
    **_LETTER_KEYS,
    "ESCAPE": glfw.KEY_ESCAPE,
    "F11": glfw.KEY_F11,
    "LEFT_SHIFT": glfw.KEY_LEFT_SHIFT,
    "RIGHT_SHIFT": glfw.KEY_RIGHT_SHIFT,
    "LEFT_CONTROL": glfw.KEY_LEFT_CONTROL,
    "RIGHT_CONTROL": glfw.KEY_RIGHT_CONTROL,
    "UP": glfw.KEY_UP,
    "DOWN": glfw.KEY_DOWN,
    "LEFT": glfw.KEY_LEFT,
    "RIGHT": glfw.KEY_RIGHT,
    "PAGE_UP": glfw.KEY_PAGE_UP,
    "PAGE_DOWN": glfw.KEY_PAGE_DOWN,
    "EQUAL": glfw.KEY_EQUAL,
    "MINUS": glfw.KEY_MINUS,
    "LEFT_BRACKET": glfw.KEY_LEFT_BRACKET,
    "RIGHT_BRACKET": glfw.KEY_RIGHT_BRACKET,
    "KP_ADD": glfw.KEY_KP_ADD,
    "KP_SUBTRACT": glfw.KEY_KP_SUBTRACT,
    "1": glfw.KEY_1,
    "2": glfw.KEY_2,
    "3": glfw.KEY_3,
}

# Aliase für Demo-Logik
_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "W": ("UP",),
    "S": ("DOWN",),
    "A": ("LEFT",),
    "D": ("RIGHT",),
    "E": ("PAGE_UP", "KP_ADD"),
    "Q": ("PAGE_DOWN", "KP_SUBTRACT"),
    "SHIFT": ("LEFT_SHIFT", "RIGHT_SHIFT"),
    "CTRL": ("LEFT_CONTROL", "RIGHT_CONTROL"),
}


@dataclass(frozen=True, slots=True)
class InputFrame:
    keys_held: frozenset[str]
    keys_pressed: frozenset[str]
    ctrl_held: bool
    shift_held: bool
    mouse_left: bool
    mouse_right: bool
    scroll_delta: float
    cursor_fb: tuple[float, float]
    escape: bool
    should_close: bool


def key_held(frame: InputFrame, name: str) -> bool:
    """Taste gehalten — inkl. Aliase (W → UP)."""
    upper = name.upper()
    if upper in frame.keys_held:
        return True
    for alias in _KEY_ALIASES.get(upper, ()):
        if alias in frame.keys_held:
            return True
    return False


def key_pressed(frame: InputFrame, name: str) -> bool:
    """Rising edge — inkl. Aliase."""
    upper = name.upper()
    if upper in frame.keys_pressed:
        return True
    for alias in _KEY_ALIASES.get(upper, ()):
        if alias in frame.keys_pressed:
            return True
    return False


def ctrl_combo_pressed(frame: InputFrame, name: str) -> bool:
    """Strg+Taste — Rising edge."""
    return frame.ctrl_held and key_pressed(frame, name)


class InputState:
    """Sammelt GLFW-Input pro Frame — ein Poll-Punkt für Apps."""

    def __init__(self, window: Window) -> None:
        self._window = window
        self._prev_held: frozenset[str] = frozenset()
        self._scroll_pending = 0.0
        glfw.set_scroll_callback(window.handle, self._on_scroll)

    def _on_scroll(self, _window, _xoffset: float, yoffset: float) -> None:
        self._scroll_pending += yoffset

    def poll(self) -> InputFrame:
        self._window.poll_events()
        handle = self._window.handle

        held: set[str] = set()
        for name, glfw_key in _NAMED_KEYS.items():
            if glfw.get_key(handle, glfw_key) == glfw.PRESS:
                held.add(name)

        pressed = frozenset(held - set(self._prev_held))
        self._prev_held = frozenset(held)

        scroll = self._scroll_pending
        self._scroll_pending = 0.0

        return InputFrame(
            keys_held=frozenset(held),
            keys_pressed=pressed,
            ctrl_held="LEFT_CONTROL" in held or "RIGHT_CONTROL" in held,
            shift_held="LEFT_SHIFT" in held or "RIGHT_SHIFT" in held,
            mouse_left=glfw.get_mouse_button(handle, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS,
            mouse_right=glfw.get_mouse_button(handle, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS,
            scroll_delta=scroll,
            cursor_fb=_framebuffer_cursor(self._window),
            escape="ESCAPE" in held,
            should_close=self._window.should_close,
        )


def _framebuffer_cursor(window: Window) -> tuple[float, float]:
    cursor_x, cursor_y = glfw.get_cursor_pos(window.handle)
    fb_w, fb_h = window.framebuffer_size
    win_w, win_h = glfw.get_window_size(window.handle)
    if win_w < 1 or win_h < 1:
        return cursor_x, cursor_y
    return cursor_x * fb_w / win_w, cursor_y * fb_h / win_h
