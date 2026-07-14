"""Parallele Chunk-Terrain-Generierung via ProcessPoolExecutor (M22b)."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Sequence

from game_core.biomes import BiomesConfig
from game_core.world import Chunk, World
from game_core.world_gen_context import WorldGenContext
from game_core.content_registry import load_content_registry
from game_core.world_gen_result import ChunkGenResult, chunk_from_result

from game_core.chunk_build import BuildKey
from game_core.chunk_stage import (
    TerrainResult,
    DecoResult,
    build_deco_stage,
    build_terrain_stage,
    to_deco_result,
    to_terrain_result,
)
from game_core.field_cache_lru import worker_terrain_stage_lru

_worker_ctx: WorldGenContext | None = None

_pool: ProcessPoolExecutor | None = None
_pool_signature: tuple | None = None
_pool_worker_count: int = 0


def resolve_worker_count(setting: int | str | None) -> int:
    if setting is None or setting == 0 or setting == "0":
        return 0
    if setting == "auto":
        count = os.cpu_count() or 1
        return max(1, count - 1)
    if isinstance(setting, str):
        return max(0, int(setting))
    return max(0, int(setting))


def _pool_worker_init(config, biomes: BiomesConfig) -> None:
    global _worker_ctx
    from game_core.world_gen import bind_generation_context
    from game_core.collision_catalog import load_collision_catalog
    from game_core.content_registry import load_content_registry
    from game_core.worker_content_snapshot import WorkerContentSnapshot

    ctx = WorldGenContext.from_configs(config, biomes)
    ctx.warm_fbm_cache()
    ctx._worker_snapshot = WorkerContentSnapshot.from_registry(load_content_registry())
    ctx._worker_collision = load_collision_catalog()
    _worker_ctx = ctx
    bind_generation_context(ctx)


def _generate_terrain_task(build_key: BuildKey) -> TerrainResult:
    assert _worker_ctx is not None
    stage = build_terrain_stage(build_key, _worker_ctx)
    worker_terrain_stage_lru().put(build_key, stage)
    return to_terrain_result(stage)


def _generate_deco_task(build_key: BuildKey) -> DecoResult:
    assert _worker_ctx is not None
    lru = worker_terrain_stage_lru()
    stage = lru.get(build_key)
    if stage is None:
        stage = build_terrain_stage(build_key, _worker_ctx)
    deco_stage = build_deco_stage(stage, _worker_ctx)
    lru.consume(build_key)
    return to_deco_result(deco_stage)


def _generate_chunk_pipeline_task(build_key: BuildKey) -> tuple[TerrainResult, DecoResult]:
    """M24c.2 — Terrain+Deco in einem Worker-Job (kein Cross-Process-LRU-Miss)."""
    assert _worker_ctx is not None
    stage = build_terrain_stage(build_key, _worker_ctx)
    deco_stage = build_deco_stage(stage, _worker_ctx)
    return to_terrain_result(stage), to_deco_result(deco_stage)


def _generate_terrain_task_legacy(coord: tuple[int, int]) -> ChunkGenResult:
    assert _worker_ctx is not None
    cx, cy = coord
    return _worker_ctx.generate_chunk_result(cx, cy)


def invalidate_parallel_pool() -> None:
    global _pool, _pool_signature, _pool_worker_count
    if _pool is not None:
        _pool.shutdown(wait=False, cancel_futures=True)
    _pool = None
    _pool_signature = None
    _pool_worker_count = 0


def shutdown_parallel_pool() -> None:
    invalidate_parallel_pool()


def get_or_create_pool(ctx: WorldGenContext, workers: int) -> ProcessPoolExecutor | None:
    global _pool, _pool_signature, _pool_worker_count
    if workers <= 0:
        return None
    signature = ctx.pool_signature()
    if _pool is not None and _pool_signature == signature and _pool_worker_count == workers:
        return _pool
    invalidate_parallel_pool()
    _pool = ProcessPoolExecutor(
        max_workers=workers,
        initializer=_pool_worker_init,
        initargs=(ctx.config, ctx.biomes),
    )
    _pool_signature = signature
    _pool_worker_count = workers
    return _pool


def generate_results_parallel(
    coords: Sequence[tuple[int, int]],
    *,
    ctx: WorldGenContext | None = None,
    workers: int | None = None,
) -> dict[tuple[int, int], ChunkGenResult]:
    if not coords:
        return {}
    context = ctx or WorldGenContext.from_active()
    from game_core.world_gen import get_debug_mode, get_world_gen_config

    if get_debug_mode() is not None:
        results: dict[tuple[int, int], ChunkGenResult] = {}
        for cx, cy in coords:
            results[(cx, cy)] = context.generate_terrain_result(cx, cy)
        return results

    worker_count = resolve_worker_count(
        workers if workers is not None else get_world_gen_config().parallel_workers
    )
    if worker_count <= 0 or len(coords) == 1:
        results = {}
        for cx, cy in coords:
            results[(cx, cy)] = context.generate_terrain_result(cx, cy)
        return results

    pool = get_or_create_pool(context, worker_count)
    assert pool is not None
    ordered = list(dict.fromkeys(coords))
    results: dict[tuple[int, int], ChunkGenResult] = {}
    futures = {pool.submit(_generate_terrain_task_legacy, coord): coord for coord in ordered}
    for future in as_completed(futures):
        result = future.result()
        results[result.coord] = result
    return results


def generate_chunks_parallel(
    coords: Sequence[tuple[int, int]],
    *,
    ctx: WorldGenContext | None = None,
    workers: int | None = None,
) -> dict[tuple[int, int], Chunk]:
    results = generate_results_parallel(coords, ctx=ctx, workers=workers)
    content = load_content_registry()
    return {coord: chunk_from_result(result, content) for coord, result in results.items()}


def generate_demo_world_parallel(cols: int = 16, rows: int = 16) -> World:
    coords = [(cx, cy) for cy in range(rows) for cx in range(cols)]
    chunks = generate_chunks_parallel(coords)
    return World(chunks=chunks)
