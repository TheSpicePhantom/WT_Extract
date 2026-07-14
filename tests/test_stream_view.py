"""Tests — Stream-View-Mengen (M22d)."""

from __future__ import annotations

import math

from dataclasses import replace

from game_core.stream_view import (
    StreamViewParams,
    compute_stream_sets,
    expand_aabb,
    viewport_world_bounds,
)
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX


def _demo_params(
    *,
    zoom: float = 0.35,
    focus_x: float = float(CHUNK_SIZE_PX),
    focus_y: float = float(CHUNK_SIZE_PX),
    move_dx: float = 0.0,
    move_dy: float = 0.0,
) -> StreamViewParams:
    return StreamViewParams(
        focus_x=focus_x,
        focus_y=focus_y,
        player_x=focus_x,
        player_y=focus_y,
        zoom=zoom,
        viewport_w=1280,
        viewport_h=720,
        move_dx=move_dx,
        move_dy=move_dy,
    )


def _hybrid_config(**overrides) -> StreamingConfig:
    return replace(StreamingConfig(mode="hybrid"), **overrides)


def test_hybrid_visible_smaller_than_radius_at_gameplay_zoom() -> None:
    params = _demo_params()
    hybrid = compute_stream_sets(params, _hybrid_config())
    radius = compute_stream_sets(
        params,
        StreamingConfig(mode="radius", load_radius=8, unload_radius=10),
    )
    assert len(hybrid.visible) < len(radius.wanted)
    assert len(hybrid.wanted) < len(radius.wanted)


def test_zoom_out_respects_max_loaded_chunks() -> None:
    params = _demo_params(zoom=0.05)
    policy = _hybrid_config(max_loaded_chunks=80)
    sets = compute_stream_sets(params, policy)
    assert len(sets.wanted) <= 80


def test_keep_is_superset_of_wanted_with_padding() -> None:
    params = _demo_params()
    policy = _hybrid_config(keep_padding_chunks=1)
    sets = compute_stream_sets(params, policy)
    assert sets.wanted.issubset(sets.keep)
    assert len(sets.keep) >= len(sets.wanted)


def test_player_safety_outside_viewport_stays_in_wanted() -> None:
    params = StreamViewParams(
        focus_x=float(CHUNK_SIZE_PX * 2),
        focus_y=float(CHUNK_SIZE_PX * 2),
        player_x=float(CHUNK_SIZE_PX),
        player_y=float(CHUNK_SIZE_PX),
        zoom=0.35,
        viewport_w=1280,
        viewport_h=720,
    )
    sets = compute_stream_sets(params, _hybrid_config(player_safety_ring=1))
    player_chunk = (1, 1)
    assert player_chunk in sets.wanted


def test_prefetch_strip_east_of_keep() -> None:
    from game_core.stream_view import prefetch_strip

    keep = {(0, 0), (1, 0), (0, 1), (1, 1)}
    params = StreamViewParams(
        focus_x=128.0,
        focus_y=128.0,
        player_x=128.0,
        player_y=128.0,
        zoom=1.0,
        viewport_w=512,
        viewport_h=512,
        move_dx=32.0,
        move_dy=0.0,
    )
    policy = _hybrid_config(prefetch_chunks=2, prefetch_min_speed_px=1.0)
    strip = prefetch_strip(keep, params, policy)
    assert any(coord[0] > 1 for coord in strip)


def test_viewport_bounds_match_half_width_formula() -> None:
    params = _demo_params(zoom=1.0)
    policy = _hybrid_config(max_half_chunks_cap=100)
    left, right, bottom, top = viewport_world_bounds(params, policy)
    expected_half_w = (1280 / 1.0) * 0.5
    assert math.isclose(right - params.focus_x, expected_half_w, rel_tol=1e-6)
    assert math.isclose(params.focus_x - left, expected_half_w, rel_tol=1e-6)
    assert math.isclose(top - params.focus_y, (720 / 1.0) * 0.5, rel_tol=1e-6)


def test_cap_trim_keeps_nearest_to_focus() -> None:
    params = _demo_params(zoom=0.05)
    policy = _hybrid_config(max_loaded_chunks=10)
    sets = compute_stream_sets(params, policy)
    focus_chunk = (int(params.focus_x // CHUNK_SIZE_PX), int(params.focus_y // CHUNK_SIZE_PX))
    for coord in sets.wanted:
        assert max(abs(coord[0] - focus_chunk[0]), abs(coord[1] - focus_chunk[1])) <= 3
