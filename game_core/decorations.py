"""Platzierte Decorations — Weltobjekte (keine GPU-IDs)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PlacedDecoration:
    """Decoration-Instanz — Anker unten links, Tile-snapped."""

    world_x: float
    world_y: float
    decoration_id: str
    procedural: bool = False
