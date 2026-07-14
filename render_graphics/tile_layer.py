"""Tile-Layer — SoA-Batches zu GPU-Instanzdaten (TileId = SpriteId)."""

from __future__ import annotations

from render_scene.handles import LayerId, MaterialHandle
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import (
    TILE_SIZE_PX,
    SpriteInstanceData,
    TileChunkRenderData,
    TileLayerBatch,
)

from render_graphics.instancing import (
    pack_textured_sprite_instances,
    pack_textured_tile_instances,
)
from render_graphics.sprite_sort import sort_sprites_for_depth


def pack_textured_tile_layer(batch: TileLayerBatch) -> bytes:
    """Packt ein TileLayerBatch — Anker unten links, Größe aus Atlas-Lookup."""
    sprite_ids = [int(tile_id) for tile_id in batch.tile_ids]
    return pack_textured_tile_instances(batch.world_x, batch.world_y, sprite_ids)


def pack_textured_tile_chunks(chunks: tuple[TileChunkRenderData, ...]) -> bytes:
    """Alle Tile-Layer aller Chunks — sortiert nach LayerId, dann Chunk."""
    if not chunks:
        return b""

    layers: list[TileLayerBatch] = []
    for chunk in chunks:
        layers.extend(chunk.layers)
    layers.sort(key=lambda layer: int(layer.layer))

    parts = [pack_textured_tile_layer(layer) for layer in layers]
    return b"".join(parts)


def pack_textured_tiles_and_sprites(
    tile_chunks: tuple[TileChunkRenderData, ...],
    sprites: tuple[SpriteInstanceData, ...],
) -> bytes:
    """Tiles zuerst, Sprites darüber — ein Instanz-Buffer für einen Draw."""
    tile_bytes = pack_textured_tile_chunks(tile_chunks)
    sorted_sprites = sort_sprites_for_depth(sprites)
    sprite_bytes = pack_textured_sprite_instances(sorted_sprites)
    if not tile_bytes:
        return sprite_bytes
    if not sprite_bytes:
        return tile_bytes
    return tile_bytes + sprite_bytes


def build_tile_layer_from_keys(
    catalog: SpriteCatalog,
    tile_keys: tuple[str, ...],
    world_x: tuple[float, ...],
    world_y: tuple[float, ...],
    layer: LayerId = LayerId(0),
    material: MaterialHandle = MaterialHandle(1),
) -> TileLayerBatch:
    """Baut TileLayerBatch aus wt:…-Keys — TileId = aufgelöste SpriteId."""
    if not (len(tile_keys) == len(world_x) == len(world_y)):
        raise ValueError("tile_keys, world_x und world_y müssen gleiche Länge haben.")

    tile_ids = tuple(catalog.resolve(key) for key in tile_keys)
    materials = tuple(material for _ in tile_keys)
    return TileLayerBatch(
        layer=layer,
        tile_ids=tile_ids,
        world_x=world_x,
        world_y=world_y,
        materials=materials,
    )


def demo_tile_chunk_checkerboard(
    catalog: SpriteCatalog,
    cols: int = 48,
    rows: int = 32,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    chunk_coord: tuple[int, int] = (0, 0),
) -> TileChunkRenderData:
    """Test-Chunk: Schachbrett aus wt:tiles/grass und wt:tiles/dirt."""
    keys: list[str] = []
    xs: list[float] = []
    ys: list[float] = []
    step = float(TILE_SIZE_PX)

    for row in range(rows):
        for col in range(cols):
            key = "wt:tiles/grass" if (row + col) % 2 == 0 else "wt:tiles/dirt"
            keys.append(key)
            xs.append(origin_x + col * step)
            ys.append(origin_y + row * step)

    layer = build_tile_layer_from_keys(
        catalog,
        tile_keys=tuple(keys),
        world_x=tuple(xs),
        world_y=tuple(ys),
        layer=LayerId(0),
    )
    return TileChunkRenderData(chunk_coord=chunk_coord, layers=(layer,))


def demo_tile_chunk_with_pond(
    catalog: SpriteCatalog,
    cols: int = 48,
    rows: int = 32,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    chunk_coord: tuple[int, int] = (0, 0),
) -> TileChunkRenderData:
    """Test-Chunk: Gras/Dirt mit Wasser-Fleck in der Mitte."""
    keys: list[str] = []
    xs: list[float] = []
    ys: list[float] = []
    step = float(TILE_SIZE_PX)
    pond_cx = cols // 2
    pond_cy = rows // 2

    for row in range(rows):
        for col in range(cols):
            dx = abs(col - pond_cx)
            dy = abs(row - pond_cy)
            if dx <= 4 and dy <= 3:
                key = "wt:tiles/water"
            elif (row + col) % 2 == 0:
                key = "wt:tiles/grass"
            else:
                key = "wt:tiles/dirt"
            keys.append(key)
            xs.append(origin_x + col * step)
            ys.append(origin_y + row * step)

    layer = build_tile_layer_from_keys(
        catalog,
        tile_keys=tuple(keys),
        world_x=tuple(xs),
        world_y=tuple(ys),
        layer=LayerId(0),
    )
    return TileChunkRenderData(chunk_coord=chunk_coord, layers=(layer,))
