# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `steady` |
| run_id | `20260714T080831Z_steady_b0f57bb` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `mixed`
- **reason:** kein eindeutiger Sieger: present_wait=0.0%, extract_deco=31.3%
- cpu_full_frame_ms_mean: 9.56
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 32 | 18.23 | `stream_pool` | 44.9% |
| p99 | 0 | 29.71 | `stream_pool` | 65.1% |

## Hitch-Cluster (Top)

- **unclear** (73 Hitches): `stream_pool` (49.3%) frame=33
- **apply_dominant** (17 Hitches): `stream_pool` (69.9%) frame=20
