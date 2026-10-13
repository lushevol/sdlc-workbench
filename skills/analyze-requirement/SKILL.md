---
name: analyze-requirement
description: Analyze requirement intent, source quality, and acceptance criteria before implementation or impact analysis.
---

# Analyze a requirement

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
   Select relevant capabilities, knowledge resources, repositories, and tool operations.
   Read each operation schema before calling it.
2. **Understand:** Read exact requirement, acceptance criteria, design, and decision sources.
   Record source locators, revisions, authority, and freshness.
   Separate approved intent from drafts, current implementation, and inferred behavior.
3. **Relate:** Map each expected behavior to business capabilities and relevant services.
   Attach source references to each relationship.
   Mark candidate links and missing evidence explicitly.
4. **Analyze:** Identify conflicting rules, missing conditions, unclear outcomes, and acceptance criteria that tests cannot evaluate.
   A search miss does not prove that a rule does not exist.
   Request an owner decision only when available evidence cannot resolve a material ambiguity.
5. **Execute:** Invoke relevant configured operations through CLI `call` or MCP `workbench_call`.
   Preserve the task scope and existing authorization.
   Continue independent work when a missing decision blocks only part of the analysis.
6. **Verify:** Check that every behavior has a source and a testable expected result.
   Retain action IDs and evidence references.
   State confirmed facts, inferences, and unresolved questions separately.

Use this CLI form with discovered resource IDs, operation names, and schema arguments:

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Report the behavior baseline and remaining requirement gaps.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.

Phase 1 uses agent reasoning and existing tool execution.
Automated governance and complete behavior verification remain future core capabilities.
A passing command does not establish `VERIFIED` behavior.
