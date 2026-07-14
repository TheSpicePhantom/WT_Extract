"""Swapchain — GPU-Framebuffer für Präsentation."""

from __future__ import annotations

from dataclasses import dataclass, field

from vulkan import *  # noqa: F403

from render_core.device import query_swapchain_support
from render_core.errors import VulkanSetupError
from render_core.vk_loader import VulkanKhrApi
from render_core.vk_types import (
    VkDevice,
    VkFormat,
    VkImage,
    VkImageView,
    VkPhysicalDevice,
    VkSurfaceKHR,
    VkSwapchainKHR,
)


@dataclass
class Swapchain:
    handle: VkSwapchainKHR
    images: list[VkImage]
    image_views: list[VkImageView]
    image_format: VkFormat
    _extent: tuple[int, int] = field(repr=False)

    @property
    def extent(self):
        width, height = self._extent
        return VkExtent2D(width=width, height=height)

    @property
    def extent_size(self) -> tuple[int, int]:
        return self._extent


def _choose_surface_format(formats: list[VkSurfaceFormatKHR]) -> VkSurfaceFormatKHR:
    preferred = VkSurfaceFormatKHR(
        format=VK_FORMAT_B8G8R8A8_SRGB,
        colorSpace=VK_COLOR_SPACE_SRGB_NONLINEAR_KHR,
    )
    for fmt in formats:
        if fmt.format == preferred.format and fmt.colorSpace == preferred.colorSpace:
            return fmt
    return formats[0]


def _choose_present_mode(modes: list[VkPresentModeKHR]) -> VkPresentModeKHR:
    # FIFO = stabil, kein unnötiges SUBOPTIMAL-Flackern auf manchen Treibern.
    if VK_PRESENT_MODE_FIFO_KHR in modes:
        return VK_PRESENT_MODE_FIFO_KHR
    if VK_PRESENT_MODE_MAILBOX_KHR in modes:
        return VK_PRESENT_MODE_MAILBOX_KHR
    return modes[0]


def _is_valid_extent(extent) -> bool:
    return (
        extent.width != 0xFFFFFFFF
        and extent.width >= 1
        and extent.height >= 1
    )


def _choose_extent(capabilities: VkSurfaceCapabilitiesKHR, width: int, height: int):
    current = capabilities.currentExtent
    if _is_valid_extent(current):
        return current

    width = max(capabilities.minImageExtent.width, min(capabilities.maxImageExtent.width, width))
    height = max(capabilities.minImageExtent.height, min(capabilities.maxImageExtent.height, height))
    return VkExtent2D(width=width, height=height)


def create_swapchain(
    khr: VulkanKhrApi,
    device: VkDevice,
    physical: VkPhysicalDevice,
    surface: VkSurfaceKHR,
    indices,
    width: int,
    height: int,
    old_swapchain: VkSwapchainKHR | None = None,
) -> Swapchain:
    support = query_swapchain_support(khr, physical, surface)
    if not support.is_adequate():
        raise VulkanSetupError("Swapchain-Support unzureichend.")

    surface_format = _choose_surface_format(support.formats)
    present_mode = _choose_present_mode(support.present_modes)
    extent = _choose_extent(support.capabilities, width, height)
    stored_extent = (int(extent.width), int(extent.height))
    image_extent = VkExtent2D(width=stored_extent[0], height=stored_extent[1])

    image_count = support.capabilities.minImageCount + 1
    if support.capabilities.maxImageCount > 0 and image_count > support.capabilities.maxImageCount:
        image_count = support.capabilities.maxImageCount

    queue_family_indices = [indices.graphics, indices.present]
    sharing_mode = VK_SHARING_MODE_EXCLUSIVE
    queue_family_index_list = None

    if indices.graphics != indices.present:
        sharing_mode = VK_SHARING_MODE_CONCURRENT
        queue_family_index_list = queue_family_indices

    chosen_format = int(surface_format.format)
    chosen_color_space = int(surface_format.colorSpace)

    create_info = VkSwapchainCreateInfoKHR(
        surface=surface,
        minImageCount=image_count,
        imageFormat=chosen_format,
        imageColorSpace=chosen_color_space,
        imageExtent=image_extent,
        imageArrayLayers=1,
        imageUsage=VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT,
        imageSharingMode=sharing_mode,
        queueFamilyIndexCount=len(queue_family_index_list) if queue_family_index_list else 0,
        pQueueFamilyIndices=queue_family_index_list,
        preTransform=support.capabilities.currentTransform,
        compositeAlpha=VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR,
        presentMode=present_mode,
        clipped=True,
        oldSwapchain=old_swapchain or VK_NULL_HANDLE,
    )

    swapchain = khr.vkCreateSwapchainKHR(device, create_info, None)
    images = khr.vkGetSwapchainImagesKHR(device, swapchain)
    image_views = [_create_image_view(device, image, chosen_format) for image in images]

    return Swapchain(
        handle=swapchain,
        images=list(images),
        image_views=image_views,
        image_format=chosen_format,
        _extent=stored_extent,
    )


def _create_image_view(device: VkDevice, image: VkImage, fmt: VkFormat) -> VkImageView:
    create_info = VkImageViewCreateInfo(
        image=image,
        viewType=VK_IMAGE_VIEW_TYPE_2D,
        format=fmt,
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


def destroy_swapchain(khr: VulkanKhrApi, device: VkDevice, swapchain: Swapchain) -> None:
    for view in swapchain.image_views:
        vkDestroyImageView(device, view, None)
    khr.vkDestroySwapchainKHR(device, swapchain.handle, None)
