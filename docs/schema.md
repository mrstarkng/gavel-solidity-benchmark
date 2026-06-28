# LBE-Curated Unified Schema Report

Dataset id: `lbe-curated-unified`
Dataset version: `freeze-candidate-20260628-phase2z`
Manifest files: `lbe_curated_unified_manifest.jsonl`, `lbe_curated_unified_manifest.csv`

## Required fields
The manifest includes every requested field: dataset_id, dataset_version, row_id, row_type, source_set, source_phase_or_file, project_slug, source_origin, source_url_or_report_url, report_evidence, source_path, contract, function, original_line_start, original_line_end, category, swc_id, severity, expected_root_cause, evidence_summary, safe_selection_reason, human_verified, verification_status, leakage_policy, provenance_notes.

## Source mapping
- v0 rows are loaded from real JSON files in `/Users/tonynguyen/Projects/poc_demo/data/lbe_curated/`, excluding `2026-05-lbe-synthetic-small.json`.
- v2 rows are loaded from the accepted Phase 2Y assembled preview, which already applies Phase 2M-R and Phase 2W-R repaired safe rows.
- `2024-08-phi:safe:1` is repaired in the generated manifest only; the original v0 JSON file was not edited.

## Row ids
- v0 row ids are preserved from source JSON.
- v2 row ids are deterministic freeze-candidate ids using phase, row type, ordinal, project, contract, and function.

## Legacy line ranges
V2 rows are line-exact. V0 line ranges are backfilled only where the exact function body can be bounded in local source. Missing legacy line ranges, if any, are represented as JSON null and marked in provenance.
