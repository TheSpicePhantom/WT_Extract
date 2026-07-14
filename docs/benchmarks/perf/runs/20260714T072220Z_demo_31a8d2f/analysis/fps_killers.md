# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T072220Z_demo_31a8d2f` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.2% < 35%; stream_pool_mean=35.6%
- cpu_full_frame_ms_mean: 36.07
- present_wait_cpu_ms_mean: 0.09
- render_cpu_ms_mean: 0.29

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 1866 | 38.42 | `stream_pool` | 36.9% |
| p99 | 1234 | 41.97 | `stream_pool` | 37.8% |

## Hitch-Cluster (Top)

- **apply_dominant** (2457 Hitches): `stream_pool` (37.0%) frame=1232
- **unclear** (38 Hitches): `mixed` (30.4%) frame=1157
