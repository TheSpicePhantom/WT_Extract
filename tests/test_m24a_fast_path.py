"""Tests — M24a Worker-Complete-Fast-Path Predicates und Streaming."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock, patch

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.streaming_config import StreamingConfig
from game_core.world import World
from game_core.world_gen import generate_chunk, get_world_gen_config
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_result import (
    ChunkGenResult,
    apply_worker_complete_result,
)
from game_core.worker_fast_path import (
    can_apply_worker_complete_fast_path,
    is_worker_complete_result,
)
from game_core.world import CHUNK_TILE_COUNT


def _worker_ctx() -> WorldGenContext:
    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    return WorldGenContext.from_configs(config)


def _complete_result(coord: tuple[int, int] = (0, 0)) -> ChunkGenResult:
    ctx = _worker_ctx()
    return ctx.generate_chunk_result(coord[0], coord[1])


def test_is_worker_complete_result_positive() -> None:
    result = _complete_result()
    assert is_worker_complete_result(
        result,
        worker_apply_enabled=True,
        debug_mode=None,
    )


def test_is_worker_complete_result_rejects_terrain_only() -> None:
    terrain = ChunkGenResult(
        coord=(0, 0),
        layer0=tuple(0 for _ in range(CHUNK_TILE_COUNT)),
        layer1=tuple(0 for _ in range(CHUNK_TILE_COUNT)),
        decorations=None,
        solid_grid=None,
    )
    assert not is_worker_complete_result(
        result=terrain, worker_apply_enabled=True, debug_mode=None
    )


def test_can_apply_fast_path_rejects_dirty_chunk() -> None:
    world = World()
    world.mark_dirty((0, 0))
    streamer = ChunkStreamer(config=StreamingConfig(mode="radius"))
    result = _complete_result()
    assert not can_apply_worker_complete_fast_path(
        world,
        streamer,
        result,
        worker_apply_enabled=True,
        debug_mode=None,
    )


def test_can_apply_fast_path_rejects_override() -> None:
    world = World()
    streamer = ChunkStreamer(config=StreamingConfig(mode="radius"))
    streamer.persistent_overrides[(0, 0)] = generate_chunk(0, 0)
    result = _complete_result()
    assert not can_apply_worker_complete_fast_path(
        world,
        streamer,
        result,
        worker_apply_enabled=True,
        debug_mode=None,
    )


def test_can_apply_fast_path_rejects_user_deco() -> None:
    content = load_content_registry()
    if not content.decorations:
        return
    world = World()
    deco_id = content.decorations[0].id
    world.place_decoration(1, 1, deco_id, procedural=False)
    streamer = ChunkStreamer(config=StreamingConfig(mode="radius"))
    result = _complete_result()
    assert not can_apply_worker_complete_fast_path(
        world,
        streamer,
        result,
        worker_apply_enabled=True,
        debug_mode=None,
    )


def test_streaming_worker_apply_skips_collision_flush() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    config = StreamingConfig(mode="radius", max_applies_per_frame=0)
    streamer = ChunkStreamer(config=config)
    extractor = MagicMock()
    ready = _complete_result()

    rebuild_calls = 0
    original = world.rebuild_chunk_solid

    def counting_rebuild(coord, content_arg, collision_arg):
        nonlocal rebuild_calls
        rebuild_calls += 1
        return original(coord, content_arg, collision_arg)

    world.rebuild_chunk_solid = counting_rebuild  # type: ignore[method-assign]

    gen_config = replace(get_world_gen_config(), parallel_worker_apply=True, parallel_prefetch=True)
    with patch("game_core.chunk_streaming.get_world_gen_config", return_value=gen_config):
        with patch.object(streamer, "ensure_chunk_gen_pool") as pool_factory:
            pool = MagicMock()
            pool.poll_ready.return_value = [ready]
            pool.in_flight_count.return_value = 0
            pool.is_in_flight.return_value = False
            pool.in_flight_age_ms.return_value = 0.0
            pool_factory.return_value = pool
            stream_sets = MagicMock()
            stream_sets.wanted = {(0, 0)}
            stream_sets.keep = {(0, 0)}
            stream_sets.prefetch = set()
            with patch.object(streamer, "_resolve_stream_sets", return_value=stream_sets):
                with patch.object(streamer, "_should_use_worker_apply", return_value=True):
                    streamer.update(world, 0.0, 0.0, content, collision, extractor)

    assert (0, 0) in world.chunks
    assert rebuild_calls == 0
    assert world.chunks[(0, 0)].solid_grid is not None


def test_apply_worker_complete_matches_reference_deco_count() -> None:
    content = load_content_registry()
    ctx = _worker_ctx()
    coord = (0, 0)
    result = ctx.generate_chunk_result(coord[0], coord[1])
    world = World()
    apply_worker_complete_result(world, result, content)
    ref = ctx.generate_chunk_result(coord[0], coord[1])
    assert is_worker_complete_result(ref, worker_apply_enabled=True, debug_mode=None)
    assert len(world.decorations) == len(ref.decorations)
