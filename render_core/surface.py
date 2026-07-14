"""Vulkan Surface aus GLFW-Fenster — GPU-Präsentation."""

from __future__ import annotations

import ctypes

import glfw
from vulkan import VK_SUCCESS

from render_core.errors import VulkanSetupError
from render_core.vk_loader import VulkanKhrApi
from render_core.vk_types import VkInstance, VkSurfaceKHR
from wt_platform.window import Window


def create_surface(instance: VkInstance, window: Window) -> VkSurfaceKHR:
    surface_out = ctypes.c_uint64()
    result = glfw.create_window_surface(instance, window.handle, None, ctypes.byref(surface_out))
    if result != VK_SUCCESS:
        raise VulkanSetupError(f"Vulkan Surface konnte nicht erstellt werden (VkResult={result}).")
    return surface_out.value


def destroy_surface(khr: VulkanKhrApi, instance: VkInstance, surface: VkSurfaceKHR) -> None:
    khr.vkDestroySurfaceKHR(instance, surface, None)
