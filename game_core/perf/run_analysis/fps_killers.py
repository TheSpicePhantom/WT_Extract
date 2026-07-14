"""M25/M25a: FPS/Frame-Time Attribution (CPU vs Present, Plan-Enum dominant_phase)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Any

from game_core.perf.run_analysis.models import FrameRecord, HitchAnalysis
from game_core.perf.run_analysis.phase_enum import (
    ATTRIBUTION_VERSION,
    CPU_DOMINANT_THRESHOLD,
    DOMINANT_PHASES,
    DOMINANT_THRESHOLD,
    MIXED_MAX_GAP,
    MIXED_MIN_SHARE,
    PRESENT_WAIT_DOMINANT_THRESHOLD,
    UNCLEAR_MAX_TOP,
)
from game_core.perf.run_analysis.stats import mean, percentile


@dataclass(frozen=True, slots=True)
class PhaseDominance:
    quantile: str
    frame_index: int
    cpu_full_frame_ms: float
    dominant_phase: str
    dominant_share: float
    shares: dict[str, float]


def _gpu_frame_ms(frame: FrameRecord) -> float:
    value = frame.extra.get("gpu_frame_ms")
    if value is None:
        return 0.0
    return max(float(value), 0.0)


def phase_ms_buckets(frame: FrameRecord) -> dict[str, float]:
    """Disjunkte ms-Buckets für Plan-Phasen."""
    pool_ms = max(frame.apply_pool_ms or 0.0, 0.0)
    apply_net = max(0.0, frame.stream_apply_ms - pool_ms)
    return {
        "stream_pool": pool_ms,
        "stream_apply": apply_net,
        "extract_tiles": max(frame.tile_extract_ms or 0.0, 0.0),
        "extract_deco": max(frame.deco_extract_ms or 0.0, 0.0),
        "render_cpu": max(frame.render_cpu_ms or 0.0, 0.0),
        "present_wait": max(frame.present_wait_cpu_ms or 0.0, 0.0),
        "gpu": _gpu_frame_ms(frame),
    }


def phase_shares(frame: FrameRecord) -> dict[str, float] | None:
    full = frame.cpu_full_frame_ms
    if full is None or full <= 0.0:
        return None
    buckets = phase_ms_buckets(frame)
    return {k: min(v / full, 1.0) for k, v in buckets.items()}


def classify_dominant_phase(shares: dict[str, float]) -> tuple[str, float]:
    """Plan-Enum aus Share-Dict ableiten."""
    if not shares:
        return "unclear", 0.0

    ranked = sorted(
        ((phase, share) for phase, share in shares.items() if phase in DOMINANT_PHASES),
        key=lambda item: (-item[1], item[0]),
    )
    if not ranked:
        return "unclear", 0.0

    top_phase, top_share = ranked[0]
    if top_share >= DOMINANT_THRESHOLD:
        return top_phase, top_share

    if len(ranked) >= 2:
        second_phase, second_share = ranked[1]
        if (
            top_share >= MIXED_MIN_SHARE
            and second_share >= MIXED_MIN_SHARE
            and (top_share - second_share) <= MIXED_MAX_GAP
        ):
            return "mixed", top_share

    if top_share < UNCLEAR_MAX_TOP:
        return "unclear", top_share

    return top_phase, top_share


def _frames_with_full(frames: list[FrameRecord]) -> list[FrameRecord]:
    return [f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]


def pick_quantile_frame(
    frames: list[FrameRecord],
    threshold: float,
    *,
    exclude_indices: set[int] | None = None,
) -> FrameRecord:
    exclude = exclude_indices or set()
    candidates = [f for f in frames if f.frame_index not in exclude]
    if not candidates:
        candidates = list(frames)
    return min(
        candidates,
        key=lambda f: (abs((f.cpu_full_frame_ms or 0.0) - threshold), f.frame_index),
    )


def _dominance_entry(frame: FrameRecord, quantile: str) -> PhaseDominance:
    shares = phase_shares(frame) or {}
    phase, share = classify_dominant_phase(shares)
    return PhaseDominance(
        quantile=quantile,
        frame_index=frame.frame_index,
        cpu_full_frame_ms=float(frame.cpu_full_frame_ms or 0.0),
        dominant_phase=phase,
        dominant_share=share,
        shares=shares,
    )


def build_quantile_dominance(frames: list[FrameRecord]) -> tuple[dict[str, dict[str, Any]], bool]:
    with_full = _frames_with_full(frames)
    if not with_full:
        return {}, False

    full_values = [float(f.cpu_full_frame_ms) for f in with_full if f.cpu_full_frame_ms is not None]
    p95_threshold = percentile(full_values, 0.95)
    p99_threshold = percentile(full_values, 0.99)

    p95_frame = pick_quantile_frame(with_full, p95_threshold)
    p99_frame = pick_quantile_frame(
        with_full,
        p99_threshold,
        exclude_indices={p95_frame.frame_index},
    )
    same_frame = p95_frame.frame_index == p99_frame.frame_index

    quantiles = {
        "p95": asdict(_dominance_entry(p95_frame, "p95")),
        "p99": asdict(_dominance_entry(p99_frame, "p99")),
    }
    return quantiles, same_frame


def build_phase_dominance(frames: list[FrameRecord]) -> list[PhaseDominance]:
    """Legacy-Liste für Abwärtskompatibilität (dominance-Key)."""
    quantiles, _ = build_quantile_dominance(frames)
    if not quantiles:
        return []
    return [
        PhaseDominance(**quantiles["p95"]),
        PhaseDominance(**quantiles["p99"]),
    ]


def _mean_phase_shares(frames: list[FrameRecord]) -> dict[str, float]:
    totals: dict[str, list[float]] = {phase: [] for phase in DOMINANT_PHASES}
    for frame in frames:
        shares = phase_shares(frame)
        if shares is None:
            continue
        for phase in DOMINANT_PHASES:
            totals[phase].append(shares.get(phase, 0.0))
    return {phase: mean(values) if values else 0.0 for phase, values in totals.items()}


def decision_cpu_vs_present_vs_gpu(frames: list[FrameRecord]) -> dict[str, Any]:
    """M25a: CPU-vs-Present Entscheidung (GPU optional, M25a ignoriert GPU)."""
    with_full = _frames_with_full(frames)
    if not with_full:
        return {
            "decision": "unclear",
            "reason_cpu_vs_present": "cpu_full_frame_ms fehlt",
            "gpu_dominant": False,
        }

    mean_shares = _mean_phase_shares(with_full)
    present_share = mean_shares.get("present_wait", 0.0)
    cpu_phases = [p for p in DOMINANT_PHASES if p != "gpu"]
    max_cpu_phase = max(cpu_phases, key=lambda p: mean_shares.get(p, 0.0))
    max_cpu_share = mean_shares.get(max_cpu_phase, 0.0)

    cpu_full_values = [float(f.cpu_full_frame_ms) for f in with_full if f.cpu_full_frame_ms is not None]
    present_ms_values = [float(f.present_wait_cpu_ms or 0.0) for f in with_full]
    render_ms_values = [float(f.render_cpu_ms or 0.0) for f in with_full]

    cpu_full_mean = mean(cpu_full_values)
    present_ms_mean = mean(present_ms_values)
    render_ms_mean = mean(render_ms_values)

    if present_share >= PRESENT_WAIT_DOMINANT_THRESHOLD and present_share >= max_cpu_share:
        decision = "present_wait_dominant"
        reason = (
            f"present_wait_mean_share={present_share * 100:.1f}% >= "
            f"{PRESENT_WAIT_DOMINANT_THRESHOLD * 100:.0f}%; "
            f"max_cpu_phase={max_cpu_phase} ({max_cpu_share * 100:.1f}%)"
        )
    elif max_cpu_share >= CPU_DOMINANT_THRESHOLD and present_share < PRESENT_WAIT_DOMINANT_THRESHOLD:
        decision = "cpu_dominant"
        reason = (
            f"present_wait_mean_share={present_share * 100:.1f}% < "
            f"{PRESENT_WAIT_DOMINANT_THRESHOLD * 100:.0f}%; "
            f"{max_cpu_phase}_mean={max_cpu_share * 100:.1f}%"
        )
    elif max_cpu_share >= MIXED_MIN_SHARE or present_share >= MIXED_MIN_SHARE:
        decision = "mixed"
        reason = (
            f"kein eindeutiger Sieger: present_wait={present_share * 100:.1f}%, "
            f"{max_cpu_phase}={max_cpu_share * 100:.1f}%"
        )
    else:
        decision = "unclear"
        reason = "keine Phase erreicht MIXED_MIN_SHARE"

    return {
        "decision": decision,
        "reason_cpu_vs_present": reason,
        "cpu_full_frame_ms_mean": cpu_full_mean,
        "present_wait_cpu_ms_mean": present_ms_mean,
        "render_cpu_ms_mean": render_ms_mean,
        "present_wait_share_mean": present_share,
        "max_cpu_phase": max_cpu_phase,
        "max_cpu_phase_share_mean": max_cpu_share,
        "mean_phase_shares": mean_shares,
        "gpu_dominant": False,
    }


def build_hitch_clusters(hitch_analyses: list[HitchAnalysis]) -> list[dict[str, Any]]:
    by_cause: dict[str, list[HitchAnalysis]] = defaultdict(list)
    for analysis in hitch_analyses:
        by_cause[analysis.cause.cause_id].append(analysis)

    clusters: list[dict[str, Any]] = []
    for cause_id, analyses in sorted(by_cause.items(), key=lambda item: -len(item[1])):
        with_frame = [a for a in analyses if a.frame is not None]
        if not with_frame:
            continue
        representative = max(
            with_frame,
            key=lambda a: float(a.frame.cpu_full_frame_ms or 0.0) if a.frame else 0.0,
        )
        frame = representative.frame
        assert frame is not None
        shares = phase_shares(frame) or {}
        phase, share = classify_dominant_phase(shares)
        clusters.append(
            {
                "cluster_id": cause_id,
                "label": representative.cause.label,
                "hitch_count": len(analyses),
                "representative_frame_index": frame.frame_index,
                "cpu_full_frame_ms": float(frame.cpu_full_frame_ms or 0.0),
                "dominant_phase": phase,
                "dominant_share": share,
                "shares": shares,
            }
        )
    return clusters


def toggles_from_manifest(manifest: dict[str, Any]) -> dict[str, bool]:
    return {
        "extract_enabled": bool(manifest.get("extract_enabled", True)),
        "stream_enabled": bool(manifest.get("stream_enabled", True)),
        "deco_extract_enabled": bool(manifest.get("deco_extract_enabled", True)),
        "tile_extract_enabled": bool(manifest.get("tile_extract_enabled", True)),
    }


def fps_killers_payload(
    frames: list[FrameRecord],
    *,
    manifest: dict[str, Any] | None = None,
    hitch_analyses: list[HitchAnalysis] | None = None,
) -> dict[str, Any]:
    quantiles, same_frame = build_quantile_dominance(frames)
    has_full_frame = bool(quantiles)
    decision = decision_cpu_vs_present_vs_gpu(frames)
    dominance = [quantiles["p95"], quantiles["p99"]] if has_full_frame else []

    payload: dict[str, Any] = {
        "schema_version": 1,
        "attribution_version": ATTRIBUTION_VERSION,
        "has_full_frame": has_full_frame,
        "decision": decision,
        "quantiles": quantiles,
        "dominance": dominance,
        "same_frame_for_both_quantiles": same_frame if has_full_frame else None,
        "hitch_clusters": build_hitch_clusters(hitch_analyses or []),
        "ab_comparisons": [],
    }

    if manifest is not None:
        scenario_id = str(manifest.get("scenario_id", "unknown"))
        payload.update(
            {
                "scenario_id": scenario_id,
                "run_id": str(manifest.get("run_id", "")),
                "scenario_label": scenario_id,
                "run_mode": str(manifest.get("run_mode", "")),
                "toggles": toggles_from_manifest(manifest),
            }
        )

    return payload


def quantile_metric(payload: dict[str, Any], quantile: str, key: str) -> float | None:
    entry = payload.get("quantiles", {}).get(quantile)
    if not entry:
        return None
    value = entry.get(key)
    return float(value) if value is not None else None


def build_ab_comparison(
    baseline: dict[str, Any],
    variant: dict[str, Any],
    *,
    causal_feature: str,
) -> dict[str, Any]:
    baseline_p95 = baseline.get("quantiles", {}).get("p95", {})
    variant_p95 = variant.get("quantiles", {}).get("p95", {})
    baseline_decision = baseline.get("decision", {}).get("decision")
    variant_decision = variant.get("decision", {}).get("decision")

    def _delta(key: str) -> float | None:
        b = baseline_p95.get(key)
        v = variant_p95.get(key)
        if b is None or v is None:
            return None
        return float(v) - float(b)

    return {
        "scenario_id": baseline.get("scenario_id"),
        "causal_feature": causal_feature,
        "baseline": {
            "run_id": baseline.get("run_id"),
            "decision": baseline_decision,
            "dominant_phase": baseline_p95.get("dominant_phase"),
            "p95": baseline_p95,
            "p99": baseline.get("quantiles", {}).get("p99", {}),
            "toggles": baseline.get("toggles"),
        },
        "variant": {
            "run_id": variant.get("run_id"),
            "toggles": variant.get("toggles"),
            "decision": variant_decision,
            "dominant_phase": variant_p95.get("dominant_phase"),
            "p95": variant_p95,
            "p99": variant.get("quantiles", {}).get("p99", {}),
        },
        "delta": {
            "cpu_full_frame_ms_p95": _delta("cpu_full_frame_ms"),
            "dominant_share_p95": _delta("dominant_share"),
            "decision_changed": baseline_decision != variant_decision,
        },
    }
