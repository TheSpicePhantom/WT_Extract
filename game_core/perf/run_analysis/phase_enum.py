"""M25d: Plan-konformes dominant_phase-Enum und Klassifikations-Schwellen."""

from __future__ import annotations

from typing import Literal

DominantPhase = Literal[
    "stream_apply",
    "stream_pool",
    "extract_tiles",
    "extract_deco",
    "render_cpu",
    "present_wait",
    "gpu",
    "cpu_input",
    "cpu_app_ui",
    "canonical_tick",
    "cpu_sim",
    "cpu_camera",
    "cpu_extract_render",
    "cpu_tile_render",
    "cpu_render_prep",
    "cpu_framework",
    "cpu_residual",
    "cpu_framework_pre_tick",
    "cpu_framework_post_tick",
    "cpu_render_submit",
    "cpu_present_cpu",
    "cpu_framework_post_present",
    "cpu_measurement_residual",
    "mixed",
    "mixed_cpu_workload",
    "unclear",
]

DOMINANT_PHASES: tuple[str, ...] = (
    "stream_apply",
    "stream_pool",
    "extract_tiles",
    "extract_deco",
    "render_cpu",
    "present_wait",
    "gpu",
    "cpu_input",
    "cpu_app_ui",
    "canonical_tick",
    "cpu_sim",
    "cpu_camera",
    "cpu_extract_render",
    "cpu_tile_render",
    "cpu_render_prep",
    "cpu_framework",
    "cpu_residual",
    "cpu_framework_pre_tick",
    "cpu_framework_post_tick",
    "cpu_render_submit",
    "cpu_present_cpu",
    "cpu_framework_post_present",
    "cpu_measurement_residual",
)

DOMINANT_PHASES_V4: tuple[str, ...] = (
    "cpu_input",
    "cpu_framework_pre_tick",
    "canonical_tick",
    "cpu_framework_post_tick",
    "cpu_render_submit",
    "cpu_present_cpu",
    "cpu_framework_post_present",
    "cpu_measurement_residual",
)

# Anteil von cpu_full_frame_ms
DOMINANT_THRESHOLD = 0.35
MIXED_MIN_SHARE = 0.25
MIXED_MAX_GAP = 0.10
UNCLEAR_MAX_TOP = 0.20

# Run-level CPU vs Present
PRESENT_WAIT_DOMINANT_THRESHOLD = 0.35
CPU_DOMINANT_THRESHOLD = 0.35

ATTRIBUTION_VERSION = 4

V4_REQUIRED_FRAME_FIELDS: tuple[str, ...] = (
    "cpu_framework_pre_tick_ms",
    "cpu_render_submit_ms",
    "cpu_measurement_residual_ms",
)
