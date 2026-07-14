# M25 Baseline-Contract — FPS Profiling & Hitch Attribution

Verbindliche Referenz für M25: vollständige Frame-Time-Attribution über **CPU-Phasen**, **Renderer-CPU**, **Present/VSync-Wartezeit** und optional **GPU-Timestamps**, ohne Architekturgrenzen zu brechen.

## Milestone-Einordnung

| Milestone | Inhalt |
|-----------|--------|
| M23 | Kanonischer CPU-Tick (`frame_ms`) für Streaming + Extract (ohne Render/GPU/Present) |
| M24c.2 | Streaming Scheduler/Warm-E2E (keine FPS-Attribution) |
| **M25** | **FPS/Frame-Time Attribution** (CPU vs GPU/Present, dominierende Phase, Feature-Kausalität, CI Gates) |

## Vorher-Referenz (bindend, Post-M24c.2 Lage)

Primärbeleg: `docs/benchmarks/perf/runs/20260713T190307Z_demo_unknown/analysis/analysis_report.md`

### Ist-KPIs (M23 kanonischer Tick)

| KPI | Wert |
|-----|------:|
| `frame_ms_mean` | 23.0587 |
| `frame_ms_p95` | 26.4927 |
| `frame_ms_max` | 57.2723 |
| `stream_ms_mean` | 17.8216 |
| `stream_ms_p95` | 19.2320 |
| Hitch-Hauptursache | 314/321 `apply_dominant` |
| Mittel-Anteile an `frame_ms` | stream 77.3 %, apply 56.6 %, extract 22.6 %, unload 0.0 % |

**Wichtige Einschränkung:** Das sind **nicht** FPS-Werte, sondern nur der kanonische CPU-Tick (siehe `docs/benchmarks/perf/README.md`).

## M25 Kern-Contract (bindend)

### Neue Pflichtfelder (CPU Full-Frame)

M25 ergänzt eine zweite Zeitdomäne: vollständiger App-Frame.

| Feld | Bedeutung |
|------|-----------|
| `cpu_full_frame_ms` | Wall-Clock vom Frame-Beginn (vor kanonischem Tick) bis nach Present-Return/Frame-Ende |
| `render_cpu_ms` | Renderer-CPU: Record/Upload/Submit (ohne Present-Block) |
| `present_wait_cpu_ms` | CPU-Wartezeit durch Present/VSync/Acquire/Fences (architekturabhängig) |
| `cpu_unattributed_ms` | Rest = `cpu_full_frame_ms - Sum(cpu_phase_*_ms)` (Guardrail) |

### Optionalfelder (GPU Timing)

| Feld | Bedeutung |
|------|-----------|
| `gpu_frame_ms` | GPU-Zeit pro Frame über Vulkan-Timestamps |
| `gpu_renderpass_ms` | GPU-Zeit RenderPass/Render-Abschnitt |

### Attribution (abgeleitet, Pflicht im Report)

| Feld | Bedeutung |
|------|-----------|
| `dominant_phase_p95` / `dominant_phase_p99` | dominierende Phase für P95/P99 Frames |
| `dominant_share_p95` / `dominant_share_p99` | Anteil der dominanten Phase |
| `cpu_vs_gpu_decision` | `cpu_dominant` / `present_wait_dominant` / `gpu_dominant` (+ Begründungsfelder) |

## Harte Gates (Phase-weise, CI-fähig)

### Gate G0 — Coverage/Accounting

- Für jeden Frame: `cpu_full_frame_ms >= frame_ms`
- Guardrail: `cpu_unattributed_ms / cpu_full_frame_ms ≤ 0.05` (≤ 5 %)

### Gate G1 — Reproduzierbarkeit

- `tools/run_perf_scenario.py --scenario steady` erzeugt einen Run mit stabiler `schema_version`
- `tools/analyze_perf_run.py` erzeugt zusätzlich M25-Report-Artefakte (siehe unten)

### Gate G2 — Regression (CI, CPU-only Pflicht)

- Für Szenarien `steady` und `pan` (mindestens):
  - `cpu_full_frame_ms_p95` darf Baseline nicht um mehr als \(+x\%\) überschreiten (Toleranz in Gate-Config)
  - `dominant_phase` muss bestimmt werden (nicht `unclear`) für P95 und P99

GPU-Timing ist CI-optional.

## Artefakte pro Run (zusätzlich zu M23)

Unter `docs/benchmarks/perf/runs/<run_id>/analysis/`:

- `fps_killers.md` — Top-Killer pro Szenario, P95/P99 Dominanz, CPU-vs-GPU Entscheidung
- `fps_killers.json` — maschinenlesbares Pendant
- `fps_killers_by_scenario.csv` — Tabellenexport für Vergleiche

## Auswertung / Workflow

```bash
python tools/run_perf_scenario.py --scenario steady
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

