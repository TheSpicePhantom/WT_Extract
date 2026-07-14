"""Tests — Sprite-Tiefensortierung (M13)."""

from __future__ import annotations

from render_graphics.sprite_sort import effective_sort_y, sort_sprites_for_depth, sprite_depth_key
from render_scene.handles import LayerId, MaterialHandle
from render_scene.types import SpriteInstanceData


def _sprite(
    world_y: float,
    layer: int,
    *,
    world_x: float = 0.0,
    sort_y: float | None = None,
) -> SpriteInstanceData:
    return SpriteInstanceData(
        world_x=world_x,
        world_y=world_y,
        sprite_id=1,
        material=MaterialHandle(1),
        layer=LayerId(layer),
        sort_y=sort_y,
    )


def test_character_south_of_tree_draws_on_top_of_trunk() -> None:
    trunk = _sprite(320.0, 5)
    character = _sprite(288.0, 2)
    ordered = sort_sprites_for_depth((trunk, character))
    assert ordered.index(character) > ordered.index(trunk)


def test_character_north_of_tree_draws_behind_trunk() -> None:
    trunk = _sprite(320.0, 5)
    character = _sprite(352.0, 2)
    ordered = sort_sprites_for_depth((trunk, character))
    assert ordered.index(trunk) > ordered.index(character)


def test_same_foot_tree_layer_wins_over_character() -> None:
    trunk = _sprite(320.0, 5)
    character = _sprite(320.0, 2)
    ordered = sort_sprites_for_depth((character, trunk))
    assert ordered.index(trunk) > ordered.index(character)


def test_canopy_sorts_after_character_south_of_tree() -> None:
    trunk = _sprite(320.0, 5, sort_y=320.0)
    character = _sprite(288.0, 2)
    canopy = _sprite(320.0, 6, sort_y=270.0)
    ordered = sort_sprites_for_depth((canopy, character, trunk))
    assert ordered.index(trunk) < ordered.index(character) < ordered.index(canopy)


def test_sort_y_offset_overrides_world_y() -> None:
    sprite = _sprite(100.0, 4, sort_y=200.0)
    assert effective_sort_y(sprite) == 200.0
    assert sprite_depth_key(sprite)[0] == -200.0


def test_stable_sort_by_world_x_on_tie() -> None:
    left = _sprite(320.0, 5, world_x=0.0)
    right = _sprite(320.0, 5, world_x=64.0)
    ordered = sort_sprites_for_depth((right, left))
    assert ordered == (left, right)
