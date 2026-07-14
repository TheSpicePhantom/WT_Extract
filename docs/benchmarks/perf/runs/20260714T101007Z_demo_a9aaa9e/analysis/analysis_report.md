# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T101007Z_demo_a9aaa9e`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 321
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T10:10:20.084339+00:00
- **git_commit:** a9aaa9e

### Config-Fingerprints

- `profiling`: `-117422704200611592`
- `streaming`: `2804618425307970701`
- `visibility_lod`: `-9180978099767775273`
- `world_gen`: `-2529664552746078696`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, present_wait_cpu_ms, render_cpu_ms, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 10.3676 | 10.3676 | +0.0000 | OK |
| frame_ms_p95 | 15.3483 | 15.3483 | +0.0000 | OK |
| frame_ms_max | 45.8421 | 45.8421 | +0.0000 | OK |
| stream_ms_mean | 5.5271 | 5.5271 | +0.0000 | OK |
| stream_ms_p95 | 9.8496 | 9.8496 | +0.0000 | OK |
| stream_ms_max | 39.4875 | 39.4875 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0049 | 0.0049 | +0.0000 | OK |
| stream_unload_ms_max | 0.0061 | 0.0061 | +0.0000 | OK |
| chunk_count_mean | 17.4206 | 17.4206 | +0.0000 | OK |
| recorded_frames | 321.0000 | 321.0000 | +0.0000 | OK |
| hitch_count | 30.0000 | 30.0000 | +0.0000 | OK |
| hitch_frame_count | 14.0000 | 14.0000 | +0.0000 | OK |
| hitch_stream_count | 28.0000 | 28.0000 | +0.0000 | OK |
| hitch_load_count | 1.0000 | 1.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Nicht eindeutig** (dominant_bottleneck, Konfidenz: hoch)
   - In 24/30 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch stream_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 53.3% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: extract_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 46.5% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (45.84) deutlich über P95 (15.35) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `stream_slow`: 28
- `frame_slow`: 14
- `load_burst`: 1

### Frame 29

- **frame_ms:** 12.812
- **stream_ms / apply / unload:** 8.722 / 4.220 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 26:8.8, 27:8.7, 28:9.3
- **Kontext danach:** 30:10.0, 31:9.7, 32:9.0

### Frame 60

- **frame_ms:** 13.075
- **stream_ms / apply / unload:** 8.768 / 4.288 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 57:11.8, 58:8.8, 59:9.4
- **Kontext danach:** 61:8.6, 62:9.4, 63:9.0

### Frame 91

- **frame_ms:** 16.941
- **stream_ms / apply / unload:** 11.789 / 5.652 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Konstanter Kostentreiber
  - Hoher Stream-Anteil ohne klaren Einzelspike.
- **Kontext davor:** 88:8.8, 89:9.8, 90:9.6
- **Kontext danach:** 92:9.1, 93:10.6, 94:8.8

### Frame 111

- **frame_ms:** 16.257
- **stream_ms / apply / unload:** 5.365 / 0.024 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** frame_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 0.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
- **Kontextmuster:** Wiederkehrendes Cluster
  - 3 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 108:8.8, 109:8.7, 110:9.1
- **Kontext danach:** 112:9.2, 113:9.4, 114:9.8

### Frame 122

- **frame_ms:** 14.798
- **stream_ms / apply / unload:** 10.655 / 4.634 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 119:10.4, 120:9.8, 121:9.8
- **Kontext danach:** 123:9.0, 124:8.8, 125:8.7

### Frame 153

- **frame_ms:** 13.523
- **stream_ms / apply / unload:** 9.395 / 4.484 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 150:8.9, 151:8.7, 152:9.0
- **Kontext danach:** 154:8.6, 155:9.5, 156:9.5

### Frame 184

- **frame_ms:** 13.217
- **stream_ms / apply / unload:** 9.103 / 4.454 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 181:8.8, 182:8.8, 183:8.8
- **Kontext danach:** 185:9.8, 186:9.7, 187:9.7

### Frame 215

- **frame_ms:** 13.484
- **stream_ms / apply / unload:** 9.237 / 4.540 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 212:9.2, 213:9.5, 214:9.0
- **Kontext danach:** 216:9.7, 217:9.9, 218:9.4

### Frame 246

- **frame_ms:** 13.076
- **stream_ms / apply / unload:** 8.858 / 4.327 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 243:15.8, 244:8.5, 245:8.8
- **Kontext danach:** 247:8.8, 248:8.8, 249:45.8

### Frame 249

- **frame_ms:** 45.842
- **stream_ms / apply / unload:** 39.488 / 34.883 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 76.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Burst mit Nachlauf
  - Hitch frame_ms (45.84) deutlich über Nachbar-Mittel (12.85).
  - Weitere Hitches in ±3 Frames: [246, 250, 251, 252].
- **Kontext davor:** 246:13.1, 247:8.8, 248:8.8
- **Kontext danach:** 250:14.6, 251:17.2, 252:14.7

### Frame 250

- **frame_ms:** 14.563
- **stream_ms / apply / unload:** 9.902 / 4.726 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 247:8.8, 248:8.8, 249:45.8
- **Kontext danach:** 251:17.2, 252:14.7, 253:14.7

### Frame 251

- **frame_ms:** 17.169
- **stream_ms / apply / unload:** 12.499 / 4.679 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2609
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 248:8.8, 249:45.8, 250:14.6
- **Kontext danach:** 252:14.7, 253:14.7, 254:14.5

### Frame 252

- **frame_ms:** 14.708
- **stream_ms / apply / unload:** 9.617 / 4.835 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2252
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 249:45.8, 250:14.6, 251:17.2
- **Kontext danach:** 253:14.7, 254:14.5, 255:17.0

### Frame 253

- **frame_ms:** 14.740
- **stream_ms / apply / unload:** 9.850 / 4.894 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1944
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 250:14.6, 251:17.2, 252:14.7
- **Kontext danach:** 254:14.5, 255:17.0, 256:13.8

### Frame 254

- **frame_ms:** 14.539
- **stream_ms / apply / unload:** 9.759 / 4.943 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 251:17.2, 252:14.7, 253:14.7
- **Kontext danach:** 255:17.0, 256:13.8, 257:13.6

### Frame 255

- **frame_ms:** 17.033
- **stream_ms / apply / unload:** 12.263 / 5.250 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 252:14.7, 253:14.7, 254:14.5
- **Kontext danach:** 256:13.8, 257:13.6, 258:20.9

### Frame 256

- **frame_ms:** 13.792
- **stream_ms / apply / unload:** 9.450 / 4.627 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 253:14.7, 254:14.5, 255:17.0
- **Kontext danach:** 257:13.6, 258:20.9, 259:19.9

### Frame 257

- **frame_ms:** 13.574
- **stream_ms / apply / unload:** 9.280 / 4.633 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 254:14.5, 255:17.0, 256:13.8
- **Kontext danach:** 258:20.9, 259:19.9, 260:16.7

### Frame 258

- **frame_ms:** 20.913
- **stream_ms / apply / unload:** 14.449 / 5.235 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 25.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 255:17.0, 256:13.8, 257:13.6
- **Kontext danach:** 259:19.9, 260:16.7, 261:14.9

### Frame 259

- **frame_ms:** 19.852
- **stream_ms / apply / unload:** 15.169 / 5.568 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 256:13.8, 257:13.6, 258:20.9
- **Kontext danach:** 260:16.7, 261:14.9, 262:15.3

### Frame 260

- **frame_ms:** 16.689
- **stream_ms / apply / unload:** 12.373 / 4.995 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 257:13.6, 258:20.9, 259:19.9
- **Kontext danach:** 261:14.9, 262:15.3, 263:18.5

### Frame 261

- **frame_ms:** 14.921
- **stream_ms / apply / unload:** 10.412 / 5.084 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 258:20.9, 259:19.9, 260:16.7
- **Kontext danach:** 262:15.3, 263:18.5, 264:16.6

### Frame 262

- **frame_ms:** 15.348
- **stream_ms / apply / unload:** 10.706 / 5.132 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 18 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 259:19.9, 260:16.7, 261:14.9
- **Kontext danach:** 263:18.5, 264:16.6, 265:18.1

### Frame 263

- **frame_ms:** 18.505
- **stream_ms / apply / unload:** 13.434 / 8.032 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 43.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 260:16.7, 261:14.9, 262:15.3
- **Kontext danach:** 264:16.6, 265:18.1, 266:17.3

### Frame 264

- **frame_ms:** 16.612
- **stream_ms / apply / unload:** 11.046 / 6.570 / 0.005
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 39.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 261:14.9, 262:15.3, 263:18.5
- **Kontext danach:** 265:18.1, 266:17.3, 267:17.1

### Frame 265

- **frame_ms:** 18.077
- **stream_ms / apply / unload:** 11.976 / 6.095 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 22 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 262:15.3, 263:18.5, 264:16.6
- **Kontext danach:** 266:17.3, 267:17.1, 268:11.0

### Frame 266

- **frame_ms:** 17.274
- **stream_ms / apply / unload:** 11.259 / 5.506 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 23 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 20 Hitches in einem 20-Frame-Fenster (Spanne 21).
- **Kontext davor:** 263:18.5, 264:16.6, 265:18.1
- **Kontext danach:** 267:17.1, 268:11.0, 269:11.1

### Frame 267

- **frame_ms:** 17.123
- **stream_ms / apply / unload:** 10.288 / 5.567 / 0.006
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 18).
- **Kontext davor:** 264:16.6, 265:18.1, 266:17.3
- **Kontext danach:** 268:11.0, 269:11.1, 270:10.9

### Frame 298

- **frame_ms:** 15.067
- **stream_ms / apply / unload:** 8.867 / 4.331 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 295:11.8, 296:10.9, 297:12.3
- **Kontext danach:** 299:11.0, 300:12.2, 301:11.2

### Frame 309

- **frame_ms:** 20.528
- **stream_ms / apply / unload:** 5.267 / 0.027 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 0.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 306:11.5, 307:12.9, 308:12.1
- **Kontext danach:** 310:11.0, 311:11.0, 312:11.9

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 10.368 | 9.448 | 15.348 | 45.842 |
| stream_ms | 5.527 | 4.839 | 9.850 | 39.488 |
| stream_apply_ms | 0.561 | 0.025 | 4.726 | 34.883 |
| stream_unload_ms | 0.004 | 0.004 | 0.005 | 0.006 |
| stream_loaded | 0.050 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 17.421 | 16.000 | 24.000 | 24.000 |
| zoom | 0.313 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 4.713 | 4.196 | 6.583 | 15.100 |
| tile_extract_ms | 0.110 | 0.099 | 0.149 | 0.581 |
| extract_ms | 4.823 | 4.299 | 6.720 | 15.243 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 30.283 | 23.523 | 54.223 | 81.310 |
| render_cpu_ms | 0.311 | 0.291 | 0.437 | 0.775 |
| present_wait_cpu_ms | 0.095 | 0.090 | 0.122 | 0.237 |
| cpu_unattributed_ms | 0.125 | 0.108 | 0.195 | 0.368 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.909, n=321): Hitch-Frames: stream_ms-Mittel 11.308 vs. übrige 4.931 (Faktor 2.29). Pearson r=0.909 (stark).
- **frame_ms ↔ stream_apply_ms** (r=0.873, n=321): Hitch-Frames: stream_apply_ms-Mittel 5.741 vs. übrige 0.027 (Faktor 215.66). Pearson r=0.873 (stark).
- **frame_ms ↔ stream_unload_ms** (r=0.283, n=321): Hitch-Frames: stream_unload_ms-Mittel 0.004 vs. übrige 0.004 (Faktor 1.03). Pearson r=0.283 (schwach).
- **frame_ms ↔ stream_loaded** (r=0.310, n=321): Hitch-Frames: stream_loaded-Mittel 0.533 vs. übrige 0.000 (Faktor inf). Pearson r=0.310 (schwach).
- **frame_ms ↔ stream_unloaded** (r=n/a, n=321): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.272, n=321): Hitch-Frames: chunk_count-Mittel 17.600 vs. übrige 17.402 (Faktor 1.01). Pearson r=0.272 (schwach).
- **frame_ms ↔ zoom** (r=-0.466, n=321): Hitch-Frames: zoom-Mittel 0.244 vs. übrige 0.320 (Faktor 0.76). Pearson r=-0.466 (moderat).
- **frame_ms ↔ pending_unload_count** (r=n/a, n=321): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.487, n=321): Hitch-Frames: deco_extract_ms-Mittel 5.334 vs. übrige 4.648 (Faktor 1.15). Pearson r=0.487 (moderat).
- **frame_ms ↔ tile_extract_ms** (r=0.727, n=321): Hitch-Frames: tile_extract_ms-Mittel 0.141 vs. übrige 0.107 (Faktor 1.32). Pearson r=0.727 (stark).
- **frame_ms ↔ extract_ms** (r=0.504, n=321): Hitch-Frames: extract_ms-Mittel 5.475 vs. übrige 4.756 (Faktor 1.15). Pearson r=0.504 (moderat).
- **cpu_full_frame_ms ↔ stream_ms** (r=0.468, n=321): Pearson r=0.468 (moderat) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.624, n=321): Pearson r=0.624 (moderat) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=0.179, n=321): Pearson r=0.179 (vernachlässigbar) zwischen cpu_full_frame_ms und render_cpu_ms.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=0.250, n=321): Pearson r=0.250 (schwach) zwischen cpu_full_frame_ms und present_wait_cpu_ms.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 1/321 Frames (0.3%).
- stream_unloaded am Unload-Cap (2): 0/321 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 1/30 (3.3%).
- Hitchs mit stream_unloaded am Cap: 0/30 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/321 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: unclear (Nicht eindeutig) in 24/30 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 53.3%, Apply 5.4%, Unload 0.0%, Extract 46.5%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 35.7%.
- Häufigstes Hitch-Muster: periodic_cluster (20×).

## Offene Fragen

- 24 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
