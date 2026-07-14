"""M24b — CompiledDecoPass (datengetrieben, deterministisch)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DECO_CONFIG = PROJECT_ROOT / "assets" / "content" / "deco_generation.json"

_COMPILED: tuple[CompiledDecoPass, ...] | None = None
_CONFIG_VERSION: int | None = None


@dataclass(frozen=True, slots=True)
class DecoPassRule:
    decoration: str
    weight: int = 1


@dataclass(frozen=True, slots=True)
class CompiledDecoPass:
    name: str
    enabled: bool
    priority: int
    declaration_order: int
    biomes: frozenset[str]
    allowed_ground_tiles: frozenset[str]
    density: float
    noise_threshold: float
    height_min: float
    height_max: float
    variants: tuple[DecoPassRule, ...]
    collision_profile: str | None = None

    @property
    def sort_key(self) -> tuple[int, int, str]:
        return (self.priority, self.declaration_order, self.name)


def _default_config_data() -> dict:
    return {
        "passes": [
            {
                "name": "default",
                "enabled": True,
                "priority": 0,
                "biomes": [],
                "allowed_ground_tiles": [],
                "density": 1.0,
                "noise_threshold": 0.0,
                "height_min": 0.0,
                "height_max": 1.0,
                "variants": [],
                "collision_profile": None,
            }
        ]
    }


def _compile_pass(raw: dict, declaration_order: int) -> CompiledDecoPass:
    variants = tuple(
        DecoPassRule(
            decoration=str(rule.get("decoration", "")),
            weight=int(rule.get("weight", 1)),
        )
        for rule in raw.get("variants", raw.get("rules", []))
    )
    return CompiledDecoPass(
        name=str(raw["name"]),
        enabled=bool(raw.get("enabled", True)),
        priority=int(raw.get("priority", 0)),
        declaration_order=declaration_order,
        biomes=frozenset(str(b) for b in raw.get("biomes", [])),
        allowed_ground_tiles=frozenset(str(t) for t in raw.get("allowed_ground_tiles", [])),
        density=float(raw.get("density", raw.get("chance", 1.0))),
        noise_threshold=float(raw.get("noise_threshold", 0.0)),
        height_min=float(raw.get("height_min", 0.0)),
        height_max=float(raw.get("height_max", 1.0)),
        variants=variants,
        collision_profile=raw.get("collision_profile"),
    )


def compile_deco_config(data: dict | None = None) -> tuple[CompiledDecoPass, ...]:
    payload = data if data is not None else _default_config_data()
    passes_raw = list(payload.get("passes", []))
    name_order = {
        str(raw["name"]): idx
        for idx, raw in enumerate(sorted(passes_raw, key=lambda r: str(r["name"])))
    }
    compiled = [_compile_pass(raw, name_order[str(raw["name"])]) for raw in passes_raw]
    compiled.sort(key=lambda p: p.sort_key)
    return tuple(compiled)


def _config_hash(passes: tuple[CompiledDecoPass, ...]) -> int:
    import hashlib

    payload = [
        {
            "name": p.name,
            "priority": p.priority,
            "declaration_order": p.declaration_order,
            "enabled": p.enabled,
            "density": p.density,
            "variants": [(r.decoration, r.weight) for r in p.variants],
        }
        for p in passes
    ]
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return int(digest[:8], 16) & 0x7FFFFFFF


def load_compiled_deco_passes(path: Path | None = None) -> tuple[CompiledDecoPass, ...]:
    global _COMPILED, _CONFIG_VERSION
    config_path = path or DEFAULT_DECO_CONFIG
    if config_path.is_file():
        data = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        data = _default_config_data()
    passes = compile_deco_config(data)
    _COMPILED = passes
    _CONFIG_VERSION = _config_hash(passes)
    return passes


def get_compiled_deco_passes() -> tuple[CompiledDecoPass, ...]:
    global _COMPILED
    if _COMPILED is None:
        return load_compiled_deco_passes()
    return _COMPILED


def get_deco_config_version() -> int:
    global _CONFIG_VERSION
    if _CONFIG_VERSION is None:
        load_compiled_deco_passes()
    assert _CONFIG_VERSION is not None
    return _CONFIG_VERSION


def reset_deco_config_cache() -> None:
    global _COMPILED, _CONFIG_VERSION
    _COMPILED = None
    _CONFIG_VERSION = None
