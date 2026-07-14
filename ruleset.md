# Projektbriefing: Python + Vulkan Rendering Engine als wiederverwendbarer Blueprint

## Kontext

Wir bauen zuerst **eine eigenständige Rendering Engine in Python + Vulkan** und **keine vollständige Game Engine**.  
Das erste Testprojekt ist ein **top-down Spiel im Stil von Factorio**, aber dieses Spiel ist **nur ein Anwendungsfall**, nicht die Definition der Architektur.

Die Rendering Engine soll so gebaut werden, dass sie später auch für andere Projekte wiederverwendet werden kann, z. B.:
- top-down Aufbau-/Automationsspiele
- Shooter oder Survival-Prototypen
- Simulationen
- andere tile-, chunk- oder spritebasierte Projekte

## Primäres Ziel

Das Ziel ist eine **leichte, performante, modulare und strikt getrennte Rendering Engine**, bei der Python die Steuerung übernimmt und Vulkan die GPU-nahe Arbeit erledigt.

Die Engine soll:
- möglichst viel Arbeit GPU-seitig vorbereiten oder ausführen
- Python-Overhead im Frame-Loop klein halten
- klar geschichtete Zuständigkeiten haben
- später neue Features integrierbar machen, ohne die Basis zu zerbrechen
- bewusst **renderer-first** gedacht sein, nicht gameplay-first

## Entwicklungsreihenfolge

Die Reihenfolge des Gesamtprojekts ist fest:

1. Rendering Engine stabil aufbauen
2. Welt- / Chunk-Generierung
3. Charakter
4. Decoration
5. Prozedurales Terrain

Wichtig:  
Die Architektur der Rendering Engine darf **nicht** vom ersten Spielkontext abhängig gemacht werden.

---

# Source of Truth

Diese Datei (`ruleset.md`) ist die **einzige verbindliche Source of Truth** für:
- Architekturprinzipien und Verbote
- Meilenstein-Roadmap (M1–M28+)
- Abhängigkeitsregeln
- Konventionen (Koordinaten, Layer, Naming)

`docs/ARCHITECTURE.md` dokumentiert **Implementierungsdetails abgeschlossener Meilensteine** — konkrete Dateipfade, Fehlerbehebungen, Demohinweise, technische Entscheidungen die getroffen wurden.  
Bei Widerspruch gilt `ruleset.md`.

> Bei Änderungen an Architektur oder Roadmap: erst `ruleset.md` aktualisieren, dann ggf. `ARCHITECTURE.md` ergänzen.

---

# Architekturprinzipien

## 1. Strikte Trennung: Render Engine != Game Engine

Die Render Engine muss **vollständig von der Game Engine getrennt** sein.  
Rendering darf den Spielzustand nicht verändern; es darf nur aus vorbereiteten Daten ein Bild erzeugen.

### Das bedeutet konkret:
- Die Game Engine erzeugt Bedeutung und Simulation.
- Die Render Engine verarbeitet neutrale Renderdaten.
- Die Verbindung erfolgt über eine klar definierte Übergabeschicht.
- Die Render Engine kennt keine Spielregeln.
- Die Game Engine kennt keine Vulkan-Details.

### Erlaubtes Modell
`game_core -> extractor/bridge -> render_scene -> render_core`

### Nicht erlaubt
`render_core -> game_core`

---

## 2. Layered Architecture

Wir wollen bewusst eine **Layered Architecture** mit klaren Verantwortlichkeiten, weil sie für komplexe Engine-Systeme Modularität und Wartbarkeit verbessert.

Jede Schicht hat eine klar definierte Rolle.  
Abhängigkeiten laufen möglichst nur **in eine Richtung**.

### Zielstruktur

- `wt_platform/` (ehem. `platform/` — Name vermeidet Konflikt mit Python-Stdlib)
  - Fenster
  - Surface-Erstellung
  - Input-Grundlagen
  - keine Spielregeln

- `render_core/`
  - Vulkan Instance
  - Physical/Logical Device
  - Queues
  - Swapchain
  - Command Pools / Command Buffers
  - Synchronisation
  - Speicher / Ressourcen-Lifetime
  - Low-Level GPU-Infrastruktur

- `render_graphics/`
  - Pipelines
  - Shaderverwaltung
  - Render Passes / Framegraph-Vorbereitung
  - Kamera
  - Materialsystem
  - Instancing
  - Sprite- / Tile-Rendering
  - Render Submission

- `render_scene/`
  - neutrale Datentypen für Renderdaten
  - z. B. `RenderFrame`, `CameraData`, `SpriteInstanceData`, `TileChunkRenderData`
  - keine Vulkan-spezifische Geschäftslogik
  - keine Gameplay-Semantik

- `game_core/`
  - Welt
  - Chunklogik
  - Generierung
  - Charakter
  - Interaktion
  - Simulation
  - spätere Gameplay-Systeme

- `bridge/` oder `extractors/`
  - übersetzt Game-Daten in neutrale Renderdaten
  - einzige legitime Stelle, an der Spielwelt und Renderer-Input aufeinandertreffen

---

## 3. Renderdaten statt Game-Objekte

Der Renderer darf **niemals direkt mit Game-Objekten arbeiten**.

### Das heißt:
Die Game Engine übergibt nicht:
- `Player`
- `OrePatch`
- `TransportBelt`
- `FactoryBuilding`
- `EnemyUnit`

Sondern nur neutrale, renderbare Daten wie:
- Kamera
- Layer
- Positionen
- Instanzdaten
- Material- oder Texture-Handles
- Sprite-/Tile-IDs
- sichtbare Chunkdaten

### Gewünschte Datentypen
- `RenderFrame`
- `CameraData`
- `TileLayerBatch`
- `TileChunkRenderData`
- `SpriteInstanceData`
- `MaterialHandle`
- `TextureHandle`

---

## 4. Datenorientiertes Denken

Die Renderdaten sollen möglichst **datenorientiert** strukturiert werden, nicht als tiefer OOP-Objektbaum.

Bevorzugt:
- kompakte Arrays
- handles / ids
- SoA oder klar strukturierte Buffers
- wiederverwendbare GPU-Ressourcen
- geringe per-frame Allokation
- Caching statt Neubau

Nicht bevorzugt:
- tiefe Vererbung
- tausende kleine Python-Objekte im Hot Path
- Renderer pro Entity
- zu viele dynamische Spezialklassen

---

# Technische Zielrichtung

## Python + Vulkan

Die Basis ist **Python + Vulkan**.

### Rollenverteilung
- Python:
  - Engine-Steuerung
  - Ressourcenverwaltung
  - Szenen-/Frame-Aufbereitung
  - Brückenlogik
  - Tooling / Iteration

- Vulkan:
  - GPU-Ressourcen
  - Command Recording
  - Draws / Dispatches
  - Synchronisation
  - Speicher- und Pipelinekontrolle

## Performance-Ziel

Die Architektur soll so ausgelegt werden, dass:
- CPU-seitige Draw-Submission effizient bleibt
- Command Buffers nicht chaotisch erzeugt/zerstört werden
- Pipeline-Wechsel minimiert werden
- Queue Submissions bewusst gebündelt werden
- Instancing früh sauber unterstützt wird
- Chunk-Rendering ohne Architekturbruch nachgerüstet werden kann

---

# Erster konkreter Use Case

## Spieltyp

Erster Testfall:  
ein **top-down Factorio-artiges Spiel**

## Aber wichtig:
Der Renderer wird **nicht** als „Factorio-Renderer" gebaut, sondern als generischer:
- orthographischer 2D/2.5D Renderer
- mit Tile-Layern
- Sprite-/Atlas-Unterstützung
- Instancing
- chunkfreundlicher Datenstruktur

## Frühe Kernfeatures des Renderers

Der erste Renderer soll idealerweise vorbereiten oder unterstützen:
- Orthographic Camera
- Texture Atlas
- Instanced Quads für Tiles und Sprites
- Layer-basiertes Rendering
- sichtbarkeitsfreundliche Chunkdaten
- stabile RenderFrame-Einspeisung
- sauber getrennte Low-Level / Mid-Level / Frame-Daten-Struktur

---

# Was auf gar keinen Fall passieren darf

## Harte Verbote

### 1. Keine Vermischung von Render- und Gameplay-Logik
Nicht erlaubt:
- Gameplay-Code im Renderer
- Renderer-Code in Welt-/Entity-Klassen
- Shader- oder Pipeline-Entscheidungen auf Basis direkter Spielregeln
- Spielzustandsänderungen im Renderpfad

### 2. Keine spielspezifische Semantik im Renderer
Nicht erlaubt:
- `PlayerRenderer`
- `OreRenderer`
- `FactoryChunkRenderer`
- `EnemySpriteManager`

Wenn spezielle Spielobjekte gerendert werden, müssen sie **vorher** in generische Renderdaten übersetzt werden.

### 3. Kein monolithischer Engine-Klumpen
Nicht erlaubt:
- eine riesige `engine.py`
- eine `Renderer`-Klasse, die Fenster, Welt, Kamera, Simulation und GPU gleichzeitig kennt
- unklare Zuständigkeiten
- globale, implizite Engine-Zustände

### 4. Kein vorschneller Feature-Bloat

Dieses Verbot gilt für **Phase 1** (Kern-Renderer, M1–M20).  
In Phase 2 (World, M21–M24) und Phase 3 (Gameplay, M25–M29) werden diese Systeme gezielt eingeführt — jeweils mit eigenem Scope und bewusstem "Bewusst nicht in diesem Milestone".

Vor dem stabilen Kernrenderer (Phase 1) **nicht** einbauen:
- komplexe Partikelsysteme
- generische Engine-Animations-Frameworks (Spritesheet-Sub-UV per Instanz wie in M11 ist kein Framework — das ist eine direkte GPU-Datenstruktur; gemeint sind abstrakte `Animator`-Klassen mit eigenem Lifecycle)
- Editor
- Audio (→ Phase 3, M28)
- UI-Framework (→ Phase 3, M27)
- Networking
- komplexes Beleuchtungssystem
- Gameplay-ECS mit vielen Spezialfällen

### 5. Keine Architektur nur für dieses eine Spiel
Nicht erlaubt:
- Tile-/Chunk-Systeme so zu codieren, dass sie nur für Factorio-artige Weltlogik funktionieren
- Renderer-APIs auf konkrete Spielobjekte zuzuschneiden
- spätere Wiederverwendung unbrauchbar zu machen

### 6. Kein verschwenderischer Vulkan-Umgang
Nicht erlaubt:
- wildes Erzeugen/Zerstören von Command Pools
- chaotisches pro-frame Neuaufbauen aller Ressourcen
- unnötig viele Queue Submits
- unnötig viele Pipeline Binds
- per-frame CPU-Müllproduktion im Hot Path

---

# Anforderungen an Cursor

## Arbeitsweise

Arbeite **architekturorientiert**, nicht demo-orientiert.  
Wenn mehrere Lösungen möglich sind:
- nenne die bevorzugte Lösung
- begründe sie knapp
- priorisiere Wiederverwendbarkeit, Trennung und Performance

## Bitte nicht tun
- Keine riesige Komplettlösung ohne Struktur
- Keine voreilige Vollimplementierung aller Systeme
- Kein „hier ist schon mal alles in einer Datei"
- Keine Vermischung von endgültiger Architektur und schneller Wegwerf-Demo

## Bitte stattdessen tun
Arbeite in klaren Schritten:
1. Architektur definieren
2. Modulbaum definieren
3. Kerninterfaces definieren
4. Abhängigkeitsregeln definieren
5. Minimalen Renderer planen
6. Danach Erweiterungspfad für Chunk-Welt vorbereiten

---

# Meilensteinübersicht

## Abgeschlossene Meilensteine (M1–M20)

| # | Meilenstein | Module | Status |
|---|-------------|--------|--------|
| M1 | Projektstruktur + Interfaces | `render_scene`, `bridge`, `docs` | ✅ |
| M2 | Fenster + Vulkan Instance/Device | `wt_platform`, `render_core` | ✅ |
| M3 | Swapchain + erster Clear-Frame | `render_core` | ✅ |
| M4 | Orthographische Kamera | `render_graphics` | ✅ |
| M5 | Instanced Quads (einfarbig) | `render_graphics` | ✅ |
| M6 | Texture Atlas + Material-Handles | `render_graphics`, `render_scene` | ✅ |
| M7 | Erster Tile-Layer aus `TileLayerBatch` | `render_graphics` | ✅ |
| M8 | Chunk-Daten via `TileChunkRenderData` | `render_graphics`, `bridge`, `game_core` | ✅ |
| M9 | Frame-Staging-Upload (kein per-Frame Command Pool / WaitIdle) | `render_core`, `render_graphics` | ✅ |
| M9b | Mehrere Tile-Layer pro Chunk — Draw-Reihenfolge nach `LayerId` | `render_graphics`, `bridge`, `game_core` | ✅ |
| M10 | Mutable Welt — Tiles zur Laufzeit ändern, Dirty-Chunks | `game_core`, `bridge`, `apps` | ✅ |
| M11 | Charakter + Spritesheet-Animation (Idle/Walk/Run, 8-Wege) | `game_core`, `bridge`, `render_graphics`, `apps` | ✅ |
| M12 | Decoration-Sprites + Content-Registry (JSON) | `game_core`, `bridge`, `tools`, `apps` | ✅ |
| M12b | Data-driven Tile-Pinsel (`tiles.json` Brushes) | `game_core`, `apps` | ✅ |
| M13 | Y-Sort + Stamm/Krone-Split (Tiefen-Sortierung) | `render_graphics`, `bridge`, `game_core` | ✅ |
| M14 | Kollision / Walkability (Tiles + Decorations) | `game_core`, `apps` | ✅ |
| M15 | Pixel-Kollision (Masken + 8×8 Solid-Grid) | `game_core`, `tools`, `apps` | ✅ |
| M16 | Welt-Persistenz (Save/Load JSON) | `game_core`, `apps` | ✅ |
| M17 | Dirty-Chunk-Render-Cache | `bridge`, `game_core` | ✅ |
| M18 | Chunk-Streaming (infinite prozedural) | `game_core`, `apps` | ✅ |
| M19 | Fenster-Resize & Vollbild (Swapchain/Surface) | `wt_platform`, `render_core`, `render_graphics`, `apps` | ✅ |
| M20 | Platform-Schale + Streaming-Persistenz | `wt_platform`, `game_core`, `apps` | ✅ |

## Aktuelle und kommende Meilensteine (M21+)

| # | Meilenstein | Module | Status |
|---|-------------|--------|--------|
| M21 | Hybrid World-Gen (Noise, Klima, Voronoi-Biome) | `game_core`, `apps` | ✅ |
| M22 | Biome-System (Feinschliff / Erweiterungen) | `game_core`, `apps` | ✅ |
| M22b | Parallel Chunk Generation (ProcessPool) | `game_core`, `apps` | ✅ |
| M22c | FNV Tile-ID IPC (ChunkGenResult ints) | `game_core` | ✅ |
| M22d | Hybrides Chunk-Streaming (Viewport + Safety) | `game_core`, `apps` | ✅ |
| M22e | Worker-Deko + Worker-Solid (ProcessPool Apply) | `game_core` | ✅ |
| M23 | Profiling & Runtime-Metriken | `game_core`, `tools`, `apps` | ✅ |
| M23a | Deferred Unload & Sparse Persistence | `game_core`, `apps` | ✅ |
| M23b | Apply-/Load-Burst-Entschärfung | `game_core`, `tools` | ✅ |
| M23c | Extract-Optimierung (Tile/Deko) | `bridge`, `game_core/perf`, `tools` | ✅ |
| M23d | Chunk-Render-Batching | `bridge`, `game_core/perf`, `tools` | ✅ |
| M23e | Visibility LOD / Map-Mode | `bridge`, `game_core/perf`, `assets/content`, `tools` | ✅ |
| M24 | Ore-Patches + Resource-Deposits (prozedural) | `game_core`, `apps` | ⬜ |
| M25 | Mini-Map / Fog of War | `render_graphics`, `render_scene`, `bridge`, `game_core` | ⬜ |
| M26 | Inventar & Item-System (Grundlagen) | `game_core`, `apps` | ⬜ |
| M27 | Entity-System (NPCs / Feinde, Grundstruktur) | `game_core`, `bridge`, `apps` | ⬜ |
| M28 | Einfaches UI-Framework (HUD, Labels) | `render_graphics`, `render_scene`, `apps` | ⬜ |
| M29 | Audio-System (Grundlagen, SFX) | `wt_platform`, `apps` | ⬜ |

> **Hinweis Modul-Spalte M21:** Bridge und Renderer benötigen keine Änderungen — `game_core` liefert nach M21 weiterhin denselben `TileLayerBatch`. Nur `game_core` und `apps` sind betroffen.

---

# Meilenstein-Details

## M21 — Hybrid World-Gen (Noise, Klima, Voronoi-Biome)

**Ziel:** Deterministische prozedurale Welt — Height/Wasser, Klima, unendliche Voronoi-Biomregionen (Warp, Blend), biomabhängige Tiles/Decorations, Startgebiet-Regeln. Detail-Spec: [`milestones_detailed/world-gen.md`](milestones_detailed/world-gen.md).

**Anforderungen:**
- Deterministisch: gleicher `world_seed` + Weltkoordinate `(wx, wy)` → identisches Ergebnis über Sessions und Chunk-Grenzen
- Generierung vollständig in `game_core` — Renderer/Bridge **keine Änderungen**
- Kompatibel mit M18 Streaming und M20 Persistenz (`persistent_overrides` hat Vorrang)

**Noise:** fBM auf **eigener 2D-Simplex-Implementierung** in [`game_core/noise.py`](game_core/noise.py) (keine PyPI-Dependency)

**Module:**
- [`game_core/world_gen.py`](game_core/world_gen.py) — `WorldGenConfig`, `sample_climate`, `sample_biome_region`, `resolve_tile`, `generate_chunk`, `populate_chunk_decorations`
- [`game_core/biomes.py`](game_core/biomes.py) — `BiomeId`, `ClimateClass`, JSON-Mapping
- [`assets/content/world_gen.json`](assets/content/world_gen.json), [`assets/content/biomes.json`](assets/content/biomes.json)
- Neue Tiles: `deep_water`, `shallow_water`, `sand`, `snow`

**Streaming:** Save v3 — `world_seed` in `manifest.json`; Load setzt `configure_world_gen()`

**Demos:**
- `chunk_world_demo` — `G` = neuer Seed via `ensure_playable_seed`, nur prozedurale Chunks flushen, Overrides bleiben
- `world_gen_debug_demo` — Zwischenschritte visualisieren (Height, Water, Klima, Voronoi, Terrain, Decorations)

**M21-Rest (abgeschlossen mit M22):** `ChunkFieldCache`, Debug-Modus Decorations, Startgebiet-Scoring (`score_spawn_area`, `ensure_playable_seed`)

**Bewusst nicht in M21:** Rivers/Hydrologie, Ore/Ressourcen (→ M24), GPU-Noise, async Jobs

---

## M22 — Biome-System (Feinschliff)

**Ziel:** Layer-0-Biom-Blend via `blend_t`, Sub-Biom-Noise, Deko-Blend in Übergangszone, erweiterte `biomes.json`. **Kern-Biomlogik aus M21.**

**Umsetzung:**
- [`game_core/biomes.py`](game_core/biomes.py) — `resolve_blended_layer0`, `decorations_for_blend_zone`, `pick_biome_variant`
- [`game_core/world_gen.py`](game_core/world_gen.py) — `ChunkFieldCache`, `build_chunk_field_cache`, `resolve_tile_cached`, `sample_sub_biome`
- [`assets/content/biomes.json`](assets/content/biomes.json) — `blend.threshold`, `blend.transitions`
- [`assets/content/world_gen.json`](assets/content/world_gen.json) — `sub_biome`, erweiterte `start_area`-Felder

**Demos:**
- `world_gen_debug_demo` — `S` SubBiome, `D` Decorations (Terrain + `populate_chunk_decorations`)
- `chunk_world_demo` — Titel zeigt `seed` + Spawn-`score` nach `G`-Regen

**Bewusst nicht in M22:**
- Rivers/Hydrologie, Ore/Ressourcen (→ M24)
- Wetter oder Tageszeit pro Biom
- GPU-Noise, async Worldgen

> **Hinweis M22 (historisch):** Kern-Biomlogik (Voronoi, Klima, Tile-/Decoration-Mapping) war bereits in M21 enthalten; M22 liefert Blend-Tiles, Sub-Biom-Noise und Performance-Cache.

---

## M22b — Parallel Chunk Generation

**Ziel:** Terrain parallel erzeugen; Decorations und Solid-Rebuild **ausschließlich Main-Thread** (→ M22e: optional Worker-Apply).

**Module:**
- [`game_core/world_gen_context.py`](game_core/world_gen_context.py) — `WorldGenContext`, lokaler fBM-Cache
- [`game_core/world_gen_result.py`](game_core/world_gen_result.py) — `ChunkGenResult` (kompakte IPC, `decorations=None` in M22b)
- [`game_core/world_gen_parallel.py`](game_core/world_gen_parallel.py) — `generate_chunks_parallel`, langlebiger Pool
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — Streaming-Prefetch, discard-on-arrival
- [`tools/benchmark_world_gen.py`](tools/benchmark_world_gen.py) — Vorher/Nachher in [`docs/benchmarks/world_gen_m22b.md`](docs/benchmarks/world_gen_m22b.md)

**Config:** `world_gen.json` → `parallel.workers` (`"auto"` / `0`), `parallel.prefetch`

**Bewusst nicht in M22b:** Worker-Deko, Tile-ID-IPC (→ M22c), hartes Task-Cancel

---

## M22c — FNV Tile-ID IPC

**Ziel:** `ChunkGenResult.layer0/layer1` als `tuple[int, ...]` (FNV-1a auf normalisierte Tile-Keys); Worker ohne Registry-Map; Main-Thread `chunk_from_result(result, content)`.

**Module:**
- [`game_core/tile_ids.py`](game_core/tile_ids.py) — `stable_tile_id`, `EMPTY_TILE_ID`, `build_tile_key_by_id` (Kollisions-Assert beim Laden)
- [`game_core/world_gen_result.py`](game_core/world_gen_result.py) — `ChunkGenResult` mit int-Layern
- [`game_core/content_registry.py`](game_core/content_registry.py) — `tile_key_to_id` / `tile_id_to_key` via FNV

**Modding:** Keys `namespace:path` — Reihenfolge in `tiles.json` irrelevant; Kollisionen beim Content-Merge → Build-Fehler.

---

## M22d — Hybrides Chunk-Streaming

**Ziel:** Viewport-basiertes Laden statt fixem Radius — weniger Chunks pro Frame, keine Multi-Sekunden-Spikes beim Panning; Spieler-Safety-Ring und Prefetch-Strip in Bewegungsrichtung.

**Module:**
- [`game_core/stream_view.py`](game_core/stream_view.py) — `StreamViewParams`, `compute_stream_sets` (wanted/keep/prefetch)
- [`game_core/streaming_config.py`](game_core/streaming_config.py) — `StreamingConfig`, `load_streaming_config()`
- [`assets/content/streaming.json`](assets/content/streaming.json) — `mode: hybrid` \| `radius`, Caps, `max_applies_per_frame`
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — hybrid + radius fallback; Apply-Budget; Pool ohne Sync-Fallback

**Mengen (hybrid):**
- `wanted` = Viewport (gecappt) ∪ Player-Safety-Ring (Chebyshev)
- `keep` = AABB von wanted + `keep_padding_chunks` (Hysterese)
- `prefetch` = Strip in Bewegungsrichtung (`move_dx`/`move_dy`)

**Demos:** `chunk_world_demo`, `world_gen_debug_demo`, `tools/profile_frame.py` und `tools/run_perf_scenario.py` nutzen den gemeinsamen kanonischen Tick (M23).

**Bewusst nicht in M22d:** Spatial Index für Decorations, GPU-Culling-Änderungen

---

## M22e — Worker-Deko + Worker-Solid

**Ziel:** Prozedurale Deko-Platzierung und Solid-Grid-Berechnung im ProcessPool; Main-Thread wendet nur `WORKER_COMPLETE`-`ChunkGenResult` via `apply_chunk_result` an.

**Module:**
- [`game_core/world_gen.py`](game_core/world_gen.py) — `compute_procedural_decorations` (Pure)
- [`game_core/world_gen_context.py`](game_core/world_gen_context.py) — `generate_chunk_result`
- [`game_core/world_gen_result.py`](game_core/world_gen_result.py) — `apply_worker_complete_result`, `apply_chunk_result`, `is_worker_complete`
- [`game_core/worker_content_snapshot.py`](game_core/worker_content_snapshot.py) — Walkable/Deko-Regeln für Worker-Solid
- [`game_core/collision_grid.py`](game_core/collision_grid.py) — `build_chunk_solid_grid` (Pure)
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Router `_apply_chunk_from_result`

**Pfadtrennung:** Override, Sync, Debug, `worker_apply=false` → `_ensure_procedural_decorations` + `rebuild_chunk_solid`.

**Config:** `world_gen.json` → `parallel.worker_apply`

**Golden-Tests:** [`tests/support/chunk_reference.py`](tests/support/chunk_reference.py) — `sequential_reference_chunk`

**Bewusst nicht in M22e:** Spatial Index, Renderer-Änderungen

---

## M24a — Worker-Complete-Fast-Path

**Ziel:** Nach M22e redundanten Main-`rebuild_chunk_solid` nach Worker-Apply entfernen; Apply-only für frische prozedurale Chunks.

**Module:**
- [`game_core/worker_fast_path.py`](game_core/worker_fast_path.py) — `is_worker_complete_result`, `can_apply_worker_complete_fast_path`
- [`game_core/world_gen_result.py`](game_core/world_gen_result.py) — `apply_worker_complete_result` (Batch-Deko-Append)
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — deferred Collision nur Slow-Path
- [`game_core/navigation.py`](game_core/navigation.py) — `ensure_collision_fresh_for_coords` (enger Scope)
- [`assets/content/streaming.json`](assets/content/streaming.json) — `max_in_flight_chunks`, `sync_fallback_in_flight_ms`

**Pfadtrennung:** Fast-Path wenn Payload vollständig + keine Override/Delta/Dirty/User-Deko/Pending.

**Tests:** [`tests/test_m24a_fast_path.py`](tests/test_m24a_fast_path.py)

**Bewusst nicht in M24a:** Deko-Spatial-Index, Persistenz v5, Renderer-Umbau

---

## M24b — Terrain/Deco-Pipeline-Split

**Ziel:** Terrain und Deco als getrennte Worker-Stages mit symmetrischen Apply-Verträgen; Deco darf Terrain weder beim Apply noch bei der CPU-Belegung vorauslaufen.

**Ownership (verbindlich):**

| Ressource | Owner |
|-----------|-------|
| `build_epoch` | `BuildCoordinator` / `ChunkGenPool` (einzige Schreibquelle) |
| Ready consume/discard + Stale/Duplicate-Metriken | `ChunkStreamer._route_pool_results` |
| Worker-LRU-Cleanup (Main) | Router bei consume/discard |
| `last_applied_deco_build_key` | `apply_deco_stage` (Single-Writer) |
| `deco_incomplete` | `_mark_pending_unload` / Revive |

**Module:**
- [`game_core/chunk_build.py`](game_core/chunk_build.py) — `BuildKey`, `BuildCoordinator`, `ChunkBuildState`
- [`game_core/chunk_build_guards.py`](game_core/chunk_build_guards.py) — `can_apply_terrain_result`, `can_apply_deco_result`
- [`game_core/chunk_stage.py`](game_core/chunk_stage.py) — Stage-API (`build_*`, `apply_*`, IPC-Results)
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — `submit_terrain` / `submit_deco`, zwei Jobtypen
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Router, Scheduler-Caps, `visible_terrain_pending`
- [`game_core/field_cache_lru.py`](game_core/field_cache_lru.py) — bounded LRU keyed by `BuildKey` (worker-lokal, nie IPC)
- [`game_core/deco_generation.py`](game_core/deco_generation.py) — `CompiledDecoPass`, deterministische `deco_config_version`
- [`assets/content/streaming.json`](assets/content/streaming.json) — `terrain_max_in_flight`, `deco_max_in_flight`, Caps

**Scheduler:** `max_in_flight` zählt submitted + running + ready-but-not-applied; `parallelism_cap` nur laufende Jobs. Solange `visible_terrain_pending > 0`: kein Deco-Prefetch/Backfill.

**M24a-Kompat:** `apply_worker_complete_result` für monolithisches `WORKER_COMPLETE`; Legacy-`poll_ready`-Pfad bei nicht-`ChunkGenPool`-Mocks.

**Tests:** [`tests/test_m24b_pipeline.py`](tests/test_m24b_pipeline.py), [`tests/test_m24b_deco_config.py`](tests/test_m24b_deco_config.py)

**Bewusst nicht in M24b:** zweiter ProcessPool (Phase 4b), `decorations_by_chunk`-Index, Persistenz v5, Renderer-Umbau

---

## M24c — Terrain-Generierung beschleunigen

**Ziel:** `build_terrain_stage` drastisch beschleunigen ohne M24b-Verträge zu brechen.

**Ergebnis (Gate A/D, coord=(1,1)):** `worker_build_terrain_stage` ~22 s → **~1,1 s** (≈20×).

**Phase 0+1 umgesetzt:**
- [`game_core/terrain_gen_profile.py`](game_core/terrain_gen_profile.py) — Sub-Timings, Cost Breakdown
- [`game_core/noise.py`](game_core/noise.py) — Perm-Table-Cache (`get_perm`, `FbmPrecalc.perm`)
- [`game_core/world_gen.py`](game_core/world_gen.py) — `build_terrain_layers_and_field_cache` (Ein-Pass)
- [`game_core/chunk_stage.py`](game_core/chunk_stage.py) — kein doppelter `field_cache`
- [`game_core/world_gen_context.py`](game_core/world_gen_context.py) — `spawn_score()` Session-Cache

**Benchmarks:** [`docs/benchmarks/terrain_m24c.md`](docs/benchmarks/terrain_m24c.md), `python tools/benchmark_single_chunk.py --cost-breakdown`

**Tests:** [`tests/test_m24c_terrain_perf.py`](tests/test_m24c_terrain_perf.py)

**Phase 2–4 (optional):** Noise-Bündelung, Compiled Terrain Runtime, SoA — nur wenn weiterer Hebel nach Breakdown nötig (H3/H5).

**Bewusst nicht in M24c:** M24b-Pipeline-Umbau, Deco/Persistenz/Renderer

---

## M24c.1 — Streaming-E2E & verbleibende Terrain-Hebel

**Ziel:** Lücke Mikro-Benchmark (~1 s) vs. Demo-Hitches (~4 s) schließen.

**Primärmetrik:** `stream_ms` P95 bei Bewegung ≤ 800 ms (nicht nur Mikro-Gate).

**Umgesetzt:**
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — `is_in_flight` symmetrisch zu `in_flight_count` (inkl. READY), `has_pending_result`, `is_deco_in_flight`
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Sync-Fallback-Contract, M24b-Warmup, `sync_fallback_triggered`
- [`game_core/world_gen.py`](game_core/world_gen.py) — H3/H5 (Warp-Reuse, Coast-Grid)
- [`game_core/field_cache_lru.py`](game_core/field_cache_lru.py) — `TerrainStageLRU` für Deco-Fast-Path
- [`tools/benchmark_stream_step.py`](tools/benchmark_stream_step.py) — E2E-Streaming-Benchmark
- [`assets/content/streaming.json`](assets/content/streaming.json) — `sync_fallback_in_flight_ms: 2500`

**Benchmarks:** [`docs/benchmarks/terrain_m24c1.md`](docs/benchmarks/terrain_m24c1.md)

**Tests:** [`tests/test_m24c1_streaming.py`](tests/test_m24c1_streaming.py)

**Diagnose:** Env `WT_STREAM_DIAG=1` in Demo

---

## M24c.2 — Streaming Scheduler & Warm-E2E

**Ziel:** Scheduler/Config so nachziehen, dass Sync-Fallback im Warm-Pfad verschwindet und P95 `stream_ms` ≤ 800 ms.

**Warum nach M24c.1:** Mikro-Worker ~465–917 ms/Chunk, aber E2E P95 ~4523 ms durch alternierendes Sync-Muster (2× `_load_chunk` pro Frame).

**Umgesetzt:**
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Submit-Filter, `_step_submitted_coords`, verschärfter Sync-Contract
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — `submit_chunk_pipeline` (Combined Terrain+Deco)
- [`game_core/world_gen_parallel.py`](game_core/world_gen_parallel.py) — `_generate_chunk_pipeline_task`
- [`assets/content/streaming.json`](assets/content/streaming.json) — M24c.2 Defaults (`pipeline_mode: combined`, `max_sync_applies_per_frame: 0`)
- [`tools/benchmark_stream_step.py`](tools/benchmark_stream_step.py) — `--warmup-steps` / `--measure-steps`, Cold/Warm-Summary

**Gate S4 erreicht (Warm):** P95 ~77 ms, `sync_fallback_triggered: 0`

**Health-Signal:** `deco_applied_total` im Fast-Move-Benchmark oft 0 (Szenario, nicht hartes Gate) — siehe [`docs/benchmarks/terrain_m24c2.md`](docs/benchmarks/terrain_m24c2.md)

**Tests:** [`tests/test_m24c2_streaming.py`](tests/test_m24c2_streaming.py)

**M24c Phase 3–4** (Noise/SoA) erst nach M24c.2 Gate S4.

---

## M23 — Profiling & Runtime-Metriken

**Ziel:** Reproduzierbare CPU-Metriken für Streaming und Bridge-Extract — architekturkonform, versionierter Export, identischer kanonischer Tick für CLI und Demo.

**Module:**
- [`game_core/perf/`](game_core/perf/) — `PerfSession`, Modelle, Hitch-Klassifikation, Aggregation, Export-Schema
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — optionales `StreamStepMetrics` in `update`
- [`assets/content/profiling.json`](assets/content/profiling.json) — Szenarien, Hitch-Schwellen
- [`tools/run_perf_scenario.py`](tools/run_perf_scenario.py), [`tools/profile_frame.py`](tools/profile_frame.py), [`tools/compare_perf_runs.py`](tools/compare_perf_runs.py)
- [`docs/benchmarks/perf/`](docs/benchmarks/perf/) — README, SCHEMA, Run-Artefakte

**Kanonischer Tick:** `frame_ms` = Szenario-Schritt + `streamer.update` + optional Extract — kein GPU/Render/Input/Bewegung.

**Hitch-Tags (geschlossen):** `frame_slow`, `stream_slow`, `load_burst`, `unload_burst` — Schwellen nur aus Config.

**Export:** `schema_version = 1`, Artefakte `manifest.json`, `frames.jsonl`, `hitches.jsonl`, `summary.json` unter `docs/benchmarks/perf/runs/<run_id>/`.

**Demo:** `python -m apps.chunk_world_demo --profile` — HUD-Rolling-Metriken, Export bei Exit.

**Bewusst nicht in M23:**
- GPU-/Vulkan-Profiling
- Ores/Ressourcen (→ M24)
- Allgemeine Telemetrie

---

## M23a — Deferred Unload & Sparse Persistence

**Ziel:** Unload-Spitzen (`stream_unload_ms`) durch budgetierten Main-Thread-Drain eliminieren; Persistenz nur für echte Abweichungen von der deterministischen Baseline.

**Module:**
- [`game_core/pending_unload.py`](game_core/pending_unload.py) — Pending-Queue, Mark/Revive/Drain
- [`game_core/persistenz.py`](game_core/persistenz.py) — PersistenzFlags (entkoppelt von RuntimeDirty)
- [`game_core/chunk_delta.py`](game_core/chunk_delta.py) — TerrainDelta, OverlayDelta-Slot
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Revive vor Load, budgetierter Drain
- [`game_core/streaming_world_io.py`](game_core/streaming_world_io.py) — Save v4 + v3-Migration + Fingerprint
- [`assets/content/streaming.json`](assets/content/streaming.json) — `max_unloads_per_frame`, `max_unload_ms_per_frame`

**Verbindliche Regeln:**
- Unbearbeitete Chunks werden verworfen, nicht gespeichert
- `world.chunks` = nur aktive Runtime-Chunks; Pending = Übergang; Delta-Store = Persistenz
- Revive hat Vorrang vor Delta-Load, Neu-Generierung und Worker-Apply
- Ghost-Deko nach Mark semantisch inaktiv (Render/Kollision/Queries)
- Persistenz folgt nur PersistenzFlags

**Bewusst nicht in M23a:**
- Exploration/Fog/Heatmap (Overlay-Slot only)
- Worker-Mutation von World

---

## M23b — Apply-/Load-Burst-Entschärfung

**Ziel:** Apply-/Load-Spitzen (`stream_apply_ms` am Cap) messbar reduzieren oder über Frames glätten — auf Basis M23-Analyse, ohne Unload-Re-Litigation.

**Module:**
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Apply-Microprofile, deferred Collision, Pool in-flight skip, Sync-Cap
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — `is_in_flight` für Sync-Vermeidung
- [`game_core/perf/models.py`](game_core/perf/models.py) — optionale Apply-Submetriken
- [`game_core/perf/run_analysis/m23b_dod.py`](game_core/perf/run_analysis/m23b_dod.py) — DoD-Checker Apply-Burst-Signatur
- [`assets/content/streaming.json`](assets/content/streaming.json) — `max_applies_per_frame: 2`, `max_sync_applies_per_frame: 2`
- [`tools/analyze_perf_run.py`](tools/analyze_perf_run.py) — M23b DoD im Report

**Verbindliche Regeln:**
- Kein Streaming-Neudesign; Phasen Revive → Load/Apply → Mark → Drain bleiben
- Apply-Submetriken nur additiv unter `schema_version: 1`
- Caps nur über Config, nicht hardcoded
- Vorher/Nachher auf identischen Szenarien (`catchup`, `pan`)

**Bewusst nicht in M23b:**
- Ores/Suppression (→ M24)
- Save v5, Overlay-Implementierung, Worker-Neudesign

---

## M23c — Extract-Optimierung (Tile/Deko)

**Ziel:** `tile_extract_ms` / `deco_extract_ms` im kanonischen Tick messbar senken — nach M23b (Extract-dominant), ohne Streaming/Apply/Unload anzutasten.

**Module:**
- [`bridge/chunk_extractor.py`](bridge/chunk_extractor.py) — Extract-Microprofile, `_materials_for`-Cache, Batch-Hot-Path
- [`bridge/decoration_extractor.py`](bridge/decoration_extractor.py) — optionale Deko-Zähler
- [`game_core/perf/models.py`](game_core/perf/models.py) — `ExtractStepMetrics`, optionale Frame-Subfelder
- [`game_core/perf/run_analysis/extract_kpis.py`](game_core/perf/run_analysis/extract_kpis.py) — Extract-KPIs aus `frames.jsonl`
- [`tools/compare_perf_runs.py`](tools/compare_perf_runs.py) — Extract-Deltas Pre/Post
- [`docs/benchmarks/perf/M23C_BASELINE.md`](docs/benchmarks/perf/M23C_BASELINE.md) — Baseline-Contract

**Verbindliche Regeln:**
- Nur Extract-Phasen (3–4) im kanonischen Tick; `frame_ms`-Definition unverändert
- Extract-Submetriken additiv unter `schema_version: 1`; zero overhead wenn Profiling aus
- Cache-Vertrag: Full-Rebuild bei Miss oder `dirty_chunks`; Cull-only bei Cache-Hit; `invalidate()` ohne Dirty-Flag
- M23b DoD muss auf Post-M23c-Runs grün bleiben

**Bewusst nicht in M23c:**
- Streaming-Policy, Apply-Caps, Unload (M23a/M23b)
- Ores/Suppression (→ M24)
- GPU-Renderer-Umbau

---

## M23d — Chunk-Render-Batching

**Ziel:** Sichtbare Welt über Batch-Registry `(coord, layer_id)` + Cull-Cache statt per-Chunk-Detailpfad als Primärrepräsentation — sublinearere Skalierung bei großem Sichtfeld.

**Module:**
- [`bridge/chunk_extractor.py`](bridge/chunk_extractor.py) — Batch-Registry, Cull-Cache, produktiver Batching-Pfad
- [`game_core/world.py`](game_core/world.py) — `dirty_chunk_layers` für Layer-Granularität
- [`game_core/perf/models.py`](game_core/perf/models.py) — Batching-Submetriken
- [`docs/benchmarks/perf/M23D_BASELINE.md`](docs/benchmarks/perf/M23D_BASELINE.md)

**Verbindliche Regeln:**
- Batch-Einheit `(chunk_coord, layer_id)` — keine globale Welt-Batch-Primärrepräsentation
- Detailpfad (`extract_mode='per_chunk'`) nur Tests
- LOD/Mipmaps **nicht** in M23d
- M23b DoD + M23c Cache-Vertrag + Kostenverschiebungs-Guardrails erhalten

**Bewusst nicht in M23d:**
- LOD / Map-Mode / GPU-Backend
- Streaming, Ores (→ M24)

---

## M23e — Visibility LOD / Map-Mode

**Ziel:** Sichtbarkeitsabhängiges LOD (LOD0/LOD1/LOD2) und expliziter Map-Mode auf dem Extract-Pfad — auf Basis M23c/M23d — für messbare Senkung von `tile_extract_ms`/`frame_ms` bei großem Sichtfeld / Zoom-Out.

**Module:**
- [`bridge/chunk_extractor.py`](bridge/chunk_extractor.py) — LOD-Auswahl, LOD-Registry, Integration M23d-Batching für LOD0
- [`game_core/visibility_lod_config.py`](game_core/visibility_lod_config.py) — Config-Lader
- [`assets/content/visibility_lod.json`](assets/content/visibility_lod.json) — Zoom-Grenzen, Map-Mode
- [`game_core/perf/models.py`](game_core/perf/models.py) — LOD-Submetriken
- [`docs/benchmarks/perf/M23E_BASELINE.md`](docs/benchmarks/perf/M23E_BASELINE.md)

**Verbindliche Regeln:**
- LOD0 = M23d Voll-Detail; LOD1 = chunkgebundene Aggregation; LOD2 = Map-Mode/Overview
- Umschaltung deterministisch aus `zoom` + Config; `map_mode=true` erzwingt LOD2
- Registry-Key `(chunk_coord, layer_id, lod_level)` — keine globale Welt-Primärrepräsentation
- Detailpfad (`extract_mode='per_chunk'`) nur Tests
- M23b DoD + M23c Cache + M23d Batching + Kostenverschiebungs-Guardrails erhalten
- Kein Ores/Suppression (→ M24)

**Bewusst nicht in M23e:**
- Streaming/Apply/Unload/Save-Redesign
- GPU-Renderer-Umbau
- Exploration/Fog/Traffic (→ M25+)

---

## M24 — Ore-Patches & Resource-Deposits

**Ziel:** Prozedural generierte Rohstoff-Vorkommen (Erz, Holz-Cluster, Steinfelder) — data-driven, spatial konsistent, Chunk-Seed-verknüpft.

**Technischer Ansatz:**
- Ore-Patches als Overlay-Tiles (Layer 1) oder als Decoration (Layer 4+) — kein eigenständiger Renderer
- `assets/content/resources.json`: Ressourcentypen, Noise-Skala, Dichte, Min/Max-Patchgröße
- Abbau-Stand (welche Tiles entfernt wurden) persistiert via `persistent_overrides` (M20)
- Kein `OreRenderer` — Overlay-Tiles und Decoration-Sprites über bestehende Pipeline

**Bewusst nicht in M24:**
- Abbau-Mechanik (Gameplay-Logik)
- Inventar-Integration (→ M26)

---

## M25 — Mini-Map / Fog of War

**Ziel:** Kleine Übersichtskarte im HUD zeigt besuchte Chunks; unbesuchte Bereiche ausgeblendet (Fog of War).

**Technischer Ansatz:**
- `game_core/exploration.py` — `ExplorationMap`: besuchte Chunk-Koordinaten als Set
- Bridge liefert `ExplorationData` als Teilfeld von `RenderFrame`
- `render_scene/ui_types.py` — `ExplorationData` (gameplay-neutral)
- Mini-Map als Screen-Space Overlay-Quad (separater Uniform-Buffer, kein eigener Swapchain)

**Bewusst nicht in M25:**
- Vollbild-Karte, Zoom
- Marker / Waypoints

---

## M26 — Inventar & Item-System

**Ziel:** Spieler kann Items aufnehmen und tragen — einfaches Slot-basiertes Inventar, kein UI (→ M28).

**Technischer Ansatz:**
- `game_core/inventory.py` — `Inventory`, `ItemStack`, `ItemId`
- `assets/content/items.json` — Item-Definitionen (Name, Sprite-Key, Max-Stack)
- Inventar gehört zum `Character` — keine Render-Abhängigkeit
- Vollständig in `game_core`; Bridge transportiert ggf. HUD-Daten wenn M28 aktiv

---

## M27 — Entity-System (Grundstruktur)

**Ziel:** Allgemeine Entity-Struktur für NPCs, Feinde, interaktive Objekte — nicht hardcoded, erweiterbar.

**Technischer Ansatz:**
- `game_core/entities.py` — `Entity` (Position, SpriteKey, AnimState, optional: AI-State)
- `World.entities: list[Entity]` — kein spezialisierter Renderer
- Bridge: `entities_to_sprites()` analog zu `character_to_sprite()` — generisch
- Kein ECS-Overhead in M27: einfache Liste + Komponentenfelder reichen

**Bewusst nicht in M27:**
- Vollständiges ECS-Framework
- KI / Pathfinding (Folgemeilenstein)

---

## M28 — UI-Framework (HUD, Labels)

**Ziel:** Einfaches, rendererseitig generisches HUD — Tile-Koordinaten, FPS, Inventar-Anzeige (M26-Daten).

**Technischer Ansatz:**
- `render_graphics/ui_renderer.py` — Quads für UI-Elemente, Textur-basierte Labels
- UI-Elemente in Screen-Space (separater Uniform-Buffer, orthographisch, kein World-Transform)
- `render_scene/ui_types.py` — `UIFrame`, `LabelData`, `UIQuad` — Gameplay-neutral
- Bridge liefert `UIFrame` als Teilfeld von `RenderFrame`

**Bewusst nicht in M28:**
- Vollständiges Widget-System
- Maus-interaktive UI-Elemente (Buttons, Dialoge)

---

## M29 — Audio-System (Grundlagen)

**Ziel:** SFX-Playback für Schritte, Aktionen und Ambient-Sounds — komplett losgelöst vom Render-Pfad.

**Technischer Ansatz:**
- `wt_platform/audio.py` — `AudioSystem`, `play_sfx(sound_id)`, `play_ambient(track_id)`
- Keine Vulkan-Abhängigkeit; unabhängiger Thread oder Event-Queue
- `assets/audio/` — SFX und Ambient-Tracks
- `game_core` sendet `AudioEvent`s, `wt_platform/audio.py` konsumiert sie

**Bewusst nicht in M29:**
- 3D-Positional Audio
- Musik-Streaming oder dynamische Komposition

---

# Architekturkonventionen (gültig ab M6, kumulativ)

## Koordinaten & Tile-Einheiten
- 1 Tile = **32×32 px** Weltkoordinaten
- Sprite-Anker: **unten links** (`world_x/y` in `SpriteInstanceData`)
- Sprite-Keys: **`wt:pfad/zum/sprite`** (Minecraft-Style, stabil über Rebakes)
- **TileId = SpriteId** — Tiles sind 1×1 Atlas-Einträge (`wt:tiles/grass`, …)
- **Chunk `(cx, cy)`** — 8×8 Tiles = 256×256 px, Anker `(cx * 256, cy * 256)`

## Atlas & Sprites
- Atlas-Raster: 32px-Zellen mit 1px Gutter
- Nicht-32px-Vielfache werden in `bake_atlas.py` auf 32px-Raster gepaddet (horizontal zentriert, unten ausgerichtet)
- `sprite_rect_uv` nutzt exakte `pixel_w`/`pixel_h` — kein Gutter-Inset auf Sheet-Breite
- `TEXTURED_INSTANCE_STRIDE = 36` (inkl. Clip-Pack M13b)

## Render-Layer

| LayerId | Inhalt |
|---------|--------|
| 0 | Terrain (Boden) |
| 1 | Overlay (Pfade, Fundamente, Ore-Overlay) |
| 2 | Charakter |
| 3 | (reserviert) |
| 4 | Büsche, Stumps, kleine Decorations |
| 5 | Baum-Stamm |
| 6 | Baum-Krone |
| 7+ | UI / HUD Screen-Space (M27) |

## Upload & Synchronisation
- `FrameStagingUploader` — pro Frame-Slot Staging-Buffer, Copy + Barrier im Frame-CB vor Render-Pass
- Instance-Buffer double-buffered (`MAX_FRAMES_IN_FLIGHT`)
- Kein `vkQueueWaitIdle` im Hot-Path

## Sichtbarkeit & Culling
- Chunk außerhalb Viewport → nicht extrahieren/rendern
- Sichtbarer Chunk → nur Tiles im Viewport in `TileLayerBatch`
- `dirty_chunks`: Tile-Extraktion nur bei geänderten Chunks (M17)

## Streaming & Persistenz
- `persistent_overrides` ∪ `world.dirty_chunks` → schreiben; prozedurale Baseline niemals speichern
- Decorations: nur `procedural=False` im Manifest persistiert
- Solid-Grid nicht gespeichert — nach Load `rebuild_all_solid`

## Y-Sortierung (M13)
```
(-sort_y, layer, world_x)   aufsteigend → Norden zuerst, Süden zuletzt
```

---

# Kerninterfaces (render_scene/)

| Typ | Zweck |
|-----|-------|
| `RenderFrame` | Kompletter Frame-Input pro Draw-Zyklus |
| `CameraData` | Orthographische View-Parameter |
| `TileChunkRenderData` | Sichtbarer Chunk mit Layer-Batches |
| `TileLayerBatch` | SoA-nahe Tile-Instanzen pro Layer |
| `SpriteInstanceData` | Instanzierbares Sprite (Position, ID, Material, Layer) |
| `TextureHandle` / `MaterialHandle` | Typisierte GPU-Ressourcen-IDs |
| `SpriteRect` / `MaterialDescriptor` | UV-Lookup + Material→Atlas |
| `SpriteKey` / `SpriteCatalog` | Minecraft-Style Keys → GPU-SpriteId |
| `TextureAtlasDescriptor` | Atlas-Metadaten inkl. Manifest-Einträge |
| `UIFrame` | Screen-Space UI-Elemente (M27) |
| `ExplorationData` | Besuchte Chunk-Koordinaten für Mini-Map (M25) |

Bridge-Protokoll in `bridge/`:
- `RenderExtractor.extract() -> RenderFrame` — liest Spielzustand, schreibt ihn nicht.

---

# Abhängigkeitsregeln

Maschinenlesbar in `bridge/dependency_rules.py`.

| Modul | Darf importieren von |
|-------|----------------------|
| `wt_platform` | — |
| `render_core` | `wt_platform` |
| `render_graphics` | `render_core`, `render_scene` |
| `render_scene` | — |
| `bridge` | `render_scene`, `game_core` |
| `game_core` | — |

**Niemals:** `render_*` → `game_core`, `game_core` → `render_*`.

---

# GPU-only Policy

Rendering erfolgt **ausschließlich über Vulkan auf der GPU**. Kein CPU-Fallback, kein Software-Rasterizer.  
Erzwingt durch `render_core/policy.py` (`GPU_ONLY = True`, `assert_gpu_only()`).

---

# Frühe Architekturfehler (aktiv vermeiden)

1. **Render/Gameplay vermischen** — kein Gameplay-Code in `render_*`, kein Vulkan in `game_core`.
2. **Spielspezifische Renderer** — kein `PlayerRenderer`, nur generische `SpriteInstanceData`.
3. **Monolith** — keine `engine.py`, die Fenster + Welt + GPU vereint.
4. **Feature-Bloat vor Kern** — gilt für Phase 1; M28/M29 sind gezielt in Phase 3 geplant (siehe Abschnitt „Harte Verbote", Punkt 4).
5. **Game-Objekte an Renderer** — immer über `bridge` → `RenderFrame`.
6. **Verschwendender Vulkan-Umgang** — Command Pools cachen, Pipeline-Binds minimieren, kein per-frame Ressourcen-Chaos.
7. **Swapchain-Extent als CFFI-Referenz** — Extent-Werte kopieren (`extent_size`); vor `vkCreateSwapchainKHR` GLFW-FB und `currentExtent` abgleichen; `oldSwapchain` erst nach erfolgreichem Create zerstören.
8. **Factorio-only APIs** — Chunk-/Tile-Strukturen generisch halten (orthographisch, layerbasiert, instanced).
9. **Terrain-Generierung im Renderer** — `world_gen.py` bleibt vollständig in `game_core`; Noise-Parameter nicht in Shader-Konstanten hardcoden.
10. **Spielspezifische Noise-Konfiguration im Code** — `WorldGenConfig` ist data-driven aus `assets/content/world_gen.json`; kein Hardcode im Generierungscode.

---

# Definition of Done

## Phase 1 — Kern-Renderer ✅
- [x] Modulgrenzen und Ordnerbaum angelegt
- [x] Kerninterfaces in `render_scene/` definiert
- [x] Abhängigkeitsregeln dokumentiert
- [x] Bridge-Protokoll (`RenderExtractor`) skizziert
- [x] Minimaler Vulkan-Renderpfad (GPU Clear)
- [x] Orthographische Kamera + GPU Uniform (M4)
- [x] Instancing für Quads/Tiles (M5)
- [x] Texture Atlas + SpriteRect-Lookup (M6)
- [x] Tile-Layer aus `TileLayerBatch` / `TileChunkRenderData` (M7)
- [x] Chunk-Welt via `game_core` → `bridge` → `RenderFrame` (M8)
- [x] Frame-Staging-Upload ohne per-Frame Command-Pool (M9)
- [x] Mehrere Tile-Layer pro Chunk — Layer 0/1, Draw-Reihenfolge (M9b)
- [x] Mutable Welt — Tiles ändern, Dirty-Chunks (M10)
- [x] Charakter + Spritesheet-Animation Idle/Walk/Run (M11)
- [x] Decoration-Sprites + Content-Registry (M12)
- [x] Data-driven Tile-Pinsel (M12b)
- [x] Y-Sort + Stamm/Krone-Split (M13)
- [x] Kollision / Walkability (M14)
- [x] Pixel-Kollision Masken + Solid-Grid (M15)
- [x] Welt Save/Load JSON (M16)
- [x] Dirty-Chunk-Render-Cache (M17)
- [x] Chunk-Streaming infinite prozedural (M18)
- [x] Fenster-Resize & Vollbild — Swapchain/Surface-Sync (M19)
- [x] Platform-Schale + Streaming-Persistenz (M20)

## Phase 2 — Procedural World 🔄
- [x] Hybrid World-Gen: Noise, Klima, Voronoi-Biome, data-driven (M21)
- [x] Biome-System: Blend L0, Sub-Biom-Noise, ChunkFieldCache (M22)
- [x] Parallel Chunk Gen: ProcessPool, ChunkGenResult, Streaming-Prefetch (M22b)
- [x] FNV Tile-ID IPC: kompakte int-Payload, modding-sichere Keys (M22c)
- [x] Hybrides Chunk-Streaming: Viewport, Safety-Ring, Apply-Budget (M22d)
- [x] Worker-Deko + Worker-Solid: ProcessPool Apply, Golden-Determinismus (M22e)
- [x] Profiling & Runtime-Metriken: kanonischer Tick, Export schema v1 (M23)
- [x] Deferred Unload & Sparse Persistence: Pending-Queue, Save v4 (M23a)
- [x] Apply-/Load-Burst-Entschärfung: Cap-Tuning, Microprofile, DoD-Checker (M23b)
- [x] Extract-Optimierung: Microprofile, Cache-Vertrag, Batch-Hot-Path, Compare-KPIs (M23c)
- [x] Chunk-Render-Batching: Registry, Cull-Cache, Batching-Submetriken (M23d)
- [x] Visibility LOD / Map-Mode: LOD0–LOD2, Config, LOD-Submetriken (M23e)
- [ ] Ore-Patches & Resource-Deposits, über Overlay/Decoration-Pipeline (M24)

## Phase 3 — Gameplay-Kern ⬜
- [ ] Mini-Map / Fog of War, `ExplorationData` in `RenderFrame` (M25)
- [ ] Inventar & Item-System, vollständig in `game_core` (M26)
- [ ] Entity-System Grundstruktur, generisch via Bridge (M27)
- [ ] UI-Framework HUD, Screen-Space in `render_graphics` (M28)
- [ ] Audio-System Grundlagen, in `wt_platform/audio.py` (M29)

---

# Demos

- `python -m apps.gpu_clear_demo` — GPU Clear
- `python -m apps.ortho_camera_demo` — Ortho-Kamera (WASD, +/- Zoom)
- `python -m apps.instance_demo` — Instanced Quads (texturiert via Atlas)
- `python -m apps.atlas_demo` — Texture Atlas (Mix 1×1, 1×3, 2×4 Tiles)
- `python -m apps.tile_layer_demo` — Tile-Layer (3072 Tiles + Dekoration)
- `python -m apps.chunk_world_demo` — Chunk-Welt infinite (Streaming, `--profile` für M23-Metriken, Pinsel `1`/`2`/`3`, Free-Cam `F`, Vollbild `F11`, Save/Load `Ctrl+S`/`Ctrl+L`, Regen `G`)
- `python -m apps.world_gen_debug_demo` — World-Gen Debug-Ansichten (M21–M22, `1`–`0`, `F`, `S`, `T`, `D`)

**Atlas bake:** `python tools/bake_atlas.py --generate-placeholders`  
**Collision bake:** `python tools/bake_collision.py`

Sprites liegen rekursiv unter `assets/sprites/` (z. B. `decoration/trees/oak.png` → Key `wt:decoration/trees/oak`).  
Stabile IDs in `assets/demo_atlas/sprite_registry.json`.
