"""Sparse Terrain-/Overlay-Deltas (M23a)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from game_core.persistenz import (
    PersistenzFlags,
    ProceduralSuppression,
    TileOverride,
    is_persistenz_relevant,
)
from game_core.world import (
    CHUNK_SIZE_TILES,
    Chunk,
    EMPTY_OVERLAY_KEY,
    OVERLAY_LAYER_ID,
    copy_chunk,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OVERLAY_DELTA_SCHEMA_VERSION = 0


@dataclass(frozen=True, slots=True)
class TerrainDelta:
    """Sparse Abweichung von der deterministischen Baseline."""

    coord: tuple[int, int]
    tile_overrides: tuple[TileOverride, ...] = ()
    suppressions: tuple[ProceduralSuppression, ...] = ()


@dataclass(frozen=True, slots=True)
class OverlayDelta:
    """Vorbereiteter Schema-Slot — keine Daten in M23a."""

    coord: tuple[int, int]
    schema_version: int = OVERLAY_DELTA_SCHEMA_VERSION


def compute_terrain_delta(
    snapshot: Chunk,
    flags: PersistenzFlags,
    *,
    tile_overrides: tuple[TileOverride, ...] = (),
    suppressions: tuple[ProceduralSuppression, ...] = (),
    existing: TerrainDelta | None = None,
) -> TerrainDelta | None:
    """Baut Terrain-Delta aus PersistenzFlags + eager Tracking — kein Baseline-Vergleich."""
    if not is_persistenz_relevant(flags):
        return None

    merged_tiles: dict[tuple[int, int, int], str] = {}
    merged_suppressions: dict[tuple[int, int], ProceduralSuppression] = {}

    if existing is not None:
        for override in existing.tile_overrides:
            merged_tiles[(override.layer, override.local_tx, override.local_ty)] = override.tile_key
        for item in existing.suppressions:
            merged_suppressions[(item.wx, item.wy)] = item

    if flags & PersistenzFlags.TILE_MODIFIED:
        for override in tile_overrides:
            merged_tiles[(override.layer, override.local_tx, override.local_ty)] = override.tile_key

    if flags & PersistenzFlags.SUPPRESSION:
        for item in suppressions:
            merged_suppressions[(item.wx, item.wy)] = item

    if not merged_tiles and not merged_suppressions and not (flags & PersistenzFlags.USER_DECO_IN_BOUNDS):
        if flags & PersistenzFlags.HAS_EXISTING_DELTA and existing is not None:
            return existing
        if flags & PersistenzFlags.USER_DECO_IN_BOUNDS:
            return TerrainDelta(coord=snapshot.coord)
        return None

    ordered_tiles = tuple(
        TileOverride(layer=layer, local_tx=tx, local_ty=ty, tile_key=key)
        for (layer, tx, ty), key in sorted(merged_tiles.items())
    )
    ordered_suppressions = tuple(sorted(merged_suppressions.values(), key=lambda s: (s.wx, s.wy)))
    return TerrainDelta(
        coord=snapshot.coord,
        tile_overrides=ordered_tiles,
        suppressions=ordered_suppressions,
    )


def apply_terrain_delta(baseline: Chunk, delta: TerrainDelta) -> Chunk:
    """Wendet sparse Tile-Overrides auf Baseline-Chunk an."""
    result = copy_chunk(baseline)
    for override in delta.tile_overrides:
        if override.layer not in result.layer_keys:
            if override.layer == OVERLAY_LAYER_ID:
                result.layer_keys[override.layer] = [EMPTY_OVERLAY_KEY] * (
                    CHUNK_SIZE_TILES * CHUNK_SIZE_TILES
                )
            else:
                raise ValueError(f"Unknown layer {override.layer} in delta for {delta.coord}")
        result.set_key(override.local_tx, override.local_ty, override.tile_key, override.layer)
    return result


def terrain_delta_to_dict(delta: TerrainDelta) -> dict:
    return {
        "coord": list(delta.coord),
        "tile_overrides": [
            {
                "layer": item.layer,
                "local_tx": item.local_tx,
                "local_ty": item.local_ty,
                "tile_key": item.tile_key,
            }
            for item in delta.tile_overrides
        ],
        "suppressions": [
            {
                "wx": item.wx,
                "wy": item.wy,
                "decoration_id": item.decoration_id,
            }
            for item in delta.suppressions
        ],
    }


def terrain_delta_from_dict(data: dict) -> TerrainDelta:
    coord_raw = data["coord"]
    coord = (int(coord_raw[0]), int(coord_raw[1]))
    tile_overrides = tuple(
        TileOverride(
            layer=int(entry["layer"]),
            local_tx=int(entry["local_tx"]),
            local_ty=int(entry["local_ty"]),
            tile_key=str(entry["tile_key"]),
        )
        for entry in data.get("tile_overrides", [])
    )
    suppressions = tuple(
        ProceduralSuppression(
            wx=int(entry["wx"]),
            wy=int(entry["wy"]),
            decoration_id=str(entry["decoration_id"]),
        )
        for entry in data.get("suppressions", [])
    )
    return TerrainDelta(coord=coord, tile_overrides=tile_overrides, suppressions=suppressions)


def compute_world_gen_fingerprint() -> str:
    """Stabiler Hash über relevante World-Gen-Config-Dateien."""
    hasher = hashlib.sha256()
    for relative in (
        "assets/content/world_gen.json",
        "assets/content/biomes.json",
        "assets/content/tiles.json",
    ):
        path = PROJECT_ROOT / relative
        if path.is_file():
            hasher.update(relative.encode("utf-8"))
            hasher.update(path.read_bytes())
    return hasher.hexdigest()
