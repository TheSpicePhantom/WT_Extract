# M25b Baseline — Stream Pool Load/Apply FPS-Killer

Referenz für Gate S0 und M25b-Zielkorridor (M25a-Attribution unverändert).

## Ausgangslage (M25a A/B)

| Run | run_id | cpu_full P95 | pool P95-Share | apply_pool P95 (abs.) |
| --- | --- | ---: | ---: | ---: |
| Baseline (extract on) | `20260713T194433Z_steady_unknown` | 58.37 ms | 59.8 % | ~35 ms |
| Extract-off | `20260714T073857Z_steady_31a8d2f` | 19.94 ms | 76.3 % | ~15 ms |
| **M25b Kandidat** | `20260714T080831Z_steady_b0f57bb` | **11.64 ms** | **36.7 %** | **~8 ms** |

**Kernbefund:** Post-Warmup bei `stream_loaded=0` bleibt `apply_pool_ms ≈ 32 ms` — Idle-Pool-Steuerungs-Overhead, nicht Present/GPU.

## M25b-Ziele (harte Gates, steady + extract)

| Gate | Baseline | Ziel M25b |
| --- | ---: | ---: |
| `cpu_full_frame_ms_p95` | ~58 ms | **≤ 30 ms** |
| `stream_pool` P95-Share | ~60 % | **≤ 40 %** |
| `apply_pool_ms` P95 (abs.) | ~35 ms | **≤ 12 ms** |
| `decision.decision` | `cpu_dominant` | `cpu_dominant` |
| `present_wait_share_mean` | ~0 % | **< 5 %** |

Zielkorridor gesamt: **25–30 ms** Frame-P95 bei Pool-P95 **≤ 12 ms**.

## Repro-Kommandos

```bash
python tools/run_perf_scenario.py --scenario steady
python tools/run_perf_scenario.py --scenario steady --no-extract
python tools/analyze_perf_run.py
python tools/compare_fps_killers.py \
  docs/benchmarks/perf/runs/20260713T194433Z_steady_unknown \
  docs/benchmarks/perf/runs/<m25b_candidate>
python tools/gate_perf_run.py docs/benchmarks/perf/runs/<m25b_candidate> \
  --cpu-full-frame-p95-max-ms 30 \
  --stream-pool-p95-share-max 0.40 \
  --present-wait-share-max 0.05 \
  --skip-warmup 60
```

## Verwandte Dokumente

- [M25A_BASELINE.md](M25A_BASELINE.md) — FPS-Killer-Attribution v2
- [docs/milestones/m25b_stream_pool_fps.plan.md](../../milestones/m25b_stream_pool_fps.plan.md)
