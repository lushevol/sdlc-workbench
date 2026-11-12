---
name: classify-knowledge-change
description: Compare old knowledge with new intent and implementation evidence to distinguish intended-rule changes, supported no-change outcomes, independent gaps, and unresolved intent.
---

# Classify a knowledge change

Input: scoped change or release, exact old knowledge ID/version/hash, new sources, affected consumers, and applicable intent.
Use during incremental ingestion and release synchronization before preparing record changes.
This operation returns dispositions. It does not edit knowledge, grant publication, or establish deployment.

## Compare meaning and applicability

Use [retrieve-knowledge-evidence](../retrieve-knowledge-evidence/SKILL.md) to inspect exact source revisions and surrounding context.
Use [assess-knowledge-applicability](../assess-knowledge-applicability/SKILL.md) for actors, environments, conditions, and intended rule dates.
Compare old intent, proposed intent, old/new implementation, deployment evidence, and observed execution separately.
Include consequential unchanged consumers. Release order, code changes, or passing tests cannot supply missing policy.

| Evidence-backed condition | Disposition and next route |
| --- | --- |
| Applicable requirement, decision, or clarification changes intended behavior | Prepare an intent successor through [compose-knowledge-records](../compose-knowledge-records/SKILL.md) and governance. |
| A fix restores the existing rule | Keep canonical meaning unchanged. Update conformance and gap evidence. |
| Implementation contradicts intended behavior | Preserve intent. Record the difference in independent task gap Markdown. |
| Only implementation, deployment, or execution evidence changes | Record a supported knowledge no-change rationale and its evidence boundary. |
| Intent sources are missing or conflict materially | Preserve the unresolved intent gap. Investigate before changing meaning. |
| Only navigation or metadata needs correction | Classify a maintenance edit separately from intended-rule change; changed bytes still need matching governance evidence. |

Record each disposition by stable row ID, target rule, old ID/version/hash, intended applicability, evidence, consequence, owner, and action.
Identify dependent records and still-applicable predecessors. Never globally supersede a rule that remains applicable elsewhere.
Keep unknown owners and dates explicit. A rollout or rollback changes intent only with a supported intended-rule decision.
For actual rollback claims, inspect configuration, migrations, persistent state, and external effects alongside code.

## Return the classified inventory

Return changed-intent rows, supported no-change rows, maintenance edits, implementation gaps, and unresolved intent separately.
Link exact source locators for each outcome. Reuse [the old/new gap case rules](../verify-implementation/references/behavior-review.md#compare-old-and-new-behavior).
Keep setup, numbered steps, intended result, old result, new result, assertions, and observations outside canonical knowledge.
Stop affected candidate preparation when intent or starting hashes cannot support the proposed meaning.
Publication and execution verification remain separate downstream operations.
