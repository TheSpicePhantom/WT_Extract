"""Dynamische Colored-Vertex-Pipeline für optionale Debug-Overlays (Chunk-Grenzen)."""

from __future__ import annotations

from dataclasses import dataclass, field

from vulkan import *  # noqa: F403

from render_core.buffer import create_buffer, destroy_buffer
from render_core.device import GpuDevice
from render_core.errors import VulkanSetupError
from render_core.frame_sync import MAX_FRAMES_IN_FLIGHT
from render_core.staging import FrameStagingUploader
from render_core.vk_types import (
    VkBuffer,
    VkCommandBuffer,
    VkDevice,
    VkDeviceMemory,
    VkPipeline,
    VkPipelineLayout,
    VkRenderPass,
    VkShaderModule,
)
from render_graphics.camera import CAMERA_UBO_SIZE
from render_graphics.debug_grid import VERTEX_STRIDE, vertex_count as overlay_vertex_count
from render_graphics.pipeline import _create_shader_module
from render_graphics.shaders.loader import load_spirv

INITIAL_OVERLAY_BUFFER_BYTES = 512 * 1024


@dataclass
class ColoredOverlayPipeline:
    pipeline: VkPipeline
    layout: VkPipelineLayout
    vertex_buffers: tuple[VkBuffer, ...]
    vertex_memories: tuple[VkDeviceMemory, ...]
    vertex_buffer_size: int
    vert_shader: VkShaderModule = field(repr=False)
    frag_shader: VkShaderModule = field(repr=False)
    vertex_count: int = 0
    pending_upload_size: int = 0
    active_frame_index: int = 0


def _create_colored_graphics_pipeline(
    device: GpuDevice,
    render_pass: VkRenderPass,
) -> tuple[VkPipeline, VkPipelineLayout, VkShaderModule, VkShaderModule]:
    vert_code = load_spirv("colored_vert.spv")
    frag_code = load_spirv("colored_frag.spv")
    vert_shader = _create_shader_module(device.logical, vert_code)
    frag_shader = _create_shader_module(device.logical, frag_code)

    push_constant_range = VkPushConstantRange(
        stageFlags=VK_SHADER_STAGE_VERTEX_BIT,
        offset=0,
        size=CAMERA_UBO_SIZE,
    )
    pipeline_layout_info = VkPipelineLayoutCreateInfo(
        pushConstantRangeCount=1,
        pPushConstantRanges=[push_constant_range],
    )
    layout = vkCreatePipelineLayout(device.logical, pipeline_layout_info, None)

    binding_desc = VkVertexInputBindingDescription(
        binding=0,
        stride=VERTEX_STRIDE,
        inputRate=VK_VERTEX_INPUT_RATE_VERTEX,
    )
    attr_desc = [
        VkVertexInputAttributeDescription(location=0, binding=0, format=VK_FORMAT_R32G32_SFLOAT, offset=0),
        VkVertexInputAttributeDescription(location=1, binding=0, format=VK_FORMAT_R32G32B32A32_SFLOAT, offset=8),
    ]
    vertex_input = VkPipelineVertexInputStateCreateInfo(
        vertexBindingDescriptionCount=1,
        pVertexBindingDescriptions=[binding_desc],
        vertexAttributeDescriptionCount=len(attr_desc),
        pVertexAttributeDescriptions=attr_desc,
    )

    input_assembly = VkPipelineInputAssemblyStateCreateInfo(topology=VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST)
    viewport_state = VkPipelineViewportStateCreateInfo(viewportCount=1, scissorCount=1)
    rasterizer = VkPipelineRasterizationStateCreateInfo(
        polygonMode=VK_POLYGON_MODE_FILL,
        cullMode=VK_CULL_MODE_NONE,
        frontFace=VK_FRONT_FACE_COUNTER_CLOCKWISE,
        lineWidth=1.0,
    )
    multisampling = VkPipelineMultisampleStateCreateInfo(rasterizationSamples=VK_SAMPLE_COUNT_1_BIT)
    depth_stencil = VkPipelineDepthStencilStateCreateInfo(
        depthTestEnable=VK_FALSE,
        depthWriteEnable=VK_FALSE,
    )
    color_blend_attachment = VkPipelineColorBlendAttachmentState(
        colorWriteMask=VK_COLOR_COMPONENT_R_BIT
        | VK_COLOR_COMPONENT_G_BIT
        | VK_COLOR_COMPONENT_B_BIT
        | VK_COLOR_COMPONENT_A_BIT,
        blendEnable=VK_TRUE,
        srcColorBlendFactor=VK_BLEND_FACTOR_SRC_ALPHA,
        dstColorBlendFactor=VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA,
        colorBlendOp=VK_BLEND_OP_ADD,
        srcAlphaBlendFactor=VK_BLEND_FACTOR_ONE,
        dstAlphaBlendFactor=VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA,
        alphaBlendOp=VK_BLEND_OP_ADD,
    )
    color_blending = VkPipelineColorBlendStateCreateInfo(
        attachmentCount=1,
        pAttachments=[color_blend_attachment],
    )
    dynamic_state = VkPipelineDynamicStateCreateInfo(
        pDynamicStates=[VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR],
    )

    shader_stages = [
        VkPipelineShaderStageCreateInfo(
            stage=VK_SHADER_STAGE_VERTEX_BIT,
            module=vert_shader,
            pName="main",
        ),
        VkPipelineShaderStageCreateInfo(
            stage=VK_SHADER_STAGE_FRAGMENT_BIT,
            module=frag_shader,
            pName="main",
        ),
    ]

    pipeline_info = VkGraphicsPipelineCreateInfo(
        stageCount=len(shader_stages),
        pStages=shader_stages,
        pVertexInputState=vertex_input,
        pInputAssemblyState=input_assembly,
        pViewportState=viewport_state,
        pRasterizationState=rasterizer,
        pMultisampleState=multisampling,
        pDepthStencilState=depth_stencil,
        pColorBlendState=color_blending,
        pDynamicState=dynamic_state,
        layout=layout,
        renderPass=render_pass,
        subpass=0,
    )

    pipeline_result = vkCreateGraphicsPipelines(device.logical, VK_NULL_HANDLE, 1, [pipeline_info], None)
    if pipeline_result is None:
        raise VulkanSetupError("Colored-Overlay-Pipeline konnte nicht erstellt werden.")
    pipeline = pipeline_result[0] if hasattr(pipeline_result, "__getitem__") else pipeline_result
    return pipeline, layout, vert_shader, frag_shader


def _create_vertex_buffers(device: GpuDevice, size: int) -> tuple[tuple[VkBuffer, ...], tuple[VkDeviceMemory, ...]]:
    buffers: list[VkBuffer] = []
    memories: list[VkDeviceMemory] = []
    for _ in range(MAX_FRAMES_IN_FLIGHT):
        buffer, memory = create_buffer(
            device.physical,
            device.logical,
            size,
            VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
        )
        buffers.append(buffer)
        memories.append(memory)
    return tuple(buffers), tuple(memories)


def _ensure_vertex_buffer_capacity(pipeline: ColoredOverlayPipeline, device: GpuDevice, required_size: int) -> None:
    if required_size <= pipeline.vertex_buffer_size:
        return

    vkDeviceWaitIdle(device.logical)
    for buffer, memory in zip(pipeline.vertex_buffers, pipeline.vertex_memories, strict=True):
        destroy_buffer(device.logical, buffer, memory)

    new_size = max(required_size, pipeline.vertex_buffer_size * 2, INITIAL_OVERLAY_BUFFER_BYTES)
    buffers, memories = _create_vertex_buffers(device, new_size)
    pipeline.vertex_buffers = buffers
    pipeline.vertex_memories = memories
    pipeline.vertex_buffer_size = new_size


def create_colored_overlay_pipeline(device: GpuDevice, render_pass: VkRenderPass) -> ColoredOverlayPipeline:
    pipeline, layout, vert_shader, frag_shader = _create_colored_graphics_pipeline(device, render_pass)
    vertex_buffers, vertex_memories = _create_vertex_buffers(device, INITIAL_OVERLAY_BUFFER_BYTES)
    return ColoredOverlayPipeline(
        pipeline=pipeline,
        layout=layout,
        vertex_buffers=vertex_buffers,
        vertex_memories=vertex_memories,
        vertex_buffer_size=INITIAL_OVERLAY_BUFFER_BYTES,
        vert_shader=vert_shader,
        frag_shader=frag_shader,
    )


def prepare_colored_overlay(
    pipeline: ColoredOverlayPipeline,
    device: GpuDevice,
    staging: FrameStagingUploader,
    vertex_bytes: bytes,
    frame_index: int,
) -> None:
    if not (0 <= frame_index < MAX_FRAMES_IN_FLIGHT):
        raise ValueError(f"frame_index muss 0..{MAX_FRAMES_IN_FLIGHT - 1} sein, erhalten {frame_index}.")

    count = overlay_vertex_count(vertex_bytes)
    pipeline.vertex_count = count
    pipeline.pending_upload_size = 0
    pipeline.active_frame_index = frame_index
    if count == 0:
        return

    required_size = len(vertex_bytes)
    _ensure_vertex_buffer_capacity(pipeline, device, required_size)
    staging.write(frame_index, vertex_bytes)
    pipeline.pending_upload_size = required_size


def record_colored_overlay_upload(
    command_buffer: VkCommandBuffer,
    staging: FrameStagingUploader,
    pipeline: ColoredOverlayPipeline,
    frame_index: int,
) -> None:
    size = pipeline.pending_upload_size
    if size <= 0 or pipeline.vertex_count <= 0:
        return

    staging.record_copy_to_vertex_buffer(
        command_buffer,
        frame_index,
        pipeline.vertex_buffers[frame_index],
        size,
    )


def record_colored_overlay_draw(
    command_buffer: VkCommandBuffer,
    pipeline: ColoredOverlayPipeline,
    extent,
    camera_ubo: bytes,
    frame_index: int,
) -> None:
    from vulkan import ffi

    if pipeline.vertex_count <= 0:
        return
    if len(camera_ubo) != CAMERA_UBO_SIZE:
        raise ValueError(f"camera_ubo muss {CAMERA_UBO_SIZE} Bytes haben.")

    push_data = ffi.new(f"char[{CAMERA_UBO_SIZE}]", camera_ubo)

    viewport = VkViewport(
        x=0.0,
        y=0.0,
        width=float(max(extent.width, 1)),
        height=float(max(extent.height, 1)),
        minDepth=0.0,
        maxDepth=1.0,
    )
    scissor = VkRect2D(
        offset=VkOffset2D(0, 0),
        extent=VkExtent2D(width=max(extent.width, 1), height=max(extent.height, 1)),
    )

    vkCmdSetViewport(command_buffer, 0, 1, [viewport])
    vkCmdSetScissor(command_buffer, 0, 1, [scissor])
    vkCmdBindPipeline(command_buffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline.pipeline)
    vkCmdPushConstants(
        command_buffer,
        pipeline.layout,
        VK_SHADER_STAGE_VERTEX_BIT,
        0,
        CAMERA_UBO_SIZE,
        push_data,
    )
    vkCmdBindVertexBuffers(command_buffer, 0, 1, [pipeline.vertex_buffers[frame_index]], [0])
    vkCmdDraw(command_buffer, pipeline.vertex_count, 1, 0, 0)


def destroy_colored_overlay_pipeline(device: VkDevice, pipeline: ColoredOverlayPipeline) -> None:
    vkDestroyPipeline(device, pipeline.pipeline, None)
    vkDestroyPipelineLayout(device, pipeline.layout, None)
    vkDestroyShaderModule(device, pipeline.vert_shader, None)
    vkDestroyShaderModule(device, pipeline.frag_shader, None)
    for buffer, memory in zip(pipeline.vertex_buffers, pipeline.vertex_memories, strict=True):
        destroy_buffer(device, buffer, memory)
