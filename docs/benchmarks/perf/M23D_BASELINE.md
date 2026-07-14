# M23d Baseline-Contract

Verbindliche Referenz für Chunk-/Gruppen-Batching im sichtbarkeitsabhängigen Extract-Pfad.

## Milestone-Einordnung

| Milestone | Inhalt |
|-----------|--------|
| M23c | Extract-Hot-Path / Microprofile / Cache-Vertrag |
| **M23d** | Chunk-Layer-Batch-Registry + Cull-Cache (produktiver Pfad) |
| M24 | Ores (nicht vorweggenommen) |

**Kein LOD-Milestone** — Batching ist Repräsentations- und Kostenfrage, keine Mipmaps/Map-Mode.

## M23d-Vorher-Referenz (Post-M23c)

| Run | Rolle |
|-----|--------|
| `20260712T082720Z_demo_unknown` | **Primäre Demo-Baseline** |
| `m23c_candidate_zoom_out` | CLI Zoom-Out Referenz |

### Demo-KPIs (Post-M23c, bindend)

| KPI | Wert |
|-----|------|
| M23b DoD | **bestanden** |
| Anteil an `frame_ms` | Extract **~91.8 %** |
| `tile_extract_ms` mean / p95 / max | **2.95 / 4.89 / 6.41 ms** |
| `frame_ms` mean / p95 / max | 3.85 / **6.42 / 11.95 ms** |
| `chunk_count` mean / p95 | **176.8 / 189** |
| `frame_ms ↔ tile_extract_ms` | r ≈ 0.943 |

## Batch-Einheit (bindend)

| Ebene | Festlegung |
|-------|------------|
| Kleinste Einheit | `(chunk_coord, layer_id)` → `TileLayerBatch` |
| Cull-Cache | `(chunk_coord, layer_id, tile_range)` |
| Sammel-Einheit | `TileChunkRenderData` → `RenderFrame.tile_chunks` |
| Verboten | Globale Welt-Super-Batches |

## Dirty-/Invalidierungs-Vertrag

| Ereignis | Verhalten |
|----------|-----------|
| `set_tile` | `dirty_chunk_layers[coord]` → nur betroffene Layer rebuilden |
| `invalidate(coord)` | Registry + Cull-Cache + `_registry_empty` chunkweise leeren |
| Reine Pan/Zoom | Cull-Cache-Hits wenn `tile_range` unverändert |
| Range-Änderung | Cull-Miss, kein Full-Rebuild |

## Schwellenvertrag

| KPI | Baseline | M23d-Ziel |
|-----|----------|-----------|
| `tile_extract_ms` p95 (Demo, `chunk_count ≥ 150`) | ~4.9 ms | **≥ 1.5× Reduktion** |
| `frame_ms` p95 (Demo) | 6.42 ms | **messbar gesenkt** |
| `zoom_out` tile p95 | Post-M23c | **nicht regressiv** |
| M23b DoD / M23c Cache | grün | **grün bleiben** |

### Kostenverschiebungs-Guardrails

- `deco_extract_ms`, `stream_ms`, `stream_apply_ms`, `stream_unload_ms` **nicht regressiv**
- Keine Arbeit außerhalb `tile_extract_ms` im kanonischen Tick verschieben
- `RenderFrame`-Determinismus unverändert

## Batching-Submetriken (optional, M23d)

| Feld | Bedeutung |
|------|-----------|
| `tile_visible_batches` | Sichtbare Chunk-Layer-Gruppen |
| `tile_registry_hits` / `tile_registry_misses` | Batch-Registry |
| `tile_cull_cache_hits` / `tile_cull_cache_misses` | Cull-Cache |
| `tile_assemble_ms` | Gruppen-Sammlung innerhalb Tile-Extract |

M23c-Felder (`tile_cache_hits`, …) bleiben parallel exportiert.

## Auswertung

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

CLI-Baselines: `m23d_baseline_zoom_out`, `m23d_baseline_steady`  
Post-M23d: `m23d_candidate_*`

## Post-M23d Ergebnisse (Microbench + CLI)

| Szenario | Metrik | Post-M23c | Post-M23d |
|----------|--------|-----------|-----------|
| 24-Chunk-Synthese (zoom 0.05) | Extract mean / Frame | 0.537 ms legacy | **0.293 ms batch (1.83×)** |
| `pan` CLI | `frame_ms` p95 | 3.45 ms | **2.93 ms (−15 %)** |
| `zoom_out` CLI | `tile_extract_ms` max | 1.70 ms | **1.07 ms (−37 %)** |

Demo-Vollrun (`chunk_count ≥ 150`): Baseline `20260712T082720Z_demo_unknown` tile p95 **4.95 ms** — Post-M23d Demo via `chunk_world_demo --profile` (gleicher Config-Fingerprint).

M23b DoD auf `m23d_candidate_pan` / `m23d_baseline_zoom_out`: **grün**.
