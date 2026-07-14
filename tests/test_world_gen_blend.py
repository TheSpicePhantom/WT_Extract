"""Tests — Layer-0-Biom-Blend und Deko-Blendzone (M22)."""

from __future__ import annotations

from game_core.biomes import BiomeId, load_biomes_config, resolve_blended_layer0
from game_core.world_gen import BiomeRegionSample, ClimateClass


def _region(
    *,
    nearest: BiomeId,
    second: BiomeId | None,
    blend_t: float,
) -> BiomeRegionSample:
    return BiomeRegionSample(
        cell_x=0,
        cell_y=0,
        nearest_biome=nearest,
        second_biome=second,
        distance_1=1.0,
        distance_2=2.0,
        border_distance=blend_t * 12.0,
        blend_t=blend_t,
        climate_class=ClimateClass.NEUTRAL,
    )


def test_blend_layer0_uses_nearest_when_blend_high() -> None:
    biomes = load_biomes_config()
    region = _region(nearest=BiomeId.PLAINS, second=BiomeId.DESERT, blend_t=0.9)
    layer0, _ = resolve_blended_layer0(region, BiomeId.PLAINS, biomes)
    assert layer0 == biomes.climate_classes[ClimateClass.NEUTRAL].tiles["plains"].layer0


def test_blend_layer0_uses_second_when_blend_low() -> None:
    biomes = load_biomes_config()
    region = _region(nearest=BiomeId.PLAINS, second=BiomeId.DESERT, blend_t=0.1)
    layer0, _ = resolve_blended_layer0(region, BiomeId.PLAINS, biomes)
    assert layer0 == biomes.climate_classes[ClimateClass.HOT_DRY].tiles["desert"].layer0


def test_blend_layer0_transition_key() -> None:
    biomes = load_biomes_config()
    region = _region(nearest=BiomeId.DESERT, second=BiomeId.SAVANNA, blend_t=0.2)
    layer0, _ = resolve_blended_layer0(region, BiomeId.DESERT, biomes)
    assert layer0 == "wt:tiles/sand"
