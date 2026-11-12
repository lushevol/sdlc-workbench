---
name: bind-wiki-sources
description: Prepare validated canonical source identities, aliases, hashes, and recovery material before a Workbench wiki update.
---

# Bind canonical wiki sources

Input: the selected workspace, authorized canonical record scope, and current wiki source bindings.
Use this unit before semantic maintenance or after an authorized canonical relocation.

## Prepare the binding

1. Select canonical records outside `knowledge/llm-wiki/` and run [canonical integrity checks](../check-knowledge-integrity/SKILL.md).
   Reject conflicting IDs, duplicate filenames, paths outside the workspace, and derived wiki inputs.
   Raw exports and filtered excerpts enter through [source preparation](../prepare-knowledge-sources/SKILL.md), not wiki aliases.
   Run local wiki `plan --source DIR --record PATH` before semantic dispatch. Repeat `--record` for each exact input.
   Save full inventory with `--output` and read compact queued scope.
   Matching reviewed completion and output hashes permit skipping. A source hash alone cannot establish completion.
2. Record each source's path, full-file SHA-256, ID, version, status, and governance state before semantic work.
   Read existing manifest entries to identify new, changed, relocated, or unchanged inputs.
   Do not promote candidate knowledge or select a business answer from a newer timestamp alone.
   Legacy bindings without receipts require scoped review of existing pages, not automatic global recompilation.
   Preserve `expected_outputs`, including former dependents and affected explorations, for maintenance and review.
3. Check `raw/<name>.md` and `wiki/sources/<name>.md` inside the wiki.
   Both must be relative symlinks to the same selected canonical record.
   The native bridge creates/checks aliases during compilation. ADE authoring creates only these validated relative aliases when absent.
   A conflicting alias or symlink failure stops affected work. Do not duplicate a canonical source as a workaround.
4. Before ADE semantic edits, retain both provenance before-images in a new ignored `.workbench/wiki/<run-id>/` directory.
   Preserve `source-manifest.json` and `.openkb/hashes.json`, previous bindings, and affected page hashes together.
   Record both before-image hashes and the attempt identity in the receipt for interrupted recovery.
   Use the existing hashing tools; hash complete bytes without displaying source content unnecessarily.

Hash a selected source or output with the existing Python standard library:

```sh
python3 -c "import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())" PATH
```

Replace `PATH` with the inspected source or output path.

The [project procedures](../llm-wiki/references/workflows.md#compile-canonical-records) define native command boundaries.
Do not run source-owning native `add`, `remove`, `watch`, `recompile`, `ingest`, or `refresh` on these aliases.
Missing sources require investigation; they do not authorize source history or wiki deletion.

## Result and stop conditions

Return the selected IDs/paths, starting source hashes, alias checks, previous bindings, and recovery-material location.
Pass that scope to [maintain-wiki-content](../maintain-wiki-content/SKILL.md).
No provenance hash advances during preparation.
Stop when source identity, authority, applicability, or alias conflicts prevent a reliable binding.
Resolve canonical changes through ingestion/governance, then capture a fresh starting hash.
