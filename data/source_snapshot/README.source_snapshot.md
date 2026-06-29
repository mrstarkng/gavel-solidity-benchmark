# Full Benchmark Solidity Source Snapshot

This branch publishes the Solidity source files for the 81 projects referenced by the GAVEL Solidity Benchmark manifest. The benchmark labels remain in `data/manifest/`; this snapshot adds source code so reviewers can reproduce source-level validation and experiments without separately fetching upstream repositories.

## Scope

- Snapshot type: full Solidity tree for manifest projects
- Source path: `data/source_snapshot/full_solidity_sources/`
- Benchmark projects represented: 81
- Solidity files: 10703
- Manifest-referenced source files: 312
- Total Solidity bytes: 71179451

Only `.sol` files under benchmark manifest project directories are included. Non-benchmark local workspace projects, build outputs, reports, caches, and local experiment outputs are excluded.

## License Notice

The benchmark metadata in this repository is covered by this repository's license. The Solidity files in this snapshot are third-party source files from their upstream projects and retain their original upstream licenses. See `THIRD_PARTY_LICENSES.md` and `SOURCE_PROVENANCE.json` for provenance details.

## Validation

From the repository root, run:

```bash
python3 scripts/validate_manifest.py
python3 scripts/validate_sources.py --sources-root data/source_snapshot/full_solidity_sources
shasum -a 256 -c data/source_snapshot/source_snapshot_sha256sums.txt
```

The manifest rows are the scoring units. Project directories provide source/provenance context for those function-level labels.
