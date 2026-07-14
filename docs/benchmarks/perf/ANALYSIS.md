# Run-Analyse — Diagnosewerkzeug

Das Tool `tools/analyze_perf_run.py` wertet exportierte Profiling-Runs (M23/M23a) diagnostisch aus. Es rekonstruiert KPIs aus `frames.jsonl`, klassifiziert Hitches regelbasiert und leitet Run-weite Muster ab.

## Aufruf

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
python tools/analyze_perf_run.py
```

Ohne Argument werden **alle** Run-Ordner unter `docs/benchmarks/perf/runs/` mit `manifest.json` analysiert.

Optional:

```bash
python tools/analyze_perf_run.py <run_dir> --output-dir ./out --context-radius 5
python tools/analyze_perf_run.py --manifest m.json --summary s.json --frames f.jsonl --hitches h.jsonl
python tools/analyze_perf_run.py <run_dir> --no-files
python tools/analyze_perf_run.py <run_dir> --max-applies 4 --max-unloads 2
```

## Erwartete Dateien

| Datei | Pflicht |
| --- | --- |
| `manifest.json` | ja |
| `summary.json` | ja |
| `frames.jsonl` | ja |
| `hitches.jsonl` | ja |

Alle Dateien müssen `schema_version: 1` tragen. Inkompatible Versionen werden abgelehnt.

## Ausgaben

**Terminal:** Kurzdiagnose, Problem-Ranking, Hitch-Übersicht, KPI-Check.

**Standard (<run_dir>/analysis/):**

- `analysis_report.md` — vollständiger Report
- `analysis_diagnosis.json` — maschinenlesbare Diagnose
- `hitches.csv` — Hitch-Tabelle mit Ursache und Muster
- `notable_frames.csv` — P95+- und Hitch-Frames
- `fps_killers.md` — M25a: FPS-Killer/Attribution (nur wenn Full-Frame-Felder vorhanden)
- `fps_killers.json` — M25a: maschinenlesbare Attribution (`attribution_version: 2`)
- `fps_killers_ab.json` — optional via `tools/compare_fps_killers.py`

## M25c — CPU-Bilanz & Burst-Attribution

- Analyse-Name **`canonical_tick_ms`** = JSONL-Feld **`frame_ms`**.
- **`cpu_full_frame_ms`** = gesamter App-Frame (`begin_full_frame` … `end_full_frame`).
- Burst-Tabellen führen **beide** Zeitdomänen nebeneinander.
- `cpu_balance_delta_ms` ist **signiert**; Gates nutzen `abs(delta)` P95 ≤ 0.05 ms.
- `cpu_scenario_ms` ist nur Tick-Breakdown, **nicht** zur Bilanz-Summe addieren.

## M25a — dominant_phase & Quantile

### Share-Buckets (Basis: `cpu_full_frame_ms`)

| Phase | ms-Quelle |
| --- | --- |
| `stream_pool` | `apply_pool_ms` |
| `stream_apply` | `max(0, stream_apply_ms - apply_pool_ms)` |
| `extract_tiles` | `tile_extract_ms` |
| `extract_deco` | `deco_extract_ms` |
| `render_cpu` | `render_cpu_ms` |
| `present_wait` | `present_wait_cpu_ms` |
| `gpu` | `gpu_frame_ms` (optional, M25a nicht für Decision) |

### Klassifikationsregeln

- **Dominant:** höchster Share ≥ **35 %**
- **mixed:** Top-2 ≥ **25 %**, Differenz ≤ **10 pp**
- **unclear:** kein Bucket ≥ **20 %** oder fehlendes `cpu_full_frame_ms`

### CPU-vs-Present (Run-Level)

- `present_wait_dominant`: `present_wait_share_mean ≥ 35 %` und ≥ max CPU-Phase
- `cpu_dominant`: max CPU-Phase ≥ **35 %** und present < **35 %**
- sonst `mixed` / `unclear`

Schwellen in `game_core/perf/run_analysis/phase_enum.py`.

### Quantil-Frame-Auswahl

1. Schwellwert: `percentile(cpu_full_frame_ms[], p)` mit Index `round((n-1)*p)` ([`stats.py`](../../game_core/perf/run_analysis/stats.py))
2. Frame: minimaler Abstand `|cpu_full_frame_ms - threshold|`, Tie-Breaker: kleinerer `frame_index`
3. p99: p95-`frame_index` ausgeschlossen, falls Alternative existiert
4. Flag `same_frame_for_both_quantiles` wenn p95 == p99

### A/B-Vergleich

```bash
python tools/compare_fps_killers.py <baseline_run> <variant_run>
```

Baseline-Vertrag: [`M25A_BASELINE.md`](M25A_BASELINE.md)

## Diagnosebegriffe

### Hitch-Ursachen (regelbasiert)

| ID | Bedeutung |
| --- | --- |
| `apply_dominant` | `stream_apply_ms` ≥ 50 % von `frame_ms` |
| `unload_dominant` | `stream_unload_ms` ≥ 50 % von `frame_ms` |
| `extract_dominant` | `deco_extract_ms + tile_extract_ms` ≥ 50 % von `frame_ms` |
| `stream_total_dominant` | `stream_ms` dominiert, Apply/Unload nicht klar trennbar |
| `mixed` | Mindestens zwei Subsysteme ≥ 30 % Anteil |
| `unclear` | Keine klare Dominanz |

Jede Klassifikation enthält eine Begründungsliste (Anteile, Tags). **Das ist eine Heuristik, keine Kausalitätsaussage.**

### Kontextmuster

| ID | Bedeutung |
| --- | --- |
| `isolated_spike` | Einzelner Frame deutlich über Nachbarn |
| `burst_with_tail` | Spike plus Hitches in ±3 Frames |
| `backlog_buildup` | `pending_unload_count` steigt vor dem Hitch |
| `periodic_cluster` | Mehrere Hitches in engem Fenster |
| `steady_cost` | Hoher Stream-Anteil ohne klaren Spike |
| `unknown` | Kein eindeutiges Muster |

### Problem-Ranking-Kategorien

- **dominant_bottleneck** — häufigste Hitch-Ursache
- **steady_load** — Dauerlast über den Run
- **secondary_cost** — zweitrangiger Mittel-Anteil
- **rare_outlier** — Max >> P95
- **relieved** — Subsystem aktuell unauffällig (z. B. Unload)

### M23b DoD (Apply-Burst-Signatur)

Der Report enthält **M23b DoD** (bestanden/nicht bestanden). Inakzeptable Hitchs erfüllen gleichzeitig:

- Tags `frame_slow` + `stream_slow` + `load_burst`
- Ursache `apply_dominant`, `stream_loaded` am Cap, `stream_apply_ms/frame_ms ≥ 0.9`

Schwellenvertrag: [`M23B_BASELINE.md`](M23B_BASELINE.md)

### Optionale Apply-Submetriken (M23b)

| Feld | Bedeutung |
| --- | --- |
| `apply_worker_ms` | Worker-Apply-Pfad |
| `apply_sync_generate_ms` | Sync `generate_chunk` |
| `apply_delta_ms` | Delta-Apply |
| `apply_override_ms` | Override-Copy |
| `apply_pool_ms` | Pool submit/poll |
| `apply_collision_ms` | Collision-Rebuild im Apply-Block |

### Optionale Pool-Submetriken (M25b)

| Feld | Bedeutung |
| --- | --- |
| `apply_pool_poll_ms` | Collect + `poll_*_ready` im Pool-Block |
| `apply_pool_submit_ms` | Submit-Scan + `submit_chunk_pipeline` |
| `apply_pool_apply_ms` | `apply_terrain_stage` + `apply_deco_stage` |
| `apply_pool_suppress_ms` | `_update_deco_suppression` |
| `apply_pool_discard_ms` | `discard_outside` |
| `apply_pool_route_passes` | Route-Durchläufe pro Frame (1–2) |
| `apply_pool_in_flight_peak` | Max in-flight während Frame |
| `apply_pool_idle_skip` | 1 wenn Idle-Fast-Path genutzt |

Analyse: `stream_pool_breakdown` in `analysis_diagnosis.json` (mean/p95).

Summe ≈ `stream_apply_ms` (Revive-Anteil nicht subsumiert).

### Optionale Extract-Submetriken (M23c)

Nur wenn `tile_extract_ms > 0` im Export:

| Feld | Bedeutung |
| --- | --- |
| `tile_visible_chunks` | Sichtbare Chunks mit geladenem World-Eintrag |
| `tile_cache_hits` / `tile_cache_misses` | Cache-Verhalten pro Frame |
| `tile_full_rebuild_ms` / `tile_cull_ms` | Microprofile innerhalb Tile-Extract |
| `deco_scanned_count` / `deco_visible_count` | Deko-Iteration vs. sichtbare Sprites |

Extract-KPIs für Compare: `game_core/perf/run_analysis/extract_kpis.py`

Schwellenvertrag und Cache-Vertrag: [`M23C_BASELINE.md`](M23C_BASELINE.md)

### Optionale Batching-Submetriken (M23d)

| Feld | Bedeutung |
| --- | --- |
| `tile_visible_batches` | Sichtbare Chunk-Layer-Gruppen pro Frame |
| `tile_registry_hits` / `tile_registry_misses` | Batch-Registry |
| `tile_cull_cache_hits` / `tile_cull_cache_misses` | Cull-Cache bei Pan/Zoom |
| `tile_assemble_ms` | Gruppen-Sammlung innerhalb `tile_extract_ms` |

Schwellenvertrag und Guardrails: [`M23D_BASELINE.md`](M23D_BASELINE.md). **LOD ist nicht Teil von M23d.**

### Optionale LOD-Submetriken (M23e)

| Feld | Bedeutung |
| --- | --- |
| `tile_lod0_groups` / `tile_lod1_groups` / `tile_lod2_groups` | Sichtbare Gruppen pro LOD-Stufe |
| `tile_lod0_ms` / `tile_lod1_ms` / `tile_lod2_ms` | Zeitanteil pro Stufe innerhalb `tile_extract_ms` |
| `tile_lod_switches` | Umschalt-Ereignisse zwischen LOD-Stufen |
| `tile_map_mode_active` | Map-Mode explizit aktiv (0/1) |

Schwellenvertrag und Guardrails: [`M23E_BASELINE.md`](M23E_BASELINE.md)

## Harte Befunde vs. Indizien

| Hart | Indiz |
| --- | --- |
| Summary-Abweichung bei Rekonstruktion | Pearson-Korrelation (r) |
| Anteil an `frame_ms` im Hitch-Frame | Hitch-Häufung am Budget-Cap |
| Tag-Zählung aus Export | Backlog-Korrelation über Mittelwerte |
| P95/Max aus Rohdaten | Periodisches Muster (heuristisches Fenster) |

Korrelationen werden interpretiert, aber **nicht als Ursache** behauptet.

## Budget-/Cap-Referenz

Caps (`max_applies_per_frame`, `max_unloads_per_frame`) werden aus `assets/content/streaming.json` geladen, Hitch-Schwellen aus `assets/content/profiling.json`. Bei abweichendem `config_fingerprint` im Manifest können die Referenzwerte vom aufgezeichneten Run abweichen — dann `--max-applies` / `--max-unloads` setzen.

## Architektur

```
game_core/perf/run_analysis/
  load.py        — Laden, schema_version, JSONL
  reconstruct.py — Summary nachrechnen, Plausibilität
  hitch.py       — Ursachen + Kontextmuster
  stats.py       — Verteilungen, Korrelation
  diagnose.py    — Run-Diagnose, Ranking
  fps_killers.py — M25a Attribution v2 (dominant_phase, quantiles, decision)
  report.py      — Terminal, Markdown, CSV, JSON
tools/analyze_perf_run.py — CLI
tools/compare_fps_killers.py — A/B fps_killers (M25a)
```

## Grenzen

- Keine Frame-by-Frame-Visualisierung
- Cap-Werte aus Projekt-Config, nicht aus dem Run-Snapshot
- Extract-Analyse nur wenn Felder im Export vorhanden
- M23a-Backlog nur mit `pending_unload_count` / Drain-Feldern
- Ursachenklassifikation threshold-basiert (50 % / 30 %)
