#!/usr/bin/env python3
"""Audit a pokeemerald source tree against the pinned BUGFIX/UBFIX manifest.

This is deliberately read-only.  It verifies that every pinned marker path is
present, checks that its expected marker still exists, and discovers marker
sites that are present in the source tree but absent from the manifest.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

MARKERS = ("BUGFIX", "UBFIX")
TEXT_SUFFIXES = {
    ".c", ".h", ".s", ".inc", ".md", ".mk", ".json", ".txt", ".yml", ".yaml"
}


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"marker", "path", "upstream_commit"}
    if not rows:
        raise SystemExit(f"manifest has no rows: {path}")
    missing = required.difference(rows[0])
    if missing:
        raise SystemExit(f"manifest missing columns: {', '.join(sorted(missing))}")
    return rows


def iter_text_files(root: Path) -> Iterable[Path]:
    ignored = {".git", "build", "tools"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in ignored for part in path.parts):
            continue
        yield path


def scan_markers(root: Path) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root).as_posix()
        for marker in MARKERS:
            if marker in text:
                found.add((marker, rel))
    return found


def audit(manifest_path: Path, source_root: Path) -> dict[str, object]:
    rows = load_manifest(manifest_path)
    expected = {(row["marker"], row["path"]) for row in rows}

    missing_paths: list[dict[str, str]] = []
    missing_markers: list[dict[str, str]] = []

    for row in rows:
        candidate = source_root / row["path"]
        if not candidate.is_file():
            missing_paths.append(row)
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            missing_markers.append({**row, "reason": "non-UTF-8 source"})
            continue
        if row["marker"] not in text:
            missing_markers.append({**row, "reason": "marker not found"})

    discovered = scan_markers(source_root)
    untracked = sorted(discovered.difference(expected))

    commits = sorted({row["upstream_commit"] for row in rows})
    counts = {
        marker: sum(1 for row in rows if row["marker"] == marker)
        for marker in MARKERS
    }

    return {
        "manifest": str(manifest_path),
        "source_root": str(source_root),
        "manifest_rows": len(rows),
        "manifest_marker_counts": counts,
        "upstream_commits": commits,
        "missing_paths": missing_paths,
        "missing_markers": missing_markers,
        "untracked_marker_sites": [
            {"marker": marker, "path": path} for marker, path in untracked
        ],
        "ok": not missing_paths and not missing_markers and not untracked,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_root",
        type=Path,
        help="Path to the exact pokeemerald source snapshot being audited",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/bugs/pret-marked-bug-surface.csv"),
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if not args.source_root.is_dir():
        parser.error(f"source_root is not a directory: {args.source_root}")
    if not args.manifest.is_file():
        parser.error(f"manifest does not exist: {args.manifest}")

    result = audit(args.manifest, args.source_root)

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"manifest rows: {result['manifest_rows']}")
        print(f"marker counts: {result['manifest_marker_counts']}")
        print(f"missing paths: {len(result['missing_paths'])}")
        print(f"missing markers: {len(result['missing_markers'])}")
        print(f"untracked marker sites: {len(result['untracked_marker_sites'])}")
        if result["missing_paths"]:
            print("\nMissing paths:")
            for row in result["missing_paths"]:
                print(f"  {row['marker']:6} {row['path']}")
        if result["missing_markers"]:
            print("\nMissing expected markers:")
            for row in result["missing_markers"]:
                print(f"  {row['marker']:6} {row['path']} ({row['reason']})")
        if result["untracked_marker_sites"]:
            print("\nUntracked marker sites:")
            for row in result["untracked_marker_sites"]:
                print(f"  {row['marker']:6} {row['path']}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
