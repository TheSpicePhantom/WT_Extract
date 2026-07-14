"""Tests — M24c Terrain-Performance und Determinismus."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import patch

import pytest

from game_core.chunk_build import BuildCoordinator
from game_core.chunk_stage import build_terrain_stage, to_terrain_result
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.noise import clear_perm_cache, get_perm
from game_core.tile_ids import stable_tile_id
from game_core.world import CHUNK_TILE_COUNT
from game_core.world_gen import get_world_gen_config
from game_core.world_gen_context import WorldGenContext
from tests.support.chunk_reference import REFERENCE_TEST_COORDS, sequential_reference_chunk


def _ctx() -> WorldGenContext:
    config = replace(get_world_gen_config(), parallel_worker_apply=True)
    return WorldGenContext.from_configs(config)


def test_build_terrain_stage_single_field_cache_pass() -> None:
    coordinator = BuildCoordinator()
    ctx = _ctx()
    build_key = coordinator.next_terrain_build_key((0, 0))
    calls = {"count": 0}
    import game_core.world_gen as world_gen

    original = world_gen.build_chunk_field_cache

    def counting(*args, **kwargs):
        calls["count"] += 1
        return original(*args, **kwargs)

    with patch.object(world_gen, "build_chunk_field_cache", side_effect=counting):
        build_terrain_stage(build_key, ctx)

    assert calls["count"] == 1


def test_perm_cache_reuses_table() -> None:
    clear_perm_cache()
    perm_a = get_perm(12345)
    perm_b = get_perm(12345)
    assert perm_a is perm_b
    assert len(perm_a) == 512


def test_spawn_score_at_most_once_per_chunk_session() -> None:
    from game_core.world_gen import score_spawn_area

    ctx = _ctx()
    ctx.reset_chunk_build_session()
    calls = {"count": 0}
    original = score_spawn_area

    def counting(cfg):
        calls["count"] += 1
        return original(cfg)

    with patch("game_core.world_gen.score_spawn_area", side_effect=counting):
        ctx.spawn_score()
        ctx.spawn_score()
        ctx.spawn_score()

    assert calls["count"] == 1


@pytest.mark.parametrize("coord", REFERENCE_TEST_COORDS[:4])
def test_build_terrain_stage_matches_reference_layers(coord: tuple[int, int]) -> None:
    content = load_content_registry()
    collision = load_collision_catalog()
    ref = sequential_reference_chunk(coord, content, collision)
    ctx = _ctx()
    coordinator = BuildCoordinator()
    build_key = coordinator.next_terrain_build_key(coord)
    stage = build_terrain_stage(build_key, ctx)
    result = to_terrain_result(stage)

    assert len(result.layer0) == CHUNK_TILE_COUNT
    assert result.layer0 == ref.layer0
    assert tuple(stable_tile_id(k) for k in stage.layer1) == ref.layer1


def test_fbm_precalc_has_perm() -> None:
    from game_core.noise import FbmParams, precalc_fbm

    precalc = precalc_fbm(
        FbmParams(octaves=2, lacunarity=2.0, persistence=0.5, scale=0.01, seed=99)
    )
    assert len(precalc.perm) == 512
