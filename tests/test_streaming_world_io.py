"""Tests — Streaming-Welt Save/Load v4 (M23a)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from game_core.character import Character
from game_core.chunk_delta import apply_terrain_delta, compute_world_gen_fingerprint
from game_core.chunk_streaming import ChunkStreamer
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, World
from game_core.world_gen import KEY_GRASS, KEY_STONE, generate_chunk
from game_core.streaming_world_io import (
    STREAMING_SAVE_VERSION,
    load_streaming_world,
    save_streaming_world,
)

_RADIUS_STREAMER = StreamingConfig(mode="radius", max_applies_per_frame=0)


def _radius_streamer() -> ChunkStreamer:
    return ChunkStreamer(config=_RADIUS_STREAMER)


def _setup_world_with_dirty_chunk() -> tuple[World, Character, ChunkStreamer]:
    world = World()
    streamer = ChunkStreamer()
    world.chunks[(1, 2)] = generate_chunk(1, 2)
    world.set_tile(10, 18, KEY_STONE)
    player = Character(world_x=float(CHUNK_SIZE_PX), world_y=float(CHUNK_SIZE_PX))
    world.place_decoration(10, 18, "trees/apple/summer/apple_1")
    return world, player, streamer


def test_streaming_save_only_dirty_deltas(tmp_path: Path) -> None:
    world, player, streamer = _setup_world_with_dirty_chunk()
    save_dir = tmp_path / "stream_save"
    save_streaming_world(save_dir, world, player, streamer)

    manifest = json.loads((save_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == STREAMING_SAVE_VERSION
    assert manifest["world_gen_fingerprint"] == compute_world_gen_fingerprint()
    assert manifest["overlay_schema_version"] == 0
    assert (save_dir / "chunks" / "1_2.json").is_file()
    assert not (save_dir / "chunks" / "0_0.json").exists()
    chunk_data = json.loads((save_dir / "chunks" / "1_2.json").read_text(encoding="utf-8"))
    assert "tile_overrides" in chunk_data


def test_streaming_roundtrip(tmp_path: Path) -> None:
    world, player, streamer = _setup_world_with_dirty_chunk()
    save_dir = tmp_path / "stream_save"
    save_streaming_world(save_dir, world, player, streamer)

    snapshot = load_streaming_world(save_dir)
    assert snapshot.player.world_x == float(CHUNK_SIZE_PX)
    assert (1, 2) in snapshot.persistent_deltas
    baseline = generate_chunk(1, 2)
    restored = apply_terrain_delta(baseline, snapshot.persistent_deltas[(1, 2)])
    assert restored.get_key(2, 2) == KEY_STONE
    assert len(snapshot.decorations) == 1
    assert snapshot.decorations[0].procedural is False
    assert snapshot.world_seed == 12345


def test_streaming_world_seed_in_manifest(tmp_path: Path) -> None:
    world, player, streamer = _setup_world_with_dirty_chunk()
    save_dir = tmp_path / "seed_save"
    save_streaming_world(save_dir, world, player, streamer)
    manifest = json.loads((save_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["world_seed"] == 12345


def test_streaming_negative_coord_filename(tmp_path: Path) -> None:
    world = World()
    streamer = ChunkStreamer()
    world.chunks[(-1, 0)] = generate_chunk(-1, 0)
    world.set_tile(-8, 0, KEY_STONE)
    player = Character(world_x=0.0, world_y=0.0)

    save_dir = tmp_path / "neg"
    save_streaming_world(save_dir, world, player, streamer)
    snapshot = load_streaming_world(save_dir)

    assert (-1, 0) in snapshot.persistent_deltas
    baseline = generate_chunk(-1, 0)
    restored = apply_terrain_delta(baseline, snapshot.persistent_deltas[(-1, 0)])
    assert restored.get_key(0, 0) == KEY_STONE


def test_save_survives_unload_after_clear_dirty(tmp_path: Path) -> None:
    from game_core.collision_catalog import load_collision_catalog
    from game_core.content_registry import load_content_registry
    from game_core.world import CHUNK_SIZE_PX

    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    streamer = _radius_streamer()

    class _Extractor:
        def invalidate(self, _coord: tuple[int, int]) -> None:
            pass

    extractor = _Extractor()
    spawn = float(CHUNK_SIZE_PX)
    streamer.update(world, spawn, spawn, content, collision, extractor)

    for wx in range(10, 15):
        for wy in range(10, 15):
            world.set_tile(wx, wy, KEY_STONE)

    player = Character(world_x=spawn, world_y=spawn)
    save_dir = tmp_path / "after_save_unload"
    save_streaming_world(save_dir, world, player, streamer)
    assert len(streamer.persistent_deltas) > 0

    far = 40 * CHUNK_SIZE_PX
    streamer.update(world, far, far, content, collision, extractor)

    snapshot = load_streaming_world(save_dir)
    world2 = World()
    streamer2 = _radius_streamer()
    streamer2.load_persistent_deltas(snapshot.persistent_deltas)
    streamer2.update(world2, spawn, spawn, content, collision, extractor)

    assert world2.get_tile(12, 12) == KEY_STONE


def test_procedural_decorations_not_saved(tmp_path: Path) -> None:
    world = World()
    streamer = ChunkStreamer()
    world.chunks[(0, 0)] = generate_chunk(0, 0)
    world.place_decoration(1, 1, "trees/apple/summer/apple_1", procedural=True)
    player = Character(world_x=32.0, world_y=32.0)

    save_dir = tmp_path / "proc"
    save_streaming_world(save_dir, world, player, streamer)
    snapshot = load_streaming_world(save_dir)

    assert snapshot.decorations == []
    assert snapshot.persistent_deltas == {}


def test_fingerprint_mismatch_rejected(tmp_path: Path) -> None:
    world, player, streamer = _setup_world_with_dirty_chunk()
    save_dir = tmp_path / "fp"
    save_streaming_world(save_dir, world, player, streamer)
    manifest_path = save_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["world_gen_fingerprint"] = "invalid"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="world_gen_fingerprint mismatch"):
        load_streaming_world(save_dir)


def test_load_after_active_chunk_gen_pool(tmp_path: Path) -> None:
    """STRG+L: configure_world_gen darf keinen stale Executor hinterlassen."""
    from dataclasses import replace
    from unittest.mock import MagicMock

    from game_core.collision_catalog import load_collision_catalog
    from game_core.content_registry import load_content_registry
    from game_core.world_gen import configure_world_gen, get_world_gen_config

    configure_world_gen(
        replace(get_world_gen_config(), parallel_prefetch=True, parallel_workers=2)
    )
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    streamer = ChunkStreamer()
    extractor = MagicMock()

    try:
        streamer.update(world, float(CHUNK_SIZE_PX), float(CHUNK_SIZE_PX), content, collision, extractor)
        assert streamer.chunk_gen_pool is not None

        player = Character(world_x=320.0, world_y=320.0)
        save_dir = tmp_path / "pool_reload"
        save_streaming_world(save_dir, world, player, streamer)

        load_streaming_world(save_dir)
        streamer.shutdown_chunk_gen_pool()
        streamer.update(world, 320.0, 320.0, content, collision, extractor)
    finally:
        streamer.shutdown_chunk_gen_pool()

