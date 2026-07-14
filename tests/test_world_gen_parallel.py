"""Tests — parallele Chunk-Generierung (M22b)."""

from __future__ import annotations

from game_core.content_registry import load_content_registry
from game_core.chunk_gen_pool import ChunkGenPool
from game_core.world_gen import generate_chunk
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_parallel import (
    generate_chunks_parallel,
    generate_results_parallel,
    resolve_worker_count,
)
from game_core.world_gen_result import chunk_from_result


def test_resolve_worker_count() -> None:
    assert resolve_worker_count(0) == 0
    assert resolve_worker_count("0") == 0
    assert resolve_worker_count(2) == 2


def test_parallel_matches_sequential_layer_keys() -> None:
    coords = [(0, 0), (1, 2), (-1, 3), (4, -2)]
    sequential = {coord: generate_chunk(coord[0], coord[1]) for coord in coords}
    parallel = generate_chunks_parallel(coords, workers=2)
    assert set(parallel.keys()) == set(sequential.keys())
    for coord in coords:
        assert parallel[coord].layer_keys == sequential[coord].layer_keys


def test_worker_results_use_tile_ids() -> None:
    results = generate_results_parallel([(2, 2)], workers=2)
    result = results[(2, 2)]
    assert len(result.layer0) == 64
    assert all(isinstance(tile_id, int) for tile_id in result.layer0)
    assert all(isinstance(tile_id, int) for tile_id in result.layer1)


def test_worker_results_have_no_decorations_when_apply_disabled() -> None:
    results = generate_results_parallel([(2, 2)], workers=2)
    result = results[(2, 2)]
    assert result.decorations is None


def test_worker_results_include_decorations_when_apply_enabled() -> None:
    from dataclasses import replace

    from game_core.world_gen import get_world_gen_config

    ctx = WorldGenContext.from_configs(
        replace(get_world_gen_config(), parallel_worker_apply=True)
    )
    results = generate_results_parallel([(2, 2)], ctx=ctx, workers=2)
    result = results[(2, 2)]
    assert result.decorations is not None
    assert result.solid_grid is not None


def test_chunk_from_result_roundtrip() -> None:
    ctx = WorldGenContext.from_active()
    content = load_content_registry()
    result = ctx.generate_terrain_result(3, 3)
    chunk = chunk_from_result(result, content)
    direct = generate_chunk(3, 3)
    assert chunk.layer_keys == direct.layer_keys


def test_workers_zero_uses_sequential_path() -> None:
    coords = [(0, 0), (1, 1)]
    parallel = generate_chunks_parallel(coords, workers=0)
    for coord in coords:
        assert parallel[coord].layer_keys == generate_chunk(coord[0], coord[1]).layer_keys


def test_chunk_gen_pool_discard_drops_result() -> None:
    ctx = WorldGenContext.from_active()
    pool = ChunkGenPool(ctx, workers=2)
    try:
        pool.submit([(0, 0)])
        pool.discard([(0, 0)])
        ready = pool.poll_ready()
        while not ready:
            ready = pool.poll_ready()
            if not pool._futures and not pool._ready:
                break
        assert all(result.coord != (0, 0) for result in ready)
    finally:
        pool.shutdown()
