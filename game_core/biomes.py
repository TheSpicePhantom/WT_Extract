"""Biom-IDs, Klimaklassen und datengetriebenes Tile-/Decoration-Mapping."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BIOMES_CONFIG = PROJECT_ROOT / "assets" / "content" / "biomes.json"

if TYPE_CHECKING:
    from game_core.world_gen import BiomeRegionSample


class ClimateClass(str, Enum):
    NEUTRAL = "neutral"
    HOT_HUMID = "hot_humid"
    HOT_DRY = "hot_dry"
    COLD_HUMID = "cold_humid"
    COLD_DRY = "cold_dry"


class WaterClass(str, Enum):
    DEEP = "deep"
    SHALLOW = "shallow"
    LAND = "land"


class BiomeId(str, Enum):
    PLAINS = "plains"
    MIXED_FOREST = "mixed_forest"
    BIRCH_FOREST = "birch_forest"
    LUSH_PLAINS = "lush_plains"
    WET_FOREST = "wet_forest"
    DESERT = "desert"
    SAVANNA = "savanna"
    STEPPE = "steppe"
    TAIGA = "taiga"
    CONIFER_FOREST = "conifer_forest"
    TUNDRA = "tundra"
    DEEP_WATER = "deep_water"
    SHALLOW_WATER = "shallow_water"


@dataclass(frozen=True, slots=True)
class BiomeTileMapping:
    layer0: str
    layer1: str | None


@dataclass(frozen=True, slots=True)
class ClimateClassDef:
    biomes: tuple[str, ...]
    tiles: dict[str, BiomeTileMapping]
    decorations: dict[str, tuple[str, ...]]
    decoration_density: float


@dataclass(frozen=True, slots=True)
class BiomesConfig:
    water_tiles: dict[str, str]
    climate_classes: dict[ClimateClass, ClimateClassDef]
    coast_overlay: str
    highland_overlay: str
    blend_threshold: float
    blend_transitions: dict[str, str]


def _parse_tile_mapping(raw: dict | None) -> BiomeTileMapping:
    if not raw:
        return BiomeTileMapping(layer0="wt:tiles/grass", layer1=None)
    layer1 = raw.get("layer1")
    return BiomeTileMapping(
        layer0=str(raw.get("layer0", "wt:tiles/grass")),
        layer1=str(layer1) if layer1 else None,
    )


def load_biomes_config(path: Path | None = None) -> BiomesConfig:
    config_path = path or DEFAULT_BIOMES_CONFIG
    data = json.loads(config_path.read_text(encoding="utf-8"))
    climate_classes: dict[ClimateClass, ClimateClassDef] = {}
    for key, entry in data.get("climate_classes", {}).items():
        climate = ClimateClass(key)
        tiles = {
            biome: _parse_tile_mapping(tile_raw)
            for biome, tile_raw in entry.get("tiles", {}).items()
        }
        decorations = {
            biome: tuple(str(item) for item in ids)
            for biome, ids in entry.get("decorations", {}).items()
        }
        climate_classes[climate] = ClimateClassDef(
            biomes=tuple(str(item) for item in entry.get("biomes", [])),
            tiles=tiles,
            decorations=decorations,
            decoration_density=float(entry.get("decoration_density", 0.05)),
        )
    blend = data.get("blend", {})
    return BiomesConfig(
        water_tiles={key: str(value) for key, value in data.get("water_tiles", {}).items()},
        climate_classes=climate_classes,
        coast_overlay=str(data.get("coast_overlay", "wt:tiles/sand")),
        highland_overlay=str(data.get("highland_overlay", "wt:tiles/stone")),
        blend_threshold=float(blend.get("threshold", 0.45)),
        blend_transitions={
            str(key): str(value) for key, value in blend.get("transitions", {}).items()
        },
    )


def climate_class_from_samples(
    temperature: float,
    moisture: float,
    *,
    hot_threshold: float,
    cold_threshold: float,
    humid_threshold: float,
    dry_threshold: float,
    neutral_width: float,
) -> ClimateClass:
    temp_neutral = abs(temperature - 0.5) < neutral_width
    moist_neutral = abs(moisture - 0.5) < neutral_width
    if temp_neutral and moist_neutral:
        return ClimateClass.NEUTRAL
    if temp_neutral or moist_neutral:
        return ClimateClass.NEUTRAL
    hot = temperature >= hot_threshold
    cold = temperature <= cold_threshold
    humid = moisture >= humid_threshold
    dry = moisture <= dry_threshold
    if not hot and not cold:
        return ClimateClass.NEUTRAL
    if hot and humid:
        return ClimateClass.HOT_HUMID
    if hot and dry:
        return ClimateClass.HOT_DRY
    if cold and humid:
        return ClimateClass.COLD_HUMID
    if cold and dry:
        return ClimateClass.COLD_DRY
    return ClimateClass.NEUTRAL


def pick_biome_for_cell(
    climate: ClimateClass,
    cell_hash: int,
    biomes_config: BiomesConfig,
) -> BiomeId:
    return pick_biome_variant(climate, cell_hash, 0.0, biomes_config)


def pick_biome_variant(
    climate: ClimateClass,
    cell_hash: int,
    sub_sample: float,
    biomes_config: BiomesConfig,
) -> BiomeId:
    class_def = biomes_config.climate_classes.get(climate)
    if class_def is None or not class_def.biomes:
        return BiomeId.PLAINS
    variant_hash = abs(cell_hash ^ int(sub_sample * 1_000_000))
    index = variant_hash % len(class_def.biomes)
    return BiomeId(class_def.biomes[index])


def biome_pair_key(first: BiomeId, second: BiomeId) -> str:
    ordered = sorted([first.value, second.value])
    return f"{ordered[0]}|{ordered[1]}"


def resolve_blended_layer0(
    region: BiomeRegionSample,
    biome: BiomeId,
    biomes_config: BiomesConfig,
) -> tuple[str, BiomeId]:
    nearest = region.nearest_biome
    second = region.second_biome
    if second is None or second == nearest or region.blend_t >= biomes_config.blend_threshold:
        mapping = tile_mapping_for_biome(biome, biomes_config)
        return mapping.layer0, biome

    pair_key = biome_pair_key(nearest, second)
    transition = biomes_config.blend_transitions.get(pair_key)
    if transition:
        return transition, biome

    chosen = second if region.blend_t < 0.5 else nearest
    mapping = tile_mapping_for_biome(chosen, biomes_config)
    return mapping.layer0, chosen


def tile_mapping_for_biome(biome: BiomeId, biomes_config: BiomesConfig) -> BiomeTileMapping:
    for class_def in biomes_config.climate_classes.values():
        if biome.value in class_def.tiles:
            return class_def.tiles[biome.value]
    return BiomeTileMapping(layer0="wt:tiles/grass", layer1=None)


def decorations_for_biome(biome: BiomeId, biomes_config: BiomesConfig) -> tuple[str, ...]:
    for class_def in biomes_config.climate_classes.values():
        if biome.value in class_def.decorations:
            return class_def.decorations[biome.value]
    return ()


def decorations_for_blend_zone(
    region: BiomeRegionSample,
    biomes_config: BiomesConfig,
) -> tuple[str, ...]:
    primary = decorations_for_biome(region.nearest_biome, biomes_config)
    if region.second_biome is None or region.second_biome == region.nearest_biome:
        return primary
    if region.blend_t >= biomes_config.blend_threshold:
        return primary
    secondary = decorations_for_biome(region.second_biome, biomes_config)
    if not secondary:
        return primary
    if not primary:
        return secondary
    merged: list[str] = []
    seen: set[str] = set()
    for item in primary + secondary:
        if item not in seen:
            seen.add(item)
            merged.append(item)
    return tuple(merged)


def decoration_density_for_biome(biome: BiomeId, biomes_config: BiomesConfig) -> float:
    for class_def in biomes_config.climate_classes.values():
        if biome.value in class_def.tiles:
            return class_def.decoration_density
    return 0.05


def blended_decoration_density(
    region: BiomeRegionSample,
    biomes_config: BiomesConfig,
) -> float:
    primary = decoration_density_for_biome(region.nearest_biome, biomes_config)
    if region.second_biome is None or region.second_biome == region.nearest_biome:
        return primary
    if region.blend_t >= biomes_config.blend_threshold:
        return primary
    secondary = decoration_density_for_biome(region.second_biome, biomes_config)
    return primary * region.blend_t + secondary * (1.0 - region.blend_t)
