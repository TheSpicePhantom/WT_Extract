# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260713T194934Z_steady_unknown`
- **scenario_id:** `steady`
- **run_mode:** `cli`
- **recorded_frames:** 300
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-13T19:49:43.524400+00:00
- **git_commit:** unknown

### Config-Fingerprints

- `profiling`: `1882321295579174239`
- `streaming`: `8534220285179978824`
- `visibility_lod`: `-8339274955832645338`
- `world_gen`: `4083826086791026578`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 23.5864 | 23.5864 | +0.0000 | OK |
| frame_ms_p95 | 31.9319 | 31.9319 | +0.0000 | OK |
| frame_ms_max | 43.4747 | 43.4747 | +0.0000 | OK |
| stream_ms_mean | 19.8288 | 19.8288 | +0.0000 | OK |
| stream_ms_p95 | 27.7976 | 27.7976 | +0.0000 | OK |
| stream_ms_max | 41.4462 | 41.4462 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0064 | 0.0064 | +0.0000 | OK |
| stream_unload_ms_max | 0.0090 | 0.0090 | +0.0000 | OK |
| chunk_count_mean | 15.3067 | 15.3067 | +0.0000 | OK |
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
   - In 299/300 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 84.1% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_apply_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 63.0% an frame_ms.

4. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `frame_slow`: 300
- `stream_slow`: 300
- `load_burst`: 1

### Frame 0

- **frame_ms:** 32.080
- **stream_ms / apply / unload:** 29.759 / 22.241 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:31.4, 2:35.4, 3:35.8

### Frame 1

- **frame_ms:** 31.437
- **stream_ms / apply / unload:** 29.112 / 21.807 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:32.1
- **Kontext danach:** 2:35.4, 3:35.8, 4:26.7

### Frame 2

- **frame_ms:** 35.439
- **stream_ms / apply / unload:** 33.118 / 24.277 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:32.1, 1:31.4
- **Kontext danach:** 3:35.8, 4:26.7, 5:33.1

### Frame 3

- **frame_ms:** 35.762
- **stream_ms / apply / unload:** 33.153 / 25.324 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:32.1, 1:31.4, 2:35.4
- **Kontext danach:** 4:26.7, 5:33.1, 6:23.1

### Frame 4

- **frame_ms:** 26.705
- **stream_ms / apply / unload:** 24.132 / 15.672 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:31.4, 2:35.4, 3:35.8
- **Kontext danach:** 5:33.1, 6:23.1, 7:33.7

### Frame 5

- **frame_ms:** 33.087
- **stream_ms / apply / unload:** 31.555 / 23.361 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:35.4, 3:35.8, 4:26.7
- **Kontext danach:** 6:23.1, 7:33.7, 8:22.4

### Frame 6

- **frame_ms:** 23.070
- **stream_ms / apply / unload:** 21.838 / 17.421 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:35.8, 4:26.7, 5:33.1
- **Kontext danach:** 7:33.7, 8:22.4, 9:31.8

### Frame 7

- **frame_ms:** 33.656
- **stream_ms / apply / unload:** 31.084 / 24.828 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:26.7, 5:33.1, 6:23.1
- **Kontext danach:** 8:22.4, 9:31.8, 10:25.8

### Frame 8

- **frame_ms:** 22.408
- **stream_ms / apply / unload:** 19.876 / 14.332 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:33.1, 6:23.1, 7:33.7
- **Kontext danach:** 9:31.8, 10:25.8, 11:27.0

### Frame 9

- **frame_ms:** 31.815
- **stream_ms / apply / unload:** 29.294 / 20.877 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:23.1, 7:33.7, 8:22.4
- **Kontext danach:** 10:25.8, 11:27.0, 12:32.6

### Frame 10

- **frame_ms:** 25.789
- **stream_ms / apply / unload:** 24.571 / 16.137 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:33.7, 8:22.4, 9:31.8
- **Kontext danach:** 11:27.0, 12:32.6, 13:33.9

### Frame 11

- **frame_ms:** 26.997
- **stream_ms / apply / unload:** 24.894 / 19.756 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:22.4, 9:31.8, 10:25.8
- **Kontext danach:** 12:32.6, 13:33.9, 14:34.8

### Frame 12

- **frame_ms:** 32.565
- **stream_ms / apply / unload:** 31.356 / 22.097 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:31.8, 10:25.8, 11:27.0
- **Kontext danach:** 13:33.9, 14:34.8, 15:32.5

### Frame 13

- **frame_ms:** 33.902
- **stream_ms / apply / unload:** 31.404 / 24.216 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:25.8, 11:27.0, 12:32.6
- **Kontext danach:** 14:34.8, 15:32.5, 16:43.5

### Frame 14

- **frame_ms:** 34.799
- **stream_ms / apply / unload:** 32.471 / 24.095 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:27.0, 12:32.6, 13:33.9
- **Kontext danach:** 15:32.5, 16:43.5, 17:26.9

### Frame 15

- **frame_ms:** 32.478
- **stream_ms / apply / unload:** 31.265 / 23.963 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:32.6, 13:33.9, 14:34.8
- **Kontext danach:** 16:43.5, 17:26.9, 18:23.8

### Frame 16

- **frame_ms:** 43.475
- **stream_ms / apply / unload:** 41.446 / 37.107 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 10 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 85.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:33.9, 14:34.8, 15:32.5
- **Kontext danach:** 17:26.9, 18:23.8, 19:24.3

### Frame 17

- **frame_ms:** 26.872
- **stream_ms / apply / unload:** 24.924 / 20.056 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 10 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:34.8, 15:32.5, 16:43.5
- **Kontext danach:** 18:23.8, 19:24.3, 20:28.4

### Frame 18

- **frame_ms:** 23.850
- **stream_ms / apply / unload:** 20.903 / 14.777 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:32.5, 16:43.5, 17:26.9
- **Kontext danach:** 19:24.3, 20:28.4, 21:21.3

### Frame 19

- **frame_ms:** 24.257
- **stream_ms / apply / unload:** 20.645 / 16.327 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:43.5, 17:26.9, 18:23.8
- **Kontext danach:** 20:28.4, 21:21.3, 22:26.6

### Frame 20

- **frame_ms:** 28.364
- **stream_ms / apply / unload:** 24.463 / 19.918 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 17:26.9, 18:23.8, 19:24.3
- **Kontext danach:** 21:21.3, 22:26.6, 23:23.0

### Frame 21

- **frame_ms:** 21.270
- **stream_ms / apply / unload:** 17.787 / 13.248 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 18:23.8, 19:24.3, 20:28.4
- **Kontext danach:** 22:26.6, 23:23.0, 24:22.6

### Frame 22

- **frame_ms:** 26.633
- **stream_ms / apply / unload:** 22.862 / 16.697 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 19:24.3, 20:28.4, 21:21.3
- **Kontext danach:** 23:23.0, 24:22.6, 25:26.5

### Frame 23

- **frame_ms:** 22.984
- **stream_ms / apply / unload:** 19.173 / 14.550 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 20:28.4, 21:21.3, 22:26.6
- **Kontext danach:** 24:22.6, 25:26.5, 26:23.9

### Frame 24

- **frame_ms:** 22.641
- **stream_ms / apply / unload:** 18.920 / 14.042 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 21:21.3, 22:26.6, 23:23.0
- **Kontext danach:** 25:26.5, 26:23.9, 27:32.1

### Frame 25

- **frame_ms:** 26.539
- **stream_ms / apply / unload:** 19.914 / 15.026 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 22:26.6, 23:23.0, 24:22.6
- **Kontext danach:** 26:23.9, 27:32.1, 28:28.4

### Frame 26

- **frame_ms:** 23.877
- **stream_ms / apply / unload:** 20.362 / 13.577 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 23:23.0, 24:22.6, 25:26.5
- **Kontext danach:** 27:32.1, 28:28.4, 29:22.6

### Frame 27

- **frame_ms:** 32.118
- **stream_ms / apply / unload:** 28.602 / 22.798 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 24:22.6, 25:26.5, 26:23.9
- **Kontext danach:** 28:28.4, 29:22.6, 30:22.4

### Frame 28

- **frame_ms:** 28.413
- **stream_ms / apply / unload:** 23.873 / 17.228 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:26.5, 26:23.9, 27:32.1
- **Kontext danach:** 29:22.6, 30:22.4, 31:27.4

### Frame 29

- **frame_ms:** 22.613
- **stream_ms / apply / unload:** 18.829 / 13.647 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:23.9, 27:32.1, 28:28.4
- **Kontext danach:** 30:22.4, 31:27.4, 32:20.5

### Frame 30

- **frame_ms:** 22.350
- **stream_ms / apply / unload:** 18.530 / 13.909 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 27:32.1, 28:28.4, 29:22.6
- **Kontext danach:** 31:27.4, 32:20.5, 33:27.7

### Frame 31

- **frame_ms:** 27.426
- **stream_ms / apply / unload:** 21.764 / 17.180 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 28:28.4, 29:22.6, 30:22.4
- **Kontext danach:** 32:20.5, 33:27.7, 34:21.4

### Frame 32

- **frame_ms:** 20.452
- **stream_ms / apply / unload:** 16.974 / 12.635 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 29:22.6, 30:22.4, 31:27.4
- **Kontext danach:** 33:27.7, 34:21.4, 35:25.3

### Frame 33

- **frame_ms:** 27.687
- **stream_ms / apply / unload:** 24.087 / 19.252 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:22.4, 31:27.4, 32:20.5
- **Kontext danach:** 34:21.4, 35:25.3, 36:20.8

### Frame 34

- **frame_ms:** 21.445
- **stream_ms / apply / unload:** 17.882 / 13.429 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 31:27.4, 32:20.5, 33:27.7
- **Kontext danach:** 35:25.3, 36:20.8, 37:25.3

### Frame 35

- **frame_ms:** 25.321
- **stream_ms / apply / unload:** 21.787 / 17.389 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:20.5, 33:27.7, 34:21.4
- **Kontext danach:** 36:20.8, 37:25.3, 38:27.3

### Frame 36

- **frame_ms:** 20.823
- **stream_ms / apply / unload:** 17.355 / 12.831 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:27.7, 34:21.4, 35:25.3
- **Kontext danach:** 37:25.3, 38:27.3, 39:27.8

### Frame 37

- **frame_ms:** 25.256
- **stream_ms / apply / unload:** 21.735 / 17.475 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 34:21.4, 35:25.3, 36:20.8
- **Kontext danach:** 38:27.3, 39:27.8, 40:22.5

### Frame 38

- **frame_ms:** 27.300
- **stream_ms / apply / unload:** 20.876 / 16.471 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 35:25.3, 36:20.8, 37:25.3
- **Kontext danach:** 39:27.8, 40:22.5, 41:32.7

### Frame 39

- **frame_ms:** 27.779
- **stream_ms / apply / unload:** 24.270 / 18.719 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 36:20.8, 37:25.3, 38:27.3
- **Kontext danach:** 40:22.5, 41:32.7, 42:23.7

### Frame 40

- **frame_ms:** 22.526
- **stream_ms / apply / unload:** 18.736 / 13.943 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 37:25.3, 38:27.3, 39:27.8
- **Kontext danach:** 41:32.7, 42:23.7, 43:26.9

### Frame 41

- **frame_ms:** 32.691
- **stream_ms / apply / unload:** 25.732 / 19.254 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 38:27.3, 39:27.8, 40:22.5
- **Kontext danach:** 42:23.7, 43:26.9, 44:28.1

### Frame 42

- **frame_ms:** 23.661
- **stream_ms / apply / unload:** 20.095 / 12.925 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 39:27.8, 40:22.5, 41:32.7
- **Kontext danach:** 43:26.9, 44:28.1, 45:29.8

### Frame 43

- **frame_ms:** 26.930
- **stream_ms / apply / unload:** 20.302 / 15.998 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 40:22.5, 41:32.7, 42:23.7
- **Kontext danach:** 44:28.1, 45:29.8, 46:21.1

### Frame 44

- **frame_ms:** 28.100
- **stream_ms / apply / unload:** 24.606 / 17.412 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 41:32.7, 42:23.7, 43:26.9
- **Kontext danach:** 45:29.8, 46:21.1, 47:27.0

### Frame 45

- **frame_ms:** 29.757
- **stream_ms / apply / unload:** 26.209 / 18.858 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 42:23.7, 43:26.9, 44:28.1
- **Kontext danach:** 46:21.1, 47:27.0, 48:27.3

### Frame 46

- **frame_ms:** 21.067
- **stream_ms / apply / unload:** 17.595 / 13.304 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 43:26.9, 44:28.1, 45:29.8
- **Kontext danach:** 47:27.0, 48:27.3, 49:32.5

### Frame 47

- **frame_ms:** 27.025
- **stream_ms / apply / unload:** 23.030 / 18.743 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 44:28.1, 45:29.8, 46:21.1
- **Kontext danach:** 48:27.3, 49:32.5, 50:31.6

### Frame 48

- **frame_ms:** 27.330
- **stream_ms / apply / unload:** 23.645 / 15.554 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 45:29.8, 46:21.1, 47:27.0
- **Kontext danach:** 49:32.5, 50:31.6, 51:22.8

### Frame 49

- **frame_ms:** 32.481
- **stream_ms / apply / unload:** 25.829 / 20.936 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 46:21.1, 47:27.0, 48:27.3
- **Kontext danach:** 50:31.6, 51:22.8, 52:22.0

### Frame 50

- **frame_ms:** 31.564
- **stream_ms / apply / unload:** 27.798 / 20.355 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 47:27.0, 48:27.3, 49:32.5
- **Kontext danach:** 51:22.8, 52:22.0, 53:21.7

### Frame 51

- **frame_ms:** 22.802
- **stream_ms / apply / unload:** 18.553 / 14.152 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 48:27.3, 49:32.5, 50:31.6
- **Kontext danach:** 52:22.0, 53:21.7, 54:20.4

### Frame 52

- **frame_ms:** 21.999
- **stream_ms / apply / unload:** 18.247 / 13.370 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 49:32.5, 50:31.6, 51:22.8
- **Kontext danach:** 53:21.7, 54:20.4, 55:21.1

### Frame 53

- **frame_ms:** 21.685
- **stream_ms / apply / unload:** 18.206 / 13.262 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 50:31.6, 51:22.8, 52:22.0
- **Kontext danach:** 54:20.4, 55:21.1, 56:22.7

### Frame 54

- **frame_ms:** 20.353
- **stream_ms / apply / unload:** 16.913 / 12.523 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 51:22.8, 52:22.0, 53:21.7
- **Kontext danach:** 55:21.1, 56:22.7, 57:25.8

### Frame 55

- **frame_ms:** 21.060
- **stream_ms / apply / unload:** 17.598 / 13.016 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 52:22.0, 53:21.7, 54:20.4
- **Kontext danach:** 56:22.7, 57:25.8, 58:31.7

### Frame 56

- **frame_ms:** 22.702
- **stream_ms / apply / unload:** 19.227 / 14.866 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 53:21.7, 54:20.4, 55:21.1
- **Kontext danach:** 57:25.8, 58:31.7, 59:21.2

### Frame 57

- **frame_ms:** 25.842
- **stream_ms / apply / unload:** 21.292 / 12.802 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 54:20.4, 55:21.1, 56:22.7
- **Kontext danach:** 58:31.7, 59:21.2, 60:27.4

### Frame 58

- **frame_ms:** 31.677
- **stream_ms / apply / unload:** 27.449 / 20.064 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 55:21.1, 56:22.7, 57:25.8
- **Kontext danach:** 59:21.2, 60:27.4, 61:29.3

### Frame 59

- **frame_ms:** 21.157
- **stream_ms / apply / unload:** 17.673 / 13.231 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 56:22.7, 57:25.8, 58:31.7
- **Kontext danach:** 60:27.4, 61:29.3, 62:21.7

### Frame 60

- **frame_ms:** 27.362
- **stream_ms / apply / unload:** 20.721 / 15.747 / 0.006
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
- **Kontext davor:** 57:25.8, 58:31.7, 59:21.2
- **Kontext danach:** 61:29.3, 62:21.7, 63:22.6

### Frame 61

- **frame_ms:** 29.297
- **stream_ms / apply / unload:** 25.443 / 18.341 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 58:31.7, 59:21.2, 60:27.4
- **Kontext danach:** 62:21.7, 63:22.6, 64:25.9

### Frame 62

- **frame_ms:** 21.661
- **stream_ms / apply / unload:** 18.156 / 13.395 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 59:21.2, 60:27.4, 61:29.3
- **Kontext danach:** 63:22.6, 64:25.9, 65:25.1

### Frame 63

- **frame_ms:** 22.577
- **stream_ms / apply / unload:** 18.985 / 14.527 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 60:27.4, 61:29.3, 62:21.7
- **Kontext danach:** 64:25.9, 65:25.1, 66:21.9

### Frame 64

- **frame_ms:** 25.879
- **stream_ms / apply / unload:** 19.299 / 15.028 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 61:29.3, 62:21.7, 63:22.6
- **Kontext danach:** 65:25.1, 66:21.9, 67:21.6

### Frame 65

- **frame_ms:** 25.114
- **stream_ms / apply / unload:** 21.521 / 14.240 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 62:21.7, 63:22.6, 64:25.9
- **Kontext danach:** 66:21.9, 67:21.6, 68:21.3

### Frame 66

- **frame_ms:** 21.930
- **stream_ms / apply / unload:** 18.463 / 13.859 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 63:22.6, 64:25.9, 65:25.1
- **Kontext danach:** 67:21.6, 68:21.3, 69:20.5

### Frame 67

- **frame_ms:** 21.550
- **stream_ms / apply / unload:** 18.103 / 13.183 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 64:25.9, 65:25.1, 66:21.9
- **Kontext danach:** 68:21.3, 69:20.5, 70:21.5

### Frame 68

- **frame_ms:** 21.263
- **stream_ms / apply / unload:** 17.769 / 13.411 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 65:25.1, 66:21.9, 67:21.6
- **Kontext danach:** 69:20.5, 70:21.5, 71:21.4

### Frame 69

- **frame_ms:** 20.535
- **stream_ms / apply / unload:** 17.085 / 12.672 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 66:21.9, 67:21.6, 68:21.3
- **Kontext danach:** 70:21.5, 71:21.4, 72:21.1

### Frame 70

- **frame_ms:** 21.451
- **stream_ms / apply / unload:** 17.929 / 13.400 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 67:21.6, 68:21.3, 69:20.5
- **Kontext danach:** 71:21.4, 72:21.1, 73:21.9

### Frame 71

- **frame_ms:** 21.356
- **stream_ms / apply / unload:** 17.535 / 12.756 / 0.006
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
- **Kontext davor:** 68:21.3, 69:20.5, 70:21.5
- **Kontext danach:** 72:21.1, 73:21.9, 74:20.8

### Frame 72

- **frame_ms:** 21.066
- **stream_ms / apply / unload:** 17.549 / 13.109 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 69:20.5, 70:21.5, 71:21.4
- **Kontext danach:** 73:21.9, 74:20.8, 75:22.8

### Frame 73

- **frame_ms:** 21.897
- **stream_ms / apply / unload:** 18.083 / 13.797 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 70:21.5, 71:21.4, 72:21.1
- **Kontext danach:** 74:20.8, 75:22.8, 76:28.0

### Frame 74

- **frame_ms:** 20.848
- **stream_ms / apply / unload:** 17.420 / 13.073 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 71:21.4, 72:21.1, 73:21.9
- **Kontext danach:** 75:22.8, 76:28.0, 77:24.2

### Frame 75

- **frame_ms:** 22.814
- **stream_ms / apply / unload:** 19.352 / 13.008 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 72:21.1, 73:21.9, 74:20.8
- **Kontext danach:** 76:28.0, 77:24.2, 78:22.0

### Frame 76

- **frame_ms:** 27.952
- **stream_ms / apply / unload:** 21.379 / 17.053 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 73:21.9, 74:20.8, 75:22.8
- **Kontext danach:** 77:24.2, 78:22.0, 79:22.8

### Frame 77

- **frame_ms:** 24.169
- **stream_ms / apply / unload:** 20.329 / 14.190 / 0.005
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
- **Kontext davor:** 74:20.8, 75:22.8, 76:28.0
- **Kontext danach:** 78:22.0, 79:22.8, 80:28.1

### Frame 78

- **frame_ms:** 21.972
- **stream_ms / apply / unload:** 18.030 / 13.615 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 75:22.8, 76:28.0, 77:24.2
- **Kontext danach:** 79:22.8, 80:28.1, 81:23.8

### Frame 79

- **frame_ms:** 22.756
- **stream_ms / apply / unload:** 18.892 / 13.331 / 0.005
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
- **Kontext davor:** 76:28.0, 77:24.2, 78:22.0
- **Kontext danach:** 80:28.1, 81:23.8, 82:21.5

### Frame 80

- **frame_ms:** 28.057
- **stream_ms / apply / unload:** 21.464 / 16.376 / 0.006
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
- **Kontext davor:** 77:24.2, 78:22.0, 79:22.8
- **Kontext danach:** 81:23.8, 82:21.5, 83:29.9

### Frame 81

- **frame_ms:** 23.775
- **stream_ms / apply / unload:** 19.434 / 13.617 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 78:22.0, 79:22.8, 80:28.1
- **Kontext danach:** 82:21.5, 83:29.9, 84:21.7

### Frame 82

- **frame_ms:** 21.546
- **stream_ms / apply / unload:** 18.054 / 13.100 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 79:22.8, 80:28.1, 81:23.8
- **Kontext danach:** 83:29.9, 84:21.7, 85:20.8

### Frame 83

- **frame_ms:** 29.851
- **stream_ms / apply / unload:** 26.363 / 21.342 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 80:28.1, 81:23.8, 82:21.5
- **Kontext danach:** 84:21.7, 85:20.8, 86:21.5

### Frame 84

- **frame_ms:** 21.659
- **stream_ms / apply / unload:** 18.194 / 13.863 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 81:23.8, 82:21.5, 83:29.9
- **Kontext danach:** 85:20.8, 86:21.5, 87:23.2

### Frame 85

- **frame_ms:** 20.829
- **stream_ms / apply / unload:** 17.327 / 12.588 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 82:21.5, 83:29.9, 84:21.7
- **Kontext danach:** 86:21.5, 87:23.2, 88:22.5

### Frame 86

- **frame_ms:** 21.470
- **stream_ms / apply / unload:** 17.755 / 12.887 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 83:29.9, 84:21.7, 85:20.8
- **Kontext danach:** 87:23.2, 88:22.5, 89:21.7

### Frame 87

- **frame_ms:** 23.225
- **stream_ms / apply / unload:** 18.836 / 14.204 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 84:21.7, 85:20.8, 86:21.5
- **Kontext danach:** 88:22.5, 89:21.7, 90:22.1

### Frame 88

- **frame_ms:** 22.477
- **stream_ms / apply / unload:** 19.053 / 13.927 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 85:20.8, 86:21.5, 87:23.2
- **Kontext danach:** 89:21.7, 90:22.1, 91:21.7

### Frame 89

- **frame_ms:** 21.678
- **stream_ms / apply / unload:** 18.209 / 12.766 / 0.005
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
- **Kontext davor:** 86:21.5, 87:23.2, 88:22.5
- **Kontext danach:** 90:22.1, 91:21.7, 92:25.9

### Frame 90

- **frame_ms:** 22.113
- **stream_ms / apply / unload:** 18.631 / 14.025 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 87:23.2, 88:22.5, 89:21.7
- **Kontext danach:** 91:21.7, 92:25.9, 93:22.8

### Frame 91

- **frame_ms:** 21.707
- **stream_ms / apply / unload:** 18.003 / 13.438 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 88:22.5, 89:21.7, 90:22.1
- **Kontext danach:** 92:25.9, 93:22.8, 94:22.2

### Frame 92

- **frame_ms:** 25.918
- **stream_ms / apply / unload:** 22.263 / 15.958 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 89:21.7, 90:22.1, 91:21.7
- **Kontext danach:** 93:22.8, 94:22.2, 95:25.4

### Frame 93

- **frame_ms:** 22.826
- **stream_ms / apply / unload:** 19.022 / 14.510 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 90:22.1, 91:21.7, 92:25.9
- **Kontext danach:** 94:22.2, 95:25.4, 96:21.1

### Frame 94

- **frame_ms:** 22.151
- **stream_ms / apply / unload:** 17.624 / 13.092 / 0.005
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
- **Kontext davor:** 91:21.7, 92:25.9, 93:22.8
- **Kontext danach:** 95:25.4, 96:21.1, 97:22.0

### Frame 95

- **frame_ms:** 25.397
- **stream_ms / apply / unload:** 21.919 / 14.614 / 0.005
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
- **Kontext davor:** 92:25.9, 93:22.8, 94:22.2
- **Kontext danach:** 96:21.1, 97:22.0, 98:23.3

### Frame 96

- **frame_ms:** 21.140
- **stream_ms / apply / unload:** 17.711 / 13.134 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 93:22.8, 94:22.2, 95:25.4
- **Kontext danach:** 97:22.0, 98:23.3, 99:21.1

### Frame 97

- **frame_ms:** 21.955
- **stream_ms / apply / unload:** 17.721 / 13.400 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 94:22.2, 95:25.4, 96:21.1
- **Kontext danach:** 98:23.3, 99:21.1, 100:22.6

### Frame 98

- **frame_ms:** 23.268
- **stream_ms / apply / unload:** 19.574 / 13.686 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 95:25.4, 96:21.1, 97:22.0
- **Kontext danach:** 99:21.1, 100:22.6, 101:22.1

### Frame 99

- **frame_ms:** 21.117
- **stream_ms / apply / unload:** 17.481 / 12.985 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 96:21.1, 97:22.0, 98:23.3
- **Kontext danach:** 100:22.6, 101:22.1, 102:21.2

### Frame 100

- **frame_ms:** 22.630
- **stream_ms / apply / unload:** 16.841 / 12.577 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 97:22.0, 98:23.3, 99:21.1
- **Kontext danach:** 101:22.1, 102:21.2, 103:20.5

### Frame 101

- **frame_ms:** 22.138
- **stream_ms / apply / unload:** 18.692 / 12.700 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 98:23.3, 99:21.1, 100:22.6
- **Kontext danach:** 102:21.2, 103:20.5, 104:20.7

### Frame 102

- **frame_ms:** 21.207
- **stream_ms / apply / unload:** 17.715 / 13.495 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 99:21.1, 100:22.6, 101:22.1
- **Kontext danach:** 103:20.5, 104:20.7, 105:26.2

### Frame 103

- **frame_ms:** 20.517
- **stream_ms / apply / unload:** 16.668 / 12.400 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 100:22.6, 101:22.1, 102:21.2
- **Kontext danach:** 104:20.7, 105:26.2, 106:21.5

### Frame 104

- **frame_ms:** 20.676
- **stream_ms / apply / unload:** 17.224 / 12.780 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 101:22.1, 102:21.2, 103:20.5
- **Kontext danach:** 105:26.2, 106:21.5, 107:20.7

### Frame 105

- **frame_ms:** 26.160
- **stream_ms / apply / unload:** 22.181 / 17.923 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 102:21.2, 103:20.5, 104:20.7
- **Kontext danach:** 106:21.5, 107:20.7, 108:22.0

### Frame 106

- **frame_ms:** 21.505
- **stream_ms / apply / unload:** 17.604 / 12.890 / 0.005
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
- **Kontext davor:** 103:20.5, 104:20.7, 105:26.2
- **Kontext danach:** 107:20.7, 108:22.0, 109:21.9

### Frame 107

- **frame_ms:** 20.706
- **stream_ms / apply / unload:** 17.175 / 12.611 / 0.005
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
- **Kontext davor:** 104:20.7, 105:26.2, 106:21.5
- **Kontext danach:** 108:22.0, 109:21.9, 110:20.9

### Frame 108

- **frame_ms:** 22.046
- **stream_ms / apply / unload:** 18.551 / 14.053 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 105:26.2, 106:21.5, 107:20.7
- **Kontext danach:** 109:21.9, 110:20.9, 111:27.9

### Frame 109

- **frame_ms:** 21.858
- **stream_ms / apply / unload:** 17.988 / 13.280 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 106:21.5, 107:20.7, 108:22.0
- **Kontext danach:** 110:20.9, 111:27.9, 112:22.5

### Frame 110

- **frame_ms:** 20.930
- **stream_ms / apply / unload:** 17.371 / 12.905 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 107:20.7, 108:22.0, 109:21.9
- **Kontext danach:** 111:27.9, 112:22.5, 113:20.7

### Frame 111

- **frame_ms:** 27.916
- **stream_ms / apply / unload:** 24.193 / 19.707 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 108:22.0, 109:21.9, 110:20.9
- **Kontext danach:** 112:22.5, 113:20.7, 114:23.1

### Frame 112

- **frame_ms:** 22.524
- **stream_ms / apply / unload:** 19.057 / 14.509 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 109:21.9, 110:20.9, 111:27.9
- **Kontext danach:** 113:20.7, 114:23.1, 115:21.0

### Frame 113

- **frame_ms:** 20.667
- **stream_ms / apply / unload:** 17.201 / 12.803 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 110:20.9, 111:27.9, 112:22.5
- **Kontext danach:** 114:23.1, 115:21.0, 116:20.7

### Frame 114

- **frame_ms:** 23.057
- **stream_ms / apply / unload:** 19.585 / 14.750 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 111:27.9, 112:22.5, 113:20.7
- **Kontext danach:** 115:21.0, 116:20.7, 117:20.3

### Frame 115

- **frame_ms:** 21.020
- **stream_ms / apply / unload:** 17.550 / 13.239 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 112:22.5, 113:20.7, 114:23.1
- **Kontext danach:** 116:20.7, 117:20.3, 118:20.2

### Frame 116

- **frame_ms:** 20.672
- **stream_ms / apply / unload:** 17.232 / 12.876 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 113:20.7, 114:23.1, 115:21.0
- **Kontext danach:** 117:20.3, 118:20.2, 119:21.5

### Frame 117

- **frame_ms:** 20.331
- **stream_ms / apply / unload:** 16.871 / 12.626 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 114:23.1, 115:21.0, 116:20.7
- **Kontext danach:** 118:20.2, 119:21.5, 120:22.5

### Frame 118

- **frame_ms:** 20.234
- **stream_ms / apply / unload:** 16.658 / 12.464 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 115:21.0, 116:20.7, 117:20.3
- **Kontext danach:** 119:21.5, 120:22.5, 121:22.5

### Frame 119

- **frame_ms:** 21.544
- **stream_ms / apply / unload:** 18.069 / 12.664 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 116:20.7, 117:20.3, 118:20.2
- **Kontext danach:** 120:22.5, 121:22.5, 122:22.6

### Frame 120

- **frame_ms:** 22.469
- **stream_ms / apply / unload:** 18.649 / 14.242 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 117:20.3, 118:20.2, 119:21.5
- **Kontext danach:** 121:22.5, 122:22.6, 123:21.2

### Frame 121

- **frame_ms:** 22.539
- **stream_ms / apply / unload:** 18.407 / 13.708 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 118:20.2, 119:21.5, 120:22.5
- **Kontext danach:** 122:22.6, 123:21.2, 124:20.3

### Frame 122

- **frame_ms:** 22.552
- **stream_ms / apply / unload:** 17.714 / 12.897 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 119:21.5, 120:22.5, 121:22.5
- **Kontext danach:** 123:21.2, 124:20.3, 125:21.5

### Frame 123

- **frame_ms:** 21.228
- **stream_ms / apply / unload:** 17.700 / 13.408 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 120:22.5, 121:22.5, 122:22.6
- **Kontext danach:** 124:20.3, 125:21.5, 126:21.7

### Frame 124

- **frame_ms:** 20.301
- **stream_ms / apply / unload:** 16.844 / 12.469 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 121:22.5, 122:22.6, 123:21.2
- **Kontext danach:** 125:21.5, 126:21.7, 127:22.0

### Frame 125

- **frame_ms:** 21.544
- **stream_ms / apply / unload:** 18.003 / 13.326 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 122:22.6, 123:21.2, 124:20.3
- **Kontext danach:** 126:21.7, 127:22.0, 128:22.3

### Frame 126

- **frame_ms:** 21.686
- **stream_ms / apply / unload:** 17.923 / 13.710 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 123:21.2, 124:20.3, 125:21.5
- **Kontext danach:** 127:22.0, 128:22.3, 129:21.8

### Frame 127

- **frame_ms:** 22.019
- **stream_ms / apply / unload:** 18.093 / 13.675 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 124:20.3, 125:21.5, 126:21.7
- **Kontext danach:** 128:22.3, 129:21.8, 130:20.8

### Frame 128

- **frame_ms:** 22.330
- **stream_ms / apply / unload:** 18.724 / 14.430 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 125:21.5, 126:21.7, 127:22.0
- **Kontext danach:** 129:21.8, 130:20.8, 131:22.5

### Frame 129

- **frame_ms:** 21.836
- **stream_ms / apply / unload:** 18.339 / 14.020 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 126:21.7, 127:22.0, 128:22.3
- **Kontext danach:** 130:20.8, 131:22.5, 132:20.9

### Frame 130

- **frame_ms:** 20.835
- **stream_ms / apply / unload:** 17.379 / 12.998 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 127:22.0, 128:22.3, 129:21.8
- **Kontext danach:** 131:22.5, 132:20.9, 133:21.1

### Frame 131

- **frame_ms:** 22.532
- **stream_ms / apply / unload:** 19.021 / 14.307 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 128:22.3, 129:21.8, 130:20.8
- **Kontext danach:** 132:20.9, 133:21.1, 134:22.0

### Frame 132

- **frame_ms:** 20.939
- **stream_ms / apply / unload:** 17.316 / 13.006 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 129:21.8, 130:20.8, 131:22.5
- **Kontext danach:** 133:21.1, 134:22.0, 135:20.6

### Frame 133

- **frame_ms:** 21.056
- **stream_ms / apply / unload:** 17.560 / 12.999 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 130:20.8, 131:22.5, 132:20.9
- **Kontext danach:** 134:22.0, 135:20.6, 136:21.6

### Frame 134

- **frame_ms:** 21.951
- **stream_ms / apply / unload:** 18.098 / 13.287 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 131:22.5, 132:20.9, 133:21.1
- **Kontext danach:** 135:20.6, 136:21.6, 137:28.4

### Frame 135

- **frame_ms:** 20.561
- **stream_ms / apply / unload:** 16.892 / 12.598 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 132:20.9, 133:21.1, 134:22.0
- **Kontext danach:** 136:21.6, 137:28.4, 138:23.2

### Frame 136

- **frame_ms:** 21.625
- **stream_ms / apply / unload:** 18.093 / 13.681 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 133:21.1, 134:22.0, 135:20.6
- **Kontext danach:** 137:28.4, 138:23.2, 139:22.3

### Frame 137

- **frame_ms:** 28.391
- **stream_ms / apply / unload:** 22.839 / 17.657 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 134:22.0, 135:20.6, 136:21.6
- **Kontext danach:** 138:23.2, 139:22.3, 140:22.6

### Frame 138

- **frame_ms:** 23.224
- **stream_ms / apply / unload:** 18.728 / 13.944 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 135:20.6, 136:21.6, 137:28.4
- **Kontext danach:** 139:22.3, 140:22.6, 141:21.8

### Frame 139

- **frame_ms:** 22.271
- **stream_ms / apply / unload:** 18.604 / 13.584 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 136:21.6, 137:28.4, 138:23.2
- **Kontext danach:** 140:22.6, 141:21.8, 142:20.5

### Frame 140

- **frame_ms:** 22.622
- **stream_ms / apply / unload:** 18.664 / 13.577 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 137:28.4, 138:23.2, 139:22.3
- **Kontext danach:** 141:21.8, 142:20.5, 143:20.3

### Frame 141

- **frame_ms:** 21.785
- **stream_ms / apply / unload:** 18.332 / 13.549 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 138:23.2, 139:22.3, 140:22.6
- **Kontext danach:** 142:20.5, 143:20.3, 144:20.6

### Frame 142

- **frame_ms:** 20.483
- **stream_ms / apply / unload:** 17.036 / 12.663 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 139:22.3, 140:22.6, 141:21.8
- **Kontext danach:** 143:20.3, 144:20.6, 145:22.4

### Frame 143

- **frame_ms:** 20.335
- **stream_ms / apply / unload:** 16.870 / 12.653 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 140:22.6, 141:21.8, 142:20.5
- **Kontext danach:** 144:20.6, 145:22.4, 146:28.6

### Frame 144

- **frame_ms:** 20.631
- **stream_ms / apply / unload:** 16.804 / 12.558 / 0.005
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
- **Kontext davor:** 141:21.8, 142:20.5, 143:20.3
- **Kontext danach:** 145:22.4, 146:28.6, 147:21.2

### Frame 145

- **frame_ms:** 22.409
- **stream_ms / apply / unload:** 18.514 / 13.535 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 142:20.5, 143:20.3, 144:20.6
- **Kontext danach:** 146:28.6, 147:21.2, 148:22.2

### Frame 146

- **frame_ms:** 28.648
- **stream_ms / apply / unload:** 25.176 / 19.867 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 143:20.3, 144:20.6, 145:22.4
- **Kontext danach:** 147:21.2, 148:22.2, 149:25.2

### Frame 147

- **frame_ms:** 21.238
- **stream_ms / apply / unload:** 17.716 / 13.382 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 144:20.6, 145:22.4, 146:28.6
- **Kontext danach:** 148:22.2, 149:25.2, 150:21.6

### Frame 148

- **frame_ms:** 22.221
- **stream_ms / apply / unload:** 17.799 / 13.161 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 145:22.4, 146:28.6, 147:21.2
- **Kontext danach:** 149:25.2, 150:21.6, 151:20.5

### Frame 149

- **frame_ms:** 25.157
- **stream_ms / apply / unload:** 21.590 / 15.796 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 146:28.6, 147:21.2, 148:22.2
- **Kontext danach:** 150:21.6, 151:20.5, 152:20.7

### Frame 150

- **frame_ms:** 21.586
- **stream_ms / apply / unload:** 18.136 / 13.492 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 147:21.2, 148:22.2, 149:25.2
- **Kontext danach:** 151:20.5, 152:20.7, 153:21.5

### Frame 151

- **frame_ms:** 20.517
- **stream_ms / apply / unload:** 16.837 / 12.591 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 148:22.2, 149:25.2, 150:21.6
- **Kontext danach:** 152:20.7, 153:21.5, 154:20.9

### Frame 152

- **frame_ms:** 20.719
- **stream_ms / apply / unload:** 17.263 / 12.666 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 149:25.2, 150:21.6, 151:20.5
- **Kontext danach:** 153:21.5, 154:20.9, 155:21.8

### Frame 153

- **frame_ms:** 21.475
- **stream_ms / apply / unload:** 17.558 / 12.987 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 150:21.6, 151:20.5, 152:20.7
- **Kontext danach:** 154:20.9, 155:21.8, 156:22.2

### Frame 154

- **frame_ms:** 20.938
- **stream_ms / apply / unload:** 17.418 / 12.998 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 151:20.5, 152:20.7, 153:21.5
- **Kontext danach:** 155:21.8, 156:22.2, 157:20.9

### Frame 155

- **frame_ms:** 21.796
- **stream_ms / apply / unload:** 18.312 / 14.031 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 152:20.7, 153:21.5, 154:20.9
- **Kontext danach:** 156:22.2, 157:20.9, 158:24.9

### Frame 156

- **frame_ms:** 22.206
- **stream_ms / apply / unload:** 18.695 / 13.983 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 153:21.5, 154:20.9, 155:21.8
- **Kontext danach:** 157:20.9, 158:24.9, 159:23.3

### Frame 157

- **frame_ms:** 20.923
- **stream_ms / apply / unload:** 17.458 / 13.063 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 154:20.9, 155:21.8, 156:22.2
- **Kontext danach:** 158:24.9, 159:23.3, 160:29.2

### Frame 158

- **frame_ms:** 24.943
- **stream_ms / apply / unload:** 20.328 / 15.989 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 155:21.8, 156:22.2, 157:20.9
- **Kontext danach:** 159:23.3, 160:29.2, 161:23.4

### Frame 159

- **frame_ms:** 23.252
- **stream_ms / apply / unload:** 19.637 / 15.350 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 156:22.2, 157:20.9, 158:24.9
- **Kontext danach:** 160:29.2, 161:23.4, 162:26.7

### Frame 160

- **frame_ms:** 29.231
- **stream_ms / apply / unload:** 22.690 / 18.368 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 157:20.9, 158:24.9, 159:23.3
- **Kontext danach:** 161:23.4, 162:26.7, 163:21.4

### Frame 161

- **frame_ms:** 23.385
- **stream_ms / apply / unload:** 19.855 / 13.312 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 158:24.9, 159:23.3, 160:29.2
- **Kontext danach:** 162:26.7, 163:21.4, 164:26.0

### Frame 162

- **frame_ms:** 26.679
- **stream_ms / apply / unload:** 23.024 / 18.042 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 159:23.3, 160:29.2, 161:23.4
- **Kontext danach:** 163:21.4, 164:26.0, 165:21.8

### Frame 163

- **frame_ms:** 21.354
- **stream_ms / apply / unload:** 17.794 / 13.417 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 160:29.2, 161:23.4, 162:26.7
- **Kontext danach:** 164:26.0, 165:21.8, 166:22.4

### Frame 164

- **frame_ms:** 25.976
- **stream_ms / apply / unload:** 22.021 / 16.493 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 161:23.4, 162:26.7, 163:21.4
- **Kontext danach:** 165:21.8, 166:22.4, 167:28.2

### Frame 165

- **frame_ms:** 21.796
- **stream_ms / apply / unload:** 17.914 / 13.487 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 162:26.7, 163:21.4, 164:26.0
- **Kontext danach:** 166:22.4, 167:28.2, 168:22.5

### Frame 166

- **frame_ms:** 22.442
- **stream_ms / apply / unload:** 18.932 / 14.700 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 163:21.4, 164:26.0, 165:21.8
- **Kontext danach:** 167:28.2, 168:22.5, 169:34.7

### Frame 167

- **frame_ms:** 28.165
- **stream_ms / apply / unload:** 24.412 / 20.143 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 164:26.0, 165:21.8, 166:22.4
- **Kontext danach:** 168:22.5, 169:34.7, 170:31.9

### Frame 168

- **frame_ms:** 22.504
- **stream_ms / apply / unload:** 18.919 / 13.843 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 165:21.8, 166:22.4, 167:28.2
- **Kontext danach:** 169:34.7, 170:31.9, 171:27.5

### Frame 169

- **frame_ms:** 34.673
- **stream_ms / apply / unload:** 28.085 / 21.157 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 166:22.4, 167:28.2, 168:22.5
- **Kontext danach:** 170:31.9, 171:27.5, 172:22.5

### Frame 170

- **frame_ms:** 31.932
- **stream_ms / apply / unload:** 25.285 / 19.553 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 167:28.2, 168:22.5, 169:34.7
- **Kontext danach:** 171:27.5, 172:22.5, 173:22.3

### Frame 171

- **frame_ms:** 27.455
- **stream_ms / apply / unload:** 21.791 / 15.411 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 168:22.5, 169:34.7, 170:31.9
- **Kontext danach:** 172:22.5, 173:22.3, 174:22.6

### Frame 172

- **frame_ms:** 22.512
- **stream_ms / apply / unload:** 18.688 / 13.872 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 169:34.7, 170:31.9, 171:27.5
- **Kontext danach:** 173:22.3, 174:22.6, 175:22.2

### Frame 173

- **frame_ms:** 22.250
- **stream_ms / apply / unload:** 18.240 / 13.612 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 170:31.9, 171:27.5, 172:22.5
- **Kontext danach:** 174:22.6, 175:22.2, 176:20.5

### Frame 174

- **frame_ms:** 22.628
- **stream_ms / apply / unload:** 18.812 / 14.183 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 171:27.5, 172:22.5, 173:22.3
- **Kontext danach:** 175:22.2, 176:20.5, 177:27.2

### Frame 175

- **frame_ms:** 22.242
- **stream_ms / apply / unload:** 18.783 / 13.277 / 0.005
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
- **Kontext davor:** 172:22.5, 173:22.3, 174:22.6
- **Kontext danach:** 176:20.5, 177:27.2, 178:24.0

### Frame 176

- **frame_ms:** 20.477
- **stream_ms / apply / unload:** 16.839 / 12.523 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 173:22.3, 174:22.6, 175:22.2
- **Kontext danach:** 177:27.2, 178:24.0, 179:22.3

### Frame 177

- **frame_ms:** 27.182
- **stream_ms / apply / unload:** 23.723 / 19.345 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 174:22.6, 175:22.2, 176:20.5
- **Kontext danach:** 178:24.0, 179:22.3, 180:21.3

### Frame 178

- **frame_ms:** 23.996
- **stream_ms / apply / unload:** 20.411 / 15.863 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 175:22.2, 176:20.5, 177:27.2
- **Kontext danach:** 179:22.3, 180:21.3, 181:26.4

### Frame 179

- **frame_ms:** 22.307
- **stream_ms / apply / unload:** 18.063 / 13.765 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 176:20.5, 177:27.2, 178:24.0
- **Kontext danach:** 180:21.3, 181:26.4, 182:22.5

### Frame 180

- **frame_ms:** 21.309
- **stream_ms / apply / unload:** 17.868 / 13.205 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 177:27.2, 178:24.0, 179:22.3
- **Kontext danach:** 181:26.4, 182:22.5, 183:22.7

### Frame 181

- **frame_ms:** 26.442
- **stream_ms / apply / unload:** 22.879 / 17.934 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 178:24.0, 179:22.3, 180:21.3
- **Kontext danach:** 182:22.5, 183:22.7, 184:20.5

### Frame 182

- **frame_ms:** 22.489
- **stream_ms / apply / unload:** 18.998 / 14.739 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 179:22.3, 180:21.3, 181:26.4
- **Kontext danach:** 183:22.7, 184:20.5, 185:20.4

### Frame 183

- **frame_ms:** 22.717
- **stream_ms / apply / unload:** 18.966 / 14.075 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 180:21.3, 181:26.4, 182:22.5
- **Kontext danach:** 184:20.5, 185:20.4, 186:20.3

### Frame 184

- **frame_ms:** 20.492
- **stream_ms / apply / unload:** 17.048 / 12.585 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 181:26.4, 182:22.5, 183:22.7
- **Kontext danach:** 185:20.4, 186:20.3, 187:20.9

### Frame 185

- **frame_ms:** 20.376
- **stream_ms / apply / unload:** 16.903 / 12.601 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 182:22.5, 183:22.7, 184:20.5
- **Kontext danach:** 186:20.3, 187:20.9, 188:22.3

### Frame 186

- **frame_ms:** 20.324
- **stream_ms / apply / unload:** 16.863 / 12.441 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 183:22.7, 184:20.5, 185:20.4
- **Kontext danach:** 187:20.9, 188:22.3, 189:22.4

### Frame 187

- **frame_ms:** 20.941
- **stream_ms / apply / unload:** 17.439 / 13.117 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 184:20.5, 185:20.4, 186:20.3
- **Kontext danach:** 188:22.3, 189:22.4, 190:22.3

### Frame 188

- **frame_ms:** 22.300
- **stream_ms / apply / unload:** 18.822 / 14.005 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 185:20.4, 186:20.3, 187:20.9
- **Kontext danach:** 189:22.4, 190:22.3, 191:21.0

### Frame 189

- **frame_ms:** 22.368
- **stream_ms / apply / unload:** 18.884 / 14.292 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 186:20.3, 187:20.9, 188:22.3
- **Kontext danach:** 190:22.3, 191:21.0, 192:22.8

### Frame 190

- **frame_ms:** 22.316
- **stream_ms / apply / unload:** 18.840 / 14.474 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 187:20.9, 188:22.3, 189:22.4
- **Kontext danach:** 191:21.0, 192:22.8, 193:28.1

### Frame 191

- **frame_ms:** 20.973
- **stream_ms / apply / unload:** 17.478 / 12.850 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 188:22.3, 189:22.4, 190:22.3
- **Kontext danach:** 192:22.8, 193:28.1, 194:21.2

### Frame 192

- **frame_ms:** 22.816
- **stream_ms / apply / unload:** 19.358 / 13.834 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 189:22.4, 190:22.3, 191:21.0
- **Kontext danach:** 193:28.1, 194:21.2, 195:20.5

### Frame 193

- **frame_ms:** 28.078
- **stream_ms / apply / unload:** 24.606 / 19.887 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 190:22.3, 191:21.0, 192:22.8
- **Kontext danach:** 194:21.2, 195:20.5, 196:26.7

### Frame 194

- **frame_ms:** 21.245
- **stream_ms / apply / unload:** 17.538 / 13.247 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 191:21.0, 192:22.8, 193:28.1
- **Kontext danach:** 195:20.5, 196:26.7, 197:23.1

### Frame 195

- **frame_ms:** 20.484
- **stream_ms / apply / unload:** 16.987 / 12.636 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 192:22.8, 193:28.1, 194:21.2
- **Kontext danach:** 196:26.7, 197:23.1, 198:26.7

### Frame 196

- **frame_ms:** 26.678
- **stream_ms / apply / unload:** 23.167 / 18.201 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 193:28.1, 194:21.2, 195:20.5
- **Kontext danach:** 197:23.1, 198:26.7, 199:20.4

### Frame 197

- **frame_ms:** 23.110
- **stream_ms / apply / unload:** 19.589 / 15.249 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 194:21.2, 195:20.5, 196:26.7
- **Kontext danach:** 198:26.7, 199:20.4, 200:23.1

### Frame 198

- **frame_ms:** 26.743
- **stream_ms / apply / unload:** 23.243 / 18.911 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 195:20.5, 196:26.7, 197:23.1
- **Kontext danach:** 199:20.4, 200:23.1, 201:21.4

### Frame 199

- **frame_ms:** 20.428
- **stream_ms / apply / unload:** 16.961 / 12.603 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 196:26.7, 197:23.1, 198:26.7
- **Kontext danach:** 200:23.1, 201:21.4, 202:22.0

### Frame 200

- **frame_ms:** 23.083
- **stream_ms / apply / unload:** 19.545 / 15.048 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 197:23.1, 198:26.7, 199:20.4
- **Kontext danach:** 201:21.4, 202:22.0, 203:21.5

### Frame 201

- **frame_ms:** 21.436
- **stream_ms / apply / unload:** 17.845 / 13.317 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 198:26.7, 199:20.4, 200:23.1
- **Kontext danach:** 202:22.0, 203:21.5, 204:21.5

### Frame 202

- **frame_ms:** 22.024
- **stream_ms / apply / unload:** 18.600 / 14.209 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 199:20.4, 200:23.1, 201:21.4
- **Kontext danach:** 203:21.5, 204:21.5, 205:22.4

### Frame 203

- **frame_ms:** 21.522
- **stream_ms / apply / unload:** 18.013 / 13.699 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 200:23.1, 201:21.4, 202:22.0
- **Kontext danach:** 204:21.5, 205:22.4, 206:21.4

### Frame 204

- **frame_ms:** 21.451
- **stream_ms / apply / unload:** 17.442 / 12.612 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 201:21.4, 202:22.0, 203:21.5
- **Kontext danach:** 205:22.4, 206:21.4, 207:23.9

### Frame 205

- **frame_ms:** 22.428
- **stream_ms / apply / unload:** 18.902 / 13.955 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 202:22.0, 203:21.5, 204:21.5
- **Kontext danach:** 206:21.4, 207:23.9, 208:21.3

### Frame 206

- **frame_ms:** 21.409
- **stream_ms / apply / unload:** 17.678 / 13.274 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 203:21.5, 204:21.5, 205:22.4
- **Kontext danach:** 207:23.9, 208:21.3, 209:22.6

### Frame 207

- **frame_ms:** 23.924
- **stream_ms / apply / unload:** 20.416 / 14.273 / 0.005
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
- **Kontext davor:** 204:21.5, 205:22.4, 206:21.4
- **Kontext danach:** 208:21.3, 209:22.6, 210:21.9

### Frame 208

- **frame_ms:** 21.337
- **stream_ms / apply / unload:** 17.717 / 13.164 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 205:22.4, 206:21.4, 207:23.9
- **Kontext danach:** 209:22.6, 210:21.9, 211:21.2

### Frame 209

- **frame_ms:** 22.625
- **stream_ms / apply / unload:** 19.186 / 14.496 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 206:21.4, 207:23.9, 208:21.3
- **Kontext danach:** 210:21.9, 211:21.2, 212:23.2

### Frame 210

- **frame_ms:** 21.929
- **stream_ms / apply / unload:** 18.379 / 13.292 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 207:23.9, 208:21.3, 209:22.6
- **Kontext danach:** 211:21.2, 212:23.2, 213:22.2

### Frame 211

- **frame_ms:** 21.231
- **stream_ms / apply / unload:** 17.361 / 12.800 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 208:21.3, 209:22.6, 210:21.9
- **Kontext danach:** 212:23.2, 213:22.2, 214:20.9

### Frame 212

- **frame_ms:** 23.187
- **stream_ms / apply / unload:** 19.413 / 14.953 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 209:22.6, 210:21.9, 211:21.2
- **Kontext danach:** 213:22.2, 214:20.9, 215:24.3

### Frame 213

- **frame_ms:** 22.211
- **stream_ms / apply / unload:** 18.727 / 14.275 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 210:21.9, 211:21.2, 212:23.2
- **Kontext danach:** 214:20.9, 215:24.3, 216:26.8

### Frame 214

- **frame_ms:** 20.926
- **stream_ms / apply / unload:** 17.369 / 12.707 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 211:21.2, 212:23.2, 213:22.2
- **Kontext danach:** 215:24.3, 216:26.8, 217:21.9

### Frame 215

- **frame_ms:** 24.257
- **stream_ms / apply / unload:** 20.732 / 16.390 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 212:23.2, 213:22.2, 214:20.9
- **Kontext danach:** 216:26.8, 217:21.9, 218:23.5

### Frame 216

- **frame_ms:** 26.784
- **stream_ms / apply / unload:** 20.079 / 15.284 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 213:22.2, 214:20.9, 215:24.3
- **Kontext danach:** 217:21.9, 218:23.5, 219:24.2

### Frame 217

- **frame_ms:** 21.942
- **stream_ms / apply / unload:** 18.464 / 12.535 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 214:20.9, 215:24.3, 216:26.8
- **Kontext danach:** 218:23.5, 219:24.2, 220:21.0

### Frame 218

- **frame_ms:** 23.471
- **stream_ms / apply / unload:** 20.012 / 14.167 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 215:24.3, 216:26.8, 217:21.9
- **Kontext danach:** 219:24.2, 220:21.0, 221:22.7

### Frame 219

- **frame_ms:** 24.159
- **stream_ms / apply / unload:** 20.404 / 16.169 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 216:26.8, 217:21.9, 218:23.5
- **Kontext danach:** 220:21.0, 221:22.7, 222:21.1

### Frame 220

- **frame_ms:** 21.019
- **stream_ms / apply / unload:** 17.481 / 13.066 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 217:21.9, 218:23.5, 219:24.2
- **Kontext danach:** 221:22.7, 222:21.1, 223:21.5

### Frame 221

- **frame_ms:** 22.736
- **stream_ms / apply / unload:** 19.189 / 14.069 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 218:23.5, 219:24.2, 220:21.0
- **Kontext danach:** 222:21.1, 223:21.5, 224:22.3

### Frame 222

- **frame_ms:** 21.087
- **stream_ms / apply / unload:** 17.602 / 13.332 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 219:24.2, 220:21.0, 221:22.7
- **Kontext danach:** 223:21.5, 224:22.3, 225:21.5

### Frame 223

- **frame_ms:** 21.469
- **stream_ms / apply / unload:** 17.945 / 13.403 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 220:21.0, 221:22.7, 222:21.1
- **Kontext danach:** 224:22.3, 225:21.5, 226:20.7

### Frame 224

- **frame_ms:** 22.329
- **stream_ms / apply / unload:** 18.907 / 13.649 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 221:22.7, 222:21.1, 223:21.5
- **Kontext danach:** 225:21.5, 226:20.7, 227:23.0

### Frame 225

- **frame_ms:** 21.492
- **stream_ms / apply / unload:** 17.919 / 13.300 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 222:21.1, 223:21.5, 224:22.3
- **Kontext danach:** 226:20.7, 227:23.0, 228:25.4

### Frame 226

- **frame_ms:** 20.687
- **stream_ms / apply / unload:** 17.065 / 12.696 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 223:21.5, 224:22.3, 225:21.5
- **Kontext danach:** 227:23.0, 228:25.4, 229:21.3

### Frame 227

- **frame_ms:** 22.951
- **stream_ms / apply / unload:** 19.330 / 13.940 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 224:22.3, 225:21.5, 226:20.7
- **Kontext danach:** 228:25.4, 229:21.3, 230:23.1

### Frame 228

- **frame_ms:** 25.421
- **stream_ms / apply / unload:** 21.644 / 16.836 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 225:21.5, 226:20.7, 227:23.0
- **Kontext danach:** 229:21.3, 230:23.1, 231:22.7

### Frame 229

- **frame_ms:** 21.252
- **stream_ms / apply / unload:** 17.781 / 13.380 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 226:20.7, 227:23.0, 228:25.4
- **Kontext danach:** 230:23.1, 231:22.7, 232:21.7

### Frame 230

- **frame_ms:** 23.093
- **stream_ms / apply / unload:** 19.344 / 14.346 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 227:23.0, 228:25.4, 229:21.3
- **Kontext danach:** 231:22.7, 232:21.7, 233:21.2

### Frame 231

- **frame_ms:** 22.699
- **stream_ms / apply / unload:** 19.146 / 14.788 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 228:25.4, 229:21.3, 230:23.1
- **Kontext danach:** 232:21.7, 233:21.2, 234:20.7

### Frame 232

- **frame_ms:** 21.693
- **stream_ms / apply / unload:** 17.854 / 13.352 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 229:21.3, 230:23.1, 231:22.7
- **Kontext danach:** 233:21.2, 234:20.7, 235:20.5

### Frame 233

- **frame_ms:** 21.156
- **stream_ms / apply / unload:** 17.651 / 13.188 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 230:23.1, 231:22.7, 232:21.7
- **Kontext danach:** 234:20.7, 235:20.5, 236:21.0

### Frame 234

- **frame_ms:** 20.678
- **stream_ms / apply / unload:** 17.042 / 12.770 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 231:22.7, 232:21.7, 233:21.2
- **Kontext danach:** 235:20.5, 236:21.0, 237:25.6

### Frame 235

- **frame_ms:** 20.486
- **stream_ms / apply / unload:** 16.877 / 12.538 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 232:21.7, 233:21.2, 234:20.7
- **Kontext danach:** 236:21.0, 237:25.6, 238:33.3

### Frame 236

- **frame_ms:** 21.016
- **stream_ms / apply / unload:** 17.496 / 12.957 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 233:21.2, 234:20.7, 235:20.5
- **Kontext danach:** 237:25.6, 238:33.3, 239:20.8

### Frame 237

- **frame_ms:** 25.618
- **stream_ms / apply / unload:** 19.031 / 14.736 / 0.006
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
- **Kontext davor:** 234:20.7, 235:20.5, 236:21.0
- **Kontext danach:** 238:33.3, 239:20.8, 240:24.1

### Frame 238

- **frame_ms:** 33.345
- **stream_ms / apply / unload:** 28.076 / 20.862 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 235:20.5, 236:21.0, 237:25.6
- **Kontext danach:** 239:20.8, 240:24.1, 241:23.8

### Frame 239

- **frame_ms:** 20.797
- **stream_ms / apply / unload:** 16.906 / 12.527 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 236:21.0, 237:25.6, 238:33.3
- **Kontext danach:** 240:24.1, 241:23.8, 242:20.6

### Frame 240

- **frame_ms:** 24.104
- **stream_ms / apply / unload:** 20.165 / 14.506 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 237:25.6, 238:33.3, 239:20.8
- **Kontext danach:** 241:23.8, 242:20.6, 243:23.3

### Frame 241

- **frame_ms:** 23.777
- **stream_ms / apply / unload:** 20.312 / 13.357 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 238:33.3, 239:20.8, 240:24.1
- **Kontext danach:** 242:20.6, 243:23.3, 244:21.1

### Frame 242

- **frame_ms:** 20.632
- **stream_ms / apply / unload:** 17.132 / 12.855 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 239:20.8, 240:24.1, 241:23.8
- **Kontext danach:** 243:23.3, 244:21.1, 245:24.7

### Frame 243

- **frame_ms:** 23.313
- **stream_ms / apply / unload:** 19.818 / 14.214 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 240:24.1, 241:23.8, 242:20.6
- **Kontext danach:** 244:21.1, 245:24.7, 246:20.8

### Frame 244

- **frame_ms:** 21.113
- **stream_ms / apply / unload:** 17.605 / 13.347 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 241:23.8, 242:20.6, 243:23.3
- **Kontext danach:** 245:24.7, 246:20.8, 247:21.3

### Frame 245

- **frame_ms:** 24.678
- **stream_ms / apply / unload:** 21.071 / 16.598 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 242:20.6, 243:23.3, 244:21.1
- **Kontext danach:** 246:20.8, 247:21.3, 248:21.3

### Frame 246

- **frame_ms:** 20.848
- **stream_ms / apply / unload:** 17.299 / 12.763 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 243:23.3, 244:21.1, 245:24.7
- **Kontext danach:** 247:21.3, 248:21.3, 249:25.2

### Frame 247

- **frame_ms:** 21.309
- **stream_ms / apply / unload:** 17.733 / 13.355 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 244:21.1, 245:24.7, 246:20.8
- **Kontext danach:** 248:21.3, 249:25.2, 250:22.2

### Frame 248

- **frame_ms:** 21.315
- **stream_ms / apply / unload:** 17.339 / 12.876 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 245:24.7, 246:20.8, 247:21.3
- **Kontext danach:** 249:25.2, 250:22.2, 251:22.7

### Frame 249

- **frame_ms:** 25.165
- **stream_ms / apply / unload:** 18.525 / 13.109 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 246:20.8, 247:21.3, 248:21.3
- **Kontext danach:** 250:22.2, 251:22.7, 252:20.7

### Frame 250

- **frame_ms:** 22.179
- **stream_ms / apply / unload:** 18.533 / 13.647 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 247:21.3, 248:21.3, 249:25.2
- **Kontext danach:** 251:22.7, 252:20.7, 253:20.4

### Frame 251

- **frame_ms:** 22.681
- **stream_ms / apply / unload:** 18.744 / 14.021 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 248:21.3, 249:25.2, 250:22.2
- **Kontext danach:** 252:20.7, 253:20.4, 254:20.4

### Frame 252

- **frame_ms:** 20.724
- **stream_ms / apply / unload:** 17.210 / 12.713 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 249:25.2, 250:22.2, 251:22.7
- **Kontext danach:** 253:20.4, 254:20.4, 255:21.0

### Frame 253

- **frame_ms:** 20.353
- **stream_ms / apply / unload:** 16.862 / 12.593 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 250:22.2, 251:22.7, 252:20.7
- **Kontext danach:** 254:20.4, 255:21.0, 256:26.1

### Frame 254

- **frame_ms:** 20.352
- **stream_ms / apply / unload:** 16.866 / 12.608 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 251:22.7, 252:20.7, 253:20.4
- **Kontext danach:** 255:21.0, 256:26.1, 257:26.3

### Frame 255

- **frame_ms:** 21.011
- **stream_ms / apply / unload:** 17.533 / 13.032 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 252:20.7, 253:20.4, 254:20.4
- **Kontext danach:** 256:26.1, 257:26.3, 258:22.5

### Frame 256

- **frame_ms:** 26.104
- **stream_ms / apply / unload:** 19.426 / 15.001 / 0.006
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
- **Kontext davor:** 253:20.4, 254:20.4, 255:21.0
- **Kontext danach:** 257:26.3, 258:22.5, 259:29.8

### Frame 257

- **frame_ms:** 26.342
- **stream_ms / apply / unload:** 21.853 / 14.278 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 254:20.4, 255:21.0, 256:26.1
- **Kontext danach:** 258:22.5, 259:29.8, 260:24.4

### Frame 258

- **frame_ms:** 22.514
- **stream_ms / apply / unload:** 18.856 / 14.294 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 255:21.0, 256:26.1, 257:26.3
- **Kontext danach:** 259:29.8, 260:24.4, 261:21.3

### Frame 259

- **frame_ms:** 29.802
- **stream_ms / apply / unload:** 26.045 / 21.198 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 256:26.1, 257:26.3, 258:22.5
- **Kontext danach:** 260:24.4, 261:21.3, 262:25.4

### Frame 260

- **frame_ms:** 24.402
- **stream_ms / apply / unload:** 20.871 / 16.203 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 257:26.3, 258:22.5, 259:29.8
- **Kontext danach:** 261:21.3, 262:25.4, 263:29.1

### Frame 261

- **frame_ms:** 21.323
- **stream_ms / apply / unload:** 16.941 / 12.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 258:22.5, 259:29.8, 260:24.4
- **Kontext danach:** 262:25.4, 263:29.1, 264:22.7

### Frame 262

- **frame_ms:** 25.441
- **stream_ms / apply / unload:** 21.987 / 15.978 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 259:29.8, 260:24.4, 261:21.3
- **Kontext danach:** 263:29.1, 264:22.7, 265:21.8

### Frame 263

- **frame_ms:** 29.110
- **stream_ms / apply / unload:** 25.623 / 20.822 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 71.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 260:24.4, 261:21.3, 262:25.4
- **Kontext danach:** 264:22.7, 265:21.8, 266:26.2

### Frame 264

- **frame_ms:** 22.748
- **stream_ms / apply / unload:** 19.087 / 14.814 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 261:21.3, 262:25.4, 263:29.1
- **Kontext danach:** 265:21.8, 266:26.2, 267:20.4

### Frame 265

- **frame_ms:** 21.820
- **stream_ms / apply / unload:** 17.611 / 13.211 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 262:25.4, 263:29.1, 264:22.7
- **Kontext danach:** 266:26.2, 267:20.4, 268:20.5

### Frame 266

- **frame_ms:** 26.231
- **stream_ms / apply / unload:** 22.570 / 15.298 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 263:29.1, 264:22.7, 265:21.8
- **Kontext danach:** 267:20.4, 268:20.5, 269:21.6

### Frame 267

- **frame_ms:** 20.379
- **stream_ms / apply / unload:** 16.920 / 12.567 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 264:22.7, 265:21.8, 266:26.2
- **Kontext danach:** 268:20.5, 269:21.6, 270:22.4

### Frame 268

- **frame_ms:** 20.520
- **stream_ms / apply / unload:** 17.006 / 12.644 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 265:21.8, 266:26.2, 267:20.4
- **Kontext danach:** 269:21.6, 270:22.4, 271:20.4

### Frame 269

- **frame_ms:** 21.648
- **stream_ms / apply / unload:** 18.125 / 13.645 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 266:26.2, 267:20.4, 268:20.5
- **Kontext danach:** 270:22.4, 271:20.4, 272:20.5

### Frame 270

- **frame_ms:** 22.390
- **stream_ms / apply / unload:** 18.878 / 14.522 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 267:20.4, 268:20.5, 269:21.6
- **Kontext danach:** 271:20.4, 272:20.5, 273:21.8

### Frame 271

- **frame_ms:** 20.408
- **stream_ms / apply / unload:** 16.939 / 12.691 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 268:20.5, 269:21.6, 270:22.4
- **Kontext danach:** 272:20.5, 273:21.8, 274:20.6

### Frame 272

- **frame_ms:** 20.474
- **stream_ms / apply / unload:** 17.021 / 12.631 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 269:21.6, 270:22.4, 271:20.4
- **Kontext danach:** 273:21.8, 274:20.6, 275:22.7

### Frame 273

- **frame_ms:** 21.760
- **stream_ms / apply / unload:** 18.292 / 13.723 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 270:22.4, 271:20.4, 272:20.5
- **Kontext danach:** 274:20.6, 275:22.7, 276:23.7

### Frame 274

- **frame_ms:** 20.600
- **stream_ms / apply / unload:** 17.118 / 12.666 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 271:20.4, 272:20.5, 273:21.8
- **Kontext danach:** 275:22.7, 276:23.7, 277:20.8

### Frame 275

- **frame_ms:** 22.741
- **stream_ms / apply / unload:** 19.227 / 14.673 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 272:20.5, 273:21.8, 274:20.6
- **Kontext danach:** 276:23.7, 277:20.8, 278:21.1

### Frame 276

- **frame_ms:** 23.728
- **stream_ms / apply / unload:** 19.554 / 14.936 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 273:21.8, 274:20.6, 275:22.7
- **Kontext danach:** 277:20.8, 278:21.1, 279:20.6

### Frame 277

- **frame_ms:** 20.781
- **stream_ms / apply / unload:** 17.265 / 12.618 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 274:20.6, 275:22.7, 276:23.7
- **Kontext danach:** 278:21.1, 279:20.6, 280:20.5

### Frame 278

- **frame_ms:** 21.062
- **stream_ms / apply / unload:** 17.548 / 12.996 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 275:22.7, 276:23.7, 277:20.8
- **Kontext danach:** 279:20.6, 280:20.5, 281:20.9

### Frame 279

- **frame_ms:** 20.554
- **stream_ms / apply / unload:** 16.887 / 12.535 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 276:23.7, 277:20.8, 278:21.1
- **Kontext danach:** 280:20.5, 281:20.9, 282:23.4

### Frame 280

- **frame_ms:** 20.545
- **stream_ms / apply / unload:** 17.043 / 12.693 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 277:20.8, 278:21.1, 279:20.6
- **Kontext danach:** 281:20.9, 282:23.4, 283:21.8

### Frame 281

- **frame_ms:** 20.891
- **stream_ms / apply / unload:** 17.381 / 13.036 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 278:21.1, 279:20.6, 280:20.5
- **Kontext danach:** 282:23.4, 283:21.8, 284:21.9

### Frame 282

- **frame_ms:** 23.386
- **stream_ms / apply / unload:** 19.304 / 15.012 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 279:20.6, 280:20.5, 281:20.9
- **Kontext danach:** 283:21.8, 284:21.9, 285:21.9

### Frame 283

- **frame_ms:** 21.830
- **stream_ms / apply / unload:** 18.279 / 13.788 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 280:20.5, 281:20.9, 282:23.4
- **Kontext danach:** 284:21.9, 285:21.9, 286:21.4

### Frame 284

- **frame_ms:** 21.920
- **stream_ms / apply / unload:** 18.474 / 13.911 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 281:20.9, 282:23.4, 283:21.8
- **Kontext danach:** 285:21.9, 286:21.4, 287:21.2

### Frame 285

- **frame_ms:** 21.851
- **stream_ms / apply / unload:** 17.508 / 12.690 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 282:23.4, 283:21.8, 284:21.9
- **Kontext danach:** 286:21.4, 287:21.2, 288:20.3

### Frame 286

- **frame_ms:** 21.374
- **stream_ms / apply / unload:** 17.531 / 12.921 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 283:21.8, 284:21.9, 285:21.9
- **Kontext danach:** 287:21.2, 288:20.3, 289:24.1

### Frame 287

- **frame_ms:** 21.169
- **stream_ms / apply / unload:** 17.655 / 13.363 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 284:21.9, 285:21.9, 286:21.4
- **Kontext danach:** 288:20.3, 289:24.1, 290:24.8

### Frame 288

- **frame_ms:** 20.273
- **stream_ms / apply / unload:** 16.772 / 12.465 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 285:21.9, 286:21.4, 287:21.2
- **Kontext danach:** 289:24.1, 290:24.8, 291:27.2

### Frame 289

- **frame_ms:** 24.104
- **stream_ms / apply / unload:** 17.458 / 12.918 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 286:21.4, 287:21.2, 288:20.3
- **Kontext danach:** 290:24.8, 291:27.2, 292:20.7

### Frame 290

- **frame_ms:** 24.850
- **stream_ms / apply / unload:** 21.186 / 13.887 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 287:21.2, 288:20.3, 289:24.1
- **Kontext danach:** 291:27.2, 292:20.7, 293:23.1

### Frame 291

- **frame_ms:** 27.228
- **stream_ms / apply / unload:** 23.529 / 18.762 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 288:20.3, 289:24.1, 290:24.8
- **Kontext danach:** 292:20.7, 293:23.1, 294:23.0

### Frame 292

- **frame_ms:** 20.658
- **stream_ms / apply / unload:** 17.175 / 12.643 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 289:24.1, 290:24.8, 291:27.2
- **Kontext danach:** 293:23.1, 294:23.0, 295:22.0

### Frame 293

- **frame_ms:** 23.097
- **stream_ms / apply / unload:** 19.008 / 14.721 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 290:24.8, 291:27.2, 292:20.7
- **Kontext danach:** 294:23.0, 295:22.0, 296:21.3

### Frame 294

- **frame_ms:** 23.044
- **stream_ms / apply / unload:** 19.542 / 14.953 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 291:27.2, 292:20.7, 293:23.1
- **Kontext danach:** 295:22.0, 296:21.3, 297:20.9

### Frame 295

- **frame_ms:** 21.990
- **stream_ms / apply / unload:** 18.076 / 13.693 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 292:20.7, 293:23.1, 294:23.0
- **Kontext danach:** 296:21.3, 297:20.9, 298:20.5

### Frame 296

- **frame_ms:** 21.278
- **stream_ms / apply / unload:** 17.769 / 12.955 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 293:23.1, 294:23.0, 295:22.0
- **Kontext danach:** 297:20.9, 298:20.5, 299:20.6

### Frame 297

- **frame_ms:** 20.877
- **stream_ms / apply / unload:** 17.401 / 13.004 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 294:23.0, 295:22.0, 296:21.3
- **Kontext danach:** 298:20.5, 299:20.6

### Frame 298

- **frame_ms:** 20.484
- **stream_ms / apply / unload:** 16.984 / 12.572 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 295:22.0, 296:21.3, 297:20.9
- **Kontext danach:** 299:20.6

### Frame 299

- **frame_ms:** 20.610
- **stream_ms / apply / unload:** 17.134 / 12.959 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 296:21.3, 297:20.9, 298:20.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 23.586 | 22.329 | 31.932 | 43.475 |
| stream_ms | 19.829 | 18.604 | 27.798 | 41.446 |
| stream_apply_ms | 14.848 | 13.708 | 20.936 | 37.107 |
| stream_unload_ms | 0.005 | 0.005 | 0.006 | 0.009 |
| stream_loaded | 0.043 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 15.307 | 16.000 | 16.000 | 16.000 |
| zoom | 0.350 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 3.645 | 3.427 | 6.367 | 6.802 |
| tile_extract_ms | 0.097 | 0.090 | 0.150 | 0.279 |
| extract_ms | 3.742 | 3.519 | 6.524 | 6.938 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 23.599 | 22.340 | 31.947 | 43.485 |
| cpu_unattributed_ms | 0.012 | 0.012 | 0.016 | 0.038 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.969, n=300): Pearson r=0.969 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_apply_ms** (r=0.945, n=300): Pearson r=0.945 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unload_ms** (r=0.118, n=300): Pearson r=0.118 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_loaded** (r=0.190, n=300): Pearson r=0.190 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=-0.585, n=300): Pearson r=-0.585 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ zoom** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.099, n=300): Pearson r=0.099 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ tile_extract_ms** (r=0.147, n=300): Pearson r=0.147 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ extract_ms** (r=0.101, n=300): Pearson r=0.101 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **cpu_full_frame_ms ↔ stream_ms** (r=0.969, n=300): Pearson r=0.969 (stark) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.101, n=300): Pearson r=0.101 (vernachlässigbar) zwischen cpu_full_frame_ms und extract_ms.
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

- Hitch-Hauptursachen: apply_dominant (Load-/Apply-dominant) in 299/300 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 84.1%, Apply 63.0%, Unload 0.0%, Extract 15.9%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 16.1%.
- Häufigstes Hitch-Muster: periodic_cluster (300×).

## Offene Fragen

- 1 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
