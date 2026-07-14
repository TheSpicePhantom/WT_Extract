"""Charakter — Position, 8-Richtungs-Spritesheets, Idle/Walk/Run."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

CHARACTER_LAYER = 2
CHARACTER_SPRITE_PX = 64.0
# Schrittweite pro Animationszyklus — speed = stride * fps / frame_count
WALK_STRIDE_PX = 32.0
RUN_STRIDE_PX = 56.0

# Zeilen im Spritesheet (Index 0…7 = R1…R8):
# R1 links oben, R2 links, R3 links unten, R4 zugewandt,
# R5 rechts unten, R6 rechts, R7 rechts oben, R8 abgewandt
# Bewegungs-Oktant (atan2) → Sheet-Zeile
_OCT_TO_ROW = (5, 6, 7, 0, 1, 2, 3, 4)


class AnimClip(str, Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"


CLIP_SPRITE_KEYS: dict[AnimClip, str] = {
    AnimClip.IDLE: "wt:character/idle/idle",
    AnimClip.WALK: "wt:character/walk/walk",
    AnimClip.RUN: "wt:character/run/run",
}

CLIP_FRAME_COUNT: dict[AnimClip, int] = {
    AnimClip.IDLE: 12,
    AnimClip.WALK: 8,
    AnimClip.RUN: 8,
}

CLIP_FPS: dict[AnimClip, float] = {
    AnimClip.IDLE: 8.0,
    AnimClip.WALK: 10.0,
    AnimClip.RUN: 14.0,
}

CLIP_STRIDE_PX: dict[AnimClip, float] = {
    AnimClip.WALK: WALK_STRIDE_PX,
    AnimClip.RUN: RUN_STRIDE_PX,
}


def move_speed_for_clip(clip: AnimClip) -> float:
    """Welt-Pixel/s — ein Animationszyklus = eine Schrittweite."""
    frames = CLIP_FRAME_COUNT[clip]
    if frames <= 0:
        return 0.0
    return CLIP_STRIDE_PX[clip] * CLIP_FPS[clip] / frames


def direction_from_delta(dx: float, dy: float, fallback: int) -> int:
    """Bewegungsvektor → Sheet-Zeile 0..7 (8-Wege)."""
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return fallback
    angle = math.atan2(dy, dx)
    if angle < 0.0:
        angle += 2.0 * math.pi
    octant = int((angle + math.pi / 8.0) / (math.pi / 4.0)) % 8
    return _OCT_TO_ROW[octant]


@dataclass
class Character:
    """Spielerfigur — Welt-Pixel, Anker unten links (64×64 Sprite)."""

    world_x: float
    world_y: float
    direction: int = 3  # R4 zugewandt (Standard-Blick)
    clip: AnimClip = AnimClip.IDLE
    anim_time: float = 0.0
    force_run: bool = False

    @property
    def sprite_key(self) -> str:
        return CLIP_SPRITE_KEYS[self.clip]

    @property
    def frame_count(self) -> int:
        return CLIP_FRAME_COUNT[self.clip]

    @property
    def current_frame(self) -> int:
        fps = CLIP_FPS[self.clip]
        index = int(self.anim_time * fps) % self.frame_count
        return index

    @property
    def camera_focus_x(self) -> float:
        return self.world_x + CHARACTER_SPRITE_PX * 0.5

    @property
    def camera_focus_y(self) -> float:
        return self.world_y + CHARACTER_SPRITE_PX * 0.5

    @classmethod
    def at_center(cls, center_x: float, center_y: float) -> Character:
        """Anker so setzen, dass die Sprite-Mitte auf (center_x, center_y) liegt."""
        half = CHARACTER_SPRITE_PX * 0.5
        return cls(world_x=center_x - half, world_y=center_y - half)

    def tick_animation(self, dt: float) -> None:
        self.anim_time += max(dt, 0.0)

    def apply_input(
        self,
        dt: float,
        move_x: float,
        move_y: float,
        *,
        force_run: bool = False,
    ) -> None:
        """move_x/move_y in {-1,0,1} — aktualisiert Clip, Richtung und Position."""
        self.force_run = force_run
        dx = float(move_x)
        dy = float(move_y)
        speed_len = math.hypot(dx, dy)

        if speed_len > 1e-6:
            dx /= speed_len
            dy /= speed_len
            self.direction = direction_from_delta(dx, dy, self.direction)
            if force_run:
                self.clip = AnimClip.RUN
                scalar_speed = move_speed_for_clip(AnimClip.RUN)
            else:
                self.clip = AnimClip.WALK
                scalar_speed = move_speed_for_clip(AnimClip.WALK)
            self.world_x += dx * scalar_speed * dt
            self.world_y += dy * scalar_speed * dt
        else:
            self.clip = AnimClip.IDLE

        self.tick_animation(dt)
