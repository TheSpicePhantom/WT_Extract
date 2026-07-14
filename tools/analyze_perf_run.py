"""Profiling-Run analysieren — CLI (M23/M23a)."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RUNS_DIR = PROJECT_ROOT / "docs" / "benchmarks" / "perf" / "runs"
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.diagnose import analyze_run, load_budget_caps
from game_core.perf.run_analysis.load import RunLoadError, load_run
from game_core.perf.run_analysis.report import format_terminal_summary, write_all_reports


@dataclass(frozen=True, slots=True)
class AnalyzeArgs:
    run_dir: Path | None
    manifest: Path | None
    summary: Path | None
    frames: Path | None
    hitches: Path | None
    output_dir: Path | None
    context_radius: int
    max_applies: int | None
    max_unloads: int | None
    no_files: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Diagnostische Analyse exportierter Profiling-Runs (schema_version=1)."
    )
    parser.add_argument(
        "run_dir",
        type=Path,
        nargs="?",
        help="Run-Verzeichnis (manifest/summary/frames/hitches). "
        "Ohne Argument: alle Runs unter docs/benchmarks/perf/runs/",
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


def discover_run_dirs(runs_root: Path = DEFAULT_RUNS_DIR) -> list[Path]:
    """Alle Run-Ordner mit manifest.json unter runs_root (sortiert nach Name)."""
    if not runs_root.is_dir():
        return []
    candidates: list[Path] = []
    for child in runs_root.iterdir():
        if not child.is_dir():
            continue
        if (child / "manifest.json").is_file():
            candidates.append(child)
    return sorted(candidates, key=lambda path: path.name)


def analyze_one_run(args: AnalyzeArgs, *, run_dir: Path | None = None) -> int:
    target = run_dir if run_dir is not None else args.run_dir
    try:
        loaded = load_run(
            target,
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
        label = target or args.manifest or "?"
        print(f"Fehler ({label}): {exc}", file=sys.stderr)
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


def _args_from_namespace(args: argparse.Namespace) -> AnalyzeArgs:
    return AnalyzeArgs(
        run_dir=args.run_dir,
        manifest=args.manifest,
        summary=args.summary,
        frames=args.frames,
        hitches=args.hitches,
        output_dir=args.output_dir,
        context_radius=args.context_radius,
        max_applies=args.max_applies,
        max_unloads=args.max_unloads,
        no_files=args.no_files,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    analyze_args = _args_from_namespace(ns)

    if analyze_args.manifest is not None:
        return analyze_one_run(analyze_args)

    if analyze_args.run_dir is not None:
        return analyze_one_run(analyze_args)

    run_dirs = discover_run_dirs()
    if not run_dirs:
        print(f"Keine Runs gefunden unter {DEFAULT_RUNS_DIR}", file=sys.stderr)
        return 1

    print(f"Analysiere {len(run_dirs)} Run(s) unter {DEFAULT_RUNS_DIR}\n")
    failures = 0
    for index, run_dir in enumerate(run_dirs, start=1):
        if index > 1:
            print("\n" + "=" * 72 + "\n")
        print(f"[{index}/{len(run_dirs)}] {run_dir.name}")
        print("-" * 72)
        per_run = AnalyzeArgs(
            run_dir=run_dir,
            manifest=None,
            summary=None,
            frames=None,
            hitches=None,
            output_dir=None,
            context_radius=analyze_args.context_radius,
            max_applies=analyze_args.max_applies,
            max_unloads=analyze_args.max_unloads,
            no_files=analyze_args.no_files,
        )
        if analyze_one_run(per_run, run_dir=run_dir) != 0:
            failures += 1

    print("\n" + "=" * 72)
    ok = len(run_dirs) - failures
    print(f"Fertig: {ok}/{len(run_dirs)} erfolgreich, {failures} fehlgeschlagen.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
