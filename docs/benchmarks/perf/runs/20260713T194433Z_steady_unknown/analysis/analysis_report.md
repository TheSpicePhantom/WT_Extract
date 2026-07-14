# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260713T194433Z_steady_unknown`
- **scenario_id:** `steady`
- **run_mode:** `cli`
- **recorded_frames:** 300
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-13T19:44:51.335109+00:00
- **git_commit:** unknown

### Config-Fingerprints

- `profiling`: `-3969074690138833690`
- `streaming`: `5018087761709251249`
- `visibility_lod`: `6770386004332636457`
- `world_gen`: `8245417814985786336`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 51.3794 | 51.3794 | +0.0000 | OK |
| frame_ms_p95 | 58.3510 | 58.3510 | +0.0000 | OK |
| frame_ms_max | 106.9031 | 106.9031 | +0.0000 | OK |
| stream_ms_mean | 42.0592 | 42.0592 | +0.0000 | OK |
| stream_ms_p95 | 46.7910 | 46.7910 | +0.0000 | OK |
| stream_ms_max | 88.0697 | 88.0697 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0089 | 0.0089 | +0.0000 | OK |
| stream_unload_ms_max | 0.0514 | 0.0514 | +0.0000 | OK |
| chunk_count_mean | 15.4100 | 15.4100 | +0.0000 | OK |
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
   - Mittlerer Anteil 81.9% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_apply_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 61.2% an frame_ms.

4. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `frame_slow`: 300
- `stream_slow`: 300
- `load_burst`: 1

### Frame 0

- **frame_ms:** 33.960
- **stream_ms / apply / unload:** 30.648 / 22.545 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:34.0, 2:38.7, 3:33.2

### Frame 1

- **frame_ms:** 34.039
- **stream_ms / apply / unload:** 32.022 / 22.426 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:34.0
- **Kontext danach:** 2:38.7, 3:33.2, 4:34.7

### Frame 2

- **frame_ms:** 38.661
- **stream_ms / apply / unload:** 34.527 / 25.519 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:34.0, 1:34.0
- **Kontext danach:** 3:33.2, 4:34.7, 5:31.6

### Frame 3

- **frame_ms:** 33.160
- **stream_ms / apply / unload:** 29.135 / 20.619 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:34.0, 1:34.0, 2:38.7
- **Kontext danach:** 4:34.7, 5:31.6, 6:32.5

### Frame 4

- **frame_ms:** 34.711
- **stream_ms / apply / unload:** 30.537 / 22.183 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:34.0, 2:38.7, 3:33.2
- **Kontext danach:** 5:31.6, 6:32.5, 7:39.9

### Frame 5

- **frame_ms:** 31.608
- **stream_ms / apply / unload:** 29.650 / 24.319 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:38.7, 3:33.2, 4:34.7
- **Kontext danach:** 6:32.5, 7:39.9, 8:32.9

### Frame 6

- **frame_ms:** 32.466
- **stream_ms / apply / unload:** 28.391 / 22.513 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:33.2, 4:34.7, 5:31.6
- **Kontext danach:** 7:39.9, 8:32.9, 9:31.1

### Frame 7

- **frame_ms:** 39.860
- **stream_ms / apply / unload:** 36.830 / 27.261 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:34.7, 5:31.6, 6:32.5
- **Kontext danach:** 8:32.9, 9:31.1, 10:25.7

### Frame 8

- **frame_ms:** 32.935
- **stream_ms / apply / unload:** 30.922 / 24.112 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:31.6, 6:32.5, 7:39.9
- **Kontext danach:** 9:31.1, 10:25.7, 11:31.4

### Frame 9

- **frame_ms:** 31.086
- **stream_ms / apply / unload:** 28.526 / 21.328 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:32.5, 7:39.9, 8:32.9
- **Kontext danach:** 10:25.7, 11:31.4, 12:37.5

### Frame 10

- **frame_ms:** 25.744
- **stream_ms / apply / unload:** 23.502 / 18.263 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:39.9, 8:32.9, 9:31.1
- **Kontext danach:** 11:31.4, 12:37.5, 13:27.5

### Frame 11

- **frame_ms:** 31.372
- **stream_ms / apply / unload:** 29.151 / 23.070 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:32.9, 9:31.1, 10:25.7
- **Kontext danach:** 12:37.5, 13:27.5, 14:39.4

### Frame 12

- **frame_ms:** 37.550
- **stream_ms / apply / unload:** 33.969 / 25.719 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:31.1, 10:25.7, 11:31.4
- **Kontext danach:** 13:27.5, 14:39.4, 15:39.2

### Frame 13

- **frame_ms:** 27.515
- **stream_ms / apply / unload:** 25.339 / 19.341 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:25.7, 11:31.4, 12:37.5
- **Kontext danach:** 14:39.4, 15:39.2, 16:31.5

### Frame 14

- **frame_ms:** 39.361
- **stream_ms / apply / unload:** 35.649 / 29.521 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 75.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:31.4, 12:37.5, 13:27.5
- **Kontext danach:** 15:39.2, 16:31.5, 17:34.4

### Frame 15

- **frame_ms:** 39.207
- **stream_ms / apply / unload:** 35.111 / 26.101 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 66.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:37.5, 13:27.5, 14:39.4
- **Kontext danach:** 16:31.5, 17:34.4, 18:32.5

### Frame 16

- **frame_ms:** 31.502
- **stream_ms / apply / unload:** 27.000 / 17.979 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 10 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:27.5, 14:39.4, 15:39.2
- **Kontext danach:** 17:34.4, 18:32.5, 19:23.1

### Frame 17

- **frame_ms:** 34.444
- **stream_ms / apply / unload:** 29.043 / 23.961 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 11 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:39.4, 15:39.2, 16:31.5
- **Kontext danach:** 18:32.5, 19:23.1, 20:25.7

### Frame 18

- **frame_ms:** 32.490
- **stream_ms / apply / unload:** 28.781 / 21.776 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:39.2, 16:31.5, 17:34.4
- **Kontext danach:** 19:23.1, 20:25.7, 21:24.2

### Frame 19

- **frame_ms:** 23.128
- **stream_ms / apply / unload:** 18.723 / 13.925 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:31.5, 17:34.4, 18:32.5
- **Kontext danach:** 20:25.7, 21:24.2, 22:34.5

### Frame 20

- **frame_ms:** 25.727
- **stream_ms / apply / unload:** 18.783 / 13.837 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 17:34.4, 18:32.5, 19:23.1
- **Kontext danach:** 21:24.2, 22:34.5, 23:48.2

### Frame 21

- **frame_ms:** 24.151
- **stream_ms / apply / unload:** 19.750 / 14.701 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 18:32.5, 19:23.1, 20:25.7
- **Kontext danach:** 22:34.5, 23:48.2, 24:52.3

### Frame 22

- **frame_ms:** 34.458
- **stream_ms / apply / unload:** 23.791 / 18.950 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 19:23.1, 20:25.7, 21:24.2
- **Kontext danach:** 23:48.2, 24:52.3, 25:48.8

### Frame 23

- **frame_ms:** 48.160
- **stream_ms / apply / unload:** 39.733 / 33.635 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 69.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 20:25.7, 21:24.2, 22:34.5
- **Kontext danach:** 24:52.3, 25:48.8, 26:51.7

### Frame 24

- **frame_ms:** 52.278
- **stream_ms / apply / unload:** 43.949 / 33.044 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 21:24.2, 22:34.5, 23:48.2
- **Kontext danach:** 25:48.8, 26:51.7, 27:53.6

### Frame 25

- **frame_ms:** 48.759
- **stream_ms / apply / unload:** 40.737 / 30.911 / 0.009
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
- **Kontext davor:** 22:34.5, 23:48.2, 24:52.3
- **Kontext danach:** 26:51.7, 27:53.6, 28:61.2

### Frame 26

- **frame_ms:** 51.655
- **stream_ms / apply / unload:** 43.021 / 31.679 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 23:48.2, 24:52.3, 25:48.8
- **Kontext danach:** 27:53.6, 28:61.2, 29:71.5

### Frame 27

- **frame_ms:** 53.631
- **stream_ms / apply / unload:** 44.631 / 33.559 / 0.007
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
- **Kontext davor:** 24:52.3, 25:48.8, 26:51.7
- **Kontext danach:** 28:61.2, 29:71.5, 30:62.8

### Frame 28

- **frame_ms:** 61.218
- **stream_ms / apply / unload:** 50.388 / 38.714 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:48.8, 26:51.7, 27:53.6
- **Kontext danach:** 29:71.5, 30:62.8, 31:60.1

### Frame 29

- **frame_ms:** 71.513
- **stream_ms / apply / unload:** 58.330 / 41.131 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:51.7, 27:53.6, 28:61.2
- **Kontext danach:** 30:62.8, 31:60.1, 32:59.8

### Frame 30

- **frame_ms:** 62.788
- **stream_ms / apply / unload:** 54.956 / 41.156 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 27:53.6, 28:61.2, 29:71.5
- **Kontext danach:** 31:60.1, 32:59.8, 33:57.2

### Frame 31

- **frame_ms:** 60.094
- **stream_ms / apply / unload:** 49.986 / 35.692 / 0.006
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
- **Kontext davor:** 28:61.2, 29:71.5, 30:62.8
- **Kontext danach:** 32:59.8, 33:57.2, 34:64.8

### Frame 32

- **frame_ms:** 59.829
- **stream_ms / apply / unload:** 49.872 / 36.765 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 29:71.5, 30:62.8, 31:60.1
- **Kontext danach:** 33:57.2, 34:64.8, 35:57.9

### Frame 33

- **frame_ms:** 57.168
- **stream_ms / apply / unload:** 46.791 / 35.653 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:62.8, 31:60.1, 32:59.8
- **Kontext danach:** 34:64.8, 35:57.9, 36:58.4

### Frame 34

- **frame_ms:** 64.830
- **stream_ms / apply / unload:** 54.385 / 40.799 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 31:60.1, 32:59.8, 33:57.2
- **Kontext danach:** 35:57.9, 36:58.4, 37:60.6

### Frame 35

- **frame_ms:** 57.872
- **stream_ms / apply / unload:** 48.424 / 36.779 / 0.051
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.6% von frame_ms
  - Unload-dominant: 0.1% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:59.8, 33:57.2, 34:64.8
- **Kontext danach:** 36:58.4, 37:60.6, 38:58.4

### Frame 36

- **frame_ms:** 58.406
- **stream_ms / apply / unload:** 49.212 / 37.137 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:57.2, 34:64.8, 35:57.9
- **Kontext danach:** 37:60.6, 38:58.4, 39:52.6

### Frame 37

- **frame_ms:** 60.590
- **stream_ms / apply / unload:** 51.170 / 37.947 / 0.007
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
- **Kontext davor:** 34:64.8, 35:57.9, 36:58.4
- **Kontext danach:** 38:58.4, 39:52.6, 40:51.2

### Frame 38

- **frame_ms:** 58.351
- **stream_ms / apply / unload:** 48.313 / 34.907 / 0.008
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 35:57.9, 36:58.4, 37:60.6
- **Kontext danach:** 39:52.6, 40:51.2, 41:52.7

### Frame 39

- **frame_ms:** 52.616
- **stream_ms / apply / unload:** 42.051 / 32.144 / 0.007
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 36:58.4, 37:60.6, 38:58.4
- **Kontext danach:** 40:51.2, 41:52.7, 42:51.3

### Frame 40

- **frame_ms:** 51.208
- **stream_ms / apply / unload:** 41.462 / 30.558 / 0.009
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
- **Kontext davor:** 37:60.6, 38:58.4, 39:52.6
- **Kontext danach:** 41:52.7, 42:51.3, 43:52.5

### Frame 41

- **frame_ms:** 52.722
- **stream_ms / apply / unload:** 43.389 / 31.870 / 0.007
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
- **Kontext davor:** 38:58.4, 39:52.6, 40:51.2
- **Kontext danach:** 42:51.3, 43:52.5, 44:53.6

### Frame 42

- **frame_ms:** 51.289
- **stream_ms / apply / unload:** 41.334 / 30.224 / 0.007
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
- **Kontext davor:** 39:52.6, 40:51.2, 41:52.7
- **Kontext danach:** 43:52.5, 44:53.6, 45:57.2

### Frame 43

- **frame_ms:** 52.469
- **stream_ms / apply / unload:** 41.677 / 30.845 / 0.007
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
- **Kontext davor:** 40:51.2, 41:52.7, 42:51.3
- **Kontext danach:** 44:53.6, 45:57.2, 46:54.2

### Frame 44

- **frame_ms:** 53.574
- **stream_ms / apply / unload:** 43.282 / 32.415 / 0.009
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
- **Kontext davor:** 41:52.7, 42:51.3, 43:52.5
- **Kontext danach:** 45:57.2, 46:54.2, 47:51.9

### Frame 45

- **frame_ms:** 57.153
- **stream_ms / apply / unload:** 46.870 / 36.381 / 0.009
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
- **Kontext davor:** 42:51.3, 43:52.5, 44:53.6
- **Kontext danach:** 46:54.2, 47:51.9, 48:51.9

### Frame 46

- **frame_ms:** 54.216
- **stream_ms / apply / unload:** 43.310 / 32.652 / 0.008
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
- **Kontext davor:** 43:52.5, 44:53.6, 45:57.2
- **Kontext danach:** 47:51.9, 48:51.9, 49:52.2

### Frame 47

- **frame_ms:** 51.877
- **stream_ms / apply / unload:** 43.015 / 31.943 / 0.008
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
- **Kontext davor:** 44:53.6, 45:57.2, 46:54.2
- **Kontext danach:** 48:51.9, 49:52.2, 50:53.8

### Frame 48

- **frame_ms:** 51.893
- **stream_ms / apply / unload:** 41.869 / 32.009 / 0.009
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
- **Kontext davor:** 45:57.2, 46:54.2, 47:51.9
- **Kontext danach:** 49:52.2, 50:53.8, 51:52.9

### Frame 49

- **frame_ms:** 52.159
- **stream_ms / apply / unload:** 42.460 / 32.066 / 0.008
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
- **Kontext davor:** 46:54.2, 47:51.9, 48:51.9
- **Kontext danach:** 50:53.8, 51:52.9, 52:55.0

### Frame 50

- **frame_ms:** 53.782
- **stream_ms / apply / unload:** 44.109 / 32.713 / 0.008
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
- **Kontext davor:** 47:51.9, 48:51.9, 49:52.2
- **Kontext danach:** 51:52.9, 52:55.0, 53:53.6

### Frame 51

- **frame_ms:** 52.931
- **stream_ms / apply / unload:** 42.846 / 32.303 / 0.007
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
- **Kontext davor:** 48:51.9, 49:52.2, 50:53.8
- **Kontext danach:** 52:55.0, 53:53.6, 54:51.2

### Frame 52

- **frame_ms:** 55.032
- **stream_ms / apply / unload:** 45.342 / 33.626 / 0.007
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
- **Kontext davor:** 49:52.2, 50:53.8, 51:52.9
- **Kontext danach:** 53:53.6, 54:51.2, 55:53.2

### Frame 53

- **frame_ms:** 53.606
- **stream_ms / apply / unload:** 44.214 / 33.241 / 0.008
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
- **Kontext davor:** 50:53.8, 51:52.9, 52:55.0
- **Kontext danach:** 54:51.2, 55:53.2, 56:52.2

### Frame 54

- **frame_ms:** 51.157
- **stream_ms / apply / unload:** 41.124 / 30.107 / 0.008
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
- **Kontext davor:** 51:52.9, 52:55.0, 53:53.6
- **Kontext danach:** 55:53.2, 56:52.2, 57:53.8

### Frame 55

- **frame_ms:** 53.205
- **stream_ms / apply / unload:** 43.543 / 32.599 / 0.008
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
- **Kontext davor:** 52:55.0, 53:53.6, 54:51.2
- **Kontext danach:** 56:52.2, 57:53.8, 58:50.9

### Frame 56

- **frame_ms:** 52.235
- **stream_ms / apply / unload:** 42.942 / 31.945 / 0.008
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
- **Kontext davor:** 53:53.6, 54:51.2, 55:53.2
- **Kontext danach:** 57:53.8, 58:50.9, 59:52.2

### Frame 57

- **frame_ms:** 53.768
- **stream_ms / apply / unload:** 43.785 / 32.732 / 0.008
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
- **Kontext davor:** 54:51.2, 55:53.2, 56:52.2
- **Kontext danach:** 58:50.9, 59:52.2, 60:51.8

### Frame 58

- **frame_ms:** 50.873
- **stream_ms / apply / unload:** 40.603 / 29.800 / 0.008
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
- **Kontext davor:** 55:53.2, 56:52.2, 57:53.8
- **Kontext danach:** 59:52.2, 60:51.8, 61:82.5

### Frame 59

- **frame_ms:** 52.218
- **stream_ms / apply / unload:** 42.834 / 31.977 / 0.009
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
- **Kontext davor:** 56:52.2, 57:53.8, 58:50.9
- **Kontext danach:** 60:51.8, 61:82.5, 62:106.9

### Frame 60

- **frame_ms:** 51.849
- **stream_ms / apply / unload:** 42.324 / 31.692 / 0.008
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
- **Kontext davor:** 57:53.8, 58:50.9, 59:52.2
- **Kontext danach:** 61:82.5, 62:106.9, 63:77.7

### Frame 61

- **frame_ms:** 82.508
- **stream_ms / apply / unload:** 64.303 / 53.649 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 58:50.9, 59:52.2, 60:51.8
- **Kontext danach:** 62:106.9, 63:77.7, 64:72.5

### Frame 62

- **frame_ms:** 106.903
- **stream_ms / apply / unload:** 88.070 / 63.780 / 0.008
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
- **Kontext davor:** 59:52.2, 60:51.8, 61:82.5
- **Kontext danach:** 63:77.7, 64:72.5, 65:52.3

### Frame 63

- **frame_ms:** 77.739
- **stream_ms / apply / unload:** 65.303 / 39.812 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 60:51.8, 61:82.5, 62:106.9
- **Kontext danach:** 64:72.5, 65:52.3, 66:51.5

### Frame 64

- **frame_ms:** 72.501
- **stream_ms / apply / unload:** 61.610 / 41.758 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 61:82.5, 62:106.9, 63:77.7
- **Kontext danach:** 65:52.3, 66:51.5, 67:51.9

### Frame 65

- **frame_ms:** 52.277
- **stream_ms / apply / unload:** 42.295 / 32.155 / 0.007
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
- **Kontext davor:** 62:106.9, 63:77.7, 64:72.5
- **Kontext danach:** 66:51.5, 67:51.9, 68:50.5

### Frame 66

- **frame_ms:** 51.477
- **stream_ms / apply / unload:** 41.795 / 30.987 / 0.007
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
- **Kontext davor:** 63:77.7, 64:72.5, 65:52.3
- **Kontext danach:** 67:51.9, 68:50.5, 69:50.8

### Frame 67

- **frame_ms:** 51.904
- **stream_ms / apply / unload:** 42.316 / 31.251 / 0.008
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
- **Kontext davor:** 64:72.5, 65:52.3, 66:51.5
- **Kontext danach:** 68:50.5, 69:50.8, 70:51.2

### Frame 68

- **frame_ms:** 50.512
- **stream_ms / apply / unload:** 41.684 / 31.171 / 0.008
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
- **Kontext davor:** 65:52.3, 66:51.5, 67:51.9
- **Kontext danach:** 69:50.8, 70:51.2, 71:54.1

### Frame 69

- **frame_ms:** 50.758
- **stream_ms / apply / unload:** 41.697 / 31.695 / 0.009
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
- **Kontext davor:** 66:51.5, 67:51.9, 68:50.5
- **Kontext danach:** 70:51.2, 71:54.1, 72:51.7

### Frame 70

- **frame_ms:** 51.153
- **stream_ms / apply / unload:** 42.193 / 31.883 / 0.008
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
- **Kontext davor:** 67:51.9, 68:50.5, 69:50.8
- **Kontext danach:** 71:54.1, 72:51.7, 73:52.3

### Frame 71

- **frame_ms:** 54.116
- **stream_ms / apply / unload:** 44.702 / 33.137 / 0.008
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
- **Kontext davor:** 68:50.5, 69:50.8, 70:51.2
- **Kontext danach:** 72:51.7, 73:52.3, 74:52.7

### Frame 72

- **frame_ms:** 51.679
- **stream_ms / apply / unload:** 42.025 / 31.578 / 0.009
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
- **Kontext davor:** 69:50.8, 70:51.2, 71:54.1
- **Kontext danach:** 73:52.3, 74:52.7, 75:51.7

### Frame 73

- **frame_ms:** 52.320
- **stream_ms / apply / unload:** 43.140 / 31.834 / 0.008
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
- **Kontext davor:** 70:51.2, 71:54.1, 72:51.7
- **Kontext danach:** 74:52.7, 75:51.7, 76:51.6

### Frame 74

- **frame_ms:** 52.668
- **stream_ms / apply / unload:** 42.964 / 32.873 / 0.009
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
- **Kontext davor:** 71:54.1, 72:51.7, 73:52.3
- **Kontext danach:** 75:51.7, 76:51.6, 77:49.6

### Frame 75

- **frame_ms:** 51.719
- **stream_ms / apply / unload:** 42.131 / 30.770 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 72:51.7, 73:52.3, 74:52.7
- **Kontext danach:** 76:51.6, 77:49.6, 78:52.4

### Frame 76

- **frame_ms:** 51.618
- **stream_ms / apply / unload:** 42.481 / 32.105 / 0.008
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
- **Kontext davor:** 73:52.3, 74:52.7, 75:51.7
- **Kontext danach:** 77:49.6, 78:52.4, 79:49.9

### Frame 77

- **frame_ms:** 49.644
- **stream_ms / apply / unload:** 40.083 / 29.865 / 0.008
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
- **Kontext davor:** 74:52.7, 75:51.7, 76:51.6
- **Kontext danach:** 78:52.4, 79:49.9, 80:51.4

### Frame 78

- **frame_ms:** 52.425
- **stream_ms / apply / unload:** 42.479 / 31.253 / 0.007
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
- **Kontext davor:** 75:51.7, 76:51.6, 77:49.6
- **Kontext danach:** 79:49.9, 80:51.4, 81:50.7

### Frame 79

- **frame_ms:** 49.919
- **stream_ms / apply / unload:** 40.090 / 29.085 / 0.009
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
- **Kontext davor:** 76:51.6, 77:49.6, 78:52.4
- **Kontext danach:** 80:51.4, 81:50.7, 82:52.4

### Frame 80

- **frame_ms:** 51.390
- **stream_ms / apply / unload:** 41.993 / 30.838 / 0.008
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
- **Kontext davor:** 77:49.6, 78:52.4, 79:49.9
- **Kontext danach:** 81:50.7, 82:52.4, 83:50.3

### Frame 81

- **frame_ms:** 50.700
- **stream_ms / apply / unload:** 41.455 / 31.576 / 0.008
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
- **Kontext davor:** 78:52.4, 79:49.9, 80:51.4
- **Kontext danach:** 82:52.4, 83:50.3, 84:51.7

### Frame 82

- **frame_ms:** 52.443
- **stream_ms / apply / unload:** 41.545 / 31.859 / 0.007
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
- **Kontext davor:** 79:49.9, 80:51.4, 81:50.7
- **Kontext danach:** 83:50.3, 84:51.7, 85:50.8

### Frame 83

- **frame_ms:** 50.288
- **stream_ms / apply / unload:** 40.598 / 29.485 / 0.008
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
- **Kontext davor:** 80:51.4, 81:50.7, 82:52.4
- **Kontext danach:** 84:51.7, 85:50.8, 86:51.1

### Frame 84

- **frame_ms:** 51.741
- **stream_ms / apply / unload:** 42.891 / 32.392 / 0.008
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
- **Kontext davor:** 81:50.7, 82:52.4, 83:50.3
- **Kontext danach:** 85:50.8, 86:51.1, 87:52.7

### Frame 85

- **frame_ms:** 50.822
- **stream_ms / apply / unload:** 41.727 / 31.391 / 0.008
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
- **Kontext davor:** 82:52.4, 83:50.3, 84:51.7
- **Kontext danach:** 86:51.1, 87:52.7, 88:50.6

### Frame 86

- **frame_ms:** 51.139
- **stream_ms / apply / unload:** 41.650 / 30.916 / 0.008
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
- **Kontext davor:** 83:50.3, 84:51.7, 85:50.8
- **Kontext danach:** 87:52.7, 88:50.6, 89:52.9

### Frame 87

- **frame_ms:** 52.726
- **stream_ms / apply / unload:** 43.699 / 32.552 / 0.009
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
- **Kontext davor:** 84:51.7, 85:50.8, 86:51.1
- **Kontext danach:** 88:50.6, 89:52.9, 90:51.4

### Frame 88

- **frame_ms:** 50.601
- **stream_ms / apply / unload:** 41.549 / 30.544 / 0.007
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
- **Kontext davor:** 85:50.8, 86:51.1, 87:52.7
- **Kontext danach:** 89:52.9, 90:51.4, 91:52.7

### Frame 89

- **frame_ms:** 52.908
- **stream_ms / apply / unload:** 43.537 / 32.956 / 0.008
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
- **Kontext davor:** 86:51.1, 87:52.7, 88:50.6
- **Kontext danach:** 90:51.4, 91:52.7, 92:51.2

### Frame 90

- **frame_ms:** 51.435
- **stream_ms / apply / unload:** 41.591 / 30.800 / 0.007
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
- **Kontext davor:** 87:52.7, 88:50.6, 89:52.9
- **Kontext danach:** 91:52.7, 92:51.2, 93:50.9

### Frame 91

- **frame_ms:** 52.682
- **stream_ms / apply / unload:** 43.479 / 31.696 / 0.007
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
- **Kontext davor:** 88:50.6, 89:52.9, 90:51.4
- **Kontext danach:** 92:51.2, 93:50.9, 94:53.3

### Frame 92

- **frame_ms:** 51.204
- **stream_ms / apply / unload:** 41.469 / 30.313 / 0.008
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
- **Kontext davor:** 89:52.9, 90:51.4, 91:52.7
- **Kontext danach:** 93:50.9, 94:53.3, 95:51.1

### Frame 93

- **frame_ms:** 50.909
- **stream_ms / apply / unload:** 41.578 / 30.978 / 0.008
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
- **Kontext davor:** 90:51.4, 91:52.7, 92:51.2
- **Kontext danach:** 94:53.3, 95:51.1, 96:51.3

### Frame 94

- **frame_ms:** 53.252
- **stream_ms / apply / unload:** 43.857 / 33.804 / 0.008
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
- **Kontext davor:** 91:52.7, 92:51.2, 93:50.9
- **Kontext danach:** 95:51.1, 96:51.3, 97:50.3

### Frame 95

- **frame_ms:** 51.061
- **stream_ms / apply / unload:** 41.573 / 31.185 / 0.007
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
- **Kontext davor:** 92:51.2, 93:50.9, 94:53.3
- **Kontext danach:** 96:51.3, 97:50.3, 98:51.1

### Frame 96

- **frame_ms:** 51.318
- **stream_ms / apply / unload:** 41.623 / 30.987 / 0.008
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
- **Kontext davor:** 93:50.9, 94:53.3, 95:51.1
- **Kontext danach:** 97:50.3, 98:51.1, 99:50.5

### Frame 97

- **frame_ms:** 50.300
- **stream_ms / apply / unload:** 40.605 / 30.806 / 0.008
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
- **Kontext davor:** 94:53.3, 95:51.1, 96:51.3
- **Kontext danach:** 98:51.1, 99:50.5, 100:52.3

### Frame 98

- **frame_ms:** 51.071
- **stream_ms / apply / unload:** 41.789 / 31.655 / 0.007
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
- **Kontext davor:** 95:51.1, 96:51.3, 97:50.3
- **Kontext danach:** 99:50.5, 100:52.3, 101:51.9

### Frame 99

- **frame_ms:** 50.515
- **stream_ms / apply / unload:** 40.964 / 30.246 / 0.008
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
- **Kontext davor:** 96:51.3, 97:50.3, 98:51.1
- **Kontext danach:** 100:52.3, 101:51.9, 102:53.5

### Frame 100

- **frame_ms:** 52.320
- **stream_ms / apply / unload:** 42.412 / 32.066 / 0.007
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
- **Kontext davor:** 97:50.3, 98:51.1, 99:50.5
- **Kontext danach:** 101:51.9, 102:53.5, 103:50.6

### Frame 101

- **frame_ms:** 51.920
- **stream_ms / apply / unload:** 42.368 / 31.277 / 0.011
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
- **Kontext davor:** 98:51.1, 99:50.5, 100:52.3
- **Kontext danach:** 102:53.5, 103:50.6, 104:51.1

### Frame 102

- **frame_ms:** 53.466
- **stream_ms / apply / unload:** 43.799 / 32.308 / 0.007
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
- **Kontext davor:** 99:50.5, 100:52.3, 101:51.9
- **Kontext danach:** 103:50.6, 104:51.1, 105:54.0

### Frame 103

- **frame_ms:** 50.591
- **stream_ms / apply / unload:** 40.920 / 30.234 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 100:52.3, 101:51.9, 102:53.5
- **Kontext danach:** 104:51.1, 105:54.0, 106:51.1

### Frame 104

- **frame_ms:** 51.093
- **stream_ms / apply / unload:** 42.140 / 31.352 / 0.009
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
- **Kontext davor:** 101:51.9, 102:53.5, 103:50.6
- **Kontext danach:** 105:54.0, 106:51.1, 107:51.1

### Frame 105

- **frame_ms:** 53.982
- **stream_ms / apply / unload:** 44.130 / 32.808 / 0.008
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
- **Kontext davor:** 102:53.5, 103:50.6, 104:51.1
- **Kontext danach:** 106:51.1, 107:51.1, 108:52.5

### Frame 106

- **frame_ms:** 51.087
- **stream_ms / apply / unload:** 42.047 / 31.194 / 0.007
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
- **Kontext davor:** 103:50.6, 104:51.1, 105:54.0
- **Kontext danach:** 107:51.1, 108:52.5, 109:52.8

### Frame 107

- **frame_ms:** 51.067
- **stream_ms / apply / unload:** 41.532 / 30.423 / 0.008
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
- **Kontext davor:** 104:51.1, 105:54.0, 106:51.1
- **Kontext danach:** 108:52.5, 109:52.8, 110:52.1

### Frame 108

- **frame_ms:** 52.462
- **stream_ms / apply / unload:** 42.984 / 31.844 / 0.008
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
- **Kontext davor:** 105:54.0, 106:51.1, 107:51.1
- **Kontext danach:** 109:52.8, 110:52.1, 111:50.6

### Frame 109

- **frame_ms:** 52.787
- **stream_ms / apply / unload:** 42.667 / 31.157 / 0.008
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
- **Kontext davor:** 106:51.1, 107:51.1, 108:52.5
- **Kontext danach:** 110:52.1, 111:50.6, 112:51.6

### Frame 110

- **frame_ms:** 52.144
- **stream_ms / apply / unload:** 42.857 / 32.507 / 0.008
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
- **Kontext davor:** 107:51.1, 108:52.5, 109:52.8
- **Kontext danach:** 111:50.6, 112:51.6, 113:50.1

### Frame 111

- **frame_ms:** 50.642
- **stream_ms / apply / unload:** 41.211 / 31.368 / 0.008
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
- **Kontext davor:** 108:52.5, 109:52.8, 110:52.1
- **Kontext danach:** 112:51.6, 113:50.1, 114:54.1

### Frame 112

- **frame_ms:** 51.639
- **stream_ms / apply / unload:** 42.041 / 31.091 / 0.008
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
- **Kontext davor:** 109:52.8, 110:52.1, 111:50.6
- **Kontext danach:** 113:50.1, 114:54.1, 115:49.7

### Frame 113

- **frame_ms:** 50.070
- **stream_ms / apply / unload:** 41.073 / 30.647 / 0.008
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
- **Kontext davor:** 110:52.1, 111:50.6, 112:51.6
- **Kontext danach:** 114:54.1, 115:49.7, 116:50.4

### Frame 114

- **frame_ms:** 54.116
- **stream_ms / apply / unload:** 44.184 / 33.674 / 0.008
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
- **Kontext davor:** 111:50.6, 112:51.6, 113:50.1
- **Kontext danach:** 115:49.7, 116:50.4, 117:51.0

### Frame 115

- **frame_ms:** 49.697
- **stream_ms / apply / unload:** 40.269 / 29.773 / 0.007
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
- **Kontext davor:** 112:51.6, 113:50.1, 114:54.1
- **Kontext danach:** 116:50.4, 117:51.0, 118:50.7

### Frame 116

- **frame_ms:** 50.368
- **stream_ms / apply / unload:** 41.454 / 30.315 / 0.008
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
- **Kontext davor:** 113:50.1, 114:54.1, 115:49.7
- **Kontext danach:** 117:51.0, 118:50.7, 119:63.9

### Frame 117

- **frame_ms:** 50.987
- **stream_ms / apply / unload:** 42.038 / 31.550 / 0.008
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
- **Kontext davor:** 114:54.1, 115:49.7, 116:50.4
- **Kontext danach:** 118:50.7, 119:63.9, 120:51.6

### Frame 118

- **frame_ms:** 50.745
- **stream_ms / apply / unload:** 40.561 / 30.500 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 115:49.7, 116:50.4, 117:51.0
- **Kontext danach:** 119:63.9, 120:51.6, 121:51.3

### Frame 119

- **frame_ms:** 63.867
- **stream_ms / apply / unload:** 44.367 / 32.677 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 116:50.4, 117:51.0, 118:50.7
- **Kontext danach:** 120:51.6, 121:51.3, 122:53.3

### Frame 120

- **frame_ms:** 51.639
- **stream_ms / apply / unload:** 41.898 / 31.081 / 0.007
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
- **Kontext davor:** 117:51.0, 118:50.7, 119:63.9
- **Kontext danach:** 121:51.3, 122:53.3, 123:49.9

### Frame 121

- **frame_ms:** 51.295
- **stream_ms / apply / unload:** 41.980 / 31.534 / 0.007
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
- **Kontext davor:** 118:50.7, 119:63.9, 120:51.6
- **Kontext danach:** 122:53.3, 123:49.9, 124:50.4

### Frame 122

- **frame_ms:** 53.306
- **stream_ms / apply / unload:** 43.284 / 32.133 / 0.008
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
- **Kontext davor:** 119:63.9, 120:51.6, 121:51.3
- **Kontext danach:** 123:49.9, 124:50.4, 125:52.2

### Frame 123

- **frame_ms:** 49.918
- **stream_ms / apply / unload:** 40.530 / 30.246 / 0.008
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
- **Kontext davor:** 120:51.6, 121:51.3, 122:53.3
- **Kontext danach:** 124:50.4, 125:52.2, 126:52.0

### Frame 124

- **frame_ms:** 50.448
- **stream_ms / apply / unload:** 40.710 / 29.664 / 0.008
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
- **Kontext davor:** 121:51.3, 122:53.3, 123:49.9
- **Kontext danach:** 125:52.2, 126:52.0, 127:52.7

### Frame 125

- **frame_ms:** 52.236
- **stream_ms / apply / unload:** 42.860 / 32.555 / 0.008
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
- **Kontext davor:** 122:53.3, 123:49.9, 124:50.4
- **Kontext danach:** 126:52.0, 127:52.7, 128:53.6

### Frame 126

- **frame_ms:** 52.042
- **stream_ms / apply / unload:** 42.312 / 31.150 / 0.007
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
- **Kontext davor:** 123:49.9, 124:50.4, 125:52.2
- **Kontext danach:** 127:52.7, 128:53.6, 129:49.7

### Frame 127

- **frame_ms:** 52.747
- **stream_ms / apply / unload:** 42.998 / 31.976 / 0.008
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
- **Kontext davor:** 124:50.4, 125:52.2, 126:52.0
- **Kontext danach:** 128:53.6, 129:49.7, 130:51.3

### Frame 128

- **frame_ms:** 53.627
- **stream_ms / apply / unload:** 43.352 / 32.926 / 0.007
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
- **Kontext davor:** 125:52.2, 126:52.0, 127:52.7
- **Kontext danach:** 129:49.7, 130:51.3, 131:53.4

### Frame 129

- **frame_ms:** 49.675
- **stream_ms / apply / unload:** 40.775 / 30.484 / 0.007
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
- **Kontext davor:** 126:52.0, 127:52.7, 128:53.6
- **Kontext danach:** 130:51.3, 131:53.4, 132:50.3

### Frame 130

- **frame_ms:** 51.276
- **stream_ms / apply / unload:** 41.896 / 30.978 / 0.008
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
- **Kontext davor:** 127:52.7, 128:53.6, 129:49.7
- **Kontext danach:** 131:53.4, 132:50.3, 133:49.1

### Frame 131

- **frame_ms:** 53.416
- **stream_ms / apply / unload:** 43.288 / 32.470 / 0.008
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
- **Kontext davor:** 128:53.6, 129:49.7, 130:51.3
- **Kontext danach:** 132:50.3, 133:49.1, 134:51.2

### Frame 132

- **frame_ms:** 50.342
- **stream_ms / apply / unload:** 41.310 / 31.529 / 0.008
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
- **Kontext davor:** 129:49.7, 130:51.3, 131:53.4
- **Kontext danach:** 133:49.1, 134:51.2, 135:51.2

### Frame 133

- **frame_ms:** 49.074
- **stream_ms / apply / unload:** 39.758 / 29.844 / 0.008
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
- **Kontext davor:** 130:51.3, 131:53.4, 132:50.3
- **Kontext danach:** 134:51.2, 135:51.2, 136:51.5

### Frame 134

- **frame_ms:** 51.171
- **stream_ms / apply / unload:** 41.735 / 31.422 / 0.008
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
- **Kontext davor:** 131:53.4, 132:50.3, 133:49.1
- **Kontext danach:** 135:51.2, 136:51.5, 137:52.6

### Frame 135

- **frame_ms:** 51.238
- **stream_ms / apply / unload:** 41.357 / 30.199 / 0.008
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
- **Kontext davor:** 132:50.3, 133:49.1, 134:51.2
- **Kontext danach:** 136:51.5, 137:52.6, 138:51.7

### Frame 136

- **frame_ms:** 51.509
- **stream_ms / apply / unload:** 41.859 / 31.113 / 0.008
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
- **Kontext davor:** 133:49.1, 134:51.2, 135:51.2
- **Kontext danach:** 137:52.6, 138:51.7, 139:53.7

### Frame 137

- **frame_ms:** 52.559
- **stream_ms / apply / unload:** 43.570 / 32.682 / 0.008
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
- **Kontext davor:** 134:51.2, 135:51.2, 136:51.5
- **Kontext danach:** 138:51.7, 139:53.7, 140:51.4

### Frame 138

- **frame_ms:** 51.652
- **stream_ms / apply / unload:** 42.016 / 31.297 / 0.008
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
- **Kontext davor:** 135:51.2, 136:51.5, 137:52.6
- **Kontext danach:** 139:53.7, 140:51.4, 141:51.6

### Frame 139

- **frame_ms:** 53.745
- **stream_ms / apply / unload:** 44.063 / 33.538 / 0.008
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
- **Kontext davor:** 136:51.5, 137:52.6, 138:51.7
- **Kontext danach:** 140:51.4, 141:51.6, 142:52.6

### Frame 140

- **frame_ms:** 51.369
- **stream_ms / apply / unload:** 41.341 / 30.782 / 0.007
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
- **Kontext davor:** 137:52.6, 138:51.7, 139:53.7
- **Kontext danach:** 141:51.6, 142:52.6, 143:50.9

### Frame 141

- **frame_ms:** 51.621
- **stream_ms / apply / unload:** 42.788 / 31.798 / 0.008
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
- **Kontext davor:** 138:51.7, 139:53.7, 140:51.4
- **Kontext danach:** 142:52.6, 143:50.9, 144:48.7

### Frame 142

- **frame_ms:** 52.561
- **stream_ms / apply / unload:** 42.346 / 31.913 / 0.007
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
- **Kontext davor:** 139:53.7, 140:51.4, 141:51.6
- **Kontext danach:** 143:50.9, 144:48.7, 145:51.4

### Frame 143

- **frame_ms:** 50.924
- **stream_ms / apply / unload:** 41.210 / 30.902 / 0.008
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
- **Kontext davor:** 140:51.4, 141:51.6, 142:52.6
- **Kontext danach:** 144:48.7, 145:51.4, 146:49.5

### Frame 144

- **frame_ms:** 48.711
- **stream_ms / apply / unload:** 39.703 / 29.849 / 0.007
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
- **Kontext davor:** 141:51.6, 142:52.6, 143:50.9
- **Kontext danach:** 145:51.4, 146:49.5, 147:52.2

### Frame 145

- **frame_ms:** 51.385
- **stream_ms / apply / unload:** 41.270 / 29.971 / 0.008
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
- **Kontext davor:** 142:52.6, 143:50.9, 144:48.7
- **Kontext danach:** 146:49.5, 147:52.2, 148:51.8

### Frame 146

- **frame_ms:** 49.457
- **stream_ms / apply / unload:** 39.386 / 29.774 / 0.007
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
- **Kontext davor:** 143:50.9, 144:48.7, 145:51.4
- **Kontext danach:** 147:52.2, 148:51.8, 149:50.7

### Frame 147

- **frame_ms:** 52.187
- **stream_ms / apply / unload:** 41.817 / 30.897 / 0.008
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
- **Kontext davor:** 144:48.7, 145:51.4, 146:49.5
- **Kontext danach:** 148:51.8, 149:50.7, 150:53.6

### Frame 148

- **frame_ms:** 51.762
- **stream_ms / apply / unload:** 42.622 / 31.603 / 0.007
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
- **Kontext davor:** 145:51.4, 146:49.5, 147:52.2
- **Kontext danach:** 149:50.7, 150:53.6, 151:52.2

### Frame 149

- **frame_ms:** 50.655
- **stream_ms / apply / unload:** 41.522 / 31.738 / 0.008
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
- **Kontext davor:** 146:49.5, 147:52.2, 148:51.8
- **Kontext danach:** 150:53.6, 151:52.2, 152:50.8

### Frame 150

- **frame_ms:** 53.638
- **stream_ms / apply / unload:** 44.385 / 33.154 / 0.008
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
- **Kontext davor:** 147:52.2, 148:51.8, 149:50.7
- **Kontext danach:** 151:52.2, 152:50.8, 153:52.6

### Frame 151

- **frame_ms:** 52.187
- **stream_ms / apply / unload:** 42.734 / 32.346 / 0.021
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
- **Kontext davor:** 148:51.8, 149:50.7, 150:53.6
- **Kontext danach:** 152:50.8, 153:52.6, 154:50.1

### Frame 152

- **frame_ms:** 50.817
- **stream_ms / apply / unload:** 40.829 / 31.228 / 0.008
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
- **Kontext davor:** 149:50.7, 150:53.6, 151:52.2
- **Kontext danach:** 153:52.6, 154:50.1, 155:51.9

### Frame 153

- **frame_ms:** 52.569
- **stream_ms / apply / unload:** 43.781 / 31.851 / 0.007
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
- **Kontext davor:** 150:53.6, 151:52.2, 152:50.8
- **Kontext danach:** 154:50.1, 155:51.9, 156:51.3

### Frame 154

- **frame_ms:** 50.053
- **stream_ms / apply / unload:** 40.289 / 29.784 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 151:52.2, 152:50.8, 153:52.6
- **Kontext danach:** 155:51.9, 156:51.3, 157:49.9

### Frame 155

- **frame_ms:** 51.877
- **stream_ms / apply / unload:** 41.318 / 31.268 / 0.008
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
- **Kontext davor:** 152:50.8, 153:52.6, 154:50.1
- **Kontext danach:** 156:51.3, 157:49.9, 158:51.4

### Frame 156

- **frame_ms:** 51.327
- **stream_ms / apply / unload:** 41.754 / 31.011 / 0.008
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
- **Kontext davor:** 153:52.6, 154:50.1, 155:51.9
- **Kontext danach:** 157:49.9, 158:51.4, 159:51.2

### Frame 157

- **frame_ms:** 49.891
- **stream_ms / apply / unload:** 40.266 / 30.420 / 0.008
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
- **Kontext davor:** 154:50.1, 155:51.9, 156:51.3
- **Kontext danach:** 158:51.4, 159:51.2, 160:51.7

### Frame 158

- **frame_ms:** 51.401
- **stream_ms / apply / unload:** 42.635 / 32.082 / 0.008
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
- **Kontext davor:** 155:51.9, 156:51.3, 157:49.9
- **Kontext danach:** 159:51.2, 160:51.7, 161:52.3

### Frame 159

- **frame_ms:** 51.241
- **stream_ms / apply / unload:** 42.286 / 31.919 / 0.007
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
- **Kontext davor:** 156:51.3, 157:49.9, 158:51.4
- **Kontext danach:** 160:51.7, 161:52.3, 162:51.6

### Frame 160

- **frame_ms:** 51.724
- **stream_ms / apply / unload:** 42.087 / 32.158 / 0.008
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
- **Kontext davor:** 157:49.9, 158:51.4, 159:51.2
- **Kontext danach:** 161:52.3, 162:51.6, 163:51.9

### Frame 161

- **frame_ms:** 52.345
- **stream_ms / apply / unload:** 42.995 / 31.093 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 158:51.4, 159:51.2, 160:51.7
- **Kontext danach:** 162:51.6, 163:51.9, 164:50.1

### Frame 162

- **frame_ms:** 51.551
- **stream_ms / apply / unload:** 41.865 / 31.273 / 0.008
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
- **Kontext davor:** 159:51.2, 160:51.7, 161:52.3
- **Kontext danach:** 163:51.9, 164:50.1, 165:51.8

### Frame 163

- **frame_ms:** 51.914
- **stream_ms / apply / unload:** 42.837 / 32.227 / 0.008
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
- **Kontext davor:** 160:51.7, 161:52.3, 162:51.6
- **Kontext danach:** 164:50.1, 165:51.8, 166:51.9

### Frame 164

- **frame_ms:** 50.128
- **stream_ms / apply / unload:** 41.294 / 30.302 / 0.009
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
- **Kontext davor:** 161:52.3, 162:51.6, 163:51.9
- **Kontext danach:** 165:51.8, 166:51.9, 167:50.9

### Frame 165

- **frame_ms:** 51.832
- **stream_ms / apply / unload:** 42.424 / 32.097 / 0.008
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
- **Kontext davor:** 162:51.6, 163:51.9, 164:50.1
- **Kontext danach:** 166:51.9, 167:50.9, 168:52.0

### Frame 166

- **frame_ms:** 51.899
- **stream_ms / apply / unload:** 42.540 / 31.159 / 0.008
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
- **Kontext davor:** 163:51.9, 164:50.1, 165:51.8
- **Kontext danach:** 167:50.9, 168:52.0, 169:52.1

### Frame 167

- **frame_ms:** 50.884
- **stream_ms / apply / unload:** 41.678 / 31.421 / 0.008
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
- **Kontext davor:** 164:50.1, 165:51.8, 166:51.9
- **Kontext danach:** 168:52.0, 169:52.1, 170:49.1

### Frame 168

- **frame_ms:** 52.011
- **stream_ms / apply / unload:** 42.599 / 31.745 / 0.008
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
- **Kontext davor:** 165:51.8, 166:51.9, 167:50.9
- **Kontext danach:** 169:52.1, 170:49.1, 171:52.2

### Frame 169

- **frame_ms:** 52.133
- **stream_ms / apply / unload:** 42.227 / 31.295 / 0.008
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
- **Kontext davor:** 166:51.9, 167:50.9, 168:52.0
- **Kontext danach:** 170:49.1, 171:52.2, 172:51.3

### Frame 170

- **frame_ms:** 49.103
- **stream_ms / apply / unload:** 40.056 / 29.786 / 0.007
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
- **Kontext davor:** 167:50.9, 168:52.0, 169:52.1
- **Kontext danach:** 171:52.2, 172:51.3, 173:51.3

### Frame 171

- **frame_ms:** 52.177
- **stream_ms / apply / unload:** 42.216 / 32.158 / 0.008
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
- **Kontext davor:** 168:52.0, 169:52.1, 170:49.1
- **Kontext danach:** 172:51.3, 173:51.3, 174:54.0

### Frame 172

- **frame_ms:** 51.282
- **stream_ms / apply / unload:** 42.425 / 31.999 / 0.008
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
- **Kontext davor:** 169:52.1, 170:49.1, 171:52.2
- **Kontext danach:** 173:51.3, 174:54.0, 175:50.5

### Frame 173

- **frame_ms:** 51.329
- **stream_ms / apply / unload:** 42.302 / 31.810 / 0.009
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
- **Kontext davor:** 170:49.1, 171:52.2, 172:51.3
- **Kontext danach:** 174:54.0, 175:50.5, 176:54.2

### Frame 174

- **frame_ms:** 54.026
- **stream_ms / apply / unload:** 43.824 / 33.192 / 0.008
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
- **Kontext davor:** 171:52.2, 172:51.3, 173:51.3
- **Kontext danach:** 175:50.5, 176:54.2, 177:52.0

### Frame 175

- **frame_ms:** 50.512
- **stream_ms / apply / unload:** 40.988 / 30.328 / 0.008
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
- **Kontext davor:** 172:51.3, 173:51.3, 174:54.0
- **Kontext danach:** 176:54.2, 177:52.0, 178:53.5

### Frame 176

- **frame_ms:** 54.173
- **stream_ms / apply / unload:** 44.627 / 32.600 / 0.011
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
- **Kontext davor:** 173:51.3, 174:54.0, 175:50.5
- **Kontext danach:** 177:52.0, 178:53.5, 179:53.6

### Frame 177

- **frame_ms:** 52.002
- **stream_ms / apply / unload:** 42.397 / 31.310 / 0.008
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
- **Kontext davor:** 174:54.0, 175:50.5, 176:54.2
- **Kontext danach:** 178:53.5, 179:53.6, 180:50.4

### Frame 178

- **frame_ms:** 53.490
- **stream_ms / apply / unload:** 43.603 / 32.656 / 0.008
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
- **Kontext davor:** 175:50.5, 176:54.2, 177:52.0
- **Kontext danach:** 179:53.6, 180:50.4, 181:54.4

### Frame 179

- **frame_ms:** 53.552
- **stream_ms / apply / unload:** 43.984 / 33.420 / 0.008
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
- **Kontext davor:** 176:54.2, 177:52.0, 178:53.5
- **Kontext danach:** 180:50.4, 181:54.4, 182:52.3

### Frame 180

- **frame_ms:** 50.432
- **stream_ms / apply / unload:** 40.990 / 30.268 / 0.007
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
- **Kontext davor:** 177:52.0, 178:53.5, 179:53.6
- **Kontext danach:** 181:54.4, 182:52.3, 183:51.2

### Frame 181

- **frame_ms:** 54.380
- **stream_ms / apply / unload:** 45.165 / 33.597 / 0.008
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
- **Kontext davor:** 178:53.5, 179:53.6, 180:50.4
- **Kontext danach:** 182:52.3, 183:51.2, 184:53.3

### Frame 182

- **frame_ms:** 52.303
- **stream_ms / apply / unload:** 42.527 / 31.838 / 0.008
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
- **Kontext davor:** 179:53.6, 180:50.4, 181:54.4
- **Kontext danach:** 183:51.2, 184:53.3, 185:53.9

### Frame 183

- **frame_ms:** 51.219
- **stream_ms / apply / unload:** 41.598 / 31.501 / 0.009
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
- **Kontext davor:** 180:50.4, 181:54.4, 182:52.3
- **Kontext danach:** 184:53.3, 185:53.9, 186:51.1

### Frame 184

- **frame_ms:** 53.333
- **stream_ms / apply / unload:** 43.381 / 32.026 / 0.008
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
- **Kontext davor:** 181:54.4, 182:52.3, 183:51.2
- **Kontext danach:** 185:53.9, 186:51.1, 187:52.8

### Frame 185

- **frame_ms:** 53.900
- **stream_ms / apply / unload:** 44.393 / 34.455 / 0.008
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
- **Kontext davor:** 182:52.3, 183:51.2, 184:53.3
- **Kontext danach:** 186:51.1, 187:52.8, 188:58.6

### Frame 186

- **frame_ms:** 51.064
- **stream_ms / apply / unload:** 41.417 / 30.384 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 183:51.2, 184:53.3, 185:53.9
- **Kontext danach:** 187:52.8, 188:58.6, 189:51.6

### Frame 187

- **frame_ms:** 52.780
- **stream_ms / apply / unload:** 43.133 / 31.897 / 0.010
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
- **Kontext davor:** 184:53.3, 185:53.9, 186:51.1
- **Kontext danach:** 188:58.6, 189:51.6, 190:53.1

### Frame 188

- **frame_ms:** 58.600
- **stream_ms / apply / unload:** 45.633 / 32.919 / 0.009
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
- **Kontext davor:** 185:53.9, 186:51.1, 187:52.8
- **Kontext danach:** 189:51.6, 190:53.1, 191:52.5

### Frame 189

- **frame_ms:** 51.594
- **stream_ms / apply / unload:** 41.728 / 30.593 / 0.007
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
- **Kontext davor:** 186:51.1, 187:52.8, 188:58.6
- **Kontext danach:** 190:53.1, 191:52.5, 192:52.4

### Frame 190

- **frame_ms:** 53.101
- **stream_ms / apply / unload:** 43.790 / 32.836 / 0.008
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
- **Kontext davor:** 187:52.8, 188:58.6, 189:51.6
- **Kontext danach:** 191:52.5, 192:52.4, 193:50.4

### Frame 191

- **frame_ms:** 52.546
- **stream_ms / apply / unload:** 43.463 / 33.138 / 0.008
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
- **Kontext davor:** 188:58.6, 189:51.6, 190:53.1
- **Kontext danach:** 192:52.4, 193:50.4, 194:52.7

### Frame 192

- **frame_ms:** 52.438
- **stream_ms / apply / unload:** 42.855 / 31.971 / 0.008
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
- **Kontext davor:** 189:51.6, 190:53.1, 191:52.5
- **Kontext danach:** 193:50.4, 194:52.7, 195:51.7

### Frame 193

- **frame_ms:** 50.430
- **stream_ms / apply / unload:** 41.311 / 30.904 / 0.008
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
- **Kontext davor:** 190:53.1, 191:52.5, 192:52.4
- **Kontext danach:** 194:52.7, 195:51.7, 196:51.6

### Frame 194

- **frame_ms:** 52.701
- **stream_ms / apply / unload:** 43.026 / 32.627 / 0.008
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
- **Kontext davor:** 191:52.5, 192:52.4, 193:50.4
- **Kontext danach:** 195:51.7, 196:51.6, 197:50.2

### Frame 195

- **frame_ms:** 51.683
- **stream_ms / apply / unload:** 42.460 / 31.472 / 0.008
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
- **Kontext davor:** 192:52.4, 193:50.4, 194:52.7
- **Kontext danach:** 196:51.6, 197:50.2, 198:51.1

### Frame 196

- **frame_ms:** 51.635
- **stream_ms / apply / unload:** 42.364 / 31.753 / 0.008
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
- **Kontext davor:** 193:50.4, 194:52.7, 195:51.7
- **Kontext danach:** 197:50.2, 198:51.1, 199:51.9

### Frame 197

- **frame_ms:** 50.223
- **stream_ms / apply / unload:** 41.247 / 30.167 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 194:52.7, 195:51.7, 196:51.6
- **Kontext danach:** 198:51.1, 199:51.9, 200:53.4

### Frame 198

- **frame_ms:** 51.108
- **stream_ms / apply / unload:** 41.564 / 30.750 / 0.007
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
- **Kontext davor:** 195:51.7, 196:51.6, 197:50.2
- **Kontext danach:** 199:51.9, 200:53.4, 201:55.2

### Frame 199

- **frame_ms:** 51.886
- **stream_ms / apply / unload:** 42.614 / 31.626 / 0.008
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
- **Kontext davor:** 196:51.6, 197:50.2, 198:51.1
- **Kontext danach:** 200:53.4, 201:55.2, 202:54.0

### Frame 200

- **frame_ms:** 53.432
- **stream_ms / apply / unload:** 42.221 / 31.702 / 0.007
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
- **Kontext davor:** 197:50.2, 198:51.1, 199:51.9
- **Kontext danach:** 201:55.2, 202:54.0, 203:51.9

### Frame 201

- **frame_ms:** 55.197
- **stream_ms / apply / unload:** 45.945 / 31.394 / 0.008
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
- **Kontext davor:** 198:51.1, 199:51.9, 200:53.4
- **Kontext danach:** 202:54.0, 203:51.9, 204:52.8

### Frame 202

- **frame_ms:** 54.038
- **stream_ms / apply / unload:** 42.707 / 31.943 / 0.009
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
- **Kontext davor:** 199:51.9, 200:53.4, 201:55.2
- **Kontext danach:** 203:51.9, 204:52.8, 205:52.4

### Frame 203

- **frame_ms:** 51.868
- **stream_ms / apply / unload:** 41.976 / 31.571 / 0.008
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
- **Kontext davor:** 200:53.4, 201:55.2, 202:54.0
- **Kontext danach:** 204:52.8, 205:52.4, 206:52.8

### Frame 204

- **frame_ms:** 52.814
- **stream_ms / apply / unload:** 42.868 / 31.729 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 201:55.2, 202:54.0, 203:51.9
- **Kontext danach:** 205:52.4, 206:52.8, 207:53.0

### Frame 205

- **frame_ms:** 52.365
- **stream_ms / apply / unload:** 42.911 / 32.678 / 0.008
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
- **Kontext davor:** 202:54.0, 203:51.9, 204:52.8
- **Kontext danach:** 206:52.8, 207:53.0, 208:51.8

### Frame 206

- **frame_ms:** 52.775
- **stream_ms / apply / unload:** 43.791 / 32.241 / 0.008
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
- **Kontext davor:** 203:51.9, 204:52.8, 205:52.4
- **Kontext danach:** 207:53.0, 208:51.8, 209:52.1

### Frame 207

- **frame_ms:** 53.044
- **stream_ms / apply / unload:** 43.158 / 32.528 / 0.008
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
- **Kontext davor:** 204:52.8, 205:52.4, 206:52.8
- **Kontext danach:** 208:51.8, 209:52.1, 210:52.0

### Frame 208

- **frame_ms:** 51.804
- **stream_ms / apply / unload:** 41.877 / 30.897 / 0.008
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
- **Kontext davor:** 205:52.4, 206:52.8, 207:53.0
- **Kontext danach:** 209:52.1, 210:52.0, 211:50.7

### Frame 209

- **frame_ms:** 52.070
- **stream_ms / apply / unload:** 41.586 / 30.841 / 0.008
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
- **Kontext davor:** 206:52.8, 207:53.0, 208:51.8
- **Kontext danach:** 210:52.0, 211:50.7, 212:50.8

### Frame 210

- **frame_ms:** 51.981
- **stream_ms / apply / unload:** 42.004 / 30.971 / 0.007
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
- **Kontext davor:** 207:53.0, 208:51.8, 209:52.1
- **Kontext danach:** 211:50.7, 212:50.8, 213:52.9

### Frame 211

- **frame_ms:** 50.733
- **stream_ms / apply / unload:** 41.257 / 30.935 / 0.009
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
- **Kontext davor:** 208:51.8, 209:52.1, 210:52.0
- **Kontext danach:** 212:50.8, 213:52.9, 214:52.2

### Frame 212

- **frame_ms:** 50.842
- **stream_ms / apply / unload:** 41.404 / 30.908 / 0.007
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
- **Kontext davor:** 209:52.1, 210:52.0, 211:50.7
- **Kontext danach:** 213:52.9, 214:52.2, 215:52.7

### Frame 213

- **frame_ms:** 52.869
- **stream_ms / apply / unload:** 43.195 / 31.750 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 210:52.0, 211:50.7, 212:50.8
- **Kontext danach:** 214:52.2, 215:52.7, 216:53.2

### Frame 214

- **frame_ms:** 52.171
- **stream_ms / apply / unload:** 42.817 / 31.913 / 0.008
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
- **Kontext davor:** 211:50.7, 212:50.8, 213:52.9
- **Kontext danach:** 215:52.7, 216:53.2, 217:53.3

### Frame 215

- **frame_ms:** 52.676
- **stream_ms / apply / unload:** 43.314 / 32.069 / 0.008
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
- **Kontext davor:** 212:50.8, 213:52.9, 214:52.2
- **Kontext danach:** 216:53.2, 217:53.3, 218:52.3

### Frame 216

- **frame_ms:** 53.194
- **stream_ms / apply / unload:** 43.618 / 32.070 / 0.008
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
- **Kontext davor:** 213:52.9, 214:52.2, 215:52.7
- **Kontext danach:** 217:53.3, 218:52.3, 219:51.6

### Frame 217

- **frame_ms:** 53.269
- **stream_ms / apply / unload:** 43.893 / 32.758 / 0.008
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
- **Kontext davor:** 214:52.2, 215:52.7, 216:53.2
- **Kontext danach:** 218:52.3, 219:51.6, 220:52.7

### Frame 218

- **frame_ms:** 52.295
- **stream_ms / apply / unload:** 43.059 / 31.949 / 0.008
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
- **Kontext davor:** 215:52.7, 216:53.2, 217:53.3
- **Kontext danach:** 219:51.6, 220:52.7, 221:54.5

### Frame 219

- **frame_ms:** 51.593
- **stream_ms / apply / unload:** 41.033 / 30.625 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 216:53.2, 217:53.3, 218:52.3
- **Kontext danach:** 220:52.7, 221:54.5, 222:54.2

### Frame 220

- **frame_ms:** 52.695
- **stream_ms / apply / unload:** 43.574 / 32.496 / 0.008
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
- **Kontext davor:** 217:53.3, 218:52.3, 219:51.6
- **Kontext danach:** 221:54.5, 222:54.2, 223:50.0

### Frame 221

- **frame_ms:** 54.451
- **stream_ms / apply / unload:** 43.958 / 32.569 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 218:52.3, 219:51.6, 220:52.7
- **Kontext danach:** 222:54.2, 223:50.0, 224:52.1

### Frame 222

- **frame_ms:** 54.178
- **stream_ms / apply / unload:** 44.651 / 33.472 / 0.008
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
- **Kontext davor:** 219:51.6, 220:52.7, 221:54.5
- **Kontext danach:** 223:50.0, 224:52.1, 225:51.1

### Frame 223

- **frame_ms:** 50.036
- **stream_ms / apply / unload:** 40.659 / 30.548 / 0.007
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
- **Kontext davor:** 220:52.7, 221:54.5, 222:54.2
- **Kontext danach:** 224:52.1, 225:51.1, 226:53.5

### Frame 224

- **frame_ms:** 52.086
- **stream_ms / apply / unload:** 41.974 / 31.675 / 0.007
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
- **Kontext davor:** 221:54.5, 222:54.2, 223:50.0
- **Kontext danach:** 225:51.1, 226:53.5, 227:50.9

### Frame 225

- **frame_ms:** 51.119
- **stream_ms / apply / unload:** 41.642 / 30.784 / 0.009
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
- **Kontext davor:** 222:54.2, 223:50.0, 224:52.1
- **Kontext danach:** 226:53.5, 227:50.9, 228:53.8

### Frame 226

- **frame_ms:** 53.547
- **stream_ms / apply / unload:** 44.221 / 33.354 / 0.007
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
- **Kontext davor:** 223:50.0, 224:52.1, 225:51.1
- **Kontext danach:** 227:50.9, 228:53.8, 229:51.6

### Frame 227

- **frame_ms:** 50.943
- **stream_ms / apply / unload:** 41.831 / 30.507 / 0.009
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
- **Kontext davor:** 224:52.1, 225:51.1, 226:53.5
- **Kontext danach:** 228:53.8, 229:51.6, 230:53.0

### Frame 228

- **frame_ms:** 53.776
- **stream_ms / apply / unload:** 44.035 / 32.473 / 0.007
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
- **Kontext davor:** 225:51.1, 226:53.5, 227:50.9
- **Kontext danach:** 229:51.6, 230:53.0, 231:49.1

### Frame 229

- **frame_ms:** 51.591
- **stream_ms / apply / unload:** 42.703 / 32.197 / 0.009
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
- **Kontext davor:** 226:53.5, 227:50.9, 228:53.8
- **Kontext danach:** 230:53.0, 231:49.1, 232:50.8

### Frame 230

- **frame_ms:** 53.005
- **stream_ms / apply / unload:** 42.837 / 32.086 / 0.007
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
- **Kontext davor:** 227:50.9, 228:53.8, 229:51.6
- **Kontext danach:** 231:49.1, 232:50.8, 233:49.8

### Frame 231

- **frame_ms:** 49.075
- **stream_ms / apply / unload:** 40.259 / 30.491 / 0.008
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
- **Kontext davor:** 228:53.8, 229:51.6, 230:53.0
- **Kontext danach:** 232:50.8, 233:49.8, 234:50.2

### Frame 232

- **frame_ms:** 50.809
- **stream_ms / apply / unload:** 41.074 / 31.339 / 0.007
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
- **Kontext davor:** 229:51.6, 230:53.0, 231:49.1
- **Kontext danach:** 233:49.8, 234:50.2, 235:52.9

### Frame 233

- **frame_ms:** 49.813
- **stream_ms / apply / unload:** 40.951 / 31.238 / 0.007
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
- **Kontext davor:** 230:53.0, 231:49.1, 232:50.8
- **Kontext danach:** 234:50.2, 235:52.9, 236:54.1

### Frame 234

- **frame_ms:** 50.170
- **stream_ms / apply / unload:** 41.091 / 30.662 / 0.007
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
- **Kontext davor:** 231:49.1, 232:50.8, 233:49.8
- **Kontext danach:** 235:52.9, 236:54.1, 237:51.5

### Frame 235

- **frame_ms:** 52.901
- **stream_ms / apply / unload:** 43.614 / 33.404 / 0.009
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
- **Kontext davor:** 232:50.8, 233:49.8, 234:50.2
- **Kontext danach:** 236:54.1, 237:51.5, 238:51.5

### Frame 236

- **frame_ms:** 54.118
- **stream_ms / apply / unload:** 43.257 / 32.694 / 0.008
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
- **Kontext davor:** 233:49.8, 234:50.2, 235:52.9
- **Kontext danach:** 237:51.5, 238:51.5, 239:53.5

### Frame 237

- **frame_ms:** 51.463
- **stream_ms / apply / unload:** 41.373 / 30.656 / 0.008
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
- **Kontext davor:** 234:50.2, 235:52.9, 236:54.1
- **Kontext danach:** 238:51.5, 239:53.5, 240:55.4

### Frame 238

- **frame_ms:** 51.475
- **stream_ms / apply / unload:** 41.958 / 31.384 / 0.008
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
- **Kontext davor:** 235:52.9, 236:54.1, 237:51.5
- **Kontext danach:** 239:53.5, 240:55.4, 241:51.0

### Frame 239

- **frame_ms:** 53.478
- **stream_ms / apply / unload:** 43.063 / 32.969 / 0.007
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
- **Kontext davor:** 236:54.1, 237:51.5, 238:51.5
- **Kontext danach:** 240:55.4, 241:51.0, 242:54.0

### Frame 240

- **frame_ms:** 55.410
- **stream_ms / apply / unload:** 44.264 / 33.410 / 0.008
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
- **Kontext davor:** 237:51.5, 238:51.5, 239:53.5
- **Kontext danach:** 241:51.0, 242:54.0, 243:50.5

### Frame 241

- **frame_ms:** 51.023
- **stream_ms / apply / unload:** 40.950 / 29.849 / 0.008
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
- **Kontext davor:** 238:51.5, 239:53.5, 240:55.4
- **Kontext danach:** 242:54.0, 243:50.5, 244:54.3

### Frame 242

- **frame_ms:** 53.988
- **stream_ms / apply / unload:** 44.288 / 32.807 / 0.008
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
- **Kontext davor:** 239:53.5, 240:55.4, 241:51.0
- **Kontext danach:** 243:50.5, 244:54.3, 245:51.8

### Frame 243

- **frame_ms:** 50.457
- **stream_ms / apply / unload:** 41.172 / 31.061 / 0.008
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
- **Kontext davor:** 240:55.4, 241:51.0, 242:54.0
- **Kontext danach:** 244:54.3, 245:51.8, 246:51.7

### Frame 244

- **frame_ms:** 54.275
- **stream_ms / apply / unload:** 45.125 / 34.369 / 0.008
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
- **Kontext davor:** 241:51.0, 242:54.0, 243:50.5
- **Kontext danach:** 245:51.8, 246:51.7, 247:53.6

### Frame 245

- **frame_ms:** 51.800
- **stream_ms / apply / unload:** 42.429 / 32.393 / 0.009
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
- **Kontext davor:** 242:54.0, 243:50.5, 244:54.3
- **Kontext danach:** 246:51.7, 247:53.6, 248:54.1

### Frame 246

- **frame_ms:** 51.696
- **stream_ms / apply / unload:** 41.871 / 30.573 / 0.009
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
- **Kontext davor:** 243:50.5, 244:54.3, 245:51.8
- **Kontext danach:** 247:53.6, 248:54.1, 249:52.2

### Frame 247

- **frame_ms:** 53.561
- **stream_ms / apply / unload:** 43.643 / 32.277 / 0.008
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
- **Kontext davor:** 244:54.3, 245:51.8, 246:51.7
- **Kontext danach:** 248:54.1, 249:52.2, 250:53.0

### Frame 248

- **frame_ms:** 54.104
- **stream_ms / apply / unload:** 44.077 / 32.509 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 245:51.8, 246:51.7, 247:53.6
- **Kontext danach:** 249:52.2, 250:53.0, 251:51.2

### Frame 249

- **frame_ms:** 52.195
- **stream_ms / apply / unload:** 42.745 / 32.296 / 0.008
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
- **Kontext davor:** 246:51.7, 247:53.6, 248:54.1
- **Kontext danach:** 250:53.0, 251:51.2, 252:60.6

### Frame 250

- **frame_ms:** 52.980
- **stream_ms / apply / unload:** 43.230 / 32.377 / 0.008
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
- **Kontext davor:** 247:53.6, 248:54.1, 249:52.2
- **Kontext danach:** 251:51.2, 252:60.6, 253:52.9

### Frame 251

- **frame_ms:** 51.152
- **stream_ms / apply / unload:** 41.383 / 31.010 / 0.008
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
- **Kontext davor:** 248:54.1, 249:52.2, 250:53.0
- **Kontext danach:** 252:60.6, 253:52.9, 254:53.5

### Frame 252

- **frame_ms:** 60.584
- **stream_ms / apply / unload:** 40.090 / 30.393 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 50.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 249:52.2, 250:53.0, 251:51.2
- **Kontext danach:** 253:52.9, 254:53.5, 255:53.2

### Frame 253

- **frame_ms:** 52.915
- **stream_ms / apply / unload:** 43.834 / 33.291 / 0.007
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
- **Kontext davor:** 250:53.0, 251:51.2, 252:60.6
- **Kontext danach:** 254:53.5, 255:53.2, 256:50.7

### Frame 254

- **frame_ms:** 53.476
- **stream_ms / apply / unload:** 43.382 / 33.229 / 0.007
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
- **Kontext davor:** 251:51.2, 252:60.6, 253:52.9
- **Kontext danach:** 255:53.2, 256:50.7, 257:52.0

### Frame 255

- **frame_ms:** 53.213
- **stream_ms / apply / unload:** 43.088 / 32.838 / 0.009
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
- **Kontext davor:** 252:60.6, 253:52.9, 254:53.5
- **Kontext danach:** 256:50.7, 257:52.0, 258:50.5

### Frame 256

- **frame_ms:** 50.726
- **stream_ms / apply / unload:** 41.270 / 30.377 / 0.006
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
- **Kontext davor:** 253:52.9, 254:53.5, 255:53.2
- **Kontext danach:** 257:52.0, 258:50.5, 259:51.0

### Frame 257

- **frame_ms:** 51.992
- **stream_ms / apply / unload:** 41.438 / 30.353 / 0.008
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
- **Kontext davor:** 254:53.5, 255:53.2, 256:50.7
- **Kontext danach:** 258:50.5, 259:51.0, 260:52.2

### Frame 258

- **frame_ms:** 50.457
- **stream_ms / apply / unload:** 41.401 / 30.515 / 0.008
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
- **Kontext davor:** 255:53.2, 256:50.7, 257:52.0
- **Kontext danach:** 259:51.0, 260:52.2, 261:51.8

### Frame 259

- **frame_ms:** 50.972
- **stream_ms / apply / unload:** 41.087 / 31.158 / 0.008
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
- **Kontext davor:** 256:50.7, 257:52.0, 258:50.5
- **Kontext danach:** 260:52.2, 261:51.8, 262:53.9

### Frame 260

- **frame_ms:** 52.179
- **stream_ms / apply / unload:** 42.881 / 32.417 / 0.007
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
- **Kontext davor:** 257:52.0, 258:50.5, 259:51.0
- **Kontext danach:** 261:51.8, 262:53.9, 263:50.8

### Frame 261

- **frame_ms:** 51.799
- **stream_ms / apply / unload:** 42.198 / 31.595 / 0.007
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
- **Kontext davor:** 258:50.5, 259:51.0, 260:52.2
- **Kontext danach:** 262:53.9, 263:50.8, 264:50.9

### Frame 262

- **frame_ms:** 53.932
- **stream_ms / apply / unload:** 44.413 / 32.948 / 0.007
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
- **Kontext davor:** 259:51.0, 260:52.2, 261:51.8
- **Kontext danach:** 263:50.8, 264:50.9, 265:52.1

### Frame 263

- **frame_ms:** 50.791
- **stream_ms / apply / unload:** 41.514 / 31.623 / 0.008
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
- **Kontext davor:** 260:52.2, 261:51.8, 262:53.9
- **Kontext danach:** 264:50.9, 265:52.1, 266:51.5

### Frame 264

- **frame_ms:** 50.921
- **stream_ms / apply / unload:** 41.658 / 30.986 / 0.008
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
- **Kontext davor:** 261:51.8, 262:53.9, 263:50.8
- **Kontext danach:** 265:52.1, 266:51.5, 267:51.9

### Frame 265

- **frame_ms:** 52.066
- **stream_ms / apply / unload:** 42.775 / 32.197 / 0.007
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
- **Kontext davor:** 262:53.9, 263:50.8, 264:50.9
- **Kontext danach:** 266:51.5, 267:51.9, 268:50.7

### Frame 266

- **frame_ms:** 51.487
- **stream_ms / apply / unload:** 42.160 / 31.763 / 0.008
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
- **Kontext davor:** 263:50.8, 264:50.9, 265:52.1
- **Kontext danach:** 267:51.9, 268:50.7, 269:50.2

### Frame 267

- **frame_ms:** 51.903
- **stream_ms / apply / unload:** 42.309 / 31.732 / 0.009
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
- **Kontext davor:** 264:50.9, 265:52.1, 266:51.5
- **Kontext danach:** 268:50.7, 269:50.2, 270:53.2

### Frame 268

- **frame_ms:** 50.692
- **stream_ms / apply / unload:** 41.500 / 31.048 / 0.008
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
- **Kontext davor:** 265:52.1, 266:51.5, 267:51.9
- **Kontext danach:** 269:50.2, 270:53.2, 271:50.0

### Frame 269

- **frame_ms:** 50.242
- **stream_ms / apply / unload:** 41.339 / 31.223 / 0.008
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
- **Kontext davor:** 266:51.5, 267:51.9, 268:50.7
- **Kontext danach:** 270:53.2, 271:50.0, 272:52.6

### Frame 270

- **frame_ms:** 53.183
- **stream_ms / apply / unload:** 42.599 / 32.649 / 0.007
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
- **Kontext davor:** 267:51.9, 268:50.7, 269:50.2
- **Kontext danach:** 271:50.0, 272:52.6, 273:51.8

### Frame 271

- **frame_ms:** 49.976
- **stream_ms / apply / unload:** 40.996 / 31.142 / 0.008
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
- **Kontext davor:** 268:50.7, 269:50.2, 270:53.2
- **Kontext danach:** 272:52.6, 273:51.8, 274:52.2

### Frame 272

- **frame_ms:** 52.576
- **stream_ms / apply / unload:** 43.508 / 32.516 / 0.007
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
- **Kontext davor:** 269:50.2, 270:53.2, 271:50.0
- **Kontext danach:** 273:51.8, 274:52.2, 275:52.3

### Frame 273

- **frame_ms:** 51.804
- **stream_ms / apply / unload:** 42.800 / 32.318 / 0.008
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
- **Kontext davor:** 270:53.2, 271:50.0, 272:52.6
- **Kontext danach:** 274:52.2, 275:52.3, 276:51.6

### Frame 274

- **frame_ms:** 52.153
- **stream_ms / apply / unload:** 42.688 / 31.923 / 0.008
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
- **Kontext davor:** 271:50.0, 272:52.6, 273:51.8
- **Kontext danach:** 275:52.3, 276:51.6, 277:53.3

### Frame 275

- **frame_ms:** 52.296
- **stream_ms / apply / unload:** 43.287 / 32.112 / 0.008
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
- **Kontext davor:** 272:52.6, 273:51.8, 274:52.2
- **Kontext danach:** 276:51.6, 277:53.3, 278:52.8

### Frame 276

- **frame_ms:** 51.553
- **stream_ms / apply / unload:** 40.695 / 30.810 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 273:51.8, 274:52.2, 275:52.3
- **Kontext danach:** 277:53.3, 278:52.8, 279:51.0

### Frame 277

- **frame_ms:** 53.330
- **stream_ms / apply / unload:** 43.895 / 33.090 / 0.008
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
- **Kontext davor:** 274:52.2, 275:52.3, 276:51.6
- **Kontext danach:** 278:52.8, 279:51.0, 280:54.6

### Frame 278

- **frame_ms:** 52.771
- **stream_ms / apply / unload:** 42.536 / 32.494 / 0.007
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
- **Kontext davor:** 275:52.3, 276:51.6, 277:53.3
- **Kontext danach:** 279:51.0, 280:54.6, 281:51.3

### Frame 279

- **frame_ms:** 50.964
- **stream_ms / apply / unload:** 41.991 / 31.436 / 0.007
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
- **Kontext davor:** 276:51.6, 277:53.3, 278:52.8
- **Kontext danach:** 280:54.6, 281:51.3, 282:55.0

### Frame 280

- **frame_ms:** 54.560
- **stream_ms / apply / unload:** 44.218 / 33.091 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 277:53.3, 278:52.8, 279:51.0
- **Kontext danach:** 281:51.3, 282:55.0, 283:54.4

### Frame 281

- **frame_ms:** 51.328
- **stream_ms / apply / unload:** 41.676 / 31.366 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 278:52.8, 279:51.0, 280:54.6
- **Kontext danach:** 282:55.0, 283:54.4, 284:53.5

### Frame 282

- **frame_ms:** 54.955
- **stream_ms / apply / unload:** 45.432 / 34.371 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 279:51.0, 280:54.6, 281:51.3
- **Kontext danach:** 283:54.4, 284:53.5, 285:52.6

### Frame 283

- **frame_ms:** 54.407
- **stream_ms / apply / unload:** 44.695 / 33.502 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 280:54.6, 281:51.3, 282:55.0
- **Kontext danach:** 284:53.5, 285:52.6, 286:53.3

### Frame 284

- **frame_ms:** 53.530
- **stream_ms / apply / unload:** 43.782 / 32.256 / 0.009
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 281:51.3, 282:55.0, 283:54.4
- **Kontext danach:** 285:52.6, 286:53.3, 287:53.2

### Frame 285

- **frame_ms:** 52.630
- **stream_ms / apply / unload:** 42.917 / 32.030 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 282:55.0, 283:54.4, 284:53.5
- **Kontext danach:** 286:53.3, 287:53.2, 288:54.3

### Frame 286

- **frame_ms:** 53.327
- **stream_ms / apply / unload:** 43.227 / 32.850 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 283:54.4, 284:53.5, 285:52.6
- **Kontext danach:** 287:53.2, 288:54.3, 289:54.2

### Frame 287

- **frame_ms:** 53.241
- **stream_ms / apply / unload:** 44.295 / 33.668 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 63.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 284:53.5, 285:52.6, 286:53.3
- **Kontext danach:** 288:54.3, 289:54.2, 290:52.2

### Frame 288

- **frame_ms:** 54.327
- **stream_ms / apply / unload:** 43.217 / 32.467 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 285:52.6, 286:53.3, 287:53.2
- **Kontext danach:** 289:54.2, 290:52.2, 291:52.2

### Frame 289

- **frame_ms:** 54.224
- **stream_ms / apply / unload:** 44.530 / 32.917 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 286:53.3, 287:53.2, 288:54.3
- **Kontext danach:** 290:52.2, 291:52.2, 292:53.9

### Frame 290

- **frame_ms:** 52.164
- **stream_ms / apply / unload:** 42.676 / 32.118 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 287:53.2, 288:54.3, 289:54.2
- **Kontext danach:** 291:52.2, 292:53.9, 293:52.6

### Frame 291

- **frame_ms:** 52.184
- **stream_ms / apply / unload:** 42.062 / 31.516 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 288:54.3, 289:54.2, 290:52.2
- **Kontext danach:** 292:53.9, 293:52.6, 294:52.2

### Frame 292

- **frame_ms:** 53.913
- **stream_ms / apply / unload:** 44.106 / 33.412 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 289:54.2, 290:52.2, 291:52.2
- **Kontext danach:** 293:52.6, 294:52.2, 295:52.3

### Frame 293

- **frame_ms:** 52.637
- **stream_ms / apply / unload:** 43.032 / 31.953 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 290:52.2, 291:52.2, 292:53.9
- **Kontext danach:** 294:52.2, 295:52.3, 296:51.3

### Frame 294

- **frame_ms:** 52.212
- **stream_ms / apply / unload:** 42.674 / 31.923 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 291:52.2, 292:53.9, 293:52.6
- **Kontext danach:** 295:52.3, 296:51.3, 297:50.9

### Frame 295

- **frame_ms:** 52.265
- **stream_ms / apply / unload:** 42.332 / 31.707 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 292:53.9, 293:52.6, 294:52.2
- **Kontext danach:** 296:51.3, 297:50.9, 298:51.5

### Frame 296

- **frame_ms:** 51.279
- **stream_ms / apply / unload:** 41.450 / 30.960 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 293:52.6, 294:52.2, 295:52.3
- **Kontext danach:** 297:50.9, 298:51.5, 299:53.4

### Frame 297

- **frame_ms:** 50.881
- **stream_ms / apply / unload:** 40.755 / 30.793 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 294:52.2, 295:52.3, 296:51.3
- **Kontext danach:** 298:51.5, 299:53.4

### Frame 298

- **frame_ms:** 51.532
- **stream_ms / apply / unload:** 42.312 / 31.952 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 295:52.3, 296:51.3, 297:50.9
- **Kontext danach:** 299:53.4

### Frame 299

- **frame_ms:** 53.389
- **stream_ms / apply / unload:** 43.399 / 32.807 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 296:51.3, 297:50.9, 298:51.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 51.379 | 51.893 | 58.351 | 106.903 |
| stream_ms | 42.059 | 42.312 | 46.791 | 88.070 |
| stream_apply_ms | 31.429 | 31.702 | 34.907 | 63.780 |
| stream_unload_ms | 0.008 | 0.008 | 0.009 | 0.051 |
| stream_loaded | 0.043 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 15.410 | 16.000 | 16.000 | 16.000 |
| zoom | 0.350 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 9.109 | 9.315 | 10.584 | 20.280 |
| tile_extract_ms | 0.188 | 0.180 | 0.229 | 1.179 |
| extract_ms | 9.297 | 9.504 | 10.835 | 20.472 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 51.401 | 51.915 | 58.373 | 106.924 |
| cpu_unattributed_ms | 0.021 | 0.021 | 0.023 | 0.095 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.979, n=300): Pearson r=0.979 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_apply_ms** (r=0.961, n=300): Pearson r=0.961 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unload_ms** (r=0.245, n=300): Pearson r=0.245 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_loaded** (r=-0.267, n=300): Pearson r=-0.267 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.601, n=300): Pearson r=0.601 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ zoom** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.827, n=300): Pearson r=0.827 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ tile_extract_ms** (r=0.246, n=300): Pearson r=0.246 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ extract_ms** (r=0.829, n=300): Pearson r=0.829 (stark) — nur Indiz, keine Kausalität.
- **cpu_full_frame_ms ↔ stream_ms** (r=0.979, n=300): Pearson r=0.979 (stark) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.829, n=300): Pearson r=0.829 (stark) zwischen cpu_full_frame_ms und extract_ms.
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
- Durchschnittlicher Anteil an frame_ms: Stream 81.9%, Apply 61.2%, Unload 0.0%, Extract 18.1%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 17.9%.
- Häufigstes Hitch-Muster: periodic_cluster (300×).
