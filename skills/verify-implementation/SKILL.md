---
name: verify-implementation
description: Compare approved behavior with exact implementation revisions, inspected assertions, and retained execution evidence.
---

# Verify implementation behavior

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
   Identify requirement revisions, repository comparison refs, test engine, environment, and available operations.
   Read operation schemas before calling tools.
2. **Understand:** Read exact requirements, design decisions, and expected outcomes.
   Record source authority, revisions, freshness, and conflicting rules.
   Keep unresolved intent separate from implementation defects.
3. **Relate:** Map each behavior to implementation source and concrete test assertions.
   Inspect source at the selected refs, rather than assuming the current checkout matches them.
   A test name or suite listing does not establish assertion coverage.
4. **Analyze:** Identify missing implementation, incomplete assertions, and differences between expected and observed behavior.
   Distinguish business repository unit tests from test-engine E2E verification.
   Record unsupported boundaries and unavailable environments.
5. **Execute:** Run relevant configured verification operations through CLI `call` or MCP `workbench_call`.
   Preserve the task scope and existing authorization.
   Retain execution inputs, code revision, environment identity, action IDs, results, and output evidence.
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
