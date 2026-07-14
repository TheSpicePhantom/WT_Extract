# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `steady` |
| run_id | `20260714T073857Z_steady_31a8d2f` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.0% < 35%; stream_pool_mean=74.9%
- cpu_full_frame_ms_mean: 18.10
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 27 | 19.94 | `stream_pool` | 76.0% |
| p99 | 19 | 26.06 | `stream_pool` | 72.5% |

## Hitch-Cluster (Top)

- **apply_dominant** (300 Hitches): `stream_pool` (74.8%) frame=16
