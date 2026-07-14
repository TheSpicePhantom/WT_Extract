# M24c — Strikter Planungs-Prompt für Cursor

M24b ist abgeschlossen. Terrain- und Deco-Pipeline sind jetzt sauber getrennt, die Architektur ist testbar, und die Benchmarks zeigen klar: **Der nächste dominante Kostenblock ist die Terrain-/Weltgenerierung selbst.** [file:651][file:652]

Deine Aufgabe ist jetzt, einen neuen Milestone **M24c** zu planen.

M24c ist **kein** weiterer Deco-Milestone, **kein** Persistenz-Milestone und **kein** Renderer-Milestone. M24c ist ein **reiner Performance-/Worldgen-Milestone** mit einem Ziel:

> **Die Terrain-/Weltgenerierung muss massiv schneller werden.** [file:651][file:652]

## Rolle

Du arbeitest als Technical Lead / Performance-Architekt.

Du sollst:

1. aus den vorhandenen M24b-Benchmarks und Verträgen einen neuen, strengen M24c-Plan ableiten,
2. die größten Kostenblöcke der Terrain-Erzeugung isolieren,
3. konkrete Umbauten in klaren Phasen definieren,
4. Risiken, Messgrößen und Definition of Done hart formulieren.

Du sollst **nicht**:

- M24b erneut umbauen,
- Deco erneut optimieren, wenn es nicht direkt der Terrain-Generierung dient,
- zur Persistenz abbiegen,
- vage „Profiling später“-Pläne schreiben,
- einen Sammel-Milestone aus allen offenen Themen machen.

## Verbindlicher Ausgangspunkt

Die Benchmarks zeigen:

### Terrain-only

- `build_terrain_stage`: ca. **25.6 s** sync für 64×64 / 4096 Tiles inkl. `field_cache`. [file:651]
- `worker_build_terrain_stage`: ca. **22.4 s** im Worker. [file:651]
- `apply_terrain_stage`: nur **0.78 ms** auf Main. [file:651]

### Terrain + Deco

- `build_terrain_stage`: ca. **19.8 s**. [file:652]
- `build_deco_stage`: ca. **4.29 s** sync. [file:652]
- `worker_build_terrain_stage`: ca. **22.0 s**. [file:652]
- `worker_build_deco_stage`: ca. **19.0 s**. [file:652]
- `worker_apply_main_total`: nur **0.795 ms**. [file:652]

### Schluss daraus

- **Main-Apply ist nicht das Problem.** [file:651][file:652]
- **Deco ist aktuell nicht die erste Schraube.** [file:652]
- **Terrain-/Worldgen-Build ist die nächste große Kostenwand.** [file:651][file:652]

M24c muss deshalb auf die Frage antworten:

> **Warum kostet `build_terrain_stage` pro 64×64-Chunk noch ~20–25 Sekunden, und wie bringen wir das drastisch nach unten?** [file:651][file:652]

## Was M24c liefern soll

Erstelle einen vollständigen Markdown-Plan für **M24c** mit einem klaren Dateinamen im Stil der bisherigen Milestones, z. B.:

- `m24c_terrain_generation_acceleration_<hash>.plan.md`

Der Plan muss so formuliert sein, dass er direkt als nächste Umsetzungsgrundlage dienen kann.

## Inhaltliche Leitplanken für M24c

Der Plan muss zwingend diese Themen prüfen und strukturieren.

### 1. Cost Breakdown innerhalb von `build_terrain_stage`

Lege offen, welche Anteile in `build_terrain_stage` eigentlich teuer sind. Zerlege mindestens in:

- Height/Noise-Sampling
- Biome/Material-Auswahl
- Tile-Key-/Layer-Build
- `field_cache`-Aufbau
- eventuelle Nachbearbeitung / Strukturen / sonstige Schleifen

Wenn dafür zuerst zusätzliche Benchmark-Metriken nötig sind, dann ist das **Phase 0** von M24c und muss als verpflichtend formuliert werden.

### 2. Algorithmische Komplexität prüfen

Der Plan muss explizit nach O(Tile), O(Tile × Layer), O(Tile × Rule), O(Tile × Radius), O(Tile × Neighbor) oder ähnlichen Kosten suchen.

Er soll insbesondere aufspüren:

- doppelte oder dreifache Tile-Schleifen,
- Noise mehrfach pro Tile statt gebündelt,
- biome/material rules, die pro Tile zu teuer dispatchen,
- Python-Objekt-/Dict-/String-Overhead im innersten Loop,
- unnötige Konvertierungen oder Lookup-Ketten.

### 3. Datenlayout und Hotpath-Härtung

M24c soll prüfen, ob Terrain-Gen noch zu sehr von Python-Objektgraphen, Dicts, String-Keys oder config-lastiger Laufzeitlogik abhängt.

Der Plan muss klar beantworten, ob folgende Richtungen nötig sind:

- Precompilierte Terrain-Regeln,
- integerbasierte/arraybasierte Hotpath-Daten,
- aggressive Lookup-Vorbereitung,
- strukturierte Worker-lokale Scratch-Buffers,
- weniger Python-Objekte pro Tile.

### 4. Config-Logik vs. compiled runtime

So wie M24b bei Deco auf `CompiledDecoPass` gegangen ist, muss M24c prüfen, ob Terrain-Regeln ebenfalls stärker kompiliert werden müssen.

Zum Beispiel:

- JSON/Config nur beim Laden interpretieren,
- danach kompiliertes Runtime-Modell,
- keine verzweigte Interpretationslogik pro Tile.

### 5. `field_cache` kritisch prüfen

M24b hat sauber gemacht, dass `field_cache` nur einmal pro Chunk-Basis gebaut wird. M24c muss jetzt prüfen, ob **dieser eine Build** selbst zu teuer ist. [file:651][file:652]

Der Plan soll explizit fragen:

- Welche Daten landen im `field_cache`?
- Was davon ist wirklich nötig?
- Was könnte lazily oder kompakter entstehen?
- Baut `field_cache` Informationen, die Terrain gar nicht unmittelbar braucht?

### 6. Worker-Hotpath, nicht Main-Thread

M24c ist primär ein Worker-/Worldgen-Milestone. Der Plan darf nicht wieder in Main-Thread-Apply-Themen abdriften, weil M24b dort bereits geliefert hat. [file:651][file:652]

Wenn Main-Thread-Themen auftauchen, dann nur, wenn sie direkt durch Terrain-Gen-Kosten verursacht oder messbar gekoppelt sind.

### 7. Messbarkeit als Pflicht

Der Plan muss klare Benchmark-/Profiling-Artefakte definieren, z. B.:

- erweiterter `benchmark_single_chunk.py`,
- Teilzeiten innerhalb von `build_terrain_stage`,
- Vergleich alt vs. neu,
- Metriken pro 64×64-Chunk,
- Worker-Zeit vs. Sync-Zeit,
- eventuell Heatmap/Histogramm, falls sinnvoll.

Das darf kein optionaler Appendix sein. Messbarkeit ist Kernbestandteil, weil die nächste Optimierungsrunde datengetrieben laufen soll. [cite:648]

## Erwartete Planstruktur

Der M24c-Plan soll mindestens enthalten:

- Titel + Overview
- Problembeleg aus den Benchmarks
- harte Zieldefinition
- In Scope / Out of Scope
- Phasenplan
- betroffene Kernmodule
- Pflicht-Metriken / Benchmarks
- Risiken / Guardrails
- Definition of Done
- Erfolgskriterium

## Form der Phasen

Die Phasen sollen **klein, technisch sauber und implementierbar** sein. Nicht alles in eine Phase kippen.

Eine gute Richtung wäre zum Beispiel:

- **Phase 0:** Instrumentation / Cost Breakdown in `build_terrain_stage`
- **Phase 1:** Terrain-Hotpath zerlegen und innere Schleifen vereinfachen
- **Phase 2:** compiled runtime model / rule precomputation
- **Phase 3:** data layout / scratch buffers / lower Python overhead
- **Phase 4:** benchmark hardening + regression tests

Das ist nur eine Richtung — keine Pflichtstruktur. Wichtig ist, dass der Plan klar priorisiert, **wo zuerst der größte Hebel liegt**.

## Harte Verbote

Der M24c-Plan darf **nicht**:

- M24b wieder aufrollen,
- Deco als Hauptthema wählen,
- sich in Persistenz verlieren,
- vage Optimierungslisten ohne Reihenfolge liefern,
- „wir könnten mal NumPy/Cython/Rust prüfen“ als leere Worthülse stehen lassen,
- ohne Messkriterien bleiben,
- neue Architektur einführen, die die M24b-Verträge beschädigt.

## Ton und Schärfe

Formuliere den Plan hart und konkret, so wie die finalen M24b-Pläne formuliert wurden.

Das Ziel ist nicht „ein paar Prozent schneller“, sondern eine neue, klare Optimierungsstufe für die Weltgenerierung.

Leitfrage:

> **Wie machen wir `build_terrain_stage` nicht kosmetisch, sondern drastisch schneller, ohne die saubere M24b-Architektur wieder kaputtzumachen?** [file:644][file:651][file:652]

## Erwartetes Ergebnis

Liefere den vollständigen M24c-Plan als Markdown-Datei.

Der Plan muss so gut sein, dass er danach wieder extern reviewt und anschließend ähnlich strikt umgesetzt werden kann — genau im Stil der bisherigen Milestone-Kette. [cite:646][cite:647]
