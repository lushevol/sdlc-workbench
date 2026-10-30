# Conversation improvement plan, 30 October 2026

No critical conclusions require user attention or action.

Intent source: [exact planning request](../evidence/conversation-retrospective-20261030/planning-user-input.md).
Scope source: [seven retrospective recommendations](CONVERSATION_RETROSPECTIVE_20261030.md#seven-recommendations).

**Proposed sequence: establish shared references, deliver the report, automate reconciliation, then prove consequential behavior.**
Proposed owner: Workbench maintainer. First action: freeze the pilot source identities and define the minimum shared contract.
This order reduces duplicate implementation and inconsistent report totals.
The [retrospective](CONVERSATION_RETROSPECTIVE_20261030.md#seven-recommendations) supplies the evidence for the seven items.

This plan covers all seven recommendations. Individual owners and calendar dates remain unassigned.
Current source baseline: `35529d8db3be1041e550547c83ef044228668a9c`. Implementation effort estimates remain qualitative.

## Delivery stages

| Stage | Items | Deliverable | Completion check |
| --- | --- | --- | --- |
| 1. Establish references | Foundation for 1, 2, 7 | Minimal versioned references for criteria, changes, cases, assertions, executions, environments, and reviewed assessments. | Import existing Session Refresh records without changing original evidence bytes or outcomes. |
| 2. Deliver the reusable report | 1 | One decision-first renderer using a reviewed assessment and retained evidence. | Show recommendation, demonstrated impact, blockers, owner, next action, and metric meaning. Keep supporting details collapsed. |
| 3. Calculate coverage and reconcile evidence | 2, 7 | A derived case index and all three coverage matrices. Start with existing browser and unit results. | All denominators reconcile. Include unmapped, failed, partial, stale, and simulated evidence with explicit limits. |
| 4. Prepare repeatable execution | 4 | One plan and preflight entry point over existing runners and environment configuration. | Check selected browser, services, authentication prerequisites, and actual served build identity before long runs. |
| 5. Prove consequential behavior | 3 | Paired baseline and candidate checks for selected Session Refresh gaps. | Each selected gap gains authoritative assertion evidence or a named unresolved external dependency. |
| 6. Improve supporting workflows | 5, 6 | Question propagation checks and dependency change reports. | Identify missing answer propagation, changed graph claims, affected consumers, and evidence requiring reinvestigation. |

Stages 2 and 3 can run in parallel after stage 1.
Stage 4 can run alongside stage 3.
Question reconciliation and dependency reporting can start once their shared identities are stable.
Stage 5 uses the case index, coverage inventories, and preflight results.
Knowledge questions can proceed earlier when they block a selected assertion.

## Scope for each item

### Item 1: Reusable release summary

Extend the [existing renderer](../../core/release_report_render.py) and [report contract](../../core/release_report_contract.py).
Create an adapter for retained Session Refresh assessments.
Keep reviewed recommendations separate from computed evidence totals.
Preserve evidence confidence, release readiness, and human deployment authorization as distinct fields.
Render offline. Layout changes must not repeat external collection.

Deliver one concise HTML view with expandable issue details.
Check readability, source links, adverse-status visibility, and consistency with supplied assessment data.
The initial view can use existing recorded values before calculated coverage becomes available.
Keep each assessment's provenance and review state visible.
Reuse the [existing presentation proposal](../RELEASE_REPORT_UX_PROPOSAL.md#decision-the-first-screen) where it fits current evidence.

### Item 2: Behavioral coverage calculation

Extend [assurance](../../core/assurance.py) with explicit AC, changed-behavior, and case inventories.
Generate AC-to-test, AC-to-code-change, and code-change-to-test matrices from the same records.
Keep assertion coverage and matching passing execution separate.
Expose missing behavior, contradictions, unsupported additions, and untraced changes.

Check many-to-many mappings, missing inventory items, stale revisions, and empty denominators.
Use the [traceability contract](../../core/knowledge/templates/sdlc/traceability-record.md#coverage-inventories-and-summary) as the output contract.
Semantic conformance remains an evidence-backed review judgment.

### Item 3: Stronger business verification

Select gaps by demonstrated user consequence and genuine blocking applicability.
Begin with logout revocation, stale-response session disruption, and protected-operation state preservation where evidence supports those paths.
Declare the same setup and assertions for baseline and candidate.
Retain requests, state evidence, source identities, environment identity, and disclosed substitutions per case.

The [current assessment](../../tasks/portal-background-session-20261019/10-release-confidence.md#release-scope) warns that newer server code remains unassessed.
Reconcile the intended source composition before new execution.
The [coverage report](../../tasks/portal-background-session-20261019/09-renewal-coverage.md#retained-execution-and-verification) records partial predicates requiring authoritative checks.
Do not expand case counts until the selected proof gaps have a clear disposition.

This work belongs to the existing business task and its scope-specific readiness procedure.
List required policy, accounts, service contracts, and environment access before execution.
Complete independent harness work while those external dependencies remain unresolved.
Unavailable access does not establish a product failure or automatic release hold.

### Item 4: Reliable test entry point

Wrap existing commands rather than replacing their runners.
Reuse [environment selection](../../e2e/README.md#select-a-target-environment) and the current local stack launcher.
Provide a plan that lists the engine, target, exact command, source identities, and output directory.
Check browser assets, installed dependencies, services, authenticated state prerequisites, and served fingerprints.

Report missing or unsupported build fingerprints as unknown identity.
Configured revisions alone cannot prove the running build.
Check failure diagnoses using controlled local fixtures before a representative application run.
Keep setup problems separate from application assertion failures.

### Item 5: Question and answer reconciliation

Preserve the [existing living document](../../tasks/README.md#document-based-knowledge-review) as the editable answer location.
Add checks for stable question IDs, duplicate entry points, answer-source references, and consuming knowledge versions.
Show resolved answers that still lack their required knowledge update.
Investigate available evidence before presenting unresolved questions.

The checker identifies missing propagation. It does not answer business questions or publish knowledge.
Pilot it on one existing clarification scope before extending its supported forms.

### Item 6: Dependency change reporting

Extend the canonical graph skill with a comparison view over retained validated snapshots.
Show changed claims, affected edges, old and new evidence, stale references, and unresolved boundaries.
Link affected consumers to existing contract and case IDs where supporting evidence exists.
Reuse the [investigated context contract](../../.agents/skills/service-dependencies-graph/references/architecture/user-architecture-context.md#investigated-contract-version-110).

Check unchanged snapshots, changed repositories, changed instructions, and unsupported dynamic dependencies.
Keep static relationships separate from observed runtime calls.
Generate concise API, schema, and data comparisons for leadership views when the evidence supports them.

### Item 7: Shared case evidence index

Reuse [immediate case saving](../../e2e/audit.reporter.ts#L85) and [resume records](../../e2e/audit.reporter.ts#L141).
Add adapters for the existing unit and browser result formats first.
Add service and manual result adapters when their pilot consumers require them.
The index references original artifacts and hashes. It does not replace them.

Keep retries, duplicate imports, stale sources, partial assertions, and interrupted runs explicit.
Generate report totals and coverage execution joins from this index.
Check interruption, restart, source changes, and duplicate ingestion without hiding prior failures.

## Minimum shared contract

Use existing canonical identities and references wherever supported.
Add fields only when a named pilot consumer requires them.

- AC, changed-behavior, case, and assertion IDs with exact definition references.
- Repository, baseline, candidate, test revision, and evidence SHA-256 values.
- Environment, configuration, served build identity, and disclosed substitutions.
- Original runner outcome, derived verification disposition, and evidence limits.
- Demonstrated consequence, priority, owner, next action, and reviewed release disposition.

Store a derived index beside supporting evidence.
Preserve existing original snapshots, case artifacts, and immutable audit history.
Keep the single Python runtime and separate collection, rendering, and Release Clinic responsibilities.

## Completion and adoption

Use Session Refresh as the first complete consumer.
Then apply the same contracts to CES migration to detect task-specific assumptions.
Reuse retained evidence for harness checks. Obtain scope-specific readiness before new business execution.
Do not change business application behavior as part of report and evidence-tool maintenance.

For each implementation stage, inspect affected callers and preserve unrelated changes.
Run focused regression checks, complete runtime tests, wheel builds, and workspace validation as applicable.
For packaging changes, initialize and validate a fresh workspace from the built wheel.
Review the staged diff and commit each completed stage separately.

Keep the complete applicable unit suite as a release condition with zero failures.
Selective investigation reruns do not replace that suite.
Compare report corrections, setup failures, repeated questions, stale evidence, and decision time against a recorded baseline.
Set numerical targets after that baseline exists.

## Limits and validation

This stage creates a plan only. No runtime implementation or business execution occurred.
Stage sequence confidence is high. Effort and external verification duration remain uncertain.

The plan adds no executable approval engine or automatic business conformance decision.
Source inspection and an independent dependency review support the proposed sequence.
Document checks are retained in the [planning validation receipt](../evidence/conversation-retrospective-20261030/planning-validation.json).

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
