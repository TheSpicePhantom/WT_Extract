"""Debug-Demo: World-Gen Zwischenschritte visualisieren (Height, Klima, Voronoi, Terrain)."""

from __future__ import annotations

import random
import sys
import time
from dataclasses import replace

from bridge.chunk_extractor import ChunkRenderExtractor
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import load_content_registry
from game_core.stream_view import StreamViewParams
from game_core.world import World
from game_core.world_gen import (
    DebugMode,
    configure_world_gen,
    flush_procedural_chunks,
    get_world_gen_config,
    load_world_gen_config,
    populate_chunk_decorations,
    remove_procedural_decorations_in_chunk,
    set_debug_mode,
)
from wt_platform.input import InputState, key_held, key_pressed
from wt_platform.window import Window, WindowConfig
from render_core.policy import assert_gpu_only
from render_graphics.camera import camera_from_viewport
from render_graphics.ortho_renderer import OrthoFrameRenderer

CAM_X = 256.0
CAM_Y = 256.0
CAM_MOVE_SPEED = 720.0
ZOOM_SPEED = 1.8
WINDOW_TITLE_BASE = "WT Extract — World-Gen Debug (GPU)"
FPS_UPDATE_INTERVAL = 0.5

_DEBUG_MODES: tuple[tuple[str, DebugMode], ...] = (
    ("1 Height", DebugMode.HEIGHT),
    ("2 Water", DebugMode.WATER),
    ("3 Temperature", DebugMode.TEMPERATURE),
    ("4 Moisture", DebugMode.MOISTURE),
    ("5 ClimateClass", DebugMode.CLIMATE_CLASS),
    ("6 VoronoiCells", DebugMode.VORONOI_CELLS),
    ("7 VoronoiSeeds", DebugMode.VORONOI_SEEDS),
    ("8 VoronoiRaw", DebugMode.VORONOI_RAW),
    ("9 VoronoiWarp", DebugMode.VORONOI_WARP),
    ("0 VoronoiBlend", DebugMode.VORONOI_BLEND),
    ("F FinalBiome", DebugMode.FINAL_BIOME),
    ("S SubBiome", DebugMode.SUB_BIOME),
    ("T Terrain", DebugMode.TERRAIN),
    ("D Decorations", DebugMode.DECORATIONS),
)


class FpsCounter:
    def __init__(self, update_interval: float = FPS_UPDATE_INTERVAL) -> None:
        self._update_interval = update_interval
        self._elapsed = 0.0
        self._frames = 0
        self.fps = 0.0

    def tick(self, dt: float) -> bool:
        self._elapsed += dt
        self._frames += 1
        if self._elapsed < self._update_interval:
            return False
        self.fps = self._frames / self._elapsed
        self._elapsed = 0.0
        self._frames = 0
        return True


def _movement_vector(input_frame) -> tuple[float, float]:
    mx = 0.0
    my = 0.0
    if key_held(input_frame, "W") or key_held(input_frame, "UP"):
        my += 1.0
    if key_held(input_frame, "S") or key_held(input_frame, "DOWN"):
        my -= 1.0
    if key_held(input_frame, "A") or key_held(input_frame, "LEFT"):
        mx -= 1.0
    if key_held(input_frame, "D") or key_held(input_frame, "RIGHT"):
        mx += 1.0
    return mx, my


def _mode_label(mode: DebugMode) -> str:
    for label, candidate in _DEBUG_MODES:
        if candidate == mode:
            return label
    return mode.value


def _stream_view(
    cam_x: float,
    cam_y: float,
    zoom: float,
    width: int,
    height: int,
    *,
    move_dx: float = 0.0,
    move_dy: float = 0.0,
) -> StreamViewParams:
    return StreamViewParams(
        focus_x=cam_x,
        focus_y=cam_y,
        player_x=cam_x,
        player_y=cam_y,
        zoom=zoom,
        viewport_w=width,
        viewport_h=height,
        move_dx=move_dx,
        move_dy=move_dy,
    )


def _switch_mode(
    world: World,
    streamer: ChunkStreamer,
    content,
    collision,
    extractor,
    mode: DebugMode,
    deco_populated_chunks: set[tuple[int, int]],
) -> None:
    set_debug_mode(mode)
    flush_procedural_chunks(world, streamer, content, collision, extractor)
    deco_populated_chunks.clear()
    if mode == DebugMode.DECORATIONS:
        for coord in list(world.chunks.keys()):
            remove_procedural_decorations_in_chunk(world, coord)
            populate_chunk_decorations(world, content, coord[0], coord[1])
            deco_populated_chunks.add(coord)


def main() -> int:
    assert_gpu_only("world_gen_debug_demo")

    window = Window(WindowConfig(title=WINDOW_TITLE_BASE, width=1280, height=720))
    window.focus()

    try:
        renderer = OrthoFrameRenderer.create(window)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        print("Bake ausführen: python tools/bake_atlas.py", file=sys.stderr)
        window.destroy()
        return 1

    window.on_framebuffer_resized(lambda _w, _h: renderer.handle_surface_resize())
    input_state = InputState(window)

    configure_world_gen(load_world_gen_config())
    set_debug_mode(DebugMode.HEIGHT)

    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    streamer = ChunkStreamer()
    extractor = ChunkRenderExtractor(world, renderer.sprite_catalog)

    cam_x, cam_y = CAM_X, CAM_Y
    zoom = 0.35
    width, height = window.framebuffer_size
    debug_mode = DebugMode.HEIGHT
    last_time = time.monotonic()
    fps_counter = FpsCounter()
    deco_populated_chunks: set[tuple[int, int]] = set()
    last_cam_x, last_cam_y = cam_x, cam_y

    streamer.update(
        world,
        cam_x,
        cam_y,
        content,
        collision,
        extractor,
        view=_stream_view(cam_x, cam_y, zoom, width, height),
    )

    key_to_mode = {
        "1": DebugMode.HEIGHT,
        "2": DebugMode.WATER,
        "3": DebugMode.TEMPERATURE,
        "4": DebugMode.MOISTURE,
        "5": DebugMode.CLIMATE_CLASS,
        "6": DebugMode.VORONOI_CELLS,
        "7": DebugMode.VORONOI_SEEDS,
        "8": DebugMode.VORONOI_RAW,
        "9": DebugMode.VORONOI_WARP,
        "0": DebugMode.VORONOI_BLEND,
    }

    try:
        while not window.should_close:
            frame = input_state.poll()
            if frame.should_close:
                break

            now = time.monotonic()
            dt = min(now - last_time, 0.05)
            last_time = now

            width, height = window.framebuffer_size
            if width < 1 or height < 1:
                continue

            if frame.escape:
                window.request_close()
                continue

            if key_pressed(frame, "F"):
                debug_mode = DebugMode.FINAL_BIOME
                _switch_mode(world, streamer, content, collision, extractor, debug_mode, deco_populated_chunks)
            if key_pressed(frame, "S"):
                debug_mode = DebugMode.SUB_BIOME
                _switch_mode(world, streamer, content, collision, extractor, debug_mode, deco_populated_chunks)
            if key_pressed(frame, "T"):
                debug_mode = DebugMode.TERRAIN
                _switch_mode(world, streamer, content, collision, extractor, debug_mode, deco_populated_chunks)
            if key_pressed(frame, "D"):
                debug_mode = DebugMode.DECORATIONS
                _switch_mode(world, streamer, content, collision, extractor, debug_mode, deco_populated_chunks)
            for key, mode in key_to_mode.items():
                if key_pressed(frame, key):
                    debug_mode = mode
                    _switch_mode(world, streamer, content, collision, extractor, debug_mode, deco_populated_chunks)

            if key_pressed(frame, "G"):
                config = get_world_gen_config()
                new_seed = random.randint(1, 2_000_000_000)
                streamer.shutdown_chunk_gen_pool()
                configure_world_gen(replace(config, world_seed=new_seed))
                deco_populated_chunks.clear()
                flush_procedural_chunks(world, streamer, content, collision, extractor)
                streamer.update(
                    world,
                    cam_x,
                    cam_y,
                    content,
                    collision,
                    extractor,
                    view=_stream_view(cam_x, cam_y, zoom, width, height),
                )

            if key_pressed(frame, "F11"):
                window.toggle_fullscreen()

            move_x, move_y = _movement_vector(frame)
            move = CAM_MOVE_SPEED * dt / max(zoom, 0.1)
            cam_x += move_x * move
            cam_y += move_y * move

            move_dx = cam_x - last_cam_x
            move_dy = cam_y - last_cam_y
            streamer.update(
                world,
                cam_x,
                cam_y,
                content,
                collision,
                extractor,
                view=_stream_view(
                    cam_x,
                    cam_y,
                    zoom,
                    width,
                    height,
                    move_dx=move_dx,
                    move_dy=move_dy,
                ),
            )
            last_cam_x, last_cam_y = cam_x, cam_y
            if debug_mode == DebugMode.DECORATIONS:
                for coord in list(world.chunks.keys()):
                    if coord in deco_populated_chunks:
                        continue
                    populate_chunk_decorations(world, content, coord[0], coord[1])
                    deco_populated_chunks.add(coord)

            if key_pressed(frame, "E") or key_pressed(frame, "EQUAL"):
                zoom *= ZOOM_SPEED ** dt
            if key_pressed(frame, "Q") or key_pressed(frame, "MINUS"):
                zoom /= ZOOM_SPEED ** dt
            if frame.scroll_delta != 0.0:
                zoom *= ZOOM_SPEED ** (frame.scroll_delta * 0.25)
            zoom = max(0.05, min(zoom, 32.0))

            width, height = window.framebuffer_size
            camera = camera_from_viewport(cam_x, cam_y, zoom, width, height)
            render_frame = extractor.extract(camera)
            renderer.draw(render_frame)

            if fps_counter.tick(dt):
                seed = get_world_gen_config().world_seed
                fs = "fullscreen" if window.is_fullscreen else "windowed"
                window.set_window_title(
                    f"{WINDOW_TITLE_BASE} | {fps_counter.fps:.0f} FPS | {fs} | "
                    f"seed {seed} | mode {_mode_label(debug_mode)} | "
                    f"loaded {world.chunk_count} | G seed | 1-0/F/S/T/D modes | WASD pan | Q/E zoom",
                )
    finally:
        set_debug_mode(None)
        streamer.shutdown_chunk_gen_pool()
        renderer.destroy()
        window.destroy()

    return 0


if __name__ == "__main__":
    sys.exit(main())
