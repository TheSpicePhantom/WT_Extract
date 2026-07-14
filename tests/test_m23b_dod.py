"""Tests M23b — Apply-Burst DoD."""

from __future__ import annotations

from game_core.perf.run_analysis.m23b_dod import (
    M23bThresholds,
    evaluate_m23b_dod,
    is_unacceptable_apply_burst_hitch,
)
from game_core.perf.run_analysis.models import HitchRecord


def _hitch(**kwargs) -> HitchRecord:
    defaults = dict(
        frame_index=1,
        frame_ms=100.0,
        stream_ms=99.0,
        stream_apply_ms=95.0,
        stream_unload_ms=0.1,
        stream_loaded=4,
        stream_unloaded=0,
        chunk_count=100,
        focus_x=0.0,
        focus_y=0.0,
        zoom=1.0,
        tags=("frame_slow", "stream_slow", "load_burst"),
    )
    defaults.update(kwargs)
    return HitchRecord(**defaults)


def test_unacceptable_apply_burst_signature() -> None:
    hitch = _hitch()
    is_bad, reasons = is_unacceptable_apply_burst_hitch(hitch, thresholds=M23bThresholds())
    assert is_bad
    assert reasons


def test_acceptable_load_burst_tail() -> None:
    hitch = _hitch(frame_ms=4.0, stream_ms=0.3, stream_apply_ms=0.2, tags=("load_burst",))
    is_bad, _ = is_unacceptable_apply_burst_hitch(hitch, thresholds=M23bThresholds())
    assert not is_bad


def test_dod_fails_on_baseline_like_hitch() -> None:
    result = evaluate_m23b_dod([_hitch()])
    assert not result.passed
    assert len(result.unacceptable_hitches) == 1


def test_dod_passes_without_unacceptable() -> None:
    result = evaluate_m23b_dod([_hitch(frame_ms=4.0, stream_ms=0.3, stream_apply_ms=0.2, tags=("load_burst",))])
    assert result.passed
