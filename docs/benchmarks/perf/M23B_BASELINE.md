# M23b Baseline-Contract

Verbindliche Referenz für Apply-/Load-Burst-Entschärfung (M23b).

## Milestone-Einordnung

| Milestone | Inhalt |
|-----------|--------|
| M23 | Beobachtbarkeit / Profiling-Basis |
| M23a | Deferred Unload / Unload-Entschärfung |
| **M23b** | Apply-/Load-Burst-Entschärfung |
| M24 | Ores (nicht vorweggenommen) |

## Referenz-Baseline (pre-M23b)

| Run | Rolle |
|-----|--------|
| `20260710T204430Z_demo_unknown` | Demo-Integrationsreferenz (post-M23a) |

**Belegte KPIs (Demo):**

- `frame_ms_max`: 1063.64 ms
- `hitch_frame_count`: 10
- `hitch_load_count`: 20
- `hitch_unload_count`: 0
- Apply-Burst-Signatur: 10 inakzeptable Hitchs (DoD-Checker)

## Burst-Referenzszenarien (CLI)

| Szenario | Rolle |
|----------|--------|
| `catchup` | **Primäres Burst-Reproduktionsszenario** |
| `pan` | Regression (Unload/Streaming-Stabilität) |

Runs unter `docs/benchmarks/perf/runs/` mit Präfix `m23b_baseline_*`.

## Schwellenvertrag (Phase 0, verbindlich für M23b)

Quelle Hitch-Schwellen: [`assets/content/profiling.json`](../../../assets/content/profiling.json)

| Parameter | Wert |
|-----------|------|
| `hitch.frame_ms` | 16.0 ms |
| `hitch.stream_ms` | 8.0 ms |
| `hitch.loaded_count` | 4 |
| Apply-Anteil `stream_apply_ms / frame_ms` (inakzeptabel) | **≥ 0.9** |
| Cap-Referenz `max_applies_per_frame` | **2** (M23b, [`streaming.json`](../../../assets/content/streaming.json)) |

## Inakzeptable Apply-Burst-Signatur

Ein Hitch ist **inakzeptabel**, wenn gleichzeitig:

1. Tags: `frame_slow`, `stream_slow`, `load_burst`
2. Ursache: `apply_dominant`
3. `stream_loaded = max_applies_per_frame`
4. `stream_apply_ms / frame_ms ≥ 0.9`

**Akzeptabel:** `load_burst` ohne `frame_slow` (Cap-Tail unter Hitch-Schwellwerten).

## DoD-Auswertung

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
```

Terminal und Report enthalten **M23b DoD** (grün/rot).

## Vorher/Nachher

```bash
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

Identische `scenario_id`, gleiches `extract_enabled`, dokumentierter Config-Fingerprint.
