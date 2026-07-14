"""M25: FPS/Frame-Time Attribution Reports (CPU vs Present vs GPU)."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from game_core.perf.run_analysis.models import FrameRecord
from game_core.perf.run_analysis.stats import percentile, mean


@dataclass(frozen=True, slots=True)
class PhaseDominance:
    quantile: str  # "p95" | "p99"
    frame_index: int
    cpu_full_frame_ms: float
    dominant_phase: str
    dominant_share: float
    shares: dict[str, float]


def _shares(frame: FrameRecord) -> dict[str, float] | None:
    full = frame.cpu_full_frame_ms
    if full is None or full <= 0.0:
        return None

    # CPU-side buckets (M25 initial approximation).
    stream = max(frame.stream_ms, 0.0)
    extract = max(frame.extract_ms, 0.0)
    render = max(frame.render_cpu_ms or 0.0, 0.0)
    present = max(frame.present_wait_cpu_ms or 0.0, 0.0)

    buckets = {
        "stream": stream,
        "extract": extract,
        "render_cpu": render,
        "present_wait": present,
    }
    # Normalize to shares of cpu_full_frame_ms.
    return {k: min(v / full, 1.0) for k, v in buckets.items()}


def _dominant_phase(shares: dict[str, float]) -> tuple[str, float]:
    best = max(shares.items(), key=lambda kv: kv[1])
    return best[0], best[1]


def build_phase_dominance(frames: list[FrameRecord]) -> list[PhaseDominance]:
    with_full = [f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not with_full:
        return []

    full_values = [f.cpu_full_frame_ms for f in with_full if f.cpu_full_frame_ms is not None]
    p95 = percentile([float(v) for v in full_values], 0.95)
    p99 = percentile([float(v) for v in full_values], 0.99)

    def pick(target: float, label: str) -> PhaseDominance:
        # Pick the first frame at/above quantile, then compute shares.
        candidate = next((f for f in with_full if (f.cpu_full_frame_ms or 0.0) >= target), with_full[-1])
        shares = _shares(candidate) or {}
        phase, share = _dominant_phase(shares) if shares else ("unclear", 0.0)
        return PhaseDominance(
            quantile=label,
            frame_index=candidate.frame_index,
            cpu_full_frame_ms=float(candidate.cpu_full_frame_ms or 0.0),
            dominant_phase=phase,
            dominant_share=share,
            shares=shares,
        )

    return [pick(p95, "p95"), pick(p99, "p99")]


def decision_cpu_vs_present_vs_gpu(frames: list[FrameRecord]) -> dict[str, Any]:
    """Sehr konservative Entscheidung (CPU-only, GPU optional)."""
    with_full = [f for f in frames if f.cpu_full_frame_ms is not None and f.cpu_full_frame_ms > 0.0]
    if not with_full:
        return {"decision": "unknown", "reason": "cpu_full_frame_ms fehlt"}

    present_shares = []
    render_shares = []
    stream_shares = []
    extract_shares = []
    for f in with_full:
        shares = _shares(f)
        if shares is None:
            continue
        present_shares.append(shares.get("present_wait", 0.0))
        render_shares.append(shares.get("render_cpu", 0.0))
        stream_shares.append(shares.get("stream", 0.0))
        extract_shares.append(shares.get("extract", 0.0))

    mean_present = mean(present_shares) if present_shares else 0.0
    mean_render = mean(render_shares) if render_shares else 0.0
    mean_cpu_work = mean(stream_shares) + mean(extract_shares) + mean_render

    # Decision heuristic: present_wait dominates if it is the single biggest share and >= 40%.
    if mean_present >= 0.40 and mean_present >= max(mean_render, mean(stream_shares or [0.0]), mean(extract_shares or [0.0])):
        return {"decision": "present_wait_dominant", "mean_present_share": mean_present}
    if mean_cpu_work >= 0.60:
        return {"decision": "cpu_dominant", "mean_cpu_work_share": mean_cpu_work, "mean_present_share": mean_present}
    return {"decision": "mixed", "mean_cpu_work_share": mean_cpu_work, "mean_present_share": mean_present}


def fps_killers_payload(frames: list[FrameRecord]) -> dict[str, Any]:
    dominance = build_phase_dominance(frames)
    decision = decision_cpu_vs_present_vs_gpu(frames)
    return {
        "has_full_frame": bool(dominance),
        "decision": decision,
        "dominance": [asdict(d) for d in dominance],
    }

