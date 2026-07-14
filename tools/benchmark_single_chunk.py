"""Micro-Benchmark — ein 64×64-Chunk, M24c Terrain→Deco-Pipeline (Sync + Worker)."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.chunk_build import BuildCoordinator, ChunkBuildState
from game_core.chunk_stage import (
    apply_deco_stage,
    apply_terrain_stage,
    build_deco_stage,
    build_terrain_stage,
    to_deco_result,
    to_terrain_result,
)
from game_core.content_registry import load_content_registry
from game_core.world import CHUNK_SIZE_TILES, CHUNK_TILE_COUNT, World
from game_core.world_gen import (
    configure_world_gen,
    get_world_gen_config,
    load_world_gen_config,
    set_debug_mode,
)
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_parallel import (
    _generate_deco_task,
    _generate_terrain_task,
    get_or_create_pool,
    resolve_worker_count,
    shutdown_parallel_pool,
)

DEFAULT_COORD = (1, 1)
OUTPUT_DIR = PROJECT_ROOT / "docs" / "benchmarks"
DEFAULT_OUTPUT_BASENAME = "single_chunk_64.json"
PIPELINE_VERSION = "M24c"


@dataclass(frozen=True, slots=True)
class StepTiming:
    name: str
    thread: str
    ms: float
    notes: str = ""


def _ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000.0


def _timed(name: str, thread: str, fn, *, notes: str = "") -> StepTiming:
    start = time.perf_counter()
    fn()
    return StepTiming(name=name, thread=thread, ms=_ms(start), notes=notes)


def _prefixed_output_path(base: Path, prefix: str) -> Path:
    return base.parent / f"{prefix}{base.name}"


def _fresh_build_key(coordinator: BuildCoordinator, coord: tuple[int, int]):
    return coordinator.next_terrain_build_key(coord)


def collect_cost_breakdown(coord: tuple[int, int]) -> dict:
    """M24c Phase 0 — Sub-Timings innerhalb build_terrain_stage."""
    from game_core.terrain_gen_profile import begin_profile, end_profile

    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    ctx = WorldGenContext.from_configs(config)
    coordinator = BuildCoordinator()
    build_key = _fresh_build_key(coordinator, coord)

    begin_profile()
    build_terrain_stage(build_key, ctx)
    profile = end_profile()
    assert profile is not None

    breakdown = profile.to_dict()
    breakdown["hypotheses_pct"] = _map_hypotheses(breakdown)
    return breakdown


def _map_hypotheses(breakdown: dict) -> dict[str, float]:
    """H1–H7 grobe Zuordnung zu Profil-Sektionen."""
    pct = breakdown.get("breakdown_pct", {})
    field_cache = pct.get("field_cache_climate", 0.0) + pct.get("field_cache_region", 0.0)
    noise = pct.get("noise_fbm", 0.0) + pct.get("noise_simplex", 0.0)
    resolve = pct.get("resolve_tiles", 0.0)
    coast = pct.get("coast_overlay", 0.0)
    start = pct.get("start_area_rules", 0.0)
    builds = breakdown.get("field_cache_builds", 0)
    h1_dup = 50.0 if builds > 1 else 0.0
    return {
        "H1_double_field_cache": h1_dup,
        "H2_perm_noise": noise,
        "H3_biome_region_redundancy": pct.get("field_cache_region", 0.0),
        "H4_spawn_score": start,
        "H5_coast_overlay": coast,
        "H6_resolve_python_overhead": resolve,
        "H7_field_cache_structure": field_cache,
    }


def collect_timings(coord: tuple[int, int], *, include_decorations: bool) -> list[StepTiming]:
    cx, cy = coord
    content = load_content_registry()
    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    ctx = WorldGenContext.from_configs(config)
    coordinator = BuildCoordinator()
    build_key = _fresh_build_key(coordinator, coord)

    timings: list[StepTiming] = []
    terrain_stage_holder: list = []
    terrain_result_holder: list = []
    deco_stage_holder: list = []
    deco_result_holder: list = []

    # --- Sync-Pfad (Main-Thread, M24b Stage-API) ---
    timings.append(
        _timed(
            "build_terrain_stage",
            "main",
            lambda: terrain_stage_holder.append(build_terrain_stage(build_key, ctx)),
            notes=f"{CHUNK_TILE_COUNT} Tiles + field_cache",
        )
    )
    terrain_stage = terrain_stage_holder[0]
    terrain_result = to_terrain_result(terrain_stage)
    terrain_result_holder.append(terrain_result)

    world_terrain = World()
    build_state_terrain = ChunkBuildState()
    timings.append(
        _timed(
            "apply_terrain_stage",
            "main",
            lambda: apply_terrain_stage(
                world_terrain, terrain_result, content, build_state_terrain
            ),
            notes="Chunk in world.chunks, kein solid_grid",
        )
    )

    if include_decorations:
        timings.append(
            _timed(
                "build_deco_stage",
                "main",
                lambda: deco_stage_holder.append(build_deco_stage(terrain_stage, ctx)),
                notes="compute_procedural_decorations + build_chunk_solid_grid",
            )
        )
        deco_stage = deco_stage_holder[0]
        deco_result = to_deco_result(deco_stage)
        deco_result_holder.append(deco_result)

        world_deco = World()
        build_state_deco = ChunkBuildState()
        apply_terrain_stage(world_deco, terrain_result, content, build_state_deco)
        timings.append(
            _timed(
                "apply_deco_stage",
                "main",
                lambda: apply_deco_stage(world_deco, deco_result, content, build_state_deco),
                notes="batch-deco + solid_grid vom DecoResult",
            )
        )

        sync_step_names = {
            "build_terrain_stage",
            "apply_terrain_stage",
            "build_deco_stage",
            "apply_deco_stage",
        }
        sync_notes = "M24c Sync: terrain build/apply + deco build/apply"
    else:
        sync_step_names = {"build_terrain_stage", "apply_terrain_stage"}
        sync_notes = "M24c Sync terrain-only: kein Deco/Solid"

    sync_total = sum(step.ms for step in timings if step.name in sync_step_names)
    timings.append(
        StepTiming(
            name="sync_load_total",
            thread="main",
            ms=sync_total,
            notes=sync_notes,
        )
    )

    # --- Worker-CPU (ProcessPool, M24b zwei Jobtypen) ---
    workers = max(1, resolve_worker_count(config.parallel_workers))
    worker_coordinator = BuildCoordinator()
    worker_build_key = _fresh_build_key(worker_coordinator, coord)
    executor = get_or_create_pool(ctx, workers)
    assert executor is not None

    worker_terrain_holder: list = []

    def _worker_terrain() -> None:
        worker_terrain_holder.clear()
        worker_terrain_holder.append(
            executor.submit(_generate_terrain_task, worker_build_key).result()
        )

    timings.append(
        _timed(
            "worker_build_terrain_stage",
            "worker",
            _worker_terrain,
            notes=f"ProcessPool workers={workers}, IPC=TerrainResult",
        )
    )
    worker_terrain_result = worker_terrain_holder[0]

    world_worker = World()
    build_state_worker = ChunkBuildState()
    timings.append(
        _timed(
            "apply_terrain_stage_after_worker",
            "main",
            lambda: apply_terrain_stage(
                world_worker, worker_terrain_result, content, build_state_worker
            ),
            notes="Main-Apply nach Worker-Terrain",
        )
    )

    if include_decorations:
        worker_deco_holder: list = []

        def _worker_deco() -> None:
            worker_deco_holder.clear()
            worker_deco_holder.append(
                executor.submit(_generate_deco_task, worker_build_key).result()
            )

        timings.append(
            _timed(
                "worker_build_deco_stage",
                "worker",
                _worker_deco,
                notes="field_cache aus Worker-LRU, IPC=DecoResult",
            )
        )
        worker_deco_result = worker_deco_holder[0]

        timings.append(
            _timed(
                "apply_deco_stage_after_worker",
                "main",
                lambda: apply_deco_stage(
                    world_worker, worker_deco_result, content, build_state_worker
                ),
                notes="Main-Apply nach Worker-Deco, kein Main-rebuild",
            )
        )

        worker_apply_total = sum(
            step.ms
            for step in timings
            if step.name in {"apply_terrain_stage_after_worker", "apply_deco_stage_after_worker"}
        )
        worker_apply_notes = "M24c Main-Apply: terrain + deco, ohne rebuild_chunk_solid"
    else:
        worker_apply_total = sum(
            step.ms
            for step in timings
            if step.name == "apply_terrain_stage_after_worker"
        )
        worker_apply_notes = "M24c terrain-only: nur apply_terrain_stage auf Main"

    timings.append(
        StepTiming(
            name="worker_apply_main_total",
            thread="main",
            ms=worker_apply_total,
            notes=worker_apply_notes,
        )
    )

    shutdown_parallel_pool()
    return timings


def _print_report(coord: tuple[int, int], timings: list[StepTiming], *, label: str) -> None:
    print(f"\n=== {label} — coord={coord}, CHUNK_SIZE_TILES={CHUNK_SIZE_TILES} ===")
    print(f"{'Schritt':<36} {'Thread':<8} {'ms':>10}  Notizen")
    print("-" * 90)
    for step in timings:
        print(f"{step.name:<36} {step.thread:<8} {step.ms:>10.2f}  {step.notes}")
    print("-" * 90)


def _write_payload(
    output_path: Path,
    coord: tuple[int, int],
    timings: list[StepTiming],
    *,
    include_decorations: bool,
    cost_breakdown: dict | None = None,
) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "include_decorations": include_decorations,
        "coord": list(coord),
        "chunk_size_tiles": CHUNK_SIZE_TILES,
        "chunk_tile_count": CHUNK_TILE_COUNT,
        "steps": [
            {
                "name": step.name,
                "thread": step.thread,
                "ms": round(step.ms, 3),
                "notes": step.notes,
            }
            for step in timings
        ],
    }
    if cost_breakdown is not None:
        payload["cost_breakdown"] = cost_breakdown
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Geschrieben: {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Einzelner 64×64-Chunk — M24c Terrain/Deco Schritt-Timing"
    )
    parser.add_argument("--coord", nargs=2, type=int, metavar=("CX", "CY"), default=DEFAULT_COORD)
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR / DEFAULT_OUTPUT_BASENAME,
        help="JSON-Basisname (es entstehen deco_<name> und nodeco_<name>)",
    )
    parser.add_argument(
        "--cost-breakdown",
        action="store_true",
        help="Zusätzlich cost_breakdown für nodeco-Lauf (terrain-only)",
    )
    args = parser.parse_args()
    coord = (args.coord[0], args.coord[1])

    configure_world_gen(load_world_gen_config())
    set_debug_mode(None)

    cost_breakdown = None
    if args.cost_breakdown:
        print(f"Cost breakdown coord={coord} ...")
        cost_breakdown = collect_cost_breakdown(coord)

    runs = (
        ("deco_", True, "Mit Decoration (M24c vollständig)"),
        ("nodeco_", False, "Ohne Decoration (M24c terrain-only)"),
    )
    print(f"Messe coord={coord} ... (2 Läufe, kann mehrere Minuten dauern)")

    for prefix, include_decorations, label in runs:
        timings = collect_timings(coord, include_decorations=include_decorations)
        _print_report(coord, timings, label=label)
        output_path = _prefixed_output_path(args.output, prefix)
        breakdown_for_run = cost_breakdown if not include_decorations else None
        _write_payload(
            output_path,
            coord,
            timings,
            include_decorations=include_decorations,
            cost_breakdown=breakdown_for_run,
        )

    if cost_breakdown is not None:
        breakdown_path = OUTPUT_DIR / "terrain_cost_breakdown_baseline.json"
        breakdown_path.write_text(
            json.dumps(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "pipeline_version": PIPELINE_VERSION,
                    "coord": list(coord),
                    **cost_breakdown,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"Cost breakdown: {breakdown_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
