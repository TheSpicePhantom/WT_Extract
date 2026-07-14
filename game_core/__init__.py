"""Spielwelt, Simulation und Gameplay — keine Vulkan-Abhängigkeiten."""

from game_core.character import Character
from game_core.world import (
    CHUNK_SIZE_PX,
    CHUNK_SIZE_TILES,
    Chunk,
    World,
    chunk_local_to_world_tile,
    world_tile_to_chunk_local,
)
from game_core.world_gen import generate_demo_world

__all__ = [
    "CHUNK_SIZE_PX",
    "CHUNK_SIZE_TILES",
    "Character",
    "Chunk",
    "World",
    "chunk_local_to_world_tile",
    "generate_demo_world",
    "world_tile_to_chunk_local",
]
