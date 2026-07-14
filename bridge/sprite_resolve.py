"""Bridge-Helfer — SpriteKey → SpriteId für RenderFrame (ohne render_graphics)."""

from __future__ import annotations

from render_scene.handles import SpriteId, SpriteKey
from render_scene.sprite_catalog import SpriteCatalog


def resolve_sprite(catalog: SpriteCatalog, key: str | SpriteKey) -> SpriteId:
    """Löst einen Minecraft-Style-Key in eine GPU-SpriteId auf."""
    return catalog.resolve(key)
