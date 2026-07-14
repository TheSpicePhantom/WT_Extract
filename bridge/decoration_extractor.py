"""Bridge — platzierte Decorations → SpriteInstanceData."""

from __future__ import annotations

import sys

from bridge.visibility import visible_chunk_coords
from game_core.content_registry import ContentRegistry
from game_core.perf.models import ExtractStepMetrics
from game_core.world import TILE_SIZE_PX, World, world_tile_to_chunk_local
from render_scene.handles import LayerId, MaterialHandle
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import CameraData, SpriteInstanceData


def _append_sprite(
    sprites: list[SpriteInstanceData],
    *,
    world_x: float,
    world_y: float,
    sprite_id: int,
    layer: int,
    sort_y: float,
    clip_v0: float,
    clip_v1: float,
) -> None:
    sprites.append(
        SpriteInstanceData(
            world_x=world_x,
            world_y=world_y,
            sprite_id=sprite_id,
            material=MaterialHandle(1),
            layer=LayerId(layer),
            sort_y=sort_y,
            clip_v0=clip_v0,
            clip_v1=clip_v1,
        )
    )


def _placed_in_visible_chunks(
    placed,
    visible: set[tuple[int, int]],
) -> bool:
    wx = int(placed.world_x) // TILE_SIZE_PX
    wy = int(placed.world_y) // TILE_SIZE_PX
    chunk_coord, _, _ = world_tile_to_chunk_local(wx, wy)
    return chunk_coord in visible


def decorations_to_sprites(
    content: ContentRegistry,
    catalog: SpriteCatalog,
    world: World,
    *,
    camera: CameraData | None = None,
    padding_chunks: int = 1,
    step_metrics: ExtractStepMetrics | None = None,
) -> tuple[SpriteInstanceData, ...]:
    """Mappt World.decorations auf generische Sprite-Instanzen."""
    if step_metrics is not None:
        step_metrics.deco_scanned_count = len(world.decorations)

    visible: set[tuple[int, int]] | None = None
    if camera is not None:
        visible = set(visible_chunk_coords(camera, world, padding_chunks))

    sprites: list[SpriteInstanceData] = []
    for placed in world.decorations:
        if visible is not None and not _placed_in_visible_chunks(placed, visible):
            continue
        definition = content.decoration_by_id(placed.decoration_id)
        if definition is None:
            print(
                f"Unbekannte decoration_id: {placed.decoration_id}",
                file=sys.stderr,
            )
            continue
        try:
            sprite_id = catalog.resolve(definition.sprite_key)
        except KeyError:
            print(
                f"Sprite-Key nicht im Katalog: {definition.sprite_key}",
                file=sys.stderr,
            )
            continue

        sort_y = placed.world_y + definition.sort_y_offset
        split_tree = (
            definition.canopy_layer is not None and definition.trunk_clip_v1 < 1.0
        )
        if split_tree:
            _append_sprite(
                sprites,
                world_x=placed.world_x,
                world_y=placed.world_y,
                sprite_id=sprite_id,
                layer=definition.render_layer,
                sort_y=sort_y,
                clip_v0=0.0,
                clip_v1=definition.trunk_clip_v1,
            )
            _append_sprite(
                sprites,
                world_x=placed.world_x,
                world_y=placed.world_y,
                sprite_id=sprite_id,
                layer=definition.canopy_layer,
                sort_y=placed.world_y + definition.canopy_sort_y_offset,
                clip_v0=definition.canopy_clip_v0,
                clip_v1=1.0,
            )
        else:
            _append_sprite(
                sprites,
                world_x=placed.world_x,
                world_y=placed.world_y,
                sprite_id=sprite_id,
                layer=definition.render_layer,
                sort_y=sort_y,
                clip_v0=0.0,
                clip_v1=1.0,
            )
    if step_metrics is not None:
        step_metrics.deco_visible_count = len(sprites)
    return tuple(sprites)
