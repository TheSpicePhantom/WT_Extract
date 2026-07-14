"""CI Gate für Perf-Runs (M25 / M25b).

Ziel: harte Regression-Gates für Full-Frame Metriken, ohne Summary-Schema zu ändern.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.fps_killers import (  # noqa: E402
    decision_cpu_vs_present_vs_gpu,
    phase_shares,
    pick_quantile_frame,
)
from game_core.perf.run_analysis.load import RunLoadError, load_run  # noqa: E402
from game_core.perf.run_analysis.stats import percentile  # noqa: E402


def _load_frames(run_dir: Path, *, skip_warmup: int):
    loaded = load_run(run_dir)
    if skip_warmup > 0:
        return loaded.frames[skip_warmup:]
    return loaded.frames


def gate_cpu_full_frame_p95(frames, *, max_ms: float) -> tuple[bool, str]:
    values = [f.cpu_full_frame_ms for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not values:
        return False, "cpu_full_frame_ms fehlt in frames.jsonl"
    p95 = percentile([float(v) for v in values], 0.95)
    ok = p95 <= max_ms
    return ok, f"cpu_full_frame_ms_p95={p95:.3f}ms (max={max_ms:.3f}ms)"


def gate_stream_pool_p95_share(frames, *, max_share: float) -> tuple[bool, str]:
    with_full = [f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not with_full:
        return False, "cpu_full_frame_ms fehlt — stream_pool share nicht berechenbar"
    p95_threshold = percentile([float(f.cpu_full_frame_ms) for f in with_full], 0.95)
    frame = pick_quantile_frame(with_full, p95_threshold)
    shares = phase_shares(frame)
    if not shares:
        return False, "phase_shares am P95-Frame nicht berechenbar"
    share = shares.get("stream_pool", 0.0)
    ok = share <= max_share
    return ok, f"stream_pool_p95_share={share * 100:.1f}% (max={max_share * 100:.1f}%)"


def gate_present_wait_share_mean(frames, *, max_share: float) -> tuple[bool, str]:
    with_full = [f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not with_full:
        return False, "cpu_full_frame_ms fehlt — present_wait share nicht berechenbar"
    decision = decision_cpu_vs_present_vs_gpu(with_full)
    mean_share = float(decision.get("present_wait_share_mean", 0.0))
    ok = mean_share < max_share
    return ok, f"present_wait_share_mean={mean_share * 100:.2f}% (max<{max_share * 100:.1f}%)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CI Gate für Perf-Runs (M25/M25b)")
    parser.add_argument("run_dir", type=Path, help="Run-Verzeichnis (manifest/frames/summary/hitches)")
    parser.add_argument("--cpu-full-frame-p95-max-ms", type=float, default=None)
    parser.add_argument("--stream-pool-p95-share-max", type=float, default=None)
    parser.add_argument("--present-wait-share-max", type=float, default=None)
    parser.add_argument("--skip-warmup", type=int, default=0)
    args = parser.parse_args(argv)

    try:
        frames = _load_frames(args.run_dir, skip_warmup=max(0, int(args.skip_warmup)))
    except RunLoadError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 2

    checks: list[tuple[bool, str]] = []
    if args.cpu_full_frame_p95_max_ms is not None:
        checks.append(gate_cpu_full_frame_p95(frames, max_ms=float(args.cpu_full_frame_p95_max_ms)))
    if args.stream_pool_p95_share_max is not None:
        checks.append(
            gate_stream_pool_p95_share(frames, max_share=float(args.stream_pool_p95_share_max))
        )
    if args.present_wait_share_max is not None:
        checks.append(
            gate_present_wait_share_mean(frames, max_share=float(args.present_wait_share_max))
        )

    if not checks:
        print("Keine Gates angegeben.", file=sys.stderr)
        return 2

    failed = [msg for ok, msg in checks if not ok]
    for ok, msg in checks:
        print(("OK  " if ok else "FAIL") + " " + msg)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
