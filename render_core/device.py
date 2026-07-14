"""Physical/Logical Device und Queues — ausschließlich GPU."""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403

from render_core.errors import VulkanSetupError
from render_core.vk_loader import VulkanKhrApi
from render_core.vk_types import VkDevice, VkInstance, VkPhysicalDevice, VkQueue, VkSurfaceKHR


DEVICE_EXTENSIONS = [VK_KHR_SWAPCHAIN_EXTENSION_NAME]


@dataclass(frozen=True, slots=True)
class QueueFamilyIndices:
    graphics: int | None = None
    present: int | None = None

    def is_complete(self) -> bool:
        return self.graphics is not None and self.present is not None


@dataclass(frozen=True, slots=True)
class GpuDevice:
    physical: VkPhysicalDevice
    logical: VkDevice
    graphics_queue: VkQueue
    present_queue: VkQueue
    queue_family_indices: QueueFamilyIndices


def _find_queue_families(
    khr: VulkanKhrApi,
    physical: VkPhysicalDevice,
    surface: VkSurfaceKHR,
) -> QueueFamilyIndices:
    families = vkGetPhysicalDeviceQueueFamilyProperties(physical)
    graphics: int | None = None
    present: int | None = None

    for index, family in enumerate(families):
        if graphics is None and family.queueFlags & VK_QUEUE_GRAPHICS_BIT:
            graphics = index
        if present is None and khr.vkGetPhysicalDeviceSurfaceSupportKHR(physical, index, surface):
            present = index
        if graphics is not None and present is not None:
            break

    return QueueFamilyIndices(graphics=graphics, present=present)


def _score_physical_device(physical: VkPhysicalDevice) -> int:
    props = vkGetPhysicalDeviceProperties(physical)
    score = 0
    if props.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU:
        score += 1000
    elif props.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU:
        score += 100
    score += props.limits.maxImageDimension2D
    return score


def _pick_physical_device(
    khr: VulkanKhrApi,
    instance: VkInstance,
    surface: VkSurfaceKHR,
) -> VkPhysicalDevice:
    devices = vkEnumeratePhysicalDevices(instance)
    if not devices:
        raise VulkanSetupError("Keine Vulkan-GPU gefunden.")

    candidates: list[tuple[int, VkPhysicalDevice]] = []
    for device in devices:
        indices = _find_queue_families(khr, device, surface)
        if not indices.is_complete():
            continue

        if not _check_device_extension_support(device):
            continue

        if not query_swapchain_support(khr, device, surface).is_adequate():
            continue

        candidates.append((_score_physical_device(device), device))

    if not candidates:
        raise VulkanSetupError(
            "Keine geeignete GPU mit Graphics/Present-Queues und Swapchain-Support."
        )

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def _check_device_extension_support(physical: VkPhysicalDevice) -> bool:
    available = {ext.extensionName for ext in vkEnumerateDeviceExtensionProperties(physical, None)}
    return set(DEVICE_EXTENSIONS).issubset(available)


@dataclass(frozen=True, slots=True)
class SwapchainSupportDetails:
    capabilities: VkSurfaceCapabilitiesKHR
    formats: list[VkSurfaceFormatKHR]
    present_modes: list[VkPresentModeKHR]

    def is_adequate(self) -> bool:
        return bool(self.formats and self.present_modes)


def query_swapchain_support(
    khr: VulkanKhrApi,
    physical: VkPhysicalDevice,
    surface: VkSurfaceKHR,
) -> SwapchainSupportDetails:
    capabilities = khr.vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physical, surface)
    formats = khr.vkGetPhysicalDeviceSurfaceFormatsKHR(physical, surface)
    present_modes = khr.vkGetPhysicalDeviceSurfacePresentModesKHR(physical, surface)
    return SwapchainSupportDetails(
        capabilities=capabilities,
        formats=list(formats),
        present_modes=list(present_modes),
    )


def create_gpu_device(
    khr: VulkanKhrApi,
    instance: VkInstance,
    surface: VkSurfaceKHR,
) -> GpuDevice:
    physical = _pick_physical_device(khr, instance, surface)
    indices = _find_queue_families(khr, physical, surface)
    if not indices.is_complete():
        raise VulkanSetupError("Queue-Familien unvollständig.")

    queue_create_infos: list[VkDeviceQueueCreateInfo] = []
    unique_families = {indices.graphics, indices.present}
    queue_priority = [1.0]

    for family in unique_families:
        if family is None:
            continue
        queue_create_infos.append(
            VkDeviceQueueCreateInfo(
                queueFamilyIndex=family,
                queueCount=1,
                pQueuePriorities=queue_priority,
            )
        )

    device_features = VkPhysicalDeviceFeatures()

    create_info = VkDeviceCreateInfo(
        queueCreateInfoCount=len(queue_create_infos),
        pQueueCreateInfos=queue_create_infos,
        enabledExtensionCount=len(DEVICE_EXTENSIONS),
        ppEnabledExtensionNames=DEVICE_EXTENSIONS,
        pEnabledFeatures=device_features,
    )

    logical = vkCreateDevice(physical, create_info, None)
    graphics_queue = vkGetDeviceQueue(logical, indices.graphics, 0)
    present_queue = vkGetDeviceQueue(logical, indices.present, 0)

    return GpuDevice(
        physical=physical,
        logical=logical,
        graphics_queue=graphics_queue,
        present_queue=present_queue,
        queue_family_indices=indices,
    )


def destroy_gpu_device(device: GpuDevice) -> None:
    vkDestroyDevice(device.logical, None)
