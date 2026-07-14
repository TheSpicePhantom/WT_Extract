# M21 - World-Gen

Dieses Dokument beschreibt die nächste Ausbaustufe der Engine für prozedurale Weltgenerierung. Ziel ist eine deterministische, unendliche, chunk-basierte Welt mit Wasser, Klima, Biomregionen, weichen Übergängen und datengetriebener Platzierung von Terrain, Overlays, Decorations und später Ressourcen. Die bestehende Architektur trennt Renderer und Gameplay bereits sauber; World-Gen bleibt deshalb vollständig in `game_core` und liefert nur fertige Weltzustände an die Bridge, die daraus `RenderFrame`-Daten extrahiert. Die vorhandenen Systeme für Chunk-Streaming, Dirty-Chunk-Cache, Layer, Decorations und Walkability bleiben erhalten und werden erweitert, nicht ersetzt. [cite:101]

Die mitgelieferten Unity-Prototypen liefern dafür eine sehr brauchbare Referenz. `HeightmapGenerator.cs` verwendet fraktales Perlin-Noise mit Oktaven, Lacunarity und Persistence zur Erzeugung eines normalisierten Höhenfelds. `BiomeGenerator-4.cs` erzeugt Biome über ein Voronoi-/Worley-artiges Zellmodell mit deterministisch erzeugten Seed-Punkten, Perlin-basierter Kantenverzerrung und Blendfaktor zwischen nächstem und zweitnächstem Biom. `BiomeMath-5.cs` enthält die Hash-Funktionen für Zell-Seed-Punkte sowie eine einfache Einteilung in Klima-Klassen über Heat- und Humidity-Noise. `GridGenerator-6.cs` visualisiert Zellgrenzen und Seed-Punkte, und `TerrainGenerator-3.cs` verbindet Höhenfeld, Grid und Biome in einer testbaren Vorschau. Diese Logik wird hier nicht 1:1 übernommen, sondern in die bestehende Python-Engine architekturgerecht übersetzt. [cite:117][cite:118][cite:120][cite:121][cite:122]

## Ziel von M21

M21 ergänzt M18 um echte Weltgenerierung auf Basis globaler, koordinatenstabiler Felder. Jeder Tile soll aus Weltkoordinaten deterministisch Height, Temperature, Moisture, Water-Class, Biome-Region und finalen Biomtyp ableiten können. Die Welt darf niemals chunk-lokal "zufällig" aussehen; benachbarte Chunks müssen ohne Nähte zusammenpassen, auch wenn sie zu unterschiedlichen Zeitpunkten geladen werden. Das passt zur bestehenden Streaming-Architektur, in der Chunks nur RAM- und Render-Einheiten sind, während die Weltlogik aus absoluten Weltkoordinaten folgt. [cite:101]

Das Ziel ist ausdrücklich ein Hybridmodell. Wasser und Landmassen werden primär aus einem Höhenfeld und Wasserlogik abgeleitet. Biomregionen werden über eine unendliche Voronoi-Struktur organisiert, deren Zellpunkte aus Zellenkoordinaten und Seed per Hash entstehen. Temperatur und Feuchtigkeit ändern sich langsam über die Welt und beeinflussen, welche Biomfamilien in einer Region zulässig sind. Kanten zwischen Regionen werden zusätzlich per Noise verzerrt und über den Abstand zum nächst- und zweitnächsten Zellpunkt weich gemacht. Diese Kombination entspricht sowohl dem Videoansatz als auch etablierten Empfehlungen für prozedurale Karten mit Noise-basierten Geländeformen und klimabasierten Biomen. [cite:4][cite:107][cite:108][cite:109][cite:110][cite:112]

## Modulgrenzen

Die komplette Generierung bleibt in `game_core`. Neue oder erweiterte Dateien sollten ungefähr so aufgeteilt werden:

- `game_core/world_gen.py` — Einstiegspunkt für Chunk-Generierung, Klima-Sampling, Tile-Ableitung, Wasserklassifikation, Biome und Decorations.
- `game_core/noise.py` — performante Noise-Wrapper und Utility-Funktionen für fBM, Domain Warp und normalisierte Samples.
- `game_core/biomes.py` — `BiomeId`, `ClimateClass`, Regeln für Tile-Mapping, Vegetation und Wahrscheinlichkeiten.
- `game_core/world.py` — optionale Erweiterungen an `Chunk` oder `World`, falls Biom-Metadaten oder Debug-Caches gespeichert werden sollen.
- `apps/world_gen_debug_demo.py` — neue Debug-App für testbare Zwischenschritte, analog zur Unity-Vorschau mit Umschaltung zwischen Height, Water, Climate, Voronoi, Blend und finalem Terrain.

Der Renderer bleibt unverändert. `bridge/chunk_extractor.py` extrahiert nur die fertigen Tile-Layer und Decorations, genauso wie heute. Das ist wichtig, weil die bestehende Architektur Rückwärtsabhängigkeiten vom Renderer zur Spielwelt explizit verbietet. [cite:101]

## Effizienteste Noise-Strategie

Für diese Engine ist die effizienteste praktikable Noise-Strategie nicht „maximal fancy“, sondern „wenige globale Felder, koordinatenstabil, wiederverwendbar, cachebar pro Chunk“. Die teuerste Variante wäre, pro Tile und pro Subsystem viele unabhängige Noise-Aufrufe ohne Struktur zu machen. Stattdessen sollte pro Chunk in einem Schritt ein kleines Set an Makrofeldern berechnet werden, die anschließend mehrfach genutzt werden: Height, Temperature, Moisture, optional Continentalness und Warp-X/Warp-Y. So vermeidest du doppelte Samples bei Tile-Auswahl, Wasserklassifikation, Biomwahl und Deko-Platzierung. [cite:101][cite:117][cite:110]

Für das Höhenfeld eignet sich fraktales Brownian Motion (fBM) auf Basis einer schnellen 2D-Gradient-Noise-Funktion. Der Unity-Prototyp verwendet `Mathf.PerlinNoise` mit mehreren Oktaven, Frequenzen und Amplituden und normalisiert durch `maxAmplitude`; das ist der richtige Grundaufbau und sollte in Python nahezu identisch übernommen werden. Für maximale Effizienz in deiner Engine sollte das pro Chunk zeilenweise in Weltkoordinaten berechnet werden, nicht über einzelne Funktionsaufrufe verstreut im restlichen Code. Zusätzlich sollten `frequency`-, `amplitude`- und Offset-Konstanten pro Generatorinstanz vorkalkuliert werden, statt sie pro Tile neu herzuleiten. [cite:117]

Für Voronoi-/Biome-Zellen ist der effizienteste Ansatz, keine globale Seed-Liste zu speichern, sondern Seed-Punkte deterministisch aus Zellkoordinaten zu hashen. Genau das macht `BiomeMath.HashCell()` bereits: Aus `gridPositionX`, `gridPositionY` und `seed` entsteht per Integer-Hash ein reproduzierbarer Wert, aus dem wiederum Punktposition und Biomauswahl folgen. Das ist für eine unendliche Welt optimal, weil du nur die aktuelle Zelle und ihre Nachbarzellen prüfen musst, statt Datenstrukturen für die ganze Welt zu pflegen. [cite:122][cite:108][cite:109]

Für weichere Grenzen wird die Position vor dem Voronoi-Test durch zwei günstige Noise-Abfragen verzerrt. Der Unity-Prototyp samplet zwei Perlin-Felder mit verschiedenen Offsets und nutzt das Ergebnis als 2D-Offset (`distortionX`, `distortionY`). Diese Form von Domain Warp ist erheblich günstiger als komplexe nachträgliche Polygonbearbeitung und genügt für natürliche Biomgrenzen in einer top-down Fabrikwelt. Sie sollte aber bewusst moderat eingesetzt werden, damit Regionen lesbar bleiben und nicht in zu viele kleine Ausstülpungen zerfallen. [cite:118][cite:110][cite:112]

Kurz gesagt: effizient ist in M21 ein zweistufiges Modell aus wenigen wiederverwendeten Noise-Feldern plus gehashten Voronoi-Zellen. Die Performance gewinnt man nicht über exotische Mathematik, sondern über wenig Redundanz, deterministische Zellseeds, Chunk-lokale Feldberechnung und klare Wiederverwendung derselben Samples in mehreren Schritten. [cite:117][cite:118][cite:122]

## Datenmodell

M21 sollte drei neue Kernstrukturen einführen.

Erstens `ClimateSample`: eine strukturierte Sammlung aller globalen Werte, die für einen Weltpunkt relevant sind. Dazu gehören mindestens `height`, `temperature`, `moisture`, `continentalness`, `warp_x` und `warp_y`. Optional kann hier bereits `water_depth_like` oder `distance_to_sea_level` gespeichert werden, damit Wasserlogik und Debug-Ansichten einfacher werden. [cite:4][cite:110]

Zweitens `BiomeRegionSample`: das Ergebnis des Voronoi-Systems für einen Weltpunkt. Diese Struktur sollte mindestens enthalten: `cell_x`, `cell_y`, `nearest_biome`, `second_biome`, `distance_1`, `distance_2`, `border_distance` und `blend_t`. Genau dieser Gedanke steckt im Unity-Prototyp `BiomeBlend`, der das nächste und zweitnächste Biom sowie den Interpolationsfaktor `t` zurückgibt. [cite:118]

Drittens `ResolvedTileSample`: das finale Ergebnis für einen Tile oder Weltpunkt. Darin stehen `tile_key_layer0`, `tile_key_layer1`, `biome_id`, `is_walkable`, optionale Deko-/Feature-Flags und später vielleicht `resource_profile`. Diese Struktur bildet die Brücke von der abstrakten Weltgenerierung zur bestehenden `Chunk.layer_keys`-Welt. [cite:101]

## Übernahme der Beispiel-Logik aus den Anhängen

Die Logik aus den Anhängen sollte in vier Teilbereiche übertragen werden.

Die erste übernommene Logik ist das Heightmap-Prinzip aus `HeightmapGenerator.cs`. Dort wird pro Pixel eine skalierte Weltposition berechnet, danach über mehrere Oktaven Perlin-Noise addiert, wobei Frequenz mit `lacunarity` steigt und Amplitude mit `persistence` sinkt. Am Ende wird durch die akkumulierte Gesamtamplitude geteilt. Dieses Muster soll als `sample_fbm_height(wx, wy)` übernommen werden, nur eben in Weltkoordinaten und nicht in einem Unity-Texture-Array. [cite:117]

Die zweite übernommene Logik ist die Zell- und Hash-Logik aus `BiomeMath-5.cs`. Die Funktionen `Hash`, `HashCell`, `GetPointPositionInCell` und `GetBiomeType` sind der Kern des unendlichen Voronoi-Systems. `GetPointPositionInCell()` erzeugt pro Zelle einen zufälligen Seed-Punkt innerhalb der Zelle. `GetBiomeType()` nutzt langsames Heat-/Humidity-Noise, um Klimaklassen wie neutral, hot+humid, hot+dry, cold+humid und cold+dry zu bestimmen. Genau diese Rollen sollen erhalten bleiben, auch wenn die finale Python-API anders aussieht. [cite:122]

Die dritte übernommene Logik ist die Biome-Abfrage aus `BiomeGenerator-4.cs`. Dort wird aus Weltkoordinaten zuerst die Zellkoordinate ermittelt, dann in den 3×3 Nachbarzellen nach dem nächsten und zweitnächsten Seed gesucht. Vor dem Distanzvergleich wird die Position mit einem Noise-Offset verzerrt. Anschließend wird über `distance2 - distance1` eine Randbreite berechnet und daraus der Blendfaktor bestimmt. Dieses Muster ist sehr wertvoll und sollte nahezu direkt in `sample_biome_region(wx, wy)` übersetzt werden. [cite:118]

Die vierte übernommene Logik ist die Debug-/Visualisierungsidee aus `GridGenerator-6.cs`, `TerrainGenerator-3.cs` und `TerrainDisplay-2.cs`. Die produktive Engine braucht das Unity-UI natürlich nicht, aber sie braucht ein eigenes Debug-Demo, in dem Height, Wasser, Voronoi-Grenzen, Seed-Punkte, Klima-Klassen und finales Terrain umgeschaltet werden können. Nur so lassen sich Schritt für Schritt Fehler bei Skalierung, Seed-Stabilität, Blendbreite und Biomauswahl erkennen. [cite:119][cite:120][cite:121]

## Testbare Zwischenschritte

### Schritt 1 — Reines Height-Field

Zuerst wird nur das globale Höhenfeld eingeführt. `game_core/world_gen.py` bekommt einen einfachen Generator, der für jede Weltkoordinate einen normalisierten Höhenwert liefert. Ein Chunk wird initial ausschließlich aus zwei oder drei Grundtypen gebaut: tiefes Wasser, flaches Wasser und Land. Dafür reicht ein einziger Generator auf Basis von fBM-Perlin mit `octaves`, `lacunarity`, `persistence`, `scale` und `offset/seed`, analog zu `HeightmapGenerator.cs`. [cite:117]

**Testziel:** Eine Debug-Ansicht zeigt nur Height bzw. Water-Class. Beim Bewegen der Kamera oder beim Streaming dürfen keine sichtbaren Brüche zwischen Chunks entstehen. Unterschiedliche Seeds müssen sichtbar andere Kontinente liefern, aber dieselbe Seed immer dieselbe Welt. [cite:101][cite:117]

**Definition of Done:**
- Height-Sampling läuft in Weltkoordinaten.
- Chunks generieren deterministisch denselben Inhalt bei Reload.
- Wasserklassifikation funktioniert mindestens mit `deep_water`, `shallow_water`, `land`.
- Keine Chunk-Nähte in der Debug-Ansicht.

### Schritt 2 — Klima-Felder einführen

Danach werden `temperature` und `moisture` als zusätzliche globale Noise-Felder eingeführt. Diese sollen deutlich großräumiger und glatter sein als das Höhenfeld. Das Vorbild hierfür ist `BiomeMath.GetBiomeType()`, wo Heat und Humidity über zwei getrennte Perlin-Felder berechnet werden. In der Engine sollen diese Felder noch nicht direkt Biome erzeugen, sondern zunächst nur als Debug-Daten existieren. [cite:122]

**Testziel:** Eine Debug-Ansicht kann zwischen Height, Temperature und Moisture umschalten. Die Temperatur- und Feuchteverteilung soll großflächig und plausibel sein, nicht kleinteilig oder pixelig. [cite:122][cite:110]

**Definition of Done:**
- `sample_climate(wx, wy)` liefert mindestens Height, Temperature und Moisture.
- Temperatur und Feuchtigkeit sind chunk-stabil und seed-stabil.
- Debug-Ansichten zeigen glatte, langsame Gradienten.

### Schritt 3 — Unendliche Voronoi-Biom-Zellen

Jetzt wird das Voronoi-System eingeführt. Pro Biom-Zelle existiert ein deterministisch gehashter Seed-Punkt innerhalb der Zelle, analog zu `BiomeMath.GetPointPositionInCell()`. Für einen Weltpunkt werden die Seed-Punkte der aktuellen Zelle und der 8 Nachbarn betrachtet; der nächstgelegene Seed bestimmt die Region. In diesem Schritt gibt es noch keine Noise-Verzerrung und keine weichen Übergänge. [cite:122][cite:118]

**Testziel:** Eine Debug-Ansicht rendert Zellgrenzen und Seed-Punkte, wie im Unity-Prototyp über `GridGenerator`. Beim Durchscrollen der Welt müssen die Seed-Punkte absolut stabil bleiben, und Zellen dürfen keine Sprünge an Chunkgrenzen zeigen. [cite:120][cite:108]

**Definition of Done:**
- `HashCell`-Äquivalent ist implementiert.
- Jede Zelle hat genau einen deterministischen Seed-Punkt.
- Regionenzuordnung ist über Chunkgrenzen hinweg stabil.
- Debug-Demo zeigt Zellen und Seed-Punkte korrekt.

### Schritt 4 — Klima-Klassen für Regionen

Nun bekommt jede Voronoi-Zelle eine Klimaklasse. Das Muster kommt direkt aus `BiomeMath.GetBiomeType()`: Heat/Humidity definieren mindestens neutral, hot+humid, hot+dry, cold+humid und cold+dry. In der Engine sollte daraus eine `ClimateClass` entstehen, aus der wiederum zulässige Biomfamilien abgeleitet werden. Noch gibt es keine finalen Tiles, sondern nur Regionstypen. [cite:122]

**Testziel:** Eine Debug-Ansicht färbt Voronoi-Regionen nach Klimaklasse. Benachbarte Regionen dürfen unterschiedliche konkrete Seeds haben, aber insgesamt sollen zusammenhängende warme, kalte, trockene und feuchte Zonen sichtbar werden. [cite:122][cite:109]

**Definition of Done:**
- Jede Region erhält eine deterministische Klimaklasse.
- Die Klimaklassen folgen globalen Gradienten statt reinem Zellzufall.
- Neutrale Regionen existieren als Puffer zwischen Extremen.

### Schritt 5 — Domain Warp für organische Grenzen

Erst jetzt kommt die Noise-Verzerrung dazu. Die Positionsverzerrung vor dem Distanzvergleich wird direkt aus `BiomeGenerator-4.cs` übernommen: zwei Perlin-Samples erzeugen einen 2D-Offset, der mit `biomeShapeDistortion` und `biomeDistortionFrequency` skaliert wird. Diese Verzerrung sollte moderat bleiben, damit Regionen lesbar bleiben und das Weltbild für ein Fabrikspiel nicht zu chaotisch wird. [cite:118][cite:112]

**Testziel:** Vergleichsansicht „Voronoi roh“ gegen „Voronoi mit Warp“. Die Kanten sollen sichtbar natürlicher werden, dürfen aber keine winzigen Nadel- oder Fransenformen erzeugen, die später Terrain und Ressourcenverteilung schwer lesbar machen. [cite:118][cite:112]

**Definition of Done:**
- Warp funktioniert deterministisch.
- Kanten sehen organischer aus als im Rohzustand.
- Regionen bleiben groß genug und spielbar.

### Schritt 6 — Border Blend zwischen Regionen

Danach wird die Distanz zum zweitnächsten Seed genutzt. Wie im Unity-Prototyp wird `border_distance = distance_2 - distance_1` berechnet. Wenn dieser Wert kleiner als eine konfigurierte `blend_width` ist, liegt der Weltpunkt in einer Übergangszone. Diese Blend-Information soll nicht nur Farben mischen, sondern auch im Datenmodell verfügbar sein, damit später Tiles, Decorations und Ressourcen semantisch gemischt werden können. [cite:118][cite:112]

**Testziel:** Debug-Ansicht zeigt `border_distance` oder direkt die Übergangszonen. Die Übergänge sollen sichtbar weicher sein, aber nicht so breit, dass jede Region hauptsächlich aus Mischzonen besteht. [cite:118][cite:112]

**Definition of Done:**
- `sample_biome_region()` liefert nearest, second nearest und `blend_t`.
- Blendzonen sind deterministisch und optisch plausibel.
- Blenddaten können später von Tile- und Decoration-Logik genutzt werden.

### Schritt 7 — Finale Landbiome auflösen

Jetzt werden aus Height, Water-Class, Climate und Region die eigentlichen Biome bestimmt. Wasser wird weiterhin primär über das Height-System behandelt. Landbiome ergeben sich aus Klimaklasse plus lokalen Modifikatoren. Ein mögliches erstes Mapping ist: `hot+dry -> desert, savanna, steppe`, `hot+humid -> lush_plains, wet_forest`, `cold+humid -> taiga, conifer_forest`, `cold+dry -> tundra`, `neutral -> plains, mixed_forest, birch_forest`. Die genaue Liste kann in `game_core/biomes.py` datengetrieben hinterlegt werden. [cite:122][cite:107][cite:109]

**Testziel:** Eine finale Terrain-Ansicht zeigt erstmals echte Grundbiome. Die Karte soll lesbare Regionen ergeben, keine rein höhenbasierten Streifen und keine chaotisch verstreuten Klimasprünge. [cite:4][cite:107][cite:109]

**Definition of Done:**
- Wasser- und Landbiome sind getrennte Konzepte.
- Biome folgen Klima und Region, nicht nur der Höhe.
- Die Welt wirkt regional, nicht zufällig gestreut.

### Schritt 8 — Tile-Keys und Layer-Mapping

Sobald die Biome stimmen, wird die Ableitung zu realen Tiles in `Chunk.layer_keys` integriert. Layer 0 bekommt das Basisterrain (`wt:tiles/deep_water`, `wt:tiles/shallow_water`, `wt:tiles/sand`, `wt:tiles/grass`, `wt:tiles/snow`, `wt:tiles/dirt`, usw.). Layer 1 kann für Küstenränder, Geröll, Schneeinseln, Ufervegetation oder Pfad-/Spezialoverlays genutzt werden. Das passt direkt auf die vorhandene Layer-Architektur aus M9b und M10. [cite:101]

**Testziel:** Ein generierter Chunk ist nicht mehr nur eine Debug-Map, sondern eine echte `Chunk`-Instanz mit `layer_keys`, die in `chunk_world_demo` gerendert werden kann. [cite:101]

**Definition of Done:**
- `generate_chunk()` produziert echte Tile-Keys.
- Terrain erscheint im bestehenden Renderer ohne Sonderlogik.
- Layer 0 und Layer 1 werden sinnvoll genutzt.

### Schritt 9 — Biomabhängige Decorations

Danach wird `populate_chunk_decorations()` biomabhängig gemacht. Das bestehende Decoration-System eignet sich dafür bereits gut. Wälder erzeugen passende Baumtypen, Steppe und Savanne eher spärliche Büsche, tote Regionen Stümpfe und tote Bäume, Küsten einzelne Steine oder trockenes Gras. Wichtig ist, dass Decorations ebenfalls aus Weltkoordinaten und deterministischen Seeds abgeleitet werden. [cite:101]

**Testziel:** Beim Laden und Entladen von Chunks entstehen immer dieselben Decorations. Unterschiedliche Biome wirken nicht nur über Bodentextur, sondern auch über Vegetation und Objektverteilung klar unterscheidbar. [cite:101]

**Definition of Done:**
- Decorations folgen dem Biomtyp.
- Chunk-Reload erzeugt identische Ergebnisse.
- Walkability und Solid-Grid bleiben konsistent.

### Schritt 10 — Startgebiet und Spielbarkeitsregeln

Zum Schluss wird die Generierung gameplaytauglich gemacht. Für ein Factorio-like reicht „sieht natürlich aus“ nicht. Es braucht zusammenhängende Bauflächen, vernünftige Wasseranteile, lesbare Küsten und keine komplett zersplitterten Biome im Startbereich. Deshalb sollte ein Startgebiet explizit geglättet oder mit Sonderregeln belegt werden: weniger Extremwasser, weniger dichte Wälder, bevorzugt gemäßigte Biome und ausreichend freie Fläche. Red Blob und andere Quellen weisen darauf hin, dass Noise allein zwar gute lokale Varianz erzeugt, aber globale Spielstruktur oft zusätzliche Regeln braucht. [cite:4][cite:112]

**Testziel:** Der Spawn-Bereich bleibt über viele Seeds hinweg gut bespielbar. Beim schnellen Seed-Wechsel gibt es nicht zu viele unbrauchbare Welten mit Mini-Inseln, dauernden Engstellen oder riesigen Wasserbarrieren. [cite:4]

**Definition of Done:**
- Startbereich hat minimale Qualitätsgarantien.
- Welt bleibt trotzdem sichtbar prozedural.
- Gameplay-Anforderungen dominieren über rein ästhetische Noise-Details.

## Konkrete Implementierung der Kernalgorithmen

Die Heightmap-Logik aus `HeightmapGenerator.cs` sollte in Python in eine Funktion oder Klasse übersetzt werden, die pro Chunk ein Feld berechnet und wiederverwendet. Inhaltlich bleibt der Ablauf gleich: `scaled_position = (world_x, world_y) * scale`, dann Oktaven-Loop mit `frequency`, `amplitude`, Summierung und Normalisierung per `max_amplitude`. Die festen Oktav-Offsets aus dem Unity-Prototyp können erhalten bleiben oder seed-basiert erweitert werden, um Wiederholungsmuster weiter zu minimieren. [cite:117]

Die Hash- und Zellpunktlogik aus `BiomeMath-5.cs` sollte nahezu direkt übertragen werden. Die Integer-Hash-Funktion ist billig, deterministisch und für unendliche Zellen gut geeignet. `GetPointPositionInCell()` bleibt fachlich identisch: Aus einem Hash werden zwei 16-Bit-Fraktionen gewonnen, die als `rx` und `ry` den Seed-Punkt innerhalb der Zelle definieren. [cite:122]

Die Regionensuche aus `BiomeGenerator-4.cs` bleibt ebenfalls fast gleich: Bestimme anhand von Weltkoordinate und Zellgröße die aktuelle Zelle, prüfe die 3×3 Nachbarzellen, ermittle `distance_1` und `distance_2`, und berechne daraus `blend_t`. Ein Unterschied zur finalen Engine sollte sein, dass die Klimaklasse oder Biomauswahl der Zelle nicht nur über den Zellindex selbst bestimmt wird, sondern sauber aus globalen Klima-Feldern plus Zellseed hervorgeht. So bleiben großräumige Klimazonen konsistenter als bei rein zellbasiertem Rauschen. [cite:118][cite:122][cite:107]

Die Debug-Idee aus `GridGenerator-6.cs` und `TerrainDisplay-2.cs` ist ausdrücklich Teil von M21. Ohne Debug-Ansichten wird das Tuning von Zellgrößen, Warp-Frequenz, Blend-Breite, Wasserlevel und Klimaskalen extrem mühsam. Die Debug-App sollte mindestens folgende Modi haben: Height, Water, Temperature, Moisture, ClimateClass, VoronoiCells, VoronoiBlend, FinalBiome, Decorations. [cite:119][cite:120][cite:121]

## Parameter, die früh konfigurierbar sein sollten

Schon in M21 sollten die wichtigsten Parameter zentral konfigurierbar sein: `height_scale`, `height_octaves`, `height_lacunarity`, `height_persistence`, `sea_level`, `shallow_water_band`, `biome_cell_size`, `biome_distortion_frequency`, `biome_shape_distortion`, `biome_blend_width`, `temperature_scale`, `moisture_scale`, `neutral_climate_width` und optionale Startgebiet-Parameter. Diese Konfigurierbarkeit entspricht der Rolle, die ähnliche Parameter in den Unity-Prototypen spielen, etwa `scale`, `octaves`, `biomeCellSize`, `biomeShapeDistortion`, `biomeDistortionFrequency` und `biomeBlendWidth`. [cite:117][cite:118][cite:121]

## Nicht-Ziele für M21

M21 soll bewusst noch keine vollständige Ressourcenlogik, kein Wetter, keine Rivers-/Hydrologie-Simulation und kein asynchrones Worldgen-Job-System enthalten. Rivers, Hydrologie, Qualitätsmetriken für Seeds oder Multithreading können später folgen. Der Fokus liegt auf einer sauberen, deterministischen, testbaren Weltgrundlage mit gut lesbaren Regionen, stabilen Chunkgrenzen und echter Trennung zwischen Makroterrain, Biomstruktur und Deko. [cite:101][cite:106]

## Definition of Done für M21

M21 ist abgeschlossen, wenn die Engine deterministisch unendliche Chunks mit Height, Water-Class, Climate, Voronoi-Biomregionen, Warp, Blend und finalem Terrain generieren kann, ohne Chunk-Nähte und ohne Render-Sonderlogik. Zusätzlich muss es eine Debug-Demo geben, die jeden Zwischenschritt sichtbar macht, und die aus den vorhandenen Anhängen übernommene Logik muss in architekturgerechter Form im `game_core`-Worldgen angekommen sein. Decorations sollen mindestens in einer ersten Form biomabhängig sein, und das Ergebnis muss im bestehenden `chunk_world_demo` oder einer dedizierten Worldgen-Demo renderbar sein. [cite:101][cite:117][cite:118][cite:119][cite:120][cite:121][cite:122]
