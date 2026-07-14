"""M24b — Bounded LRU für ChunkFieldCache (Router-owned Cleanup auf Main)."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_core.chunk_build import BuildKey
    from game_core.chunk_stage import TerrainStageData
    from game_core.world_gen import ChunkFieldCache


@dataclass
class FieldCacheMetrics:
    hits: int = 0
    misses: int = 0
    evictions: int = 0

    @property
    def live_count(self) -> int:
        return 0


@dataclass
class TerrainStageLRU:
    """Worker-LRU für vollständiges TerrainStageData (M24c.1 Deco-Fast-Path)."""

    max_entries: int
    _store: OrderedDict = field(default_factory=OrderedDict)
    metrics: FieldCacheMetrics = field(default_factory=FieldCacheMetrics)

    def get(self, key: BuildKey) -> TerrainStageData | None:
        entry = self._store.get(key)
        if entry is None:
            self.metrics.misses += 1
            return None
        self._store.move_to_end(key)
        self.metrics.hits += 1
        return entry

    def put(self, key: BuildKey, stage: TerrainStageData) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = stage
        self._evict_if_needed()

    def consume(self, key: BuildKey) -> None:
        if key in self._store:
            del self._store[key]

    def discard(self, key: BuildKey) -> None:
        if key in self._store:
            del self._store[key]

    def flush_all(self) -> None:
        self._store.clear()

    def _evict_if_needed(self) -> None:
        while len(self._store) > self.max_entries:
            self._store.popitem(last=False)
            self.metrics.evictions += 1


@dataclass
class FieldCacheLRU:
    max_entries: int
    _store: OrderedDict = field(default_factory=OrderedDict)
    metrics: FieldCacheMetrics = field(default_factory=FieldCacheMetrics)

    @property
    def live_count(self) -> int:
        return len(self._store)

    def get(self, key: BuildKey) -> ChunkFieldCache | None:
        entry = self._store.get(key)
        if entry is None:
            self.metrics.misses += 1
            return None
        self._store.move_to_end(key)
        self.metrics.hits += 1
        return entry

    def put(self, key: BuildKey, cache: ChunkFieldCache) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = cache
        self._evict_if_needed()

    def consume(self, key: BuildKey) -> None:
        if key in self._store:
            del self._store[key]

    def discard(self, key: BuildKey) -> None:
        if key in self._store:
            del self._store[key]

    def flush_all(self) -> None:
        self._store.clear()

    def _evict_if_needed(self) -> None:
        while len(self._store) > self.max_entries:
            self._store.popitem(last=False)
            self.metrics.evictions += 1


_worker_lru: FieldCacheLRU | None = None


def worker_field_cache_lru(max_entries: int = 10) -> FieldCacheLRU:
    global _worker_lru
    if _worker_lru is None:
        _worker_lru = FieldCacheLRU(max_entries=max_entries)
    return _worker_lru


_worker_terrain_lru: TerrainStageLRU | None = None


def worker_terrain_stage_lru(max_entries: int = 10) -> TerrainStageLRU:
    global _worker_terrain_lru
    if _worker_terrain_lru is None:
        _worker_terrain_lru = TerrainStageLRU(max_entries=max_entries)
    return _worker_terrain_lru


def reset_worker_field_cache_lru() -> None:
    global _worker_lru, _worker_terrain_lru
    if _worker_lru is not None:
        _worker_lru.flush_all()
    _worker_lru = None
    if _worker_terrain_lru is not None:
        _worker_terrain_lru.flush_all()
    _worker_terrain_lru = None
