"""CPU-Profil — delegiert an gemeinsamen Szenario-Runner (M23)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.config import load_profiling_config
from tools.run_perf_scenario import print_run_summary, run_perf_scenario


def main() -> int:
    config = load_profiling_config()
    scenarios = sorted(config.scenarios.keys())

    parser = argparse.ArgumentParser(
        description="CPU-Profil für kanonischen Tick (steady/pan via profiling.json)",
    )
    parser.add_argument(
        "--scenario",
        choices=scenarios,
        default=None,
        help="Szenario-ID (Standard: steady, oder --mode pan -> pan)",
    )
    parser.add_argument(
        "--mode",
        choices=("steady", "pan"),
        default=None,
        help="Legacy-Alias: steady oder pan",
    )
    parser.add_argument(
        "--no-extract",
        action="store_true",
        help="Extract-Pfad deaktivieren",
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=None,
        help="Export-Zielverzeichnis",
    )
    args = parser.parse_args()

    scenario_id = args.scenario
    if scenario_id is None:
        if args.mode == "pan":
            scenario_id = "pan"
        else:
            scenario_id = "steady"

    run_dir = run_perf_scenario(
        scenario_id,
        run_mode="cli",
        extract_enabled=not args.no_extract,
        run_dir=args.run_dir,
    )
    print_run_summary(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
