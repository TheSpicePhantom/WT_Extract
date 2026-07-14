"""PerfSession — Tick-Grenzen, Aufzeichnung, Export (M23)."""

from __future__ import annotations

import json
import subprocess
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from game_core.perf.aggregate import PerfAggregator
from game_core.perf.config import ProfilingConfig, HitchThresholds
from game_core.perf.export_schema import SCHEMA_VERSION, write_run_export
from game_core.perf.hitch import classify_hitch
from game_core.perf.models import ExtractStepMetrics, FrameMetrics, HitchEvent, StreamStepMetrics

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RUNS_DIR = PROJECT_ROOT / "docs" / "benchmarks" / "perf" / "runs"


class TickCallbacks(Protocol):
    def on_scenario_step(
        self,
        focus_x: float,
        focus_y: float,
        zoom: float,
        move_dx: float,
        move_dy: float,
    ) -> None: ...

    def on_stream_update(self, step_metrics: StreamStepMetrics) -> tuple[int, int]: ...

    def on_deco_extract(self, extract_metrics: ExtractStepMetrics | None) -> float: ...

    def on_tile_extract(self, extract_metrics: ExtractStepMetrics | None) -> float: ...

    @property
    def chunk_count(self) -> int: ...

    @property
    def deco_sprite_count(self) -> int: ...


@dataclass
class PerfSession:
    config: ProfilingConfig
    scenario_id: str
    run_mode: str
    extract_enabled: bool = True
    stream_enabled: bool = True
    deco_extract_enabled: bool = True
    tile_extract_enabled: bool = True
    run_id: str = ""
    _aggregator: PerfAggregator = field(default_factory=PerfAggregator)
    _ring: deque[FrameMetrics] = field(default_factory=deque)
    _tick_start: float = 0.0
    _scenario_ms: float = 0.0
    _stream_ms: float = 0.0
    _deco_ms: float = 0.0
    _tile_ms: float = 0.0
    _stream_step: StreamStepMetrics = field(default_factory=StreamStepMetrics)
    _extract_step: ExtractStepMetrics = field(default_factory=ExtractStepMetrics)
    _recording_index: int = 0
    _total_ticks: int = 0
    _warmup_frames: int = 0
    _last_focus_x: float = 256.0
    _last_focus_y: float = 256.0
    _current_focus_x: float = 256.0
    _current_focus_y: float = 256.0
    _current_zoom: float = 0.35
    _deco_sprite_count: int | None = None
    # M25: Full-frame Tracking (optional)
    full_frame_enabled: bool = False
    _full_frame_start: float = 0.0
    _pending_frame: FrameMetrics | None = None
    _render_timings: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.run_id:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            self.run_id = f"{timestamp}_{self.scenario_id}_{_git_commit_short()}"
        self._ring = deque(maxlen=self.config.ring_buffer_frames)

    def begin_tick(self) -> None:
        self._tick_start = time.perf_counter()
        self._scenario_ms = 0.0
        self._stream_ms = 0.0
        self._deco_ms = 0.0
        self._tile_ms = 0.0
        self._stream_step.reset()
        self._extract_step.reset()
        self._pending_frame = None
        self._render_timings.clear()

    def end_tick(self) -> None:
        pass

    # --- M25: Full-frame API (optional) ---
    def begin_full_frame(self) -> None:
        """Startet die Full-Frame-Zeitmessung (App-Frame, inkl. Render/Present-Waits)."""
        if not self.full_frame_enabled:
            return
        self._full_frame_start = time.perf_counter()
        self._render_timings.clear()

    def record_render_timing(self, name: str, ms: float) -> None:
        """Nimmt Renderer/Present CPU-Submetriken entgegen (aus render_core/render_graphics)."""
        if not self.full_frame_enabled:
            return
        if ms < 0.0:
            return
        # additive, da einige Phasen mehrfach auftreten können (Swapchain retry).
        self._render_timings[name] = self._render_timings.get(name, 0.0) + float(ms)

    def end_full_frame(self) -> float | None:
        """Beendet Full-Frame-Messung und finalisiert ggf. einen pending Frame."""
        if not self.full_frame_enabled:
            return None
        if self._full_frame_start <= 0.0:
            return None
        return (time.perf_counter() - self._full_frame_start) * 1000.0

    def run_canonical_tick(
        self,
        callbacks: TickCallbacks,
        *,
        focus_x: float,
        focus_y: float,
        zoom: float,
        move_dx: float,
        move_dy: float,
    ) -> FrameMetrics | None:
        self.begin_tick()
        self._current_focus_x = focus_x
        self._current_focus_y = focus_y
        self._current_zoom = zoom

        t0 = time.perf_counter()
        callbacks.on_scenario_step(focus_x, focus_y, zoom, move_dx, move_dy)
        self._scenario_ms = (time.perf_counter() - t0) * 1000.0

        t1 = time.perf_counter()
        loaded, unloaded = callbacks.on_stream_update(self._stream_step)
        self._stream_ms = (time.perf_counter() - t1) * 1000.0

        deco_ms: float | None = None
        tile_ms: float | None = None
        if self.extract_enabled:
            t2 = time.perf_counter()
            deco_ms = callbacks.on_deco_extract(self._extract_step)
            self._deco_ms = deco_ms
            t3 = time.perf_counter()
            tile_ms = callbacks.on_tile_extract(self._extract_step)
            self._tile_ms = tile_ms
            _ = t2, t3

        frame_ms = (time.perf_counter() - self._tick_start) * 1000.0
        self._total_ticks += 1

        if self._total_ticks <= self._warmup_frames:
            self._last_focus_x, self._last_focus_y = focus_x, focus_y
            return None

        apply_detail = self._stream_step.apply_ms > 0.0
        tile_detail = tile_ms is not None and tile_ms > 0.0
        frame = FrameMetrics(
            schema_version=SCHEMA_VERSION,
            frame_index=self._recording_index,
            scenario_id=self.scenario_id,
            frame_ms=frame_ms,
            stream_ms=self._stream_step.total_ms,
            stream_apply_ms=self._stream_step.apply_ms,
            stream_unload_ms=self._stream_step.unload_ms,
            stream_loaded=loaded,
            stream_unloaded=unloaded,
            chunk_count=callbacks.chunk_count,
            focus_x=focus_x,
            focus_y=focus_y,
            zoom=zoom,
            deco_extract_ms=deco_ms,
            tile_extract_ms=tile_ms,
            deco_sprite_count=callbacks.deco_sprite_count if self.extract_enabled else None,
            stream_unload_marked=self._stream_step.unload_marked,
            stream_unload_drained=unloaded,
            pending_unload_count=self._stream_step.pending_unload_count,
            apply_worker_ms=self._stream_step.apply_worker_ms if apply_detail else None,
            apply_sync_generate_ms=self._stream_step.apply_sync_generate_ms if apply_detail else None,
            apply_delta_ms=self._stream_step.apply_delta_ms if apply_detail else None,
            apply_override_ms=self._stream_step.apply_override_ms if apply_detail else None,
            apply_pool_ms=self._stream_step.apply_pool_ms if apply_detail else None,
            apply_collision_ms=self._stream_step.apply_collision_ms if apply_detail else None,
            apply_pool_poll_ms=self._stream_step.apply_pool_poll_ms if apply_detail else None,
            apply_pool_submit_ms=self._stream_step.apply_pool_submit_ms if apply_detail else None,
            apply_pool_apply_ms=self._stream_step.apply_pool_apply_ms if apply_detail else None,
            apply_pool_suppress_ms=self._stream_step.apply_pool_suppress_ms if apply_detail else None,
            apply_pool_discard_ms=self._stream_step.apply_pool_discard_ms if apply_detail else None,
            apply_pool_route_passes=self._stream_step.apply_pool_route_passes if apply_detail else None,
            apply_pool_in_flight_peak=self._stream_step.apply_pool_in_flight_peak if apply_detail else None,
            apply_pool_idle_skip=self._stream_step.apply_pool_idle_skip if apply_detail else None,
            tile_visible_chunks=self._extract_step.tile_visible_chunks if tile_detail else None,
            tile_cache_hits=self._extract_step.tile_cache_hits if tile_detail else None,
            tile_cache_misses=self._extract_step.tile_cache_misses if tile_detail else None,
            tile_full_rebuild_ms=self._extract_step.tile_full_rebuild_ms if tile_detail else None,
            tile_cull_ms=self._extract_step.tile_cull_ms if tile_detail else None,
            deco_scanned_count=self._extract_step.deco_scanned_count if tile_detail else None,
            deco_visible_count=self._extract_step.deco_visible_count if tile_detail else None,
            tile_visible_batches=self._extract_step.tile_visible_batches if tile_detail else None,
            tile_registry_hits=self._extract_step.tile_registry_hits if tile_detail else None,
            tile_registry_misses=self._extract_step.tile_registry_misses if tile_detail else None,
            tile_cull_cache_hits=self._extract_step.tile_cull_cache_hits if tile_detail else None,
            tile_cull_cache_misses=self._extract_step.tile_cull_cache_misses if tile_detail else None,
            tile_assemble_ms=self._extract_step.tile_assemble_ms if tile_detail else None,
            tile_lod0_groups=self._extract_step.tile_lod0_groups if tile_detail else None,
            tile_lod1_groups=self._extract_step.tile_lod1_groups if tile_detail else None,
            tile_lod2_groups=self._extract_step.tile_lod2_groups if tile_detail else None,
            tile_lod0_ms=self._extract_step.tile_lod0_ms if tile_detail else None,
            tile_lod1_ms=self._extract_step.tile_lod1_ms if tile_detail else None,
            tile_lod2_ms=self._extract_step.tile_lod2_ms if tile_detail else None,
            tile_lod_switches=self._extract_step.tile_lod_switches if tile_detail else None,
            tile_map_mode_active=self._extract_step.tile_map_mode_active if tile_detail else None,
        )
        if self.full_frame_enabled:
            # Finalisierung erfolgt nach Render/Present via end_full_frame().
            self._pending_frame = frame
            self._last_focus_x, self._last_focus_y = focus_x, focus_y
            return frame
        return self._finalize_frame(frame)

    def finalize_pending_frame(self, *, cpu_full_frame_ms: float | None) -> FrameMetrics | None:
        """Finalisiert den pending Frame (M25), inkl. Render/Present Submetriken."""
        if not self.full_frame_enabled:
            return None
        frame = self._pending_frame
        if frame is None:
            return None
        self._pending_frame = None

        frame.cpu_full_frame_ms = cpu_full_frame_ms
        frame.render_wait_fence_ms = self._render_timings.get("wait_fence_ms")
        frame.render_acquire_ms = self._render_timings.get("acquire_ms")
        frame.render_pre_render_ms = self._render_timings.get("pre_render_ms")
        frame.render_record_ms = self._render_timings.get("record_ms")
        frame.render_submit_ms = self._render_timings.get("submit_ms")
        frame.render_present_ms = self._render_timings.get("present_ms")
        frame.gpu_frame_ms = self._render_timings.get("gpu_frame_ms")
        frame.gpu_renderpass_ms = self._render_timings.get("gpu_renderpass_ms")

        # Aggregate render/present categories if present.
        render_cpu_ms = 0.0
        present_wait_cpu_ms = 0.0
        for key, value in self._render_timings.items():
            if key in ("pre_render_ms", "record_ms", "submit_ms"):
                render_cpu_ms += value
            if key in ("wait_fence_ms", "acquire_ms", "present_ms"):
                present_wait_cpu_ms += value
        frame.render_cpu_ms = render_cpu_ms if render_cpu_ms > 0.0 else None
        frame.present_wait_cpu_ms = (
            present_wait_cpu_ms if present_wait_cpu_ms > 0.0 else None
        )

        if frame.cpu_full_frame_ms is not None:
            attributed = 0.0
            for v in (
                frame.frame_ms,
                frame.render_cpu_ms or 0.0,
                frame.present_wait_cpu_ms or 0.0,
            ):
                attributed += v
            rest = frame.cpu_full_frame_ms - max(attributed - frame.frame_ms, 0.0) - frame.frame_ms
            # Rest hier ist konservativ; in späteren Phasen werden Phasen disjunkt.
            frame.cpu_unattributed_ms = max(rest, 0.0)

        return self._finalize_frame(frame)

    def _finalize_frame(self, frame: FrameMetrics) -> FrameMetrics:
        self._recording_index += 1
        self._aggregator.record_frame(frame)
        self._ring.append(frame)

        tags = classify_hitch(frame, self.config.hitch)
        if tags:
            hitch = HitchEvent(
                schema_version=SCHEMA_VERSION,
                frame_index=frame.frame_index,
                scenario_id=self.scenario_id,
                tags=tags,
                frame_ms=frame.frame_ms,
                stream_ms=frame.stream_ms,
                stream_apply_ms=frame.stream_apply_ms,
                stream_unload_ms=frame.stream_unload_ms,
                stream_loaded=frame.stream_loaded,
                stream_unloaded=frame.stream_unloaded,
                chunk_count=frame.chunk_count,
                focus_x=frame.focus_x,
                focus_y=frame.focus_y,
                zoom=frame.zoom,
            )
            self._aggregator.record_hitch(hitch)

        return frame

    @property
    def rolling_stream_ms_mean(self) -> float:
        if not self._ring:
            return 0.0
        return sum(frame.stream_ms for frame in self._ring) / len(self._ring)

    @property
    def rolling_chunk_count(self) -> int:
        if not self._ring:
            return 0
        return self._ring[-1].chunk_count

    @property
    def rolling_hitch_count(self) -> int:
        return len(self._aggregator.hitches)

    def flush(self, run_dir: Path | None = None) -> Path:
        destination = run_dir or (DEFAULT_RUNS_DIR / self.run_id)
        summary = self._aggregator.build_summary(
            schema_version=SCHEMA_VERSION,
            run_id=self.run_id,
            scenario_id=self.scenario_id,
            run_mode=self.run_mode,
        )
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "scenario_id": self.scenario_id,
            "run_mode": self.run_mode,
            "extract_enabled": self.extract_enabled,
            "stream_enabled": self.stream_enabled,
            "deco_extract_enabled": self.deco_extract_enabled,
            "tile_extract_enabled": self.tile_extract_enabled,
            "warmup_frames": self._warmup_frames,
            "recorded_frames": summary.recorded_frames,
            "git_commit": _git_commit_short(),
            "config_fingerprint": _config_fingerprint(),
        }
        write_run_export(
            destination,
            manifest=manifest,
            frames=self._aggregator.frames,
            hitches=self._aggregator.hitches,
            summary=summary,
        )
        return destination


def _git_commit_short() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _config_fingerprint() -> dict[str, str]:
    fingerprints: dict[str, str] = {}
    for name, relative in (
        ("profiling", "assets/content/profiling.json"),
        ("streaming", "assets/content/streaming.json"),
        ("world_gen", "assets/content/world_gen.json"),
        ("visibility_lod", "assets/content/visibility_lod.json"),
    ):
        path = PROJECT_ROOT / relative
        if path.is_file():
            fingerprints[name] = str(hash(path.read_text(encoding="utf-8")))
    return fingerprints
