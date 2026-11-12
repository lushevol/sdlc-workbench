---
name: prepare-knowledge-sources
description: Orchestrate retention, semantic filtering, and hash-bound source views from complete knowledge document exports.
---

# Prepare knowledge sources

Coordinate complete raw export → filtered source view before canonical ingestion.
Use the existing [source command contract](../ingest-knowledge/references/source-preparation.md).
This stage preserves evidence and selects inputs. Canonical meaning and publication have separate owners.

## Inputs

Use the selected workspace, registered collection ID, complete export, applicable filter policy, and governing context.
Keep replaceable exports in ignored `evidence/knowledge/incoming/COLLECTION/`.
Retain originals under `evidence/knowledge/sources/`; do not introduce another top-level raw directory.
Review-only requests inspect these inputs without importing or changing selections.

## Coordinate the operations

1. Use [capture-knowledge-sources](../capture-knowledge-sources/SKILL.md) to protect prior bytes and retain new revisions.
2. Use [select-knowledge-sources](../select-knowledge-sources/SKILL.md) to review meaning, verify bindings, and generate needed views.
3. Run `sources plan` and return its compact queues before loading source contents into semantic work.
   After selection changes, save a fresh plan. Use `sources view --plan` for queued kept pages.
4. Return source identities, hashes, selected ranges, policy/context bindings, view mappings, and explicit omissions to the caller.

Reuse completed operations when their input hashes still match.
Selection completion does not establish canonical processing completion. Preserve pending processing across repeated refreshes.
New or changed pages require review, including previous exclusions.
Changed policy or governing context requires reassessment.
Missing pages preserve history and trigger no downstream deletion.

## Completion and handoff

Report the collection's actual `READY` or pending result from `sources verify`.
A partial view can supply reviewed selections when the caller accepts its declared omitted scope.
Do not describe partial coverage as a ready complete collection.
Stop use of affected selections when source, policy, context, or output bindings are stale.
Use [ingest-knowledge](../ingest-knowledge/SKILL.md) for canonical candidates after source preparation.
Wiki inputs remain canonical knowledge records rather than raw exports or generated views.
