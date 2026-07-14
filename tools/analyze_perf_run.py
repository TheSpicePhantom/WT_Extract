"""Profiling-Run analysieren — CLI (M23/M23a)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.diagnose import analyze_run, load_budget_caps
from game_core.perf.run_analysis.load import RunLoadError, load_run
from game_core.perf.run_analysis.report import format_terminal_summary, write_all_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Diagnostische Analyse eines exportierten Profiling-Runs (schema_version=1)."
    )
    parser.add_argument(
        "run_dir",
        type=Path,
        nargs="?",
        help="Verzeichnis mit manifest.json, summary.json, frames.jsonl, hitches.jsonl",
    )
    parser.add_argument("--manifest", type=Path, help="Alternativ: Pfad zu manifest.json")
    parser.add_argument("--summary", type=Path, help="Pfad zu summary.json")
    parser.add_argument("--frames", type=Path, help="Pfad zu frames.jsonl")
    parser.add_argument("--hitches", type=Path, help="Pfad zu hitches.jsonl")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Ausgabeordner für Report/CSV/JSON (Standard: <run_dir>/analysis)",
    )
    parser.add_argument(
        "--context-radius",
        type=int,
        default=3,
        help="Frames vor/nach jedem Hitch für Kontextanalyse (Standard: 3)",
    )
    parser.add_argument(
        "--max-applies",
        type=int,
        help="Apply-Cap-Override für Budget-Analyse",
    )
    parser.add_argument(
        "--max-unloads",
        type=int,
        help="Unload-Cap-Override für Budget-Analyse",
    )
    parser.add_argument(
        "--no-files",
        action="store_true",
        help="Nur Terminal-Ausgabe, keine Report-Dateien schreiben",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.run_dir is None and args.manifest is None:
        parser.error("run_dir oder --manifest angeben.")

    try:
        loaded = load_run(
            args.run_dir,
            manifest=args.manifest,
            summary=args.summary,
            frames=args.frames,
            hitches=args.hitches,
        )
        caps = load_budget_caps(
            project_root=PROJECT_ROOT,
            max_applies=args.max_applies,
            max_unloads=args.max_unloads,
        )
        diagnosis = analyze_run(loaded, caps=caps, context_radius=args.context_radius)
    except RunLoadError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    print(format_terminal_summary(diagnosis))

    if not args.no_files:
        output_dir = args.output_dir or (loaded.run_dir / "analysis")
        paths = write_all_reports(diagnosis, output_dir)
        print("")
        print("Report geschrieben:")
        for label, path in paths.items():
            print(f"  {label}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
