# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T090831Z_demo_a9aaa9e` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.3% < 35%; cpu_residual_mean=46.1%
- cpu_full_frame_ms_mean: 32.98
- present_wait_cpu_ms_mean: 0.09
- render_cpu_ms_mean: 0.29

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 565 | 52.03 | `canonical_tick` | 23.7% |
| p99 | 764 | 57.52 | `canonical_tick` | 20.1% |

## Hitch-Cluster (Top)

- **unclear** (29 Hitches): `canonical_tick` (33.3%) frame=527
- **stream_total_dominant** (13 Hitches): `canonical_tick` (25.5%) frame=524
- **apply_dominant** (1 Hitches): `canonical_tick` (68.2%) frame=523
