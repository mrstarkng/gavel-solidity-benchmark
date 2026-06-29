# LBE-Curated Unified Leakage Plan

This freeze candidate writes the exact slug list to `lbe_curated_unified_kb_exclude_slugs.txt` for later application to `/Users/tonynguyen/Projects/poc_demo/data/lists/kb_exclude_eval_slugs.txt`.

No KB exclusion file was edited in Phase 2Z.

## Policy
- Every unified project slug has `leakage_policy=exclude_project_from_kb_retrieval` in the manifest.
- Project slugs are leakage-control and provenance groups. They preserve audited project/source context, while labels remain function-level manifest rows.
- The synthetic diagnostic fixture `2026-05-lbe-synthetic-small` is excluded.
- Source-only, rejected, and candidate-blocker projects are not included.
- Before evaluation, copy or merge the slug list into the KB exclusion list, rebuild processed KB, and run the local leakage check.

## Slug count
- Unified evaluation slugs: 81
