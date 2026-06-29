# LBE-Curated Unified Line Range Policy

Line ranges support function-level labels in a project-grounded benchmark. Each accepted row points to the source span for one selected contract/function, not to an entire project audit.

## V2 rows
All accepted v2 gold rows carry exact `original_line_start` and `original_line_end` values from manual curation. These values are preserved.

## V0 legacy rows
The v0 JSON source does not store line ranges. Phase 2Z backfills a line range only when the exact function name exists in the referenced source file and the function body can be bounded by braces. No fake line ranges are invented.

Rows that cannot be backfilled keep null line-range fields and include `legacy_v0_line_range_missing` in `provenance_notes` with `verification_status=accepted_legacy_v0`.

## Required repair
`2024-08-phi:safe:1` is repaired to `Cred.getCredCreator` with the required exact range `391-393`. The invalid `invalid original Phi safe function` reference is not present in the manifest.

## Backfill result
- v0 rows with missing line ranges after exact backfill: 0
