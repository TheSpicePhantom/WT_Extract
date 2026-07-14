"""Stabile Tile-IDs via FNV-1a — content-addressable, modding-sicher (M22c)."""

from __future__ import annotations

from collections.abc import Iterable

from render_scene.sprite_keys import normalize_key_part

EMPTY_TILE_ID = 0
_FNV_OFFSET = 2166136261
_FNV_PRIME = 16777619


def normalize_tile_key(key: str) -> str:
    """Kanonische Tile-Key-Form — gleiche Regeln wie Sprite-Keys."""
    if not key:
        return ""
    return normalize_key_part(key)


def stable_tile_id(key: str) -> int:
    """FNV-1a 32-bit — deterministisch in Main-Thread und Worker-Prozessen."""
    if not key:
        return EMPTY_TILE_ID
    normalized = normalize_tile_key(key)
    hash_value = _FNV_OFFSET
    for byte in normalized.encode("utf-8"):
        hash_value ^= byte
        hash_value = (hash_value * _FNV_PRIME) & 0xFFFFFFFF
    return hash_value


def build_tile_key_by_id(keys: Iterable[str]) -> dict[int, str]:
    """Reverse-Map für bekannte Keys — wirft bei Hash-Kollisionen."""
    key_by_id: dict[int, str] = {}
    for key in keys:
        canonical = str(key)
        tile_id = stable_tile_id(canonical)
        if tile_id == EMPTY_TILE_ID and canonical:
            raise ValueError(
                f"Tile-Key {canonical!r} erzeugt EMPTY_TILE_ID ({EMPTY_TILE_ID})"
            )
        existing = key_by_id.get(tile_id)
        if existing is not None and existing != canonical:
            raise ValueError(
                f"Tile-ID-Kollision {tile_id}: {existing!r} und {canonical!r}"
            )
        key_by_id[tile_id] = canonical
    return key_by_id
