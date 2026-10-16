---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Static source dependencies do not establish runtime execution or deployment.
  - Diagram exports do not establish browser layout quality.
---

# Architecture trace delivery

Date: 16 October 2026.
Implementation status: COMPLETE.
The user requested a plan and implementation after rejecting record counts as evidence of useful graph improvement.

## Scope and risk

The graph skill owns extraction, trace projections, viewer behavior, regressions, and supporting guides.
Business repositories and Workbench runtime interfaces retain their current responsibilities.
Unrelated working changes remain outside this stage.
No parent runtime becomes a standalone dependency.

The qualitative risk is high for method identity and provider matching.
Incorrect joins can invent API paths or selected runtime implementations.
Focused negative regressions check ambiguity, deferred callbacks, unscoped declarations, and dynamic gateway identities.
The presentation risk is medium because large dependency sets require readable pagination and complete indexes.

## Plan

1. Preserve the baseline graph and inspect current callers, projections, and exact business source.
2. Preserve Java method callsites, handler declarations, helper calls, and configuration or HTTP caller context.
3. Extract supported imported frontend HTTP wrappers with consumer and wrapper evidence.
4. Add bounded API and client traces with explicit method, implementation, declaration, and class context.
5. Add architecture cards, semantic role columns, complete labels, and directed routes.
6. Run focused regressions, full required checks, graph builds, and independent source review.
7. Compare the baseline, latest local graph, and parent graph with retained visual evidence.
8. Review the complete staged diff and commit the completed stage.

## Confirmed defects

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Class aggregation overwrites method details. | `Graph.add_edge` and Java `CALLS_COMPONENT` construction | API traces cannot distinguish calls from different controller methods. | Skill maintainer; person UNKNOWN | Retain caller-specific callsites and test method selection. |
| Same-class helper calls disappear. | Java receiver extraction skips implicit receivers. | API paths stop before supported internal helper behavior. | Skill maintainer; person UNKNOWN | Extract uniquely declared local helper calls. |
| Imported wrappers hide frontend HTTP calls. | Base UI service imports and inspected HTTP forwarding functions | Login, logout, and validation calls remain absent. | Skill maintainer; person UNKNOWN | Add bounded wrapper summaries with supporting source evidence. |
| Existing rendering clips identity. | Retained configuration comparison pictures | Users cannot distinguish common-prefix keys or follow overlapping links. | Skill maintainer; person UNKNOWN | Wrap complete names and route labelled arrows through separate gutters. |
| Confirmed repository joins remain limited by missing providers. | Parent source census and templated gateway upstream | More declarations cannot justify additional resolved service links. | Workspace maintainer; person UNKNOWN | Expose available detail and identify missing provider evidence. |

## Acceptance criteria

```gherkin
Scenario: Distinguish controller methods
  Given two API handlers call different methods on one declared dependency
  When the user selects either API trace
  Then the trace retains only that handler's direct callsites as method paths
  And deferred callbacks remain separate declaration context

Scenario: Follow a supported helper
  Given a handler invokes one uniquely declared local helper
  When the skill builds the trace
  Then the helper call retains its caller and target declaration locations
  And equal-arity ambiguous overloads do not establish an exact target

Scenario: Inspect an implementation alternative
  Given a controller calls a service interface
  And source declares an implementation of that interface
  When the user inspects the API trace
  Then the graph shows the implementation as an unselected alternative
  And related repository mappings remain declaration context

Scenario: Discover imported frontend calls
  Given the base UI imports inspected HTTP forwarding functions
  When the skill extracts its service source
  Then login, logout, and validation calls retain consumer and wrapper evidence
  And a templated gateway upstream does not establish a resolved provider

Scenario: Read configuration identities
  Given selected configuration keys exceed 27 characters
  When the viewer draws their dependency diagram
  Then each complete name appears across wrapped text lines
  And every rendered relationship retains a direction and label

Scenario: Reach detail from the architecture overview
  Given the snapshot contains provided APIs, configuration, storage, and unknown boundaries
  When the user opens the overview
  Then repository cards expose those categories
  And category controls open the corresponding complete repository indexes

Scenario: Retain trace limits
  Given a trace exceeds six hops or its node or relationship budget
  When the viewer projects the trace
  Then the limit record retains omitted canonical edge IDs
  And the complete canonical indexes remain available
```

## Validation and evidence

Validation status: PASSED.

The skill suite passed 145 tests.
The Workbench runtime suite passed 312 tests.
The skill quick validator passed.
The local graph validator passed with 6,564 nodes and 17,057 edges.
The rebuilt parent graph validator passed with 10,722 nodes and 26,763 edges.
The package smoke test passed after wheel extraction and workspace initialization.
The offline wheel build passed.

The local updated graph contains 163 trace entries.
It contains 41 provided API traces.
Thirty-five provided API traces contain method-path calls.
The graph retains 1,138 Java callsites and 40 SQL method sites.
The parent updated graph contains 149 provided API traces with method-path calls and 21,390 Java callsites.

Comparison artifacts are stored in [service-dependencies-trace-comparison-20261016](../evidence/service-dependencies-trace-comparison-20261016/README.md).
The focused export traces `POST /v1/fmo/admin/tile/data` through its handler, service, repository, and selected SQL methods.
The trace retains explicit implementation alternatives, deferred boundaries, and traversal omissions.

The source inventories differ between local and parent snapshots.
Ten parent backend repositories are absent from the local inventory comparison.
Static source extraction does not prove deployment, runtime dispatch, or executed database access.
SVG exports do not establish browser layout quality.
The ASD-STE100 review remains pending.
