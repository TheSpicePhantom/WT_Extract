"""Streaming-Welt-Persistenz — Save v4 (sparse Terrain-Deltas + Fingerprint)."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path

from game_core.character import Character
from game_core.chunk_delta import (
    OVERLAY_DELTA_SCHEMA_VERSION,
    TerrainDelta,
    compute_terrain_delta,
    compute_world_gen_fingerprint,
    terrain_delta_from_dict,
    terrain_delta_to_dict,
)
from game_core.chunk_streaming import ChunkStreamer
from game_core.decorations import PlacedDecoration
from game_core.persistenz import TileOverride
from game_core.world import CHUNK_SIZE_TILES, Chunk, World
from game_core.world_gen import (
    chunk_differs_from_baseline,
    configure_world_gen,
    generate_chunk,
    get_world_gen_config,
    load_world_gen_config,
)
from game_core.world_io import (
    _chunk_from_dict,
    _decoration_from_dict,
    _decoration_to_dict,
    _player_from_dict,
    _player_to_dict,
)

STREAMING_SAVE_VERSION = 4
LEGACY_STREAMING_SAVE_VERSION = 3
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STREAMING_SAVE_DIR = PROJECT_ROOT / "saves" / "streaming_world"


@dataclass(frozen=True, slots=True)
class StreamingSnapshot:
    """Geladener Streaming-Spielstand — Deltas, Decorations, Spieler."""

    persistent_deltas: dict[tuple[int, int], TerrainDelta]
    decorations: list[PlacedDecoration]
    player: Character
    world_seed: int | None = None
    world_gen_fingerprint: str | None = None


def _coord_filename(cx: int, cy: int) -> str:
    return f"{cx}_{cy}.json"


def _parse_coord_filename(name: str) -> tuple[int, int]:
    stem = name.removesuffix(".json")
    parts = stem.split("_", 1)
    if len(parts) != 2:
        raise ValueError(f"Ungültiger Chunk-Dateiname: {name}")
    return int(parts[0]), int(parts[1])


def _migrate_full_chunk_to_delta(chunk: Chunk) -> TerrainDelta:
    """Einmalige Migration v3 Full-Chunk → sparse TerrainDelta."""
    cx, cy = chunk.coord
    baseline = generate_chunk(cx, cy)
    tile_overrides: list[TileOverride] = []
    for layer_id in sorted(chunk.layer_keys.keys()):
        for ty in range(CHUNK_SIZE_TILES):
            for tx in range(CHUNK_SIZE_TILES):
                key = chunk.get_key(tx, ty, layer_id)
                if key != baseline.get_key(tx, ty, layer_id):
                    tile_overrides.append(TileOverride(layer_id, tx, ty, key))
    return TerrainDelta(coord=(cx, cy), tile_overrides=tuple(tile_overrides))


def save_streaming_world(
    directory: Path,
    world: World,
    player: Character,
    streamer: ChunkStreamer,
) -> None:
    """Schreibt nur Terrain-Deltas + Spieler + User-Decorations."""
    for coord, chunk in list(world.chunks.items()):
        if not world.is_persistenz_relevant(coord):
            continue
        flags = world.get_persistenz_flags(coord)
        delta = compute_terrain_delta(
            chunk,
            flags,
            tile_overrides=world.get_persistenz_tile_overrides(coord),
            suppressions=world.get_persistenz_suppressions(coord),
            existing=streamer.persistent_deltas.get(coord),
        )
        if delta is not None:
            streamer.persistent_deltas[coord] = delta

    deltas = dict(streamer.persistent_deltas)
    chunks_dir = directory / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    for path in chunks_dir.glob("*.json"):
        path.unlink()

    chunk_coords: list[list[int]] = []
    for coord in sorted(deltas.keys()):
        cx, cy = coord
        chunk_coords.append([cx, cy])
        chunk_path = chunks_dir / _coord_filename(cx, cy)
        chunk_path.write_text(
            json.dumps(terrain_delta_to_dict(deltas[coord]), indent=2),
            encoding="utf-8",
        )

    user_decorations = [
        _decoration_to_dict(placed)
        for placed in world.decorations
        if not placed.procedural
    ]

    manifest = {
        "version": STREAMING_SAVE_VERSION,
        "chunk_size_tiles": world.chunk_size_tiles,
        "world_seed": get_world_gen_config().world_seed,
        "world_gen_fingerprint": compute_world_gen_fingerprint(),
        "overlay_schema_version": OVERLAY_DELTA_SCHEMA_VERSION,
        "player": _player_to_dict(player),
        "decorations": user_decorations,
        "chunk_coords": chunk_coords,
    }
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    streamer.persistent_overrides.clear()
    world.clear_dirty()


def load_streaming_world(directory: Path) -> StreamingSnapshot:
    """Liest manifest + Chunk-Deltas (v4) oder migriert v3 Full-Chunks."""
    manifest_path = directory / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Streaming-Spielstand nicht gefunden: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = int(data.get("version", 0))
    if version not in (2, LEGACY_STREAMING_SAVE_VERSION, STREAMING_SAVE_VERSION):
        raise ValueError(f"Unsupported streaming save version: {version}")

    chunk_size = int(data.get("chunk_size_tiles", CHUNK_SIZE_TILES))
    if chunk_size != CHUNK_SIZE_TILES:
        raise ValueError(
            f"Chunk-Größe {chunk_size} passt nicht zur Engine ({CHUNK_SIZE_TILES})."
        )

    world_seed_raw = data.get("world_seed")
    world_seed = int(world_seed_raw) if world_seed_raw is not None else None
    if world_seed is not None:
        base = load_world_gen_config()
        configure_world_gen(replace(base, world_seed=world_seed))

    saved_fingerprint = data.get("world_gen_fingerprint")
    if version >= STREAMING_SAVE_VERSION:
        if not saved_fingerprint:
            raise ValueError("manifest.json missing world_gen_fingerprint")
        current = compute_world_gen_fingerprint()
        if saved_fingerprint != current:
            raise ValueError(
                f"world_gen_fingerprint mismatch: save={saved_fingerprint} current={current}"
            )

    player = _player_from_dict(data["player"])
    decorations = [_decoration_from_dict(entry) for entry in data.get("decorations", [])]

    persistent_deltas: dict[tuple[int, int], TerrainDelta] = {}
    chunks_dir = directory / "chunks"

    for coord_raw in data.get("chunk_coords", []):
        cx, cy = int(coord_raw[0]), int(coord_raw[1])
        chunk_path = chunks_dir / _coord_filename(cx, cy)
        if not chunk_path.is_file():
            raise FileNotFoundError(f"Chunk-Datei fehlt: {chunk_path}")
        chunk_data = json.loads(chunk_path.read_text(encoding="utf-8"))
        if version >= STREAMING_SAVE_VERSION and "tile_overrides" in chunk_data:
            delta = terrain_delta_from_dict(chunk_data)
            persistent_deltas[delta.coord] = delta
        else:
            chunk = _chunk_from_dict(chunk_data)
            if chunk_differs_from_baseline(chunk):
                persistent_deltas[chunk.coord] = _migrate_full_chunk_to_delta(chunk)

    return StreamingSnapshot(
        persistent_deltas=persistent_deltas,
        decorations=decorations,
        player=player,
        world_seed=world_seed,
        world_gen_fingerprint=str(saved_fingerprint) if saved_fingerprint else None,
    )
