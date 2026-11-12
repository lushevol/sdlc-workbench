---
name: check-knowledge-integrity
description: Run existing deterministic knowledge, provenance, retention, and prepared-content checks without supplying semantic review or changing records.
---

# Check knowledge integrity

Input: workspace, selected records, source and audit history, and any existing ingestion baseline, plan, and prepared seal.
Output: actual check status, reports, exact checked scope, failures, deferred preparation findings, and unchecked limits.
This operation checks saved records. It does not repair evidence, transition states, approve knowledge, or run business tests.

## Check

1. Run `ai-sdlc --workspace PATH validate` against the complete proposed records and recorded gates.
2. For an ingestion or governance batch, use the existing [harness commands](../ingest-knowledge/references/workflow.md#harness-commands).
3. At preparation, use `--phase prepare` and report its selected deferred findings. A prepared result is not final acceptance.
4. At completion, use the captured baseline, actual plan, and `--seal` prepared checkpoint for the final harness check.
5. Inspect retention findings, source and manifest hashes, audit history, locators, execution bindings, and prepared document hashes.
6. Review the diff against the baseline. Preserve unrelated changes, prior sources, candidates, findings, and immutable events.

Use unused report paths. Keep earlier checkpoint reports as evidence.
The final check cannot defer missing events or approval gates. A changed prepared document requires new preparation and affected review.
Report unintended raw or audit changes and the required recovery. Route authorized repairs through their owning procedure.
New snapshots and correction events belong to those procedures.
Mark mismatched execution support stale. Do not edit retained execution or weaken assertions to obtain a passing check.
Keep semantic support and applicability assessment separate from structural validity and hash agreement.

## Report

Report actual validator and harness results, selected scope, counts or findings, output paths, and remaining required actions.
Use `NOT_RUN` if a checker is unavailable. List manual checks and their limits without inventing a passed result.
The validator excludes the derived wiki subtree. Use [wiki health checks](../check-wiki-health/SKILL.md) for that separate format and source bindings.
Report a missing, stale, failed, or partial check beside the claims it limits.
Validation cannot authenticate reviewers, establish append-only history by itself, decide intent, or prove deployed business behavior.
