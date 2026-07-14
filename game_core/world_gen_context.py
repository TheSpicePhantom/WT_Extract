"""World-Gen-Kontext — lokaler fBM-Cache, worker-sicher (M22b/M22e)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from game_core.biomes import BiomesConfig, load_biomes_config
from game_core.world import Chunk
from game_core.tile_ids import stable_tile_id
from game_core.world_gen_result import (
    ChunkGenResult,
    procedural_to_ipc,
    validate_chunk_gen_result,
)

if TYPE_CHECKING:
    from game_core.collision_catalog import CollisionCatalog
    from game_core.world_gen import WorldGenConfig
    from game_core.worker_content_snapshot import WorkerContentSnapshot

_FBM_FIELDS = ("height", "temperature", "moisture", "continentalness", "sub_biome")


@dataclass
class WorldGenContext:
    config: WorldGenConfig
    biomes: BiomesConfig
    _fbm_cache: dict[str, object] = field(default_factory=dict)
    _worker_snapshot: WorkerContentSnapshot | None = field(default=None, repr=False)
    _worker_collision: CollisionCatalog | None = field(default=None, repr=False)
    _session_spawn_score: float | None = field(default=None, repr=False)

    def reset_chunk_build_session(self) -> None:
        """Pro Chunk-Build: spawn_score einmal berechnen (M24c)."""
        self._session_spawn_score = None

    def spawn_score(self) -> float:
        if self._session_spawn_score is None:
            from game_core.world_gen import score_spawn_area

            self._session_spawn_score = score_spawn_area(self.config)
        return self._session_spawn_score

    @classmethod
    def from_configs(
        cls,
        config: WorldGenConfig,
        biomes: BiomesConfig | None = None,
    ) -> WorldGenContext:
        return cls(config=config, biomes=biomes or load_biomes_config())

    @classmethod
    def from_active(cls) -> WorldGenContext:
        from game_core.world_gen import get_biomes_config, get_world_gen_config

        return cls.from_configs(get_world_gen_config(), get_biomes_config())

    def pool_signature(self) -> tuple:
        from game_core.world_gen import worker_pool_signature

        return worker_pool_signature(self.config)

    def warm_fbm_cache(self) -> None:
        for field_name in _FBM_FIELDS:
            self.fbm_for(field_name)

    def fbm_for(self, field: str):
        from game_core.world_gen import _build_fbm_precalc

        cache_key = f"{self.config.world_seed}:{field}"
        cached = self._fbm_cache.get(cache_key)
        if cached is not None:
            return cached
        precalc = _build_fbm_precalc(self.config, field)
        self._fbm_cache[cache_key] = precalc
        return precalc

    def generate_terrain_layers(
        self,
        cx: int,
        cy: int,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        from game_core.world_gen import build_terrain_layers_and_field_cache

        layer0, layer1, _cache = build_terrain_layers_and_field_cache(cx, cy, self)
        return layer0, layer1

    def generate_chunk_result(self, cx: int, cy: int) -> ChunkGenResult:
        from game_core.collision_catalog import load_collision_catalog
        from game_core.collision_grid import build_chunk_solid_grid
        from game_core.content_registry import load_content_registry
        from game_core.world_gen import compute_procedural_decorations, get_debug_mode
        from game_core.worker_content_snapshot import WorkerContentSnapshot

        layer0, layer1 = self.generate_terrain_layers(cx, cy)
        layer0_ids = tuple(stable_tile_id(key) for key in layer0)
        layer1_ids = tuple(stable_tile_id(key) for key in layer1)

        if get_debug_mode() is not None or not self.config.parallel_worker_apply:
            return ChunkGenResult(
                coord=(cx, cy),
                layer0=layer0_ids,
                layer1=layer1_ids,
                decorations=None,
                solid_grid=None,
            )

        if self._worker_snapshot is not None and self._worker_collision is not None:
            snapshot = self._worker_snapshot
            collision = self._worker_collision
            walkable = _walkable_map_from_snapshot(snapshot)
        else:
            content = load_content_registry()
            collision = load_collision_catalog()
            snapshot = WorkerContentSnapshot.from_registry(content)
            walkable = _walkable_map_from_content(content)

        known_ids = snapshot.known_decoration_ids
        procedural = compute_procedural_decorations(
            cx, cy, ctx=self, known_decoration_ids=known_ids
        )
        chunk = Chunk.from_terrain((cx, cy), list(layer0), list(layer1))
        solid_grid = build_chunk_solid_grid(
            chunk,
            procedural,
            walkable_by_tile_id=walkable,
            snapshot=snapshot,
            collision=collision,
        )
        result = ChunkGenResult(
            coord=(cx, cy),
            layer0=layer0_ids,
            layer1=layer1_ids,
            decorations=procedural_to_ipc(procedural),
            solid_grid=solid_grid,
        )
        validate_chunk_gen_result(result)
        return result

    def generate_terrain_result(self, cx: int, cy: int) -> ChunkGenResult:
        return self.generate_chunk_result(cx, cy)

    def generate_chunk(self, cx: int, cy: int) -> Chunk:
        layer0, layer1 = self.generate_terrain_layers(cx, cy)
        return Chunk.from_terrain((cx, cy), list(layer0), list(layer1))


def _walkable_map_from_content(content) -> dict[int, bool]:
    from game_core.tile_ids import stable_tile_id

    mapping = {0: True}
    for tile in content.tiles:
        mapping[stable_tile_id(tile.sprite_key)] = tile.walkable
    return mapping


def _walkable_map_from_snapshot(snapshot: WorkerContentSnapshot) -> dict[int, bool]:
    mapping: dict[int, bool] = {0: True}
    for tile_id in snapshot.non_walkable_tile_ids:
        mapping[tile_id] = False
    return mapping
