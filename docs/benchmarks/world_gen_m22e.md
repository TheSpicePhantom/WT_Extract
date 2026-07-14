# World-Gen Benchmark M22e — Worker Apply

## Ziel

Messung des Main-Thread-Apply-Engpasses vor/nach M22e.

## Setup

- Seed: `world_gen.json` (Default 42)
- Test-Koordinaten: 8×8 Grid `(0..7, 0..7)`
- Config: `parallel.worker_apply=true`

## Erwartete Effekte

| Pfad | Vor M22e | Nach M22e |
|------|----------|-----------|
| Pool-Apply pro Chunk | `populate` + `rebuild_chunk_solid` auf Main | `apply_chunk_result` (Batch-Deko + Solid-Copy) |
| `profile_frame --mode pan` | streamer.update dominiert durch Deko | Apply ms/Chunk deutlich reduziert |

## Messbefehle

```bash
python tools/benchmark_world_gen.py
python tools/profile_frame.py --mode pan --frames 120
python -m pytest tests/test_worker_chunk_result.py tests/test_worker_apply.py -q
```

## Determinismus

Golden-Referenz: `tests/support/chunk_reference.py` — Worker-Output muss byte-identisch zum Sequential-Pfad sein.
