"""Instanced-Quad-Pipeline — ein GPU-Draw für viele einfarbige Quads."""

from __future__ import annotations

from dataclasses import dataclass, field

from vulkan import *  # noqa: F403

from render_core.buffer import (
    copy_to_device_local_buffer,
    create_buffer,
    destroy_buffer,
    upload_device_local_buffer,
)
from render_core.device import GpuDevice
from render_core.errors import VulkanSetupError
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
from render_graphics.instancing import (
    INSTANCE_STRIDE,
    UNIT_QUAD_VERTEX_COUNT,
    build_unit_quad_vertices,
)
from render_graphics.pipeline import _create_shader_module
from render_graphics.shaders.loader import load_spirv

INITIAL_INSTANCE_CAPACITY = 4096


@dataclass
class InstancedQuadPipeline:
    pipeline: VkPipeline
    layout: VkPipelineLayout
    unit_quad_buffer: VkBuffer
    unit_quad_memory: VkDeviceMemory
    instance_buffer: VkBuffer
    instance_memory: VkDeviceMemory
    instance_buffer_size: int
    vert_shader: VkShaderModule = field(repr=False)
    frag_shader: VkShaderModule = field(repr=False)
    instance_count: int = 0


def create_instanced_quad_pipeline(
    device: GpuDevice,
    render_pass: VkRenderPass,
    initial_capacity: int = INITIAL_INSTANCE_CAPACITY,
) -> InstancedQuadPipeline:
    vert_code = load_spirv("instanced_vert.spv")
    frag_code = load_spirv("instanced_frag.spv")
    vert_shader = _create_shader_module(device.logical, vert_code)
    frag_shader = _create_shader_module(device.logical, frag_code)

    push_constant_range = VkPushConstantRange(
        stageFlags=VK_SHADER_STAGE_VERTEX_BIT,
        offset=0,
        size=CAMERA_UBO_SIZE,
    )
    layout = vkCreatePipelineLayout(
        device.logical,
        VkPipelineLayoutCreateInfo(
            pushConstantRangeCount=1,
            pPushConstantRanges=[push_constant_range],
        ),
        None,
    )

    unit_quad_buffer, unit_quad_memory = upload_device_local_buffer(
        device.physical,
        device.logical,
        device.graphics_queue,
        device.queue_family_indices.graphics,
        build_unit_quad_vertices(),
        VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
    )

    instance_buffer_size = max(initial_capacity, 1) * INSTANCE_STRIDE
    instance_buffer, instance_memory = create_buffer(
        device.physical,
        device.logical,
        instance_buffer_size,
        VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
        VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
    )

    bindings = [
        VkVertexInputBindingDescription(
            binding=0,
            stride=8,
            inputRate=VK_VERTEX_INPUT_RATE_VERTEX,
        ),
        VkVertexInputBindingDescription(
            binding=1,
            stride=INSTANCE_STRIDE,
            inputRate=VK_VERTEX_INPUT_RATE_INSTANCE,
        ),
    ]
    attrs = [
        VkVertexInputAttributeDescription(
            location=0, binding=0, format=VK_FORMAT_R32G32_SFLOAT, offset=0
        ),
        VkVertexInputAttributeDescription(
            location=1, binding=1, format=VK_FORMAT_R32G32B32A32_SFLOAT, offset=0
        ),
        VkVertexInputAttributeDescription(
            location=2, binding=1, format=VK_FORMAT_R32G32B32A32_SFLOAT, offset=16
        ),
    ]

    pipeline = _create_graphics_pipeline(
        device.logical,
        layout,
        render_pass,
        vert_shader,
        frag_shader,
        bindings,
        attrs,
    )

    return InstancedQuadPipeline(
        pipeline=pipeline,
        layout=layout,
        unit_quad_buffer=unit_quad_buffer,
        unit_quad_memory=unit_quad_memory,
        instance_buffer=instance_buffer,
        instance_memory=instance_memory,
        instance_buffer_size=instance_buffer_size,
        vert_shader=vert_shader,
        frag_shader=frag_shader,
    )


def _create_graphics_pipeline(
    device: VkDevice,
    layout: VkPipelineLayout,
    render_pass: VkRenderPass,
    vert_shader: VkShaderModule,
    frag_shader: VkShaderModule,
    bindings: list,
    attrs: list,
) -> VkPipeline:
    vertex_input = VkPipelineVertexInputStateCreateInfo(
        vertexBindingDescriptionCount=len(bindings),
        pVertexBindingDescriptions=bindings,
        vertexAttributeDescriptionCount=len(attrs),
        pVertexAttributeDescriptions=attrs,
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
        blendEnable=VK_FALSE,
    )
    color_blending = VkPipelineColorBlendStateCreateInfo(
        attachmentCount=1,
        pAttachments=[color_blend_attachment],
    )
    dynamic_state = VkPipelineDynamicStateCreateInfo(
        pDynamicStates=[VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR],
    )
    shader_stages = [
        VkPipelineShaderStageCreateInfo(stage=VK_SHADER_STAGE_VERTEX_BIT, module=vert_shader, pName="main"),
        VkPipelineShaderStageCreateInfo(stage=VK_SHADER_STAGE_FRAGMENT_BIT, module=frag_shader, pName="main"),
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
    pipeline_result = vkCreateGraphicsPipelines(device, VK_NULL_HANDLE, 1, [pipeline_info], None)
    if pipeline_result is None:
        raise VulkanSetupError("Instanced-Pipeline konnte nicht erstellt werden.")
    return pipeline_result[0] if hasattr(pipeline_result, "__getitem__") else pipeline_result


def upload_instances(
    pipeline: InstancedQuadPipeline,
    device: GpuDevice,
    instance_bytes: bytes,
) -> None:
    """Instanzdaten auf GPU (DEVICE_LOCAL) — wächst bei Bedarf."""
    from render_graphics.instancing import instance_count

    count = instance_count(instance_bytes)
    pipeline.instance_count = count
    if count == 0:
        return

    required_size = len(instance_bytes)
    if required_size > pipeline.instance_buffer_size:
        destroy_buffer(device.logical, pipeline.instance_buffer, pipeline.instance_memory)
        new_size = max(required_size, pipeline.instance_buffer_size * 2)
        pipeline.instance_buffer, pipeline.instance_memory = create_buffer(
            device.physical,
            device.logical,
            new_size,
            VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
        )
        pipeline.instance_buffer_size = new_size

    copy_to_device_local_buffer(
        device.physical,
        device.logical,
        device.graphics_queue,
        device.queue_family_indices.graphics,
        pipeline.instance_buffer,
        instance_bytes,
    )


def destroy_instanced_quad_pipeline(device: VkDevice, pipeline: InstancedQuadPipeline) -> None:
    vkDestroyPipeline(device, pipeline.pipeline, None)
    vkDestroyPipelineLayout(device, pipeline.layout, None)
    vkDestroyShaderModule(device, pipeline.vert_shader, None)
    vkDestroyShaderModule(device, pipeline.frag_shader, None)
    destroy_buffer(device, pipeline.unit_quad_buffer, pipeline.unit_quad_memory)
    destroy_buffer(device, pipeline.instance_buffer, pipeline.instance_memory)


def record_instanced_draw(
    command_buffer: VkCommandBuffer,
    pipeline: InstancedQuadPipeline,
    extent,
    camera_ubo: bytes,
) -> None:
    from vulkan import ffi

    if pipeline.instance_count <= 0:
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
    vkCmdBindVertexBuffers(command_buffer, 0, 1, [pipeline.unit_quad_buffer], [0])
    vkCmdBindVertexBuffers(command_buffer, 1, 1, [pipeline.instance_buffer], [0])
    vkCmdDraw(
        command_buffer,
        UNIT_QUAD_VERTEX_COUNT,
        pipeline.instance_count,
        0,
        0,
    )
