#!/usr/bin/env python3
"""Fetch upstream Solidity source repositories for the benchmark.

The benchmark repository does not vendor Solidity source code. This script uses
data/sources/sources.lock.json to clone the upstream Code4rena repositories into
a local sources directory for reproducibility checks.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "data" / "sources" / "sources.lock.json"


def parse_projects(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {item.strip() for item in value.split(",") if item.strip()}


def run_git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


def load_lock(path: Path) -> list[dict]:
    with path.open() as handle:
        data = json.load(handle)
    projects = data.get("projects")
    if not isinstance(projects, list):
        raise SystemExit(f"Lockfile {path} does not contain a projects list")
    return projects


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--output", type=Path, default=Path("solidity_sources"))
    parser.add_argument("--projects", help="Optional comma-separated project slug list")
    parser.add_argument("--skip-existing", action="store_true")
    args = parser.parse_args()

    lock_path = args.lock if args.lock.is_absolute() else ROOT / args.lock
    output_root = args.output if args.output.is_absolute() else Path.cwd() / args.output
    selected = parse_projects(args.projects)

    projects = load_lock(lock_path)
    if selected is not None:
        projects = [project for project in projects if project.get("project_slug") in selected]

    output_root.mkdir(parents=True, exist_ok=True)

    attempted = 0
    cloned = 0
    skipped = 0
    failed: list[str] = []

    for project in projects:
        slug = project["project_slug"]
        repo_url = project.get("repo_url")
        ref = project.get("commit_sha") or project.get("commit_ref")
        dest = output_root / slug

        if not repo_url:
            failed.append(f"{slug}: missing repo_url")
            continue

        if dest.exists():
            if args.skip_existing:
                print(f"SKIP {slug}: {dest} already exists")
                skipped += 1
                continue
            failed.append(f"{slug}: destination already exists: {dest}")
            continue

        attempted += 1
        print(f"CLONE {slug}: {repo_url}")
        clone = run_git(["clone", repo_url, str(dest)])
        if clone.returncode != 0:
            failed.append(f"{slug}: git clone failed: {clone.stderr.strip()}")
            continue

        if ref:
            print(f"CHECKOUT {slug}: {ref}")
            checkout = run_git(["checkout", ref], cwd=dest)
            if checkout.returncode != 0:
                failed.append(f"{slug}: git checkout {ref} failed: {checkout.stderr.strip()}")
                continue

        cloned += 1

    print()
    print("Source fetch summary")
    print(f"attempted={attempted}")
    print(f"cloned={cloned}")
    print(f"skipped={skipped}")
    print(f"failed={len(failed)}")
    for item in failed:
        print(f"ERROR: {item}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
