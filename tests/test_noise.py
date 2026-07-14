"""Tests — Simplex/fBM Noise (M21)."""

from __future__ import annotations

from game_core.noise import FbmParams, domain_warp_xy, precalc_fbm, sample_fbm, simplex2d, simplex2d_01


def test_simplex_deterministic() -> None:
    a = simplex2d(12.5, 34.7, 99)
    b = simplex2d(12.5, 34.7, 99)
    c = simplex2d(12.5, 34.7, 100)
    assert a == b
    assert a != c


def test_simplex_01_range() -> None:
    for index in range(20):
        value = simplex2d_01(float(index) * 3.7, float(index) * 1.3, 7)
        assert 0.0 <= value <= 1.0


def test_fbm_normalized() -> None:
    precalc = precalc_fbm(
        FbmParams(octaves=4, lacunarity=2.0, persistence=0.5, scale=0.01, seed=42)
    )
    value = sample_fbm(100.0, 200.0, precalc)
    assert 0.0 <= value <= 1.0


def test_domain_warp_deterministic() -> None:
    a = domain_warp_xy(50.0, 60.0, frequency=0.01, magnitude=10.0, seed=5)
    b = domain_warp_xy(50.0, 60.0, frequency=0.01, magnitude=10.0, seed=5)
    assert a == b
