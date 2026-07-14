"""Reproduzierbare Profiling-Szenarien (M23)."""

from __future__ import annotations

from dataclasses import replace

from game_core.perf.config import ProfilingConfig, ScenarioParams
from game_core.perf.models import ScenarioDescriptor
from game_core.stream_view import StreamViewParams
from game_core.world import CHUNK_SIZE_PX

DEFAULT_SPAWN_X = float(CHUNK_SIZE_PX)
DEFAULT_SPAWN_Y = float(CHUNK_SIZE_PX)
DEFAULT_VIEWPORT_W = 1280
DEFAULT_VIEWPORT_H = 720


def scenario_descriptor(config: ProfilingConfig, scenario_id: str) -> ScenarioDescriptor:
    params = config.scenarios.get(scenario_id)
    if params is None:
        raise KeyError(f"Unknown scenario_id: {scenario_id}")
    return ScenarioDescriptor(
        scenario_id=scenario_id,
        frames=params.frames,
        warmup_frames=params.warmup_frames,
        extract_enabled=params.extract_enabled,
        stream_enabled=params.stream_enabled,
        deco_extract_enabled=params.deco_extract_enabled,
        tile_extract_enabled=params.tile_extract_enabled,
        pan_axis=params.pan_axis,
        pan_chunks_per_frame=params.pan_chunks_per_frame,
        zoom=params.zoom if scenario_id != "pan" else 0.35,
    )


def scenario_params_for_id(config: ProfilingConfig, scenario_id: str) -> ScenarioParams:
    params = config.scenarios.get(scenario_id)
    if params is None:
        raise KeyError(f"Unknown scenario_id: {scenario_id}")
    if scenario_id == "zoom_out":
        return replace(params, zoom=params.zoom)
    if scenario_id == "pan":
        return replace(params, zoom=0.35)
    return params


def focus_for_frame(
    scenario: ScenarioDescriptor,
    frame_index: int,
    *,
    last_focus_x: float,
    last_focus_y: float,
) -> tuple[float, float, float, float, float]:
    """Returns focus_x, focus_y, zoom, move_dx, move_dy."""
    zoom = scenario.zoom
    if scenario.scenario_id == "steady":
        focus_x, focus_y = DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y
    elif scenario.scenario_id == "zoom_out":
        focus_x, focus_y = DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y
    elif scenario.scenario_id in ("pan", "catchup"):
        delta = scenario.pan_chunks_per_frame * CHUNK_SIZE_PX * (frame_index + 1)
        if scenario.pan_axis == "y":
            focus_x, focus_y = DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y + delta
        else:
            focus_x, focus_y = DEFAULT_SPAWN_X + delta, DEFAULT_SPAWN_Y
    else:
        focus_x, focus_y = DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y

    move_dx = focus_x - last_focus_x
    move_dy = focus_y - last_focus_y
    return focus_x, focus_y, zoom, move_dx, move_dy


def stream_view_for_frame(
    focus_x: float,
    focus_y: float,
    zoom: float,
    *,
    move_dx: float = 0.0,
    move_dy: float = 0.0,
    viewport_w: int = DEFAULT_VIEWPORT_W,
    viewport_h: int = DEFAULT_VIEWPORT_H,
) -> StreamViewParams:
    return StreamViewParams(
        focus_x=focus_x,
        focus_y=focus_y,
        player_x=focus_x,
        player_y=focus_y,
        zoom=zoom,
        viewport_w=viewport_w,
        viewport_h=viewport_h,
        move_dx=move_dx,
        move_dy=move_dy,
    )
