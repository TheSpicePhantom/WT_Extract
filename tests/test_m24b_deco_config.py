"""Tests — M24b CompiledDecoPass Determinismus."""

from __future__ import annotations

from game_core.deco_generation import (
    compile_deco_config,
    get_deco_config_version,
    load_compiled_deco_passes,
    reset_deco_config_cache,
)


def test_stable_pass_order_regardless_of_json_key_order() -> None:
    data_a = {
        "passes": [
            {"name": "b", "priority": 10, "enabled": True},
            {"name": "a", "priority": 5, "enabled": True},
            {"name": "c", "priority": 10, "enabled": True},
        ]
    }
    data_b = {
        "passes": [
            {"name": "c", "priority": 10, "enabled": True},
            {"name": "a", "priority": 5, "enabled": True},
            {"name": "b", "priority": 10, "enabled": True},
        ]
    }
    passes_a = compile_deco_config(data_a)
    passes_b = compile_deco_config(data_b)
    assert [p.name for p in passes_a] == [p.name for p in passes_b]
    assert [p.sort_key for p in passes_a] == [p.sort_key for p in passes_b]


def test_deco_config_version_stable_for_compiled_state() -> None:
    reset_deco_config_cache()
    data = {
        "passes": [
            {"name": "alpha", "priority": 1, "enabled": True, "density": 0.5},
            {"name": "beta", "priority": 2, "enabled": True, "density": 0.7},
        ]
    }
    compile_deco_config(data)
    v1 = get_deco_config_version()
    reset_deco_config_cache()
    reversed_data = {"passes": list(reversed(data["passes"]))}
    compile_deco_config(reversed_data)
    v2 = get_deco_config_version()
    assert v1 == v2


def test_load_compiled_deco_passes_sort_key() -> None:
    reset_deco_config_cache()
    passes = load_compiled_deco_passes()
    keys = [p.sort_key for p in passes]
    assert keys == sorted(keys)
