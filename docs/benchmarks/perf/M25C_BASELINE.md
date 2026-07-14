# M25c Baseline — CPU Full-Frame Attribution & Streaming-Hitch Isolation

Referenz für Gate S0 und M25c-Zielkorridor (post-M25b Demo).

## Referenz-Run (Problemstatement)

| Feld | Wert |
| --- | --- |
| run_id | `20260714T084714Z_demo_a9aaa9e` |
| scenario_id | `demo` |
| run_mode | `demo` |
| warmup_frames | 60 |

## Ist-KPIs (post-Warmup)

| Metrik | Mean | P95 | Max (Frame) |
| --- | ---: | ---: | ---: |
| `cpu_full_frame_ms` | 46.009 ms | 51.147 ms | 75.598 ms (22) |
| `cpu_unattributed_ms` | 34.625 ms | 37.226 ms | 60.183 ms |
| `canonical_tick_ms` (`frame_ms`) | 10.999 ms | 13.914 ms | 42.334 ms (20) |
| `deco_extract_ms` | 5.593 ms | 6.218 ms | 7.277 ms |
| `stream_apply_ms` | 0.567 ms | 4.524 ms | 33.484 ms |
| `apply_pool_ms` | 0.557 ms | 4.502 ms | — |
| `apply_pool_idle_skip_rate` | 90.7 % | — | — |

**Burst-Referenz (Tick-Grenze):** Frame 20 — `canonical_tick_ms` 42.334 ms, `stream_apply_ms` 33.484 ms.

## M25c-Ziele (harte Gates, Demo post-Warmup)

| Gate | Ziel |
| --- | --- |
| `cpu_residual_ms / cpu_full_frame_ms` P95 | ≤ 10 % |
| `cpu_residual_ms` P95 absolut | ≤ 5 ms |
| `abs(cpu_balance_delta_ms)` P95 | ≤ 0.05 ms |
| `apply_pool_idle_skip_rate` | ≥ 80 % |
| `apply_pool_ms` P95 | ≤ 5 ms (außer echter Load-Burst) |

## Repro-Kommandos

```bash
python apps/chunk_world_demo.py --profile
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/20260714T084714Z_demo_a9aaa9e
python tools/gate_perf_run.py docs/benchmarks/perf/runs/<m25c_candidate> \
  --cpu-residual-p95-share-max 0.10 \
  --cpu-residual-p95-max-ms 5 \
  --cpu-balance-delta-p95-max-ms 0.05 \
  --apply-pool-idle-skip-min-rate 0.80 \
  --apply-pool-p95-max-ms 5 \
  --skip-warmup 60
```

## M25d Routing

**Vorläufige Entscheidung (Code-Landkarte + Baseline `20260714T084714Z_demo_a9aaa9e`, pre-M25c-Attribution):**

| Signal @ P95 (erwartet post-M25c) | M25d-Fokus |
| --- | --- |
| `cpu_extract_render_ms` + `cpu_tile_render_ms` dominant (~75 % der bisherigen Black-Box) | **M25d-Extract-Consolidation** — Demo-Duplikat (`decorations_to_sprites` + `extractor.extract` außerhalb Tick) entfernen |
| `burst_cause_id` ∈ `{pool_idle_refresh, pool_poll_collect}` an Tick-Bursts | **M25d-Stream-Burst** — Refresh/Collect feintunen, Idle-Skip beibehalten |
| `cpu_sim_ms` / `cpu_camera_ms` nach Bilanz sichtbar ≥ 8 ms @ P95 | **M25d-Simulation/Visibility** |

Nach Kandidat-Run: `python tools/analyze_perf_run.py <run>` → `cpu_balance` + `stream_burst_frames` prüfen und Tabelle oben mit Messwerten aktualisieren.

## Verwandte Dokumente

- [M25B_BASELINE.md](M25B_BASELINE.md)
- [docs/milestones/m25c_cpu_attribution_and_hitch_isolation.plan.md](../../milestones/m25c_cpu_attribution_and_hitch_isolation.plan.md)
