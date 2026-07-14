"""Tests — Export und Compare (M23 Phase 3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from game_core.perf.export_schema import SCHEMA_VERSION, validate_summary
from tools.compare_perf_runs import compare_runs
from tools.run_perf_scenario import run_perf_scenario


def test_export_has_required_fields(tmp_path: Path) -> None:
    run_dir = run_perf_scenario("steady", run_mode="cli", run_dir=tmp_path / "run")
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    validate_summary(summary)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == SCHEMA_VERSION
    assert "config_fingerprint" in manifest


def test_compare_rejects_unknown_schema_version(tmp_path: Path) -> None:
    baseline = run_perf_scenario("steady", run_mode="cli", run_dir=tmp_path / "base")
    candidate = tmp_path / "bad"
    candidate.mkdir()
    for name in ("manifest.json", "summary.json"):
        data = json.loads((baseline / name).read_text(encoding="utf-8"))
        data["schema_version"] = 99
        (candidate / name).write_text(json.dumps(data), encoding="utf-8")
    (candidate / "frames.jsonl").write_text("", encoding="utf-8")
    (candidate / "hitches.jsonl").write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported schema_version"):
        compare_runs(baseline, candidate)


def test_compare_additive_optional_fields_ok(tmp_path: Path) -> None:
    baseline = run_perf_scenario("steady", run_mode="cli", run_dir=tmp_path / "base")
    candidate = run_perf_scenario("steady", run_mode="cli", run_dir=tmp_path / "cand")
    summary_path = candidate / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["optional_note"] = "additive field"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    deltas = compare_runs(baseline, candidate)
    assert deltas["scenario_id"] == "steady"
    assert "tile_extract_ms_p95_baseline" in deltas
    assert "extract_ms_max_candidate" in deltas
