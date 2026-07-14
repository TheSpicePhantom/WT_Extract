"""Run laden und validieren."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from game_core.perf.export_schema import SCHEMA_VERSION, validate_manifest, validate_summary
from game_core.perf.run_analysis.models import FrameRecord, HitchRecord

EXPORT_FILES = {
    "manifest": "manifest.json",
    "summary": "summary.json",
    "frames": "frames.jsonl",
    "hitches": "hitches.jsonl",
}

KNOWN_FRAME_FIELDS = {
    "schema_version",
    "frame_index",
    "frame_ms",
    "stream_ms",
    "stream_apply_ms",
    "stream_unload_ms",
    "stream_loaded",
    "stream_unloaded",
    "chunk_count",
    "focus_x",
    "focus_y",
    "zoom",
    # M25 optional (Full-frame / Render / Present).
    "cpu_full_frame_ms",
    "render_cpu_ms",
    "present_wait_cpu_ms",
    "cpu_unattributed_ms",
    "deco_extract_ms",
    "tile_extract_ms",
    "stream_unload_marked",
    "stream_unload_drained",
    "pending_unload_count",
    "apply_worker_ms",
    "apply_sync_generate_ms",
    "apply_delta_ms",
    "apply_override_ms",
    "apply_pool_ms",
    "apply_collision_ms",
    "tile_visible_chunks",
    "tile_cache_hits",
    "tile_cache_misses",
    "tile_full_rebuild_ms",
    "tile_cull_ms",
    "deco_scanned_count",
    "deco_visible_count",
    "tile_visible_batches",
    "tile_registry_hits",
    "tile_registry_misses",
    "tile_cull_cache_hits",
    "tile_cull_cache_misses",
    "tile_assemble_ms",
    "scenario_id",
}

KNOWN_HITCH_FIELDS = KNOWN_FRAME_FIELDS | {"tags"}


@dataclass(frozen=True, slots=True)
class LoadedRun:
    run_dir: Path
    manifest: dict[str, Any]
    summary: dict[str, Any]
    frames: list[FrameRecord]
    hitches: list[HitchRecord]
    optional_fields: frozenset[str]


class RunLoadError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RunLoadError(f"Datei fehlt: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RunLoadError(f"Ungültiges JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunLoadError(f"Erwartet JSON-Objekt in {path}")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise RunLoadError(f"Datei fehlt: {path}")
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise RunLoadError(f"Ungültige JSONL-Zeile {line_no} in {path}: {exc}") from exc
        if not isinstance(row, dict):
            raise RunLoadError(f"JSONL-Zeile {line_no} in {path} ist kein Objekt")
        rows.append(row)
    return rows


def _require_schema_version(data: dict[str, Any], source: str) -> None:
    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise RunLoadError(
            f"Inkompatible schema_version in {source}: erwartet {SCHEMA_VERSION}, "
            f"gefunden {version!r}"
        )


def _parse_frame(row: dict[str, Any], optional_fields: set[str]) -> FrameRecord:
    extra = {key: value for key, value in row.items() if key not in KNOWN_FRAME_FIELDS}
    for key in (
        "cpu_full_frame_ms",
        "render_cpu_ms",
        "present_wait_cpu_ms",
        "cpu_unattributed_ms",
        "deco_extract_ms",
        "tile_extract_ms",
        "stream_unload_marked",
        "stream_unload_drained",
        "pending_unload_count",
        "apply_worker_ms",
        "apply_sync_generate_ms",
        "apply_delta_ms",
        "apply_override_ms",
        "apply_pool_ms",
        "apply_collision_ms",
    ):
        if key in row:
            optional_fields.add(key)
    return FrameRecord(
        frame_index=int(row["frame_index"]),
        frame_ms=float(row["frame_ms"]),
        stream_ms=float(row["stream_ms"]),
        stream_apply_ms=float(row["stream_apply_ms"]),
        stream_unload_ms=float(row["stream_unload_ms"]),
        stream_loaded=int(row["stream_loaded"]),
        stream_unloaded=int(row["stream_unloaded"]),
        chunk_count=int(row["chunk_count"]),
        focus_x=float(row["focus_x"]),
        focus_y=float(row["focus_y"]),
        zoom=float(row["zoom"]),
        cpu_full_frame_ms=_optional_float(row, "cpu_full_frame_ms"),
        render_cpu_ms=_optional_float(row, "render_cpu_ms"),
        present_wait_cpu_ms=_optional_float(row, "present_wait_cpu_ms"),
        cpu_unattributed_ms=_optional_float(row, "cpu_unattributed_ms"),
        deco_extract_ms=_optional_float(row, "deco_extract_ms"),
        tile_extract_ms=_optional_float(row, "tile_extract_ms"),
        stream_unload_marked=_optional_int(row, "stream_unload_marked"),
        stream_unload_drained=_optional_int(row, "stream_unload_drained"),
        pending_unload_count=_optional_int(row, "pending_unload_count"),
        apply_worker_ms=_optional_float(row, "apply_worker_ms"),
        apply_sync_generate_ms=_optional_float(row, "apply_sync_generate_ms"),
        apply_delta_ms=_optional_float(row, "apply_delta_ms"),
        apply_override_ms=_optional_float(row, "apply_override_ms"),
        apply_pool_ms=_optional_float(row, "apply_pool_ms"),
        apply_collision_ms=_optional_float(row, "apply_collision_ms"),
        extra=extra,
    )


def _parse_hitch(row: dict[str, Any], optional_fields: set[str]) -> HitchRecord:
    extra = {key: value for key, value in row.items() if key not in KNOWN_HITCH_FIELDS}
    tags = row.get("tags", [])
    if not isinstance(tags, list):
        raise RunLoadError("Hitch-Tags müssen eine Liste sein")
    for key in (
        "cpu_full_frame_ms",
        "render_cpu_ms",
        "present_wait_cpu_ms",
        "deco_extract_ms",
        "tile_extract_ms",
        "pending_unload_count",
    ):
        if key in row:
            optional_fields.add(key)
    return HitchRecord(
        frame_index=int(row["frame_index"]),
        frame_ms=float(row["frame_ms"]),
        stream_ms=float(row["stream_ms"]),
        stream_apply_ms=float(row["stream_apply_ms"]),
        stream_unload_ms=float(row["stream_unload_ms"]),
        stream_loaded=int(row["stream_loaded"]),
        stream_unloaded=int(row["stream_unloaded"]),
        chunk_count=int(row["chunk_count"]),
        focus_x=float(row["focus_x"]),
        focus_y=float(row["focus_y"]),
        zoom=float(row["zoom"]),
        tags=tuple(str(tag) for tag in tags),
        cpu_full_frame_ms=_optional_float(row, "cpu_full_frame_ms"),
        render_cpu_ms=_optional_float(row, "render_cpu_ms"),
        present_wait_cpu_ms=_optional_float(row, "present_wait_cpu_ms"),
        deco_extract_ms=_optional_float(row, "deco_extract_ms"),
        tile_extract_ms=_optional_float(row, "tile_extract_ms"),
        pending_unload_count=_optional_int(row, "pending_unload_count"),
        extra=extra,
    )


def _optional_float(row: dict[str, Any], key: str) -> float | None:
    if key not in row:
        return None
    return float(row[key])


def _optional_int(row: dict[str, Any], key: str) -> int | None:
    if key not in row:
        return None
    return int(row[key])


def resolve_run_paths(
    run_dir: Path | None = None,
    *,
    manifest: Path | None = None,
    summary: Path | None = None,
    frames: Path | None = None,
    hitches: Path | None = None,
) -> dict[str, Path]:
    if run_dir is not None:
        base = run_dir.resolve()
        return {key: base / name for key, name in EXPORT_FILES.items()}
    if manifest is None or summary is None or frames is None or hitches is None:
        raise RunLoadError("Entweder run_dir oder alle vier Dateipfade angeben.")
    return {
        "manifest": manifest.resolve(),
        "summary": summary.resolve(),
        "frames": frames.resolve(),
        "hitches": hitches.resolve(),
    }


def load_run(
    run_dir: Path | None = None,
    *,
    manifest: Path | None = None,
    summary: Path | None = None,
    frames: Path | None = None,
    hitches: Path | None = None,
) -> LoadedRun:
    paths = resolve_run_paths(
        run_dir,
        manifest=manifest,
        summary=summary,
        frames=frames,
        hitches=hitches,
    )
    manifest_data = _read_json(paths["manifest"])
    summary_data = _read_json(paths["summary"])
    _require_schema_version(manifest_data, paths["manifest"].name)
    _require_schema_version(summary_data, paths["summary"].name)

    try:
        validate_manifest(manifest_data)
        validate_summary(summary_data)
    except ValueError as exc:
        raise RunLoadError(f"Schema-Validierung fehlgeschlagen: {exc}") from exc

    optional_fields: set[str] = set()
    frame_rows = _read_jsonl(paths["frames"])
    hitch_rows = _read_jsonl(paths["hitches"])

    frames = [_parse_frame(row, optional_fields) for row in frame_rows]
    hitches = [_parse_hitch(row, optional_fields) for row in hitch_rows]

    for row in frame_rows:
        _require_schema_version(row, "frames.jsonl")
    for row in hitch_rows:
        _require_schema_version(row, "hitches.jsonl")

    base_dir = run_dir.resolve() if run_dir is not None else paths["manifest"].parent
    return LoadedRun(
        run_dir=base_dir,
        manifest=manifest_data,
        summary=summary_data,
        frames=frames,
        hitches=hitches,
        optional_fields=frozenset(optional_fields),
    )
