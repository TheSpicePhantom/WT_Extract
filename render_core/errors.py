"""Vulkan-spezifische Fehlerhilfen."""


class VulkanSetupError(RuntimeError):
    """Fehler bei Instance, Device oder Surface-Erstellung."""


class VulkanRenderError(RuntimeError):
    """Fehler beim GPU-Frame (Acquire, Submit, Present)."""
