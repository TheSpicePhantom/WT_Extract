"""Datenorientierte Render-Frame-Typen für die Übergabe an den Renderer."""

from __future__ import annotations

from dataclasses import dataclass, field

from render_scene.handles import (
    ChunkCoord,
    LayerId,
    MaterialHandle,
    SpriteId,
    TextureHandle,
    TileId,
)

TILE_SIZE_PX = 32
ATLAS_CELL_PX = 32
ATLAS_GUTTER_PX = 1


@dataclass(frozen=True, slots=True)
class SpriteRect:
    """UV-Rechteck + Pixelgröße eines Sprites im Atlas."""

    u0: float
    v0: float
    u1: float
    v1: float
    pixel_w: int
    pixel_h: int
    sheet_cols: int = 1
    sheet_rows: int = 1


@dataclass(frozen=True, slots=True)
class MaterialDescriptor:
    """Material → Atlas-Textur (M6: ein Material pro Atlas)."""

    handle: MaterialHandle
    texture: TextureHandle


@dataclass(frozen=True, slots=True)
class AtlasManifestEntry:
    """Eintrag im Atlas-Manifest — Position auf dem 32px-Zellenraster."""

    sprite_id: int
    key: str
    name: str
    cells_w: int
    cells_h: int
    cell_x: int
    cell_y: int


@dataclass(frozen=True, slots=True)
class CameraData:
    """Orthographische 2D/2.5D-Kamera — reine View-Daten, keine Spielsemantik."""

    position_x: float
    position_y: float
    zoom: float
    viewport_width: int
    viewport_height: int


@dataclass(frozen=True, slots=True)
class SpriteInstanceData:
    """Eine instanzierbare Sprite-Draw-Anweisung.

    world_x/world_y: Anker unten links in Welt-Pixeln (1 Tile = 32×32 px).
    """

    world_x: float
    world_y: float
    sprite_id: SpriteId
    material: MaterialHandle
    layer: LayerId
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    tint_r: float = 1.0
    tint_g: float = 1.0
    tint_b: float = 1.0
    tint_a: float = 1.0
    sheet_frame_col: int = 0
    sheet_frame_row: int = 0
    sort_y: float | None = None
    clip_v0: float = 0.0
    clip_v1: float = 1.0


@dataclass(frozen=True, slots=True)
class TileLayerBatch:
    """Kompakte Tile-Instanzen eines Layers — SoA, TileId = SpriteId (wt:… im Atlas)."""

    layer: LayerId
    tile_ids: tuple[TileId, ...]
    world_x: tuple[float, ...]
    world_y: tuple[float, ...]
    materials: tuple[MaterialHandle, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class TileChunkRenderData:
    """Sichtbarer Chunk mit layerweise gebündelten Tiles.

    chunk_coord: Chunk-Index (cx, cy) — Welt-Anker unten links bei (cx * CHUNK_SIZE_PX, cy * CHUNK_SIZE_PX) px.
    """

    chunk_coord: ChunkCoord
    layers: tuple[TileLayerBatch, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class RenderFrame:
    """Neutraler Frame-Input für den Renderer — einzige Einspeisung pro Draw-Zyklus."""

    camera: CameraData
    tile_chunks: tuple[TileChunkRenderData, ...] = field(default_factory=tuple)
    sprites: tuple[SpriteInstanceData, ...] = field(default_factory=tuple)
    clear_color: tuple[float, float, float, float] = (0.08, 0.09, 0.11, 1.0)
    debug_overlay_vertices: bytes | None = None


@dataclass(frozen=True, slots=True)
class TextureAtlasDescriptor:
    """Metadaten für einen Atlas — Handle verweist auf die GPU-Textur."""

    handle: TextureHandle
    width: int
    height: int
    tile_size_px: int = TILE_SIZE_PX
    entries: tuple[AtlasManifestEntry, ...] = field(default_factory=tuple)
