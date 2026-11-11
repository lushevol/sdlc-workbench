---
name: sync-release-knowledge
description: Reconcile release changes with intended business-domain knowledge. Update governed candidates for sourced changes of target rules, record intent-to-implementation gaps separately, preserve history, and reconcile release reports. Use for post-release knowledge maintenance and intent review.
---

# Synchronize release knowledge

Use this file-based agent procedure for an explicitly selected release and environment.
It coordinates existing records and governance tools. It provides no workflow runner, deployment trigger, or automatic applicability resolver.
Keep release approval, knowledge review, publication, and observed execution separate.
Knowledge describes requirements, intent, and ideal target behavior. It does not describe implementation status or observed runtime behavior.
Keep actual behavior and differences in an independent gap Markdown document under the owning task.
Follow the [knowledge boundary](../../../knowledge/README.md) and [gap procedure](../detect-gaps/SKILL.md).

## Establish the operation

Preserve exact user input before investigation. Reuse the owning business task and its current stage record.
Read the [knowledge contract](../../../knowledge/README.md) and [current task view](../analyze-requirement/references/current-task-view.md).
Use one living `tasks/<task-id>/10-knowledge-sync.md`, with evidence under that task.
Follow the [report reference](references/reporting.md) using the existing change-request form. Preserve frozen intake and historical assessments.

Select workspace, release, baseline, repositories, target environment, deployment or rollout, cohort, owner, and requested as-of time.
Discover existing evidence before asking for unavailable inputs. Keep unknown identities explicit.
Inspect registered tools through `ai-sdlc --workspace PATH status`, resource schemas, and exact grants before calls.
This procedure grants no deployment, production probe, external write, or message authorization.

Record an operation identity from workspace, release, deployment or rollout, environment, and relevant cohort.
Record input evidence fingerprints, starting knowledge ID/version/hash pairs, and the operation's prior attempts.
Prepare intended-rule candidates when supported intent sources change. A release alone does not change intended rules.
Missing deployment proof limits realization and conformance claims in the gap document. It does not prevent recording a supported target rule.
Reassess the named stage boundary before downstream publication or deployment claims.

## Map changed meaning and applicability

Inspect exact release source, affected consumers, contracts, configuration, requirements, existing knowledge, and retained observations.
Use intent sources to establish the target rule and its intended applicability.
Bind actual deployment claims in the gap document to artifact and effective configuration evidence.
Use [deployment comparison](../verify-implementation/references/deployment-comparison.md) for environment-dependent claims.
Keep UAT remote logs within their UAT scope under the [runtime evidence procedure](../release-confidence/references/runtime-log-evidence.md).
Local execution and UAT observations cannot establish production execution.

Declare required synchronization rows before counting. Give each row a stable ID, intended rule, and intended applicability scope.
Map each row to existing knowledge IDs or a proposed missing topic. Include consequential unchanged consumers.
Compare old knowledge, intended behavior, inspected implementation, deployment evidence, and observed execution separately.
Identify corrected defects, supported intent changes, and differences that need independent gap records.

- When a fix restores an existing rule, keep the knowledge rule unchanged. Update the gap disposition and release evidence.
- When implementation contradicts intent, preserve the target rule. Record the actual difference and its evidence in the independent gap document.
- When an authoritative source changes intended behavior, prepare the target-rule successor with the source, scope, and required review.
- When only code, deployment, or execution evidence changes, record a supported knowledge no-change disposition.
- When intent is missing, retain the intent gap. Do not derive a confirmed target rule from implementation.

Use stable gap IDs. Link each gap to the intended knowledge ID/version, old/new source, assertions, observations, and their limits.
Keep setup, numbered steps, intended result, old result, and new result in the gap document.
State consequence, priority, owner, and next action. Separate implementation gaps from unavailable verification or deployment evidence.
A navigation-only knowledge edit must remain distinct from a change of intended behavior.

Record intended environments, actors, conditions, and effective rule dates beside changed target rules when intent sources support them.
Keep actual artifacts, configuration, cohorts, deployments, observation intervals, and execution outcomes in gap or release evidence.
Use linked scoped attempts when deployment proof covers only part of the release.
Evidence for one component or cohort cannot establish another row's realization.
Distinguish rule applicability, deployment time, observation time, and documentation time. Keep unavailable dates unknown.
Retrieval does not interpret applicability extensions automatically.

For partial rollout, compare deployed cohorts against the applicable target rule in the gap document.
A rollout or rollback does not change intent without a supported intended-rule decision.
Record rollout outcomes and intervals outside knowledge. Preserve release evidence and publication history.
Recheck configuration, migrations, persistent state, and external effects. Old code alone cannot prove restored old behavior.
For overlapping releases, inspect actual component combinations. Release ordering alone cannot establish applicability.

## Prepare candidates and review the batch

Follow [govern-knowledge](../govern-knowledge/SKILL.md) and the [ingestion checkpoints](../ingest-knowledge/references/workflow.md#harness-commands).
Capture original source, manifest, audit, and knowledge bytes with the existing harness before record changes.
Keep raw sources and execution evidence outside `knowledge/`. Preserve stable source IDs and append changed-source snapshots.
Retain claim-bearing failed, stale, and contradictory evidence with its original bindings.

Keep the stable knowledge ID for the same concept. Create a successor version for changed content.
Record predecessor version and content hash. Use each ID/version pair once and preserve earlier bytes and required history.
Do not globally supersede a predecessor whose intended rule still applies to another environment, actor, or condition.
Prepare dependent records as one consistent group. Keep unresolved independent topics separate.

Present one review batch with old intent, proposed intent, intended applicability, source authority, and required owner decisions.
Link the independent gap document for implementation comparisons and operational evidence.
Use the existing living question document for material unresolved business answers.
Prepare all supported diffs and checks before requesting any required human decision. Do not request approval per file.
Preserve existing task authorization and recorded answers. A continuation request supplies no missing business answer or publication approval.
Important requirements and decisions require recorded human review before publication.
Release approval counts only when its actual authority explicitly covers the final knowledge content and required publication gate.
Never transfer a predecessor's approval to changed bytes.

Recheck starting knowledge hashes before applying prepared updates. Stop affected writes when concurrent edits invalidate that base.
Reconcile the current content and evidence, prepare a new diff, and repeat affected review.
Finish wording and metadata before calculating final hashes and appending immutable events.
Record actual actors, review times, reviewed hashes, and required events through the existing governance contract.
Do not edit earlier events or invent reviewers. Any later content edit requires renewed preparation and matching events.
Validate final records, provenance, audit bindings, and task references. Publication remains pending until applicable gates pass.

## Confirm accuracy and reconcile reports

Re-read knowledge against original requirements, latest intent clarifications, and applicable decisions.
Check that each changed target rule has an intent source and intended applicability. Preserve unchanged required meaning.
Review the independent gap document against exact source, deployment receipts, configuration, assertions, and retained execution.
Check that implementation or execution facts have not entered knowledge as target rules or delivery status.
Inspect old/new knowledge diffs for omissions, contradictions, unsupported additions, and accidental changes outside the selected release.
Verify source hashes, predecessor bindings, current review hashes, immutable events, and final validation results.
Use an independent reader when available to distinguish target rules from actual behavior through knowledge and the separate gap document.
Disclose self-review when independent review is unavailable. Automated checks cannot establish semantic accuracy alone.

Update domain navigation, related references, the independent gap document, the task knowledge-update log, and Markdown/HTML release-report views.
When canonical knowledge or navigation changes, use the [llm-wiki bridge](../llm-wiki/SKILL.md) and its [compile procedure](../llm-wiki/references/workflows.md#compile-canonical-records) to reconcile affected pages from exact changed sources.
Follow the bridge's selected engine, linked-source and provenance-completion rules. Run `verify`; refresh the native wiki graph when graph maintenance is in scope.
Wiki updates and model-inferred connections cannot establish rollout, publication, synchronization completion or passing behavior.
An inspected knowledge no-change disposition does not require rewriting unchanged wiki content.
Keep one canonical row inventory and synchronization summary. Link report views to it and compare displayed counts and dispositions.
Preserve frozen assessments. Record later synchronization in the maintained current view or a linked successor.
An unavailable report renderer leaves report synchronization pending. Do not claim parity from editing one format.
Knowledge updates cannot remove a failed release condition or turn an observed failure into a pass.

## Resume and complete

For identical operation identity, evidence fingerprint, and base knowledge hashes, resume pending work or return its existing result.
Inspect existing versions and audit events before writing. Do not create duplicate successors or events on retries.
Changed evidence or rollout creates a linked scoped attempt. Preserve earlier attempts and their conclusions.
Changed base knowledge hashes require a linked reconciled attempt. Preserve earlier candidate bytes and their review history.
After interruption, reconcile retained rows, final hashes, reviews, events, publication, and report views before further writes.

Use `PENDING`, `DRAFTED`, `IN_REVIEW`, `COMPLETE`, `PARTIAL`, or `BLOCKED` for this operation only.
These labels are report values, separate from knowledge lifecycle and release status. They add no executable state machine.
Count a row as synchronized only with matching eligible published knowledge or an inspected, supported no-change rationale.
Candidate preparation, intended-rule changes, gap review, publication, and report parity need separate counts.
Closing a gap or recording a knowledge no-change disposition does not establish implementation conformance.
`COMPLETE` requires all declared rows synchronized, no unknown affected scope, and reconciled required report views.
Use `DRAFTED` or `IN_REVIEW` for prepared candidates awaiting gates. Use `PARTIAL` when independent resolved rows coexist with gaps.
Use `BLOCKED` when a material dependency prevents further work. Name its owner, consequence, and next action.
Unknown or empty denominators produce `N/A`, with the reason. They cannot produce `100%` synchronization.
Return changed intent IDs/versions, knowledge no-change rows, independent gap locators, validation, report parity, and remaining owner actions.
