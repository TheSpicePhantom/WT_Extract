#version 450

layout(location = 0) in vec2 inLocalPos;
layout(location = 1) in vec2 inAnchor;
layout(location = 2) in vec4 inTint;
layout(location = 3) in uint inSpriteId;
layout(location = 4) in uint inFramePack;
layout(location = 5) in uint inClipPack;

layout(location = 0) out vec2 fragUv;
layout(location = 1) out vec4 fragTint;

layout(push_constant) uniform CameraPush {
    mat4 viewProj;
} camera;

struct SpriteRect {
    vec4 uv;
    vec4 sizePad;
};

layout(std430, set = 0, binding = 1) readonly buffer SpriteRects {
    SpriteRect rects[];
};

float clipComponent(uint packed, bool high) {
    uint value = high ? (packed >> 16u) : (packed & 0xFFFFu);
    return float(value) / 65535.0;
}

void main() {
    SpriteRect rect = rects[inSpriteId];
    vec2 sheetGrid = max(rect.sizePad.zw, vec2(1.0));
    vec2 frameSize = rect.sizePad.xy / sheetGrid;
    if (frameSize.x <= 0.0 || frameSize.y <= 0.0) {
        gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
        return;
    }

    float clipV0 = clipComponent(inClipPack, false);
    float clipV1 = clipComponent(inClipPack, true);
    if (clipV1 <= clipV0) {
        clipV0 = 0.0;
        clipV1 = 1.0;
    }

    uint frameCol = inFramePack & 0xFFFFu;
    uint frameRow = inFramePack >> 16u;

    // Unit-Quad 0..1 auf Clip-Teilregion mappen (kein Vertex-Discard)
    float localY = clipV0 + inLocalPos.y * (clipV1 - clipV0);
    vec2 local = vec2(inLocalPos.x, localY);

    vec2 world = inAnchor + local * frameSize;
    gl_Position = camera.viewProj * vec4(world, 0.0, 1.0);

    vec2 cellSize = vec2(
        (rect.uv.z - rect.uv.x) / sheetGrid.x,
        (rect.uv.w - rect.uv.y) / sheetGrid.y
    );
    vec2 cellOrigin = rect.uv.xy + vec2(float(frameCol), float(frameRow)) * cellSize;
    fragUv = cellOrigin + vec2(local.x, 1.0 - localY) * cellSize;
    fragTint = inTint;
}
