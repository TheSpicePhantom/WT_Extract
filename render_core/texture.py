"""GPU-Textur-Erstellung und Upload — ausschließlich Vulkan/GPU-Speicher."""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403

from render_core.buffer import create_buffer, destroy_buffer, find_memory_type, upload_to_buffer
from render_core.vk_types import (
    VkDevice,
    VkDeviceMemory,
    VkImage,
    VkImageView,
    VkPhysicalDevice,
    VkQueue,
    VkSampler,
)


@dataclass(frozen=True, slots=True)
class GpuTexture:
    image: VkImage
    memory: VkDeviceMemory
    view: VkImageView
    sampler: VkSampler
    width: int
    height: int


def create_nearest_sampler(device: VkDevice) -> VkSampler:
    create_info = VkSamplerCreateInfo(
        magFilter=VK_FILTER_NEAREST,
        minFilter=VK_FILTER_NEAREST,
        addressModeU=VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE,
        addressModeV=VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE,
        addressModeW=VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE,
        anisotropyEnable=VK_FALSE,
        maxAnisotropy=1.0,
        borderColor=VK_BORDER_COLOR_INT_OPAQUE_BLACK,
        unnormalizedCoordinates=VK_FALSE,
        compareEnable=VK_FALSE,
        compareOp=VK_COMPARE_OP_ALWAYS,
        mipLodBias=0.0,
        minLod=0.0,
        maxLod=0.0,
    )
    return vkCreateSampler(device, create_info, None)


def _create_image(
    physical: VkPhysicalDevice,
    device: VkDevice,
    width: int,
    height: int,
) -> tuple[VkImage, VkDeviceMemory]:
    image_info = VkImageCreateInfo(
        imageType=VK_IMAGE_TYPE_2D,
        format=VK_FORMAT_R8G8B8A8_UNORM,
        extent=VkExtent3D(width=width, height=height, depth=1),
        mipLevels=1,
        arrayLayers=1,
        samples=VK_SAMPLE_COUNT_1_BIT,
        tiling=VK_IMAGE_TILING_OPTIMAL,
        usage=VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT,
        sharingMode=VK_SHARING_MODE_EXCLUSIVE,
        initialLayout=VK_IMAGE_LAYOUT_UNDEFINED,
    )
    image = vkCreateImage(device, image_info, None)
    requirements = vkGetImageMemoryRequirements(device, image)
    memory_type = find_memory_type(
        physical,
        requirements.memoryTypeBits,
        VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
    )
    memory = vkAllocateMemory(
        device,
        VkMemoryAllocateInfo(allocationSize=requirements.size, memoryTypeIndex=memory_type),
        None,
    )
    vkBindImageMemory(device, image, memory, 0)
    return image, memory


def _create_image_view(device: VkDevice, image: VkImage) -> VkImageView:
    create_info = VkImageViewCreateInfo(
        image=image,
        viewType=VK_IMAGE_VIEW_TYPE_2D,
        format=VK_FORMAT_R8G8B8A8_UNORM,
        components=VkComponentMapping(
            r=VK_COMPONENT_SWIZZLE_IDENTITY,
            g=VK_COMPONENT_SWIZZLE_IDENTITY,
            b=VK_COMPONENT_SWIZZLE_IDENTITY,
            a=VK_COMPONENT_SWIZZLE_IDENTITY,
        ),
        subresourceRange=VkImageSubresourceRange(
            aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
            baseMipLevel=0,
            levelCount=1,
            baseArrayLayer=0,
            layerCount=1,
        ),
    )
    return vkCreateImageView(device, create_info, None)


def _run_one_shot_commands(
    device: VkDevice,
    queue: VkQueue,
    queue_family_index: int,
    record_fn,
) -> None:
    pool_info = VkCommandPoolCreateInfo(
        queueFamilyIndex=queue_family_index,
        flags=VK_COMMAND_POOL_CREATE_TRANSIENT_BIT,
    )
    command_pool = vkCreateCommandPool(device, pool_info, None)
    alloc_info = VkCommandBufferAllocateInfo(
        commandPool=command_pool,
        level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,
        commandBufferCount=1,
    )
    command_buffer = vkAllocateCommandBuffers(device, alloc_info)[0]
    begin_info = VkCommandBufferBeginInfo(flags=VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)
    vkBeginCommandBuffer(command_buffer, begin_info)
    record_fn(command_buffer)
    vkEndCommandBuffer(command_buffer)
    submit_info = VkSubmitInfo(commandBufferCount=1, pCommandBuffers=[command_buffer])
    vkQueueSubmit(queue, 1, [submit_info], VK_NULL_HANDLE)
    vkQueueWaitIdle(queue)
    vkFreeCommandBuffers(device, command_pool, 1, [command_buffer])
    vkDestroyCommandPool(device, command_pool, None)


def create_texture_rgba8(
    physical: VkPhysicalDevice,
    device: VkDevice,
    queue: VkQueue,
    queue_family_index: int,
    width: int,
    height: int,
    rgba_bytes: bytes,
) -> GpuTexture:
    expected = width * height * 4
    if len(rgba_bytes) != expected:
        raise ValueError(f"RGBA-Daten: erwartet {expected} Bytes, erhalten {len(rgba_bytes)}.")

    image, memory = _create_image(physical, device, width, height)
    view = _create_image_view(device, image)
    sampler = create_nearest_sampler(device)

    staging_buffer, staging_memory = create_buffer(
        physical,
        device,
        len(rgba_bytes),
        VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
    )
    upload_to_buffer(device, staging_memory, rgba_bytes)

    def record(command_buffer) -> None:
        barrier_to_transfer = VkImageMemoryBarrier(
            oldLayout=VK_IMAGE_LAYOUT_UNDEFINED,
            newLayout=VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            image=image,
            subresourceRange=VkImageSubresourceRange(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                baseMipLevel=0,
                levelCount=1,
                baseArrayLayer=0,
                layerCount=1,
            ),
            srcAccessMask=0,
            dstAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,
        )
        vkCmdPipelineBarrier(
            command_buffer,
            VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            VK_PIPELINE_STAGE_TRANSFER_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [barrier_to_transfer],
        )

        region = VkBufferImageCopy(
            bufferOffset=0,
            bufferRowLength=0,
            bufferImageHeight=0,
            imageSubresource=VkImageSubresourceLayers(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                mipLevel=0,
                baseArrayLayer=0,
                layerCount=1,
            ),
            imageOffset=VkOffset3D(0, 0, 0),
            imageExtent=VkExtent3D(width=width, height=height, depth=1),
        )
        vkCmdCopyBufferToImage(
            command_buffer,
            staging_buffer,
            image,
            VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            1,
            [region],
        )

        barrier_to_shader = VkImageMemoryBarrier(
            oldLayout=VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            newLayout=VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
            srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            image=image,
            subresourceRange=VkImageSubresourceRange(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                baseMipLevel=0,
                levelCount=1,
                baseArrayLayer=0,
                layerCount=1,
            ),
            srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,
            dstAccessMask=VK_ACCESS_SHADER_READ_BIT,
        )
        vkCmdPipelineBarrier(
            command_buffer,
            VK_PIPELINE_STAGE_TRANSFER_BIT,
            VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [barrier_to_shader],
        )

    _run_one_shot_commands(device, queue, queue_family_index, record)
    destroy_buffer(device, staging_buffer, staging_memory)
    return GpuTexture(image=image, memory=memory, view=view, sampler=sampler, width=width, height=height)


def destroy_texture(device: VkDevice, texture: GpuTexture) -> None:
    vkDestroySampler(device, texture.sampler, None)
    vkDestroyImageView(device, texture.view, None)
    vkDestroyImage(device, texture.image, None)
    vkFreeMemory(device, texture.memory, None)
