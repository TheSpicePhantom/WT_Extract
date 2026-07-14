"""Prefetch-Pool — Terrain/Deco zwei Jobtypen (M24b)."""

from __future__ import annotations

import time
from concurrent.futures import Future
from enum import Enum
from typing import Iterable

from game_core.chunk_build import BuildCoordinator, BuildKey
from game_core.chunk_stage import DecoResult, TerrainResult
from game_core.world_gen_context import WorldGenContext
from game_core.world_gen_parallel import (
    _generate_chunk_pipeline_task,
    _generate_deco_task,
    _generate_terrain_task,
    get_or_create_pool,
    resolve_worker_count,
    shutdown_parallel_pool,
)


class _JobState(str, Enum):
    SUBMITTED = "submitted"
    RUNNING = "running"
    READY = "ready"
    DISCARDED = "discarded"


class ChunkGenPool:
    """Ein Pool, zwei Jobtypen — BuildCoordinator owned build_epoch."""

    def __init__(self, ctx: WorldGenContext, workers: int) -> None:
        self._ctx = ctx
        self._workers = workers
        self._pool = get_or_create_pool(ctx, workers)
        self.coordinator = BuildCoordinator()
        self._terrain_futures: dict[BuildKey, Future] = {}
        self._deco_futures: dict[BuildKey, Future] = {}
        self._pipeline_futures: dict[BuildKey, Future] = {}
        self._terrain_states: dict[BuildKey, _JobState] = {}
        self._deco_states: dict[BuildKey, _JobState] = {}
        self._terrain_ready: dict[BuildKey, TerrainResult] = {}
        self._deco_ready: dict[BuildKey, DecoResult] = {}
        self._terrain_submitted_at: dict[BuildKey, float] = {}
        self._deco_submitted_at: dict[BuildKey, float] = {}
        self._running_terrain = 0
        self._running_deco = 0

    @classmethod
    def from_active_config(cls) -> ChunkGenPool | None:
        from game_core.world_gen import get_world_gen_config

        config = get_world_gen_config()
        workers = resolve_worker_count(config.parallel_workers)
        if workers <= 0 or not config.parallel_prefetch:
            return None
        return cls(WorldGenContext.from_active(), workers)

    @property
    def build_epoch(self) -> int:
        return self.coordinator.read_build_epoch()

    def sync_active(self) -> None:
        from game_core.world_gen import get_world_gen_config

        config = get_world_gen_config()
        workers = resolve_worker_count(config.parallel_workers)
        if workers <= 0 or not config.parallel_prefetch:
            self._pool = None
            return
        self._ctx = WorldGenContext.from_active()
        new_pool = get_or_create_pool(self._ctx, workers)
        if new_pool is self._pool:
            return
        self._clear_all_jobs()
        self.coordinator.bump_epoch()
        self._workers = workers
        self._pool = new_pool

    def _clear_all_jobs(self) -> None:
        self._terrain_futures.clear()
        self._deco_futures.clear()
        self._pipeline_futures.clear()
        self._terrain_states.clear()
        self._deco_states.clear()
        self._terrain_ready.clear()
        self._deco_ready.clear()
        self._terrain_submitted_at.clear()
        self._deco_submitted_at.clear()
        self._running_terrain = 0
        self._running_deco = 0

    def bump_epoch(self) -> None:
        self._clear_all_jobs()
        self.coordinator.bump_epoch()

    def discard_outside(self, keep: set[tuple[int, int]]) -> None:
        stale_terrain = [k for k in self._terrain_states if k.coord not in keep]
        stale_deco = [k for k in self._deco_states if k.coord not in keep]
        if stale_terrain:
            self.discard_terrain(stale_terrain)
        if stale_deco:
            self.discard_deco(stale_deco)

    def terrain_in_flight_count(self) -> int:
        return sum(
            1
            for state in self._terrain_states.values()
            if state in (_JobState.SUBMITTED, _JobState.RUNNING, _JobState.READY)
        )

    def deco_in_flight_count(self) -> int:
        return sum(
            1
            for state in self._deco_states.values()
            if state in (_JobState.SUBMITTED, _JobState.RUNNING, _JobState.READY)
        )

    def terrain_running_count(self) -> int:
        return self._running_terrain

    def deco_running_count(self) -> int:
        return self._running_deco

    def submit_terrain(
        self,
        coords: Iterable[tuple[int, int]],
        *,
        max_in_flight: int,
        parallelism_cap: int,
    ) -> list[BuildKey]:
        self.sync_active()
        if self._pool is None:
            return []
        submitted: list[BuildKey] = []
        for coord in coords:
            if self.terrain_in_flight_count() >= max_in_flight:
                break
            if self._running_terrain >= parallelism_cap:
                break
            build_key = self.coordinator.next_terrain_build_key(coord)
            if build_key in self._terrain_states:
                continue
            self._terrain_states[build_key] = _JobState.SUBMITTED
            self._terrain_submitted_at[build_key] = time.perf_counter()
            future = self._pool.submit(_generate_terrain_task, build_key)
            self._terrain_futures[build_key] = future
            future.add_done_callback(lambda _f, k=build_key: self._mark_terrain_running(k))
            submitted.append(build_key)
        return submitted

    def submit_chunk_pipeline(
        self,
        coords: Iterable[tuple[int, int]],
        *,
        max_in_flight: int,
        parallelism_cap: int,
    ) -> list[BuildKey]:
        """M24c.2 — Combined Terrain+Deco als ein Worker-Job pro Coord."""
        self.sync_active()
        if self._pool is None:
            return []
        submitted: list[BuildKey] = []
        for coord in coords:
            if self.terrain_in_flight_count() >= max_in_flight:
                break
            if self._running_terrain >= parallelism_cap:
                break
            build_key = self.coordinator.next_terrain_build_key(coord)
            if build_key in self._terrain_states:
                continue
            self._terrain_states[build_key] = _JobState.SUBMITTED
            self._deco_states[build_key] = _JobState.SUBMITTED
            self._terrain_submitted_at[build_key] = time.perf_counter()
            self._deco_submitted_at[build_key] = time.perf_counter()
            future = self._pool.submit(_generate_chunk_pipeline_task, build_key)
            self._pipeline_futures[build_key] = future
            future.add_done_callback(lambda _f, k=build_key: self._mark_pipeline_running(k))
            submitted.append(build_key)
        return submitted

    def _mark_pipeline_running(self, build_key: BuildKey) -> None:
        if self._terrain_states.get(build_key) == _JobState.SUBMITTED:
            self._terrain_states[build_key] = _JobState.RUNNING
            self._running_terrain += 1
        if self._deco_states.get(build_key) == _JobState.SUBMITTED:
            self._deco_states[build_key] = _JobState.RUNNING
            self._running_deco += 1

    def submit_deco(
        self,
        build_keys: Iterable[BuildKey],
        *,
        max_in_flight: int,
        parallelism_cap: int,
    ) -> list[BuildKey]:
        self.sync_active()
        if self._pool is None:
            return []
        submitted: list[BuildKey] = []
        for build_key in build_keys:
            if self.deco_in_flight_count() >= max_in_flight:
                break
            if self._running_deco >= parallelism_cap:
                break
            if build_key in self._deco_states:
                state = self._deco_states[build_key]
                if state in (_JobState.SUBMITTED, _JobState.RUNNING, _JobState.READY):
                    continue
            self._deco_states[build_key] = _JobState.SUBMITTED
            self._deco_submitted_at[build_key] = time.perf_counter()
            future = self._pool.submit(_generate_deco_task, build_key)
            self._deco_futures[build_key] = future
            future.add_done_callback(lambda _f, k=build_key: self._mark_deco_running(k))
            submitted.append(build_key)
        return submitted

    def _mark_terrain_running(self, build_key: BuildKey) -> None:
        if self._terrain_states.get(build_key) == _JobState.SUBMITTED:
            self._terrain_states[build_key] = _JobState.RUNNING
            self._running_terrain += 1

    def _mark_deco_running(self, build_key: BuildKey) -> None:
        if self._deco_states.get(build_key) == _JobState.SUBMITTED:
            self._deco_states[build_key] = _JobState.RUNNING
            self._running_deco += 1

    def discard_terrain(self, keys: Iterable[BuildKey]) -> None:
        for key in keys:
            if key in self._terrain_ready:
                del self._terrain_ready[key]
            self._terrain_states[key] = _JobState.DISCARDED
            self._terrain_futures.pop(key, None)
            self._pipeline_futures.pop(key, None)
            self._terrain_submitted_at.pop(key, None)

    def discard_deco(self, keys: Iterable[BuildKey]) -> None:
        for key in keys:
            if key in self._deco_ready:
                del self._deco_ready[key]
            self._deco_states[key] = _JobState.DISCARDED
            self._deco_futures.pop(key, None)
            self._pipeline_futures.pop(key, None)
            self._deco_submitted_at.pop(key, None)

    _IN_FLIGHT_STATES = (_JobState.SUBMITTED, _JobState.RUNNING, _JobState.READY)

    def is_terrain_in_flight(self, coord: tuple[int, int]) -> bool:
        for key, state in self._terrain_states.items():
            if key.coord == coord and state in self._IN_FLIGHT_STATES:
                return True
        return False

    def is_deco_in_flight(self, coord: tuple[int, int]) -> bool:
        for key, state in self._deco_states.items():
            if key.coord == coord and state in self._IN_FLIGHT_STATES:
                return True
        return False

    def has_pending_result(self, coord: tuple[int, int]) -> bool:
        for key in self._terrain_ready:
            if key.coord == coord:
                return True
        for key in self._deco_ready:
            if key.coord == coord:
                return True
        return False

    def terrain_in_flight_age_ms(self, coord: tuple[int, int]) -> float:
        ages: list[float] = []
        for key, submitted in self._terrain_submitted_at.items():
            if key.coord == coord:
                ages.append((time.perf_counter() - submitted) * 1000.0)
        return max(ages) if ages else 0.0

    def deco_in_flight_age_ms(self, coord: tuple[int, int]) -> float:
        ages: list[float] = []
        for key, submitted in self._deco_submitted_at.items():
            if key.coord == coord:
                ages.append((time.perf_counter() - submitted) * 1000.0)
        return max(ages) if ages else 0.0

    # Legacy compat for M24a sync-fallback
    def in_flight_count(self) -> int:
        return self.terrain_in_flight_count()

    def in_flight_age_ms(self, coord: tuple[int, int]) -> float:
        return max(self.terrain_in_flight_age_ms(coord), self.deco_in_flight_age_ms(coord))

    def is_in_flight(self, coord: tuple[int, int]) -> bool:
        return self.is_terrain_in_flight(coord) or self.is_deco_in_flight(coord)

    def poll_terrain_ready(self) -> list[TerrainResult]:
        self.sync_active()
        self._collect_terrain_futures()
        self._collect_pipeline_futures()
        ready: list[TerrainResult] = []
        for key, result in list(self._terrain_ready.items()):
            if self._terrain_states.get(key) == _JobState.DISCARDED:
                del self._terrain_ready[key]
                self._terrain_states.pop(key, None)
                continue
            ready.append(result)
        return ready

    def poll_deco_ready(self) -> list[DecoResult]:
        self.sync_active()
        self._collect_deco_futures()
        self._collect_pipeline_futures()
        ready: list[DecoResult] = []
        for key, result in list(self._deco_ready.items()):
            if self._deco_states.get(key) == _JobState.DISCARDED:
                del self._deco_ready[key]
                self._deco_states.pop(key, None)
                continue
            ready.append(result)
        return ready

    def consume_terrain(self, build_key: BuildKey) -> None:
        self._terrain_ready.pop(build_key, None)
        self._terrain_states.pop(build_key, None)
        self._terrain_futures.pop(build_key, None)
        self._pipeline_futures.pop(build_key, None)
        self._terrain_submitted_at.pop(build_key, None)
        self.coordinator.register_terrain_applied(build_key)

    def consume_deco(self, build_key: BuildKey) -> None:
        self._deco_ready.pop(build_key, None)
        self._deco_states.pop(build_key, None)
        self._deco_futures.pop(build_key, None)
        self._pipeline_futures.pop(build_key, None)
        self._deco_submitted_at.pop(build_key, None)

    def _collect_terrain_futures(self) -> None:
        for key, future in list(self._terrain_futures.items()):
            if not future.done():
                continue
            was_running = self._terrain_states.get(key) == _JobState.RUNNING
            result = future.result()
            del self._terrain_futures[key]
            self._terrain_submitted_at.pop(key, None)
            if self._terrain_states.get(key) == _JobState.DISCARDED:
                self._terrain_states.pop(key, None)
                if was_running:
                    self._running_terrain = max(0, self._running_terrain - 1)
                continue
            if was_running:
                self._running_terrain = max(0, self._running_terrain - 1)
            self._terrain_states[key] = _JobState.READY
            self._terrain_ready[key] = result

    def _collect_deco_futures(self) -> None:
        for key, future in list(self._deco_futures.items()):
            if not future.done():
                continue
            was_running = self._deco_states.get(key) == _JobState.RUNNING
            result = future.result()
            del self._deco_futures[key]
            self._deco_submitted_at.pop(key, None)
            if self._deco_states.get(key) == _JobState.DISCARDED:
                self._deco_states.pop(key, None)
                if was_running:
                    self._running_deco = max(0, self._running_deco - 1)
                continue
            if was_running:
                self._running_deco = max(0, self._running_deco - 1)
            self._deco_states[key] = _JobState.READY
            self._deco_ready[key] = result

    def _collect_pipeline_futures(self) -> None:
        for key, future in list(self._pipeline_futures.items()):
            if not future.done():
                continue
            was_terrain_running = self._terrain_states.get(key) == _JobState.RUNNING
            was_deco_running = self._deco_states.get(key) == _JobState.RUNNING
            terrain_result, deco_result = future.result()
            del self._pipeline_futures[key]
            self._terrain_submitted_at.pop(key, None)
            self._deco_submitted_at.pop(key, None)
            if self._terrain_states.get(key) == _JobState.DISCARDED:
                self._terrain_states.pop(key, None)
                self._deco_states.pop(key, None)
                if was_terrain_running:
                    self._running_terrain = max(0, self._running_terrain - 1)
                if was_deco_running:
                    self._running_deco = max(0, self._running_deco - 1)
                continue
            if was_terrain_running:
                self._running_terrain = max(0, self._running_terrain - 1)
            if was_deco_running:
                self._running_deco = max(0, self._running_deco - 1)
            self._terrain_states[key] = _JobState.READY
            self._deco_states[key] = _JobState.READY
            self._terrain_ready[key] = terrain_result
            self._deco_ready[key] = deco_result

    def shutdown(self) -> None:
        self._clear_all_jobs()
        self.coordinator.bump_epoch()
        shutdown_parallel_pool()
        self._pool = None

    # Legacy M24a — monolithischer poll für Tests die ChunkGenResult erwarten
    def poll_ready(self) -> list:
        from game_core.world_gen_result import ChunkGenResult

        results: list[ChunkGenResult] = []
        for terrain in self.poll_terrain_ready():
            for deco in self.poll_deco_ready():
                if deco.build_key == terrain.build_key:
                    from game_core.chunk_stage import deco_result_to_chunk_gen

                    results.append(deco_result_to_chunk_gen(terrain, deco))
                    self.consume_terrain(terrain.build_key)
                    self.consume_deco(deco.build_key)
                    break
        return results

    def submit(self, coords: Iterable[tuple[int, int]]) -> None:
        from game_core.streaming_config import load_streaming_config

        cfg = load_streaming_config()
        self.submit_terrain(
            coords,
            max_in_flight=cfg.terrain_max_in_flight,
            parallelism_cap=cfg.terrain_parallelism_cap,
        )

    def discard(self, coords: Iterable[tuple[int, int]]) -> None:
        coord_set = set(coords)
        stale_t = [k for k in self._terrain_states if k.coord in coord_set]
        stale_d = [k for k in self._deco_states if k.coord in coord_set]
        if stale_t:
            self.discard_terrain(stale_t)
        if stale_d:
            self.discard_deco(stale_d)
