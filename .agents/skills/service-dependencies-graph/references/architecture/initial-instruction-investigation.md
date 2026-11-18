# Discover relationships from source

Use this workflow to discover, complete, or audit dependency relationships, with or without human architecture hints.
The agent discovers relationships from available sources. Users do not need to enumerate services, endpoints, or expected edges.
The goal is an integrated, evidence-backed graph with explicit limits for evidence unavailable in the selected scope.
The agent investigates. The build validates and publishes the saved investigation.
Running the build alone does not perform AI investigation or refresh its conclusions.
Prioritize internal and external service calls: caller, operation, destination, transport, and receiving endpoint.
Use [snippet discovery](snippet-discovery.md) to collect broad candidates and connect them through AI source investigation.

## Establish the source boundary

Read registered locations, local mappings, repository census, fingerprints, coverage, and previous investigations.
Include every in-scope repository, including disconnected repositories and sources with inventory-only extraction.
Record missing repositories, excluded files, unsupported stacks, parse failures, and unknown source revisions.
Use `--repos PATH --layout flat` when every immediate directory contains one repository.
Read discovery file dispositions separately from typed parser source coverage.
Search text independently of source-root names, language classifications, and known graph neighbors.
Build a source-only baseline before using saved architecture claims as discovery answers.
Use `build --no-context --out .workbench/graph-source-baseline` for isolated extraction without saved architecture claims.
Do not delete the current context or modify the published bundle to obtain that baseline.

Read optional `relationships/service-dependencies/initial-instructions.md` when present. Its absence does not block discovery.
Preserve its current bytes as dated evidence before editing. Keep earlier snapshots unchanged.
Treat its claims and earlier context as hypotheses and regression expectations, separate from independently discovered declarations.
Keep human vocabulary as search aliases. Names do not prove component identity or the completeness of the source scope.

## Discover and close extraction gaps

Plan the source review by repository, file group, and dependency family before semantic investigation.
Reuse the task record, coverage audit, declaration ledger, and context contract. Do not create another graph state machine.
Inspect all supported boundary families: APIs, composition, shared code, configuration, routing, messaging, data, and external clients.
Read the [source audit](dependency-audit.md) for concrete syntax and the [extraction map](../../SKILL.md#dependency-extraction-map) for current limits.
Inspect independent pattern candidates and source gaps, not only already extracted nodes.
Group repeated declarations when their scope and disposition remain traceable. Sampling alone cannot establish complete family coverage.
Same-line marker accountability does not establish semantic extraction or a provider join.

For each dependency declaration, inspect its enclosing code, imports, wrapper, configuration reads, and available provider identity.
Follow both endpoints across repository boundaries, including persisted routing metadata and deployment templates when available.
Discover endpoints from clients and providers independently. Do not restrict searches to user-supplied names or known graph neighbors.
Keep library reuse, logical API contracts, transport routes, and runtime deployment bindings separate.
Record an extracted edge, a candidate with its unresolved binding, or an explicit source coverage gap.
Do not silently drop unsupported syntax or turn missing identity into an invented provider.

When source proves a missed declaration, fix the owning extractor or resolver and add a focused regression.
Use reviewed context for supported semantics the current graph cannot express, with exact source citations and stated limits.
Rebuild after repairs, compare source declarations with canonical evidence, and investigate newly exposed boundaries.
Repeat until reviewed source scope has a disposition and no repairable gap remains within the authorized scope.
Record unfinished files and families explicitly if work cannot complete. Candidate counts alone do not establish closure.

Then compare optional human expectations with the independent result.
For each missing expected edge, identify the cause: omitted source, unsupported syntax, lost data flow, ambiguous identity, or unavailable binding.
Add a reusable regression when source evidence supports a repair. Retain contradicted and unavailable expectations with their rationale.
Do not ask the user to enumerate missing relationships when accessible source can resolve them.

## Record conclusions

Create version `1.1.0` [architecture context](user-architecture-context.md) from the investigation.
Bind known subjects to exact graph node IDs and preserve unavailable subjects as explicit boundaries.
Use `SOURCE_REVIEWED` subjects with source-review evidence for independently inspected components.
Reserve `USER_REPORTED` for supplied claims. The subject status does not select a runtime provider.
Give each directed claim an assessment, rationale, exact source ranges, hashes, and actual source revisions.
Record dirty source identities through hashes alongside their repository revision.

| Assessment | Required reasoning |
| --- | --- |
| `SUPPORTED` | Inspected source supports this specific relationship within stated limits. |
| `INFERRED` | Concrete source clues support the relationship, but an identity or binding remains unproved. |
| `CONFLICTED` | Current evidence contradicts the initial claim. Explain both sources and the consequence. |
| `UNVERIFIED` | Available evidence cannot settle the claim. State the missing evidence. |
| `OUT_OF_SCOPE` | Investigation deliberately excludes the required source or boundary. |

Source citations must establish source-only findings without depending on a human explanation of the expected edge.
Hypotheses guide further searches. They never become facts through repetition or plausible names.
Do not turn a negative search into proof that a dependency does not exist.
Distinguish source-declared calls, provider identity, deployment bindings, and observed runtime execution.
Reuse canonical edges when they establish the same directed relationship.
Add reviewed relationships for supported semantics that current extractors cannot express.
Record conflicting relationships visibly rather than overwriting extracted facts.

## Publish and reconcile

Build the graph with the investigated context.
Inspect the main architecture overview, relationship queries, and selected node neighborhoods.
Check independently discovered declarations and optional expected claims against their canonical IDs and source evidence.
Check layer order, library roles, uncertain boundaries, and investigation filters.
Compare source-only baseline and final relationship coverage using reviewed declaration dispositions, not inflated node counts.
State reviewed repositories, file groups, dependency families, unresolved identities, and excluded or unavailable evidence.
Keep source changes visible. Reinvestigate stale conclusions before updating their hashes.
Report remaining evidence gaps with their next action and owner, where known.
Completion applies to the inspected source boundary. Static analysis cannot prove all relationships across unavailable code or runtime configuration.
