---
name: select-knowledge-sources
description: Select intended behavior from retained documents and generate verifiable filtered views with original source hashes and ranges.
---

# Select knowledge sources

## Inputs

Use retained source revisions, current source-page hashes, project questions, applicable policy, and governing context hashes.
Read [the source preparation contract](../ingest-knowledge/references/source-preparation.md) for decision fields and installed commands.
Use its existing [filter policy](../ingest-knowledge/assets/source-filter.yaml) or the project's explicit replacement.

Review-only scope follows reading and proposed decisions. Skip source, selection, and view mutations.

## Select and check

1. Run `sources plan` to locate pending selections without loading unchanged completed source contents.
   Read each queued complete source and necessary linked context before deciding.
   Select intended behavior, domain definitions, contracts, responsibilities, and behavior-relevant constraints.
   Technical material qualifies when it explains intended domain responsibilities or contracts.
2. Apply `KEEP`, `KEEP_SECTIONS`, `EVIDENCE_ONLY`, `EXCLUDE`, or `HOLD` using [the decision definitions](../ingest-knowledge/references/source-preparation.md#apply-the-filter-pattern).
   Keep `NEEDS_REVIEW` as the runtime's pending state rather than a semantic decision.
3. Preserve conditions, exceptions, definitions, proposal status, conflicts, and unavailable attachments.
   Use filenames and keywords to locate passages, then decide from their contents.
   Source age alone does not justify exclusion. Code or passing tests cannot define target intent.
4. Record decisions through `sources select`; bind them to original page SHA-256, selected ranges, policy, and governing context.
   Reassess changed pages, including previous exclusions, and decisions affected by changed policy or context.
5. Run `sources verify` and report its actual collection result and pending scope.
6. Save a fresh `sources plan` after applying decisions.
   When needed, use `sources view --plan` with a new ignored output directory.
   Check original-to-output ranges, source identities, revisions, hashes, and emitted output hashes before use.

The contract contains [decision JSON and commands](../ingest-knowledge/references/source-preparation.md#apply-the-filter-pattern)
and [view generation](../ingest-knowledge/references/source-preparation.md#generate-the-filtered-view).
Do not manually maintain generated excerpts or silently repair a business policy while cleaning.
Canonical citations must resolve to retained originals rather than rely on replaceable views.
Report review and processing queues separately. Source selection alone cannot clear pending canonical processing.

## Checkable output and stop conditions

Return selection metadata, reasons, exact ranges, policy/context bindings, view mappings, and omitted or missing pages.
Report `READY` only when collection verification succeeds.
Partial views may contain current reviewed selections; preserve their pending, held, and missing omissions.
Stop use of stale selected bindings. A working link alone does not establish valid selection or supported meaning.
Retain excluded and evidence-only originals; missing input authorizes no source or knowledge deletion.
For review-only requests, propose decisions without changing the selection index or generating new retained revisions.
