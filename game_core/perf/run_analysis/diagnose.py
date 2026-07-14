"""Run-weite Diagnose und Problem-Ranking."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from game_core.perf.run_analysis.hitch import CAUSE_LABELS, analyze_hitches
from game_core.perf.run_analysis.load import LoadedRun
from game_core.perf.run_analysis.models import BudgetCaps, ProblemRank, RunDiagnosis
from game_core.perf.run_analysis.m23b_dod import M23bThresholds, evaluate_m23b_dod
from game_core.perf.run_analysis.reconstruct import check_summary, hitch_tag_counts, recompute_summary
from game_core.perf.run_analysis.stats import (
    build_correlation_insight,
    distribution,
    frame_metric_values,
    mean,
    percentile,
)


def load_budget_caps(
    *,
    project_root: Path | None = None,
    max_applies: int | None = None,
    max_unloads: int | None = None,
) -> BudgetCaps:
    root = project_root or Path(__file__).resolve().parents[3]
    streaming_path = root / "assets" / "content" / "streaming.json"
    profiling_path = root / "assets" / "content" / "profiling.json"

    max_applies_per_frame = max_applies if max_applies is not None else 4
    max_unloads_per_frame = max_unloads if max_unloads is not None else 2
    hitch_loaded = 4
    hitch_unloaded = 4
    hitch_pending = 32

    if streaming_path.is_file():
        streaming = json.loads(streaming_path.read_text(encoding="utf-8"))
        hybrid = streaming.get("hybrid", {})
        max_applies_per_frame = int(hybrid.get("max_applies_per_frame", max_applies_per_frame))
        max_unloads_per_frame = int(hybrid.get("max_unloads_per_frame", max_unloads_per_frame))

    if profiling_path.is_file():
        profiling = json.loads(profiling_path.read_text(encoding="utf-8"))
        hitch_cfg = profiling.get("hitch", {})
        hitch_loaded = int(hitch_cfg.get("loaded_count", hitch_loaded))
        hitch_unloaded = int(hitch_cfg.get("unloaded_count", hitch_unloaded))
        hitch_pending = int(hitch_cfg.get("pending_unload_count", hitch_pending))

    if max_applies is not None:
        max_applies_per_frame = max_applies
    if max_unloads is not None:
        max_unloads_per_frame = max_unloads

    return BudgetCaps(
        max_applies_per_frame=max_applies_per_frame,
        max_unloads_per_frame=max_unloads_per_frame,
        hitch_loaded_count=hitch_loaded,
        hitch_unloaded_count=hitch_unloaded,
        hitch_pending_unload_count=hitch_pending,
    )


def _slow_frames(frames: list, hitch_indices: set[int], *, p95: float) -> list:
    return [frame for frame in frames if frame.frame_ms >= p95 or frame.frame_index in hitch_indices]


def _budget_insights(frames, hitches, caps: BudgetCaps) -> list[str]:
    insights: list[str] = []
    hitch_indices = {hitch.frame_index for hitch in hitches}
    loaded_at_cap = sum(1 for frame in frames if frame.stream_loaded >= caps.max_applies_per_frame)
    unloaded_at_cap = sum(1 for frame in frames if frame.stream_unloaded >= caps.max_unloads_per_frame)
    hitch_at_loaded_cap = sum(
        1 for hitch in hitches if hitch.stream_loaded >= caps.max_applies_per_frame
    )
    hitch_at_unloaded_cap = sum(
        1 for hitch in hitches if hitch.stream_unloaded >= caps.max_unloads_per_frame
    )

    total = max(len(frames), 1)
    insights.append(
        f"stream_loaded am Apply-Cap ({caps.max_applies_per_frame}): "
        f"{loaded_at_cap}/{total} Frames ({100 * loaded_at_cap / total:.1f}%)."
    )
    insights.append(
        f"stream_unloaded am Unload-Cap ({caps.max_unloads_per_frame}): "
        f"{unloaded_at_cap}/{total} Frames ({100 * unloaded_at_cap / total:.1f}%)."
    )
    if hitches:
        insights.append(
            f"Hitchs mit stream_loaded am Cap: {hitch_at_loaded_cap}/{len(hitches)} "
            f"({100 * hitch_at_loaded_cap / len(hitches):.1f}%)."
        )
        insights.append(
            f"Hitchs mit stream_unloaded am Cap: {hitch_at_unloaded_cap}/{len(hitches)} "
            f"({100 * hitch_at_unloaded_cap / len(hitches):.1f}%)."
        )

    pending_values = [
        frame.pending_unload_count
        for frame in frames
        if frame.pending_unload_count is not None
    ]
    if pending_values:
        max_pending = max(pending_values)
        high_pending = sum(1 for value in pending_values if value >= caps.hitch_pending_unload_count)
        insights.append(
            f"pending_unload_count max={max_pending}, "
            f">= Schwellwert {caps.hitch_pending_unload_count}: "
            f"{high_pending}/{len(pending_values)} Frames."
        )
        slow_with_pending = [
            frame
            for frame in frames
            if frame.pending_unload_count is not None and frame.frame_ms >= percentile(
                [f.frame_ms for f in frames], 0.95
            )
        ]
        if slow_with_pending:
            avg_pending_slow = mean([float(f.pending_unload_count) for f in slow_with_pending])
            avg_pending_all = mean([float(v) for v in pending_values])
            insights.append(
                f"P95+-Frames: pending_unload_count-Mittel {avg_pending_slow:.1f} "
                f"vs. Run-Mittel {avg_pending_all:.1f}."
            )
    else:
        insights.append("pending_unload_count nicht vorhanden — Backlog-Analyse eingeschränkt.")

    return insights


def _run_insights(
    frames,
    hitch_analyses,
    caps: BudgetCaps,
) -> list[str]:
    insights: list[str] = []
    if not frames:
        return ["Keine Frames im Run."]

    cause_counts = Counter(item.cause.cause_id for item in hitch_analyses)
    if hitch_analyses:
        top_cause = cause_counts.most_common(1)[0]
        insights.append(
            f"Hitch-Hauptursachen: {top_cause[0]} ({CAUSE_LABELS.get(top_cause[0], top_cause[0])}) "
            f"in {top_cause[1]}/{len(hitch_analyses)} Fällen."
        )

    frame_ms = [frame.frame_ms for frame in frames]
    stream_ms = [frame.stream_ms for frame in frames]
    apply_ms = [frame.stream_apply_ms for frame in frames]
    unload_ms = [frame.stream_unload_ms for frame in frames]
    extract_ms = [frame.extract_ms for frame in frames]

    stream_share = mean(stream_ms) / max(mean(frame_ms), 0.001)
    apply_share = mean(apply_ms) / max(mean(frame_ms), 0.001)
    unload_share = mean(unload_ms) / max(mean(frame_ms), 0.001)
    extract_share = mean(extract_ms) / max(mean(frame_ms), 0.001)

    insights.append(
        f"Durchschnittlicher Anteil an frame_ms: Stream {stream_share * 100:.1f}%, "
        f"Apply {apply_share * 100:.1f}%, Unload {unload_share * 100:.1f}%, "
        f"Extract {extract_share * 100:.1f}%."
    )

    if unload_share < 0.05 and max(unload_ms) < caps.max_unloads_per_frame:
        insights.append("Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).")

    hitch_indices = {item.hitch.frame_index for item in hitch_analyses}
    slow = _slow_frames(frames, hitch_indices, p95=percentile(frame_ms, 0.95))
    if slow and any(frame.deco_extract_ms is not None for frame in slow):
        slow_extract_share = mean([frame.extract_ms / max(frame.frame_ms, 0.001) for frame in slow])
        insights.append(
            f"Extract-Anteil in langsamen Frames (P95+/Hitch): {slow_extract_share * 100:.1f}%."
        )

    pattern_counts = Counter(item.context_pattern.pattern_id for item in hitch_analyses)
    if pattern_counts:
        top_pattern = pattern_counts.most_common(1)[0]
        insights.append(f"Häufigstes Hitch-Muster: {top_pattern[0]} ({top_pattern[1]}×).")

    return insights


def _problem_ranking(
    frames,
    hitch_analyses,
    caps: BudgetCaps,
) -> list[ProblemRank]:
    ranking: list[ProblemRank] = []
    if not frames:
        return ranking

    frame_ms_mean = mean([frame.frame_ms for frame in frames])
    apply_mean = mean([frame.stream_apply_ms for frame in frames])
    unload_mean = mean([frame.stream_unload_ms for frame in frames])
    extract_mean = mean([frame.extract_ms for frame in frames])
    stream_mean = mean([frame.stream_ms for frame in frames])

    shares = [
        ("apply", apply_mean / max(frame_ms_mean, 0.001), "stream_apply_ms"),
        ("unload", unload_mean / max(frame_ms_mean, 0.001), "stream_unload_ms"),
        ("extract", extract_mean / max(frame_ms_mean, 0.001), "extract_ms"),
        ("stream_total", stream_mean / max(frame_ms_mean, 0.001), "stream_ms"),
    ]
    shares.sort(key=lambda item: item[1], reverse=True)

    cause_counts = Counter(item.cause.cause_id for item in hitch_analyses)
    rank = 1

    if hitch_analyses:
        top_cause, count = cause_counts.most_common(1)[0]
        ranking.append(
            ProblemRank(
                rank=rank,
                category="dominant_bottleneck",
                title=f"Hitch-Ursache: {CAUSE_LABELS.get(top_cause, top_cause)}",
                rationale=(
                    f"In {count}/{len(hitch_analyses)} Hitch-Events als Hauptursache klassifiziert; "
                    f"regelbasiert aus Anteilen an frame_ms abgeleitet."
                ),
                confidence="hoch" if count >= len(hitch_analyses) * 0.5 else "mittel",
            )
        )
        rank += 1

    if shares[0][1] >= 0.25:
        ranking.append(
            ProblemRank(
                rank=rank,
                category="steady_load",
                title=f"Dauerlast durch {shares[0][2]}",
                rationale=(
                    f"Mittlerer Anteil {shares[0][1] * 100:.1f}% an frame_ms über den gesamten Run."
                ),
                confidence="mittel",
            )
        )
        rank += 1

    if shares[1][1] >= 0.10:
        ranking.append(
            ProblemRank(
                rank=rank,
                category="secondary_cost",
                title=f"Zweitrangiger Kostentreiber: {shares[1][2]}",
                rationale=f"Mittlerer Anteil {shares[1][1] * 100:.1f}% an frame_ms.",
                confidence="mittel",
            )
        )
        rank += 1

    max_frame = max(frame.frame_ms for frame in frames)
    p95_frame = percentile([frame.frame_ms for frame in frames], 0.95)
    if max_frame > p95_frame * 2:
        ranking.append(
            ProblemRank(
                rank=rank,
                category="rare_outlier",
                title="Seltene Frame-Ausreißer",
                rationale=(
                    f"frame_ms_max ({max_frame:.2f}) deutlich über P95 ({p95_frame:.2f}) — "
                    "einzelne Spitzen, nicht Dauerlast."
                ),
                confidence="hoch",
            )
        )
        rank += 1

    if unload_mean < 0.5 and max([frame.stream_unload_ms for frame in frames]) < caps.max_unloads_per_frame * 2:
        ranking.append(
            ProblemRank(
                rank=rank,
                category="relieved",
                title="Unload derzeit unauffällig",
                rationale="Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.",
                confidence="hoch",
            )
        )

    return ranking


def _open_questions(
    loaded: LoadedRun,
    summary_checks,
    hitch_analyses,
) -> list[str]:
    questions: list[str] = []
    failed = [check for check in summary_checks if not check.ok]
    if failed:
        questions.append(
            "Summary weicht von Rekonstruktion ab — Export oder Parsing prüfen "
            f"({len(failed)} Felder)."
        )
    if "pending_unload_count" not in loaded.optional_fields:
        questions.append("Keine M23a-Backlog-Felder — Unload-Backlog nur eingeschränkt bewertbar.")
    if not any(frame.deco_extract_ms is not None for frame in loaded.frames):
        questions.append("Keine Extract-Metriken — Extract-Anteil nicht quantifizierbar.")
    unclear = sum(1 for item in hitch_analyses if item.cause.cause_id == "unclear")
    if unclear:
        questions.append(
            f"{unclear} Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen."
        )
    return questions


_POOL_BREAKDOWN_MS = (
    "apply_pool_ms",
    "apply_pool_poll_ms",
    "apply_pool_submit_ms",
    "apply_pool_apply_ms",
    "apply_pool_suppress_ms",
    "apply_pool_discard_ms",
)
_POOL_BREAKDOWN_INT = (
    "apply_pool_route_passes",
    "apply_pool_in_flight_peak",
    "apply_pool_idle_skip",
)


def _frame_pool_metric(frame, field: str) -> float | int | None:
    if field == "apply_pool_ms":
        return frame.apply_pool_ms
    value = frame.extra.get(field)
    if value is None:
        return None
    if field in _POOL_BREAKDOWN_INT:
        return int(value)
    return float(value)


def build_stream_pool_breakdown(frames) -> dict[str, Any]:
    """M25b: mean/p95 für apply_pool Sub-Metriken."""
    if not frames:
        return {}

    breakdown: dict[str, Any] = {}
    for field in _POOL_BREAKDOWN_MS:
        values = [
            float(v)
            for frame in frames
            if (v := _frame_pool_metric(frame, field)) is not None and float(v) >= 0.0
        ]
        if values:
            breakdown[field] = {
                "mean": mean(values),
                "p95": percentile(values, 0.95),
            }

    for field in _POOL_BREAKDOWN_INT:
        values = [
            float(v)
            for frame in frames
            if (v := _frame_pool_metric(frame, field)) is not None
        ]
        if values:
            breakdown[field] = {
                "mean": mean(values),
                "p95": percentile(values, 0.95),
            }

    ratios: list[float] = []
    for frame in frames:
        pool = frame.apply_pool_ms
        stream_apply = frame.stream_apply_ms
        if pool is not None and stream_apply and stream_apply > 0.0:
            ratios.append(pool / stream_apply)
    if ratios:
        breakdown["apply_pool_to_stream_apply_ratio"] = {
            "mean": mean(ratios),
            "p95": percentile(ratios, 0.95),
        }

    idle_values = [
        float(v)
        for frame in frames
        if (v := _frame_pool_metric(frame, "apply_pool_idle_skip")) is not None
    ]
    if idle_values:
        breakdown["apply_pool_idle_skip_rate"] = mean(idle_values)

    return breakdown


def analyze_run(
    loaded: LoadedRun,
    *,
    caps: BudgetCaps | None = None,
    context_radius: int = 3,
) -> RunDiagnosis:
    budget_caps = caps or load_budget_caps()
    recomputed = recompute_summary(
        loaded.frames,
        loaded.hitches,
        run_id=str(loaded.manifest["run_id"]),
        scenario_id=str(loaded.manifest["scenario_id"]),
        run_mode=str(loaded.manifest["run_mode"]),
        schema_version=int(loaded.manifest["schema_version"]),
    )
    summary_checks = check_summary(loaded.summary, recomputed)
    hitch_analyses = analyze_hitches(
        loaded.frames,
        loaded.hitches,
        context_radius=context_radius,
    )
    hitch_indices = {hitch.frame_index for hitch in loaded.hitches}

    metric_names = [
        "frame_ms",
        "stream_ms",
        "stream_apply_ms",
        "stream_unload_ms",
        "stream_loaded",
        "stream_unloaded",
        "chunk_count",
        "zoom",
    ]
    if "deco_extract_ms" in loaded.optional_fields:
        metric_names.extend(["deco_extract_ms", "tile_extract_ms", "extract_ms"])
    if "pending_unload_count" in loaded.optional_fields:
        metric_names.append("pending_unload_count")
    if "cpu_full_frame_ms" in loaded.optional_fields:
        metric_names.extend(
            [
                "cpu_full_frame_ms",
                "render_cpu_ms",
                "present_wait_cpu_ms",
                "cpu_unattributed_ms",
            ]
        )

    distributions = [
        distribution(name, frame_metric_values(loaded.frames, name))
        for name in metric_names
    ]

    correlation_pairs = [
        ("frame_ms", "stream_ms"),
        ("frame_ms", "stream_apply_ms"),
        ("frame_ms", "stream_unload_ms"),
        ("frame_ms", "stream_loaded"),
        ("frame_ms", "stream_unloaded"),
        ("frame_ms", "chunk_count"),
        ("frame_ms", "zoom"),
    ]
    if "pending_unload_count" in loaded.optional_fields:
        correlation_pairs.append(("frame_ms", "pending_unload_count"))
    if "deco_extract_ms" in loaded.optional_fields:
        correlation_pairs.extend(
            [
                ("frame_ms", "deco_extract_ms"),
                ("frame_ms", "tile_extract_ms"),
                ("frame_ms", "extract_ms"),
            ]
        )
    if "cpu_full_frame_ms" in loaded.optional_fields:
        correlation_pairs.extend(
            [
                ("cpu_full_frame_ms", "stream_ms"),
                ("cpu_full_frame_ms", "extract_ms"),
                ("cpu_full_frame_ms", "render_cpu_ms"),
                ("cpu_full_frame_ms", "present_wait_cpu_ms"),
            ]
        )

    correlations = [
        build_correlation_insight(
            loaded.frames,
            x_name,
            y_name,
            hitch_indices=hitch_indices if y_name != "frame_ms" else None,
        )
        for x_name, y_name in correlation_pairs
    ]

    budget_insights = _budget_insights(loaded.frames, loaded.hitches, budget_caps)
    run_insights = _run_insights(loaded.frames, hitch_analyses, budget_caps)
    problem_ranking = _problem_ranking(loaded.frames, hitch_analyses, budget_caps)
    open_questions = _open_questions(loaded, summary_checks, hitch_analyses)

    m23b_thresholds = M23bThresholds(
        max_applies_per_frame=budget_caps.max_applies_per_frame,
    )
    m23b_dod = evaluate_m23b_dod(loaded.hitches, thresholds=m23b_thresholds)

    stream_pool_breakdown: dict[str, Any] | None = None
    if "apply_pool_ms" in loaded.optional_fields:
        stream_pool_breakdown = build_stream_pool_breakdown(loaded.frames)

    return RunDiagnosis(
        manifest=loaded.manifest,
        summary=loaded.summary,
        frames=loaded.frames,
        hitches=loaded.hitches,
        optional_fields=loaded.optional_fields,
        summary_checks=summary_checks,
        hitch_analyses=hitch_analyses,
        tag_counts=hitch_tag_counts(loaded.hitches),
        distributions=distributions,
        correlations=correlations,
        budget_insights=budget_insights,
        run_insights=run_insights,
        problem_ranking=problem_ranking,
        open_questions=open_questions,
        caps=budget_caps,
        m23b_dod_passed=m23b_dod.passed,
        m23b_unacceptable_count=len(m23b_dod.unacceptable_hitches),
        stream_pool_breakdown=stream_pool_breakdown,
    )
