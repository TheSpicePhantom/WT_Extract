"""Prozedurale Weltgenerierung — Height, Klima, Voronoi-Biome, Tiles, Decorations."""

from __future__ import annotations

import json
import math
from contextlib import contextmanager
from dataclasses import astuple, dataclass, replace
from enum import Enum
from pathlib import Path

from game_core.biomes import (
    BiomeId,
    BiomesConfig,
    ClimateClass,
    WaterClass,
    blended_decoration_density,
    climate_class_from_samples,
    decorations_for_biome,
    decorations_for_blend_zone,
    load_biomes_config,
    pick_biome_variant,
    resolve_blended_layer0,
    tile_mapping_for_biome,
)
from game_core.world_gen_context import WorldGenContext
from game_core.content_registry import ContentRegistry
from game_core.world_gen_result import DecorationPlacement
from game_core.noise import FbmParams, domain_warp_xy, precalc_fbm, sample_fbm
from game_core.world import (
    CHUNK_SIZE_TILES,
    EMPTY_OVERLAY_KEY,
    TILE_SIZE_PX,
    Chunk,
    World,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORLD_GEN_CONFIG = PROJECT_ROOT / "assets" / "content" / "world_gen.json"

KEY_GRASS = "wt:tiles/grass"
KEY_DIRT = "wt:tiles/dirt"
KEY_STONE = "wt:tiles/stone"
KEY_WATER = "wt:tiles/water"
KEY_PATH = "wt:tiles/path"
KEY_FOUNDATION = "wt:tiles/foundation"
KEY_DEEP_WATER = "wt:tiles/deep_water"
KEY_SHALLOW_WATER = "wt:tiles/shallow_water"
KEY_SAND = "wt:tiles/sand"
KEY_SNOW = "wt:tiles/snow"

_DEMO_DECORATION_COORDS: tuple[tuple[int, int], ...] = (
    (20, 20),
    (24, 22),
    (28, 24),
    (32, 26),
    (36, 28),
    (40, 30),
    (44, 32),
    (48, 34),
    (52, 36),
    (56, 38),
    (60, 40),
    (64, 42),
    (68, 44),
    (72, 46),
    (76, 48),
)


class DebugMode(str, Enum):
    HEIGHT = "height"
    WATER = "water"
    TEMPERATURE = "temperature"
    MOISTURE = "moisture"
    CLIMATE_CLASS = "climate_class"
    VORONOI_CELLS = "voronoi_cells"
    VORONOI_SEEDS = "voronoi_seeds"
    VORONOI_RAW = "voronoi_raw"
    VORONOI_WARP = "voronoi_warp"
    VORONOI_BLEND = "voronoi_blend"
    FINAL_BIOME = "final_biome"
    SUB_BIOME = "sub_biome"
    TERRAIN = "terrain"
    DECORATIONS = "decorations"


@dataclass(frozen=True, slots=True)
class WorldGenConfig:
    world_seed: int
    height_scale: float
    height_octaves: int
    height_lacunarity: float
    height_persistence: float
    height_offset_x: float
    height_offset_y: float
    sea_level: float
    shallow_water_band: float
    temperature_scale: float
    temperature_octaves: int
    temperature_lacunarity: float
    temperature_persistence: float
    temperature_offset_x: float
    temperature_offset_y: float
    moisture_scale: float
    moisture_octaves: int
    moisture_lacunarity: float
    moisture_persistence: float
    moisture_offset_x: float
    moisture_offset_y: float
    continentalness_scale: float
    continentalness_octaves: int
    continentalness_lacunarity: float
    continentalness_persistence: float
    continentalness_offset_x: float
    continentalness_offset_y: float
    biome_cell_size: float
    biome_shape_distortion: float
    biome_distortion_frequency: float
    biome_blend_width: float
    neutral_climate_width: float
    hot_threshold: float
    cold_threshold: float
    humid_threshold: float
    dry_threshold: float
    start_area_x: int
    start_area_y: int
    start_area_radius: float
    start_min_land_height: float
    start_decoration_density_scale: float
    start_min_score: float
    start_sample_grid_radius: int
    start_max_seed_attempts: int
    decoration_base_density: float
    sub_biome_scale: float
    sub_biome_octaves: int
    sub_biome_lacunarity: float
    sub_biome_persistence: float
    sub_biome_offset_x: float
    sub_biome_offset_y: float
    parallel_workers: int | str
    parallel_prefetch: bool
    parallel_worker_apply: bool


@dataclass(frozen=True, slots=True)
class ChunkFieldCache:
    coord: tuple[int, int]
    climate: tuple[ClimateSample, ...]
    region: tuple[BiomeRegionSample, ...]


@dataclass(frozen=True, slots=True)
class ClimateSample:
    height: float
    temperature: float
    moisture: float
    continentalness: float
    warp_x: float
    warp_y: float
    water_depth_like: float


@dataclass(frozen=True, slots=True)
class BiomeRegionSample:
    cell_x: int
    cell_y: int
    nearest_biome: BiomeId
    second_biome: BiomeId | None
    distance_1: float
    distance_2: float
    border_distance: float
    blend_t: float
    climate_class: ClimateClass


@dataclass(frozen=True, slots=True)
class ResolvedTileSample:
    tile_key_layer0: str
    tile_key_layer1: str
    biome_id: BiomeId
    is_walkable: bool
    water_class: WaterClass


_active_config: WorldGenConfig | None = None
_active_biomes: BiomesConfig | None = None
_cached_fbm: dict[str, object] = {}
_debug_mode: DebugMode | None = None
_spawn_score_cache: dict[tuple[int, float, int, int, int], float] = {}
_generation_ctx: WorldGenContext | None = None


def set_debug_mode(mode: DebugMode | None) -> None:
    global _debug_mode
    _debug_mode = mode


def get_debug_mode() -> DebugMode | None:
    return _debug_mode


def _sub_seed(base: int, tag: str) -> int:
    value = base & 0xFFFFFFFF
    for char in tag:
        value = ((value * 374761393) + ord(char)) & 0xFFFFFFFF
    return value


def load_world_gen_config(path: Path | None = None) -> WorldGenConfig:
    config_path = path or DEFAULT_WORLD_GEN_CONFIG
    data = json.loads(config_path.read_text(encoding="utf-8"))

    def _field(section: str, key: str, default: float | int) -> float | int:
        return data.get(section, {}).get(key, default)

    climate = data.get("climate", {})
    start = data.get("start_area", {})
    biome = data.get("biome", {})
    deco = data.get("decorations", {})
    sub = data.get("sub_biome", {})
    parallel = data.get("parallel", {})
    return WorldGenConfig(
        world_seed=int(data.get("world_seed", 42)),
        height_scale=float(_field("height", "scale", 0.008)),
        height_octaves=int(_field("height", "octaves", 6)),
        height_lacunarity=float(_field("height", "lacunarity", 2.0)),
        height_persistence=float(_field("height", "persistence", 0.5)),
        height_offset_x=float(_field("height", "offset_x", 0.0)),
        height_offset_y=float(_field("height", "offset_y", 0.0)),
        sea_level=float(data.get("sea_level", 0.42)),
        shallow_water_band=float(data.get("shallow_water_band", 0.06)),
        temperature_scale=float(_field("temperature", "scale", 0.002)),
        temperature_octaves=int(_field("temperature", "octaves", 3)),
        temperature_lacunarity=float(_field("temperature", "lacunarity", 2.0)),
        temperature_persistence=float(_field("temperature", "persistence", 0.55)),
        temperature_offset_x=float(_field("temperature", "offset_x", 100.0)),
        temperature_offset_y=float(_field("temperature", "offset_y", 200.0)),
        moisture_scale=float(_field("moisture", "scale", 0.0025)),
        moisture_octaves=int(_field("moisture", "octaves", 3)),
        moisture_lacunarity=float(_field("moisture", "lacunarity", 2.0)),
        moisture_persistence=float(_field("moisture", "persistence", 0.55)),
        moisture_offset_x=float(_field("moisture", "offset_x", 300.0)),
        moisture_offset_y=float(_field("moisture", "offset_y", 400.0)),
        continentalness_scale=float(_field("continentalness", "scale", 0.0015)),
        continentalness_octaves=int(_field("continentalness", "octaves", 2)),
        continentalness_lacunarity=float(_field("continentalness", "lacunarity", 2.0)),
        continentalness_persistence=float(_field("continentalness", "persistence", 0.5)),
        continentalness_offset_x=float(_field("continentalness", "offset_x", 500.0)),
        continentalness_offset_y=float(_field("continentalness", "offset_y", 600.0)),
        biome_cell_size=float(biome.get("cell_size", 96.0)),
        biome_shape_distortion=float(biome.get("shape_distortion", 18.0)),
        biome_distortion_frequency=float(biome.get("distortion_frequency", 0.012)),
        biome_blend_width=float(biome.get("blend_width", 12.0)),
        neutral_climate_width=float(climate.get("neutral_width", 0.12)),
        hot_threshold=float(climate.get("hot_threshold", 0.58)),
        cold_threshold=float(climate.get("cold_threshold", 0.42)),
        humid_threshold=float(climate.get("humid_threshold", 0.58)),
        dry_threshold=float(climate.get("dry_threshold", 0.42)),
        start_area_x=int(start.get("x", 256)),
        start_area_y=int(start.get("y", 256)),
        start_area_radius=float(start.get("radius", 128.0)),
        start_min_land_height=float(start.get("min_land_height", 0.44)),
        start_decoration_density_scale=float(start.get("decoration_density_scale", 0.35)),
        start_min_score=float(start.get("min_score", 0.55)),
        start_sample_grid_radius=int(start.get("sample_grid_radius", 24)),
        start_max_seed_attempts=int(start.get("max_seed_attempts", 32)),
        decoration_base_density=float(deco.get("base_density", 0.08)),
        sub_biome_scale=float(sub.get("scale", 0.015)),
        sub_biome_octaves=int(sub.get("octaves", 2)),
        sub_biome_lacunarity=float(sub.get("lacunarity", 2.0)),
        sub_biome_persistence=float(sub.get("persistence", 0.5)),
        sub_biome_offset_x=float(sub.get("offset_x", 700.0)),
        sub_biome_offset_y=float(sub.get("offset_y", 800.0)),
        parallel_workers=parallel.get("workers", "auto"),
        parallel_prefetch=bool(parallel.get("prefetch", True)),
        parallel_worker_apply=bool(parallel.get("worker_apply", True)),
    )


def configure_world_gen(
    config: WorldGenConfig,
    *,
    biomes_config: BiomesConfig | None = None,
) -> None:
    global _active_config, _active_biomes, _cached_fbm, _spawn_score_cache, _generation_ctx
    _active_config = config
    _active_biomes = biomes_config or load_biomes_config()
    _cached_fbm.clear()
    _spawn_score_cache.clear()
    _generation_ctx = None
    from game_core.world_gen_parallel import invalidate_parallel_pool

    invalidate_parallel_pool()


def get_world_gen_config() -> WorldGenConfig:
    global _active_config, _active_biomes
    if _active_config is None:
        configure_world_gen(load_world_gen_config())
    assert _active_config is not None
    return _active_config


def get_biomes_config() -> BiomesConfig:
    global _active_biomes
    if _active_biomes is None:
        _active_biomes = load_biomes_config()
    return _active_biomes


def world_gen_pool_signature(config: WorldGenConfig) -> tuple:
    return astuple(config)


def worker_pool_signature(config: WorldGenConfig) -> tuple:
    from game_core.collision_catalog import DEFAULT_COLLISION_MANIFEST, load_collision_catalog
    from game_core.content_registry import load_content_registry
    from game_core.worker_content_snapshot import WorkerContentSnapshot

    collision_path = DEFAULT_COLLISION_MANIFEST
    if collision_path.is_file():
        stat = collision_path.stat()
        collision_stat = (stat.st_mtime_ns, stat.st_size)
    else:
        collision_stat = (0, 0)
    snapshot = WorkerContentSnapshot.from_registry(load_content_registry())
    return (world_gen_pool_signature(config), snapshot.fingerprint, collision_stat, "m22e")


@contextmanager
def use_world_gen_context(ctx: WorldGenContext | None):
    global _generation_ctx
    previous = _generation_ctx
    _generation_ctx = ctx
    try:
        yield
    finally:
        _generation_ctx = previous


def bind_generation_context(ctx: WorldGenContext | None) -> None:
    global _generation_ctx
    _generation_ctx = ctx


def _build_fbm_precalc(config: WorldGenConfig, field: str):
    seed = _sub_seed(config.world_seed, field)
    if field == "height":
        params = FbmParams(
            octaves=config.height_octaves,
            lacunarity=config.height_lacunarity,
            persistence=config.height_persistence,
            scale=config.height_scale,
            seed=seed,
            offset_x=config.height_offset_x,
            offset_y=config.height_offset_y,
        )
    elif field == "temperature":
        params = FbmParams(
            octaves=config.temperature_octaves,
            lacunarity=config.temperature_lacunarity,
            persistence=config.temperature_persistence,
            scale=config.temperature_scale,
            seed=seed,
            offset_x=config.temperature_offset_x,
            offset_y=config.temperature_offset_y,
        )
    elif field == "moisture":
        params = FbmParams(
            octaves=config.moisture_octaves,
            lacunarity=config.moisture_lacunarity,
            persistence=config.moisture_persistence,
            scale=config.moisture_scale,
            seed=seed,
            offset_x=config.moisture_offset_x,
            offset_y=config.moisture_offset_y,
        )
    elif field == "sub_biome":
        params = FbmParams(
            octaves=config.sub_biome_octaves,
            lacunarity=config.sub_biome_lacunarity,
            persistence=config.sub_biome_persistence,
            scale=config.sub_biome_scale,
            seed=seed,
            offset_x=config.sub_biome_offset_x,
            offset_y=config.sub_biome_offset_y,
        )
    else:
        params = FbmParams(
            octaves=config.continentalness_octaves,
            lacunarity=config.continentalness_lacunarity,
            persistence=config.continentalness_persistence,
            scale=config.continentalness_scale,
            seed=seed,
            offset_x=config.continentalness_offset_x,
            offset_y=config.continentalness_offset_y,
        )
    return precalc_fbm(params)


def _fbm_for(config: WorldGenConfig, field: str):
    if _generation_ctx is not None and _generation_ctx.config == config:
        return _generation_ctx.fbm_for(field)
    cache_key = f"{config.world_seed}:{field}"
    if cache_key in _cached_fbm:
        return _cached_fbm[cache_key]
    precalc = _build_fbm_precalc(config, field)
    _cached_fbm[cache_key] = precalc
    return precalc


def sample_height(wx: float, wy: float, config: WorldGenConfig | None = None) -> float:
    cfg = config or get_world_gen_config()
    return sample_fbm(wx, wy, _fbm_for(cfg, "height"))


def classify_water(height: float, config: WorldGenConfig | None = None) -> WaterClass:
    cfg = config or get_world_gen_config()
    if height < cfg.sea_level - cfg.shallow_water_band:
        return WaterClass.DEEP
    if height < cfg.sea_level:
        return WaterClass.SHALLOW
    return WaterClass.LAND


def sample_climate(wx: float, wy: float, config: WorldGenConfig | None = None) -> ClimateSample:
    cfg = config or get_world_gen_config()
    height = sample_height(wx, wy, cfg)
    temperature = sample_fbm(wx, wy, _fbm_for(cfg, "temperature"))
    moisture = sample_fbm(wx, wy, _fbm_for(cfg, "moisture"))
    continentalness = sample_fbm(wx, wy, _fbm_for(cfg, "continentalness"))
    warp_x, warp_y = domain_warp_xy(
        wx,
        wy,
        frequency=cfg.biome_distortion_frequency,
        magnitude=cfg.biome_shape_distortion,
        seed=_sub_seed(cfg.world_seed, "warp"),
    )
    return ClimateSample(
        height=height,
        temperature=temperature,
        moisture=moisture,
        continentalness=continentalness,
        warp_x=warp_x,
        warp_y=warp_y,
        water_depth_like=height - cfg.sea_level,
    )


def hash_cell(cell_x: int, cell_y: int, seed: int) -> int:
    value = seed & 0xFFFFFFFF
    value = (value * 374761393 + cell_x) & 0xFFFFFFFF
    value = (value * 668265263 + cell_y) & 0xFFFFFFFF
    value = ((value ^ (value >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((value ^ (value >> 16)) & 0xFFFFFFFF) - (1 << 31)


def seed_point_in_cell(
    cell_x: int,
    cell_y: int,
    cell_size: float,
    seed: int,
) -> tuple[float, float]:
    cell_hash = hash_cell(cell_x, cell_y, seed)
    rx = ((cell_hash & 0xFFFF) / 65535.0) * cell_size
    ry = (((cell_hash >> 16) & 0xFFFF) / 65535.0) * cell_size
    return cell_x * cell_size + rx, cell_y * cell_size + ry


def _cell_coord(value: float, cell_size: float) -> int:
    return int(math.floor(value / cell_size))


def _climate_at_point(
    wx: float,
    wy: float,
    config: WorldGenConfig,
    biomes_config: BiomesConfig,
    *,
    seed_cell: tuple[int, int] | None = None,
) -> ClimateClass:
    if seed_cell is not None and _seed_climate_cache is not None:
        key = (seed_cell[0], seed_cell[1], config.world_seed)
        cached = _seed_climate_cache.get(key)
        if cached is not None:
            return cached
    climate = sample_climate(wx, wy, config)
    result = climate_class_from_samples(
        climate.temperature,
        climate.moisture,
        hot_threshold=config.hot_threshold,
        cold_threshold=config.cold_threshold,
        humid_threshold=config.humid_threshold,
        dry_threshold=config.dry_threshold,
        neutral_width=config.neutral_climate_width,
    )
    if seed_cell is not None and _seed_climate_cache is not None:
        _seed_climate_cache[(seed_cell[0], seed_cell[1], config.world_seed)] = result
    return result


_seed_climate_cache: dict[tuple[int, int, int], ClimateClass] | None = None


@contextmanager
def _chunk_seed_climate_cache_scope():
    global _seed_climate_cache
    previous = _seed_climate_cache
    _seed_climate_cache = {}
    try:
        yield
    finally:
        _seed_climate_cache = previous


def sample_sub_biome(wx: float, wy: float, config: WorldGenConfig | None = None) -> float:
    cfg = config or get_world_gen_config()
    return sample_fbm(wx, wy, _fbm_for(cfg, "sub_biome"))


def _chunk_field_index(tx: int, ty: int) -> int:
    return ty * CHUNK_SIZE_TILES + tx


def build_chunk_field_cache(
    cx: int,
    cy: int,
    *,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
) -> ChunkFieldCache:
    from game_core.terrain_gen_profile import profile_section, record_field_cache_build

    record_field_cache_build()
    cfg = config or get_world_gen_config()
    biomes = biomes_config or get_biomes_config()
    climate: list[ClimateSample] = []
    region: list[BiomeRegionSample] = []
    with _chunk_seed_climate_cache_scope():
        for ty in range(CHUNK_SIZE_TILES):
            for tx in range(CHUNK_SIZE_TILES):
                wx = cx * CHUNK_SIZE_TILES + tx
                wy = cy * CHUNK_SIZE_TILES + ty
                with profile_section("field_cache_climate"):
                    climate_sample = sample_climate(float(wx), float(wy), cfg)
                    climate.append(climate_sample)
                with profile_section("field_cache_region"):
                    region.append(
                        sample_biome_region(
                            float(wx),
                            float(wy),
                            config=cfg,
                            biomes_config=biomes,
                            warp_xy=(climate_sample.warp_x, climate_sample.warp_y),
                            use_warp=False,
                        )
                    )
    return ChunkFieldCache(coord=(cx, cy), climate=tuple(climate), region=tuple(region))


def score_spawn_area(config: WorldGenConfig | None = None) -> float:
    """0..1 — Landanteil im Startgitter, Strafe für Tiefwasser im Kern."""
    cfg = config or get_world_gen_config()
    cached = _spawn_score_cache.get(
        (
            cfg.world_seed,
            cfg.sea_level,
            cfg.start_sample_grid_radius,
            cfg.start_area_x,
            cfg.start_area_y,
        )
    )
    if cached is not None:
        return cached

    radius = max(1, cfg.start_sample_grid_radius)
    sx, sy = cfg.start_area_x, cfg.start_area_y
    land = 0
    total = 0
    deep_in_core = 0
    core_radius = max(4, radius // 3)

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            wx = sx + dx
            wy = sy + dy
            height = sample_height(float(wx), float(wy), cfg)
            water = classify_water(height, cfg)
            total += 1
            if water == WaterClass.LAND:
                land += 1
            if math.hypot(float(dx), float(dy)) <= core_radius and water == WaterClass.DEEP:
                deep_in_core += 1

    land_ratio = land / total if total else 0.0
    core_area = math.pi * core_radius * core_radius
    deep_penalty = min(1.0, deep_in_core / max(1.0, core_area))
    score = max(0.0, min(1.0, land_ratio * (1.0 - deep_penalty)))
    _spawn_score_cache[
        (
            cfg.world_seed,
            cfg.sea_level,
            cfg.start_sample_grid_radius,
            cfg.start_area_x,
            cfg.start_area_y,
        )
    ] = score
    return score


def ensure_playable_seed(
    config: WorldGenConfig,
    *,
    max_attempts: int | None = None,
) -> WorldGenConfig:
    attempts = max_attempts if max_attempts is not None else config.start_max_seed_attempts
    candidate = config
    best = candidate
    best_score = score_spawn_area(candidate)
    for offset in range(attempts):
        if best_score >= config.start_min_score:
            return best
        candidate = replace(config, world_seed=config.world_seed + offset + 1)
        score = score_spawn_area(candidate)
        if score > best_score:
            best = candidate
            best_score = score
    return best


def sample_biome_region(
    wx: float,
    wy: float,
    *,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
    use_warp: bool = True,
    warp_xy: tuple[float, float] | None = None,
) -> BiomeRegionSample:
    cfg = config or get_world_gen_config()
    biomes = biomes_config or get_biomes_config()
    cell_size = cfg.biome_cell_size
    sample_x, sample_y = wx, wy
    if warp_xy is not None:
        sample_x, sample_y = warp_xy
    elif use_warp:
        sample_x, sample_y = domain_warp_xy(
            wx,
            wy,
            frequency=cfg.biome_distortion_frequency,
            magnitude=cfg.biome_shape_distortion,
            seed=_sub_seed(cfg.world_seed, "warp"),
        )
    cell_x = _cell_coord(sample_x, cell_size)
    cell_y = _cell_coord(sample_y, cell_size)

    best_dist = float("inf")
    second_dist = float("inf")
    best_cell = (cell_x, cell_y)
    second_cell = (cell_x, cell_y)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            neighbor_x = cell_x + dx
            neighbor_y = cell_y + dy
            point_x, point_y = seed_point_in_cell(
                neighbor_x, neighbor_y, cell_size, cfg.world_seed
            )
            dist = math.hypot(sample_x - point_x, sample_y - point_y)
            if dist < best_dist:
                second_dist = best_dist
                second_cell = best_cell
                best_dist = dist
                best_cell = (neighbor_x, neighbor_y)
            elif dist < second_dist:
                second_dist = dist
                second_cell = (neighbor_x, neighbor_y)

    best_hash = hash_cell(best_cell[0], best_cell[1], cfg.world_seed)
    second_hash = hash_cell(second_cell[0], second_cell[1], cfg.world_seed)
    seed_x, seed_y = seed_point_in_cell(best_cell[0], best_cell[1], cell_size, cfg.world_seed)
    climate = _climate_at_point(seed_x, seed_y, cfg, biomes, seed_cell=best_cell)
    sub_sample = sample_sub_biome(wx, wy, cfg)
    nearest = pick_biome_variant(climate, best_hash, sub_sample, biomes)
    second_seed = seed_point_in_cell(second_cell[0], second_cell[1], cell_size, cfg.world_seed)
    second_climate = _climate_at_point(
        second_seed[0],
        second_seed[1],
        cfg,
        biomes,
        seed_cell=second_cell,
    )
    second_sub = sample_sub_biome(
        second_cell[0] * cell_size + cell_size * 0.5,
        second_cell[1] * cell_size + cell_size * 0.5,
        cfg,
    )
    second = pick_biome_variant(second_climate, second_hash, second_sub, biomes)

    border_distance = second_dist - best_dist
    blend_t = 0.0
    if cfg.biome_blend_width > 0.0 and border_distance < cfg.biome_blend_width:
        blend_t = max(0.0, min(1.0, border_distance / cfg.biome_blend_width))

    return BiomeRegionSample(
        cell_x=best_cell[0],
        cell_y=best_cell[1],
        nearest_biome=nearest,
        second_biome=second if second != nearest else None,
        distance_1=best_dist,
        distance_2=second_dist,
        border_distance=border_distance,
        blend_t=blend_t,
        climate_class=climate,
    )


def resolve_biome(
    climate: ClimateSample,
    region: BiomeRegionSample,
    water_class: WaterClass,
) -> BiomeId:
    if water_class == WaterClass.DEEP:
        return BiomeId.DEEP_WATER
    if water_class == WaterClass.SHALLOW:
        return BiomeId.SHALLOW_WATER
    return region.nearest_biome


def _coast_overlay(
    wx: int,
    wy: int,
    water_class: WaterClass,
    biomes_config: BiomesConfig,
    config: WorldGenConfig,
) -> str | None:
    from game_core.terrain_gen_profile import profile_section, record_counter

    if water_class != WaterClass.LAND:
        return None
    with profile_section("coast_overlay"):
        record_counter("coast_overlay_calls")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = classify_water(sample_height(wx + dx, wy + dy, config), config)
            if neighbor != WaterClass.LAND:
                return biomes_config.coast_overlay
    return None


def _coast_overlay_from_grid(
    tx: int,
    ty: int,
    water_classes: tuple[WaterClass, ...],
    biomes_config: BiomesConfig,
    config: WorldGenConfig,
    *,
    chunk_coord: tuple[int, int],
) -> str | None:
    from game_core.terrain_gen_profile import profile_section, record_counter

    idx = _chunk_field_index(tx, ty)
    if water_classes[idx] != WaterClass.LAND:
        return None
    cx, cy = chunk_coord
    with profile_section("coast_overlay"):
        record_counter("coast_overlay_calls")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ntx, nty = tx + dx, ty + dy
            if 0 <= ntx < CHUNK_SIZE_TILES and 0 <= nty < CHUNK_SIZE_TILES:
                neighbor = water_classes[_chunk_field_index(ntx, nty)]
            else:
                wx = cx * CHUNK_SIZE_TILES + tx + dx
                wy = cy * CHUNK_SIZE_TILES + ty + dy
                neighbor = classify_water(sample_height(wx, wy, config), config)
            if neighbor != WaterClass.LAND:
                return biomes_config.coast_overlay
    return None


def _highland_overlay(height: float, biomes_config: BiomesConfig) -> str | None:
    if height > 0.78:
        return biomes_config.highland_overlay
    return None


def _resolve_tile_from_fields(
    wx: int,
    wy: int,
    climate: ClimateSample,
    region: BiomeRegionSample,
    *,
    config: WorldGenConfig,
    biomes_config: BiomesConfig,
    tx: int | None = None,
    ty: int | None = None,
    water_class_grid: tuple[WaterClass, ...] | None = None,
    chunk_coord: tuple[int, int] | None = None,
) -> ResolvedTileSample:
    water_class = classify_water(climate.height, config)
    biome = resolve_biome(climate, region, water_class)

    if water_class == WaterClass.DEEP:
        layer0 = biomes_config.water_tiles.get("deep", KEY_DEEP_WATER)
        layer1 = EMPTY_OVERLAY_KEY
        walkable = False
    elif water_class == WaterClass.SHALLOW:
        layer0 = biomes_config.water_tiles.get("shallow", KEY_SHALLOW_WATER)
        layer1 = EMPTY_OVERLAY_KEY
        walkable = False
    else:
        layer0, _blend_biome = resolve_blended_layer0(region, biome, biomes_config)
        mapping = tile_mapping_for_biome(biome, biomes_config)
        layer1 = mapping.layer1 or EMPTY_OVERLAY_KEY
        if water_class_grid is not None and tx is not None and ty is not None and chunk_coord is not None:
            coast = _coast_overlay_from_grid(
                tx,
                ty,
                water_class_grid,
                biomes_config,
                config,
                chunk_coord=chunk_coord,
            )
        else:
            coast = _coast_overlay(wx, wy, water_class, biomes_config, config)
        highland = _highland_overlay(climate.height, biomes_config)
        if coast is not None:
            layer1 = coast
        elif highland is not None and layer1 == EMPTY_OVERLAY_KEY:
            layer1 = highland
        walkable = True

    resolved = ResolvedTileSample(
        tile_key_layer0=layer0,
        tile_key_layer1=layer1,
        biome_id=biome,
        is_walkable=walkable,
        water_class=water_class,
    )
    return apply_start_area_rules(wx, wy, climate, resolved, config, biomes_config)


def resolve_tile_cached(
    tx: int,
    ty: int,
    cache: ChunkFieldCache,
    *,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
    water_class_grid: tuple[WaterClass, ...] | None = None,
) -> ResolvedTileSample:
    cfg = config or get_world_gen_config()
    biomes = biomes_config or get_biomes_config()
    idx = _chunk_field_index(tx, ty)
    cx, cy = cache.coord
    wx = cx * CHUNK_SIZE_TILES + tx
    wy = cy * CHUNK_SIZE_TILES + ty
    return _resolve_tile_from_fields(
        wx,
        wy,
        cache.climate[idx],
        cache.region[idx],
        config=cfg,
        biomes_config=biomes,
        tx=tx,
        ty=ty,
        water_class_grid=water_class_grid,
        chunk_coord=cache.coord,
    )


def resolve_tile(
    wx: int,
    wy: int,
    *,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
) -> ResolvedTileSample:
    cfg = config or get_world_gen_config()
    biomes = biomes_config or get_biomes_config()
    climate = sample_climate(float(wx), float(wy), cfg)
    region = sample_biome_region(float(wx), float(wy), config=cfg, biomes_config=biomes)
    return _resolve_tile_from_fields(
        wx, wy, climate, region, config=cfg, biomes_config=biomes
    )


def apply_start_area_rules(
    wx: int,
    wy: int,
    climate: ClimateSample,
    resolved: ResolvedTileSample,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
) -> ResolvedTileSample:
    from game_core.terrain_gen_profile import profile_section, record_counter

    cfg = config or get_world_gen_config()
    biomes = biomes_config or get_biomes_config()
    dx = float(wx) - cfg.start_area_x
    dy = float(wy) - cfg.start_area_y
    dist = math.hypot(dx, dy)
    if dist > cfg.start_area_radius:
        return resolved

    with profile_section("start_area_rules"):
        record_counter("start_area_tiles")
        if _generation_ctx is not None:
            spawn_score = _generation_ctx.spawn_score()
        else:
            spawn_score = score_spawn_area(cfg)
        falloff = 1.0 - (dist / cfg.start_area_radius)
        adjusted_height = climate.height + falloff * max(
            0.0, cfg.start_min_land_height - climate.height
        )
        water_class = classify_water(adjusted_height, cfg)
        in_core = dist <= cfg.start_area_radius * 0.4
        needs_fixup = spawn_score < cfg.start_min_score or (
            in_core and water_class == WaterClass.DEEP
        )

        if not needs_fixup:
            if resolved.water_class == WaterClass.LAND:
                return resolved
            if water_class == WaterClass.LAND and falloff > 0.25:
                return ResolvedTileSample(
                    tile_key_layer0=resolved.tile_key_layer0,
                    tile_key_layer1=resolved.tile_key_layer1,
                    biome_id=resolved.biome_id,
                    is_walkable=True,
                    water_class=WaterClass.LAND,
                )
            return resolved

        if water_class != WaterClass.LAND:
            if falloff > 0.55:
                water_class = WaterClass.LAND
            elif water_class == WaterClass.DEEP:
                return ResolvedTileSample(
                    tile_key_layer0=biomes.water_tiles.get("shallow", KEY_SHALLOW_WATER),
                    tile_key_layer1=EMPTY_OVERLAY_KEY,
                    biome_id=BiomeId.SHALLOW_WATER,
                    is_walkable=False,
                    water_class=WaterClass.SHALLOW,
                )
            elif falloff < 0.35:
                return resolved

        blend = max(0.0, min(1.0, falloff))
        neutral_mapping = tile_mapping_for_biome(BiomeId.PLAINS, biomes)
        if blend >= 0.85 or spawn_score < cfg.start_min_score * 0.75:
            layer0 = neutral_mapping.layer0
            layer1 = neutral_mapping.layer1 or EMPTY_OVERLAY_KEY
            biome_id = BiomeId.PLAINS
        else:
            layer0 = resolved.tile_key_layer0
            layer1 = resolved.tile_key_layer1
            biome_id = resolved.biome_id

        return ResolvedTileSample(
            tile_key_layer0=layer0,
            tile_key_layer1=layer1,
            biome_id=biome_id,
            is_walkable=True,
            water_class=WaterClass.LAND,
        )


def generate_chunk_terrain(
    cx: int,
    cy: int,
    config: WorldGenConfig | None = None,
    biomes_config: BiomesConfig | None = None,
) -> dict[int, list[str]]:
    ctx = WorldGenContext.from_configs(
        config or get_world_gen_config(),
        biomes_config or get_biomes_config(),
    )
    return generate_chunk_terrain_with_context(cx, cy, ctx)


def build_terrain_layers_and_field_cache(
    cx: int,
    cy: int,
    ctx: WorldGenContext,
) -> tuple[tuple[str, ...], tuple[str, ...], ChunkFieldCache]:
    """M24c — Ein-Pass: field_cache einmal, Layers daraus."""
    from game_core.terrain_gen_profile import profile_section

    with use_world_gen_context(ctx):
        ctx.reset_chunk_build_session()
        cfg = ctx.config
        biomes = ctx.biomes
        cache = build_chunk_field_cache(cx, cy, config=cfg, biomes_config=biomes)
        water_class_grid = tuple(
            classify_water(climate.height, cfg) for climate in cache.climate
        )
        layer0: list[str] = []
        layer1: list[str] = []
        with profile_section("resolve_tiles"):
            for ty in range(CHUNK_SIZE_TILES):
                for tx in range(CHUNK_SIZE_TILES):
                    resolved = resolve_tile_cached(
                        tx,
                        ty,
                        cache,
                        config=cfg,
                        biomes_config=biomes,
                        water_class_grid=water_class_grid,
                    )
                    layer0.append(resolved.tile_key_layer0)
                    layer1.append(resolved.tile_key_layer1)
        return tuple(layer0), tuple(layer1), cache


def generate_chunk_terrain_with_context(
    cx: int,
    cy: int,
    ctx: WorldGenContext,
) -> dict[int, list[str]]:
    layer0, layer1, _cache = build_terrain_layers_and_field_cache(cx, cy, ctx)
    return {0: list(layer0), 1: list(layer1)}


def generate_chunk(cx: int, cy: int) -> Chunk:
    if _debug_mode is not None and _debug_mode != DebugMode.DECORATIONS:
        return generate_chunk_debug(cx, cy, _debug_mode)
    layers = generate_chunk_terrain(cx, cy)
    return Chunk.from_terrain((cx, cy), layers[0], layers[1])


_DEBUG_PALETTE: tuple[str, ...] = (
    KEY_DEEP_WATER,
    KEY_SHALLOW_WATER,
    KEY_WATER,
    KEY_SAND,
    KEY_DIRT,
    KEY_GRASS,
    KEY_STONE,
    KEY_SNOW,
    KEY_PATH,
)


def _quantize(value: float, buckets: int) -> int:
    clamped = max(0.0, min(1.0, value))
    if buckets <= 1:
        return 0
    return min(buckets - 1, int(clamped * buckets))


def _debug_tile_for_mode(
    wx: int,
    wy: int,
    mode: DebugMode,
    config: WorldGenConfig,
    biomes_config: BiomesConfig,
) -> tuple[str, str]:
    climate = sample_climate(float(wx), float(wy), config)
    buckets = len(_DEBUG_PALETTE)

    if mode == DebugMode.HEIGHT:
        key = _DEBUG_PALETTE[_quantize(climate.height, buckets)]
        return key, EMPTY_OVERLAY_KEY
    if mode == DebugMode.WATER:
        water = classify_water(climate.height, config)
        if water == WaterClass.DEEP:
            return KEY_DEEP_WATER, EMPTY_OVERLAY_KEY
        if water == WaterClass.SHALLOW:
            return KEY_SHALLOW_WATER, EMPTY_OVERLAY_KEY
        return KEY_GRASS, EMPTY_OVERLAY_KEY
    if mode == DebugMode.TEMPERATURE:
        return _DEBUG_PALETTE[_quantize(climate.temperature, buckets)], EMPTY_OVERLAY_KEY
    if mode == DebugMode.MOISTURE:
        return _DEBUG_PALETTE[_quantize(climate.moisture, buckets)], EMPTY_OVERLAY_KEY
    if mode == DebugMode.CLIMATE_CLASS:
        region = sample_biome_region(float(wx), float(wy), config=config, biomes_config=biomes_config)
        index = list(ClimateClass).index(region.climate_class)
        return _DEBUG_PALETTE[index % buckets], EMPTY_OVERLAY_KEY
    if mode in (DebugMode.VORONOI_CELLS, DebugMode.VORONOI_RAW):
        region = sample_biome_region(
            float(wx), float(wy), config=config, biomes_config=biomes_config, use_warp=False
        )
        index = abs(hash_cell(region.cell_x, region.cell_y, config.world_seed)) % buckets
        return _DEBUG_PALETTE[index], EMPTY_OVERLAY_KEY
    if mode == DebugMode.VORONOI_WARP:
        region = sample_biome_region(
            float(wx), float(wy), config=config, biomes_config=biomes_config, use_warp=True
        )
        index = abs(hash_cell(region.cell_x, region.cell_y, config.world_seed)) % buckets
        return _DEBUG_PALETTE[index], EMPTY_OVERLAY_KEY
    if mode == DebugMode.VORONOI_BLEND:
        region = sample_biome_region(float(wx), float(wy), config=config, biomes_config=biomes_config)
        return _DEBUG_PALETTE[_quantize(region.blend_t, buckets)], EMPTY_OVERLAY_KEY
    if mode == DebugMode.VORONOI_SEEDS:
        cell_size = config.biome_cell_size
        cell_x = _cell_coord(float(wx), cell_size)
        cell_y = _cell_coord(float(wy), cell_size)
        sx, sy = seed_point_in_cell(cell_x, cell_y, cell_size, config.world_seed)
        if abs(wx - sx) <= 1.5 and abs(wy - sy) <= 1.5:
            return KEY_PATH, KEY_FOUNDATION
        region = sample_biome_region(
            float(wx), float(wy), config=config, biomes_config=biomes_config, use_warp=False
        )
        index = abs(hash_cell(region.cell_x, region.cell_y, config.world_seed)) % buckets
        return _DEBUG_PALETTE[index], EMPTY_OVERLAY_KEY
    if mode == DebugMode.FINAL_BIOME:
        resolved = resolve_tile(wx, wy, config=config, biomes_config=biomes_config)
        index = abs(hash(resolved.biome_id.value)) % buckets
        return _DEBUG_PALETTE[index], EMPTY_OVERLAY_KEY
    if mode == DebugMode.SUB_BIOME:
        region = sample_biome_region(float(wx), float(wy), config=config, biomes_config=biomes_config)
        sub = sample_sub_biome(float(wx), float(wy), config)
        variant = pick_biome_variant(region.climate_class, hash_cell(region.cell_x, region.cell_y, config.world_seed), sub, biomes_config)
        index = abs(hash(variant.value)) % buckets
        return _DEBUG_PALETTE[index], EMPTY_OVERLAY_KEY
    if mode == DebugMode.TERRAIN:
        resolved = resolve_tile(wx, wy, config=config, biomes_config=biomes_config)
        return resolved.tile_key_layer0, resolved.tile_key_layer1
    resolved = resolve_tile(wx, wy, config=config, biomes_config=biomes_config)
    return resolved.tile_key_layer0, resolved.tile_key_layer1


def generate_chunk_debug(cx: int, cy: int, mode: DebugMode) -> Chunk:
    config = get_world_gen_config()
    biomes = get_biomes_config()
    layer0: list[str] = []
    layer1: list[str] = []
    for ty in range(CHUNK_SIZE_TILES):
        for tx in range(CHUNK_SIZE_TILES):
            wx = cx * CHUNK_SIZE_TILES + tx
            wy = cy * CHUNK_SIZE_TILES + ty
            t0, t1 = _debug_tile_for_mode(wx, wy, mode, config, biomes)
            layer0.append(t0)
            layer1.append(t1)
    return Chunk.from_terrain((cx, cy), layer0, layer1)


def chunk_differs_from_baseline(chunk: Chunk) -> bool:
    cx, cy = chunk.coord
    baseline = generate_chunk(cx, cy)
    layer_ids = set(baseline.layer_keys) | set(chunk.layer_keys)
    for layer_id in layer_ids:
        if baseline.layer_keys.get(layer_id) != chunk.layer_keys.get(layer_id):
            return True
    return False


def _tile_hash(seed: int, wx: int, wy: int) -> int:
    value = seed & 0xFFFFFFFF
    value = (value * 73856093 + wx) & 0xFFFFFFFF
    value = (value * 19349663 + wy) & 0xFFFFFFFF
    return value


def _first_decoration_id(content: ContentRegistry, predicate) -> str | None:
    for entry in content.decorations:
        if predicate(entry):
            return entry.id
    return None


def populate_demo_decorations(world: World, content: ContentRegistry) -> None:
    bush_id = _first_decoration_id(content, lambda entry: entry.category == "bush")
    apple_id = _first_decoration_id(
        content, lambda entry: entry.id == "trees/apple/summer/apple_3"
    )
    maple_id = _first_decoration_id(
        content, lambda entry: entry.id == "trees/maple/summer/maple_2"
    )
    spruce_id = _first_decoration_id(
        content, lambda entry: entry.id == "trees/spruce/spruce_tree_1"
    )
    jungle_id = _first_decoration_id(
        content, lambda entry: entry.id == "trees/jungle/jungle_tree_1"
    )
    rotation = [item for item in (bush_id, apple_id, maple_id, spruce_id, jungle_id) if item]
    if not rotation:
        return
    for index, (wx, wy) in enumerate(_DEMO_DECORATION_COORDS):
        decoration_id = rotation[index % len(rotation)]
        world.place_decoration(wx, wy, decoration_id, procedural=True)


def compute_procedural_decorations(
    cx: int,
    cy: int,
    *,
    ctx: WorldGenContext,
    known_decoration_ids: frozenset[str],
    field_cache: ChunkFieldCache | None = None,
) -> tuple[DecorationPlacement, ...]:
    config = ctx.config
    biomes = ctx.biomes
    cache = field_cache or build_chunk_field_cache(cx, cy, config=config, biomes_config=biomes)
    placements: list[DecorationPlacement] = []
    for ty in range(CHUNK_SIZE_TILES):
        for tx in range(CHUNK_SIZE_TILES):
            wx = cx * CHUNK_SIZE_TILES + tx
            wy = cy * CHUNK_SIZE_TILES + ty
            resolved = resolve_tile_cached(tx, ty, cache, config=config, biomes_config=biomes)
            if not resolved.is_walkable or resolved.water_class != WaterClass.LAND:
                continue

            region = cache.region[_chunk_field_index(tx, ty)]
            allowed = decorations_for_blend_zone(region, biomes)
            if not allowed:
                allowed = decorations_for_biome(resolved.biome_id, biomes)
            if not allowed:
                continue

            density = blended_decoration_density(region, biomes)
            density *= config.decoration_base_density * 10.0
            dx = float(wx) - config.start_area_x
            dy = float(wy) - config.start_area_y
            if math.hypot(dx, dy) <= config.start_area_radius:
                density *= config.start_decoration_density_scale

            tile_hash = _tile_hash(config.world_seed, wx, wy)
            threshold = int(density * 1000)
            if (tile_hash % 1000) >= threshold:
                continue

            decoration_id = allowed[tile_hash % len(allowed)]
            if decoration_id not in known_decoration_ids:
                continue
            placements.append(DecorationPlacement(wx=wx, wy=wy, decoration_id=decoration_id))
    return tuple(placements)


def populate_chunk_decorations(
    world: World,
    content: ContentRegistry,
    cx: int,
    cy: int,
) -> None:
    ctx = WorldGenContext.from_active()
    known_ids = frozenset(content.decoration_ids())
    for placement in compute_procedural_decorations(
        cx, cy, ctx=ctx, known_decoration_ids=known_ids
    ):
        world.place_decoration(
            placement.wx,
            placement.wy,
            placement.decoration_id,
            procedural=True,
        )


def remove_procedural_decorations_in_chunk(world: World, coord: tuple[int, int]) -> None:
    cx, cy = coord
    wx_min = cx * CHUNK_SIZE_TILES
    wx_max = wx_min + CHUNK_SIZE_TILES - 1
    wy_min = cy * CHUNK_SIZE_TILES
    wy_max = wy_min + CHUNK_SIZE_TILES - 1

    kept: list = []
    for placed in world.decorations:
        tile_x = int(placed.world_x) // TILE_SIZE_PX
        tile_y = int(placed.world_y) // TILE_SIZE_PX
        in_chunk = wx_min <= tile_x <= wx_max and wy_min <= tile_y <= wy_max
        if in_chunk and placed.procedural:
            world._mark_decoration_collision_dirty(placed.world_x, placed.world_y)
            continue
        kept.append(placed)
    world.decorations = kept


def remove_decorations_in_chunk(world: World, coord: tuple[int, int]) -> None:
    cx, cy = coord
    wx_min = cx * CHUNK_SIZE_TILES
    wx_max = wx_min + CHUNK_SIZE_TILES - 1
    wy_min = cy * CHUNK_SIZE_TILES
    wy_max = wy_min + CHUNK_SIZE_TILES - 1

    kept: list = []
    for placed in world.decorations:
        tile_x = int(placed.world_x) // TILE_SIZE_PX
        tile_y = int(placed.world_y) // TILE_SIZE_PX
        if wx_min <= tile_x <= wx_max and wy_min <= tile_y <= wy_max:
            world._mark_decoration_collision_dirty(placed.world_x, placed.world_y)
            continue
        kept.append(placed)
    world.decorations = kept


def generate_demo_world(cols: int = 16, rows: int = 16) -> World:
    from game_core.world_gen_parallel import generate_demo_world_parallel

    return generate_demo_world_parallel(cols, rows)


def flush_procedural_chunks(world, streamer, content, collision, extractor) -> None:
    """Entlädt prozedurale Chunks und lädt neu — persistent_overrides bleiben."""
    focus_chunks = list(world.chunks.keys())
    for coord in focus_chunks:
        streamer._flush_modified_chunk(world, coord)
        remove_procedural_decorations_in_chunk(world, coord)
        world.chunks.pop(coord)
        streamer._decorated_chunks.discard(coord)
        world.dirty_chunks.discard(coord)
        world.collision_dirty_chunks.discard(coord)
        extractor.invalidate(coord)

    for coord in focus_chunks:
        streamer._load_chunk(world, coord, content, collision)
