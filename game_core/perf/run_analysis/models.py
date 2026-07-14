"""Datenmodelle für Run-Analyse."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class FrameRecord:
    frame_index: int
    frame_ms: float
    stream_ms: float
    stream_apply_ms: float
    stream_unload_ms: float
    stream_loaded: int
    stream_unloaded: int
    chunk_count: int
    focus_x: float
    focus_y: float
    zoom: float
    # M25 optional: Full-frame Attribution (CPU).
    cpu_full_frame_ms: float | None = None
    render_cpu_ms: float | None = None
    present_wait_cpu_ms: float | None = None
    cpu_unattributed_ms: float | None = None
    deco_extract_ms: float | None = None
    tile_extract_ms: float | None = None
    stream_unload_marked: int | None = None
    stream_unload_drained: int | None = None
    pending_unload_count: int | None = None
    apply_worker_ms: float | None = None
    apply_sync_generate_ms: float | None = None
    apply_delta_ms: float | None = None
    apply_override_ms: float | None = None
    apply_pool_ms: float | None = None
    apply_collision_ms: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def extract_ms(self) -> float:
        deco = self.deco_extract_ms or 0.0
        tile = self.tile_extract_ms or 0.0
        return deco + tile

    @property
    def scenario_ms(self) -> float:
        return max(
            0.0,
            self.frame_ms - self.stream_ms - self.extract_ms,
        )


@dataclass(frozen=True, slots=True)
class HitchRecord:
    frame_index: int
    frame_ms: float
    stream_ms: float
    stream_apply_ms: float
    stream_unload_ms: float
    stream_loaded: int
    stream_unloaded: int
    chunk_count: int
    focus_x: float
    focus_y: float
    zoom: float
    tags: tuple[str, ...]
    # M25 optional: Full-frame Attribution (CPU).
    cpu_full_frame_ms: float | None = None
    render_cpu_ms: float | None = None
    present_wait_cpu_ms: float | None = None
    deco_extract_ms: float | None = None
    tile_extract_ms: float | None = None
    pending_unload_count: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def extract_ms(self) -> float:
        deco = self.deco_extract_ms or 0.0
        tile = self.tile_extract_ms or 0.0
        return deco + tile


@dataclass(frozen=True, slots=True)
class BudgetCaps:
    max_applies_per_frame: int
    max_unloads_per_frame: int
    hitch_loaded_count: int
    hitch_unloaded_count: int
    hitch_pending_unload_count: int


@dataclass
class SummaryCheck:
    field: str
    summary_value: float
    recomputed_value: float
    delta: float
    ok: bool


@dataclass(frozen=True, slots=True)
class HitchCause:
    cause_id: str
    label: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HitchContextPattern:
    pattern_id: str
    label: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HitchAnalysis:
    hitch: HitchRecord
    frame: FrameRecord | None
    cause: HitchCause
    context_pattern: HitchContextPattern
    context_before: tuple[FrameRecord, ...]
    context_after: tuple[FrameRecord, ...]


@dataclass(frozen=True, slots=True)
class MetricDistribution:
    name: str
    mean: float
    p50: float
    p95: float
    max: float
    present: bool = True


@dataclass(frozen=True, slots=True)
class CorrelationInsight:
    metric_x: str
    metric_y: str
    coefficient: float | None
    strength: str
    interpretation: str
    sample_size: int


@dataclass(frozen=True, slots=True)
class ProblemRank:
    rank: int
    category: str
    title: str
    rationale: str
    confidence: str


@dataclass
class RunDiagnosis:
    manifest: dict[str, Any]
    summary: dict[str, Any]
    frames: list[FrameRecord]
    hitches: list[HitchRecord]
    optional_fields: frozenset[str]
    summary_checks: list[SummaryCheck]
    hitch_analyses: list[HitchAnalysis]
    tag_counts: dict[str, int]
    distributions: list[MetricDistribution]
    correlations: list[CorrelationInsight]
    budget_insights: list[str]
    run_insights: list[str]
    problem_ranking: list[ProblemRank]
    open_questions: list[str]
    caps: BudgetCaps
    m23b_dod_passed: bool
    m23b_unacceptable_count: int
