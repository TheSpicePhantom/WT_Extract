# M24c — Terrain-Performance (Phase 0 + 1)

## Vorher / Nachher (coord=(1,1), 64×64)

| Metrik | M24b | M24c | Speedup |
|--------|------|------|---------|
| `build_terrain_stage` sync | ~25.6 s | ~1.0 s | ~25× |
| `worker_build_terrain_stage` | ~22.4 s | ~1.1 s | ~20× |
| `apply_terrain_stage` | ~0.8 ms | ~0.4 ms | — |
| `field_cache` Builds pro Chunk | 2 | **1** | H1 behoben |

## Cost Breakdown (nach M24c Phase 1)

Quelle: [`terrain_cost_breakdown_baseline.json`](terrain_cost_breakdown_baseline.json)

| Sektion | Anteil |
|---------|--------|
| `noise_fbm` + `noise_simplex` | ~46 % |
| `field_cache_region` | ~24 % |
| `field_cache_climate` | ~9 % |
| `resolve_tiles` | ~11 % |
| `coast_overlay` | ~10 % |

**H1 (Doppel-Cache):** falsifiziert als aktives Problem — `field_cache_builds: 1`.

**Nächste Hebel (Phase 2, optional):** H3 Noise-Redundanz in `sample_biome_region`, H5 Coast aus Height-Grid.

## Reproduktion

```bash
python tools/benchmark_single_chunk.py --cost-breakdown --coord 1 1
```

Artefakte: `nodeco_single_chunk_64.json`, `deco_single_chunk_64.json`, `terrain_cost_breakdown_baseline.json`.

## Tests

```bash
pytest tests/test_m24c_terrain_perf.py tests/test_chunk_reference.py -q
```
