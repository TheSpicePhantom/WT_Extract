"""Tests — Worker ChunkGenResult (M22e Phase 3)."""

from __future__ import annotations

from dataclasses import replace

from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.world_gen import get_world_gen_config
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_parallel import generate_results_parallel
from game_core.world import CHUNK_TILE_COUNT
from game_core.world_gen_result import is_worker_complete, validate_chunk_gen_result

from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def _worker_ctx() -> WorldGenContext:
    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    return WorldGenContext.from_configs(config)


def test_generate_chunk_result_matches_reference() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = _worker_ctx()

    for coord in REFERENCE_TEST_COORDS:
        ref = sequential_reference_chunk(coord, content, collision)
        result = ctx.generate_chunk_result(coord[0], coord[1])
        assert is_worker_complete(result)
        validate_chunk_gen_result(result)
        assert result.layer0 == ref.layer0
        assert result.layer1 == ref.layer1
        assert result.solid_grid == ref.solid_grid
        ipc_deco = tuple(
            sorted(
                (p.wx, p.wy, content.decoration_id_to_key(p.decoration_id))
                for p in result.decorations or ()
            )
        )
        ref_deco = tuple(
            sorted((d.wx, d.wy, d.decoration_id) for d in ref.procedural_decorations)
        )
        assert ipc_deco == ref_deco


def test_parallel_chunk_result_matches_reference() -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ctx = _worker_ctx()
    coords = REFERENCE_TEST_COORDS[:4]

    results = generate_results_parallel(coords, ctx=ctx, workers=2)
    for coord in coords:
        ref = sequential_reference_chunk(coord, content, collision)
        result = results[coord]
        assert is_worker_complete(result)
        assert result.layer0 == ref.layer0
        assert result.solid_grid == ref.solid_grid


def test_invalid_partial_result_raises() -> None:
    from game_core.world_gen_result import ChunkGenResult
    import pytest

    with pytest.raises(ValueError):
        validate_chunk_gen_result(
            ChunkGenResult(
                coord=(0, 0),
                layer0=(0,) * CHUNK_TILE_COUNT,
                layer1=(0,) * CHUNK_TILE_COUNT,
                decorations=(),
                solid_grid=None,
            )
        )
