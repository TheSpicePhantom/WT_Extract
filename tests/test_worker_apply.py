"""Tests — apply_chunk_result und Streaming-Router (M22e Phase 4)."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock, patch

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.streaming_config import StreamingConfig
from game_core.world import World
from game_core.world_gen import generate_chunk, get_world_gen_config, populate_chunk_decorations
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_result import apply_chunk_result, apply_worker_complete_result
from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def _worker_ctx() -> WorldGenContext:
    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    return WorldGenContext.from_configs(config)


def test_apply_chunk_result_matches_reference() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = _worker_ctx()

    for coord in REFERENCE_TEST_COORDS[:6]:
        ref = sequential_reference_chunk(coord, content, collision)
        result = ctx.generate_chunk_result(coord[0], coord[1])
        world = World()
        apply_chunk_result(world, result, content, collision)

        ref_world = World()
        ref_world.chunks[coord] = generate_chunk(coord[0], coord[1])
        populate_chunk_decorations(ref_world, content, coord[0], coord[1])
        ref_world.rebuild_chunk_solid(coord, content, collision)

        assert world.chunks[coord].solid_grid == ref.solid_grid
        assert world.chunks[coord].solid_grid == ref_world.chunks[coord].solid_grid
        assert len(world.decorations) == len(ref.procedural_decorations)


def test_apply_sets_no_dirty_chunks() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = _worker_ctx()
    result = ctx.generate_chunk_result(0, 0)
    world = World()
    apply_chunk_result(world, result, content, collision)
    assert (0, 0) not in world.dirty_chunks
    assert (0, 0) not in world.collision_dirty_chunks


def test_streaming_pool_uses_apply_not_populate() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    config = StreamingConfig(mode="radius", max_applies_per_frame=0)
    streamer = ChunkStreamer(config=config)
    extractor = MagicMock()
    ctx = _worker_ctx()
    ready = ctx.generate_chunk_result(0, 0)
    gen_config = replace(get_world_gen_config(), parallel_worker_apply=True, parallel_prefetch=True)

    with patch("game_core.world_gen.get_world_gen_config", return_value=gen_config):
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
                    with patch("game_core.world_gen.populate_chunk_decorations") as populate_mock:
                        with patch(
                            "game_core.chunk_streaming.apply_worker_complete_result",
                            wraps=apply_worker_complete_result,
                        ) as apply_mock:
                            streamer.update(world, 0.0, 0.0, content, collision, extractor)
                            assert apply_mock.called
                            populate_mock.assert_not_called()


def test_streaming_override_uses_load_chunk_path() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    config = StreamingConfig(mode="radius", max_applies_per_frame=0)
    streamer = ChunkStreamer(config=config)
    streamer.persistent_overrides[(0, 0)] = generate_chunk(0, 0)
    extractor = MagicMock()
    stream_sets = MagicMock()
    stream_sets.wanted = {(0, 0)}
    stream_sets.keep = {(0, 0)}
    stream_sets.prefetch = set()

    with patch.object(streamer, "_resolve_stream_sets", return_value=stream_sets):
        with patch("game_core.chunk_streaming.apply_worker_complete_result") as apply_mock:
            streamer.update(world, 0.0, 0.0, content, collision, extractor)
            apply_mock.assert_not_called()
            assert (0, 0) in world.chunks


def test_streaming_debug_mode_disables_worker_apply() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    config = StreamingConfig(mode="radius", max_applies_per_frame=0)
    streamer = ChunkStreamer(config=config)
    extractor = MagicMock()
    ctx = _worker_ctx()
    ready = ctx.generate_chunk_result(0, 0)

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
            with patch("game_core.world_gen.get_debug_mode", return_value=object()):
                with patch("game_core.chunk_streaming.apply_worker_complete_result") as apply_mock:
                    streamer.update(world, 0.0, 0.0, content, collision, extractor)
                    apply_mock.assert_not_called()
