"""Tests — Platform Input (M20)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from wt_platform.input import InputFrame, InputState, ctrl_combo_pressed, key_held, key_pressed


def test_key_held_with_alias() -> None:
    frame = InputFrame(
        keys_held=frozenset({"UP"}),
        keys_pressed=frozenset(),
        ctrl_held=False,
        shift_held=False,
        mouse_left=False,
        mouse_right=False,
        scroll_delta=0.0,
        cursor_fb=(100.0, 200.0),
        escape=False,
        should_close=False,
    )
    assert key_held(frame, "W")
    assert not key_held(frame, "S")


def test_key_pressed_rising_edge() -> None:
    frame = InputFrame(
        keys_held=frozenset({"F"}),
        keys_pressed=frozenset({"F"}),
        ctrl_held=False,
        shift_held=False,
        mouse_left=False,
        mouse_right=False,
        scroll_delta=0.0,
        cursor_fb=(0.0, 0.0),
        escape=False,
        should_close=False,
    )
    assert key_pressed(frame, "F")
    assert not key_pressed(frame, "1")


def test_ctrl_combo_pressed() -> None:
    frame = InputFrame(
        keys_held=frozenset({"S", "LEFT_CONTROL"}),
        keys_pressed=frozenset({"S"}),
        ctrl_held=True,
        shift_held=False,
        mouse_left=False,
        mouse_right=False,
        scroll_delta=0.0,
        cursor_fb=(0.0, 0.0),
        escape=False,
        should_close=False,
    )
    assert ctrl_combo_pressed(frame, "S")
    assert not ctrl_combo_pressed(frame, "L")


def test_input_state_poll_scroll_and_cursor() -> None:
    window = MagicMock()
    window.handle = MagicMock()
    window.should_close = False
    window.framebuffer_size = (1920, 1080)

    with patch("wt_platform.input.glfw") as glfw_mock:
        glfw_mock.PRESS = 1
        glfw_mock.set_scroll_callback = MagicMock()
        glfw_mock.get_key.return_value = 0
        glfw_mock.get_mouse_button.return_value = 0
        glfw_mock.get_cursor_pos.return_value = (640.0, 360.0)
        glfw_mock.get_window_size.return_value = (1280, 720)

        state = InputState(window)
        state._scroll_pending = 2.0
        frame = state.poll()

    assert frame.scroll_delta == 2.0
    assert frame.cursor_fb == (960.0, 540.0)
    window.poll_events.assert_called_once()
