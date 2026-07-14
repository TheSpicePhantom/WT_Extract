"""Tests — ChunkStreamer StreamStepMetrics (M23 Phase 1)."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.models import StreamStepMetrics
from game_core.stream_view import StreamViewParams
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, World


def _setup() -> tuple[ChunkStreamer, World, object, object, MagicMock]:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=1,
        unload_radius=3,
        max_applies_per_frame=4,
        max_sync_applies_per_frame=4,
    )
    streamer = ChunkStreamer(config=config)
    return streamer, world, content, collision, extractor


def test_update_without_metrics_unchanged() -> None:
    streamer, world, content, collision, extractor = _setup()
    loaded, unloaded = streamer.update(world, 0.0, 0.0, content, collision, extractor)
    assert loaded > 0
    assert unloaded == 0
    assert world.chunk_count > 0


def test_update_with_metrics_populates_fields() -> None:
    streamer, world, content, collision, extractor = _setup()
    metrics = StreamStepMetrics()
    loaded, unloaded = streamer.update(
        world,
        0.0,
        0.0,
        content,
        collision,
        extractor,
        step_metrics=metrics,
    )
    assert metrics.loaded == loaded
    assert metrics.unloaded == unloaded
    assert metrics.total_ms >= metrics.apply_ms
    assert metrics.total_ms >= metrics.unload_ms
    assert metrics.sets_ms >= 0.0


def test_update_metrics_apply_unload_on_pan() -> None:
    streamer, world, content, collision, extractor = _setup()
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    metrics = StreamStepMetrics()
    far_x = 40 * CHUNK_SIZE_PX
    far_y = 40 * CHUNK_SIZE_PX
    view = StreamViewParams(
        focus_x=far_x,
        focus_y=far_y,
        player_x=far_x,
        player_y=far_y,
        zoom=0.35,
        viewport_w=1280,
        viewport_h=720,
    )
    loaded, unloaded = streamer.update(
        world,
        far_x,
        far_y,
        content,
        collision,
        extractor,
        view=view,
        step_metrics=metrics,
    )
    assert loaded > 0 or unloaded > 0
    assert metrics.apply_ms >= 0.0
    assert metrics.unload_ms >= 0.0
    assert metrics.total_ms >= metrics.apply_ms + metrics.unload_ms - 0.01
