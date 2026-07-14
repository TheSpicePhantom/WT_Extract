"""Demo: Chunk-Welt — Character (M11), Tiles (M10), Decorations (M12), Bridge → GPU."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import replace
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bridge.character_extractor import character_to_sprite
from bridge.chunk_extractor import ChunkRenderExtractor
from bridge.decoration_extractor import decorations_to_sprites
from bridge.screen_to_world import screen_to_world_tile
from game_core.character import Character
from game_core.chunk_streaming import ChunkStreamer
from game_core.collision_catalog import load_collision_catalog
from game_core.content_registry import ContentRegistry, load_content_registry
from game_core.navigation import apply_character_movement, spawn_character_at_center
from game_core.paint_brushes import apply_paint_at_cursor, palette_label
from game_core.stream_view import StreamViewParams
from game_core.streaming_world_io import DEFAULT_STREAMING_SAVE_DIR, load_streaming_world, save_streaming_world
from game_core.world import CHUNK_SIZE_PX, World
from game_core.world_gen import (
    configure_world_gen,
    ensure_playable_seed,
    flush_procedural_chunks,
    get_world_gen_config,
    load_world_gen_config,
    score_spawn_area,
    set_debug_mode,
)
from game_core.world_io import DEFAULT_WORLD_SAVE_PATH, load_world, save_world
from game_core.perf.config import load_profiling_config
from game_core.perf.session import PerfSession
from tools.run_perf_scenario import ScenarioRuntime
from wt_platform.input import InputState, ctrl_combo_pressed, key_held, key_pressed
from wt_platform.window import Window, WindowConfig
from render_core.policy import assert_gpu_only
from render_graphics.camera import camera_from_viewport
from render_graphics.chunk_debug_overlay import build_overlay_vertices, loaded_chunks_layer
from render_graphics.ortho_renderer import OrthoFrameRenderer
from render_scene.types import SpriteInstanceData

STREAMING_MODE = True
STREAM_DIAG_ENV = "WT_STREAM_DIAG"
SPAWN_X = float(CHUNK_SIZE_PX)
SPAWN_Y = float(CHUNK_SIZE_PX)
CAM_MOVE_SPEED = 720.0
ZOOM_SPEED = 1.8
WINDOW_TITLE_BASE = "WT Extract — Chunk World + Character (GPU)"
FPS_UPDATE_INTERVAL = 0.5

PAINT_TERRAIN = "terrain"
PAINT_OVERLAY = "overlay"
PAINT_DECORATION = "decoration"


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


def _stream_focus(free_camera: bool, cam_x: float, cam_y: float, player: Character) -> tuple[float, float]:
    if free_camera:
        return cam_x, cam_y
    return player.camera_focus_x, player.camera_focus_y


def _cursor_world_tile(camera, input_frame) -> tuple[int, int]:
    screen_x, screen_y = input_frame.cursor_fb
    return screen_to_world_tile(camera, screen_x, screen_y)


def _apply_decoration_brush(world, camera, input_frame, decoration_id: str) -> bool:
    wx, wy = _cursor_world_tile(camera, input_frame)
    return world.place_decoration(wx, wy, decoration_id)


def _remove_decoration_brush(world, camera, input_frame) -> bool:
    wx, wy = _cursor_world_tile(camera, input_frame)
    return world.remove_decoration_at(wx, wy)


def _movement_vector(input_frame) -> tuple[float, float]:
    mx = 0.0
    my = 0.0
    if key_held(input_frame, "W"):
        my += 1.0
    if key_held(input_frame, "S"):
        my -= 1.0
    if key_held(input_frame, "A"):
        mx -= 1.0
    if key_held(input_frame, "D"):
        mx += 1.0
    return mx, my


def _stream_view(
    focus_x: float,
    focus_y: float,
    player: Character,
    zoom: float,
    viewport_w: int,
    viewport_h: int,
    *,
    move_dx: float = 0.0,
    move_dy: float = 0.0,
) -> StreamViewParams:
    return StreamViewParams(
        focus_x=focus_x,
        focus_y=focus_y,
        player_x=player.world_x,
        player_y=player.world_y,
        zoom=zoom,
        viewport_w=viewport_w,
        viewport_h=viewport_h,
        move_dx=move_dx,
        move_dy=move_dy,
    )


def _paint_mode_label(paint_mode: str, content: ContentRegistry, decoration_index: int) -> str:
    palette = content.brush_palette(paint_mode)
    if palette is not None:
        return palette_label(content, palette)
    if paint_mode == PAINT_DECORATION:
        if not content.decorations:
            return "decoration (empty)"
        entry = content.decorations[decoration_index % len(content.decorations)]
        return f"decoration {entry.id}"
    return paint_mode


def main() -> int:
    assert_gpu_only("chunk_world_demo")

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--profile", action="store_true", help="Runtime-Profiling (M23)")
    demo_args, _unknown = parser.parse_known_args()
    profile_enabled = demo_args.profile
    stream_diag_enabled = os.environ.get(STREAM_DIAG_ENV, "").strip() in ("1", "true", "yes")

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
    set_debug_mode(None)
    spawn_score = score_spawn_area()

    content = load_content_registry()
    collision = load_collision_catalog()
    world = World()
    streamer = ChunkStreamer()
    streamer.warmup_chunk_gen_pool()
    extractor = ChunkRenderExtractor(world, renderer.sprite_catalog)

    width, height = window.framebuffer_size
    perf_session: PerfSession | None = None
    perf_runtime: ScenarioRuntime | None = None
    if profile_enabled:
        perf_config = load_profiling_config()
        steady = perf_config.scenarios.get("steady")
        warmup = steady.warmup_frames if steady is not None else 0
        perf_session = PerfSession(
            config=perf_config,
            scenario_id="demo",
            run_mode="demo",
            extract_enabled=True,
        )
        perf_session.full_frame_enabled = True
        perf_session._warmup_frames = warmup
        perf_runtime = ScenarioRuntime(
            world=world,
            streamer=streamer,
            content=content,
            collision=collision,
            extractor=extractor,
            catalog=renderer.sprite_catalog,
            viewport_w=width,
            viewport_h=height,
        )

    zoom = 0.35
    streamer.update(
        world,
        SPAWN_X,
        SPAWN_Y,
        content,
        collision,
        extractor,
        view=StreamViewParams(
            focus_x=SPAWN_X,
            focus_y=SPAWN_Y,
            player_x=SPAWN_X,
            player_y=SPAWN_Y,
            zoom=zoom,
            viewport_w=width,
            viewport_h=height,
        ),
    )
    player = spawn_character_at_center(world, content, collision, SPAWN_X, SPAWN_Y)

    cam_x, cam_y = player.camera_focus_x, player.camera_focus_y
    free_camera = False
    show_chunk_bounds = False
    paint_mode = PAINT_TERRAIN
    decoration_index = 0
    last_time = time.monotonic()
    fps_counter = FpsCounter()
    last_visible_chunks = 0
    last_visible_tiles = 0
    loaded_chunks = world.chunk_count
    last_focus_x, last_focus_y = SPAWN_X, SPAWN_Y

    try:
        while not window.should_close:
            frame = input_state.poll()

            if frame.should_close:
                break

            if perf_session is not None:
                perf_session.begin_full_frame()

            now = time.monotonic()
            dt = min(now - last_time, 0.05)
            last_time = now

            width, height = window.framebuffer_size
            if width < 1 or height < 1:
                continue

            if frame.escape:
                window.request_close()
                continue

            if ctrl_combo_pressed(frame, "S"):
                if STREAMING_MODE:
                    save_streaming_world(DEFAULT_STREAMING_SAVE_DIR, world, player, streamer)
                    print(f"Streaming-Spielstand gespeichert: {DEFAULT_STREAMING_SAVE_DIR}", file=sys.stderr)
                else:
                    save_world(DEFAULT_WORLD_SAVE_PATH, world, player)
                    print(f"Spielstand gespeichert: {DEFAULT_WORLD_SAVE_PATH}", file=sys.stderr)

            if ctrl_combo_pressed(frame, "L"):
                if STREAMING_MODE:
                    try:
                        snapshot = load_streaming_world(DEFAULT_STREAMING_SAVE_DIR)
                        streamer.shutdown_chunk_gen_pool()
                        world = World(decorations=list(snapshot.decorations))
                        streamer.clear_persistent_overrides()
                        streamer.load_persistent_deltas(snapshot.persistent_deltas)
                        player = snapshot.player
                        extractor.set_world(world)
                        extractor.invalidate_all()
                        fx, fy = player.camera_focus_x, player.camera_focus_y
                        streamer.update(
                            world,
                            fx,
                            fy,
                            content,
                            collision,
                            extractor,
                            view=_stream_view(fx, fy, player, zoom, width, height),
                        )
                        last_focus_x, last_focus_y = fx, fy
                        world.rebuild_all_solid(content, collision)
                        if not free_camera:
                            cam_x, cam_y = player.camera_focus_x, player.camera_focus_y
                        print(f"Streaming-Spielstand geladen: {DEFAULT_STREAMING_SAVE_DIR}", file=sys.stderr)
                    except FileNotFoundError:
                        print(f"Kein Streaming-Spielstand: {DEFAULT_STREAMING_SAVE_DIR}", file=sys.stderr)
                    except (ValueError, KeyError, json.JSONDecodeError) as exc:
                        print(f"Streaming-Spielstand ungültig: {exc}", file=sys.stderr)
                else:
                    try:
                        snapshot = load_world(DEFAULT_WORLD_SAVE_PATH)
                        world = snapshot.world
                        player = snapshot.player
                        world.rebuild_all_solid(content, collision)
                        extractor.set_world(world)
                        if not free_camera:
                            cam_x, cam_y = player.camera_focus_x, player.camera_focus_y
                        print(f"Spielstand geladen: {DEFAULT_WORLD_SAVE_PATH}", file=sys.stderr)
                    except FileNotFoundError:
                        print(f"Kein Spielstand: {DEFAULT_WORLD_SAVE_PATH}", file=sys.stderr)
                    except (ValueError, KeyError, json.JSONDecodeError) as exc:
                        print(f"Spielstand ungültig: {exc}", file=sys.stderr)

            if key_pressed(frame, "F"):
                free_camera = not free_camera

            if key_pressed(frame, "C"):
                show_chunk_bounds = not show_chunk_bounds

            if key_pressed(frame, "F11"):
                window.toggle_fullscreen()

            if key_pressed(frame, "1"):
                paint_mode = PAINT_TERRAIN
            if key_pressed(frame, "2"):
                paint_mode = PAINT_OVERLAY
            if key_pressed(frame, "3"):
                paint_mode = PAINT_DECORATION

            if content.decorations:
                count = len(content.decorations)
                if key_pressed(frame, "LEFT_BRACKET"):
                    decoration_index = (decoration_index - 1) % count
                if key_pressed(frame, "RIGHT_BRACKET"):
                    decoration_index = (decoration_index + 1) % count

            move_x, move_y = _movement_vector(frame)
            force_run = key_held(frame, "SHIFT")

            focus_x, focus_y = _stream_focus(free_camera, cam_x, cam_y, player)
            move_dx = focus_x - last_focus_x
            move_dy = focus_y - last_focus_y
            stream_view = _stream_view(
                focus_x,
                focus_y,
                player,
                zoom,
                width,
                height,
                move_dx=move_dx,
                move_dy=move_dy,
            )

            if key_pressed(frame, "G"):
                config = get_world_gen_config()
                new_seed = random.randint(1, 2_000_000_000)
                playable = ensure_playable_seed(replace(config, world_seed=new_seed))
                streamer.shutdown_chunk_gen_pool()
                configure_world_gen(playable)
                spawn_score = score_spawn_area()
                flush_procedural_chunks(world, streamer, content, collision, extractor)
                streamer.update(
                    world,
                    focus_x,
                    focus_y,
                    content,
                    collision,
                    extractor,
                    view=stream_view,
                )
                world.rebuild_all_solid(content, collision)

            t_stream = time.perf_counter()
            step_metrics = None
            if perf_session is not None and perf_runtime is not None:
                perf_runtime.viewport_w = width
                perf_runtime.viewport_h = height
                perf_session.run_canonical_tick(
                    perf_runtime,
                    focus_x=focus_x,
                    focus_y=focus_y,
                    zoom=zoom,
                    move_dx=move_dx,
                    move_dy=move_dy,
                )
                loaded, unloaded = 0, 0
            else:
                if stream_diag_enabled:
                    from game_core.perf.models import StreamStepMetrics

                    step_metrics = StreamStepMetrics()
                loaded, unloaded = streamer.update(
                    world,
                    focus_x,
                    focus_y,
                    content,
                    collision,
                    extractor,
                    view=stream_view,
                    step_metrics=step_metrics,
                )
            last_focus_x, last_focus_y = focus_x, focus_y
            if not profile_enabled and (loaded or unloaded):
                stream_ms = (time.perf_counter() - t_stream) * 1000.0
                if stream_diag_enabled and step_metrics is not None:
                    print(
                        f"stream hitch: loaded={loaded} unloaded={unloaded} "
                        f"stream={stream_ms:.2f} ms chunks={world.chunk_count} "
                        f"terrain_applied={step_metrics.terrain_applied} "
                        f"deco_applied={step_metrics.deco_applied} "
                        f"sync_ms={step_metrics.apply_sync_generate_ms:.2f} "
                        f"sync_fallback={step_metrics.sync_fallback_triggered}",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"stream hitch: loaded={loaded} unloaded={unloaded} "
                        f"stream={stream_ms:.2f} ms chunks={world.chunk_count}",
                        file=sys.stderr,
                    )
            loaded_chunks = world.chunk_count

            if free_camera:
                move = CAM_MOVE_SPEED * dt / max(zoom, 0.1)
                cam_x += move_x * move
                cam_y += move_y * move
                player.tick_animation(dt)
            else:
                apply_character_movement(
                    player, world, content, collision, dt, move_x, move_y, force_run=force_run
                )
                cam_x, cam_y = player.camera_focus_x, player.camera_focus_y

            if key_held(frame, "E"):
                zoom *= ZOOM_SPEED ** dt
            if key_held(frame, "Q"):
                zoom /= ZOOM_SPEED ** dt
            if key_held(frame, "EQUAL"):
                zoom *= ZOOM_SPEED ** dt
            if key_held(frame, "MINUS"):
                zoom /= ZOOM_SPEED ** dt

            if frame.scroll_delta != 0.0:
                zoom *= ZOOM_SPEED ** (frame.scroll_delta * 0.25)

            zoom = max(0.18, min(zoom, 32.0))

            width, height = window.framebuffer_size
            camera = camera_from_viewport(cam_x, cam_y, zoom, width, height)

            if free_camera:
                if paint_mode in (PAINT_TERRAIN, PAINT_OVERLAY):
                    apply_paint_at_cursor(world, content, paint_mode, camera, frame)
                elif paint_mode == PAINT_DECORATION and content.decorations:
                    if frame.mouse_left:
                        decoration_id = content.decorations[decoration_index].id
                        _apply_decoration_brush(world, camera, frame, decoration_id)
                    if frame.mouse_right or key_held(frame, "X"):
                        _remove_decoration_brush(world, camera, frame)

            deco_sprites = decorations_to_sprites(
                content, renderer.sprite_catalog, world, camera=camera
            )
            player_sprite = character_to_sprite(renderer.sprite_catalog, player)
            sprites: tuple[SpriteInstanceData, ...] = deco_sprites + (player_sprite,)
            render_frame = extractor.extract(camera, sprites=sprites)
            if show_chunk_bounds:
                overlay = build_overlay_vertices(
                    [loaded_chunks_layer(world.chunks.keys())],
                    zoom=zoom,
                )
                render_frame = replace(render_frame, debug_overlay_vertices=overlay or None)
            last_visible_chunks = len(render_frame.tile_chunks)
            last_visible_tiles = sum(
                sum(len(layer.tile_ids) for layer in chunk.layers)
                for chunk in render_frame.tile_chunks
            )
            if perf_session is not None:
                timings: dict[str, float] = {}
                renderer.draw(
                    render_frame,
                    timing_fn=lambda k, v: timings.__setitem__(k, timings.get(k, 0.0) + v),
                )
                for k, v in timings.items():
                    perf_session.record_render_timing(k, v)
                full_ms = perf_session.end_full_frame()
                perf_session.finalize_pending_frame(cpu_full_frame_ms=full_ms)
            else:
                renderer.draw(render_frame)

            if fps_counter.tick(dt):
                mode = "free cam" if free_camera else "follow"
                fs = "fullscreen" if window.is_fullscreen else "windowed"
                paint_label = _paint_mode_label(paint_mode, content, decoration_index)
                perf_suffix = ""
                if perf_session is not None and perf_session._total_ticks > perf_session._warmup_frames:
                    perf_suffix = (
                        f" | prof stream {perf_session.rolling_stream_ms_mean:.1f} ms"
                        f" hitches {perf_session.rolling_hitch_count}"
                        f" chunks {perf_session.rolling_chunk_count}"
                    )
                bounds_label = "chunk bounds ON" if show_chunk_bounds else "chunk bounds OFF"
                window.set_window_title(
                    f"{WINDOW_TITLE_BASE} | {fps_counter.fps:.0f} FPS | {mode} | {fs} | "
                    f"seed {get_world_gen_config().world_seed} score {spawn_score:.2f} | "
                    f"{player.clip.value} f{player.current_frame} | "
                    f"visible {last_visible_chunks} loaded {loaded_chunks} tiles {last_visible_tiles} | "
                    f"{bounds_label} (C) | "
                    f"paint {paint_label} (1/2/3) | [/] | F cam | F11 fs | G regen | Shift run | Ctrl+S/L stream"
                    f"{perf_suffix}",
                )
    finally:
        if perf_session is not None:
            export_dir = perf_session.flush()
            print(f"Profiling export: {export_dir}", file=sys.stderr)
        streamer.shutdown_chunk_gen_pool()
        renderer.destroy()
        window.destroy()

    return 0


if __name__ == "__main__":
    sys.exit(main())
