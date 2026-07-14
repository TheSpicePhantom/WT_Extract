"""PersistenzFlags und eager Tracking-Typen (M23a)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag


class PersistenzFlags(IntFlag):
    """Eager persistenzrelevante Änderungen — unabhängig von RuntimeDirty."""

    NONE = 0
    TILE_MODIFIED = 1
    HAS_EXISTING_DELTA = 2
    USER_DECO_IN_BOUNDS = 4
    SUPPRESSION = 8


def is_persistenz_relevant(flags: PersistenzFlags) -> bool:
    return flags != PersistenzFlags.NONE


@dataclass(frozen=True, slots=True)
class TileOverride:
    layer: int
    local_tx: int
    local_ty: int
    tile_key: str


@dataclass(frozen=True, slots=True)
class ProceduralSuppression:
    wx: int
    wy: int
    decoration_id: str
