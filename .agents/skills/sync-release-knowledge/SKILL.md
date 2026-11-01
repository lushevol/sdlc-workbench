---
name: sync-release-knowledge
description: Synchronize business-domain knowledge with a release's actual implementation, deployment scope, and retained observations. Prepare governed candidate updates, review applicability and accuracy, preserve history, and reconcile release reports. Use for post-release knowledge updates or candidate preparation when deployment proof is unavailable.
---

# Synchronize release knowledge

Use this file-based agent procedure for an explicitly selected release and environment.
It coordinates existing records and governance tools. It provides no workflow runner, deployment trigger, or automatic applicability resolver.
Keep release approval, knowledge review, publication, and observed execution separate.

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
With no deployment proof, select candidate preparation. Do not describe the result as deployed or current target behavior.
Missing deployment identity must not prevent useful source-backed candidate work.
Reassess the named stage boundary before downstream publication or target-applicability claims.

## Map changed meaning and applicability

Inspect exact release source, affected consumers, contracts, configuration, requirements, existing knowledge, and retained observations.
Bind deployed applicability to artifact and effective configuration evidence, rather than release names or branch labels.
Use [deployment comparison](../verify-implementation/references/deployment-comparison.md) for environment-dependent claims.
Keep UAT remote logs within their UAT scope under the [runtime evidence procedure](../release-confidence/references/runtime-log-evidence.md).
Local execution and UAT observations cannot establish production execution.

Declare required synchronization rows before counting. Give each row a stable ID, topic, claim, and target applicability scope.
Map each row to existing knowledge IDs or a proposed missing topic. Include consequential unchanged consumers.
Compare old knowledge, intended behavior, inspected implementation, deployment evidence, and observed execution separately.
Identify corrected defects, changed rules, contract responsibilities, configuration semantics, and contradictory behavior.

- When a fix restores an existing rule, preserve that rule. Update outdated actual-behavior or delivery descriptions instead.
- When actual behavior contradicts approved intent, record scoped actual behavior and a conflict finding. Preserve the intended rule.
- When only supporting evidence changes, keep a sourced no-change disposition unless reusable meaning or applicability changes.
- When affected knowledge is absent, prepare a domain topic with sources and an explicit owner or `unknown`.

Record environment, cohort, artifact/configuration identities, effective interval, evidence class, review state, and limits for changed claims.
Use row-level modes or linked scoped attempts when deployment proof covers only part of the release.
Evidence for one component or cohort cannot establish another row's deployed applicability.
Distinguish deployment time, observation time, and documentation time. Use unknown effective dates when evidence cannot establish them.
Existing schemas permit applicability extensions. Retrieval does not interpret those extensions automatically.

For partial rollout, preserve old and new descriptions within their separate applicable scopes.
For rollback, record a new rollout outcome and interval. Preserve withdrawn behavior, release evidence, and publication history.
Recheck configuration, migrations, persistent state, and external effects. Old code alone cannot prove restored old behavior.
For overlapping releases, inspect actual component combinations. Release ordering alone cannot establish applicability.

## Prepare candidates and review the batch

Follow [govern-knowledge](../govern-knowledge/SKILL.md) and the [ingestion checkpoints](../ingest-knowledge/references/workflow.md#harness-commands).
Capture original source, manifest, audit, and knowledge bytes with the existing harness before record changes.
Keep raw sources and execution evidence outside `knowledge/`. Preserve stable source IDs and append changed-source snapshots.
Retain claim-bearing failed, stale, and contradictory evidence with its original bindings.

Keep the stable knowledge ID for the same concept. Create a successor version for changed content.
Record predecessor version and content hash. Use each ID/version pair once and preserve earlier bytes and required history.
Do not globally supersede a predecessor that remains applicable to another supported environment or cohort.
Prepare dependent records as one consistent group. Keep unresolved independent topics separate.

Present one review batch with old meaning, proposed meaning, applicability, source evidence, conflicts, and owner actions by topic.
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

Re-read final bytes against original requirements, source, deployment receipts, configuration, assertions, and retained execution.
Check that each new claim states its supported class and applicability. Check that unchanged required meaning remains intact.
Inspect old/new knowledge diffs for omissions, contradictions, unsupported additions, and accidental changes outside the selected release.
Verify source hashes, predecessor bindings, current review hashes, immutable events, and final validation results.
Use an independent reader when available to answer representative environment/as-of questions from the updated records.
Disclose self-review when independent review is unavailable. Automated checks cannot establish semantic accuracy alone.

Update domain navigation, related references, the task knowledge-update log, and maintained Markdown/HTML release-report views.
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
Candidate preparation, review completion, publication, and report parity need separate counts.
`COMPLETE` requires all declared rows synchronized, no unknown affected scope, and reconciled required report views.
Use `DRAFTED` or `IN_REVIEW` for prepared candidates awaiting gates. Use `PARTIAL` when independent resolved rows coexist with gaps.
Use `BLOCKED` when a material dependency prevents further work. Name its owner, consequence, and next action.
Unknown or empty denominators produce `N/A`, with the reason. They cannot produce `100%` synchronization.
Return changed IDs/versions, no-change rows, unresolved rows, scope limits, validation, report parity, and remaining owner actions.
