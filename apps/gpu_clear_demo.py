"""Demo: erster sichtbarer GPU-Frame (Vulkan Clear) — kein CPU-Rendering."""

from __future__ import annotations

import sys

from wt_platform.window import Window, WindowConfig
from render_core.gpu_renderer import GpuRenderer
from render_core.policy import assert_gpu_only


def main() -> int:
    assert_gpu_only("gpu_clear_demo")

    window = Window(WindowConfig(title="WT Extract — GPU Clear", width=1280, height=720))
    renderer = GpuRenderer.create(window)

    try:
        while not window.should_close:
            window.poll_events()
            renderer.draw_frame(clear_color=(0.08, 0.09, 0.11, 1.0))
    finally:
        renderer.destroy()
        window.destroy()

    return 0


if __name__ == "__main__":
    sys.exit(main())
