# Reproducing the Full Benchmark Sources

This repository publishes the benchmark labels, metadata, splits, and validation tools. It does not vendor Solidity source repositories or upstream Code4rena contest repositories.

The source lockfile is:

```text
data/sources/sources.lock.json
```

It lists every benchmark project, the upstream repository URL when recoverable, the pinned local git commit when available, the source files referenced by benchmark rows, and the judged report files used as evidence.

## External Workflow

From a fresh clone of this repository:

```bash
python3 scripts/validate_manifest.py
python3 scripts/fetch_sources.py --output solidity_sources
python3 scripts/validate_sources.py --sources-root solidity_sources
```

Use these paths for downstream experiments:

```text
Manifest: data/manifest/gavel_solidity_benchmark_manifest.jsonl
Sources root: solidity_sources
Leakage exclusions: data/splits/kb_exclude_slugs.txt
```

## Why Sources Are Not Vendored

The benchmark references public Code4rena reports and public Solidity repositories, but it does not redistribute full upstream source trees. This keeps the benchmark repository compact and avoids republishing third-party source code under potentially different licensing terms.

Before redistributing fetched source code, review the upstream repository license and terms. The lockfile field `license_status` is a convenience signal from the local source snapshot, not legal advice.

## If a Repository Moved

Most `repo_url` values use the Code4rena convention:

```text
https://github.com/code-423n4/<project_slug>
```

Some URLs were recovered from local source metadata or git remotes. If a repository has moved, update a local copy of `data/sources/sources.lock.json` with the new URL and rerun:

```bash
python3 scripts/fetch_sources.py --lock data/sources/sources.lock.json --output solidity_sources --projects <project_slug>
python3 scripts/validate_sources.py --sources-root solidity_sources --projects <project_slug>
```

## If a Commit Is Unavailable

For projects where the local source snapshot was not a git repository, the lockfile sets `commit_sha` and `commit_ref` to `null` and notes `commit unavailable from local snapshot`.

In that case, fetching reproduces the upstream repository default branch unless you manually add a reviewed commit ref. The benchmark labels remain reproducible from the manifest, but byte-for-byte source reproduction may require recovering the original contest commit from Code4rena or the upstream project.

## Labels vs Full Experiment Inputs

Label reproduction means verifying the manifest structure and counts:

```bash
python3 scripts/validate_manifest.py
```

Full experiment-input reproduction additionally fetches Solidity source repositories and validates that every benchmark row still maps to the expected file, contract, function, and line range:

```bash
python3 scripts/fetch_sources.py --output solidity_sources
python3 scripts/validate_sources.py --sources-root solidity_sources
```

Before running any retrieval-augmented evaluation, apply all slugs from `data/splits/kb_exclude_slugs.txt` to the retrieval knowledge base. This prevents benchmark label leakage from Code4rena reports or source-derived documents.
