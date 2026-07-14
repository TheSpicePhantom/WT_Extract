"""M24c — optionale Sub-Timings für Terrain-Worldgen (Phase 0 Instrumentation)."""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterator

_ENABLED_ENV = "WT_TERRAIN_PROFILE"

_active: TerrainGenProfile | None = None


@dataclass
class TerrainGenProfile:
    sections: dict[str, float] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)
    field_cache_builds: int = 0

    def add_ms(self, name: str, delta_ms: float) -> None:
        self.sections[name] = self.sections.get(name, 0.0) + delta_ms

    def inc(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def total_ms(self) -> float:
        return sum(self.sections.values())

    def breakdown_pct(self) -> dict[str, float]:
        total = self.total_ms()
        if total <= 0.0:
            return {name: 0.0 for name in self.sections}
        return {name: (ms / total) * 100.0 for name, ms in self.sections.items()}

    def to_dict(self) -> dict:
        total = self.total_ms()
        return {
            "sections_ms": {k: round(v, 3) for k, v in sorted(self.sections.items())},
            "breakdown_pct": {k: round(v, 2) for k, v in sorted(self.breakdown_pct().items())},
            "counters": dict(sorted(self.counters.items())),
            "field_cache_builds": self.field_cache_builds,
            "total_ms": round(total, 3),
        }


def is_enabled() -> bool:
    if _active is not None:
        return True
    return os.environ.get(_ENABLED_ENV, "").strip() in ("1", "true", "yes")


def get_active() -> TerrainGenProfile | None:
    return _active


def begin_profile() -> TerrainGenProfile:
    global _active
    profile = TerrainGenProfile()
    _active = profile
    return profile


def end_profile() -> TerrainGenProfile | None:
    global _active
    profile = _active
    _active = None
    return profile


@contextmanager
def profile_section(name: str) -> Iterator[None]:
    if not is_enabled():
        yield
        return
    profile = _active
    if profile is None:
        yield
        return
    start = time.perf_counter()
    try:
        yield
    finally:
        profile.add_ms(name, (time.perf_counter() - start) * 1000.0)


def record_counter(name: str, amount: int = 1) -> None:
    if not is_enabled() or _active is None:
        return
    _active.inc(name, amount)


def record_field_cache_build() -> None:
    if not is_enabled() or _active is None:
        return
    _active.field_cache_builds += 1
    _active.inc("field_cache_build_calls")
