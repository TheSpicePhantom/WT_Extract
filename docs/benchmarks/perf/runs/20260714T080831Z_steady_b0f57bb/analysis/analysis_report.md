# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T080831Z_steady_b0f57bb`
- **scenario_id:** `steady`
- **run_mode:** `cli`
- **recorded_frames:** 300
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T08:08:34.895738+00:00
- **git_commit:** b0f57bb

### Config-Fingerprints

- `profiling`: `-3649097159505803740`
- `streaming`: `5259473258370463336`
- `visibility_lod`: `4227292874147130016`
- `world_gen`: `-9026376527574192949`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 9.5460 | 9.5460 | +0.0000 | OK |
| frame_ms_p95 | 18.2139 | 18.2139 | +0.0000 | OK |
| frame_ms_max | 41.9559 | 41.9559 | +0.0000 | OK |
| stream_ms_mean | 6.8710 | 6.8710 | +0.0000 | OK |
| stream_ms_p95 | 16.7473 | 16.7473 | +0.0000 | OK |
| stream_ms_max | 40.1285 | 40.1285 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0046 | 0.0046 | +0.0000 | OK |
| stream_unload_ms_max | 0.0109 | 0.0109 | +0.0000 | OK |
| chunk_count_mean | 13.9533 | 13.9533 | +0.0000 | OK |
| recorded_frames | 300.0000 | 300.0000 | +0.0000 | OK |
| hitch_count | 90.0000 | 90.0000 | +0.0000 | OK |
| hitch_frame_count | 27.0000 | 27.0000 | +0.0000 | OK |
| hitch_stream_count | 90.0000 | 90.0000 | +0.0000 | OK |
| hitch_load_count | 1.0000 | 1.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Nicht eindeutig** (dominant_bottleneck, Konfidenz: hoch)
   - In 73/90 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 72.0% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: extract_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 27.9% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (41.96) deutlich über P95 (18.21) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `stream_slow`: 90
- `frame_slow`: 27
- `load_burst`: 1

### Frame 0

- **frame_ms:** 29.664
- **stream_ms / apply / unload:** 27.027 / 19.390 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 65.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:18.5, 2:16.9, 3:9.9

### Frame 1

- **frame_ms:** 18.478
- **stream_ms / apply / unload:** 18.350 / 9.256 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 50.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:29.7
- **Kontext danach:** 2:16.9, 3:9.9, 4:14.1

### Frame 2

- **frame_ms:** 16.891
- **stream_ms / apply / unload:** 16.774 / 8.438 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 50.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:29.7, 1:18.5
- **Kontext danach:** 3:9.9, 4:14.1, 5:16.5

### Frame 3

- **frame_ms:** 9.949
- **stream_ms / apply / unload:** 9.872 / 4.671 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 47.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:29.7, 1:18.5, 2:16.9
- **Kontext danach:** 4:14.1, 5:16.5, 6:16.2

### Frame 4

- **frame_ms:** 14.140
- **stream_ms / apply / unload:** 14.033 / 8.214 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:18.5, 2:16.9, 3:9.9
- **Kontext danach:** 5:16.5, 6:16.2, 7:18.8

### Frame 5

- **frame_ms:** 16.512
- **stream_ms / apply / unload:** 16.394 / 8.237 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:16.9, 3:9.9, 4:14.1
- **Kontext danach:** 6:16.2, 7:18.8, 8:16.9

### Frame 6

- **frame_ms:** 16.177
- **stream_ms / apply / unload:** 16.053 / 7.786 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 48.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:9.9, 4:14.1, 5:16.5
- **Kontext danach:** 7:18.8, 8:16.9, 9:16.5

### Frame 7

- **frame_ms:** 18.791
- **stream_ms / apply / unload:** 18.676 / 9.289 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:14.1, 5:16.5, 6:16.2
- **Kontext danach:** 8:16.9, 9:16.5, 10:16.6

### Frame 8

- **frame_ms:** 16.860
- **stream_ms / apply / unload:** 16.747 / 8.362 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:16.5, 6:16.2, 7:18.8
- **Kontext danach:** 9:16.5, 10:16.6, 11:12.9

### Frame 9

- **frame_ms:** 16.526
- **stream_ms / apply / unload:** 16.415 / 8.325 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 50.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:16.2, 7:18.8, 8:16.9
- **Kontext danach:** 10:16.6, 11:12.9, 12:9.5

### Frame 10

- **frame_ms:** 16.636
- **stream_ms / apply / unload:** 16.551 / 8.359 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 50.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:18.8, 8:16.9, 9:16.5
- **Kontext danach:** 11:12.9, 12:9.5, 13:13.7

### Frame 11

- **frame_ms:** 12.940
- **stream_ms / apply / unload:** 12.828 / 8.364 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 64.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:16.9, 9:16.5, 10:16.6
- **Kontext danach:** 12:9.5, 13:13.7, 14:14.9

### Frame 12

- **frame_ms:** 9.464
- **stream_ms / apply / unload:** 9.388 / 4.723 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:16.5, 10:16.6, 11:12.9
- **Kontext danach:** 13:13.7, 14:14.9, 15:18.4

### Frame 13

- **frame_ms:** 13.731
- **stream_ms / apply / unload:** 13.604 / 8.481 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:16.6, 11:12.9, 12:9.5
- **Kontext danach:** 14:14.9, 15:18.4, 16:18.3

### Frame 14

- **frame_ms:** 14.943
- **stream_ms / apply / unload:** 14.814 / 6.924 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 46.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:12.9, 12:9.5, 13:13.7
- **Kontext danach:** 15:18.4, 16:18.3, 17:14.1

### Frame 15

- **frame_ms:** 18.386
- **stream_ms / apply / unload:** 18.261 / 9.082 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:9.5, 13:13.7, 14:14.9
- **Kontext danach:** 16:18.3, 17:14.1, 18:13.7

### Frame 16

- **frame_ms:** 18.309
- **stream_ms / apply / unload:** 18.188 / 8.977 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:13.7, 14:14.9, 15:18.4
- **Kontext danach:** 17:14.1, 18:13.7, 19:15.1

### Frame 17

- **frame_ms:** 14.097
- **stream_ms / apply / unload:** 14.021 / 6.013 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 42.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:14.9, 15:18.4, 16:18.3
- **Kontext danach:** 18:13.7, 19:15.1, 20:42.0

### Frame 18

- **frame_ms:** 13.673
- **stream_ms / apply / unload:** 13.572 / 7.525 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:18.4, 16:18.3, 17:14.1
- **Kontext danach:** 19:15.1, 20:42.0, 21:14.9

### Frame 19

- **frame_ms:** 15.080
- **stream_ms / apply / unload:** 14.976 / 7.450 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 1 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:18.3, 17:14.1, 18:13.7
- **Kontext danach:** 20:42.0, 21:14.9, 22:13.1

### Frame 20

- **frame_ms:** 41.956
- **stream_ms / apply / unload:** 38.591 / 29.390 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 2 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Burst mit Nachlauf
  - Hitch frame_ms (41.96) deutlich über Nachbar-Mittel (14.82).
  - Weitere Hitches in ±3 Frames: [17, 18, 19, 21, 22, 23].
- **Kontext davor:** 17:14.1, 18:13.7, 19:15.1
- **Kontext danach:** 21:14.9, 22:13.1, 23:18.1

### Frame 21

- **frame_ms:** 14.905
- **stream_ms / apply / unload:** 14.360 / 5.144 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 2 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 18:13.7, 19:15.1, 20:42.0
- **Kontext danach:** 22:13.1, 23:18.1, 24:33.2

### Frame 22

- **frame_ms:** 13.091
- **stream_ms / apply / unload:** 12.168 / 7.614 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 2 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 19:15.1, 20:42.0, 21:14.9
- **Kontext danach:** 23:18.1, 24:33.2, 25:41.1

### Frame 23

- **frame_ms:** 18.096
- **stream_ms / apply / unload:** 17.538 / 8.590 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 2 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 47.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 20:42.0, 21:14.9, 22:13.1
- **Kontext danach:** 24:33.2, 25:41.1, 26:19.1

### Frame 24

- **frame_ms:** 33.155
- **stream_ms / apply / unload:** 29.365 / 23.402 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 4 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 70.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 21:14.9, 22:13.1, 23:18.1
- **Kontext danach:** 25:41.1, 26:19.1, 27:18.7

### Frame 25

- **frame_ms:** 41.073
- **stream_ms / apply / unload:** 40.128 / 30.650 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 4 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 22:13.1, 23:18.1, 24:33.2
- **Kontext danach:** 26:19.1, 27:18.7, 28:17.1

### Frame 26

- **frame_ms:** 19.149
- **stream_ms / apply / unload:** 17.427 / 7.606 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 5 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 23:18.1, 24:33.2, 25:41.1
- **Kontext danach:** 27:18.7, 28:17.1, 29:25.1

### Frame 27

- **frame_ms:** 18.655
- **stream_ms / apply / unload:** 16.856 / 8.771 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 6 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 47.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 24:33.2, 25:41.1, 26:19.1
- **Kontext danach:** 28:17.1, 29:25.1, 30:9.8

### Frame 28

- **frame_ms:** 17.052
- **stream_ms / apply / unload:** 15.327 / 7.679 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 6 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 45.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:41.1, 26:19.1, 27:18.7
- **Kontext danach:** 29:25.1, 30:9.8, 31:18.3

### Frame 29

- **frame_ms:** 25.129
- **stream_ms / apply / unload:** 22.461 / 15.007 / 0.004
- **stream_loaded / unloaded:** 3 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:19.1, 27:18.7, 28:17.1
- **Kontext danach:** 30:9.8, 31:18.3, 32:18.2

### Frame 30

- **frame_ms:** 9.825
- **stream_ms / apply / unload:** 8.819 / 4.371 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 44.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 27:18.7, 28:17.1, 29:25.1
- **Kontext danach:** 31:18.3, 32:18.2, 33:21.0

### Frame 31

- **frame_ms:** 18.293
- **stream_ms / apply / unload:** 16.395 / 8.237 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 45.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 28:17.1, 29:25.1, 30:9.8
- **Kontext danach:** 32:18.2, 33:21.0, 34:19.1

### Frame 32

- **frame_ms:** 18.214
- **stream_ms / apply / unload:** 16.297 / 8.221 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 8 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 45.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 29:25.1, 30:9.8, 31:18.3
- **Kontext danach:** 33:21.0, 34:19.1, 35:18.6

### Frame 33

- **frame_ms:** 21.019
- **stream_ms / apply / unload:** 18.654 / 10.399 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 9 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:9.8, 31:18.3, 32:18.2
- **Kontext danach:** 34:19.1, 35:18.6, 36:10.7

### Frame 34

- **frame_ms:** 19.087
- **stream_ms / apply / unload:** 16.918 / 8.321 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 11 / 0.3500
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 43.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 31:18.3, 32:18.2, 33:21.0
- **Kontext danach:** 35:18.6, 36:10.7, 37:10.5

### Frame 35

- **frame_ms:** 18.636
- **stream_ms / apply / unload:** 16.400 / 10.019 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:18.2, 33:21.0, 34:19.1
- **Kontext danach:** 36:10.7, 37:10.5, 38:11.2

### Frame 36

- **frame_ms:** 10.723
- **stream_ms / apply / unload:** 8.573 / 4.258 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:21.0, 34:19.1, 35:18.6
- **Kontext danach:** 37:10.5, 38:11.2, 39:11.1

### Frame 37

- **frame_ms:** 10.540
- **stream_ms / apply / unload:** 8.372 / 4.248 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 34:19.1, 35:18.6, 36:10.7
- **Kontext danach:** 38:11.2, 39:11.1, 40:11.3

### Frame 38

- **frame_ms:** 11.203
- **stream_ms / apply / unload:** 8.803 / 4.610 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 41.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 35:18.6, 36:10.7, 37:10.5
- **Kontext danach:** 39:11.1, 40:11.3, 41:11.1

### Frame 39

- **frame_ms:** 11.077
- **stream_ms / apply / unload:** 8.730 / 4.511 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 36:10.7, 37:10.5, 38:11.2
- **Kontext danach:** 40:11.3, 41:11.1, 42:11.2

### Frame 40

- **frame_ms:** 11.279
- **stream_ms / apply / unload:** 8.933 / 4.483 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 37:10.5, 38:11.2, 39:11.1
- **Kontext danach:** 41:11.1, 42:11.2, 43:10.9

### Frame 41

- **frame_ms:** 11.093
- **stream_ms / apply / unload:** 8.750 / 4.576 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 41.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 38:11.2, 39:11.1, 40:11.3
- **Kontext danach:** 42:11.2, 43:10.9, 44:10.8

### Frame 42

- **frame_ms:** 11.172
- **stream_ms / apply / unload:** 8.740 / 4.489 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 39:11.1, 40:11.3, 41:11.1
- **Kontext danach:** 43:10.9, 44:10.8, 45:10.5

### Frame 43

- **frame_ms:** 10.861
- **stream_ms / apply / unload:** 8.664 / 4.303 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 40:11.3, 41:11.1, 42:11.2
- **Kontext danach:** 44:10.8, 45:10.5, 46:10.8

### Frame 44

- **frame_ms:** 10.791
- **stream_ms / apply / unload:** 8.572 / 4.302 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 41:11.1, 42:11.2, 43:10.9
- **Kontext danach:** 45:10.5, 46:10.8, 47:11.0

### Frame 45

- **frame_ms:** 10.532
- **stream_ms / apply / unload:** 8.369 / 4.210 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 42:11.2, 43:10.9, 44:10.8
- **Kontext danach:** 46:10.8, 47:11.0, 48:11.6

### Frame 46

- **frame_ms:** 10.767
- **stream_ms / apply / unload:** 8.436 / 4.232 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 43:10.9, 44:10.8, 45:10.5
- **Kontext danach:** 47:11.0, 48:11.6, 49:11.4

### Frame 47

- **frame_ms:** 11.035
- **stream_ms / apply / unload:** 8.869 / 4.522 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 41.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 44:10.8, 45:10.5, 46:10.8
- **Kontext danach:** 48:11.6, 49:11.4, 50:11.2

### Frame 48

- **frame_ms:** 11.637
- **stream_ms / apply / unload:** 9.344 / 4.989 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 42.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 45:10.5, 46:10.8, 47:11.0
- **Kontext danach:** 49:11.4, 50:11.2, 51:11.0

### Frame 49

- **frame_ms:** 11.391
- **stream_ms / apply / unload:** 8.956 / 4.654 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 46:10.8, 47:11.0, 48:11.6
- **Kontext danach:** 50:11.2, 51:11.0, 52:11.1

### Frame 50

- **frame_ms:** 11.215
- **stream_ms / apply / unload:** 8.846 / 4.555 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 47:11.0, 48:11.6, 49:11.4
- **Kontext danach:** 51:11.0, 52:11.1, 53:10.8

### Frame 51

- **frame_ms:** 10.960
- **stream_ms / apply / unload:** 8.692 / 4.329 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 48:11.6, 49:11.4, 50:11.2
- **Kontext danach:** 52:11.1, 53:10.8, 54:10.9

### Frame 52

- **frame_ms:** 11.132
- **stream_ms / apply / unload:** 8.709 / 4.444 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 49:11.4, 50:11.2, 51:11.0
- **Kontext danach:** 53:10.8, 54:10.9, 55:11.1

### Frame 53

- **frame_ms:** 10.763
- **stream_ms / apply / unload:** 8.604 / 4.399 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 50:11.2, 51:11.0, 52:11.1
- **Kontext danach:** 54:10.9, 55:11.1, 56:11.6

### Frame 54

- **frame_ms:** 10.925
- **stream_ms / apply / unload:** 8.715 / 4.302 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 51:11.0, 52:11.1, 53:10.8
- **Kontext danach:** 55:11.1, 56:11.6, 57:10.7

### Frame 55

- **frame_ms:** 11.051
- **stream_ms / apply / unload:** 8.854 / 4.636 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 42.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 52:11.1, 53:10.8, 54:10.9
- **Kontext danach:** 56:11.6, 57:10.7, 58:10.7

### Frame 56

- **frame_ms:** 11.597
- **stream_ms / apply / unload:** 9.317 / 4.644 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 53:10.8, 54:10.9, 55:11.1
- **Kontext danach:** 57:10.7, 58:10.7, 59:10.5

### Frame 57

- **frame_ms:** 10.655
- **stream_ms / apply / unload:** 8.491 / 4.284 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 54:10.9, 55:11.1, 56:11.6
- **Kontext danach:** 58:10.7, 59:10.5, 60:10.7

### Frame 58

- **frame_ms:** 10.654
- **stream_ms / apply / unload:** 8.469 / 4.237 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 55:11.1, 56:11.6, 57:10.7
- **Kontext danach:** 59:10.5, 60:10.7, 61:13.2

### Frame 59

- **frame_ms:** 10.503
- **stream_ms / apply / unload:** 8.348 / 4.209 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 56:11.6, 57:10.7, 58:10.7
- **Kontext danach:** 60:10.7, 61:13.2, 62:11.6

### Frame 60

- **frame_ms:** 10.723
- **stream_ms / apply / unload:** 8.512 / 4.316 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 12 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 57:10.7, 58:10.7, 59:10.5
- **Kontext danach:** 61:13.2, 62:11.6, 63:11.8

### Frame 61

- **frame_ms:** 13.212
- **stream_ms / apply / unload:** 9.972 / 5.084 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 58:10.7, 59:10.5, 60:10.7
- **Kontext danach:** 62:11.6, 63:11.8, 64:11.4

### Frame 62

- **frame_ms:** 11.614
- **stream_ms / apply / unload:** 8.692 / 4.401 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 59:10.5, 60:10.7, 61:13.2
- **Kontext danach:** 63:11.8, 64:11.4, 65:11.3

### Frame 63

- **frame_ms:** 11.825
- **stream_ms / apply / unload:** 8.766 / 4.467 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 60:10.7, 61:13.2, 62:11.6
- **Kontext danach:** 64:11.4, 65:11.3, 66:11.0

### Frame 64

- **frame_ms:** 11.415
- **stream_ms / apply / unload:** 8.558 / 4.179 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 36.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 61:13.2, 62:11.6, 63:11.8
- **Kontext danach:** 65:11.3, 66:11.0, 67:11.2

### Frame 65

- **frame_ms:** 11.286
- **stream_ms / apply / unload:** 8.430 / 4.253 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 62:11.6, 63:11.8, 64:11.4
- **Kontext danach:** 66:11.0, 67:11.2, 68:11.2

### Frame 66

- **frame_ms:** 11.041
- **stream_ms / apply / unload:** 8.201 / 4.107 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 63:11.8, 64:11.4, 65:11.3
- **Kontext danach:** 67:11.2, 68:11.2, 69:11.2

### Frame 67

- **frame_ms:** 11.238
- **stream_ms / apply / unload:** 8.309 / 4.205 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 64:11.4, 65:11.3, 66:11.0
- **Kontext danach:** 68:11.2, 69:11.2, 70:11.3

### Frame 68

- **frame_ms:** 11.185
- **stream_ms / apply / unload:** 8.345 / 4.167 / 0.003
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 65:11.3, 66:11.0, 67:11.2
- **Kontext danach:** 69:11.2, 70:11.3, 71:11.8

### Frame 69

- **frame_ms:** 11.232
- **stream_ms / apply / unload:** 8.375 / 4.264 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 66:11.0, 67:11.2, 68:11.2
- **Kontext danach:** 70:11.3, 71:11.8, 72:11.5

### Frame 70

- **frame_ms:** 11.309
- **stream_ms / apply / unload:** 8.472 / 4.373 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 67:11.2, 68:11.2, 69:11.2
- **Kontext danach:** 71:11.8, 72:11.5, 73:16.7

### Frame 71

- **frame_ms:** 11.824
- **stream_ms / apply / unload:** 8.862 / 4.468 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 68:11.2, 69:11.2, 70:11.3
- **Kontext danach:** 72:11.5, 73:16.7, 74:11.5

### Frame 72

- **frame_ms:** 11.492
- **stream_ms / apply / unload:** 8.614 / 4.283 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 13 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 69:11.2, 70:11.3, 71:11.8
- **Kontext danach:** 73:16.7, 74:11.5, 75:11.5

### Frame 73

- **frame_ms:** 16.713
- **stream_ms / apply / unload:** 13.869 / 9.592 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 70:11.3, 71:11.8, 72:11.5
- **Kontext danach:** 74:11.5, 75:11.5, 76:11.1

### Frame 74

- **frame_ms:** 11.514
- **stream_ms / apply / unload:** 8.660 / 4.419 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 71:11.8, 72:11.5, 73:16.7
- **Kontext danach:** 75:11.5, 76:11.1, 77:11.6

### Frame 75

- **frame_ms:** 11.531
- **stream_ms / apply / unload:** 8.645 / 4.506 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 72:11.5, 73:16.7, 74:11.5
- **Kontext danach:** 76:11.1, 77:11.6, 78:11.8

### Frame 76

- **frame_ms:** 11.115
- **stream_ms / apply / unload:** 8.292 / 4.150 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 73:16.7, 74:11.5, 75:11.5
- **Kontext danach:** 77:11.6, 78:11.8, 79:11.5

### Frame 77

- **frame_ms:** 11.601
- **stream_ms / apply / unload:** 8.689 / 4.546 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 74:11.5, 75:11.5, 76:11.1
- **Kontext danach:** 78:11.8, 79:11.5, 80:11.6

### Frame 78

- **frame_ms:** 11.840
- **stream_ms / apply / unload:** 8.933 / 4.512 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 75:11.5, 76:11.1, 77:11.6
- **Kontext danach:** 79:11.5, 80:11.6, 81:11.4

### Frame 79

- **frame_ms:** 11.470
- **stream_ms / apply / unload:** 8.473 / 4.348 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 76:11.1, 77:11.6, 78:11.8
- **Kontext danach:** 80:11.6, 81:11.4, 82:17.0

### Frame 80

- **frame_ms:** 11.626
- **stream_ms / apply / unload:** 8.696 / 4.283 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 36.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 77:11.6, 78:11.8, 79:11.5
- **Kontext danach:** 81:11.4, 82:17.0, 83:17.4

### Frame 81

- **frame_ms:** 11.410
- **stream_ms / apply / unload:** 8.541 / 4.206 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 14 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 36.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 78:11.8, 79:11.5, 80:11.6
- **Kontext danach:** 82:17.0, 83:17.4, 84:7.4

### Frame 82

- **frame_ms:** 17.034
- **stream_ms / apply / unload:** 14.022 / 9.586 / 0.004
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 79:11.5, 80:11.6, 81:11.4
- **Kontext danach:** 83:17.4, 84:7.4, 85:7.4

### Frame 83

- **frame_ms:** 17.412
- **stream_ms / apply / unload:** 14.195 / 9.598 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 80:11.6, 81:11.4, 82:17.0
- **Kontext danach:** 84:7.4, 85:7.4, 86:7.3

### Frame 114

- **frame_ms:** 12.307
- **stream_ms / apply / unload:** 9.187 / 4.677 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 111:7.4, 112:7.3, 113:7.4
- **Kontext danach:** 115:7.3, 116:7.6, 117:7.5

### Frame 145

- **frame_ms:** 11.682
- **stream_ms / apply / unload:** 8.839 / 4.439 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 142:7.1, 143:7.8, 144:7.5
- **Kontext danach:** 146:7.4, 147:7.3, 148:7.3

### Frame 176

- **frame_ms:** 11.613
- **stream_ms / apply / unload:** 8.640 / 4.354 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 173:7.4, 174:7.3, 175:7.2
- **Kontext danach:** 177:7.2, 178:7.7, 179:7.3

### Frame 207

- **frame_ms:** 12.064
- **stream_ms / apply / unload:** 9.115 / 4.686 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 38.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 204:7.5, 205:7.1, 206:7.6
- **Kontext danach:** 208:7.3, 209:7.4, 210:7.7

### Frame 238

- **frame_ms:** 11.743
- **stream_ms / apply / unload:** 8.684 / 4.238 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 36.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 235:7.3, 236:7.6, 237:7.5
- **Kontext danach:** 239:7.2, 240:7.6, 241:7.5

### Frame 269

- **frame_ms:** 11.822
- **stream_ms / apply / unload:** 8.983 / 4.486 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 266:7.4, 267:7.6, 268:7.3
- **Kontext danach:** 270:7.7, 271:7.5, 272:7.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 9.546 | 7.562 | 18.214 | 41.956 |
| stream_ms | 6.871 | 4.574 | 16.747 | 40.128 |
| stream_apply_ms | 2.066 | 0.023 | 8.590 | 30.650 |
| stream_unload_ms | 0.004 | 0.004 | 0.005 | 0.011 |
| stream_loaded | 0.083 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 13.953 | 16.000 | 16.000 | 16.000 |
| zoom | 0.350 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 2.547 | 2.800 | 3.061 | 4.004 |
| tile_extract_ms | 0.116 | 0.087 | 0.107 | 2.927 |
| extract_ms | 2.662 | 2.889 | 3.161 | 4.095 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 9.560 | 7.577 | 18.230 | 41.976 |
| cpu_unattributed_ms | 0.014 | 0.013 | 0.018 | 0.085 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.990, n=300): Hitch-Frames: stream_ms-Mittel 12.444 vs. übrige 4.482 (Faktor 2.78). Pearson r=0.990 (stark).
- **frame_ms ↔ stream_apply_ms** (r=0.986, n=300): Hitch-Frames: stream_apply_ms-Mittel 6.832 vs. übrige 0.023 (Faktor 291.79). Pearson r=0.986 (stark).
- **frame_ms ↔ stream_unload_ms** (r=0.259, n=300): Hitch-Frames: stream_unload_ms-Mittel 0.004 vs. übrige 0.004 (Faktor 1.01). Pearson r=0.259 (schwach).
- **frame_ms ↔ stream_loaded** (r=0.582, n=300): Hitch-Frames: stream_loaded-Mittel 0.278 vs. übrige 0.000 (Faktor inf). Pearson r=0.582 (moderat).
- **frame_ms ↔ stream_unloaded** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=-0.739, n=300): Hitch-Frames: chunk_count-Mittel 9.178 vs. übrige 16.000 (Faktor 0.57). Pearson r=-0.739 (stark).
- **frame_ms ↔ zoom** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=300): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=-0.667, n=300): Hitch-Frames: deco_extract_ms-Mittel 1.769 vs. übrige 2.880 (Faktor 0.61). Pearson r=-0.667 (moderat).
- **frame_ms ↔ tile_extract_ms** (r=0.573, n=300): Hitch-Frames: tile_extract_ms-Mittel 0.174 vs. übrige 0.091 (Faktor 1.92). Pearson r=0.573 (moderat).
- **frame_ms ↔ extract_ms** (r=-0.477, n=300): Hitch-Frames: extract_ms-Mittel 1.943 vs. übrige 2.971 (Faktor 0.65). Pearson r=-0.477 (moderat).
- **cpu_full_frame_ms ↔ stream_ms** (r=0.990, n=300): Pearson r=0.990 (stark) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=-0.477, n=300): Pearson r=-0.477 (moderat) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=n/a, n=0): Zu wenige Datenpunkte für eine belastbare Korrelation.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 1/300 Frames (0.3%).
- stream_unloaded am Unload-Cap (2): 0/300 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 1/90 (1.1%).
- Hitchs mit stream_unloaded am Cap: 0/90 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/300 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: unclear (Nicht eindeutig) in 73/90 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 72.0%, Apply 21.6%, Unload 0.0%, Extract 27.9%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 15.3%.
- Häufigstes Hitch-Muster: periodic_cluster (83×).

## Offene Fragen

- 73 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
