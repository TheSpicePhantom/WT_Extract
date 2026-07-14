"""Übersetzt Game-Daten in neutrale Renderdaten — einzige legitime Kreuzung."""

from bridge.chunk_extractor import ChunkRenderExtractor
from typing import Protocol, runtime_checkable

from render_scene.types import RenderFrame

__all__ = ["ChunkRenderExtractor", "RenderExtractor"]


@runtime_checkable
class RenderExtractor(Protocol):
    """Extrahiert pro Frame einen neutralen RenderFrame aus dem Spielzustand."""

    def extract(self) -> RenderFrame:
        """Erzeugt Renderdaten ohne Spielzustand zu verändern."""
        ...
