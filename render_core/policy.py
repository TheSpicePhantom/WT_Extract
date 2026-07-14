"""Rendering-Policy: ausschließlich GPU (Vulkan), kein CPU-Fallback."""

GPU_ONLY: bool = True


class CpuRenderingForbiddenError(RuntimeError):
    """Wird ausgelöst, wenn ein CPU-Renderpfad angefordert oder erkannt wird."""


def assert_gpu_only(context: str = "") -> None:
    if not GPU_ONLY:
        raise CpuRenderingForbiddenError(
            f"CPU-Rendering ist deaktiviert. Kontext: {context or 'unbekannt'}"
        )
