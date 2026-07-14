"""Sichtbarkeits-LOD-Konfiguration (M23e)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VISIBILITY_LOD_CONFIG = PROJECT_ROOT / "assets" / "content" / "visibility_lod.json"

LOD0 = 0
LOD1 = 1
LOD2 = 2


@dataclass(frozen=True, slots=True)
class VisibilityLodConfig:
    lod_enabled: bool = True
    map_mode: bool = False
    lod1_zoom_max: float = 0.4
    lod2_zoom_max: float = 0.2


def load_visibility_lod_config(path: Path | None = None) -> VisibilityLodConfig:
    config_path = path or DEFAULT_VISIBILITY_LOD_CONFIG
    if not config_path.is_file():
        return _default_config()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return VisibilityLodConfig(
        lod_enabled=bool(data.get("lod_enabled", True)),
        map_mode=bool(data.get("map_mode", False)),
        lod1_zoom_max=float(data.get("lod1_zoom_max", 0.4)),
        lod2_zoom_max=float(data.get("lod2_zoom_max", 0.2)),
    )


def resolve_lod_level(zoom: float, config: VisibilityLodConfig) -> int:
    """Deterministische LOD-Stufe aus zoom und Config — keine Heuristik."""
    if not config.lod_enabled:
        return LOD0
    if config.map_mode:
        return LOD2
    if zoom <= config.lod2_zoom_max:
        return LOD2
    if zoom <= config.lod1_zoom_max:
        return LOD1
    return LOD0


def _default_config() -> VisibilityLodConfig:
    return VisibilityLodConfig(
        lod_enabled=True,
        map_mode=False,
        lod1_zoom_max=0.4,
        lod2_zoom_max=0.2,
    )
