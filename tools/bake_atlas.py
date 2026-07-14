"""Atlas-Bake-Tool — 32px-Grid-Packing, Minecraft-Style Sprite-Keys."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

from render_scene.sprite_keys import DEFAULT_SPRITE_NAMESPACE, make_sprite_key, sprite_key_from_file
from render_scene.types import ATLAS_CELL_PX, ATLAS_GUTTER_PX, TILE_SIZE_PX

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILENAME = "sprite_registry.json"

# (relativer_pfad_ohne_png, breite, höhe, rgba)
PLACEHOLDER_SPECS: tuple[tuple[str, int, int, tuple[int, int, int, int]], ...] = (
    ("tiles/grass", 32, 32, (80, 160, 70, 255)),
    ("tiles/dirt", 32, 32, (120, 85, 55, 255)),
    ("tiles/stone", 32, 32, (130, 130, 140, 255)),
    ("tiles/water", 32, 32, (50, 100, 200, 255)),
    ("tiles/deep_water", 32, 32, (20, 50, 120, 255)),
    ("tiles/shallow_water", 32, 32, (70, 140, 210, 255)),
    ("tiles/sand", 32, 32, (210, 190, 120, 255)),
    ("tiles/snow", 32, 32, (230, 235, 245, 255)),
    ("tiles/path", 32, 32, (180, 160, 100, 255)),
    ("tiles/foundation", 32, 32, (140, 140, 150, 255)),
    ("items/gear", 32, 32, (200, 180, 60, 255)),
    ("buildings/small", 64, 64, (160, 100, 70, 255)),
    ("buildings/large", 64, 128, (100, 110, 180, 255)),
)


@dataclass(frozen=True, slots=True)
class SourceSprite:
    sprite_id: int
    key: str
    name: str
    width: int
    height: int
    path: Path
    cells_w: int
    cells_h: int


@dataclass(frozen=True, slots=True)
class PackedSprite:
    sprite_id: int
    key: str
    name: str
    cells_w: int
    cells_h: int
    cell_x: int
    cell_y: int
    width: int
    height: int
    path: Path


def _next_power_of_two(value: int) -> int:
    if value <= 1:
        return 1
    return 1 << (value - 1).bit_length()


def _cells_for_size(size: int) -> int:
    if size % ATLAS_CELL_PX != 0:
        raise ValueError(f"Größe {size} ist kein Vielfaches von {ATLAS_CELL_PX}.")
    return size // ATLAS_CELL_PX


def _atlas_grid_size(size: int) -> int:
    """Nächstes Vielfaches von ATLAS_CELL_PX (mindestens eine Zelle)."""
    if size <= 0:
        return ATLAS_CELL_PX
    return max(ATLAS_CELL_PX, int(math.ceil(size / ATLAS_CELL_PX)) * ATLAS_CELL_PX)


def _pad_to_atlas_grid(image) -> tuple:
    """Pad auf 32px-Raster — horizontal zentriert, am unteren Rand ausgerichtet."""
    from PIL import Image

    width, height = image.size
    target_w = _atlas_grid_size(width)
    target_h = _atlas_grid_size(height)
    if (width, height) == (target_w, target_h):
        return image.convert("RGBA"), target_w, target_h

    padded = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    offset_x = (target_w - width) // 2
    offset_y = target_h - height
    padded.paste(image.convert("RGBA"), (offset_x, offset_y))
    return padded, target_w, target_h


def _load_sprite_registry(registry_path: Path) -> dict[str, int]:
    if not registry_path.is_file():
        return {}
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    return {str(key): int(value) for key, value in data.get("keys", data).items()}


def _save_sprite_registry(registry_path: Path, mapping: dict[str, int]) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"namespace": DEFAULT_SPRITE_NAMESPACE, "keys": dict(sorted(mapping.items()))}
    registry_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _assign_stable_sprite_ids(
    keys: list[str],
    registry_path: Path,
) -> dict[str, int]:
    """Vergibt stabile sprite_ids — bestehende Keys behalten ihre ID."""
    registry = _load_sprite_registry(registry_path)
    used_ids = set(registry.values())
    next_id = max(used_ids, default=-1) + 1
    unique_keys = sorted(set(keys))

    for key in unique_keys:
        if key in registry:
            continue
        while next_id in used_ids:
            next_id += 1
        registry[key] = next_id
        used_ids.add(next_id)
        next_id += 1

    registry = {key: registry[key] for key in unique_keys}
    _save_sprite_registry(registry_path, registry)
    return registry


def generate_placeholder_sprites(
    out_dir: Path,
    registry_path: Path,
    namespace: str = DEFAULT_SPRITE_NAMESPACE,
) -> list[SourceSprite]:
    from PIL import Image, ImageDraw

    out_dir.mkdir(parents=True, exist_ok=True)
    keys = [str(make_sprite_key(rel_path, namespace)) for rel_path, _, _, _ in PLACEHOLDER_SPECS]
    id_map = _assign_stable_sprite_ids(keys, registry_path)

    sources: list[SourceSprite] = []
    for rel_path, width, height, color in PLACEHOLDER_SPECS:
        path = out_dir / f"{rel_path}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        key = str(make_sprite_key(rel_path, namespace))
        image = Image.new("RGBA", (width, height), color)
        draw = ImageDraw.Draw(image)
        border = (255, 255, 255, 180)
        draw.rectangle((0, 0, width - 1, height - 1), outline=border, width=2)
        label = Path(rel_path).name[:8]
        draw.text((4, 4), label, fill=(255, 255, 255, 220))
        image.save(path)
        sources.append(
            SourceSprite(
                sprite_id=id_map[key],
                key=key,
                name=Path(rel_path).name,
                width=width,
                height=height,
                path=path,
                cells_w=_cells_for_size(width),
                cells_h=_cells_for_size(height),
            )
        )
    return sources


def load_sources(
    sprites_dir: Path,
    registry_path: Path,
    namespace: str = DEFAULT_SPRITE_NAMESPACE,
) -> list[SourceSprite]:
    from PIL import Image

    if not sprites_dir.is_dir():
        raise FileNotFoundError(f"Sprite-Ordner nicht gefunden: {sprites_dir}")

    paths = sorted(sprites_dir.rglob("*.png"))
    if not paths:
        raise FileNotFoundError(f"Keine PNGs unter {sprites_dir}")

    keys = [str(sprite_key_from_file(path, sprites_dir, namespace=namespace)) for path in paths]
    id_map = _assign_stable_sprite_ids(keys, registry_path)

    sources: list[SourceSprite] = []
    for path in paths:
        key = str(sprite_key_from_file(path, sprites_dir, namespace=namespace))
        with Image.open(path) as image:
            _, width, height = _pad_to_atlas_grid(image)
        sources.append(
            SourceSprite(
                sprite_id=id_map[key],
                key=key,
                name=path.stem,
                width=width,
                height=height,
                path=path,
                cells_w=_cells_for_size(width),
                cells_h=_cells_for_size(height),
            )
        )
    return sources


def pack_grid(
    sources: list[SourceSprite],
    atlas_cells_x: int,
    atlas_cells_y: int,
) -> list[PackedSprite]:
    """Shelf-Packing auf Zellenraster — sortiert nach Höhe absteigend."""
    sorted_sources = sorted(sources, key=lambda s: (s.cells_h, s.cells_w), reverse=True)
    occupied: set[tuple[int, int]] = set()
    packed: list[PackedSprite] = []

    def can_place(cx: int, cy: int, cw: int, ch: int) -> bool:
        if cx + cw > atlas_cells_x or cy + ch > atlas_cells_y:
            return False
        for y in range(cy, cy + ch):
            for x in range(cx, cx + cw):
                if (x, y) in occupied:
                    return False
        return True

    def occupy(cx: int, cy: int, cw: int, ch: int) -> None:
        for y in range(cy, cy + ch):
            for x in range(cx, cx + cw):
                occupied.add((x, y))

    for source in sorted_sources:
        placed = False
        for cy in range(atlas_cells_y):
            for cx in range(atlas_cells_x):
                if can_place(cx, cy, source.cells_w, source.cells_h):
                    occupy(cx, cy, source.cells_w, source.cells_h)
                    packed.append(
                        PackedSprite(
                            sprite_id=source.sprite_id,
                            key=source.key,
                            name=source.name,
                            cells_w=source.cells_w,
                            cells_h=source.cells_h,
                            cell_x=cx,
                            cell_y=cy,
                            width=source.width,
                            height=source.height,
                            path=source.path,
                        )
                    )
                    placed = True
                    break
            if placed:
                break
        if not placed:
            raise RuntimeError(
                f"Sprite {source.key} ({source.cells_w}x{source.cells_h} Zellen) "
                f"passt nicht in {atlas_cells_x}x{atlas_cells_y} Atlas."
            )
    return packed


def _atlas_size_for_sources(sources: list[SourceSprite]) -> tuple[int, int]:
    total_cells = sum(s.cells_w * s.cells_h for s in sources)
    side = _next_power_of_two(int(math.ceil(math.sqrt(total_cells))))
    cells = max(side, 8)
    return cells, cells


SHEET_FRAME_PX = 64


def _detect_sheet_grid(width: int, height: int) -> tuple[int, int]:
    """Spritesheet-Grid in 64px-Frames — sonst 1×1."""
    if (
        width >= SHEET_FRAME_PX * 2
        and height >= SHEET_FRAME_PX
        and width % SHEET_FRAME_PX == 0
        and height % SHEET_FRAME_PX == 0
    ):
        return width // SHEET_FRAME_PX, height // SHEET_FRAME_PX
    return 1, 1


def sprite_rect_uv(
    cell_x: int,
    cell_y: int,
    cells_w: int,
    cells_h: int,
    atlas_w: int,
    atlas_h: int,
    pixel_w: int,
    pixel_h: int,
) -> tuple[float, float, float, float]:
    """UV-Rect exakt über eingefügten Pixelbereich (pixel_w×pixel_h ab Gutter-Offset)."""
    px_x = cell_x * ATLAS_CELL_PX + ATLAS_GUTTER_PX
    px_y = cell_y * ATLAS_CELL_PX + ATLAS_GUTTER_PX
    u0 = px_x / atlas_w
    v0 = px_y / atlas_h
    u1 = (px_x + pixel_w) / atlas_w
    v1 = (px_y + pixel_h) / atlas_h
    return u0, v0, u1, v1


def bake_atlas(
    sources: list[SourceSprite],
    out_dir: Path,
    atlas_cells_x: int | None = None,
    atlas_cells_y: int | None = None,
) -> tuple[Path, Path]:
    from PIL import Image

    if not sources:
        raise ValueError("Keine Quell-Sprites zum Backen.")

    if atlas_cells_x is None or atlas_cells_y is None:
        atlas_cells_x, atlas_cells_y = _atlas_size_for_sources(sources)

    packed = pack_grid(sources, atlas_cells_x, atlas_cells_y)
    atlas_w = atlas_cells_x * ATLAS_CELL_PX
    atlas_h = atlas_cells_y * ATLAS_CELL_PX

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    entries: list[dict] = []

    for item in packed:
        with Image.open(item.path) as sprite_image:
            padded_image, _, _ = _pad_to_atlas_grid(sprite_image)
            px_x = item.cell_x * ATLAS_CELL_PX + ATLAS_GUTTER_PX
            px_y = item.cell_y * ATLAS_CELL_PX + ATLAS_GUTTER_PX
            atlas.paste(padded_image, (px_x, px_y))
        u0, v0, u1, v1 = sprite_rect_uv(
            item.cell_x,
            item.cell_y,
            item.cells_w,
            item.cells_h,
            atlas_w,
            atlas_h,
            item.width,
            item.height,
        )
        sheet_cols, sheet_rows = _detect_sheet_grid(item.width, item.height)
        entries.append(
            {
                "sprite_id": item.sprite_id,
                "key": item.key,
                "name": item.name,
                "cells_w": item.cells_w,
                "cells_h": item.cells_h,
                "cell_x": item.cell_x,
                "cell_y": item.cell_y,
                "pixel_w": item.width,
                "pixel_h": item.height,
                "sheet_cols": sheet_cols,
                "sheet_rows": sheet_rows,
                "u0": u0,
                "v0": v0,
                "u1": u1,
                "v1": v1,
            }
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    atlas_path = out_dir / "atlas.png"
    manifest_path = out_dir / "manifest.json"
    atlas.save(atlas_path)

    manifest = {
        "version": 2,
        "namespace": DEFAULT_SPRITE_NAMESPACE,
        "tile_size_px": TILE_SIZE_PX,
        "atlas_cell_px": ATLAS_CELL_PX,
        "gutter_px": ATLAS_GUTTER_PX,
        "width": atlas_w,
        "height": atlas_h,
        "texture_handle": 1,
        "material_handle": 1,
        "entries": sorted(entries, key=lambda entry: entry["key"]),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return atlas_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Backt einen 32px-Grid-Texture-Atlas.")
    parser.add_argument(
        "--sprites",
        type=Path,
        default=PROJECT_ROOT / "assets" / "sprites",
        help="Wurzelordner mit Quell-PNGs (rekursiv)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "assets" / "demo_atlas",
        help="Ausgabeordner für atlas.png + manifest.json",
    )
    parser.add_argument(
        "--namespace",
        type=str,
        default=DEFAULT_SPRITE_NAMESPACE,
        help="Sprite-Key-Namespace (default: wt)",
    )
    parser.add_argument(
        "--generate-placeholders",
        action="store_true",
        help="Platzhalter-Sprites erzeugen, falls Ordner leer ist",
    )
    args = parser.parse_args()

    sprites_dir = args.sprites
    registry_path = args.out / REGISTRY_FILENAME
    has_pngs = sprites_dir.exists() and bool(list(sprites_dir.rglob("*.png")))

    if args.generate_placeholders or not has_pngs:
        print(f"Platzhalter-Sprites -> {sprites_dir}")
        sources = generate_placeholder_sprites(sprites_dir, registry_path, namespace=args.namespace)
    else:
        sources = load_sources(sprites_dir, registry_path, namespace=args.namespace)

    atlas_path, manifest_path = bake_atlas(sources, args.out)
    print(f"Atlas: {atlas_path}")
    print(f"Manifest: {manifest_path} ({len(sources)} Sprites)")
    print(f"Registry: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
