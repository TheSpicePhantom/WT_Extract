# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T083849Z_demo_b0f57bb` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `unclear`
- **reason:** keine Phase erreicht MIXED_MIN_SHARE
- cpu_full_frame_ms_mean: 40.82
- present_wait_cpu_ms_mean: 0.09
- render_cpu_ms_mean: 0.30

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 283 | 56.97 | `unclear` | 14.0% |
| p99 | 175 | 63.64 | `unclear` | 9.2% |

## Hitch-Cluster (Top)

- **stream_total_dominant** (15 Hitches): `unclear` (9.2%) frame=177
- **unclear** (14 Hitches): `unclear` (16.4%) frame=183
- **apply_dominant** (2 Hitches): `stream_pool` (42.4%) frame=173
