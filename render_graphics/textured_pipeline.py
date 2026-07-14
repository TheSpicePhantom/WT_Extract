"""Textured Instanced-Quad-Pipeline — Atlas + SpriteRect SSBO."""

from __future__ import annotations

from dataclasses import dataclass, field

from vulkan import *  # noqa: F403

from render_core.buffer import (
    create_buffer,
    destroy_buffer,
    upload_device_local_buffer,
)
from render_core.device import GpuDevice
from render_core.errors import VulkanSetupError
from render_core.frame_sync import MAX_FRAMES_IN_FLIGHT
from render_core.staging import FrameStagingUploader
from render_core.vk_types import (
    VkBuffer,
    VkCommandBuffer,
    VkDescriptorPool,
    VkDescriptorSet,
    VkDescriptorSetLayout,
    VkDevice,
    VkDeviceMemory,
    VkPipeline,
    VkPipelineLayout,
    VkRenderPass,
    VkShaderModule,
)
from render_graphics.atlas_registry import AtlasRegistry, SPRITE_RECT_GPU_STRIDE
from render_graphics.camera import CAMERA_UBO_SIZE
from render_graphics.instancing import (
    TEXTURED_INSTANCE_STRIDE,
    UNIT_QUAD_VERTEX_COUNT,
    build_unit_quad_vertices,
    textured_instance_count,
)
from render_graphics.pipeline import _create_shader_module
from render_graphics.shaders.loader import load_spirv

INITIAL_INSTANCE_CAPACITY = 4096


@dataclass
class TexturedInstancedPipeline:
    pipeline: VkPipeline
    layout: VkPipelineLayout
    descriptor_set_layout: VkDescriptorSetLayout
    descriptor_pool: VkDescriptorPool
    descriptor_set: VkDescriptorSet
    unit_quad_buffer: VkBuffer
    unit_quad_memory: VkDeviceMemory
    instance_buffers: tuple[VkBuffer, ...]
    instance_memories: tuple[VkDeviceMemory, ...]
    instance_buffer_size: int
    vert_shader: VkShaderModule = field(repr=False)
    frag_shader: VkShaderModule = field(repr=False)
    instance_count: int = 0
    pending_upload_size: int = 0
    active_frame_index: int = 0


def _create_descriptor_set_layout(device: VkDevice) -> VkDescriptorSetLayout:
    bindings = [
        VkDescriptorSetLayoutBinding(
            binding=0,
            descriptorType=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
            descriptorCount=1,
            stageFlags=VK_SHADER_STAGE_FRAGMENT_BIT,
        ),
        VkDescriptorSetLayoutBinding(
            binding=1,
            descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
            descriptorCount=1,
            stageFlags=VK_SHADER_STAGE_VERTEX_BIT,
        ),
    ]
    return vkCreateDescriptorSetLayout(
        device,
        VkDescriptorSetLayoutCreateInfo(bindingCount=len(bindings), pBindings=bindings),
        None,
    )


def _create_descriptor_pool(device: VkDevice) -> VkDescriptorPool:
    pool_sizes = [
        VkDescriptorPoolSize(type=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, descriptorCount=1),
        VkDescriptorPoolSize(type=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER, descriptorCount=1),
    ]
    return vkCreateDescriptorPool(
        device,
        VkDescriptorPoolCreateInfo(
            maxSets=1,
            poolSizeCount=len(pool_sizes),
            pPoolSizes=pool_sizes,
        ),
        None,
    )


def _allocate_descriptor_set(
    device: VkDevice,
    pool: VkDescriptorPool,
    layout: VkDescriptorSetLayout,
) -> VkDescriptorSet:
    alloc_info = VkDescriptorSetAllocateInfo(
        descriptorPool=pool,
        descriptorSetCount=1,
        pSetLayouts=[layout],
    )
    return vkAllocateDescriptorSets(device, alloc_info)[0]


def _update_descriptor_set(
    device: VkDevice,
    descriptor_set: VkDescriptorSet,
    registry: AtlasRegistry,
) -> None:
    lookup_size = len(registry.sprite_rects) * SPRITE_RECT_GPU_STRIDE
    image_info = VkDescriptorImageInfo(
        sampler=registry.gpu_texture.sampler,
        imageView=registry.gpu_texture.view,
        imageLayout=VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
    )
    buffer_info = VkDescriptorBufferInfo(
        buffer=registry.sprite_lookup_buffer,
        offset=0,
        range=max(lookup_size, SPRITE_RECT_GPU_STRIDE),
    )
    writes = [
        VkWriteDescriptorSet(
            dstSet=descriptor_set,
            dstBinding=0,
            dstArrayElement=0,
            descriptorType=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
            descriptorCount=1,
            pImageInfo=[image_info],
        ),
        VkWriteDescriptorSet(
            dstSet=descriptor_set,
            dstBinding=1,
            dstArrayElement=0,
            descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
            descriptorCount=1,
            pBufferInfo=[buffer_info],
        ),
    ]
    vkUpdateDescriptorSets(device, len(writes), writes, 0, None)


def create_textured_instanced_pipeline(
    device: GpuDevice,
    render_pass: VkRenderPass,
    registry: AtlasRegistry,
    initial_capacity: int = INITIAL_INSTANCE_CAPACITY,
) -> TexturedInstancedPipeline:
    vert_code = load_spirv("textured_instanced_vert.spv")
    frag_code = load_spirv("textured_instanced_frag.spv")
    vert_shader = _create_shader_module(device.logical, vert_code)
    frag_shader = _create_shader_module(device.logical, frag_code)

    descriptor_set_layout = _create_descriptor_set_layout(device.logical)
    descriptor_pool = _create_descriptor_pool(device.logical)
    descriptor_set = _allocate_descriptor_set(device.logical, descriptor_pool, descriptor_set_layout)
    _update_descriptor_set(device.logical, descriptor_set, registry)

    push_constant_range = VkPushConstantRange(
        stageFlags=VK_SHADER_STAGE_VERTEX_BIT,
        offset=0,
        size=CAMERA_UBO_SIZE,
    )
    layout = vkCreatePipelineLayout(
        device.logical,
        VkPipelineLayoutCreateInfo(
            setLayoutCount=1,
            pSetLayouts=[descriptor_set_layout],
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

    instance_buffer_size = max(initial_capacity, 1) * TEXTURED_INSTANCE_STRIDE
    instance_buffers: list[VkBuffer] = []
    instance_memories: list[VkDeviceMemory] = []
    for _ in range(MAX_FRAMES_IN_FLIGHT):
        buffer, memory = create_buffer(
            device.physical,
            device.logical,
            instance_buffer_size,
            VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
        )
        instance_buffers.append(buffer)
        instance_memories.append(memory)

    bindings = [
        VkVertexInputBindingDescription(
            binding=0,
            stride=8,
            inputRate=VK_VERTEX_INPUT_RATE_VERTEX,
        ),
        VkVertexInputBindingDescription(
            binding=1,
            stride=TEXTURED_INSTANCE_STRIDE,
            inputRate=VK_VERTEX_INPUT_RATE_INSTANCE,
        ),
    ]
    attrs = [
        VkVertexInputAttributeDescription(
            location=0, binding=0, format=VK_FORMAT_R32G32_SFLOAT, offset=0
        ),
        VkVertexInputAttributeDescription(
            location=1, binding=1, format=VK_FORMAT_R32G32_SFLOAT, offset=0
        ),
        VkVertexInputAttributeDescription(
            location=2, binding=1, format=VK_FORMAT_R32G32B32A32_SFLOAT, offset=8
        ),
        VkVertexInputAttributeDescription(
            location=3, binding=1, format=VK_FORMAT_R32_UINT, offset=24
        ),
        VkVertexInputAttributeDescription(
            location=4, binding=1, format=VK_FORMAT_R32_UINT, offset=28
        ),
        VkVertexInputAttributeDescription(
            location=5, binding=1, format=VK_FORMAT_R32_UINT, offset=32
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

    return TexturedInstancedPipeline(
        pipeline=pipeline,
        layout=layout,
        descriptor_set_layout=descriptor_set_layout,
        descriptor_pool=descriptor_pool,
        descriptor_set=descriptor_set,
        unit_quad_buffer=unit_quad_buffer,
        unit_quad_memory=unit_quad_memory,
        instance_buffers=tuple(instance_buffers),
        instance_memories=tuple(instance_memories),
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
        raise VulkanSetupError("Textured-Pipeline konnte nicht erstellt werden.")
    return pipeline_result[0] if hasattr(pipeline_result, "__getitem__") else pipeline_result


def _ensure_instance_buffer_capacity(
    pipeline: TexturedInstancedPipeline,
    device: GpuDevice,
    required_size: int,
) -> None:
    if required_size <= pipeline.instance_buffer_size:
        return

    vkDeviceWaitIdle(device.logical)
    for buffer, memory in zip(pipeline.instance_buffers, pipeline.instance_memories, strict=True):
        destroy_buffer(device.logical, buffer, memory)

    new_size = max(required_size, pipeline.instance_buffer_size * 2)
    instance_buffers: list[VkBuffer] = []
    instance_memories: list[VkDeviceMemory] = []
    for _ in range(MAX_FRAMES_IN_FLIGHT):
        buffer, memory = create_buffer(
            device.physical,
            device.logical,
            new_size,
            VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
        )
        instance_buffers.append(buffer)
        instance_memories.append(memory)

    pipeline.instance_buffers = tuple(instance_buffers)
    pipeline.instance_memories = tuple(instance_memories)
    pipeline.instance_buffer_size = new_size


def prepare_textured_instances(
    pipeline: TexturedInstancedPipeline,
    device: GpuDevice,
    staging: FrameStagingUploader,
    instance_bytes: bytes,
    frame_index: int,
) -> None:
    """CPU: Instanzdaten in Frame-Staging schreiben (nach Fence-Wait, vor Command-Buffer-Record)."""
    if not (0 <= frame_index < MAX_FRAMES_IN_FLIGHT):
        raise ValueError(f"frame_index muss 0..{MAX_FRAMES_IN_FLIGHT - 1} sein, erhalten {frame_index}.")

    count = textured_instance_count(instance_bytes)
    pipeline.instance_count = count
    pipeline.pending_upload_size = 0
    pipeline.active_frame_index = frame_index
    if count == 0:
        return

    required_size = len(instance_bytes)
    _ensure_instance_buffer_capacity(pipeline, device, required_size)
    staging.write(frame_index, instance_bytes)
    pipeline.pending_upload_size = required_size


def record_textured_instance_upload(
    command_buffer: VkCommandBuffer,
    staging: FrameStagingUploader,
    pipeline: TexturedInstancedPipeline,
    frame_index: int,
) -> None:
    """GPU: Staging → Instance-Vertex-Buffer im Frame-Command-Buffer (vor Render-Pass)."""
    size = pipeline.pending_upload_size
    if size <= 0 or pipeline.instance_count <= 0:
        return

    staging.record_copy_to_vertex_buffer(
        command_buffer,
        frame_index,
        pipeline.instance_buffers[frame_index],
        size,
    )


def destroy_textured_instanced_pipeline(device: VkDevice, pipeline: TexturedInstancedPipeline) -> None:
    vkDestroyPipeline(device, pipeline.pipeline, None)
    vkDestroyPipelineLayout(device, pipeline.layout, None)
    vkDestroyDescriptorPool(device, pipeline.descriptor_pool, None)
    vkDestroyDescriptorSetLayout(device, pipeline.descriptor_set_layout, None)
    vkDestroyShaderModule(device, pipeline.vert_shader, None)
    vkDestroyShaderModule(device, pipeline.frag_shader, None)
    destroy_buffer(device, pipeline.unit_quad_buffer, pipeline.unit_quad_memory)
    for buffer, memory in zip(pipeline.instance_buffers, pipeline.instance_memories, strict=True):
        destroy_buffer(device, buffer, memory)


def record_textured_draw(
    command_buffer: VkCommandBuffer,
    pipeline: TexturedInstancedPipeline,
    extent,
    camera_ubo: bytes,
    frame_index: int = 0,
) -> None:
    from vulkan import ffi

    if pipeline.instance_count <= 0:
        return
    if not (0 <= frame_index < len(pipeline.instance_buffers)):
        raise ValueError(f"frame_index außerhalb der Instance-Buffer: {frame_index}")
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
    vkCmdBindDescriptorSets(
        command_buffer,
        VK_PIPELINE_BIND_POINT_GRAPHICS,
        pipeline.layout,
        0,
        1,
        [pipeline.descriptor_set],
        0,
        None,
    )
    vkCmdPushConstants(
        command_buffer,
        pipeline.layout,
        VK_SHADER_STAGE_VERTEX_BIT,
        0,
        CAMERA_UBO_SIZE,
        push_data,
    )
    vkCmdBindVertexBuffers(command_buffer, 0, 1, [pipeline.unit_quad_buffer], [0])
    instance_buffer = pipeline.instance_buffers[frame_index]
    vkCmdBindVertexBuffers(command_buffer, 1, 1, [instance_buffer], [0])
    vkCmdDraw(
        command_buffer,
        UNIT_QUAD_VERTEX_COUNT,
        pipeline.instance_count,
        0,
        0,
    )
