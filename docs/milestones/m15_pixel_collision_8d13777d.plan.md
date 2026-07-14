---
name: M15 Pixel Collision
overview: "M15 ersetzt die grobe Tile-Footprint-Kollision (M14) durch Alpha-basierte Masken und ein 8×8-px Chunk-Solid-Grid. Charakter: voller 64×64-Körper pro Blickrichtung (8 Masken); Decorations: Stamm-Maske aus Alpha; Tiles: Wasser als volle Tile-Zelle im Grid."
todos:
  - id: m15-bake
    content: tools/bake_collision.py + assets/collision/manifest.json (Char 8× Walk-Union, Deco Stamm/Alpha)
    status: completed
  - id: m15-catalog
    content: game_core/collision_catalog.py — CollisionMask, load_collision_catalog()
    status: completed
  - id: m15-grid
    content: game_core/collision_grid.py + World.solid_grid rebuild/dirty hooks
    status: completed
  - id: m15-nav
    content: "navigation.py: mask_position_blocked + apply_character_movement mit CollisionCatalog"
    status: completed
  - id: m15-demo
    content: "chunk_world_demo: collision load, rebuild_all_solid nach world gen"
    status: completed
  - id: m15-tests
    content: tests/test_collision.py — Stamm vs Tile, Wasser, Grid-Stamp
    status: completed
  - id: m15-docs
    content: ARCHITECTURE.md M15 Abschnitt + Rebake-Hinweis
    status: completed
isProject: false
---

# M15 — Pixel-Kollision (Masken + Solid-Grid)

## Ziel

Bewegung blockiert dort, wo **opaque Sprite-Pixel** (bzw. eingestempelte Solid-Zellen) überlappen — nicht mehr das ganze 32×32-Tile. Renderer und Bridge bleiben unverändert; alles in `game_core` + Bake-Tool.

**Bestätigte Entscheidungen:**
- Charakter: **voller 64×64-Körper**, **8 Masken** (eine pro Sheet-Zeile/Richtung)
- Welt-Solid-Grid: **8×8 px pro Zelle** (4×4 Zellen pro Tile)

```mermaid
flowchart LR
  png[PNG Alpha]
  bake[tools/bake_collision.py]
  manifest[assets/collision/manifest.json]
  catalog[CollisionCatalog]
  chunk[ChunkSolidGrid]
  nav[navigation.py]
  png --> bake --> manifest --> catalog
  catalog --> chunk
  chunk --> nav
```

---

## 1. Kollisionsmasken bake

**Neu:** [`tools/bake_collision.py`](tools/bake_collision.py)

- Liest dieselben PNGs wie [`tools/bake_atlas.py`](tools/bake_atlas.py) (`_pad_to_atlas_grid` wiederverwenden oder importieren)
- **Alpha-Schwelle:** Pixel solid wenn `alpha >= 128`
- **Output:** [`assets/collision/manifest.json`](assets/collision/manifest.json)

Manifest-Eintrag pro Maske:

```json
{
  "key": "wt:character/walk/walk",
  "direction": 3,
  "width": 64,
  "height": 64,
  "bits": "<base64 row-major bitset>"
}
```

**Charakter (8 Richtungen):**
- Quelle: [`assets/sprites/character/walk/walk.png`](assets/sprites/character/walk/walk.png) (8×8 Grid, 64px Frames)
- Pro Zeile `direction 0..7`: **Union aller 8 Frames** in dieser Zeile → voller Körper über den Walk-Zyklus, keine Lücken zwischen Frames
- Idle/Run optional identisch später; M15 nutzt Walk-Union als Kollisions-Hülle für alle Clips

**Decorations:**
- Key `wt:decoration/…` → Maske aus gepaddeter PNG
- **Bäume:** nur Stamm — vertikal `0 .. trunk_clip_v1` (Default **0.38**, gleiche Konstante wie [`assets/content/decorations.json`](assets/content/decorations.json))
- **Bush/Stump:** volle Alpha-Maske
- Metadaten: `width`, `height`, `anchor: bottom-left` (implizit)

**Aufruf:** `python tools/bake_collision.py` (parallel zu Atlas-Rebake, kein GPU-Bezug)

---

## 2. CollisionCatalog (gameplay)

**Neu:** [`game_core/collision_catalog.py`](game_core/collision_catalog.py)

```python
@dataclass(frozen=True)
class CollisionMask:
    width: int
    height: int
    bits: bytes  # row-major, bit=1 → solid

@dataclass(frozen=True)
class CollisionCatalog:
    character_by_direction: tuple[CollisionMask, ...]  # len 8
    decoration_by_key: dict[str, CollisionMask]
```

- Loader aus `assets/collision/manifest.json`
- Hilfsmethoden: `mask_solid_pixels(mask) -> list[tuple[int,int]]` (lazy gecacht pro Maske)
- `load_collision_catalog()` in Demo neben `load_content_registry()` aufrufen

---

## 3. Chunk-Solid-Grid (Broad Phase)

**Neu:** [`game_core/collision_grid.py`](game_core/collision_grid.py)

Konstanten:
- `COLLISION_CELL_PX = 8`
- Pro Chunk (256×256 px): **32×32 Zellen** = 128 Byte Bitset

**Neu in [`game_core/world.py`](game_core/world.py):**

```python
@dataclass
class Chunk:
    ...
    solid_grid: bytes | None = None  # 128 Byte, lazy

@dataclass
class World:
    ...
    def rebuild_chunk_solid(self, coord, content, collision): ...
    def mark_collision_dirty(self, coord): ...
    collision_dirty_chunks: set[tuple[int,int]]
```

**Grid befüllen (`rebuild_chunk_solid`):**
1. **Terrain L0:** nicht walkable (Wasser) → 4×4 Zellen pro Tile solid ([`ContentRegistry.tile_walkable`](game_core/content_registry.py))
2. **Overlay L1:** nur wenn Key gesetzt und `walkable: false`
3. **Decorations** in Chunk-Bounds: Maske an `(world_x, world_y)` einstempeln (nur solid bits)

**Hooks (Dirty):**
- `World.set_tile` → `mark_collision_dirty(coord)`
- `World.place_decoration` / `remove_decoration_at` → alle betroffenen Chunks (Maske kann 96×96 über Tile-Grenzen ragen)

**Abfrage:**

```python
def world_cell_solid(world, wx_cell, wy_cell) -> bool
def mask_position_blocked(world, collision, content, char, world_x, world_y) -> bool
```

Narrow phase: für jede solide Pixelkoordinate `(px, py)` in `character_mask[direction]`:

```text
world_cell_solid(floor((world_x+px)/8), floor((world_y+py)/8))
```

---

## 4. Navigation ersetzen/ erweitern

**Datei:** [`game_core/navigation.py`](game_core/navigation.py)

| Funktion | Änderung |
|----------|----------|
| `anchor_position_blocked` | Signatur + Implementierung: nutzt `CollisionCatalog` + `character.direction` |
| `apply_character_movement` | `collision`-Parameter durchreichen |
| `spawn_character_at_center` | ebenfalls Masken-Check |
| `footprint_tile_coords` | deprecated / intern nur Fallback |

**Fallback (M14):** Wenn für Decoration kein Mask-Eintrag → `blocks_movement` + Tile-Check wie bisher.

**Axis-Slide** bleibt unverändert — nur die Blockier-Prüfung wird feiner.

---

## 5. Demo + Welt-Init

**Datei:** [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py)

```python
collision = load_collision_catalog()
content = load_content_registry()
world = generate_demo_world(...)
world.rebuild_all_solid(content, collision)  # einmalig nach Gen + populate_demo_decorations
```

Reihenfolge: Welt → Decorations → **Solid-Rebuild** → `spawn_character_at_center`.

---

## 6. Tests

**Neu:** [`tests/test_collision.py`](tests/test_collision.py)

- Mask bake: Baum-Stamm-Maske hat weniger solid pixels als volle Höhe
- Charakter-Maske Richtung 0 vs 3 unterschiedlich (nicht identisch)
- `mask_position_blocked`: Position in Wasser blockiert
- Position **neben** schmalem Stamm (gleiches Tile, anderer Pixel) **nicht** blockiert — Kernfall vs M14
- Decoration platzieren → Solid-Grid aktualisiert

---

## 7. Dokumentation

**Datei:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

- Meilenstein **M15** in Tabelle + Abschnitt
- Konventionen: 8px-Grid, 8 Char-Masken, Stamm-Clip = Kollision
- Rebake: `python tools/bake_collision.py`

---

## Betroffene Dateien (Kern)

| Datei | Änderung |
|-------|----------|
| [`tools/bake_collision.py`](tools/bake_collision.py) | **neu** |
| [`assets/collision/manifest.json`](assets/collision/manifest.json) | **neu** (generiert) |
| [`game_core/collision_catalog.py`](game_core/collision_catalog.py) | **neu** |
| [`game_core/collision_grid.py`](game_core/collision_grid.py) | **neu** |
| [`game_core/world.py`](game_core/world.py) | `solid_grid`, dirty, rebuild |
| [`game_core/navigation.py`](game_core/navigation.py) | Masken-Check |
| [`apps/chunk_world_demo.py`](apps/chunk_world_demo.py) | Catalog + rebuild |
| [`tests/test_collision.py`](tests/test_collision.py) | **neu** |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | M15 |

**Keine Änderung:** Shader, `render_*`, Bridge, Atlas-Manifest (Render)

---

## Manuelle Verifikation

1. `python tools/bake_collision.py`
2. `python -m apps.chunk_world_demo`
3. Um Baumstamm herumlaufen — ** seitlich enger** als Tile-Box; unter Krone durchlaufen (Kollision nur Stamm)
4. Wasser weiterhin undurchlässig
5. Richtungswechsel: Kollisionshülle dreht mit (`character.direction`)

---

## Bewusst nicht in M15

- Krone blockiert separat (nur Stamm-Maske)
- Idle/Run eigene Masken (Walk-Union für alle Clips)
- Swept pixel collision entlang Bewegungsvektor
- Save/Load des Solid-Grids (wird aus Welt neu gebaut)
- Multi-Entity-Kollision
