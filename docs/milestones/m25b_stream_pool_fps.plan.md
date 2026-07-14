# M25b — Stream Pool Load/Apply FPS-Killer reduzieren

Milestone-Übersicht (Implementierung). Detailplan: Cursor-Plan `m25b_stream_pool_fps`.

## Ziel

Steady-State `apply_pool_ms` von ~32 ms auf ≤ 12 ms (P95) senken; `cpu_full_frame_ms_p95` ≤ 30 ms.

## Phasen

| Phase | Inhalt | Gate |
| --- | --- | --- |
| 0 | M25B_BASELINE.md, Zielkorridor | Baseline committed |
| 1 | `apply_pool_*` Sub-Metriken, `stream_pool_breakdown` | Breakdown sichtbar |
| 2 | Pool Idle-Fast-Path + `pool_idle_skip_*` Config | idle_skip > 80 %, mean ≤ 15 ms |
| 3 | Single-Route + bedingter Second-Pass; Poll early-exit | route_passes mean ≤ 1.2 |
| 4 | Submit early-exit, Suppression-Throttle | M24c2 grün |
| 5 | gate_perf_run, Tests, Kandidat-Run | DoD-Gates |

## Hauptdateien

- `game_core/chunk_streaming.py` — Pool-Block
- `game_core/chunk_gen_pool.py` — Poll/Collect
- `assets/content/streaming.json` — Idle-Config
- `tools/gate_perf_run.py`, `tests/test_m25b_stream_pool_reduction.py`
