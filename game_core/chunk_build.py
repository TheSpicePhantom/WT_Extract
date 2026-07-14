"""M24b — BuildKey, BuildCoordinator, ChunkBuildState (Pipeline-Vertrag)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass(frozen=True, slots=True)
class BuildKey:
    coord: tuple[int, int]
    terrain_revision: int
    terrain_config_version: int
    deco_config_version: int
    build_epoch: int


class TerrainState(Enum):
    EMPTY = auto()
    IN_FLIGHT = auto()
    APPLIED = auto()


class DecoState(Enum):
    NONE = auto()
    IN_FLIGHT = auto()
    APPLIED = auto()
    SUPPRESSED = auto()


@dataclass
class ChunkBuildState:
    terrain_build_key: BuildKey | None = None
    terrain_state: TerrainState = TerrainState.EMPTY
    deco_state: DecoState = DecoState.NONE
    last_applied_deco_build_key: BuildKey | None = None
    deco_suppression_reason: str | None = None
    deco_incomplete: bool = False
    pending_terrain_build_key: BuildKey | None = None


def terrain_config_version() -> int:
    from game_core.world_gen import get_world_gen_config, worker_pool_signature

    return hash(worker_pool_signature(get_world_gen_config())) & 0x7FFFFFFF


def deco_config_version() -> int:
    from game_core.deco_generation import get_deco_config_version

    return get_deco_config_version()


class BuildCoordinator:
    """Einzige Schreibquelle für build_epoch und terrain_revision bei Submit."""

    def __init__(self) -> None:
        self.build_epoch: int = 0
        self._terrain_revision: dict[tuple[int, int], int] = {}
        self._pending_keys: dict[tuple[int, int], BuildKey] = {}

    def read_build_epoch(self) -> int:
        return self.build_epoch

    def bump_epoch(self) -> None:
        self.build_epoch += 1
        self._terrain_revision.clear()
        self._pending_keys.clear()

    def next_terrain_build_key(self, coord: tuple[int, int]) -> BuildKey:
        current = self._terrain_revision.get(coord, 0)
        revision = current + 1
        self._terrain_revision[coord] = revision
        key = BuildKey(
            coord=coord,
            terrain_revision=revision,
            terrain_config_version=terrain_config_version(),
            deco_config_version=deco_config_version(),
            build_epoch=self.build_epoch,
        )
        self._pending_keys[coord] = key
        return key

    def pending_terrain_build_key(self, coord: tuple[int, int]) -> BuildKey | None:
        return self._pending_keys.get(coord)

    def register_terrain_applied(self, build_key: BuildKey) -> None:
        self._pending_keys.pop(build_key.coord, None)

    def current_terrain_revision(self, coord: tuple[int, int]) -> int:
        return self._terrain_revision.get(coord, 0)

    def deco_build_key_for(self, terrain_key: BuildKey) -> BuildKey:
        return terrain_key


@dataclass
class ChunkBuildTracker:
    """Streamer-intern: Build-State pro Coord."""

    _states: dict[tuple[int, int], ChunkBuildState] = field(default_factory=dict)

    def get(self, coord: tuple[int, int]) -> ChunkBuildState:
        if coord not in self._states:
            self._states[coord] = ChunkBuildState()
        return self._states[coord]

    def pop(self, coord: tuple[int, int]) -> None:
        self._states.pop(coord, None)

    def items(self):
        return self._states.items()
