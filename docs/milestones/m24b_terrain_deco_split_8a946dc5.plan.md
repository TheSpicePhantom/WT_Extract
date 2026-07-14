---
name: M24b Terrain Deco Split
overview: "M24b (umsetzungsreif, Review M24b.3): Terrain→Deco-Pipeline mit BuildKey+build_epoch (Ownership in ChunkGenPool), symmetrischen Apply-Verträgen, klarem Ready/Discard-Ownership, worker-lokalem LRU-Cache, Single-Writer via last_applied_deco_build_key, deco_incomplete E2E-Persistenz. M24a kompatibel."
todos:
  - id: p0-contracts
    content: "Phase 0: BuildKey+build_epoch (Pool-Ownership), can_apply_terrain/deco_result symmetrisch, ChunkBuildState, Failure-Modes inkl. Terrain-stale/Epoch + Duplicate-Apply"
    status: pending
  - id: p1-split-tasks
    content: "Phase 1: Kanonische Stage-API; TerrainStageData worker-lokal; BuildCoordinator injiziert build_epoch in BuildKey; Pool zwei Jobtypen"
    status: pending
  - id: p2-cache-share
    content: "Phase 2: Bounded LRU (Router-owned Cleanup bei consume/discard); Epoch-Eviction; Pflicht-Metriken"
    status: pending
  - id: p3-apply-streamer
    content: "Phase 3: apply_terrain/deco_stage; last_applied_deco_build_key; deco_incomplete E2E (4 Schritte); Streamer-Router owned discard/consume"
    status: pending
  - id: p4-scheduler
    content: "Phase 4: max_in_flight vs parallelism_cap mit Beispiel; visible_terrain_pending; Terrain-Druck-Metriken; streaming.json"
    status: completed
  - id: p5-deco-config
    content: "Phase 5: CompiledDecoPass + Determinismus-Tests (Reihenfolge, deco_config_version-Hash); kein DSL"
    status: pending
  - id: p4b-dual-pool
    content: "Phase 4b (optional): zweiter ProcessPool nur wenn Ein-Pool-Caps Terrain messbar blockieren"
    status: pending
isProject: false
---

# M24b — Terrain/Deco-Trennung (umsetzungsreif, Review M24b.3)

Quellen: [m24b_architektur_skizze.md](m24b_architektur_skizze.md), [m24b_review_fuer_cursor.md](m24b_review_fuer_cursor.md), [m24b_2_finaler_schliff.md](m24b_2_finaler_schliff.md), [m24b_3_final_review.md](m24b_3_final_review.md). Aufbauend auf M24a ([game_core/worker_fast_path.py](game_core/worker_fast_path.py)).

## Problem (belegt)

Heute liefert ein Worker-Task monolithisch Terrain + Deko + Solid (~25 s/Chunk bei 64×64). M24a optimiert nur Main-Apply (~0,9 ms); Worker-Pipeline bleibt monolithisch.

## Kernregel

> **Deco darf Terrain weder beim Apply noch bei der CPU-Belegung vorauslaufen.**

## Ownership-Übersicht (M24b.3)

| Ressource | Owner (einzige Schreibquelle) | Konsumenten (nur lesen) |
|-----------|------------------------------|-------------------------|
| `build_epoch` | [`ChunkGenPool`](game_core/chunk_gen_pool.py) / `BuildCoordinator` | Streamer, Apply, Predicates, Result-Typen |
| Ready-Result consume/discard | Streamer-Router (`_route_pool_results`) | Apply (nur bei positivem Guard) |
| Metriken `discarded_stale/duplicate` | Streamer-Router (beim Discard) | Perf-Export |
| Worker-LRU Cache-Cleanup | Streamer-Router (bei consume/discard) | Worker (nur lesen/schreiben lokal) |
| `deco_incomplete` setzen | `_mark_pending_unload` / Persistenz-IO | Revive, `submit_deco_allowed` |
| `last_applied_deco_build_key` | `apply_deco_stage` (einmalig) | `can_apply_deco_result`, Duplicate-Guard |

**Verboten:** Streamer, Apply-Code oder Predicates erzeugen eigene `build_epoch`-Werte.

---

## Phase 0 — Verträge und Statusmodell

**Dateien:** neu [`game_core/chunk_build.py`](game_core/chunk_build.py), [`game_core/worker_fast_path.py`](game_core/worker_fast_path.py), [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py)

### BuildKey (vollständig)

```python
@dataclass(frozen=True)
class BuildKey:
    coord: tuple[int, int]
    terrain_revision: int
    terrain_config_version: int
    deco_config_version: int
    build_epoch: int               # nur vom BuildCoordinator injiziert
```

### `build_epoch` — Ownership und Injektion

- **Owner:** `ChunkGenPool` (oder `BuildCoordinator` als Pool-Nachbar) — einzige Quelle
- **Erhöhung nur bei:** Pool-Reset, Worker-Neustart, World-Reinit, harte Streaming-Rekonfiguration
- **Injektion:** Bei `submit_terrain` / `submit_deco` setzt der Coordinator `build_epoch` in den `BuildKey` — Streamer und Worker lesen nur

```python
# chunk_gen_pool.py — kanonisch
class BuildCoordinator:
    build_epoch: int  # einzige Schreibquelle

    def next_terrain_build_key(self, coord) -> BuildKey:
        return BuildKey(coord=coord, terrain_revision=..., build_epoch=self.build_epoch, ...)

    def bump_epoch(self) -> None:  # nur bei Systemereignissen
        self.build_epoch += 1
```

### `terrain_revision` — an Submission gekoppelt

> Jede neue Terrain-Submission, die nicht dieselbe aktive Build-Linie fortsetzt, erzeugt neue `terrain_revision` (bei Submit, nicht Apply).

### ChunkBuildState

```python
@dataclass
class ChunkBuildState:
    terrain_build_key: BuildKey | None
    terrain_state: TerrainState
    deco_state: DecoState
    last_applied_deco_build_key: BuildKey | None = None  # Single-Writer-Quelle
    deco_suppression_reason: str | None = None
    deco_incomplete: bool = False
```

`last_applied_deco_build_key` ist die **kanonische Quelle** für Duplicate-Erkennung (robuster als nur `deco_state == APPLIED`).

### Predicates — symmetrisch und zweistufig

#### `can_apply_terrain_result(...)` (gleich scharf wie Deco)

Ein `TerrainResult` ist **stale** und wird verworfen wenn:

- `result.build_key.build_epoch != coordinator.build_epoch`
- zwischen Submit und Poll eine **neuere Terrain-Linie** für dieselbe Coord gestartet wurde (`terrain_revision` am `ChunkBuildState` höher als im Result)
- Coord hat bereits einen **neueren** `terrain_build_key` in `ChunkBuildState` — kein Überschreiben
- `pending_unload`, Override/Delta aktiv, Coord nicht mehr wanted

Ein `TerrainResult` darf **apply** wenn:

- `result.build_key` exakt der erwarteten Build-Linie entspricht (Submit-Zeitpunkt)
- Coord nicht in `world.chunks` (oder Revive mit passendem Key)
- kein Guard-Verstoß

#### `can_apply_deco_result(...)`

- `result.build_key` exakt `ChunkBuildState.terrain_build_key`
- `result.build_key != last_applied_deco_build_key` (Duplicate-Guard)
- kein Suppression-Grund

#### Submit-Ebene

| Funktion | Zweck |
|----------|-------|
| `submit_terrain_allowed(...)` | Budget, Caps, wanted |
| `submit_deco_allowed(...)` | `terrain_state == APPLIED`, nicht SUPPRESSED, Guards |

### Tests — `tests/test_m24b_pipeline.py`

**Terrain-Failure-Modes (neu, Pflicht):**
8. Altes `TerrainResult` kommt nach Resubmit zurück → `terrain_discarded_stale++`
9. `TerrainResult` aus alter Epoch nach Pool-Reset → discard

**Bestehende Failure-Modes:** 1–7 (Deco stale, Revive, User-Mod, CPU-Druck, LRU, `deco_incomplete`, Duplicate-Apply)

**DoD Phase 0:** `can_apply_terrain_result` dokumentiert und getestet; Epoch-Ownership eindeutig.

---

## Phase 1 — Kanonische Stage-API

```python
build_terrain_stage(coord, ctx) -> TerrainStageData
build_deco_stage(terrain_stage_data, ctx) -> DecoStageData
to_terrain_result(stage_data) -> TerrainResult
to_deco_result(stage_data) -> DecoResult
apply_terrain_stage(world, result, content)   # nur nach can_apply_terrain_result
apply_deco_stage(world, result, content)      # nur nach can_apply_deco_result
```

**IPC-Grenze:** `ChunkFieldCache` nie in Results; nur `TerrainResult`/`DecoResult` IPC.

**Pool:** `submit_terrain` ruft `BuildCoordinator.next_terrain_build_key()` — Epoch-Injektion zentral.

---

## Phase 2 — Cache-Sharing (bounded, Router-owned Cleanup)

```python
_worker_field_cache_lru: OrderedDict[BuildKey, ChunkFieldCache]
MAX_SHARED_FIELD_CACHES = terrain_max_in_flight + 2
```

**Cache-Cleanup-Ownership:**
- **Streamer-Router** (`_route_pool_results`) entfernt LRU-Einträge bei consume (Deco applied) und discard (stale/duplicate)
- Worker schreibt in LRU; Router ist einziger Evictor auf Main-Thread
- Epoch-Wechsel: Router flusht gesamte LRU via `BuildCoordinator.bump_epoch()`

**Metriken:** `field_cache_hits/misses/evictions/live_count`

---

## Phase 3 — Apply, Single-Writer, Persistenz E2E

### Apply-Ownership

- **Router** pollt, prüft Guards, entscheidet consume vs. discard, zählt Metriken
- **Apply** (`apply_terrain_stage` / `apply_deco_stage`) verändert World-State **nur** bei bereits positivem Guard — kein Discard in Apply

### Single-Writer (kanonische Quelle)

Duplicate-Erkennung via `last_applied_deco_build_key`:

```python
# can_apply_deco_result — vor Apply
if result.build_key == build_state.last_applied_deco_build_key:
    return False  # → deco_discarded_duplicate++

# apply_deco_stage — nach erfolgreichem Apply
build_state.last_applied_deco_build_key = result.build_key
build_state.deco_state = DecoState.APPLIED
build_state.deco_incomplete = False
```

### `deco_incomplete` — End-to-End (4 Schritte)

1. **Terrain applied, Deco fehlt** — `deco_state == NONE`, `deco_incomplete` noch false
2. **Unload/Persist** — `_mark_pending_unload` setzt `deco_incomplete = true` in `PendingUnloadEntry` + Persistenz-Flags; **keine** prozedurale Deco serialisieren
3. **Revive/Reload** — Terrain-Snapshot wiederherstellen; `deco_incomplete` bleibt true; `deco_state = NONE`; Deco offen, nicht rekonstruieren
4. **Deco neu angefordert + `apply_deco_stage` erfolgreich** — `deco_incomplete = false`, `last_applied_deco_build_key` gesetzt; Chunk vollständig

**Verboten bei `deco_incomplete`:** prozedurale Deko aus Persistenz/Snapshot rekonstruieren, `populate_chunk_decorations` als Heuristik, Save mit falscher Deco-Annahme.

### Terrain-only-Semantik

| Subsystem | Verhalten |
|-----------|-----------|
| Render | Terrain-Tiles anzeigen |
| Navigation | Tile-Walkability bis `solid_grid` |
| Harvest/Loot/Tree-Hit | Terrain-only ignorieren |
| Save/Persist | `deco_incomplete`; keine prozedurale Deco |
| Revive | Deco neu anfordern |

**M24a-Kompat:** `apply_worker_complete_result` für `WORKER_COMPLETE`.

---

## Phase 4 — Scheduler, Invarianten, Beispiel

### `max_in_flight` vs. `parallelism_cap`

| Config | Zählt |
|--------|-------|
| `terrain_max_in_flight` | submitted + running + **ready-but-not-applied** |
| `terrain_parallelism_cap` | nur **aktiv laufende** Worker-Jobs |

**Invarianten:** `deco_max_in_flight <= terrain_max_in_flight`; `deco_parallelism_cap < terrain_parallelism_cap`

### Mini-Beispiel (verbindlich)

```
terrain_max_in_flight = 8
terrain_parallelism_cap = 6

Zustand:
  - 6 Terrain-Jobs laufen (CPU)
  - 2 Terrain-Results fertig in Ready-Queue (noch nicht applied)

→ in_flight_count = 8 (6 running + 2 ready)
→ KEINE weiteren Terrain-Submits erlaubt
→ obwohl nur 6 Worker CPU belegen
```

Ready-Queues zählen gegen `max_in_flight` bis Result **konsumiert oder verworfen** wurde (Router-Ownership).

### Ready-/Discard-Ownership (3–5 Sätze)

Der **Streamer-Router** (`ChunkStreamer._route_pool_results`) ist Owner für Ready-Result-Konsum und alle Discards. Er prüft Guards, ruft bei Erfolg `apply_*_stage` auf (Consume), und bei Verstoß verwirft er das Result und inkrementiert `terrain_discarded_stale`, `deco_discarded_stale` oder `deco_discarded_duplicate`. Die Apply-Schicht ändert World-State nur bei positivem Guard und führt selbst kein Discard durch. LRU-Cache-Cleanup auf dem Main-Thread hängt an Router-Consume/Dismiss-Events — der Worker schreibt nur in die LRU, der Router ist einziger Evictor.

### `visible_terrain_pending`

```python
visible_terrain_pending = count(coord in wanted_visible where terrain_state != APPLIED)
```

Solange `> 0`: kein Prefetch-Deco, kein Deco-Backfill.

### Config + Metriken

Siehe Phase 4 in vorheriger Version; Pflicht: `visible_terrain_wait_frames`, `terrain_discarded_stale`, `deco_discarded_duplicate`.

---

## Phase 5 — CompiledDecoPass (deterministisch + getestet)

```python
sort_key = (priority, declaration_order, pass_name)
```

**Determinismus-Tests (Pflicht, `tests/test_m24b_deco_config.py`):**
1. Gleiche Inputs → gleiche Pass-Reihenfolge trotz variierender JSON-Ladereihenfolge
2. `deco_config_version` (= `BuildKey.deco_config_version`) hängt vom kompilierten+sortierten Zustand ab, nicht vom Einlesepfad

---

## Implementierungsreihenfolge

1. Phase 0 + 1 — Vertrag, Epoch-Ownership, Stage-API
2. Phase 2 — LRU + Router-Cleanup
3. Phase 3 — Apply, Single-Writer, `deco_incomplete` E2E
4. Phase 4 — Scheduler + Beispiel
5. Phase 5 — CompiledDecoPass + Determinismus-Tests
6. Phase 4b — optional

## Betroffene Kernmodule

- [`game_core/chunk_build.py`](game_core/chunk_build.py) — BuildKey, ChunkBuildState, BuildCoordinator
- [`game_core/chunk_gen_pool.py`](game_core/chunk_gen_pool.py) — `build_epoch` Owner
- [`game_core/chunk_streaming.py`](game_core/chunk_streaming.py) — Router (consume/discard/metrics/cache-cleanup)
- [`game_core/pending_unload.py`](game_core/pending_unload.py) — `deco_incomplete`
- [`game_core/worker_fast_path.py`](game_core/worker_fast_path.py) — symmetrische Guards
- [`tests/test_m24b_pipeline.py`](tests/test_m24b_pipeline.py), [`tests/test_m24b_deco_config.py`](tests/test_m24b_deco_config.py)

## Definition of Done (M24b) — final

**Ownership (explizit dokumentiert):**
- `build_epoch`: nur `BuildCoordinator`/`ChunkGenPool`
- Ready-Queues, Discard, Metriken: Streamer-Router
- LRU-Cleanup: Router bei consume/discard

**Verträge (symmetrisch):**
- `can_apply_terrain_result` gleich scharf wie `can_apply_deco_result` — beide getestet (Failure-Modes 8+9)
- `last_applied_deco_build_key` als Single-Writer-Quelle
- `deco_incomplete` E2E (4 Schritte) getestet

**Scheduler:**
- `max_in_flight` vs. `parallelism_cap` mit Mini-Beispiel im Code/Doku
- `visible_terrain_pending` deterministisch

**Determinismus:**
- `CompiledDecoPass`-Sortierung + 2 Determinismus-Tests

**Performance:** wie bisher (Terrain früher, Deco kontrolliert, Main-Apply ≥ M24a, bounded Cache, keine O(D)-Scans)

**Tests:** 9 Pipeline-Failure-Modes + 2 Deco-Config-Determinismus-Tests grün

## Freigabekriterium (M24b.3)

- Zustände klar
- Datenfluss klar
- **Ownership klar** (Epoch, Ready, Discard, Cache)
- Scheduler-Regeln klar (inkl. Zählbeispiel)
- Persistenz Terrain-only klar (E2E)
- Duplicate-/Stale-Fälle explizit testbar
- Terrain-Apply-Vertrag = Deco-Apply-Vertrag

**Ein guter Plan ist die halbe Umsetzung.**
