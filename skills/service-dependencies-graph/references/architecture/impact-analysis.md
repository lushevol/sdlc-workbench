# Impact analysis with graph evidence

Use the same canonical snapshot for planning and code review.
Call `coverage` before interpreting relationships.
Record snapshot identity, repository revisions, source fingerprints, and missing scope.
Inspect the returned `CURRENT`, `STALE`, or `UNKNOWN` freshness result and its evidence limits.

## Requirement to source

Read cited requirements and decisions before deriving intent.
Separate approved intent, candidate knowledge, implementation behavior, and graph descriptions.
Search concrete business nouns, actions, interface paths, and repository names.
Use returned node IDs with `neighborhood` to inspect relevant edges.

Inspect source evidence for each proposed relationship.
Semantic matches identify candidates and cannot approve business requirements.

When authoritative context is absent, state the missing decision and its owner.
Mark unknown owners explicitly.
Continue independent analysis that does not require that decision.

## Code to dependencies

Select each independent repository and exact base/head revisions.
For uncommitted changes, record worktree state and analyzed source fingerprints.
Never substitute the Workbench repository for a business repository.
Map changed paths to graph `source_paths`, then inspect public interfaces, consumers, data access, and message boundaries.

Exact paths take precedence over broad wildcard matches.

Incoming dependency edges can identify affected consumers.
Containment supplies navigation context.
Outgoing reads and dependencies do not make their other callers affected.
Build dependencies identify declared consumers and do not establish runtime invocation.

Unresolved boundaries remain unresolved during traversal.
Read source before assigning impact to a path discovered through broad graph grouping.

Use `search`, `relationships`, and `neighborhood` through registered CLI or MCP operations.
The graph provider does not perform repository diffs or complete requirement-to-test tracing.
It has no semantic impact operation.
Use direct Git and source inspection for exact changes and callers.

Use an owning repository's index only when it is available and current.

## Reporting

Report direct effects, possible indirect effects, context, candidates, and unresolved boundaries separately.
Include affected repositories, public interfaces, source evidence, and relevant test assertions.
State traversal limits and unexamined repositories.
A missing graph edge does not establish no impact.

A successful analysis command does not establish passing behavior.

Follow the shared `impact-analysis` skill for retained actions and report review metadata.
