#!/usr/bin/env python3
"""Validate the published GAVEL benchmark manifest."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifest" / "gavel_solidity_benchmark_manifest.jsonl"
COUNTS = ROOT / "data" / "manifest" / "gavel_solidity_benchmark_counts.json"
EXCLUDE = ROOT / "data" / "splits" / "kb_exclude_slugs.txt"

EXPECTED_TOTAL = 582
EXPECTED_VULN = 306
EXPECTED_SAFE = 276
EXPECTED_PROJECTS = 81

REQUIRED_FIELDS = {
    "dataset_id",
    "dataset_version",
    "row_id",
    "row_type",
    "source_set",
    "project_slug",
    "source_origin",
    "source_path",
    "contract",
    "function",
    "original_line_start",
    "original_line_end",
    "human_verified",
    "verification_status",
    "leakage_policy",
    "provenance_notes",
}

FORBIDDEN_STRINGS = {
    "Cred.getPriceData",
    "TokenRoles.transferOwnership",
    "Crowdfund.getCrowdfundLifecycle",
    "MuteBond.currentEpoch",
    "FacadeRead.pendingIssuances",
    "2026-05-lbe-synthetic-small",
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at line {line_no}: {exc}") from exc
    return rows


def main() -> int:
    rows = load_jsonl(MANIFEST)
    counts = Counter(row.get("row_type") for row in rows)
    projects = {row.get("project_slug") for row in rows}
    errors: list[str] = []

    if len(rows) != EXPECTED_TOTAL:
        errors.append(f"expected {EXPECTED_TOTAL} rows, found {len(rows)}")
    if counts.get("vuln") != EXPECTED_VULN:
        errors.append(f"expected {EXPECTED_VULN} vuln rows, found {counts.get('vuln')}")
    if counts.get("safe") != EXPECTED_SAFE:
        errors.append(f"expected {EXPECTED_SAFE} safe rows, found {counts.get('safe')}")
    if len(projects) != EXPECTED_PROJECTS:
        errors.append(f"expected {EXPECTED_PROJECTS} projects, found {len(projects)}")

    for idx, row in enumerate(rows, 1):
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            errors.append(f"row {idx} missing fields: {', '.join(missing)}")
        if row.get("row_type") not in {"vuln", "safe"}:
            errors.append(f"row {idx} has invalid row_type={row.get('row_type')!r}")
        if row.get("source_set") not in {"v0", "v2"}:
            errors.append(f"row {idx} has invalid source_set={row.get('source_set')!r}")
        for key in ("original_line_start", "original_line_end"):
            try:
                if int(row[key]) <= 0:
                    errors.append(f"row {idx} has non-positive {key}")
            except Exception:
                errors.append(f"row {idx} has invalid {key}={row.get(key)!r}")

    manifest_text = MANIFEST.read_text()
    for forbidden in sorted(FORBIDDEN_STRINGS):
        if forbidden in manifest_text:
            errors.append(f"forbidden string still present: {forbidden}")

    exclude_slugs = {
        line.strip()
        for line in EXCLUDE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
    if exclude_slugs != projects:
        missing = sorted(projects - exclude_slugs)
        extra = sorted(exclude_slugs - projects)
        errors.append(f"exclude slug mismatch; missing={missing[:10]} extra={extra[:10]}")

    counts_data = json.loads(COUNTS.read_text())
    expected_from_counts = {
        "total_rows": EXPECTED_TOTAL,
        "vuln_rows": EXPECTED_VULN,
        "safe_rows": EXPECTED_SAFE,
        "unified_unique_projects": EXPECTED_PROJECTS,
    }
    for key, expected in expected_from_counts.items():
        if counts_data.get(key) != expected:
            errors.append(f"counts file {key} expected {expected}, found {counts_data.get(key)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Manifest validation passed")
    print(f"rows={len(rows)} vuln={counts['vuln']} safe={counts['safe']} projects={len(projects)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
