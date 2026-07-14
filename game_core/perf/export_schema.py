"""Export-Schema — Validierung und Serialisierung (M23)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from game_core.perf.models import FrameMetrics, HitchEvent, RunSummary

SCHEMA_VERSION = 1
SUPPORTED_SCHEMA_VERSIONS: frozenset[int] = frozenset({SCHEMA_VERSION})

MANIFEST_REQUIRED = frozenset(
    {
        "schema_version",
        "run_id",
        "recorded_at",
        "scenario_id",
        "run_mode",
        "extract_enabled",
        "warmup_frames",
        "recorded_frames",
        "git_commit",
        "config_fingerprint",
    }
)

FRAME_REQUIRED = frozenset(
    {
        "schema_version",
        "frame_index",
        "scenario_id",
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
    }
)

HITCH_REQUIRED = frozenset(
    {
        "schema_version",
        "frame_index",
        "scenario_id",
        "tags",
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
    }
)

SUMMARY_REQUIRED = frozenset(
    {
        "schema_version",
        "run_id",
        "scenario_id",
        "run_mode",
        "recorded_frames",
        "frame_ms_mean",
        "frame_ms_p95",
        "frame_ms_max",
        "stream_ms_mean",
        "stream_ms_p95",
        "stream_ms_max",
        "stream_unload_ms_p95",
        "stream_unload_ms_max",
        "hitch_count",
        "hitch_frame_count",
        "hitch_stream_count",
        "hitch_load_count",
        "hitch_unload_count",
        "max_loaded_per_frame",
        "max_unloaded_per_frame",
        "chunk_count_mean",
    }
)


def assert_supported_schema_version(version: int) -> None:
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        supported = ", ".join(str(item) for item in sorted(SUPPORTED_SCHEMA_VERSIONS))
        raise ValueError(
            f"Unsupported schema_version {version}; supported: {supported}"
        )


def validate_manifest(data: dict[str, Any]) -> None:
    assert_supported_schema_version(int(data["schema_version"]))
    missing = MANIFEST_REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"manifest.json missing fields: {sorted(missing)}")


def validate_frame_line(data: dict[str, Any]) -> None:
    assert_supported_schema_version(int(data["schema_version"]))
    missing = FRAME_REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"frames.jsonl missing fields: {sorted(missing)}")


def validate_hitch_line(data: dict[str, Any]) -> None:
    assert_supported_schema_version(int(data["schema_version"]))
    missing = HITCH_REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"hitches.jsonl missing fields: {sorted(missing)}")


def validate_summary(data: dict[str, Any]) -> None:
    assert_supported_schema_version(int(data["schema_version"]))
    missing = SUMMARY_REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"summary.json missing fields: {sorted(missing)}")


def write_run_export(
    run_dir: Path,
    *,
    manifest: dict[str, Any],
    frames: list[FrameMetrics],
    hitches: list[HitchEvent],
    summary: RunSummary,
) -> None:
    validate_manifest(manifest)
    summary_dict = summary.to_dict()
    validate_summary(summary_dict)

    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    with (run_dir / "frames.jsonl").open("w", encoding="utf-8") as handle:
        for frame in frames:
            payload = frame.to_dict()
            validate_frame_line(payload)
            handle.write(json.dumps(payload, sort_keys=True) + "\n")
    with (run_dir / "hitches.jsonl").open("w", encoding="utf-8") as handle:
        for hitch in hitches:
            payload = hitch.to_dict()
            validate_hitch_line(payload)
            handle.write(json.dumps(payload, sort_keys=True) + "\n")
    (run_dir / "summary.json").write_text(
        json.dumps(summary_dict, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def load_summary(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_summary(data)
    return data
