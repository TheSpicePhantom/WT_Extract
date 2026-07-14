"""Tests — ContentRegistry."""

from __future__ import annotations

from game_core.content_registry import load_content_registry


def test_decoration_by_id_dict_lookup() -> None:
    content = load_content_registry()
    if not content.decorations:
        return
    sample = content.decorations[0]
    assert content.decoration_by_id(sample.id) is sample
    assert content.decoration_by_id("__missing__") is None
