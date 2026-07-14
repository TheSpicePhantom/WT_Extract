"""Welt-Persistenz — JSON Save/Load für Chunks, Decorations und Spieler."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from game_core.character import AnimClip, Character
from game_core.decorations import PlacedDecoration
from game_core.world import (
    CHUNK_SIZE_TILES,
    CHUNK_TILE_COUNT,
    Chunk,
    World,
)

WORLD_SAVE_VERSION = 1
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORLD_SAVE_PATH = PROJECT_ROOT / "saves" / "chunk_world.json"


@dataclass(frozen=True, slots=True)
class WorldSnapshot:
    """Geladener Spielstand — World + Charakter."""

    world: World
    player: Character


def _chunk_to_dict(chunk: Chunk) -> dict:
    layers: dict[str, list[str]] = {}
    for layer_id in sorted(chunk.layer_keys):
        layers[str(layer_id)] = list(chunk.layer_keys[layer_id])
    cx, cy = chunk.coord
    return {"coord": [cx, cy], "layers": layers}


def _chunk_from_dict(data: dict) -> Chunk:
    coord_raw = data["coord"]
    coord = (int(coord_raw[0]), int(coord_raw[1]))
    layer_keys: dict[int, list[str]] = {}
    for layer_str, keys in data["layers"].items():
        layer_id = int(layer_str)
        key_list = list(keys)
        if len(key_list) != CHUNK_TILE_COUNT:
            raise ValueError(
                f"Chunk {coord} Layer {layer_id}: erwartet {CHUNK_TILE_COUNT} keys, "
                f"erhalten {len(key_list)}."
            )
        layer_keys[layer_id] = key_list
    return Chunk(coord=coord, layer_keys=layer_keys, solid_grid=None)


def _decoration_to_dict(placed: PlacedDecoration) -> dict:
    return {
        "world_x": placed.world_x,
        "world_y": placed.world_y,
        "decoration_id": placed.decoration_id,
    }


def _decoration_from_dict(data: dict) -> PlacedDecoration:
    return PlacedDecoration(
        world_x=float(data["world_x"]),
        world_y=float(data["world_y"]),
        decoration_id=str(data["decoration_id"]),
    )


def _player_to_dict(player: Character) -> dict:
    return {
        "world_x": player.world_x,
        "world_y": player.world_y,
        "direction": player.direction,
        "clip": player.clip.value,
        "anim_time": player.anim_time,
    }


def _player_from_dict(data: dict) -> Character:
    clip = AnimClip(str(data.get("clip", AnimClip.IDLE.value)))
    return Character(
        world_x=float(data["world_x"]),
        world_y=float(data["world_y"]),
        direction=int(data.get("direction", 3)),
        clip=clip,
        anim_time=float(data.get("anim_time", 0.0)),
    )


def world_to_dict(world: World, player: Character) -> dict:
    """Serialisiert World + Charakter für JSON."""
    chunks = [_chunk_to_dict(chunk) for chunk in sorted(world.chunks.values(), key=lambda c: c.coord)]
    decorations = [_decoration_to_dict(placed) for placed in world.decorations]
    return {
        "version": WORLD_SAVE_VERSION,
        "chunk_size_tiles": world.chunk_size_tiles,
        "chunks": chunks,
        "decorations": decorations,
        "player": _player_to_dict(player),
    }


def world_from_dict(data: dict) -> WorldSnapshot:
    """Deserialisiert JSON → WorldSnapshot."""
    version = int(data.get("version", 0))
    if version != WORLD_SAVE_VERSION:
        raise ValueError(f"Unsupported world save version: {version}")

    chunk_size = int(data.get("chunk_size_tiles", CHUNK_SIZE_TILES))
    if chunk_size != CHUNK_SIZE_TILES:
        raise ValueError(
            f"Chunk-Größe {chunk_size} passt nicht zur Engine ({CHUNK_SIZE_TILES})."
        )

    chunks: dict[tuple[int, int], Chunk] = {}
    for chunk_data in data.get("chunks", []):
        chunk = _chunk_from_dict(chunk_data)
        chunks[chunk.coord] = chunk

    decorations = [_decoration_from_dict(entry) for entry in data.get("decorations", [])]
    player = _player_from_dict(data["player"])

    world = World(
        chunks=chunks,
        decorations=decorations,
        chunk_size_tiles=chunk_size,
    )
    return WorldSnapshot(world=world, player=player)


def save_world(path: Path, world: World, player: Character) -> None:
    """Schreibt Spielstand als JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = world_to_dict(world, player)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_world(path: Path) -> WorldSnapshot:
    """Liest Spielstand aus JSON."""
    if not path.is_file():
        raise FileNotFoundError(f"Spielstand nicht gefunden: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return world_from_dict(data)
