# M24c.2 — Streaming Scheduler & Warm-E2E

## Problem (nach M24c.1)

M24c.1 behebt READY/Timeout-Integrationsbugs, aber E2E blieb Sync-dominiert:

| Metrik | M24c.1 Baseline (100 Steps) | M24c.2 Warm (100 Steps) |
|--------|----------------------------|-------------------------|
| `stream_ms` P95 | **4523 ms** | **~77 ms** |
| `stream_ms` P50 | 1877 ms | ~64 ms |
| `sync_fallback_triggered_total` | 193 | **0** |
| `apply_sync_generate_ms_total` | 84941 ms | **0** |

**Root Cause (M24c.2):** Submit-Guard-Loop filterte Liste nicht (S2); `max_sync_applies_per_frame: 2` erlaubte Sync parallel zum Worker; Sync feuerte für nicht-submitted Coords im selben Frame.

## Änderungen

| Phase | Inhalt |
|-------|--------|
| 0 | Warm/Cold-Split, Submit-Trace-Metriken (`terrain_submit_attempted/accepted`, `sync_skipped_*`) |
| 1 | Submit-Listen-Filter, `max_sync_applies_per_frame: 0`, Apply-Budget 4, Prefetch/Caps, `sync_fallback_only_when_pool_disabled` |
| 2 | `pipeline_mode: combined` — `_generate_chunk_pipeline_task`, `submit_chunk_pipeline` |
| 3 | `tests/test_m24c2_streaming.py`, Warm-Baseline, Doku |

## Config ([`streaming.json`](../../assets/content/streaming.json))

| Key | M24c.1 | M24c.2 |
|-----|--------|--------|
| `max_sync_applies_per_frame` | 2 | **0** |
| `max_applies_per_frame` | 2 | **4** |
| `terrain_max_in_flight` | 8 | **12** |
| `terrain_parallelism_cap` | 6 | **8** |
| `prefetch_chunks` | 2 | **3** |
| `deco_parallelism_cap` | 2 | **4** |
| `deco_pause_when_visible_terrain_pending` | true | **false** |
| `pipeline_mode` | split | **combined** |
| `sync_fallback_only_when_pool_disabled` | — | **true** |

## Gates

| Gate | Kriterium | Ergebnis |
|------|-----------|----------|
| S1 | Warm `apply_sync_generate_ms_total` < 5000 ms | **0 ms** |
| S2 | Warm P95 ≤ 1200 ms, `sync_fallback` ≤ 5 | **P95 ~77 ms, 0** |
| S4 | Warm P95 ≤ 800 ms, `apply_sync` ≈ 0 | **erreicht** |

### Health-Signal: `deco_applied_total`

Im Benchmark-Szenario (`step_px=4096`, 1 Chunk/Schritt) bleibt `deco_applied_total` oft **0**, obwohl Worker-Jobs submitted werden. Ursache: Fokus bewegt sich schneller als Worker-Wallclock (~900 ms); fertige Results verlassen `wanted`/`keep` bevor Apply — kein Scheduling-Bug, sondern Szenario-Wahl.

**Interpretation:** Wert unter Schwelle → Diagnose-Kapitel prüfen, ob Route/Sichtbarkeit oder echter Scheduler-Defekt. In `chunk_world_demo` mit normaler Bewegung erwarten wir `deco_applied > 0`.

## Reproduktion

```bash
# Warm-E2E (20 Warmup + 100 Mess-Steps)
python tools/benchmark_stream_step.py --warmup-steps 20 --measure-steps 100

# Phase-0-Diagnose
python tools/benchmark_stream_step.py --phase0

# Demo-Diagnose
set WT_STREAM_DIAG=1
python apps/chunk_world_demo.py
```

Artefakte:
- [`baselines/stream_step_warm_m24c2.json`](baselines/stream_step_warm_m24c2.json)
- [`baselines/stream_step_m24c2_phase0.json`](baselines/stream_step_m24c2_phase0.json)

## Tests

```bash
pytest tests/test_m24c2_streaming.py tests/test_m24c1_streaming.py -q
```

## Nächste Schritte

M24c Terrain Phase 3–4 (Noise/SoA/Compiled) erst nach Gate S4 — Mikro ist schnell genug; verbleibender Spieler-Pfad-Hebel wäre langsameres Benchmark-Routing oder aggressiveres Prefetch für Apply-Rate.
