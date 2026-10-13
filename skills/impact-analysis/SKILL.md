---
name: impact-analysis
description: Assess proposed requirement or code changes through source-backed service, repository, symbol, and test relationships.
---

# Analyze change impact

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
   Identify the change, affected capability, comparison refs, and available analysis tools.
   Read operation schemas before calling tools.
2. **Understand:** Read authoritative requirements, design decisions, and exact code revisions.
   Record source authority, freshness, and analysis limits.
   For a proposed requirement, establish intent before deriving technical impact.
3. **Relate:** Follow requirement, service dependency, repository, symbol, caller, and test relationships.
   Preserve source locators and revisions for both ends of each relationship.
   Label static declarations, inferred candidates, and confirmed source links separately.
4. **Analyze:** Identify affected behaviors, interfaces, consumers, data, and verification cases.
   Inspect relevant source and callers at the specified refs.
   Report missing repositories, stale indexes, and unsupported analysis boundaries.
   Do not derive a numerical risk score without a tool that establishes it.
5. **Execute:** Invoke configured analysis operations through CLI `call` or MCP `workbench_call`.
   Preserve the task scope and existing authorization.
   An impact review does not authorize implementation changes by itself.
6. **Verify:** Check each impact claim against its exact supporting sources.
   Retain action IDs and evidence references.
   Separate confirmed effects, possible effects, and unresolved boundaries.

Use this CLI form with discovered resource IDs, operation names, and schema arguments:

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Report affected behaviors, repositories, interfaces, tests, and evidence limits.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.
Static dependencies do not prove runtime execution or deployment.

Phase 1 uses configured tools and agent analysis.
Automatic cross-repository traceability remains a future core capability.
A passing command does not establish `VERIFIED` behavior.
