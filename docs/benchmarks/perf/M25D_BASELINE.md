# M25d — CPU Full-Frame Bilanz (attribution_version 4)

Referenz-Run (vor M25d): `20260714T090831Z_demo_a9aaa9e` — `cpu_residual_p95_share` 61,7 %.

## Zeitbasis

Einheitlich `time.perf_counter()` (Wall-Clock, Main-Thread) für alle `cpu_*`-Phasen und `cpu_full_frame_ms`.

## Exklusive Top-Level-Phasen (v4)

```text
cpu_attributed_ms =
  cpu_input_ms
+ cpu_framework_pre_tick_ms
+ frame_ms                    # canonical_tick_ms
+ cpu_framework_post_tick_ms
+ cpu_render_submit_ms
+ cpu_present_cpu_ms
+ cpu_framework_post_present_ms

cpu_balance_delta_ms = cpu_full_frame_ms - cpu_attributed_ms   # signiert
cpu_measurement_residual_ms = cpu_balance_delta_ms
cpu_residual_ms = max(0, cpu_balance_delta_ms)                 # Anteil-Gates
```

Kein `cpu_other_named_ms` in v4.0 — Rest nur über `cpu_measurement_residual_ms`.

## Demo-Loop (chunk_world_demo.py)

| Phase | Bereich |
| --- | --- |
| `cpu_input_ms` | `input_state.poll()` |
| `cpu_framework_pre_tick_ms` | dt, UI, Regen — bis `run_canonical_tick` |
| `canonical_tick_ms` | `run_canonical_tick()` → `frame_ms` |
| `cpu_framework_post_tick_ms` | Sim, Camera, Extract-Dup, Render-Prep, Visible-Count |
| `cpu_render_submit_ms` | `render_pack_ms` + `render_prepare_ms` + `render_sync_pipeline_ms` + pre_render/record/submit |
| `cpu_present_cpu_ms` | wait_fence + acquire + present |
| Titel-Update | **außerhalb** Full-Frame (nach `finalize_pending_frame`) |

## Child-Diagnose (nicht in Bilanz-Summe)

`cpu_sim_ms`, `cpu_camera_ms`, `cpu_extract_render_ms`, `cpu_tile_render_ms`, `cpu_render_prep_ms`, `cpu_app_ui_ms`

## Pflicht-Gates (DoD)

```bash
python tools/gate_perf_run.py <run> --attribution-version-min 4 \
  --cpu-residual-p95-share-max 0.10 --cpu-residual-p95-max-ms 5 \
  --cpu-balance-delta-p95-max-ms 0.05 \
  --negative-cpu-balance-delta-max 0 \
  --missing-cpu-attribution-fields-max 0 \
  --apply-pool-idle-skip-min-rate 0.80 --apply-pool-p95-max-ms 5 \
  --skip-warmup 60
```

## Gate E — Instrumentierungs-Overhead A/B

```bash
python tools/gate_perf_run.py --compare-runs <control> <candidate> \
  --cpu-full-frame-p50-delta-max-ms 0.5 \
  --cpu-full-frame-p95-delta-max-ms 1.5 \
  --cpu-full-frame-p95-delta-max-pct 0.03 \
  --cpu-full-frame-mean-delta-max-ms 0.3 \
  --skip-warmup 60
```

Kontroll: `detailed_cpu_attribution: false` — Kandidat: `true`.
