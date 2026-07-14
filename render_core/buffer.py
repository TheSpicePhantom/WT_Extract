"""GPU-Buffer-Erstellung und Upload — ausschließlich Vulkan/GPU-Speicher."""

from __future__ import annotations

from vulkan import *  # noqa: F403

from render_core.errors import VulkanSetupError
from render_core.vk_types import VkBuffer, VkDevice, VkDeviceMemory, VkPhysicalDevice, VkQueue


def find_memory_type(
    physical: VkPhysicalDevice,
    type_filter: int,
    properties: int,
) -> int:
    memory_props = vkGetPhysicalDeviceMemoryProperties(physical)
    best: int | None = None
    best_score = -1

    for i in range(memory_props.memoryTypeCount):
        if not (type_filter & (1 << i)):
            continue
        flags = memory_props.memoryTypes[i].propertyFlags
        if (flags & properties) != properties:
            continue

        score = 0
        if flags & VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT:
            score += 2
        if flags & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT:
            score += 1
        if score > best_score:
            best_score = score
            best = i

    if best is None:
        raise VulkanSetupError("Passender Vulkan Memory Type nicht gefunden.")
    return best


def create_buffer(
    physical: VkPhysicalDevice,
    device: VkDevice,
    size: int,
    usage: int,
    properties: int,
) -> tuple[VkBuffer, VkDeviceMemory]:
    buffer_info = VkBufferCreateInfo(size=size, usage=usage, sharingMode=VK_SHARING_MODE_EXCLUSIVE)
    buffer = vkCreateBuffer(device, buffer_info, None)

    mem_requirements = vkGetBufferMemoryRequirements(device, buffer)
    memory_type = find_memory_type(physical, mem_requirements.memoryTypeBits, properties)
    alloc_info = VkMemoryAllocateInfo(
        allocationSize=mem_requirements.size,
        memoryTypeIndex=memory_type,
    )
    memory = vkAllocateMemory(device, alloc_info, None)
    vkBindBufferMemory(device, buffer, memory, 0)
    return buffer, memory


def upload_to_buffer(device: VkDevice, memory: VkDeviceMemory, data: bytes, offset: int = 0) -> None:
    mapped = vkMapMemory(device, memory, offset, len(data), 0)
    mapped[:] = data
    vkUnmapMemory(device, memory)


def upload_device_local_buffer(
    physical: VkPhysicalDevice,
    device: VkDevice,
    queue: VkQueue,
    queue_family_index: int,
    data: bytes,
    usage: int,
) -> tuple[VkBuffer, VkDeviceMemory]:
    """Staging-Upload in DEVICE_LOCAL — Vertex-Daten müssen GPU-seitig lesbar sein."""
    staging_buffer, staging_memory = create_buffer(
        physical,
        device,
        len(data),
        VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
    )
    device_buffer, device_memory = create_buffer(
        physical,
        device,
        len(data),
        usage | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
        VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
    )
    upload_to_buffer(device, staging_memory, data)

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

    copy_region = VkBufferCopy(srcOffset=0, dstOffset=0, size=len(data))
    vkCmdCopyBuffer(command_buffer, staging_buffer, device_buffer, 1, [copy_region])

    vkEndCommandBuffer(command_buffer)

    submit_info = VkSubmitInfo(commandBufferCount=1, pCommandBuffers=[command_buffer])
    vkQueueSubmit(queue, 1, [submit_info], VK_NULL_HANDLE)
    vkQueueWaitIdle(queue)

    vkFreeCommandBuffers(device, command_pool, 1, [command_buffer])
    vkDestroyCommandPool(device, command_pool, None)
    destroy_buffer(device, staging_buffer, staging_memory)

    return device_buffer, device_memory


def copy_to_device_local_buffer(
    physical: VkPhysicalDevice,
    device: VkDevice,
    queue: VkQueue,
    queue_family_index: int,
    device_buffer: VkBuffer,
    data: bytes,
) -> None:
    """Einmal-Copy mit separatem Submit — nur für Init/legacy, nicht im Frame-Loop.

    Per-Frame-Uploads: FrameStagingUploader + Copy im Frame-Command-Buffer (M9).
    """
    if not data:
        return

    staging_buffer, staging_memory = create_buffer(
        physical,
        device,
        len(data),
        VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
    )
    upload_to_buffer(device, staging_memory, data)

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
    copy_region = VkBufferCopy(srcOffset=0, dstOffset=0, size=len(data))
    vkCmdCopyBuffer(command_buffer, staging_buffer, device_buffer, 1, [copy_region])
    vkEndCommandBuffer(command_buffer)

    submit_info = VkSubmitInfo(commandBufferCount=1, pCommandBuffers=[command_buffer])
    vkQueueSubmit(queue, 1, [submit_info], VK_NULL_HANDLE)
    vkQueueWaitIdle(queue)

    vkFreeCommandBuffers(device, command_pool, 1, [command_buffer])
    vkDestroyCommandPool(device, command_pool, None)
    destroy_buffer(device, staging_buffer, staging_memory)


def destroy_buffer(device: VkDevice, buffer: VkBuffer, memory: VkDeviceMemory) -> None:
    vkDestroyBuffer(device, buffer, None)
    vkFreeMemory(device, memory, None)
