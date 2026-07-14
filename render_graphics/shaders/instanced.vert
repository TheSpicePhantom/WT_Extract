#version 450

// Unit-Quad lokal (0..1), Anker unten links + Größe, Farbe
layout(location = 0) in vec2 inLocalPos;

layout(location = 1) in vec4 inAnchorSize;
layout(location = 2) in vec4 inColor;

layout(location = 0) out vec4 fragColor;

layout(push_constant) uniform CameraPush {
    mat4 viewProj;
} camera;

void main() {
    vec2 world = inAnchorSize.xy + inLocalPos * inAnchorSize.zw;
    gl_Position = camera.viewProj * vec4(world, 0.0, 1.0);
    fragColor = inColor;
}
