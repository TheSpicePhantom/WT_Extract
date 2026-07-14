"""Sprite-Keys im Minecraft-Stil: namespace:path (z. B. wt:decoration/trees/tree_oak)."""

from __future__ import annotations

from pathlib import Path

from render_scene.handles import SpriteKey

DEFAULT_SPRITE_NAMESPACE = "wt"


def normalize_key_part(part: str) -> str:
    return part.strip().lower().replace("\\", "/").replace(" ", "_")


def make_sprite_key(relative_path: str | Path, namespace: str = DEFAULT_SPRITE_NAMESPACE) -> SpriteKey:
    """Erzeugt einen Key aus relativem Pfad ohne Endung."""
    path = normalize_key_part(str(relative_path).replace("\\", "/"))
    if path.endswith(".png"):
        path = path[:-4]
    if ":" in path:
        raise ValueError(f"Pfad darf keinen Namespace enthalten: {path}")
    namespace = normalize_key_part(namespace)
    if not path:
        raise ValueError("Sprite-Pfad darf nicht leer sein.")
    return SpriteKey(f"{namespace}:{path}")


def sprite_key_from_file(path: Path, root: Path, namespace: str = DEFAULT_SPRITE_NAMESPACE) -> SpriteKey:
    relative = path.relative_to(root).with_suffix("")
    return make_sprite_key(relative.as_posix(), namespace=namespace)


def parse_sprite_key(key: str | SpriteKey) -> tuple[str, str]:
    text = normalize_key_part(str(key))
    if ":" not in text:
        raise ValueError(f"Ungültiger Sprite-Key (namespace:path erwartet): {key}")
    namespace, path = text.split(":", 1)
    if not namespace or not path:
        raise ValueError(f"Ungültiger Sprite-Key: {key}")
    return namespace, path
