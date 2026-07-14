# Run-Analyse — Diagnosewerkzeug

Das Tool `tools/analyze_perf_run.py` wertet exportierte Profiling-Runs (M23/M23a) diagnostisch aus. Es rekonstruiert KPIs aus `frames.jsonl`, klassifiziert Hitches regelbasiert und leitet Run-weite Muster ab.

## Aufruf

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
```

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
- `fps_killers.md` — M25: FPS-Killer/Attribution (nur wenn Full-Frame-Felder vorhanden)
- `fps_killers.json` — M25: maschinenlesbare Attribution

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
  report.py      — Terminal, Markdown, CSV, JSON
tools/analyze_perf_run.py — CLI
```

## Grenzen

- Keine Frame-by-Frame-Visualisierung
- Cap-Werte aus Projekt-Config, nicht aus dem Run-Snapshot
- Extract-Analyse nur wenn Felder im Export vorhanden
- M23a-Backlog nur mit `pending_unload_count` / Drain-Feldern
- Ursachenklassifikation threshold-basiert (50 % / 30 %)
