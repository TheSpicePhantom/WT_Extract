"""2D Simplex Noise, fBM und Domain Warp — deterministisch, seed-basiert."""

from __future__ import annotations

import math
from dataclasses import dataclass

_F2 = 0.5 * (math.sqrt(3.0) - 1.0)
_G2 = (3.0 - math.sqrt(3.0)) / 6.0

_GRAD2 = (
    (1.0, 1.0),
    (-1.0, 1.0),
    (1.0, -1.0),
    (-1.0, -1.0),
    (1.0, 0.0),
    (-1.0, 0.0),
    (0.0, 1.0),
    (0.0, -1.0),
)

_PERM_CACHE: dict[int, tuple[int, ...]] = {}


def _lcg(state: int) -> int:
    return (state * 1664525 + 1013904223) & 0xFFFFFFFF


def _build_perm(seed: int) -> tuple[int, ...]:
    cached = _PERM_CACHE.get(seed)
    if cached is not None:
        return cached
    perm = list(range(256))
    state = seed & 0xFFFFFFFF
    for index in range(255, 0, -1):
        state = _lcg(state)
        swap = state % (index + 1)
        perm[index], perm[swap] = perm[swap], perm[index]
    result = tuple(perm + perm)
    _PERM_CACHE[seed] = result
    return result


def get_perm(seed: int) -> tuple[int, ...]:
    """Vorgebaute Permutation — einmal pro Seed (M24c)."""
    return _build_perm(seed)


def clear_perm_cache() -> None:
    _PERM_CACHE.clear()


def _grad2(hash_value: int, x: float, y: float) -> float:
    gradient = _GRAD2[hash_value & 7]
    return gradient[0] * x + gradient[1] * y


def simplex2d_perm(x: float, y: float, perm: tuple[int, ...]) -> float:
    """Simplex-Noise mit vorgebauter Permutation."""
    s = (x + y) * _F2
    i = math.floor(x + s)
    j = math.floor(y + s)
    t = (i + j) * _G2
    x0 = x - (i - t)
    y0 = y - (j - t)
    if x0 > y0:
        i1, j1 = 1, 0
    else:
        i1, j1 = 0, 1
    x1 = x0 - i1 + _G2
    y1 = y0 - j1 + _G2
    x2 = x0 - 1.0 + 2.0 * _G2
    y2 = y0 - 1.0 + 2.0 * _G2
    ii = int(i) & 255
    jj = int(j) & 255
    gi0 = perm[ii + perm[jj]]
    gi1 = perm[ii + i1 + perm[jj + j1]]
    gi2 = perm[ii + 1 + perm[jj + 1]]
    n0 = n1 = n2 = 0.0
    t0 = 0.5 - x0 * x0 - y0 * y0
    if t0 >= 0.0:
        t0 *= t0
        n0 = t0 * t0 * _grad2(gi0, x0, y0)
    t1 = 0.5 - x1 * x1 - y1 * y1
    if t1 >= 0.0:
        t1 *= t1
        n1 = t1 * t1 * _grad2(gi1, x1, y1)
    t2 = 0.5 - x2 * x2 - y2 * y2
    if t2 >= 0.0:
        t2 *= t2
        n2 = t2 * t2 * _grad2(gi2, x2, y2)
    return 70.0 * (n0 + n1 + n2)


def simplex2d(x: float, y: float, seed: int) -> float:
    """Simplex-Noise in etwa [-1, 1]."""
    return simplex2d_perm(x, y, get_perm(seed))


def simplex2d_01(x: float, y: float, seed: int) -> float:
    """Simplex-Noise normalisiert auf [0, 1]."""
    return max(0.0, min(1.0, simplex2d(x, y, seed) * 0.5 + 0.5))


@dataclass(frozen=True, slots=True)
class FbmParams:
    octaves: int
    lacunarity: float
    persistence: float
    scale: float
    seed: int
    offset_x: float = 0.0
    offset_y: float = 0.0


@dataclass(frozen=True, slots=True)
class FbmPrecalc:
    frequencies: tuple[float, ...]
    amplitudes: tuple[float, ...]
    max_amplitude: float
    scale: float
    seed: int
    offset_x: float
    offset_y: float
    perm: tuple[int, ...]


def precalc_fbm(params: FbmParams) -> FbmPrecalc:
    frequencies: list[float] = []
    amplitudes: list[float] = []
    frequency = 1.0
    amplitude = 1.0
    max_amplitude = 0.0
    for _ in range(max(1, params.octaves)):
        frequencies.append(frequency)
        amplitudes.append(amplitude)
        max_amplitude += amplitude
        frequency *= params.lacunarity
        amplitude *= params.persistence
    return FbmPrecalc(
        frequencies=tuple(frequencies),
        amplitudes=tuple(amplitudes),
        max_amplitude=max_amplitude,
        scale=params.scale,
        seed=params.seed,
        offset_x=params.offset_x,
        offset_y=params.offset_y,
        perm=get_perm(params.seed),
    )


def sample_fbm(wx: float, wy: float, precalc: FbmPrecalc) -> float:
    """fBM-Summe normalisiert auf [0, 1]."""
    from game_core.terrain_gen_profile import profile_section, record_counter

    sx = (wx + precalc.offset_x) * precalc.scale
    sy = (wy + precalc.offset_y) * precalc.scale
    total = 0.0
    with profile_section("noise_fbm"):
        for frequency, amplitude in zip(precalc.frequencies, precalc.amplitudes, strict=True):
            with profile_section("noise_simplex"):
                sample = simplex2d_perm(sx * frequency, sy * frequency, precalc.perm)
                record_counter("simplex_samples")
            total += sample * amplitude
    if precalc.max_amplitude <= 0.0:
        return 0.5
    normalized = total / precalc.max_amplitude
    return max(0.0, min(1.0, normalized * 0.5 + 0.5))


def domain_warp_xy(
    wx: float,
    wy: float,
    *,
    frequency: float,
    magnitude: float,
    seed: int,
) -> tuple[float, float]:
    """2D Domain Warp — Offset aus zwei Simplex-Feldern."""
    from game_core.terrain_gen_profile import profile_section

    nx = wx * frequency + seed * 0.0137
    ny = wy * frequency + seed * 0.0241
    with profile_section("noise_simplex"):
        perm_a = get_perm(seed ^ 0xA3C59AC3)
        perm_b = get_perm(seed ^ 0xC3A59AC3)
        offset_x = simplex2d_perm(nx, ny, perm_a) * magnitude
        offset_y = simplex2d_perm(nx + 19.7, ny + 31.3, perm_b) * magnitude
    return wx + offset_x, wy + offset_y
