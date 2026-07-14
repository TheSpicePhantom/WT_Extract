"""Atlas-Laden, SpriteRect-Lookup und GPU-SSBO für texturierte Instanzen."""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path

from vulkan import *  # noqa: F403

from render_core.buffer import destroy_buffer, upload_device_local_buffer
from render_core.device import GpuDevice
from render_core.texture import GpuTexture, create_texture_rgba8, destroy_texture
from render_core.vk_types import VkBuffer, VkDevice, VkDeviceMemory
from render_scene.handles import MaterialHandle, SpriteId, TextureHandle
from render_scene.sprite_catalog import SpriteCatalog, catalog_from_manifest_data
from render_scene.types import (
    AtlasManifestEntry,
    MaterialDescriptor,
    SpriteRect,
    TextureAtlasDescriptor,
)

SPRITE_RECT_GPU_STRIDE = 32
DEFAULT_ATLAS_DIR = Path(__file__).resolve().parent.parent / "assets" / "demo_atlas"


@dataclass
class AtlasRegistry:
    atlas: TextureAtlasDescriptor
    gpu_texture: GpuTexture
    sprite_rects: list[SpriteRect]
    sprite_lookup_buffer: VkBuffer
    sprite_lookup_memory: VkDeviceMemory
    material: MaterialDescriptor
    catalog: SpriteCatalog
    max_sprite_id: int


def resolve_sprite_key(registry: AtlasRegistry, key: str) -> SpriteId:
    return registry.catalog.resolve(key)


def _load_rgba_bytes(png_path: Path) -> tuple[int, int, bytes]:
    from PIL import Image

    with Image.open(png_path) as image:
        rgba = image.convert("RGBA")
        width, height = rgba.size
        return width, height, rgba.tobytes()


def _pack_sprite_rects_ssbo(sprite_rects: list[SpriteRect]) -> bytes:
    chunks: list[bytes] = []
    for rect in sprite_rects:
        chunks.append(
            struct.pack(
                "8f",
                rect.u0,
                rect.v0,
                rect.u1,
                rect.v1,
                float(rect.pixel_w),
                float(rect.pixel_h),
                float(rect.sheet_cols),
                float(rect.sheet_rows),
            )
        )
    return b"".join(chunks)


def load_from_manifest(
    device: GpuDevice,
    manifest_path: Path,
    png_path: Path | None = None,
) -> AtlasRegistry:
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    atlas_png = png_path or manifest_path.parent / "atlas.png"
    if not atlas_png.is_file():
        raise FileNotFoundError(f"Atlas-PNG nicht gefunden: {atlas_png}")

    width, height, rgba_bytes = _load_rgba_bytes(atlas_png)
    gpu_texture = create_texture_rgba8(
        device.physical,
        device.logical,
        device.graphics_queue,
        device.queue_family_indices.graphics,
        width,
        height,
        rgba_bytes,
    )

    entries_raw = manifest_data.get("entries", [])
    max_sprite_id = max((entry["sprite_id"] for entry in entries_raw), default=0)
    sprite_rects = [
        SpriteRect(u0=0.0, v0=0.0, u1=0.0, v1=0.0, pixel_w=0, pixel_h=0)
        for _ in range(max_sprite_id + 1)
    ]
    manifest_entries: list[AtlasManifestEntry] = []

    catalog = catalog_from_manifest_data(manifest_data)

    for entry in entries_raw:
        sprite_id = int(entry["sprite_id"])
        rect = SpriteRect(
            u0=float(entry["u0"]),
            v0=float(entry["v0"]),
            u1=float(entry["u1"]),
            v1=float(entry["v1"]),
            pixel_w=int(entry["pixel_w"]),
            pixel_h=int(entry["pixel_h"]),
            sheet_cols=int(entry.get("sheet_cols", 1)),
            sheet_rows=int(entry.get("sheet_rows", 1)),
        )
        sprite_rects[sprite_id] = rect
        key = str(entry.get("key", f"wt:{entry['name']}"))
        manifest_entries.append(
            AtlasManifestEntry(
                sprite_id=sprite_id,
                key=key,
                name=str(entry["name"]),
                cells_w=int(entry["cells_w"]),
                cells_h=int(entry["cells_h"]),
                cell_x=int(entry["cell_x"]),
                cell_y=int(entry["cell_y"]),
            )
        )

    lookup_bytes = _pack_sprite_rects_ssbo(sprite_rects)
    lookup_buffer, lookup_memory = upload_device_local_buffer(
        device.physical,
        device.logical,
        device.graphics_queue,
        device.queue_family_indices.graphics,
        lookup_bytes,
        VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
    )

    texture_handle = TextureHandle(int(manifest_data.get("texture_handle", 1)))
    material_handle = MaterialHandle(int(manifest_data.get("material_handle", 1)))

    atlas = TextureAtlasDescriptor(
        handle=texture_handle,
        width=int(manifest_data.get("width", width)),
        height=int(manifest_data.get("height", height)),
        entries=tuple(manifest_entries),
    )
    material = MaterialDescriptor(handle=material_handle, texture=texture_handle)

    return AtlasRegistry(
        atlas=atlas,
        gpu_texture=gpu_texture,
        sprite_rects=sprite_rects,
        sprite_lookup_buffer=lookup_buffer,
        sprite_lookup_memory=lookup_memory,
        material=material,
        catalog=catalog,
        max_sprite_id=max_sprite_id,
    )


def load_default_atlas(device: GpuDevice, atlas_dir: Path | None = None) -> AtlasRegistry:
    directory = atlas_dir or DEFAULT_ATLAS_DIR
    manifest_path = directory / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Demo-Atlas fehlt: {manifest_path}. "
            "Ausführen: python tools/bake_atlas.py --generate-placeholders"
        )
    return load_from_manifest(device, manifest_path)


def sprite_rect_for(registry: AtlasRegistry, sprite_id: SpriteId) -> SpriteRect | None:
    index = int(sprite_id)
    if index < 0 or index >= len(registry.sprite_rects):
        return None
    rect = registry.sprite_rects[index]
    if rect.pixel_w <= 0 or rect.pixel_h <= 0:
        return None
    return rect


def destroy_atlas_registry(device: VkDevice, registry: AtlasRegistry) -> None:
    destroy_buffer(device, registry.sprite_lookup_buffer, registry.sprite_lookup_memory)
    destroy_texture(device, registry.gpu_texture)
