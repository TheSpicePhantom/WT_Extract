# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T073943Z_demo_31a8d2f`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 94
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T07:39:50.342336+00:00
- **git_commit:** 31a8d2f

### Config-Fingerprints

- `profiling`: `7736186744267695084`
- `streaming`: `-3812481342282706032`
- `visibility_lod`: `9167578406108031767`
- `world_gen`: `5645910170583930555`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, present_wait_cpu_ms, render_cpu_ms, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 23.4957 | 23.4957 | +0.0000 | OK |
| frame_ms_p95 | 26.4406 | 26.4406 | +0.0000 | OK |
| frame_ms_max | 42.0597 | 42.0597 | +0.0000 | OK |
| stream_ms_mean | 18.2082 | 18.2082 | +0.0000 | OK |
| stream_ms_p95 | 20.8019 | 20.8019 | +0.0000 | OK |
| stream_ms_max | 37.0867 | 37.0867 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0054 | 0.0054 | +0.0000 | OK |
| stream_unload_ms_max | 0.0063 | 0.0063 | +0.0000 | OK |
| chunk_count_mean | 19.0106 | 19.0106 | +0.0000 | OK |
| recorded_frames | 94.0000 | 94.0000 | +0.0000 | OK |
| hitch_count | 94.0000 | 94.0000 | +0.0000 | OK |
| hitch_frame_count | 94.0000 | 94.0000 | +0.0000 | OK |
| hitch_stream_count | 94.0000 | 94.0000 | +0.0000 | OK |
| hitch_load_count | 2.0000 | 2.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Load-/Apply-dominant** (dominant_bottleneck, Konfidenz: hoch)
   - In 92/94 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 77.5% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_apply_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 56.6% an frame_ms.

4. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `frame_slow`: 94
- `stream_slow`: 94
- `load_burst`: 2

### Frame 0

- **frame_ms:** 19.921
- **stream_ms / apply / unload:** 16.785 / 12.468 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:19.4, 2:22.3, 3:22.2

### Frame 1

- **frame_ms:** 19.410
- **stream_ms / apply / unload:** 16.305 / 12.103 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:19.9
- **Kontext danach:** 2:22.3, 3:22.2, 4:22.8

### Frame 2

- **frame_ms:** 22.250
- **stream_ms / apply / unload:** 18.222 / 13.461 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:19.9, 1:19.4
- **Kontext danach:** 3:22.2, 4:22.8, 5:22.6

### Frame 3

- **frame_ms:** 22.202
- **stream_ms / apply / unload:** 18.021 / 13.332 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:19.9, 1:19.4, 2:22.3
- **Kontext danach:** 4:22.8, 5:22.6, 6:22.2

### Frame 4

- **frame_ms:** 22.821
- **stream_ms / apply / unload:** 18.322 / 13.484 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:19.4, 2:22.3, 3:22.2
- **Kontext danach:** 5:22.6, 6:22.2, 7:20.9

### Frame 5

- **frame_ms:** 22.579
- **stream_ms / apply / unload:** 18.143 / 13.303 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:22.3, 3:22.2, 4:22.8
- **Kontext danach:** 6:22.2, 7:20.9, 8:22.0

### Frame 6

- **frame_ms:** 22.199
- **stream_ms / apply / unload:** 17.709 / 13.121 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:22.2, 4:22.8, 5:22.6
- **Kontext danach:** 7:20.9, 8:22.0, 9:22.4

### Frame 7

- **frame_ms:** 20.887
- **stream_ms / apply / unload:** 16.548 / 12.189 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:22.8, 5:22.6, 6:22.2
- **Kontext danach:** 8:22.0, 9:22.4, 10:22.4

### Frame 8

- **frame_ms:** 21.999
- **stream_ms / apply / unload:** 17.741 / 13.135 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:22.6, 6:22.2, 7:20.9
- **Kontext danach:** 9:22.4, 10:22.4, 11:20.7

### Frame 9

- **frame_ms:** 22.390
- **stream_ms / apply / unload:** 18.050 / 13.150 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:22.2, 7:20.9, 8:22.0
- **Kontext danach:** 10:22.4, 11:20.7, 12:22.2

### Frame 10

- **frame_ms:** 22.420
- **stream_ms / apply / unload:** 18.104 / 13.335 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:20.9, 8:22.0, 9:22.4
- **Kontext danach:** 11:20.7, 12:22.2, 13:21.7

### Frame 11

- **frame_ms:** 20.701
- **stream_ms / apply / unload:** 16.378 / 12.159 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:22.0, 9:22.4, 10:22.4
- **Kontext danach:** 12:22.2, 13:21.7, 14:22.2

### Frame 12

- **frame_ms:** 22.169
- **stream_ms / apply / unload:** 17.903 / 12.842 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:22.4, 10:22.4, 11:20.7
- **Kontext danach:** 13:21.7, 14:22.2, 15:21.5

### Frame 13

- **frame_ms:** 21.655
- **stream_ms / apply / unload:** 17.263 / 12.608 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:22.4, 11:20.7, 12:22.2
- **Kontext danach:** 14:22.2, 15:21.5, 16:21.4

### Frame 14

- **frame_ms:** 22.219
- **stream_ms / apply / unload:** 17.668 / 13.023 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:20.7, 12:22.2, 13:21.7
- **Kontext danach:** 15:21.5, 16:21.4, 17:21.5

### Frame 15

- **frame_ms:** 21.477
- **stream_ms / apply / unload:** 17.219 / 12.760 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:22.2, 13:21.7, 14:22.2
- **Kontext danach:** 16:21.4, 17:21.5, 18:21.9

### Frame 16

- **frame_ms:** 21.387
- **stream_ms / apply / unload:** 17.114 / 12.527 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:21.7, 14:22.2, 15:21.5
- **Kontext danach:** 17:21.5, 18:21.9, 19:21.6

### Frame 17

- **frame_ms:** 21.530
- **stream_ms / apply / unload:** 17.328 / 12.544 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:22.2, 15:21.5, 16:21.4
- **Kontext danach:** 18:21.9, 19:21.6, 20:22.0

### Frame 18

- **frame_ms:** 21.949
- **stream_ms / apply / unload:** 17.636 / 12.912 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:21.5, 16:21.4, 17:21.5
- **Kontext danach:** 19:21.6, 20:22.0, 21:22.6

### Frame 19

- **frame_ms:** 21.573
- **stream_ms / apply / unload:** 17.107 / 12.819 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:21.4, 17:21.5, 18:21.9
- **Kontext danach:** 20:22.0, 21:22.6, 22:21.9

### Frame 20

- **frame_ms:** 22.036
- **stream_ms / apply / unload:** 17.716 / 12.865 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 17:21.5, 18:21.9, 19:21.6
- **Kontext danach:** 21:22.6, 22:21.9, 23:21.8

### Frame 21

- **frame_ms:** 22.577
- **stream_ms / apply / unload:** 18.241 / 13.067 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 18:21.9, 19:21.6, 20:22.0
- **Kontext danach:** 22:21.9, 23:21.8, 24:21.3

### Frame 22

- **frame_ms:** 21.863
- **stream_ms / apply / unload:** 17.509 / 12.763 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 19:21.6, 20:22.0, 21:22.6
- **Kontext danach:** 23:21.8, 24:21.3, 25:21.9

### Frame 23

- **frame_ms:** 21.796
- **stream_ms / apply / unload:** 17.548 / 12.883 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 20:22.0, 21:22.6, 22:21.9
- **Kontext danach:** 24:21.3, 25:21.9, 26:22.3

### Frame 24

- **frame_ms:** 21.298
- **stream_ms / apply / unload:** 17.050 / 12.585 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 21:22.6, 22:21.9, 23:21.8
- **Kontext danach:** 25:21.9, 26:22.3, 27:21.6

### Frame 25

- **frame_ms:** 21.867
- **stream_ms / apply / unload:** 17.563 / 12.682 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 22:21.9, 23:21.8, 24:21.3
- **Kontext danach:** 26:22.3, 27:21.6, 28:21.8

### Frame 26

- **frame_ms:** 22.290
- **stream_ms / apply / unload:** 17.909 / 12.936 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 23:21.8, 24:21.3, 25:21.9
- **Kontext danach:** 27:21.6, 28:21.8, 29:22.1

### Frame 27

- **frame_ms:** 21.591
- **stream_ms / apply / unload:** 17.185 / 12.525 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 24:21.3, 25:21.9, 26:22.3
- **Kontext danach:** 28:21.8, 29:22.1, 30:21.9

### Frame 28

- **frame_ms:** 21.759
- **stream_ms / apply / unload:** 17.382 / 12.709 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:21.9, 26:22.3, 27:21.6
- **Kontext danach:** 29:22.1, 30:21.9, 31:22.2

### Frame 29

- **frame_ms:** 22.067
- **stream_ms / apply / unload:** 17.592 / 13.165 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:22.3, 27:21.6, 28:21.8
- **Kontext danach:** 30:21.9, 31:22.2, 32:22.0

### Frame 30

- **frame_ms:** 21.924
- **stream_ms / apply / unload:** 17.586 / 12.823 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 27:21.6, 28:21.8, 29:22.1
- **Kontext danach:** 31:22.2, 32:22.0, 33:21.2

### Frame 31

- **frame_ms:** 22.210
- **stream_ms / apply / unload:** 17.877 / 13.529 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 28:21.8, 29:22.1, 30:21.9
- **Kontext danach:** 32:22.0, 33:21.2, 34:22.2

### Frame 32

- **frame_ms:** 22.047
- **stream_ms / apply / unload:** 17.705 / 12.931 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 29:22.1, 30:21.9, 31:22.2
- **Kontext danach:** 33:21.2, 34:22.2, 35:21.4

### Frame 33

- **frame_ms:** 21.200
- **stream_ms / apply / unload:** 17.005 / 12.698 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:21.9, 31:22.2, 32:22.0
- **Kontext danach:** 34:22.2, 35:21.4, 36:22.4

### Frame 34

- **frame_ms:** 22.153
- **stream_ms / apply / unload:** 17.702 / 13.070 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 31:22.2, 32:22.0, 33:21.2
- **Kontext danach:** 35:21.4, 36:22.4, 37:23.1

### Frame 35

- **frame_ms:** 21.445
- **stream_ms / apply / unload:** 17.027 / 12.449 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:22.0, 33:21.2, 34:22.2
- **Kontext danach:** 36:22.4, 37:23.1, 38:21.0

### Frame 36

- **frame_ms:** 22.352
- **stream_ms / apply / unload:** 17.850 / 12.962 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:21.2, 34:22.2, 35:21.4
- **Kontext danach:** 37:23.1, 38:21.0, 39:21.1

### Frame 37

- **frame_ms:** 23.052
- **stream_ms / apply / unload:** 18.765 / 13.586 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 34:22.2, 35:21.4, 36:22.4
- **Kontext danach:** 38:21.0, 39:21.1, 40:20.9

### Frame 38

- **frame_ms:** 21.031
- **stream_ms / apply / unload:** 16.799 / 12.297 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 35:21.4, 36:22.4, 37:23.1
- **Kontext danach:** 39:21.1, 40:20.9, 41:21.3

### Frame 39

- **frame_ms:** 21.074
- **stream_ms / apply / unload:** 16.776 / 12.371 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 36:22.4, 37:23.1, 38:21.0
- **Kontext danach:** 40:20.9, 41:21.3, 42:22.7

### Frame 40

- **frame_ms:** 20.918
- **stream_ms / apply / unload:** 16.350 / 12.018 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 37:23.1, 38:21.0, 39:21.1
- **Kontext danach:** 41:21.3, 42:22.7, 43:20.8

### Frame 41

- **frame_ms:** 21.314
- **stream_ms / apply / unload:** 17.077 / 12.483 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 38:21.0, 39:21.1, 40:20.9
- **Kontext danach:** 42:22.7, 43:20.8, 44:21.1

### Frame 42

- **frame_ms:** 22.719
- **stream_ms / apply / unload:** 18.303 / 13.113 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 39:21.1, 40:20.9, 41:21.3
- **Kontext danach:** 43:20.8, 44:21.1, 45:22.3

### Frame 43

- **frame_ms:** 20.798
- **stream_ms / apply / unload:** 16.551 / 12.156 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 40:20.9, 41:21.3, 42:22.7
- **Kontext danach:** 44:21.1, 45:22.3, 46:42.1

### Frame 44

- **frame_ms:** 21.103
- **stream_ms / apply / unload:** 16.890 / 12.572 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 41:21.3, 42:22.7, 43:20.8
- **Kontext danach:** 45:22.3, 46:42.1, 47:24.4

### Frame 45

- **frame_ms:** 22.348
- **stream_ms / apply / unload:** 17.987 / 13.346 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 42:22.7, 43:20.8, 44:21.1
- **Kontext danach:** 46:42.1, 47:24.4, 48:31.2

### Frame 46

- **frame_ms:** 42.060
- **stream_ms / apply / unload:** 37.087 / 32.667 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 77.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 43:20.8, 44:21.1, 45:22.3
- **Kontext danach:** 47:24.4, 48:31.2, 49:29.2

### Frame 47

- **frame_ms:** 24.373
- **stream_ms / apply / unload:** 19.798 / 12.445 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2609
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 44:21.1, 45:22.3, 46:42.1
- **Kontext danach:** 48:31.2, 49:29.2, 50:23.7

### Frame 48

- **frame_ms:** 31.182
- **stream_ms / apply / unload:** 23.499 / 17.604 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2252
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 45:22.3, 46:42.1, 47:24.4
- **Kontext danach:** 49:29.2, 50:23.7, 51:21.6

### Frame 49

- **frame_ms:** 29.227
- **stream_ms / apply / unload:** 18.782 / 12.552 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 42.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 46:42.1, 47:24.4, 48:31.2
- **Kontext danach:** 50:23.7, 51:21.6, 52:29.2

### Frame 50

- **frame_ms:** 23.729
- **stream_ms / apply / unload:** 19.419 / 12.716 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 47:24.4, 48:31.2, 49:29.2
- **Kontext danach:** 51:21.6, 52:29.2, 53:25.2

### Frame 51

- **frame_ms:** 21.593
- **stream_ms / apply / unload:** 17.142 / 12.640 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 48:31.2, 49:29.2, 50:23.7
- **Kontext danach:** 52:29.2, 53:25.2, 54:25.5

### Frame 52

- **frame_ms:** 29.169
- **stream_ms / apply / unload:** 19.944 / 15.317 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 49:29.2, 50:23.7, 51:21.6
- **Kontext danach:** 53:25.2, 54:25.5, 55:23.2

### Frame 53

- **frame_ms:** 25.176
- **stream_ms / apply / unload:** 20.802 / 12.894 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 50:23.7, 51:21.6, 52:29.2
- **Kontext danach:** 54:25.5, 55:23.2, 56:24.2

### Frame 54

- **frame_ms:** 25.499
- **stream_ms / apply / unload:** 21.119 / 12.704 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 51:21.6, 52:29.2, 53:25.2
- **Kontext danach:** 55:23.2, 56:24.2, 57:26.8

### Frame 55

- **frame_ms:** 23.247
- **stream_ms / apply / unload:** 18.666 / 13.168 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 52:29.2, 53:25.2, 54:25.5
- **Kontext danach:** 56:24.2, 57:26.8, 58:23.1

### Frame 56

- **frame_ms:** 24.165
- **stream_ms / apply / unload:** 19.617 / 13.031 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 18 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 53:25.2, 54:25.5, 55:23.2
- **Kontext danach:** 57:26.8, 58:23.1, 59:22.4

### Frame 57

- **frame_ms:** 26.781
- **stream_ms / apply / unload:** 21.017 / 16.503 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 54:25.5, 55:23.2, 56:24.2
- **Kontext danach:** 58:23.1, 59:22.4, 60:26.0

### Frame 58

- **frame_ms:** 23.107
- **stream_ms / apply / unload:** 18.000 / 13.460 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 55:23.2, 56:24.2, 57:26.8
- **Kontext danach:** 59:22.4, 60:26.0, 61:24.7

### Frame 59

- **frame_ms:** 22.386
- **stream_ms / apply / unload:** 17.306 / 12.649 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 56:24.2, 57:26.8, 58:23.1
- **Kontext danach:** 60:26.0, 61:24.7, 62:25.3

### Frame 60

- **frame_ms:** 25.966
- **stream_ms / apply / unload:** 20.803 / 15.395 / 0.005
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 57:26.8, 58:23.1, 59:22.4
- **Kontext danach:** 61:24.7, 62:25.3, 63:24.5

### Frame 61

- **frame_ms:** 24.741
- **stream_ms / apply / unload:** 17.906 / 13.189 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 58:23.1, 59:22.4, 60:26.0
- **Kontext danach:** 62:25.3, 63:24.5, 64:25.3

### Frame 62

- **frame_ms:** 25.256
- **stream_ms / apply / unload:** 18.855 / 13.428 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 59:22.4, 60:26.0, 61:24.7
- **Kontext danach:** 63:24.5, 64:25.3, 65:24.4

### Frame 63

- **frame_ms:** 24.495
- **stream_ms / apply / unload:** 18.036 / 13.515 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 60:26.0, 61:24.7, 62:25.3
- **Kontext danach:** 64:25.3, 65:24.4, 66:24.0

### Frame 64

- **frame_ms:** 25.253
- **stream_ms / apply / unload:** 18.529 / 13.376 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 61:24.7, 62:25.3, 63:24.5
- **Kontext danach:** 65:24.4, 66:24.0, 67:24.2

### Frame 65

- **frame_ms:** 24.423
- **stream_ms / apply / unload:** 18.146 / 13.443 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 62:25.3, 63:24.5, 64:25.3
- **Kontext danach:** 66:24.0, 67:24.2, 68:25.6

### Frame 66

- **frame_ms:** 23.961
- **stream_ms / apply / unload:** 17.549 / 12.835 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 63:24.5, 64:25.3, 65:24.4
- **Kontext danach:** 67:24.2, 68:25.6, 69:23.8

### Frame 67

- **frame_ms:** 24.164
- **stream_ms / apply / unload:** 17.598 / 12.802 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 64:25.3, 65:24.4, 66:24.0
- **Kontext danach:** 68:25.6, 69:23.8, 70:24.9

### Frame 68

- **frame_ms:** 25.620
- **stream_ms / apply / unload:** 18.847 / 13.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 65:24.4, 66:24.0, 67:24.2
- **Kontext danach:** 69:23.8, 70:24.9, 71:24.3

### Frame 69

- **frame_ms:** 23.806
- **stream_ms / apply / unload:** 17.493 / 12.788 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 66:24.0, 67:24.2, 68:25.6
- **Kontext danach:** 70:24.9, 71:24.3, 72:24.2

### Frame 70

- **frame_ms:** 24.863
- **stream_ms / apply / unload:** 18.400 / 13.810 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 67:24.2, 68:25.6, 69:23.8
- **Kontext danach:** 71:24.3, 72:24.2, 73:25.5

### Frame 71

- **frame_ms:** 24.324
- **stream_ms / apply / unload:** 17.916 / 13.182 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 68:25.6, 69:23.8, 70:24.9
- **Kontext danach:** 72:24.2, 73:25.5, 74:22.9

### Frame 72

- **frame_ms:** 24.213
- **stream_ms / apply / unload:** 17.821 / 12.550 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 69:23.8, 70:24.9, 71:24.3
- **Kontext danach:** 73:25.5, 74:22.9, 75:25.0

### Frame 73

- **frame_ms:** 25.530
- **stream_ms / apply / unload:** 18.821 / 13.631 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 70:24.9, 71:24.3, 72:24.2
- **Kontext danach:** 74:22.9, 75:25.0, 76:24.6

### Frame 74

- **frame_ms:** 22.940
- **stream_ms / apply / unload:** 16.652 / 12.118 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 71:24.3, 72:24.2, 73:25.5
- **Kontext danach:** 75:25.0, 76:24.6, 77:24.5

### Frame 75

- **frame_ms:** 24.971
- **stream_ms / apply / unload:** 18.253 / 13.006 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 72:24.2, 73:25.5, 74:22.9
- **Kontext danach:** 76:24.6, 77:24.5, 78:24.9

### Frame 76

- **frame_ms:** 24.616
- **stream_ms / apply / unload:** 17.605 / 12.971 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 73:25.5, 74:22.9, 75:25.0
- **Kontext danach:** 77:24.5, 78:24.9, 79:25.6

### Frame 77

- **frame_ms:** 24.470
- **stream_ms / apply / unload:** 18.095 / 13.139 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 74:22.9, 75:25.0, 76:24.6
- **Kontext danach:** 78:24.9, 79:25.6, 80:24.7

### Frame 78

- **frame_ms:** 24.892
- **stream_ms / apply / unload:** 18.386 / 13.260 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 75:25.0, 76:24.6, 77:24.5
- **Kontext danach:** 79:25.6, 80:24.7, 81:23.6

### Frame 79

- **frame_ms:** 25.560
- **stream_ms / apply / unload:** 18.793 / 13.930 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 76:24.6, 77:24.5, 78:24.9
- **Kontext danach:** 80:24.7, 81:23.6, 82:24.4

### Frame 80

- **frame_ms:** 24.676
- **stream_ms / apply / unload:** 18.282 / 13.836 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 77:24.5, 78:24.9, 79:25.6
- **Kontext danach:** 81:23.6, 82:24.4, 83:25.0

### Frame 81

- **frame_ms:** 23.571
- **stream_ms / apply / unload:** 17.173 / 12.659 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 78:24.9, 79:25.6, 80:24.7
- **Kontext danach:** 82:24.4, 83:25.0, 84:24.9

### Frame 82

- **frame_ms:** 24.391
- **stream_ms / apply / unload:** 17.591 / 13.031 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 79:25.6, 80:24.7, 81:23.6
- **Kontext danach:** 83:25.0, 84:24.9, 85:26.4

### Frame 83

- **frame_ms:** 25.002
- **stream_ms / apply / unload:** 18.381 / 13.427 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 80:24.7, 81:23.6, 82:24.4
- **Kontext danach:** 84:24.9, 85:26.4, 86:24.7

### Frame 84

- **frame_ms:** 24.945
- **stream_ms / apply / unload:** 18.450 / 13.212 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 81:23.6, 82:24.4, 83:25.0
- **Kontext danach:** 85:26.4, 86:24.7, 87:24.9

### Frame 85

- **frame_ms:** 26.441
- **stream_ms / apply / unload:** 19.990 / 14.595 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 82:24.4, 83:25.0, 84:24.9
- **Kontext danach:** 86:24.7, 87:24.9, 88:23.9

### Frame 86

- **frame_ms:** 24.703
- **stream_ms / apply / unload:** 18.287 / 12.964 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 83:25.0, 84:24.9, 85:26.4
- **Kontext danach:** 87:24.9, 88:23.9, 89:23.8

### Frame 87

- **frame_ms:** 24.921
- **stream_ms / apply / unload:** 18.561 / 13.866 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 84:24.9, 85:26.4, 86:24.7
- **Kontext danach:** 88:23.9, 89:23.8, 90:23.8

### Frame 88

- **frame_ms:** 23.891
- **stream_ms / apply / unload:** 17.493 / 12.703 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 85:26.4, 86:24.7, 87:24.9
- **Kontext danach:** 89:23.8, 90:23.8, 91:24.0

### Frame 89

- **frame_ms:** 23.758
- **stream_ms / apply / unload:** 17.166 / 12.467 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 86:24.7, 87:24.9, 88:23.9
- **Kontext danach:** 90:23.8, 91:24.0, 92:23.5

### Frame 90

- **frame_ms:** 23.811
- **stream_ms / apply / unload:** 17.493 / 12.745 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 87:24.9, 88:23.9, 89:23.8
- **Kontext danach:** 91:24.0, 92:23.5, 93:24.6

### Frame 91

- **frame_ms:** 24.050
- **stream_ms / apply / unload:** 17.642 / 13.049 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 88:23.9, 89:23.8, 90:23.8
- **Kontext danach:** 92:23.5, 93:24.6

### Frame 92

- **frame_ms:** 23.475
- **stream_ms / apply / unload:** 16.978 / 12.575 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 89:23.8, 90:23.8, 91:24.0
- **Kontext danach:** 93:24.6

### Frame 93

- **frame_ms:** 24.640
- **stream_ms / apply / unload:** 17.875 / 13.431 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 90:23.8, 91:24.0, 92:23.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 23.496 | 22.821 | 26.441 | 42.060 |
| stream_ms | 18.208 | 17.821 | 20.802 | 37.087 |
| stream_apply_ms | 13.306 | 12.962 | 14.595 | 32.667 |
| stream_unload_ms | 0.005 | 0.005 | 0.005 | 0.006 |
| stream_loaded | 0.213 | 0.000 | 2.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 19.011 | 16.000 | 24.000 | 24.000 |
| zoom | 0.266 | 0.261 | 0.350 | 0.350 |
| deco_extract_ms | 5.166 | 4.398 | 6.662 | 10.333 |
| tile_extract_ms | 0.105 | 0.096 | 0.130 | 0.288 |
| extract_ms | 5.272 | 4.484 | 6.784 | 10.427 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 50.071 | 54.278 | 65.247 | 94.677 |
| render_cpu_ms | 0.336 | 0.285 | 0.570 | 1.218 |
| present_wait_cpu_ms | 0.093 | 0.086 | 0.126 | 0.297 |
| cpu_unattributed_ms | 26.146 | 27.486 | 39.549 | 64.966 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.888, n=94): Pearson r=0.888 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_apply_ms** (r=0.836, n=94): Pearson r=0.836 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unload_ms** (r=0.367, n=94): Pearson r=0.367 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_loaded** (r=0.068, n=94): Pearson r=0.068 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=94): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.320, n=94): Pearson r=0.320 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ zoom** (r=-0.504, n=94): Pearson r=-0.504 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=94): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.573, n=94): Pearson r=0.573 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ tile_extract_ms** (r=0.840, n=94): Pearson r=0.840 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ extract_ms** (r=0.584, n=94): Pearson r=0.584 (moderat) — nur Indiz, keine Kausalität.
- **cpu_full_frame_ms ↔ stream_ms** (r=0.400, n=94): Pearson r=0.400 (moderat) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.815, n=94): Pearson r=0.815 (stark) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=0.174, n=94): Pearson r=0.174 (vernachlässigbar) zwischen cpu_full_frame_ms und render_cpu_ms.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=0.185, n=94): Pearson r=0.185 (vernachlässigbar) zwischen cpu_full_frame_ms und present_wait_cpu_ms.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 2/94 Frames (2.1%).
- stream_unloaded am Unload-Cap (2): 0/94 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 2/94 (2.1%).
- Hitchs mit stream_unloaded am Cap: 0/94 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/94 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: apply_dominant (Load-/Apply-dominant) in 92/94 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 77.5%, Apply 56.6%, Unload 0.0%, Extract 22.4%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 22.3%.
- Häufigstes Hitch-Muster: periodic_cluster (94×).

## Offene Fragen

- 2 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
