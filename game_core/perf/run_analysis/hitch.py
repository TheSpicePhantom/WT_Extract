"""Hitch-Klassifikation und Kontextfenster."""

from __future__ import annotations

from game_core.perf.run_analysis.models import (
    FrameRecord,
    HitchAnalysis,
    HitchCause,
    HitchContextPattern,
    HitchRecord,
)
from game_core.perf.run_analysis.stats import mean

CAUSE_APPLY = "apply_dominant"
CAUSE_UNLOAD = "unload_dominant"
CAUSE_EXTRACT = "extract_dominant"
CAUSE_STREAM = "stream_total_dominant"
CAUSE_MIXED = "mixed"
CAUSE_UNCLEAR = "unclear"

CAUSE_LABELS = {
    CAUSE_APPLY: "Load-/Apply-dominant",
    CAUSE_UNLOAD: "Unload-dominant",
    CAUSE_EXTRACT: "Extract-dominant",
    CAUSE_STREAM: "Stream gesamt dominant",
    CAUSE_MIXED: "Gemischt",
    CAUSE_UNCLEAR: "Nicht eindeutig",
}

PATTERN_ISOLATED = "isolated_spike"
PATTERN_BURST = "burst_with_tail"
PATTERN_BACKLOG = "backlog_buildup"
PATTERN_PERIODIC = "periodic_cluster"
PATTERN_STEADY = "steady_cost"
PATTERN_UNKNOWN = "unknown"

PATTERN_LABELS = {
    PATTERN_ISOLATED: "Isolierter Spike",
    PATTERN_BURST: "Burst mit Nachlauf",
    PATTERN_BACKLOG: "Backlog-Aufbau",
    PATTERN_PERIODIC: "Wiederkehrendes Cluster",
    PATTERN_STEADY: "Konstanter Kostentreiber",
    PATTERN_UNKNOWN: "Unklares Muster",
}

DOMINANCE_THRESHOLD = 0.50
MIXED_THRESHOLD = 0.30


def _share(part: float, total: float) -> float:
    if total <= 0.0:
        return 0.0
    return part / total


def classify_hitch_cause(hitch: HitchRecord) -> HitchCause:
    frame_ms = hitch.frame_ms
    apply_share = _share(hitch.stream_apply_ms, frame_ms)
    unload_share = _share(hitch.stream_unload_ms, frame_ms)
    extract_share = _share(hitch.extract_ms, frame_ms)
    stream_share = _share(hitch.stream_ms, frame_ms)

    shares = {
        CAUSE_APPLY: apply_share,
        CAUSE_UNLOAD: unload_share,
        CAUSE_EXTRACT: extract_share,
        CAUSE_STREAM: stream_share,
    }
    reasons: list[str] = []
    for key, share in shares.items():
        if key != CAUSE_STREAM:
            reasons.append(f"{CAUSE_LABELS[key]}: {share * 100:.1f}% von frame_ms")

    dominant = max(
        ((CAUSE_APPLY, apply_share), (CAUSE_UNLOAD, unload_share), (CAUSE_EXTRACT, extract_share)),
        key=lambda item: item[1],
    )
    mixed_hits = sum(
        1
        for share in (apply_share, unload_share, extract_share)
        if share >= MIXED_THRESHOLD
    )

    if "load_burst" in hitch.tags and apply_share >= MIXED_THRESHOLD:
        reasons.append("Tag load_burst unterstützt Apply-Dominanz.")
    if "unload_burst" in hitch.tags and unload_share >= MIXED_THRESHOLD:
        reasons.append("Tag unload_burst unterstützt Unload-Dominanz.")
    if "unload_backlog" in hitch.tags:
        reasons.append("Tag unload_backlog — Backlog-Indiz.")
    if "stream_slow" in hitch.tags and stream_share >= MIXED_THRESHOLD:
        reasons.append("Tag stream_slow — Stream-Anteil erhöht.")

    if mixed_hits >= 2:
        return HitchCause(CAUSE_MIXED, CAUSE_LABELS[CAUSE_MIXED], tuple(reasons))
    if dominant[1] >= DOMINANCE_THRESHOLD:
        return HitchCause(dominant[0], CAUSE_LABELS[dominant[0]], tuple(reasons))
    if stream_share >= DOMINANCE_THRESHOLD and apply_share < MIXED_THRESHOLD:
        return HitchCause(CAUSE_STREAM, CAUSE_LABELS[CAUSE_STREAM], tuple(reasons))
    return HitchCause(CAUSE_UNCLEAR, CAUSE_LABELS[CAUSE_UNCLEAR], tuple(reasons))


def _frame_by_index(frames: list[FrameRecord]) -> dict[int, FrameRecord]:
    return {frame.frame_index: frame for frame in frames}


def _context_slice(
    frames_by_index: dict[int, FrameRecord],
    frame_index: int,
    *,
    before: int,
    after: int,
) -> tuple[tuple[FrameRecord, ...], FrameRecord | None, tuple[FrameRecord, ...]]:
    before_frames = tuple(
        frames_by_index[idx]
        for idx in range(frame_index - before, frame_index)
        if idx in frames_by_index
    )
    center = frames_by_index.get(frame_index)
    after_frames = tuple(
        frames_by_index[idx]
        for idx in range(frame_index + 1, frame_index + after + 1)
        if idx in frames_by_index
    )
    return before_frames, center, after_frames


def detect_context_pattern(
    hitch: HitchRecord,
    *,
    before: tuple[FrameRecord, ...],
    after: tuple[FrameRecord, ...],
    all_hitch_indices: set[int],
) -> HitchContextPattern:
    reasons: list[str] = []

    if before and before[-1].pending_unload_count is not None and hitch.pending_unload_count is not None:
        pending_before = [frame.pending_unload_count for frame in before if frame.pending_unload_count is not None]
        if pending_before and hitch.pending_unload_count > pending_before[-1]:
            reasons.append(
                f"pending_unload_count steigt von {pending_before[-1]} auf {hitch.pending_unload_count}."
            )
            return HitchContextPattern(PATTERN_BACKLOG, PATTERN_LABELS[PATTERN_BACKLOG], tuple(reasons))

    neighbors = list(before) + list(after)
    neighbor_ms = [frame.frame_ms for frame in neighbors]
    neighbor_mean = mean(neighbor_ms) if neighbor_ms else 0.0

    if neighbor_mean > 0 and hitch.frame_ms >= neighbor_mean * 2.5:
        reasons.append(
            f"Hitch frame_ms ({hitch.frame_ms:.2f}) deutlich über Nachbar-Mittel ({neighbor_mean:.2f})."
        )
        nearby_hitches = [
            idx
            for idx in all_hitch_indices
            if idx != hitch.frame_index and abs(idx - hitch.frame_index) <= 3
        ]
        if nearby_hitches:
            reasons.append(f"Weitere Hitches in ±3 Frames: {sorted(nearby_hitches)}.")
            return HitchContextPattern(PATTERN_BURST, PATTERN_LABELS[PATTERN_BURST], tuple(reasons))
        return HitchContextPattern(PATTERN_ISOLATED, PATTERN_LABELS[PATTERN_ISOLATED], tuple(reasons))

    cluster = [idx for idx in all_hitch_indices if abs(idx - hitch.frame_index) <= 20]
    if len(cluster) >= 3:
        span = max(cluster) - min(cluster)
        if span >= 10:
            reasons.append(f"{len(cluster)} Hitches in einem 20-Frame-Fenster (Spanne {span}).")
            return HitchContextPattern(PATTERN_PERIODIC, PATTERN_LABELS[PATTERN_PERIODIC], tuple(reasons))

    if hitch.frame_ms >= 16.0 and hitch.stream_ms / max(hitch.frame_ms, 0.001) >= 0.6:
        reasons.append("Hoher Stream-Anteil ohne klaren Einzelspike.")
        return HitchContextPattern(PATTERN_STEADY, PATTERN_LABELS[PATTERN_STEADY], tuple(reasons))

    reasons.append("Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.")
    return HitchContextPattern(PATTERN_UNKNOWN, PATTERN_LABELS[PATTERN_UNKNOWN], tuple(reasons))


def analyze_hitches(
    frames: list[FrameRecord],
    hitches: list[HitchRecord],
    *,
    context_radius: int = 3,
) -> list[HitchAnalysis]:
    frames_by_index = _frame_by_index(frames)
    hitch_indices = {hitch.frame_index for hitch in hitches}
    analyses: list[HitchAnalysis] = []
    for hitch in sorted(hitches, key=lambda item: item.frame_index):
        before, center, after = _context_slice(
            frames_by_index,
            hitch.frame_index,
            before=context_radius,
            after=context_radius,
        )
        analyses.append(
            HitchAnalysis(
                hitch=hitch,
                frame=center,
                cause=classify_hitch_cause(hitch),
                context_pattern=detect_context_pattern(
                    hitch,
                    before=before,
                    after=after,
                    all_hitch_indices=hitch_indices,
                ),
                context_before=before,
                context_after=after,
            )
        )
    return analyses
