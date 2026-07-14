"""Orthographische Kamera — View/Projection aus neutralem CameraData."""

from __future__ import annotations

from render_scene.types import CameraData

# Column-major 4x4 (GLSL/Vulkan-kompatibel).
Mat4 = list[float]

CAMERA_UBO_SIZE = 64


def mat4_identity() -> Mat4:
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ]


def mat4_multiply(a: Mat4, b: Mat4) -> Mat4:
    out = [0.0] * 16
    for col in range(4):
        for row in range(4):
            out[col * 4 + row] = sum(a[k * 4 + row] * b[col * 4 + k] for k in range(4))
    return out


def mat4_orthographic(
    left: float,
    right: float,
    bottom: float,
    top: float,
    near: float,
    far: float,
) -> Mat4:
    rl = right - left
    tb = top - bottom
    fn = far - near
    return [
        2.0 / rl, 0.0, 0.0, 0.0,
        0.0, 2.0 / tb, 0.0, 0.0,
        0.0, 0.0, -2.0 / fn, 0.0,
        -(right + left) / rl, -(top + bottom) / tb, -(far + near) / fn, 1.0,
    ]


def mat4_translate(x: float, y: float, z: float) -> Mat4:
    m = mat4_identity()
    m[12] = x
    m[13] = y
    m[14] = z
    return m


def build_view_projection(camera: CameraData) -> Mat4:
    """Baut viewProj-Matrix für top-down 2D — Y-up Welt, GLFW-kompatible Projection."""
    zoom = max(camera.zoom, 1e-6)
    vp_w = max(camera.viewport_width, 1)
    vp_h = max(camera.viewport_height, 1)
    half_w = (vp_w / zoom) * 0.5
    half_h = (vp_h / zoom) * 0.5

    view = mat4_translate(-camera.position_x, -camera.position_y, 0.0)
    # bottom > top: Y-up Welt → korrekte Bildschirm-Orientierung (GLFW/Vulkan)
    proj = mat4_orthographic(-half_w, half_w, half_h, -half_h, -1.0, 1.0)

    return mat4_multiply(proj, view)


def pack_camera_ubo(view_proj: Mat4) -> bytes:
    import struct

    if len(view_proj) != 16:
        raise ValueError("view_proj muss 16 floats (Mat4) enthalten.")
    return struct.pack("16f", *view_proj)


def camera_from_viewport(
    position_x: float,
    position_y: float,
    zoom: float,
    viewport_width: int,
    viewport_height: int,
) -> CameraData:
    return CameraData(
        position_x=position_x,
        position_y=position_y,
        zoom=zoom,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
    )
