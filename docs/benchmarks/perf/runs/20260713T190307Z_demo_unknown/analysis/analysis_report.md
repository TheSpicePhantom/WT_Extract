# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260713T190307Z_demo_unknown`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 321
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-13T19:03:22.937075+00:00
- **git_commit:** unknown

### Config-Fingerprints

- `profiling`: `-416893896343030827`
- `streaming`: `4052651995577490327`
- `visibility_lod`: `-5364246785342016830`
- `world_gen`: `-3289618735192297230`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, deco_extract_ms, pending_unload_count, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 23.0587 | 23.0587 | +0.0000 | OK |
| frame_ms_p95 | 26.4927 | 26.4927 | +0.0000 | OK |
| frame_ms_max | 57.2723 | 57.2723 | +0.0000 | OK |
| stream_ms_mean | 17.8216 | 17.8216 | +0.0000 | OK |
| stream_ms_p95 | 19.2320 | 19.2320 | +0.0000 | OK |
| stream_ms_max | 47.2222 | 47.2222 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0058 | 0.0058 | +0.0000 | OK |
| stream_unload_ms_max | 0.0077 | 0.0077 | +0.0000 | OK |
| chunk_count_mean | 16.7632 | 16.7632 | +0.0000 | OK |
| recorded_frames | 321.0000 | 321.0000 | +0.0000 | OK |
| hitch_count | 321.0000 | 321.0000 | +0.0000 | OK |
| hitch_frame_count | 321.0000 | 321.0000 | +0.0000 | OK |
| hitch_stream_count | 321.0000 | 321.0000 | +0.0000 | OK |
| hitch_load_count | 1.0000 | 1.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Load-/Apply-dominant** (dominant_bottleneck, Konfidenz: hoch)
   - In 314/321 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 77.3% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_apply_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 56.6% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (57.27) deutlich über P95 (26.49) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `frame_slow`: 321
- `stream_slow`: 321
- `load_burst`: 1

### Frame 0

- **frame_ms:** 21.626
- **stream_ms / apply / unload:** 17.061 / 12.325 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:21.4, 2:21.8, 3:23.0

### Frame 1

- **frame_ms:** 21.420
- **stream_ms / apply / unload:** 16.878 / 12.413 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:21.6
- **Kontext danach:** 2:21.8, 3:23.0, 4:25.1

### Frame 2

- **frame_ms:** 21.785
- **stream_ms / apply / unload:** 16.913 / 12.387 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:21.6, 1:21.4
- **Kontext danach:** 3:23.0, 4:25.1, 5:21.5

### Frame 3

- **frame_ms:** 23.019
- **stream_ms / apply / unload:** 18.049 / 12.999 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 0:21.6, 1:21.4, 2:21.8
- **Kontext danach:** 4:25.1, 5:21.5, 6:21.9

### Frame 4

- **frame_ms:** 25.132
- **stream_ms / apply / unload:** 20.534 / 15.711 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 1:21.4, 2:21.8, 3:23.0
- **Kontext danach:** 5:21.5, 6:21.9, 7:21.8

### Frame 5

- **frame_ms:** 21.470
- **stream_ms / apply / unload:** 16.940 / 12.440 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 26 Hitches in einem 20-Frame-Fenster (Spanne 25).
- **Kontext davor:** 2:21.8, 3:23.0, 4:25.1
- **Kontext danach:** 6:21.9, 7:21.8, 8:21.5

### Frame 6

- **frame_ms:** 21.937
- **stream_ms / apply / unload:** 17.343 / 12.445 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 3:23.0, 4:25.1, 5:21.5
- **Kontext danach:** 7:21.8, 8:21.5, 9:21.7

### Frame 7

- **frame_ms:** 21.766
- **stream_ms / apply / unload:** 17.241 / 12.433 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 4:25.1, 5:21.5, 6:21.9
- **Kontext danach:** 8:21.5, 9:21.7, 10:21.6

### Frame 8

- **frame_ms:** 21.494
- **stream_ms / apply / unload:** 16.911 / 12.409 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 5:21.5, 6:21.9, 7:21.8
- **Kontext danach:** 9:21.7, 10:21.6, 11:22.3

### Frame 9

- **frame_ms:** 21.748
- **stream_ms / apply / unload:** 17.195 / 12.638 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 6:21.9, 7:21.8, 8:21.5
- **Kontext danach:** 10:21.6, 11:22.3, 12:21.6

### Frame 10

- **frame_ms:** 21.649
- **stream_ms / apply / unload:** 17.064 / 12.502 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 7:21.8, 8:21.5, 9:21.7
- **Kontext danach:** 11:22.3, 12:21.6, 13:22.2

### Frame 11

- **frame_ms:** 22.334
- **stream_ms / apply / unload:** 17.758 / 12.738 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 8:21.5, 9:21.7, 10:21.6
- **Kontext danach:** 12:21.6, 13:22.2, 14:21.5

### Frame 12

- **frame_ms:** 21.554
- **stream_ms / apply / unload:** 16.990 / 12.424 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 9:21.7, 10:21.6, 11:22.3
- **Kontext danach:** 13:22.2, 14:21.5, 15:21.5

### Frame 13

- **frame_ms:** 22.177
- **stream_ms / apply / unload:** 17.256 / 12.642 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 10:21.6, 11:22.3, 12:21.6
- **Kontext danach:** 14:21.5, 15:21.5, 16:21.9

### Frame 14

- **frame_ms:** 21.524
- **stream_ms / apply / unload:** 16.888 / 12.330 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 11:22.3, 12:21.6, 13:22.2
- **Kontext danach:** 15:21.5, 16:21.9, 17:21.8

### Frame 15

- **frame_ms:** 21.455
- **stream_ms / apply / unload:** 16.909 / 12.395 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 12:21.6, 13:22.2, 14:21.5
- **Kontext danach:** 16:21.9, 17:21.8, 18:23.3

### Frame 16

- **frame_ms:** 21.888
- **stream_ms / apply / unload:** 17.335 / 12.694 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 13:22.2, 14:21.5, 15:21.5
- **Kontext danach:** 17:21.8, 18:23.3, 19:22.7

### Frame 17

- **frame_ms:** 21.763
- **stream_ms / apply / unload:** 17.254 / 12.643 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 14:21.5, 15:21.5, 16:21.9
- **Kontext danach:** 18:23.3, 19:22.7, 20:21.5

### Frame 18

- **frame_ms:** 23.327
- **stream_ms / apply / unload:** 18.642 / 13.916 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 15:21.5, 16:21.9, 17:21.8
- **Kontext danach:** 19:22.7, 20:21.5, 21:22.6

### Frame 19

- **frame_ms:** 22.720
- **stream_ms / apply / unload:** 18.155 / 12.883 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 16:21.9, 17:21.8, 18:23.3
- **Kontext danach:** 20:21.5, 21:22.6, 22:21.8

### Frame 20

- **frame_ms:** 21.476
- **stream_ms / apply / unload:** 16.937 / 12.376 / 0.005
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
- **Kontext davor:** 17:21.8, 18:23.3, 19:22.7
- **Kontext danach:** 21:22.6, 22:21.8, 23:21.6

### Frame 21

- **frame_ms:** 22.579
- **stream_ms / apply / unload:** 17.931 / 12.866 / 0.005
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
- **Kontext davor:** 18:23.3, 19:22.7, 20:21.5
- **Kontext danach:** 22:21.8, 23:21.6, 24:21.7

### Frame 22

- **frame_ms:** 21.804
- **stream_ms / apply / unload:** 17.251 / 12.556 / 0.005
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
- **Kontext davor:** 19:22.7, 20:21.5, 21:22.6
- **Kontext danach:** 23:21.6, 24:21.7, 25:21.5

### Frame 23

- **frame_ms:** 21.615
- **stream_ms / apply / unload:** 17.051 / 12.509 / 0.005
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
- **Kontext davor:** 20:21.5, 21:22.6, 22:21.8
- **Kontext danach:** 24:21.7, 25:21.5, 26:21.5

### Frame 24

- **frame_ms:** 21.738
- **stream_ms / apply / unload:** 17.117 / 12.431 / 0.005
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
- **Kontext davor:** 21:22.6, 22:21.8, 23:21.6
- **Kontext danach:** 25:21.5, 26:21.5, 27:28.6

### Frame 25

- **frame_ms:** 21.502
- **stream_ms / apply / unload:** 16.860 / 12.356 / 0.005
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
- **Kontext davor:** 22:21.8, 23:21.6, 24:21.7
- **Kontext danach:** 26:21.5, 27:28.6, 28:23.0

### Frame 26

- **frame_ms:** 21.520
- **stream_ms / apply / unload:** 16.957 / 12.482 / 0.005
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
- **Kontext davor:** 23:21.6, 24:21.7, 25:21.5
- **Kontext danach:** 27:28.6, 28:23.0, 29:22.8

### Frame 27

- **frame_ms:** 28.597
- **stream_ms / apply / unload:** 19.945 / 15.348 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 24:21.7, 25:21.5, 26:21.5
- **Kontext danach:** 28:23.0, 29:22.8, 30:22.7

### Frame 28

- **frame_ms:** 22.958
- **stream_ms / apply / unload:** 18.259 / 12.995 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 25:21.5, 26:21.5, 27:28.6
- **Kontext danach:** 29:22.8, 30:22.7, 31:22.3

### Frame 29

- **frame_ms:** 22.810
- **stream_ms / apply / unload:** 18.131 / 12.900 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 26:21.5, 27:28.6, 28:23.0
- **Kontext danach:** 30:22.7, 31:22.3, 32:23.1

### Frame 30

- **frame_ms:** 22.713
- **stream_ms / apply / unload:** 18.087 / 12.945 / 0.005
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
- **Kontext davor:** 27:28.6, 28:23.0, 29:22.8
- **Kontext danach:** 31:22.3, 32:23.1, 33:22.1

### Frame 31

- **frame_ms:** 22.343
- **stream_ms / apply / unload:** 17.619 / 12.655 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 28:23.0, 29:22.8, 30:22.7
- **Kontext danach:** 32:23.1, 33:22.1, 34:22.8

### Frame 32

- **frame_ms:** 23.051
- **stream_ms / apply / unload:** 18.460 / 13.307 / 0.005
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
- **Kontext davor:** 29:22.8, 30:22.7, 31:22.3
- **Kontext danach:** 33:22.1, 34:22.8, 35:21.9

### Frame 33

- **frame_ms:** 22.146
- **stream_ms / apply / unload:** 17.375 / 12.805 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 30:22.7, 31:22.3, 32:23.1
- **Kontext danach:** 34:22.8, 35:21.9, 36:21.9

### Frame 34

- **frame_ms:** 22.816
- **stream_ms / apply / unload:** 18.243 / 13.304 / 0.005
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
- **Kontext davor:** 31:22.3, 32:23.1, 33:22.1
- **Kontext danach:** 35:21.9, 36:21.9, 37:22.0

### Frame 35

- **frame_ms:** 21.862
- **stream_ms / apply / unload:** 17.258 / 12.731 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 32:23.1, 33:22.1, 34:22.8
- **Kontext danach:** 36:21.9, 37:22.0, 38:22.6

### Frame 36

- **frame_ms:** 21.874
- **stream_ms / apply / unload:** 17.302 / 12.726 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 33:22.1, 34:22.8, 35:21.9
- **Kontext danach:** 37:22.0, 38:22.6, 39:21.7

### Frame 37

- **frame_ms:** 21.963
- **stream_ms / apply / unload:** 17.437 / 12.690 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 34:22.8, 35:21.9, 36:21.9
- **Kontext danach:** 38:22.6, 39:21.7, 40:22.6

### Frame 38

- **frame_ms:** 22.630
- **stream_ms / apply / unload:** 17.922 / 13.248 / 0.005
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
- **Kontext davor:** 35:21.9, 36:21.9, 37:22.0
- **Kontext danach:** 39:21.7, 40:22.6, 41:29.8

### Frame 39

- **frame_ms:** 21.657
- **stream_ms / apply / unload:** 17.076 / 12.477 / 0.005
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
- **Kontext davor:** 36:21.9, 37:22.0, 38:22.6
- **Kontext danach:** 40:22.6, 41:29.8, 42:21.8

### Frame 40

- **frame_ms:** 22.551
- **stream_ms / apply / unload:** 17.876 / 12.800 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 37:22.0, 38:22.6, 39:21.7
- **Kontext danach:** 41:29.8, 42:21.8, 43:22.0

### Frame 41

- **frame_ms:** 29.824
- **stream_ms / apply / unload:** 18.289 / 13.036 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 43.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 38:22.6, 39:21.7, 40:22.6
- **Kontext danach:** 42:21.8, 43:22.0, 44:22.0

### Frame 42

- **frame_ms:** 21.811
- **stream_ms / apply / unload:** 17.238 / 12.708 / 0.005
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
- **Kontext davor:** 39:21.7, 40:22.6, 41:29.8
- **Kontext danach:** 43:22.0, 44:22.0, 45:22.0

### Frame 43

- **frame_ms:** 21.979
- **stream_ms / apply / unload:** 17.383 / 12.800 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 40:22.6, 41:29.8, 42:21.8
- **Kontext danach:** 44:22.0, 45:22.0, 46:22.8

### Frame 44

- **frame_ms:** 21.969
- **stream_ms / apply / unload:** 17.215 / 12.690 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 41:29.8, 42:21.8, 43:22.0
- **Kontext danach:** 45:22.0, 46:22.8, 47:21.8

### Frame 45

- **frame_ms:** 21.960
- **stream_ms / apply / unload:** 17.354 / 12.743 / 0.005
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
- **Kontext davor:** 42:21.8, 43:22.0, 44:22.0
- **Kontext danach:** 46:22.8, 47:21.8, 48:21.6

### Frame 46

- **frame_ms:** 22.787
- **stream_ms / apply / unload:** 18.199 / 12.699 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 43:22.0, 44:22.0, 45:22.0
- **Kontext danach:** 47:21.8, 48:21.6, 49:21.7

### Frame 47

- **frame_ms:** 21.770
- **stream_ms / apply / unload:** 17.208 / 12.617 / 0.005
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
- **Kontext davor:** 44:22.0, 45:22.0, 46:22.8
- **Kontext danach:** 48:21.6, 49:21.7, 50:21.6

### Frame 48

- **frame_ms:** 21.623
- **stream_ms / apply / unload:** 17.038 / 12.470 / 0.005
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
- **Kontext davor:** 45:22.0, 46:22.8, 47:21.8
- **Kontext danach:** 49:21.7, 50:21.6, 51:21.8

### Frame 49

- **frame_ms:** 21.675
- **stream_ms / apply / unload:** 17.086 / 12.504 / 0.005
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
- **Kontext davor:** 46:22.8, 47:21.8, 48:21.6
- **Kontext danach:** 50:21.6, 51:21.8, 52:22.2

### Frame 50

- **frame_ms:** 21.607
- **stream_ms / apply / unload:** 17.058 / 12.499 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 47:21.8, 48:21.6, 49:21.7
- **Kontext danach:** 51:21.8, 52:22.2, 53:22.3

### Frame 51

- **frame_ms:** 21.807
- **stream_ms / apply / unload:** 17.089 / 12.528 / 0.005
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
- **Kontext davor:** 48:21.6, 49:21.7, 50:21.6
- **Kontext danach:** 52:22.2, 53:22.3, 54:21.7

### Frame 52

- **frame_ms:** 22.189
- **stream_ms / apply / unload:** 17.115 / 12.517 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 49:21.7, 50:21.6, 51:21.8
- **Kontext danach:** 53:22.3, 54:21.7, 55:23.6

### Frame 53

- **frame_ms:** 22.292
- **stream_ms / apply / unload:** 17.706 / 12.910 / 0.005
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
- **Kontext davor:** 50:21.6, 51:21.8, 52:22.2
- **Kontext danach:** 54:21.7, 55:23.6, 56:23.1

### Frame 54

- **frame_ms:** 21.707
- **stream_ms / apply / unload:** 17.100 / 12.531 / 0.005
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
- **Kontext davor:** 51:21.8, 52:22.2, 53:22.3
- **Kontext danach:** 55:23.6, 56:23.1, 57:22.2

### Frame 55

- **frame_ms:** 23.636
- **stream_ms / apply / unload:** 18.935 / 13.828 / 0.006
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
- **Kontext davor:** 52:22.2, 53:22.3, 54:21.7
- **Kontext danach:** 56:23.1, 57:22.2, 58:21.8

### Frame 56

- **frame_ms:** 23.051
- **stream_ms / apply / unload:** 18.316 / 13.101 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 53:22.3, 54:21.7, 55:23.6
- **Kontext danach:** 57:22.2, 58:21.8, 59:22.1

### Frame 57

- **frame_ms:** 22.182
- **stream_ms / apply / unload:** 17.567 / 12.739 / 0.005
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
- **Kontext davor:** 54:21.7, 55:23.6, 56:23.1
- **Kontext danach:** 58:21.8, 59:22.1, 60:21.7

### Frame 58

- **frame_ms:** 21.814
- **stream_ms / apply / unload:** 17.190 / 12.596 / 0.005
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
- **Kontext davor:** 55:23.6, 56:23.1, 57:22.2
- **Kontext danach:** 59:22.1, 60:21.7, 61:21.9

### Frame 59

- **frame_ms:** 22.075
- **stream_ms / apply / unload:** 17.515 / 12.732 / 0.005
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
- **Kontext davor:** 56:23.1, 57:22.2, 58:21.8
- **Kontext danach:** 60:21.7, 61:21.9, 62:21.8

### Frame 60

- **frame_ms:** 21.727
- **stream_ms / apply / unload:** 17.211 / 12.584 / 0.005
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
- **Kontext davor:** 57:22.2, 58:21.8, 59:22.1
- **Kontext danach:** 61:21.9, 62:21.8, 63:21.6

### Frame 61

- **frame_ms:** 21.898
- **stream_ms / apply / unload:** 17.209 / 12.603 / 0.005
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
- **Kontext davor:** 58:21.8, 59:22.1, 60:21.7
- **Kontext danach:** 62:21.8, 63:21.6, 64:21.7

### Frame 62

- **frame_ms:** 21.815
- **stream_ms / apply / unload:** 17.213 / 12.556 / 0.005
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
- **Kontext davor:** 59:22.1, 60:21.7, 61:21.9
- **Kontext danach:** 63:21.6, 64:21.7, 65:21.9

### Frame 63

- **frame_ms:** 21.590
- **stream_ms / apply / unload:** 16.966 / 12.431 / 0.005
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
- **Kontext davor:** 60:21.7, 61:21.9, 62:21.8
- **Kontext danach:** 64:21.7, 65:21.9, 66:21.7

### Frame 64

- **frame_ms:** 21.678
- **stream_ms / apply / unload:** 17.090 / 12.504 / 0.005
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
- **Kontext davor:** 61:21.9, 62:21.8, 63:21.6
- **Kontext danach:** 65:21.9, 66:21.7, 67:21.8

### Frame 65

- **frame_ms:** 21.906
- **stream_ms / apply / unload:** 17.349 / 12.712 / 0.005
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
- **Kontext davor:** 62:21.8, 63:21.6, 64:21.7
- **Kontext danach:** 66:21.7, 67:21.8, 68:21.6

### Frame 66

- **frame_ms:** 21.718
- **stream_ms / apply / unload:** 17.057 / 12.505 / 0.005
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
- **Kontext davor:** 63:21.6, 64:21.7, 65:21.9
- **Kontext danach:** 67:21.8, 68:21.6, 69:21.8

### Frame 67

- **frame_ms:** 21.811
- **stream_ms / apply / unload:** 17.198 / 12.674 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4054
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 64:21.7, 65:21.9, 66:21.7
- **Kontext danach:** 68:21.6, 69:21.8, 70:21.9

### Frame 68

- **frame_ms:** 21.639
- **stream_ms / apply / unload:** 17.008 / 12.525 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4054
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 65:21.9, 66:21.7, 67:21.8
- **Kontext danach:** 69:21.8, 70:21.9, 71:21.6

### Frame 69

- **frame_ms:** 21.751
- **stream_ms / apply / unload:** 17.142 / 12.601 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4054
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 66:21.7, 67:21.8, 68:21.6
- **Kontext danach:** 70:21.9, 71:21.6, 72:22.4

### Frame 70

- **frame_ms:** 21.920
- **stream_ms / apply / unload:** 17.376 / 12.563 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4054
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 67:21.8, 68:21.6, 69:21.8
- **Kontext danach:** 71:21.6, 72:22.4, 73:21.7

### Frame 71

- **frame_ms:** 21.593
- **stream_ms / apply / unload:** 16.822 / 12.369 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4696
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 68:21.6, 69:21.8, 70:21.9
- **Kontext danach:** 72:22.4, 73:21.7, 74:23.3

### Frame 72

- **frame_ms:** 22.403
- **stream_ms / apply / unload:** 17.803 / 12.931 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.4696
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 69:21.8, 70:21.9, 71:21.6
- **Kontext danach:** 73:21.7, 74:23.3, 75:21.6

### Frame 73

- **frame_ms:** 21.728
- **stream_ms / apply / unload:** 17.094 / 12.542 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.5439
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 70:21.9, 71:21.6, 72:22.4
- **Kontext danach:** 74:23.3, 75:21.6, 76:22.3

### Frame 74

- **frame_ms:** 23.316
- **stream_ms / apply / unload:** 18.709 / 13.385 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.6300
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 71:21.6, 72:22.4, 73:21.7
- **Kontext danach:** 75:21.6, 76:22.3, 77:21.7

### Frame 75

- **frame_ms:** 21.571
- **stream_ms / apply / unload:** 16.959 / 12.411 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.6300
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 72:22.4, 73:21.7, 74:23.3
- **Kontext danach:** 76:22.3, 77:21.7, 78:21.8

### Frame 76

- **frame_ms:** 22.345
- **stream_ms / apply / unload:** 17.668 / 13.003 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.7297
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 73:21.7, 74:23.3, 75:21.6
- **Kontext danach:** 77:21.7, 78:21.8, 79:21.7

### Frame 77

- **frame_ms:** 21.734
- **stream_ms / apply / unload:** 17.122 / 12.620 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.7297
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 74:23.3, 75:21.6, 76:22.3
- **Kontext danach:** 78:21.8, 79:21.7, 80:22.0

### Frame 78

- **frame_ms:** 21.781
- **stream_ms / apply / unload:** 17.094 / 12.650 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 75:21.6, 76:22.3, 77:21.7
- **Kontext danach:** 79:21.7, 80:22.0, 81:21.7

### Frame 79

- **frame_ms:** 21.661
- **stream_ms / apply / unload:** 17.069 / 12.570 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 76:22.3, 77:21.7, 78:21.8
- **Kontext danach:** 80:22.0, 81:21.7, 82:21.7

### Frame 80

- **frame_ms:** 22.049
- **stream_ms / apply / unload:** 17.423 / 12.841 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 77:21.7, 78:21.8, 79:21.7
- **Kontext danach:** 81:21.7, 82:21.7, 83:21.6

### Frame 81

- **frame_ms:** 21.689
- **stream_ms / apply / unload:** 17.053 / 12.539 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 78:21.8, 79:21.7, 80:22.0
- **Kontext danach:** 82:21.7, 83:21.6, 84:21.7

### Frame 82

- **frame_ms:** 21.680
- **stream_ms / apply / unload:** 17.096 / 12.533 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 79:21.7, 80:22.0, 81:21.7
- **Kontext danach:** 83:21.6, 84:21.7, 85:21.8

### Frame 83

- **frame_ms:** 21.597
- **stream_ms / apply / unload:** 17.027 / 12.507 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 80:22.0, 81:21.7, 82:21.7
- **Kontext danach:** 84:21.7, 85:21.8, 86:21.6

### Frame 84

- **frame_ms:** 21.723
- **stream_ms / apply / unload:** 17.125 / 12.516 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 81:21.7, 82:21.7, 83:21.6
- **Kontext danach:** 85:21.8, 86:21.6, 87:21.6

### Frame 85

- **frame_ms:** 21.845
- **stream_ms / apply / unload:** 17.269 / 12.700 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 82:21.7, 83:21.6, 84:21.7
- **Kontext danach:** 86:21.6, 87:21.6, 88:21.6

### Frame 86

- **frame_ms:** 21.577
- **stream_ms / apply / unload:** 16.965 / 12.466 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 83:21.6, 84:21.7, 85:21.8
- **Kontext danach:** 87:21.6, 88:21.6, 89:21.7

### Frame 87

- **frame_ms:** 21.627
- **stream_ms / apply / unload:** 17.002 / 12.525 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 84:21.7, 85:21.8, 86:21.6
- **Kontext danach:** 88:21.6, 89:21.7, 90:22.4

### Frame 88

- **frame_ms:** 21.645
- **stream_ms / apply / unload:** 17.070 / 12.592 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 85:21.8, 86:21.6, 87:21.6
- **Kontext danach:** 89:21.7, 90:22.4, 91:22.0

### Frame 89

- **frame_ms:** 21.695
- **stream_ms / apply / unload:** 17.087 / 12.591 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 86:21.6, 87:21.6, 88:21.6
- **Kontext danach:** 90:22.4, 91:22.0, 92:21.6

### Frame 90

- **frame_ms:** 22.389
- **stream_ms / apply / unload:** 17.776 / 13.158 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 87:21.6, 88:21.6, 89:21.7
- **Kontext danach:** 91:22.0, 92:21.6, 93:22.1

### Frame 91

- **frame_ms:** 21.963
- **stream_ms / apply / unload:** 17.377 / 12.753 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 88:21.6, 89:21.7, 90:22.4
- **Kontext danach:** 92:21.6, 93:22.1, 94:22.7

### Frame 92

- **frame_ms:** 21.596
- **stream_ms / apply / unload:** 16.944 / 12.437 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8452
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 89:21.7, 90:22.4, 91:22.0
- **Kontext danach:** 93:22.1, 94:22.7, 95:21.8

### Frame 93

- **frame_ms:** 22.124
- **stream_ms / apply / unload:** 17.217 / 12.584 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.9790
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 90:22.4, 91:22.0, 92:21.6
- **Kontext danach:** 94:22.7, 95:21.8, 96:22.6

### Frame 94

- **frame_ms:** 22.664
- **stream_ms / apply / unload:** 17.893 / 12.696 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.9790
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 91:22.0, 92:21.6, 93:22.1
- **Kontext danach:** 95:21.8, 96:22.6, 97:22.3

### Frame 95

- **frame_ms:** 21.816
- **stream_ms / apply / unload:** 17.067 / 12.536 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.1340
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 92:21.6, 93:22.1, 94:22.7
- **Kontext danach:** 96:22.6, 97:22.3, 98:22.0

### Frame 96

- **frame_ms:** 22.585
- **stream_ms / apply / unload:** 17.753 / 12.786 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.3135
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 93:22.1, 94:22.7, 95:21.8
- **Kontext danach:** 97:22.3, 98:22.0, 99:21.8

### Frame 97

- **frame_ms:** 22.275
- **stream_ms / apply / unload:** 17.470 / 12.784 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.5214
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 94:22.7, 95:21.8, 96:22.6
- **Kontext danach:** 98:22.0, 99:21.8, 100:23.0

### Frame 98

- **frame_ms:** 22.028
- **stream_ms / apply / unload:** 17.255 / 12.540 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.7622
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 95:21.8, 96:22.6, 97:22.3
- **Kontext danach:** 99:21.8, 100:23.0, 101:23.3

### Frame 99

- **frame_ms:** 21.775
- **stream_ms / apply / unload:** 17.043 / 12.462 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.0412
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 96:22.6, 97:22.3, 98:22.0
- **Kontext danach:** 100:23.0, 101:23.3, 102:23.8

### Frame 100

- **frame_ms:** 22.951
- **stream_ms / apply / unload:** 18.129 / 12.892 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.0412
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 97:22.3, 98:22.0, 99:21.8
- **Kontext danach:** 101:23.3, 102:23.8, 103:23.4

### Frame 101

- **frame_ms:** 23.306
- **stream_ms / apply / unload:** 18.410 / 13.094 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.0412
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 98:22.0, 99:21.8, 100:23.0
- **Kontext danach:** 102:23.8, 103:23.4, 104:22.7

### Frame 102

- **frame_ms:** 23.787
- **stream_ms / apply / unload:** 18.970 / 13.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 99:21.8, 100:23.0, 101:23.3
- **Kontext danach:** 103:23.4, 104:22.7, 105:22.1

### Frame 103

- **frame_ms:** 23.402
- **stream_ms / apply / unload:** 18.552 / 13.416 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 100:23.0, 101:23.3, 102:23.8
- **Kontext danach:** 104:22.7, 105:22.1, 106:21.6

### Frame 104

- **frame_ms:** 22.682
- **stream_ms / apply / unload:** 17.929 / 13.131 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 101:23.3, 102:23.8, 103:23.4
- **Kontext danach:** 105:22.1, 106:21.6, 107:28.3

### Frame 105

- **frame_ms:** 22.149
- **stream_ms / apply / unload:** 17.410 / 12.921 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 102:23.8, 103:23.4, 104:22.7
- **Kontext danach:** 106:21.6, 107:28.3, 108:22.2

### Frame 106

- **frame_ms:** 21.550
- **stream_ms / apply / unload:** 16.796 / 12.372 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 103:23.4, 104:22.7, 105:22.1
- **Kontext danach:** 107:28.3, 108:22.2, 109:21.9

### Frame 107

- **frame_ms:** 28.338
- **stream_ms / apply / unload:** 17.173 / 12.622 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 44.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 104:22.7, 105:22.1, 106:21.6
- **Kontext danach:** 108:22.2, 109:21.9, 110:22.1

### Frame 108

- **frame_ms:** 22.187
- **stream_ms / apply / unload:** 17.434 / 12.866 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 105:22.1, 106:21.6, 107:28.3
- **Kontext danach:** 109:21.9, 110:22.1, 111:22.8

### Frame 109

- **frame_ms:** 21.900
- **stream_ms / apply / unload:** 17.080 / 12.566 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 106:21.6, 107:28.3, 108:22.2
- **Kontext danach:** 110:22.1, 111:22.8, 112:22.0

### Frame 110

- **frame_ms:** 22.124
- **stream_ms / apply / unload:** 17.387 / 12.719 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 107:28.3, 108:22.2, 109:21.9
- **Kontext danach:** 111:22.8, 112:22.0, 113:22.0

### Frame 111

- **frame_ms:** 22.827
- **stream_ms / apply / unload:** 18.124 / 13.490 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 108:22.2, 109:21.9, 110:22.1
- **Kontext danach:** 112:22.0, 113:22.0, 114:21.8

### Frame 112

- **frame_ms:** 21.973
- **stream_ms / apply / unload:** 17.210 / 12.577 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 109:21.9, 110:22.1, 111:22.8
- **Kontext danach:** 113:22.0, 114:21.8, 115:31.6

### Frame 113

- **frame_ms:** 21.962
- **stream_ms / apply / unload:** 17.216 / 12.574 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 110:22.1, 111:22.8, 112:22.0
- **Kontext danach:** 114:21.8, 115:31.6, 116:22.0

### Frame 114

- **frame_ms:** 21.764
- **stream_ms / apply / unload:** 17.043 / 12.493 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.3643
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 111:22.8, 112:22.0, 113:22.0
- **Kontext danach:** 115:31.6, 116:22.0, 117:22.2

### Frame 115

- **frame_ms:** 31.637
- **stream_ms / apply / unload:** 26.729 / 19.348 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.7386
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 112:22.0, 113:22.0, 114:21.8
- **Kontext danach:** 116:22.0, 117:22.2, 118:23.5

### Frame 116

- **frame_ms:** 21.957
- **stream_ms / apply / unload:** 17.093 / 12.583 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 3.1720
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 113:22.0, 114:21.8, 115:31.6
- **Kontext danach:** 117:22.2, 118:23.5, 119:23.8

### Frame 117

- **frame_ms:** 22.231
- **stream_ms / apply / unload:** 17.133 / 12.521 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.2558
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 114:21.8, 115:31.6, 116:22.0
- **Kontext danach:** 118:23.5, 119:23.8, 120:22.7

### Frame 118

- **frame_ms:** 23.492
- **stream_ms / apply / unload:** 18.168 / 13.528 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.9294
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 115:31.6, 116:22.0, 117:22.2
- **Kontext danach:** 119:23.8, 120:22.7, 121:22.0

### Frame 119

- **frame_ms:** 23.824
- **stream_ms / apply / unload:** 18.695 / 13.432 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 116:22.0, 117:22.2, 118:23.5
- **Kontext danach:** 120:22.7, 121:22.0, 122:22.2

### Frame 120

- **frame_ms:** 22.708
- **stream_ms / apply / unload:** 17.613 / 13.030 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 117:22.2, 118:23.5, 119:23.8
- **Kontext danach:** 121:22.0, 122:22.2, 123:22.1

### Frame 121

- **frame_ms:** 21.960
- **stream_ms / apply / unload:** 16.865 / 12.496 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 118:23.5, 119:23.8, 120:22.7
- **Kontext danach:** 122:22.2, 123:22.1, 124:23.0

### Frame 122

- **frame_ms:** 22.209
- **stream_ms / apply / unload:** 17.114 / 12.563 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 119:23.8, 120:22.7, 121:22.0
- **Kontext danach:** 123:22.1, 124:23.0, 125:23.2

### Frame 123

- **frame_ms:** 22.085
- **stream_ms / apply / unload:** 17.061 / 12.592 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 120:22.7, 121:22.0, 122:22.2
- **Kontext danach:** 124:23.0, 125:23.2, 126:22.2

### Frame 124

- **frame_ms:** 23.036
- **stream_ms / apply / unload:** 17.930 / 12.558 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 121:22.0, 122:22.2, 123:22.1
- **Kontext danach:** 125:23.2, 126:22.2, 127:22.4

### Frame 125

- **frame_ms:** 23.219
- **stream_ms / apply / unload:** 17.938 / 12.906 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 122:22.2, 123:22.1, 124:23.0
- **Kontext danach:** 126:22.2, 127:22.4, 128:22.4

### Frame 126

- **frame_ms:** 22.209
- **stream_ms / apply / unload:** 17.075 / 12.561 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 123:22.1, 124:23.0, 125:23.2
- **Kontext danach:** 127:22.4, 128:22.4, 129:22.2

### Frame 127

- **frame_ms:** 22.414
- **stream_ms / apply / unload:** 17.323 / 12.514 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 124:23.0, 125:23.2, 126:22.2
- **Kontext danach:** 128:22.4, 129:22.2, 130:23.1

### Frame 128

- **frame_ms:** 22.371
- **stream_ms / apply / unload:** 17.147 / 12.538 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 125:23.2, 126:22.2, 127:22.4
- **Kontext danach:** 129:22.2, 130:23.1, 131:22.1

### Frame 129

- **frame_ms:** 22.216
- **stream_ms / apply / unload:** 17.077 / 12.506 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 126:22.2, 127:22.4, 128:22.4
- **Kontext danach:** 130:23.1, 131:22.1, 132:22.0

### Frame 130

- **frame_ms:** 23.100
- **stream_ms / apply / unload:** 17.970 / 12.706 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 127:22.4, 128:22.4, 129:22.2
- **Kontext danach:** 131:22.1, 132:22.0, 133:21.9

### Frame 131

- **frame_ms:** 22.052
- **stream_ms / apply / unload:** 16.951 / 12.465 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 5.7097
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 128:22.4, 129:22.2, 130:23.1
- **Kontext danach:** 132:22.0, 133:21.9, 134:21.9

### Frame 132

- **frame_ms:** 21.998
- **stream_ms / apply / unload:** 16.845 / 12.415 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 6.6135
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 129:22.2, 130:23.1, 131:22.1
- **Kontext danach:** 133:21.9, 134:21.9, 135:22.5

### Frame 133

- **frame_ms:** 21.888
- **stream_ms / apply / unload:** 16.754 / 12.311 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 7.6604
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 130:23.1, 131:22.1, 132:22.0
- **Kontext danach:** 134:21.9, 135:22.5, 136:22.1

### Frame 134

- **frame_ms:** 21.857
- **stream_ms / apply / unload:** 16.728 / 12.428 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.8729
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 131:22.1, 132:22.0, 133:21.9
- **Kontext danach:** 135:22.5, 136:22.1, 137:23.0

### Frame 135

- **frame_ms:** 22.471
- **stream_ms / apply / unload:** 17.305 / 12.748 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 10.2774
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 132:22.0, 133:21.9, 134:21.9
- **Kontext danach:** 136:22.1, 137:23.0, 138:21.9

### Frame 136

- **frame_ms:** 22.089
- **stream_ms / apply / unload:** 16.847 / 12.366 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 11.9043
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 133:21.9, 134:21.9, 135:22.5
- **Kontext danach:** 137:23.0, 138:21.9, 139:22.1

### Frame 137

- **frame_ms:** 23.003
- **stream_ms / apply / unload:** 17.747 / 12.597 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 134:21.9, 135:22.5, 136:22.1
- **Kontext danach:** 138:21.9, 139:22.1, 140:23.3

### Frame 138

- **frame_ms:** 21.943
- **stream_ms / apply / unload:** 16.848 / 12.376 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 135:22.5, 136:22.1, 137:23.0
- **Kontext danach:** 139:22.1, 140:23.3, 141:22.8

### Frame 139

- **frame_ms:** 22.116
- **stream_ms / apply / unload:** 16.982 / 12.432 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 136:22.1, 137:23.0, 138:21.9
- **Kontext danach:** 140:23.3, 141:22.8, 142:22.1

### Frame 140

- **frame_ms:** 23.291
- **stream_ms / apply / unload:** 18.046 / 12.842 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 137:23.0, 138:21.9, 139:22.1
- **Kontext danach:** 141:22.8, 142:22.1, 143:22.0

### Frame 141

- **frame_ms:** 22.779
- **stream_ms / apply / unload:** 17.689 / 12.716 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 138:21.9, 139:22.1, 140:23.3
- **Kontext danach:** 142:22.1, 143:22.0, 144:21.9

### Frame 142

- **frame_ms:** 22.109
- **stream_ms / apply / unload:** 16.997 / 12.540 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 139:22.1, 140:23.3, 141:22.8
- **Kontext danach:** 143:22.0, 144:21.9, 145:21.9

### Frame 143

- **frame_ms:** 22.025
- **stream_ms / apply / unload:** 16.952 / 12.621 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 140:23.3, 141:22.8, 142:22.1
- **Kontext danach:** 144:21.9, 145:21.9, 146:22.0

### Frame 144

- **frame_ms:** 21.875
- **stream_ms / apply / unload:** 16.739 / 12.391 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 141:22.8, 142:22.1, 143:22.0
- **Kontext danach:** 145:21.9, 146:22.0, 147:22.3

### Frame 145

- **frame_ms:** 21.901
- **stream_ms / apply / unload:** 16.741 / 12.376 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 142:22.1, 143:22.0, 144:21.9
- **Kontext danach:** 146:22.0, 147:22.3, 148:22.2

### Frame 146

- **frame_ms:** 22.013
- **stream_ms / apply / unload:** 16.817 / 12.334 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 143:22.0, 144:21.9, 145:21.9
- **Kontext danach:** 147:22.3, 148:22.2, 149:22.2

### Frame 147

- **frame_ms:** 22.250
- **stream_ms / apply / unload:** 16.982 / 12.448 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 144:21.9, 145:21.9, 146:22.0
- **Kontext danach:** 148:22.2, 149:22.2, 150:22.6

### Frame 148

- **frame_ms:** 22.249
- **stream_ms / apply / unload:** 17.143 / 12.501 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 145:21.9, 146:22.0, 147:22.3
- **Kontext danach:** 149:22.2, 150:22.6, 151:22.5

### Frame 149

- **frame_ms:** 22.159
- **stream_ms / apply / unload:** 16.942 / 12.370 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 146:22.0, 147:22.3, 148:22.2
- **Kontext danach:** 150:22.6, 151:22.5, 152:22.8

### Frame 150

- **frame_ms:** 22.602
- **stream_ms / apply / unload:** 17.464 / 12.644 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 13.7886
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 147:22.3, 148:22.2, 149:22.2
- **Kontext danach:** 151:22.5, 152:22.8, 153:22.3

### Frame 151

- **frame_ms:** 22.455
- **stream_ms / apply / unload:** 17.354 / 12.576 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 15.9713
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 148:22.2, 149:22.2, 150:22.6
- **Kontext danach:** 152:22.8, 153:22.3, 154:22.3

### Frame 152

- **frame_ms:** 22.765
- **stream_ms / apply / unload:** 17.616 / 12.762 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 21.4277
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 149:22.2, 150:22.6, 151:22.5
- **Kontext danach:** 153:22.3, 154:22.3, 155:22.3

### Frame 153

- **frame_ms:** 22.276
- **stream_ms / apply / unload:** 17.133 / 12.576 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 24.8195
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 150:22.6, 151:22.5, 152:22.8
- **Kontext danach:** 154:22.3, 155:22.3, 156:22.2

### Frame 154

- **frame_ms:** 22.311
- **stream_ms / apply / unload:** 17.153 / 12.642 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 28.7483
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 151:22.5, 152:22.8, 153:22.3
- **Kontext danach:** 155:22.3, 156:22.2, 157:22.0

### Frame 155

- **frame_ms:** 22.258
- **stream_ms / apply / unload:** 17.126 / 12.539 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 152:22.8, 153:22.3, 154:22.3
- **Kontext danach:** 156:22.2, 157:22.0, 158:22.5

### Frame 156

- **frame_ms:** 22.212
- **stream_ms / apply / unload:** 17.084 / 12.581 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 153:22.3, 154:22.3, 155:22.3
- **Kontext danach:** 157:22.0, 158:22.5, 159:22.2

### Frame 157

- **frame_ms:** 22.038
- **stream_ms / apply / unload:** 16.898 / 12.418 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 154:22.3, 155:22.3, 156:22.2
- **Kontext danach:** 158:22.5, 159:22.2, 160:22.9

### Frame 158

- **frame_ms:** 22.500
- **stream_ms / apply / unload:** 17.380 / 12.757 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 155:22.3, 156:22.2, 157:22.0
- **Kontext danach:** 159:22.2, 160:22.9, 161:22.2

### Frame 159

- **frame_ms:** 22.219
- **stream_ms / apply / unload:** 17.080 / 12.496 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 156:22.2, 157:22.0, 158:22.5
- **Kontext danach:** 160:22.9, 161:22.2, 162:22.2

### Frame 160

- **frame_ms:** 22.870
- **stream_ms / apply / unload:** 17.761 / 12.898 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 157:22.0, 158:22.5, 159:22.2
- **Kontext danach:** 161:22.2, 162:22.2, 163:22.1

### Frame 161

- **frame_ms:** 22.170
- **stream_ms / apply / unload:** 17.015 / 12.469 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 158:22.5, 159:22.2, 160:22.9
- **Kontext danach:** 162:22.2, 163:22.1, 164:22.3

### Frame 162

- **frame_ms:** 22.150
- **stream_ms / apply / unload:** 17.033 / 12.499 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 159:22.2, 160:22.9, 161:22.2
- **Kontext danach:** 163:22.1, 164:22.3, 165:22.3

### Frame 163

- **frame_ms:** 22.148
- **stream_ms / apply / unload:** 17.069 / 12.560 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 160:22.9, 161:22.2, 162:22.2
- **Kontext danach:** 164:22.3, 165:22.3, 166:22.5

### Frame 164

- **frame_ms:** 22.314
- **stream_ms / apply / unload:** 17.193 / 12.821 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 161:22.2, 162:22.2, 163:22.1
- **Kontext danach:** 165:22.3, 166:22.5, 167:22.2

### Frame 165

- **frame_ms:** 22.312
- **stream_ms / apply / unload:** 17.109 / 12.579 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 162:22.2, 163:22.1, 164:22.3
- **Kontext danach:** 166:22.5, 167:22.2, 168:22.1

### Frame 166

- **frame_ms:** 22.548
- **stream_ms / apply / unload:** 17.392 / 12.819 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 163:22.1, 164:22.3, 165:22.3
- **Kontext danach:** 167:22.2, 168:22.1, 169:22.6

### Frame 167

- **frame_ms:** 22.223
- **stream_ms / apply / unload:** 17.078 / 12.521 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 164:22.3, 165:22.3, 166:22.5
- **Kontext danach:** 168:22.1, 169:22.6, 170:23.2

### Frame 168

- **frame_ms:** 22.087
- **stream_ms / apply / unload:** 16.918 / 12.423 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 165:22.3, 166:22.5, 167:22.2
- **Kontext danach:** 169:22.6, 170:23.2, 171:22.0

### Frame 169

- **frame_ms:** 22.600
- **stream_ms / apply / unload:** 17.408 / 12.798 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 166:22.5, 167:22.2, 168:22.1
- **Kontext danach:** 170:23.2, 171:22.0, 172:22.3

### Frame 170

- **frame_ms:** 23.161
- **stream_ms / apply / unload:** 17.933 / 12.778 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 167:22.2, 168:22.1, 169:22.6
- **Kontext danach:** 171:22.0, 172:22.3, 173:30.0

### Frame 171

- **frame_ms:** 21.993
- **stream_ms / apply / unload:** 16.857 / 12.394 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 168:22.1, 169:22.6, 170:23.2
- **Kontext danach:** 172:22.3, 173:30.0, 174:22.5

### Frame 172

- **frame_ms:** 22.262
- **stream_ms / apply / unload:** 17.007 / 12.528 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 169:22.6, 170:23.2, 171:22.0
- **Kontext danach:** 173:30.0, 174:22.5, 175:23.7

### Frame 173

- **frame_ms:** 30.024
- **stream_ms / apply / unload:** 18.442 / 13.283 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 44.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 170:23.2, 171:22.0, 172:22.3
- **Kontext danach:** 174:22.5, 175:23.7, 176:22.2

### Frame 174

- **frame_ms:** 22.510
- **stream_ms / apply / unload:** 17.410 / 12.801 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 171:22.0, 172:22.3, 173:30.0
- **Kontext danach:** 175:23.7, 176:22.2, 177:22.0

### Frame 175

- **frame_ms:** 23.658
- **stream_ms / apply / unload:** 18.462 / 12.921 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 172:22.3, 173:30.0, 174:22.5
- **Kontext danach:** 176:22.2, 177:22.0, 178:22.1

### Frame 176

- **frame_ms:** 22.170
- **stream_ms / apply / unload:** 17.034 / 12.475 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 173:30.0, 174:22.5, 175:23.7
- **Kontext danach:** 177:22.0, 178:22.1, 179:22.2

### Frame 177

- **frame_ms:** 21.966
- **stream_ms / apply / unload:** 16.804 / 12.398 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 174:22.5, 175:23.7, 176:22.2
- **Kontext danach:** 178:22.1, 179:22.2, 180:22.2

### Frame 178

- **frame_ms:** 22.139
- **stream_ms / apply / unload:** 16.976 / 12.496 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 175:23.7, 176:22.2, 177:22.0
- **Kontext danach:** 179:22.2, 180:22.2, 181:22.1

### Frame 179

- **frame_ms:** 22.155
- **stream_ms / apply / unload:** 17.007 / 12.553 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 176:22.2, 177:22.0, 178:22.1
- **Kontext danach:** 180:22.2, 181:22.1, 182:22.1

### Frame 180

- **frame_ms:** 22.218
- **stream_ms / apply / unload:** 17.134 / 12.553 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 177:22.0, 178:22.1, 179:22.2
- **Kontext danach:** 181:22.1, 182:22.1, 183:22.1

### Frame 181

- **frame_ms:** 22.079
- **stream_ms / apply / unload:** 16.954 / 12.490 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 178:22.1, 179:22.2, 180:22.2
- **Kontext danach:** 182:22.1, 183:22.1, 184:22.1

### Frame 182

- **frame_ms:** 22.119
- **stream_ms / apply / unload:** 17.007 / 12.465 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 179:22.2, 180:22.2, 181:22.1
- **Kontext danach:** 183:22.1, 184:22.1, 185:22.1

### Frame 183

- **frame_ms:** 22.133
- **stream_ms / apply / unload:** 17.026 / 12.492 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 180:22.2, 181:22.1, 182:22.1
- **Kontext danach:** 184:22.1, 185:22.1, 186:22.2

### Frame 184

- **frame_ms:** 22.072
- **stream_ms / apply / unload:** 16.957 / 12.415 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 181:22.1, 182:22.1, 183:22.1
- **Kontext danach:** 185:22.1, 186:22.2, 187:22.9

### Frame 185

- **frame_ms:** 22.107
- **stream_ms / apply / unload:** 17.037 / 12.453 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 182:22.1, 183:22.1, 184:22.1
- **Kontext danach:** 186:22.2, 187:22.9, 188:22.3

### Frame 186

- **frame_ms:** 22.238
- **stream_ms / apply / unload:** 17.114 / 12.486 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 183:22.1, 184:22.1, 185:22.1
- **Kontext danach:** 187:22.9, 188:22.3, 189:23.2

### Frame 187

- **frame_ms:** 22.865
- **stream_ms / apply / unload:** 17.697 / 13.026 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 184:22.1, 185:22.1, 186:22.2
- **Kontext danach:** 188:22.3, 189:23.2, 190:23.9

### Frame 188

- **frame_ms:** 22.278
- **stream_ms / apply / unload:** 17.134 / 12.609 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 185:22.1, 186:22.2, 187:22.9
- **Kontext danach:** 189:23.2, 190:23.9, 191:22.2

### Frame 189

- **frame_ms:** 23.180
- **stream_ms / apply / unload:** 17.867 / 13.348 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 186:22.2, 187:22.9, 188:22.3
- **Kontext danach:** 190:23.9, 191:22.2, 192:22.3

### Frame 190

- **frame_ms:** 23.941
- **stream_ms / apply / unload:** 18.805 / 13.811 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 187:22.9, 188:22.3, 189:23.2
- **Kontext danach:** 191:22.2, 192:22.3, 193:22.2

### Frame 191

- **frame_ms:** 22.248
- **stream_ms / apply / unload:** 17.076 / 12.581 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 188:22.3, 189:23.2, 190:23.9
- **Kontext danach:** 192:22.3, 193:22.2, 194:22.0

### Frame 192

- **frame_ms:** 22.298
- **stream_ms / apply / unload:** 17.163 / 12.548 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 189:23.2, 190:23.9, 191:22.2
- **Kontext danach:** 193:22.2, 194:22.0, 195:23.3

### Frame 193

- **frame_ms:** 22.238
- **stream_ms / apply / unload:** 17.121 / 12.575 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 190:23.9, 191:22.2, 192:22.3
- **Kontext danach:** 194:22.0, 195:23.3, 196:23.4

### Frame 194

- **frame_ms:** 22.001
- **stream_ms / apply / unload:** 16.907 / 12.415 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 191:22.2, 192:22.3, 193:22.2
- **Kontext danach:** 195:23.3, 196:23.4, 197:22.9

### Frame 195

- **frame_ms:** 23.284
- **stream_ms / apply / unload:** 18.098 / 13.007 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 192:22.3, 193:22.2, 194:22.0
- **Kontext danach:** 196:23.4, 197:22.9, 198:22.8

### Frame 196

- **frame_ms:** 23.403
- **stream_ms / apply / unload:** 18.171 / 13.082 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 193:22.2, 194:22.0, 195:23.3
- **Kontext danach:** 197:22.9, 198:22.8, 199:22.8

### Frame 197

- **frame_ms:** 22.853
- **stream_ms / apply / unload:** 17.720 / 12.654 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 194:22.0, 195:23.3, 196:23.4
- **Kontext danach:** 198:22.8, 199:22.8, 200:22.6

### Frame 198

- **frame_ms:** 22.779
- **stream_ms / apply / unload:** 17.654 / 12.664 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 195:23.3, 196:23.4, 197:22.9
- **Kontext danach:** 199:22.8, 200:22.6, 201:23.1

### Frame 199

- **frame_ms:** 22.828
- **stream_ms / apply / unload:** 17.636 / 12.923 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 196:23.4, 197:22.9, 198:22.8
- **Kontext danach:** 200:22.6, 201:23.1, 202:22.0

### Frame 200

- **frame_ms:** 22.625
- **stream_ms / apply / unload:** 17.454 / 12.844 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 197:22.9, 198:22.8, 199:22.8
- **Kontext danach:** 201:23.1, 202:22.0, 203:22.2

### Frame 201

- **frame_ms:** 23.053
- **stream_ms / apply / unload:** 17.890 / 12.800 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 198:22.8, 199:22.8, 200:22.6
- **Kontext danach:** 202:22.0, 203:22.2, 204:22.1

### Frame 202

- **frame_ms:** 22.029
- **stream_ms / apply / unload:** 16.914 / 12.464 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 199:22.8, 200:22.6, 201:23.1
- **Kontext danach:** 203:22.2, 204:22.1, 205:22.6

### Frame 203

- **frame_ms:** 22.184
- **stream_ms / apply / unload:** 17.030 / 12.485 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 200:22.6, 201:23.1, 202:22.0
- **Kontext danach:** 204:22.1, 205:22.6, 206:22.2

### Frame 204

- **frame_ms:** 22.127
- **stream_ms / apply / unload:** 16.853 / 12.316 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 201:23.1, 202:22.0, 203:22.2
- **Kontext danach:** 205:22.6, 206:22.2, 207:22.7

### Frame 205

- **frame_ms:** 22.565
- **stream_ms / apply / unload:** 17.316 / 12.671 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 202:22.0, 203:22.2, 204:22.1
- **Kontext danach:** 206:22.2, 207:22.7, 208:22.4

### Frame 206

- **frame_ms:** 22.225
- **stream_ms / apply / unload:** 17.081 / 12.540 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 203:22.2, 204:22.1, 205:22.6
- **Kontext danach:** 207:22.7, 208:22.4, 209:22.7

### Frame 207

- **frame_ms:** 22.672
- **stream_ms / apply / unload:** 17.334 / 12.748 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 204:22.1, 205:22.6, 206:22.2
- **Kontext danach:** 208:22.4, 209:22.7, 210:22.3

### Frame 208

- **frame_ms:** 22.373
- **stream_ms / apply / unload:** 17.008 / 12.481 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 205:22.6, 206:22.2, 207:22.7
- **Kontext danach:** 209:22.7, 210:22.3, 211:23.3

### Frame 209

- **frame_ms:** 22.717
- **stream_ms / apply / unload:** 17.577 / 12.637 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 206:22.2, 207:22.7, 208:22.4
- **Kontext danach:** 210:22.3, 211:23.3, 212:22.8

### Frame 210

- **frame_ms:** 22.259
- **stream_ms / apply / unload:** 17.143 / 12.563 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 32.0000
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 207:22.7, 208:22.4, 209:22.7
- **Kontext danach:** 211:23.3, 212:22.8, 213:22.0

### Frame 211

- **frame_ms:** 23.256
- **stream_ms / apply / unload:** 17.988 / 13.465 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 23.8514
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 208:22.4, 209:22.7, 210:22.3
- **Kontext danach:** 212:22.8, 213:22.0, 214:24.3

### Frame 212

- **frame_ms:** 22.818
- **stream_ms / apply / unload:** 17.693 / 12.741 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 20.5919
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 209:22.7, 210:22.3, 211:23.3
- **Kontext danach:** 213:22.0, 214:24.3, 215:22.1

### Frame 213

- **frame_ms:** 22.026
- **stream_ms / apply / unload:** 16.858 / 12.438 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 210:22.3, 211:23.3, 212:22.8
- **Kontext danach:** 214:24.3, 215:22.1, 216:22.1

### Frame 214

- **frame_ms:** 24.323
- **stream_ms / apply / unload:** 19.167 / 14.639 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 60.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 211:23.3, 212:22.8, 213:22.0
- **Kontext danach:** 215:22.1, 216:22.1, 217:22.7

### Frame 215

- **frame_ms:** 22.086
- **stream_ms / apply / unload:** 16.900 / 12.429 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 212:22.8, 213:22.0, 214:24.3
- **Kontext danach:** 216:22.1, 217:22.7, 218:22.4

### Frame 216

- **frame_ms:** 22.142
- **stream_ms / apply / unload:** 16.984 / 12.543 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 213:22.0, 214:24.3, 215:22.1
- **Kontext danach:** 217:22.7, 218:22.4, 219:22.1

### Frame 217

- **frame_ms:** 22.688
- **stream_ms / apply / unload:** 17.497 / 12.894 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 214:24.3, 215:22.1, 216:22.1
- **Kontext danach:** 218:22.4, 219:22.1, 220:22.1

### Frame 218

- **frame_ms:** 22.374
- **stream_ms / apply / unload:** 17.259 / 12.691 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 215:22.1, 216:22.1, 217:22.7
- **Kontext danach:** 219:22.1, 220:22.1, 221:22.1

### Frame 219

- **frame_ms:** 22.110
- **stream_ms / apply / unload:** 17.022 / 12.500 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 216:22.1, 217:22.7, 218:22.4
- **Kontext danach:** 220:22.1, 221:22.1, 222:23.7

### Frame 220

- **frame_ms:** 22.077
- **stream_ms / apply / unload:** 16.979 / 12.448 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 217:22.7, 218:22.4, 219:22.1
- **Kontext danach:** 221:22.1, 222:23.7, 223:23.5

### Frame 221

- **frame_ms:** 22.067
- **stream_ms / apply / unload:** 16.972 / 12.442 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 218:22.4, 219:22.1, 220:22.1
- **Kontext danach:** 222:23.7, 223:23.5, 224:24.0

### Frame 222

- **frame_ms:** 23.730
- **stream_ms / apply / unload:** 18.511 / 13.735 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 17.7778
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 219:22.1, 220:22.1, 221:22.1
- **Kontext danach:** 223:23.5, 224:24.0, 225:22.5

### Frame 223

- **frame_ms:** 23.463
- **stream_ms / apply / unload:** 18.343 / 13.381 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 15.3483
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 220:22.1, 221:22.1, 222:23.7
- **Kontext danach:** 224:24.0, 225:22.5, 226:22.3

### Frame 224

- **frame_ms:** 23.989
- **stream_ms / apply / unload:** 18.719 / 13.665 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 11.4399
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 221:22.1, 222:23.7, 223:23.5
- **Kontext danach:** 225:22.5, 226:22.3, 227:23.2

### Frame 225

- **frame_ms:** 22.500
- **stream_ms / apply / unload:** 17.275 / 12.701 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 222:23.7, 223:23.5, 224:24.0
- **Kontext danach:** 226:22.3, 227:23.2, 228:23.9

### Frame 226

- **frame_ms:** 22.280
- **stream_ms / apply / unload:** 17.122 / 12.588 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 223:23.5, 224:24.0, 225:22.5
- **Kontext danach:** 227:23.2, 228:23.9, 229:23.3

### Frame 227

- **frame_ms:** 23.208
- **stream_ms / apply / unload:** 17.974 / 12.983 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 224:24.0, 225:22.5, 226:22.3
- **Kontext danach:** 228:23.9, 229:23.3, 230:23.1

### Frame 228

- **frame_ms:** 23.850
- **stream_ms / apply / unload:** 17.797 / 12.695 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 225:22.5, 226:22.3, 227:23.2
- **Kontext danach:** 229:23.3, 230:23.1, 231:22.9

### Frame 229

- **frame_ms:** 23.277
- **stream_ms / apply / unload:** 17.914 / 12.915 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 226:22.3, 227:23.2, 228:23.9
- **Kontext danach:** 230:23.1, 231:22.9, 232:23.4

### Frame 230

- **frame_ms:** 23.118
- **stream_ms / apply / unload:** 17.848 / 12.963 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 227:23.2, 228:23.9, 229:23.3
- **Kontext danach:** 231:22.9, 232:23.4, 233:23.3

### Frame 231

- **frame_ms:** 22.944
- **stream_ms / apply / unload:** 17.715 / 12.675 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 228:23.9, 229:23.3, 230:23.1
- **Kontext danach:** 232:23.4, 233:23.3, 234:23.2

### Frame 232

- **frame_ms:** 23.368
- **stream_ms / apply / unload:** 18.182 / 12.873 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 229:23.3, 230:23.1, 231:22.9
- **Kontext danach:** 233:23.3, 234:23.2, 235:23.4

### Frame 233

- **frame_ms:** 23.338
- **stream_ms / apply / unload:** 18.037 / 13.010 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 8.5268
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 230:23.1, 231:22.9, 232:23.4
- **Kontext danach:** 234:23.2, 235:23.4, 236:23.8

### Frame 234

- **frame_ms:** 23.164
- **stream_ms / apply / unload:** 17.955 / 12.782 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 6.3555
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 231:22.9, 232:23.4, 233:23.3
- **Kontext danach:** 235:23.4, 236:23.8, 237:22.9

### Frame 235

- **frame_ms:** 23.377
- **stream_ms / apply / unload:** 18.115 / 12.933 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.7371
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 232:23.4, 233:23.3, 234:23.2
- **Kontext danach:** 236:23.8, 237:22.9, 238:23.5

### Frame 236

- **frame_ms:** 23.839
- **stream_ms / apply / unload:** 18.634 / 13.483 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 233:23.3, 234:23.2, 235:23.4
- **Kontext danach:** 237:22.9, 238:23.5, 239:29.9

### Frame 237

- **frame_ms:** 22.856
- **stream_ms / apply / unload:** 17.756 / 12.703 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 234:23.2, 235:23.4, 236:23.8
- **Kontext danach:** 238:23.5, 239:29.9, 240:23.7

### Frame 238

- **frame_ms:** 23.478
- **stream_ms / apply / unload:** 18.113 / 13.358 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 235:23.4, 236:23.8, 237:22.9
- **Kontext danach:** 239:29.9, 240:23.7, 241:22.5

### Frame 239

- **frame_ms:** 29.940
- **stream_ms / apply / unload:** 18.468 / 13.491 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 45.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 236:23.8, 237:22.9, 238:23.5
- **Kontext danach:** 240:23.7, 241:22.5, 242:23.3

### Frame 240

- **frame_ms:** 23.671
- **stream_ms / apply / unload:** 18.626 / 13.242 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 237:22.9, 238:23.5, 239:29.9
- **Kontext danach:** 241:22.5, 242:23.3, 243:23.3

### Frame 241

- **frame_ms:** 22.532
- **stream_ms / apply / unload:** 17.445 / 12.729 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 238:23.5, 239:29.9, 240:23.7
- **Kontext danach:** 242:23.3, 243:23.3, 244:23.3

### Frame 242

- **frame_ms:** 23.300
- **stream_ms / apply / unload:** 18.110 / 13.091 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 239:29.9, 240:23.7, 241:22.5
- **Kontext danach:** 243:23.3, 244:23.3, 245:23.5

### Frame 243

- **frame_ms:** 23.347
- **stream_ms / apply / unload:** 18.026 / 13.271 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 4.0897
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 240:23.7, 241:22.5, 242:23.3
- **Kontext danach:** 244:23.3, 245:23.5, 246:21.8

### Frame 244

- **frame_ms:** 23.326
- **stream_ms / apply / unload:** 18.192 / 13.179 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 3.5308
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 241:22.5, 242:23.3, 243:23.3
- **Kontext danach:** 245:23.5, 246:21.8, 247:22.1

### Frame 245

- **frame_ms:** 23.475
- **stream_ms / apply / unload:** 18.731 / 14.318 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 2.2721
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 242:23.3, 243:23.3, 244:23.3
- **Kontext danach:** 246:21.8, 247:22.1, 248:22.1

### Frame 246

- **frame_ms:** 21.798
- **stream_ms / apply / unload:** 17.105 / 12.677 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.9616
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 243:23.3, 244:23.3, 245:23.5
- **Kontext danach:** 247:22.1, 248:22.1, 249:21.8

### Frame 247

- **frame_ms:** 22.077
- **stream_ms / apply / unload:** 17.306 / 12.817 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 244:23.3, 245:23.5, 246:21.8
- **Kontext danach:** 248:22.1, 249:21.8, 250:22.0

### Frame 248

- **frame_ms:** 22.094
- **stream_ms / apply / unload:** 17.271 / 12.808 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 245:23.5, 246:21.8, 247:22.1
- **Kontext danach:** 249:21.8, 250:22.0, 251:21.7

### Frame 249

- **frame_ms:** 21.751
- **stream_ms / apply / unload:** 17.080 / 12.458 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 246:21.8, 247:22.1, 248:22.1
- **Kontext danach:** 250:22.0, 251:21.7, 252:22.0

### Frame 250

- **frame_ms:** 22.007
- **stream_ms / apply / unload:** 17.279 / 12.704 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 247:22.1, 248:22.1, 249:21.8
- **Kontext danach:** 251:21.7, 252:22.0, 253:22.0

### Frame 251

- **frame_ms:** 21.735
- **stream_ms / apply / unload:** 17.038 / 12.504 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 248:22.1, 249:21.8, 250:22.0
- **Kontext danach:** 252:22.0, 253:22.0, 254:22.3

### Frame 252

- **frame_ms:** 22.036
- **stream_ms / apply / unload:** 17.281 / 12.606 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 249:21.8, 250:22.0, 251:21.7
- **Kontext danach:** 253:22.0, 254:22.3, 255:21.7

### Frame 253

- **frame_ms:** 22.049
- **stream_ms / apply / unload:** 17.305 / 12.899 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 250:22.0, 251:21.7, 252:22.0
- **Kontext danach:** 254:22.3, 255:21.7, 256:22.2

### Frame 254

- **frame_ms:** 22.250
- **stream_ms / apply / unload:** 17.535 / 13.001 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.6935
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 251:21.7, 252:22.0, 253:22.0
- **Kontext danach:** 255:21.7, 256:22.2, 257:23.4

### Frame 255

- **frame_ms:** 21.735
- **stream_ms / apply / unload:** 16.984 / 12.560 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.4621
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 252:22.0, 253:22.0, 254:22.3
- **Kontext danach:** 256:22.2, 257:23.4, 258:23.5

### Frame 256

- **frame_ms:** 22.221
- **stream_ms / apply / unload:** 17.029 / 12.596 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 1.2623
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 253:22.0, 254:22.3, 255:21.7
- **Kontext danach:** 257:23.4, 258:23.5, 259:23.2

### Frame 257

- **frame_ms:** 23.357
- **stream_ms / apply / unload:** 18.232 / 13.207 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.9408
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 254:22.3, 255:21.7, 256:22.2
- **Kontext danach:** 258:23.5, 259:23.2, 260:23.3

### Frame 258

- **frame_ms:** 23.450
- **stream_ms / apply / unload:** 18.566 / 13.363 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 255:21.7, 256:22.2, 257:23.4
- **Kontext danach:** 259:23.2, 260:23.3, 261:22.6

### Frame 259

- **frame_ms:** 23.217
- **stream_ms / apply / unload:** 18.144 / 13.176 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 256:22.2, 257:23.4, 258:23.5
- **Kontext danach:** 260:23.3, 261:22.6, 262:21.9

### Frame 260

- **frame_ms:** 23.268
- **stream_ms / apply / unload:** 18.241 / 13.143 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 257:23.4, 258:23.5, 259:23.2
- **Kontext danach:** 261:22.6, 262:21.9, 263:22.3

### Frame 261

- **frame_ms:** 22.605
- **stream_ms / apply / unload:** 17.825 / 12.801 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 258:23.5, 259:23.2, 260:23.3
- **Kontext danach:** 262:21.9, 263:22.3, 264:22.2

### Frame 262

- **frame_ms:** 21.888
- **stream_ms / apply / unload:** 17.395 / 12.829 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 259:23.2, 260:23.3, 261:22.6
- **Kontext danach:** 263:22.3, 264:22.2, 265:21.6

### Frame 263

- **frame_ms:** 22.336
- **stream_ms / apply / unload:** 17.691 / 12.711 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 260:23.3, 261:22.6, 262:21.9
- **Kontext danach:** 264:22.2, 265:21.6, 266:21.6

### Frame 264

- **frame_ms:** 22.227
- **stream_ms / apply / unload:** 17.594 / 12.592 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 261:22.6, 262:21.9, 263:22.3
- **Kontext danach:** 265:21.6, 266:21.6, 267:21.5

### Frame 265

- **frame_ms:** 21.601
- **stream_ms / apply / unload:** 17.012 / 12.427 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 262:21.9, 263:22.3, 264:22.2
- **Kontext danach:** 266:21.6, 267:21.5, 268:21.8

### Frame 266

- **frame_ms:** 21.590
- **stream_ms / apply / unload:** 17.013 / 12.439 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.8123
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 263:22.3, 264:22.2, 265:21.6
- **Kontext danach:** 267:21.5, 268:21.8, 269:22.0

### Frame 267

- **frame_ms:** 21.541
- **stream_ms / apply / unload:** 16.905 / 12.271 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.7013
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 264:22.2, 265:21.6, 266:21.6
- **Kontext danach:** 268:21.8, 269:22.0, 270:22.9

### Frame 268

- **frame_ms:** 21.805
- **stream_ms / apply / unload:** 17.146 / 12.531 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.5227
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 265:21.6, 266:21.6, 267:21.5
- **Kontext danach:** 269:22.0, 270:22.9, 271:22.4

### Frame 269

- **frame_ms:** 21.965
- **stream_ms / apply / unload:** 17.207 / 12.504 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 266:21.6, 267:21.5, 268:21.8
- **Kontext danach:** 270:22.9, 271:22.4, 272:22.6

### Frame 270

- **frame_ms:** 22.887
- **stream_ms / apply / unload:** 18.213 / 13.309 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 267:21.5, 268:21.8, 269:22.0
- **Kontext danach:** 271:22.4, 272:22.6, 273:21.5

### Frame 271

- **frame_ms:** 22.399
- **stream_ms / apply / unload:** 17.737 / 12.660 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 268:21.8, 269:22.0, 270:22.9
- **Kontext danach:** 272:22.6, 273:21.5, 274:21.3

### Frame 272

- **frame_ms:** 22.639
- **stream_ms / apply / unload:** 18.012 / 12.958 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 269:22.0, 270:22.9, 271:22.4
- **Kontext danach:** 273:21.5, 274:21.3, 275:22.5

### Frame 273

- **frame_ms:** 21.483
- **stream_ms / apply / unload:** 16.808 / 12.339 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 270:22.9, 271:22.4, 272:22.6
- **Kontext danach:** 274:21.3, 275:22.5, 276:22.1

### Frame 274

- **frame_ms:** 21.340
- **stream_ms / apply / unload:** 16.789 / 12.283 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 271:22.4, 272:22.6, 273:21.5
- **Kontext danach:** 275:22.5, 276:22.1, 277:21.4

### Frame 275

- **frame_ms:** 22.526
- **stream_ms / apply / unload:** 17.931 / 13.354 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 272:22.6, 273:21.5, 274:21.3
- **Kontext danach:** 276:22.1, 277:21.4, 278:57.3

### Frame 276

- **frame_ms:** 22.149
- **stream_ms / apply / unload:** 17.548 / 12.816 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 273:21.5, 274:21.3, 275:22.5
- **Kontext danach:** 277:21.4, 278:57.3, 279:27.8

### Frame 277

- **frame_ms:** 21.375
- **stream_ms / apply / unload:** 16.825 / 12.327 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3896
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 274:21.3, 275:22.5, 276:22.1
- **Kontext danach:** 278:57.3, 279:27.8, 280:32.7

### Frame 278

- **frame_ms:** 57.272
- **stream_ms / apply / unload:** 47.222 / 42.692 / 0.007
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2904
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 74.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 275:22.5, 276:22.1, 277:21.4
- **Kontext danach:** 279:27.8, 280:32.7, 281:40.4

### Frame 279

- **frame_ms:** 27.790
- **stream_ms / apply / unload:** 19.567 / 13.567 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1869
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 48.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 276:22.1, 277:21.4, 278:57.3
- **Kontext danach:** 280:32.7, 281:40.4, 282:29.6

### Frame 280

- **frame_ms:** 32.706
- **stream_ms / apply / unload:** 27.179 / 17.366 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1869
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 277:21.4, 278:57.3, 279:27.8
- **Kontext danach:** 281:40.4, 282:29.6, 283:31.3

### Frame 281

- **frame_ms:** 40.352
- **stream_ms / apply / unload:** 33.538 / 27.693 / 0.008
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1869
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 68.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 278:57.3, 279:27.8, 280:32.7
- **Kontext danach:** 282:29.6, 283:31.3, 284:27.8

### Frame 282

- **frame_ms:** 29.614
- **stream_ms / apply / unload:** 24.747 / 17.610 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1869
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 279:27.8, 280:32.7, 281:40.4
- **Kontext danach:** 283:31.3, 284:27.8, 285:24.2

### Frame 283

- **frame_ms:** 31.295
- **stream_ms / apply / unload:** 25.647 / 17.356 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 55.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 280:32.7, 281:40.4, 282:29.6
- **Kontext danach:** 284:27.8, 285:24.2, 286:23.8

### Frame 284

- **frame_ms:** 27.787
- **stream_ms / apply / unload:** 22.360 / 17.451 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 62.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 281:40.4, 282:29.6, 283:31.3
- **Kontext danach:** 285:24.2, 286:23.8, 287:31.4

### Frame 285

- **frame_ms:** 24.166
- **stream_ms / apply / unload:** 19.232 / 14.297 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 59.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 282:29.6, 283:31.3, 284:27.8
- **Kontext danach:** 286:23.8, 287:31.4, 288:25.8

### Frame 286

- **frame_ms:** 23.753
- **stream_ms / apply / unload:** 18.729 / 13.966 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 283:31.3, 284:27.8, 285:24.2
- **Kontext danach:** 287:31.4, 288:25.8, 289:31.2

### Frame 287

- **frame_ms:** 31.426
- **stream_ms / apply / unload:** 22.104 / 15.274 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 48.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 284:27.8, 285:24.2, 286:23.8
- **Kontext danach:** 288:25.8, 289:31.2, 290:25.0

### Frame 288

- **frame_ms:** 25.766
- **stream_ms / apply / unload:** 20.620 / 15.786 / 0.005
- **stream_loaded / unloaded:** 3 / 0
- **chunk_count / zoom:** 18 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 61.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 285:24.2, 286:23.8, 287:31.4
- **Kontext danach:** 289:31.2, 290:25.0, 291:24.5

### Frame 289

- **frame_ms:** 31.216
- **stream_ms / apply / unload:** 25.891 / 20.966 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 67.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 286:23.8, 287:31.4, 288:25.8
- **Kontext danach:** 290:25.0, 291:24.5, 292:26.1

### Frame 290

- **frame_ms:** 24.958
- **stream_ms / apply / unload:** 19.459 / 14.657 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 20 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 58.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 287:31.4, 288:25.8, 289:31.2
- **Kontext danach:** 291:24.5, 292:26.1, 293:25.7

### Frame 291

- **frame_ms:** 24.491
- **stream_ms / apply / unload:** 18.819 / 14.122 / 0.005
- **stream_loaded / unloaded:** 1 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 57.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 288:25.8, 289:31.2, 290:25.0
- **Kontext danach:** 292:26.1, 293:25.7, 294:24.0

### Frame 292

- **frame_ms:** 26.127
- **stream_ms / apply / unload:** 19.998 / 14.844 / 0.005
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 23 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 56.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 289:31.2, 290:25.0, 291:24.5
- **Kontext danach:** 293:25.7, 294:24.0, 295:23.7

### Frame 293

- **frame_ms:** 25.734
- **stream_ms / apply / unload:** 19.069 / 14.089 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 54.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 290:25.0, 291:24.5, 292:26.1
- **Kontext danach:** 294:24.0, 295:23.7, 296:25.7

### Frame 294

- **frame_ms:** 24.022
- **stream_ms / apply / unload:** 17.478 / 12.922 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 291:24.5, 292:26.1, 293:25.7
- **Kontext danach:** 295:23.7, 296:25.7, 297:24.5

### Frame 295

- **frame_ms:** 23.692
- **stream_ms / apply / unload:** 17.044 / 12.493 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 292:26.1, 293:25.7, 294:24.0
- **Kontext danach:** 296:25.7, 297:24.5, 298:24.2

### Frame 296

- **frame_ms:** 25.698
- **stream_ms / apply / unload:** 18.484 / 13.189 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 51.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 293:25.7, 294:24.0, 295:23.7
- **Kontext danach:** 297:24.5, 298:24.2, 299:24.2

### Frame 297

- **frame_ms:** 24.484
- **stream_ms / apply / unload:** 17.708 / 13.068 / 0.006
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
- **Kontext davor:** 294:24.0, 295:23.7, 296:25.7
- **Kontext danach:** 298:24.2, 299:24.2, 300:23.8

### Frame 298

- **frame_ms:** 24.198
- **stream_ms / apply / unload:** 17.611 / 12.665 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 295:23.7, 296:25.7, 297:24.5
- **Kontext danach:** 299:24.2, 300:23.8, 301:26.5

### Frame 299

- **frame_ms:** 24.198
- **stream_ms / apply / unload:** 17.485 / 12.868 / 0.006
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
- **Kontext davor:** 296:25.7, 297:24.5, 298:24.2
- **Kontext danach:** 300:23.8, 301:26.5, 302:24.9

### Frame 300

- **frame_ms:** 23.801
- **stream_ms / apply / unload:** 17.183 / 12.548 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 41 Hitches in einem 20-Frame-Fenster (Spanne 40).
- **Kontext davor:** 297:24.5, 298:24.2, 299:24.2
- **Kontext danach:** 301:26.5, 302:24.9, 303:23.9

### Frame 301

- **frame_ms:** 26.493
- **stream_ms / apply / unload:** 19.775 / 14.016 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 40 Hitches in einem 20-Frame-Fenster (Spanne 39).
- **Kontext davor:** 298:24.2, 299:24.2, 300:23.8
- **Kontext danach:** 302:24.9, 303:23.9, 304:24.4

### Frame 302

- **frame_ms:** 24.891
- **stream_ms / apply / unload:** 18.153 / 13.272 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 39 Hitches in einem 20-Frame-Fenster (Spanne 38).
- **Kontext davor:** 299:24.2, 300:23.8, 301:26.5
- **Kontext danach:** 303:23.9, 304:24.4, 305:33.5

### Frame 303

- **frame_ms:** 23.890
- **stream_ms / apply / unload:** 17.302 / 12.637 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 38 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 300:23.8, 301:26.5, 302:24.9
- **Kontext danach:** 304:24.4, 305:33.5, 306:24.8

### Frame 304

- **frame_ms:** 24.440
- **stream_ms / apply / unload:** 17.812 / 12.941 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 37 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 301:26.5, 302:24.9, 303:23.9
- **Kontext danach:** 305:33.5, 306:24.8, 307:25.1

### Frame 305

- **frame_ms:** 33.519
- **stream_ms / apply / unload:** 18.712 / 13.675 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 36 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 302:24.9, 303:23.9, 304:24.4
- **Kontext danach:** 306:24.8, 307:25.1, 308:24.3

### Frame 306

- **frame_ms:** 24.751
- **stream_ms / apply / unload:** 18.181 / 13.008 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 35 Hitches in einem 20-Frame-Fenster (Spanne 34).
- **Kontext davor:** 303:23.9, 304:24.4, 305:33.5
- **Kontext danach:** 307:25.1, 308:24.3, 309:25.0

### Frame 307

- **frame_ms:** 25.130
- **stream_ms / apply / unload:** 18.483 / 13.173 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 34 Hitches in einem 20-Frame-Fenster (Spanne 33).
- **Kontext davor:** 304:24.4, 305:33.5, 306:24.8
- **Kontext danach:** 308:24.3, 309:25.0, 310:23.5

### Frame 308

- **frame_ms:** 24.298
- **stream_ms / apply / unload:** 17.581 / 12.627 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 33 Hitches in einem 20-Frame-Fenster (Spanne 32).
- **Kontext davor:** 305:33.5, 306:24.8, 307:25.1
- **Kontext danach:** 309:25.0, 310:23.5, 311:24.0

### Frame 309

- **frame_ms:** 24.994
- **stream_ms / apply / unload:** 18.336 / 12.987 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 32 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 306:24.8, 307:25.1, 308:24.3
- **Kontext danach:** 310:23.5, 311:24.0, 312:23.8

### Frame 310

- **frame_ms:** 23.543
- **stream_ms / apply / unload:** 16.951 / 12.434 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 31 Hitches in einem 20-Frame-Fenster (Spanne 30).
- **Kontext davor:** 307:25.1, 308:24.3, 309:25.0
- **Kontext danach:** 311:24.0, 312:23.8, 313:24.1

### Frame 311

- **frame_ms:** 23.990
- **stream_ms / apply / unload:** 17.474 / 12.839 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 30 Hitches in einem 20-Frame-Fenster (Spanne 29).
- **Kontext davor:** 308:24.3, 309:25.0, 310:23.5
- **Kontext danach:** 312:23.8, 313:24.1, 314:23.7

### Frame 312

- **frame_ms:** 23.801
- **stream_ms / apply / unload:** 17.248 / 12.724 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 29 Hitches in einem 20-Frame-Fenster (Spanne 28).
- **Kontext davor:** 309:25.0, 310:23.5, 311:24.0
- **Kontext danach:** 313:24.1, 314:23.7, 315:23.5

### Frame 313

- **frame_ms:** 24.091
- **stream_ms / apply / unload:** 17.244 / 12.681 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 28 Hitches in einem 20-Frame-Fenster (Spanne 27).
- **Kontext davor:** 310:23.5, 311:24.0, 312:23.8
- **Kontext danach:** 314:23.7, 315:23.5, 316:24.9

### Frame 314

- **frame_ms:** 23.651
- **stream_ms / apply / unload:** 17.026 / 12.500 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 27 Hitches in einem 20-Frame-Fenster (Spanne 26).
- **Kontext davor:** 311:24.0, 312:23.8, 313:24.1
- **Kontext danach:** 315:23.5, 316:24.9, 317:23.5

### Frame 315

- **frame_ms:** 23.499
- **stream_ms / apply / unload:** 16.982 / 12.490 / 0.006
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
- **Kontext davor:** 312:23.8, 313:24.1, 314:23.7
- **Kontext danach:** 316:24.9, 317:23.5, 318:23.6

### Frame 316

- **frame_ms:** 24.857
- **stream_ms / apply / unload:** 18.205 / 13.299 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 25 Hitches in einem 20-Frame-Fenster (Spanne 24).
- **Kontext davor:** 313:24.1, 314:23.7, 315:23.5
- **Kontext danach:** 317:23.5, 318:23.6, 319:23.5

### Frame 317

- **frame_ms:** 23.550
- **stream_ms / apply / unload:** 17.015 / 12.463 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 24 Hitches in einem 20-Frame-Fenster (Spanne 23).
- **Kontext davor:** 314:23.7, 315:23.5, 316:24.9
- **Kontext danach:** 318:23.6, 319:23.5, 320:23.7

### Frame 318

- **frame_ms:** 23.565
- **stream_ms / apply / unload:** 17.071 / 12.516 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 23 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 315:23.5, 316:24.9, 317:23.5
- **Kontext danach:** 319:23.5, 320:23.7

### Frame 319

- **frame_ms:** 23.503
- **stream_ms / apply / unload:** 16.973 / 12.463 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 53.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 22 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 316:24.9, 317:23.5, 318:23.6
- **Kontext danach:** 320:23.7

### Frame 320

- **frame_ms:** 23.689
- **stream_ms / apply / unload:** 17.051 / 12.503 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 52.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 317:23.5, 318:23.6, 319:23.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 23.059 | 22.262 | 26.493 | 57.272 |
| stream_ms | 17.822 | 17.279 | 19.232 | 47.222 |
| stream_apply_ms | 13.050 | 12.654 | 14.297 | 42.692 |
| stream_unload_ms | 0.005 | 0.005 | 0.006 | 0.008 |
| stream_loaded | 0.044 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 16.763 | 16.000 | 24.000 | 24.000 |
| zoom | 8.447 | 1.262 | 32.000 | 32.000 |
| deco_extract_ms | 4.891 | 4.515 | 6.558 | 14.660 |
| tile_extract_ms | 0.330 | 0.228 | 0.642 | 0.708 |
| extract_ms | 5.221 | 5.080 | 6.695 | 14.791 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.924, n=321): Pearson r=0.924 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_apply_ms** (r=0.901, n=321): Pearson r=0.901 (stark) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unload_ms** (r=0.459, n=321): Pearson r=0.459 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_loaded** (r=0.152, n=321): Pearson r=0.152 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ stream_unloaded** (r=n/a, n=321): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.201, n=321): Pearson r=0.201 (schwach) — nur Indiz, keine Kausalität.
- **frame_ms ↔ zoom** (r=-0.110, n=321): Pearson r=-0.110 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ pending_unload_count** (r=n/a, n=321): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.640, n=321): Pearson r=0.640 (moderat) — nur Indiz, keine Kausalität.
- **frame_ms ↔ tile_extract_ms** (r=-0.014, n=321): Pearson r=-0.014 (vernachlässigbar) — nur Indiz, keine Kausalität.
- **frame_ms ↔ extract_ms** (r=0.643, n=321): Pearson r=0.643 (moderat) — nur Indiz, keine Kausalität.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 1/321 Frames (0.3%).
- stream_unloaded am Unload-Cap (2): 0/321 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 1/321 (0.3%).
- Hitchs mit stream_unloaded am Cap: 0/321 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/321 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: apply_dominant (Load-/Apply-dominant) in 314/321 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 77.3%, Apply 56.6%, Unload 0.0%, Extract 22.6%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 22.6%.
- Häufigstes Hitch-Muster: periodic_cluster (321×).

## Offene Fragen

- 7 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
