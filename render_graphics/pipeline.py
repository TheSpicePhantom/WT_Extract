"""Graphics Pipeline, Descriptors und Draw-Setup für 2D-Orthographic."""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403

from render_core.buffer import destroy_buffer, upload_device_local_buffer
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
from render_graphics.debug_grid import VERTEX_STRIDE
from render_graphics.shaders.loader import load_spirv


@dataclass
class ColoredPipeline:
    pipeline: VkPipeline
    layout: VkPipelineLayout
    vertex_buffer: VkBuffer
    vertex_memory: VkDeviceMemory
    vertex_count: int
    vert_shader: VkShaderModule
    frag_shader: VkShaderModule


def _create_shader_module(device: VkDevice, code: bytes) -> VkShaderModule:
    import ctypes

    if len(code) % 4 != 0:
        raise VulkanSetupError("SPIR-V Code-Länge muss durch 4 teilbar sein.")
    words = (ctypes.c_uint32 * (len(code) // 4)).from_buffer_copy(code)
    create_info = VkShaderModuleCreateInfo(codeSize=len(code), pCode=words)
    return vkCreateShaderModule(device, create_info, None)


def create_colored_pipeline(
    device: GpuDevice,
    render_pass: VkRenderPass,
    vertex_bytes: bytes,
) -> ColoredPipeline:
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

    vertex_buffer, vertex_memory = upload_device_local_buffer(
        device.physical,
        device.logical,
        device.graphics_queue,
        device.queue_family_indices.graphics,
        vertex_bytes,
        VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
    )

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
        raise VulkanSetupError("Graphics Pipeline konnte nicht erstellt werden.")
    pipeline = pipeline_result[0] if hasattr(pipeline_result, "__getitem__") else pipeline_result

    return ColoredPipeline(
        pipeline=pipeline,
        layout=layout,
        vertex_buffer=vertex_buffer,
        vertex_memory=vertex_memory,
        vertex_count=len(vertex_bytes) // VERTEX_STRIDE,
        vert_shader=vert_shader,
        frag_shader=frag_shader,
    )


def destroy_colored_pipeline(device: VkDevice, colored: ColoredPipeline) -> None:
    vkDestroyPipeline(device, colored.pipeline, None)
    vkDestroyPipelineLayout(device, colored.layout, None)
    vkDestroyShaderModule(device, colored.vert_shader, None)
    vkDestroyShaderModule(device, colored.frag_shader, None)
    destroy_buffer(device, colored.vertex_buffer, colored.vertex_memory)


def record_colored_draw(
    command_buffer: VkCommandBuffer,
    colored: ColoredPipeline,
    extent,
    camera_ubo: bytes,
) -> None:
    from vulkan import ffi

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
    vkCmdBindPipeline(command_buffer, VK_PIPELINE_BIND_POINT_GRAPHICS, colored.pipeline)
    vkCmdPushConstants(
        command_buffer,
        colored.layout,
        VK_SHADER_STAGE_VERTEX_BIT,
        0,
        CAMERA_UBO_SIZE,
        push_data,
    )
    vkCmdBindVertexBuffers(command_buffer, 0, 1, [colored.vertex_buffer], [0])
    vkCmdDraw(command_buffer, colored.vertex_count, 1, 0, 0)
