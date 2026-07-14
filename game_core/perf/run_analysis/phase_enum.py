"""M25a: Plan-konformes dominant_phase-Enum und Klassifikations-Schwellen."""

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
    "mixed",
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
)

# Anteil von cpu_full_frame_ms
DOMINANT_THRESHOLD = 0.35
MIXED_MIN_SHARE = 0.25
MIXED_MAX_GAP = 0.10
UNCLEAR_MAX_TOP = 0.20

# Run-level CPU vs Present
PRESENT_WAIT_DOMINANT_THRESHOLD = 0.35
CPU_DOMINANT_THRESHOLD = 0.35

ATTRIBUTION_VERSION = 2
