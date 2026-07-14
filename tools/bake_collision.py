"""Kollisionsmasken-Bake — Alpha aus PNGs, unabhängig vom GPU-Atlas."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from render_scene.sprite_keys import DEFAULT_SPRITE_NAMESPACE, make_sprite_key

from tools.bake_atlas import SHEET_FRAME_PX, _pad_to_atlas_grid
ALPHA_THRESHOLD = 128
CHARACTER_WALK_KEY = f"{DEFAULT_SPRITE_NAMESPACE}:character/walk/walk"
CHARACTER_WALK_PATH = PROJECT_ROOT / "assets" / "sprites" / "character" / "walk" / "walk.png"
DECORATIONS_CONFIG = PROJECT_ROOT / "assets" / "content" / "decorations.json"
DECORATION_ROOT = PROJECT_ROOT / "assets" / "sprites" / "decoration"


def _infer_category(relative_id: str) -> str:
    lowered = relative_id.lower().replace("\\", "/")
    if "stump" in lowered:
        return "stump"
    if "/bush/" in lowered or lowered.startswith("bush/"):
        return "bush"
    return "tree"


def _load_deco_defaults() -> dict:
    if not DECORATIONS_CONFIG.is_file():
        return {}
    data = json.loads(DECORATIONS_CONFIG.read_text(encoding="utf-8"))
    return data.get("defaults", {})


def _trunk_clip_v1(category: str, defaults: dict) -> float:
    category_defaults = defaults.get(category, {})
    if category == "tree":
        return float(category_defaults.get("trunk_clip_v1", 0.38))
    return 1.0


def _mask_bits_from_alpha(
    image,
    *,
    alpha_threshold: int = ALPHA_THRESHOLD,
    trunk_clip_v1: float = 1.0,
) -> tuple[int, int, bytes]:
    """Bitmaske row-major — Anker unten links, py=0 unten."""
    width, height = image.size
    pixel_count = width * height
    byte_count = (pixel_count + 7) // 8
    raw = bytearray(byte_count)
    pixels = image.load()
    max_trunk_y = int(height * trunk_clip_v1) if trunk_clip_v1 < 1.0 else height

    for iy in range(height):
        local_y = height - 1 - iy
        if local_y > max_trunk_y:
            continue
        for ix in range(width):
            _, _, _, alpha = pixels[ix, iy]
            if alpha < alpha_threshold:
                continue
            bit_index = local_y * width + ix
            raw[bit_index >> 3] |= 1 << (bit_index & 7)
    return width, height, bytes(raw)


def _encode_bits(bits: bytes) -> str:
    return base64.standard_b64encode(bits).decode("ascii")


def _union_frame_into(accumulator: bytearray, frame_bits: bytes) -> None:
    for index, value in enumerate(frame_bits):
        accumulator[index] |= value


def bake_character_masks(
    walk_path: Path,
    *,
    alpha_threshold: int = ALPHA_THRESHOLD,
) -> list[dict]:
    from PIL import Image

    if not walk_path.is_file():
        raise FileNotFoundError(f"Walk-Sheet nicht gefunden: {walk_path}")

    entries: list[dict] = []
    with Image.open(walk_path) as sheet:
        padded, width, height = _pad_to_atlas_grid(sheet)
        cols = width // SHEET_FRAME_PX
        rows = height // SHEET_FRAME_PX
        if cols < 1 or rows < 8:
            raise ValueError(f"Walk-Sheet erwartet 8 Zeilen à 64px, erhalten {cols}x{rows} Frames.")

        for direction in range(8):
            union_bits: bytearray | None = None
            mask_w = SHEET_FRAME_PX
            mask_h = SHEET_FRAME_PX
            for col in range(cols):
                left = col * SHEET_FRAME_PX
                top = direction * SHEET_FRAME_PX
                frame = padded.crop((left, top, left + SHEET_FRAME_PX, top + SHEET_FRAME_PX))
                frame_w, frame_h, frame_bits = _mask_bits_from_alpha(
                    frame,
                    alpha_threshold=alpha_threshold,
                )
                mask_w, mask_h = frame_w, frame_h
                if union_bits is None:
                    union_bits = bytearray(frame_bits)
                else:
                    _union_frame_into(union_bits, frame_bits)
            if union_bits is None:
                continue
            entries.append(
                {
                    "kind": "character",
                    "key": CHARACTER_WALK_KEY,
                    "direction": direction,
                    "width": mask_w,
                    "height": mask_h,
                    "bits": _encode_bits(bytes(union_bits)),
                }
            )
    return entries


def bake_decoration_masks(
    sprites_root: Path,
    *,
    alpha_threshold: int = ALPHA_THRESHOLD,
) -> list[dict]:
    from PIL import Image

    defaults = _load_deco_defaults()
    if not sprites_root.is_dir():
        return []

    entries: list[dict] = []
    for path in sorted(sprites_root.rglob("*.png")):
        relative = path.relative_to(sprites_root).with_suffix("").as_posix()
        category = _infer_category(relative)
        trunk_clip = _trunk_clip_v1(category, defaults)
        key = str(make_sprite_key(f"decoration/{relative}", DEFAULT_SPRITE_NAMESPACE))
        with Image.open(path) as image:
            padded, _, _ = _pad_to_atlas_grid(image)
            mask_w, mask_h, mask_bits = _mask_bits_from_alpha(
                padded,
                alpha_threshold=alpha_threshold,
                trunk_clip_v1=trunk_clip,
            )
        entries.append(
            {
                "kind": "decoration",
                "key": key,
                "width": mask_w,
                "height": mask_h,
                "bits": _encode_bits(mask_bits),
            }
        )
    return entries


def bake_collision_manifest(
    *,
    walk_path: Path = CHARACTER_WALK_PATH,
    decoration_root: Path = DECORATION_ROOT,
    alpha_threshold: int = ALPHA_THRESHOLD,
) -> dict:
    masks = bake_character_masks(walk_path, alpha_threshold=alpha_threshold)
    masks.extend(bake_decoration_masks(decoration_root, alpha_threshold=alpha_threshold))
    return {
        "version": 1,
        "alpha_threshold": alpha_threshold,
        "character_key": CHARACTER_WALK_KEY,
        "masks": sorted(masks, key=lambda entry: (entry.get("kind", ""), entry.get("key", ""), entry.get("direction", -1))),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Backt Kollisionsmasken aus Sprite-PNGs.")
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "assets" / "collision" / "manifest.json",
        help="Ausgabe manifest.json",
    )
    parser.add_argument(
        "--walk",
        type=Path,
        default=CHARACTER_WALK_PATH,
        help="Charakter-Walk-Spritesheet",
    )
    parser.add_argument(
        "--decorations",
        type=Path,
        default=DECORATION_ROOT,
        help="Decoration-Sprite-Wurzel",
    )
    args = parser.parse_args()

    manifest = bake_collision_manifest(walk_path=args.walk, decoration_root=args.decorations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    character_count = sum(1 for entry in manifest["masks"] if entry["kind"] == "character")
    decoration_count = sum(1 for entry in manifest["masks"] if entry["kind"] == "decoration")
    print(f"Collision manifest: {args.out}")
    print(f"  character directions: {character_count}")
    print(f"  decorations: {decoration_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
