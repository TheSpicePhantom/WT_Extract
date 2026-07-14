"""Vulkan Instance und Debug-Extensions."""

from __future__ import annotations

import os
from dataclasses import dataclass

import glfw
from vulkan import *  # noqa: F403

from render_core.errors import VulkanSetupError


@dataclass(frozen=True, slots=True)
class InstanceConfig:
    app_name: str = "WT Extract"
    enable_validation: bool = False


def _validation_layers_available() -> list[str]:
    layers = vkEnumerateInstanceLayerProperties()
    available = {layer.layerName for layer in layers}
    required = {"VK_LAYER_KHRONOS_validation"}
    if required.issubset(available):
        return ["VK_LAYER_KHRONOS_validation"]
    return []


def create_instance(config: InstanceConfig | None = None) -> VkInstance:
    config = config or InstanceConfig(
        enable_validation=os.getenv("WT_VK_DEBUG", "0") == "1",
    )

    app_info = VkApplicationInfo(
        pApplicationName=config.app_name,
        applicationVersion=VK_MAKE_VERSION(0, 1, 0),
        pEngineName="WT Extract Render Core",
        engineVersion=VK_MAKE_VERSION(0, 1, 0),
        apiVersion=VK_API_VERSION_1_0,
    )

    extensions = glfw.get_required_instance_extensions()
    if extensions is None:
        raise VulkanSetupError("GLFW liefert keine Vulkan-Instance-Extensions.")

    extensions = list(extensions)
    layers: list[str] = []
    if config.enable_validation:
        layers = _validation_layers_available()
        if not layers:
            raise VulkanSetupError(
                "Validation Layers angefordert, aber VK_LAYER_KHRONOS_validation fehlt."
            )
        extensions.append(VK_EXT_DEBUG_UTILS_EXTENSION_NAME)

    create_info = VkInstanceCreateInfo(
        pApplicationInfo=app_info,
        enabledExtensionCount=len(extensions),
        ppEnabledExtensionNames=extensions,
        enabledLayerCount=len(layers),
        ppEnabledLayerNames=layers,
    )

    instance = vkCreateInstance(create_info, None)
    if instance is None:
        raise VulkanSetupError("vkCreateInstance fehlgeschlagen.")
    return instance


def destroy_instance(instance: VkInstance) -> None:
    vkDestroyInstance(instance, None)
