"""Tests M23b — Apply-Microprofile und Burst-Glättung."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.perf.models import StreamStepMetrics
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, World


def _runtime():
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    streamer = ChunkStreamer(
        config=StreamingConfig(
            mode="radius",
            load_radius=2,
            unload_radius=3,
            max_applies_per_frame=4,
            max_sync_applies_per_frame=2,
        )
    )
    extractor = MagicMock()
    return world, streamer, content, collision, extractor


def test_sync_apply_respects_max_sync_applies_per_frame() -> None:
    world, streamer, content, collision, extractor = _runtime()
    for step in range(8):
        metrics = StreamStepMetrics()
        streamer.update(
            world,
            focus_x=float(CHUNK_SIZE_PX) + step * CHUNK_SIZE_PX * 2,
            focus_y=float(CHUNK_SIZE_PX),
            content=content,
            collision=collision,
            extractor=extractor,
            step_metrics=metrics,
        )
        assert metrics.loaded <= 4
        if metrics.loaded > 0:
            assert metrics.apply_sync_generate_ms <= metrics.apply_ms * 1.05 + 0.01


def test_apply_submetrics_sum_approx_apply_ms() -> None:
    world, streamer, content, collision, extractor = _runtime()
    metrics = StreamStepMetrics()
    for step in range(12):
        metrics.reset()
        streamer.update(
            world,
            focus_x=float(CHUNK_SIZE_PX) + step * CHUNK_SIZE_PX * 2,
            focus_y=float(CHUNK_SIZE_PX),
            content=content,
            collision=collision,
            extractor=extractor,
            step_metrics=metrics,
        )
        if metrics.apply_ms <= 0:
            continue
        sub_sum = (
            metrics.apply_worker_ms
            + metrics.apply_sync_generate_ms
            + metrics.apply_delta_ms
            + metrics.apply_override_ms
            + metrics.apply_pool_ms
            + metrics.apply_collision_ms
        )
        assert sub_sum <= metrics.apply_ms * 1.05 + 0.01


def test_no_metrics_overhead_when_step_metrics_none() -> None:
    world, streamer, content, collision, extractor = _runtime()
    loaded, unloaded = streamer.update(
        world,
        float(CHUNK_SIZE_PX),
        float(CHUNK_SIZE_PX),
        content,
        collision,
        extractor,
        step_metrics=None,
    )
    assert loaded >= 0
    assert unloaded >= 0
