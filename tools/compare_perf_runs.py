"""Vergleich von Performance-Runs (M23)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.export_schema import (
    SCHEMA_VERSION,
    assert_supported_schema_version,
    load_summary,
    validate_manifest,
)
from game_core.perf.run_analysis.extract_kpis import extract_kpis_from_run


def _load_manifest(run_dir: Path) -> dict:
    path = run_dir / "manifest.json"
    if not path.is_file():
        raise FileNotFoundError(f"manifest.json missing in {run_dir}")
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_manifest(data)
    return data


def compare_runs(baseline_dir: Path, candidate_dir: Path) -> dict[str, float | int | str]:
    baseline_manifest = _load_manifest(baseline_dir)
    candidate_manifest = _load_manifest(candidate_dir)

    baseline_summary = load_summary(baseline_dir / "summary.json")
    candidate_summary = load_summary(candidate_dir / "summary.json")

    if baseline_manifest["scenario_id"] != candidate_manifest["scenario_id"]:
        raise ValueError(
            "scenario_id mismatch: "
            f"{baseline_manifest['scenario_id']} vs {candidate_manifest['scenario_id']}"
        )

    deltas: dict[str, float | int | str] = {
        "baseline_run_id": baseline_manifest["run_id"],
        "candidate_run_id": candidate_manifest["run_id"],
        "scenario_id": baseline_manifest["scenario_id"],
        "schema_version": SCHEMA_VERSION,
    }
    for key in (
        "frame_ms_mean",
        "frame_ms_p95",
        "frame_ms_max",
        "stream_ms_mean",
        "stream_ms_p95",
        "stream_ms_max",
        "hitch_count",
    ):
        base_val = float(baseline_summary[key])
        cand_val = float(candidate_summary[key])
        deltas[f"{key}_baseline"] = base_val
        deltas[f"{key}_candidate"] = cand_val
        deltas[f"{key}_delta"] = cand_val - base_val
        if base_val != 0.0:
            deltas[f"{key}_delta_pct"] = (cand_val - base_val) / base_val * 100.0
        else:
            deltas[f"{key}_delta_pct"] = 0.0 if cand_val == 0.0 else float("inf")

    baseline_extract = extract_kpis_from_run(baseline_dir)
    candidate_extract = extract_kpis_from_run(candidate_dir)
    all_extract_keys = sorted(set(baseline_extract) | set(candidate_extract))
    for key in all_extract_keys:
        base_val = float(baseline_extract.get(key, 0.0))
        cand_val = float(candidate_extract.get(key, 0.0))
        deltas[f"{key}_baseline"] = base_val
        deltas[f"{key}_candidate"] = cand_val
        deltas[f"{key}_delta"] = cand_val - base_val
        if base_val != 0.0:
            deltas[f"{key}_delta_pct"] = (cand_val - base_val) / base_val * 100.0
        else:
            deltas[f"{key}_delta_pct"] = 0.0 if cand_val == 0.0 else float("inf")
    return deltas


def main() -> int:
    parser = argparse.ArgumentParser(description="Vergleiche zwei Performance-Runs (M23)")
    parser.add_argument("baseline", type=Path, help="Baseline-Run-Verzeichnis")
    parser.add_argument("candidate", type=Path, help="Kandidaten-Run-Verzeichnis")
    parser.add_argument(
        "--schema-version",
        type=int,
        default=None,
        help="Erwartete schema_version (Standard: unterstützte Version prüfen)",
    )
    args = parser.parse_args()

    if args.schema_version is not None:
        assert_supported_schema_version(args.schema_version)

    try:
        deltas = compare_runs(args.baseline, args.candidate)
    except ValueError as exc:
        print(f"compare failed: {exc}", file=sys.stderr)
        return 1

    print(f"=== Compare {deltas['scenario_id']} ===")
    print(f"  baseline:  {deltas['baseline_run_id']}")
    print(f"  candidate: {deltas['candidate_run_id']}")
    for metric in ("frame_ms_mean", "frame_ms_p95", "stream_ms_p95", "hitch_count"):
        base = deltas[f"{metric}_baseline"]
        cand = deltas[f"{metric}_candidate"]
        delta = deltas[f"{metric}_delta"]
        pct = deltas[f"{metric}_delta_pct"]
        print(f"  {metric:16s} {base:10.3f} -> {cand:10.3f}  ({delta:+.3f}, {pct:+.1f}%)")
    batching_metrics = (
        "tile_registry_hits_mean",
        "tile_cull_cache_hits_mean",
    )
    for metric in (
        "tile_extract_ms_mean",
        "tile_extract_ms_p95",
        "tile_extract_ms_max",
        "extract_ms_p95",
        "extract_ms_max",
        "deco_extract_ms_max",
        *batching_metrics,
    ):
        base_key = f"{metric}_baseline"
        if base_key not in deltas:
            continue
        base = deltas[base_key]
        cand = deltas[f"{metric}_candidate"]
        delta = deltas[f"{metric}_delta"]
        pct = deltas[f"{metric}_delta_pct"]
        print(f"  {metric:22s} {base:10.3f} -> {cand:10.3f}  ({delta:+.3f}, {pct:+.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
