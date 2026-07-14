# M23e Baseline-Contract

Verbindliche Referenz für Visibility LOD / Map-Mode im sichtbarkeitsabhängigen Extract-Pfad.

## Milestone-Einordnung

| Milestone | Inhalt |
|-----------|--------|
| M23d | Chunk-Layer-Batch-Registry + Cull-Cache (produktiver Pfad) |
| **M23e** | Visibility LOD / Map-Mode / Mipmap-Settings auf Extract-Pfad |
| M24 | Ores (nicht vorweggenommen) |

## M23e-Vorher-Referenz (Post-M23d)

| Run | Rolle |
|-----|--------|
| Post-M23d Demo (`chunk_count ≥ 150`) | **Primäre Demo-Baseline** — tile p95 **~4.95 ms** |
| `20260712T082720Z_demo_unknown` | Historische Post-M23c Demo — `frame_ms` p95 **6.42 ms** |
| `m23d_baseline_zoom_out` / Post-M23d `zoom_out` CLI | **Primär-LOD-Reproduktionsszenario** |

### Demo-KPIs (Post-M23d, bindend als Vorher)

| KPI | Wert |
|-----|------|
| M23b DoD | **bestanden** |
| `tile_extract_ms` p95 (Demo, `chunk_count ≥ 150`) | **~4.95 ms** |
| `frame_ms` p95 (Demo) | **~6.42 ms** |
| `chunk_count` mean / p95 (Post-M23c Referenz) | **176.8 / 189** |
| Extract-Anteil an `frame_ms` | **~91–92 %** |
| `frame_ms ↔ tile_extract_ms` | r ≈ 0.943 (stark) |
| `frame_ms ↔ zoom` (Post-M23b) | r ≈ **−0.824** (Zoom-Out verschlechtert Performance) |

## Szenario-Set M23e

| Szenario | Rolle |
|----------|--------|
| `demo` | Integrations-Referenz |
| `zoom_out` | **Primär-LOD-Reproduktion** (Zoom 0.05) |
| `steady` | LOD-Stabilität / Cache-Reuse |
| `catchup` | Regression (Streaming + Extract) |

CLI-Baselines: `m23e_baseline_zoom_out`, `m23e_baseline_steady`  
Post-M23e-Kandidaten: `m23e_candidate_*`

## LOD-Stufenmodell (bindend)

| Stufe | Repräsentation |
|-------|----------------|
| **LOD0** | Voll-Detail-Chunk-Layer-Batches (M23d) |
| **LOD1** | Chunkgebundene 2×2-Aggregation (Schritt 2 Subsample) |
| **LOD2** | Chunk-Dominant-Tile / Map-Mode Overview |
| **Bindung** | `(chunk_coord, layer_id, lod_level)` — keine globale Welt-Primärrepräsentation |
| **Umschaltung** | Deterministisch aus `zoom` + [`visibility_lod.json`](../../../assets/content/visibility_lod.json); `map_mode=true` erzwingt LOD2 |

## Schwellenvertrag (Phase 0, verbindlich)

M23e-Ziel gegen Post-M23d-Baseline:

| KPI | Baseline (Post-M23d) | M23e-Ziel |
|-----|----------------------|-----------|
| `tile_extract_ms` p95 (Demo, `chunk_count ≥ 150`) | ~4.95 ms | **≥ 1.5× Reduktion** |
| `frame_ms` p95 (Demo) | ~6.42 ms | **messbar gesenkt** (extract-getrieben) |
| `tile_extract_ms` p95/max (`zoom_out` CLI) | Post-M23d Referenz | **signifikant gesenkt** |
| `deco_extract_ms` | Post-M23d | **nicht regressiv** |
| M23b DoD / M23c Cache / M23d Batching | grün | **grün bleiben** |

### Kostenverschiebungs-Guardrails

Verbesserungen zählen nur bei erfüllten Guardrails:

| Guardrail | Regel |
|-----------|-------|
| `deco_extract_ms` | **nicht regressiv** |
| `stream_ms` / `stream_apply_ms` / `stream_unload_ms` | **nicht regressiv** |
| Kanonischer Tick | Keine LOD-Arbeit außerhalb `tile_extract_ms` verschieben |
| Determinismus | `RenderFrame`-Semantik reproduzierbar bei gleichem Welt+Kamera+Zoom+LOD-Stufe |
| Kurzform | LOD-Erfolg ungültig bei reiner Kostenumbuchung |

## LOD-Submetriken (optional, M23e)

| Feld | Bedeutung |
|------|-----------|
| `tile_lod0_groups` / `tile_lod1_groups` / `tile_lod2_groups` | Sichtbare Gruppen pro LOD-Stufe |
| `tile_lod0_ms` / `tile_lod1_ms` / `tile_lod2_ms` | Zeitanteil pro Stufe innerhalb `tile_extract_ms` |
| `tile_lod_switches` | Umschalt-Ereignisse zwischen LOD-Stufen |
| `tile_map_mode_active` | Map-Mode explizit aktiv (0/1) |

M23c/M23d-Felder bleiben parallel exportiert.

## Auswertung

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

## Post-M23e Ergebnisse (Microbench + CLI)

| Szenario | Metrik | Post-M23d / Vorher | Post-M23e |
|----------|--------|-------------------|-----------|
| Synthese ~221 sichtbare Chunks, zoom 0.05, **Cold-Extract** | Extract | ~7.89 ms (LOD0/detail) | **~4.07 ms (LOD2/auto) — ~1.94×** |
| Synthese, zoom 0.05 | Sichtbare Tiles | 14 144 | **221** |
| `zoom_out` CLI (`m23e_candidate_zoom_out`) | `tile_extract_ms` p95 | Post-M23c ~0.35 ms | **~0.36 ms** (nicht regressiv) |
| `zoom_out` CLI | M23b DoD | grün | **grün** |

Hinweis: CLI-`zoom_out` lädt im aktuellen Szenario-Runtime oft `chunk_count=0`; synthetische Microbench mit geladenen Chunks ist die verbindliche LOD-Skalierungsreferenz. Demo-Vollrun mit `chunk_count ≥ 150` via `chunk_world_demo --profile` für Integrations-KPIs.

### CLI-Vergleich Post-M23d → Post-M23e

| Szenario | KPI | Baseline (M23d) | Kandidat (M23e) | Δ |
|----------|-----|-----------------|-----------------|---|
| `zoom_out` | `tile_extract_ms` p95 | 0.430 ms | **0.364 ms** | **−15.5 %** |
| `zoom_out` | `frame_ms` p95 | 2.142 ms | **1.946 ms** | **−9.1 %** |
| `zoom_out` | M23b DoD | grün | **grün** | — |
| `steady` | `tile_extract_ms` p95 | 0.031 ms | **0.025 ms** | **−19.2 %** (nicht regressiv) |
| `steady` | `extract_ms` max | 0.264 ms | **0.166 ms** | **−37.0 %** |

Runs: `m23d_baseline_*` vs `m23e_candidate_*` unter `docs/benchmarks/perf/runs/`.
