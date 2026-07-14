# M25a Baseline — FPS Killer Attribution v2 (CPU)

Referenz für Gate S0/S2 des M25a-Milestones.

## Referenz-Run (Baseline)

| Feld | Wert |
| --- | --- |
| run_id | `20260713T194433Z_steady_unknown` |
| scenario_id | `steady` |
| run_mode | `cli` |
| recorded_frames | 300 |
| extract_enabled | true |

## Erwartete M25a-Ergebnisse (nach Regenerierung)

| KPI | Erwartung |
| --- | --- |
| `decision.decision` | `cpu_dominant` |
| `decision.reason_cpu_vs_present` | present_wait_mean_share deutlich unter 35 % |
| `quantiles.p95.dominant_phase` | `stream_pool` (apply_pool_ms dominiert) |
| `quantiles.p99.dominant_phase` | `stream_pool` oder `extract_deco` |
| p95 vs p99 frame_index | unterschiedlich (28 vs 61 im Ist-Export) |

## A/B-Referenz (extract on/off)

| Arm | run_id | extract_enabled |
| --- | --- | --- |
| Baseline | `20260713T194433Z_steady_unknown` | true |
| Variant | `20260714T073857Z_steady_31a8d2f` | false |

Vergleich:

```bash
python tools/compare_fps_killers.py \
  docs/benchmarks/perf/runs/20260713T194433Z_steady_unknown \
  docs/benchmarks/perf/runs/20260714T073857Z_steady_31a8d2f
```

## Regenerierung

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/20260713T194433Z_steady_unknown
```

Artefakte: `analysis/fps_killers.json`, `analysis/fps_killers.md`

## M25b-Zielkorridor (Follow-up)

Siehe [M25B_BASELINE.md](M25B_BASELINE.md): `cpu_full_frame_ms_p95` ≤ 30 ms, `stream_pool` P95-Share ≤ 40 %.
