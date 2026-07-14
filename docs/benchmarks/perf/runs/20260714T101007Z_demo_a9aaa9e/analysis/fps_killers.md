# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `demo` |
| run_id | `20260714T101007Z_demo_a9aaa9e` |
| run_mode | `demo` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.0% < 35%; cpu_render_submit_mean=44.5%
- cpu_full_frame_ms_mean: 30.28
- present_wait_cpu_ms_mean: 0.10
- render_cpu_ms_mean: 0.31

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 307 | 54.22 | `cpu_render_submit` | 61.6% |
| p99 | 253 | 67.26 | `cpu_render_submit` | 58.1% |

## Hitch-Cluster (Top)

- **unclear** (24 Hitches): `cpu_render_submit` (51.8%) frame=252
- **stream_total_dominant** (5 Hitches): `cpu_render_submit` (64.9%) frame=258
- **apply_dominant** (1 Hitches): `canonical_tick` (64.7%) frame=249
