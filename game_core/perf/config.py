"""Profiling-Konfiguration (M23)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_PROFILING_CONFIG = PROJECT_ROOT / "assets" / "content" / "profiling.json"


@dataclass(frozen=True, slots=True)
class HitchThresholds:
    stream_ms: float
    frame_ms: float
    loaded_count: int
    unloaded_count: int
    pending_unload_count: int = 32


@dataclass(frozen=True, slots=True)
class ProfilingConfig:
    enabled: bool
    hitch: HitchThresholds
    scenarios: dict[str, ScenarioParams]
    ring_buffer_frames: int


@dataclass(frozen=True, slots=True)
class ScenarioParams:
    frames: int
    warmup_frames: int = 0
    extract_enabled: bool = True
    stream_enabled: bool = True
    deco_extract_enabled: bool = True
    tile_extract_enabled: bool = True
    pan_axis: str = "x"
    pan_chunks_per_frame: float = 1.0
    zoom: float = 0.35


def load_profiling_config(path: Path | None = None) -> ProfilingConfig:
    config_path = path or DEFAULT_PROFILING_CONFIG
    if not config_path.is_file():
        return _default_config()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    hitch = data.get("hitch", {})
    export = data.get("export", {})
    scenarios: dict[str, ScenarioParams] = {}
    for scenario_id, params in data.get("scenarios", {}).items():
        scenarios[str(scenario_id)] = ScenarioParams(
            frames=int(params.get("frames", 300)),
            warmup_frames=int(params.get("warmup_frames", 0)),
            extract_enabled=bool(params.get("extract_enabled", True)),
            stream_enabled=bool(params.get("stream_enabled", True)),
            deco_extract_enabled=bool(params.get("deco_extract_enabled", True)),
            tile_extract_enabled=bool(params.get("tile_extract_enabled", True)),
            pan_axis=str(params.get("pan_axis", "x")),
            pan_chunks_per_frame=float(params.get("pan_chunks_per_frame", 1.0)),
            zoom=float(params.get("zoom", 0.35)),
        )
    return ProfilingConfig(
        enabled=bool(data.get("enabled", False)),
        hitch=HitchThresholds(
            stream_ms=float(hitch.get("stream_ms", 8.0)),
            frame_ms=float(hitch.get("frame_ms", 16.0)),
            loaded_count=int(hitch.get("loaded_count", 4)),
            unloaded_count=int(hitch.get("unloaded_count", 4)),
            pending_unload_count=int(hitch.get("pending_unload_count", 32)),
        ),
        scenarios=scenarios,
        ring_buffer_frames=int(export.get("ring_buffer_frames", 120)),
    )


def _default_config() -> ProfilingConfig:
    return ProfilingConfig(
        enabled=False,
        hitch=HitchThresholds(
            stream_ms=8.0,
            frame_ms=16.0,
            loaded_count=4,
            unloaded_count=4,
        ),
        scenarios={
            "steady": ScenarioParams(frames=300, warmup_frames=60),
            "pan": ScenarioParams(frames=300, warmup_frames=60, pan_chunks_per_frame=1.0),
            "zoom_out": ScenarioParams(frames=200, warmup_frames=60, zoom=0.05),
            "catchup": ScenarioParams(frames=400, warmup_frames=120, pan_chunks_per_frame=1.0),
        },
        ring_buffer_frames=120,
    )
