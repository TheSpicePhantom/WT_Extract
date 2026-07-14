"""World-Gen Performance-Benchmarks (M22b)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_JSON = PROJECT_ROOT / "docs" / "benchmarks" / "world_gen_m22b.json"
BENCHMARK_MD = PROJECT_ROOT / "docs" / "benchmarks" / "world_gen_m22b.md"

sys.path.insert(0, str(PROJECT_ROOT))

from game_core.chunk_streaming import coords_in_radius
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.world import CHUNK_SIZE_TILES, World
from game_core.world_gen import (
    configure_world_gen,
    generate_chunk,
    generate_demo_world,
    load_world_gen_config,
    populate_chunk_decorations,
    sample_climate,
    set_debug_mode,
)

BENCH_COORDS = [(cx, cy) for cy in range(8) for cx in range(8)]
STREAMING_COORDS = sorted(coords_in_radius((0, 0), 8))


def _git_commit() -> str:
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


def _timed(callable_obj) -> float:
    start = time.perf_counter()
    callable_obj()
    return time.perf_counter() - start


def collect_metrics(*, use_parallel: bool) -> dict[str, float]:
    from dataclasses import replace

    config = load_world_gen_config()
    if use_parallel:
        config = replace(config, parallel_workers="auto", parallel_prefetch=True)
    else:
        config = replace(config, parallel_workers=0, parallel_prefetch=False)
    configure_world_gen(config)
    set_debug_mode(None)
    content = load_content_registry()
    collision = load_collision_catalog()

    def noise_only() -> None:
        for cx, cy in BENCH_COORDS:
            for ty in range(CHUNK_SIZE_TILES):
                for tx in range(CHUNK_SIZE_TILES):
                    wx = cx * CHUNK_SIZE_TILES + tx
                    wy = cy * CHUNK_SIZE_TILES + ty
                    sample_climate(float(wx), float(wy))

    def generate_chunks() -> None:
        for cx, cy in BENCH_COORDS:
            generate_chunk(cx, cy)

    def decorations() -> None:
        world = World()
        for cx, cy in BENCH_COORDS:
            world.chunks[(cx, cy)] = generate_chunk(cx, cy)
            populate_chunk_decorations(world, content, cx, cy)

    def solid_rebuild() -> None:
        world = World()
        for cx, cy in BENCH_COORDS:
            world.chunks[(cx, cy)] = generate_chunk(cx, cy)
            world.rebuild_chunk_solid((cx, cy), content, collision)

    def apply_full() -> None:
        world = World()
        for cx, cy in BENCH_COORDS:
            world.chunks[(cx, cy)] = generate_chunk(cx, cy)
            populate_chunk_decorations(world, content, cx, cy)
            world.rebuild_chunk_solid((cx, cy), content, collision)

    def demo_world() -> None:
        generate_demo_world(16, 16)

    def streaming_first_load() -> None:
        for cx, cy in STREAMING_COORDS:
            generate_chunk(cx, cy)

    return {
        "noise_only_s": _timed(noise_only),
        "generate_chunk_s": _timed(generate_chunks),
        "decorations_s": _timed(decorations),
        "solid_rebuild_s": _timed(solid_rebuild),
        "apply_full_s": _timed(apply_full),
        "demo_world_16x16_s": _timed(demo_world),
        "streaming_first_load_s": _timed(streaming_first_load),
    }


def write_label(label: str, metrics: dict[str, float]) -> None:
    BENCHMARK_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload: dict = {}
    if BENCHMARK_JSON.is_file():
        payload = json.loads(BENCHMARK_JSON.read_text(encoding="utf-8"))
    payload[label] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "commit": _git_commit(),
        "metrics": metrics,
    }
    BENCHMARK_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _write_markdown(payload)


def _write_markdown(payload: dict) -> None:
    metric_names = [
        "noise_only_s",
        "generate_chunk_s",
        "decorations_s",
        "solid_rebuild_s",
        "apply_full_s",
        "demo_world_16x16_s",
        "streaming_first_load_s",
    ]
    lines = [
        "# World-Gen Performance — M22b",
        "",
        "| Metrik | Baseline | Parallel | Speedup |",
        "|--------|----------|----------|---------|",
    ]
    baseline = payload.get("baseline", {}).get("metrics", {})
    parallel = payload.get("parallel", {}).get("metrics", {})
    for name in metric_names:
        base_val = baseline.get(name)
        par_val = parallel.get(name)
        if base_val is not None and par_val is not None and par_val > 0:
            speedup = f"{base_val / par_val:.2f}×"
        else:
            speedup = "—"
        base_text = f"{base_val:.3f}s" if base_val is not None else "—"
        par_text = f"{par_val:.3f}s" if par_val is not None else "—"
        lines.append(f"| `{name}` | {base_text} | {par_text} | {speedup} |")
    lines.extend(
        [
            "",
            "Ausführung:",
            "",
            "```bash",
            "python tools/benchmark_world_gen.py --label baseline",
            "python tools/benchmark_world_gen.py --label parallel",
            "python tools/benchmark_world_gen.py --compare",
            "```",
        ]
    )
    for label in ("baseline", "parallel"):
        entry = payload.get(label)
        if entry:
            lines.append(f"\n**{label}** — {entry.get('timestamp', '?')} @ `{entry.get('commit', '?')}`")
    BENCHMARK_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def compare_labels() -> None:
    if not BENCHMARK_JSON.is_file():
        print("Keine Benchmark-Daten — zuerst --label baseline/parallel ausführen.", file=sys.stderr)
        sys.exit(1)
    payload = json.loads(BENCHMARK_JSON.read_text(encoding="utf-8"))
    _write_markdown(payload)
    baseline = payload.get("baseline", {}).get("metrics", {})
    parallel = payload.get("parallel", {}).get("metrics", {})
    if not baseline or not parallel:
        print("Vergleich benötigt baseline und parallel.", file=sys.stderr)
        sys.exit(1)
    print("World-Gen Benchmark Vergleich")
    for key in baseline:
        base_val = baseline[key]
        par_val = parallel.get(key)
        if par_val is None:
            continue
        ratio = base_val / par_val if par_val > 0 else float("inf")
        print(f"  {key}: {base_val:.3f}s -> {par_val:.3f}s ({ratio:.2f}x)")


def main() -> int:
    parser = argparse.ArgumentParser(description="World-Gen Benchmarks (M22b)")
    parser.add_argument("--label", choices=("baseline", "parallel"), help="Messung speichern")
    parser.add_argument("--compare", action="store_true", help="baseline vs parallel vergleichen")
    args = parser.parse_args()

    if args.compare:
        compare_labels()
        return 0
    if not args.label:
        parser.error("--label oder --compare erforderlich")
    print(f"Sammle Metriken ({args.label}) …")
    metrics = collect_metrics(use_parallel=args.label == "parallel")
    for key, value in metrics.items():
        print(f"  {key}: {value:.3f}s")
    write_label(args.label, metrics)
    print(f"Geschrieben: {BENCHMARK_JSON}")
    print(f"Aktualisiert: {BENCHMARK_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
