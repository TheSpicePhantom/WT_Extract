"""Aggregation — P95, Mean, Summary (M23)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from game_core.perf.hitch import HITCH_TAG_ORDER
from game_core.perf.models import FrameMetrics, HitchEvent, RunSummary


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * pct))
    index = max(0, min(index, len(ordered) - 1))
    return ordered[index]


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


@dataclass
class RollingAggregate:
    capacity: int
    _frames: deque[FrameMetrics] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self._frames = deque(maxlen=self.capacity)

    def push(self, frame: FrameMetrics) -> None:
        self._frames.append(frame)

    @property
    def stream_ms_mean(self) -> float:
        return _mean([frame.stream_ms for frame in self._frames])

    @property
    def hitch_count(self) -> int:
        return sum(1 for _ in self._iter_hitches_from_buffer())

    def _iter_hitches_from_buffer(self):
        return iter(())


class PerfAggregator:
    def __init__(self) -> None:
        self._frames: list[FrameMetrics] = []
        self._hitches: list[HitchEvent] = []

    def record_frame(self, frame: FrameMetrics) -> None:
        self._frames.append(frame)

    def record_hitch(self, hitch: HitchEvent) -> None:
        self._hitches.append(hitch)

    @property
    def frames(self) -> list[FrameMetrics]:
        return list(self._frames)

    @property
    def hitches(self) -> list[HitchEvent]:
        return list(self._hitches)

    def build_summary(
        self,
        *,
        schema_version: int,
        run_id: str,
        scenario_id: str,
        run_mode: str,
    ) -> RunSummary:
        frames = self._frames
        frame_ms_values = [frame.frame_ms for frame in frames]
        stream_ms_values = [frame.stream_ms for frame in frames]
        unload_ms_values = [frame.stream_unload_ms for frame in frames]
        chunk_counts = [float(frame.chunk_count) for frame in frames]

        hitch_frame = sum(1 for event in self._hitches if "frame_slow" in event.tags)
        hitch_stream = sum(1 for event in self._hitches if "stream_slow" in event.tags)
        hitch_load = sum(1 for event in self._hitches if "load_burst" in event.tags)
        hitch_unload = sum(1 for event in self._hitches if "unload_burst" in event.tags)

        max_loaded = max((frame.stream_loaded for frame in frames), default=0)
        max_unloaded = max((frame.stream_unloaded for frame in frames), default=0)

        return RunSummary(
            schema_version=schema_version,
            run_id=run_id,
            scenario_id=scenario_id,
            run_mode=run_mode,
            recorded_frames=len(frames),
            frame_ms_mean=_mean(frame_ms_values),
            frame_ms_p95=_percentile(frame_ms_values, 0.95),
            frame_ms_max=max(frame_ms_values, default=0.0),
            stream_ms_mean=_mean(stream_ms_values),
            stream_ms_p95=_percentile(stream_ms_values, 0.95),
            stream_ms_max=max(stream_ms_values, default=0.0),
            stream_unload_ms_p95=_percentile(unload_ms_values, 0.95),
            stream_unload_ms_max=max(unload_ms_values, default=0.0),
            hitch_count=len(self._hitches),
            hitch_frame_count=hitch_frame,
            hitch_stream_count=hitch_stream,
            hitch_load_count=hitch_load,
            hitch_unload_count=hitch_unload,
            max_loaded_per_frame=max_loaded,
            max_unloaded_per_frame=max_unloaded,
            chunk_count_mean=_mean(chunk_counts),
        )


def count_hitch_tags(hitches: list[HitchEvent]) -> dict[str, int]:
    counts = {tag: 0 for tag in HITCH_TAG_ORDER}
    for event in hitches:
        for tag in event.tags:
            if tag in counts:
                counts[tag] += 1
    return counts
