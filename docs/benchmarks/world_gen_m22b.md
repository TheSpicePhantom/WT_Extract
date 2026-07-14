# World-Gen Performance — M22b

| Metrik | Baseline | Parallel | Speedup |
|--------|----------|----------|---------|
| `noise_only_s` | 1.699s | 1.662s | 1.02× |
| `generate_chunk_s` | 6.074s | 5.928s | 1.02× |
| `decorations_s` | 11.843s | 11.829s | 1.00× |
| `solid_rebuild_s` | 5.893s | 5.822s | 1.01× |
| `apply_full_s` | 11.611s | 11.599s | 1.00× |
| `demo_world_16x16_s` | 27.738s | 3.415s | 8.12× |
| `streaming_first_load_s` | 33.268s | 33.584s | 0.99× |

Ausführung:

```bash
python tools/benchmark_world_gen.py --label baseline
python tools/benchmark_world_gen.py --label parallel
python tools/benchmark_world_gen.py --compare
```

**baseline** — 2026-07-05T19:35:14.318625+00:00 @ `unknown`

**parallel** — 2026-07-05T19:36:28.312678+00:00 @ `unknown`
