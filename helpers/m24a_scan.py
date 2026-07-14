"""Codebase-Scan für M24a-Fragen — Call-Sites, Scans, Metriken."""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_CORE = PROJECT_ROOT / "game_core"
BRIDGE = PROJECT_ROOT / "bridge"
TESTS = PROJECT_ROOT / "tests"
APPS = PROJECT_ROOT / "apps"
TOOLS = PROJECT_ROOT / "tools"


@dataclass
class CallSite:
    file: str
    line: int
    context: str
    category: str = ""


def _iter_py_files(*roots: Path) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        files.extend(sorted(root.rglob("*.py")))
    return files


def grep_pattern(pattern: str, *roots: Path, exclude_tests: bool = False) -> list[CallSite]:
    rx = re.compile(pattern)
    sites: list[CallSite] = []
    for path in _iter_py_files(*roots):
        if exclude_tests and "tests" in path.parts:
            continue
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                sites.append(CallSite(file=rel, line=index, context=line.strip()))
    return sites


def classify_decorations_scans(sites: list[CallSite]) -> dict[str, list[dict]]:
    categories: dict[str, list[dict]] = {
        "load_hotpath": [],
        "collision_navigation": [],
        "unload_pending_revive": [],
        "render_extract": [],
        "save_persistenz": [],
        "world_mutation": [],
        "debug_tools_legacy": [],
        "tests_only": [],
    }

    def put(cat: str, site: CallSite, notes: str = "") -> None:
        entry = asdict(site)
        entry["notes"] = notes
        categories[cat].append(entry)

    for site in sites:
        f = site.file
        ctx = site.context
        if f.startswith("tests/"):
            put("tests_only", site)
            continue
        if "collision_grid.py" in f and "for placed in world.decorations" in ctx:
            put("collision_navigation", site, "O(D) pro rebuild_chunk_solid")
        elif "chunk_streaming.py" in f:
            if "_chunk_has_procedural_deco" in f or "_has_user_decorations" in ctx:
                put("unload_pending_revive" if "procedural_deco" in ctx else "load_hotpath", site, "O(D)")
            else:
                put("unload_pending_revive", site, "O(D)")
        elif "world_gen.py" in f and "remove_" in ctx:
            put("unload_pending_revive", site, "O(D) pro Unload")
        elif "decoration_extractor.py" in f:
            put("render_extract", site, "O(D) pro Frame")
        elif "streaming_world_io.py" in f or "world_io.py" in f:
            put("save_persistenz", site, "O(D) bei Save")
        elif "world.py" in f:
            if "place_decoration" in ctx or "enumerate(self.decorations)" in ctx:
                put("world_mutation", site, "O(D) pro place_decoration-Aufruf")
            elif "decoration_at_tile" in ctx:
                put("collision_navigation", site, "O(D) pro Query")
            else:
                put("world_mutation", site)
        elif "navigation.py" in f:
            put("collision_navigation", site)
        elif "benchmark" in f or "tools/" in f:
            put("debug_tools_legacy", site)
        else:
            put("debug_tools_legacy", site)

    return categories


def scan_rebuild_chunk_solid() -> list[dict]:
    patterns = [
        r"rebuild_chunk_solid\s*\(",
        r"\.rebuild_chunk_solid\s*\(",
        r"build_chunk_solid_grid\s*\(",
    ]
    seen: set[tuple[str, int]] = set()
    out: list[dict] = []
    for pattern in patterns:
        for site in grep_pattern(pattern, GAME_CORE, BRIDGE, TESTS, TOOLS, APPS):
            key = (site.file, site.line)
            if key in seen:
                continue
            seen.add(key)
            out.append(asdict(site))
    return sorted(out, key=lambda x: (x["file"], x["line"]))


def scan_ensure_collision_fresh() -> list[dict]:
    return [asdict(s) for s in grep_pattern(r"ensure_collision_fresh\s*\(", GAME_CORE, TESTS, APPS)]


def scan_world_decorations() -> list[dict]:
    return [asdict(s) for s in grep_pattern(r"world\.decorations|self\.decorations", GAME_CORE, BRIDGE, TESTS, TOOLS)]


def read_streaming_defer_flush_snippet() -> dict:
    path = GAME_CORE / "chunk_streaming.py"
    lines = path.read_text(encoding="utf-8").splitlines()
    snippets: dict[str, list[str]] = {}
    for name, start in [
        ("worker_apply", 268),
        ("update_pool_apply", 445),
        ("sync_load", 481),
        ("flush_deferred", 505),
    ]:
        end = min(start + 25, len(lines))
        snippets[name] = [f"{i + 1}:{lines[i]}" for i in range(start - 1, end)]
    return snippets


def load_single_chunk_benchmark() -> dict | None:
    path = PROJECT_ROOT / "docs" / "benchmarks" / "single_chunk_64.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def run_analysis() -> dict:
    deco_sites = grep_pattern(r"for .* in world\.decorations|for placed in world\.decorations", GAME_CORE, BRIDGE, TESTS, TOOLS)
    return {
        "rebuild_chunk_solid_calls": scan_rebuild_chunk_solid(),
        "ensure_collision_fresh_calls": scan_ensure_collision_fresh(),
        "decorations_loop_sites": [asdict(s) for s in deco_sites],
        "decorations_by_category": classify_decorations_scans(deco_sites),
        "streaming_snippets": read_streaming_defer_flush_snippet(),
        "single_chunk_benchmark": load_single_chunk_benchmark(),
        "world_gen_parallel_config_note": "parallel.workers=auto -> resolve_worker_count -> cpu_count-1",
    }


def main() -> int:
    report = run_analysis()
    out_path = PROJECT_ROOT / "helpers" / "m24a_scan_report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report: {out_path}")
    print(f"rebuild_chunk_solid call sites: {len(report['rebuild_chunk_solid_calls'])}")
    print(f"world.decorations loop sites: {len(report['decorations_loop_sites'])}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(PROJECT_ROOT))
    raise SystemExit(main())
