"""Profiling-Datenmodelle (M23)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class StreamStepMetrics:
    """Out-Parameter für ChunkStreamer.update — mutable, zero-init."""

    sets_ms: float = 0.0
    apply_ms: float = 0.0
    unload_ms: float = 0.0
    total_ms: float = 0.0
    loaded: int = 0
    unloaded: int = 0
    unload_marked: int = 0
    pending_unload_count: int = 0
    apply_worker_ms: float = 0.0
    apply_sync_generate_ms: float = 0.0
    apply_delta_ms: float = 0.0
    apply_override_ms: float = 0.0
    apply_pool_ms: float = 0.0
    apply_collision_ms: float = 0.0
    apply_terrain_ms: float = 0.0
    apply_deco_ms: float = 0.0
    terrain_submitted: int = 0
    terrain_applied: int = 0
    terrain_discarded_stale: int = 0
    deco_submitted: int = 0
    deco_applied: int = 0
    deco_discarded_stale: int = 0
    deco_discarded_duplicate: int = 0
    deco_suppressed: int = 0
    deco_submit_skipped_visible_terrain_pressure: int = 0
    visible_terrain_wait_frames: int = 0
    terrain_submit_skipped_worker_saturation: int = 0
    field_cache_hits: int = 0
    field_cache_misses: int = 0
    field_cache_evictions: int = 0
    field_cache_live_count: int = 0
    sync_fallback_triggered: int = 0
    sync_skipped_worker_submitted: int = 0
    sync_skipped_pending_result: int = 0
    terrain_submit_attempted: int = 0
    terrain_submit_accepted: int = 0

    def reset(self) -> None:
        self.sets_ms = 0.0
        self.apply_ms = 0.0
        self.unload_ms = 0.0
        self.total_ms = 0.0
        self.loaded = 0
        self.unloaded = 0
        self.unload_marked = 0
        self.pending_unload_count = 0
        self.apply_worker_ms = 0.0
        self.apply_sync_generate_ms = 0.0
        self.apply_delta_ms = 0.0
        self.apply_override_ms = 0.0
        self.apply_pool_ms = 0.0
        self.apply_collision_ms = 0.0
        self.apply_terrain_ms = 0.0
        self.apply_deco_ms = 0.0
        self.terrain_submitted = 0
        self.terrain_applied = 0
        self.terrain_discarded_stale = 0
        self.deco_submitted = 0
        self.deco_applied = 0
        self.deco_discarded_stale = 0
        self.deco_discarded_duplicate = 0
        self.deco_suppressed = 0
        self.deco_submit_skipped_visible_terrain_pressure = 0
        self.visible_terrain_wait_frames = 0
        self.terrain_submit_skipped_worker_saturation = 0
        self.field_cache_hits = 0
        self.field_cache_misses = 0
        self.field_cache_evictions = 0
        self.field_cache_live_count = 0
        self.sync_fallback_triggered = 0
        self.sync_skipped_worker_submitted = 0
        self.sync_skipped_pending_result = 0
        self.terrain_submit_attempted = 0
        self.terrain_submit_accepted = 0


@dataclass(slots=True)
class ExtractStepMetrics:
    """Out-Parameter für Extract-Phasen — mutable, zero-init (M23c)."""

    tile_visible_chunks: int = 0
    tile_cache_hits: int = 0
    tile_cache_misses: int = 0
    tile_full_rebuild_ms: float = 0.0
    tile_cull_ms: float = 0.0
    deco_scanned_count: int = 0
    deco_visible_count: int = 0
    tile_visible_batches: int = 0
    tile_registry_hits: int = 0
    tile_registry_misses: int = 0
    tile_cull_cache_hits: int = 0
    tile_cull_cache_misses: int = 0
    tile_assemble_ms: float = 0.0
    tile_lod0_groups: int = 0
    tile_lod1_groups: int = 0
    tile_lod2_groups: int = 0
    tile_lod0_ms: float = 0.0
    tile_lod1_ms: float = 0.0
    tile_lod2_ms: float = 0.0
    tile_lod_switches: int = 0
    tile_map_mode_active: int = 0

    def reset(self) -> None:
        self.tile_visible_chunks = 0
        self.tile_cache_hits = 0
        self.tile_cache_misses = 0
        self.tile_full_rebuild_ms = 0.0
        self.tile_cull_ms = 0.0
        self.deco_scanned_count = 0
        self.deco_visible_count = 0
        self.tile_visible_batches = 0
        self.tile_registry_hits = 0
        self.tile_registry_misses = 0
        self.tile_cull_cache_hits = 0
        self.tile_cull_cache_misses = 0
        self.tile_assemble_ms = 0.0
        self.tile_lod0_groups = 0
        self.tile_lod1_groups = 0
        self.tile_lod2_groups = 0
        self.tile_lod0_ms = 0.0
        self.tile_lod1_ms = 0.0
        self.tile_lod2_ms = 0.0
        self.tile_lod_switches = 0
        self.tile_map_mode_active = 0


@dataclass(slots=True)
class FrameMetrics:
    schema_version: int
    frame_index: int
    scenario_id: str
    frame_ms: float
    stream_ms: float
    stream_apply_ms: float
    stream_unload_ms: float
    stream_loaded: int
    stream_unloaded: int
    chunk_count: int
    focus_x: float
    focus_y: float
    zoom: float
    # M25: Vollständiger App-Frame (optional, solange nicht instrumentiert).
    cpu_full_frame_ms: float | None = None
    render_cpu_ms: float | None = None
    present_wait_cpu_ms: float | None = None
    cpu_unattributed_ms: float | None = None
    # M25: Renderer-CPU Unterphasen (optional).
    render_wait_fence_ms: float | None = None
    render_acquire_ms: float | None = None
    render_pre_render_ms: float | None = None
    render_record_ms: float | None = None
    render_submit_ms: float | None = None
    render_present_ms: float | None = None
    # M25: GPU-Zeit (optional).
    gpu_frame_ms: float | None = None
    gpu_renderpass_ms: float | None = None
    deco_extract_ms: float | None = None
    tile_extract_ms: float | None = None
    deco_sprite_count: int | None = None
    stream_unload_marked: int | None = None
    stream_unload_drained: int | None = None
    pending_unload_count: int | None = None
    apply_worker_ms: float | None = None
    apply_sync_generate_ms: float | None = None
    apply_delta_ms: float | None = None
    apply_override_ms: float | None = None
    apply_pool_ms: float | None = None
    apply_collision_ms: float | None = None
    tile_visible_chunks: int | None = None
    tile_cache_hits: int | None = None
    tile_cache_misses: int | None = None
    tile_full_rebuild_ms: float | None = None
    tile_cull_ms: float | None = None
    deco_scanned_count: int | None = None
    deco_visible_count: int | None = None
    tile_visible_batches: int | None = None
    tile_registry_hits: int | None = None
    tile_registry_misses: int | None = None
    tile_cull_cache_hits: int | None = None
    tile_cull_cache_misses: int | None = None
    tile_assemble_ms: float | None = None
    tile_lod0_groups: int | None = None
    tile_lod1_groups: int | None = None
    tile_lod2_groups: int | None = None
    tile_lod0_ms: float | None = None
    tile_lod1_ms: float | None = None
    tile_lod2_ms: float | None = None
    tile_lod_switches: int | None = None
    tile_map_mode_active: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True, slots=True)
class HitchEvent:
    schema_version: int
    frame_index: int
    scenario_id: str
    tags: tuple[str, ...]
    frame_ms: float
    stream_ms: float
    stream_apply_ms: float
    stream_unload_ms: float
    stream_loaded: int
    stream_unloaded: int
    chunk_count: int
    focus_x: float
    focus_y: float
    zoom: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RunSummary:
    schema_version: int
    run_id: str
    scenario_id: str
    run_mode: str
    recorded_frames: int
    frame_ms_mean: float
    frame_ms_p95: float
    frame_ms_max: float
    stream_ms_mean: float
    stream_ms_p95: float
    stream_ms_max: float
    stream_unload_ms_p95: float
    stream_unload_ms_max: float
    hitch_count: int
    hitch_frame_count: int
    hitch_stream_count: int
    hitch_load_count: int
    hitch_unload_count: int
    max_loaded_per_frame: int
    max_unloaded_per_frame: int
    chunk_count_mean: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScenarioDescriptor:
    scenario_id: str
    frames: int
    warmup_frames: int
    extract_enabled: bool = True
    stream_enabled: bool = True
    deco_extract_enabled: bool = True
    tile_extract_enabled: bool = True
    pan_axis: str = "x"
    pan_chunks_per_frame: float = 1.0
    zoom: float = 0.35
