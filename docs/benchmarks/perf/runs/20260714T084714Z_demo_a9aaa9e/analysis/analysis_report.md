# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T084714Z_demo_a9aaa9e`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 335
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T08:47:32.303920+00:00
- **git_commit:** a9aaa9e

### Config-Fingerprints

- `profiling`: `6283327464990334584`
- `streaming`: `6316402554757774428`
- `visibility_lod`: `8674576106818500327`
- `world_gen`: `4794244940440254489`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, present_wait_cpu_ms, render_cpu_ms, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 10.9992 | 10.9992 | +0.0000 | OK |
| frame_ms_p95 | 13.9141 | 13.9141 | +0.0000 | OK |
| frame_ms_max | 42.3338 | 42.3338 | +0.0000 | OK |
| stream_ms_mean | 5.2640 | 5.2640 | +0.0000 | OK |
| stream_ms_p95 | 9.2887 | 9.2887 | +0.0000 | OK |
| stream_ms_max | 37.9413 | 37.9413 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0049 | 0.0049 | +0.0000 | OK |
| stream_unload_ms_max | 0.0115 | 0.0115 | +0.0000 | OK |
| chunk_count_mean | 23.1731 | 23.1731 | +0.0000 | OK |
| recorded_frames | 335.0000 | 335.0000 | +0.0000 | OK |
| hitch_count | 31.0000 | 31.0000 | +0.0000 | OK |
| hitch_frame_count | 4.0000 | 4.0000 | +0.0000 | OK |
| hitch_stream_count | 31.0000 | 31.0000 | +0.0000 | OK |
| hitch_load_count | 2.0000 | 2.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Nicht eindeutig** (dominant_bottleneck, Konfidenz: hoch)
   - In 21/31 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch extract_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 52.0% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 47.9% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (42.33) deutlich über P95 (13.91) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `stream_slow`: 31
- `frame_slow`: 4
- `load_burst`: 2

### Frame 0

- **frame_ms:** 11.880
- **stream_ms / apply / unload:** 8.650 / 4.170 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 4 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext danach:** 1:11.4, 2:13.6, 3:8.5

### Frame 1

- **frame_ms:** 11.422
- **stream_ms / apply / unload:** 8.373 / 4.159 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 15 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 36.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 5 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 0:11.9
- **Kontext danach:** 2:13.6, 3:8.5, 4:7.9

### Frame 2

- **frame_ms:** 13.602
- **stream_ms / apply / unload:** 9.556 / 5.031 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 6 Hitches in einem 20-Frame-Fenster (Spanne 22).
- **Kontext davor:** 0:11.9, 1:11.4
- **Kontext danach:** 3:8.5, 4:7.9, 5:8.1

### Frame 20

- **frame_ms:** 42.334
- **stream_ms / apply / unload:** 37.941 / 33.484 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 79.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Burst mit Nachlauf
  - Hitch frame_ms (42.33) deutlich über Nachbar-Mittel (12.88).
  - Weitere Hitches in ±3 Frames: [21, 22, 23].
- **Kontext davor:** 17:8.2, 18:8.1, 19:8.1
- **Kontext danach:** 21:13.6, 22:26.1, 23:13.2

### Frame 21

- **frame_ms:** 13.553
- **stream_ms / apply / unload:** 9.186 / 4.636 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2252
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 21 Hitches in einem 20-Frame-Fenster (Spanne 37).
- **Kontext davor:** 18:8.1, 19:8.1, 20:42.3
- **Kontext danach:** 22:26.1, 23:13.2, 24:13.4

### Frame 22

- **frame_ms:** 26.118
- **stream_ms / apply / unload:** 18.629 / 9.286 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 36).
- **Kontext davor:** 19:8.1, 20:42.3, 21:13.6
- **Kontext danach:** 23:13.2, 24:13.4, 25:13.0

### Frame 23

- **frame_ms:** 13.211
- **stream_ms / apply / unload:** 9.289 / 4.595 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 20:42.3, 21:13.6, 22:26.1
- **Kontext danach:** 24:13.4, 25:13.0, 26:13.4

### Frame 24

- **frame_ms:** 13.354
- **stream_ms / apply / unload:** 9.216 / 4.542 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 21:13.6, 22:26.1, 23:13.2
- **Kontext danach:** 25:13.0, 26:13.4, 27:20.5

### Frame 25

- **frame_ms:** 13.036
- **stream_ms / apply / unload:** 9.225 / 4.571 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 22:26.1, 23:13.2, 24:13.4
- **Kontext danach:** 26:13.4, 27:20.5, 28:15.0

### Frame 26

- **frame_ms:** 13.372
- **stream_ms / apply / unload:** 9.413 / 4.660 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 23:13.2, 24:13.4, 25:13.0
- **Kontext danach:** 27:20.5, 28:15.0, 29:13.4

### Frame 27

- **frame_ms:** 20.451
- **stream_ms / apply / unload:** 16.605 / 8.221 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 40.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 24:13.4, 25:13.0, 26:13.4
- **Kontext danach:** 28:15.0, 29:13.4, 30:13.1

### Frame 28

- **frame_ms:** 15.048
- **stream_ms / apply / unload:** 11.093 / 6.411 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 42.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 25:13.0, 26:13.4, 27:20.5
- **Kontext danach:** 29:13.4, 30:13.1, 31:12.9

### Frame 29

- **frame_ms:** 13.385
- **stream_ms / apply / unload:** 9.493 / 4.968 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 26:13.4, 27:20.5, 28:15.0
- **Kontext danach:** 30:13.1, 31:12.9, 32:13.9

### Frame 30

- **frame_ms:** 13.116
- **stream_ms / apply / unload:** 8.949 / 4.404 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 27:20.5, 28:15.0, 29:13.4
- **Kontext danach:** 31:12.9, 32:13.9, 33:13.1

### Frame 31

- **frame_ms:** 12.939
- **stream_ms / apply / unload:** 9.078 / 4.524 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 28:15.0, 29:13.4, 30:13.1
- **Kontext danach:** 32:13.9, 33:13.1, 34:13.8

### Frame 32

- **frame_ms:** 13.914
- **stream_ms / apply / unload:** 9.676 / 5.244 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 37.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 29:13.4, 30:13.1, 31:12.9
- **Kontext danach:** 33:13.1, 34:13.8, 35:14.6

### Frame 33

- **frame_ms:** 13.130
- **stream_ms / apply / unload:** 8.866 / 4.386 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 30:13.1, 31:12.9, 32:13.9
- **Kontext danach:** 34:13.8, 35:14.6, 36:14.4

### Frame 34

- **frame_ms:** 13.838
- **stream_ms / apply / unload:** 9.335 / 4.898 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 20 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 31:12.9, 32:13.9, 33:13.1
- **Kontext danach:** 35:14.6, 36:14.4, 37:15.1

### Frame 35

- **frame_ms:** 14.608
- **stream_ms / apply / unload:** 10.028 / 5.020 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 32:13.9, 33:13.1, 34:13.8
- **Kontext danach:** 36:14.4, 37:15.1, 38:15.5

### Frame 36

- **frame_ms:** 14.425
- **stream_ms / apply / unload:** 9.440 / 4.510 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 33:13.1, 34:13.8, 35:14.6
- **Kontext danach:** 37:15.1, 38:15.5, 39:10.7

### Frame 37

- **frame_ms:** 15.134
- **stream_ms / apply / unload:** 9.975 / 5.065 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 22 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 34:13.8, 35:14.6, 36:14.4
- **Kontext danach:** 38:15.5, 39:10.7, 40:10.8

### Frame 38

- **frame_ms:** 15.484
- **stream_ms / apply / unload:** 9.860 / 5.518 / 0.005
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 35.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 35:14.6, 36:14.4, 37:15.1
- **Kontext danach:** 39:10.7, 40:10.8, 41:10.1

### Frame 69

- **frame_ms:** 15.019
- **stream_ms / apply / unload:** 8.865 / 4.396 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 66:10.4, 67:10.9, 68:10.5
- **Kontext danach:** 70:10.6, 71:10.4, 72:10.9

### Frame 100

- **frame_ms:** 15.335
- **stream_ms / apply / unload:** 9.422 / 4.436 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 97:10.6, 98:10.4, 99:10.9
- **Kontext danach:** 101:10.2, 102:11.1, 103:10.6

### Frame 131

- **frame_ms:** 14.388
- **stream_ms / apply / unload:** 8.677 / 4.274 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 128:10.1, 129:10.8, 130:10.4
- **Kontext danach:** 132:10.9, 133:10.6, 134:10.2

### Frame 162

- **frame_ms:** 16.008
- **stream_ms / apply / unload:** 9.751 / 4.453 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Konstanter Kostentreiber
  - Hoher Stream-Anteil ohne klaren Einzelspike.
- **Kontext davor:** 159:10.9, 160:10.8, 161:11.8
- **Kontext danach:** 163:11.1, 164:10.9, 165:10.6

### Frame 193

- **frame_ms:** 14.857
- **stream_ms / apply / unload:** 9.147 / 4.308 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 190:10.1, 191:11.5, 192:11.1
- **Kontext danach:** 194:10.7, 195:10.8, 196:10.1

### Frame 224

- **frame_ms:** 15.206
- **stream_ms / apply / unload:** 9.407 / 4.543 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 221:10.6, 222:10.6, 223:10.8
- **Kontext danach:** 225:10.2, 226:10.5, 227:10.9

### Frame 255

- **frame_ms:** 14.646
- **stream_ms / apply / unload:** 8.689 / 4.232 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 252:10.5, 253:10.3, 254:10.2
- **Kontext danach:** 256:10.4, 257:11.0, 258:11.3

### Frame 286

- **frame_ms:** 15.083
- **stream_ms / apply / unload:** 9.305 / 4.395 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 283:10.9, 284:11.4, 285:10.6
- **Kontext danach:** 287:10.3, 288:11.2, 289:10.3

### Frame 317

- **frame_ms:** 14.838
- **stream_ms / apply / unload:** 9.032 / 4.407 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 314:10.3, 315:10.3, 316:10.8
- **Kontext danach:** 318:11.2, 319:10.7, 320:11.0

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 10.999 | 10.694 | 13.914 | 42.334 |
| stream_ms | 5.264 | 4.738 | 9.289 | 37.941 |
| stream_apply_ms | 0.567 | 0.027 | 4.524 | 33.484 |
| stream_unload_ms | 0.004 | 0.004 | 0.005 | 0.012 |
| stream_loaded | 0.054 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 23.173 | 24.000 | 24.000 | 24.000 |
| zoom | 0.191 | 0.180 | 0.350 | 0.350 |
| deco_extract_ms | 5.593 | 5.713 | 6.218 | 7.277 |
| tile_extract_ms | 0.126 | 0.126 | 0.137 | 0.291 |
| extract_ms | 5.719 | 5.845 | 6.376 | 7.464 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 46.009 | 46.859 | 51.147 | 75.598 |
| render_cpu_ms | 0.295 | 0.288 | 0.324 | 0.725 |
| present_wait_cpu_ms | 0.089 | 0.087 | 0.102 | 0.315 |
| cpu_unattributed_ms | 34.625 | 35.696 | 37.226 | 60.183 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.959, n=335): Hitch-Frames: stream_ms-Mittel 10.780 vs. übrige 4.702 (Faktor 2.29). Pearson r=0.959 (stark).
- **frame_ms ↔ stream_apply_ms** (r=0.929, n=335): Hitch-Frames: stream_apply_ms-Mittel 5.863 vs. übrige 0.027 (Faktor 216.29). Pearson r=0.929 (stark).
- **frame_ms ↔ stream_unload_ms** (r=0.058, n=335): Hitch-Frames: stream_unload_ms-Mittel 0.004 vs. übrige 0.004 (Faktor 0.97). Pearson r=0.058 (vernachlässigbar).
- **frame_ms ↔ stream_loaded** (r=0.200, n=335): Hitch-Frames: stream_loaded-Mittel 0.581 vs. übrige 0.000 (Faktor inf). Pearson r=0.200 (vernachlässigbar).
- **frame_ms ↔ stream_unloaded** (r=n/a, n=335): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=-0.179, n=335): Hitch-Frames: chunk_count-Mittel 19.452 vs. übrige 23.553 (Faktor 0.83). Pearson r=-0.179 (vernachlässigbar).
- **frame_ms ↔ zoom** (r=-0.112, n=335): Hitch-Frames: zoom-Mittel 0.202 vs. übrige 0.190 (Faktor 1.07). Pearson r=-0.112 (vernachlässigbar).
- **frame_ms ↔ pending_unload_count** (r=n/a, n=335): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=-0.008, n=335): Hitch-Frames: deco_extract_ms-Mittel 4.657 vs. übrige 5.689 (Faktor 0.82). Pearson r=-0.008 (vernachlässigbar).
- **frame_ms ↔ tile_extract_ms** (r=0.481, n=335): Hitch-Frames: tile_extract_ms-Mittel 0.120 vs. übrige 0.127 (Faktor 0.94). Pearson r=0.481 (moderat).
- **frame_ms ↔ extract_ms** (r=0.004, n=335): Hitch-Frames: extract_ms-Mittel 4.777 vs. übrige 5.815 (Faktor 0.82). Pearson r=0.004 (vernachlässigbar).
- **cpu_full_frame_ms ↔ stream_ms** (r=0.351, n=335): Pearson r=0.351 (schwach) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.593, n=335): Pearson r=0.593 (moderat) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=0.268, n=335): Pearson r=0.268 (schwach) zwischen cpu_full_frame_ms und render_cpu_ms.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=0.211, n=335): Pearson r=0.211 (schwach) zwischen cpu_full_frame_ms und present_wait_cpu_ms.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 2/335 Frames (0.6%).
- stream_unloaded am Unload-Cap (2): 0/335 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 2/31 (6.5%).
- Hitchs mit stream_unloaded am Cap: 0/31 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/335 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: unclear (Nicht eindeutig) in 21/31 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 47.9%, Apply 5.2%, Unload 0.0%, Extract 52.0%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 32.0%.
- Häufigstes Hitch-Muster: periodic_cluster (21×).

## Offene Fragen

- 21 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
