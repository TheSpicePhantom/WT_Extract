"""A/B-Vergleich für fps_killers.json (M25a)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game_core.perf.run_analysis.diagnose import analyze_run, load_budget_caps
from game_core.perf.run_analysis.fps_killers import build_ab_comparison, fps_killers_payload
from game_core.perf.run_analysis.load import RunLoadError, load_run


def _infer_causal_feature(baseline: dict, variant: dict) -> str:
    base_toggles = baseline.get("toggles") or {}
    var_toggles = variant.get("toggles") or {}
    for key in ("extract_enabled", "stream_enabled", "deco_extract_enabled", "tile_extract_enabled"):
        if base_toggles.get(key) != var_toggles.get(key):
            return key
    return "unknown_toggle"


def compare_fps_killers(
    baseline_dir: Path,
    variant_dir: Path,
    *,
    causal_feature: str | None = None,
) -> dict:
    baseline_loaded = load_run(baseline_dir)
    variant_loaded = load_run(variant_dir)

    if baseline_loaded.manifest.get("scenario_id") != variant_loaded.manifest.get("scenario_id"):
        raise ValueError(
            "scenario_id mismatch: "
            f"{baseline_loaded.manifest.get('scenario_id')} vs "
            f"{variant_loaded.manifest.get('scenario_id')}"
        )

    baseline_payload = fps_killers_payload(
        baseline_loaded.frames,
        manifest=baseline_loaded.manifest,
        hitch_analyses=analyze_run(baseline_loaded, caps=load_budget_caps(project_root=PROJECT_ROOT)).hitch_analyses,
    )
    variant_payload = fps_killers_payload(
        variant_loaded.frames,
        manifest=variant_loaded.manifest,
        hitch_analyses=analyze_run(variant_loaded, caps=load_budget_caps(project_root=PROJECT_ROOT)).hitch_analyses,
    )

    feature = causal_feature or _infer_causal_feature(baseline_payload, variant_payload)
    ab_entry = build_ab_comparison(baseline_payload, variant_payload, causal_feature=feature)

    merged = dict(baseline_payload)
    merged["ab_comparisons"] = [ab_entry]
    merged["ab_baseline_run_id"] = baseline_payload.get("run_id")
    merged["ab_variant_run_id"] = variant_payload.get("run_id")
    return merged


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vergleicht zwei Runs für M25a fps_killers A/B.")
    parser.add_argument("baseline_dir", type=Path, help="Baseline-Run-Verzeichnis")
    parser.add_argument("variant_dir", type=Path, help="Variant-Run-Verzeichnis")
    parser.add_argument(
        "--causal-feature",
        type=str,
        default=None,
        help="Feature-Name für Kausalität (z. B. extract_enabled)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Ausgabe fps_killers_ab.json (Standard: baseline_dir/analysis/)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        merged = compare_fps_killers(
            args.baseline_dir.resolve(),
            args.variant_dir.resolve(),
            causal_feature=args.causal_feature,
        )
    except (RunLoadError, ValueError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    output = args.output
    if output is None:
        output = args.baseline_dir.resolve() / "analysis" / "fps_killers_ab.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"A/B fps_killers geschrieben: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
