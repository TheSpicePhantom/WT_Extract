"""Kompakter Content-Snapshot für Worker-Solid (M22e)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from game_core.content_registry import ContentRegistry
from game_core.tile_ids import stable_tile_id


@dataclass(frozen=True, slots=True)
class WorkerContentSnapshot:
    known_decoration_ids: frozenset[str]
    non_walkable_tile_ids: frozenset[int]
    decoration_sprite_key_by_id: dict[int, str]
    decoration_blocks_by_id: dict[int, bool]
    fingerprint: str

    @classmethod
    def from_registry(cls, content: ContentRegistry) -> WorkerContentSnapshot:
        known_decoration_ids = frozenset(content.decoration_ids())
        non_walkable: set[int] = set()
        for tile in content.tiles:
            if not tile.walkable:
                non_walkable.add(stable_tile_id(tile.sprite_key))
        decoration_sprite_key_by_id: dict[int, str] = {}
        decoration_blocks_by_id: dict[int, bool] = {}
        for deco_id in known_decoration_ids:
            entry = content.decoration_by_id(deco_id)
            if entry is None:
                continue
            deco_int = stable_tile_id(deco_id)
            decoration_sprite_key_by_id[deco_int] = entry.sprite_key
            decoration_blocks_by_id[deco_int] = entry.blocks_movement
        fingerprint = _build_fingerprint(
            known_decoration_ids,
            non_walkable,
            decoration_sprite_key_by_id,
            decoration_blocks_by_id,
        )
        return cls(
            known_decoration_ids=known_decoration_ids,
            non_walkable_tile_ids=frozenset(non_walkable),
            decoration_sprite_key_by_id=decoration_sprite_key_by_id,
            decoration_blocks_by_id=decoration_blocks_by_id,
            fingerprint=fingerprint,
        )

    def tile_walkable_by_id(self, tile_id: int) -> bool:
        if tile_id == 0:
            return True
        return tile_id not in self.non_walkable_tile_ids


def _build_fingerprint(
    known_decoration_ids: frozenset[str],
    non_walkable: set[int],
    decoration_sprite_key_by_id: dict[int, str],
    decoration_blocks_by_id: dict[int, bool],
) -> str:
    payload = {
        "decorations": sorted(known_decoration_ids),
        "non_walkable": sorted(non_walkable),
        "deco_sprite": {str(k): v for k, v in sorted(decoration_sprite_key_by_id.items())},
        "deco_blocks": {str(k): v for k, v in sorted(decoration_blocks_by_id.items())},
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
