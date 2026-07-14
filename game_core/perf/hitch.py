"""Hitch-Klassifikation (M23)."""

from __future__ import annotations

from game_core.perf.config import HitchThresholds
from game_core.perf.models import FrameMetrics

HITCH_TAG_ORDER: tuple[str, ...] = (
    "frame_slow",
    "stream_slow",
    "load_burst",
    "unload_burst",
    "unload_backlog",
)


def classify_hitch(metrics: FrameMetrics, thresholds: HitchThresholds) -> tuple[str, ...]:
    tags: list[str] = []
    if metrics.frame_ms >= thresholds.frame_ms:
        tags.append("frame_slow")
    if metrics.stream_ms >= thresholds.stream_ms:
        tags.append("stream_slow")
    if metrics.stream_loaded >= thresholds.loaded_count:
        tags.append("load_burst")
    if metrics.stream_unloaded >= thresholds.unloaded_count:
        tags.append("unload_burst")
    pending = metrics.pending_unload_count
    if pending is not None and pending >= thresholds.pending_unload_count:
        tags.append("unload_backlog")
    return tuple(tag for tag in HITCH_TAG_ORDER if tag in tags)
