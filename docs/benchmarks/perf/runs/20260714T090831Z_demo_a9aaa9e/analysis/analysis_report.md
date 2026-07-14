# Profiling-Run-Analyse

## Metadaten

- **run_id:** `20260714T090831Z_demo_a9aaa9e`
- **scenario_id:** `demo`
- **run_mode:** `demo`
- **recorded_frames:** 803
- **warmup_frames:** 60
- **extract_enabled:** True
- **recorded_at:** 2026-07-14T09:09:00.642890+00:00
- **git_commit:** a9aaa9e

### Config-Fingerprints

- `profiling`: `-1733439823750414964`
- `streaming`: `-239789045633498775`
- `visibility_lod`: `5571976836251803251`
- `world_gen`: `-4454078274797939716`

**Optionale Felder:** apply_collision_ms, apply_delta_ms, apply_override_ms, apply_pool_ms, apply_sync_generate_ms, apply_worker_ms, cpu_full_frame_ms, cpu_unattributed_ms, deco_extract_ms, pending_unload_count, present_wait_cpu_ms, render_cpu_ms, stream_unload_drained, stream_unload_marked, tile_extract_ms

## KPI-Check

| Feld | summary.json | rekonstruiert | Δ | Status |
| --- | ---: | ---: | ---: | --- |
| frame_ms_mean | 10.3817 | 10.3817 | +0.0000 | OK |
| frame_ms_p95 | 13.1718 | 13.1718 | +0.0000 | OK |
| frame_ms_max | 39.7939 | 39.7939 | +0.0000 | OK |
| stream_ms_mean | 4.9559 | 4.9559 | +0.0000 | OK |
| stream_ms_p95 | 8.5788 | 8.5788 | +0.0000 | OK |
| stream_ms_max | 34.4773 | 34.4773 | +0.0000 | OK |
| stream_unload_ms_p95 | 0.0048 | 0.0048 | +0.0000 | OK |
| stream_unload_ms_max | 0.0314 | 0.0314 | +0.0000 | OK |
| chunk_count_mean | 18.6476 | 18.6476 | +0.0000 | OK |
| recorded_frames | 803.0000 | 803.0000 | +0.0000 | OK |
| hitch_count | 43.0000 | 43.0000 | +0.0000 | OK |
| hitch_frame_count | 12.0000 | 12.0000 | +0.0000 | OK |
| hitch_stream_count | 43.0000 | 43.0000 | +0.0000 | OK |
| hitch_load_count | 1.0000 | 1.0000 | +0.0000 | OK |
| hitch_unload_count | 0.0000 | 0.0000 | +0.0000 | OK |
| max_loaded_per_frame | 4.0000 | 4.0000 | +0.0000 | OK |
| max_unloaded_per_frame | 0.0000 | 0.0000 | +0.0000 | OK |

## M23b DoD

- **Apply-Burst-Signatur:** BESTANDEN
- **Inakzeptable Hitchs:** 0

## Problem-Ranking

1. **Hitch-Ursache: Nicht eindeutig** (dominant_bottleneck, Konfidenz: hoch)
   - In 29/43 Hitch-Events als Hauptursache klassifiziert; regelbasiert aus Anteilen an frame_ms abgeleitet.

2. **Dauerlast durch extract_ms** (steady_load, Konfidenz: mittel)
   - Mittlerer Anteil 52.1% an frame_ms über den gesamten Run.

3. **Zweitrangiger Kostentreiber: stream_ms** (secondary_cost, Konfidenz: mittel)
   - Mittlerer Anteil 47.7% an frame_ms.

4. **Seltene Frame-Ausreißer** (rare_outlier, Konfidenz: hoch)
   - frame_ms_max (39.79) deutlich über P95 (13.17) — einzelne Spitzen, nicht Dauerlast.

5. **Unload derzeit unauffällig** (relieved, Konfidenz: hoch)
   - Niedrige stream_unload_ms-Mittel und Maxima; kein dominanter Unload-Engpass.

## Hitch-Analyse

### Tag-Häufigkeiten

- `stream_slow`: 43
- `frame_slow`: 12
- `load_burst`: 1

### Frame 25

- **frame_ms:** 14.029
- **stream_ms / apply / unload:** 9.260 / 4.347 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 22:8.8, 23:9.0, 24:10.0
- **Kontext danach:** 26:9.1, 27:10.4, 28:10.0

### Frame 56

- **frame_ms:** 14.442
- **stream_ms / apply / unload:** 9.327 / 4.257 / 0.005
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
- **Kontext davor:** 53:9.9, 54:9.0, 55:9.0
- **Kontext danach:** 57:9.5, 58:9.2, 59:10.2

### Frame 87

- **frame_ms:** 13.410
- **stream_ms / apply / unload:** 8.633 / 4.277 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 84:9.2, 85:9.1, 86:9.4
- **Kontext danach:** 88:9.6, 89:8.9, 90:9.0

### Frame 118

- **frame_ms:** 13.806
- **stream_ms / apply / unload:** 9.128 / 4.255 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 115:9.1, 116:9.7, 117:9.4
- **Kontext danach:** 119:9.5, 120:9.1, 121:9.2

### Frame 149

- **frame_ms:** 13.156
- **stream_ms / apply / unload:** 8.579 / 4.170 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 146:9.5, 147:9.0, 148:9.0
- **Kontext danach:** 150:9.0, 151:8.9, 152:9.3

### Frame 180

- **frame_ms:** 13.213
- **stream_ms / apply / unload:** 8.668 / 4.164 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 177:9.1, 178:9.0, 179:9.0
- **Kontext danach:** 181:8.9, 182:10.0, 183:9.0

### Frame 211

- **frame_ms:** 13.205
- **stream_ms / apply / unload:** 8.609 / 4.203 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 208:9.1, 209:8.9, 210:9.1
- **Kontext danach:** 212:9.2, 213:9.0, 214:9.2

### Frame 242

- **frame_ms:** 13.584
- **stream_ms / apply / unload:** 8.697 / 4.229 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 239:9.0, 240:9.9, 241:9.1
- **Kontext danach:** 243:9.1, 244:9.7, 245:9.1

### Frame 273

- **frame_ms:** 13.172
- **stream_ms / apply / unload:** 8.602 / 4.143 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 270:9.9, 271:8.9, 272:10.2
- **Kontext danach:** 274:9.1, 275:9.0, 276:9.0

### Frame 304

- **frame_ms:** 13.165
- **stream_ms / apply / unload:** 8.496 / 4.153 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 301:9.0, 302:9.3, 303:8.9
- **Kontext danach:** 305:9.0, 306:9.0, 307:8.9

### Frame 335

- **frame_ms:** 13.306
- **stream_ms / apply / unload:** 8.740 / 4.245 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 332:10.3, 333:8.9, 334:9.3
- **Kontext danach:** 336:9.4, 337:9.3, 338:9.8

### Frame 366

- **frame_ms:** 13.381
- **stream_ms / apply / unload:** 8.798 / 4.293 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 363:9.0, 364:9.0, 365:9.2
- **Kontext danach:** 367:9.3, 368:9.5, 369:8.9

### Frame 397

- **frame_ms:** 13.373
- **stream_ms / apply / unload:** 8.776 / 4.216 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 394:9.0, 395:9.6, 396:8.9
- **Kontext danach:** 398:9.8, 399:9.3, 400:9.2

### Frame 428

- **frame_ms:** 13.831
- **stream_ms / apply / unload:** 8.905 / 4.380 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 425:9.0, 426:9.1, 427:9.6
- **Kontext danach:** 429:9.1, 430:9.2, 431:9.0

### Frame 459

- **frame_ms:** 13.686
- **stream_ms / apply / unload:** 8.810 / 4.229 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 30.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 456:10.0, 457:9.8, 458:9.9
- **Kontext danach:** 460:9.3, 461:9.2, 462:9.5

### Frame 490

- **frame_ms:** 13.088
- **stream_ms / apply / unload:** 8.511 / 4.203 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 487:9.1, 488:9.5, 489:9.8
- **Kontext danach:** 491:9.1, 492:9.2, 493:9.0

### Frame 521

- **frame_ms:** 13.209
- **stream_ms / apply / unload:** 8.591 / 4.155 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3500
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 518:9.6, 519:9.0, 520:9.2
- **Kontext danach:** 522:9.1, 523:39.8, 524:17.7

### Frame 523

- **frame_ms:** 39.794
- **stream_ms / apply / unload:** 34.477 / 29.257 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Load-/Apply-dominant
  - Load-/Apply-dominant: 73.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Burst mit Nachlauf
  - Hitch frame_ms (39.79) deutlich über Nachbar-Mittel (13.36).
  - Weitere Hitches in ±3 Frames: [521, 524, 525, 526].
- **Kontext davor:** 520:9.2, 521:13.2, 522:9.1
- **Kontext danach:** 524:17.7, 525:16.2, 526:14.8

### Frame 524

- **frame_ms:** 17.723
- **stream_ms / apply / unload:** 9.409 / 4.564 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.3022
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 25.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 521:13.2, 522:9.1, 523:39.8
- **Kontext danach:** 525:16.2, 526:14.8, 527:24.1

### Frame 525

- **frame_ms:** 16.244
- **stream_ms / apply / unload:** 11.156 / 4.561 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.2252
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 522:9.1, 523:39.8, 524:17.7
- **Kontext danach:** 526:14.8, 527:24.1, 528:15.9

### Frame 526

- **frame_ms:** 14.769
- **stream_ms / apply / unload:** 9.430 / 4.590 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1944
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 523:39.8, 524:17.7, 525:16.2
- **Kontext danach:** 527:24.1, 528:15.9, 529:15.0

### Frame 527

- **frame_ms:** 24.114
- **stream_ms / apply / unload:** 15.570 / 7.681 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 524:17.7, 525:16.2, 526:14.8
- **Kontext danach:** 528:15.9, 529:15.0, 530:14.3

### Frame 528

- **frame_ms:** 15.902
- **stream_ms / apply / unload:** 10.516 / 5.029 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 525:16.2, 526:14.8, 527:24.1
- **Kontext danach:** 529:15.0, 530:14.3, 531:14.2

### Frame 529

- **frame_ms:** 14.966
- **stream_ms / apply / unload:** 10.153 / 4.656 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 526:14.8, 527:24.1, 528:15.9
- **Kontext danach:** 530:14.3, 531:14.2, 532:17.6

### Frame 530

- **frame_ms:** 14.254
- **stream_ms / apply / unload:** 9.150 / 4.558 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 527:24.1, 528:15.9, 529:15.0
- **Kontext danach:** 531:14.2, 532:17.6, 533:14.0

### Frame 531

- **frame_ms:** 14.236
- **stream_ms / apply / unload:** 9.322 / 4.650 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 528:15.9, 529:15.0, 530:14.3
- **Kontext danach:** 532:17.6, 533:14.0, 534:14.9

### Frame 532

- **frame_ms:** 17.626
- **stream_ms / apply / unload:** 12.768 / 4.548 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 25.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 529:15.0, 530:14.3, 531:14.2
- **Kontext danach:** 533:14.0, 534:14.9, 535:20.8

### Frame 533

- **frame_ms:** 14.028
- **stream_ms / apply / unload:** 9.201 / 4.619 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 16 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 32.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 530:14.3, 531:14.2, 532:17.6
- **Kontext danach:** 534:14.9, 535:20.8, 536:25.8

### Frame 534

- **frame_ms:** 14.857
- **stream_ms / apply / unload:** 9.834 / 5.124 / 0.004
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 531:14.2, 532:17.6, 533:14.0
- **Kontext danach:** 535:20.8, 536:25.8, 537:15.4

### Frame 535

- **frame_ms:** 20.795
- **stream_ms / apply / unload:** 15.659 / 6.950 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 17 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 33.4% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 532:17.6, 533:14.0, 534:14.9
- **Kontext danach:** 536:25.8, 537:15.4, 538:14.6

### Frame 536

- **frame_ms:** 25.844
- **stream_ms / apply / unload:** 19.853 / 12.795 / 0.004
- **stream_loaded / unloaded:** 3 / 0
- **chunk_count / zoom:** 19 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 49.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 533:14.0, 534:14.9, 535:20.8
- **Kontext danach:** 537:15.4, 538:14.6, 539:20.3

### Frame 537

- **frame_ms:** 15.359
- **stream_ms / apply / unload:** 9.946 / 5.358 / 0.004
- **stream_loaded / unloaded:** 4 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** stream_slow, load_burst
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 34.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag load_burst unterstützt Apply-Dominanz.
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 534:14.9, 535:20.8, 536:25.8
- **Kontext danach:** 538:14.6, 539:20.3, 540:15.7

### Frame 538

- **frame_ms:** 14.630
- **stream_ms / apply / unload:** 9.069 / 4.323 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 21 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 29.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 535:20.8, 536:25.8, 537:15.4
- **Kontext danach:** 539:20.3, 540:15.7, 541:11.3

### Frame 539

- **frame_ms:** 20.341
- **stream_ms / apply / unload:** 14.424 / 9.917 / 0.004
- **stream_loaded / unloaded:** 3 / 0
- **chunk_count / zoom:** 23 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 48.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 536:25.8, 537:15.4, 538:14.6
- **Kontext danach:** 540:15.7, 541:11.3, 542:12.2

### Frame 540

- **frame_ms:** 15.742
- **stream_ms / apply / unload:** 9.228 / 4.885 / 0.005
- **stream_loaded / unloaded:** 2 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Nicht eindeutig
  - Load-/Apply-dominant: 31.0% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Wiederkehrendes Cluster
  - 19 Hitches in einem 20-Frame-Fenster (Spanne 19).
- **Kontext davor:** 537:15.4, 538:14.6, 539:20.3
- **Kontext danach:** 541:11.3, 542:12.2, 543:12.3

### Frame 571

- **frame_ms:** 15.483
- **stream_ms / apply / unload:** 8.873 / 4.323 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.9% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 568:11.4, 569:12.5, 570:11.2
- **Kontext danach:** 572:11.5, 573:11.4, 574:11.9

### Frame 602

- **frame_ms:** 16.120
- **stream_ms / apply / unload:** 8.836 / 4.326 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 26.8% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 599:11.3, 600:11.1, 601:12.2
- **Kontext danach:** 603:11.4, 604:11.2, 605:12.5

### Frame 633

- **frame_ms:** 15.773
- **stream_ms / apply / unload:** 8.930 / 4.369 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.7% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 630:11.5, 631:11.8, 632:11.7
- **Kontext danach:** 634:11.0, 635:11.1, 636:11.9

### Frame 664

- **frame_ms:** 17.035
- **stream_ms / apply / unload:** 9.751 / 4.540 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 26.6% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 661:12.0, 662:11.6, 663:11.6
- **Kontext danach:** 665:12.4, 666:11.1, 667:11.3

### Frame 695

- **frame_ms:** 15.634
- **stream_ms / apply / unload:** 8.960 / 4.538 / 0.005
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
- **Kontext davor:** 692:11.7, 693:12.6, 694:12.0
- **Kontext danach:** 696:11.5, 697:12.6, 698:11.6

### Frame 726

- **frame_ms:** 15.542
- **stream_ms / apply / unload:** 8.863 / 4.279 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.5% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 723:11.3, 724:11.5, 725:12.4
- **Kontext danach:** 727:11.6, 728:12.2, 729:12.4

### Frame 757

- **frame_ms:** 16.303
- **stream_ms / apply / unload:** 9.716 / 4.576 / 0.004
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 28.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 754:11.5, 755:12.0, 756:11.5
- **Kontext danach:** 758:11.9, 759:11.2, 760:11.4

### Frame 788

- **frame_ms:** 16.156
- **stream_ms / apply / unload:** 9.028 / 4.376 / 0.005
- **stream_loaded / unloaded:** 0 / 0
- **chunk_count / zoom:** 24 / 0.1800
- **Tags:** frame_slow, stream_slow
- **Vermutete Ursache:** Stream gesamt dominant
  - Load-/Apply-dominant: 27.1% von frame_ms
  - Unload-dominant: 0.0% von frame_ms
  - Extract-dominant: 0.0% von frame_ms
  - Tag stream_slow — Stream-Anteil erhöht.
- **Kontextmuster:** Unklares Muster
  - Kein eindeutiges Burst-, Backlog- oder Spike-Muster erkennbar.
- **Kontext davor:** 785:12.0, 786:11.5, 787:11.1
- **Kontext danach:** 789:12.5, 790:13.2, 791:12.3

## Verteilungen

| Metrik | mean | p50 | p95 | max |
| --- | ---: | ---: | ---: | ---: |
| frame_ms | 10.382 | 9.463 | 13.172 | 39.794 |
| stream_ms | 4.956 | 4.547 | 8.579 | 34.477 |
| stream_apply_ms | 0.317 | 0.024 | 4.155 | 29.257 |
| stream_unload_ms | 0.004 | 0.004 | 0.005 | 0.031 |
| stream_loaded | 0.017 | 0.000 | 0.000 | 4.000 |
| stream_unloaded | 0.000 | 0.000 | 0.000 | 0.000 |
| chunk_count | 18.648 | 16.000 | 24.000 | 24.000 |
| zoom | 0.291 | 0.350 | 0.350 | 0.350 |
| deco_extract_ms | 5.301 | 4.689 | 7.054 | 8.415 |
| tile_extract_ms | 0.109 | 0.094 | 0.142 | 0.584 |
| extract_ms | 5.410 | 4.780 | 7.196 | 8.526 |
| pending_unload_count | 0.000 | 0.000 | 0.000 | 0.000 |
| cpu_full_frame_ms | 32.977 | 23.519 | 52.030 | 72.381 |
| render_cpu_ms | 0.288 | 0.280 | 0.341 | 0.722 |
| present_wait_cpu_ms | 0.088 | 0.085 | 0.104 | 0.265 |
| cpu_unattributed_ms | 16.670 | 8.882 | 32.140 | 42.081 |

## Korrelationen / Zusammenhänge

- **frame_ms ↔ stream_ms** (r=0.857, n=803): Hitch-Frames: stream_ms-Mittel 10.494 vs. übrige 4.643 (Faktor 2.26). Pearson r=0.857 (stark).
- **frame_ms ↔ stream_apply_ms** (r=0.804, n=803): Hitch-Frames: stream_apply_ms-Mittel 5.472 vs. übrige 0.026 (Faktor 214.44). Pearson r=0.804 (stark).
- **frame_ms ↔ stream_unload_ms** (r=0.049, n=803): Hitch-Frames: stream_unload_ms-Mittel 0.004 vs. übrige 0.004 (Faktor 1.00). Pearson r=0.049 (vernachlässigbar).
- **frame_ms ↔ stream_loaded** (r=0.305, n=803): Hitch-Frames: stream_loaded-Mittel 0.326 vs. übrige 0.000 (Faktor inf). Pearson r=0.305 (schwach).
- **frame_ms ↔ stream_unloaded** (r=n/a, n=803): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ chunk_count** (r=0.515, n=803): Hitch-Frames: chunk_count-Mittel 18.186 vs. übrige 18.674 (Faktor 0.97). Pearson r=0.515 (moderat).
- **frame_ms ↔ zoom** (r=-0.620, n=803): Hitch-Frames: zoom-Mittel 0.254 vs. übrige 0.293 (Faktor 0.87). Pearson r=-0.620 (moderat).
- **frame_ms ↔ pending_unload_count** (r=n/a, n=803): Zu wenige Datenpunkte für eine belastbare Korrelation.
- **frame_ms ↔ deco_extract_ms** (r=0.587, n=803): Hitch-Frames: deco_extract_ms-Mittel 5.372 vs. übrige 5.297 (Faktor 1.01). Pearson r=0.587 (moderat).
- **frame_ms ↔ tile_extract_ms** (r=0.576, n=803): Hitch-Frames: tile_extract_ms-Mittel 0.124 vs. übrige 0.108 (Faktor 1.15). Pearson r=0.576 (moderat).
- **frame_ms ↔ extract_ms** (r=0.591, n=803): Hitch-Frames: extract_ms-Mittel 5.497 vs. übrige 5.405 (Faktor 1.02). Pearson r=0.591 (moderat).
- **cpu_full_frame_ms ↔ stream_ms** (r=0.285, n=803): Pearson r=0.285 (schwach) zwischen cpu_full_frame_ms und stream_ms.
- **cpu_full_frame_ms ↔ extract_ms** (r=0.949, n=803): Pearson r=0.949 (stark) zwischen cpu_full_frame_ms und extract_ms.
- **cpu_full_frame_ms ↔ render_cpu_ms** (r=0.237, n=803): Pearson r=0.237 (schwach) zwischen cpu_full_frame_ms und render_cpu_ms.
- **cpu_full_frame_ms ↔ present_wait_cpu_ms** (r=0.224, n=803): Pearson r=0.224 (schwach) zwischen cpu_full_frame_ms und present_wait_cpu_ms.

## Budget- und Cap-Verhalten

Referenz-Caps: max_applies=4, max_unloads=2 (aus Projekt-config, Fingerprint-Abweichung beachten).
- stream_loaded am Apply-Cap (4): 1/803 Frames (0.1%).
- stream_unloaded am Unload-Cap (2): 0/803 Frames (0.0%).
- Hitchs mit stream_loaded am Cap: 1/43 (2.3%).
- Hitchs mit stream_unloaded am Cap: 0/43 (0.0%).
- pending_unload_count max=0, >= Schwellwert 32: 0/803 Frames.
- P95+-Frames: pending_unload_count-Mittel 0.0 vs. Run-Mittel 0.0.

## Run-weite Diagnose

- Hitch-Hauptursachen: unclear (Nicht eindeutig) in 29/43 Fällen.
- Durchschnittlicher Anteil an frame_ms: Stream 47.7%, Apply 3.1%, Unload 0.0%, Extract 52.1%.
- Unload ist im Run durchgehend unauffällig (niedrige Mittel- und Max-Werte).
- Extract-Anteil in langsamen Frames (P95+/Hitch): 35.9%.
- Häufigstes Hitch-Muster: unknown (24×).

## Offene Fragen

- 29 Hitch(s) mit unklarer Ursache — manuelle Frame-Inspektion empfohlen.
