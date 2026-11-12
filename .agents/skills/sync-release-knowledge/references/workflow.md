# Release synchronization operation contract

Use this contract with the [sync-release-knowledge orchestrator](../SKILL.md).
Knowledge describes intended domain behavior. Keep actual behavior and differences in independent task gap Markdown.

## Establish the operation

Preserve exact user input before investigation. Reuse the owning business task and its current stage record.
Read the [current task view](../../analyze-requirement/references/current-task-view.md).
Use one living `tasks/<task-id>/10-knowledge-sync.md`, with evidence under that task.
Follow [the reporting reference](reporting.md). Preserve frozen intake and historical assessments.

Select workspace, release, baseline, repositories, environment, deployment or rollout, cohort, owner, and requested as-of time.
Investigate available sources before clarification. Keep unavailable identities explicit.
Discover tools, schemas, and exact grants before calls. This procedure grants no additional external access.

Record an operation identity from workspace, release, deployment or rollout, environment, and cohort.
Record evidence fingerprints, starting knowledge ID/version/hash pairs, and prior attempts.
Use existing [ingestion checkpoints](../../ingest-knowledge/references/workflow.md#harness-commands) before authorized record changes.
Missing deployment evidence limits realization claims. It does not prevent recording a supported intended rule.
Reassess the named stage boundary before downstream publication or deployment claims.

## Declare and classify synchronization rows

Declare the complete required row inventory before counting. Give each row a stable ID, target rule, and intended applicability.
Map rows to existing knowledge IDs or missing topics. Include consequential unchanged consumers and unknown affected scope.
Use [change classification](../../classify-knowledge-change/SKILL.md) for intent, no-change, maintenance, and gap dispositions.
Keep setup, numbered steps, intended result, old result, and new result in the independent gap document.
Use stable gap IDs and link exact knowledge, source revisions, assertions, observations, consequence, owner, and next action.
Separate actual implementation gaps from unavailable verification or deployment evidence.

Use [deployment comparison](../../verify-implementation/references/deployment-comparison.md) for actual environment-dependent claims.
Keep [UAT remote logs](../../release-confidence/references/runtime-log-evidence.md) within their tested build and environment scope.
Local execution or UAT observations cannot establish production execution.
For partial rollout, bind each row's realization to its component, cohort, effective configuration, and observation interval.
Use linked scoped attempts when proof covers only part of the release. One row's evidence cannot establish another's realization.
For overlapping releases, inspect actual component combinations. Release order alone does not establish applicability.

## Prepare and review the batch

Route supported changes through the orchestrator's composition and governance skills.
Keep a stable ID for the same concept and retain earlier bytes, predecessor versions, and content hashes.
Do not globally supersede a predecessor whose rule remains applicable to another actor, environment, or condition.
Prepare dependent records as one consistent group. Keep unresolved independent topics separate.

Present old intent, proposed intent, applicability, source authority, and required owner decisions in one review batch.
Link the independent gap document for implementation and operational comparisons.
Keep material business questions in the existing living question document.
Release approval supplies knowledge approval only when its actual authority covers the final content and publication gate.
Important requirements and decisions require recorded human review before publication.

Recheck starting hashes before affected writes. Concurrent changes require reconciliation and renewed affected review.
Finalize wording and metadata before exact-byte preparation and append-only audit events.
Any later content edit requires renewed preparation and matching events. Never invent actors or rewrite historical events.

## Confirm accuracy and reconcile reports

Review final intent against original requirements, latest clarifications, and applicable decisions through the shared claim-review skill.
Check omissions, contradictions, unsupported additions, and changes outside the selected release.
Review the gap document against exact source, deployment, configuration, assertions, retained execution, and their limits.
Use an independent reader where available. Disclose self-review; automated validation cannot establish semantic accuracy.

Update domain navigation, related references, gap records, task knowledge-update log, and required Markdown/HTML release views.
Use [llm-wiki](../../llm-wiki/SKILL.md) for affected canonical changes. Preserve qualified candidates and engine provenance.
An inspected no-change disposition does not require rewriting unchanged wiki content.
Wiki maintenance cannot establish rollout, publication, passing behavior, or synchronization completion.

Keep one canonical row inventory and summary. Compare displayed scope, versions, counts, dispositions, conflicts, and actions across views.
Preserve frozen assessments. Update a maintained view or link a successor.
An unavailable renderer leaves parity pending. Editing one format cannot establish cross-format parity.
Knowledge maintenance cannot remove a failed release condition or turn an observed failure into a pass.

## Resume and complete

For identical operation identity, evidence fingerprint, and base hashes, resume pending work or return the existing result.
Inspect versions and audit events before writing. Do not create duplicate successors or events on retries.
Changed evidence or rollout creates a linked scoped attempt. Changed base hashes require a linked reconciled attempt.
Preserve earlier candidate bytes, attempts, conclusions, and review history.
After interruption, reconcile retained rows, final hashes, reviews, events, publication, wiki outcome, and report views before further writes.

Use `PENDING`, `DRAFTED`, `IN_REVIEW`, `COMPLETE`, `PARTIAL`, or `BLOCKED` for the operation only.
These report values remain separate from knowledge lifecycle and release status. They add no executable state machine.
Count a row as synchronized only with applicable published knowledge or an inspected, supported no-change rationale.
Keep preparation, intended-rule change, gap review, review completion, publication, and report parity counts separate.
Closing a gap or recording no change cannot establish implementation conformance.
`COMPLETE` requires all declared rows synchronized, no unknown affected scope, and reconciled required report views.
Use `DRAFTED` or `IN_REVIEW` for candidates awaiting gates; use `PARTIAL` for independent resolved rows beside remaining gaps.
Use `BLOCKED` when a material dependency prevents further work. Name owner, consequence, and next action.
Unknown or empty denominators produce `N/A` with a reason. They cannot produce `100%` synchronization.
