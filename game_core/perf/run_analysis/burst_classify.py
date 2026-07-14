"""M25c — regelbasierte Stream-Burst-Klassifikation."""

from __future__ import annotations

from game_core.perf.run_analysis.models import FrameRecord

_SUBPHASE_DOMINANT_MS = 2.0


def _extra_float(frame: FrameRecord, key: str) -> float:
    value = frame.extra.get(key)
    if value is None:
        return 0.0
    return max(float(value), 0.0)


def _extra_int(frame: FrameRecord, key: str) -> int:
    value = frame.extra.get(key)
    if value is None:
        return 0
    return int(value)


def _pool_subphases(frame: FrameRecord) -> dict[str, float]:
    pool_ms = max(frame.apply_pool_ms or 0.0, 0.0)
    sub_sum = (
        _extra_float(frame, "apply_pool_poll_ms")
        + _extra_float(frame, "apply_pool_submit_ms")
        + _extra_float(frame, "apply_pool_apply_ms")
        + _extra_float(frame, "apply_pool_suppress_ms")
        + _extra_float(frame, "apply_pool_discard_ms")
    )
    return {
        "apply_sets_ms": _extra_float(frame, "apply_sets_ms"),
        "apply_revive_ms": _extra_float(frame, "apply_revive_ms"),
        "apply_pool_poll_ms": _extra_float(frame, "apply_pool_poll_ms"),
        "apply_pool_submit_ms": _extra_float(frame, "apply_pool_submit_ms"),
        "apply_pool_apply_ms": _extra_float(frame, "apply_pool_apply_ms"),
        "apply_pool_suppress_ms": _extra_float(frame, "apply_pool_suppress_ms"),
        "apply_pool_discard_ms": _extra_float(frame, "apply_pool_discard_ms"),
        "apply_pool_other_ms": max(0.0, pool_ms - sub_sum),
        "apply_non_pool_ms": _extra_float(frame, "apply_non_pool_ms"),
        "apply_sync_generate_ms": max(frame.apply_sync_generate_ms or 0.0, 0.0),
        "apply_collision_ms": max(frame.apply_collision_ms or 0.0, 0.0),
    }


def classify_stream_burst(frame: FrameRecord) -> str:
    """Priorisierte burst_cause_id für Burst-Frames (canonical_tick_ms-Grenze)."""
    pool_ms = max(frame.apply_pool_ms or 0.0, 0.0)
    subs = _pool_subphases(frame)

    if _extra_int(frame, "apply_pool_idle_refresh") == 1 and pool_ms >= 4.0:
        return "pool_idle_refresh"
    if subs["apply_pool_poll_ms"] >= _SUBPHASE_DOMINANT_MS:
        return "pool_poll_collect"
    if _extra_int(frame, "apply_pool_route_passes") >= 2:
        return "pool_route_multi"
    if subs["apply_pool_submit_ms"] >= _SUBPHASE_DOMINANT_MS and _extra_int(
        frame, "terrain_submit_attempted"
    ) > 0:
        return "pool_submit_scan"
    if subs["apply_sets_ms"] >= _SUBPHASE_DOMINANT_MS:
        return "stream_sets_recompute"
    if _extra_int(frame, "sync_fallback_triggered") > 0 or subs["apply_sync_generate_ms"] >= _SUBPHASE_DOMINANT_MS:
        return "sync_fallback_apply"
    if subs["apply_collision_ms"] >= _SUBPHASE_DOMINANT_MS:
        return "apply_collision_flush"
    if subs["apply_pool_suppress_ms"] >= 1.0 and _extra_int(frame, "deco_suppressed") > 0:
        return "pool_suppression_scan"
    if any(v >= _SUBPHASE_DOMINANT_MS for v in subs.values()):
        dominant = max(subs.items(), key=lambda item: item[1])
        return f"subphase_{dominant[0]}"
    return "burst_unknown"


def is_burst_frame(frame: FrameRecord, *, threshold_ms: float = 4.0) -> bool:
    return frame.stream_apply_ms >= threshold_ms or max(frame.apply_pool_ms or 0.0, 0.0) >= threshold_ms
