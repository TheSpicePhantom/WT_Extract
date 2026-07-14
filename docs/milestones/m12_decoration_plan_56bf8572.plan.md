---
name: M12 Decoration Plan
overview: "M12 führt platzierte Decoration-Sprites (Bäume, Büsche, …) mit data-driven Content-Registry ein: Auto-Scan der ~58 PNGs, Bake-Padding für 80×96-Assets, World-Platzierung, Bridge-Extraktion, Sprite-Layer-Sortierung und Demo-Pinsel (Modus 3)."
todos:
  - id: bake-pad
    content: "bake_atlas.py: Pad-to-32-Grid (80×96→96×96) + Rebake aller decoration PNGs"
    status: completed
  - id: content-registry
    content: game_core/content_registry.py + assets/content/decorations.json (Auto-Scan + Overrides)
    status: completed
  - id: world-placement
    content: PlacedDecoration in World + world_gen Demo-Spawn + place/remove API
    status: completed
  - id: bridge-extract
    content: bridge/decoration_extractor.py + sprite layer sort in tile_layer.py
    status: completed
  - id: demo-m12
    content: "chunk_world_demo: Modus 3, [/] cycle, LMB/X paint + title"
    status: completed
  - id: docs-m12
    content: "ARCHITECTURE.md: M12 Meilenstein + Abschnitt dokumentieren"
    status: completed
isProject: false
---

# M12 — Decoration + Content-Registry

## Ziel

Spieler/platzierte **Decoration-Objekte** (Bäume, Büsche, Stumps, …) als `SpriteInstanceData` rendern — Metadaten data-driven, Keys aus dem Atlas. Kein spielspezifischer Renderer.

**Draw-Reihenfolge (unverändert ein `vkCmdDraw`):**

```mermaid
flowchart LR
  tilesL0[Tiles Layer 0]
  tilesL1[Tiles Layer 1]
  decoSprites[Decoration Sprites L4-L5]
  charSprite[Character L10]
  tilesL0 --> tilesL1 --> decoSprites --> charSprite
```

---

## Entscheidungen (bestätigt)

| Thema | Wahl |
|-------|------|
| 80×96-Bäume | **Bake-Padding** auf 96×96 (8 px transparent je Seite, Inhalt unten zentriert) |
| Registry | **Auto-Scan** `assets/sprites/decoration/**/*.png` + optionale Overrides in JSON |

---

## 1. Atlas-Bake — Padding + Rebake

**Datei:** [`tools/bake_atlas.py`](tools/bake_atlas.py)

- Neue Hilfsfunktion `_pad_to_atlas_grid(image) -> Image`:
  - Pro Dimension auf nächstes Vielfaches von `ATLAS_CELL_PX` (32) aufrunden
  - 80×96 → **96×96**; Inhalt **horizontal zentriert**, **am unteren Rand** ausgerichtet (passt zu Anker unten links + Baum-Footprint)
  - 32×32 / 64×64 unverändert
- In `load_sources` / `bake_atlas`: vor dem Packen padden; `pixel_w/h` und Zellengröße aus gepaddeter Größe
- `.pdn`-Dateien weiter ignorieren (nur `.png`)
- Rebake: `python tools/bake_atlas.py` → ~70+ Sprites im Manifest (58 Decoration + bestehende Tiles/Character/…)

**Erwartete Keys (Beispiele):**
- `wt:decoration/bush/ice/ice_berry_bush_1`
- `wt:decoration/trees/apple/spring/apple_4`
- `wt:decoration/trees/maple/winter/maple_4_snowy`

---

## 2. Content-Registry (data-driven)

**Neu:** [`game_core/content_registry.py`](game_core/content_registry.py)

```python
@dataclass(frozen=True)
class DecorationDef:
    id: str              # z.B. "trees/apple/spring/apple_4"
    sprite_key: str      # wt:decoration/...
    category: str        # bush | tree | stump (aus Pfad heuristisch)
    render_layer: int    # 4=bush/stump, 5=tree (Default, override in JSON)
```

**Neu:** [`assets/content/decorations.json`](assets/content/decorations.json) — nur **Overrides**, z.B.:

```json
{
  "version": 1,
  "defaults": { "bush": { "render_layer": 4 }, "tree": { "render_layer": 5 } },
  "overrides": {
    "trees/apple/spring/apple_stump": { "category": "stump", "render_layer": 4 }
  },
  "exclude": ["*.pdn"]
}
```

**Loader-Logik:**
1. Alle `wt:decoration/…`-Keys aus [`SpriteCatalog`](render_scene/sprite_catalog.py) / Manifest iterieren **oder** PNG-Pfade unter `assets/sprites/decoration/` scannen und Keys via [`sprite_key_from_file`](render_scene/sprite_keys.py) erzeugen
2. `id` = Pfad relativ zu `decoration/` (ohne `.png`)
3. Kategorie-Heuristik: Pfad enthält `bush` → bush; `stump` → stump; sonst tree
4. Overrides aus JSON anwenden; Einträge in `exclude` überspringen

**Optional (M12b-Anteil, minimal):** [`assets/content/tiles.json`](assets/content/tiles.json) — Metadaten für `wt:tiles/path`, `foundation`, … (`layer: 1`, `walkable: true`). Nur Loader + Konstanten in `world_gen`; Pinsel-Keys bleiben vorerst hardcoded, JSON ist Vorbereitung für später data-driven Pinsel.

---

## 3. Gameplay — platzierte Decorations

**Datei:** [`game_core/world.py`](game_core/world.py) oder neu [`game_core/decorations.py`](game_core/decorations.py)

```python
@dataclass
class PlacedDecoration:
    world_x: float   # Anker unten links, Tile-snapped
    world_y: float
    decoration_id: str

# World erweitern:
decorations: list[PlacedDecoration]
place_decoration(wx_tile, wy_tile, decoration_id) -> bool
remove_decoration_at(wx_tile, wy_tile) -> bool  # Toleranz ~ halbe Tile
```

- Snap: `world_x = wx * TILE_SIZE_PX`, `world_y = wy * TILE_SIZE_PX`
- Keine Chunk-Zugehörigkeit nötig (Weltliste reicht für Demo-Größe)

**Datei:** [`game_core/world_gen.py`](game_core/world_gen.py)

- Nach `generate_demo_world`: 10–20 Decorations aus Registry (mix bush + summer trees) für sichtbaren Test

---

## 4. Bridge — Extraktion

**Neu:** [`bridge/decoration_extractor.py`](bridge/decoration_extractor.py)

```python
def decorations_to_sprites(
    registry: ContentRegistry,
    catalog: SpriteCatalog,
    world: World,
) -> tuple[SpriteInstanceData, ...]:
```

- `decoration_id` → `DecorationDef` → `catalog.resolve(sprite_key)`
- `SpriteInstanceData(world_x, world_y, sprite_id, layer=LayerId(render_layer), …)`
- Fehlende Keys → skip + log (robust bei Registry/Atlas-Drift)

**Datei:** [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py) — Frame bauen:

```python
deco = decorations_to_sprites(content, catalog, world)
player = character_to_sprite(catalog, player)
sprites = merge_and_sort_by_layer(deco + (player,))
```

---

## 5. Renderer — Sprite-Layer-Sortierung

**Datei:** [`render_graphics/tile_layer.py`](render_graphics/tile_layer.py)

- `pack_textured_tiles_and_sprites`: Sprites **vor** dem Pack nach `int(sprite.layer)` sortieren (aktuell: Reihenfolge der Übergabe, unsortiert)
- Tiles weiter global nach LayerId sortiert (bereits in `pack_textured_tile_chunks`) — **ein Draw** beibehalten

---

## 6. Demo-Steuerung (Free-Cam)

**Datei:** [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py)

Erweiterung des Pinsel-Systems (parallel zu `1`/`2` Tile-Layer):

| Taste | Aktion |
|-------|--------|
| `3` | Pinsel-Modus: **Decoration** |
| `[` / `]` | Nächster/vorheriger `DecorationDef` aus Registry (zyklisch) |
| LMB | Platzieren (Tile unter Cursor) |
| X / RMB | Entfernen an Cursor-Tile |

Fenstertitel: `paint L0/L1/decoration (1/2/3) | [name]`

Modi schließen sich gegenseitig aus: `1`=Terrain, `2`=Overlay, `3`=Decoration.

---

## 7. Dokumentation

**Datei:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

- Meilenstein-Tabelle: **M12 ✓**
- Abschnitt M12: Registry, Layer 4/5, Bake-Padding, Draw-Reihenfolge, Demo-Steuerung
- Hinweis: Jahreszeiten-Varianten (`spring`/`winter`/…) über separate Registry-IDs — Season-Logik kommt später

---

## Betroffene Dateien (Kern)

| Datei | Änderung |
|-------|----------|
| [`tools/bake_atlas.py`](tools/bake_atlas.py) | Pad-to-grid beim Laden |
| [`game_core/content_registry.py`](game_core/content_registry.py) | **neu** |
| [`assets/content/decorations.json`](assets/content/decorations.json) | **neu** (Overrides) |
| [`game_core/world.py`](game_core/world.py) | `PlacedDecoration`, place/remove |
| [`game_core/world_gen.py`](game_core/world_gen.py) | Demo-Placements |
| [`bridge/decoration_extractor.py`](bridge/decoration_extractor.py) | **neu** |
| [`render_graphics/tile_layer.py`](render_graphics/tile_layer.py) | Sprite-Sort |
| [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py) | Modus 3, `[`/`]` |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | M12 |

---

## Manuelle Verifikation

1. `python tools/bake_atlas.py` — kein Fehler bei 80×96-Bäumen; Manifest enthält `wt:decoration/…`
2. `python -m apps.chunk_world_demo` — Free-Cam: diagonale Demo-Pfade (L1) + gespawnte Bäume sichtbar
3. Modus `3`: Apfelbaum platzieren, Charakter läuft darunter/davor (L10 über L5)
4. `[`/`]`: verschiedene Varianten (bush vs tree vs stump) wechseln

---

## Bewusst nicht in M12

- Kollision / Blockierung
- Y-Sort innerhalb eines Layers (Bäume vor/hinter Figur nach `world_y`)
- Dynamische Jahreszeiten-Umschaltung
- Hot-Reload ohne Rebake
