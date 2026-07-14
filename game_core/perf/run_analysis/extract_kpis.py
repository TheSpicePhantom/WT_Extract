"""Extract-KPIs aus frames.jsonl rekonstruieren (M23c/M23d)."""

from __future__ import annotations

from pathlib import Path

from game_core.perf.run_analysis.load import load_run
from game_core.perf.run_analysis.stats import mean, percentile


def _frame_metric(frames, attr: str) -> list[float]:
    values: list[float] = []
    for frame in frames:
        value = getattr(frame, attr, None)
        if value is None:
            value = frame.extra.get(attr)
        if value is not None:
            values.append(float(value))
    return values


def extract_kpis_from_run(run_dir: Path) -> dict[str, float]:
    loaded = load_run(run_dir)
    frames = loaded.frames
    tile_values = [frame.tile_extract_ms or 0.0 for frame in frames]
    deco_values = [frame.deco_extract_ms or 0.0 for frame in frames]
    extract_values = [frame.extract_ms for frame in frames]

    kpis: dict[str, float] = {
        "tile_extract_ms_mean": mean(tile_values),
        "tile_extract_ms_p95": percentile(tile_values, 0.95),
        "tile_extract_ms_max": max(tile_values, default=0.0),
        "deco_extract_ms_mean": mean(deco_values),
        "deco_extract_ms_p95": percentile(deco_values, 0.95),
        "deco_extract_ms_max": max(deco_values, default=0.0),
        "extract_ms_mean": mean(extract_values),
        "extract_ms_p95": percentile(extract_values, 0.95),
        "extract_ms_max": max(extract_values, default=0.0),
    }

    for attr, prefix in (
        ("tile_registry_hits", "tile_registry_hits"),
        ("tile_registry_misses", "tile_registry_misses"),
        ("tile_cull_cache_hits", "tile_cull_cache_hits"),
        ("tile_cull_cache_misses", "tile_cull_cache_misses"),
        ("tile_visible_batches", "tile_visible_batches"),
    ):
        values = _frame_metric(frames, attr)
        if values:
            kpis[f"{prefix}_mean"] = mean(values)
            kpis[f"{prefix}_p95"] = percentile(values, 0.95)

    assemble_values = _frame_metric(frames, "tile_assemble_ms")
    if assemble_values:
        kpis["tile_assemble_ms_mean"] = mean(assemble_values)
        kpis["tile_assemble_ms_p95"] = percentile(assemble_values, 0.95)

    for attr, prefix in (
        ("tile_lod0_groups", "tile_lod0_groups"),
        ("tile_lod1_groups", "tile_lod1_groups"),
        ("tile_lod2_groups", "tile_lod2_groups"),
        ("tile_lod_switches", "tile_lod_switches"),
    ):
        values = _frame_metric(frames, attr)
        if values:
            kpis[f"{prefix}_mean"] = mean(values)
            kpis[f"{prefix}_p95"] = percentile(values, 0.95)

    for attr, prefix in (
        ("tile_lod0_ms", "tile_lod0_ms"),
        ("tile_lod1_ms", "tile_lod1_ms"),
        ("tile_lod2_ms", "tile_lod2_ms"),
    ):
        values = _frame_metric(frames, attr)
        if values:
            kpis[f"{prefix}_mean"] = mean(values)
            kpis[f"{prefix}_p95"] = percentile(values, 0.95)

    return kpis
