# Performance-Benchmarks (M23/M25)

Reproduzierbare CPU-Metriken für Streaming und Bridge-Extract (M23) plus Full-Frame-/Render-/Present-Attribution (M25).

## Milestone-Reihenfolge

| Milestone | Inhalt |
|-----------|--------|
| **M23** | Profiling & Runtime-Metriken (dieses Dokument) |
| **M23a** | Deferred Unload (in M23-Doku referenziert) |
| **M23b** | Apply-/Load-Burst-Entschärfung — [`M23B_BASELINE.md`](M23B_BASELINE.md) |
| **M23c** | Extract-Optimierung (Tile/Deko) — [`M23C_BASELINE.md`](M23C_BASELINE.md) |
| **M23d** | Chunk-Render-Batching — [`M23D_BASELINE.md`](M23D_BASELINE.md) |
| **M23e** | Visibility LOD / Map-Mode — [`M23E_BASELINE.md`](M23E_BASELINE.md) |
| **M24** | Ore-Patches & Resource-Deposits |
| **M25** | FPS Profiling & Hitch Attribution (Full-Frame, Render/Present, optional GPU) |

## Kanonischer Tick (`frame_ms`)

`frame_ms` misst Wall-Clock von `PerfSession.begin_tick()` bis `end_tick()` und umfasst **nur**:

1. Szenario-Schritt / Fokus-, View- und Delta-Berechnung
2. `ChunkStreamer.update`
3. `decorations_to_sprites` (wenn Extract aktiv)
4. `extractor.extract` (wenn Extract aktiv)

**Nicht enthalten:** GPU-Render, Swapchain, VSync, Input, Charakterbewegung, Paint/Editor, Save/Load, asynchrone Worker-Zeit außerhalb des Main-Thread-Ticks.

CLI und Demo nutzen dieselbe Funktion: `PerfSession.run_canonical_tick()`.

## M25: Full-Frame (`cpu_full_frame_ms`)

Zusätzlich zu M23 misst M25 optional den **vollständigen App-Frame** (inkl. Renderer-CPU und Present/VSync-Wartezeit):

- `cpu_full_frame_ms`: Frame-Beginn bis nach Present-Return
- `render_cpu_ms`: Renderer CPU (Record/Upload/Submit)
- `present_wait_cpu_ms`: CPU-Waits (Fence/Acquire/Present)

Diese Felder sind **optional** und erscheinen erst, wenn `PerfSession.full_frame_enabled = True` und die jeweiligen Timing-Hooks aktiv sind.

## Warmup

Profiling-Frames zählen erst **nach** der Warmup-Phase. Warmup-Ticks werden intern gezählt, fließen aber nicht in Export, Hitch-Events oder Summary-KPIs ein.

## Hitch-Tags

Geschlossene Menge (Mehrfach-Tags erlaubt, feste Sortierung):

1. `frame_slow`
2. `stream_slow`
3. `load_burst`
4. `unload_burst`

Schwellen ausschließlich aus [`assets/content/profiling.json`](../../assets/content/profiling.json). Apply- vs. Unload-Dominanz über `stream_apply_ms` / `stream_unload_ms`, nicht über extra Tags.

## CLI-Runs

```bash
python tools/run_perf_scenario.py --scenario steady
python tools/profile_frame.py --scenario pan
python tools/profile_frame.py --mode steady   # Legacy-Alias
```

Szenarien: `steady`, `pan`, `zoom_out`, `catchup` — Parameter in `profiling.json`.

Export nach: `docs/benchmarks/perf/runs/<run_id>/`

## Demo-Profiling

```bash
python -m apps.chunk_world_demo --profile
```

- Aktiviert `PerfSession` mit `run_mode = demo`
- Kanonischer Tick **vor** Bewegung und Render
- Minimales HUD (Rolling Stream-Mean, Hitch-Count, Chunk-Count) im Fenstertitel
- Export bei Exit

## Vergleich

```bash
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

- Nur identische `scenario_id`
- Unbekannte `schema_version` → harter Fehler (kein stiller Fallback)
- Additive optionale Summary-Felder brechen bekannte Version nicht

## Run-Analyse

```bash
python tools/analyze_perf_run.py docs/benchmarks/perf/runs/<run_id>
```

Diagnostische Auswertung: Summary-Plausibilität, Hitch-Ursachen, Kontextmuster, Korrelationen, Budget/Cap-Verhalten, priorisiertes Problem-Ranking. Ausgabe: Terminal + `<run_id>/analysis/` (Markdown, JSON, CSV).

Details, Begriffe und Heuristiken: [`ANALYSIS.md`](ANALYSIS.md)

M23b Baseline und DoD: [`M23B_BASELINE.md`](M23B_BASELINE.md)

M23c Extract-Baseline: [`M23C_BASELINE.md`](M23C_BASELINE.md)

M23d Batching-Baseline: [`M23D_BASELINE.md`](M23D_BASELINE.md)

M23e LOD-Baseline: [`M23E_BASELINE.md`](M23E_BASELINE.md)

Extract-Vergleich Pre/Post:

```bash
python tools/compare_perf_runs.py docs/benchmarks/perf/runs/<baseline> docs/benchmarks/perf/runs/<candidate>
```

Enthält ab M23c zusätzlich `tile_extract_ms_*`, `extract_ms_*`, `deco_extract_ms_*` aus `frames.jsonl`.

## Artefakte pro Run

| Datei | Inhalt |
|-------|--------|
| `manifest.json` | Schema-Version, Run-Metadaten, Config-Fingerprint |
| `frames.jsonl` | Eine Zeile pro Profiling-Frame |
| `hitches.jsonl` | Hitch-Events mit sortierten Tags |
| `summary.json` | Aggregierte KPIs (Mean, P95, Max, Hitch-Counts) |

### Zusätzliche M25-Artefakte (wenn Full-Frame vorhanden)

Unter `<run_id>/analysis/`:

- `fps_killers.md` — M25a: P95/P99 Dominanz, Plan-Enum `dominant_phase`, CPU-vs-Present
- `fps_killers.json` — maschinenlesbar (`attribution_version: 2`)
- `fps_killers_ab.json` — optional via `tools/compare_fps_killers.py`

Schema-Details: [`SCHEMA.md`](SCHEMA.md)

## Architektur

- Kern in `game_core/perf/` — **keine** `bridge`- oder `render_*`-Imports
- Instrumentierung in `ChunkStreamer.update(..., step_metrics=None)` — zero overhead wenn `None`
- Gemeinsamer Runner: `tools/run_perf_scenario.py`

## Deaktiviert = kein Hot-Path-Overhead

Profiling ist standardmäßig deaktiviert (`profiling.json` → `"enabled": false`). Ohne aktives Profiling: keine dauerhaften `perf_counter`-Aufrufe in Hot Paths, kein Export, kein HUD.
