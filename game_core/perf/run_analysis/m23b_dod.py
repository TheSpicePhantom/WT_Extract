"""M23b Definition-of-Done — Apply-Burst-Signatur (schema v1)."""

from __future__ import annotations

from dataclasses import dataclass

from game_core.perf.run_analysis.hitch import CAUSE_APPLY, classify_hitch_cause
from game_core.perf.run_analysis.models import HitchRecord

DEFAULT_APPLY_SHARE_THRESHOLD = 0.9

REQUIRED_TAGS = frozenset({"frame_slow", "stream_slow", "load_burst"})


@dataclass(frozen=True, slots=True)
class M23bThresholds:
    apply_share_threshold: float = DEFAULT_APPLY_SHARE_THRESHOLD
    max_applies_per_frame: int = 4


@dataclass(frozen=True, slots=True)
class ApplyBurstHitchMatch:
    hitch: HitchRecord
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class M23bDoDResult:
    thresholds: M23bThresholds
    unacceptable_hitches: tuple[ApplyBurstHitchMatch, ...]
    acceptable_load_burst_only: int
    total_hitches: int

    @property
    def passed(self) -> bool:
        return len(self.unacceptable_hitches) == 0

    @property
    def hitch_frame_count_unacceptable(self) -> int:
        return sum(
            1
            for match in self.unacceptable_hitches
            if "frame_slow" in match.hitch.tags
        )


def is_unacceptable_apply_burst_hitch(
    hitch: HitchRecord,
    *,
    thresholds: M23bThresholds,
) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    tags = set(hitch.tags)

    if not REQUIRED_TAGS.issubset(tags):
        return False, tuple()

    cause = classify_hitch_cause(hitch)
    if cause.cause_id != CAUSE_APPLY:
        reasons.append(f"Ursache ist {cause.cause_id}, nicht apply_dominant.")
        return False, tuple(reasons)

    if hitch.stream_loaded < thresholds.max_applies_per_frame:
        reasons.append(
            f"stream_loaded={hitch.stream_loaded} < Cap {thresholds.max_applies_per_frame}."
        )
        return False, tuple(reasons)

    if hitch.frame_ms <= 0:
        return False, tuple()

    share = hitch.stream_apply_ms / hitch.frame_ms
    if share < thresholds.apply_share_threshold:
        reasons.append(
            f"stream_apply_ms/frame_ms={share:.3f} < Schwelle {thresholds.apply_share_threshold}."
        )
        return False, tuple(reasons)

    reasons.extend(
        [
            "Tags frame_slow + stream_slow + load_burst.",
            f"apply_dominant, stream_loaded={hitch.stream_loaded} am Cap.",
            f"stream_apply_ms/frame_ms={share:.3f}.",
        ]
    )
    return True, tuple(reasons)


def evaluate_m23b_dod(
    hitches: list[HitchRecord],
    *,
    thresholds: M23bThresholds | None = None,
) -> M23bDoDResult:
    caps = thresholds or M23bThresholds()
    unacceptable: list[ApplyBurstHitchMatch] = []
    acceptable_tail = 0

    for hitch in hitches:
        is_bad, reasons = is_unacceptable_apply_burst_hitch(hitch, thresholds=caps)
        if is_bad:
            unacceptable.append(ApplyBurstHitchMatch(hitch=hitch, reasons=reasons))
        elif "load_burst" in hitch.tags and "frame_slow" not in hitch.tags:
            acceptable_tail += 1

    return M23bDoDResult(
        thresholds=caps,
        unacceptable_hitches=tuple(unacceptable),
        acceptable_load_burst_only=acceptable_tail,
        total_hitches=len(hitches),
    )
