# FPS Killer Report (M25a)

## Szenario

| Feld | Wert |
| --- | --- |
| scenario_id | `render_only` |
| run_id | `20260713T194702Z_render_only_unknown` |
| run_mode | `cli` |

## Entscheidung (CPU vs Present)

- **decision:** `mixed`
- **reason:** kein eindeutiger Sieger: present_wait=0.0%, extract_tiles=34.4%
- cpu_full_frame_ms_mean: 0.02
- present_wait_cpu_ms_mean: 0.00
- render_cpu_ms_mean: 0.00

## Dominanz (P95 / P99)

| Quantil | frame | cpu_full_frame_ms | dominant_phase | share |
| --- | ---: | ---: | --- | ---: |
| p95 | 166 | 0.03 | `extract_tiles` | 35.9% |
| p99 | 251 | 0.04 | `extract_tiles` | 23.4% |
