# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `steady` |
| run_id | `20260713T194934Z_steady_unknown` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.0% < 35%; stream_pool_mean=62.6%
- cpu_full_frame_ms_mean: 23.60
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 170 | 31.95 | `stream_pool` | 61.2% |
| p99 | 14 | 34.81 | `stream_pool` | 69.1% |

## Hitch-Cluster (Top)

- **apply_dominant** (299 Hitches): `stream_pool` (85.3%) frame=16
- **unclear** (1 Hitches): `stream_pool` (49.5%) frame=57
