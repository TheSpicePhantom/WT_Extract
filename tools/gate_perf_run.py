"""CI Gate für Perf-Runs (M25).

Ziel: harte Regression-Gates für Full-Frame Metriken, ohne Summary-Schema zu ändern.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.load import RunLoadError, load_run  # noqa: E402
from game_core.perf.run_analysis.stats import percentile  # noqa: E402


def _load_frames(run_dir: Path):
    loaded = load_run(run_dir)
    return loaded.frames


def gate_cpu_full_frame_p95(frames, *, max_ms: float) -> tuple[bool, str]:
    values = [f.cpu_full_frame_ms for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not values:
        return False, "cpu_full_frame_ms fehlt in frames.jsonl"
    p95 = percentile([float(v) for v in values], 0.95)
    ok = p95 <= max_ms
    return ok, f"cpu_full_frame_ms_p95={p95:.3f}ms (max={max_ms:.3f}ms)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CI Gate für Perf-Runs (M25)")
    parser.add_argument("run_dir", type=Path, help="Run-Verzeichnis (manifest/frames/summary/hitches)")
    parser.add_argument("--cpu-full-frame-p95-max-ms", type=float, default=None)
    args = parser.parse_args(argv)

    try:
        frames = _load_frames(args.run_dir)
    except RunLoadError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 2

    checks: list[tuple[bool, str]] = []
    if args.cpu_full_frame_p95_max_ms is not None:
        checks.append(gate_cpu_full_frame_p95(frames, max_ms=float(args.cpu_full_frame_p95_max_ms)))

    if not checks:
        print("Keine Gates angegeben.", file=sys.stderr)
        return 2

    failed = [msg for ok, msg in checks if not ok]
    for ok, msg in checks:
        print(("OK  " if ok else "FAIL") + " " + msg)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

