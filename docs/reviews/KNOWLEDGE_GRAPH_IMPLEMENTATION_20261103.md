# Knowledge graph implementation

**Completed: Workbench now builds a local knowledge graph with evidence, lifecycle filters, reverse references, bounded paths, and a viewer.**

No critical conclusions require user attention or action.

## Scope and authorization

The [continuation input](../evidence/knowledge-mechanism-review-20261103/user-input.md#exact-continuation-input) authorizes this implementation.
The [solution review](KNOWLEDGE_GRAPH_SOLUTION_20261103.md) defines the proposed first delivery.
This is Workbench harness maintenance, started 3 November and completed 4 November 2026.

## Affected scope and risk

Extend the canonical graph skill's schema, projection, snapshot queries, and viewer.
Inspection covered builder, validation, snapshot comparison, CLI/MCP adapters, and package consumers before interface changes.
Qualitative risk: medium. Existing graph snapshots and source evidence need compatible read behavior.
Use deterministic projections, exact identities, bounded paths, and visible lifecycle and freshness limits.
Preserve unrelated README changes and the untracked release-report directory.

## Delivered behavior

The [knowledge graph guide](../../.agents/skills/service-dependencies-graph/references/architecture/knowledge-graph.md) defines inputs, identities, relationships, commands, and limits.
The existing graph skill owns the implementation.
CLI and MCP retain their shared resource adapter.
Generator `2.3.0` adds an optional knowledge extension within graph schema `2.0.0`.
Legacy snapshots remain readable.

The projection connects knowledge versions, exact source revisions, catalogs, criteria, governance events, and behavior-review declarations.
Original lifecycle states, evidence classes, baseline grades, endpoint bindings, and execution limits remain separate.
Missing and ambiguous targets remain unresolved.
Raw source, assertion, command, and result bodies remain outside the graph.
Authoritative knowledge remains in its existing Markdown and YAML records.

The `knowledge` operation filters projected identities.
The `references` operation returns direct incoming or outgoing references.
The `paths` operation follows bounded declared relationships and retains canonical arrow direction.
Lifecycle filtering also applies to intermediate path records.
Truncation reasons identify traversal, depth, and result limits.

The viewer provides separate Knowledge and Architecture tabs.
Complete record and relationship lists use pagination.
Knowledge navigation does not enter architecture dependency or API counts.
Inspectors expose exact versions, hashes, source links, lifecycle, and original evidence grades.

Publication compares repository, architecture context, and knowledge inputs before replacing the saved bundle.
Changed inputs abort publication and preserve the previous bundle.
Coverage and snapshot comparison expose knowledge freshness separately from repository freshness.
No new package, database, server, LLM, API key, or startup download is required.

## Current workspace result

The [retained build log](../evidence/knowledge-mechanism-review-20261103/implementation/workspace-build.log) records successful graph generation and validation.
The [query checks](../evidence/knowledge-mechanism-review-20261103/implementation/workspace-query-checks.json) retain snapshot hashes, action IDs, assertions, and freshness.

| Measure | Result |
| --- | --- |
| Repository census | Nine repositories. |
| Combined graph | 7,368 nodes, 19,002 edges, and 18,634 evidence records. |
| Knowledge projection | 827 nodes, 1,088 edges, and 552 fingerprinted inputs. |
| Canonical domain records | 12 candidates; zero published records. |
| Unresolved knowledge references | 83 explicit nodes. Historical and unavailable targets remain visible. |
| Checked local freshness | Repository and knowledge inputs are `CURRENT` at validation time. |

Checks exercised candidate search, published-only filtering, outgoing references, an exact citation path, source backlinks, and coverage.
A citation path establishes a retained declaration. It does not establish semantic support or business approval.
The current graph cannot supply published intent where no publication exists.

Stale architecture evidence initially blocked the build.
The [source refresh](../evidence/knowledge-mechanism-review-20261103/implementation/architecture-context-refresh.md) records bounded review of eight changed files.
All 46 cited files now match their hashes.
All 23 relationship assessments retain their previous status.
The preserved context and instructions support comparison.
This refresh changes no business intent or application source.

## Validation and remaining limits

The [validation record](../evidence/knowledge-mechanism-review-20261103/implementation/validation.json) indexes commands, counts, logs, and evidence hashes.

| Check | Result |
| --- | --- |
| Full runtime suite, including installed optional Node checks | 883 passed; zero failures, errors, or skips. |
| Full graph skill suite | 213 passed; zero failures, errors, or skips. |
| Focused knowledge suite | 31 passed. Included in broader suites where discovered. |
| Wheel build | Passed with installed build tools and `--no-build-isolation`. |
| Installed wheel and generated workspace | Passed package-origin, asset, initialization, validation, empty-build, and copied-query checks. |
| Actual workspace graph | Build, schema, semantic validation, checksums, six query cases, and freshness checks passed. |

The [installed wheel check](../evidence/knowledge-mechanism-review-20261103/implementation/installed-wheel-check.json) used a clean directory outside this checkout.
It reused the existing dependency environment.
Generated workspaces received the new modules, schema, and guide without copied runtime source or live graph outputs.
Tests also check unsafe paths, metadata tampering, candidate filtering, and atomic publication after source changes.

The [initial check record](../evidence/knowledge-mechanism-review-20261103/implementation/initial-checks-and-corrections.json) preserves failures, corrections, and unavailable checks.
CLI integration exposed enum schemas without explicit string types.
The correction and regression protect provider loading and all three granted query operations.
Snapshot review exposed omitted knowledge freshness in comparison results.
Its [regression evidence](../evidence/knowledge-mechanism-review-20261103/graph/local/snapshot-comparison-freshness-check.json) preserves that correction.

Browser policy blocked opening the local HTML file for visual inspection.
Viewer interaction, escaping, pagination, filtering, and architecture isolation passed automated checks.
Visual layout review remains incomplete.
Connected package downloads and Windows execution remain untested.
No comparative database benchmark, LLM extraction evaluation, or production behavior verification occurred.
The [documentation checks](../evidence/knowledge-mechanism-review-20261103/implementation/document-checks.json) passed 202 local links across 12 files, plus fence, prose-length, and whitespace checks.

The [original recommendation](KNOWLEDGE_GRAPH_SOLUTION_20261103.md) remains applicable.
Evaluate useful project questions before adding SQLite indexing, a graph service, or LLM extraction.
Improving source review and publication can improve the current corpus without another knowledge platform.

## Checks and writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
