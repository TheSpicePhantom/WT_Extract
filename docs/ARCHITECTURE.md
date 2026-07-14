# Architektur: WT Extract Rendering Engine

> Grundlage: `ruleset.md` — renderer-first, strikt getrennt von Gameplay.

## 1. Zielarchitektur

Die Engine besteht aus zwei unabhängigen Teilen:

| Teil | Rolle |
|------|--------|
| **Render Engine** | Erzeugt aus neutralen Daten ein Bild (GPU/Vulkan) |
| **Game Engine** | Simulation, Welt, Regeln — kennt kein Vulkan |

**Erlaubter Datenfluss:**

```
game_core  →  bridge  →  render_scene  →  render_graphics  →  render_core  →  wt_platform
```

**Verboten:** Jede Rückwärts- oder Quer-Abhängigkeit (z. B. `render_core → game_core`).

Der Renderer verändert niemals den Spielzustand. Er konsumiert nur `RenderFrame`.

---

## 2. Modulbaum

```
WT_Extract/
├── wt_platform/        # Fenster, Surface, OS-Grundlagen (Name avoids stdlib `platform`)
├── render_core/        # Vulkan: Instance, Device, Swapchain, Sync, Buffer
├── render_graphics/    # Pipelines, Shader, Passes, Kamera, Instancing, Submit
├── render_scene/       # Neutrale Datentypen (RenderFrame, CameraData, …)
├── bridge/             # Game → RenderFrame Extraktion
├── game_core/          # Welt, Chunks, Charakter, Simulation (später)
└── docs/
    └── ARCHITECTURE.md
```

### Verantwortlichkeiten

- **wt_platform/** — Fenstererstellung, Vulkan-Surface, Vollbild (`F11`, borderless), Input-State (`InputState`), FB-Resize-Callbacks. Keine Spielregeln.
- **render_core/** — Low-Level GPU-Infrastruktur (Instance, Device, Swapchain-Lifecycle, Surface-Sync). Kein Wissen über Tiles, Sprites oder Gameplay.
- **render_graphics/** — Mid-Level: orthographische Kamera, Materialien, instanced Quads, Tile-/Sprite-Batches, Render Submission.
- **render_scene/** — Reine Datentypen und Handles. Kein Vulkan, kein Gameplay.
- **bridge/** — Einzige Stelle, an der Spielwelt und Render-Input zusammentreffen.
- **game_core/** — Welt, Chunks, Charakter, Simulation. Keine Render-Imports.

---

## 3. Kerninterfaces

Definiert in `render_scene/`:

| Typ | Zweck |
|-----|--------|
| `RenderFrame` | Kompletter Frame-Input pro Draw-Zyklus |
| `CameraData` | Orthographische View-Parameter |
| `TileChunkRenderData` | Sichtbarer Chunk mit Layer-Batches |
| `TileLayerBatch` | SoA-nahe Tile-Instanzen pro Layer |
| `SpriteInstanceData` | Instanzierbares Sprite (Position, ID, Material, Layer) |
| `TextureHandle` / `MaterialHandle` | Typisierte GPU-Ressourcen-IDs |
| `SpriteRect` / `MaterialDescriptor` | UV-Lookup + Material→Atlas |
| `SpriteKey` / `SpriteCatalog` | Minecraft-Style Keys → GPU-SpriteId |
| `TextureAtlasDescriptor` | Atlas-Metadaten inkl. Manifest-Einträge |

**Konventionen (M6):**
- 1 Tile = 32×32 px Weltkoordinaten
- Sprite-Anker: **unten links** (`world_x/y` in `SpriteInstanceData`)
- Sprite-Keys: **`wt:pfad/zum/sprite`** (Minecraft-Style, stabil über Rebakes)
- **TileId = SpriteId** — Tiles sind 1×1 Atlas-Einträge (`wt:tiles/grass`, …)
- **Chunk `(cx, cy)`** — 8×8 Tiles = 256×256 px, Anker `(cx * 256, cy * 256)`
- **Sichtbarkeit (Bridge):** Chunk außerhalb Viewport → nicht extrahieren/rendern; sichtbarer Chunk → nur Tiles im Viewport in `TileLayerBatch`
- **Upload (M9):** `FrameStagingUploader` — pro Frame-Slot Staging-Buffer, Copy + Barrier im Frame-CB vor Render-Pass; Instance-Buffer double-buffered (`MAX_FRAMES_IN_FLIGHT`)
- **Spritesheet-Animation (M11):** `SpriteInstanceData.sheet_frame_col/row`; Manifest `sheet_cols/rows`; Shader wählt Sub-UV pro Zelle; `TEXTURED_INSTANCE_STRIDE = 36` (inkl. Clip-Pack M13b)
- **Atlas-UV (M11):** `sprite_rect_uv` nutzt exakte `pixel_w`/`pixel_h` — kein Gutter-Inset auf Sheet-Breite (verhindert Frame-Drift bei Animation)
- **Tile-Layer (M9b):** `Chunk.layer_keys` pro `LayerId`; Draw-Reihenfolge via sortierten Instanz-Buffer (ein `vkCmdDraw`); Overlay leer = `""` (nicht gerendert)
- **Decoration (M12):** `World.decorations` → `SpriteInstanceData` via Content-Registry; Render-Layer 4/5
- **Charakter:** Sprite-Layer 2 — Y-sortiert mit Decorations (M13)
- **Y-Sort (M13):** Sprites nach `(-sort_y, layer, world_x)`; Bäume optional Stamm L5 + Krone L6 (Shader-Clip)
- **Walkability (M14):** `ContentRegistry.tile_walkable` / `decoration_blocks`
- **Pixel-Kollision (M15):** Alpha-Masken + 8×8 Chunk-Solid-Grid; Walk-Union 8 Richtungen
- Atlas-Raster: 32px-Zellen mit 1px Gutter

Bridge-Protokoll in `bridge/`:

- `RenderExtractor.extract() -> RenderFrame` — liest Spielzustand, schreibt ihn nicht.

---

## 4. Abhängigkeitsregeln

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

## GPU-only Policy

Rendering erfolgt **ausschließlich über Vulkan auf der GPU**. Kein CPU-Fallback, kein Software-Rasterizer.
Erzwingt durch `render_core/policy.py` (`GPU_ONLY = True`, `assert_gpu_only()`).

---

## 5. Minimaler Entwicklungsplan (Meilensteine)

| # | Meilenstein | Module | Status |
|---|-------------|--------|--------|
| M1 | Projektstruktur + Interfaces | `render_scene`, `bridge`, `docs` | ✓ |
| M2 | Fenster + Vulkan Instance/Device | `wt_platform`, `render_core` | ✓ |
| M3 | Swapchain + erster Clear-Frame | `render_core` | ✓ |
| M4 | Orthographische Kamera | `render_graphics` | ✓ |
| M5 | Instanced Quads (einfarbig) | `render_graphics` | ✓ |
| M6 | Texture Atlas + Material-Handles | `render_graphics`, `render_scene` | ✓ |
| M7 | Erster Tile-Layer aus `TileLayerBatch` | `render_graphics` | ✓ |
| M8 | Chunk-Daten via `TileChunkRenderData` | `render_graphics`, `bridge`, `game_core` | ✓ |
| M9 | Frame-Staging-Upload (kein per-Frame Command Pool / WaitIdle) | `render_core`, `render_graphics` | ✓ |
| M9b | Mehrere Tile-Layer pro Chunk — Draw-Reihenfolge nach `LayerId` | `render_graphics`, `bridge`, `game_core` | ✓ |
| M10 | Mutable Welt — Tiles zur Laufzeit ändern, Dirty-Chunks | `game_core`, `bridge`, `apps` | ✓ |
| M11 | Charakter + Spritesheet-Animation (Idle/Walk/Run, 8-Wege) | `game_core`, `bridge`, `render_graphics`, `apps` | ✓ |
| M12 | Decoration-Sprites + Content-Registry (JSON) | `game_core`, `bridge`, `tools`, `apps` | ✓ |
| M12b | Data-driven Tile-Pinsel (`tiles.json` Brushes) | `game_core`, `apps` | ✓ |
| M13 | Y-Sort + Stamm/Krone-Split (Tiefen-Sortierung) | `render_graphics`, `bridge`, `game_core` | ✓ |
| M14 | Kollision / Walkability (Tiles + Decorations) | `game_core`, `apps` | ✓ |
| M15 | Pixel-Kollision (Masken + 8×8 Solid-Grid) | `game_core`, `tools`, `apps` | ✓ |
| M16 | Welt-Persistenz (Save/Load JSON) | `game_core`, `apps` | ✓ |
| M17 | Dirty-Chunk-Render-Cache | `bridge`, `game_core` | ✓ |
| M18 | Chunk-Streaming (infinite prozedural) | `game_core`, `apps` | ✓ |
| M19 | Fenster-Resize & Vollbild (Swapchain/Surface) | `wt_platform`, `render_core`, `render_graphics`, `apps` | ✓ |
| M20 | Platform-Schale + Streaming-Persistenz | `wt_platform`, `game_core`, `apps` | ✓ |
| M22 | Biome-System (Blend, Sub-Biom, Cache) | `game_core`, `apps` | ✓ |
| M22b | Parallel Chunk Generation | `game_core`, `apps` | ✓ |
| M22c | FNV Tile-ID IPC | `game_core` | ✓ |
| M22d | Hybrides Chunk-Streaming | `game_core`, `apps` | ✓ |
| M22e | Worker-Deko + Worker-Solid | `game_core` | ✓ |
| M23 | Profiling & Runtime-Metriken | `game_core`, `tools`, `apps` | ✓ |
| M23a | Deferred Unload & Sparse Persistence | `game_core`, `apps` | ✓ |
| M23b | Apply-/Load-Burst-Entschärfung | `game_core`, `tools` | ✓ |
| M23c | Extract-Optimierung (Tile/Deko) | `bridge`, `game_core/perf`, `tools` | ✓ |
| M23d | Chunk-Render-Batching | `bridge`, `game_core/perf`, `tools` | ✓ |
| M23e | Visibility LOD / Map-Mode | `bridge`, `game_core`, `assets/content` | ✓ |

### World-Gen Performance

Benchmarks: [`docs/benchmarks/world_gen_m22b.md`](docs/benchmarks/world_gen_m22b.md) — `python tools/benchmark_world_gen.py --label baseline|parallel --compare`

### Runtime Performance (M23)

Benchmarks: [`docs/benchmarks/perf/README.md`](docs/benchmarks/perf/README.md) — `python tools/run_perf_scenario.py --scenario steady`

### M21 — Hybrid World-Gen (Noise, Klima, Voronoi-Biome)

**Ziel:** Deterministische, unendliche Welt aus globalen Feldern — Height/Wasser, Klima, Voronoi-Regionen mit Warp/Blend, biomabhängige Tiles und Decorations. Spec: [`milestones_detailed/world-gen.md`](milestones_detailed/world-gen.md).

**Module (`game_core/`):**
- [`game_core/noise.py`](game_core/noise.py) — 2D-Simplex, fBM, Domain Warp (eigene Impl., keine Extra-Dep)
- [`game_core/biomes.py`](game_core/biomes.py) — `BiomeId`, `ClimateClass`, `WaterClass`; Mapping aus JSON
- [`game_core/world_gen.py`](game_core/world_gen.py) — `WorldGenConfig`, `sample_climate`, `sample_biome_region`, `resolve_tile`, `generate_chunk`, `populate_chunk_decorations`, Startgebiet-Regeln

**Config (data-driven):**
- [`assets/content/world_gen.json`](assets/content/world_gen.json) — Noise-, Wasser-, Biom-, Startgebiet-Parameter, `world_seed`
- [`assets/content/biomes.json`](assets/content/biomes.json) — Klimaklassen, Biom→Tile/Decoration-Mapping
- Neue Tiles: `deep_water`, `shallow_water`, `sand`, `snow` in [`assets/content/tiles.json`](assets/content/tiles.json)

**Datenfluss:** Welt-Tile `(wx, wy)` → `ClimateSample` → Wasserklassifikation → Voronoi-Region (3×3, optional Warp, `blend_t`) → `BiomeId` → `Chunk.layer_keys` L0/L1. Renderer/Bridge unverändert.

**Streaming:** Save v3 in [`game_core/streaming_world_io.py`](game_core/streaming_world_io.py) — `world_seed` im Manifest; Load ruft `configure_world_gen()`. `persistent_overrides` weiterhin Vorrang; `chunk_differs_from_baseline()` nutzt `generate_chunk()`.

**Demos:**
- [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py) — prozedurales Terrain, `G` = neuer Seed (Overrides bleiben)
- [`apps/world_gen_debug_demo.py`](apps/world_gen_debug_demo.py) — Modi Height/Water/Temp/Moisture/Voronoi/FinalBiome/SubBiome/Terrain/Decorations (`1`–`0`, `F`, `S`, `T`, `D`)

**Bewusst nicht in M21:** Rivers/Hydrologie, Ore/Ressourcen, GPU-Noise, async Worldgen-Jobs.

### M22 — Biome-System (Feinschliff)

**Ziel:** Sichtbare Biom-Übergänge auf Layer 0, feine Variation innerhalb Voronoi-Zellen, Performance-Cache pro Chunk, Spawn-Qualität.

**Erweiterungen:**
- [`game_core/biomes.py`](game_core/biomes.py) — `resolve_blended_layer0`, `pick_biome_variant`, `decorations_for_blend_zone`, `blended_decoration_density`; `biomes.json` → `blend.transitions`
- [`game_core/world_gen.py`](game_core/world_gen.py) — `ChunkFieldCache`, `build_chunk_field_cache`, `resolve_tile_cached`, `sample_sub_biome`, `score_spawn_area`, `ensure_playable_seed`
- [`assets/content/world_gen.json`](assets/content/world_gen.json) — `sub_biome`, `start_area.min_score` / `sample_grid_radius` / `max_seed_attempts`

**Datenfluss (M22):** Pro Chunk einmal `build_chunk_field_cache` (8×8 Klima + Region) → `resolve_tile_cached` pro Tile → optional `resolve_blended_layer0` (Land) → Deko via `decorations_for_blend_zone`.

**Demos:** `chunk_world_demo` — `G` nutzt `ensure_playable_seed`, Titel mit Spawn-Score; `world_gen_debug_demo` — `D` lädt prozedurale Decorations on top of Terrain.

**Bewusst nicht in M22:** Rivers/Hydrologie, Ore/Ressourcen (→ M24), GPU-Noise, async Worldgen.

### M22b — Parallel Chunk Generation

**Ziel:** Terrain parallel erzeugen; IPC via kompaktes `ChunkGenResult` (`layer0`/`layer1` als int-Tuples seit M22c, `decorations=None`); Deko/Solid nur Main-Thread.

**Module:**
- [`game_core/world_gen_context.py`](game_core/world_gen_context.py), [`game_core/world_gen_result.py`](game_core/world_gen_result.py)
- [`game_core/world_gen_parallel.py`](game_core/world_gen_parallel.py) — Batch + langlebiger `ProcessPoolExecutor`
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — Prefetch in [`ChunkStreamer`](game_core/chunk_streaming.py), discard-on-arrival
- [`game_core/content_registry.py`](game_core/content_registry.py) — `tile_key_to_id` / `tile_id_to_key`

**Datenflug:** Worker → `ChunkGenResult` (FNV Tile-IDs) → Main: `chunk_from_result(result, content)` → `populate_chunk_decorations` → `rebuild_chunk_solid`

**Performance:** [`docs/benchmarks/world_gen_m22b.md`](docs/benchmarks/world_gen_m22b.md) — `demo_world_16x16` ~8× schneller (parallel vs. sequentiell)

**Bewusst nicht in M22b:** Worker-Deko, hartes Task-Cancel

### M22c — FNV Tile-ID IPC

- [`game_core/tile_ids.py`](game_core/tile_ids.py) — `stable_tile_id` (FNV-1a 32-bit), `EMPTY_TILE_ID=0` für Overlay-Leerfeld
- Worker: `stable_tile_id(key)` ohne ContentRegistry; Main: `tile_id_to_key` aus Registry-Reverse-Map (Kollisions-Assert beim Laden)
- Modding: content-addressable IDs — `mymod:tiles/foo` unabhängig von JSON-Reihenfolge

### M22d — Hybrides Chunk-Streaming

**Ziel:** Statt fixem Chebyshev-Radius (`load_radius=8` → ~289 Chunks) lädt der Streamer nur Viewport-relevante Chunks plus Safety-Ring um den Spieler; Prefetch in Bewegungsrichtung; `max_applies_per_frame` begrenzt Main-Thread-Applies.

**Datenfluss:**
1. Demo/Profiler baut `StreamViewParams` (Fokus, Spieler, Zoom, Viewport-Pixel, Bewegungsdelta)
2. [`game_core/stream_view.py`](game_core/stream_view.py) — `compute_stream_sets` → `wanted`, `keep`, `prefetch`
3. [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Load/Unload/Prefetch; bei aktivem `ChunkGenPool` kein Sync-`generate_chunk` wenn Budget erschöpft
4. [`bridge/visibility.py`](bridge/visibility.py) — `camera_world_bounds` delegiert an `game_core.stream_view` (DRY)

**Config:** [`assets/content/streaming.json`](assets/content/streaming.json) via [`game_core/streaming_config.py`](game_core/streaming_config.py). `mode: radius` für Legacy-Tests und reproduzierbare Benchmarks.

**Bewusst nicht in M22d:** Decoration-Spatial-Index, Renderer-Änderungen

### M22e — Worker-Deko + Worker-Solid

**Ziel:** Apply-Pfad entlasten — Worker liefert `WORKER_COMPLETE`-Results (Terrain + IPC-Deko + Solid-Bytes); Main-Thread übernimmt Daten per Fast-Path.

**Datenfluss:**
1. Worker: `generate_chunk_result` → `compute_procedural_decorations` + `build_chunk_solid_grid`
2. Main (Fast-Path): `apply_worker_complete_result` — Chunk, Deko-Batch, `solid_grid` direkt übernehmen
3. Main (Slow-Path): `_ensure_procedural_decorations` + deferred `rebuild_chunk_solid`
4. Golden: `sequential_reference_chunk` in Tests

**Config:** `parallel.worker_apply` in [`assets/content/world_gen.json`](assets/content/world_gen.json)

### M24a — Worker-Complete-Fast-Path

**Ziel:** Redundanten Main-Rebuild nach Worker-Apply entfernen; Predicates in [`game_core/worker_fast_path.py`](game_core/worker_fast_path.py).

**Regel:** Wenn `can_apply_worker_complete_fast_path(...)` → kein `_flush_deferred_collisions` für diese Coord.

**Bewusst nicht in M24a:** `decorations_by_chunk`-Index, Persistenz v5, Renderer-Umbau

### M24b — Terrain/Deco-Pipeline-Split

**Ziel:** Getrennte Terrain- und Deco-Worker-Stages mit `BuildKey`/`build_epoch`, symmetrischen Guards und Router-owned Ready/Discard.

**Ownership:**
- `build_epoch` — nur `BuildCoordinator` in `ChunkGenPool` (`bump_epoch` bei Pool-Reset/Reinit)
- `terrain_revision` — bei `submit_terrain`, nicht bei Apply
- Ready-Queues, Discard, `terrain_discarded_stale` / `deco_discarded_stale` / `deco_discarded_duplicate` — `_route_pool_results`
- `ChunkFieldCache` — worker-lokal in LRU; nie in IPC-Results
- `last_applied_deco_build_key` — kanonische Duplicate-Quelle (nicht `deco_state == APPLIED`)

**Pipeline:** `build_terrain_stage` → `TerrainResult` (IPC) → `apply_terrain_stage` → `build_deco_stage` → `DecoResult` (IPC) → `apply_deco_stage`. Apply-Funktionen discarden nie — nur der Router.

**Scheduler-Beispiel:** `terrain_max_in_flight=8`, `terrain_parallelism_cap=6`, 6 Jobs laufen + 2 Results in Ready → `in_flight=8`, keine weiteren Submits.

**`deco_incomplete`:** Terrain-only nach Unload/Revive; keine prozedurale Deco-Rekonstruktion aus Snapshot; erst `apply_deco_stage` hebt den Zustand auf.

**Config:** [`assets/content/streaming.json`](assets/content/streaming.json) — separate Terrain/Deco-Caps, `deco_pause_when_visible_terrain_pending`

**Tests:** [`tests/test_m24b_pipeline.py`](tests/test_m24b_pipeline.py) (9 Failure-Modes), [`tests/test_m24b_deco_config.py`](tests/test_m24b_deco_config.py) (Determinismus)

**Bewusst nicht in M24b:** zweiter ProcessPool (4b), Persistenz v5, Renderer-Umbau

### M24c — Terrain-Generierung beschleunigen

**Ziel:** Worker-/Sync-Worldgen-Hotpath — `build_terrain_stage` von ~22 s auf ~1 s (coord=(1,1)).

**Phase 0:** [`game_core/terrain_gen_profile.py`](game_core/terrain_gen_profile.py) — Cost Breakdown (`WT_TERRAIN_PROFILE` / `begin_profile`)

**Phase 1 Quick Wins:**
- Ein-Pass: `build_terrain_layers_and_field_cache` — ein `field_cache`, keine Doppel-Generierung
- Perm-Cache in [`game_core/noise.py`](game_core/noise.py) — `_build_perm` nicht mehr pro Simplex-Sample
- `WorldGenContext.spawn_score()` — einmal pro Chunk-Session

**M24b-Vertrag:** `TerrainResult` IPC, `ChunkFieldCache` worker-lokal, Guards/Router unverändert.

**Benchmark:** `python tools/benchmark_single_chunk.py --cost-breakdown` → [`docs/benchmarks/terrain_m24c.md`](docs/benchmarks/terrain_m24c.md)

### M24c.1 — Streaming-E2E

**Ziel:** Demo-`stream_ms` P95 ≤ 800 ms — kein 4-Sekunden-Hitch trotz Mikro-Speedup.

**Phase 1 Streaming-Fixes:** `is_in_flight` inkl. `READY`, `has_pending_result`, Warmup Terrain+Deco, `sync_fallback_in_flight_ms: 2500`

**Phase 2 Terrain:** H3 Warp-Reuse/Seed-Klima-Cache, H5 Coast aus Height-Grid

**Phase 3 Deco:** `TerrainStageLRU` — kein `generate_terrain_layers` bei LRU-Hit

**E2E-Benchmark:** `python tools/benchmark_stream_step.py` → [`docs/benchmarks/terrain_m24c1.md`](docs/benchmarks/terrain_m24c1.md)

**Tests:** [`tests/test_m24c1_streaming.py`](tests/test_m24c1_streaming.py)

**Diagnose:** `WT_STREAM_DIAG=1` in `chunk_world_demo` — loggt `terrain_applied`, `deco_applied`, `sync_ms`, `sync_fallback`

### M24c.2 — Streaming Scheduler & Warm-E2E

**Ziel:** Warm-Pfad ohne Sync-Fallback; P95 `stream_ms` ≤ 800 ms.

**Umgesetzt:**
- Submit-Listen-Filter (Bug S2), `sync_fallback_only_when_pool_disabled`, `max_sync_applies_per_frame: 0`
- `pipeline_mode: combined` — `submit_chunk_pipeline` / `_generate_chunk_pipeline_task`
- Warm/Cold-Benchmark-Split in [`tools/benchmark_stream_step.py`](tools/benchmark_stream_step.py)

**Ergebnis Warm (100 Steps):** P95 **~77 ms**, `sync_fallback_triggered_total: 0`, `apply_sync_generate_ms_total: 0`

**Benchmarks:** [`docs/benchmarks/terrain_m24c2.md`](docs/benchmarks/terrain_m24c2.md), [`docs/benchmarks/baselines/stream_step_warm_m24c2.json`](docs/benchmarks/baselines/stream_step_warm_m24c2.json)

**Tests:** [`tests/test_m24c2_streaming.py`](tests/test_m24c2_streaming.py)

### M23 — Profiling & Runtime-Metriken

**Ziel:** Reproduzierbare CPU-Metriken — kanonischer Tick für CLI und Demo, versionierter JSON-Export, deterministische Hitch-Klassifikation.

**Module (`game_core/perf/`):**
- [`game_core/perf/session.py`](game_core/perf/session.py) — `PerfSession.run_canonical_tick`, Warmup-Trennung, Flush
- [`game_core/perf/hitch.py`](game_core/perf/hitch.py) — geschlossene Hitch-Tags, Config-Schwellen
- [`game_core/perf/export_schema.py`](game_core/perf/export_schema.py) — `schema_version = 1`, Pflichtfeld-Validierung
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — `update(..., step_metrics=None)` ohne Overhead wenn deaktiviert

**Datenfluss:**
1. Szenario-Runner / Demo berechnet Fokus/View
2. `PerfSession.run_canonical_tick` — Szenario + Stream + optional Extract
3. Export nach `docs/benchmarks/perf/runs/<run_id>/`

**Tools:** [`tools/run_perf_scenario.py`](tools/run_perf_scenario.py), [`tools/compare_perf_runs.py`](tools/compare_perf_runs.py)

**Config:** [`assets/content/profiling.json`](assets/content/profiling.json)

**Bewusst nicht in M23:** GPU-Profiling, Ores (→ M24), Telemetrie

### Kanonischer Tick und Load-/Apply-Pfad

#### Frame-Definition

Ein **Profiling-Frame** ist die CPU-Tick-Iteration von `PerfSession.begin_tick()` bis `PerfSession.end_tick()`.

Er umfasst genau diese Phasen in **fester Reihenfolge**:

1. **Szenario-Schritt** — Fokus, Zoom, Bewegungsdelta, `StreamViewParams`
2. **`ChunkStreamer.update()`** — Streaming, Revive, Load/Apply, Unload
3. **Deko-Extract** — `decorations_to_sprites`
4. **Tile-Extract** — `ChunkRenderExtractor.extract`

`frame_ms` misst ausschließlich diesen kanonischen Tick. GPU-Render, VSync, HUD und sonstige Gameplay-Logik liegen **außerhalb** von `frame_ms`.

#### Reihenfolge im Streaming-Schritt

Der Load-/Apply-Pfad liegt vollständig in [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) (`ChunkStreamer.update()`) und folgt einer bindenden Reihenfolge, die durch M23a/M23b festgelegt ist:

**Revive → Load/Apply → Mark → Drain**

##### Ablauf pro Frame

**1. Stream-Sets berechnen**

`compute_stream_sets()` bestimmt aus Viewport und Streaming-Config die Sets `wanted`, `keep` und `prefetch`.

Die Konfiguration (z. B. `max_applies_per_frame`, `max_sync_applies_per_frame`) kommt aus [`assets/content/streaming.json`](assets/content/streaming.json) und ist die Single Source für das Apply- und Unload-Budget.

**2. Revive aus Pending-Unload (schnellster Pfad)**

Für Koordinaten, die sowohl in `wanted` als auch in der Pending-Queue liegen, wird zuerst `_revive_pending(world, coord)` ausgeführt.

Der Snapshot wandert zurück nach `world.chunks` — ohne Neu-Generierung, ohne Worker-Apply und **außerhalb** des Apply-Budgets.

Regel: Eine revive-fähige Koordinate wird **niemals** im selben Frame neu generiert oder per Worker-Apply geladen.

**3. Worker-Apply (Pool, vorbereitete Ergebnisse)**

- `pool.poll_ready()` holt fertige `ChunkGenResult`-Objekte. Für jede passende Coord wird — solange das Apply-Budget nicht erschöpft ist — `_apply_chunk_from_result(..., defer_collision=True)` ausgeführt.
- Wenn `_should_use_worker_apply(...)` erfüllt ist, läuft `apply_worker_complete_result(...)` (Metrik: `apply_worker_ms`) — **ohne** deferred Collision-Rebuild (M24a).
- Andernfalls wird der Chunk aus dem Result aufgebaut, nach `world.chunks` gelegt und prozedurale Deko ergänzt (Metrik: `apply_sync_generate_ms`).
- Danach werden fehlende `wanted`- und `prefetch`-Coords via `pool.submit(...)` an den Worker übergeben (budgetiert via `max_in_flight_chunks`). Sync-Fallback nach `sync_fallback_in_flight_ms` wenn Worker zu lange braucht.

**4. Sync-Load (Main-Thread-Fallback)**

Für verbleibende `wanted`-Coords, die nicht bereits geladen, pending oder in-flight sind, wird der Sync-Pfad ausgeführt — sortiert nach Fokusnähe (Chebyshev-Distanz).

`_load_chunk(..., defer_collision=True)` wählt eine der drei Datenquellen:

| Quelle | Pfad | Metrik |
|--------|------|--------|
| Terrain-Delta | `persistent_deltas` → `generate_chunk` + `apply_terrain_delta` | `apply_delta_ms` |
| Override | `persistent_overrides` → `copy_chunk` | `apply_override_ms` |
| Baseline | `generate_chunk` | `apply_sync_generate_ms` |

Anschließend wird der Chunk semantisch aktiv gesetzt und mit prozeduraler Deko versehen.

**5. Deferred Collision-Flush (Slow-Path only, M24a)**

Nur Slow-Path-Koordinaten landen in `deferred_collision_coords`. Worker-Complete-Fast-Path überspringt den Flush — `solid_grid` kommt vom Worker.

Am Ende des Apply-Blocks verarbeitet `_flush_deferred_collisions(...)` die gesammelten Slow-Path-Coords via `world.rebuild_chunk_solid(...)` (Metrik: `apply_collision_ms`).

**6. Mark Unload (nach Apply)**

Nach dem Load-/Apply-Schritt werden aus `world.chunks` alle Chunks entfernt, die nicht mehr in `keep` liegen.

`_mark_pending_unload(world, coord, extractor)`:

- entfernt den Chunk aus `world.chunks`
- legt einen Snapshot in der Pending-Queue ab
- invalidiert den Extract-Cache (`extractor.invalidate(coord)`)
- setzt `PersistenzFlags` für spätere Delta-Berechnung

**7. Drain Pending-Unload (budgetierter Unload)**

`_drain_pending(max_count=..., max_ms=..., ...)` verarbeitet Pending-Einträge und führt je nach `PersistenzFlags` entweder Terrain-Delta-Persistenz oder Verwerfen unveränderter Chunks aus.

Budget: `max_unloads_per_frame` (Chunkanzahl) und `max_unload_ms_per_frame` (Zeit) — beide aus `streaming.json`.

#### Budget und Metriken

| Cap | Wirkung |
|-----|---------|
| `max_applies_per_frame` | Begrenzt Applies pro Frame; Worker-Apply und Sync-Load teilen sich dieses Budget |
| `max_sync_applies_per_frame` | Begrenzt zusätzlich die Anzahl der Sync-Loads |
| `max_unloads_per_frame` / `max_unload_ms_per_frame` | Begrenzen den Unload-Drain |

Die Microprofile-Felder in `StreamStepMetrics`:

- `apply_worker_ms`
- `apply_sync_generate_ms`
- `apply_delta_ms`
- `apply_override_ms`
- `apply_pool_ms`
- `apply_collision_ms`

Ihre Summe entspricht näherungsweise `stream_apply_ms`. Unload-Zeit wird separat als `stream_unload_ms` gemessen.

#### Abgrenzung zu Extract und zu M23c/M23d

- Load/Apply läuft **vollständig vor** Deko-Extract und Tile-Extract.
- Unload invalidiert den Extract-Cache chunkweise; der Extract-Pfad bleibt zustandsbasiert (`dirty_chunks`, Cache-Hits/Misses, Registry/Cull-Cache) — **nicht** streaminggesteuert.
- **M23b** darf nur Kosten und Burst-Verteilung innerhalb dieses Load-/Apply-Ablaufs optimieren, ohne die Reihenfolge oder die M23-Streaming-Architektur zu verändern.
- **M23c**, **M23d** und **M23e** arbeiten ausschließlich am sichtbarkeitsabhängigen Extract-/Darstellungspfad (`deco_extract_ms`, `tile_extract_ms`) und lassen `ChunkStreamer.update()` sowie die M23b-Caps unangetastet.

### M23a — Deferred Unload & Sparse Persistence

**Ziel:** Budgetierter Unload-Drain statt synchroner Massen-Entladung; sparse Terrain-Deltas statt Full-Chunk-Kopien.

**Datenfluss:**
1. `update`: Revive → Load → Mark (aus `keep`) → budgetierter Drain
2. Pending hält Snapshot; semantisch inaktiv bis Revive oder Drain
3. Drain: unmodified → discard; modified → `persistent_deltas`
4. Save v4: nur Delta-Koordinaten + `world_gen_fingerprint`

**Module:** `pending_unload.py`, `persistenz.py`, `chunk_delta.py`, Save v4 in `streaming_world_io.py`

**Bewusst nicht in M23a:** Overlay-Features, Worker-Mutation

### M23b — Apply-/Load-Burst-Entschärfung

**Ziel:** Monolithische 4er-Apply-Bursts eliminieren; Apply-Kosten lokalisieren und glätten.

**Hebel:**
1. Apply-Submetriken (`apply_worker_ms`, `apply_sync_generate_ms`, …) — additiv in Export
2. Deferred Collision-Rebuild + Pool in-flight skip — weniger Sync-Doppelarbeit
3. `max_applies_per_frame: 2`, `max_sync_applies_per_frame: 2` in Config
4. M23b DoD-Checker in Run-Analyse

**Baseline:** [`docs/benchmarks/perf/M23B_BASELINE.md`](benchmarks/perf/M23B_BASELINE.md)

**Bewusst nicht in M23b:** Ores (→ M24), Streaming-Redesign

### M23c — Extract-Optimierung (Tile/Deko)

**Ziel:** Nach M23b ist Extract der dominante CPU-Block; `tile_extract_ms` / `deco_extract_ms` messbar senken.

**Hebel:**
1. `ExtractStepMetrics` — Cache-Hits/Misses, Full-Rebuild-ms, Cull-ms (additiv in Export)
2. Cache-/Dirty-Vertrag dokumentiert und getestet (Full-Rebuild nur bei Miss oder `dirty_chunks`)
3. `_build_full_layer_batch` — `_materials_for`-Cache, Hot-Loop-Optimierungen
4. `compare_perf_runs.py` — Extract-KPIs aus `frames.jsonl`

**Baseline:** [`docs/benchmarks/perf/M23C_BASELINE.md`](benchmarks/perf/M23C_BASELINE.md)

**Bewusst nicht in M23c:** Streaming/Apply/Unload (M23a/M23b), Ores (→ M24), GPU-Renderer

### M23d — Chunk-Render-Batching

**Ziel:** Sichtbare Welt primär als vorbereitete `(chunk_coord, layer_id)`-Batches + Cull-Cache — weniger per-Frame-Detailarbeit bei großem Sichtfeld.

**Hebel:**
1. Batch-Registry + `_registry_empty` für leere Overlay-Layer
2. Cull-Cache keyed by `tile_range` — Pan/Zoom ohne Full-Rebuild
3. Batching-Submetriken (`tile_registry_hits`, `tile_cull_cache_hits`, …)
4. Legacy-Pfad nur `extract_mode='per_chunk'` (Tests)

**Baseline:** [`docs/benchmarks/perf/M23D_BASELINE.md`](benchmarks/perf/M23D_BASELINE.md)

**Bewusst nicht in M23d:** LOD/Mipmaps (→ M23e), GPU-Packing, Streaming, Ores (→ M24)

### M23e — Visibility LOD / Map-Mode

**Ziel:** Sichtbarkeitsabhängige LOD-Repräsentation LOD0–LOD2 für große Sichtfelder; expliziter Map-Mode erzwingt LOD2.

**Hebel:**
1. LOD-Registry keyed by `(chunk_coord, layer_id, lod_level)` — keine globale Welt-Primärrepräsentation
2. Deterministische LOD-Auswahl aus `zoom` + [`assets/content/visibility_lod.json`](../assets/content/visibility_lod.json); `map_mode=true` → LOD2
3. LOD0 = M23d Voll-Detail; LOD1 = 2×2-Subsample; LOD2 = dominantes Tile pro Chunk-Layer
4. LOD-Submetriken (`tile_lod0_groups`, `tile_lod*_ms`, `tile_lod_switches`, `tile_map_mode_active`) — additiv in Export
5. Detailpfad nur `extract_mode='per_chunk'` oder `lod_mode='detail_only'` (Tests/Debug)

**Baseline:** [`docs/benchmarks/perf/M23E_BASELINE.md`](benchmarks/perf/M23E_BASELINE.md)

**M23b + M23c + M23d + M23e = M23-CPU-/Extract-Basis vor M24-Ores.**

**Bewusst nicht in M23e:** Ores/Suppression (→ M24), GPU-Renderer, Streaming/Apply/Unload, globale Welt-Batch-Primärrepräsentation

### M20 — Platform-Schale + Streaming-Persistenz

**Ziel:** Zentraler Input/Resize in `wt_platform/`; Save/Load für infinite Streaming-Welt — nur geänderte Chunks persistieren, prozedurale Baseline für den Rest.

**Platform-Schale (`wt_platform/`):**
- [`wt_platform/input.py`](wt_platform/input.py) — `InputState`, `InputFrame`, `key_held`/`key_pressed`/`ctrl_combo_pressed`
- [`wt_platform/window.py`](wt_platform/window.py) — `on_framebuffer_resized()`, `set_window_title()`, `request_close()`

**Streaming-Persistenz (`game_core/`):**
- [`game_core/streaming_world_io.py`](game_core/streaming_world_io.py) — Save v2: `saves/streaming_world/manifest.json` + `chunks/cx_cy.json`
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — `persistent_overrides`, `_flush_modified_chunk` beim Unload, Override vor `generate_chunk`; Baseline-Vergleich via `chunk_differs_from_baseline`
- [`game_core/decorations.py`](game_core/decorations.py) — `PlacedDecoration.procedural`; prozedurale Deko wird beim Unload entfernt, User-Deko bleibt global
- [`game_core/world.py`](game_core/world.py) — `copy_chunk()` für Override-Cache

**Save-Modell:**
- Nur Chunks in `persistent_overrides` ∪ `world.dirty_chunks` (geladen) werden geschrieben
- Decorations: nur `procedural=False` in manifest
- Solid-Grid nicht gespeichert — nach Load `rebuild_all_solid`
- M16 [`world_io.py`](game_core/world_io.py) bleibt für Fixed-World (`STREAMING_MODE=False`)

**Demo (`chunk_world_demo`):** kein direktes `import glfw`; `Ctrl+S`/`Ctrl+L` → `DEFAULT_STREAMING_SAVE_DIR`

**Bewusst nicht in M20:** Async I/O, binäres Format, Migration aller Demos auf `InputState`, Input-Hot-Reload.

---

### M19 — Fenster-Resize & Vollbild

**Ziel:** Wechsel zwischen Fenster- und Vollbildmodus sowie Resize (Maximieren, HiDPI) ohne Absturz oder schwarzen Bildschirm.

**Runtime:**
- [`wt_platform/window.py`](wt_platform/window.py) — `toggle_fullscreen()` (borderless auf Primärmonitor), `_wait_for_framebuffer_stable()` (GLFW-Poll bis FB-Größe stabil)
- [`render_core/gpu_renderer.py`](render_core/gpu_renderer.py) — `_needs_swapchain_recreate()`, `_resolve_swapchain_size()` (GLFW-FB ↔ Vulkan `currentExtent`), `_recreate_swapchain()` mit korrekter `oldSwapchain`-Reihenfolge
- [`render_core/swapchain.py`](render_core/swapchain.py) — Extent als `(width, height)`-Tuple (`extent_size`); ungültige `0×0`-Extents ablehnen; frisches `VkExtent2D` nur für Vulkan-Calls
- [`render_graphics/ortho_renderer.py`](render_graphics/ortho_renderer.py) — `handle_surface_resize()`, Pipeline-Rebind nach Swapchain-Wechsel, Draw-Retry (max. 8 + Fallback-Draw)

**Ablauf bei Größenänderung:**
1. Framebuffers zerstören → neue Swapchain mit gültigem `oldSwapchain`-Handle → alte Swapchain zerstören
2. Render-Pass + Framebuffers neu → Pipelines neu binden (Render-Pass-Handle wechselt)
3. Kamera-Viewport aus aktuellem `framebuffer_size` (nicht stale Werte vom Frame-Anfang)

**Behobene Fehler:**
- Falsche Destroy-Reihenfolge → Crash beim Vollbildwechsel (Exit `-1073740791`)
- CFFI-Alias: gespeichertes `VkExtent2D` nach `vkCreateSwapchainKHR` ungültig → Extent `0×0` → schwarzer Bildschirm
- Race: Surface meldet kurz `currentExtent=(0,0)` während Transition
- Demo: Kamera vor `F11` berechnet → falscher Viewport nach Vollbild

**Demo (`chunk_world_demo`):** `F11` = Vollbild; FB-Resize-Callback → Swapchain-Rebuild (M20).

**Bewusst nicht in M19:** Multi-Monitor-Auswahl, exklusiver Fullscreen-Modus.

---

### M18 — Chunk-Streaming

**Ziel:** Infinite prozedurale Welt — nur Chunks im Radius um Spieler/Kamera im RAM; Load/Unload mit M17-Cache und M15-Kollision.

**Runtime:**
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — `ChunkStreamer`, hybrid (`compute_stream_sets`) oder radius fallback; `focus_to_chunk`
- [`game_core/world_gen.py`](game_core/world_gen.py) — `populate_chunk_decorations`, `remove_decorations_in_chunk` (deterministisch via `_chunk_seed`)
- Default: `load_radius=8`, `unload_radius=10` (Hysterese)

**Ablauf:** `generate_chunk` → `rebuild_chunk_solid` → Decorations → bei Unload: Decorations entfernen, `extractor.invalidate(coord)`

**Demo:** Leere `World()`, Spawn `(256,256)`, `streamer.update` pro Frame vor Bewegung. Save/Load deaktiviert (`stderr`-Hinweis).

**Bewusst nicht in M18:** Fixed-World-Toggle, async Loading. (Chunked Save → M20)

---

### M17 — Dirty-Chunk-Render-Cache

**Ziel:** `World.dirty_chunks` in der Bridge nutzen — Tile-Extraktion nur bei geänderten Chunks, nicht jedes Frame für alle sichtbaren.

**Cache:** [`bridge/chunk_extractor.py`](bridge/chunk_extractor.py)
- `_tile_cache: dict[(cx,cy), TileChunkRenderData]` — voller 8×8-Chunk (kamera-unabhängig)
- Cache-Hit + nicht dirty → `_cull_chunk_to_camera()` (View-Culling pro Frame)
- Dirty oder Cache-Miss → `_extract_full_chunk()`, Cache speichern, `dirty_chunks.discard(coord)`
- Off-screen dirty: lazy rebuild wenn Chunk sichtbar wird
- `set_world()` / `invalidate_all()` / `invalidate(coord)` — Hooks für Load und M18 Streaming

**Unverändert:** GPU-Upload voller Instanz-Buffer pro Frame (M9); Sprites/Decorations pro Frame extrahiert.

**Demo:** Nach `Ctrl+L` → `extractor.set_world(world)` leert den Cache.

**Bewusst nicht in M17:** Partielle GPU-Updates, Decoration-Cache, LRU/Eviction.

---

### M16 — Welt-Persistenz

**Ziel:** Demo-Welt und Spielerstand speichern/laden — Tiles, Overlays, Decorations und Charakterposition.

**Format:** JSON in [`saves/chunk_world.json`](saves/chunk_world.json) (Version 1)
- Chunks: Koordinate + Layer-Keys (row-major, `wt:…`)
- Decorations: `world_x`, `world_y`, `decoration_id`
- Player: Position, Richtung, AnimClip, `anim_time`

**Runtime:**
- [`game_core/world_io.py`](game_core/world_io.py) — `save_world`, `load_world`, `WorldSnapshot`
- Solid-Grid wird **nicht** gespeichert — nach Load `rebuild_all_solid(content, collision)`

**Demo:** `Ctrl+S` speichern, `Ctrl+L` laden (`python -m apps.chunk_world_demo`).

**Bewusst nicht in M16:** Kamera/Zoom, Free-Cam-Modus, Streaming, binäres Format.

---

### M15 — Pixel-Kollision

**Ziel:** Kollision auf Masken-Ebene (Alpha) statt grober Tile-Boxen — Charakter 64×64 pro Richtung, Decorations aus PNG-Alpha.

**Bake:** [`tools/bake_collision.py`](tools/bake_collision.py) → [`assets/collision/manifest.json`](assets/collision/manifest.json)
- Charakter: Walk-Sheet, Union pro Richtung (8 Masken)
- Decorations: Bäume nur Stamm (`trunk_clip_v1`), Bush/Stump volle Maske
- Alpha-Schwelle: 128

**Runtime:**
- [`game_core/collision_catalog.py`](game_core/collision_catalog.py) — `CollisionMask`, `load_collision_catalog()`
- [`game_core/collision_grid.py`](game_core/collision_grid.py) — 8×8 px Zellen, 128 Byte/Chunk
- [`game_core/world.py`](game_core/world.py) — `Chunk.solid_grid`, `rebuild_all_solid`, `collision_dirty_chunks`
- [`game_core/navigation.py`](game_core/navigation.py) — `mask_position_blocked`, Axis-Slide gegen Solid-Grid

**Ablauf Demo:** Welt → Decorations → `rebuild_all_solid` → Spawn → Bewegung.

**Rebake:** `python tools/bake_collision.py` (parallel zum Atlas).

---

### M14 — Kollision / Walkability

**Ziel:** Charakterbewegung respektiert begehbare Tiles und blockierende Decorations — data-driven aus Content-Registry.

**Metadaten:**
- [`assets/content/tiles.json`](assets/content/tiles.json) — `walkable` pro Tile-Key (z. B. Wasser `false`)
- [`assets/content/decorations.json`](assets/content/decorations.json) — `blocks_movement` pro Kategorie (bush/stump/tree)

**Gameplay:**
- [`game_core/navigation.py`](game_core/navigation.py) — `tile_blocks_movement`, `anchor_position_blocked`, `apply_character_movement`
- **Footprint:** 2×2 Tiles (64×64 px Sprite, Anker unten links)
- **Axis-Slide:** X- und Y-Schritt getrennt prüfen → Gleiten entlang Hindernissen
- `World.decoration_at_tile(wx, wy)` — Decoration-Lookup für Kollision

**Demo:** Follow-Modus nutzt `apply_character_movement` statt `Character.apply_input`.

**Bewusst nicht in M14:** Krone blockiert nicht separat vom Stamm; Multi-Tile-Deko-Footprint.

---

### M13 — Y-Sort + Stamm/Krone (M13b)

**Ziel:** Charakter und Decorations nach Tiefe sortieren — natürliches Vor-/Hintereinander; Bäume mit Stamm/Krone-Split.

**Sortierschlüssel** (`render_graphics/sprite_sort.py`):

```text
(-sort_y, layer, world_x)   aufsteigend → Norden zuerst, Süden zuletzt
```

- `sort_y` aus `SpriteInstanceData.sort_y` oder `world_y` (Fußpunkt)
- Layer als Tie-Breaker bei gleichem Fuß

**Draw:** Tiles L0/L1 → Sprites Y-sortiert (ein `vkCmdDraw`).

**M13b — Bäume (category `tree`):**
- Zwei Instanzen pro Baum: **Stamm** (Layer 5, `clip_v0..trunk_clip_v1`) + **Krone** (Layer 6, `canopy_clip_v0..1`)
- Metadaten in [`assets/content/decorations.json`](assets/content/decorations.json): `canopy_layer`, `trunk_clip_v1`, `canopy_clip_v0`, `canopy_sort_y_offset`, `sort_y_offset`
- Shader-Clip via `inClipPack` — Instanz-Stride **36 Byte**

**Render-Layer:**

| LayerId | Inhalt |
|---------|--------|
| 2 | Charakter |
| 4 | Büsche, Stumps |
| 5 | Baum-Stamm |
| 6 | Baum-Krone |

**Demo:** Charakter nördlich → hinter Baum; südlich → vor Stamm, hinter Krone.

---

### M12 — Decoration + Content-Registry

**Ziel:** Bäume, Büsche, Stumps als platzierte `SpriteInstanceData`; Metadaten data-driven aus JSON + Auto-Scan der PNGs.

**Assets:** `assets/sprites/decoration/**/*.png` → Keys `wt:decoration/…` (58+ Sprites nach Rebake).

**Bake-Padding:** Nicht-32px-Vielfache (z. B. 80×96) werden in [`tools/bake_atlas.py`](tools/bake_atlas.py) auf 32px-Raster gepaddet (horizontal zentriert, unten ausgerichtet).

**Content-Registry:**
- [`game_core/content_registry.py`](game_core/content_registry.py) — Auto-Scan + [`assets/content/decorations.json`](assets/content/decorations.json) (Overrides)
- [`assets/content/tiles.json`](assets/content/tiles.json) — Tile-Metadaten + Pinsel-Paletten (M12b)

**Gameplay:**
- [`game_core/decorations.py`](game_core/decorations.py) — `PlacedDecoration`
- `World.decorations`, `place_decoration`, `remove_decoration_at`
- [`game_core/world_gen.py`](game_core/world_gen.py) — `populate_demo_decorations()`

**Bridge:** [`bridge/decoration_extractor.py`](bridge/decoration_extractor.py) — `decorations_to_sprites()`

**Render-Layer:**

| LayerId | Inhalt |
|---------|--------|
| 2 | Charakter |
| 4 | Büsche, Stumps |
| 5 | Bäume (Stamm) |
| 6 | Bäume (Krone, M13b) |

**Draw:** Tiles L0 → L1 → Sprites Y-sortiert (M13, ein `vkCmdDraw`).

**Demo (Free-Cam):** `1`/`2`/`3` = Terrain/Overlay/Decoration; `[`/`]` = Decoration-Typ; LMB platzieren; RMB/X entfernen.

---

### M12b — Data-driven Tile-Pinsel

**Ziel:** Demo-Pinsel ohne Hardcode — Tile-Keys, Layer und Input-Bindings aus [`assets/content/tiles.json`](assets/content/tiles.json).

**JSON:**
- `tiles` — pro Key: `layer`, `walkable`, `label`
- `brushes` — pro Modus (`terrain`, `overlay`): `mouse_left`, `mouse_right`, `keys` (z. B. `R` → dirt)

**Runtime:**
- [`game_core/content_registry.py`](game_core/content_registry.py) — `TileBrushPalette`, `ContentRegistry.brush_palette()`
- [`game_core/paint_brushes.py`](game_core/paint_brushes.py) — `apply_paint_at_cursor()`, `palette_label()`

**Demo:** Modus `1`/`2` liest Palette aus Registry; Fenstertitel zeigt aktive Bindings (z. B. `LMB=stone R=dirt`).

**Neues Tile:** Eintrag in `tiles` + Referenz in `brushes` — kein Demo-Code nötig.

**Bewusst nicht in M12b:** Decoration-Pinsel (bleibt `[`/`]` + Auto-Scan); Hot-Reload der JSON.

---

### M9b — Mehrere Tile-Layer

**Ziel:** Terrain (Layer 0) und Overlay-Tiles (Layer 1) mit fester Draw-Reihenfolge; ein instanced Draw (performanter als Draw pro Layer bei gleicher Pipeline).

**Layer-Konvention:**

| LayerId | Konstante | Inhalt | Platzhalter-Keys |
|---------|-----------|--------|------------------|
| `0` | `TERRAIN_LAYER_ID` | Boden | `wt:tiles/grass`, … |
| `1` | `OVERLAY_LAYER_ID` | Pfade, Fundamente | `wt:tiles/path`, `wt:tiles/foundation` |
| `2+` | — | reserviert | später data-driven |

**`game_core/world.py`:**
- `Chunk.layer_keys: dict[int, list[str]]` — row-major pro Layer
- `Chunk.from_terrain(coord, terrain_keys, overlay_keys?)`
- Leeres Overlay: `EMPTY_OVERLAY_KEY = ""` → Bridge überspringt Tile
- `World.get_tile` / `set_tile(..., layer=0|1)`

**`bridge/chunk_extractor.py`:**
- Pro sichtbarem Chunk und Layer ein `TileLayerBatch` (Overlay sparse)
- Gleiches Tile-Culling wie Layer 0

**`render_graphics/tile_layer.py`:**
- `pack_textured_tile_chunks()` sortiert global nach `LayerId` → korrekte Überlagerung in einem Buffer
- **Ein Draw** statt Draw pro Layer: weniger CPU-Overhead; bei 2–3 Layern und tausenden Instanzen optimal

**Demo (`chunk_world_demo`, Free-Cam):** Bindings in [`assets/content/tiles.json`](assets/content/tiles.json) (`brushes.terrain` / `brushes.overlay`).

| Taste | Layer 0 (Terrain) | Layer 1 (Overlay) |
|-------|-------------------|-------------------|
| `1` / `2` | Pinsel-Modus wählen | |
| LMB | Stein | Pfad |
| RMB | Gras | Foundation |
| R / T | Dirt / Water | — |
| X | — | Overlay löschen |

**Welt-Gen:** Diagonale Demo-Pfade (Layer 1) zur Visualisierung.

---

### M10 — Mutable Welt

**Ziel:** Tiles zur Laufzeit ändern; Bridge liest live Weltzustand; Renderer bleibt unverändert.

**`game_core/world.py`:**
- `World.get_tile(wx, wy, layer=0)` / `World.set_tile(wx, wy, key, layer=0|1)`
- `World.dirty_chunks` — bei jeder Mutation markiert
- Terrain-Layer 0 immer voll; Overlay Layer 1 sparse (`""` = leer)

**`bridge/`:**
- `ChunkRenderExtractor` — live aus `World` + Tile-Chunk-Cache (M17)
- `screen_to_world.py` — Maus → Welt-Tile für Pinsel

**Demo (Free-Cam, Layer 0 — siehe auch M9b für Layer 1):**
| Input | Aktion (Layer 0) |
|-------|------------------|
| LMB | Stein |
| RMB | Gras |
| R / T | Dirt / Water |

**Datenfluss:** `World.set_tile` → `dirty_chunks` → `extractor.extract()` (Cache-Hit oder Rebuild) → `RenderFrame` → GPU (M9).

### M11 — Charakter + Spritesheet-Animation

**Ziel:** Spielerfigur mit Idle/Walk/Run-Clips und 8-Richtungs-Spritesheets; generisches Animations-Framework ohne spielspezifischen Renderer.

**Assets (`assets/sprites/character/`):**

| Clip | Key | Grid | Frame |
|------|-----|------|-------|
| Idle | `wt:character/idle/idle` | 12×8 | 64×64 px |
| Walk | `wt:character/walk/walk` | 8×8 | 64×64 px |
| Run | `wt:character/run/run` | 8×8 | 64×64 px |

**Sheet-Zeilen (R1…R8, Index 0…7):** links oben, links, links unten, zugewandt, rechts unten, rechts, rechts oben, abgewandt.

**Architektur (Way 2 — Sub-UV pro Instanz):**

| Schicht | Datei | Rolle |
|---------|-------|-------|
| Gameplay | `game_core/character.py` | `Character`, `AnimClip`, Anim-Timer, 8-Wege-Richtung, lauf-Sync |
| Bridge | `bridge/character_extractor.py` | `character_to_sprite()` → `SpriteInstanceData` |
| Scene | `render_scene/types.py` | `sheet_frame_col/row` in `SpriteInstanceData`; `sheet_cols/rows` in `SpriteRect` |
| Bake | `tools/bake_atlas.py` | `_detect_sheet_grid()` (64px-Frames); Manifest-Eintrag pro Sheet |
| GPU | `render_graphics/instancing.py` | Instanz-Pack `<2f4fII` (32 Byte): Pos, Tint, `sprite_id`, Frame-Pack |
| GPU | `render_graphics/shaders/textured_instanced.vert` | Sub-UV pro Sheet-Zelle; Anker unten links |
| GPU | `render_graphics/atlas_registry.py` | SSBO: `sizePad.xy` = Pixelgröße, `sizePad.zw` = Sheet-Grid |

**Richtung:** `direction_from_delta(dx, dy)` — `atan2` mit Winkel-Normalisierung auf `[0, 2π)`, Oktant → Sheet-Zeile via `_OCT_TO_ROW`.

**Bewegungs-Sync:** `move_speed_for_clip(clip) = CLIP_STRIDE_PX × CLIP_FPS / frame_count` — ein Animationszyklus = eine Schrittweite (Walk 32 px, Run 56 px), kein Gleiten über die Karte.

**Kamera-Follow:** `Character.camera_focus_x/y` = Sprite-Mitte (`world + CHARACTER_SPRITE_PX/2`); `Character.at_center()` für Spawn in Weltmitte.

**Draw-Reihenfolge:** Tiles L0/L1 → Sprites Y-sortiert (M13) — Fußpunkt + Layer; Bäume Stamm/Krone via Clip.

**Demo (`chunk_world_demo`):**

| Modus | Steuerung |
|-------|-----------|
| Follow (Standard) | WASD = Charakter; Shift = Run; Kamera auf Sprite-Mitte |
| Free-Cam (`F`, Edge-Toggle) | WASD = Kamera; Pinsel wie M10 |

**Shader neu bauen nach Änderung:** `python render_graphics/shaders/compile_shaders.py`  
**Atlas neu backen nach Sprite-Änderung:** `python tools/bake_atlas.py`

---

## 6. Frühe Architekturfehler (aktiv vermeiden)

1. **Render/Gameplay vermischen** — kein Gameplay-Code in `render_*`, kein Vulkan in `game_core`.
2. **Spielspezifische Renderer** — kein `PlayerRenderer`, nur generische `SpriteInstanceData`.
3. **Monolith** — keine `engine.py`, die Fenster + Welt + GPU vereint.
4. **Feature-Bloat vor Kern** — keine Partikel, kein Audio, kein UI vor stabilem Tile-/Sprite-Pfad.
5. **Game-Objekte an Renderer** — immer über `bridge` → `RenderFrame`.
6. **Verschwendender Vulkan-Umgang** — Command Pools cachen, Pipeline-Binds minimieren, kein per-frame Ressourcen-Chaos.
7. **Swapchain-Extent als CFFI-Referenz** — Extent-Werte kopieren (`extent_size`); vor `vkCreateSwapchainKHR` GLFW-FB und `currentExtent` abgleichen; `oldSwapchain` erst nach erfolgreichem Create zerstören.
8. **Factorio-only APIs** — Chunk-/Tile-Strukturen generisch halten (orthographisch, layerbasiert, instanced).

---

## 7. Definition of Done — Phase 1 (Struktur)

- [x] Modulgrenzen und Ordnerbaum angelegt
- [x] Kerninterfaces in `render_scene/` definiert
- [x] Abhängigkeitsregeln dokumentiert
- [x] Bridge-Protokoll (`RenderExtractor`) skizziert
- [x] Minimaler Vulkan-Renderpfad (Phase 2 — GPU Clear)
- [x] Orthographische Kamera + GPU Uniform (Phase 2 — M4)
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
- [x] Hybrid World-Gen: Noise, Klima, Voronoi-Biome (M21)
- [x] Biome-System: Blend L0, Sub-Biom-Noise, ChunkFieldCache (M22)
- [x] Parallel Chunk Gen: ProcessPool, ChunkGenResult, Streaming-Prefetch (M22b)
- [x] FNV Tile-ID IPC (M22c)
- [x] Hybrides Chunk-Streaming: Viewport, Safety, Apply-Budget (M22d)
- [x] Worker-Deko + Worker-Solid (M22e)
- [x] Profiling & Runtime-Metriken (M23)
- [x] Deferred Unload & Sparse Persistence (M23a)

**Demos:**
- `python -m apps.gpu_clear_demo` — GPU Clear
- `python -m apps.ortho_camera_demo` — Ortho-Kamera (WASD, +/- Zoom)
- `python -m apps.instance_demo` — Instanced Quads (texturiert via Atlas)
- `python -m apps.atlas_demo` — Texture Atlas (Mix 1×1, 1×3, 2×4 Tiles)
- `python -m apps.tile_layer_demo` — Tile-Layer (3072 Tiles + Dekoration)
- `python -m apps.chunk_world_demo` — Chunk-Welt infinite (M8–M21, Streaming, Pinsel `1`/`2`/`3`, Free-Cam `F`, Vollbild `F11`, Save/Load `Ctrl+S`/`Ctrl+L`, Regen `G`)
- `python -m apps.world_gen_debug_demo` — World-Gen Debug-Ansichten (M21–M22)

**Atlas bake:** `python tools/bake_atlas.py --generate-placeholders`  
**Collision bake:** `python tools/bake_collision.py`

Sprites liegen rekursiv unter `assets/sprites/` (z. B. `decoration/trees/oak.png` → Key `wt:decoration/trees/oak`).
Stabile IDs in `assets/demo_atlas/sprite_registry.json`.
