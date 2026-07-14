#version 450

layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec4 inColor;

layout(location = 0) out vec4 fragColor;

layout(push_constant) uniform CameraPush {
    mat4 viewProj;
} camera;

void main() {
    gl_Position = camera.viewProj * vec4(inPosition, 0.0, 1.0);
    fragColor = inColor;
}
