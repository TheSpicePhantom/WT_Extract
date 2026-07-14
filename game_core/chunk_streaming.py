"""Chunk-Streaming — dynamisches Laden/Entladen (hybrid viewport + radius fallback, M22d)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol

from game_core.chunk_delta import TerrainDelta, apply_terrain_delta, compute_terrain_delta
from game_core.collision_catalog import CollisionCatalog
from game_core.content_registry import ContentRegistry
from game_core.pending_unload import PendingUnloadEntry, PendingUnloadQueue
from game_core.perf.models import StreamStepMetrics
from game_core.persistenz import PersistenzFlags, is_persistenz_relevant
from game_core.world import CHUNK_SIZE_TILES, TILE_SIZE_PX, Chunk, World, copy_chunk
from game_core.chunk_build import ChunkBuildTracker, DecoState, TerrainState
from game_core.chunk_build_guards import (
    can_apply_deco_result,
    can_apply_terrain_result,
    should_suppress_deco,
    submit_deco_allowed,
    submit_terrain_allowed,
)
from game_core.chunk_gen_pool import ChunkGenPool
from game_core.chunk_stage import apply_deco_stage, apply_terrain_stage
from game_core.field_cache_lru import FieldCacheLRU
from game_core.stream_view import (
    StreamViewParams,
    chebyshev_distance,
    compute_stream_sets,
    focus_to_chunk,
)
from game_core.streaming_config import StreamingConfig, load_streaming_config
from game_core.world_gen import (
    generate_chunk,
    get_debug_mode,
    get_world_gen_config,
    populate_chunk_decorations,
    remove_procedural_decorations_in_chunk,
)
from game_core.worker_fast_path import (
    can_apply_worker_complete_fast_path,
    has_user_decorations_in_chunk,
)
from game_core.world_gen_result import (
    ChunkGenResult,
    apply_worker_complete_result,
    chunk_from_result,
)

# Re-export für Tests und Legacy-Imports.
from game_core.stream_view import coords_in_radius  # noqa: F401


class ChunkCacheInvalidator(Protocol):
    def invalidate(self, coord: tuple[int, int]) -> None: ...


@dataclass
class ChunkStreamer:
    """Lädt/entlädt Chunks — hybrid (viewport) oder radius (Tests/Legacy)."""

    config: StreamingConfig = field(default_factory=load_streaming_config)
    persistent_overrides: dict[tuple[int, int], Chunk] = field(default_factory=dict)
    persistent_deltas: dict[tuple[int, int], TerrainDelta] = field(default_factory=dict)
    pending_unload: PendingUnloadQueue = field(default_factory=PendingUnloadQueue)
    chunk_gen_pool: ChunkGenPool | None = None
    _decorated_chunks: set[tuple[int, int]] = field(default_factory=set)
    _build_tracker: ChunkBuildTracker = field(default_factory=ChunkBuildTracker)
    _main_field_cache: FieldCacheLRU | None = None

    @property
    def load_radius(self) -> int:
        return self.config.load_radius

    @property
    def unload_radius(self) -> int:
        return self.config.unload_radius

    def ensure_chunk_gen_pool(self) -> ChunkGenPool | None:
        fresh = ChunkGenPool.from_active_config()
        if fresh is None:
            self.shutdown_chunk_gen_pool()
            return None
        if self.chunk_gen_pool is None:
            self.chunk_gen_pool = fresh
        else:
            self.chunk_gen_pool.sync_active()
        return self.chunk_gen_pool

    def shutdown_chunk_gen_pool(self) -> None:
        if self.chunk_gen_pool is not None:
            self.chunk_gen_pool.shutdown()
            self.chunk_gen_pool = None
        if self._main_field_cache is not None:
            self._main_field_cache.flush_all()

    def _ensure_main_field_cache(self) -> FieldCacheLRU:
        if self._main_field_cache is None:
            cap = self.config.terrain_max_in_flight + 2
            self._main_field_cache = FieldCacheLRU(max_entries=cap)
        return self._main_field_cache

    def _sync_field_cache_metrics(self, step_metrics: StreamStepMetrics | None) -> None:
        if step_metrics is None or self._main_field_cache is None:
            return
        m = self._main_field_cache.metrics
        step_metrics.field_cache_hits = m.hits
        step_metrics.field_cache_misses = m.misses
        step_metrics.field_cache_evictions = m.evictions
        step_metrics.field_cache_live_count = self._main_field_cache.live_count

    def warmup_chunk_gen_pool(
        self,
        coord: tuple[int, int] = (-999, -999),
        timeout_s: float = 30.0,
    ) -> bool:
        """Dummy-Chunk nach Pool-Init — M24b Terrain+Deco-Pipeline vor sichtbarem Streaming."""
        from game_core.streaming_config import load_streaming_config

        pool = self.ensure_chunk_gen_pool()
        if pool is None:
            return False
        cfg = load_streaming_config()
        if cfg.pipeline_mode == "combined":
            keys = pool.submit_chunk_pipeline(
                [coord],
                max_in_flight=cfg.terrain_max_in_flight,
                parallelism_cap=cfg.terrain_parallelism_cap,
            )
            if not keys:
                return False
            build_key = keys[0]
            deadline = time.perf_counter() + timeout_s
            while time.perf_counter() < deadline:
                pool.poll_terrain_ready()
                pool.poll_deco_ready()
                if build_key in pool._terrain_ready and build_key in pool._deco_ready:
                    pool.consume_terrain(build_key)
                    pool.consume_deco(build_key)
                    return True
                if build_key not in pool._terrain_states:
                    return False
                time.sleep(0.02)
            pool.discard([coord])
            return False

        terrain_keys = pool.submit_terrain(
            [coord],
            max_in_flight=cfg.terrain_max_in_flight,
            parallelism_cap=cfg.terrain_parallelism_cap,
        )
        if not terrain_keys:
            return False
        terrain_key = terrain_keys[0]
        deadline = time.perf_counter() + timeout_s
        while time.perf_counter() < deadline:
            pool.poll_terrain_ready()
            if terrain_key in pool._terrain_ready:
                break
            if terrain_key not in pool._terrain_states:
                return False
            time.sleep(0.02)
        else:
            pool.discard([coord])
            return False

        deco_keys = pool.submit_deco(
            [terrain_key],
            max_in_flight=cfg.deco_max_in_flight,
            parallelism_cap=cfg.deco_parallelism_cap,
        )
        if not deco_keys:
            pool.discard([coord])
            return False
        deco_key = deco_keys[0]
        while time.perf_counter() < deadline:
            pool.poll_deco_ready()
            if deco_key in pool._deco_ready:
                pool.consume_terrain(terrain_key)
                pool.consume_deco(deco_key)
                return True
            if deco_key not in pool._deco_states:
                pool.discard([coord])
                return False
            time.sleep(0.02)
        pool.discard([coord])
        return False

    def clear_persistent_overrides(self) -> None:
        self.persistent_overrides.clear()
        self.persistent_deltas.clear()

    def load_persistent_overrides(self, overrides: dict[tuple[int, int], Chunk]) -> None:
        self.persistent_overrides = {
            coord: copy_chunk(chunk) for coord, chunk in overrides.items()
        }

    def load_persistent_deltas(self, deltas: dict[tuple[int, int], TerrainDelta]) -> None:
        self.persistent_deltas = dict(deltas)

    def _collect_persistenz_flags(self, world: World, coord: tuple[int, int]) -> PersistenzFlags:
        flags = world.get_persistenz_flags(coord)
        if coord in self.persistent_deltas or coord in self.persistent_overrides:
            flags |= PersistenzFlags.HAS_EXISTING_DELTA
        return flags

    def _mark_pending_unload(
        self,
        world: World,
        coord: tuple[int, int],
        extractor: ChunkCacheInvalidator,
    ) -> None:
        chunk = world.chunks.get(coord)
        if chunk is None:
            return
        flags = self._collect_persistenz_flags(world, coord)
        build_state = self._build_tracker.get(coord)
        deco_incomplete = build_state.deco_state != DecoState.APPLIED
        entry = PendingUnloadEntry(
            coord=coord,
            snapshot=copy_chunk(chunk),
            persistenz_flags=flags,
            deco_incomplete=deco_incomplete,
        )
        world.chunks.pop(coord)
        world.mark_semantically_inactive(coord)
        world.dirty_chunks.discard(coord)
        world.collision_dirty_chunks.discard(coord)
        self._decorated_chunks.discard(coord)
        extractor.invalidate(coord)
        self.pending_unload.mark(entry)
        self._build_tracker.pop(coord)

    def _revive_pending(
        self,
        world: World,
        coord: tuple[int, int],
    ) -> bool:
        entry = self.pending_unload.revive(coord)
        if entry is None:
            return False
        world.chunks[coord] = entry.snapshot
        world.mark_semantically_active(coord)
        build_state = self._build_tracker.get(coord)
        build_state.deco_incomplete = entry.deco_incomplete
        if entry.deco_incomplete:
            build_state.deco_state = DecoState.NONE
            build_state.last_applied_deco_build_key = None
        elif self._chunk_has_procedural_deco(world, coord):
            self._decorated_chunks.add(coord)
            build_state.deco_state = DecoState.APPLIED
        return True

    def _chunk_has_procedural_deco(self, world: World, coord: tuple[int, int]) -> bool:
        cx, cy = coord
        wx_min = cx * CHUNK_SIZE_TILES
        wx_max = wx_min + CHUNK_SIZE_TILES - 1
        wy_min = cy * CHUNK_SIZE_TILES
        wy_max = wy_min + CHUNK_SIZE_TILES - 1
        for placed in world.decorations:
            if not placed.procedural:
                continue
            wx = int(placed.world_x // TILE_SIZE_PX)
            wy = int(placed.world_y // TILE_SIZE_PX)
            if wx_min <= wx <= wx_max and wy_min <= wy <= wy_max:
                return True
        return False

    def _finalize_pending_entry(self, world: World, entry: PendingUnloadEntry) -> str:
        remove_procedural_decorations_in_chunk(world, entry.coord)
        if not is_persistenz_relevant(entry.persistenz_flags):
            world.clear_persistenz(entry.coord)
            return "discarded"
        existing = self.persistent_deltas.get(entry.coord)
        delta = compute_terrain_delta(
            entry.snapshot,
            entry.persistenz_flags,
            tile_overrides=world.get_persistenz_tile_overrides(entry.coord),
            suppressions=world.get_persistenz_suppressions(entry.coord),
            existing=existing,
        )
        if delta is not None:
            self.persistent_deltas[entry.coord] = delta
        world.clear_persistenz(entry.coord)
        return "persisted"

    def _drain_pending(
        self,
        world: World,
        *,
        max_count: int | None = None,
        max_ms: float = 0.0,
        skip_coords: frozenset[tuple[int, int]] | None = None,
    ) -> tuple[int, int]:
        """Finalisiert Pending-Einträge — budgetiert nach Anzahl und optional Zeit."""
        skip = skip_coords or frozenset()
        drained = 0
        discarded = 0
        deferred: list[PendingUnloadEntry] = []
        t0 = time.perf_counter()
        unlimited = max_count is not None and max_count == 0
        budget = max_count if max_count is not None else 0
        while unlimited or drained < budget:
            if max_ms > 0.0 and (time.perf_counter() - t0) * 1000.0 >= max_ms:
                break
            entry = self.pending_unload.pop_next()
            if entry is None:
                break
            if entry.coord in skip:
                deferred.append(entry)
                self.pending_unload.finish_draining(entry.coord)
                continue
            outcome = self._finalize_pending_entry(world, entry)
            if outcome == "discarded":
                discarded += 1
            drained += 1
            self.pending_unload.finish_draining(entry.coord)
        for entry in deferred:
            self.pending_unload.mark(entry)
        return drained, discarded

    def _resolve_stream_sets(
        self,
        focus_x: float,
        focus_y: float,
        view: StreamViewParams | None,
    ):
        if view is not None:
            params = view
        else:
            params = StreamViewParams(
                focus_x=focus_x,
                focus_y=focus_y,
                player_x=focus_x,
                player_y=focus_y,
                zoom=0.35,
                viewport_w=1280,
                viewport_h=720,
            )
        return compute_stream_sets(params, self.config)

    def _flush_modified_chunk(self, world: World, coord: tuple[int, int]) -> None:
        """Legacy-Pfad — wird durch deferred drain ersetzt; nur noch für flush_procedural_chunks."""
        if not world.is_persistenz_relevant(coord):
            return
        chunk = world.chunks.get(coord)
        if chunk is None:
            return
        self.persistent_overrides[coord] = copy_chunk(chunk)

    def _visible_terrain_pending(self, wanted_visible: set[tuple[int, int]]) -> int:
        count = 0
        for coord in wanted_visible:
            state = self._build_tracker.get(coord)
            if state.terrain_state != TerrainState.APPLIED:
                count += 1
        return count

    def _update_deco_suppression(self, world: World, wanted: set[tuple[int, int]], step_metrics) -> None:
        for coord in list(self._build_tracker._states.keys()):
            build_state = self._build_tracker.get(coord)
            if build_state.deco_state == DecoState.APPLIED:
                continue
            reason = should_suppress_deco(world, self, coord, wanted=coord in wanted)
            if reason is not None:
                if build_state.deco_state != DecoState.SUPPRESSED:
                    build_state.deco_state = DecoState.SUPPRESSED
                    build_state.deco_suppression_reason = reason
                    if step_metrics is not None:
                        step_metrics.deco_suppressed += 1

    def _route_pool_results(
        self,
        pool: ChunkGenPool,
        world: World,
        content: ContentRegistry,
        wanted: set[tuple[int, int]],
        *,
        budget: int,
        unlimited: bool,
        step_metrics: StreamStepMetrics | None,
    ) -> tuple[int, int]:
        """Router-owned consume/discard — Apply nur bei positivem Guard."""
        loaded = 0
        coordinator = pool.coordinator
        lru = self._ensure_main_field_cache()

        for terrain in pool.poll_terrain_ready():
            coord = terrain.coord
            build_state = self._build_tracker.get(coord)
            wanted_coord = coord in wanted
            if can_apply_terrain_result(
                world, self, terrain, build_state, coordinator, wanted=wanted_coord
            ):
                allowed, budget = self._consume_apply_budget(budget, unlimited)
                if not allowed:
                    break
                t0 = time.perf_counter() if step_metrics is not None else None
                apply_terrain_stage(world, terrain, content, build_state)
                pool.consume_terrain(terrain.build_key)
                lru.discard(terrain.build_key)
                loaded += 1
                if step_metrics is not None:
                    step_metrics.terrain_applied += 1
                    step_metrics.apply_terrain_ms += (time.perf_counter() - t0) * 1000.0
            else:
                pool.discard_terrain([terrain.build_key])
                lru.discard(terrain.build_key)
                if step_metrics is not None:
                    step_metrics.terrain_discarded_stale += 1

        for deco in pool.poll_deco_ready():
            coord = deco.coord
            build_state = self._build_tracker.get(coord)
            wanted_coord = coord in wanted
            if build_state.last_applied_deco_build_key == deco.build_key:
                pool.discard_deco([deco.build_key])
                lru.discard(deco.build_key)
                if step_metrics is not None:
                    step_metrics.deco_discarded_duplicate += 1
                continue
            if can_apply_deco_result(
                world, self, deco, build_state, coordinator, wanted=wanted_coord
            ):
                allowed, budget = self._consume_apply_budget(budget, unlimited)
                if not allowed:
                    break
                t0 = time.perf_counter() if step_metrics is not None else None
                apply_deco_stage(world, deco, content, build_state)
                pool.consume_deco(deco.build_key)
                lru.consume(deco.build_key)
                self._decorated_chunks.add(coord)
                loaded += 1
                if step_metrics is not None:
                    step_metrics.deco_applied += 1
                    step_metrics.apply_deco_ms += (time.perf_counter() - t0) * 1000.0
            else:
                if (
                    build_state.last_applied_deco_build_key is not None
                    and deco.build_key == build_state.last_applied_deco_build_key
                ):
                    if step_metrics is not None:
                        step_metrics.deco_discarded_duplicate += 1
                else:
                    if step_metrics is not None:
                        step_metrics.deco_discarded_stale += 1
                pool.discard_deco([deco.build_key])
                lru.discard(deco.build_key)

        return loaded, budget

    def _has_user_decorations_in_chunk(self, world: World, coord: tuple[int, int]) -> bool:
        return has_user_decorations_in_chunk(world, coord)

    def _should_use_worker_apply(
        self,
        world: World,
        result: ChunkGenResult,
    ) -> bool:
        config = get_world_gen_config()
        return can_apply_worker_complete_fast_path(
            world,
            self,
            result,
            worker_apply_enabled=config.parallel_worker_apply,
            debug_mode=get_debug_mode(),
        )

    def _apply_chunk_from_result(
        self,
        world: World,
        result: ChunkGenResult,
        content: ContentRegistry,
        collision: CollisionCatalog,
        *,
        step_metrics: StreamStepMetrics | None = None,
        defer_collision: bool = False,
    ) -> bool:
        """Returns True wenn Worker-Complete-Fast-Path angewendet wurde."""
        t0 = time.perf_counter() if step_metrics is not None else None
        if self._should_use_worker_apply(world, result):
            apply_worker_complete_result(world, result, content)
            self._decorated_chunks.add(result.coord)
            if step_metrics is not None:
                step_metrics.apply_worker_ms += (time.perf_counter() - t0) * 1000.0
            return True
        chunk = chunk_from_result(result, content)
        world.chunks[result.coord] = chunk
        if step_metrics is not None:
            step_metrics.apply_sync_generate_ms += (time.perf_counter() - t0) * 1000.0
        self._ensure_procedural_decorations(
            world,
            result.coord,
            content,
            collision,
            defer_collision=defer_collision,
            step_metrics=step_metrics,
        )
        return False

    def _apply_generated_chunk(
        self,
        world: World,
        coord: tuple[int, int],
        chunk: Chunk,
        content: ContentRegistry,
        collision: CollisionCatalog,
        *,
        step_metrics: StreamStepMetrics | None = None,
        defer_collision: bool = False,
    ) -> None:
        world.chunks[coord] = chunk
        self._ensure_procedural_decorations(
            world,
            coord,
            content,
            collision,
            defer_collision=defer_collision,
            step_metrics=step_metrics,
        )

    def _ensure_procedural_decorations(
        self,
        world: World,
        coord: tuple[int, int],
        content: ContentRegistry,
        collision: CollisionCatalog,
        *,
        defer_collision: bool = False,
        step_metrics: StreamStepMetrics | None = None,
    ) -> None:
        if coord not in world.chunks:
            return
        cx, cy = coord
        decorated_now = False
        if coord not in self._decorated_chunks:
            populate_chunk_decorations(world, content, cx, cy)
            self._decorated_chunks.add(coord)
            decorated_now = True
        if defer_collision:
            return
        if decorated_now or coord in world.collision_dirty_chunks:
            t0 = time.perf_counter() if step_metrics is not None else None
            world.rebuild_chunk_solid(coord, content, collision)
            if step_metrics is not None:
                step_metrics.apply_collision_ms += (time.perf_counter() - t0) * 1000.0

    def _flush_deferred_collisions(
        self,
        world: World,
        coords: list[tuple[int, int]],
        content: ContentRegistry,
        collision: CollisionCatalog,
        step_metrics: StreamStepMetrics | None = None,
    ) -> None:
        for coord in coords:
            if coord not in world.chunks:
                continue
            t0 = time.perf_counter() if step_metrics is not None else None
            world.rebuild_chunk_solid(coord, content, collision)
            if step_metrics is not None:
                step_metrics.apply_collision_ms += (time.perf_counter() - t0) * 1000.0

    def _load_chunk(
        self,
        world: World,
        coord: tuple[int, int],
        content: ContentRegistry,
        collision: CollisionCatalog,
        *,
        step_metrics: StreamStepMetrics | None = None,
        defer_collision: bool = False,
    ) -> None:
        cx, cy = coord
        t0 = time.perf_counter() if step_metrics is not None else None
        if coord in self.persistent_deltas:
            baseline = generate_chunk(cx, cy)
            world.chunks[coord] = apply_terrain_delta(baseline, self.persistent_deltas[coord])
            if step_metrics is not None:
                step_metrics.apply_delta_ms += (time.perf_counter() - t0) * 1000.0
        elif coord in self.persistent_overrides:
            world.chunks[coord] = copy_chunk(self.persistent_overrides[coord])
            if step_metrics is not None:
                step_metrics.apply_override_ms += (time.perf_counter() - t0) * 1000.0
        else:
            world.chunks[coord] = generate_chunk(cx, cy)
            if step_metrics is not None:
                step_metrics.apply_sync_generate_ms += (time.perf_counter() - t0) * 1000.0
        world.mark_semantically_active(coord)
        self._ensure_procedural_decorations(
            world,
            coord,
            content,
            collision,
            defer_collision=defer_collision,
            step_metrics=step_metrics,
        )

    def _consume_apply_budget(self, budget: int, unlimited: bool) -> tuple[bool, int]:
        if unlimited:
            return True, budget
        if budget <= 0:
            return False, budget
        return True, budget - 1

    def update(
        self,
        world: World,
        focus_x: float,
        focus_y: float,
        content: ContentRegistry,
        collision: CollisionCatalog,
        extractor: ChunkCacheInvalidator,
        view: StreamViewParams | None = None,
        step_metrics: StreamStepMetrics | None = None,
    ) -> tuple[int, int]:
        """Streaming-Schritt — Returns (loaded, unloaded)."""
        if step_metrics is not None:
            t_total = time.perf_counter()

        if step_metrics is not None:
            t_sets = time.perf_counter()
        sets = self._resolve_stream_sets(focus_x, focus_y, view)
        if step_metrics is not None:
            step_metrics.sets_ms = (time.perf_counter() - t_sets) * 1000.0

        wanted = set(sets.wanted)
        keep = set(sets.keep)
        prefetch = set(sets.prefetch)
        pool_retention = keep | prefetch

        budget = self.config.max_applies_per_frame
        unlimited = budget == 0
        sync_budget = self.config.max_sync_applies_per_frame
        focus_chunk = focus_to_chunk(focus_x, focus_y)
        loaded = 0
        deferred_collision_coords: list[tuple[int, int]] = []
        step_submitted_coords: set[tuple[int, int]] = set()

        pool = self.ensure_chunk_gen_pool()
        if pool is None and sync_budget == 0:
            sync_budget = budget

        if step_metrics is not None:
            t_apply = time.perf_counter()

        revived = 0
        for coord in sorted(wanted & self.pending_unload.pending_coords()):
            if self._revive_pending(world, coord):
                revived += 1

        if pool is not None:
            if step_metrics is not None:
                t_pool = time.perf_counter()
            pool.discard_outside(pool_retention)
            self._update_deco_suppression(world, wanted, step_metrics)
            visible_pending = self._visible_terrain_pending(wanted)
            if step_metrics is not None and visible_pending > 0:
                step_metrics.visible_terrain_wait_frames += 1

            if isinstance(pool, ChunkGenPool):
                m24b_loaded, budget = self._route_pool_results(
                    pool,
                    world,
                    content,
                    wanted,
                    budget=budget,
                    unlimited=unlimited,
                    step_metrics=step_metrics,
                )
                loaded += m24b_loaded

                terrain_submit_coords = [
                    coord
                    for coord in sorted(
                        wanted | prefetch, key=lambda c: chebyshev_distance(c, focus_chunk)
                    )
                    if coord not in world.chunks
                    and not self.pending_unload.contains(coord)
                    and coord not in self.persistent_overrides
                    and coord not in self.persistent_deltas
                ]
                terrain_room = max(
                    0, self.config.terrain_max_in_flight - pool.terrain_in_flight_count()
                )
                terrain_cap_room = max(
                    0, self.config.terrain_parallelism_cap - pool.terrain_running_count()
                )
                terrain_submit_coords = terrain_submit_coords[: min(terrain_room, terrain_cap_room)]
                filtered_terrain_coords: list[tuple[int, int]] = []
                for coord in terrain_submit_coords:
                    if step_metrics is not None:
                        step_metrics.terrain_submit_attempted += 1
                    bs = self._build_tracker.get(coord)
                    if not submit_terrain_allowed(
                        world,
                        self,
                        coord,
                        bs,
                        wanted=coord in wanted,
                        in_flight_room=pool.terrain_in_flight_count()
                        < self.config.terrain_max_in_flight,
                    ):
                        continue
                    filtered_terrain_coords.append(coord)
                terrain_submit_coords = filtered_terrain_coords
                if terrain_submit_coords:
                    if self.config.pipeline_mode == "combined":
                        keys = pool.submit_chunk_pipeline(
                            terrain_submit_coords,
                            max_in_flight=self.config.terrain_max_in_flight,
                            parallelism_cap=self.config.terrain_parallelism_cap,
                        )
                    else:
                        keys = pool.submit_terrain(
                            terrain_submit_coords,
                            max_in_flight=self.config.terrain_max_in_flight,
                            parallelism_cap=self.config.terrain_parallelism_cap,
                        )
                    for key in keys:
                        step_submitted_coords.add(key.coord)
                        bs = self._build_tracker.get(key.coord)
                        bs.pending_terrain_build_key = key
                        bs.terrain_state = TerrainState.IN_FLIGHT
                        if self.config.pipeline_mode == "combined":
                            bs.deco_state = DecoState.IN_FLIGHT
                    if step_metrics is not None:
                        step_metrics.terrain_submitted += len(keys)
                        step_metrics.terrain_submit_accepted += len(keys)

                if self.config.pipeline_mode != "combined":
                    visible_wanted_pending = self._visible_terrain_pending(wanted)
                    deco_submit_keys = []
                    for coord in sorted(wanted | prefetch, key=lambda c: chebyshev_distance(c, focus_chunk)):
                        bs = self._build_tracker.get(coord)
                        if not submit_deco_allowed(
                            world,
                            self,
                            coord,
                            bs,
                            wanted=coord in wanted,
                            in_flight_room=pool.deco_in_flight_count()
                            < self.config.deco_max_in_flight,
                            visible_terrain_pending=visible_wanted_pending
                            if self.config.deco_pause_when_visible_terrain_pending
                            else 0,
                        ):
                            if (
                                self.config.deco_pause_when_visible_terrain_pending
                                and visible_wanted_pending > 0
                                and step_metrics is not None
                            ):
                                step_metrics.deco_submit_skipped_visible_terrain_pressure += 1
                            continue
                        if bs.terrain_build_key is not None:
                            deco_submit_keys.append(bs.terrain_build_key)
                        if len(deco_submit_keys) >= self.config.deco_backfill_budget_per_frame:
                            break
                    if deco_submit_keys:
                        submitted = pool.submit_deco(
                            deco_submit_keys,
                            max_in_flight=self.config.deco_max_in_flight,
                            parallelism_cap=self.config.deco_parallelism_cap,
                        )
                        for key in submitted:
                            step_submitted_coords.add(key.coord)
                            bs = self._build_tracker.get(key.coord)
                            bs.deco_state = DecoState.IN_FLIGHT
                        if step_metrics is not None:
                            step_metrics.deco_submitted += len(submitted)

                pool.poll_terrain_ready()
                pool.poll_deco_ready()
                m24b_loaded2, budget = self._route_pool_results(
                    pool,
                    world,
                    content,
                    wanted,
                    budget=budget,
                    unlimited=unlimited,
                    step_metrics=step_metrics,
                )
                loaded += m24b_loaded2
            else:
                for result in pool.poll_ready():
                    if result.coord not in wanted or result.coord in world.chunks:
                        continue
                    if self.pending_unload.contains(result.coord):
                        continue
                    allowed, budget = self._consume_apply_budget(budget, unlimited)
                    if not allowed:
                        break
                    used_fast = self._apply_chunk_from_result(
                        world,
                        result,
                        content,
                        collision,
                        step_metrics=step_metrics,
                        defer_collision=True,
                    )
                    if not used_fast:
                        deferred_collision_coords.append(result.coord)
                    loaded += 1
                submit_coords = [
                    coord
                    for coord in sorted(
                        wanted | prefetch, key=lambda c: chebyshev_distance(c, focus_chunk)
                    )
                    if coord not in world.chunks
                    and not self.pending_unload.contains(coord)
                    and coord not in self.persistent_overrides
                    and coord not in self.persistent_deltas
                ]
                max_in_flight = self.config.max_in_flight_chunks
                if max_in_flight > 0 and submit_coords:
                    room = max(0, max_in_flight - pool.in_flight_count())
                    submit_coords = submit_coords[:room]
                if submit_coords:
                    pool.submit(submit_coords)

            self._sync_field_cache_metrics(step_metrics)
            if step_metrics is not None:
                step_metrics.apply_pool_ms += (time.perf_counter() - t_pool) * 1000.0

        for coord in sorted(wanted, key=lambda c: chebyshev_distance(c, focus_chunk)):
            if coord in world.chunks:
                continue
            if self.pending_unload.contains(coord):
                continue
            if pool is not None:
                if pool.has_pending_result(coord):
                    if step_metrics is not None:
                        step_metrics.sync_skipped_pending_result += 1
                    continue
                if coord in step_submitted_coords:
                    if step_metrics is not None:
                        step_metrics.sync_skipped_worker_submitted += 1
                    continue
                if self.config.sync_fallback_only_when_pool_disabled:
                    if pool.is_in_flight(coord):
                        age_ms = pool.in_flight_age_ms(coord)
                        if age_ms <= 0.0:
                            if step_metrics is not None:
                                step_metrics.sync_skipped_worker_submitted += 1
                            continue
                        fallback_ms = self.config.sync_fallback_in_flight_ms
                        if fallback_ms <= 0.0 or age_ms < fallback_ms:
                            if step_metrics is not None:
                                step_metrics.sync_skipped_worker_submitted += 1
                            continue
                    else:
                        if step_metrics is not None:
                            step_metrics.sync_skipped_worker_submitted += 1
                        continue
                elif pool.is_in_flight(coord):
                    age_ms = pool.in_flight_age_ms(coord)
                    if age_ms <= 0.0:
                        if step_metrics is not None:
                            step_metrics.sync_skipped_worker_submitted += 1
                        continue
                    fallback_ms = self.config.sync_fallback_in_flight_ms
                    if fallback_ms <= 0.0 or age_ms < fallback_ms:
                        if step_metrics is not None:
                            step_metrics.sync_skipped_worker_submitted += 1
                        continue
            allowed, budget = self._consume_apply_budget(budget, unlimited)
            if not allowed:
                break
            allowed_sync, sync_budget = self._consume_apply_budget(sync_budget, unlimited)
            if not allowed_sync:
                break
            if step_metrics is not None:
                step_metrics.sync_fallback_triggered += 1
            self._load_chunk(
                world,
                coord,
                content,
                collision,
                step_metrics=step_metrics,
                defer_collision=True,
            )
            deferred_collision_coords.append(coord)
            loaded += 1

        if deferred_collision_coords:
            self._flush_deferred_collisions(
                world,
                deferred_collision_coords,
                content,
                collision,
                step_metrics=step_metrics,
            )

        if pool is not None:
            pool.discard_outside(pool_retention)

        if step_metrics is not None:
            step_metrics.apply_ms = (time.perf_counter() - t_apply) * 1000.0
            t_unload = time.perf_counter()

        marked_coords: list[tuple[int, int]] = []
        for coord in list(world.chunks.keys()):
            if coord in keep:
                continue
            self._mark_pending_unload(world, coord, extractor)
            marked_coords.append(coord)

        drained, _discarded = self._drain_pending(
            world,
            max_count=self.config.max_unloads_per_frame,
            max_ms=self.config.max_unload_ms_per_frame,
            skip_coords=frozenset(marked_coords),
        )
        unloaded = drained

        if step_metrics is not None:
            step_metrics.unload_marked = len(marked_coords)
            step_metrics.pending_unload_count = self.pending_unload.count()

        if step_metrics is not None:
            step_metrics.unload_ms = (time.perf_counter() - t_unload) * 1000.0
            step_metrics.total_ms = (time.perf_counter() - t_total) * 1000.0
            step_metrics.loaded = loaded
            step_metrics.unloaded = unloaded

        return loaded, unloaded

    def overrides_for_save(self, world: World) -> dict[tuple[int, int], Chunk]:
        """Legacy v3 — aktive persistenzrelevante Chunks; v4 nutzt persistent_deltas direkt."""
        result = {coord: copy_chunk(chunk) for coord, chunk in self.persistent_overrides.items()}
        for coord, chunk in world.chunks.items():
            if coord in result:
                continue
            if world.is_persistenz_relevant(coord):
                result[coord] = copy_chunk(chunk)
        return result
