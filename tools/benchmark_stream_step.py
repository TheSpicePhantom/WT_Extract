"""M24c.2 — Streaming-E2E-Benchmark: Cold/Warm-Split mit Submit-Trace."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.models import StreamStepMetrics
from game_core.stream_view import StreamViewParams
from game_core.world import CHUNK_SIZE_PX, World
from game_core.world_gen import configure_world_gen, load_world_gen_config, set_debug_mode

OUTPUT_DIR = PROJECT_ROOT / "docs" / "benchmarks"
BASELINES_DIR = OUTPUT_DIR / "baselines"
DEFAULT_OUTPUT = BASELINES_DIR / "stream_step_warm_m24c2.json"
PIPELINE_VERSION = "M24c.2"


@dataclass(frozen=True, slots=True)
class StepRecord:
    phase: str
    step: int
    focus_x: float
    focus_y: float
    stream_ms: float
    total_ms: float
    apply_sync_generate_ms: float
    sync_fallback_triggered: int
    sync_skipped_worker_submitted: int
    sync_skipped_pending_result: int
    terrain_submit_attempted: int
    terrain_submit_accepted: int
    terrain_applied: int
    deco_applied: int
    terrain_discarded_stale: int
    loaded: int
    unloaded: int
    chunk_count: int


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, min(len(ordered) - 1, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return ordered[rank]


def _summarize(records: list[StepRecord], *, phase: str) -> dict:
    phase_records = [r for r in records if r.phase == phase]
    if not phase_records:
        return {"phase": phase, "steps": 0}
    stream_times = [r.stream_ms for r in phase_records]
    submit_gap_steps = sum(
        1
        for r in phase_records
        if r.terrain_submit_attempted > r.terrain_submit_accepted
    )
    return {
        "phase": phase,
        "steps": len(phase_records),
        "stream_ms_p50": round(statistics.median(stream_times), 3),
        "stream_ms_p95": round(_percentile(stream_times, 95.0), 3),
        "stream_ms_max": round(max(stream_times), 3),
        "apply_sync_generate_ms_total": round(
            sum(r.apply_sync_generate_ms for r in phase_records), 3
        ),
        "sync_fallback_triggered_total": sum(r.sync_fallback_triggered for r in phase_records),
        "sync_skipped_worker_submitted_total": sum(
            r.sync_skipped_worker_submitted for r in phase_records
        ),
        "sync_skipped_pending_result_total": sum(
            r.sync_skipped_pending_result for r in phase_records
        ),
        "terrain_submit_attempted_total": sum(r.terrain_submit_attempted for r in phase_records),
        "terrain_submit_accepted_total": sum(r.terrain_submit_accepted for r in phase_records),
        "submit_gap_steps": submit_gap_steps,
        "submit_gap_pct": round(100.0 * submit_gap_steps / len(phase_records), 2),
        "terrain_applied_total": sum(r.terrain_applied for r in phase_records),
        "deco_applied_total": sum(r.deco_applied for r in phase_records),
    }


def _run_steps(
    streamer: ChunkStreamer,
    world: World,
    content,
    collision,
    extractor,
    *,
    phase: str,
    steps: int,
    step_px: float,
    start_x: float,
    start_y: float,
) -> tuple[list[StepRecord], float, float]:
    records: list[StepRecord] = []
    focus_x, focus_y = start_x, start_y
    for step in range(steps):
        view = StreamViewParams(
            focus_x=focus_x,
            focus_y=focus_y,
            player_x=focus_x,
            player_y=focus_y,
            zoom=0.35,
            viewport_w=1280,
            viewport_h=720,
        )
        metrics = StreamStepMetrics()
        t0 = time.perf_counter()
        loaded, unloaded = streamer.update(
            world,
            focus_x,
            focus_y,
            content,
            collision,
            extractor,
            view=view,
            step_metrics=metrics,
        )
        stream_ms = (time.perf_counter() - t0) * 1000.0
        records.append(
            StepRecord(
                phase=phase,
                step=step,
                focus_x=focus_x,
                focus_y=focus_y,
                stream_ms=stream_ms,
                total_ms=metrics.total_ms,
                apply_sync_generate_ms=metrics.apply_sync_generate_ms,
                sync_fallback_triggered=metrics.sync_fallback_triggered,
                sync_skipped_worker_submitted=metrics.sync_skipped_worker_submitted,
                sync_skipped_pending_result=metrics.sync_skipped_pending_result,
                terrain_submit_attempted=metrics.terrain_submit_attempted,
                terrain_submit_accepted=metrics.terrain_submit_accepted,
                terrain_applied=metrics.terrain_applied,
                deco_applied=metrics.deco_applied,
                terrain_discarded_stale=metrics.terrain_discarded_stale,
                loaded=loaded,
                unloaded=unloaded,
                chunk_count=world.chunk_count,
            )
        )
        focus_x += step_px
        focus_y += step_px * 0.25
    end_x, end_y = focus_x, focus_y
    return records, end_x, end_y


def run_stream_benchmark(
    *,
    warmup_steps: int,
    measure_steps: int,
    step_px: float,
    start_x: float,
    start_y: float,
    pool_warmup: bool,
) -> tuple[list[StepRecord], dict, dict]:
    configure_world_gen(load_world_gen_config())
    set_debug_mode(None)
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    streamer = ChunkStreamer()
    if pool_warmup:
        streamer.warmup_chunk_gen_pool()
    extractor = MagicMock()

    cold_records: list[StepRecord] = []
    warm_records: list[StepRecord] = []
    focus_x, focus_y = start_x, start_y

    if warmup_steps > 0:
        cold_records, focus_x, focus_y = _run_steps(
            streamer,
            world,
            content,
            collision,
            extractor,
            phase="warmup",
            steps=warmup_steps,
            step_px=step_px,
            start_x=focus_x,
            start_y=focus_y,
        )

    warm_records, _, _ = _run_steps(
        streamer,
        world,
        content,
        collision,
        extractor,
        phase="measure",
        steps=measure_steps,
        step_px=step_px,
        start_x=focus_x,
        start_y=focus_y,
    )

    all_records = cold_records + warm_records
    cold_summary = _summarize(all_records, phase="warmup") if warmup_steps > 0 else None
    warm_summary = _summarize(all_records, phase="measure")
    combined = {
        "pipeline_version": PIPELINE_VERSION,
        "warmup_steps": warmup_steps,
        "measure_steps": measure_steps,
        "warm_summary": warm_summary,
    }
    if cold_summary is not None:
        combined["cold_summary"] = cold_summary
    streamer.shutdown_chunk_gen_pool()
    return all_records, combined, warm_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="M24c.2 Streaming-E2E-Benchmark")
    parser.add_argument("--warmup-steps", type=int, default=20)
    parser.add_argument("--measure-steps", type=int, default=100)
    parser.add_argument("--steps", type=int, default=None, help="Legacy: nur measure-steps")
    parser.add_argument("--step-px", type=float, default=float(CHUNK_SIZE_PX * 2))
    parser.add_argument("--start", type=float, nargs=2, default=(0.0, 0.0), metavar=("X", "Y"))
    parser.add_argument("--no-pool-warmup", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--phase0", action="store_true", help="Phase-0-Diagnose-Output")
    args = parser.parse_args()

    measure_steps = args.measure_steps
    if args.steps is not None:
        measure_steps = args.steps

    records, combined, warm_summary = run_stream_benchmark(
        warmup_steps=args.warmup_steps,
        measure_steps=measure_steps,
        step_px=args.step_px,
        start_x=args.start[0],
        start_y=args.start[1],
        pool_warmup=not args.no_pool_warmup,
    )

    if args.phase0:
        args.output = BASELINES_DIR / "stream_step_m24c2_phase0.json"

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": combined,
        "steps": [asdict(r) for r in records],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(combined, indent=2))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
