"""GPU-Instanzdaten — kompaktes SoA-Packing für instanced Quads."""

from __future__ import annotations

import struct

from render_scene.handles import LayerId, MaterialHandle, SpriteId
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import SpriteInstanceData

# center_x, center_y, width, height, r, g, b, a  (Anker = unten links)
INSTANCE_STRIDE = 32
# anchor_x, anchor_y, tint_rgba, sprite_id, frame_pack, clip_pack
TEXTURED_INSTANCE_STRIDE = 36
UNIT_QUAD_STRIDE = 8
UNIT_QUAD_VERTEX_COUNT = 6

DEFAULT_QUAD_SIZE = 32.0


def build_unit_quad_vertices() -> bytes:
    """Einheits-Quad (0..1)² als zwei Dreiecke — binding 0, per-vertex."""
    corners = (
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    )
    flat = [coord for corner in corners for coord in corner]
    return struct.pack(f"{len(flat)}f", *flat)


def pack_sprite_instances(
    sprites: tuple[SpriteInstanceData, ...],
    default_size: float = DEFAULT_QUAD_SIZE,
) -> bytes:
    """Packt SpriteInstanceData in GPU-Instanz-Bytes (Einfarbig, Anker unten links)."""
    if not sprites:
        return b""

    floats: list[float] = []
    for sprite in sprites:
        width = default_size * sprite.scale_x
        height = default_size * sprite.scale_y
        floats.extend(
            [
                sprite.world_x,
                sprite.world_y,
                width,
                height,
                sprite.tint_r,
                sprite.tint_g,
                sprite.tint_b,
                sprite.tint_a,
            ]
        )
    return struct.pack(f"{len(floats)}f", *floats)


def _pack_frame(col: int, row: int) -> int:
    return (int(row) << 16) | (int(col) & 0xFFFF)


def _pack_clip(v0: float, v1: float) -> int:
    lo = max(0, min(int(round(v0 * 65535.0)), 65535))
    hi = max(0, min(int(round(v1 * 65535.0)), 65535))
    return (hi << 16) | lo


def _pack_textured_instance_bytes(
    world_x: float,
    world_y: float,
    sprite_id: int,
    *,
    tint_r: float = 1.0,
    tint_g: float = 1.0,
    tint_b: float = 1.0,
    tint_a: float = 1.0,
    frame_col: int = 0,
    frame_row: int = 0,
    clip_v0: float = 0.0,
    clip_v1: float = 1.0,
) -> bytes:
    clip_lo = max(0.0, min(float(clip_v0), 1.0))
    clip_hi = max(0.0, min(float(clip_v1), 1.0))
    if clip_hi < clip_lo:
        clip_lo, clip_hi = clip_hi, clip_lo
    return struct.pack(
        "<2f4fIII",
        float(world_x),
        float(world_y),
        tint_r,
        tint_g,
        tint_b,
        tint_a,
        int(sprite_id),
        _pack_frame(frame_col, frame_row),
        _pack_clip(clip_lo, clip_hi),
    )


def pack_textured_tile_instances(
    anchors_x: tuple[float, ...] | list[float],
    anchors_y: tuple[float, ...] | list[float],
    sprite_ids: tuple[int, ...] | list[int],
) -> bytes:
    """Packt Tile-Instanzen — gleiches 36-Byte-Layout wie Sprites (voller Clip)."""
    count = len(sprite_ids)
    if not (len(anchors_x) == len(anchors_y) == count):
        raise ValueError("anchors_x, anchors_y und sprite_ids müssen gleiche Länge haben.")
    return b"".join(
        _pack_textured_instance_bytes(
            float(anchors_x[index]),
            float(anchors_y[index]),
            int(sprite_ids[index]),
        )
        for index in range(count)
    )


def pack_textured_sprite_instances(
    sprites: tuple[SpriteInstanceData, ...],
) -> bytes:
    """Packt Instanzdaten für texturierte Quads — Größe kommt aus SpriteRect-Lookup."""
    if not sprites:
        return b""

    return b"".join(
        _pack_textured_instance_bytes(
            sprite.world_x,
            sprite.world_y,
            int(sprite.sprite_id),
            tint_r=sprite.tint_r,
            tint_g=sprite.tint_g,
            tint_b=sprite.tint_b,
            tint_a=sprite.tint_a,
            frame_col=sprite.sheet_frame_col,
            frame_row=sprite.sheet_frame_row,
            clip_v0=sprite.clip_v0,
            clip_v1=sprite.clip_v1,
        )
        for sprite in sprites
    )


def textured_instance_count(instance_bytes: bytes) -> int:
    return len(instance_bytes) // TEXTURED_INSTANCE_STRIDE


def pack_colored_quads(
    quads: tuple[tuple[float, float, float, float, float, float, float, float], ...],
) -> bytes:
    """Packt Roh-Quads: anchor_x, anchor_y, width, height, r, g, b, a."""
    if not quads:
        return b""
    flat = [value for quad in quads for value in quad]
    return struct.pack(f"{len(flat)}f", *flat)


def instance_count(instance_bytes: bytes) -> int:
    return len(instance_bytes) // INSTANCE_STRIDE


def demo_sprite_field(
    cols: int = 16,
    rows: int = 10,
    spacing: float = 32.0,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    sprite_keys: tuple[str, ...] | None = None,
    catalog: SpriteCatalog | None = None,
    sprite_ids: tuple[int, ...] | None = None,
) -> tuple[SpriteInstanceData, ...]:
    """Neutrales Testfeld — Anker unten links auf 32px-Grid.

    Bevorzugt sprite_keys + catalog (Minecraft-Style). sprite_ids ist Legacy-Fallback.
    """
    sprites: list[SpriteInstanceData] = []
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if sprite_keys and catalog and index < len(sprite_keys):
                sprite_id = catalog.resolve(sprite_keys[index])
            elif sprite_ids and index < len(sprite_ids):
                sprite_id = SpriteId(sprite_ids[index])
            else:
                sprite_id = SpriteId(index % max(len(catalog.key_to_id) if catalog else 9, 1))
            sprites.append(
                SpriteInstanceData(
                    world_x=origin_x + col * spacing,
                    world_y=origin_y + row * spacing,
                    sprite_id=sprite_id,
                    material=MaterialHandle(1),
                    layer=LayerId(0),
                    scale_x=1.0,
                    scale_y=1.0,
                    tint_r=1.0,
                    tint_g=1.0,
                    tint_b=1.0,
                    tint_a=1.0,
                )
            )
    return tuple(sprites)
