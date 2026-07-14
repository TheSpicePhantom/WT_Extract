"""Tests — Szenario-Runner und kanonischer Tick (M23 Phase 2)."""

from __future__ import annotations

import json
from pathlib import Path

from game_core.perf.config import load_profiling_config
from game_core.perf.scenarios import scenario_descriptor
from tools.run_perf_scenario import run_perf_scenario


def test_warmup_excluded_from_export() -> None:
    config = load_profiling_config()
    descriptor = scenario_descriptor(config, "steady")
    run_dir = run_perf_scenario("steady", run_mode="cli")
    frames_path = run_dir / "frames.jsonl"
    lines = frames_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == descriptor.frames
    first = json.loads(lines[0])
    assert first["frame_index"] == 0


def test_cli_run_produces_all_artifacts(tmp_path: Path) -> None:
    run_dir = run_perf_scenario("steady", run_mode="cli", run_dir=tmp_path / "run")
    for name in ("manifest.json", "frames.jsonl", "hitches.jsonl", "summary.json"):
        assert (run_dir / name).is_file()
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_mode"] == "cli"
    assert manifest["schema_version"] == 1
