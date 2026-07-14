"""Kompiliert GLSL → SPIR-V (GPU). Erfordert shaderc-rs-py."""

from __future__ import annotations

from pathlib import Path

import shadercrs

SHADER_DIR = Path(__file__).parent


def compile_glsl(source_path: Path, stage: str) -> bytes:
    compiler = shadercrs.Compiler()
    options = shadercrs.CompileOptions()
    options.set_source_language("glsl")
    options.set_target_env("vulkan", "vulkan_1_0")
    options.set_optimization_level("performance")

    source = source_path.read_text(encoding="utf-8")
    artifact = compiler.compile_into_spirv(
        source,
        stage,
        str(source_path),
        "main",
        options,
    )
    return bytes(artifact.as_binary_u8())


def main() -> None:
    pairs = [
        ("colored.vert", "vertex"),
        ("colored.frag", "fragment"),
        ("instanced.vert", "vertex"),
        ("instanced.frag", "fragment"),
        ("textured_instanced.vert", "vertex"),
        ("textured_instanced.frag", "fragment"),
    ]
    for filename, stage in pairs:
        src = SHADER_DIR / filename
        out = SHADER_DIR / f"{src.stem}_{stage[:4]}.spv"
        spirv = compile_glsl(src, stage)
        out.write_bytes(spirv)
        print(f"{src.name} -> {out.name} ({len(spirv)} bytes)")


if __name__ == "__main__":
    main()
