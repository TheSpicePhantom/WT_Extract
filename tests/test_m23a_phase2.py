"""Tests — M23a Phase 2: Budgetierter Drain."""

from __future__ import annotations

from unittest.mock import MagicMock

from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.streaming_config import StreamingConfig
from game_core.world import CHUNK_SIZE_PX, World


def test_drain_respects_max_unloads_per_frame() -> None:
    world = World()
    content = load_content_registry()
    collision = load_collision_catalog()
    extractor = MagicMock()
    config = StreamingConfig(
        mode="radius",
        load_radius=2,
        unload_radius=3,
        max_applies_per_frame=0,
        max_unloads_per_frame=1,
    )
    streamer = ChunkStreamer(config=config)
    streamer.update(world, 0.0, 0.0, content, collision, extractor)
    far_x = 40 * CHUNK_SIZE_PX
    streamer.update(world, far_x, 0.0, content, collision, extractor)
    pending_after_pan = streamer.pending_unload.count()
    assert pending_after_pan > 1
    streamer.update(world, far_x, 0.0, content, collision, extractor)
    assert streamer.pending_unload.count() == pending_after_pan - 1
