# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260713T194702Z_render_only_unknown`
- **scenario_id:** `render_only`
- **run_mode:** `cli`
- **recorded_frames:** 300
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-13T19:47:02.505611+00:00
- **git_commit:** unknown

### Config-Fingerprints

- `profiling`: `-4852663220488299992`
- `streaming`: `-4951301452672681343`
- `visibility_lod`: `8463443940065160197`
- `world_gen`: `-6473764025469487825`

**Optionale Felder:** cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 0.0182 | 0.0182 | +0.0000 | OK |
| frame_ms_p95 | 0.0244 | 0.0244 | +0.0000 | OK |
| frame_ms_max | 0.0381 | 0.0381 | +0.0000 | OK |
| stream_ms_mean | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_ms_p95 | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_ms_max | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_unload_ms_max | 0.0000 | 0.0000 | +0.0000 | OK |
| chunk_count_mean | 0.0000 | 0.0000 | +0.0000 | OK |
| recorded_frames | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_count | 0.0000 | 0.0000 | +0.0000 | OK |
| hitch_frame_count | 0.0000 | 0.0000 | +0.0000 | OK |
| hitch_stream_count | 0.0000 | 0.0000 | +0.0000 | OK |
| hitch_load_count | 0.0000 | 0.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Dauerlast durch extract_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 81.4% an frame_ms über den gesamten Run.

2. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten


## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 0.018 | 0.020 | 0.024 | 0.038 |
| stream_ms | 0.000 | 0.000 | 0.000 | 0.000 |
| stream_apply_ms | 0.000 | 0.000 | 0.000 | 0.000 |
| stream_unload_ms | 0.000 | 0.000 | 0.000 | 0.000 |
| stream_loaded | 0.000 | 0.000 | 0.000 | 0.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 0.000 | 0.000 | 0.000 | 0.000 |
| zoom | 0.350 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 0.007 | 0.008 | 0.009 | 0.013 |
| tile_extract_ms | 0.008 | 0.009 | 0.011 | 0.024 |
| extract_ms | 0.015 | 0.016 | 0.020 | 0.033 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 0.023 | 0.025 | 0.030 | 0.047 |
| cpu_unattributed_ms | 0.005 | 0.005 | 0.007 | 0.027 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_apply_ms** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_unload_ms** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_loaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ zoom** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.943, n=300): Pearson r=0.943 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ tile_extract_ms** (r=0.946, n=300): Pearson r=0.946 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ extract_ms** (r=0.983, n=300): Pearson r=0.983 (stark) — nur Indiz, keine Kausalität.
- **cpu_full_frame_ms ↔ stream_ms** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.944, n=300): Pearson r=0.944 (stark) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 0/300 Frames (0.0%).
- stream_unloaded am Unload-Cap (2): 0/300 Frames (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/300 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Durchschnittlicher Anteil an frame_ms: Stream 0.0%, Apply 0.0%, Unload 0.0%, Extract 81.4%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 80.9%.
