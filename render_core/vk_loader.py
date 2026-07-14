"""Lädt KHR-Extension-Funktionen nach Instance/Device-Erstellung."""

from __future__ import annotations

from dataclasses import dataclass, field

from vulkan import vkGetDeviceProcAddr, vkGetInstanceProcAddr

from render_core.errors import VulkanSetupError
from render_core.vk_types import VkDevice, VkInstance


@dataclass
class VulkanKhrApi:
    instance: VkInstance
    device: VkDevice | None = None
    vkGetPhysicalDeviceSurfaceSupportKHR: object = field(default=None, repr=False)
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR: object = field(default=None, repr=False)
    vkGetPhysicalDeviceSurfaceFormatsKHR: object = field(default=None, repr=False)
    vkGetPhysicalDeviceSurfacePresentModesKHR: object = field(default=None, repr=False)
    vkDestroySurfaceKHR: object = field(default=None, repr=False)
    vkCreateSwapchainKHR: object = field(default=None, repr=False)
    vkDestroySwapchainKHR: object = field(default=None, repr=False)
    vkGetSwapchainImagesKHR: object = field(default=None, repr=False)
    vkAcquireNextImageKHR: object = field(default=None, repr=False)
    vkQueuePresentKHR: object = field(default=None, repr=False)

    @classmethod
    def for_instance(cls, instance: VkInstance) -> VulkanKhrApi:
        api = cls(instance=instance)
        api.vkGetPhysicalDeviceSurfaceSupportKHR = _require_proc(
            instance, "vkGetPhysicalDeviceSurfaceSupportKHR"
        )
        api.vkGetPhysicalDeviceSurfaceCapabilitiesKHR = _require_proc(
            instance, "vkGetPhysicalDeviceSurfaceCapabilitiesKHR"
        )
        api.vkGetPhysicalDeviceSurfaceFormatsKHR = _require_proc(
            instance, "vkGetPhysicalDeviceSurfaceFormatsKHR"
        )
        api.vkGetPhysicalDeviceSurfacePresentModesKHR = _require_proc(
            instance, "vkGetPhysicalDeviceSurfacePresentModesKHR"
        )
        api.vkDestroySurfaceKHR = _require_proc(instance, "vkDestroySurfaceKHR")
        return api

    def bind_device(self, device: VkDevice) -> None:
        self.device = device
        self.vkCreateSwapchainKHR = _require_proc(
            self.instance, "vkCreateSwapchainKHR", device
        )
        self.vkDestroySwapchainKHR = _require_proc(
            self.instance, "vkDestroySwapchainKHR", device
        )
        self.vkGetSwapchainImagesKHR = _require_proc(
            self.instance, "vkGetSwapchainImagesKHR", device
        )
        self.vkAcquireNextImageKHR = _require_proc(
            self.instance, "vkAcquireNextImageKHR", device
        )
        self.vkQueuePresentKHR = _require_proc(self.instance, "vkQueuePresentKHR", device)


def _require_proc(instance: VkInstance, name: str, device: VkDevice | None = None):
    proc = vkGetInstanceProcAddr(instance, name)
    if proc is None and device is not None:
        proc = vkGetDeviceProcAddr(device, name)
    if proc is None:
        raise VulkanSetupError(f"Vulkan-Funktion nicht verfügbar: {name}")
    return proc
