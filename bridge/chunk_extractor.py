"""Extrahiert sichtbare TileChunkRenderData aus game_core/World."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Literal

from bridge.sprite_resolve import resolve_sprite
from bridge.visibility import visible_chunk_coords, visible_tile_range_in_chunk
from game_core.perf.models import ExtractStepMetrics
from game_core.visibility_lod_config import (
    LOD0,
    LOD1,
    LOD2,
    VisibilityLodConfig,
    load_visibility_lod_config,
    resolve_lod_level,
)
from game_core.world import (
    CHUNK_SIZE_PX,
    CHUNK_SIZE_TILES,
    EMPTY_OVERLAY_KEY,
    OVERLAY_LAYER_ID,
    Chunk,
    World,
)
from render_scene.handles import LayerId, MaterialHandle
from render_scene.sprite_catalog import SpriteCatalog
from render_scene.types import (
    TILE_SIZE_PX,
    CameraData,
    RenderFrame,
    SpriteInstanceData,
    TileChunkRenderData,
    TileLayerBatch,
)

BatchRegistryKey = tuple[tuple[int, int], int, int]
CullCacheKey = tuple[tuple[int, int], int, int, tuple[int, int, int, int]]
ExtractMode = Literal["batch", "per_chunk"]
LodMode = Literal["auto", "detail_only"]


@dataclass
class ChunkRenderExtractor:
    """RenderExtractor-Implementierung — World + Kamera → RenderFrame."""

    world: World
    catalog: SpriteCatalog
    padding_chunks: int = 1
    extract_mode: ExtractMode = "batch"
    lod_mode: LodMode = "auto"
    lod_config: VisibilityLodConfig | None = None
    _sprite_cache: dict[str, int] = field(default_factory=dict, repr=False)
    _batch_registry: dict[BatchRegistryKey, TileLayerBatch] = field(default_factory=dict, repr=False)
    _registry_empty: set[BatchRegistryKey] = field(default_factory=set, repr=False)
    _cull_cache: dict[CullCacheKey, TileLayerBatch] = field(default_factory=dict, repr=False)
    _materials_by_count: dict[int, tuple[MaterialHandle, ...]] = field(default_factory=dict, repr=False)
    _tile_cache_legacy: dict[tuple[int, int], TileChunkRenderData] = field(default_factory=dict, repr=False)
    _last_lod_level: int | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.lod_config is None:
            self.lod_config = load_visibility_lod_config()

    def set_world(self, world: World) -> None:
        """Welt ersetzen — Tile-Cache leeren (z. B. nach Load)."""
        self.world = world
        self.invalidate_all()

    def invalidate_all(self) -> None:
        """Gesamten Batch-Registry-, LOD- und Cull-Cache leeren."""
        self._batch_registry.clear()
        self._registry_empty.clear()
        self._cull_cache.clear()
        self._tile_cache_legacy.clear()
        self._last_lod_level = None

    def invalidate(self, coord: tuple[int, int]) -> None:
        """Einzelnen Chunk aus Registry und Cull-Cache entfernen (M18 Streaming)."""
        self._purge_coord(coord)
        self._tile_cache_legacy.pop(coord, None)

    def extract(
        self,
        camera: CameraData,
        sprites: tuple[SpriteInstanceData, ...] = (),
        clear_color: tuple[float, float, float, float] = (0.10, 0.11, 0.14, 1.0),
        step_metrics: ExtractStepMetrics | None = None,
    ) -> RenderFrame:
        if self.extract_mode == "per_chunk":
            tile_chunks = self._extract_per_chunk_legacy(camera, step_metrics)
        else:
            tile_chunks = self._extract_batching(camera, step_metrics)

        return RenderFrame(
            camera=camera,
            tile_chunks=tuple(tile_chunks),
            sprites=sprites,
            clear_color=clear_color,
        )

    def _resolve_active_lod(self, zoom: float, step_metrics: ExtractStepMetrics | None) -> int:
        assert self.lod_config is not None
        if self.lod_mode == "detail_only":
            lod_level = LOD0
        else:
            lod_level = resolve_lod_level(zoom, self.lod_config)

        if step_metrics is not None:
            step_metrics.tile_map_mode_active = (
                1 if self.lod_config.lod_enabled and self.lod_config.map_mode else 0
            )
            if self._last_lod_level is not None and self._last_lod_level != lod_level:
                step_metrics.tile_lod_switches += 1
        self._last_lod_level = lod_level
        return lod_level

    def _extract_batching(
        self,
        camera: CameraData,
        step_metrics: ExtractStepMetrics | None,
    ) -> list[TileChunkRenderData]:
        coords = visible_chunk_coords(camera, self.world, self.padding_chunks)
        tile_chunks: list[TileChunkRenderData] = []
        profile = step_metrics is not None
        lod_level = self._resolve_active_lod(camera.zoom, step_metrics)

        for coord in coords:
            chunk = self.world.chunks.get(coord)
            if chunk is None:
                continue

            if profile:
                step_metrics.tile_visible_chunks += 1

            tile_range = visible_tile_range_in_chunk(coord, camera)
            if tile_range is None:
                continue

            dirty_layers = self._dirty_layers_for(coord)
            if dirty_layers is None:
                self._purge_coord(coord)
            elif dirty_layers:
                self._purge_coord(coord, dirty_layers)

            if profile:
                t_assemble = time.perf_counter()

            layer_batches: list[TileLayerBatch] = []
            chunk_rebuilt = False
            for layer_id in chunk.layer_ids():
                reg_key: BatchRegistryKey = (coord, layer_id, lod_level)
                need_rebuild = (
                    dirty_layers is None
                    or layer_id in dirty_layers
                    or (
                        reg_key not in self._batch_registry
                        and reg_key not in self._registry_empty
                    )
                )
                if need_rebuild:
                    if profile:
                        t_rebuild = time.perf_counter()
                    batch = self._build_layer_batch_for_lod(chunk, layer_id, lod_level)
                    if profile:
                        step_metrics.tile_full_rebuild_ms += (time.perf_counter() - t_rebuild) * 1000.0
                        step_metrics.tile_registry_misses += 1
                    if batch is not None:
                        self._batch_registry[reg_key] = batch
                        self._registry_empty.discard(reg_key)
                    else:
                        self._batch_registry.pop(reg_key, None)
                        self._registry_empty.add(reg_key)
                    chunk_rebuilt = True
                elif profile:
                    step_metrics.tile_registry_hits += 1

                if reg_key in self._registry_empty:
                    continue

                full_batch = self._batch_registry.get(reg_key)
                if full_batch is None:
                    continue

                culled = self._get_culled_batch(
                    coord, layer_id, lod_level, full_batch, tile_range, step_metrics
                )
                if culled is not None:
                    layer_batches.append(culled)
                    if profile:
                        step_metrics.tile_visible_batches += 1
                        if lod_level == LOD0:
                            step_metrics.tile_lod0_groups += 1
                        elif lod_level == LOD1:
                            step_metrics.tile_lod1_groups += 1
                        else:
                            step_metrics.tile_lod2_groups += 1

            if profile:
                assemble_ms = (time.perf_counter() - t_assemble) * 1000.0
                step_metrics.tile_assemble_ms += assemble_ms
                if lod_level == LOD0:
                    step_metrics.tile_lod0_ms += assemble_ms
                elif lod_level == LOD1:
                    step_metrics.tile_lod1_ms += assemble_ms
                else:
                    step_metrics.tile_lod2_ms += assemble_ms
                if chunk_rebuilt:
                    step_metrics.tile_cache_misses += 1
                else:
                    step_metrics.tile_cache_hits += 1

            if coord in self.world.dirty_chunks:
                self.world.clear_chunk_dirty(coord)

            if layer_batches:
                tile_chunks.append(
                    TileChunkRenderData(chunk_coord=coord, layers=tuple(layer_batches))
                )

        return tile_chunks

    def _extract_per_chunk_legacy(
        self,
        camera: CameraData,
        step_metrics: ExtractStepMetrics | None,
    ) -> list[TileChunkRenderData]:
        """Legacy Detailpfad — nur Tests (`extract_mode='per_chunk'`)."""
        coords = visible_chunk_coords(camera, self.world, self.padding_chunks)
        tile_chunks: list[TileChunkRenderData] = []
        profile = step_metrics is not None
        for coord in coords:
            chunk = self.world.chunks.get(coord)
            if chunk is None:
                continue

            if profile:
                step_metrics.tile_visible_chunks += 1

            if coord not in self.world.dirty_chunks and coord in self._tile_cache_legacy:
                if profile:
                    step_metrics.tile_cache_hits += 1
                    t_cull = time.perf_counter()
                chunk_data = self._cull_chunk_to_camera(self._tile_cache_legacy[coord], camera)
                if profile:
                    step_metrics.tile_cull_ms += (time.perf_counter() - t_cull) * 1000.0
            else:
                if profile:
                    step_metrics.tile_cache_misses += 1
                    t_rebuild = time.perf_counter()
                full_data = self._extract_full_chunk(chunk)
                if profile:
                    step_metrics.tile_full_rebuild_ms += (time.perf_counter() - t_rebuild) * 1000.0
                if full_data is not None:
                    self._tile_cache_legacy[coord] = full_data
                else:
                    self._tile_cache_legacy.pop(coord, None)
                self.world.clear_chunk_dirty(coord)
                if profile:
                    t_cull = time.perf_counter()
                chunk_data = self._cull_chunk_to_camera(full_data, camera) if full_data else None
                if profile:
                    step_metrics.tile_cull_ms += (time.perf_counter() - t_cull) * 1000.0

            if chunk_data is not None:
                tile_chunks.append(chunk_data)
                if profile:
                    step_metrics.tile_visible_batches += sum(
                        1 for layer in chunk_data.layers if layer.tile_ids
                    )
                    step_metrics.tile_lod0_groups += sum(
                        1 for layer in chunk_data.layers if layer.tile_ids
                    )

        return tile_chunks

    def _dirty_layers_for(self, coord: tuple[int, int]) -> set[int] | None:
        """None = alle Layer dirty; leeres Set = nicht dirty."""
        if coord not in self.world.dirty_chunks:
            return set()
        layers = self.world.dirty_chunk_layers.get(coord)
        if layers:
            return set(layers)
        return None

    def _purge_coord(self, coord: tuple[int, int], layer_ids: set[int] | None = None) -> None:
        if layer_ids is None:
            keys_to_remove = [key for key in self._batch_registry if key[0] == coord]
            for key in keys_to_remove:
                del self._batch_registry[key]
            empty_to_remove = [key for key in self._registry_empty if key[0] == coord]
            for key in empty_to_remove:
                self._registry_empty.discard(key)
            cull_to_remove = [key for key in self._cull_cache if key[0] == coord]
            for key in cull_to_remove:
                del self._cull_cache[key]
            return

        for layer_id in layer_ids:
            for lod_level in (LOD0, LOD1, LOD2):
                reg_key = (coord, layer_id, lod_level)
                self._batch_registry.pop(reg_key, None)
                self._registry_empty.discard(reg_key)
                cull_to_remove = [
                    key
                    for key in self._cull_cache
                    if key[0] == coord and key[1] == layer_id and key[2] == lod_level
                ]
                for key in cull_to_remove:
                    del self._cull_cache[key]

    def _get_culled_batch(
        self,
        coord: tuple[int, int],
        layer_id: int,
        lod_level: int,
        full_batch: TileLayerBatch,
        tile_range: tuple[int, int, int, int],
        step_metrics: ExtractStepMetrics | None,
    ) -> TileLayerBatch | None:
        cull_key: CullCacheKey = (coord, layer_id, lod_level, tile_range)
        cached = self._cull_cache.get(cull_key)
        if cached is not None:
            if step_metrics is not None:
                step_metrics.tile_cull_cache_hits += 1
            return cached

        if step_metrics is not None:
            t_cull = time.perf_counter()
            step_metrics.tile_cull_cache_misses += 1
        culled = self._cull_layer_batch(full_batch, coord, tile_range)
        if step_metrics is not None:
            step_metrics.tile_cull_ms += (time.perf_counter() - t_cull) * 1000.0
        if culled is not None:
            self._cull_cache[cull_key] = culled
        return culled

    def _resolve_key(self, key: str) -> int:
        cached = self._sprite_cache.get(key)
        if cached is not None:
            return cached
        sprite_id = int(resolve_sprite(self.catalog, key))
        self._sprite_cache[key] = sprite_id
        return sprite_id

    def _materials_for(self, count: int) -> tuple[MaterialHandle, ...]:
        cached = self._materials_by_count.get(count)
        if cached is None:
            cached = tuple(MaterialHandle(1) for _ in range(count))
            self._materials_by_count[count] = cached
        return cached

    def _build_layer_batch_for_lod(
        self, chunk: Chunk, layer_id: int, lod_level: int
    ) -> TileLayerBatch | None:
        if lod_level == LOD0:
            return self._build_full_layer_batch(chunk, layer_id)
        if lod_level == LOD1:
            return self._build_lod1_layer_batch(chunk, layer_id)
        return self._build_lod2_layer_batch(chunk, layer_id)

    def _build_full_layer_batch(self, chunk: Chunk, layer_id: int) -> TileLayerBatch | None:
        cx, cy = chunk.coord
        chunk_origin_x = cx * CHUNK_SIZE_PX
        chunk_origin_y = cy * CHUNK_SIZE_PX
        keys = chunk.layer_keys[layer_id]
        is_overlay = layer_id == OVERLAY_LAYER_ID

        tile_ids: list[int] = []
        world_x: list[float] = []
        world_y: list[float] = []

        for ty in range(CHUNK_SIZE_TILES):
            wy = chunk_origin_y + ty * TILE_SIZE_PX
            row_base = ty * CHUNK_SIZE_TILES
            for tx in range(CHUNK_SIZE_TILES):
                key = keys[row_base + tx]
                if is_overlay and key == EMPTY_OVERLAY_KEY:
                    continue
                tile_ids.append(self._resolve_key(key))
                world_x.append(chunk_origin_x + tx * TILE_SIZE_PX)
                world_y.append(wy)

        count = len(tile_ids)
        if count == 0:
            return None

        return TileLayerBatch(
            layer=LayerId(layer_id),
            tile_ids=tuple(tile_ids),
            world_x=tuple(world_x),
            world_y=tuple(world_y),
            materials=self._materials_for(count),
        )

    def _build_lod1_layer_batch(self, chunk: Chunk, layer_id: int) -> TileLayerBatch | None:
        """LOD1 — 2×2-Subsample (Schritt 2), chunkgebunden."""
        cx, cy = chunk.coord
        chunk_origin_x = cx * CHUNK_SIZE_PX
        chunk_origin_y = cy * CHUNK_SIZE_PX
        keys = chunk.layer_keys[layer_id]
        is_overlay = layer_id == OVERLAY_LAYER_ID

        tile_ids: list[int] = []
        world_x: list[float] = []
        world_y: list[float] = []

        for ty in range(0, CHUNK_SIZE_TILES, 2):
            wy = chunk_origin_y + ty * TILE_SIZE_PX
            row_base = ty * CHUNK_SIZE_TILES
            for tx in range(0, CHUNK_SIZE_TILES, 2):
                key = keys[row_base + tx]
                if is_overlay and key == EMPTY_OVERLAY_KEY:
                    continue
                tile_ids.append(self._resolve_key(key))
                world_x.append(chunk_origin_x + tx * TILE_SIZE_PX)
                world_y.append(wy)

        count = len(tile_ids)
        if count == 0:
            return None

        return TileLayerBatch(
            layer=LayerId(layer_id),
            tile_ids=tuple(tile_ids),
            world_x=tuple(world_x),
            world_y=tuple(world_y),
            materials=self._materials_for(count),
        )

    def _build_lod2_layer_batch(self, chunk: Chunk, layer_id: int) -> TileLayerBatch | None:
        """LOD2 — dominantes Tile pro Chunk-Layer (Map-Mode / Overview)."""
        cx, cy = chunk.coord
        chunk_origin_x = cx * CHUNK_SIZE_PX
        chunk_origin_y = cy * CHUNK_SIZE_PX
        keys = chunk.layer_keys[layer_id]
        is_overlay = layer_id == OVERLAY_LAYER_ID

        counts: dict[str, int] = {}
        for ty in range(CHUNK_SIZE_TILES):
            row_base = ty * CHUNK_SIZE_TILES
            for tx in range(CHUNK_SIZE_TILES):
                key = keys[row_base + tx]
                if is_overlay and key == EMPTY_OVERLAY_KEY:
                    continue
                counts[key] = counts.get(key, 0) + 1

        if not counts:
            return None

        dominant_key = max(counts.items(), key=lambda item: (item[1], item[0]))[0]
        center_tx = CHUNK_SIZE_TILES // 2
        center_ty = CHUNK_SIZE_TILES // 2

        return TileLayerBatch(
            layer=LayerId(layer_id),
            tile_ids=(self._resolve_key(dominant_key),),
            world_x=(chunk_origin_x + center_tx * TILE_SIZE_PX,),
            world_y=(chunk_origin_y + center_ty * TILE_SIZE_PX,),
            materials=self._materials_for(1),
        )

    def _extract_full_chunk(self, chunk: Chunk) -> TileChunkRenderData | None:
        """Voller 8×8-Chunk — Legacy/Test-Pfad."""
        batches: list[TileLayerBatch] = []
        for layer_id in chunk.layer_ids():
            batch = self._build_full_layer_batch(chunk, layer_id)
            if batch is not None:
                batches.append(batch)
        if not batches:
            return None
        return TileChunkRenderData(chunk_coord=chunk.coord, layers=tuple(batches))

    def _cull_layer_batch(
        self,
        batch: TileLayerBatch,
        chunk_coord: tuple[int, int],
        tile_range: tuple[int, int, int, int],
    ) -> TileLayerBatch | None:
        tx_min, tx_max, ty_min, ty_max = tile_range
        cx, cy = chunk_coord
        chunk_origin_x = cx * CHUNK_SIZE_PX
        chunk_origin_y = cy * CHUNK_SIZE_PX
        inv_tile = 1.0 / TILE_SIZE_PX

        tile_ids: list[int] = []
        world_x: list[float] = []
        world_y: list[float] = []

        for tile_id, wx, wy in zip(batch.tile_ids, batch.world_x, batch.world_y, strict=True):
            tx = int((wx - chunk_origin_x) * inv_tile + 0.5)
            ty = int((wy - chunk_origin_y) * inv_tile + 0.5)
            if tx_min <= tx <= tx_max and ty_min <= ty <= ty_max:
                tile_ids.append(int(tile_id))
                world_x.append(wx)
                world_y.append(wy)

        count = len(tile_ids)
        if count == 0:
            return None

        return TileLayerBatch(
            layer=batch.layer,
            tile_ids=tuple(tile_ids),
            world_x=tuple(world_x),
            world_y=tuple(world_y),
            materials=self._materials_for(count),
        )

    def _cull_chunk_to_camera(
        self,
        data: TileChunkRenderData | None,
        camera: CameraData,
    ) -> TileChunkRenderData | None:
        """View-Culling auf gecachtem Voll-Chunk — Legacy/Test-Pfad."""
        if data is None:
            return None

        tile_range = visible_tile_range_in_chunk(data.chunk_coord, camera)
        if tile_range is None:
            return None

        batches: list[TileLayerBatch] = []
        for layer in data.layers:
            batch = self._cull_layer_batch(layer, data.chunk_coord, tile_range)
            if batch is not None:
                batches.append(batch)

        if not batches:
            return None
        return TileChunkRenderData(chunk_coord=data.chunk_coord, layers=tuple(batches))
