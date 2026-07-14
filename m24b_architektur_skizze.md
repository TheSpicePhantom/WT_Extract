# M24b – Architektur für Terrain/Deco-Trennung

M24b sollte die Chunk-Erzeugung sauber in **Terrain** und **Decoration** zerlegen, damit die teure Deko-Pipeline unabhängig steuerbar wird, ohne dass Deko Terrain überholt oder Streaming inkonsistent macht. Die bisherigen Benchmarks und Analysen zeigen, dass Terrain und Deko heute pro Worker-Chunk ungefähr je die Hälfte der Zeit verbrauchen und im Worker sequentiell in einem Task laufen. [file:635][file:634]

## Ziele

- **Saubere Trennung** zwischen Terrain-Bau und Deko-Bau, sowohl im Code als auch im Scheduling. [file:635]
- Deko darf **niemals vor Terrain sichtbar oder semantisch aktiv** werden; Terrain ist die Basisschicht, Deko ein nachgelagerter Anreicherungs-Schritt. [file:635]
- Die Deko-Generierung soll einfacher, konfigurierbarer und besser lesbar werden, statt als zweiter schwerer Pass mitten im Chunk-Build zu hängen. [file:635][cite:626]
- Die Architektur soll zu einem klaren Threading-Modell mit getrennten Verantwortlichkeiten passen, was deiner generellen Präferenz entspricht. [cite:629]

## Zielbild

Ein Chunk durchläuft in M24b zwei logisch getrennte Stufen:

1. **Terrain-Stage**
   - baut `layer0`, `layer1`
   - erzeugt ein terrain-only `Chunk`-Grundobjekt
   - kann früh sichtbar/streambar werden
   - liefert die gemeinsame Feld-/Biome-/Klima-Basis für spätere Deko

2. **Deco-Stage**
   - läuft nur auf Basis eines bereits vorhandenen Terrain-Snapshots
   - erzeugt prozedurale Placements und optional ein deco-spezifisches Collision-/Solid-Delta
   - darf erst angewendet werden, wenn Terrain für denselben Chunk bereits übernommen wurde

Damit verschwindet das heutige "ein Worker baut alles auf einmal und später entscheidet der Streamer, was davon er benutzt"-Modell. Stattdessen wird aus dem Chunk-Build ein kleiner **Pipeline-Vertrag**. [file:635]

## Empfohlenes Datenmodell

Statt nur `ChunkGenResult` mit "terrain-only oder worker-complete" sollte M24b explizite Ergebnis-Typen einführen:

| Result-Typ | Inhalt | Darf sofort applied werden? |
|-----------|--------|-----------------------------|
| `TerrainResult` | `coord`, `layer0`, `layer1`, optional `field_cache_ref`/metadata | Ja |
| `DecoResult` | `coord`, `placements`, optional `solid_grid` oder `solid_patch`, `terrain_revision` | Nur wenn Terrain bereits für dieselbe Revision aktiv ist |
| `ChunkBuildState` | Streamer-interner Status: `terrain_ready`, `deco_ready`, `applied_revision` | intern |

Wichtig ist die **Revision** oder ein ähnlicher Build-Token: Deco muss an genau den Terrain-Zustand gebunden sein, auf dessen Basis sie berechnet wurde. Sonst kann ein verspätetes Deco-Result einen schon ersetzten oder verworfenen Terrain-Chunk falsch anreichern. [file:619][file:635]

## Worker-Modell

### Variante A – Ein Pool, zwei Jobtypen

Ein Pool bearbeitet sowohl Terrain- als auch Deco-Jobs, aber als getrennte Task-Arten.

**Vorteile:**
- geringerer Implementierungsaufwand,
- weniger Warmup-/Prozessmanagement,
- einfachere gemeinsame Limits für `in_flight`.

**Nachteile:**
- Terrain und Deko konkurrieren weiter direkt um dieselben Worker-Slots,
- Priorisierung wird schwieriger,
- Deko kann Terrain indirekt ausbremsen, wenn die Queue nicht sauber priorisiert wird.

### Variante B – Zwei Worker-Pools

- **Terrain-Pool**: klein, hoch priorisiert, zuständig für sichtbare oder bald sichtbare Chunks.
- **Deco-Pool**: separat, nachrangig, zuständig nur für Anreicherung bereits vorhandener Terrain-Chunks.

**Vorteile:**
- passt sehr gut zu deinem Wunsch nach klar getrennten Verantwortlichkeiten. [cite:629]
- Terrain kann weiterfließen, auch wenn Deco teuer ist.
- Scheduling wird verständlicher: erst Welt lesbar machen, dann verschönern.
- Einfachere Guard-Regel: Deco darf nur submitted werden, wenn Terrain-Stage erfolgreich war.

**Potenzielle Nachteile:**
- mehr Komplexität bei Pool-Init, Shutdown, Telemetrie und Backpressure,
- mehr Konfigurationsbedarf (`terrain_workers`, `deco_workers`, Queue-Limits),
- Gefahr von CPU-Überbelegung, wenn beide Pools zusammen zu viele Prozesse starten.

Für M24b würde ich **zwei Pools als Zielbild**, aber mit einer ersten Implementierung beginnen, die intern noch einen Pool mit zwei Prioritätsklassen nutzen kann. So bleibt der Architekturvertrag sauber, ohne sofort maximalen Infrastrukturaufwand zu erzwingen. [file:619][cite:629]

## Reihenfolgegarantie: Deco darf Terrain nicht überholen

Das ist die wichtigste Regel in M24b.

**Invariante:** Ein `DecoResult(coord, revision)` darf nur applied werden, wenn:

- `world.chunks[coord]` existiert,
- die aktive Terrain-Revision für `coord` mit `revision` übereinstimmt,
- der Chunk nicht `pending_unload`, `discarded` oder durch Override/Delta ersetzt wurde.

Praktisch heißt das:

- Terrain-Result kann direkt sichtbar werden. [file:635]
- Deco-Result wird verworfen oder zurückgestellt, wenn Terrain noch fehlt oder inzwischen ersetzt wurde. [file:635]
- Der Streamer markiert Chunk-Zustände explizit, z. B. `TERRAIN_ONLY`, `DECO_PENDING`, `DECO_APPLIED`.

Das macht das Verhalten viel lesbarer als heute, wo `WORKER_COMPLETE`, Sync-Fallback und Race-Fälle erst nachträglich im Apply-Pfad sortiert werden. [file:635][file:619]

## Deco-Generierung einfacher machen

Heute hängt Deko eng an `compute_procedural_decorations` und baut offenbar erneut Feld-/Biome-Daten auf, was einer der größten Kostentreiber ist. Die Analyse nennt das doppelte `build_chunk_field_cache` als wichtigen Hebel. [file:635]

M24b sollte Deko daher in ein **konfigurierbares Regelmodell** überführen:

- `deco_generation.json` oder Erweiterung von `world_gen.json`,
- pro Deko-Typ Regeln wie Biome, Höhenbereich, Dichte, Noise-Kanal, Mindestabstand, Cluster-Verhalten,
- optionale Gruppen/Pässe wie `trees`, `rocks`, `bushes`, `ambient`.

Beispielhafte Struktur:

```json
{
  "passes": [
    {
      "name": "trees",
      "enabled": true,
      "priority": 10,
      "biomes": ["forest", "plains"],
      "density_noise": "trees_density",
      "rules": [
        {"decoration": "oak_tree", "weight": 5},
        {"decoration": "birch_tree", "weight": 2}
      ]
    },
    {
      "name": "rocks",
      "enabled": true,
      "priority": 20,
      "biomes": ["mountain", "plains"],
      "density_noise": "rocks_density",
      "rules": [
        {"decoration": "small_rock", "weight": 4}
      ]
    }
  ]
}
```

Das macht drei Dinge besser:

- Deko-Logik wird **datengetriebener** und leichter anpassbar. [cite:626]
- Einzelne Deco-Pässe können gezielt deaktiviert, gestaffelt oder später geladen werden.
- Der Deco-Pool kann priorisieren: erst essentielle Kollisionsträger, später rein kosmetische Deko.

## Konkrete M24b-Phasen

### Phase 0 – Verträge und Statusmodell
- `TerrainResult`, `DecoResult`, `ChunkBuildState` einführen.
- Streamer-Zustände für `terrain_ready` / `deco_ready` definieren.
- Tests für Reihenfolge und Discard-Regeln aufbauen.

### Phase 1 – Terrain/Deco im Code entkoppeln
- Terrain-Build und Deco-Build als getrennte Funktionen/Tasks strukturieren.
- `compute_procedural_decorations` darf nicht mehr „heimlich Teil von generate_chunk_result“ sein. [file:635]
- Gemeinsame Feldcache-/Sampling-Daten aus Terrain nutzbar machen.

### Phase 2 – Cache-Sharing
- `build_chunk_field_cache` einmal pro Chunk-Basis erzeugen und für Terrain + Deko wiederverwenden. [file:635]
- Gleiche Referenzlogik in Sync und Worker.
- Benchmarks separat für Terrain-only, Deco-from-cache und Full-Pipeline.

### Phase 3 – Deco-Apply-Vertrag
- `apply_deco_result(world, deco_result)` ergänzen.
- Reihenfolge-Guards: Revision, `pending_unload`, Override/Delta, Dirty.
- Keine globale Neu-Berechnung nur wegen Deco-Apply.

### Phase 4 – Scheduler / zweiter Pool
- Erst Architektur mit Jobtypen und Prioritäten.
- Danach optional echter zweiter Pool (`terrain_pool`, `deco_pool`).
- Konfigurierbare Limits wie `terrain_max_in_flight`, `deco_max_in_flight`, `deco_backfill_budget`.

### Phase 5 – Config-getriebene Deco-Generierung
- Deko-Regeln aus Code in Config verschieben.
- Pass-System, Prioritäten, Biome-/Noise-Regeln, kosmetische vs. kollisionsrelevante Deko.
- Debug-/Benchmark-Schalter pro Pass.

## Vorteile

- **Klare Architektur:** Terrain ist Basis, Deco ist nachgelagerte Anreicherung. [file:635]
- **Bessere Performance-Kontrolle:** Deco kann separat gedrosselt, deaktiviert oder gestaffelt werden. [file:635]
- **Weniger Race-Müll:** Ein verspätetes Deco-Result ist leichter verwerfbar als ein kompletter monolithischer Worker-Chunk. [file:635]
- **Bessere Lesbarkeit:** Die Weltgen-Pipeline wird nachvollziehbarer als heute. [file:635]
- **Config-Driven Design:** passt gut zu deinem bestehenden Stil bei Streaming- und LOD-Konfigurationen. [cite:622][cite:626]

## Risiken und Nachteile

- **Mehr Zustände im Streamer:** `terrain_ready` und `deco_ready` erhöhen die Komplexität.
- **Mehr Testbedarf:** Reihenfolge, Revisionen, Discards, Revive, Override/Delta müssen sauber abgesichert werden.
- **Gefahr visueller Zwischenzustände:** Terrain sichtbar, Deko noch nicht da. Das muss gestalterisch akzeptabel oder bewusst kaschiert sein.
- **Zwei Pools können überziehen:** Ohne harte Limits kann die CPU durch Terrain- und Deco-Prozesse gleichzeitig überlastet werden. [cite:629]
- **Persistenz/Revive wird anspruchsvoller:** Wenn Deco später kommt, muss klar sein, ob Save/Load Terrain-only, Deco-ready oder beide Zustände sieht.

## Empfehlung

Für M24b würde ich die Priorität so setzen:

1. **Architekturvertrag Terrain vs. Deco sauber machen.**
2. **Cache-Sharing einbauen.**
3. **Reihenfolgegarantie und Apply-Vertrag für Deco einführen.**
4. **Erst danach** über echten zweiten Pool entscheiden.
5. **Dann** Deco-Generierung in Config/Pässe überführen.

So bekommst du erst klare Verantwortlichkeiten und Messbarkeit, bevor du Infrastruktur verdoppelst. Der zweite Pool ist attraktiv, aber nur dann wirklich wertvoll, wenn Terrain- und Deco-Tasks bereits sauber getrennt beschrieben und angewendet werden können. [file:635][file:619][cite:629]
