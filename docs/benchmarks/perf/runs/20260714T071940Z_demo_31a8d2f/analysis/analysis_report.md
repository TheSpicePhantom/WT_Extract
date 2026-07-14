# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T071940Z_demo_31a8d2f`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 0
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T07:19:41.577332+00:00
- **git_commit:** 31a8d2f

### Config-Fingerprints

- `profiling`: `4585397586796883016`
- `streaming`: `-4397460582150671796`
- `visibility_lod`: `2878262071301917164`
- `world_gen`: `-4142747853839146686`

**Optionale Felder:** —

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 0.0000 | 0.0000 | +0.0000 | OK |
| frame_ms_p95 | 0.0000 | 0.0000 | +0.0000 | OK |
| frame_ms_max | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_ms_mean | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_ms_p95 | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_ms_max | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0000 | 0.0000 | +0.0000 | OK |
| stream_unload_ms_max | 0.0000 | 0.0000 | +0.0000 | OK |
| chunk_count_mean | 0.0000 | 0.0000 | +0.0000 | OK |
| recorded_frames | 0.0000 | 0.0000 | +0.0000 | OK |
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

## Hitch-Analyse

### Tag-Häufigkeiten


## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_apply_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_unload_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_loaded** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ zoom** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 0/1 Frames (0.0%).
- stream_unloaded am Unload-Cap (2): 0/1 Frames (0.0%).
- pending_unload_count nicht vorhanden — Backlog-Analyse eingeschränkt.

## Run-weite Diagnose

- Keine Frames im Run.

## Offene Fragen

- Keine M23a-Backlog-Felder — Unload-Backlog nur eingeschränkt bewertbar.
- Keine Extract-Metriken — Extract-Anteil nicht quantifizierbar.
