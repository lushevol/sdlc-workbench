---
name: manage-knowledge-lifecycle
description: Assess knowledge lifecycle progress, identify the next evidence-backed actions, and coordinate existing source, ingestion, governance, and wiki skills. Use for knowledge status, next-step guidance, or resuming a knowledge workflow.
---

# Manage the knowledge lifecycle

Give the user a clear current position and next action for the requested knowledge scope.
Coordinate the existing skills through [the lifecycle map](../../../docs/KNOWLEDGE_LIFECYCLE.md) and [knowledge contract](../../../knowledge/README.md).
This is agent guidance, not a background monitor, workflow runner, or additional stored lifecycle.

## Establish scope and authorization

Infer the collection, records, task, and goal from the request and existing evidence before asking.
Keep the user's latest answers and existing authorization when resuming; preserve exact new input before investigation or delegation.
Use one owning task and living question document for business work under [the task guide](../../../tasks/README.md).
Harness maintenance needs no business task or domain record.

For “status”, “what next”, or review-only requests, inspect evidence and return guidance without changing sources, selections, records, audit, receipts, or wiki content.
Local checks may generate ignored planning output. They do not authorize semantic updates.
For “continue”, “ingest”, or “manage this workflow”, perform the applicable authorized work through the selected skills and reassess after each result.
Continue independent work while a gate blocks one scope. Do not stop at a plan when execution is requested and authorized.
A continuation supplies no missing policy answer, reviewer identity, publication approval, or external execution grant.

## Assess recorded progress

Inspect the active task evidence index, living questions and knowledge-update log, relevant source manifest/selections/processing receipts,
canonical IDs/versions/states and review/audit evidence, then wiki bindings, pending attempts, completion receipts and outputs.
Use exact paths, source revisions and hashes. Prior summaries locate evidence; reopen claim-bearing artifacts before declaring current status.
Limit semantic reading to queued sources, affected records and necessary context. Broaden discovery when dependencies are incomplete.

Report these dimensions separately rather than assigning one overall “complete” state:

| Dimension | Evidence needed for a current claim |
| --- | --- |
| Source coverage | Current selection bindings, verification result, review/process queues and explicit held or missing pages. |
| Canonical processing | Reviewed receipts and matching current outputs; changed outputs also need their sealed final checkpoint. |
| Intent and governance | Actual record state/version, claim support, unresolved questions, prepared hashes, reviews and immutable events. |
| Publication | Required human review and approval for the final bytes, plus applicable deterministic gates. Candidate ingestion is not publication. |
| Derived wiki | Compare requested canonical IDs with reviewed completion receipt IDs, current input/output hashes, pending attempts, plan and verification. List uncovered or legacy inputs as pending scoped review even when structural verification passes. |
| Implementation or release | Independent task gaps, exact revisions and retained execution/deployment evidence, only if within the requested scope. |

Use `unknown`, `stale`, `partial`, `pending`, or `NOT_RUN` when evidence requires it. Do not manufacture percentages or authenticated authority.
A passed validator cannot establish semantic correctness. Wiki freshness cannot establish publication or deployed behavior.
A scoped unchanged wiki plan establishes only its selected scope; it cannot establish whole-wiki completion.

## Select the next action

Choose the earliest unmet prerequisite **for the requested outcome**, with separate actions for independent scopes.
Do not restart completed work merely because another lane is pending.

| Observed condition | Route and completion evidence |
| --- | --- |
| Interrupted attempt, changed prepared bytes, concurrent edits or split wiki provenance | Inspect the attempt and recovery material first. Use [transition preparation](../prepare-knowledge-transition/SKILL.md) or [wiki finalization](../finalize-wiki-update/SKILL.md). Preserve edits and prior events; reconcile ownership before retrying. |
| New export, changed source/context or unfinished selection | [Prepare sources](../prepare-knowledge-sources/SKILL.md). For authorized ingestion, capture the ingestion baseline before tracked source/record/audit edits. Refresh/select as needed, then run a current local source plan before semantic processing. |
| Current selected sources have queued canonical work | [Ingest knowledge](../ingest-knowledge/SKILL.md). Review the affected closure, seal actual changes and record reviewed results through `sources complete`; replan to show remaining work. |
| Returned answers or unresolved material intent | [Resolve questions](../resolve-knowledge-questions/SKILL.md). Investigate first; preserve answers, propagate resolved meaning into affected candidates/successors, then complete required governance and wiki work. |
| Supported candidates need review, conflict handling, stale/superseded treatment or requested publication | [Govern knowledge](../govern-knowledge/SKILL.md). Use actual final-byte reviews and gates. Required human review remains pending until supplied. |
| Canonical inputs changed or wiki completion is missing/stale | [Maintain the wiki](../llm-wiki/SKILL.md). Plan exact records, bind, maintain, review, finalize and verify through the project bridge. Qualified candidate summaries may proceed before publication. |
| A question needs an answer, with no update requested | [Query knowledge](../query-knowledge/SKILL.md). Return applicable source-backed claims and evidence limits without lifecycle mutation. |
| Release or implementation evidence differs from intent | [Classify changes](../classify-knowledge-change/SKILL.md); use [release synchronization](../sync-release-knowledge/SKILL.md) when requested. Keep conformance gaps separate; update meaning only from supported intent changes. |
| All requested processing is current | Report completed scope and remaining owner/acceptance actions, or state that no action is required until a named source, intent or evidence change. Skip unchanged semantic work. |

Load the selected skill before using its operations. Reuse its command contracts; do not duplicate their mechanics here.
Keep source preparation, canonical processing, governance and wiki completion distinct.
Held pages prevent a full-collection completion claim; an explicitly bounded partial view can still support independent reviewed work.
Missing pages authorize no deletion. Source selection alone does not clear canonical queues.
Changed approvals or prepared bytes require affected review, not hash advancement to hide unfinished work.

## Guide every handoff

Lead with the current outcome and **one immediate next action**. Add parallel or later actions only when useful.
For each material action, name the reason, evidence link, responsible owner (`unknown` if unavailable), selected skill,
required decision/input, and observable completion condition. Separate work the agent can perform now from a human or external dependency.
Give confidence and material limits beside conclusions. Ask only questions investigation cannot resolve and which affect the next decision.
For owner questions, use the living editable document with suggested options; preserve unanswered items and existing answers.

During authorized execution, update the existing living report/question document and evidence index with completed work and remaining actions.
Keep routine plans in ignored working storage. Do not create a second status ledger, duplicate payloads or rewrite immutable events.
Before final handoff, recheck that completed receipts, canonical bytes, reviews, audits and wiki outputs still agree for the declared scope.
Report checks actually run and remaining limits. Finish with a concrete next action even when it is “owner review” or “wait for the next source change”.
