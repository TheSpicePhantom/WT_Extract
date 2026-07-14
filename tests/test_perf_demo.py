"""Tests — Demo-Profiling (M23 Phase 4)."""

from __future__ import annotations

import json
from pathlib import Path

from game_core.perf.config import ProfilingConfig, HitchThresholds, ScenarioParams
from game_core.perf.session import PerfSession
from tools.run_perf_scenario import build_scenario_runtime


def test_demo_run_mode_export(tmp_path: Path) -> None:
    fast_config = ProfilingConfig(
        enabled=True,
        hitch=HitchThresholds(stream_ms=8.0, frame_ms=16.0, loaded_count=4, unloaded_count=4),
        scenarios={"steady": ScenarioParams(frames=3, warmup_frames=1)},
        ring_buffer_frames=10,
    )
    session = PerfSession(
        config=fast_config,
        scenario_id="demo",
        run_mode="demo",
        extract_enabled=True,
    )
    session._warmup_frames = 1
    rt = build_scenario_runtime(use_mock_invalidator=True)

    for tick in range(4):
        frame = session.run_canonical_tick(
            rt,
            focus_x=256.0 + tick * 32,
            focus_y=256.0,
            zoom=0.35,
            move_dx=32.0 if tick > 0 else 0.0,
            move_dy=0.0,
        )
        if frame is not None:
            assert session.rolling_stream_ms_mean >= 0.0

    run_dir = session.flush(tmp_path / "demo_run")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_mode"] == "demo"
    assert manifest["scenario_id"] == "demo"
    lines = (run_dir / "frames.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
