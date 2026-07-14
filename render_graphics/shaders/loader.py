"""SPIR-V Shader laden."""

from __future__ import annotations

from pathlib import Path

SHADER_DIR = Path(__file__).parent


def load_spirv(name: str) -> bytes:
    path = SHADER_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Shader nicht gefunden: {path}")
    return path.read_bytes()
