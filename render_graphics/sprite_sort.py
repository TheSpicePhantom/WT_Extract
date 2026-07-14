"""Sprite-Tiefensortierung — Y-up, Fußpunkt, Layer-Tie-Break."""

from __future__ import annotations

from render_scene.types import SpriteInstanceData


def effective_sort_y(sprite: SpriteInstanceData) -> float:
    """Sortier-Y — explizit gesetzt oder Anker unten links."""
    if sprite.sort_y is not None:
        return sprite.sort_y
    return sprite.world_y


def sprite_depth_key(sprite: SpriteInstanceData) -> tuple[float, int, float]:
    """Aufsteigend sortieren: Norden zuerst, Süden zuletzt (Painter)."""
    return (-effective_sort_y(sprite), int(sprite.layer), sprite.world_x)


def sort_sprites_for_depth(
    sprites: tuple[SpriteInstanceData, ...],
) -> tuple[SpriteInstanceData, ...]:
    if len(sprites) < 2:
        return sprites
    return tuple(sorted(sprites, key=sprite_depth_key))
