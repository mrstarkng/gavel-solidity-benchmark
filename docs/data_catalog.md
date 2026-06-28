# Data Catalog

This catalog describes the repository artifacts and whether each file is ground truth, metadata, split policy, provenance, validation tooling, or documentation.

## Ground Truth

- `data/manifest/gavel_solidity_benchmark_manifest.jsonl`: Primary benchmark labels. One JSON object per row.
- `data/manifest/gavel_solidity_benchmark_manifest.csv`: CSV mirror of the primary manifest for inspection.

## Metadata

- `data/manifest/gavel_solidity_benchmark_counts.json`: Expected row and project counts.
- `data/manifest/gavel_solidity_benchmark_project_index.csv`: Project-level row counts and source coverage.
- `data/manifest/gavel_solidity_benchmark_source_batch_index.csv`: Accepted curation batch provenance.
- `data/manifest/gavel_solidity_benchmark_spotcheck_queue.csv`: Recommended rows for independent audit.

## Splits and Leakage Policy

- `data/splits/kb_exclude_slugs.txt`: All benchmark project slugs that must be excluded from retrieval knowledge bases before evaluation.

## Source Provenance

- `data/sources/sources.lock.json`: Source reproducibility lockfile. Lists upstream repository URLs, available commit pins, benchmark-referenced Solidity paths, and report evidence files.

## Checksums

- `checksums/repo_sha256sums.txt`: Checksums for the current repository artifact set, excluding the checksum file itself.
- `checksums/phase2z_source_artifact_sha256sums.txt`: Checksums from the internal Phase 2Z freeze-candidate artifact source.

## Validation Scripts

- `scripts/validate_manifest.py`: Validates manifest parseability, counts, required fields, forbidden known-defect strings, and leakage slug coverage.
- `scripts/fetch_sources.py`: Clones source repositories from `data/sources/sources.lock.json`.
- `scripts/validate_sources.py`: Validates fetched or local Solidity sources against manifest file, contract, function, and line-range references.

## Documentation

- `README.md`: Repository overview and quick-start commands.
- `docs/dataset_card.md`: Dataset summary and intended use.
- `docs/creation_methodology.md`: Human curation workflow.
- `docs/leakage_policy.md`: Retrieval exclusion policy.
- `docs/line_range_policy.md`: Line-range handling and validation policy.
- `docs/quality_audit.md`: Freeze-candidate quality checks.
- `docs/schema.md`: Manifest schema.
- `docs/reproduction.md`: Full source reproduction workflow.
- `docs/data_catalog.md`: This file.
