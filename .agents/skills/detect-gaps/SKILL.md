---
name: detect-gaps
description: Find material knowledge, relationship, implementation, and verification gaps within a stated SDLC analysis scope.
---

# Detect SDLC gaps

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
   Define the capability, artifacts, repository refs, environment, and gap categories under review.
   Read operation schemas before calling tools.
2. **Understand:** Read relevant requirement, design, decision, implementation, and test sources.
   Check source authority, freshness, completeness, and conflicts.
   Do not treat generated summaries as approval for a business rule.
3. **Relate:** Trace expected behaviors through service, code, assertion, and execution evidence.
   Record source locators, revisions, and relationship evidence.
   Separate confirmed links, inferred links, and missing links.
4. **Analyze:** Distinguish missing intent, unclear intent, missing implementation, assertion gaps, and missing execution evidence.
   Use the shared [gap categories](../verify-implementation/references/behavior-review.md#classify-gaps) for requirement, implementation, and test reviews.
   Bind findings to stable behavior IDs and versions in the [evidence handoff](../verify-implementation/references/behavior-review.md#keep-one-evidence-handoff).
   Inspect relevant unchanged implementation before declaring a defect.
   Distinguish missing scenarios, weak assertions, unrun checks, failed execution, stale results, and insufficient verification levels.
   Distinguish a demonstrated absence from an unsuccessful search.
   State tool coverage limits with each affected conclusion.
5. **Execute:** Invoke relevant configured inspection or verification operations through CLI `call` or MCP `workbench_call`.
   Preserve the task scope and existing authorization.
   Do not create substitute business rules to complete a mapping.
6. **Verify:** Check each finding against inspected source or a documented evidence limit.
   Retain action IDs and evidence references.
   State confirmed facts, inferences, and unresolved questions separately.

Use this CLI form with discovered resource IDs, operation names, and schema arguments:

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Report gaps by behavior and evidence boundary.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.
Prioritize findings by the stated business consequence and available evidence.
Use declared inventories and [coverage denominators](../verify-implementation/references/behavior-review.md#report-coverage) when reporting gap rates.

Phase 1 uses agent analysis and retained tool actions.
Automatic knowledge governance and complete evidence validation remain future core capabilities.
A passing command does not establish `VERIFIED` behavior.
