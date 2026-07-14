# M24b.3 — Final Review vor Umsetzung

Ziel dieses Dokuments ist nicht mehr ein Architektur-Umbau, sondern der letzte präzise Review-Schliff vor der eigentlichen Implementierung. M24b ist inhaltlich weitgehend umsetzungsreif; die folgenden Punkte sollen nur noch Ownership, Invarianten und Failure-Modes so scharf machen, dass Cursor beim Einbau keine Interpretationsspielräume mehr hat.

## 1. `build_epoch` eindeutig verorten

Bitte im Plan und idealerweise bereits in der Zielstruktur festnageln:

- Wer **besitzt** `build_epoch`?
- Wer darf sie **erhöhen**?
- Wer darf sie **nur lesen**, aber nicht verändern?

Empfohlene Zuspitzung:

- `ChunkGenPool` oder ein klar benannter Streaming-/Build-Koordinator ist die **einzige Quelle** für `build_epoch`.
- `chunk_streaming`, `worker_fast_path`, Apply-Pfade und Result-Typen **konsumieren** `build_epoch`, erzeugen sie aber nicht selbst.
- Ein Epoch-Wechsel darf nur auf klaren Systemereignissen passieren: Pool-Reset, Worker-Neustart, World-Reinit, harte Streaming-Rekonfiguration.

Warum das wichtig ist:

Sobald mehrere Stellen Epochs lokal erhöhen oder „vorsichtshalber“ neu setzen, ist der Vertrag kaputt. Dann entstehen schwer sichtbare Bugs, bei denen gültige Results unnötig stale wirken oder alte Results versehentlich doch akzeptiert werden.

### Konkrete Frage an Cursor

- In welchem Modul lebt die kanonische `build_epoch`?
- Wie wird sie in `BuildKey` injiziert?
- Wie wird verhindert, dass Streamer oder Apply-Code eigene Epoch-Werte erzeugen?

---

## 2. `can_apply_terrain_result(...)` genauso hart definieren wie Deco

Im aktuellen Plan ist `can_apply_deco_result(...)` bereits sehr klar. Für Terrain sollte dieselbe Schärfe explizit dokumentiert werden.

Bitte ergänzen:

- Wann ist ein `TerrainResult` stale?
- Wann darf ein Terrain-Result trotz passender Coord **nicht** mehr applied werden?
- Wie verhält sich Terrain bei Unload/Revive/Race zwischen alter und neuer Build-Linie?

Empfohlene Regeln:

- `TerrainResult.build_key` muss exakt zum aktiven erwarteten Terrain-Build der Coord passen.
- Wenn zwischen Submit und Poll bereits eine neue Terrain-Linie gestartet wurde, ist das alte Result stale.
- Results aus alter `build_epoch` werden immer verworfen.
- Ein Terrain-Result darf keinen bestehenden neueren Build überschreiben, selbst wenn der Chunk aktuell wieder wanted ist.

### Konkrete Frage an Cursor

Bitte `can_apply_terrain_result(...)` als gleichwertigen Vertrag zu `can_apply_deco_result(...)` ausformulieren, inklusive mindestens 2 Failure-Modes:

1. altes TerrainResult kommt nach Resubmit zurück,
2. TerrainResult aus alter Epoch kommt nach Pool-Reset zurück.

---

## 3. `max_in_flight` vs. `parallelism_cap` mit Beispiel festziehen

Die Definition ist bereits gut, aber für Implementierende hilft ein kleines, glasklares Beispiel.

Bitte im Plan ergänzen:

- `max_in_flight` umfasst submitted + running + ready-but-not-applied.
- `parallelism_cap` umfasst nur tatsächlich laufende Worker-Jobs.
- Ready-Queues zählen weiter gegen `max_in_flight`, bis das Result konsumiert oder verworfen wurde.

Beispiel:

- `terrain_max_in_flight = 8`
- `terrain_parallelism_cap = 6`
- 6 Terrain-Jobs laufen gerade
- 2 Terrain-Results sind bereits fertig, aber noch nicht applied
- Dann dürfen **keine weiteren** Terrain-Submits erfolgen, obwohl nur 6 Jobs wirklich CPU belegen

Warum das wichtig ist:

Ohne dieses Beispiel implementieren Leute oft unbewusst zwei verschiedene Zählweisen in Pool und Streamer. Das führt später zu Queue-Aufblähung oder ungewolltem Starvation-Verhalten.

### Konkrete Frage an Cursor

Bitte eine kleine Scheduler-Notiz oder ein Mini-Beispiel in den Plan aufnehmen, das diese Zählweise verbindlich macht.

---

## 4. Ownership der Ready-/Discard-Pfade klären

Der Plan ist stark, aber Cursor sollte noch einmal explizit festlegen:

- Wer entfernt Results aus Ready-Queues?
- Wer zählt `discarded_stale` bzw. `discarded_duplicate` hoch?
- Wer räumt zugehörige worker-lokale Cache-Einträge ab?

Empfohlene Richtung:

- Poll/Router-Schicht entscheidet über consume vs. discard.
- Apply-Schicht verändert World-State nur bei bereits positivem Guard.
- Cache-Cleanup hängt an discard/consume-Ereignissen mit klarem Besitzmodell.

Warum das wichtig ist:

Wenn mehrere Schichten „vorsichtshalber“ discarden oder cleanupen, entstehen Doppelzählungen, Cache-Leaks oder schwer reproduzierbare Zustände.

### Konkrete Frage an Cursor

Bitte in 3–5 Sätzen festhalten, welche Schicht Owner ist für:

- Ready-Result-Konsum,
- Stale-Discard,
- Duplicate-Discard,
- LRU-Cleanup.

---

## 5. `deco_incomplete` im Persistenzpfad einmal end-to-end beschreiben

Die Idee ist richtig und wichtig. Für die Umsetzung fehlt nur noch eine kurze End-to-End-Beschreibung.

Bitte konkretisieren:

- Wo wird `deco_incomplete = true` gesetzt?
- Bleibt der Marker nur im Pending-Unload-Zustand oder auch im persistierten Chunk-State sichtbar?
- Wann und wodurch wird `deco_incomplete` wieder aufgelöst?
- Welche Pfade dürfen aus einem `deco_incomplete`-Chunk **keine** prozedurale Deko rekonstruieren?

Empfohlene Lesart:

- Terrain-only-Unload markiert den Chunk explizit als unvollständig.
- Revive lädt Terrain-Basis bzw. Delta, aber behandelt prozedurale Deko weiterhin als offen.
- Erst ein erfolgreicher `apply_deco_stage` für den aktiven `BuildKey` entfernt diesen Zustand.

### Konkrete Frage an Cursor

Bitte einen Mini-Ablauf mit 4 Schritten ergänzen:

1. Terrain applied, Deco fehlt.
2. Chunk unload/persist.
3. Chunk revive/reload.
4. Deco wird neu angefordert und erst danach als vollständig betrachtet.

---

## 6. Single-Writer-Regel testseitig doppelt absichern

Die Regel „pro Coord und aktivem `BuildKey` genau ein erfolgreicher `apply_deco_stage`“ ist sehr gut. Für die Praxis sollte Cursor noch festlegen, wie diese Regel sowohl logisch als auch testseitig abgesichert wird.

Bitte ergänzen:

- Welche minimale Zustandsmarke zeigt an, dass für den aktiven `BuildKey` Deco bereits erfolgreich applied wurde?
- Reicht `deco_state == APPLIED`, oder braucht es zusätzlich den letzten erfolgreich angewandten `BuildKey`?
- Wie wird verhindert, dass ein verspätetes identisches Result unbemerkt durchrutscht?

Empfohlene Richtung:

- Entweder `deco_state == APPLIED` plus identischer aktiver `BuildKey` genügt,
- oder ein explizites Feld wie `last_applied_deco_build_key` macht den Vertrag noch robuster.

### Konkrete Frage an Cursor

Bitte entscheiden und im Plan festhalten, welche Zustandsinformation für Duplicate-Erkennung die kanonische Quelle ist.

---

## 7. `CompiledDecoPass`-Determinismus nicht nur sortieren, sondern testen

Die stabile Sortierung nach `(priority, declaration_order, pass_name)` ist richtig. Der letzte Schliff ist hier vor allem testseitig.

Bitte ergänzen:

- Ein Test, dass gleiche Inputs trotz mehrfacher Config-Lade-Reihenfolge dieselbe Pass-Reihenfolge ergeben.
- Ein Test, dass `deco_config_version` vom kompilierten, sortierten Zustand abhängt und nicht vom zufälligen Einlesepfad.

Warum das wichtig ist:

Determinismus ist hier nicht nur ein „nice to have“, sondern Grundlage für Golden-Tests, Persistenz und reproduzierbares Debugging.

### Konkrete Frage an Cursor

Bitte zwei kleine Determinismus-Tests für `CompiledDecoPass` ergänzen:

1. stabile Ausführungsreihenfolge,
2. stabiler Config-Hash.

---

## 8. DoD um zwei Mini-Punkte ergänzen

Die Definition of Done ist schon stark. Ich würde nur noch zwei kleine explizite Punkte ergänzen:

- **Klare Ownership dokumentiert** für Epoch, Ready-Queues, Discard und Cache-Cleanup.
- **Terrain-Apply-Vertrag gleich scharf wie Deco-Apply-Vertrag** dokumentiert und getestet.

Diese beiden Punkte sind keine neue Architektur, sondern schließen die letzten Interpretationslücken.

---

## Empfohlene Freigabeformulierung

Wenn Cursor die obigen Punkte ohne größeren Architekturumbau sauber in den Plan integriert, ist M24b aus Review-Sicht wirklich bereit für die Umsetzung:

- Zustände sind klar.
- Datenfluss ist klar.
- Ownership ist klar.
- Scheduler-Regeln sind klar.
- Persistenz-Verhalten für Terrain-only ist klar.
- Duplicate-/Stale-Fälle sind nicht nur gedacht, sondern explizit testbar.

Dann gilt hier wirklich: **Ein guter Plan ist die halbe Umsetzung.**
