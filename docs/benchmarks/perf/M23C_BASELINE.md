# M23c Baseline-Contract

Verbindliche Referenz für Extract-Optimierung (Tile/Deko) im kanonischen Profiling-Tick.

## Milestone-Einordnung

| Milestone | Inhalt |
|-----------|--------|
| M23 | Profiling / Metriken / Export |
| M23a | Deferred Unload |
| M23b | Apply-/Load-Burst-Entschärfung |
| **M23c** | Extract-Optimierung (Tile/Deko) |
| M24 | Ores (nicht vorweggenommen) |

## M23c-Vorher-Referenz (Post-M23b)

| Run | Rolle |
|-----|--------|
| `20260712T074209Z_demo_unknown` | **Primäre Demo-Baseline** (Extract-dominant) |
| `20260710T204430Z_demo_unknown` | Historisch (Apply-dominiert, pre-M23b) — nicht M23c-Vergleichsziel |

### Demo-KPIs (Post-M23b, bindend)

| KPI | Wert |
|-----|------|
| `frame_ms` mean / p95 / max | 2.97 / 5.71 / **15.61 ms** |
| M23b DoD | **bestanden** |
| Anteil an `frame_ms` | Stream 6.6 %, Apply 3.1 %, Unload 0.3 %, **Extract 92.8 %** |
| `tile_extract_ms` mean / p95 / max | **2.378 / 4.529 / 9.184 ms** |
| `deco_extract_ms` mean / p95 / max | 0.381 / 0.883 / 1.853 ms |
| `extract_ms` mean / p95 / max | 2.759 / 5.367 / 10.929 ms |
| `frame_ms ↔ tile_extract_ms` | r ≈ 0.974 |
| `frame_ms ↔ extract_ms` | r ≈ 0.987 |

## Szenario-Set M23c

| Szenario | Rolle |
|----------|--------|
| `demo` | Integrations-Referenz |
| `steady` | Cache-Hit-Referenz (keine Tile-Änderung) |
| `pan` | Kamera + Streaming, Cache-Verhalten |
| `catchup` | Hohe Extract-Last (CLI) |

CLI-Baselines: `docs/benchmarks/perf/runs/m23c_baseline_*`

Post-M23c-Kandidaten: `m23c_candidate_pan`, `m23c_candidate_zoom_out`, `m23c_baseline_catchup`

## Schwellenvertrag (Phase 0)

M23c-Ziel gegen Demo-Baseline `20260712T074209Z_demo_unknown`:

| KPI | Baseline | M23c-Ziel | Post-M23c (zoom_out + catchup) |
|-----|----------|-----------|--------------------------------|
| `tile_extract_ms` p95 / max | 4.53 / 9.18 ms | **≥ 2× Reduktion** | **0.35 / 1.70 ms** (zoom_out) — erfüllt |
| `extract_ms` p95 / max | 5.37 / 10.93 ms | proportional | **0.76 / 12.28 ms** (zoom_out max durch Deko-Spike) |
| `deco_extract_ms` max | 1.85 ms | nicht regressiv | 0.09 ms (catchup), 11.9 ms (zoom_out Deko-Ausreißer) |

**Catchup CLI** (`m23b_candidate_catchup` → `m23c_baseline_catchup`): `tile_extract_ms` p95 **1.88 → 0.026 ms** (>70×).

**Demo** (Frames mit `chunk_count ≥ 50`): Baseline p95 **4.54 ms**; Post-M23c zoom_out p95 **0.35 ms** (>12×).

Gleiches Muster auf mindestens **steady** oder **catchup** (CLI) — **catchup erfüllt**.

## Cache-/Dirty-Vertrag (Tile-Extract)

| Ereignis | Extract-Verhalten |
|----------|-------------------|
| Cache-Hit | `coord in _tile_cache` und `coord not in dirty_chunks` → nur `_cull_chunk_to_camera` |
| Cache-Miss | Neuer/geladener Chunk ohne Cache-Eintrag → `_extract_full_chunk` |
| Tile geändert | `set_tile` → `mark_dirty` → Full-Rebuild beim nächsten sichtbaren Extract |
| Streaming Unload | `invalidate(coord)` → Cache-Eintrag weg, **kein** `dirty_chunks`-Set |
| Reine Pan/Zoom | Kein `mark_dirty` → erwartet Cache-Hits nach Warmup |

## DoD-Auswertung

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

Compare enthält Extract-KPIs aus `frames.jsonl` (ab M23c).
