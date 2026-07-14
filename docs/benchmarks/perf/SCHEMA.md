# Profiling-Export-Schema (M23)

`schema_version` ist Pflicht. M23 startet mit **Version 1**. Breaking Changes erhöhen die Version; additive optionale Felder erhöhen sie nicht.

Unbekannte Versionen müssen in Compare-Tools zu einem harten Fehler führen.

## manifest.json

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|--------------|
| `schema_version` | int | ja | Aktuell `1` |
| `run_id` | string | ja | Eindeutige Run-ID |
| `recorded_at` | string (ISO 8601) | ja | UTC-Zeitstempel |
| `scenario_id` | string | ja | z. B. `steady`, `pan`, `demo` |
| `run_mode` | string | ja | `cli` oder `demo` |
| `extract_enabled` | bool | ja | Extract im kanonischen Tick |
| `stream_enabled` | bool | optional (M25a) | Streaming im Szenario (Default: true) |
| `deco_extract_enabled` | bool | optional (M25a) | Deko-Extract aktiv |
| `tile_extract_enabled` | bool | optional (M25a) | Tile-Extract aktiv |
| `warmup_frames` | int | ja | Ausgeschlossene Warmup-Ticks |
| `recorded_frames` | int | ja | Anzahl exportierter Frames |
| `git_commit` | string | ja | Kurzer Git-Hash |
| `config_fingerprint` | object | ja | Hashes relevanter Config-Dateien |

## frames.jsonl (eine JSON-Zeile pro Frame)

| Feld | Typ | Pflicht |
|------|-----|---------|
| `schema_version` | int | ja |
| `frame_index` | int | ja | Beginnt bei 0 nach Warmup |
| `scenario_id` | string | ja |
| `frame_ms` | float | ja | Kanonischer Tick (siehe README) |
| `stream_ms` | float | ja | Gesamt-Streaming-Zeit |
| `stream_apply_ms` | float | ja | Apply-/Load-Zeit |
| `stream_unload_ms` | float | ja | Unload-Zeit |
| `stream_loaded` | int | ja |
| `stream_unloaded` | int | ja |
| `chunk_count` | int | ja |
| `focus_x` | float | ja |
| `focus_y` | float | ja |
| `zoom` | float | ja |
| `deco_extract_ms` | float | optional |
| `tile_extract_ms` | float | optional |
| `deco_sprite_count` | int | optional |
| `cpu_full_frame_ms` | float | optional | M25: vollständiger App-Frame (CPU) |
| `render_cpu_ms` | float | optional | M25: Renderer-CPU (Record/Submit) |
| `present_wait_cpu_ms` | float | optional | M25: CPU-Waits (Fence/Acquire/Present) |
| `cpu_unattributed_ms` | float | optional | M25: Restbudget (deprecated alias von `cpu_residual_ms`) |
| `cpu_balance_delta_ms` | float | optional | M25c: signiertes Bilanz-Delta (`cpu_full_frame_ms − attributed`) |
| `cpu_residual_ms` | float | optional | M25c: `max(0, cpu_balance_delta_ms)` für Rest-Gates |
| `cpu_input_ms` | float | optional | M25c: Input-Pump |
| `cpu_app_ui_ms` | float | optional | M25c: UI/Tooling vor Tick |
| `cpu_scenario_ms` | float | optional | M25c: Tick-Breakdown (Teil von `frame_ms`, nicht zur Bilanz addieren) |
| `cpu_sim_ms` | float | optional | M25c: Simulation |
| `cpu_camera_ms` | float | optional | M25c: Camera/Viewport |
| `cpu_extract_render_ms` | float | optional | M25c: Deko-Extract außerhalb Tick (Demo-Duplikat) |
| `cpu_tile_render_ms` | float | optional | M25c: Tile-Extract außerhalb Tick |
| `cpu_render_prep_ms` | float | optional | M25c: Draw-Vorbereitung |
| `cpu_framework_ms` | float | optional | M25c: Framework/dt/Titel |
| `apply_sets_ms` | float | optional | M25c: Stream-Set-Auflösung |
| `apply_revive_ms` | float | optional | M25c: Pending-Unload-Revive |
| `apply_non_pool_ms` | float | optional | M25c: Apply außerhalb Pool-Block |
| `apply_pool_other_ms` | float | optional | M25c: Pool-Block-Rest |
| `apply_pool_idle_refresh` | int | optional | M25c: Voller Pool-Tick wegen Refresh |

## hitches.jsonl

Gleiche Pflichtfelder wie Frame plus:

| Feld | Typ | Pflicht |
|------|-----|---------|
| `tags` | array[string] | ja | Sortiert: `frame_slow`, `stream_slow`, `load_burst`, `unload_burst` |

## summary.json

| Feld | Typ | Pflicht |
|------|-----|---------|
| `schema_version` | int | ja |
| `run_id` | string | ja |
| `scenario_id` | string | ja |
| `run_mode` | string | ja |
| `recorded_frames` | int | ja |
| `frame_ms_mean` | float | ja |
| `frame_ms_p95` | float | ja |
| `frame_ms_max` | float | ja |
| `stream_ms_mean` | float | ja |
| `stream_ms_p95` | float | ja |
| `stream_ms_max` | float | ja |
| `stream_unload_ms_p95` | float | ja |
| `stream_unload_ms_max` | float | ja |
| `hitch_count` | int | ja |
| `hitch_frame_count` | int | ja |
| `hitch_stream_count` | int | ja |
| `hitch_load_count` | int | ja |
| `hitch_unload_count` | int | ja |
| `max_loaded_per_frame` | int | ja |
| `max_unloaded_per_frame` | int | ja |
| `chunk_count_mean` | float | ja |

## Hitch-Schwellen (profiling.json)

```json
"hitch": {
  "stream_ms": 8.0,
  "frame_ms": 16.0,
  "loaded_count": 4,
  "unloaded_count": 4
}
```

Keine hard-coded Schwellen im Code.

## fps_killers.json (M25/M25a)

Erzeugt von `tools/analyze_perf_run.py` → `analysis/fps_killers.json` (nur wenn `cpu_full_frame_ms` in Frames vorhanden).

| Feld | Typ | Pflicht | Beschreibung |
| --- | --- | --- | --- |
| `schema_version` | int | ja | Immer `1` (Run-Schema) |
| `attribution_version` | int | ja (M25a) | `2` für Plan-Enum |
| `scenario_id` | string | ja (M25a) | Aus manifest |
| `run_id` | string | ja (M25a) | Aus manifest |
| `scenario_label` | string | optional | Anzeigename (= scenario_id) |
| `run_mode` | string | optional | `cli` / `demo` |
| `toggles` | object | optional | Snapshot der Feature-Toggles |
| `has_full_frame` | bool | ja | Full-Frame-Daten vorhanden |
| `decision` | object | ja | CPU-vs-Present Entscheidung |
| `quantiles` | object | ja | `p95` / `p99` Dominanz |
| `dominance` | array | ja | Legacy-Alias von quantiles (Liste) |
| `same_frame_for_both_quantiles` | bool | optional | p95/p99 gleicher Frame |
| `hitch_clusters` | array | optional | Dominanz pro Hitch-Ursache |
| `ab_comparisons` | array | optional | A/B-Vergleiche (via compare_fps_killers) |

### dominant_phase (Enum)

`stream_apply`, `stream_pool`, `extract_tiles`, `extract_deco`, `render_cpu`, `present_wait`, `gpu`, `mixed`, `unclear`

### decision (M25a)

| Feld | Typ |
| --- | --- |
| `decision` | `cpu_dominant` \| `present_wait_dominant` \| `mixed` \| `unclear` |
| `reason_cpu_vs_present` | string |
| `cpu_full_frame_ms_mean` | float |
| `present_wait_cpu_ms_mean` | float |
| `render_cpu_ms_mean` | float |
| `present_wait_share_mean` | float |
| `gpu_dominant` | bool (M25a: immer false) |

### ab_comparisons[] (M25a)

| Feld | Typ |
| --- | --- |
| `scenario_id` | string |
| `causal_feature` | string |
| `baseline` | object (run_id, decision, dominant_phase, p95, p99, toggles) |
| `variant` | object |
| `delta` | object (cpu_full_frame_ms_p95, dominant_share_p95, decision_changed) |
