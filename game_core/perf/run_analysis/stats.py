"""Statistik — Verteilungen und Korrelationen."""

from __future__ import annotations

import math

from game_core.perf.run_analysis.models import CorrelationInsight, FrameRecord, MetricDistribution


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * pct))
    index = max(0, min(index, len(ordered) - 1))
    return ordered[index]


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def distribution(name: str, values: list[float]) -> MetricDistribution:
    if not values:
        return MetricDistribution(name=name, mean=0.0, p50=0.0, p95=0.0, max=0.0, present=False)
    return MetricDistribution(
        name=name,
        mean=mean(values),
        p50=percentile(values, 0.50),
        p95=percentile(values, 0.95),
        max=max(values),
    )


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    mx = mean(xs)
    my = mean(ys)
    num = 0.0
    dx = 0.0
    dy = 0.0
    for x, y in zip(xs, ys):
        vx = x - mx
        vy = y - my
        num += vx * vy
        dx += vx * vx
        dy += vy * vy
    if dx <= 0.0 or dy <= 0.0:
        return None
    return num / math.sqrt(dx * dy)


def correlation_strength(value: float | None) -> str:
    if value is None:
        return "unbekannt"
    abs_val = abs(value)
    if abs_val >= 0.7:
        return "stark"
    if abs_val >= 0.4:
        return "moderat"
    if abs_val >= 0.2:
        return "schwach"
    return "vernachlässigbar"


def frame_metric_values(frames: list[FrameRecord], name: str) -> list[float]:
    values: list[float] = []
    for frame in frames:
        if name == "frame_ms":
            values.append(frame.frame_ms)
        elif name == "stream_ms":
            values.append(frame.stream_ms)
        elif name == "stream_apply_ms":
            values.append(frame.stream_apply_ms)
        elif name == "stream_unload_ms":
            values.append(frame.stream_unload_ms)
        elif name == "extract_ms":
            values.append(frame.extract_ms)
        elif name == "deco_extract_ms" and frame.deco_extract_ms is not None:
            values.append(frame.deco_extract_ms)
        elif name == "tile_extract_ms" and frame.tile_extract_ms is not None:
            values.append(frame.tile_extract_ms)
        elif name == "pending_unload_count" and frame.pending_unload_count is not None:
            values.append(float(frame.pending_unload_count))
        elif name == "stream_loaded":
            values.append(float(frame.stream_loaded))
        elif name == "stream_unloaded":
            values.append(float(frame.stream_unloaded))
        elif name == "chunk_count":
            values.append(float(frame.chunk_count))
        elif name == "zoom":
            values.append(frame.zoom)
        elif name == "cpu_full_frame_ms" and frame.cpu_full_frame_ms is not None:
            values.append(frame.cpu_full_frame_ms)
        elif name == "render_cpu_ms" and frame.render_cpu_ms is not None:
            values.append(frame.render_cpu_ms)
        elif name == "present_wait_cpu_ms" and frame.present_wait_cpu_ms is not None:
            values.append(frame.present_wait_cpu_ms)
        elif name == "cpu_unattributed_ms" and frame.cpu_unattributed_ms is not None:
            values.append(frame.cpu_unattributed_ms)
    return values


def paired_values(frames: list[FrameRecord], x_name: str, y_name: str) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    for frame in frames:
        x_vals = frame_metric_values([frame], x_name)
        y_vals = frame_metric_values([frame], y_name)
        if not x_vals or not y_vals:
            continue
        xs.append(x_vals[0])
        ys.append(y_vals[0])
    return xs, ys


def build_correlation_insight(
    frames: list[FrameRecord],
    x_name: str,
    y_name: str,
    *,
    hitch_indices: set[int] | None = None,
) -> CorrelationInsight:
    xs, ys = paired_values(frames, x_name, y_name)
    coef = pearson(xs, ys)
    strength = correlation_strength(coef)

    if coef is None:
        interpretation = "Zu wenige Datenpunkte für eine belastbare Korrelation."
    elif hitch_indices is not None and x_name == "frame_ms":
        hitch_frames = [frame for frame in frames if frame.frame_index in hitch_indices]
        other_frames = [frame for frame in frames if frame.frame_index not in hitch_indices]
        if hitch_frames and other_frames:
            hx = mean(frame_metric_values(hitch_frames, y_name))
            ox = mean(frame_metric_values(other_frames, y_name))
            ratio = hx / ox if ox > 0 else float("inf")
            interpretation = (
                f"Hitch-Frames: {y_name}-Mittel {hx:.3f} vs. übrige {ox:.3f} "
                f"(Faktor {ratio:.2f}). Pearson r={coef:.3f} ({strength})."
            )
        else:
            interpretation = f"Pearson r={coef:.3f} ({strength}) — nur Indiz, keine Kausalität."
    else:
        interpretation = f"Pearson r={coef:.3f} ({strength}) zwischen {x_name} und {y_name}."

    return CorrelationInsight(
        metric_x=x_name,
        metric_y=y_name,
        coefficient=coef,
        strength=strength,
        interpretation=interpretation,
        sample_size=len(xs),
    )
