# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `steady` |
| run_id | `20260713T194433Z_steady_unknown` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.0% < 35%; stream_pool_mean=61.3%
- cpu_full_frame_ms_mean: 51.40
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 38 | 58.37 | `stream_pool` | 59.8% |
| p99 | 64 | 72.52 | `stream_pool` | 57.6% |

## Hitch-Cluster (Top)

- **apply_dominant** (300 Hitches): `stream_pool` (59.6%) frame=62
