# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T073857Z_steady_31a8d2f`
- **scenario_id:** `steady`
- **run_mode:** `cli`
- **recorded_frames:** 300
- **warmup_frames:** 60
- **extract_enabled:** False
- **recorded_at:** 2026-07-14T07:39:04.655320+00:00
- **git_commit:** 31a8d2f

### Config-Fingerprints

- `profiling`: `-5422585132419312176`
- `streaming`: `-4153725804683380962`
- `visibility_lod`: `6226521864733223066`
- `world_gen`: `-3032753789956274089`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, pending_unload_count, stream_unload_drained, stream_unload_marked

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 18.0863 | 18.0863 | +0.0000 | OK |
| frame_ms_p95 | 19.9305 | 19.9305 | +0.0000 | OK |
| frame_ms_max | 29.3067 | 29.3067 | +0.0000 | OK |
| stream_ms_mean | 18.0744 | 18.0744 | +0.0000 | OK |
| stream_ms_p95 | 19.9185 | 19.9185 | +0.0000 | OK |
| stream_ms_max | 29.2954 | 29.2954 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0057 | 0.0057 | +0.0000 | OK |
| stream_unload_ms_max | 0.0132 | 0.0132 | +0.0000 | OK |
| chunk_count_mean | 15.1267 | 15.1267 | +0.0000 | OK |
| recorded_frames | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_count | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_frame_count | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_stream_count | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_load_count | 1.0000 | 1.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Load-/Apply-dominant** (dominant_bottleneck, Konfidenz: hoch)
   - In 300/300 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 99.9% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_apply_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 75.0% an frame_ms.

4. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `frame_slow`: 300
- `stream_slow`: 300
- `load_burst`: 1

### Frame 0

- **frame_ms:** 18.638
- **stream_ms / apply / unload:** 18.626 / 14.200 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:18.8, 2:18.1, 3:24.9

### Frame 1

- **frame_ms:** 18.761
- **stream_ms / apply / unload:** 18.749 / 13.968 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:18.6
- **Kontext danach:** 2:18.1, 3:24.9, 4:25.9

### Frame 2

- **frame_ms:** 18.106
- **stream_ms / apply / unload:** 18.094 / 13.740 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:18.6, 1:18.8
- **Kontext danach:** 3:24.9, 4:25.9, 5:19.3

### Frame 3

- **frame_ms:** 24.921
- **stream_ms / apply / unload:** 24.909 / 20.508 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 82.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:18.6, 1:18.8, 2:18.1
- **Kontext danach:** 4:25.9, 5:19.3, 6:26.4

### Frame 4

- **frame_ms:** 25.929
- **stream_ms / apply / unload:** 25.916 / 21.232 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 81.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:18.8, 2:18.1, 3:24.9
- **Kontext danach:** 5:19.3, 6:26.4, 7:20.3

### Frame 5

- **frame_ms:** 19.308
- **stream_ms / apply / unload:** 19.293 / 13.323 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:18.1, 3:24.9, 4:25.9
- **Kontext danach:** 6:26.4, 7:20.3, 8:17.8

### Frame 6

- **frame_ms:** 26.417
- **stream_ms / apply / unload:** 26.405 / 19.261 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 72.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:24.9, 4:25.9, 5:19.3
- **Kontext danach:** 7:20.3, 8:17.8, 9:17.7

### Frame 7

- **frame_ms:** 20.306
- **stream_ms / apply / unload:** 20.294 / 15.788 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 77.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:25.9, 5:19.3, 6:26.4
- **Kontext danach:** 8:17.8, 9:17.7, 10:17.5

### Frame 8

- **frame_ms:** 17.758
- **stream_ms / apply / unload:** 17.747 / 13.257 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:19.3, 6:26.4, 7:20.3
- **Kontext danach:** 9:17.7, 10:17.5, 11:19.7

### Frame 9

- **frame_ms:** 17.747
- **stream_ms / apply / unload:** 17.735 / 13.209 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:26.4, 7:20.3, 8:17.8
- **Kontext danach:** 10:17.5, 11:19.7, 12:19.3

### Frame 10

- **frame_ms:** 17.500
- **stream_ms / apply / unload:** 17.489 / 13.179 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:20.3, 8:17.8, 9:17.7
- **Kontext danach:** 11:19.7, 12:19.3, 13:19.3

### Frame 11

- **frame_ms:** 19.711
- **stream_ms / apply / unload:** 19.697 / 15.367 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 78.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:17.8, 9:17.7, 10:17.5
- **Kontext danach:** 12:19.3, 13:19.3, 14:21.5

### Frame 12

- **frame_ms:** 19.266
- **stream_ms / apply / unload:** 19.249 / 13.505 / 0.013
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.1% von frame_ms
  - Unload-dominant: 0.1% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:17.7, 10:17.5, 11:19.7
- **Kontext danach:** 13:19.3, 14:21.5, 15:20.1

### Frame 13

- **frame_ms:** 19.316
- **stream_ms / apply / unload:** 19.305 / 14.714 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:17.5, 11:19.7, 12:19.3
- **Kontext danach:** 14:21.5, 15:20.1, 16:29.3

### Frame 14

- **frame_ms:** 21.520
- **stream_ms / apply / unload:** 21.507 / 17.214 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 80.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:19.7, 12:19.3, 13:19.3
- **Kontext danach:** 15:20.1, 16:29.3, 17:21.0

### Frame 15

- **frame_ms:** 20.118
- **stream_ms / apply / unload:** 20.104 / 13.152 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:19.3, 13:19.3, 14:21.5
- **Kontext danach:** 16:29.3, 17:21.0, 18:24.5

### Frame 16

- **frame_ms:** 29.307
- **stream_ms / apply / unload:** 29.295 / 21.950 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:19.3, 14:21.5, 15:20.1
- **Kontext danach:** 17:21.0, 18:24.5, 19:26.0

### Frame 17

- **frame_ms:** 21.028
- **stream_ms / apply / unload:** 21.015 / 16.570 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 78.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:21.5, 15:20.1, 16:29.3
- **Kontext danach:** 18:24.5, 19:26.0, 20:20.9

### Frame 18

- **frame_ms:** 24.483
- **stream_ms / apply / unload:** 24.468 / 16.512 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:20.1, 16:29.3, 17:21.0
- **Kontext danach:** 19:26.0, 20:20.9, 21:20.9

### Frame 19

- **frame_ms:** 26.046
- **stream_ms / apply / unload:** 26.031 / 18.924 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 72.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:29.3, 17:21.0, 18:24.5
- **Kontext danach:** 20:20.9, 21:20.9, 22:27.9

### Frame 20

- **frame_ms:** 20.917
- **stream_ms / apply / unload:** 20.905 / 15.463 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 17:21.0, 18:24.5, 19:26.0
- **Kontext danach:** 21:20.9, 22:27.9, 23:18.6

### Frame 21

- **frame_ms:** 20.912
- **stream_ms / apply / unload:** 20.901 / 15.823 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 18:24.5, 19:26.0, 20:20.9
- **Kontext danach:** 22:27.9, 23:18.6, 24:19.4

### Frame 22

- **frame_ms:** 27.945
- **stream_ms / apply / unload:** 27.933 / 22.704 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 11 / 0.3500
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 81.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 19:26.0, 20:20.9, 21:20.9
- **Kontext danach:** 23:18.6, 24:19.4, 25:17.9

### Frame 23

- **frame_ms:** 18.649
- **stream_ms / apply / unload:** 18.637 / 14.199 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 20:20.9, 21:20.9, 22:27.9
- **Kontext danach:** 24:19.4, 25:17.9, 26:19.4

### Frame 24

- **frame_ms:** 19.365
- **stream_ms / apply / unload:** 19.353 / 14.250 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 21:20.9, 22:27.9, 23:18.6
- **Kontext danach:** 25:17.9, 26:19.4, 27:19.9

### Frame 25

- **frame_ms:** 17.907
- **stream_ms / apply / unload:** 17.895 / 13.503 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 22:27.9, 23:18.6, 24:19.4
- **Kontext danach:** 26:19.4, 27:19.9, 28:17.9

### Frame 26

- **frame_ms:** 19.375
- **stream_ms / apply / unload:** 19.363 / 14.872 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 23:18.6, 24:19.4, 25:17.9
- **Kontext danach:** 27:19.9, 28:17.9, 29:17.7

### Frame 27

- **frame_ms:** 19.930
- **stream_ms / apply / unload:** 19.919 / 15.162 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 24:19.4, 25:17.9, 26:19.4
- **Kontext danach:** 28:17.9, 29:17.7, 30:17.6

### Frame 28

- **frame_ms:** 17.942
- **stream_ms / apply / unload:** 17.931 / 13.426 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:17.9, 26:19.4, 27:19.9
- **Kontext danach:** 29:17.7, 30:17.6, 31:17.7

### Frame 29

- **frame_ms:** 17.692
- **stream_ms / apply / unload:** 17.682 / 13.181 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:19.4, 27:19.9, 28:17.9
- **Kontext danach:** 30:17.6, 31:17.7, 32:17.8

### Frame 30

- **frame_ms:** 17.611
- **stream_ms / apply / unload:** 17.599 / 13.237 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 27:19.9, 28:17.9, 29:17.7
- **Kontext danach:** 31:17.7, 32:17.8, 33:17.9

### Frame 31

- **frame_ms:** 17.717
- **stream_ms / apply / unload:** 17.705 / 13.514 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 28:17.9, 29:17.7, 30:17.6
- **Kontext danach:** 32:17.8, 33:17.9, 34:17.0

### Frame 32

- **frame_ms:** 17.836
- **stream_ms / apply / unload:** 17.825 / 13.341 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 29:17.7, 30:17.6, 31:17.7
- **Kontext danach:** 33:17.9, 34:17.0, 35:17.3

### Frame 33

- **frame_ms:** 17.948
- **stream_ms / apply / unload:** 17.937 / 13.200 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:17.6, 31:17.7, 32:17.8
- **Kontext danach:** 34:17.0, 35:17.3, 36:17.1

### Frame 34

- **frame_ms:** 16.978
- **stream_ms / apply / unload:** 16.967 / 12.622 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 31:17.7, 32:17.8, 33:17.9
- **Kontext danach:** 35:17.3, 36:17.1, 37:17.3

### Frame 35

- **frame_ms:** 17.274
- **stream_ms / apply / unload:** 17.263 / 12.937 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:17.8, 33:17.9, 34:17.0
- **Kontext danach:** 36:17.1, 37:17.3, 38:18.0

### Frame 36

- **frame_ms:** 17.134
- **stream_ms / apply / unload:** 17.122 / 12.921 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:17.9, 34:17.0, 35:17.3
- **Kontext danach:** 37:17.3, 38:18.0, 39:18.3

### Frame 37

- **frame_ms:** 17.330
- **stream_ms / apply / unload:** 17.318 / 13.091 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 34:17.0, 35:17.3, 36:17.1
- **Kontext danach:** 38:18.0, 39:18.3, 40:17.9

### Frame 38

- **frame_ms:** 18.041
- **stream_ms / apply / unload:** 18.029 / 13.797 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 35:17.3, 36:17.1, 37:17.3
- **Kontext danach:** 39:18.3, 40:17.9, 41:17.0

### Frame 39

- **frame_ms:** 18.325
- **stream_ms / apply / unload:** 18.314 / 13.942 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 36:17.1, 37:17.3, 38:18.0
- **Kontext danach:** 40:17.9, 41:17.0, 42:17.5

### Frame 40

- **frame_ms:** 17.867
- **stream_ms / apply / unload:** 17.855 / 13.187 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 37:17.3, 38:18.0, 39:18.3
- **Kontext danach:** 41:17.0, 42:17.5, 43:17.0

### Frame 41

- **frame_ms:** 17.047
- **stream_ms / apply / unload:** 17.035 / 12.721 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 38:18.0, 39:18.3, 40:17.9
- **Kontext danach:** 42:17.5, 43:17.0, 44:17.7

### Frame 42

- **frame_ms:** 17.544
- **stream_ms / apply / unload:** 17.533 / 13.285 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 39:18.3, 40:17.9, 41:17.0
- **Kontext danach:** 43:17.0, 44:17.7, 45:17.8

### Frame 43

- **frame_ms:** 16.955
- **stream_ms / apply / unload:** 16.943 / 12.745 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 40:17.9, 41:17.0, 42:17.5
- **Kontext danach:** 44:17.7, 45:17.8, 46:17.1

### Frame 44

- **frame_ms:** 17.679
- **stream_ms / apply / unload:** 17.667 / 13.122 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 41:17.0, 42:17.5, 43:17.0
- **Kontext danach:** 45:17.8, 46:17.1, 47:17.4

### Frame 45

- **frame_ms:** 17.825
- **stream_ms / apply / unload:** 17.814 / 13.359 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 42:17.5, 43:17.0, 44:17.7
- **Kontext danach:** 46:17.1, 47:17.4, 48:16.7

### Frame 46

- **frame_ms:** 17.126
- **stream_ms / apply / unload:** 17.114 / 12.832 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 43:17.0, 44:17.7, 45:17.8
- **Kontext danach:** 47:17.4, 48:16.7, 49:18.0

### Frame 47

- **frame_ms:** 17.442
- **stream_ms / apply / unload:** 17.431 / 12.975 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 44:17.7, 45:17.8, 46:17.1
- **Kontext danach:** 48:16.7, 49:18.0, 50:17.3

### Frame 48

- **frame_ms:** 16.702
- **stream_ms / apply / unload:** 16.690 / 12.480 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 45:17.8, 46:17.1, 47:17.4
- **Kontext danach:** 49:18.0, 50:17.3, 51:17.6

### Frame 49

- **frame_ms:** 17.962
- **stream_ms / apply / unload:** 17.951 / 13.655 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 46:17.1, 47:17.4, 48:16.7
- **Kontext danach:** 50:17.3, 51:17.6, 52:17.2

### Frame 50

- **frame_ms:** 17.260
- **stream_ms / apply / unload:** 17.249 / 13.074 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 47:17.4, 48:16.7, 49:18.0
- **Kontext danach:** 51:17.6, 52:17.2, 53:17.1

### Frame 51

- **frame_ms:** 17.558
- **stream_ms / apply / unload:** 17.546 / 13.270 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 48:16.7, 49:18.0, 50:17.3
- **Kontext danach:** 52:17.2, 53:17.1, 54:18.6

### Frame 52

- **frame_ms:** 17.169
- **stream_ms / apply / unload:** 17.157 / 12.521 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 72.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 49:18.0, 50:17.3, 51:17.6
- **Kontext danach:** 53:17.1, 54:18.6, 55:16.9

### Frame 53

- **frame_ms:** 17.130
- **stream_ms / apply / unload:** 17.119 / 12.925 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 50:17.3, 51:17.6, 52:17.2
- **Kontext danach:** 54:18.6, 55:16.9, 56:17.3

### Frame 54

- **frame_ms:** 18.592
- **stream_ms / apply / unload:** 18.581 / 13.785 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 51:17.6, 52:17.2, 53:17.1
- **Kontext danach:** 55:16.9, 56:17.3, 57:17.8

### Frame 55

- **frame_ms:** 16.936
- **stream_ms / apply / unload:** 16.921 / 12.750 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 52:17.2, 53:17.1, 54:18.6
- **Kontext danach:** 56:17.3, 57:17.8, 58:17.7

### Frame 56

- **frame_ms:** 17.302
- **stream_ms / apply / unload:** 17.288 / 13.010 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 53:17.1, 54:18.6, 55:16.9
- **Kontext danach:** 57:17.8, 58:17.7, 59:17.2

### Frame 57

- **frame_ms:** 17.816
- **stream_ms / apply / unload:** 17.804 / 13.479 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 54:18.6, 55:16.9, 56:17.3
- **Kontext danach:** 58:17.7, 59:17.2, 60:17.2

### Frame 58

- **frame_ms:** 17.707
- **stream_ms / apply / unload:** 17.696 / 13.298 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 55:16.9, 56:17.3, 57:17.8
- **Kontext danach:** 59:17.2, 60:17.2, 61:18.7

### Frame 59

- **frame_ms:** 17.187
- **stream_ms / apply / unload:** 17.175 / 12.834 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 56:17.3, 57:17.8, 58:17.7
- **Kontext danach:** 60:17.2, 61:18.7, 62:18.9

### Frame 60

- **frame_ms:** 17.228
- **stream_ms / apply / unload:** 17.216 / 12.770 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 57:17.8, 58:17.7, 59:17.2
- **Kontext danach:** 61:18.7, 62:18.9, 63:17.4

### Frame 61

- **frame_ms:** 18.734
- **stream_ms / apply / unload:** 18.723 / 14.103 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 58:17.7, 59:17.2, 60:17.2
- **Kontext danach:** 62:18.9, 63:17.4, 64:17.1

### Frame 62

- **frame_ms:** 18.926
- **stream_ms / apply / unload:** 18.915 / 14.762 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 78.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 59:17.2, 60:17.2, 61:18.7
- **Kontext danach:** 63:17.4, 64:17.1, 65:18.3

### Frame 63

- **frame_ms:** 17.374
- **stream_ms / apply / unload:** 17.362 / 12.883 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 60:17.2, 61:18.7, 62:18.9
- **Kontext danach:** 64:17.1, 65:18.3, 66:19.4

### Frame 64

- **frame_ms:** 17.139
- **stream_ms / apply / unload:** 17.128 / 12.884 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 61:18.7, 62:18.9, 63:17.4
- **Kontext danach:** 65:18.3, 66:19.4, 67:18.4

### Frame 65

- **frame_ms:** 18.269
- **stream_ms / apply / unload:** 18.259 / 13.797 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 62:18.9, 63:17.4, 64:17.1
- **Kontext danach:** 66:19.4, 67:18.4, 68:18.6

### Frame 66

- **frame_ms:** 19.367
- **stream_ms / apply / unload:** 19.354 / 14.989 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 77.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 63:17.4, 64:17.1, 65:18.3
- **Kontext danach:** 67:18.4, 68:18.6, 69:17.8

### Frame 67

- **frame_ms:** 18.369
- **stream_ms / apply / unload:** 18.357 / 13.387 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 72.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 64:17.1, 65:18.3, 66:19.4
- **Kontext danach:** 68:18.6, 69:17.8, 70:19.0

### Frame 68

- **frame_ms:** 18.556
- **stream_ms / apply / unload:** 18.544 / 13.780 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 65:18.3, 66:19.4, 67:18.4
- **Kontext danach:** 69:17.8, 70:19.0, 71:20.3

### Frame 69

- **frame_ms:** 17.825
- **stream_ms / apply / unload:** 17.813 / 13.333 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 66:19.4, 67:18.4, 68:18.6
- **Kontext danach:** 70:19.0, 71:20.3, 72:17.2

### Frame 70

- **frame_ms:** 19.026
- **stream_ms / apply / unload:** 19.013 / 14.390 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 67:18.4, 68:18.6, 69:17.8
- **Kontext danach:** 71:20.3, 72:17.2, 73:17.0

### Frame 71

- **frame_ms:** 20.283
- **stream_ms / apply / unload:** 20.270 / 15.470 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 68:18.6, 69:17.8, 70:19.0
- **Kontext danach:** 72:17.2, 73:17.0, 74:17.3

### Frame 72

- **frame_ms:** 17.194
- **stream_ms / apply / unload:** 17.182 / 12.807 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 69:17.8, 70:19.0, 71:20.3
- **Kontext danach:** 73:17.0, 74:17.3, 75:18.1

### Frame 73

- **frame_ms:** 17.024
- **stream_ms / apply / unload:** 17.012 / 12.723 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 70:19.0, 71:20.3, 72:17.2
- **Kontext danach:** 74:17.3, 75:18.1, 76:16.9

### Frame 74

- **frame_ms:** 17.257
- **stream_ms / apply / unload:** 17.246 / 12.893 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 71:20.3, 72:17.2, 73:17.0
- **Kontext danach:** 75:18.1, 76:16.9, 77:17.0

### Frame 75

- **frame_ms:** 18.085
- **stream_ms / apply / unload:** 18.073 / 13.303 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 72:17.2, 73:17.0, 74:17.3
- **Kontext danach:** 76:16.9, 77:17.0, 78:17.8

### Frame 76

- **frame_ms:** 16.928
- **stream_ms / apply / unload:** 16.915 / 12.723 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 73:17.0, 74:17.3, 75:18.1
- **Kontext danach:** 77:17.0, 78:17.8, 79:17.8

### Frame 77

- **frame_ms:** 17.037
- **stream_ms / apply / unload:** 17.027 / 12.841 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 74:17.3, 75:18.1, 76:16.9
- **Kontext danach:** 78:17.8, 79:17.8, 80:17.7

### Frame 78

- **frame_ms:** 17.790
- **stream_ms / apply / unload:** 17.779 / 12.697 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 75:18.1, 76:16.9, 77:17.0
- **Kontext danach:** 79:17.8, 80:17.7, 81:17.6

### Frame 79

- **frame_ms:** 17.818
- **stream_ms / apply / unload:** 17.807 / 13.441 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 76:16.9, 77:17.0, 78:17.8
- **Kontext danach:** 80:17.7, 81:17.6, 82:18.1

### Frame 80

- **frame_ms:** 17.715
- **stream_ms / apply / unload:** 17.704 / 13.166 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 77:17.0, 78:17.8, 79:17.8
- **Kontext danach:** 81:17.6, 82:18.1, 83:18.1

### Frame 81

- **frame_ms:** 17.582
- **stream_ms / apply / unload:** 17.571 / 12.974 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 78:17.8, 79:17.8, 80:17.7
- **Kontext danach:** 82:18.1, 83:18.1, 84:17.6

### Frame 82

- **frame_ms:** 18.089
- **stream_ms / apply / unload:** 18.071 / 13.633 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 79:17.8, 80:17.7, 81:17.6
- **Kontext danach:** 83:18.1, 84:17.6, 85:17.7

### Frame 83

- **frame_ms:** 18.112
- **stream_ms / apply / unload:** 18.100 / 13.565 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 80:17.7, 81:17.6, 82:18.1
- **Kontext danach:** 84:17.6, 85:17.7, 86:17.6

### Frame 84

- **frame_ms:** 17.634
- **stream_ms / apply / unload:** 17.623 / 13.254 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 81:17.6, 82:18.1, 83:18.1
- **Kontext danach:** 85:17.7, 86:17.6, 87:17.8

### Frame 85

- **frame_ms:** 17.703
- **stream_ms / apply / unload:** 17.688 / 13.386 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 82:18.1, 83:18.1, 84:17.6
- **Kontext danach:** 86:17.6, 87:17.8, 88:17.8

### Frame 86

- **frame_ms:** 17.612
- **stream_ms / apply / unload:** 17.600 / 13.174 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 83:18.1, 84:17.6, 85:17.7
- **Kontext danach:** 87:17.8, 88:17.8, 89:17.9

### Frame 87

- **frame_ms:** 17.828
- **stream_ms / apply / unload:** 17.817 / 13.588 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 84:17.6, 85:17.7, 86:17.6
- **Kontext danach:** 88:17.8, 89:17.9, 90:17.8

### Frame 88

- **frame_ms:** 17.751
- **stream_ms / apply / unload:** 17.740 / 13.159 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 85:17.7, 86:17.6, 87:17.8
- **Kontext danach:** 89:17.9, 90:17.8, 91:17.7

### Frame 89

- **frame_ms:** 17.884
- **stream_ms / apply / unload:** 17.872 / 13.352 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 86:17.6, 87:17.8, 88:17.8
- **Kontext danach:** 90:17.8, 91:17.7, 92:18.0

### Frame 90

- **frame_ms:** 17.812
- **stream_ms / apply / unload:** 17.800 / 13.329 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 87:17.8, 88:17.8, 89:17.9
- **Kontext danach:** 91:17.7, 92:18.0, 93:17.9

### Frame 91

- **frame_ms:** 17.710
- **stream_ms / apply / unload:** 17.698 / 13.118 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 88:17.8, 89:17.9, 90:17.8
- **Kontext danach:** 92:18.0, 93:17.9, 94:17.6

### Frame 92

- **frame_ms:** 18.029
- **stream_ms / apply / unload:** 18.017 / 13.729 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 89:17.9, 90:17.8, 91:17.7
- **Kontext danach:** 93:17.9, 94:17.6, 95:18.2

### Frame 93

- **frame_ms:** 17.948
- **stream_ms / apply / unload:** 17.937 / 13.452 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 90:17.8, 91:17.7, 92:18.0
- **Kontext danach:** 94:17.6, 95:18.2, 96:17.8

### Frame 94

- **frame_ms:** 17.607
- **stream_ms / apply / unload:** 17.596 / 13.059 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 91:17.7, 92:18.0, 93:17.9
- **Kontext danach:** 95:18.2, 96:17.8, 97:17.7

### Frame 95

- **frame_ms:** 18.213
- **stream_ms / apply / unload:** 18.201 / 13.436 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 92:18.0, 93:17.9, 94:17.6
- **Kontext danach:** 96:17.8, 97:17.7, 98:18.1

### Frame 96

- **frame_ms:** 17.807
- **stream_ms / apply / unload:** 17.792 / 13.438 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 93:17.9, 94:17.6, 95:18.2
- **Kontext danach:** 97:17.7, 98:18.1, 99:18.1

### Frame 97

- **frame_ms:** 17.709
- **stream_ms / apply / unload:** 17.697 / 13.340 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 94:17.6, 95:18.2, 96:17.8
- **Kontext danach:** 98:18.1, 99:18.1, 100:17.4

### Frame 98

- **frame_ms:** 18.124
- **stream_ms / apply / unload:** 18.112 / 13.537 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 95:18.2, 96:17.8, 97:17.7
- **Kontext danach:** 99:18.1, 100:17.4, 101:17.0

### Frame 99

- **frame_ms:** 18.061
- **stream_ms / apply / unload:** 18.049 / 13.457 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 96:17.8, 97:17.7, 98:18.1
- **Kontext danach:** 100:17.4, 101:17.0, 102:17.6

### Frame 100

- **frame_ms:** 17.355
- **stream_ms / apply / unload:** 17.343 / 12.998 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 97:17.7, 98:18.1, 99:18.1
- **Kontext danach:** 101:17.0, 102:17.6, 103:18.1

### Frame 101

- **frame_ms:** 16.981
- **stream_ms / apply / unload:** 16.970 / 12.797 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 98:18.1, 99:18.1, 100:17.4
- **Kontext danach:** 102:17.6, 103:18.1, 104:17.9

### Frame 102

- **frame_ms:** 17.596
- **stream_ms / apply / unload:** 17.584 / 13.419 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 99:18.1, 100:17.4, 101:17.0
- **Kontext danach:** 103:18.1, 104:17.9, 105:17.6

### Frame 103

- **frame_ms:** 18.143
- **stream_ms / apply / unload:** 18.132 / 13.576 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 100:17.4, 101:17.0, 102:17.6
- **Kontext danach:** 104:17.9, 105:17.6, 106:18.0

### Frame 104

- **frame_ms:** 17.881
- **stream_ms / apply / unload:** 17.869 / 13.352 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 101:17.0, 102:17.6, 103:18.1
- **Kontext danach:** 105:17.6, 106:18.0, 107:17.8

### Frame 105

- **frame_ms:** 17.627
- **stream_ms / apply / unload:** 17.613 / 13.159 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 102:17.6, 103:18.1, 104:17.9
- **Kontext danach:** 106:18.0, 107:17.8, 108:17.7

### Frame 106

- **frame_ms:** 18.000
- **stream_ms / apply / unload:** 17.986 / 13.508 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 103:18.1, 104:17.9, 105:17.6
- **Kontext danach:** 107:17.8, 108:17.7, 109:17.6

### Frame 107

- **frame_ms:** 17.843
- **stream_ms / apply / unload:** 17.831 / 13.362 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 104:17.9, 105:17.6, 106:18.0
- **Kontext danach:** 108:17.7, 109:17.6, 110:17.8

### Frame 108

- **frame_ms:** 17.654
- **stream_ms / apply / unload:** 17.642 / 13.122 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 105:17.6, 106:18.0, 107:17.8
- **Kontext danach:** 109:17.6, 110:17.8, 111:17.8

### Frame 109

- **frame_ms:** 17.601
- **stream_ms / apply / unload:** 17.589 / 13.134 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 106:18.0, 107:17.8, 108:17.7
- **Kontext danach:** 110:17.8, 111:17.8, 112:17.7

### Frame 110

- **frame_ms:** 17.766
- **stream_ms / apply / unload:** 17.754 / 13.336 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 107:17.8, 108:17.7, 109:17.6
- **Kontext danach:** 111:17.8, 112:17.7, 113:17.7

### Frame 111

- **frame_ms:** 17.775
- **stream_ms / apply / unload:** 17.763 / 13.352 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 108:17.7, 109:17.6, 110:17.8
- **Kontext danach:** 112:17.7, 113:17.7, 114:17.6

### Frame 112

- **frame_ms:** 17.719
- **stream_ms / apply / unload:** 17.707 / 13.500 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 109:17.6, 110:17.8, 111:17.8
- **Kontext danach:** 113:17.7, 114:17.6, 115:17.4

### Frame 113

- **frame_ms:** 17.731
- **stream_ms / apply / unload:** 17.720 / 13.207 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 110:17.8, 111:17.8, 112:17.7
- **Kontext danach:** 114:17.6, 115:17.4, 116:18.0

### Frame 114

- **frame_ms:** 17.622
- **stream_ms / apply / unload:** 17.611 / 13.160 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 111:17.8, 112:17.7, 113:17.7
- **Kontext danach:** 115:17.4, 116:18.0, 117:17.6

### Frame 115

- **frame_ms:** 17.399
- **stream_ms / apply / unload:** 17.387 / 12.958 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 112:17.7, 113:17.7, 114:17.6
- **Kontext danach:** 116:18.0, 117:17.6, 118:17.9

### Frame 116

- **frame_ms:** 18.006
- **stream_ms / apply / unload:** 17.994 / 13.385 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 113:17.7, 114:17.6, 115:17.4
- **Kontext danach:** 117:17.6, 118:17.9, 119:17.8

### Frame 117

- **frame_ms:** 17.637
- **stream_ms / apply / unload:** 17.625 / 13.437 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 114:17.6, 115:17.4, 116:18.0
- **Kontext danach:** 118:17.9, 119:17.8, 120:17.7

### Frame 118

- **frame_ms:** 17.893
- **stream_ms / apply / unload:** 17.882 / 13.464 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 115:17.4, 116:18.0, 117:17.6
- **Kontext danach:** 119:17.8, 120:17.7, 121:17.9

### Frame 119

- **frame_ms:** 17.831
- **stream_ms / apply / unload:** 17.821 / 13.281 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 116:18.0, 117:17.6, 118:17.9
- **Kontext danach:** 120:17.7, 121:17.9, 122:18.0

### Frame 120

- **frame_ms:** 17.671
- **stream_ms / apply / unload:** 17.660 / 13.232 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 117:17.6, 118:17.9, 119:17.8
- **Kontext danach:** 121:17.9, 122:18.0, 123:17.5

### Frame 121

- **frame_ms:** 17.925
- **stream_ms / apply / unload:** 17.913 / 13.561 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 118:17.9, 119:17.8, 120:17.7
- **Kontext danach:** 122:18.0, 123:17.5, 124:17.3

### Frame 122

- **frame_ms:** 17.983
- **stream_ms / apply / unload:** 17.971 / 13.585 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 119:17.8, 120:17.7, 121:17.9
- **Kontext danach:** 123:17.5, 124:17.3, 125:17.3

### Frame 123

- **frame_ms:** 17.507
- **stream_ms / apply / unload:** 17.495 / 12.988 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 120:17.7, 121:17.9, 122:18.0
- **Kontext danach:** 124:17.3, 125:17.3, 126:17.7

### Frame 124

- **frame_ms:** 17.292
- **stream_ms / apply / unload:** 17.281 / 13.033 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 121:17.9, 122:18.0, 123:17.5
- **Kontext danach:** 125:17.3, 126:17.7, 127:17.5

### Frame 125

- **frame_ms:** 17.282
- **stream_ms / apply / unload:** 17.270 / 12.878 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 122:18.0, 123:17.5, 124:17.3
- **Kontext danach:** 126:17.7, 127:17.5, 128:17.1

### Frame 126

- **frame_ms:** 17.685
- **stream_ms / apply / unload:** 17.674 / 13.043 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 123:17.5, 124:17.3, 125:17.3
- **Kontext danach:** 127:17.5, 128:17.1, 129:17.5

### Frame 127

- **frame_ms:** 17.521
- **stream_ms / apply / unload:** 17.509 / 13.265 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 124:17.3, 125:17.3, 126:17.7
- **Kontext danach:** 128:17.1, 129:17.5, 130:17.4

### Frame 128

- **frame_ms:** 17.137
- **stream_ms / apply / unload:** 17.125 / 13.047 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 125:17.3, 126:17.7, 127:17.5
- **Kontext danach:** 129:17.5, 130:17.4, 131:17.8

### Frame 129

- **frame_ms:** 17.463
- **stream_ms / apply / unload:** 17.451 / 13.100 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 126:17.7, 127:17.5, 128:17.1
- **Kontext danach:** 130:17.4, 131:17.8, 132:17.8

### Frame 130

- **frame_ms:** 17.447
- **stream_ms / apply / unload:** 17.436 / 13.115 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 127:17.5, 128:17.1, 129:17.5
- **Kontext danach:** 131:17.8, 132:17.8, 133:17.9

### Frame 131

- **frame_ms:** 17.824
- **stream_ms / apply / unload:** 17.812 / 13.378 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 128:17.1, 129:17.5, 130:17.4
- **Kontext danach:** 132:17.8, 133:17.9, 134:17.4

### Frame 132

- **frame_ms:** 17.768
- **stream_ms / apply / unload:** 17.757 / 13.237 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 129:17.5, 130:17.4, 131:17.8
- **Kontext danach:** 133:17.9, 134:17.4, 135:17.9

### Frame 133

- **frame_ms:** 17.879
- **stream_ms / apply / unload:** 17.866 / 13.501 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 130:17.4, 131:17.8, 132:17.8
- **Kontext danach:** 134:17.4, 135:17.9, 136:17.6

### Frame 134

- **frame_ms:** 17.408
- **stream_ms / apply / unload:** 17.397 / 13.150 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 131:17.8, 132:17.8, 133:17.9
- **Kontext danach:** 135:17.9, 136:17.6, 137:18.7

### Frame 135

- **frame_ms:** 17.884
- **stream_ms / apply / unload:** 17.873 / 13.341 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 132:17.8, 133:17.9, 134:17.4
- **Kontext danach:** 136:17.6, 137:18.7, 138:17.7

### Frame 136

- **frame_ms:** 17.568
- **stream_ms / apply / unload:** 17.557 / 13.175 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 133:17.9, 134:17.4, 135:17.9
- **Kontext danach:** 137:18.7, 138:17.7, 139:17.3

### Frame 137

- **frame_ms:** 18.689
- **stream_ms / apply / unload:** 18.678 / 13.383 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 134:17.4, 135:17.9, 136:17.6
- **Kontext danach:** 138:17.7, 139:17.3, 140:17.8

### Frame 138

- **frame_ms:** 17.724
- **stream_ms / apply / unload:** 17.712 / 13.561 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 135:17.9, 136:17.6, 137:18.7
- **Kontext danach:** 139:17.3, 140:17.8, 141:18.3

### Frame 139

- **frame_ms:** 17.322
- **stream_ms / apply / unload:** 17.310 / 13.169 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 136:17.6, 137:18.7, 138:17.7
- **Kontext danach:** 140:17.8, 141:18.3, 142:18.0

### Frame 140

- **frame_ms:** 17.814
- **stream_ms / apply / unload:** 17.802 / 13.343 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 137:18.7, 138:17.7, 139:17.3
- **Kontext danach:** 141:18.3, 142:18.0, 143:17.5

### Frame 141

- **frame_ms:** 18.266
- **stream_ms / apply / unload:** 18.255 / 13.737 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 138:17.7, 139:17.3, 140:17.8
- **Kontext danach:** 142:18.0, 143:17.5, 144:17.8

### Frame 142

- **frame_ms:** 17.976
- **stream_ms / apply / unload:** 17.965 / 13.552 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 139:17.3, 140:17.8, 141:18.3
- **Kontext danach:** 143:17.5, 144:17.8, 145:17.9

### Frame 143

- **frame_ms:** 17.540
- **stream_ms / apply / unload:** 17.530 / 13.164 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 140:17.8, 141:18.3, 142:18.0
- **Kontext danach:** 144:17.8, 145:17.9, 146:17.7

### Frame 144

- **frame_ms:** 17.758
- **stream_ms / apply / unload:** 17.748 / 13.164 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 141:18.3, 142:18.0, 143:17.5
- **Kontext danach:** 145:17.9, 146:17.7, 147:19.0

### Frame 145

- **frame_ms:** 17.872
- **stream_ms / apply / unload:** 17.861 / 13.385 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 142:18.0, 143:17.5, 144:17.8
- **Kontext danach:** 146:17.7, 147:19.0, 148:17.5

### Frame 146

- **frame_ms:** 17.699
- **stream_ms / apply / unload:** 17.687 / 13.182 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 143:17.5, 144:17.8, 145:17.9
- **Kontext danach:** 147:19.0, 148:17.5, 149:17.7

### Frame 147

- **frame_ms:** 19.017
- **stream_ms / apply / unload:** 19.005 / 14.606 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 144:17.8, 145:17.9, 146:17.7
- **Kontext danach:** 148:17.5, 149:17.7, 150:17.5

### Frame 148

- **frame_ms:** 17.484
- **stream_ms / apply / unload:** 17.473 / 13.039 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 145:17.9, 146:17.7, 147:19.0
- **Kontext danach:** 149:17.7, 150:17.5, 151:17.4

### Frame 149

- **frame_ms:** 17.717
- **stream_ms / apply / unload:** 17.707 / 13.173 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 146:17.7, 147:19.0, 148:17.5
- **Kontext danach:** 150:17.5, 151:17.4, 152:17.4

### Frame 150

- **frame_ms:** 17.539
- **stream_ms / apply / unload:** 17.529 / 13.091 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 147:19.0, 148:17.5, 149:17.7
- **Kontext danach:** 151:17.4, 152:17.4, 153:17.1

### Frame 151

- **frame_ms:** 17.370
- **stream_ms / apply / unload:** 17.359 / 12.923 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 148:17.5, 149:17.7, 150:17.5
- **Kontext danach:** 152:17.4, 153:17.1, 154:17.8

### Frame 152

- **frame_ms:** 17.417
- **stream_ms / apply / unload:** 17.406 / 13.206 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 149:17.7, 150:17.5, 151:17.4
- **Kontext danach:** 153:17.1, 154:17.8, 155:17.5

### Frame 153

- **frame_ms:** 17.054
- **stream_ms / apply / unload:** 17.042 / 12.776 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 150:17.5, 151:17.4, 152:17.4
- **Kontext danach:** 154:17.8, 155:17.5, 156:17.8

### Frame 154

- **frame_ms:** 17.811
- **stream_ms / apply / unload:** 17.800 / 13.653 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 151:17.4, 152:17.4, 153:17.1
- **Kontext danach:** 155:17.5, 156:17.8, 157:17.8

### Frame 155

- **frame_ms:** 17.542
- **stream_ms / apply / unload:** 17.531 / 12.990 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 152:17.4, 153:17.1, 154:17.8
- **Kontext danach:** 156:17.8, 157:17.8, 158:17.9

### Frame 156

- **frame_ms:** 17.834
- **stream_ms / apply / unload:** 17.823 / 13.492 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 153:17.1, 154:17.8, 155:17.5
- **Kontext danach:** 157:17.8, 158:17.9, 159:17.6

### Frame 157

- **frame_ms:** 17.755
- **stream_ms / apply / unload:** 17.743 / 13.209 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 154:17.8, 155:17.5, 156:17.8
- **Kontext danach:** 158:17.9, 159:17.6, 160:17.8

### Frame 158

- **frame_ms:** 17.918
- **stream_ms / apply / unload:** 17.906 / 13.544 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 155:17.5, 156:17.8, 157:17.8
- **Kontext danach:** 159:17.6, 160:17.8, 161:17.6

### Frame 159

- **frame_ms:** 17.606
- **stream_ms / apply / unload:** 17.594 / 13.217 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 156:17.8, 157:17.8, 158:17.9
- **Kontext danach:** 160:17.8, 161:17.6, 162:18.1

### Frame 160

- **frame_ms:** 17.810
- **stream_ms / apply / unload:** 17.798 / 13.343 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 157:17.8, 158:17.9, 159:17.6
- **Kontext danach:** 161:17.6, 162:18.1, 163:17.7

### Frame 161

- **frame_ms:** 17.555
- **stream_ms / apply / unload:** 17.543 / 13.110 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 158:17.9, 159:17.6, 160:17.8
- **Kontext danach:** 162:18.1, 163:17.7, 164:17.6

### Frame 162

- **frame_ms:** 18.094
- **stream_ms / apply / unload:** 18.081 / 13.557 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 159:17.6, 160:17.8, 161:17.6
- **Kontext danach:** 163:17.7, 164:17.6, 165:17.7

### Frame 163

- **frame_ms:** 17.721
- **stream_ms / apply / unload:** 17.708 / 13.429 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 160:17.8, 161:17.6, 162:18.1
- **Kontext danach:** 164:17.6, 165:17.7, 166:17.8

### Frame 164

- **frame_ms:** 17.614
- **stream_ms / apply / unload:** 17.603 / 13.181 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 161:17.6, 162:18.1, 163:17.7
- **Kontext danach:** 165:17.7, 166:17.8, 167:18.0

### Frame 165

- **frame_ms:** 17.694
- **stream_ms / apply / unload:** 17.682 / 13.096 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 162:18.1, 163:17.7, 164:17.6
- **Kontext danach:** 166:17.8, 167:18.0, 168:18.0

### Frame 166

- **frame_ms:** 17.766
- **stream_ms / apply / unload:** 17.754 / 13.212 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 163:17.7, 164:17.6, 165:17.7
- **Kontext danach:** 167:18.0, 168:18.0, 169:18.3

### Frame 167

- **frame_ms:** 17.950
- **stream_ms / apply / unload:** 17.934 / 13.392 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 164:17.6, 165:17.7, 166:17.8
- **Kontext danach:** 168:18.0, 169:18.3, 170:17.8

### Frame 168

- **frame_ms:** 17.998
- **stream_ms / apply / unload:** 17.986 / 13.753 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 165:17.7, 166:17.8, 167:18.0
- **Kontext danach:** 169:18.3, 170:17.8, 171:18.1

### Frame 169

- **frame_ms:** 18.290
- **stream_ms / apply / unload:** 18.279 / 13.678 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 166:17.8, 167:18.0, 168:18.0
- **Kontext danach:** 170:17.8, 171:18.1, 172:17.9

### Frame 170

- **frame_ms:** 17.780
- **stream_ms / apply / unload:** 17.769 / 13.122 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 167:18.0, 168:18.0, 169:18.3
- **Kontext danach:** 171:18.1, 172:17.9, 173:17.7

### Frame 171

- **frame_ms:** 18.076
- **stream_ms / apply / unload:** 18.065 / 13.391 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 168:18.0, 169:18.3, 170:17.8
- **Kontext danach:** 172:17.9, 173:17.7, 174:18.1

### Frame 172

- **frame_ms:** 17.897
- **stream_ms / apply / unload:** 17.884 / 13.585 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 169:18.3, 170:17.8, 171:18.1
- **Kontext danach:** 173:17.7, 174:18.1, 175:17.9

### Frame 173

- **frame_ms:** 17.704
- **stream_ms / apply / unload:** 17.691 / 13.330 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 170:17.8, 171:18.1, 172:17.9
- **Kontext danach:** 174:18.1, 175:17.9, 176:17.8

### Frame 174

- **frame_ms:** 18.141
- **stream_ms / apply / unload:** 18.130 / 13.664 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 171:18.1, 172:17.9, 173:17.7
- **Kontext danach:** 175:17.9, 176:17.8, 177:17.9

### Frame 175

- **frame_ms:** 17.937
- **stream_ms / apply / unload:** 17.925 / 13.290 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 172:17.9, 173:17.7, 174:18.1
- **Kontext danach:** 176:17.8, 177:17.9, 178:17.9

### Frame 176

- **frame_ms:** 17.761
- **stream_ms / apply / unload:** 17.749 / 13.370 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 173:17.7, 174:18.1, 175:17.9
- **Kontext danach:** 177:17.9, 178:17.9, 179:17.5

### Frame 177

- **frame_ms:** 17.918
- **stream_ms / apply / unload:** 17.907 / 13.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 174:18.1, 175:17.9, 176:17.8
- **Kontext danach:** 178:17.9, 179:17.5, 180:17.8

### Frame 178

- **frame_ms:** 17.950
- **stream_ms / apply / unload:** 17.939 / 13.390 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 175:17.9, 176:17.8, 177:17.9
- **Kontext danach:** 179:17.5, 180:17.8, 181:18.0

### Frame 179

- **frame_ms:** 17.483
- **stream_ms / apply / unload:** 17.471 / 12.923 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 176:17.8, 177:17.9, 178:17.9
- **Kontext danach:** 180:17.8, 181:18.0, 182:17.4

### Frame 180

- **frame_ms:** 17.804
- **stream_ms / apply / unload:** 17.781 / 13.251 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 177:17.9, 178:17.9, 179:17.5
- **Kontext danach:** 181:18.0, 182:17.4, 183:18.0

### Frame 181

- **frame_ms:** 17.998
- **stream_ms / apply / unload:** 17.987 / 13.703 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 178:17.9, 179:17.5, 180:17.8
- **Kontext danach:** 182:17.4, 183:18.0, 184:17.7

### Frame 182

- **frame_ms:** 17.409
- **stream_ms / apply / unload:** 17.397 / 13.183 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 179:17.5, 180:17.8, 181:18.0
- **Kontext danach:** 183:18.0, 184:17.7, 185:18.0

### Frame 183

- **frame_ms:** 18.033
- **stream_ms / apply / unload:** 18.017 / 13.338 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 180:17.8, 181:18.0, 182:17.4
- **Kontext danach:** 184:17.7, 185:18.0, 186:17.7

### Frame 184

- **frame_ms:** 17.700
- **stream_ms / apply / unload:** 17.689 / 13.059 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 181:18.0, 182:17.4, 183:18.0
- **Kontext danach:** 185:18.0, 186:17.7, 187:17.4

### Frame 185

- **frame_ms:** 18.009
- **stream_ms / apply / unload:** 17.993 / 13.497 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 182:17.4, 183:18.0, 184:17.7
- **Kontext danach:** 186:17.7, 187:17.4, 188:17.8

### Frame 186

- **frame_ms:** 17.655
- **stream_ms / apply / unload:** 17.642 / 13.467 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 183:18.0, 184:17.7, 185:18.0
- **Kontext danach:** 187:17.4, 188:17.8, 189:17.6

### Frame 187

- **frame_ms:** 17.400
- **stream_ms / apply / unload:** 17.388 / 13.310 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 184:17.7, 185:18.0, 186:17.7
- **Kontext danach:** 188:17.8, 189:17.6, 190:18.1

### Frame 188

- **frame_ms:** 17.755
- **stream_ms / apply / unload:** 17.743 / 13.443 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 185:18.0, 186:17.7, 187:17.4
- **Kontext danach:** 189:17.6, 190:18.1, 191:17.8

### Frame 189

- **frame_ms:** 17.625
- **stream_ms / apply / unload:** 17.615 / 13.150 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 186:17.7, 187:17.4, 188:17.8
- **Kontext danach:** 190:18.1, 191:17.8, 192:17.8

### Frame 190

- **frame_ms:** 18.080
- **stream_ms / apply / unload:** 18.069 / 13.400 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 187:17.4, 188:17.8, 189:17.6
- **Kontext danach:** 191:17.8, 192:17.8, 193:17.7

### Frame 191

- **frame_ms:** 17.805
- **stream_ms / apply / unload:** 17.794 / 13.400 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 188:17.8, 189:17.6, 190:18.1
- **Kontext danach:** 192:17.8, 193:17.7, 194:17.6

### Frame 192

- **frame_ms:** 17.819
- **stream_ms / apply / unload:** 17.807 / 13.430 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 189:17.6, 190:18.1, 191:17.8
- **Kontext danach:** 193:17.7, 194:17.6, 195:18.0

### Frame 193

- **frame_ms:** 17.696
- **stream_ms / apply / unload:** 17.684 / 13.277 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 190:18.1, 191:17.8, 192:17.8
- **Kontext danach:** 194:17.6, 195:18.0, 196:17.7

### Frame 194

- **frame_ms:** 17.642
- **stream_ms / apply / unload:** 17.630 / 13.158 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 191:17.8, 192:17.8, 193:17.7
- **Kontext danach:** 195:18.0, 196:17.7, 197:17.8

### Frame 195

- **frame_ms:** 17.977
- **stream_ms / apply / unload:** 17.965 / 13.333 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 192:17.8, 193:17.7, 194:17.6
- **Kontext danach:** 196:17.7, 197:17.8, 198:18.0

### Frame 196

- **frame_ms:** 17.696
- **stream_ms / apply / unload:** 17.684 / 13.428 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 193:17.7, 194:17.6, 195:18.0
- **Kontext danach:** 197:17.8, 198:18.0, 199:17.8

### Frame 197

- **frame_ms:** 17.802
- **stream_ms / apply / unload:** 17.791 / 13.210 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 194:17.6, 195:18.0, 196:17.7
- **Kontext danach:** 198:18.0, 199:17.8, 200:18.0

### Frame 198

- **frame_ms:** 17.963
- **stream_ms / apply / unload:** 17.951 / 13.406 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 195:18.0, 196:17.7, 197:17.8
- **Kontext danach:** 199:17.8, 200:18.0, 201:18.0

### Frame 199

- **frame_ms:** 17.803
- **stream_ms / apply / unload:** 17.792 / 13.288 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 196:17.7, 197:17.8, 198:18.0
- **Kontext danach:** 200:18.0, 201:18.0, 202:17.7

### Frame 200

- **frame_ms:** 17.969
- **stream_ms / apply / unload:** 17.958 / 13.486 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 197:17.8, 198:18.0, 199:17.8
- **Kontext danach:** 201:18.0, 202:17.7, 203:18.0

### Frame 201

- **frame_ms:** 17.962
- **stream_ms / apply / unload:** 17.950 / 13.716 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 198:18.0, 199:17.8, 200:18.0
- **Kontext danach:** 202:17.7, 203:18.0, 204:17.6

### Frame 202

- **frame_ms:** 17.678
- **stream_ms / apply / unload:** 17.667 / 13.117 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 199:17.8, 200:18.0, 201:18.0
- **Kontext danach:** 203:18.0, 204:17.6, 205:17.6

### Frame 203

- **frame_ms:** 18.045
- **stream_ms / apply / unload:** 18.033 / 13.364 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 200:18.0, 201:18.0, 202:17.7
- **Kontext danach:** 204:17.6, 205:17.6, 206:18.1

### Frame 204

- **frame_ms:** 17.588
- **stream_ms / apply / unload:** 17.576 / 13.233 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 201:18.0, 202:17.7, 203:18.0
- **Kontext danach:** 205:17.6, 206:18.1, 207:17.5

### Frame 205

- **frame_ms:** 17.609
- **stream_ms / apply / unload:** 17.598 / 13.378 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 202:17.7, 203:18.0, 204:17.6
- **Kontext danach:** 206:18.1, 207:17.5, 208:17.2

### Frame 206

- **frame_ms:** 18.066
- **stream_ms / apply / unload:** 18.055 / 13.673 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 203:18.0, 204:17.6, 205:17.6
- **Kontext danach:** 207:17.5, 208:17.2, 209:17.5

### Frame 207

- **frame_ms:** 17.490
- **stream_ms / apply / unload:** 17.479 / 13.166 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 204:17.6, 205:17.6, 206:18.1
- **Kontext danach:** 208:17.2, 209:17.5, 210:17.4

### Frame 208

- **frame_ms:** 17.194
- **stream_ms / apply / unload:** 17.183 / 12.793 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 205:17.6, 206:18.1, 207:17.5
- **Kontext danach:** 209:17.5, 210:17.4, 211:17.6

### Frame 209

- **frame_ms:** 17.513
- **stream_ms / apply / unload:** 17.502 / 13.129 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 206:18.1, 207:17.5, 208:17.2
- **Kontext danach:** 210:17.4, 211:17.6, 212:17.7

### Frame 210

- **frame_ms:** 17.351
- **stream_ms / apply / unload:** 17.340 / 12.770 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 207:17.5, 208:17.2, 209:17.5
- **Kontext danach:** 211:17.6, 212:17.7, 213:17.6

### Frame 211

- **frame_ms:** 17.573
- **stream_ms / apply / unload:** 17.561 / 13.296 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 208:17.2, 209:17.5, 210:17.4
- **Kontext danach:** 212:17.7, 213:17.6, 214:17.7

### Frame 212

- **frame_ms:** 17.672
- **stream_ms / apply / unload:** 17.661 / 13.368 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 209:17.5, 210:17.4, 211:17.6
- **Kontext danach:** 213:17.6, 214:17.7, 215:17.8

### Frame 213

- **frame_ms:** 17.560
- **stream_ms / apply / unload:** 17.549 / 13.074 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 210:17.4, 211:17.6, 212:17.7
- **Kontext danach:** 214:17.7, 215:17.8, 216:17.8

### Frame 214

- **frame_ms:** 17.740
- **stream_ms / apply / unload:** 17.730 / 13.405 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 211:17.6, 212:17.7, 213:17.6
- **Kontext danach:** 215:17.8, 216:17.8, 217:17.5

### Frame 215

- **frame_ms:** 17.826
- **stream_ms / apply / unload:** 17.813 / 13.306 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 212:17.7, 213:17.6, 214:17.7
- **Kontext danach:** 216:17.8, 217:17.5, 218:17.7

### Frame 216

- **frame_ms:** 17.823
- **stream_ms / apply / unload:** 17.811 / 13.315 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 213:17.6, 214:17.7, 215:17.8
- **Kontext danach:** 217:17.5, 218:17.7, 219:17.8

### Frame 217

- **frame_ms:** 17.489
- **stream_ms / apply / unload:** 17.476 / 13.155 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 214:17.7, 215:17.8, 216:17.8
- **Kontext danach:** 218:17.7, 219:17.8, 220:17.5

### Frame 218

- **frame_ms:** 17.680
- **stream_ms / apply / unload:** 17.668 / 13.420 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 215:17.8, 216:17.8, 217:17.5
- **Kontext danach:** 219:17.8, 220:17.5, 221:17.2

### Frame 219

- **frame_ms:** 17.792
- **stream_ms / apply / unload:** 17.780 / 13.409 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 216:17.8, 217:17.5, 218:17.7
- **Kontext danach:** 220:17.5, 221:17.2, 222:22.8

### Frame 220

- **frame_ms:** 17.538
- **stream_ms / apply / unload:** 17.527 / 12.988 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 217:17.5, 218:17.7, 219:17.8
- **Kontext danach:** 221:17.2, 222:22.8, 223:17.3

### Frame 221

- **frame_ms:** 17.238
- **stream_ms / apply / unload:** 17.227 / 12.883 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 218:17.7, 219:17.8, 220:17.5
- **Kontext danach:** 222:22.8, 223:17.3, 224:17.2

### Frame 222

- **frame_ms:** 22.754
- **stream_ms / apply / unload:** 22.742 / 18.441 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 81.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 219:17.8, 220:17.5, 221:17.2
- **Kontext danach:** 223:17.3, 224:17.2, 225:17.4

### Frame 223

- **frame_ms:** 17.326
- **stream_ms / apply / unload:** 17.314 / 13.109 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 220:17.5, 221:17.2, 222:22.8
- **Kontext danach:** 224:17.2, 225:17.4, 226:17.3

### Frame 224

- **frame_ms:** 17.220
- **stream_ms / apply / unload:** 17.208 / 12.979 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 221:17.2, 222:22.8, 223:17.3
- **Kontext danach:** 225:17.4, 226:17.3, 227:17.4

### Frame 225

- **frame_ms:** 17.406
- **stream_ms / apply / unload:** 17.394 / 13.136 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 222:22.8, 223:17.3, 224:17.2
- **Kontext danach:** 226:17.3, 227:17.4, 228:18.0

### Frame 226

- **frame_ms:** 17.340
- **stream_ms / apply / unload:** 17.328 / 13.006 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 223:17.3, 224:17.2, 225:17.4
- **Kontext danach:** 227:17.4, 228:18.0, 229:18.1

### Frame 227

- **frame_ms:** 17.446
- **stream_ms / apply / unload:** 17.434 / 13.025 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 224:17.2, 225:17.4, 226:17.3
- **Kontext danach:** 228:18.0, 229:18.1, 230:17.6

### Frame 228

- **frame_ms:** 17.968
- **stream_ms / apply / unload:** 17.958 / 13.348 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 225:17.4, 226:17.3, 227:17.4
- **Kontext danach:** 229:18.1, 230:17.6, 231:17.8

### Frame 229

- **frame_ms:** 18.149
- **stream_ms / apply / unload:** 18.138 / 13.548 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 226:17.3, 227:17.4, 228:18.0
- **Kontext danach:** 230:17.6, 231:17.8, 232:18.0

### Frame 230

- **frame_ms:** 17.576
- **stream_ms / apply / unload:** 17.564 / 13.390 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 227:17.4, 228:18.0, 229:18.1
- **Kontext danach:** 231:17.8, 232:18.0, 233:18.1

### Frame 231

- **frame_ms:** 17.834
- **stream_ms / apply / unload:** 17.823 / 13.238 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 228:18.0, 229:18.1, 230:17.6
- **Kontext danach:** 232:18.0, 233:18.1, 234:17.8

### Frame 232

- **frame_ms:** 17.973
- **stream_ms / apply / unload:** 17.962 / 13.387 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 229:18.1, 230:17.6, 231:17.8
- **Kontext danach:** 233:18.1, 234:17.8, 235:17.9

### Frame 233

- **frame_ms:** 18.056
- **stream_ms / apply / unload:** 18.045 / 13.491 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 230:17.6, 231:17.8, 232:18.0
- **Kontext danach:** 234:17.8, 235:17.9, 236:17.7

### Frame 234

- **frame_ms:** 17.792
- **stream_ms / apply / unload:** 17.780 / 13.501 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 231:17.8, 232:18.0, 233:18.1
- **Kontext danach:** 235:17.9, 236:17.7, 237:17.7

### Frame 235

- **frame_ms:** 17.863
- **stream_ms / apply / unload:** 17.851 / 13.469 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 232:18.0, 233:18.1, 234:17.8
- **Kontext danach:** 236:17.7, 237:17.7, 238:18.5

### Frame 236

- **frame_ms:** 17.690
- **stream_ms / apply / unload:** 17.678 / 13.085 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 233:18.1, 234:17.8, 235:17.9
- **Kontext danach:** 237:17.7, 238:18.5, 239:17.7

### Frame 237

- **frame_ms:** 17.727
- **stream_ms / apply / unload:** 17.716 / 13.353 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 234:17.8, 235:17.9, 236:17.7
- **Kontext danach:** 238:18.5, 239:17.7, 240:17.9

### Frame 238

- **frame_ms:** 18.455
- **stream_ms / apply / unload:** 18.444 / 13.703 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 235:17.9, 236:17.7, 237:17.7
- **Kontext danach:** 239:17.7, 240:17.9, 241:17.6

### Frame 239

- **frame_ms:** 17.747
- **stream_ms / apply / unload:** 17.735 / 13.524 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 236:17.7, 237:17.7, 238:18.5
- **Kontext danach:** 240:17.9, 241:17.6, 242:17.9

### Frame 240

- **frame_ms:** 17.939
- **stream_ms / apply / unload:** 17.927 / 13.521 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 237:17.7, 238:18.5, 239:17.7
- **Kontext danach:** 241:17.6, 242:17.9, 243:18.1

### Frame 241

- **frame_ms:** 17.599
- **stream_ms / apply / unload:** 17.588 / 13.188 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 238:18.5, 239:17.7, 240:17.9
- **Kontext danach:** 242:17.9, 243:18.1, 244:17.8

### Frame 242

- **frame_ms:** 17.900
- **stream_ms / apply / unload:** 17.888 / 13.375 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 239:17.7, 240:17.9, 241:17.6
- **Kontext danach:** 243:18.1, 244:17.8, 245:18.2

### Frame 243

- **frame_ms:** 18.086
- **stream_ms / apply / unload:** 18.072 / 13.655 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 240:17.9, 241:17.6, 242:17.9
- **Kontext danach:** 244:17.8, 245:18.2, 246:18.0

### Frame 244

- **frame_ms:** 17.787
- **stream_ms / apply / unload:** 17.776 / 13.374 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 241:17.6, 242:17.9, 243:18.1
- **Kontext danach:** 245:18.2, 246:18.0, 247:18.0

### Frame 245

- **frame_ms:** 18.185
- **stream_ms / apply / unload:** 18.174 / 13.520 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 242:17.9, 243:18.1, 244:17.8
- **Kontext danach:** 246:18.0, 247:18.0, 248:18.2

### Frame 246

- **frame_ms:** 18.004
- **stream_ms / apply / unload:** 17.991 / 13.508 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 243:18.1, 244:17.8, 245:18.2
- **Kontext danach:** 247:18.0, 248:18.2, 249:18.0

### Frame 247

- **frame_ms:** 17.972
- **stream_ms / apply / unload:** 17.960 / 13.500 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 244:17.8, 245:18.2, 246:18.0
- **Kontext danach:** 248:18.2, 249:18.0, 250:17.8

### Frame 248

- **frame_ms:** 18.171
- **stream_ms / apply / unload:** 18.159 / 13.646 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 245:18.2, 246:18.0, 247:18.0
- **Kontext danach:** 249:18.0, 250:17.8, 251:17.9

### Frame 249

- **frame_ms:** 17.953
- **stream_ms / apply / unload:** 17.941 / 13.346 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 246:18.0, 247:18.0, 248:18.2
- **Kontext danach:** 250:17.8, 251:17.9, 252:17.7

### Frame 250

- **frame_ms:** 17.827
- **stream_ms / apply / unload:** 17.815 / 13.329 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 247:18.0, 248:18.2, 249:18.0
- **Kontext danach:** 251:17.9, 252:17.7, 253:17.7

### Frame 251

- **frame_ms:** 17.938
- **stream_ms / apply / unload:** 17.926 / 13.494 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 248:18.2, 249:18.0, 250:17.8
- **Kontext danach:** 252:17.7, 253:17.7, 254:17.5

### Frame 252

- **frame_ms:** 17.742
- **stream_ms / apply / unload:** 17.731 / 13.528 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 249:18.0, 250:17.8, 251:17.9
- **Kontext danach:** 253:17.7, 254:17.5, 255:17.7

### Frame 253

- **frame_ms:** 17.651
- **stream_ms / apply / unload:** 17.639 / 13.173 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 250:17.8, 251:17.9, 252:17.7
- **Kontext danach:** 254:17.5, 255:17.7, 256:18.2

### Frame 254

- **frame_ms:** 17.522
- **stream_ms / apply / unload:** 17.511 / 12.965 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 251:17.9, 252:17.7, 253:17.7
- **Kontext danach:** 255:17.7, 256:18.2, 257:18.1

### Frame 255

- **frame_ms:** 17.686
- **stream_ms / apply / unload:** 17.675 / 13.206 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 252:17.7, 253:17.7, 254:17.5
- **Kontext danach:** 256:18.2, 257:18.1, 258:17.8

### Frame 256

- **frame_ms:** 18.219
- **stream_ms / apply / unload:** 18.204 / 13.557 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 253:17.7, 254:17.5, 255:17.7
- **Kontext danach:** 257:18.1, 258:17.8, 259:17.5

### Frame 257

- **frame_ms:** 18.075
- **stream_ms / apply / unload:** 18.064 / 13.666 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 254:17.5, 255:17.7, 256:18.2
- **Kontext danach:** 258:17.8, 259:17.5, 260:17.5

### Frame 258

- **frame_ms:** 17.800
- **stream_ms / apply / unload:** 17.789 / 13.138 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 255:17.7, 256:18.2, 257:18.1
- **Kontext danach:** 259:17.5, 260:17.5, 261:17.7

### Frame 259

- **frame_ms:** 17.511
- **stream_ms / apply / unload:** 17.499 / 13.016 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 256:18.2, 257:18.1, 258:17.8
- **Kontext danach:** 260:17.5, 261:17.7, 262:18.0

### Frame 260

- **frame_ms:** 17.469
- **stream_ms / apply / unload:** 17.458 / 13.032 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 257:18.1, 258:17.8, 259:17.5
- **Kontext danach:** 261:17.7, 262:18.0, 263:17.8

### Frame 261

- **frame_ms:** 17.657
- **stream_ms / apply / unload:** 17.644 / 13.397 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 258:17.8, 259:17.5, 260:17.5
- **Kontext danach:** 262:18.0, 263:17.8, 264:18.1

### Frame 262

- **frame_ms:** 17.994
- **stream_ms / apply / unload:** 17.982 / 13.583 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 259:17.5, 260:17.5, 261:17.7
- **Kontext danach:** 263:17.8, 264:18.1, 265:18.4

### Frame 263

- **frame_ms:** 17.754
- **stream_ms / apply / unload:** 17.743 / 13.167 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 260:17.5, 261:17.7, 262:18.0
- **Kontext danach:** 264:18.1, 265:18.4, 266:17.7

### Frame 264

- **frame_ms:** 18.132
- **stream_ms / apply / unload:** 18.121 / 13.517 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 261:17.7, 262:18.0, 263:17.8
- **Kontext danach:** 265:18.4, 266:17.7, 267:17.8

### Frame 265

- **frame_ms:** 18.370
- **stream_ms / apply / unload:** 18.359 / 13.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 262:18.0, 263:17.8, 264:18.1
- **Kontext danach:** 266:17.7, 267:17.8, 268:17.6

### Frame 266

- **frame_ms:** 17.697
- **stream_ms / apply / unload:** 17.686 / 13.307 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 263:17.8, 264:18.1, 265:18.4
- **Kontext danach:** 267:17.8, 268:17.6, 269:18.3

### Frame 267

- **frame_ms:** 17.840
- **stream_ms / apply / unload:** 17.829 / 13.377 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 264:18.1, 265:18.4, 266:17.7
- **Kontext danach:** 268:17.6, 269:18.3, 270:17.6

### Frame 268

- **frame_ms:** 17.606
- **stream_ms / apply / unload:** 17.594 / 13.070 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 265:18.4, 266:17.7, 267:17.8
- **Kontext danach:** 269:18.3, 270:17.6, 271:17.8

### Frame 269

- **frame_ms:** 18.286
- **stream_ms / apply / unload:** 18.274 / 13.531 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 266:17.7, 267:17.8, 268:17.6
- **Kontext danach:** 270:17.6, 271:17.8, 272:17.6

### Frame 270

- **frame_ms:** 17.574
- **stream_ms / apply / unload:** 17.563 / 13.416 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 267:17.8, 268:17.6, 269:18.3
- **Kontext danach:** 271:17.8, 272:17.6, 273:17.7

### Frame 271

- **frame_ms:** 17.766
- **stream_ms / apply / unload:** 17.754 / 13.317 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 268:17.6, 269:18.3, 270:17.6
- **Kontext danach:** 272:17.6, 273:17.7, 274:18.1

### Frame 272

- **frame_ms:** 17.646
- **stream_ms / apply / unload:** 17.628 / 13.159 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 269:18.3, 270:17.6, 271:17.8
- **Kontext danach:** 273:17.7, 274:18.1, 275:17.9

### Frame 273

- **frame_ms:** 17.733
- **stream_ms / apply / unload:** 17.722 / 13.190 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 270:17.6, 271:17.8, 272:17.6
- **Kontext danach:** 274:18.1, 275:17.9, 276:17.8

### Frame 274

- **frame_ms:** 18.127
- **stream_ms / apply / unload:** 18.116 / 13.707 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 271:17.8, 272:17.6, 273:17.7
- **Kontext danach:** 275:17.9, 276:17.8, 277:18.1

### Frame 275

- **frame_ms:** 17.924
- **stream_ms / apply / unload:** 17.912 / 13.539 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 272:17.6, 273:17.7, 274:18.1
- **Kontext danach:** 276:17.8, 277:18.1, 278:18.0

### Frame 276

- **frame_ms:** 17.821
- **stream_ms / apply / unload:** 17.810 / 13.338 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 273:17.7, 274:18.1, 275:17.9
- **Kontext danach:** 277:18.1, 278:18.0, 279:18.0

### Frame 277

- **frame_ms:** 18.149
- **stream_ms / apply / unload:** 18.138 / 13.589 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 274:18.1, 275:17.9, 276:17.8
- **Kontext danach:** 278:18.0, 279:18.0, 280:17.7

### Frame 278

- **frame_ms:** 17.979
- **stream_ms / apply / unload:** 17.968 / 13.405 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 275:17.9, 276:17.8, 277:18.1
- **Kontext danach:** 279:18.0, 280:17.7, 281:17.9

### Frame 279

- **frame_ms:** 17.960
- **stream_ms / apply / unload:** 17.949 / 13.586 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 276:17.8, 277:18.1, 278:18.0
- **Kontext danach:** 280:17.7, 281:17.9, 282:17.8

### Frame 280

- **frame_ms:** 17.651
- **stream_ms / apply / unload:** 17.640 / 13.156 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 277:18.1, 278:18.0, 279:18.0
- **Kontext danach:** 281:17.9, 282:17.8, 283:17.4

### Frame 281

- **frame_ms:** 17.911
- **stream_ms / apply / unload:** 17.901 / 13.371 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 278:18.0, 279:18.0, 280:17.7
- **Kontext danach:** 282:17.8, 283:17.4, 284:18.0

### Frame 282

- **frame_ms:** 17.829
- **stream_ms / apply / unload:** 17.818 / 13.201 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 279:18.0, 280:17.7, 281:17.9
- **Kontext danach:** 283:17.4, 284:18.0, 285:17.8

### Frame 283

- **frame_ms:** 17.414
- **stream_ms / apply / unload:** 17.402 / 13.051 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 280:17.7, 281:17.9, 282:17.8
- **Kontext danach:** 284:18.0, 285:17.8, 286:17.4

### Frame 284

- **frame_ms:** 17.951
- **stream_ms / apply / unload:** 17.937 / 13.624 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 281:17.9, 282:17.8, 283:17.4
- **Kontext danach:** 285:17.8, 286:17.4, 287:17.1

### Frame 285

- **frame_ms:** 17.848
- **stream_ms / apply / unload:** 17.836 / 13.249 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 282:17.8, 283:17.4, 284:18.0
- **Kontext danach:** 286:17.4, 287:17.1, 288:17.6

### Frame 286

- **frame_ms:** 17.360
- **stream_ms / apply / unload:** 17.349 / 13.047 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 283:17.4, 284:18.0, 285:17.8
- **Kontext danach:** 287:17.1, 288:17.6, 289:17.1

### Frame 287

- **frame_ms:** 17.145
- **stream_ms / apply / unload:** 17.134 / 12.778 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 284:18.0, 285:17.8, 286:17.4
- **Kontext danach:** 288:17.6, 289:17.1, 290:17.9

### Frame 288

- **frame_ms:** 17.585
- **stream_ms / apply / unload:** 17.575 / 13.206 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 285:17.8, 286:17.4, 287:17.1
- **Kontext danach:** 289:17.1, 290:17.9, 291:18.5

### Frame 289

- **frame_ms:** 17.139
- **stream_ms / apply / unload:** 17.127 / 12.650 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 286:17.4, 287:17.1, 288:17.6
- **Kontext danach:** 290:17.9, 291:18.5, 292:17.2

### Frame 290

- **frame_ms:** 17.906
- **stream_ms / apply / unload:** 17.894 / 13.575 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 287:17.1, 288:17.6, 289:17.1
- **Kontext danach:** 291:18.5, 292:17.2, 293:17.4

### Frame 291

- **frame_ms:** 18.527
- **stream_ms / apply / unload:** 18.515 / 14.058 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 288:17.6, 289:17.1, 290:17.9
- **Kontext danach:** 292:17.2, 293:17.4, 294:17.8

### Frame 292

- **frame_ms:** 17.240
- **stream_ms / apply / unload:** 17.228 / 12.997 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 289:17.1, 290:17.9, 291:18.5
- **Kontext danach:** 293:17.4, 294:17.8, 295:18.5

### Frame 293

- **frame_ms:** 17.423
- **stream_ms / apply / unload:** 17.412 / 13.067 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 290:17.9, 291:18.5, 292:17.2
- **Kontext danach:** 294:17.8, 295:18.5, 296:17.8

### Frame 294

- **frame_ms:** 17.813
- **stream_ms / apply / unload:** 17.801 / 13.270 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 291:18.5, 292:17.2, 293:17.4
- **Kontext danach:** 295:18.5, 296:17.8, 297:17.7

### Frame 295

- **frame_ms:** 18.469
- **stream_ms / apply / unload:** 18.457 / 13.913 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 292:17.2, 293:17.4, 294:17.8
- **Kontext danach:** 296:17.8, 297:17.7, 298:17.8

### Frame 296

- **frame_ms:** 17.834
- **stream_ms / apply / unload:** 17.822 / 13.335 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 293:17.4, 294:17.8, 295:18.5
- **Kontext danach:** 297:17.7, 298:17.8, 299:17.8

### Frame 297

- **frame_ms:** 17.710
- **stream_ms / apply / unload:** 17.699 / 13.312 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 294:17.8, 295:18.5, 296:17.8
- **Kontext danach:** 298:17.8, 299:17.8

### Frame 298

- **frame_ms:** 17.790
- **stream_ms / apply / unload:** 17.763 / 13.297 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 295:18.5, 296:17.8, 297:17.7
- **Kontext danach:** 299:17.8

### Frame 299

- **frame_ms:** 17.762
- **stream_ms / apply / unload:** 17.750 / 13.273 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 296:17.8, 297:17.7, 298:17.8

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 18.086 | 17.790 | 19.930 | 29.307 |
| stream_ms | 18.074 | 17.779 | 19.919 | 29.295 |
| stream_apply_ms | 13.571 | 13.338 | 15.162 | 22.704 |
| stream_unload_ms | 0.005 | 0.005 | 0.006 | 0.013 |
| stream_loaded | 0.047 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 15.127 | 16.000 | 16.000 | 16.000 |
| zoom | 0.350 | 0.350 | 0.350 | 0.350 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 18.097 | 17.802 | 19.940 | 29.317 |
| cpu_unattributed_ms | 0.011 | 0.010 | 0.013 | 0.072 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=1.000, n=300): Pearson r=1.000 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_apply_ms** (r=0.968, n=300): Pearson r=0.968 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unload_ms** (r=-0.075, n=300): Pearson r=-0.075 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_loaded** (r=0.357, n=300): Pearson r=0.357 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=-0.613, n=300): Pearson r=-0.613 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ zoom** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ stream_ms** (r=1.000, n=300): Pearson r=1.000 (stark) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 1/300 Frames (0.3%).
- stream_unloaded am Unload-Cap (2): 0/300 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 1/300 (0.3%).
- Hitchs mit stream_unloaded am Cap: 0/300 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/300 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: apply_dominant (Load-/Apply-dominant) in 300/300 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 99.9%, Apply 75.0%, Unload 0.0%, Extract 0.0%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Häufigstes Hitch-Muster: periodic_cluster (300×).

## Offene Fragen

- Keine Extract-Metriken — Extract-Anteil nicht quantifizierbar.
