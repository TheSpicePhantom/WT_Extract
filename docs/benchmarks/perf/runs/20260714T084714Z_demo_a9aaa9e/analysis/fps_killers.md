# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T084714Z_demo_a9aaa9e` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `unclear`
- **reason:** keine Phase erreicht MIXED_MIN_SHARE
- cpu_full_frame_ms_mean: 46.01
- present_wait_cpu_ms_mean: 0.09
- render_cpu_ms_mean: 0.29

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 131 | 51.15 | `unclear` | 10.9% |
| p99 | 22 | 65.88 | `unclear` | 14.0% |

## Hitch-Cluster (Top)

- **unclear** (21 Hitches): `unclear` (8.4%) frame=28
- **stream_total_dominant** (9 Hitches): `unclear` (11.7%) frame=162
- **apply_dominant** (1 Hitches): `stream_pool` (44.7%) frame=20
