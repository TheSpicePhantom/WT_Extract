"""Summary aus frames.jsonl nachrechnen und plausibilisieren."""

from __future__ import annotations

from typing import Any

from game_core.perf.hitch import HITCH_TAG_ORDER
from game_core.perf.run_analysis.models import FrameRecord, HitchRecord, SummaryCheck
from game_core.perf.run_analysis.stats import mean, percentile



def recompute_summary(
    frames: list[FrameRecord],
    hitches: list[HitchRecord],
    *,
    run_id: str,
    scenario_id: str,
    run_mode: str,
    schema_version: int,
) -> dict[str, Any]:
    frame_ms_values = [frame.frame_ms for frame in frames]
    stream_ms_values = [frame.stream_ms for frame in frames]
    unload_ms_values = [frame.stream_unload_ms for frame in frames]
    chunk_counts = [float(frame.chunk_count) for frame in frames]

    hitch_events = hitches

    return {
        "schema_version": schema_version,
        "run_id": run_id,
        "scenario_id": scenario_id,
        "run_mode": run_mode,
        "recorded_frames": len(frames),
        "frame_ms_mean": mean(frame_ms_values),
        "frame_ms_p95": percentile(frame_ms_values, 0.95),
        "frame_ms_max": max(frame_ms_values, default=0.0),
        "stream_ms_mean": mean(stream_ms_values),
        "stream_ms_p95": percentile(stream_ms_values, 0.95),
        "stream_ms_max": max(stream_ms_values, default=0.0),
        "stream_unload_ms_p95": percentile(unload_ms_values, 0.95),
        "stream_unload_ms_max": max(unload_ms_values, default=0.0),
        "hitch_count": len(hitches),
        "hitch_frame_count": sum(1 for hitch in hitch_events if "frame_slow" in hitch.tags),
        "hitch_stream_count": sum(1 for hitch in hitch_events if "stream_slow" in hitch.tags),
        "hitch_load_count": sum(1 for hitch in hitch_events if "load_burst" in hitch.tags),
        "hitch_unload_count": sum(1 for hitch in hitch_events if "unload_burst" in hitch.tags),
        "max_loaded_per_frame": max((frame.stream_loaded for frame in frames), default=0),
        "max_unloaded_per_frame": max((frame.stream_unloaded for frame in frames), default=0),
        "chunk_count_mean": mean(chunk_counts),
    }


SUMMARY_FLOAT_FIELDS = (
    "frame_ms_mean",
    "frame_ms_p95",
    "frame_ms_max",
    "stream_ms_mean",
    "stream_ms_p95",
    "stream_ms_max",
    "stream_unload_ms_p95",
    "stream_unload_ms_max",
    "chunk_count_mean",
)

SUMMARY_INT_FIELDS = (
    "recorded_frames",
    "hitch_count",
    "hitch_frame_count",
    "hitch_stream_count",
    "hitch_load_count",
    "hitch_unload_count",
    "max_loaded_per_frame",
    "max_unloaded_per_frame",
)


def _close_enough(expected: float, actual: float, *, rel_tol: float = 0.02, abs_tol: float = 0.05) -> bool:
    delta = abs(expected - actual)
    scale = max(abs(expected), abs(actual), 1.0)
    return delta <= max(abs_tol, scale * rel_tol)


def check_summary(
    summary: dict[str, Any],
    recomputed: dict[str, Any],
) -> list[SummaryCheck]:
    checks: list[SummaryCheck] = []
    for field in SUMMARY_FLOAT_FIELDS:
        summary_value = float(summary.get(field, 0.0))
        recomputed_value = float(recomputed.get(field, 0.0))
        delta = recomputed_value - summary_value
        checks.append(
            SummaryCheck(
                field=field,
                summary_value=summary_value,
                recomputed_value=recomputed_value,
                delta=delta,
                ok=_close_enough(summary_value, recomputed_value),
            )
        )
    for field in SUMMARY_INT_FIELDS:
        summary_value = float(int(summary.get(field, 0)))
        recomputed_value = float(int(recomputed.get(field, 0)))
        delta = recomputed_value - summary_value
        checks.append(
            SummaryCheck(
                field=field,
                summary_value=summary_value,
                recomputed_value=recomputed_value,
                delta=delta,
                ok=summary_value == recomputed_value,
            )
        )
    return checks


def hitch_tag_counts(hitches: list[HitchRecord]) -> dict[str, int]:
    counts = {tag: 0 for tag in HITCH_TAG_ORDER}
    for hitch in hitches:
        for tag in hitch.tags:
            if tag in counts:
                counts[tag] += 1
            else:
                counts[tag] = counts.get(tag, 0) + 1
    return counts
