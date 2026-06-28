# GAVEL Solidity Benchmark

GAVEL Solidity Benchmark is a human-curated benchmark for evaluating Solidity smart-contract vulnerability detection. The dataset is source-grounded: each accepted row links a label to a project, Solidity source file, contract, function, and source line range.

The benchmark was built from public Code4rena audit reports and corresponding Solidity repositories. It contains both real vulnerable functions and safe production-code controls for evaluating whether a detector can identify vulnerable behavior and support its answer with source-level evidence.

## Dataset Summary

| Metric | Count |
|---|---:|
| Total rows | 582 |
| Vulnerable rows | 306 |
| Safe rows | 276 |
| Unique projects | 81 |
| v0 rows | 102 |
| v2 gold expansion rows | 480 |

The current release is a freeze candidate assembled from the accepted v0 seed and the v2 gold expansion.

## Repository Layout

```text
data/
  manifest/
    gavel_solidity_benchmark_manifest.jsonl
    gavel_solidity_benchmark_manifest.csv
    gavel_solidity_benchmark_counts.json
    gavel_solidity_benchmark_project_index.csv
    gavel_solidity_benchmark_source_batch_index.csv
    gavel_solidity_benchmark_spotcheck_queue.csv
  splits/
    kb_exclude_slugs.txt
  sources/
    sources.lock.json
docs/
  dataset_card.md
  creation_methodology.md
  leakage_policy.md
  line_range_policy.md
  quality_audit.md
  reproduction.md
  schema.md
checksums/
  repo_sha256sums.txt
  phase2z_source_artifact_sha256sums.txt
scripts/
  validate_manifest.py
  fetch_sources.py
  validate_sources.py
LICENSE
README.md
```

## Ground Truth

The primary ground truth file is:

```text
data/manifest/gavel_solidity_benchmark_manifest.jsonl
```

Each JSONL row represents one benchmark label:

- `row_type = vuln`: a real vulnerability supported by judged Code4rena report evidence.
- `row_type = safe`: a production Solidity function selected as a negative control.

Important fields include:

- `project_slug`
- `source_path`
- `contract`
- `function`
- `original_line_start`
- `original_line_end`
- `category`
- `swc_id`
- `severity`
- `expected_root_cause`
- `evidence_summary`
- `safe_selection_reason`
- `human_verified`
- `verification_status`
- `leakage_policy`
- `provenance_notes`

## Creation Methodology

The dataset was created through a human-in-the-loop curation workflow. Candidate projects and findings were collected from public Code4rena audit reports and matching Solidity source repositories. Each candidate row was manually reviewed against the original judged report and the corresponding source file.

For vulnerable rows, annotators verified that the reported issue could be mapped to a concrete Solidity contract, function, and source line range. Rows were accepted only when the vulnerability evidence, affected function, root cause, and category label were supported by the original report and source code.

For safe rows, annotators selected production Solidity functions from the same audited project that were not directly implicated in judged findings. Safe rows were checked to avoid tests, mocks, scripts, vendored dependencies, interfaces, harness code, and functions mentioned directly in vulnerability reports.

Ambiguous, synthetic, source-only, or weakly supported rows were rejected or deferred.

See [docs/creation_methodology.md](docs/creation_methodology.md) for more detail.

## Leakage Policy

All benchmark project slugs must be excluded from retrieval knowledge bases during evaluation. The exclusion list is:

```text
data/splits/kb_exclude_slugs.txt
```

This prevents systems from retrieving the same audit reports used to define the benchmark labels.

## Source Code Policy

This repository stores the benchmark manifest and metadata. It does not vendor the full Solidity source repositories. Source provenance is represented through project slugs, source paths, report evidence, and public origin metadata.

Before redistributing source code from upstream projects, review the corresponding upstream licenses and repository terms.

## Reproduce Full Benchmark Sources

```bash
python3 scripts/validate_manifest.py
python3 scripts/fetch_sources.py --output solidity_sources
python3 scripts/validate_sources.py --sources-root solidity_sources
```

The source lockfile is `data/sources/sources.lock.json`. Full details, including license/provenance cautions and moved-repository handling, are in [docs/reproduction.md](docs/reproduction.md).

## Basic Validation

From the repository root:

```bash
python3 - <<'PY'
import json
from collections import Counter

rows = []
with open("data/manifest/gavel_solidity_benchmark_manifest.jsonl") as f:
    for line in f:
        rows.append(json.loads(line))

counts = Counter(row["row_type"] for row in rows)
projects = {row["project_slug"] for row in rows}

print("rows:", len(rows))
print("row types:", dict(counts))
print("projects:", len(projects))
PY
```

Expected output:

```text
rows: 582
row types: {'vuln': 306, 'safe': 276}
projects: 81
```

To verify published file checksums:

```bash
shasum -c checksums/repo_sha256sums.txt
```

## Citation

If you use this benchmark, cite the GAVEL paper/artifact once the public citation is available.

## License

This repository is released under the MIT License. The license applies to the benchmark manifests, metadata, documentation, validation scripts, and reproducibility tooling maintained here.

The underlying Code4rena reports and referenced Solidity source repositories remain subject to their original licenses and terms. See [NOTICE.md](NOTICE.md).
