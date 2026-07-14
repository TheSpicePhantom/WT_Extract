"""CI Gate für Perf-Runs (M25 / M25b / M25c / M25d)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.fps_killers import (  # noqa: E402
    attribution_incompatible_v4,
    decision_cpu_vs_present_vs_gpu,
    phase_shares,
    pick_quantile_frame,
)
from game_core.perf.run_analysis.load import RunLoadError, load_run  # noqa: E402
from game_core.perf.run_analysis.phase_enum import V4_REQUIRED_FRAME_FIELDS  # noqa: E402
from game_core.perf.run_analysis.stats import mean, percentile  # noqa: E402


def _load_frames(run_dir: Path, *, skip_warmup: int):
    loaded = load_run(run_dir)
    if skip_warmup > 0:
        return loaded.frames[skip_warmup:], loaded
    return loaded.frames, loaded


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


def _metric_values(frames, field: str) -> list[float]:
    values: list[float] = []
    for frame in frames:
        direct = getattr(frame, field, None)
        if direct is not None:
            values.append(float(direct))
            continue
        extra = frame.extra.get(field)
        if extra is not None:
            values.append(float(extra))
    return values


def gate_cpu_residual_p95_share(frames, *, max_share: float) -> tuple[bool, str]:
    with_full = [
        f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0
    ]
    if not with_full:
        return False, "cpu_full_frame_ms fehlt — cpu_residual share nicht berechenbar"
    full_p95 = percentile([float(f.cpu_full_frame_ms) for f in with_full], 0.95)
    residual_values = _metric_values(with_full, "cpu_residual_ms")
    if not residual_values:
        residual_values = [max(v, 0.0) for v in _metric_values(with_full, "cpu_measurement_residual_ms")]
    if not residual_values:
        residual_values = _metric_values(with_full, "cpu_unattributed_ms")
    if not residual_values:
        return False, "cpu_residual_ms fehlt in frames.jsonl"
    residual_p95 = percentile([max(v, 0.0) for v in residual_values], 0.95)
    share = residual_p95 / full_p95 if full_p95 > 0.0 else 0.0
    ok = share <= max_share
    return ok, f"cpu_residual_p95_share={share * 100:.1f}% (max={max_share * 100:.1f}%)"


def gate_cpu_residual_p95_max_ms(frames, *, max_ms: float) -> tuple[bool, str]:
    residual_values = _metric_values(frames, "cpu_residual_ms")
    if not residual_values:
        residual_values = [max(v, 0.0) for v in _metric_values(frames, "cpu_measurement_residual_ms")]
    if not residual_values:
        residual_values = _metric_values(frames, "cpu_unattributed_ms")
    if not residual_values:
        return False, "cpu_residual_ms fehlt in frames.jsonl"
    p95 = percentile([max(v, 0.0) for v in residual_values], 0.95)
    ok = p95 <= max_ms
    return ok, f"cpu_residual_ms_p95={p95:.3f}ms (max={max_ms:.3f}ms)"


def gate_cpu_balance_delta_p95_max_ms(frames, *, max_ms: float) -> tuple[bool, str]:
    delta_values = _metric_values(frames, "cpu_balance_delta_ms")
    if not delta_values:
        return False, "cpu_balance_delta_ms fehlt in frames.jsonl"
    p95 = percentile([abs(v) for v in delta_values], 0.95)
    ok = p95 <= max_ms
    return ok, f"abs(cpu_balance_delta_ms)_p95={p95:.3f}ms (max={max_ms:.3f}ms)"


def gate_apply_pool_idle_skip_min_rate(frames, *, min_rate: float) -> tuple[bool, str]:
    values = _metric_values(frames, "apply_pool_idle_skip")
    if not values:
        return False, "apply_pool_idle_skip fehlt in frames.jsonl"
    rate = sum(values) / len(values)
    ok = rate >= min_rate
    return ok, f"apply_pool_idle_skip_rate={rate * 100:.1f}% (min={min_rate * 100:.1f}%)"


def gate_apply_pool_p95_max_ms(frames, *, max_ms: float) -> tuple[bool, str]:
    values = [
        float(f.apply_pool_ms)
        for f in frames
        if f.apply_pool_ms is not None and float(f.apply_pool_ms) >= 0.0
    ]
    if not values:
        return False, "apply_pool_ms fehlt in frames.jsonl"
    p95 = percentile(values, 0.95)
    ok = p95 <= max_ms
    return ok, f"apply_pool_ms_p95={p95:.3f}ms (max={max_ms:.3f}ms)"


def gate_attribution_version_min(loaded, *, min_version: int) -> tuple[bool, str]:
    version = int(getattr(loaded, "attribution_version", 0))
    if version < min_version:
        return False, f"attribution_version={version} (min={min_version})"
    if min_version >= 4 and attribution_incompatible_v4(loaded.frames):
        return False, "attribution_incompatible: v4-Felder fehlen in frames.jsonl"
    return True, f"attribution_version={version} (min={min_version})"


def gate_negative_cpu_balance_delta_max(frames, *, max_count: int) -> tuple[bool, str]:
    deltas = _metric_values(frames, "cpu_balance_delta_ms")
    negative = sum(1 for v in deltas if v < -0.001)
    ok = negative <= max_count
    return ok, f"negative_cpu_balance_delta_count={negative} (max={max_count})"


def gate_missing_cpu_attribution_fields_max(frames, *, max_missing: int) -> tuple[bool, str]:
    if not frames:
        return False, "keine Frames"
    missing_frames = 0
    for frame in frames:
        if frame.cpu_full_frame_ms is None or frame.cpu_full_frame_ms <= 0.0:
            continue
        for field in V4_REQUIRED_FRAME_FIELDS:
            if frame.extra.get(field) is None and getattr(frame, field, None) is None:
                missing_frames += 1
                break
    ok = missing_frames <= max_missing
    return ok, f"missing_cpu_attribution_fields_frames={missing_frames} (max={max_missing})"


def gate_cpu_full_frame_overhead_ab(
    control_frames,
    candidate_frames,
    *,
    p50_delta_max_ms: float,
    p95_delta_max_ms: float,
    p95_delta_max_pct: float,
    mean_delta_max_ms: float,
) -> list[tuple[bool, str]]:
    def _full_values(frames):
        return [
            float(f.cpu_full_frame_ms)
            for f in frames
            if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0
        ]

    control = _full_values(control_frames)
    candidate = _full_values(candidate_frames)
    if not control or not candidate:
        return [(False, "cpu_full_frame_ms fehlt für Overhead-A/B")]

    p50_delta = abs(percentile(candidate, 0.50) - percentile(control, 0.50))
    p95_control = percentile(control, 0.95)
    p95_candidate = percentile(candidate, 0.95)
    p95_delta = abs(p95_candidate - p95_control)
    p95_pct = p95_delta / p95_control if p95_control > 0.0 else 0.0
    mean_delta = abs(mean(candidate) - mean(control))

    checks = [
        (
            p50_delta <= p50_delta_max_ms,
            f"cpu_full_frame_p50_delta={p50_delta:.3f}ms (max={p50_delta_max_ms:.3f}ms)",
        ),
        (
            p95_delta <= p95_delta_max_ms or p95_pct <= p95_delta_max_pct,
            f"cpu_full_frame_p95_delta={p95_delta:.3f}ms ({p95_pct * 100:.1f}%) "
            f"(max={p95_delta_max_ms:.3f}ms oder {p95_delta_max_pct * 100:.1f}%)",
        ),
        (
            mean_delta <= mean_delta_max_ms,
            f"cpu_full_frame_mean_delta={mean_delta:.3f}ms (max={mean_delta_max_ms:.3f}ms)",
        ),
    ]
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CI Gate für Perf-Runs (M25/M25b/M25c/M25d)")
    parser.add_argument("run_dir", type=Path, nargs="?", help="Run-Verzeichnis (manifest/frames/summary/hitches)")
    parser.add_argument("--compare-runs", nargs=2, type=Path, metavar=("CONTROL", "CANDIDATE"))
    parser.add_argument("--cpu-full-frame-p95-max-ms", type=float, default=None)
    parser.add_argument("--stream-pool-p95-share-max", type=float, default=None)
    parser.add_argument("--present-wait-share-max", type=float, default=None)
    parser.add_argument("--cpu-residual-p95-share-max", type=float, default=None)
    parser.add_argument("--cpu-residual-p95-max-ms", type=float, default=None)
    parser.add_argument("--cpu-balance-delta-p95-max-ms", type=float, default=None)
    parser.add_argument("--apply-pool-idle-skip-min-rate", type=float, default=None)
    parser.add_argument("--apply-pool-p95-max-ms", type=float, default=None)
    parser.add_argument("--attribution-version-min", type=int, default=None)
    parser.add_argument("--negative-cpu-balance-delta-max", type=int, default=None)
    parser.add_argument("--missing-cpu-attribution-fields-max", type=int, default=None)
    parser.add_argument("--cpu-full-frame-p50-delta-max-ms", type=float, default=None)
    parser.add_argument("--cpu-full-frame-p95-delta-max-ms", type=float, default=None)
    parser.add_argument("--cpu-full-frame-p95-delta-max-pct", type=float, default=None)
    parser.add_argument("--cpu-full-frame-mean-delta-max-ms", type=float, default=None)
    parser.add_argument("--skip-warmup", type=int, default=0)
    args = parser.parse_args(argv)

    skip = max(0, int(args.skip_warmup))
    checks: list[tuple[bool, str]] = []

    if args.compare_runs is not None:
        try:
            control_frames, _ = _load_frames(args.compare_runs[0], skip_warmup=skip)
            candidate_frames, _ = _load_frames(args.compare_runs[1], skip_warmup=skip)
        except RunLoadError as exc:
            print(f"gate failed: {exc}", file=sys.stderr)
            return 2
        if (
            args.cpu_full_frame_p50_delta_max_ms is not None
            or args.cpu_full_frame_p95_delta_max_ms is not None
            or args.cpu_full_frame_mean_delta_max_ms is not None
        ):
            checks.extend(
                gate_cpu_full_frame_overhead_ab(
                    control_frames,
                    candidate_frames,
                    p50_delta_max_ms=float(args.cpu_full_frame_p50_delta_max_ms or 0.5),
                    p95_delta_max_ms=float(args.cpu_full_frame_p95_delta_max_ms or 1.5),
                    p95_delta_max_pct=float(args.cpu_full_frame_p95_delta_max_pct or 0.03),
                    mean_delta_max_ms=float(args.cpu_full_frame_mean_delta_max_ms or 0.3),
                )
            )
    else:
        if args.run_dir is None:
            print("run_dir oder --compare-runs erforderlich.", file=sys.stderr)
            return 2
        try:
            frames, loaded = _load_frames(args.run_dir, skip_warmup=skip)
        except RunLoadError as exc:
            print(f"gate failed: {exc}", file=sys.stderr)
            return 2

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
        if args.cpu_residual_p95_share_max is not None:
            checks.append(
                gate_cpu_residual_p95_share(frames, max_share=float(args.cpu_residual_p95_share_max))
            )
        if args.cpu_residual_p95_max_ms is not None:
            checks.append(
                gate_cpu_residual_p95_max_ms(frames, max_ms=float(args.cpu_residual_p95_max_ms))
            )
        if args.cpu_balance_delta_p95_max_ms is not None:
            checks.append(
                gate_cpu_balance_delta_p95_max_ms(
                    frames, max_ms=float(args.cpu_balance_delta_p95_max_ms)
                )
            )
        if args.apply_pool_idle_skip_min_rate is not None:
            checks.append(
                gate_apply_pool_idle_skip_min_rate(
                    frames, min_rate=float(args.apply_pool_idle_skip_min_rate)
                )
            )
        if args.apply_pool_p95_max_ms is not None:
            checks.append(
                gate_apply_pool_p95_max_ms(frames, max_ms=float(args.apply_pool_p95_max_ms))
            )
        if args.attribution_version_min is not None:
            checks.append(
                gate_attribution_version_min(loaded, min_version=int(args.attribution_version_min))
            )
        if args.negative_cpu_balance_delta_max is not None:
            checks.append(
                gate_negative_cpu_balance_delta_max(
                    frames, max_count=int(args.negative_cpu_balance_delta_max)
                )
            )
        if args.missing_cpu_attribution_fields_max is not None:
            checks.append(
                gate_missing_cpu_attribution_fields_max(
                    frames, max_missing=int(args.missing_cpu_attribution_fields_max)
                )
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
