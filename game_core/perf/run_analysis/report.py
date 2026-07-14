"""Report-Ausgabe — Terminal, Markdown, CSV, JSON."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from game_core.perf.run_analysis.models import RunDiagnosis
from game_core.perf.run_analysis.fps_killers import fps_killers_payload

def _fmt_ms(value: float) -> str:
    return f"{value:.2f} ms"


def format_terminal_summary(diagnosis: RunDiagnosis) -> str:
    manifest = diagnosis.manifest
    summary = diagnosis.summary
    lines = [
        "=== Profiling-Run-Analyse ===",
        f"Run: {manifest.get('run_id')} | Szenario: {manifest.get('scenario_id')} | Modus: {manifest.get('run_mode')}",
        f"Frames: {manifest.get('recorded_frames')} (Warmup: {manifest.get('warmup_frames')}) | Extract: {manifest.get('extract_enabled')}",
        f"Optionale Felder: {', '.join(sorted(diagnosis.optional_fields)) or '—'}",
        "",
        "--- KPIs (summary.json) ---",
        f"frame_ms: mean={summary.get('frame_ms_mean'):.2f} p95={summary.get('frame_ms_p95'):.2f} max={summary.get('frame_ms_max'):.2f}",
        f"stream_ms: mean={summary.get('stream_ms_mean'):.2f} p95={summary.get('stream_ms_p95'):.2f} max={summary.get('stream_ms_max'):.2f}",
        f"Hitches: {summary.get('hitch_count')} (load={summary.get('hitch_load_count')}, unload={summary.get('hitch_unload_count')})",
        "",
    ]

    failed = [check for check in diagnosis.summary_checks if not check.ok]
    if failed:
        lines.append(f"⚠ Summary-Abweichungen: {len(failed)} Feld(er)")
        for check in failed[:5]:
            lines.append(
                f"  {check.field}: summary={check.summary_value:.4f} "
                f"recomputed={check.recomputed_value:.4f} (Δ={check.delta:+.4f})"
            )
        lines.append("")
    else:
        lines.append("Summary-Plausibilität: OK")
        lines.append("")

    m23b_status = "BESTANDEN" if diagnosis.m23b_dod_passed else "NICHT BESTANDEN"
    lines.append(f"--- M23b DoD ---")
    lines.append(f"Apply-Burst-Signatur: {m23b_status} ({diagnosis.m23b_unacceptable_count} inakzeptabel)")
    lines.append("")

    lines.append("--- Problem-Ranking ---")
    for item in diagnosis.problem_ranking[:5]:
        lines.append(f"{item.rank}. [{item.category}] {item.title}")
        lines.append(f"   {item.rationale}")
    lines.append("")

    lines.append("--- Hitch-Übersicht ---")
    if not diagnosis.hitch_analyses:
        lines.append("Keine Hitches.")
    else:
        for item in diagnosis.hitch_analyses[:10]:
            hitch = item.hitch
            lines.append(
                f"#{hitch.frame_index}: {_fmt_ms(hitch.frame_ms)} | "
                f"Ursache: {item.cause.label} | Muster: {item.context_pattern.label} | "
                f"Tags: {', '.join(hitch.tags)}"
            )
        if len(diagnosis.hitch_analyses) > 10:
            lines.append(f"... +{len(diagnosis.hitch_analyses) - 10} weitere")
    lines.append("")

    lines.append("--- Run-Diagnose (Auszug) ---")
    for insight in diagnosis.run_insights[:6]:
        lines.append(f"• {insight}")
    for insight in diagnosis.budget_insights[:4]:
        lines.append(f"• {insight}")

    if diagnosis.open_questions:
        lines.append("")
        lines.append("--- Offene Punkte ---")
        for question in diagnosis.open_questions:
            lines.append(f"? {question}")

    return "\n".join(lines)


def write_markdown_report(diagnosis: RunDiagnosis, path: Path) -> None:
    manifest = diagnosis.manifest
    summary = diagnosis.summary
    lines = [
        "# Profiling-Run-Analyse",
        "",
        "## Metadaten",
        "",
        f"- **run_id:** `{manifest.get('run_id')}`",
        f"- **scenario_id:** `{manifest.get('scenario_id')}`",
        f"- **run_mode:** `{manifest.get('run_mode')}`",
        f"- **recorded_frames:** {manifest.get('recorded_frames')}",
        f"- **warmup_frames:** {manifest.get('warmup_frames')}",
        f"- **extract_enabled:** {manifest.get('extract_enabled')}",
        f"- **recorded_at:** {manifest.get('recorded_at')}",
        f"- **git_commit:** {manifest.get('git_commit')}",
        "",
        "### Config-Fingerprints",
        "",
    ]
    fingerprints = manifest.get("config_fingerprint", {})
    for key, value in sorted(fingerprints.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            f"**Optionale Felder:** {', '.join(sorted(diagnosis.optional_fields)) or '—'}",
            "",
            "## KPI-Check",
            "",
            "| Feld | summary.json | rekonstruiert | Δ | Status |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for check in diagnosis.summary_checks:
        status = "OK" if check.ok else "ABWEICHUNG"
        lines.append(
            f"| {check.field} | {check.summary_value:.4f} | {check.recomputed_value:.4f} | "
            f"{check.delta:+.4f} | {status} |"
        )

    m23b_status = "BESTANDEN" if diagnosis.m23b_dod_passed else "NICHT BESTANDEN"
    lines.extend(
        [
            "",
            "## M23b DoD",
            "",
            f"- **Apply-Burst-Signatur:** {m23b_status}",
            f"- **Inakzeptable Hitchs:** {diagnosis.m23b_unacceptable_count}",
            "",
            "## Problem-Ranking",
            "",
        ]
    )
    for item in diagnosis.problem_ranking:
        lines.append(f"{item.rank}. **{item.title}** ({item.category}, Konfidenz: {item.confidence})")
        lines.append(f"   - {item.rationale}")
        lines.append("")

    lines.extend(["## Hitch-Analyse", ""])
    lines.append("### Tag-Häufigkeiten")
    lines.append("")
    for tag, count in sorted(diagnosis.tag_counts.items(), key=lambda item: (-item[1], item[0])):
        if count:
            lines.append(f"- `{tag}`: {count}")
    lines.append("")

    for item in diagnosis.hitch_analyses:
        hitch = item.hitch
        lines.extend(
            [
                f"### Frame {hitch.frame_index}",
                "",
                f"- **frame_ms:** {hitch.frame_ms:.3f}",
                f"- **stream_ms / apply / unload:** {hitch.stream_ms:.3f} / {hitch.stream_apply_ms:.3f} / {hitch.stream_unload_ms:.3f}",
                f"- **stream_loaded / unloaded:** {hitch.stream_loaded} / {hitch.stream_unloaded}",
                f"- **chunk_count / zoom:** {hitch.chunk_count} / {hitch.zoom:.4f}",
            ]
        )
        if hitch.pending_unload_count is not None:
            lines.append(f"- **pending_unload_count:** {hitch.pending_unload_count}")
        if hitch.deco_extract_ms is not None or hitch.tile_extract_ms is not None:
            lines.append(
                f"- **Extract:** deco={hitch.deco_extract_ms or 0:.3f} tile={hitch.tile_extract_ms or 0:.3f}"
            )
        lines.extend(
            [
                f"- **Tags:** {', '.join(hitch.tags)}",
                f"- **Vermutete Ursache:** {item.cause.label}",
            ]
        )
        for reason in item.cause.reasons:
            lines.append(f"  - {reason}")
        lines.append(f"- **Kontextmuster:** {item.context_pattern.label}")
        for reason in item.context_pattern.reasons:
            lines.append(f"  - {reason}")
        if item.context_before:
            before_ms = ", ".join(f"{frame.frame_index}:{frame.frame_ms:.1f}" for frame in item.context_before)
            lines.append(f"- **Kontext davor:** {before_ms}")
        if item.context_after:
            after_ms = ", ".join(f"{frame.frame_index}:{frame.frame_ms:.1f}" for frame in item.context_after)
            lines.append(f"- **Kontext danach:** {after_ms}")
        lines.append("")

    lines.extend(["## Verteilungen", "", "| Metrik | mean | p50 | p95 | max |", "| --- | ---: | ---: | ---: | ---: |"])
    for dist in diagnosis.distributions:
        if dist.present:
            lines.append(
                f"| {dist.name} | {dist.mean:.3f} | {dist.p50:.3f} | {dist.p95:.3f} | {dist.max:.3f} |"
            )

    lines.extend(["", "## Korrelationen / Zusammenhänge", ""])
    for insight in diagnosis.correlations:
        coef = "n/a" if insight.coefficient is None else f"{insight.coefficient:.3f}"
        lines.append(f"- **{insight.metric_x} ↔ {insight.metric_y}** (r={coef}, n={insight.sample_size}): {insight.interpretation}")

    lines.extend(["", "## Budget- und Cap-Verhalten", ""])
    lines.append(
        f"Referenz-Caps: max_applies={diagnosis.caps.max_applies_per_frame}, "
        f"max_unloads={diagnosis.caps.max_unloads_per_frame} "
        "(aus Projekt-config, Fingerprint-Abweichung beachten)."
    )
    for insight in diagnosis.budget_insights:
        lines.append(f"- {insight}")

    lines.extend(["", "## Run-weite Diagnose", ""])
    for insight in diagnosis.run_insights:
        lines.append(f"- {insight}")

    if diagnosis.open_questions:
        lines.extend(["", "## Offene Fragen", ""])
        for question in diagnosis.open_questions:
            lines.append(f"- {question}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_hitch_csv(diagnosis: RunDiagnosis, path: Path) -> None:
    fieldnames = [
        "frame_index",
        "frame_ms",
        "stream_ms",
        "stream_apply_ms",
        "stream_unload_ms",
        "stream_loaded",
        "stream_unloaded",
        "chunk_count",
        "zoom",
        "pending_unload_count",
        "deco_extract_ms",
        "tile_extract_ms",
        "tags",
        "cause_id",
        "cause_label",
        "pattern_id",
        "pattern_label",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in diagnosis.hitch_analyses:
            hitch = item.hitch
            writer.writerow(
                {
                    "frame_index": hitch.frame_index,
                    "frame_ms": hitch.frame_ms,
                    "stream_ms": hitch.stream_ms,
                    "stream_apply_ms": hitch.stream_apply_ms,
                    "stream_unload_ms": hitch.stream_unload_ms,
                    "stream_loaded": hitch.stream_loaded,
                    "stream_unloaded": hitch.stream_unloaded,
                    "chunk_count": hitch.chunk_count,
                    "zoom": hitch.zoom,
                    "pending_unload_count": hitch.pending_unload_count,
                    "deco_extract_ms": hitch.deco_extract_ms,
                    "tile_extract_ms": hitch.tile_extract_ms,
                    "tags": "|".join(hitch.tags),
                    "cause_id": item.cause.cause_id,
                    "cause_label": item.cause.label,
                    "pattern_id": item.context_pattern.pattern_id,
                    "pattern_label": item.context_pattern.label,
                }
            )


def write_notable_frames_csv(diagnosis: RunDiagnosis, path: Path, *, top_n: int = 50) -> None:
    p95 = next((dist.p95 for dist in diagnosis.distributions if dist.name == "frame_ms"), 0.0)
    hitch_indices = {hitch.frame_index for hitch in diagnosis.hitches}
    notable = [
        frame
        for frame in diagnosis.frames
        if frame.frame_index in hitch_indices or frame.frame_ms >= p95
    ]
    notable.sort(key=lambda frame: frame.frame_ms, reverse=True)
    notable = notable[:top_n]

    fieldnames = [
        "frame_index",
        "frame_ms",
        "stream_ms",
        "stream_apply_ms",
        "stream_unload_ms",
        "extract_ms",
        "stream_loaded",
        "stream_unloaded",
        "pending_unload_count",
        "chunk_count",
        "zoom",
        "is_hitch",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for frame in notable:
            writer.writerow(
                {
                    "frame_index": frame.frame_index,
                    "frame_ms": frame.frame_ms,
                    "stream_ms": frame.stream_ms,
                    "stream_apply_ms": frame.stream_apply_ms,
                    "stream_unload_ms": frame.stream_unload_ms,
                    "extract_ms": frame.extract_ms,
                    "stream_loaded": frame.stream_loaded,
                    "stream_unloaded": frame.stream_unloaded,
                    "pending_unload_count": frame.pending_unload_count,
                    "chunk_count": frame.chunk_count,
                    "zoom": frame.zoom,
                    "is_hitch": frame.frame_index in hitch_indices,
                }
            )


def diagnosis_to_json(diagnosis: RunDiagnosis) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "manifest": diagnosis.manifest,
        "summary": diagnosis.summary,
        "optional_fields": sorted(diagnosis.optional_fields),
        "summary_checks": [asdict(check) for check in diagnosis.summary_checks],
        "tag_counts": diagnosis.tag_counts,
        "problem_ranking": [asdict(item) for item in diagnosis.problem_ranking],
        "run_insights": diagnosis.run_insights,
        "budget_insights": diagnosis.budget_insights,
        "open_questions": diagnosis.open_questions,
        "m23b_dod_passed": diagnosis.m23b_dod_passed,
        "m23b_unacceptable_count": diagnosis.m23b_unacceptable_count,
        "distributions": [asdict(dist) for dist in diagnosis.distributions],
        "correlations": [asdict(item) for item in diagnosis.correlations],
        "hitches": [
            {
                "frame_index": item.hitch.frame_index,
                "frame_ms": item.hitch.frame_ms,
                "tags": list(item.hitch.tags),
                "cause": asdict(item.cause),
                "context_pattern": asdict(item.context_pattern),
            }
            for item in diagnosis.hitch_analyses
        ],
        "caps": asdict(diagnosis.caps),
    }
    if diagnosis.stream_pool_breakdown:
        payload["stream_pool_breakdown"] = diagnosis.stream_pool_breakdown
    return payload


def write_json_report(diagnosis: RunDiagnosis, path: Path) -> None:
    path.write_text(
        json.dumps(diagnosis_to_json(diagnosis), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def format_fps_killers_md(payload: dict[str, Any]) -> str:
    """M25a: Markdown-Report für fps_killers.json v2."""
    lines = [
        "# FPS Killer Report (M25a)",
        "",
        "## Szenario",
        "",
        f"| Feld | Wert |",
        f"| --- | --- |",
        f"| scenario_id | `{payload.get('scenario_id', 'n/a')}` |",
        f"| run_id | `{payload.get('run_id', 'n/a')}` |",
        f"| run_mode | `{payload.get('run_mode', 'n/a')}` |",
        "",
        "## Entscheidung (CPU vs Present)",
        "",
        f"- **decision:** `{payload.get('decision', {}).get('decision')}`",
        f"- **reason:** {payload.get('decision', {}).get('reason_cpu_vs_present', 'n/a')}",
        f"- cpu_full_frame_ms_mean: {payload.get('decision', {}).get('cpu_full_frame_ms_mean', 0):.2f}",
        f"- present_wait_cpu_ms_mean: {payload.get('decision', {}).get('present_wait_cpu_ms_mean', 0):.2f}",
        f"- render_cpu_ms_mean: {payload.get('decision', {}).get('render_cpu_ms_mean', 0):.2f}",
        "",
        "## Dominanz (P95 / P99)",
        "",
        "| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    for label in ("p95", "p99"):
        item = payload.get("quantiles", {}).get(label, {})
        if not item:
            continue
        lines.append(
            f"| {label} | {item.get('frame_index')} | "
            f"{item.get('cpu_full_frame_ms', 0):.2f} | "
            f"`{item.get('dominant_phase')}` | "
            f"{item.get('dominant_share', 0) * 100:.1f}% |"
        )
    if payload.get("same_frame_for_both_quantiles"):
        lines.extend(["", "*Hinweis: p95 und p99 referenzieren denselben Frame.*", ""])

    clusters = payload.get("hitch_clusters", [])
    if clusters:
        lines.extend(["", "## Hitch-Cluster (Top)", ""])
        for cluster in clusters[:5]:
            lines.append(
                f"- **{cluster.get('cluster_id')}** ({cluster.get('hitch_count')} Hitches): "
                f"`{cluster.get('dominant_phase')}` "
                f"({cluster.get('dominant_share', 0) * 100:.1f}%) "
                f"frame={cluster.get('representative_frame_index')}"
            )

    ab_list = payload.get("ab_comparisons", [])
    if ab_list:
        lines.extend(["", "## A/B-Vergleiche", ""])
        for ab in ab_list:
            delta = ab.get("delta", {})
            lines.append(
                f"- **{ab.get('causal_feature')}**: "
                f"Δcpu_full_frame_ms_p95={delta.get('cpu_full_frame_ms_p95')} "
                f"decision_changed={delta.get('decision_changed')}"
            )
    elif payload.get("ab_comparisons_note"):
        lines.extend(["", f"*A/B: {payload['ab_comparisons_note']}*", ""])

    return "\n".join(lines) + "\n"


def write_all_reports(diagnosis: RunDiagnosis, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "markdown": output_dir / "analysis_report.md",
        "json": output_dir / "analysis_diagnosis.json",
        "hitches_csv": output_dir / "hitches.csv",
        "notable_frames_csv": output_dir / "notable_frames.csv",
        "fps_killers_md": output_dir / "fps_killers.md",
        "fps_killers_json": output_dir / "fps_killers.json",
    }
    write_markdown_report(diagnosis, paths["markdown"])
    write_json_report(diagnosis, paths["json"])
    write_hitch_csv(diagnosis, paths["hitches_csv"])
    write_notable_frames_csv(diagnosis, paths["notable_frames_csv"])

    # M25/M25a: FPS-Killer Report (nur wenn Full-Frame-Felder vorhanden).
    payload = fps_killers_payload(
        diagnosis.frames,
        manifest=diagnosis.manifest,
        hitch_analyses=diagnosis.hitch_analyses,
    )
    if payload.get("has_full_frame"):
        paths["fps_killers_json"].write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        paths["fps_killers_md"].write_text(format_fps_killers_md(payload), encoding="utf-8")
    else:
        # Nicht schreiben, um alte Runs nicht zu verwirren.
        paths.pop("fps_killers_md")
        paths.pop("fps_killers_json")
    return paths
