"""Tests — Startgebiet-Scoring und Seed-Auswahl (M21-Rest)."""

from __future__ import annotations

from dataclasses import replace

from game_core.world_gen import ensure_playable_seed, score_spawn_area


def test_score_spawn_area_in_range() -> None:
    score = score_spawn_area()
    assert 0.0 <= score <= 1.0


def test_score_spawn_monotonic_with_land_boost() -> None:
    from game_core.world_gen import get_world_gen_config

    base = get_world_gen_config()
    low_sea = replace(base, sea_level=0.95)
    high_sea = replace(base, sea_level=0.05)
    assert score_spawn_area(high_sea) >= score_spawn_area(low_sea)


def test_ensure_playable_seed_returns_config() -> None:
    from game_core.world_gen import get_world_gen_config

    config = get_world_gen_config()
    result = ensure_playable_seed(config, max_attempts=4)
    assert result.world_seed >= config.world_seed
