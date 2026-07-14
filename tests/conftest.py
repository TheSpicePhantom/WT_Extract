"""Gemeinsame Test-Fixtures für World-Gen."""

from __future__ import annotations

import pytest

from game_core.world_gen import WorldGenConfig, configure_world_gen, set_debug_mode


@pytest.fixture(autouse=True)
def _fixed_world_gen() -> None:
    configure_world_gen(
        WorldGenConfig(
            world_seed=12345,
            height_scale=0.008,
            height_octaves=4,
            height_lacunarity=2.0,
            height_persistence=0.5,
            height_offset_x=0.0,
            height_offset_y=0.0,
            sea_level=0.42,
            shallow_water_band=0.06,
            temperature_scale=0.002,
            temperature_octaves=2,
            temperature_lacunarity=2.0,
            temperature_persistence=0.55,
            temperature_offset_x=100.0,
            temperature_offset_y=200.0,
            moisture_scale=0.0025,
            moisture_octaves=2,
            moisture_lacunarity=2.0,
            moisture_persistence=0.55,
            moisture_offset_x=300.0,
            moisture_offset_y=400.0,
            continentalness_scale=0.0015,
            continentalness_octaves=2,
            continentalness_lacunarity=2.0,
            continentalness_persistence=0.5,
            continentalness_offset_x=500.0,
            continentalness_offset_y=600.0,
            biome_cell_size=96.0,
            biome_shape_distortion=18.0,
            biome_distortion_frequency=0.012,
            biome_blend_width=12.0,
            neutral_climate_width=0.12,
            hot_threshold=0.58,
            cold_threshold=0.42,
            humid_threshold=0.58,
            dry_threshold=0.42,
            start_area_x=256,
            start_area_y=256,
            start_area_radius=128.0,
            start_min_land_height=0.44,
            start_decoration_density_scale=0.35,
            start_min_score=0.55,
            start_sample_grid_radius=24,
            start_max_seed_attempts=32,
            decoration_base_density=0.5,
            sub_biome_scale=0.015,
            sub_biome_octaves=2,
            sub_biome_lacunarity=2.0,
            sub_biome_persistence=0.5,
            sub_biome_offset_x=700.0,
            sub_biome_offset_y=800.0,
            parallel_workers=2,
            parallel_prefetch=False,
            parallel_worker_apply=False,
        )
    )
    set_debug_mode(None)


@pytest.fixture(autouse=True)
def _shutdown_parallel_pool_after_test() -> None:
    yield
    from game_core.world_gen_parallel import shutdown_parallel_pool

    shutdown_parallel_pool()
