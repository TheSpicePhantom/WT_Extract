# M24c.1 — Streaming-E2E & Terrain-Hebel

## Problem

M24c beschleunigte den Mikro-Benchmark (`worker_build_terrain_stage` ~22 s → ~1,1 s), aber `chunk_world_demo` zeigte weiterhin `stream hitch: loaded=2 stream=~4000 ms`.

**Ursachen (behoben):**
- `is_terrain_in_flight` ignorierte `READY` → Sync-Fallback während Worker-Result wartete
- `sync_fallback_in_flight_ms: 500` < Worker-Zeit ~1100 ms → doppelte Generierung auf Main
- Deco-Worker baute bei LRU-Hit `generate_terrain_layers` erneut (~1 s)

## Änderungen

| Phase | Inhalt |
|-------|--------|
| 0 | `sync_fallback_triggered`, `WT_STREAM_DIAG=1`, `tools/benchmark_stream_step.py` |
| 1 | `is_in_flight` inkl. READY, `has_pending_result`, Warmup Terrain+Deco, `sync_fallback_in_flight_ms: 2500` |
| 2 | H3: Warp-Reuse + Seed-Klima-Cache; H5: Coast aus Height-Grid |
| 3 | `TerrainStageLRU` — Deco ohne Terrain-Rebuild bei Cache-Hit |
| 4 | `tests/test_m24c1_streaming.py`, diese Doku |

## Streaming-Config

[`assets/content/streaming.json`](../../assets/content/streaming.json):

- `sync_fallback_in_flight_ms: 2500` — unter typischer Worker-Wallclock (~1100 ms Terrain + ~500 ms Deco), verhindert vorzeitigen Sync-Fallback

## Reproduktion

```bash
# E2E-Streaming (10 Steps, Fokus-Bewegung)
python tools/benchmark_stream_step.py --steps 10

# Demo-Diagnose (stderr)
set WT_STREAM_DIAG=1
python apps/chunk_world_demo.py

# Mikro + Cost Breakdown
python tools/benchmark_single_chunk.py --cost-breakdown --coord 1 1
```

## Zielmetriken (Gate S4)

| Metrik | Vorher (Demo) | Nach M24c.1 (Benchmark) | Ziel |
|--------|---------------|------------------------|------|
| `stream_ms` P95 | ~4000 ms | ~2133 ms (10 Steps, Cold) | ≤ 800 ms |
| `apply_sync_generate_ms` | hoch | Cold-Start noch > 0 | ≈ 0 (Warm) |
| `sync_fallback_triggered` | > 0 | Cold-Start noch > 0 | 0 (Worker-Pfad) |
| `worker_build_terrain_stage` | ~1100 ms | **~464–538 ms** (H3/H5) | ≤ 800 ms |

Artefakt: [`stream_step_baseline.json`](stream_step_baseline.json).

**Hinweis:** Integrationsfixes (READY-aware `is_in_flight`, `has_pending_result`, `sync_fallback_in_flight_ms: 2500`) eliminieren den ~4-Sekunden-Hitch pro Coord bei laufendem Worker. Cold-Start mit vollem Radius-Load kann weiterhin Sync-Fallback für noch nicht eingereichte Coords zeigen.

## Tests

```bash
pytest tests/test_m24c1_streaming.py tests/test_m24c_terrain_perf.py -q
```
