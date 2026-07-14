"""Content-Registry — data-driven Decoration- und Tile-Metadaten."""

from __future__ import annotations

import json
import fnmatch
from dataclasses import dataclass, field
from pathlib import Path

from render_scene.sprite_keys import DEFAULT_SPRITE_NAMESPACE, make_sprite_key

from game_core.tile_ids import build_tile_key_by_id, stable_tile_id

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DECORATIONS_CONFIG = PROJECT_ROOT / "assets" / "content" / "decorations.json"
DEFAULT_TILES_CONFIG = PROJECT_ROOT / "assets" / "content" / "tiles.json"
DEFAULT_DECORATION_SPRITES_ROOT = PROJECT_ROOT / "assets" / "sprites" / "decoration"

DECORATION_LAYER_BUSH = 4
DECORATION_LAYER_TREE = 5
DECORATION_LAYER_CANOPY = 6


@dataclass(frozen=True, slots=True)
class DecorationDef:
    """Platzierbare Decoration — id relativ zu decoration/."""

    id: str
    sprite_key: str
    category: str
    render_layer: int
    sort_y_offset: float = 0.0
    canopy_layer: int | None = None
    trunk_clip_v1: float = 1.0
    canopy_clip_v0: float = 0.0
    canopy_sort_y_offset: float = 0.0
    blocks_movement: bool = False


@dataclass(frozen=True, slots=True)
class TileDef:
    """Tile-Metadaten — Layer, Walkability, Anzeige-Label."""

    sprite_key: str
    layer: int
    walkable: bool
    label: str = ""


@dataclass(frozen=True, slots=True)
class TileBrushPalette:
    """Pinsel-Set für einen Demo-Modus — Maus + Tasten → Tile-Keys."""

    mode: str
    layer: int
    mouse_left: str | None = None
    mouse_right: str | None = None
    key_bindings: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class ContentRegistry:
    decorations: tuple[DecorationDef, ...]
    tiles: tuple[TileDef, ...]
    brush_palettes: tuple[TileBrushPalette, ...] = ()
    _tile_walkable: dict[str, bool] = field(default_factory=dict, repr=False)
    _tile_by_key: dict[str, TileDef] = field(default_factory=dict, repr=False)
    _tile_key_by_id: dict[int, str] = field(default_factory=dict, repr=False)
    _decoration_key_by_id: dict[int, str] = field(default_factory=dict, repr=False)
    _brush_by_mode: dict[str, TileBrushPalette] = field(default_factory=dict, repr=False)
    _decoration_by_id: dict[str, DecorationDef] = field(default_factory=dict, repr=False)

    def decoration_by_id(self, decoration_id: str) -> DecorationDef | None:
        return self._decoration_by_id.get(decoration_id)

    def decoration_ids(self) -> tuple[str, ...]:
        return tuple(entry.id for entry in self.decorations)

    def tile_by_key(self, sprite_key: str) -> TileDef | None:
        return self._tile_by_key.get(sprite_key)

    def tile_label(self, sprite_key: str) -> str:
        """Anzeigename — Label aus JSON oder Kurzform des Keys."""
        if not sprite_key:
            return "clear"
        entry = self._tile_by_key.get(sprite_key)
        if entry is not None and entry.label:
            return entry.label
        prefix = f"{DEFAULT_SPRITE_NAMESPACE}:tiles/"
        if sprite_key.startswith(prefix):
            return sprite_key[len(prefix) :]
        return sprite_key

    def brush_palette(self, mode: str) -> TileBrushPalette | None:
        return self._brush_by_mode.get(mode)

    def tile_walkable(self, sprite_key: str) -> bool:
        """True wenn leer oder kein Eintrag — unbekannte Keys sind begehbar."""
        if not sprite_key:
            return True
        return self._tile_walkable.get(sprite_key, True)

    def tile_key_to_id(self, sprite_key: str) -> int:
        """Stabile FNV-Tile-ID — unabhängig von JSON-Reihenfolge (M22c)."""
        return stable_tile_id(sprite_key)

    def tile_id_to_key(self, tile_id: int) -> str:
        key = self._tile_key_by_id.get(tile_id)
        if key is None:
            raise KeyError(f"Unbekannte Tile-ID: {tile_id}")
        return key

    def decoration_id_to_key(self, decoration_id: int) -> str:
        key = self._decoration_key_by_id.get(decoration_id)
        if key is None:
            raise KeyError(f"Unbekannte Decoration-ID: {decoration_id}")
        return key

    def decoration_blocks(self, decoration_id: str) -> bool:
        entry = self.decoration_by_id(decoration_id)
        if entry is None:
            return False
        return entry.blocks_movement


def _infer_category(relative_id: str) -> str:
    lowered = relative_id.lower().replace("\\", "/")
    if "stump" in lowered:
        return "stump"
    if "/bush/" in lowered or lowered.startswith("bush/"):
        return "bush"
    return "tree"


def _default_render_layer(category: str, defaults: dict) -> int:
    category_defaults = defaults.get(category, {})
    layer = category_defaults.get("render_layer")
    if layer is not None:
        return int(layer)
    if category in ("bush", "stump"):
        return DECORATION_LAYER_BUSH
    return DECORATION_LAYER_TREE


def _category_default(category: str, defaults: dict, key: str, fallback):
    category_defaults = defaults.get(category, {})
    if key in category_defaults:
        return category_defaults[key]
    return fallback


def _decoration_field(override: dict, category: str, defaults: dict, key: str, fallback):
    if key in override:
        return override[key]
    return _category_default(category, defaults, key, fallback)


def _is_excluded(relative_id: str, exclude_patterns: list[str]) -> bool:
    normalized = relative_id.replace("\\", "/")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in exclude_patterns)


def _scan_decoration_pngs(sprites_root: Path) -> list[tuple[str, str]]:
    if not sprites_root.is_dir():
        return []
    entries: list[tuple[str, str]] = []
    for path in sorted(sprites_root.rglob("*.png")):
        relative = path.relative_to(sprites_root).with_suffix("")
        decoration_id = relative.as_posix()
        sprite_key = str(
            make_sprite_key(f"decoration/{decoration_id}", DEFAULT_SPRITE_NAMESPACE)
        )
        entries.append((decoration_id, sprite_key))
    return entries


def _validate_brush_key(
    sprite_key: str,
    known_keys: set[str],
    context: str,
) -> None:
    if sprite_key and sprite_key not in known_keys:
        raise ValueError(f"{context}: unbekannter Tile-Key '{sprite_key}'")


def _parse_brush_palette(
    mode: str,
    meta: dict,
    known_keys: set[str],
) -> TileBrushPalette:
    layer = int(meta.get("layer", 0))
    mouse_left = meta.get("mouse_left")
    mouse_right = meta.get("mouse_right")
    if mouse_left is not None:
        mouse_left = str(mouse_left)
        _validate_brush_key(mouse_left, known_keys, f"brushes.{mode}.mouse_left")
    if mouse_right is not None:
        mouse_right = str(mouse_right)
        _validate_brush_key(mouse_right, known_keys, f"brushes.{mode}.mouse_right")

    key_bindings: list[tuple[str, str]] = []
    for key_name, sprite_key in meta.get("keys", {}).items():
        key = str(sprite_key)
        _validate_brush_key(key, known_keys, f"brushes.{mode}.keys.{key_name}")
        key_bindings.append((str(key_name).upper(), key))

    return TileBrushPalette(
        mode=mode,
        layer=layer,
        mouse_left=mouse_left,
        mouse_right=mouse_right,
        key_bindings=tuple(key_bindings),
    )


def load_content_registry(
    decorations_config: Path | None = None,
    tiles_config: Path | None = None,
    sprites_root: Path | None = None,
) -> ContentRegistry:
    deco_path = decorations_config or DEFAULT_DECORATIONS_CONFIG
    tiles_path = tiles_config or DEFAULT_TILES_CONFIG
    root = sprites_root or DEFAULT_DECORATION_SPRITES_ROOT

    deco_data = json.loads(deco_path.read_text(encoding="utf-8"))
    defaults = deco_data.get("defaults", {})
    overrides = deco_data.get("overrides", {})
    exclude = list(deco_data.get("exclude", []))

    decorations: list[DecorationDef] = []
    for decoration_id, sprite_key in _scan_decoration_pngs(root):
        if _is_excluded(decoration_id, exclude):
            continue
        override = overrides.get(decoration_id, {})
        category = str(override.get("category", _infer_category(decoration_id)))
        render_layer = int(
            override.get("render_layer", _default_render_layer(category, defaults))
        )
        sort_y_offset = float(_decoration_field(override, category, defaults, "sort_y_offset", 0.0))
        canopy_layer_raw = _decoration_field(override, category, defaults, "canopy_layer", None)
        canopy_layer = int(canopy_layer_raw) if canopy_layer_raw is not None else None
        trunk_clip_v1 = float(_decoration_field(override, category, defaults, "trunk_clip_v1", 1.0))
        canopy_clip_v0 = float(_decoration_field(override, category, defaults, "canopy_clip_v0", 0.0))
        canopy_sort_y_offset = float(
            _decoration_field(override, category, defaults, "canopy_sort_y_offset", 0.0)
        )
        blocks_movement = bool(
            _decoration_field(override, category, defaults, "blocks_movement", False)
        )
        decorations.append(
            DecorationDef(
                id=decoration_id,
                sprite_key=sprite_key,
                category=category,
                render_layer=render_layer,
                sort_y_offset=sort_y_offset,
                canopy_layer=canopy_layer,
                trunk_clip_v1=trunk_clip_v1,
                canopy_clip_v0=canopy_clip_v0,
                canopy_sort_y_offset=canopy_sort_y_offset,
                blocks_movement=blocks_movement,
            )
        )

    tile_walkable_map: dict[str, bool] = {}
    tile_by_key: dict[str, TileDef] = {}
    tiles: list[TileDef] = []
    brush_palettes: list[TileBrushPalette] = []
    if tiles_path.is_file():
        tile_data = json.loads(tiles_path.read_text(encoding="utf-8"))
        for sprite_key, meta in tile_data.get("tiles", {}).items():
            key = str(sprite_key)
            walkable = bool(meta.get("walkable", True))
            tile_walkable_map[key] = walkable
            tile_def = TileDef(
                sprite_key=key,
                layer=int(meta.get("layer", 0)),
                walkable=walkable,
                label=str(meta.get("label", "")),
            )
            tiles.append(tile_def)
            tile_by_key[key] = tile_def

        known_keys = set(tile_by_key.keys())
        for mode, brush_meta in tile_data.get("brushes", {}).items():
            brush_palettes.append(_parse_brush_palette(str(mode), brush_meta, known_keys))

    tile_key_by_id = build_tile_key_by_id(list(tile_by_key.keys()) + [""])
    brush_by_mode = {palette.mode: palette for palette in brush_palettes}
    decoration_by_id = {entry.id: entry for entry in decorations}
    decoration_key_by_id = build_tile_key_by_id(list(decoration_by_id.keys()))

    return ContentRegistry(
        decorations=tuple(sorted(decorations, key=lambda entry: entry.id)),
        tiles=tuple(tiles),
        brush_palettes=tuple(brush_palettes),
        _tile_walkable=tile_walkable_map,
        _tile_by_key=tile_by_key,
        _tile_key_by_id=tile_key_by_id,
        _decoration_key_by_id=decoration_key_by_id,
        _brush_by_mode=brush_by_mode,
        _decoration_by_id=decoration_by_id,
    )


def decoration_id_from_sprite_key(sprite_key: str) -> str | None:
    prefix = f"{DEFAULT_SPRITE_NAMESPACE}:decoration/"
    normalized = sprite_key.strip().lower()
    if not normalized.startswith(prefix):
        return None
    return normalized[len(prefix) :]
