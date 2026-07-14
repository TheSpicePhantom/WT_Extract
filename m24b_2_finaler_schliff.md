# M24b.2 — Finaler Schliff für Cursor

Ziel dieser Nachschärfung ist **nicht** mehr ein neuer Richtungswechsel, sondern der letzte saubere Schliff vor der Umsetzung. Der überarbeitete M24b-Plan ist bereits stark. Diese Datei definiert die **letzten offenen Präzisierungen**, damit beim Implementieren keine Interpretationsräume bleiben und keine versteckte Zusatzkomplexität in Scheduler, Apply oder Persistenz nachrutscht.

Der Plan soll danach als **umsetzungsreif** gelten.

---

## 1. BuildKey um Epoch-Grenze ergänzen

Der neue `BuildKey` ist ein großer Fortschritt. Was noch fehlt, ist eine explizite Epoch-Grenze für Pool-/World-/Streamer-Resets.

### Problem

Auch wenn `coord`, `terrain_revision`, `terrain_config_version` und `deco_config_version` gleich aussehen, kann ein Resultat aus einer **alten Worker-/Streaming-Epoche** stammen. Ohne explizite Epoch-Dimension muss diese Ungültigkeit später indirekt über Sonderfälle erkannt werden.

### Nachschärfung

Bitte `BuildKey` um eine Epoch-Komponente ergänzen.

```python
@dataclass(frozen=True)
class BuildKey:
    coord: tuple[int, int]
    terrain_revision: int
    terrain_config_version: int
    deco_config_version: int
    build_epoch: int
```

### Regel

`build_epoch` wird erhöht bei mindestens:

- Pool-Reset
- World-Reinitialisierung
- harter Streaming-Rekonfiguration
- explizitem Worker-Neustart

### Wirkung

Alle Resultate aus einer alten Epoch werden automatisch stale, ohne zusätzliche Sonderlogik in `can_apply_*` oder Revive-Pfaden.

---

## 2. `terrain_revision` an Submission-Grenze koppeln

Der Plan nennt bereits mehrere Fälle für neue `terrain_revision`. Das sollte noch präziser formuliert werden.

### Problem

Wenn `terrain_revision` erst bei Apply oder nur in ausgewählten Reload-Fällen erhöht wird, können konkurrierende Terrain-Jobs derselben Coord denselben Revisionsraum teilen.

### Nachschärfung

Bitte festhalten:

> **Jede neue Terrain-Submission, die nicht direkt dieselbe aktive Build-Linie fortsetzt, erzeugt eine neue `terrain_revision`.**

Das gilt insbesondere bei:

- erneutem Terrain-Submit nach Unload
- Terrain-Resubmit nach Stale/Discard
- Terrain-Neuaufbau nach Override-/Delta-Änderung
- Terrain-Neuaufbau nach Epoch-Wechsel

### Wirkung

Zwei konkurrierende Terrain-Linien für dieselbe Coord können nie denselben `BuildKey` erzeugen.

---

## 3. `TerrainStageData` und `ChunkFieldCache` als worker-lokale Daten festschreiben

Die neue Stage-API ist gut. Jetzt muss noch sauber definiert werden, welche Daten lokal bleiben und welche IPC-tauglich sind.

### Problem

Wenn nicht klar geregelt wird, ob `TerrainStageData` oder `ChunkFieldCache` Teil von Worker-Ergebnissen sein dürfen, besteht die Gefahr, dass aus Bequemlichkeit große oder nicht serialisierungssichere Strukturen durch den falschen Pfad geschoben werden.

### Nachschärfung

Bitte ausdrücklich festhalten:

- `TerrainResult` ist die einzige standardisierte Terrain-Nutzlast für Main/IPC.
- `TerrainStageData` ist eine **worker-lokale** Hilfsstruktur.
- `ChunkFieldCache` bleibt **immer worker-lokal** bzw. lokal im Sync-Durchlauf.
- `ChunkFieldCache` wird **nie** als Teil eines IPC-Results übertragen.

### Zielbild

```python
TerrainStageData
  - layer0
  - layer1
  - field_cache   # nur lokal
  - build_key

TerrainResult
  - build_key
  - layer0
  - layer1        # IPC-fähig
```

### Wirkung

Der Datenfluss bleibt klein, klar und serialisierungssicher. Cache-Sharing bleibt eine lokale Optimierung und wird nicht ungewollt Teil der öffentlichen Pipeline.

---

## 4. Beziehung zwischen `max_in_flight` und `parallelism_cap` fest definieren

Der Plan nutzt beide Konzepte sinnvoll, aber ihre Beziehung muss explizit werden.

### Problem

Ohne formale Definition könnten zwei halb überlappende Steuerungen entstehen:

- eine für "was wurde submitted"
- eine für "was läuft wirklich"

Das erhöht Scheduler-Komplexität und erschwert Telemetrie.

### Nachschärfung

Bitte definieren:

- `terrain_max_in_flight` / `deco_max_in_flight` = **alle** Jobs dieser Klasse, die submitted, running oder ready-but-not-applied sind.
- `terrain_parallelism_cap` / `deco_parallelism_cap` = gleichzeitig **aktiv laufende** Worker-Jobs dieser Klasse.

Zusätzliche Invarianten:

- `deco_max_in_flight <= terrain_max_in_flight`
- `deco_parallelism_cap < terrain_parallelism_cap`
- Defaults müssen diese Ordnung immer einhalten

### Wirkung

Die Konfiguration wird eindeutig, und Cursor kann Scheduler, Queue und Metriken sauber darauf ausrichten.

---

## 5. "Visible terrain pending" formal definieren

Der Scheduler nutzt bereits die richtige Schutzidee. Jetzt braucht der Begriff selbst noch eine scharfe Definition.

### Problem

"sichtbares Terrain wartet" kann unterschiedlich interpretiert werden:

- wanted, aber noch nicht submitted
- submitted, aber noch nicht running
- running, aber noch nicht ready
- ready, aber noch nicht applied

Wenn der Begriff schwammig bleibt, entstehen Abweichungen in Submit- und Backfill-Logik.

### Nachschärfung

Bitte den Begriff formal definieren als:

> `visible_terrain_pending = count(coords in wanted_visible where terrain_state != APPLIED)`

### Konsequenzen

Solange `visible_terrain_pending > 0` gilt:

- kein Prefetch-Deco
- kein Deco-Backfill
- sichtbare Deco nur innerhalb `deco_parallelism_cap`
- kein aggressives Nachziehen von Deco außerhalb der sichtbaren Prioritätsklasse

### Wirkung

Die Schutzregel wird deterministisch und leicht testbar.

---

## 6. Persistenzmarker für Terrain-only / Deco-incomplete ergänzen

Der Terrain-only-Vertrag ist gut, aber für Persistenz fehlt noch ein expliziter Marker.

### Problem

Wenn ein Chunk unloaded oder gespeichert wird, während Terrain bereits applied ist, Deco aber noch fehlt, muss beim Revive klar unterscheidbar bleiben:

- Deko fehlt absichtlich nicht,
- Deko ist nur noch nicht fertig gewesen.

Ohne Marker droht implizite Heuristik.

### Nachschärfung

Bitte in M24b festhalten:

- Terrain-only-Chunks erhalten beim Unload/Persist einen expliziten Statusmarker, z. B. `deco_incomplete = true`.
- Beim Revive bedeutet dieser Marker:
  - Terrain-Basis ist gültig oder neu generierbar,
  - Deco muss neu angefordert oder neu bewertet werden,
  - es wird **keine** prozedurale Deco-Persistenz aus dem unvollständigen Zustand konstruiert.

### Wirkung

M24b bleibt sauber kompatibel zur M24-Persistenzlogik, ohne Terrain-only-Zustände zu verschleiern.

---

## 7. `apply_deco_stage` als Single-Writer pro `BuildKey`

Der Plan beschreibt `apply_deco_stage` bereits als keinen Reparaturpfad. Das sollte noch um eine Single-Writer-Regel ergänzt werden.

### Nachschärfung

Bitte festhalten:

> Pro Coord darf pro aktivem `BuildKey` genau **ein** erfolgreicher `apply_deco_stage` stattfinden.

Jeder weitere `DecoResult` mit demselben aktiven `BuildKey` ist:

- Duplicate,
- Race-Nachzügler,
- oder Scheduler-/Worker-Fehler,

und wird verworfen sowie metrisch erfasst.

### Empfohlene Metrik

- `deco_discarded_duplicate`

### Wirkung

Das schützt gegen doppelte Deko-Applies ohne neue Locking-Komplexität.

---

## 8. Stabile Reihenfolge für `CompiledDecoPass`

Die Config ist jetzt sinnvoll datengetrieben. Was noch fehlt, ist eine klare Determinismus-Regel für gleiche Prioritäten.

### Problem

Wenn zwei Pässe dieselbe Priority haben und die Reihenfolge nicht explizit stabil ist, können kleine Config-Änderungen oder Parser-Details zu nicht deterministischen Deco-Ergebnissen führen.

### Nachschärfung

Bitte die Evaluierungsreihenfolge eindeutig definieren, z. B.:

```python
sort_key = (priority, declaration_order, pass_name)
```

oder eine äquivalente stabile Ordnung.

### Wirkung

Gleiche Inputs erzeugen gleiche Deco-Ergebnisse. Das ist wichtig für Debugging, Persistenzvertrauen und Golden-Tests.

---

## 9. Duplicate-Apply-Test ergänzen

Die Failure-Modes sind bereits stark. Ein kleiner, aber wichtiger Test fehlt noch.

### Pflichtfall zusätzlich

Bitte in `tests/test_m24b_pipeline.py` ergänzen:

- `DecoResult` mit demselben aktiven `BuildKey` trifft zweimal ein
- erster Apply erfolgreich
- zweiter Apply verworfen
- `deco_discarded_duplicate` wird erhöht

### Wirkung

Dieser Test sichert die Single-Writer-Regel praktisch ab.

---

## 10. Eine Terrain-Warte-Metrik ergänzen

Die vorhandenen Metriken sind gut. Für die Bewertung des Schedulers wäre noch eine direkt sichtbare Terrain-Druck-Metrik hilfreich.

### Nachschärfung

Bitte mindestens eine der folgenden Metriken ergänzen:

- `visible_terrain_wait_frames`
- `terrain_submit_skipped_worker_saturation`
- oder eine äquivalente Kennzahl für sichtbaren Terrain-Druck

### Wirkung

Später lässt sich nicht nur sehen, dass Deco gebremst wurde, sondern auch, ob Terrain trotz Caps noch unnötig warten musste.

---

# Konkrete Anweisung an Cursor

Bitte den M24b-Plan vor Implementierung noch um diese Punkte ergänzen:

1. `BuildKey.build_epoch`
2. `terrain_revision` eindeutig an neue Terrain-Submission koppeln
3. `TerrainStageData`/`ChunkFieldCache` als worker-lokal festschreiben
4. `max_in_flight` vs. `parallelism_cap` formal definieren
5. `visible_terrain_pending` exakt definieren
6. Persistenzmarker `deco_incomplete` für Terrain-only-Zustände
7. Single-Writer-Regel für `apply_deco_stage`
8. stabile Sortierung für `CompiledDecoPass`
9. Duplicate-Apply-Test
10. zusätzliche Terrain-Druck-Metrik

---

# Freigabekriterium

Wenn diese zehn Punkte sauber eingearbeitet sind, sollte M24b als **umsetzungsreif** gelten:

- klare Zustände,
- klarer Datenfluss,
- begrenzte Cache-Lebensdauer,
- robuster Scheduler,
- deterministische Deco-Pipeline,
- keine stillen Race- oder Persistenzlücken.
