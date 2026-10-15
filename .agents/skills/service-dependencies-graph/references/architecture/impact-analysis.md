# Bidirectional impact analysis

Use one canonical snapshot for planning and regression review.
Check coverage, freshness, source revisions, and fingerprints before interpreting impact.
The graph supplies candidate architecture paths and supported static links.
It does not establish approved intent, complete function reuse, or verified business behavior.

## Requirement to source

Read cited requirements and decisions before deriving intent.
Normalize the requirement into concrete business nouns and actions.
Search capability, page, application, service, component, and interface evidence.
Inspect relevant neighborhoods in both business and runtime dimensions.

Treat semantic matches as candidates until authoritative sources corroborate them.
Prioritize direct source matches, public interfaces, persisted data, and unresolved boundaries for investigation.
Priority here describes review order and does not establish business criticality.
When context is missing, state the needed decision and its owner.

## Code to dependencies

Select exact base/head revisions in each independent business repository.
For worktree changes, record dirty state and analyzed source fingerprints.
Map changed paths to canonical `source_paths`, including documented wildcards.
Exact paths take precedence over ancestor wildcard matches.

Inspect changed interfaces, incoming consumers, data access, message boundaries, and test assertions.
Incoming dependency edges can identify affected consumers.
Containment supplies navigation context.
Outgoing dependencies do not make their other callers affected.

Build dependencies identify declared consumers without proving runtime invocation.
Module imports establish source module relationships without compiler or bundler proof.
Unresolved boundaries remain unresolved during traversal.
Missing or unexamined repositories remain limitations, not unaffected results.

## Supported commands and integrations

Use the skill runner's coverage, relationships, search, services, and neighborhood queries.
Read query help for actual operation schemas.
The current query interface does not perform repository diffs or semantic impact traversal.
Use direct Git and source inspection for exact changes and callers.

Original advanced impact and dedicated MCP wrappers required the source project's external runtime.
Do not invoke them until they are adapted and validated inside this skill.
The optional Workbench adapter exposes the same supported snapshot queries.
An owning repository's usable index can supplement exact symbol inspection.

Never substitute the Workbench commit or an unrelated repository index for business source evidence.
Do not invent index scores, source authority, or approvals.
This procedure requires no external knowledge service.

## Reporting

Report direct effects, possible indirect effects, context, candidates, and unresolved boundaries separately.
Include changed scope, affected repositories, public interfaces, source evidence, and relevant test assertions.
State traversal limits and unexamined repositories.
A missing graph edge does not establish no impact.

Give each finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Keep automated checks and ASD review separate under the skill's report instructions.
