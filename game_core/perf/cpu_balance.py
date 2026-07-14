"""M25d — CPU-Full-Frame-Bilanz (exklusive Top-Level-Phasen, attribution v4)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_core.perf.models import FrameMetrics

V4_TOP_LEVEL_FIELDS: tuple[str, ...] = (
    "cpu_input_ms",
    "cpu_framework_pre_tick_ms",
    "frame_ms",
    "cpu_framework_post_tick_ms",
    "cpu_render_submit_ms",
    "cpu_present_cpu_ms",
    "cpu_framework_post_present_ms",
)

V3_APP_FIELDS: tuple[str, ...] = (
    "cpu_input_ms",
    "cpu_app_ui_ms",
    "cpu_sim_ms",
    "cpu_camera_ms",
    "cpu_extract_render_ms",
    "cpu_tile_render_ms",
    "cpu_render_prep_ms",
    "cpu_framework_ms",
)


V4_MARKER_FIELDS: tuple[str, ...] = (
    "cpu_framework_pre_tick_ms",
    "cpu_framework_post_tick_ms",
    "cpu_render_submit_ms",
    "cpu_present_cpu_ms",
    "cpu_framework_post_present_ms",
    "cpu_measurement_residual_ms",
)


def has_v4_attribution(frame: FrameMetrics) -> bool:
    """True wenn mindestens ein v4-spezifisches Top-Level-Feld gesetzt ist."""
    for name in V4_MARKER_FIELDS:
        value = getattr(frame, name, None)
        if value is not None:
            return True
    return False


def _field_ms(frame: FrameMetrics, name: str) -> float:
    if name == "frame_ms":
        return max(float(frame.frame_ms), 0.0)
    value = getattr(frame, name, None)
    if value is None or float(value) <= 0.0:
        return 0.0
    return float(value)


def cpu_attributed_ms_v4(frame: FrameMetrics) -> float:
    """Summe exklusiver Top-Level-Phasen gegen cpu_full_frame_ms."""
    return sum(_field_ms(frame, name) for name in V4_TOP_LEVEL_FIELDS)


def cpu_attributed_ms_v3(frame: FrameMetrics) -> float:
    """M25c — flache Summe (Legacy-Fallback für alte Runs)."""
    total = float(frame.frame_ms)
    for name in V3_APP_FIELDS:
        value = getattr(frame, name, None)
        if value is not None and float(value) > 0.0:
            total += float(value)
    for name in ("render_cpu_ms", "present_wait_cpu_ms"):
        value = getattr(frame, name, None)
        if value is not None and float(value) > 0.0:
            total += float(value)
    return total


def cpu_attributed_ms(frame: FrameMetrics) -> float:
    if has_v4_attribution(frame):
        return cpu_attributed_ms_v4(frame)
    return cpu_attributed_ms_v3(frame)


def reconcile_cpu_balance(frame: FrameMetrics) -> tuple[float | None, float | None]:
    """Returns (cpu_balance_delta_ms, cpu_residual_ms). v4: signiertes cpu_measurement_residual_ms."""
    full = frame.cpu_full_frame_ms
    if full is None or full <= 0.0:
        return None, None
    attributed = cpu_attributed_ms(frame)
    delta = float(full) - attributed
    residual = max(0.0, delta)
    return delta, residual
