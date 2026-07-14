# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T083849Z_demo_b0f57bb`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 372
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T08:39:06.895753+00:00
- **git_commit:** b0f57bb

### Config-Fingerprints

- `profiling`: `-7494786195201596469`
- `streaming`: `3787745938312145605`
- `visibility_lod`: `-7108537665825236421`
- `world_gen`: `3537343272440355840`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, present_wait_cpu_ms, render_cpu_ms, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 12.0271 | 12.0271 | +0.0000 | OK |
| frame_ms_p95 | 15.2085 | 15.2085 | +0.0000 | OK |
| frame_ms_max | 43.3470 | 43.3470 | +0.0000 | OK |
| stream_ms_mean | 5.1935 | 5.1935 | +0.0000 | OK |
| stream_ms_p95 | 9.1994 | 9.1994 | +0.0000 | OK |
| stream_ms_max | 37.1405 | 37.1405 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0048 | 0.0048 | +0.0000 | OK |
| stream_unload_ms_max | 0.0359 | 0.0359 | +0.0000 | OK |
| chunk_count_mean | 19.9731 | 19.9731 | +0.0000 | OK |
| recorded_frames | 372.0000 | 372.0000 | +0.0000 | OK |
| hitch_count | 31.0000 | 31.0000 | +0.0000 | OK |
| hitch_frame_count | 15.0000 | 15.0000 | +0.0000 | OK |
| hitch_stream_count | 29.0000 | 29.0000 | +0.0000 | OK |
| hitch_load_count | 4.0000 | 4.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Stream gesamt dominant** (dominant_bottleneck, Konfidenz: mittel)
   - In 15/31 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch extract_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 56.7% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 43.2% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (43.35) deutlich über P95 (15.21) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `stream_slow`: 29
- `frame_slow`: 15
- `load_burst`: 4

### Frame 0

- **frame_ms:** 15.271
- **stream_ms / apply / unload:** 9.865 / 4.987 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext danach:** 1:10.1, 2:10.0, 3:11.0

### Frame 31

- **frame_ms:** 15.339
- **stream_ms / apply / unload:** 9.725 / 4.522 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 28:10.6, 29:10.2, 30:10.0
- **Kontext danach:** 32:10.4, 33:11.2, 34:11.0

### Frame 62

- **frame_ms:** 15.652
- **stream_ms / apply / unload:** 9.639 / 4.562 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 59:9.9, 60:10.0, 61:9.9
- **Kontext danach:** 63:11.3, 64:10.1, 65:10.2

### Frame 93

- **frame_ms:** 14.511
- **stream_ms / apply / unload:** 8.677 / 4.170 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 90:11.3, 91:10.3, 92:9.9
- **Kontext danach:** 94:10.1, 95:10.1, 96:10.0

### Frame 124

- **frame_ms:** 14.440
- **stream_ms / apply / unload:** 8.916 / 4.381 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 121:10.3, 122:9.9, 123:10.3
- **Kontext danach:** 125:10.4, 126:10.6, 127:11.0

### Frame 155

- **frame_ms:** 14.254
- **stream_ms / apply / unload:** 8.715 / 4.103 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 4 Hitches in einem 20-Frame-Fenster (Spanne 20).
- **Kontext davor:** 152:10.9, 153:10.7, 154:10.4
- **Kontext danach:** 156:11.1, 157:10.9, 158:10.9

### Frame 173

- **frame_ms:** 43.347
- **stream_ms / apply / unload:** 37.140 / 31.924 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Burst mit Nachlauf
  - Hitch frame_ms (43.35) deutlich über Nachbar-Mittel (12.83).
  - Weitere Hitches in ±3 Frames: [174, 175, 176].
- **Kontext davor:** 170:10.1, 171:10.6, 172:10.1
- **Kontext danach:** 174:15.2, 175:15.2, 176:15.8

### Frame 174

- **frame_ms:** 15.208
- **stream_ms / apply / unload:** 9.224 / 4.567 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2609
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 171:10.6, 172:10.1, 173:43.3
- **Kontext danach:** 175:15.2, 176:15.8, 177:16.4

### Frame 175

- **frame_ms:** 15.202
- **stream_ms / apply / unload:** 9.199 / 4.593 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2252
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.2% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 35).
- **Kontext davor:** 172:10.1, 173:43.3, 174:15.2
- **Kontext danach:** 176:15.8, 177:16.4, 178:14.7

### Frame 176

- **frame_ms:** 15.767
- **stream_ms / apply / unload:** 9.628 / 4.505 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 173:43.3, 174:15.2, 175:15.2
- **Kontext danach:** 177:16.4, 178:14.7, 179:15.1

### Frame 177

- **frame_ms:** 16.372
- **stream_ms / apply / unload:** 10.279 / 4.606 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 174:15.2, 175:15.2, 176:15.8
- **Kontext danach:** 178:14.7, 179:15.1, 180:14.8

### Frame 178

- **frame_ms:** 14.741
- **stream_ms / apply / unload:** 9.143 / 4.525 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 175:15.2, 176:15.8, 177:16.4
- **Kontext danach:** 179:15.1, 180:14.8, 181:15.1

### Frame 179

- **frame_ms:** 15.051
- **stream_ms / apply / unload:** 9.238 / 4.577 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 176:15.8, 177:16.4, 178:14.7
- **Kontext danach:** 180:14.8, 181:15.1, 182:15.0

### Frame 180

- **frame_ms:** 14.794
- **stream_ms / apply / unload:** 9.118 / 4.536 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 177:16.4, 178:14.7, 179:15.1
- **Kontext danach:** 181:15.1, 182:15.0, 183:25.8

### Frame 181

- **frame_ms:** 15.050
- **stream_ms / apply / unload:** 9.274 / 4.612 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 178:14.7, 179:15.1, 180:14.8
- **Kontext danach:** 182:15.0, 183:25.8, 184:15.0

### Frame 182

- **frame_ms:** 14.993
- **stream_ms / apply / unload:** 9.248 / 4.587 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 179:15.1, 180:14.8, 181:15.1
- **Kontext danach:** 183:25.8, 184:15.0, 185:19.5

### Frame 183

- **frame_ms:** 25.762
- **stream_ms / apply / unload:** 13.685 / 8.178 / 0.006
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 180:14.8, 181:15.1, 182:15.0
- **Kontext danach:** 184:15.0, 185:19.5, 186:23.1

### Frame 184

- **frame_ms:** 14.965
- **stream_ms / apply / unload:** 9.203 / 4.487 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 30.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 181:15.1, 182:15.0, 183:25.8
- **Kontext danach:** 185:19.5, 186:23.1, 187:17.4

### Frame 185

- **frame_ms:** 19.531
- **stream_ms / apply / unload:** 12.830 / 5.030 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 25.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 182:15.0, 183:25.8, 184:15.0
- **Kontext danach:** 186:23.1, 187:17.4, 188:15.0

### Frame 186

- **frame_ms:** 23.081
- **stream_ms / apply / unload:** 16.782 / 11.545 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 20 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 50.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 183:25.8, 184:15.0, 185:19.5
- **Kontext danach:** 187:17.4, 188:15.0, 189:19.5

### Frame 187

- **frame_ms:** 17.445
- **stream_ms / apply / unload:** 10.736 / 5.457 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 184:15.0, 185:19.5, 186:23.1
- **Kontext danach:** 188:15.0, 189:19.5, 190:18.7

### Frame 188

- **frame_ms:** 15.045
- **stream_ms / apply / unload:** 8.648 / 4.217 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 185:19.5, 186:23.1, 187:17.4
- **Kontext danach:** 189:19.5, 190:18.7, 191:12.5

### Frame 189

- **frame_ms:** 19.508
- **stream_ms / apply / unload:** 11.575 / 5.852 / 0.005
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 23 / 0.1800
- **Tags:** frame_slow, stream_slow, load_burst
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 30.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 186:23.1, 187:17.4, 188:15.0
- **Kontext danach:** 190:18.7, 191:12.5, 192:11.8

### Frame 190

- **frame_ms:** 18.697
- **stream_ms / apply / unload:** 10.445 / 5.203 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 18 Hitches in einem 20-Frame-Fenster (Spanne 17).
- **Kontext davor:** 187:17.4, 188:15.0, 189:19.5
- **Kontext danach:** 191:12.5, 192:11.8, 193:11.9

### Frame 211

- **frame_ms:** 20.250
- **stream_ms / apply / unload:** 4.444 / 0.024 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 0.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 208:11.9, 209:12.3, 210:12.7
- **Kontext danach:** 212:12.2, 213:12.2, 214:12.4

### Frame 221

- **frame_ms:** 17.708
- **stream_ms / apply / unload:** 9.799 / 4.520 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 25.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 218:13.2, 219:12.0, 220:12.3
- **Kontext danach:** 222:13.0, 223:13.0, 224:12.3

### Frame 252

- **frame_ms:** 16.357
- **stream_ms / apply / unload:** 8.903 / 4.424 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 249:12.8, 250:12.4, 251:12.2
- **Kontext danach:** 253:12.3, 254:14.1, 255:12.0

### Frame 264

- **frame_ms:** 18.918
- **stream_ms / apply / unload:** 4.537 / 0.024 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 0.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
- **Kontextmuster:** Wiederkehrendes Cluster
  - 3 Hitches in einem 20-Frame-Fenster (Spanne 31).
- **Kontext davor:** 261:12.3, 262:12.9, 263:12.1
- **Kontext danach:** 265:12.9, 266:12.8, 267:13.3

### Frame 283

- **frame_ms:** 17.439
- **stream_ms / apply / unload:** 9.314 / 4.240 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 24.3% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 280:12.6, 281:12.1, 282:12.1
- **Kontext danach:** 284:11.9, 285:12.4, 286:12.0

### Frame 314

- **frame_ms:** 17.367
- **stream_ms / apply / unload:** 8.680 / 4.259 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 24.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 311:12.4, 312:12.0, 313:12.1
- **Kontext danach:** 315:12.2, 316:13.1, 317:12.1

### Frame 345

- **frame_ms:** 16.325
- **stream_ms / apply / unload:** 8.684 / 4.062 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 24.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 342:12.4, 343:13.2, 344:12.2
- **Kontext danach:** 346:12.3, 347:12.0, 348:12.5

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 12.027 | 12.058 | 15.208 | 43.347 |
| stream_ms | 5.193 | 4.623 | 9.199 | 37.140 |
| stream_apply_ms | 0.483 | 0.024 | 4.505 | 31.924 |
| stream_unload_ms | 0.004 | 0.004 | 0.005 | 0.036 |
| stream_loaded | 0.054 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 19.973 | 20.000 | 24.000 | 24.000 |
| zoom | 0.260 | 0.180 | 0.350 | 0.350 |
| deco_extract_ms | 6.698 | 6.488 | 8.387 | 15.661 |
| tile_extract_ms | 0.118 | 0.128 | 0.148 | 0.294 |
| extract_ms | 6.816 | 6.680 | 8.525 | 15.790 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 40.822 | 51.437 | 56.975 | 75.192 |
| render_cpu_ms | 0.301 | 0.284 | 0.372 | 1.162 |
| present_wait_cpu_ms | 0.091 | 0.086 | 0.106 | 0.585 |
| cpu_unattributed_ms | 28.403 | 38.583 | 41.503 | 53.581 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.863, n=372): Hitch-Frames: stream_ms-Mittel 10.493 vs. übrige 4.712 (Faktor 2.23). Pearson r=0.863 (stark).
- **frame_ms ↔ stream_apply_ms** (r=0.839, n=372): Hitch-Frames: stream_apply_ms-Mittel 5.525 vs. übrige 0.024 (Faktor 228.44). Pearson r=0.839 (stark).
- **frame_ms ↔ stream_unload_ms** (r=0.055, n=372): Hitch-Frames: stream_unload_ms-Mittel 0.004 vs. übrige 0.004 (Faktor 1.00). Pearson r=0.055 (vernachlässigbar).
- **frame_ms ↔ stream_loaded** (r=0.325, n=372): Hitch-Frames: stream_loaded-Mittel 0.645 vs. übrige 0.000 (Faktor inf). Pearson r=0.325 (schwach).
- **frame_ms ↔ stream_unloaded** (r=n/a, n=372): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.355, n=372): Hitch-Frames: chunk_count-Mittel 18.774 vs. übrige 20.082 (Faktor 0.93). Pearson r=0.355 (schwach).
- **frame_ms ↔ zoom** (r=-0.497, n=372): Hitch-Frames: zoom-Mittel 0.221 vs. übrige 0.263 (Faktor 0.84). Pearson r=-0.497 (moderat).
- **frame_ms ↔ pending_unload_count** (r=n/a, n=372): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.503, n=372): Hitch-Frames: deco_extract_ms-Mittel 7.053 vs. übrige 6.665 (Faktor 1.06). Pearson r=0.503 (moderat).
- **frame_ms ↔ tile_extract_ms** (r=0.657, n=372): Hitch-Frames: tile_extract_ms-Mittel 0.126 vs. übrige 0.117 (Faktor 1.08). Pearson r=0.657 (moderat).
- **frame_ms ↔ extract_ms** (r=0.509, n=372): Hitch-Frames: extract_ms-Mittel 7.179 vs. übrige 6.783 (Faktor 1.06). Pearson r=0.509 (moderat).
- **cpu_full_frame_ms ↔ stream_ms** (r=0.279, n=372): Pearson r=0.279 (schwach) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.822, n=372): Pearson r=0.822 (stark) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=0.269, n=372): Pearson r=0.269 (schwach) zwischen cpu_full_frame_ms und render_cpu_ms.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=0.139, n=372): Pearson r=0.139 (vernachlässigbar) zwischen cpu_full_frame_ms und present_wait_cpu_ms.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 4/372 Frames (1.1%).
- stream_unloaded am Unload-Cap (2): 0/372 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 4/31 (12.9%).
- Hitchs mit stream_unloaded am Cap: 0/31 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/372 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: stream_total_dominant (Stream gesamt dominant) in 15/31 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 43.2%, Apply 4.0%, Unload 0.0%, Extract 56.7%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 41.5%.
- Häufigstes Hitch-Muster: periodic_cluster (19×).

## Offene Fragen

- 14 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
