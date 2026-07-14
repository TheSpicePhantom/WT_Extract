"""Streaming-Konfiguration — hybrid viewport + radius fallback (M22d)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STREAMING_CONFIG = PROJECT_ROOT / "assets" / "content" / "streaming.json"


@dataclass(frozen=True, slots=True)
class StreamingConfig:
    mode: str = "hybrid"
    viewport_padding_chunks: int = 1
    player_safety_ring: int = 1
    keep_padding_chunks: int = 1
    max_half_chunks_cap: int = 10
    max_loaded_chunks: int = 160
    min_zoom: float = 0.05
    prefetch_chunks: int = 2
    prefetch_min_speed_px: float = 8.0
    max_applies_per_frame: int = 4
    max_sync_applies_per_frame: int = 0
    max_unloads_per_frame: int = 2
    max_unload_ms_per_frame: float = 0.0
    max_in_flight_chunks: int = 8
    sync_fallback_in_flight_ms: float = 500.0
    terrain_max_in_flight: int = 8
    deco_max_in_flight: int = 4
    terrain_parallelism_cap: int = 6
    deco_parallelism_cap: int = 2
    deco_only_after_terrain_applied: bool = True
    deco_pause_when_visible_terrain_pending: bool = True
    prefetch_deco_only_when_idle: bool = True
    deco_backfill_budget_per_frame: int = 2
    pipeline_mode: str = "combined"
    sync_fallback_only_when_pool_disabled: bool = True
    pool_idle_skip_enabled: bool = True
    pool_idle_refresh_frames: int = 30
    pool_idle_move_epsilon_px: float = 0.5
    load_radius: int = 8
    unload_radius: int = 10


def load_streaming_config(path: Path | None = None) -> StreamingConfig:
    config_path = path or DEFAULT_STREAMING_CONFIG
    if not config_path.is_file():
        return StreamingConfig()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    hybrid = data.get("hybrid", {})
    radius = data.get("radius_fallback", {})
    return StreamingConfig(
        mode=str(data.get("mode", "hybrid")),
        viewport_padding_chunks=int(hybrid.get("viewport_padding_chunks", 1)),
        player_safety_ring=int(hybrid.get("player_safety_ring", 1)),
        keep_padding_chunks=int(hybrid.get("keep_padding_chunks", 1)),
        max_half_chunks_cap=int(hybrid.get("max_half_chunks_cap", 10)),
        max_loaded_chunks=int(hybrid.get("max_loaded_chunks", 160)),
        min_zoom=float(hybrid.get("min_zoom", 0.05)),
        prefetch_chunks=int(hybrid.get("prefetch_chunks", 2)),
        prefetch_min_speed_px=float(hybrid.get("prefetch_min_speed_px", 8.0)),
        max_applies_per_frame=int(hybrid.get("max_applies_per_frame", 4)),
        max_sync_applies_per_frame=int(hybrid.get("max_sync_applies_per_frame", 0)),
        max_unloads_per_frame=int(hybrid.get("max_unloads_per_frame", 2)),
        max_unload_ms_per_frame=float(hybrid.get("max_unload_ms_per_frame", 0.0)),
        max_in_flight_chunks=int(hybrid.get("max_in_flight_chunks", 8)),
        sync_fallback_in_flight_ms=float(hybrid.get("sync_fallback_in_flight_ms", 500.0)),
        terrain_max_in_flight=int(hybrid.get("terrain_max_in_flight", hybrid.get("max_in_flight_chunks", 8))),
        deco_max_in_flight=int(hybrid.get("deco_max_in_flight", 4)),
        terrain_parallelism_cap=int(hybrid.get("terrain_parallelism_cap", 6)),
        deco_parallelism_cap=int(hybrid.get("deco_parallelism_cap", 2)),
        deco_only_after_terrain_applied=bool(hybrid.get("deco_only_after_terrain_applied", True)),
        deco_pause_when_visible_terrain_pending=bool(
            hybrid.get("deco_pause_when_visible_terrain_pending", True)
        ),
        prefetch_deco_only_when_idle=bool(hybrid.get("prefetch_deco_only_when_idle", True)),
        deco_backfill_budget_per_frame=int(hybrid.get("deco_backfill_budget_per_frame", 2)),
        pipeline_mode=str(hybrid.get("pipeline_mode", "combined")),
        sync_fallback_only_when_pool_disabled=bool(
            hybrid.get("sync_fallback_only_when_pool_disabled", True)
        ),
        pool_idle_skip_enabled=bool(hybrid.get("pool_idle_skip_enabled", True)),
        pool_idle_refresh_frames=int(hybrid.get("pool_idle_refresh_frames", 30)),
        pool_idle_move_epsilon_px=float(hybrid.get("pool_idle_move_epsilon_px", 0.5)),
        load_radius=int(radius.get("load_radius", 8)),
        unload_radius=int(radius.get("unload_radius", 10)),
    )
