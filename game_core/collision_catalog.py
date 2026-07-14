"""CollisionCatalog — Alpha-Bitmasken für Pixel-Kollision."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COLLISION_MANIFEST = PROJECT_ROOT / "assets" / "collision" / "manifest.json"


@dataclass(frozen=True, slots=True)
class CollisionMask:
    width: int
    height: int
    bits: bytes

    def solid_pixel_count(self) -> int:
        return sum(byte.bit_count() for byte in self.bits)


@dataclass(frozen=True, slots=True)
class CollisionCatalog:
    character_key: str
    character_by_direction: tuple[CollisionMask, ...]
    decoration_by_key: dict[str, CollisionMask]

    def character_mask(self, direction: int) -> CollisionMask:
        index = direction % len(self.character_by_direction)
        return self.character_by_direction[index]

    def decoration_mask(self, sprite_key: str) -> CollisionMask | None:
        return self.decoration_by_key.get(sprite_key)

    def solid_offsets(self, mask: CollisionMask) -> tuple[tuple[int, int], ...]:
        return _solid_offsets_cached(mask.width, mask.height, mask.bits)


def _decode_bits(encoded: str) -> bytes:
    return base64.standard_b64decode(encoded.encode("ascii"))


def _solid_offsets_from_mask(mask: CollisionMask) -> tuple[tuple[int, int], ...]:
    offsets: list[tuple[int, int]] = []
    width = mask.width
    for local_y in range(mask.height):
        for local_x in range(width):
            bit_index = local_y * width + local_x
            if mask.bits[bit_index >> 3] & (1 << (bit_index & 7)):
                offsets.append((local_x, local_y))
    return tuple(offsets)


@lru_cache(maxsize=512)
def _solid_offsets_cached(width: int, height: int, bits: bytes) -> tuple[tuple[int, int], ...]:
    return _solid_offsets_from_mask(CollisionMask(width=width, height=height, bits=bits))


def load_collision_catalog(manifest_path: Path | None = None) -> CollisionCatalog:
    path = manifest_path or DEFAULT_COLLISION_MANIFEST
    if not path.is_file():
        raise FileNotFoundError(
            f"Collision-Manifest fehlt: {path}. Ausführen: python tools/bake_collision.py"
        )

    data = json.loads(path.read_text(encoding="utf-8"))
    character_key = str(data.get("character_key", ""))
    character_masks: dict[int, CollisionMask] = {}
    decoration_by_key: dict[str, CollisionMask] = {}

    for entry in data.get("masks", []):
        mask = CollisionMask(
            width=int(entry["width"]),
            height=int(entry["height"]),
            bits=_decode_bits(str(entry["bits"])),
        )
        kind = str(entry.get("kind", ""))
        if kind == "character":
            direction = int(entry["direction"])
            character_masks[direction] = mask
        elif kind == "decoration":
            decoration_by_key[str(entry["key"])] = mask

    if len(character_masks) < 8:
        raise ValueError(f"Collision-Manifest: erwartet 8 Charakter-Richtungen, erhalten {len(character_masks)}.")

    character_by_direction = tuple(character_masks[index] for index in range(8))
    return CollisionCatalog(
        character_key=character_key,
        character_by_direction=character_by_direction,
        decoration_by_key=decoration_by_key,
    )
