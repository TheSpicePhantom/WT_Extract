"""Mid-Level Rendering: Pipelines, Shader, Passes, Kamera, Instancing, Submission."""

from render_graphics.camera import (
    CAMERA_UBO_SIZE,
    build_view_projection,
    camera_from_viewport,
    pack_camera_ubo,
)
from render_graphics.atlas_registry import AtlasRegistry, load_default_atlas
from render_graphics.instancing import (
    INSTANCE_STRIDE,
    TEXTURED_INSTANCE_STRIDE,
    UNIT_QUAD_VERTEX_COUNT,
    build_unit_quad_vertices,
    demo_sprite_field,
    instance_count,
    pack_colored_quads,
    pack_sprite_instances,
    pack_textured_sprite_instances,
    textured_instance_count,
)
from render_graphics.instance_pipeline import (
    InstancedQuadPipeline,
    create_instanced_quad_pipeline,
    destroy_instanced_quad_pipeline,
    record_instanced_draw,
    upload_instances,
)
from render_graphics.textured_pipeline import (
    TexturedInstancedPipeline,
    create_textured_instanced_pipeline,
    destroy_textured_instanced_pipeline,
    prepare_textured_instances,
    record_textured_draw,
    record_textured_instance_upload,
)
from render_graphics.ortho_renderer import OrthoFrameRenderer

__all__ = [
    "AtlasRegistry",
    "CAMERA_UBO_SIZE",
    "INSTANCE_STRIDE",
    "InstancedQuadPipeline",
    "OrthoFrameRenderer",
    "TEXTURED_INSTANCE_STRIDE",
    "TexturedInstancedPipeline",
    "UNIT_QUAD_VERTEX_COUNT",
    "build_unit_quad_vertices",
    "build_view_projection",
    "camera_from_viewport",
    "create_instanced_quad_pipeline",
    "create_textured_instanced_pipeline",
    "demo_sprite_field",
    "destroy_instanced_quad_pipeline",
    "destroy_textured_instanced_pipeline",
    "instance_count",
    "load_default_atlas",
    "pack_camera_ubo",
    "pack_colored_quads",
    "pack_sprite_instances",
    "pack_textured_sprite_instances",
    "record_instanced_draw",
    "prepare_textured_instances",
    "record_textured_draw",
    "record_textured_instance_upload",
    "textured_instance_count",
    "upload_instances",
]
