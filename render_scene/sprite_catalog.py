"""Sprite-Katalog — stabile Auflösung von SpriteKey → SpriteId (Manifest-basiert)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from render_scene.handles import SpriteId, SpriteKey
from render_scene.sprite_keys import DEFAULT_SPRITE_NAMESPACE, make_sprite_key, normalize_key_part


@dataclass(frozen=True, slots=True)
class SpriteCatalog:
    """Lookup-Tabelle — Gameplay/Bridge nutzt Keys, GPU behält SpriteId."""

    key_to_id: dict[str, int]

    def resolve(self, key: str | SpriteKey) -> SpriteId:
        normalized = normalize_key_part(str(key))
        if normalized not in self.key_to_id:
            raise KeyError(f"Sprite-Key nicht im Katalog: {key}")
        return SpriteId(self.key_to_id[normalized])

    def try_resolve(self, key: str | SpriteKey) -> SpriteId | None:
        normalized = normalize_key_part(str(key))
        sprite_id = self.key_to_id.get(normalized)
        return None if sprite_id is None else SpriteId(sprite_id)

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self.key_to_id))


def catalog_from_manifest_data(manifest: dict) -> SpriteCatalog:
    mapping: dict[str, int] = {}
    for entry in manifest.get("entries", []):
        key = entry.get("key")
        if key is None:
            name = str(entry.get("name", ""))
            key = make_sprite_key(name, DEFAULT_SPRITE_NAMESPACE)
        normalized = normalize_key_part(str(key))
        mapping[normalized] = int(entry["sprite_id"])
    return SpriteCatalog(key_to_id=mapping)


def catalog_from_manifest_path(manifest_path: Path) -> SpriteCatalog:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return catalog_from_manifest_data(manifest)
