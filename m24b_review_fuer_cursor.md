# Review für Cursor — M24b Terrain/Deco Split nachschärfen

Ziel dieser Review ist, **offene Schwachstellen vor der Umsetzung zu schließen** und M24b so zu präzisieren, dass die Architektur **leistungsfähig bleibt, ohne unnötig komplex zu werden**.

Der aktuelle Plan ist in der Grundrichtung gut: Terrain und Deco werden getrennt, Deko darf Terrain nicht vorauslaufen, Cache-Sharing ist vorgesehen, und ein zweiter Pool bleibt optional. Genau diese Richtung soll beibehalten werden. Was noch fehlt, ist die **harte Definition der Verträge, Zustände, Invalidation-Regeln und Scheduler-Grenzen**. Ohne diese Präzisierungen drohen später stille Stale-Result-Fehler, Queue-Churn, Worker-Speicherdrift und zusätzliche Sonderlogik im Streamer.

---

## 1. ChunkBuildState präzisieren

Der aktuelle `ChunkBuildState` mit nur `TERRAIN_ONLY | DECO_PENDING | DECO_APPLIED` ist zu grob.

### Problem

Mit nur drei Stufen werden mehrere reale Laufzeitzustände vermischt:

- Terrain noch gar nicht submitted
- Terrain in flight
- Terrain fertig, aber noch nicht applied
- Terrain applied, Deco noch nicht submitted
- Deco in flight
- Deco fertig, aber stale
- Deco bewusst unterdrückt wegen Dirty/Override/User-Deko

Wenn diese Fälle nicht explizit modelliert werden, landet die Entscheidung später verteilt in:

- Streamer-Update-Loop
- Pool-Submit-Logik
- Apply-Guards
- Revive-/Unload-Pfad
- Dirty-/Override-Prüfungen

Das erhöht die tatsächliche Komplexität, obwohl das Zustandsmodell nach außen klein wirkt.

### Nachschärfung

Bitte `ChunkBuildState` nicht als einzelnes grobes Stage-Enum belassen, sondern minimal explizit aufteilen in:

```python
class TerrainState(Enum):
    EMPTY = auto()
    IN_FLIGHT = auto()
    APPLIED = auto()

class DecoState(Enum):
    NONE = auto()
    IN_FLIGHT = auto()
    APPLIED = auto()
    SUPPRESSED = auto()
```

Zusätzlich im State:

```python
@dataclass
class ChunkBuildState:
    terrain_build_key: BuildKey | None
    terrain_state: TerrainState
    deco_state: DecoState
    deco_suppression_reason: str | None = None
```

### Warum das besser ist

- `DECO_SUPPRESSED` verhindert, dass der Scheduler jeden Frame erneut versucht, Deco für ungeeignete Chunks zu submitten.
- Terrain- und Deco-Zustand bleiben getrennt, ohne dass ein komplexer Gesamtzustandsautomat gebaut werden muss.
- Revive, Unload und stale discards lassen sich lokal und deterministisch entscheiden.

### Konkrete Regel

`DECO_SUPPRESSED` ist zu setzen bei mindestens:

- `dirty_chunks`
- `persistent_overrides`
- `persistent_deltas`
- User-Deko im Chunk
- `pending_unload`
- Chunk nicht mehr wanted, bevor Deco submitted wurde

### Erwartete Änderung im Plan

Phase 0 muss den State explizit in **Terrain-State + Deco-State + Suppression** aufteilen, statt nur `stage: TERRAIN_ONLY | DECO_PENDING | DECO_APPLIED` zu verwenden.

---

## 2. Revision durch BuildKey ersetzen oder präzisieren

Der Plan spricht von einer monoton steigenden Revision pro Coord. Das ist als Anfang brauchbar, aber noch nicht präzise genug.

### Problem

Eine bloße numerische Revision ist nur dann sicher, wenn exakt definiert ist, **was** eine neue Revision auslöst. Wenn Terrain formal „dieselbe Coord“ ist, aber sich Build-Inputs geändert haben, können Deco-Results fälschlich als gültig erscheinen.

Gefährliche Quellen für stille Mismatches:

- geänderte Terrain-Config
- geänderte Deco-Config
- geänderte Content-Definitionen
- andere Build-Epoche nach Reload/Reset
- andere Terrain-Parameter, obwohl Coord gleich bleibt

### Nachschärfung

Bitte entweder den Begriff Revision exakt definieren oder besser direkt einen `BuildKey` verwenden.

Minimalvorschlag:

```python
@dataclass(frozen=True)
class BuildKey:
    coord: tuple[int, int]
    terrain_revision: int
    terrain_config_version: int
    deco_config_version: int
    content_version: int
```

Wenn `content_version` zu viel ist, kann sie für M24b noch entfallen. Aber `terrain_revision` + Config-Versionen sollten klar mitgedacht werden.

### Apply-Regel

`DecoResult` darf **nur** dann applied werden, wenn sein `build_key` exakt zum aktuellen `ChunkBuildState.terrain_build_key` passt.

Keine weiche Logik, kein teilweises Matching, kein „Coord passt schon“. Exakt oder discard.

### Erwartete Änderung im Plan

Phase 0 und Phase 3 müssen statt „terrain_revision matcht“ formulieren:

- `TerrainResult` erzeugt aktuellen `BuildKey`
- `ChunkBuildState` speichert diesen `BuildKey`
- `DecoResult` trägt denselben `BuildKey`
- `can_apply_deco_result` vergleicht auf **exakte Gleichheit**

---

## 3. Cache-Sharing hart begrenzen

Phase 2 ist wahrscheinlich der wichtigste Performance-Hebel des gesamten Plans. Gleichzeitig ist sie die Stelle mit dem größten Risiko für versteckte Komplexität und Speicherdrift.

### Problem

`_worker_field_caches: dict[coord, ChunkFieldCache]` im Worker-Kontext klingt einfach, kann aber schnell ausufern:

- Terrain-Jobs laufen vor
- Deco wird später nicht mehr gebraucht
- Chunks werden stale oder unwanted
- Caches bleiben trotzdem im Worker liegen

Dann wird aus einer Performance-Optimierung ein stiller Speicherhalter mit schwer nachvollziehbarer Lebensdauer.

### Nachschärfung

Bitte **keinen unbounded Coord→Cache Speicher** einführen.

Stattdessen:

- pro Worker nur eine kleine bounded Struktur
- bevorzugt FIFO oder LRU
- Größe hart begrenzen, z. B. `terrain_max_in_flight + 2`
- Eintrag sofort verwerfen bei:
  - Deco consumed
  - stale BuildKey
  - Coord nicht mehr relevant
  - Worker-Epoch-Wechsel / Reset

Beispiel:

```python
_worker_field_cache_lru: OrderedDict[BuildKey, ChunkFieldCache]
MAX_SHARED_FIELD_CACHES = 8
```

### Pflicht-Metriken

Phase 2 muss Metriken ergänzen:

- `field_cache_hits`
- `field_cache_misses`
- `field_cache_evictions`
- `field_cache_live_count`

Ohne diese Metriken kann später niemand sehen, ob das Sharing überhaupt wirkt oder nur Speicher bindet.

### Erwartete Änderung im Plan

Phase 2 muss den Cache-Lebenszyklus explizit definieren und eine harte Obergrenze enthalten. Kein offener Dict-Speicher ohne Eviction-Regeln.

---

## 4. Ein Pool mit zwei Jobtypen reicht nur mit harter Laufzeitbegrenzung für Deco

Der Plan will zurecht **nicht sofort** einen zweiten ProcessPool bauen. Das ist gut. Aber Priorität allein reicht nicht, wenn bereits laufende Deco-Jobs CPU-Zeit blockieren.

### Problem

Priorisierte Queues helfen nur beim Start neuer Jobs. Ein langer laufender Deco-Job kann trotzdem sichtbares Terrain verzögern, wenn alle Worker belegt sind.

### Nachschärfung

Bitte in Phase 4 schon im Ein-Pool-Modell eine faktische Trennung der Laufzeit erzwingen:

- `terrain_parallelism_cap`
- `deco_parallelism_cap`
- sichtbares Terrain immer zuerst
- Prefetch-Deco nur bei freier Restkapazität

Minimalregel:

```python
visible_terrain > visible_deco > prefetch_terrain > prefetch_deco
```

Und zusätzlich:

- `deco_parallelism_cap` klein halten, z. B. 1 oder 2
- neue Deco-Jobs nur starten, wenn nicht bereits sichtbares Terrain auf Ausführung wartet

### Wichtige Aussage

Das ist **noch kein echter zweiter Pool**, aber es emuliert bereits die gewünschte Schutzwirkung gegen Terrain-Starvation — ohne zusätzliche Infrastruktur.

### Erwartete Änderung im Plan

Phase 4 muss nicht nur `terrain_max_in_flight` und `deco_max_in_flight` nennen, sondern explizit festhalten:

1. **Prioritätsklassen**
2. **Startregeln** für Jobs
3. **kleines Deco-Parallelitätslimit**
4. Terrain darf durch laufende oder wartende Deco-Arbeit nicht spürbar blockiert werden

Wenn diese Regeln nicht ausreichen, **erst dann** Phase 4b mit echtem zweitem Pool.

---

## 5. Deco darf nicht nur „nicht vor Terrain applyen“ — Deco darf auch nicht zu früh submitten

Der Plan formuliert gut, dass Deco Terrain nicht vorauslaufen darf. Das sollte aber strenger formuliert werden.

### Problem

Wenn Deco zwar erst nach Terrain **applied** wird, aber bereits früh in großen Mengen **submitted** oder **running** ist, kann es trotzdem sichtbares Terrain indirekt ausbremsen.

### Nachschärfung

Bitte die Regel im Plan verschärfen:

> Deco darf Terrain weder beim Apply **noch bei der CPU-Belegung** vorauslaufen.

Daraus folgen klare Scheduler-Regeln:

- Kein Deco-Submit ohne `terrain_state == APPLIED`
- Kein Prefetch-Deco, solange sichtbares Terrain aussteht
- Kein Deco-Backfill bei Terrain-Stau
- Kein Deco-Resubmit für `SUPPRESSED`-Chunks

### Erwartete Änderung im Plan

Phase 4 sollte nicht nur `deco_submit_only_after_terrain` haben, sondern zusätzlich:

```json
{
  "deco_only_after_terrain_applied": true,
  "deco_pause_when_visible_terrain_pending": true,
  "prefetch_deco_only_when_idle": true
}
```

Die konkreten Namen können anders heißen, aber die Regeln müssen ausdrücklich in Plantext und Scheduler-Vertrag stehen.

---

## 6. Terrain-only-Zwischenzustand semantisch definieren

Der Plan akzeptiert Terrain ohne Deko bewusst. Das ist gut, aber der Zwischenzustand muss genauer beschrieben werden.

### Problem

Wenn „Terrain-only“ nur locker beschrieben wird, muss später jedes Subsystem selbst raten, was das bedeutet. Dadurch wächst Streulogik.

### Nachschärfung

Bitte in Phase 3 explizit festhalten, welche Systeme Terrain-only sehen dürfen und welche nicht:

- `render`: darf Terrain-only immer anzeigen
- `navigation`: darf Terrain-only gegen Tile-Walkability auswerten
- `interaction`: darf keine prozedurale Deko erwarten
- `harvest/loot/tree-hit`: dürfen Terrain-only-Chunks nicht gegen fehlende Deko auswerten
- `save/persist`: Terrain-only erzeugt keine prozedurale Deco-Persistenz
- `revive/unload`: Terrain-only zählt als unvollständiger Chunk und darf Deco später neu anfordern

### Erwartete Änderung im Plan

Unter „Collision-Strategie“ bzw. in Phase 3 muss nicht nur Navigation erwähnt werden, sondern ein kleiner **Semantik-Vertrag Terrain-only** für Render, Navigation, Interaction und Persistenz.

---

## 7. `apply_deco_result` enger definieren

### Problem

Der Plan beschreibt `apply_deco_result` als Batch-Append von Deko plus `solid_grid` setzen. Das ist richtig für prozedurale, unveränderte Chunks. Es muss aber glasklar ausgeschlossen werden, dass dieser Pfad auf Chunks mit Override-/Dirty-/User-Zustand angewendet wird.

Sonst wächst `apply_deco_result` später um immer mehr Sonderregeln und verliert seinen Fast-Path-Charakter.

### Nachschärfung

Bitte im Plan ausdrücklich festhalten:

`apply_deco_result` ist **nur** zulässig für Chunks, die:

- keine `dirty_chunks`-Markierung haben
- keine `persistent_overrides` haben
- keine `persistent_deltas` haben
- keine User-Deko enthalten
- nicht `pending_unload` sind
- denselben `BuildKey` tragen

Trifft einer dieser Fälle nicht zu, wird `DecoResult` **nicht angewendet**, sondern verworfen oder gar nicht erst submitted.

### Wichtig

Die Architektur soll hier **früh suppressen statt spät reparieren**.

### Erwartete Änderung im Plan

Phase 0/3/4 müssen klar zwischen:

- `submit_deco_allowed(...)`
- `can_apply_deco_result(...)`

unterscheiden.

`submit_deco_allowed` soll bereits die meisten Problemfälle blocken, damit `can_apply_deco_result` nur noch Integrität und Staleness absichert.

---

## 8. APIs reduzieren statt vermehren

### Problem

Der Plan führt mehrere neue Begriffe ein:

- `generate_terrain_result`
- `generate_deco_result`
- `generate_chunk_result`
- `generate_chunk_with_cache`
- `populate_chunk_decorations`
- `_ensure_procedural_decorations`

Wenn alle parallel „offiziell“ bleiben, steigt die mentale Komplexität trotz besserer Trennung.

### Nachschärfung

Bitte eine **kleine Zieloberfläche** definieren und Altpfade nur noch adaptieren.

Beispiel:

```python
build_terrain_stage(coord, ctx) -> TerrainStageData
build_deco_stage(coord, terrain_stage_data, ctx) -> DecoStageData
apply_terrain_stage(world, result, content)
apply_deco_stage(world, result, content)
```

Dann:

- `generate_chunk_result` bleibt nur Compat-Wrapper
- `populate_chunk_decorations` bleibt Slow-Path-Helfer, aber nicht mehr Primär-API
- `_ensure_procedural_decorations` bleibt Fallback, nicht Referenzpfad

### Erwartete Änderung im Plan

Phase 1 sollte nicht nur splitten, sondern explizit sagen, welche API nach M24b die **kanonische** ist.

---

## 9. Config-getriebene Deco bitte datengetrieben, nicht DSL-artig

Die Richtung „schönere, einfachere Gestaltung von Deco-Generierung, mit Config“ ist sehr gut. Hier liegt aber ein großes Risiko, wenn zu früh eine kleine Regelsprache entsteht.

### Problem

Ein generisches `rules[]`-System klingt elegant, kann aber die Logik nur aus Python in JSON verschieben. Dann wird Debugging schwieriger, Laufzeit langsamer und Komplexität faktisch höher.

### Nachschärfung

Bitte M24b-Config auf **Datenparameter** begrenzen.

Geeignet für M24b:

- `name`
- `enabled`
- `priority`
- `biomes`
- `allowed_ground_tiles`
- `density` / `chance`
- `noise_threshold`
- `height_min` / `height_max`
- `variants`
- `collision_profile`

Nicht Teil von M24b:

- verschachtelte Bool-Expressions
- frei kombinierbare Rule-Trees
- kleine Scripting- oder Formula-Sprache
- generische Prioritätsarithmetik

### Zusatz

Die Config sollte beim Laden in eine kompakte Runtime-Form kompiliert werden:

```python
CompiledDecoPass
```

Kein wiederholtes Interpretieren von JSON-Feldern pro Chunk.

### Erwartete Änderung im Plan

Phase 5 sollte ausdrücklicher sagen:

- M24b führt **keine** allgemeine Deco-DSL ein
- JSON wird beim Laden vorvalidiert und kompiliert
- Ziel ist bessere Lesbarkeit und Parametrierung, nicht maximale Ausdrucksstärke

---

## 10. Stale- und Discard-Pfade messbar machen

### Problem

Der Plan erwähnt stale discards, aber ohne gute Metriken ist später unklar, ob das System gesund arbeitet oder viel Arbeit wegwirft.

### Nachschärfung

Bitte folgende Metriken verpflichtend ergänzen:

- `terrain_submitted`
- `terrain_applied`
- `terrain_discarded_stale`
- `deco_submitted`
- `deco_applied`
- `deco_discarded_stale`
- `deco_suppressed`
- `deco_submit_skipped_visible_terrain_pressure`
- `field_cache_hits`
- `field_cache_misses`
- `field_cache_evictions`

Zusätzlich abgeleitete Kennzahlen im Benchmark oder Logging:

- `deco_stale_ratio`
- `terrain_visible_time_to_first_apply`
- `deco_lag_after_terrain_apply`

### Erwartete Änderung im Plan

Phase 4 und Benchmark-Abschnitt müssen diese Metriken als festen Teil des DoD aufnehmen.

---

## 11. Failure-Mode-Tests erweitern

Der aktuelle Testblock ist gut, aber noch nicht tief genug für die gefährlichen Übergänge.

### Nachschärfung: Pflichtfälle

Bitte in `tests/test_m24b_pipeline.py` zusätzlich abdecken:

1. Terrain applied, Deco in flight, Chunk wird unwanted, Deco kommt später zurück → discard.
2. Terrain applied, Chunk unloaded, gleicher Coord später neu wanted → neuer BuildKey, altes Deco discard.
3. Terrain applied, User modifiziert Chunk, altes DecoResult kommt an → suppress/discard.
4. Prefetch-Terrain fertig, sichtbares Terrain wartet noch → Deco darf nicht CPU-Budget auffressen.
5. Cache vorhanden, Deco wird nie konsumiert → Cache-Eviction greift.
6. Terrain-only-Chunk wird gespeichert/unloaded/revived → keine inkonsistente prozedurale Deco-Persistenz.

### Erwartete Änderung im Plan

Phase 0/3/4-Testliste bitte um diese Failure-Modes erweitern. Gerade diese Fälle sichern, dass nicht später zusätzliche Spezialpfade nötig werden.

---

## 12. Definition of Done schärfen

Der bisherige DoD ist gut, aber für Performance noch zu weich.

### Nachschärfung

Bitte DoD um harte Aussagen ergänzen:

- sichtbares Terrain erscheint früher oder mindestens nicht später als in M24a
- Deco-Tasks blockieren sichtbares Terrain nicht spürbar
- `build_chunk_field_cache` wird pro Chunk-Basis höchstens einmal gebaut
- Worker-Caches sind bounded und haben dokumentierte Eviction-Regeln
- `deco_stale_ratio` bleibt in normaler Bewegung niedrig
- Main-Thread-Apply bleibt mindestens so günstig wie M24a-Fast-Path
- keine neuen globalen O(D)-Scans im Terrain/Deco-Hotpath

### Wichtig

Der Erfolg von M24b ist nicht nur „sauberer Code“, sondern:

1. Terrain ist früher sichtbar,
2. Deco zieht kontrolliert nach,
3. Fast-Paths bleiben klein,
4. kein stiller Anstieg von Queue-, Cache- oder State-Komplexität.

---

# Konkrete Aufforderung an Cursor

Bitte den M24b-Plan vor Umsetzung wie folgt nachziehen:

1. `ChunkBuildState` in getrennte Terrain-/Deco-Zustände plus `DECO_SUPPRESSED` aufteilen.
2. `terrain_revision` durch einen klar definierten `BuildKey` präzisieren oder ersetzen.
3. Cache-Sharing nur mit bounded Lifetime und Eviction-Regeln einführen.
4. Ein-Pool-Scheduler um harte Prioritätsklassen und kleines `deco_parallelism_cap` ergänzen.
5. Regel verschärfen: Deco darf Terrain weder beim Apply noch bei CPU-Belegung vorauslaufen.
6. Terrain-only-Semantik für Render, Navigation, Interaction und Persistenz explizit festhalten.
7. `submit_deco_allowed(...)` und `can_apply_deco_result(...)` getrennt definieren.
8. Eine kleine kanonische Stage-API benennen; Altpfade nur adaptieren.
9. Deco-Config strikt datengetrieben halten; keine Mini-DSL in M24b.
10. Stale-/Discard-/Cache-Metriken verpflichtend machen.
11. Failure-Mode-Tests für Unload, Revive, Suppression und Cache-Eviction ergänzen.
12. DoD um harte Performance- und Komplexitätsgrenzen erweitern.

---

# Zielbild

Wenn diese Nachschärfungen im Plan landen, bleibt M24b:

- architektonisch sauber,
- für Cursor klar aufspaltbar,
- performant im sichtbaren Terrain-Pfad,
- robust gegen stale Deco-Arbeit,
- und deutlich einfacher weiterzuentwickeln als ein halb getrennter Monolith.
