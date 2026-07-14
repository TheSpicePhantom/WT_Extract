"""Mid-Level Orthographic Renderer — konsumiert RenderFrame + GPU-Kamera."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from render_core.gpu_renderer import GpuRenderer
from render_core.policy import assert_gpu_only
from render_core.staging import FrameStagingUploader
from render_core.vk_types import VkCommandBuffer, VkExtent2D, VkRenderPass
from render_graphics.atlas_registry import (
    AtlasRegistry,
    destroy_atlas_registry,
    load_default_atlas,
)
from render_graphics.camera import build_view_projection, camera_from_viewport, pack_camera_ubo
from render_graphics.debug_grid import build_world_grid_vertices
from render_graphics.tile_layer import pack_textured_tiles_and_sprites
from render_graphics.colored_overlay_pipeline import (
    ColoredOverlayPipeline,
    create_colored_overlay_pipeline,
    destroy_colored_overlay_pipeline,
    prepare_colored_overlay,
    record_colored_overlay_draw,
    record_colored_overlay_upload,
)
from render_graphics.pipeline import (
    ColoredPipeline,
    create_colored_pipeline,
    destroy_colored_pipeline,
    record_colored_draw,
)
from render_graphics.textured_pipeline import (
    TexturedInstancedPipeline,
    create_textured_instanced_pipeline,
    destroy_textured_instanced_pipeline,
    prepare_textured_instances,
    record_textured_draw,
    record_textured_instance_upload,
)
from render_scene.types import CameraData, RenderFrame
from wt_platform.window import Window


@dataclass
class OrthoFrameRenderer:
    """GPU-Renderer mit orthographischer Kamera — kein CPU-Fallback."""

    window: Window
    gpu: GpuRenderer
    pipeline: ColoredPipeline
    textured_pipeline: TexturedInstancedPipeline
    overlay_pipeline: ColoredOverlayPipeline
    overlay_staging: FrameStagingUploader
    atlas_registry: AtlasRegistry
    _bound_render_pass: VkRenderPass = field(default=None)
    _camera_ubo: bytes = field(default_factory=lambda: pack_camera_ubo(
        build_view_projection(camera_from_viewport(0.0, 0.0, 1.0, 1280, 720))
    ))

    @classmethod
    def create(
        cls,
        window: Window,
        enable_validation: bool = False,
        atlas_dir: Path | None = None,
    ) -> OrthoFrameRenderer:
        assert_gpu_only("OrthoFrameRenderer.create")
        gpu = GpuRenderer.create(window, enable_validation=enable_validation)
        atlas_registry = load_default_atlas(gpu.device, atlas_dir)
        grid_bytes = build_world_grid_vertices()
        pipeline = create_colored_pipeline(
            gpu.device,
            gpu.framebuffers.render_pass,
            grid_bytes,
        )
        textured_pipeline = create_textured_instanced_pipeline(
            gpu.device,
            gpu.framebuffers.render_pass,
            atlas_registry,
        )
        overlay_pipeline = create_colored_overlay_pipeline(
            gpu.device,
            gpu.framebuffers.render_pass,
        )
        overlay_staging = FrameStagingUploader.create(gpu.device.physical, gpu.device.logical)
        return cls(
            window=window,
            gpu=gpu,
            pipeline=pipeline,
            textured_pipeline=textured_pipeline,
            overlay_pipeline=overlay_pipeline,
            overlay_staging=overlay_staging,
            atlas_registry=atlas_registry,
            _bound_render_pass=gpu.framebuffers.render_pass,
        )

    def draw(self, frame: RenderFrame, *, timing_fn=None) -> None:
        assert_gpu_only("OrthoFrameRenderer.draw")
        t_sync = time.perf_counter()
        self._sync_pipeline_for_swapchain()
        if timing_fn is not None:
            sync_ms = (time.perf_counter() - t_sync) * 1000.0
            if sync_ms > 0.0:
                timing_fn("render_sync_pipeline_ms", sync_ms)

        camera = self._normalize_camera(frame.camera)
        t_pack = time.perf_counter()
        self._camera_ubo = pack_camera_ubo(build_view_projection(camera))
        instance_bytes = pack_textured_tiles_and_sprites(frame.tile_chunks, frame.sprites)
        if timing_fn is not None:
            timing_fn("render_pack_ms", (time.perf_counter() - t_pack) * 1000.0)
        overlay_bytes = frame.debug_overlay_vertices or b""
        draw_frame_index = [-1]

        def prepare(frame_index: int) -> None:
            t_prepare = time.perf_counter()
            draw_frame_index[0] = frame_index
            assert self.gpu.staging is not None
            prepare_textured_instances(
                self.textured_pipeline,
                self.gpu.device,
                self.gpu.staging,
                instance_bytes,
                frame_index,
            )
            prepare_colored_overlay(
                self.overlay_pipeline,
                self.gpu.device,
                self.overlay_staging,
                overlay_bytes,
                frame_index,
            )
            if timing_fn is not None:
                timing_fn("render_prepare_ms", (time.perf_counter() - t_prepare) * 1000.0)

        def pre_render(frame_index: int, command_buffer: VkCommandBuffer) -> None:
            assert self.gpu.staging is not None
            record_textured_instance_upload(
                command_buffer,
                self.gpu.staging,
                self.textured_pipeline,
                frame_index,
            )
            record_colored_overlay_upload(
                command_buffer,
                self.overlay_staging,
                self.overlay_pipeline,
                frame_index,
            )

        def record(command_buffer: VkCommandBuffer, extent: VkExtent2D) -> None:
            frame_index = draw_frame_index[0]
            record_colored_draw(command_buffer, self.pipeline, extent, self._camera_ubo)
            record_textured_draw(
                command_buffer,
                self.textured_pipeline,
                extent,
                self._camera_ubo,
                frame_index,
            )
            record_colored_overlay_draw(
                command_buffer,
                self.overlay_pipeline,
                extent,
                self._camera_ubo,
                frame_index,
            )

        swapchain_recreated = True
        for _ in range(8):
            if not swapchain_recreated:
                break
            swapchain_recreated = self.gpu.draw_frame_with_record(
                record_fn=record,
                clear_color=frame.clear_color,
                prepare_fn=prepare,
                pre_render_fn=pre_render,
                timing_fn=timing_fn,
            )
            if swapchain_recreated:
                self._sync_pipeline_for_swapchain()
        else:
            self.gpu.draw_frame_with_record(
                record_fn=record,
                clear_color=frame.clear_color,
                prepare_fn=prepare,
                pre_render_fn=pre_render,
                timing_fn=timing_fn,
            )

    def handle_surface_resize(self) -> None:
        """Nach Fenster-/Vollbild-Wechsel — Swapchain + Pipelines synchron erneuern."""
        self.gpu.recreate_swapchain_for_surface_change()
        self._sync_pipeline_for_swapchain()

    def _normalize_camera(self, camera: CameraData) -> CameraData:
        width = max(camera.viewport_width, 1)
        height = max(camera.viewport_height, 1)
        if width == camera.viewport_width and height == camera.viewport_height:
            return camera
        return CameraData(
            position_x=camera.position_x,
            position_y=camera.position_y,
            zoom=camera.zoom,
            viewport_width=width,
            viewport_height=height,
        )

    def _sync_pipeline_for_swapchain(self) -> None:
        current_pass = self.gpu.framebuffers.render_pass
        if current_pass == self._bound_render_pass:
            return
        destroy_colored_pipeline(self.gpu.device.logical, self.pipeline)
        destroy_textured_instanced_pipeline(self.gpu.device.logical, self.textured_pipeline)
        destroy_colored_overlay_pipeline(self.gpu.device.logical, self.overlay_pipeline)
        grid_bytes = build_world_grid_vertices()
        self.pipeline = create_colored_pipeline(
            self.gpu.device,
            current_pass,
            grid_bytes,
        )
        self.textured_pipeline = create_textured_instanced_pipeline(
            self.gpu.device,
            current_pass,
            self.atlas_registry,
        )
        self.overlay_pipeline = create_colored_overlay_pipeline(
            self.gpu.device,
            current_pass,
        )
        self._bound_render_pass = current_pass

    @property
    def sprite_catalog(self):
        return self.atlas_registry.catalog

    def destroy(self) -> None:
        destroy_colored_pipeline(self.gpu.device.logical, self.pipeline)
        destroy_textured_instanced_pipeline(self.gpu.device.logical, self.textured_pipeline)
        destroy_colored_overlay_pipeline(self.gpu.device.logical, self.overlay_pipeline)
        self.overlay_staging.destroy()
        destroy_atlas_registry(self.gpu.device.logical, self.atlas_registry)
        self.gpu.destroy()
        self._bound_render_pass = None
