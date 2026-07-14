"""Gemeinsamer Szenario-Runner für CLI- und Demo-Profiling (M23)."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bridge.chunk_extractor import ChunkRenderExtractor
from bridge.decoration_extractor import decorations_to_sprites
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.config import load_profiling_config
from game_core.perf.models import ExtractStepMetrics, StreamStepMetrics
from game_core.perf.scenarios import (
    DEFAULT_SPAWN_X,
    DEFAULT_SPAWN_Y,
    DEFAULT_VIEWPORT_H,
    DEFAULT_VIEWPORT_W,
    focus_for_frame,
    scenario_descriptor,
    stream_view_for_frame,
)
from game_core.perf.session import PerfSession
from game_core.stream_view import StreamViewParams
from game_core.world import World
from game_core.world_gen import configure_world_gen, load_world_gen_config, set_debug_mode
from render_graphics.camera import camera_from_viewport
from render_scene.sprite_catalog import SpriteCatalog, catalog_from_manifest_path

DEFAULT_MANIFEST = PROJECT_ROOT / "assets" / "atlases" / "main_manifest.json"


def _load_catalog() -> SpriteCatalog:
    if DEFAULT_MANIFEST.is_file():
        return catalog_from_manifest_path(DEFAULT_MANIFEST)
    content = load_content_registry()
    mapping: dict[str, int] = {}
    for index, tile in enumerate(content.tiles):
        mapping[tile.sprite_key] = index
    for index, deco in enumerate(content.decorations):
        mapping[deco.sprite_key] = 10_000 + index
    return SpriteCatalog(key_to_id=mapping)


@dataclass
class ScenarioRuntime:
    world: World
    streamer: ChunkStreamer
    content: object
    collision: object
    extractor: ChunkRenderExtractor
    catalog: SpriteCatalog
    viewport_w: int = DEFAULT_VIEWPORT_W
    viewport_h: int = DEFAULT_VIEWPORT_H
    stream_enabled: bool = True
    deco_extract_enabled: bool = True
    tile_extract_enabled: bool = True
    _view: StreamViewParams | None = None
    _deco_sprite_count: int = 0
    _cached_deco_sprites: tuple = ()

    @property
    def chunk_count(self) -> int:
        return self.world.chunk_count

    @property
    def deco_sprite_count(self) -> int:
        return self._deco_sprite_count

    def on_scenario_step(
        self,
        focus_x: float,
        focus_y: float,
        zoom: float,
        move_dx: float,
        move_dy: float,
    ) -> None:
        self._view = stream_view_for_frame(
            focus_x,
            focus_y,
            zoom,
            move_dx=move_dx,
            move_dy=move_dy,
            viewport_w=self.viewport_w,
            viewport_h=self.viewport_h,
        )

    def on_stream_update(self, step_metrics: StreamStepMetrics) -> tuple[int, int]:
        assert self._view is not None
        if not self.stream_enabled:
            return 0, 0
        return self.streamer.update(
            self.world,
            self._view.focus_x,
            self._view.focus_y,
            self.content,
            self.collision,
            self.extractor,
            view=self._view,
            step_metrics=step_metrics,
        )

    def on_deco_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        assert self._view is not None
        if not self.deco_extract_enabled:
            self._cached_deco_sprites = ()
            self._deco_sprite_count = 0
            return 0.0
        t0 = time.perf_counter()
        camera = camera_from_viewport(
            self._view.focus_x,
            self._view.focus_y,
            self._view.zoom,
            self.viewport_w,
            self.viewport_h,
        )
        self._cached_deco_sprites = decorations_to_sprites(
            self.content,
            self.catalog,
            self.world,
            camera=camera,
            step_metrics=extract_metrics,
        )
        self._deco_sprite_count = len(self._cached_deco_sprites)
        return (time.perf_counter() - t0) * 1000.0

    def on_tile_extract(self, extract_metrics: ExtractStepMetrics | None) -> float:
        assert self._view is not None
        if not self.tile_extract_enabled:
            return 0.0
        t0 = time.perf_counter()
        camera = camera_from_viewport(
            self._view.focus_x,
            self._view.focus_y,
            self._view.zoom,
            self.viewport_w,
            self.viewport_h,
        )
        if not hasattr(self, "_cached_deco_sprites"):
            self._cached_deco_sprites = decorations_to_sprites(
                self.content,
                self.catalog,
                self.world,
                camera=camera,
                step_metrics=extract_metrics,
            )
        self.extractor.extract(camera, sprites=self._cached_deco_sprites, step_metrics=extract_metrics)
        return (time.perf_counter() - t0) * 1000.0


def build_scenario_runtime(
    *,
    viewport_w: int = DEFAULT_VIEWPORT_W,
    viewport_h: int = DEFAULT_VIEWPORT_H,
    use_mock_invalidator: bool = False,
) -> ScenarioRuntime:
    configure_world_gen(load_world_gen_config())
    set_debug_mode(None)
    content = load_content_registry()
    collision = load_collision_catalog()
    catalog = _load_catalog()
    world = World()
    streamer = ChunkStreamer()
    if use_mock_invalidator:
        invalidator = MagicMock()
    else:
        invalidator = ChunkRenderExtractor(world, catalog)
    return ScenarioRuntime(
        world=world,
        streamer=streamer,
        content=content,
        collision=collision,
        extractor=invalidator,
        catalog=catalog,
        viewport_w=viewport_w,
        viewport_h=viewport_h,
    )


def run_perf_scenario(
    scenario_id: str,
    *,
    run_mode: str = "cli",
    extract_enabled: bool | None = None,
    run_dir: Path | None = None,
    runtime: ScenarioRuntime | None = None,
) -> Path:
    config = load_profiling_config()
    descriptor = scenario_descriptor(config, scenario_id)
    extract = descriptor.extract_enabled if extract_enabled is None else extract_enabled

    session = PerfSession(
        config=config,
        scenario_id=scenario_id,
        run_mode=run_mode,
        extract_enabled=extract,
    )
    # M25: auch CLI-Runs sollen Full-Frame-Felder liefern (ohne Renderer entspricht das dem CPU-Tick).
    session.full_frame_enabled = True
    session._warmup_frames = descriptor.warmup_frames

    rt = runtime or build_scenario_runtime(use_mock_invalidator=False)
    rt.stream_enabled = descriptor.stream_enabled
    rt.deco_extract_enabled = descriptor.deco_extract_enabled
    rt.tile_extract_enabled = descriptor.tile_extract_enabled
    zoom = descriptor.zoom

    initial_view = stream_view_for_frame(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, zoom)
    rt.streamer.update(
        rt.world,
        DEFAULT_SPAWN_X,
        DEFAULT_SPAWN_Y,
        rt.content,
        rt.collision,
        rt.extractor,
        view=initial_view,
    )
    rt.world.collision_dirty_chunks.clear()

    last_focus_x, last_focus_y = DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y
    total_frames = descriptor.warmup_frames + descriptor.frames

    for tick_index in range(total_frames):
        focus_x, focus_y, frame_zoom, move_dx, move_dy = focus_for_frame(
            descriptor,
            tick_index,
            last_focus_x=last_focus_x,
            last_focus_y=last_focus_y,
        )
        session.begin_full_frame()
        frame = session.run_canonical_tick(
            rt,
            focus_x=focus_x,
            focus_y=focus_y,
            zoom=frame_zoom,
            move_dx=move_dx,
            move_dy=move_dy,
        )
        full_ms = session.end_full_frame()
        session.finalize_pending_frame(cpu_full_frame_ms=full_ms)
        if frame is not None:
            session._deco_sprite_count = rt._deco_sprite_count
        last_focus_x, last_focus_y = focus_x, focus_y

    rt.streamer.shutdown_chunk_gen_pool()
    return session.flush(run_dir)


def print_run_summary(run_dir: Path) -> None:
    import json

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    print(f"\n=== Perf Run {run_dir.name} ===")
    print(f"  scenario:        {summary['scenario_id']}")
    print(f"  recorded_frames: {summary['recorded_frames']}")
    print(f"  frame_ms mean:   {summary['frame_ms_mean']:.3f}")
    print(f"  frame_ms p95:    {summary['frame_ms_p95']:.3f}")
    print(f"  stream_ms p95:   {summary['stream_ms_p95']:.3f}")
    print(f"  hitches:         {summary['hitch_count']}")
    print(f"  export:          {run_dir}")


def main(argv: list[str] | None = None) -> int:
    """CLI-Entry — entspricht docs/benchmarks/perf/README.md."""
    import argparse

    config = load_profiling_config()
    scenarios = sorted(config.scenarios.keys())
    parser = argparse.ArgumentParser(description="Perf-Szenario ausführen und exportieren (M23/M25).")
    parser.add_argument("--scenario", choices=scenarios, default="steady", help="Szenario-ID")
    parser.add_argument("--no-extract", action="store_true", help="Extract-Pfad deaktivieren")
    parser.add_argument("--run-dir", type=Path, default=None, help="Export-Zielverzeichnis")
    args = parser.parse_args(argv)

    run_dir = run_perf_scenario(
        args.scenario,
        run_mode="cli",
        extract_enabled=not args.no_extract,
        run_dir=args.run_dir,
    )
    print_run_summary(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
