# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T073943Z_demo_31a8d2f` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `mixed`
- **reason:** kein eindeutiger Sieger: present_wait=0.2%, stream_pool=28.7%
- cpu_full_frame_ms_mean: 50.07
- present_wait_cpu_ms_mean: 0.09
- render_cpu_ms_mean: 0.34

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 49 | 65.25 | `unclear` | 19.2% |
| p99 | 54 | 78.49 | `unclear` | 16.2% |

## Hitch-Cluster (Top)

- **apply_dominant** (92 Hitches): `unclear` (16.1%) frame=52
- **unclear** (2 Hitches): `unclear` (16.2%) frame=54
