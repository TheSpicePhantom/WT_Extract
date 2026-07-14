# M24a – Fragen für Cursor

**Status:** beantwortet (2026-07-12)  
**Hilfsmittel:** `helpers/m24a_scan.py` (Call-Site-Scan → `helpers/m24a_scan_report.json`), `helpers/m24a_predicates.py` (Referenz-Predicates), `docs/benchmarks/single_chunk_64.json` (Messwerte 64×64)

Ziel: offene Architektur- und Performance-Fragen für **M24a** — Schwerpunkt 64×64-Streaming-Hotpath in `game_core` (Worker-Complete-Fast-Path, Collision-Rebuilds, globale `world.decorations`-Scans).

---

## Ergebnis-Zusammenfassung (Block G vorab)

### Priorisierte Hotspots

| Prio | Hotspot | Impact | Fix |
|------|---------|--------|-----|
| 1 | `_flush_deferred_collisions` nach Worker-Apply | 15–110+ ms/Chunk (O(D) Deko-Scan) | Flush überspringen bei Fast-Path |
| 2 | Sync blockiert bei `pool.is_in_flight` | 0 sichtbare Chunks, ~16 ms/Frame Wartezeit | Timeout-Fallback oder kein Sync-Block |
| 3 | `place_decoration` O(D×N) beim Apply | wächst mit Welt | Batch-Append Fast-Path |
| 4 | Pool-Cold-Start (19 Worker) | ~16 s bis erster Chunk | Warmup, kleineres Worker-Set |
| 5 | `decorations_to_sprites` O(D)/Frame | Dauerlast Extract | später: Index (nicht M24a Pflicht) |

### Predicate-Spezifikation

Siehe `helpers/m24a_predicates.py`: `is_worker_complete_result()` + `can_apply_worker_complete_fast_path()`.

### Minimaler Patch-Plan

1. Predicate extrahieren / dokumentieren  
2. Streamer: kein `_flush_deferred_collisions` nach Worker-Fast-Path  
3. Optional: `apply_worker_complete_result()` ohne `collision`-Parameter  
4. **Nicht in M24a:** `decorations_by_chunk`-Index, v5-Persistenz, Renderer-Umbau  

---

## Block A – Worker-Complete-Fast-Path

### 1. Warum läuft nach vollständigem Worker-Result noch Collision-Flush?

#### Antwort

**Auslöser:** Jeder Apply-Pfad (Pool und Sync) setzt `defer_collision=True` und hängt die Koordinate an `deferred_collision_coords`. Am Ende des Apply-Blocks wird **unbedingt** geflusht — ohne Unterscheidung Worker vs. Sync.

```458:466:game_core/chunk_streaming.py
                self._apply_chunk_from_result(
                    ...
                    defer_collision=True,
                )
                deferred_collision_coords.append(result.coord)
```

```505:512:game_core/chunk_streaming.py
        if deferred_collision_coords:
            self._flush_deferred_collisions(
                world,
                deferred_collision_coords,
                ...
            )
```

**Bedingung:** Es gibt **keine** Bedingung — jede Koordinate in `deferred_collision_coords` bekommt `rebuild_chunk_solid`.

**Historie:** M22b/M23b **Apply-Batching** (`defer_collision` + Flush am Frame-Ende), um mehrere Loads in einem Block zu bündeln. M22e Worker-Apply setzt `solid_grid` bereits in `apply_chunk_result`, aber der Streamer wurde **nicht** angepasst, den Flush für Worker-Complete zu überspringen. → **unvollständiger M22e-Umbau**, keine echte neue Korrektheitsanforderung.

| Situation | Flush zwingend? |
|-----------|-----------------|
| Sync-Load (`generate_chunk` + `populate_chunk_decorations`) | **Ja** — Solid wurde auf Main noch nicht gebaut |
| Terrain-only Worker-Result (`decorations is None`) | **Ja** — Fallback-Pfad |
| Override / Delta / User-Deko / dirty | **Ja** — Worker-Solid nicht vertrauenswürdig |
| **`WORKER_COMPLETE` + `_should_use_worker_apply`** | **Nein (redundant)** — `apply_chunk_result` setzt bereits `chunk.solid_grid = result.solid_grid` und `collision_dirty_chunks.discard(coord)` |

**Messung:** `rebuild_chunk_solid_after_worker` ~14 ms (1 Chunk, wenig Deko) vs. ~0,5 ms für `apply_chunk_result` (`single_chunk_64.json`). Im Demo-Run wächst `apply_collision_ms` mit globaler Deko-Liste auf 30–110+ ms.

---

### 2. Wie lautet die präzise Definition von `WORKER_COMPLETE`?

#### Antwort

Zwei Ebenen (Referenz: `helpers/m24a_predicates.py`):

**Ebene A — Payload (`is_worker_complete_result`):**

```python
def is_worker_complete_result(result, *, worker_apply_enabled, debug_mode) -> bool:
    if not worker_apply_enabled: return False
    if debug_mode is not None: return False
    if result.decorations is None or result.solid_grid is None: return False
    validate_chunk_gen_result(result)  # 4096 IDs/Layer, solid_grid Byte-Länge
    return True
```

**Ebene B — Streaming (`can_apply_worker_complete_fast_path` ≡ `_should_use_worker_apply`):**

Zusätzlich:

- `not streamer.pending_unload.contains(coord)`
- `coord not in streamer.persistent_deltas`
- `coord not in streamer.persistent_overrides`
- `coord not in world.dirty_chunks`
- `not _has_user_decorations_in_chunk(world, coord)`

**Implizite Guards heute:**

- `parallel_prefetch` muss Pool liefern (kein Predicate, aber Pfad)
- `get_world_gen_config().parallel_worker_apply == True`
- Chunk darf nicht schon in `world.chunks` sein (Router in `update`)
- Budget (`max_applies_per_frame`) — kein Korrektheits-Guard

**Hinweis:** `is_worker_complete()` in `world_gen_result.py` prüft nur `decorations is not None and solid_grid is not None` — **ohne** Längenvalidierung. Validierung erst in `apply_chunk_result` via `validate_chunk_gen_result`.

---

### 3. Welche Invarianten verhindern heute direkte Übernahme von `solid_grid`?

#### Antwort

**Technisch verhindert nichts** die direkte Übernahme — `apply_chunk_result` tut das bereits. Der Streamer **invalidiert** den Gewinn durch den nachfolgenden Rebuild.

Gründe, warum `chunk.solid_grid = result.solid_grid` **allein** nicht reicht (Nebenbedingungen):

| Invariante | Erfüllt durch Worker-Apply? | Ohne Rebuild OK? |
|------------|----------------------------|------------------|
| `world.chunks[coord]` gesetzt | Ja (`chunk_from_result`) | Ja |
| Procedural-Deko in `world.decorations` | Ja (`place_decorations_batch`) | Ja |
| `collision_dirty_chunks` clean | Ja (`discard`) | Ja |
| `semantically_active` | **Nein** — `_load_chunk` ruft `mark_semantically_active`, Worker-Pfad **nicht** explizit | Prüfen: Chunk in `world.chunks` → `is_semantically_active` default True wenn nicht in inactive-Set |
| Navigation `world_cell_solid` | Liest `chunk.solid_grid` | Ja, wenn Bytes korrekt |
| Cross-Chunk-Deko-Masken | Worker baut mit chunk-lokalen Placements; große Masken können Nachbar-Chunk berühren | Worker und Main-Referenz stimmen laut `test_worker_solid` / `test_apply_chunk_result_matches_reference` überein |

**Fazit:** Kein stiller Abhängigkeit vom Main-Rebuild für reine prozedurale Worker-Chunks. Der Rebuild war **Validierungs-/Batching-Erbe**, nicht Korrektheits-Fix.

---

## Block B – Apply-Struktur

### 4. Kann `apply_chunk_result` in eine reine Übernahmefunktion zerlegt werden?

#### Antwort

**Ja.** Heute ist es bereits fast reine Übernahme; die Trennung wäre API-Klarheit.

| Funktion | Rolle |
|----------|-------|
| `apply_worker_complete_result(world, result, content)` | Fast-Path |
| `apply_sync_or_fallback_result(...)` | Langsam: `chunk_from_result` + `_ensure_procedural_decorations` |

**Side-Effects in `apply_chunk_result` heute:**

1. `validate_chunk_gen_result` — nötig
2. `chunk_from_result` — ID→Key Mapping (nötig)
3. `world.chunks[coord] = chunk` — nötig
4. `place_decorations_batch` — **Side-Effects:** O(D) Duplicate-Scan, `collision_dirty` pro Deko (sofort wieder discarded)
5. `chunk.solid_grid = result.solid_grid` — nötig
6. `collision_dirty_chunks.discard` — nötig
7. Parameter `collision` — **ungenutzt**, kann entfallen

**Worker-Complete unnötig:** `collision`-Parameter; `place_decoration`-Routing (ersetzbar durch Batch-Append).

---

### 5. Welche Nebenwirkungen von `place_decoration()` würden bei Batch-Append verloren gehen?

#### Antwort

Vollständige Liste (`game_core/world.py`):

| Nebenwirkung | Pro procedural Fast-Path relevant? |
|--------------|-------------------------------------|
| Duplicate-Scan über `world.decorations` | Verlust **gewollt** (frischer Chunk, keine Kollision) |
| Replace an gleicher Position | Bei Load irrelevant (Chunk war leer) |
| `decorations.append(PlacedDecoration(...))` | **Muss erhalten bleiben** |
| `_mark_decoration_collision_dirty` → `mark_collision_dirty_for_rect` | Verlust **gewollt** (Solid kommt vom Worker) |
| `mark_persistenz_flag(USER_DECO)` nur bei `procedural=False` | Kein Verlust bei `procedural=True` |
| Kein separater Index | Kein Verlust (gibt es nicht) |

**Query/Extract/Save:** Lesen `world.decorations` — solange `PlacedDecoration`-Einträge identisch sind, kein Unterschied.

**Risiko:** Wenn derselbe Chunk **zweimal** Worker-Apply ohne Unload → Duplicate-Deko. Heute verhindert der Streamer `coord in world.chunks` → kein Doppel-Apply.

---

### 6. Wie müsste ein sicherer Deko-Batch-Fast-Path aussehen?

#### Antwort — Patch-Skizze

```python
def apply_worker_complete_result(
    world: World,
    result: ChunkGenResult,
    content: ContentRegistry,
) -> Chunk:
    validate_chunk_gen_result(result)
    chunk = chunk_from_result(result, content)
    coord = result.coord
    assert result.decorations is not None
    assert result.solid_grid is not None

    world.chunks[coord] = chunk
    chunk.solid_grid = result.solid_grid

    batch: list[PlacedDecoration] = []
    for placement in result.decorations:
        try:
            deco_key = content.decoration_id_to_key(placement.decoration_id)
        except KeyError:
            continue
        if content.decoration_by_id(deco_key) is None:
            continue
        wx, wy = tile_to_world_anchor(placement.wx, placement.wy)
        batch.append(PlacedDecoration(
            world_x=wx, world_y=wy,
            decoration_id=deco_key, procedural=True,
        ))
    world.decorations.extend(batch)

    world.collision_dirty_chunks.discard(coord)
    return chunk
```

**Streamer-Ergänzung:**

```python
used_fast = self._should_use_worker_apply(world, result)
self._apply_chunk_from_result(..., defer_collision=not used_fast)
if not used_fast:
    deferred_collision_coords.append(coord)
```

---

## Block C – Globale O(D)-Scans

### 7. Liste alle `world.decorations`-Scans nach Fallklassen

#### Antwort

Quelle: `helpers/m24a_scan.py` → `helpers/m24a_scan_report.json` (11 Loop-Sites).

#### Load-Hotpath

| Funktion | Datei | Auslöser | Kosten | Kritisch? |
|----------|-------|----------|--------|-----------|
| `_has_user_decorations_in_chunk` | `chunk_streaming.py:235` | Vor Worker-Apply | O(D) | Ja, pro Kandidat |
| `place_decoration` (via batch) | `world.py:297` | Worker-Apply | O(D×N) | Ja |
| `rebuild_chunk_solid` | `collision_grid.py:113` | Deferred Flush | O(D) | **Ja, Hauptkosten** |

#### Collision / Navigation

| Funktion | Datei | Auslöser | Kosten | Kritisch? |
|----------|-------|----------|--------|-----------|
| `rebuild_chunk_solid` | `collision_grid.py:113` | Flush, ensure_fresh | O(D) | Ja |
| `decoration_at_tile` | `world.py:360` | Navigation-Hilfen | O(D) | Selten pro Query |
| `ensure_collision_fresh` | `world.py:254` | indirekt | O(\|dirty\|×D) | Bei Bewegung |

#### Unload / Pending / Revive

| Funktion | Datei | Auslöser | Kosten | Kritisch? |
|----------|-------|----------|--------|-----------|
| `_chunk_has_procedural_deco` | `chunk_streaming.py:138` | Revive | O(D) | Mittel |
| `remove_procedural_decorations_in_chunk` | `world_gen.py:1127` | Unload-Drain | O(D) | Mittel |
| `remove_decorations_in_chunk` | `world_gen.py:1146` | Flush/Debug | O(D) | Selten |

#### Render / Extract

| Funktion | Datei | Auslöser | Kosten | Kritisch? |
|----------|-------|----------|--------|-----------|
| `decorations_to_sprites` | `decoration_extractor.py:69` | Jeder Frame | O(D) | Dauerlast, nicht Load |

#### Save / Persistenz

| Funktion | Datei | Auslöser | Kosten | Kritisch? |
|----------|-------|----------|--------|-----------|
| `save_streaming_world` | `streaming_world_io.py:119` | STRG+S | O(D) | Selten |
| `_decoration_to_dict` loop | `world_io.py:95` | Legacy-Save | O(D) | Selten |

#### Tests / Tools

| `tests/support/chunk_reference.py`, Benchmarks | — | Tests | O(D) | — |

---

### 8. Welche dieser globalen Scans müssen wirklich global bleiben?

#### Antwort

| Call-Site | Global nötig? | Alternative | Worker-Fast-Path entbehrlich? |
|-----------|---------------|-------------|-------------------------------|
| `rebuild_chunk_solid` | **Nein** (chunk-filterbar) | chunk-lokale Deko-Liste oder Index | **Ja — ganz entfallen** |
| `_has_user_decorations_in_chunk` | **Nein** | `decorations_by_chunk` oder Persistenz-Flag | Nein (Guard bleibt) |
| `_chunk_has_procedural_deco` | **Nein** | Index / Flag beim Apply setzen | Nein |
| `remove_procedural_decorations_in_chunk` | **Nein** | Index | Nein |
| `decoration_at_tile` | **Nein** | `(wx,wy)`-Map | — |
| `decorations_to_sprites` | Kann global bleiben | Index für sichtbare Chunks | — (Extract, nicht M24a) |

---

### 9. Welche minimalen Datenstrukturen würden O(D)-Scans entschärfen?

#### Antwort

| Variante | Aufwand | Gewinn | Save/Load/Revive | Risiko |
|----------|---------|--------|------------------|--------|
| `decorations_by_chunk: dict[coord, list]` | Mittel | Hoch für Collision/Unload/Guards | Revive muss Index pflegen | Drift Liste vs. Index |
| `decorations_by_tile: dict[(x,y), ...]` | Hoch | Sehr hoch für Queries | Save serialisiert weiter global | Speicher, Updates |
| Globale Liste + Index | Mittel | Gut | Am kompatibelsten | Zwei Quellen synchron halten |
| Nur prozeduraler Index | Gering | Mittel | User-Deko weiter O(D) | Teilweise Lösung |

**M24a-Empfehlung:** Index **nicht** in M24a — erst Fast-Path ohne Rebuild (größter Gewinn, kleinster Diff). Index als M24b/M25.

---

## Block D – Collision und Navigation

### 10. Welche Call-Sites von `rebuild_chunk_solid` gibt es genau?

#### Antwort

Quelle: `helpers/m24a_scan_report.json` (17 Treffer).

| Fallklasse | Call-Site | Bewertung |
|------------|-----------|-----------|
| **Worker-Apply (Streamer Flush)** | `chunk_streaming.py:357` via `_flush_deferred_collisions` | **Unnötig teuer** — Worker-Solid reicht |
| **Sync-Load / Fallback** | `chunk_streaming.py:341` via `_ensure_procedural_decorations` | Legitim (Slow-Path) |
| **Navigation** | `world.py:257` via `ensure_collision_fresh` | Legitim, aber Scope zu breit |
| **Global rebuild all** | `world.py:251` `rebuild_all_solid` | Selten, O(C×D) |
| **Worker-Generierung** | `world_gen_context.py:112` `build_chunk_solid_grid` | Off-Main, chunk-lokal — **Referenz** |
| **Tests/Referenz** | `test_worker_apply`, `chunk_reference`, `test_collision` | Korrektheits-Baseline |
| **Benchmarks/Tools** | `benchmark_*.py` | Messung |

---

### 11. Warum ruft Navigation `ensure_collision_fresh()` in seiner heutigen Form auf?

#### Antwort

**Invariante:** Alle Chunks in `collision_dirty_chunks` haben ein aktuelles `solid_grid`, bevor `world_cell_solid` samplet.

**Call-Sites:** `navigation.py:74` (`mask_position_blocked`), `:163` (weitere Pfadfindung).

**Problem:** `ensure_collision_fresh` verarbeitet **alle** dirty Chunks, jeder Rebuild scannt **O(D)** `world.decorations` — ein einzelner User-Paint kann indirekt teuer werden.

**Engerer Scope möglich:** Nur Chunks rebuilden, die die Sample-Punkte der Maske berühren (1–2 Chunks typisch). Navigation muss nicht alle `collision_dirty_chunks` leeren.

**M24a:** Navigation **nicht** umbauen — nur sicherstellen, dass Worker-Apply **keine** dirty Marks hinterlässt (heute schon via `discard`).

---

### 12. Kann `rebuild_chunk_solid` selbst chunk-lokal werden?

#### Antwort

**Heute global wegen:**

```113:136:game_core/collision_grid.py
    for placed in world.decorations:
        ...
        if max_x <= chunk_origin_x or max_y <= chunk_origin_y:
            continue
        if anchor_x >= chunk_max_x or anchor_y >= chunk_max_y:
            continue
```

Bounding-Box-Filter ist chunk-aware, aber Iteration startet über **alle** D.

**Chunk-lokal möglich:** Parameter `decorations: Sequence[PlacedDecoration]` (wie `build_chunk_solid_grid` auf dem Worker).

**Cross-Chunk:** Große `CollisionMask` auf Deko kann benachbarte Chunks schneiden. Worker und Main-Referenz behandeln das über BBox-Clip — Nachbar-Chunk braucht **eigene** Deko/Maske, nicht den globalen Scan.

**Terrain:** Loop über 4096 Tiles via `world.get_tile` — chunk-lokal, O(4096).

---

## Block E – Streaming und Pool-Verhalten

### 13. Warum kosten Frames mit `stream_loaded = 0` trotzdem 15–17 ms?

#### Antwort

**Quelle:** Run `20260712T152006Z`, Frames 0–4 (`chunk_count=0`, `stream_loaded=0`).

| Komponente | ms (typ.) | Anteil |
|------------|-----------|--------|
| `apply_pool_ms` (submit + poll + `sync_active`) | **~7,8–8,1** | ~50 % von `stream_apply_ms` |
| Rest Apply (Revive, Sets, Sync-Loop ohne Load) | **~7,5–8,0** | ~50 % |
| `apply_worker_ms` / `apply_collision_ms` | **0** | — |
| `stream_unload_ms` | **~0,004** | vernachlässigbar |
| **`stream_ms` gesamt** | **~15,7–16,3** | |
| **`frame_ms` gesamt** | **~15,8–16,4** | fast nur Stream |

**Ursache Warte-Phase:** Pool submitted alle `wanted | prefetch` Coords (~Dutzende), Sync-Pfad blockiert via `pool.is_in_flight(coord)`, `poll_ready()` liefert noch nichts (Worker ~16 s Cold-Start). Jeder Frame: `discard_outside` + erneutes `submit` + `future.done()`-Polling über alle Futures.

**Nicht** Extract: `tile_extract_ms` ~0,02 ms in diesen Frames.

---

### 14. Wie kann der Pool sauber warm gestartet werden?

#### Antwort

| Maßnahme | Wo | Nutzen |
|----------|-----|--------|
| Explizites Warmup nach `configure_world_gen` / Demo-Start | `apps/chunk_world_demo.py`, Pool-Init | Prozesse + fBM-Cache vor erstem sichtbaren Frame |
| Warmup-Task: `generate_results_parallel([(0,0)])` | `chunk_gen_pool` / Demo | Entkoppelt Cold-Start vom Stream |
| Worker-Limit: `workers: 2` statt `"auto"` (19) | `world_gen.json` | Weniger Spawn-Overhead, stabilerer 64×64-Durchsatz |
| Lazy Pool: erst N Worker, rest on demand | größerer Umbau | Nicht M24a |

**Messung:** `worker_generate_chunk_result` 15987 ms inkl. 19-Prozess-Init (`single_chunk_64.json`); Apply danach 0,5 ms.

---

### 15. Welche In-Flight-/Prefetch-Regeln sind heute zu aggressiv?

#### Antwort

**Heute:**

- `submit_coords` = alle `wanted | prefetch` ohne In-Flight-Limit
- Kein `max_in_flight_chunks`
- Sync überspringt `in_flight` → **permanente Blockade** bis Worker fertig
- `prefetch_chunks: 2` in `streaming.json` — zusätzlich zu vollem `wanted`-Set

**Guardrail-Vorschläge:**

```python
MAX_IN_FLIGHT = 4  # config

# submit nur wenn under cap
if pool.in_flight_count() >= MAX_IN_FLIGHT:
    skip_submit

# sync fallback nach timeout
if pool.is_in_flight(coord) and pool.in_flight_age(coord) > SYNC_FALLBACK_MS:
    _load_chunk(...)  # notfall

# prefetch nur wenn wanted nicht komplett blockiert
if all(pool.is_in_flight(c) for c in wanted):
    prefetch = set()
```

---

## Block F – Tests und Sicherheit

### 16. Welche bestehenden Tests würden bei „kein Rebuild nach Worker-Apply“ brechen?

#### Antwort

| Test | Typ | Bei Flush-Skip |
|------|-----|----------------|
| `test_apply_chunk_result_matches_reference` | **Korrektheit** | **Bleibt grün** (testet Apply, nicht Streamer-Flush) |
| `test_apply_sets_no_dirty_chunks` | Korrektheit | Grün |
| `test_streaming_pool_uses_apply_not_populate` | Routing | Grün |
| `test_steady_update_does_not_rebuild_all_solids` | Verhalten | Grün (Rebuild=0 bei Steady-State) |
| `test_worker_solid` | Worker vs. Main | Grün |
| Tests mit explizitem Flush-Zähler | — | Keiner erzwingt Flush nach Worker |

**Anpassen:** ggf. neuer Test, der **Rebuild nach Worker-Apply = 0** assertiert (fehlt heute).

**conftest:** `parallel_worker_apply=False` — Streaming-Integrationstests laufen oft ohne Worker; M24a-Tests explizit mit `True`.

---

### 17. Welche neuen Tests braucht M24a zwingend?

#### Antwort

1. `test_streaming_worker_apply_skips_collision_flush` — Mock `rebuild_chunk_solid`, Pool liefert WORKER_COMPLETE → 0 Rebuilds  
2. `test_worker_solid_matches_after_streaming_apply` — solid_grid nach `update()` == Referenz  
3. `test_override_still_rebuilds_or_sync_path` — Override → kein Worker-Fast-Path  
4. `test_dirty_chunk_disables_worker_fast_path` — `dirty_chunks` → populate + rebuild  
5. `test_no_duplicate_procedural_deco_on_reapply` — Revive/Reload-Szenario  
6. `test_navigation_after_worker_apply_without_flush` — `mask_position_blocked` korrekt  

---

## Block G – konkrete Designentscheidung

### 18. Was ist der kleinste sichere erste Patch?

#### Antwort

| Schritt | Inhalt | Gewinn | Risiko |
|---------|--------|--------|--------|
| **1** | `can_apply_worker_complete_fast_path` nach `helpers/m24a_predicates.py` in `game_core` extrahieren | Klarheit | Minimal |
| **2** | Streamer: `deferred_collision_coords` nur wenn **nicht** Fast-Path | **Hoch (15–110 ms/Chunk)** | Gering — Tests 16/17 absichern |
| **3** | `apply_worker_complete_result` ohne `collision`, Batch-`extend` | Mittel (O(D×N)) | Gering |
| **4** | Pool: Sync-Fallback nach Timeout + `max_in_flight` | Fix „0 Chunks“ + Warte-Frames | Mittel |
| **5** | `decorations_by_chunk` | Hoch langfristig | **Zu groß für M24a** |

**Größtes Gewinn/Risiko-Verhältnis:** Schritt **2** allein.

---

### 19. Welche Änderung sollte explizit **nicht** Teil von M24a sein?

#### Antwort

- GPU-Worldgen / Compute-Shader-Terrain  
- Renderer-/Bridge-Extract-Umbau (`decorations_to_sprites`-Architektur)  
- M24 Persistenzformat v5 / Region-Codec (läuft parallel als M24, nicht M24a)  
- Deko-LOD / Sprite-System-Rewrites  
- Navigation-Architektur (breiter `ensure_collision_fresh`-Umbau)  
- Vollständiger `decorations_by_chunk`-Index  
- `CHUNK_SIZE`-Rollback oder Spawn/Start-Area-Redesign (separates Tuning)  

**M24a-Scope:** Worker-Complete-Fast-Path + Collision-Flush-Skip + optionale Apply-Vereinfachung + Pool-Guardrails.

---

## Erwartetes Ergebnis von Cursor

### 1. Priorisierte Hotspots

Siehe Zusammenfassung oben.

### 2. Guard-/Predicate-Spezifikation

`helpers/m24a_predicates.py` — bereit zur Integration in `game_core`.

### 3. Minimaler Patch-Plan

Schritte 1–2 (Pflicht), 3–4 (empfohlen), 5+ (später).

### 4. Abgrenzung M24a vs. Folgearbeit

| M24a | Später |
|------|--------|
| Kein Rebuild nach Worker-Apply | `decorations_by_chunk` |
| Apply Fast-Path | Extract O(D)-Fix |
| Pool Guardrails / Warmup | Navigation-Scope |
| Regression-Tests | Persistenz v5 |

---

## Hilfsmittel im Repo

```bash
# Call-Sites neu scannen
python helpers/m24a_scan.py

# Einzelchunk-Timing (64×64)
python tools/benchmark_single_chunk.py
```

- Report: `helpers/m24a_scan_report.json`  
- Benchmark: `docs/benchmarks/single_chunk_64.json`  
- Predicates: `helpers/m24a_predicates.py`
