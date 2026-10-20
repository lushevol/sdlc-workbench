---
name: verify-implementation
description: Compare approved behavior with exact implementation revisions, inspected assertions, and retained execution evidence.
---

# Verify implementation behavior

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

Apply the intake gate below only to business behavior requirements and issues in existing business repositories.
For changes limited to harness maintenance, verify exact source, assertions, and execution evidence directly.
Classify work by business impact using [the scope rules](../../../tasks/README.md#scope).
Those changes do not require a business task or business knowledge records.
For mixed requests, apply the gate to the business scope and verify supporting harness changes directly.

For the business scope, read `tasks/<task-id>/intake.md`, its evidence index, and the current stage record when present.
Require `READY` for this named phase with an explicit evidence-based rationale.
Preserve completed intake bytes. Record later phase readiness and findings in the current stage record.
Follow the [post-change procedure](../impact-analysis/references/post-change-review.md) for change-derived cases and complete real-browser execution.
`READY_WITH_LIMITS` and `NEEDS_CLARIFICATION` permit no downstream handoff.
Browser, service, and test investigations can collect intake evidence before this gate passes.
Use the [intake procedure](../analyze-requirement/SKILL.md) and retain new evidence under the same task.
Preserve existing source paths and history.

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
   Identify requirement revisions, repository comparison refs, test engine, environment, and available operations.
   Read operation schemas before calling tools.
2. **Understand:** Read exact requirements, design decisions, and expected outcomes.
   Record source authority, revisions, freshness, and conflicting rules.
   Keep unresolved intent separate from implementation defects.
3. **Relate:** Map each behavior to implementation source and concrete test assertions.
   Use the shared [evidence handoff](references/behavior-review.md#keep-one-evidence-handoff) for stable identities, versions, grades, and exact source locators.
   Inspect source at the selected refs, rather than assuming the current checkout matches them.
   A test name or suite listing does not establish assertion coverage.
4. **Analyze:** Identify missing implementation, incomplete assertions, and differences between expected and observed behavior.
   Distinguish business repository unit tests from test-engine E2E verification.
   Record unsupported boundaries and unavailable environments.
5. **Execute:** Run relevant configured verification operations through CLI `call` or MCP `workbench_call`.
   Follow [assertion and execution mapping](references/behavior-review.md#map-assertions-and-execution) for setup, helper chains, predicates, and result bindings.
   Preserve the task scope and existing authorization.
   Retain execution inputs, code revision, environment identity, action IDs, results, and output evidence.
   Follow [case evidence checkpoints](../../../tasks/README.md#save-case-evidence-and-resume-checkpoints) for immediate retention, parallel completions, and interrupted runs.
   For UI end-to-end runs, save key screenshots and attach them to the corresponding investigation.
   Follow the [screenshot evidence rules](../../../docs/BROWSER_INVESTIGATIONS.md#retain-key-screenshots) for checkpoints, scenario bindings, and capture gaps.
6. **Verify:** Compare actual results with each mapped predicate.
   Separate inspected assertions from executed results.
   Distinguish demonstration fixtures and simulations from actual implementation execution.
   Mark unsupported claims and missing evidence as unresolved.

Use this CLI form with discovered resource IDs, operation names, and schema arguments:

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Report behavior, implementation evidence, assertion evidence, execution results, and remaining gaps.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.
Use `VERIFIED` only for stated predicates with retained passing actual execution.
A successful action status or passing command alone does not establish `VERIFIED` behavior.

Phase 1 retains tool actions; complete automated verification remains a future core capability.

## Select the review mode

For an implemented story or PR, follow the shared [review sequence](references/behavior-review.md#coordinate-a-review).
Coordinate requirement extraction, gap analysis, code mapping, assertion mapping, and applicable execution through the existing skills.
Use the [coverage rules](references/behavior-review.md#report-coverage) for scoped numerators and denominators.
Check the [completed handoff](references/behavior-review.md#check-the-handoff) with the applicable artifact and workspace validators.

For later story, code, test, or contract changes, use the [incremental procedure](references/behavior-review.md#check-later-changes).
Preserve earlier records and reassess affected evidence before reusing conclusions.
This procedure runs on demand; recurring checks require separate explicit configuration.

## Bind the assertion chain to the result

Use the [assertion worksheet](../ingest-knowledge/references/evidence.md#assertion-and-execution-worksheet) for consequential behavior claims.
Record fixture, invocation, assertion, mocks, result, revision, environment, and omitted boundaries together.
Follow imported helpers and Robot keywords before interpreting their outcomes.
Keep the tested predicate narrower than the unsupported business behavior.

| Evidence | Permitted conclusion |
| --- | --- |
| Test name or suite listing | A case exists; assertion coverage remains unknown. |
| Inspected setup, call, and assertion | The case asserts that specific predicate. Execution remains unknown. |
| Runner unavailable or setup failure | The business check did not run successfully. |
| Passing result with different source hashes | The result is stale for the selected implementation. |
| Matching controlled source-function result | Those predicates passed with the disclosed transforms and mocks. |
| Matching browser/service execution | Only the retained asserted outcomes passed in that environment. |

Compare every executed source hash with the final implementation commit before reusing a passing result.
The [ingestion harness](../ingest-knowledge/references/workflow.md#harness-commands) can check compatible retained JSON results against Git bytes.
Other result formats still require their actual assertion and revision inspection.
Preserve stale or failed results and record their limits.
Rerun affected checks only when execution is authorized and the required environment exists.

Request counts cannot prove successful renewal.
A displayed logout page cannot prove global revocation.
A maximum wait cannot prove a minimum session lifetime.
A finite fixture cannot prove indefinite execution.
Keep those broader behaviors `NOT_VERIFIED` until adequate matching evidence exists.

## Investigate browser lifecycle failures

For tab inactivity, session expiry, sleep, or resume failures, use the [browser investigation procedure](references/browser-investigation.md).
Record browser settings, observer effects, elapsed time, and service evidence before interpreting a logout screen.
Validate each comparison run before calling it a control.
