"""Pending-Unload-Queue — Runtime-Übergangszustand (M23a)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from game_core.persistenz import PersistenzFlags
from game_core.world import Chunk


@dataclass(frozen=True, slots=True)
class PendingUnloadEntry:
    coord: tuple[int, int]
    snapshot: Chunk
    persistenz_flags: PersistenzFlags
    deco_incomplete: bool = False


@dataclass
class DrainResult:
    drained: int = 0
    discarded: int = 0
    persisted: int = 0
    ms_elapsed: float = 0.0
    budget_exhausted: bool = False


@dataclass
class PendingUnloadQueue:
    """FIFO-Queue für deferred unload — eine Koordinate höchstens einmal pending."""

    _entries: dict[tuple[int, int], PendingUnloadEntry] = field(default_factory=dict)
    _order: deque[tuple[int, int]] = field(default_factory=deque)
    _draining: set[tuple[int, int]] = field(default_factory=set)

    def mark(self, entry: PendingUnloadEntry) -> None:
        if entry.coord in self._entries or entry.coord in self._draining:
            raise ValueError(f"coord already pending unload: {entry.coord}")
        self._entries[entry.coord] = entry
        self._order.append(entry.coord)

    def revive(self, coord: tuple[int, int]) -> PendingUnloadEntry | None:
        if coord in self._draining:
            return None
        entry = self._entries.pop(coord, None)
        if entry is None:
            return None
        try:
            self._order.remove(coord)
        except ValueError:
            pass
        return entry

    def contains(self, coord: tuple[int, int]) -> bool:
        return coord in self._entries or coord in self._draining

    def is_draining(self, coord: tuple[int, int]) -> bool:
        return coord in self._draining

    def count(self) -> int:
        return len(self._entries)

    def pending_coords(self) -> frozenset[tuple[int, int]]:
        return frozenset(self._entries.keys())

    def pop_next(self) -> PendingUnloadEntry | None:
        while self._order:
            coord = self._order[0]
            entry = self._entries.get(coord)
            if entry is None:
                self._order.popleft()
                continue
            self._order.popleft()
            self._entries.pop(coord, None)
            self._draining.add(coord)
            return entry
        return None

    def finish_draining(self, coord: tuple[int, int]) -> None:
        self._draining.discard(coord)
