"""Bridge — Character → SpriteInstanceData (Spritesheet-Frames)."""

from __future__ import annotations

from game_core.character import CHARACTER_LAYER, Character
from render_scene.handles import LayerId, MaterialHandle
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import SpriteInstanceData


def character_to_sprite(catalog: SpriteCatalog, character: Character) -> SpriteInstanceData:
    """Mappt Character-Zustand auf eine animierte Sprite-Instanz."""
    return SpriteInstanceData(
        world_x=character.world_x,
        world_y=character.world_y,
        sprite_id=catalog.resolve(character.sprite_key),
        material=MaterialHandle(1),
        layer=LayerId(CHARACTER_LAYER),
        sheet_frame_col=character.current_frame,
        sheet_frame_row=character.direction,
    )
