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
   Use the [canonical graph skill](../service-dependencies-graph/SKILL.md) for static cross-repository discovery.
   Check snapshot coverage, source fingerprints, and revisions before interpreting graph links.
   Inspect the coverage operation's `CURRENT`, `STALE`, or `UNKNOWN` freshness result and its limits.
4. **Analyze:** Identify affected behaviors, interfaces, consumers, data, and verification cases.
   Inspect relevant source and callers at the specified refs.
   Use [implementation mapping](../verify-implementation/references/behavior-review.md#map-implementation) for a story diff or PR.
   Inspect relevant unchanged paths before declaring a behavior unimplemented.
   Preserve behavior IDs and grades from the shared handoff.
   Record unexplained edits separately from supported maintenance rationale.
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

For the configured graph resource, begin with:

```sh
ai-sdlc --workspace PATH call service-dependencies coverage --args '{}'
ai-sdlc --workspace PATH call service-dependencies relationships --args '{}'
```

If the snapshot is missing or stale for the question, run the Workbench build adapter:

```sh
ai-sdlc --workspace PATH graph build
```

The adapter invokes the canonical skill implementation.
Keep graph enhancements and extraction regressions inside that skill.
Initialization ships the skill helpers with generated workspaces.

Use advertised `search` and `neighborhood` operation schemas to inspect relevant nodes and evidence.
The graph provider does not perform repository diffs or complete requirement-to-test tracing.
It has no semantic impact operation.
Select exact comparison refs in each independent repository and inspect its callers directly.
Keep unknown upstreams, dynamic routes, build dependencies, and missing repositories explicit.
Missing edges do not establish no impact.

Phase 1 uses configured tools and agent analysis.
Complete cross-repository traceability remains a future core capability.
A passing command does not establish `VERIFIED` behavior.
