# Creation Methodology

GAVEL Solidity Benchmark was created with a human-in-the-loop curation and annotation workflow. The goal was to build a source-grounded benchmark where each accepted label can be traced to public audit evidence and concrete Solidity code.

## Source Collection

Candidate projects were selected from public Code4rena contests. For each candidate project, the curation workflow checked that both of the following were available:

- public judged findings or final report evidence;
- corresponding Solidity source files.

Projects were excluded or deferred when they were source-only, report-only, non-Solidity-heavy, synthetic, diagnostic, or insufficiently supported by public evidence.

## Vulnerable Row Annotation

For each vulnerable candidate, annotators reviewed the judged finding and source code together. A vulnerable row was accepted only when the issue could be mapped to:

- a project slug;
- a Solidity source file;
- a contract or library;
- a concrete function;
- an exact source line range;
- a report evidence file;
- a vulnerability category;
- an expected root cause.

Rows with unknown functions, fake line ranges, placeholder categories, placeholder SWC labels, weak report mapping, or ambiguous source evidence were rejected or deferred.

## Safe Row Annotation

Safe rows were selected as negative controls from production Solidity code in audited projects. A safe row was accepted only when the selected function:

- exists in the source snapshot;
- has an exact contract, function, and line range;
- is production code, not test/mock/script/deployment/harness code;
- is not vendored dependency code;
- is not an interface-only declaration;
- is preferably `view`, `pure`, or read-only;
- is not directly named in judged finding text;
- has a specific function-level selection reason.

Safe rows are not claims that a whole contract or project is vulnerability-free. They are benchmark negative controls at the selected function scope.

## Validation

Accepted rows were checked for:

- JSONL and CSV parseability;
- source file existence;
- report evidence existence for vulnerable rows;
- contract and function existence;
- line-range consistency;
- row count consistency;
- removal of known invalid or downgraded rows;
- exclusion of synthetic fixtures;
- leakage exclusion list coverage.

## Leakage Control

All benchmark project slugs are listed in `data/splits/kb_exclude_slugs.txt`. Evaluation systems should exclude these projects from retrieval knowledge bases to avoid using benchmark evidence as model context.

## Limitations

The benchmark is curated for source-grounded Solidity vulnerability detection. It should not be interpreted as a complete census of all bugs in the included projects. Safe rows are scoped negative controls, not whole-project safety proofs.
