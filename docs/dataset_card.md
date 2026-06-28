# Dataset Card

## Name

GAVEL Solidity Benchmark

## Purpose

The dataset supports evaluation of Solidity vulnerability detection systems that must identify vulnerable or safe functions and ground their predictions in source-level evidence.

## Data Sources

The benchmark is derived from public Code4rena audit contests and corresponding Solidity source repositories. Full source repositories are not vendored in this dataset release.

## Labels

The dataset contains two row types:

- `vuln`: a function associated with a judged vulnerability finding.
- `safe`: a production Solidity function selected as a negative control.

## Current Size

| Metric | Count |
|---|---:|
| Total rows | 582 |
| Vulnerable rows | 306 |
| Safe rows | 276 |
| Unique projects | 81 |

## Ground Truth File

```text
data/manifest/gavel_solidity_benchmark_manifest.jsonl
```

## Recommended Use

Use this dataset to evaluate source-grounded vulnerability detection and evidence retrieval. During evaluation, exclude benchmark projects from the retrieval knowledge base using:

```text
data/splits/kb_exclude_slugs.txt
```

## Non-Goals

This dataset does not claim to cover every vulnerability type, every Solidity project, or every bug in each included project. It is a curated benchmark, not a full audit replacement.

## Known Caveats

Safe rows are function-level negative controls. They should not be interpreted as proof that the surrounding contract or project is safe.
