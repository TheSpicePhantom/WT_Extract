---
name: M25 FPS Profiling & Hitch Attribution
overview: "M25 erweitert M23 (kanonischer CPU-Tick) zu einem vollständigen Frame-Time-Attribution-System über CPU-Phasen, Renderer-CPU, Present/VSync-Wartezeit und (optional) GPU-Timestamps — ohne Architekturgrenzen zu verletzen. Ergebnis sind reproduzierbare Szenarien, maschinenlesbare Exporte, Hitch-Klassifikation für P95/P99 und CI-regressionsfähige Gates, die eindeutig beantworten: CPU oder GPU, welche Phase dominiert, welche Feature-Toggles kausal sind und wo der höchste ROI liegt."
todos:
  - id: p0-baseline-contract
    content: "Phase 0: Ist-Daten und Contract fixieren (M23-Lücke dokumentieren, M25-Schema-Entwurf, Baseline-Run snapshotten)"
    status: pending
  - id: p1-cpu-full-frame-attribution
    content: "Phase 1: CPU-Attribution erweitern (neue Phasen: renderer_cpu, present_wait_cpu, optional sim/input) ohne game_core↔render_* Rückabhängigkeiten"
    status: pending
  - id: p2-renderer-cpu-instrumentation
    content: "Phase 2: Renderer-CPU Instrumentierung (record/submit/present) in render_core/render_graphics, Export via PerfSession-Bridge-API"
    status: pending
  - id: p3-gpu-timing-layer
    content: "Phase 3: GPU-Timestamps (QueryPool) optional aktivierbar, korrekte Korrelation pro Frame, robust gegen fehlende GPU/Extensions"
    status: pending
  - id: p4-hitch-classification-v2
    content: "Phase 4: Hitch-Klassifikation v2: P95/P99-Frames + Hitch-Events nach dominanter Phase/Feature-Toggles, Reports 'Top FPS Killer pro Szenario'"
    status: pending
  - id: p5-scenario-matrix
    content: "Phase 5: Szenario-Matrix + A/B-Toggles (idle/steady/pan/zoom/ingress/deco-heavy/render-only), deterministische Reproduktion"
    status: pending
  - id: p6-ci-gates
    content: "Phase 6: CI-Regression-Gates (CPU-Attribution Pflicht, GPU optional), harte Zahlen und Failure-Modes"
    status: pending
  - id: p7-docs-benchmarks
    content: "Phase 7: Benchmarks/Docs/Reports finalisieren (docs/benchmarks/perf/, neue M25 Baseline, DoD)"
    status: pending
isProject: false
---

# M25 — FPS Profiling & Hitch Attribution

## Ausgangslage (bindend, Ist-Daten)

Primärbeleg: `docs/benchmarks/perf/runs/20260713T190307Z_demo_unknown/analysis/analysis_report.md` und `analysis_diagnosis.json` (M23-Run-Analyse).

### Ist-KPIs (M23 kanonischer CPU-Tick)

- `frame_ms_mean = 23.0587`
- `frame_ms_p95 = 26.4927`
- `frame_ms_max = 57.2723`
- `stream_ms_mean = 17.8216`
- `stream_ms_p95 = 19.2320`
- Hitchs: `314/321` sind **Load-/Apply-dominant**
- Anteil an `frame_ms` (Run-Mittel):
  - Stream gesamt: **77.3 %**
  - Apply: **56.6 %**
  - Extract: **22.6 %**
  - Unload: **0.0 %**
- Muster: periodische Hitch-Cluster über den gesamten Run.

### Explizite Messlücke (M23 Contract)

M23 misst `frame_ms` nur von `PerfSession.begin_tick()` bis `end_tick()` und umfasst ausschließlich:

1. Szenario-Schritt
2. `ChunkStreamer.update(...)`
3. `decorations_to_sprites(...)` (wenn Extract aktiv)
4. `extractor.extract(...)` (wenn Extract aktiv)

Nicht enthalten (laut M23-Doku): GPU-Render, Swapchain, Present/VSync-Wartezeit, Input, Bewegung, HUD und sonstige Gameplay-Logik.

Quelle: `docs/benchmarks/perf/README.md` + Architekturtrennung in `docs/ARCHITECTURE.md`.

**Problem für FPS-Diagnose:** FPS/Frame-Time wird vom vollständigen Frame bestimmt (inkl. Render + Present/VSync). M23 kann deshalb nicht beantworten, ob FPS primär durch CPU-Phasen oder GPU/Present-Wait dominiert wird.

---

## Zieldefinition M25 (messbar)

M25 liefert ein **Frame-Time-Attribution-System**, das für jeden Profiling-Frame folgende Fragen eindeutig und automatisiert beantwortet:

1. **CPU oder GPU/Present?** (dominant für P95/P99)
2. **Welche Phase dominiert?** (Streaming-Unterphasen, Extract-Unterphasen, Renderer-CPU, Present-Wait, GPU)
3. **Welche Features verursachen Hitches?** (A/B-Toggles, kausale Signale)
4. **Welcher Fix hat höchsten ROI?** (Top-Killer pro Szenario + erwartbarer Gewinn)

### Primärmetriken (M25)

#### CPU (Wall-Clock, Phase-Sum)
- `cpu_full_frame_ms` — vom Beginn des „App-Frames“ bis nach Present-Return (oder nach Ende der Render-Submission), inkl. Waits auf CPU-Seite.
- `cpu_phase_*_ms` — disjunkte Phasen, Summe ≈ `cpu_full_frame_ms` (kleine Restdifferenz erlaubt).

#### Renderer/Present (CPU)
- `render_cpu_ms` — CPU-Zeit für Record/Prepare/Submit (Renderer-Pfad).
- `present_wait_cpu_ms` — CPU-Wartezeit, die mit Present/VSync/Acquire zusammenhängt (z. B. `AcquireNextImage`, Fence-Waits, Queue-Present-Block).

#### GPU (optional, Vulkan-Timestamps)
- `gpu_frame_ms` — GPU-Zeit zwischen Frame-Start/Ende-Timestamps.
- `gpu_renderpass_ms` — GPU-Zeit Render-Pass (oder Pipeline-Abschnitte, falls sinnvoll).

#### Attribution (abgeleitet)
- `dominant_phase` (enum) für P95/P99 und Hitch-Frames: `stream_apply`, `stream_pool`, `extract_tiles`, `extract_deco`, `render_cpu`, `present_wait`, `gpu`, `mixed`, `unclear`.
- `dominant_share` (0..1) — Anteil an `cpu_full_frame_ms` (bzw. GPU-Anteil, wenn GPU dominant).

---

## In Scope / Out of Scope

### In Scope

- Erweiterung von M23/M23x Perf-Export zu M25: **zusätzliche Zeitdomänen und Attribution**
- Instrumentierung in:
  - `game_core/perf/` (Modelle, Session, Export, Schema, Analyse/Report)
  - `tools/` (Runner, Analyzer, Compare, CI-gate Tooling)
  - `render_core/` + `render_graphics/` (Renderer-CPU + optional GPU-Timestamps)
  - `apps/chunk_world_demo.py` (Profiling-Hooks/Toggles, reproduzierbare Szenarien)
- Neue Szenarien und A/B-Toggles zur Kausalitätsisolation (CPU vs GPU vs Present-Wait).
- CI-regressionsfähige Gates (mindestens CPU-Attribution).

### Out of Scope (nicht M25)

- Optimierungen selbst (Streaming-Algorithmus, Deko-Indizes, Renderer-Refactors) — M25 ist Diagnose/Attribution, kein Tuning-Milestone.
- Render-Logik in `game_core` oder Imports `game_core -> render_*` (verboten durch Architektur).
- Vollständige GPU-Profiler-Integration (Vendor Tools, Tracy, RenderDoc) — optionaler Local-Workflow, aber nicht als Abhängigkeit.

---

## Root-Cause-Hypothesen (testbar, priorisiert)

H0 (Status Quo, nur M23): „stream_ms dominiert `frame_ms`“ ist wahr für den kanonischen Tick, sagt aber nichts über FPS.

### Hypothese H1 — Present/VSync dominiert (GPU/Wait)
- `cpu_full_frame_ms` ist deutlich größer als `frame_ms` und korreliert mit `present_wait_cpu_ms`.
- A/B: VSync aus / Present-Modus ändern → starke Veränderung in `cpu_full_frame_ms`, ohne Streaming/Extract zu ändern.

### Hypothese H2 — Renderer-CPU dominiert (Record/Upload/Submit)
- `render_cpu_ms` dominiert `cpu_full_frame_ms`, unabhängig von M23 `frame_ms`.
- A/B: Render-only ohne Streaming/Extract zeigt ähnliche Zeit.

### Hypothese H3 — GPU dominiert (Fill/Overdraw/Instanzcount)
- `gpu_frame_ms` oder `gpu_renderpass_ms` dominiert.
- A/B: Auflösung runter / Instanzcount runter / Draws reduzieren → GPU-Zeit fällt, CPU-Phasen stabil.

### Hypothese H4 — CPU-Kanonik ist tatsächlich der FPS-Killer (Streaming/Extract)
- `cpu_full_frame_ms` ≈ `frame_ms` + kleiner Render/Present-Anteil.
- Dominanz bleibt in `stream_apply` / `extract_*`.

### Hypothese H5 — Periodische Hitchs sind Budget-/Scheduler- oder Cache-Muster
- Hitch-Cluster korrelieren mit Caps (`max_applies_per_frame`, Registry/Cull Cache Misses, LOD Switches, Pending-Unload) und wiederholen sich in steady/pan.

---

## Phasenplan (umsetzbar, mit Artefakten und Gates)

### Phase 0 — Baseline & Contract Fixierung

**Primärquellen einchecken/referenzieren:**
- Run: `docs/benchmarks/perf/runs/20260713T190307Z_demo_unknown/analysis/analysis_diagnosis.json`
- Doku: `docs/benchmarks/perf/README.md`, `SCHEMA.md`, `ANALYSIS.md`

**Artefakte:**
- Neues Baseline-Dokument: `docs/benchmarks/perf/M25_BASELINE.md`
- Run-Snapshot (neuer run_id) mit stabilem Fingerprint für M25-Start.

**Gate P0 (Contract):**
- Der M25-Plan benennt eindeutig alle neuen Felder + deren Bedeutung + welche sind Pflicht/optional.
- Ein Baseline-Run ist reproduzierbar (CLI) und wird als Referenz verlinkt.

---

### Phase 1 — CPU Full-Frame Attribution (App-Frame statt nur kanonischer Tick)

**Ziel:** `cpu_full_frame_ms` einführen, ohne M23 zu brechen.

**Design:**
- M23 `frame_ms` bleibt unverändert (kanonischer Tick).
- M25 ergänzt eine zweite Messdomäne: „Full Frame“.

**Konkrete Code-Artefakte (Plan-Level):**
- `game_core/perf/models.py` — neue Felder/Enums (Phasen + dominant_phase)
- `game_core/perf/session.py` — neue API:
  - `begin_full_frame()` / `end_full_frame()`
  - Phasen-Timer-Helper (zero overhead wenn disabled)
- `docs/benchmarks/perf/SCHEMA.md` — Schema-Update (additiv, weiterhin `schema_version: 1` oder Version bump falls breaking)

**Gate P1 (Coverage):**
- Für jeden exportierten Frame gilt:
  - `cpu_full_frame_ms >= frame_ms`
  - Summe der CPU-Phasen erklärt **≥ 95 %** von `cpu_full_frame_ms` (Rest = `cpu_unattributed_ms` ≤ 5 %).

---

### Phase 2 — Renderer-CPU Attribution (Render-Record/Submit/Present-Wait)

**Ziel:** „Was passiert nach dem kanonischen Tick?“ messbar machen.

**Messpunkte (CPU):**
- Fence-Wait (Frame-in-flight)
- AcquireNextImage
- Staging Upload Record (Copy cmd)
- RenderPass Record (Draw cmds)
- QueueSubmit
- QueuePresent

**Konkrete Module:**
- `render_core/gpu_renderer.py` — Messpunkte rund um `vkWaitForFences`, `vkAcquireNextImageKHR`, `vkQueueSubmit`, `vkQueuePresentKHR`
- `render_graphics/ortho_renderer.py` — Abgrenzung renderer_cpu vs. game_core (keine game_core imports)
- `apps/chunk_world_demo.py` — Hook: Full-Frame beginnt vor `streamer.update` und endet nach `renderer.draw`/present.

**Export-Brücke (Architektur-konform):**
- `game_core/perf/` darf keine `render_*` Imports haben.
- Lösung: `PerfSession` bietet eine **datenträgerlose Recorder-API** (z. B. `perf.mark_phase(name, ms)`), die von Renderer/Demo gefüttert wird.

**Gate P2 (CPU Attribution):**
- In `analysis_report.md` wird für jedes Szenario ein Ranking ausgegeben:
  - `Top3_cpu_phases_by_p95_share`
  - `Top3_cpu_phases_by_mean_share`

---

### Phase 3 — GPU Timing Layer (optional, aber standardisiert)

**Ziel:** GPU-Zeit pro Frame erfassen, ohne auf Systemen ohne GPU-Timing zu brechen.

**Konkrete Implementierungsbausteine (Plan-Level):**
- `render_core/gpu_timing.py` (neu): QueryPool Lifecycle, Timestamp-Frequenz, Readback, per-frame buffering
- Hookpunkte im Command Buffer:
  - `cmd_write_timestamp(frame_start)`
  - `cmd_write_timestamp(after_renderpass)` (optional)
  - `cmd_write_timestamp(frame_end)`
- Export-Felder nur, wenn GPU timing verfügbar/aktiv.

**Gate P3 (Robustheit):**
- Wenn GPU timing nicht verfügbar: Felder fehlen/`None`, Analyse fällt nicht um.
- Wenn verfügbar: `gpu_frame_ms >= gpu_renderpass_ms`, Werte sind plausibel (nicht negativ, nicht 0 über alle Frames).

---

### Phase 4 — Hitch Attribution v2 (P95/P99 + Feature-Kausalität)

**Ziel:** Periodische Hitchs nicht nur „stream_slow“, sondern nach dominanter Ursache klassifizieren, inkl. CPU vs GPU vs present_wait.

**Analyse-Artefakte:**
- `tools/analyze_perf_run.py` erweitert um:
  - P95/P99 Frame-Sampling + Ursache
  - „dominant_phase“ für Hitch-Frames
  - Periodizitäts-/Clustererkennung über neue Phasen
- Output:
  - `docs/benchmarks/perf/runs/<run_id>/analysis/fps_killers.md`
  - `.../analysis/fps_killers.json`
  - CSV: `fps_killers_by_scenario.csv`

**Gate P4 (Antwortfähigkeit):**
- Für jedes Szenario gibt der Report **deterministisch** aus:
  - CPU-vs-GPU Entscheidung (mit Begründungsfeldern)
  - dominierende Phase P95 und P99
  - Top-Feature-Toggle Kausalität (A/B-Diff)

---

### Phase 5 — Szenario-Matrix + A/B Feature-Toggles

**Ziel:** Ursachen isolieren statt nur „Demo ist langsam“.

**Szenarien (mindestens):**
- `idle` — keine Bewegung, steady visibility (Warm)
- `steady` — heutiger steady Run (Baseline)
- `pan` — konstantes Kamera-Panning
- `zoom_stress` — Zoom-in/out innerhalb Grenzen
- `ingress_stress` — erzwungene Chunk-Ingress (Move in neue Gebiete)
- `deco_heavy` — Deko-Dichte hoch / Deko-Extract stress
- `render_only` — Streaming/Extract aus, Render + Present isoliert

**A/B-Toggles (mindestens):**
- Extract aus (`extract_enabled=false`)
- Deko-Extract aus / Deko-Sprites aus
- Tile-Extract aus / Tiles aus (nur Clear + optional Sprites)
- Streaming update aus (statisches World)
- VSync/Present-Mode Toggle (sofern Plattform das zulässt) oder „simulate present wait“ Messung
- Auflösung/Viewport-Scale Toggle (GPU-Signal)

**Artefakte:**
- `assets/content/profiling.json` — Szenarien + Toggle-Flags
- `tools/run_perf_scenario.py` — Toggle-Handling, deterministische Seeds

**Gate P5 (Isolation):**
- Für jedes Szenario existiert mindestens ein A/B-Paar, das eine Hypothese H1–H4 testet, und der Report zeigt den Effekt in Zahlen (`Δp95`, `Δdominant_share`).

---

### Phase 6 — CI Regression Gates

**Ziel:** Nicht nur messen, sondern regressionssicher verhindern.

**CI-Pflicht (CPU-only):**
- Mindestens 2 Szenarien (z. B. `steady`, `pan`) laufen in CI und erzeugen Exporte.
- Gates prüfen:
  - `cpu_full_frame_ms_p95` ≤ Zielwert (Zwischenziel) oder ≤ Baseline * (1 + tolerance)
  - `present_wait_cpu_ms_mean` ≤ Schwelle (wenn in CI stabil messbar; sonst nur lokal)
  - Anteil `cpu_unattributed_ms` ≤ 5 %

**CI-optional (GPU timing):**
- Wenn GPU timing aktiv: zusätzlich `gpu_frame_ms_p95` Gate.

**Artefakte:**
- `tools/gate_perf_run.py` (neu oder Erweiterung): liest Run(s), prüft Gates, exit!=0 bei Verstoß.
- `docs/benchmarks/perf/M25_BASELINE.md` — referenziert Gate-Zahlen + Toleranzen.

**Gate P6 (Fail-fast):**
- Ein absichtlicher Regression-Test (z. B. künstlicher Sleep/Toggles) wird zuverlässig erkannt und lässt CI fehlschlagen.

---

### Phase 7 — Docs, Baselines, DoD-Finalisierung

**Neue/aktualisierte Dokumente:**
- `docs/milestones/m25_fps_profiling.plan.md` (dieses Dokument)
- `docs/benchmarks/perf/M25_BASELINE.md`
- `docs/benchmarks/perf/README.md` (M25-Ergänzung: full frame + renderer/gpu)
- `docs/benchmarks/perf/SCHEMA.md` (Felder + Semantik)
- `docs/benchmarks/perf/ANALYSIS.md` (Attribution v2, Dominanz-Regeln, P95/P99)

**Gate P7 (Doku-Vertrag):**
- Alle neuen Felder sind dokumentiert, Analyse-Outputs sind beschrieben, und ein neuer Run zeigt die M25-Abschnitte im Report.

---

## Tests / Benchmarks (konkret)

### Unit/Contract Tests
- `tests/test_perf_schema.py` — Schema-Felder vorhanden/optional, Backward-Compat (M23→M25)
- `tests/test_perf_attribution.py` — Phasen-Summe/Restbudget, Dominanzklassifikation deterministisch
- `tests/test_perf_gates.py` — Gate-Tooling schlägt korrekt fehl

### Benchmark/Run Artefakte
- Neue Run-Outputs unter `docs/benchmarks/perf/runs/<run_id>/analysis/`:
  - `fps_killers.md`
  - `fps_killers.json`
  - `notable_frames.csv` (erweitert: P95/P99 + dominant_phase)

---

## Risiken / Nicht-Ziele

- GPU-Timestamps sind plattform-/treiberabhängig: M25 muss ohne GPU-Timing funktionieren (CPU-only Pflicht).
- Present/VSync-Wartezeiten können auf CI-Runnern instabil sein: CI-Gates müssen darauf vorbereitet sein (Tiering: CPU Pflicht, GPU/Present optional).
- Zu viele Toggle-Kombinationen explodieren: Szenario-Matrix bewusst klein halten, aber kausal aussagekräftig.

---

## Definition of Done (hart)

M25 gilt als abgeschlossen, wenn für mindestens die Kern-Szenarien `steady`, `pan`, `render_only` gilt:

1. **CPU-vs-GPU Entscheidung:** Report liefert „CPU-dominant / GPU-dominant / present-wait-dominant“ mit messbarer Begründung.
2. **Dominante Phase:** Für P95 und P99 wird `dominant_phase` ausgegeben und ist stabil reproduzierbar.
3. **Feature-Kausalität:** Mindestens ein A/B-Toggle pro Szenario isoliert die Ursache (nachweisbarer Δ in den dominanten Feldern).
4. **CI-Gates:** CPU-Attribution-Gates laufen in CI und schlagen bei Regression deterministisch fehl.
5. **Artefakte:** Neue Reports/JSON/CSV liegen pro Run vor; Doku/Schemavertrag ist aktualisiert.

