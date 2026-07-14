"""Tests — Decoration-Extraktion (Bridge)."""

from __future__ import annotations

from bridge.decoration_extractor import decorations_to_sprites
from game_core.content_registry import load_content_registry
from game_core.world import CHUNK_SIZE_PX, World
from game_core.world_gen import generate_chunk, populate_chunk_decorations
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import CameraData


def _catalog(content) -> SpriteCatalog:
    mapping = {deco.sprite_key: index for index, deco in enumerate(content.decorations)}
    return SpriteCatalog(key_to_id=mapping)


def test_decorations_to_sprites_camera_culling() -> None:
    content = load_content_registry()
    if not content.decorations:
        return

    world = World()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.chunks[(10, 0)] = generate_chunk(10, 0)
    populate_chunk_decorations(world, content, 0, 0)
    populate_chunk_decorations(world, content, 10, 0)

    all_sprites = decorations_to_sprites(content, _catalog(content), world)
    camera = CameraData(
        position_x=CHUNK_SIZE_PX * 0.5,
        position_y=CHUNK_SIZE_PX * 0.5,
        zoom=0.35,
        viewport_width=1280,
        viewport_height=720,
    )
    visible_sprites = decorations_to_sprites(
        content, _catalog(content), world, camera=camera
    )

    assert len(visible_sprites) > 0
    assert len(visible_sprites) < len(all_sprites)
