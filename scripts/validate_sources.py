#!/usr/bin/env python3
"""Validate benchmark manifest rows against a local Solidity source root."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "manifest" / "gavel_solidity_benchmark_manifest.jsonl"


def parse_projects(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {item.strip() for item in value.split(",") if item.strip()}


def load_manifest(path: Path) -> list[dict]:
    rows = []
    with path.open() as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at line {line_no}: {exc}") from exc
    return rows


def has_contract(text: str, name: str) -> bool:
    pattern = re.compile(
        r"\b(?:abstract\s+contract|contract|library|interface)\s+"
        + re.escape(name)
        + r"\b"
    )
    return bool(pattern.search(text))


def function_pattern(name: str) -> re.Pattern[str]:
    if name == "constructor":
        return re.compile(r"\bconstructor\s*\(")
    if name == "fallback":
        return re.compile(r"\bfallback\s*\(")
    if name == "receive":
        return re.compile(r"\breceive\s*\(")
    return re.compile(r"\bfunction\s+" + re.escape(name) + r"\b")


def validate_row(row: dict, sources_root: Path) -> list[str]:
    errors: list[str] = []
    row_id = row.get("row_id", "<unknown>")
    project = row.get("project_slug", "")
    source_path = row.get("source_path", "")
    contract = row.get("contract", "")
    function = row.get("function", "")
    full_path = sources_root / project / source_path

    if not full_path.exists():
        return [f"{row_id}: missing source file {full_path}"]

    text = full_path.read_text(errors="ignore")
    lines = text.splitlines()

    if contract and not has_contract(text, contract):
        errors.append(f"{row_id}: missing contract/library/interface {contract} in {full_path}")

    fn_re = function_pattern(function)
    if function and not fn_re.search(text):
        errors.append(f"{row_id}: missing function {function} in {full_path}")

    try:
        start = int(row.get("original_line_start"))
        end = int(row.get("original_line_end"))
    except Exception:
        errors.append(f"{row_id}: non-integer line range")
        return errors

    if start <= 0 or end <= 0 or end < start or end > len(lines):
        errors.append(
            f"{row_id}: bad line range {start}-{end} for file with {len(lines)} lines"
        )
        return errors

    snippet = "\n".join(lines[start - 1 : end])
    if function and not fn_re.search(snippet):
        errors.append(
            f"{row_id}: function signature {function} not found inside line range {start}-{end}"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sources-root", type=Path, default=Path("solidity_sources"))
    parser.add_argument("--projects", help="Optional comma-separated project slug list")
    args = parser.parse_args()

    manifest = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    sources_root = args.sources_root if args.sources_root.is_absolute() else Path.cwd() / args.sources_root
    selected = parse_projects(args.projects)

    rows = load_manifest(manifest)
    if selected is not None:
        rows = [row for row in rows if row.get("project_slug") in selected]

    counters = {
        "missing_files": 0,
        "missing_contracts": 0,
        "missing_functions": 0,
        "bad_line_ranges": 0,
        "other_errors": 0,
    }
    errors: list[str] = []

    for row in rows:
        row_errors = validate_row(row, sources_root)
        for error in row_errors:
            errors.append(error)
            if "missing source file" in error:
                counters["missing_files"] += 1
            elif "missing contract/library/interface" in error:
                counters["missing_contracts"] += 1
            elif "missing function" in error or "function signature" in error:
                counters["missing_functions"] += 1
            elif "line range" in error:
                counters["bad_line_ranges"] += 1
            else:
                counters["other_errors"] += 1

    projects = {row.get("project_slug") for row in rows}
    print("Source validation summary")
    print(f"rows_checked={len(rows)}")
    print(f"projects_checked={len(projects)}")
    for key, value in counters.items():
        print(f"{key}={value}")

    if errors:
        for error in errors[:100]:
            print(f"ERROR: {error}")
        if len(errors) > 100:
            print(f"ERROR: ... {len(errors) - 100} additional errors omitted")
        return 1

    print("Source validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
