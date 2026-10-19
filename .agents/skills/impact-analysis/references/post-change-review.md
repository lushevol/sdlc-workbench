# Review implemented changes after investigation

Use this procedure when issue investigation is complete and implementation changes exist.
The portal session correction is its current consumer.
It preserves initial evidence while connecting change impact, review findings, and browser results.
This procedure adds no artifact kind, runtime gate, or automatic execution grant.

## Preserve the initial baseline

Read the completed intake, requirement versions, evidence index, and owning repository instructions.
Preserve `intake.md` bytes. Record its exact Git revision and SHA-256 in the current stage record.
An explicit user freeze takes effect immediately. Do not reopen or rewrite that intake.
Record later questions, contradictions, decisions, and knowledge-update references in the current stage record.
Resolve material intent changes through the existing knowledge procedure and a versioned successor.
Keep publication review separate from clarification and execution evidence.

Use the existing [change request template](../../../../core/knowledge/templates/sdlc/change-request.md) for `tasks/<task-id>/change-review.md`.
The artifact retains `artifact_kind: change-request` and the template's required sections.
State that the selected changes are implemented when exact source evidence establishes that fact.
Record readiness for each named next stage in this record.
A ready analysis stage does not establish test readiness, release approval, or business acceptance.

## Select reusable records

Create only records that support a current decision. Keep one source for each conclusion.
A stage record can contain concise impact analysis and link larger supporting records when necessary.

| Decision or evidence | Existing template | Required addition for this procedure |
| --- | --- | --- |
| Change scope and stage readiness | [Change request](../../../../core/knowledge/templates/sdlc/change-request.md) | Frozen intake, source comparison, user impact, system impact, scoped readiness |
| Code findings and suggestions | [Pull request review](../../../../core/knowledge/templates/sdlc/pull-request-review.md) | Exact diff, affected paths, review coverage, unapplied suggestions |
| Original and additional E2E cases | [Test strategy](../../../../core/knowledge/templates/sdlc/test-strategy-plan.md) | Complete case inventory, change origin, executable assertions, completion conditions |
| Detailed case definition when needed | [Test case](../../../../core/knowledge/templates/sdlc/test-case.md) | Conditions, actions, observable results, fixture and code locators |
| Actual browser results | [Test execution report](../../../../core/knowledge/templates/sdlc/test-execution-report.md) | Per-case outcomes, browser identity, source bindings, screenshots, limits |
| Detailed mappings when needed | [Traceability record](../../../../core/knowledge/templates/sdlc/traceability-record.md) | Requirement, changed source, assertion, execution, and remaining gap |

Do not create every form automatically. Link existing suitable records instead of duplicating them.
Retain detailed inventories and file hashes in task evidence when tables become large.

## Analyze user impact

Identify affected actors and journeys from requirement evidence and inspected code.
For each material journey, record the trigger, previous behavior, changed behavior, and observable consequence.
Cover positive behavior, failure behavior, recovery, and state preservation when those paths changed.
Include accessibility or activity inputs when they affect the changed journey.
Record unaffected journeys only when their evidence establishes a relevant boundary.

Separate demonstrated effects from possible consequences and unresolved business expectations.
Give each finding evidence, a consequence, an owner, and a next action.
Use `unknown` when no owner evidence exists.
Do not invent a business limit from a timer, retry constant, or test fixture.

## Analyze system impact

Record every selected repository's full base and head commits, changed paths, and relevant file hashes.
Record local modifications separately. Review their actual bytes before including them in scope.
Inspect changed symbols and affected callers, importers, consumers, contracts, and relevant unchanged paths.
Use current graph evidence when available. Use direct source inspection when coverage is stale or absent.
Do not rebuild unrelated indexes or claim complete dependency discovery from a static graph.

Assess affected interfaces, authentication state, storage, requests, concurrency, timers, cancellation, cleanup, and error propagation where relevant.
Inspect shared libraries and deployment configuration when their values control the changed behavior.
State qualitative risk and its source basis. Identify missing repositories and uninspected boundaries beside the affected claim.
Distinguish source relationships, declared metadata, and observed runtime paths.

## Review code without applying suggestions

Read the actual selected diff and the surrounding implementation at the recorded revisions.
Check the requirement mapping before declaring a defect.
Check error paths, overlapping operations, stale state, cancellation, lifecycle cleanup, and compatibility when the diff affects them.
Inspect assertion contents and helper chains before relying on existing tests.

For each actionable finding, provide priority, exact location, evidence, consequence, owner, and suggested action.
Distinguish confirmed defects, possible risks, and optional improvements.
Keep application code unchanged when the request asks for suggestions only.
Record suggestions as unapplied. New test code requires the task's separate test authorization.
Do not merge, publish, or infer a human approval from the review report.
Record inspected paths and omitted boundaries even when no actionable defect is found.

## Expand E2E coverage from the selected changes

Inventory all original defect cases before adding cases.
Assign stable IDs to new cases and link each to a changed path or review finding.
Inspect executable setup, helpers, actions, and assertions. A case name does not prove coverage.
Include changed positive, negative, boundary, race, cancellation, retry, cleanup, and lifecycle predicates where applicable.
State why an excluded boundary does not apply, or keep its coverage gap open.

Keep new test code in the owning test repository. Preserve unrelated modifications.
Use authorized fixtures and actual target services for the requested browser checks.
Disclose interception, injected clocks, synthetic data, shortened lifetimes, and substituted dependencies.
These controls can test branches. They cannot prove omitted service behavior or natural elapsed-time conditions.
Define suite completion against the complete original-plus-new inventory.
A smaller passing subset does not satisfy a request to run every declared case.

## Execute and retain real-browser evidence

Inspect available runtimes, configured targets, existing processes, and test-engine instructions before setup.
Reuse authorized available environments. Do not overwrite unrelated services or personal browser state.
Check browser, service, configuration, application, and test revisions before the run.
Record the exact command or tool operation, timestamps, clock, environment, launch settings, and fixture state.

Run every original and new case in a real browser when the environment supports its required conditions.
Use actual elapsed time when the claimed behavior depends on natural inactivity or a policy duration.
Record tab visibility, freeze observations, sleep state, and observer effects when lifecycle behavior matters.
Keep forced lifecycle experiments separate from natural lifecycle evidence.

Retain per-case expected predicates, actual values, outcome, assertion locators, and request or event correlations.
Capture starting, decisive intermediate, and final states under the [screenshot rules](../../../../docs/BROWSER_INVESTIGATIONS.md#retain-key-screenshots).
Bind each capture to the case, step, time, phase, method, hash, supported claim, and limits.
Store results under the task with source hashes and exact revisions.
Exclude credentials and raw tokens from retained evidence. State any redaction's effect on the supported claim.

Keep failures, errors, skips, blocked cases, and missing captures visible.
Report setup failures as setup failures. Do not count them as executed business predicates.
Compare executed source hashes with final source bytes before reusing passing results.
Rerun affected cases when relevant code, tests, fixtures, or configuration change.
Do not replace a failed application predicate with a weaker assertion to obtain a pass.

## Assess stage completion

Check the frozen intake hash after completing each stage.
Run artifact lint against explicit completed artifacts and validate applicable workspace records.
Check links, source locators, hashes, and declared case totals.
Keep automated checks separate from ASD writing review, which remains pending without a complete review.

Record each stage's status, assessor, time, evidence, rationale, blocked actions, owner, and next action.
Use `READY` only when evidence supports the named next stage within the existing authorization.
Use `READY_WITH_LIMITS` for continued evidence collection and `NEEDS_CLARIFICATION` for material intent or evidence gaps.
Neither status permits a dependent stage that lacks required evidence.
Keep readiness separate from review approval, verified behavior, issue closure, and release decisions.

A requested full browser run remains incomplete while any inventoried case lacks its required real-browser result.
A completed failed run supplies evidence but does not establish passing behavior.
Report both execution completeness and behavior outcomes.
