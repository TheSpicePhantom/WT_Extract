"""Typisierte Handles für GPU-Ressourcen und Render-IDs."""

from typing import NewType, TypeAlias

TextureHandle = NewType("TextureHandle", int)
MaterialHandle = NewType("MaterialHandle", int)
SpriteId = NewType("SpriteId", int)
TileId: TypeAlias = SpriteId  # Tiles = 1×1 Atlas-Einträge, gleicher GPU-Index
SpriteKey = NewType("SpriteKey", str)
LayerId = NewType("LayerId", int)

# Chunk-Koordinate in Welt-Chunks (nicht Pixel/Tiles).
ChunkCoord: TypeAlias = tuple[int, int]

INVALID_TEXTURE: TextureHandle = TextureHandle(0)
INVALID_MATERIAL: MaterialHandle = MaterialHandle(0)
