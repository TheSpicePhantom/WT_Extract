"""Chunk-Welt — reine Spielzustandsdaten (wt:… Keys, keine GPU-IDs)."""

from __future__ import annotations

from dataclasses import dataclass, field

from game_core.persistenz import (
    PersistenzFlags,
    ProceduralSuppression,
    TileOverride,
    is_persistenz_relevant,
)
from game_core.decorations import PlacedDecoration
from game_core.world_coords import CHUNK_TILES, world_tile_to_chunk

TILE_SIZE_PX = 32
CHUNK_SIZE_TILES = CHUNK_TILES
CHUNK_SIZE_PX = CHUNK_SIZE_TILES * TILE_SIZE_PX
CHUNK_TILE_COUNT = CHUNK_SIZE_TILES * CHUNK_SIZE_TILES

TERRAIN_LAYER_ID = 0
OVERLAY_LAYER_ID = 1
DEFAULT_TILE_LAYERS = (TERRAIN_LAYER_ID, OVERLAY_LAYER_ID)
EMPTY_OVERLAY_KEY = ""


def tile_to_world_anchor(wx: int, wy: int) -> tuple[float, float]:
    return float(wx * TILE_SIZE_PX), float(wy * TILE_SIZE_PX)


def world_tile_to_chunk_local(wx: int, wy: int) -> tuple[tuple[int, int], int, int]:
    """Welt-Tile (wx, wy) → Chunk-Koordinate, lokales tx, ty."""
    cx, cy, tx, ty = world_tile_to_chunk(wx, wy)
    return (cx, cy), tx, ty


def chunk_local_to_world_tile(cx: int, cy: int, tx: int, ty: int) -> tuple[int, int]:
    """Chunk + lokales Tile → Welt-Tile-Index."""
    return cx * CHUNK_SIZE_TILES + tx, cy * CHUNK_SIZE_TILES + ty


def _empty_overlay_keys() -> list[str]:
    return [EMPTY_OVERLAY_KEY] * CHUNK_TILE_COUNT


@dataclass(slots=True)
class Chunk:
    """Ein Chunk — pro Layer row-major tile_keys (ty * width + tx)."""

    coord: tuple[int, int]
    layer_keys: dict[int, list[str]]
    solid_grid: bytes | None = None

    def __post_init__(self) -> None:
        if TERRAIN_LAYER_ID not in self.layer_keys:
            raise ValueError(f"Chunk {self.coord}: Layer {TERRAIN_LAYER_ID} fehlt.")
        for layer_id, keys in self.layer_keys.items():
            if isinstance(keys, tuple):
                self.layer_keys[layer_id] = list(keys)
            if len(self.layer_keys[layer_id]) != CHUNK_TILE_COUNT:
                raise ValueError(
                    f"Chunk {self.coord} Layer {layer_id}: erwartet {CHUNK_TILE_COUNT} keys, "
                    f"erhalten {len(self.layer_keys[layer_id])}."
                )
        if OVERLAY_LAYER_ID not in self.layer_keys:
            self.layer_keys[OVERLAY_LAYER_ID] = _empty_overlay_keys()

    @classmethod
    def from_terrain(
        cls,
        coord: tuple[int, int],
        terrain_keys: list[str] | tuple[str, ...],
        overlay_keys: list[str] | tuple[str, ...] | None = None,
    ) -> Chunk:
        overlay = list(overlay_keys) if overlay_keys is not None else _empty_overlay_keys()
        return cls(
            coord=coord,
            layer_keys={
                TERRAIN_LAYER_ID: list(terrain_keys),
                OVERLAY_LAYER_ID: overlay,
            },
        )

    @staticmethod
    def tile_index(tx: int, ty: int) -> int:
        return ty * CHUNK_SIZE_TILES + tx

    @property
    def tile_keys(self) -> list[str]:
        """Legacy — Terrain-Layer (0)."""
        return self.layer_keys[TERRAIN_LAYER_ID]

    def get_key(self, tx: int, ty: int, layer: int = TERRAIN_LAYER_ID) -> str:
        return self.layer_keys[layer][self.tile_index(tx, ty)]

    def set_key(self, tx: int, ty: int, key: str, layer: int = TERRAIN_LAYER_ID) -> None:
        self.layer_keys[layer][self.tile_index(tx, ty)] = key

    def layer_ids(self) -> tuple[int, ...]:
        return tuple(sorted(self.layer_keys.keys()))


def copy_chunk(chunk: Chunk) -> Chunk:
    """Deep-Copy eines Chunks ohne Solid-Grid (wird beim Load neu gebaut)."""
    return Chunk(
        coord=chunk.coord,
        layer_keys={layer_id: list(keys) for layer_id, keys in chunk.layer_keys.items()},
        solid_grid=None,
    )


@dataclass
class World:
    """Welt aus adressierbaren Chunks — Chunk-Index (cx, cy), nicht Pixel."""

    chunks: dict[tuple[int, int], Chunk] = field(default_factory=dict)
    decorations: list[PlacedDecoration] = field(default_factory=list)
    chunk_size_tiles: int = CHUNK_SIZE_TILES
    dirty_chunks: set[tuple[int, int]] = field(default_factory=set)
    dirty_chunk_layers: dict[tuple[int, int], set[int]] = field(default_factory=dict)
    collision_dirty_chunks: set[tuple[int, int]] = field(default_factory=set)
    _persistenz_flags: dict[tuple[int, int], PersistenzFlags] = field(default_factory=dict)
    _persistenz_tile_overrides: dict[tuple[int, int], list[TileOverride]] = field(
        default_factory=dict
    )
    _persistenz_suppressions: dict[tuple[int, int], list[ProceduralSuppression]] = field(
        default_factory=dict
    )
    _semantically_inactive_chunks: set[tuple[int, int]] = field(default_factory=set)

    def get_chunk(self, coord: tuple[int, int]) -> Chunk | None:
        return self.chunks.get(coord)

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)

    @property
    def dirty_count(self) -> int:
        return len(self.dirty_chunks)

    def mark_dirty(self, coord: tuple[int, int], layer_id: int | None = None) -> None:
        self.dirty_chunks.add(coord)
        if layer_id is not None:
            self.dirty_chunk_layers.setdefault(coord, set()).add(layer_id)

    def clear_chunk_dirty(self, coord: tuple[int, int]) -> None:
        self.dirty_chunks.discard(coord)
        self.dirty_chunk_layers.pop(coord, None)

    def clear_dirty(self) -> None:
        self.dirty_chunks.clear()
        self.dirty_chunk_layers.clear()

    def get_persistenz_flags(self, coord: tuple[int, int]) -> PersistenzFlags:
        return self._persistenz_flags.get(coord, PersistenzFlags.NONE)

    def mark_persistenz_flag(self, coord: tuple[int, int], flag: PersistenzFlags) -> None:
        current = self.get_persistenz_flags(coord)
        self._persistenz_flags[coord] = current | flag

    def is_persistenz_relevant(self, coord: tuple[int, int]) -> bool:
        return is_persistenz_relevant(self.get_persistenz_flags(coord))

    def record_tile_override(
        self,
        coord: tuple[int, int],
        layer: int,
        local_tx: int,
        local_ty: int,
        tile_key: str,
    ) -> None:
        overrides = self._persistenz_tile_overrides.setdefault(coord, [])
        for index, existing in enumerate(overrides):
            if (
                existing.layer == layer
                and existing.local_tx == local_tx
                and existing.local_ty == local_ty
            ):
                overrides[index] = TileOverride(layer, local_tx, local_ty, tile_key)
                return
        overrides.append(TileOverride(layer, local_tx, local_ty, tile_key))

    def get_persistenz_tile_overrides(self, coord: tuple[int, int]) -> tuple[TileOverride, ...]:
        return tuple(self._persistenz_tile_overrides.get(coord, ()))

    def record_procedural_suppression(
        self,
        coord: tuple[int, int],
        wx: int,
        wy: int,
        decoration_id: str,
    ) -> None:
        self.mark_persistenz_flag(coord, PersistenzFlags.SUPPRESSION)
        suppressions = self._persistenz_suppressions.setdefault(coord, [])
        for index, existing in enumerate(suppressions):
            if existing.wx == wx and existing.wy == wy:
                suppressions[index] = ProceduralSuppression(wx, wy, decoration_id)
                return
        suppressions.append(ProceduralSuppression(wx, wy, decoration_id))

    def get_persistenz_suppressions(self, coord: tuple[int, int]) -> tuple[ProceduralSuppression, ...]:
        return tuple(self._persistenz_suppressions.get(coord, ()))

    def clear_persistenz(self, coord: tuple[int, int]) -> None:
        self._persistenz_flags.pop(coord, None)
        self._persistenz_tile_overrides.pop(coord, None)
        self._persistenz_suppressions.pop(coord, None)

    def mark_semantically_inactive(self, coord: tuple[int, int]) -> None:
        self._semantically_inactive_chunks.add(coord)

    def mark_semantically_active(self, coord: tuple[int, int]) -> None:
        self._semantically_inactive_chunks.discard(coord)

    def is_semantically_active(self, coord: tuple[int, int]) -> bool:
        if coord not in self.chunks:
            return False
        return coord not in self._semantically_inactive_chunks

    def mark_collision_dirty(self, coord: tuple[int, int]) -> None:
        self.collision_dirty_chunks.add(coord)

    def mark_collision_dirty_for_rect(
        self,
        min_world_x: float,
        min_world_y: float,
        max_world_x: float,
        max_world_y: float,
    ) -> None:
        min_cx = int(min_world_x // CHUNK_SIZE_PX)
        min_cy = int(min_world_y // CHUNK_SIZE_PX)
        max_cx = int(max_world_x // CHUNK_SIZE_PX)
        max_cy = int(max_world_y // CHUNK_SIZE_PX)
        for cy in range(min_cy, max_cy + 1):
            for cx in range(min_cx, max_cx + 1):
                if (cx, cy) in self.chunks:
                    self.mark_collision_dirty((cx, cy))

    def rebuild_chunk_solid(self, coord: tuple[int, int], content, collision) -> None:
        from game_core.collision_grid import rebuild_chunk_solid

        chunk = self.chunks.get(coord)
        if chunk is None:
            return
        chunk.solid_grid = rebuild_chunk_solid(chunk, self, content, collision)
        self.collision_dirty_chunks.discard(coord)

    def rebuild_all_solid(self, content, collision) -> None:
        for coord in self.chunks:
            self.rebuild_chunk_solid(coord, content, collision)
        self.collision_dirty_chunks.clear()

    def ensure_collision_fresh(self, content, collision) -> None:
        while self.collision_dirty_chunks:
            coord = next(iter(self.collision_dirty_chunks))
            self.rebuild_chunk_solid(coord, content, collision)

    def ensure_collision_fresh_for_coords(
        self,
        coords: set[tuple[int, int]] | frozenset[tuple[int, int]],
        content,
        collision,
    ) -> None:
        """Rebuild nur für angegebene dirty Chunks (M24a — enger Navigation-Scope)."""
        for coord in coords:
            if coord in self.collision_dirty_chunks:
                self.rebuild_chunk_solid(coord, content, collision)

    def get_tile(self, wx: int, wy: int, layer: int = TERRAIN_LAYER_ID) -> str | None:
        """Tile-Key an Welt-Tile-Position — None wenn Chunk fehlt oder inaktiv."""
        coord, tx, ty = world_tile_to_chunk_local(wx, wy)
        if not self.is_semantically_active(coord):
            return None
        chunk = self.chunks.get(coord)
        if chunk is None:
            return None
        return chunk.get_key(tx, ty, layer)

    def set_tile(self, wx: int, wy: int, key: str, layer: int = TERRAIN_LAYER_ID) -> bool:
        """Setzt Tile-Key an Welt-Tile-Position — False wenn Chunk nicht existiert."""
        coord, tx, ty = world_tile_to_chunk_local(wx, wy)
        chunk = self.chunks.get(coord)
        if chunk is None:
            return False
        if layer not in chunk.layer_keys:
            chunk.layer_keys[layer] = _empty_overlay_keys()
        if chunk.get_key(tx, ty, layer) == key:
            return True
        chunk.set_key(tx, ty, key, layer)
        self.mark_dirty(coord, layer)
        self.mark_collision_dirty(coord)
        self.mark_persistenz_flag(coord, PersistenzFlags.TILE_MODIFIED)
        self.record_tile_override(coord, layer, tx, ty, key)
        return True

    def place_decoration(
        self,
        wx: int,
        wy: int,
        decoration_id: str,
        *,
        procedural: bool = False,
    ) -> bool:
        """Platziert Decoration an Welt-Tile — ersetzt vorhandene an gleicher Position."""
        world_x, world_y = tile_to_world_anchor(wx, wy)
        coord, _, _ = world_tile_to_chunk_local(wx, wy)
        for index, placed in enumerate(self.decorations):
            if int(placed.world_x) == world_x and int(placed.world_y) == world_y:
                if placed.decoration_id == decoration_id and placed.procedural == procedural:
                    return True
                self.decorations[index] = PlacedDecoration(
                    world_x=world_x,
                    world_y=world_y,
                    decoration_id=decoration_id,
                    procedural=procedural,
                )
                self._mark_decoration_collision_dirty(world_x, world_y)
                if not procedural:
                    self.mark_persistenz_flag(coord, PersistenzFlags.USER_DECO_IN_BOUNDS)
                return True
        self.decorations.append(
            PlacedDecoration(
                world_x=world_x,
                world_y=world_y,
                decoration_id=decoration_id,
                procedural=procedural,
            )
        )
        self._mark_decoration_collision_dirty(world_x, world_y)
        if not procedural:
            self.mark_persistenz_flag(coord, PersistenzFlags.USER_DECO_IN_BOUNDS)
        return True

    def place_decorations_batch(
        self,
        placements: list[tuple[int, int, str]],
        *,
        procedural: bool = False,
    ) -> None:
        """Batch-Deko-Platzierung — ersetzt prozedurale Deko an gleichen Tiles im Chunk."""
        for wx, wy, decoration_id in placements:
            self.place_decoration(wx, wy, decoration_id, procedural=procedural)

    def _mark_decoration_collision_dirty(self, world_x: float, world_y: float) -> None:
        self.mark_collision_dirty_for_rect(world_x, world_y, world_x + 96.0, world_y + 96.0)

    def remove_decoration_at(self, wx: int, wy: int) -> bool:
        """Entfernt Decoration an Welt-Tile — False wenn nichts vorhanden."""
        world_x, world_y = tile_to_world_anchor(wx, wy)
        coord, _, _ = world_tile_to_chunk_local(wx, wy)
        for index, placed in enumerate(self.decorations):
            if int(placed.world_x) == world_x and int(placed.world_y) == world_y:
                if placed.procedural:
                    self.record_procedural_suppression(
                        coord, wx, wy, placed.decoration_id
                    )
                elif not placed.procedural:
                    self.mark_persistenz_flag(coord, PersistenzFlags.USER_DECO_IN_BOUNDS)
                self.decorations.pop(index)
                self._mark_decoration_collision_dirty(world_x, world_y)
                return True
        return False

    def decoration_at_tile(self, wx: int, wy: int) -> PlacedDecoration | None:
        """Decoration an Welt-Tile — None wenn leer oder Chunk semantisch inaktiv."""
        coord, _, _ = world_tile_to_chunk_local(wx, wy)
        if not self.is_semantically_active(coord):
            return None
        world_x, world_y = tile_to_world_anchor(wx, wy)
        for placed in self.decorations:
            if int(placed.world_x) == world_x and int(placed.world_y) == world_y:
                return placed
        return None
