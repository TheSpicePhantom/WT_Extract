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
| `cpu_unattributed_ms` | float | optional | M25: Restbudget (Guardrail) |

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
