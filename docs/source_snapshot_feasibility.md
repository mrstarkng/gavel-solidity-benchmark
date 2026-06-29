# Source Snapshot Feasibility

This document evaluates whether GAVEL Solidity Benchmark should publish Solidity source files in addition to the manifest, source lockfile, and fetch/validate scripts.

The goal is to improve reproducibility while avoiding accidental relicensing of third-party Code4rena/project source code under this repository's MIT license.

## Current State

The public repository currently publishes:

- function-level benchmark manifest and metadata;
- leakage split files;
- source lockfile;
- source fetch and validation scripts;
- documentation and checksums;
- no committed `.sol` source files.

The local full source workspace is:

```text
local_workspace/sources/solidity_sources
```

It is intentionally gitignored and should not be committed.

## Measured Scope

| Scope item | Count / size |
|---|---:|
| Benchmark projects | 81 |
| Manifest rows | 582 |
| Unique manifest-referenced source files | 312 |
| Projects represented in referenced source files | 81 |
| Total `.sol` files in full local source tree | 30,816 |
| Approximate full local source tree size | 5.0 GiB |
| Total bytes across all `.sol` files in full local source tree | 199,906,507 bytes |
| Approximate size of manifest-referenced source files only | 4,671,144 bytes |

The minimal manifest-referenced snapshot is much smaller than the full local source tree and directly matches the benchmark scoring rows.

## Source Lock Coverage

The current source lockfile covers all 81 projects.

| Lock/provenance item | Count |
|---|---:|
| Projects with commit SHA/ref coverage | 39 |
| Projects without recovered commit ref | 42 |
| Projects with `license_status=known` | 39 |
| Projects with `license_status=unknown` | 42 |

For the 312 manifest-referenced candidate files:

| Candidate-file license status | Count |
|---|---:|
| `known` | 149 |
| `unknown` | 163 |

The `license_status` field is a provenance review signal from `data/sources/sources.lock.json`, not legal advice.

## Option 1: No Source Snapshot

Keep the current model: publish the manifest, source lockfile, fetch script, and source validator only.

Pros:

- Lowest legal and provenance risk.
- Keeps `main` lightweight.
- Avoids redistributing third-party Solidity code.
- Maintains a clear boundary: repository MIT license applies only to benchmark metadata, docs, and scripts.

Cons:

- External users depend on upstream repository availability.
- Projects without recovered commit refs may not reproduce byte-for-byte.
- Supervisors/reviewers must run fetch scripts before validating full source alignment.

License/provenance risk:

- Low. No upstream Solidity files are redistributed.
- `NOTICE.md` and `docs/reproduction.md` remain sufficient with current wording.

## Option 2: Minimal Source Snapshot

Publish only the 312 Solidity files referenced by manifest rows, preserving:

```text
<project_slug>/<original/source/path.sol>
```

Pros:

- Small enough for review and release packaging.
- Directly supports benchmark row validation.
- Avoids shipping unrelated upstream repository content.
- Easier to checksum and audit than the full tree.
- Closely matches the function-level ground truth.

Cons:

- May not be enough to compile full projects.
- Imports may point to files outside the snapshot.
- Still redistributes third-party source files and needs license/provenance safeguards.
- Some project commit refs and license statuses remain unknown.

License/provenance risk:

- Medium. The snapshot is small and scoped, but it still contains third-party Solidity code.
- Must preserve upstream headers exactly.
- Must include a third-party license/provenance notice.
- Should include file-level provenance and checksums.

## Option 3: Full Local Source Snapshot

Publish all `.sol` files under `local_workspace/sources/solidity_sources`.

Pros:

- Maximizes offline reproducibility.
- More likely to preserve import context.
- Similar in spirit to source-publishing benchmark repositories.

Cons:

- Very large compared with the benchmark rows.
- Includes files not used by the benchmark.
- More difficult to review for license and provenance.
- Higher chance of accidentally publishing vendored dependencies, generated files, local metadata, or unrelated contest material.
- Could be mistaken as a maintained source distribution.

License/provenance risk:

- High. This option redistributes a large multi-project source corpus with mixed or unknown licensing.
- Requires stronger license review and probably should not be committed to `main`.

## Option 4: GitHub Release Artifact

Package source files as a separate `.tar.gz` release artifact instead of committing them to `main`.

Pros:

- Keeps `main` lightweight and reviewable.
- Separates benchmark metadata/scripts from third-party source redistribution.
- Can include a strong release-specific notice.
- Allows optional download by users who need offline reproduction.
- Allows replacement/update without rewriting repository history.

Cons:

- Requires release-asset maintenance.
- Users need one extra download step.
- Still requires license/provenance review.

License/provenance risk:

- Medium for a minimal snapshot, high for a full snapshot.
- Safer than committing sources into `main` because the artifact can be explicitly labeled as third-party source material.

## Feasibility Verdict

A minimal manifest-referenced source snapshot is feasible from a size and validation perspective:

- all 312 referenced files exist locally;
- every manifest row validates against the local source workspace;
- the candidate snapshot is about 4.5 MiB before compression;
- file-level SHA256 hashes can be produced.

The main blocker is not technical. It is license/provenance review. Any snapshot must clearly state that Solidity files remain under upstream licenses and are not covered by this repository's MIT license.

## Recommended Direction

Do not commit Solidity source files to `main` now.

For review, prepare a minimal source snapshot as an optional GitHub Release artifact, not as tracked repository content. Include:

- `README.source_snapshot.md`
- `SOURCE_PROVENANCE.json`
- `THIRD_PARTY_LICENSES.md`
- `source_snapshot_sha256sums.txt`
- `sources/<project_slug>/<source_path>.sol`

Only after legal/provenance review should a release artifact be attached.
