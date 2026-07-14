# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `render_only` |
| run_id | `20260713T195254Z_render_only_unknown` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `cpu_dominant`
- **reason:** present_wait_mean_share=0.0% < 35%; extract_tiles_mean=35.1%
- cpu_full_frame_ms_mean: 0.02
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 165 | 0.03 | `mixed` | 34.7% |
| p99 | 3 | 0.04 | `extract_tiles` | 26.1% |
