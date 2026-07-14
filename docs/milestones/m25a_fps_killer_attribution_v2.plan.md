---
name: M25a FPS Attribution v2
overview: "M25a bringt die FPS-Killer-Attribution auf Plan-Vertrag: feingranulares dominant_phase-Enum, CPU-vs-Present-Entscheidung mit Begründung, Szenario-Kontext und A/B-Struktur — rein CPU-seitig, ohne GPU-Timing-Abhängigkeit."
todos:
  - id: p0-baseline
    content: "Phase 0: m25a plan-Datei + M25A_BASELINE.md mit steady Referenz-Run"
    status: completed
  - id: p1-phase-enum
    content: "Phase 1: phase_enum.py + classify_dominant_phase() mit Plan-Enum + disjoint shares"
    status: completed
  - id: p2-decision
    content: "Phase 2: decision_cpu_vs_present v2 mit reason_* und Mean-Feldern"
    status: completed
  - id: p3-scenario-export
    content: "Phase 3: fps_killers.json v2 Top-Level (scenario_id, run_id, toggles) + report.py"
    status: completed
  - id: p4-quantile
    content: "Phase 4: Quantil-Frame-Auswahl closest-to-threshold + same_frame_for_both_quantiles"
    status: completed
  - id: p5-ab-compare
    content: "Phase 5: compare_fps_killers.py + steady --no-extract Variant-Run"
    status: completed
  - id: p6-schema-tests
    content: "Phase 6: SCHEMA.md, ANALYSIS.md, test_m25a_fps_killers.py, fps_killers.md Tabelle"
    status: completed
isProject: false
---

# M25a — FPS Killer Attribution v2 (CPU-Fokus)

Untermilestone von [M25 FPS Profiling](m25_fps_profiling.plan.md) — Phase 4/5 (Attribution v2, Szenario-Kontext).

## Ziel

Plan-konformes `fps_killers.json` / `fps_killers.md` mit:

- `dominant_phase` ∈ `{stream_apply, stream_pool, extract_tiles, extract_deco, render_cpu, present_wait, gpu, mixed, unclear}`
- CPU-vs-Present-Entscheidung mit Begründung
- `scenario_id`, `run_id`, Toggle-Snapshot
- A/B-Struktur für Feature-Kausalität

## Implementierung

| Modul | Rolle |
| --- | --- |
| `game_core/perf/run_analysis/phase_enum.py` | Schwellen + Enum |
| `game_core/perf/run_analysis/fps_killers.py` | Klassifikation, Quantile, Payload v2 |
| `game_core/perf/run_analysis/report.py` | Export fps_killers.md/json |
| `tools/compare_fps_killers.py` | A/B-Vergleich |
| `tools/analyze_perf_run.py` | Single Source für fps_killers.json |

Baseline: [`docs/benchmarks/perf/M25A_BASELINE.md`](../benchmarks/perf/M25A_BASELINE.md)

## Definition of Done

- [x] `dominant_phase` plan-konform (steady regeneriert)
- [x] `decision` + `reason_cpu_vs_present`
- [x] Quantil-Logik dokumentiert + getestet
- [x] scenario_id + run_id im Export
- [x] A/B-Schema + compare tool
- [x] Keine game_core→render_* Abhängigkeit
