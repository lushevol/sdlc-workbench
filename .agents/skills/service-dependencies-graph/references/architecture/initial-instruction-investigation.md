# Discover relationships from initial instructions

Use this workflow when repositories appear unrelated or the user supplies architecture hints.
The goal is an integrated, evidence-backed graph, not a separate transcription of those hints.
The agent investigates. The build validates and publishes the saved investigation.
Running the build alone does not perform AI investigation or refresh its conclusions.

## Investigate the starting claims

Preserve the exact input and source under workspace evidence rules.
Read current repository inventories, fingerprints, existing graph coverage, and previous investigations.
Split the input into directed relationship claims, component roles, layer assignments, and explicit exclusions.
Keep the user's vocabulary as search aliases, not proof of identity.

For each claim, search both endpoints and follow their implementation paths.
Inspect callers, imports, exports, API contracts, configuration reads, deployment templates, and persisted routing metadata.
Use the extraction guides for supported React, Spring, data, messaging, and infrastructure syntax.
Trace wrappers and configuration references before matching names or paths across repositories.
Check current source bytes when an earlier report says a dependency is absent.

Expand discovery beyond the initial claims.
Inspect unmatched clients, shared coordinates, remote loaders, configuration bindings, proxies, storage, and message channels.
Search every in-scope repository, including repositories absent from the initial explanation.
Follow newly discovered counterparts until available sources establish the boundary or expose a material evidence gap.
Do not stop after confirming the user's examples.

## Record conclusions

Create version `1.1.0` [architecture context](user-architecture-context.md) from the investigation.
Bind known subjects to exact graph node IDs and preserve unavailable subjects as explicit boundaries.
Give each directed claim an assessment, rationale, exact source ranges, hashes, and actual source revisions.
Record dirty source identities through hashes alongside their repository revision.

| Assessment | Required reasoning |
| --- | --- |
| `SUPPORTED` | Inspected source supports this specific relationship within stated limits. |
| `INFERRED` | Concrete source clues support the relationship, but an identity or binding remains unproved. |
| `CONFLICTED` | Current evidence contradicts the initial claim. Explain both sources and the consequence. |
| `UNVERIFIED` | Available evidence cannot settle the claim. State the missing evidence. |
| `OUT_OF_SCOPE` | Investigation deliberately excludes the required source or boundary. |

Hypotheses guide further searches. They never become facts through repetition or plausible names.
Do not turn a negative search into proof that a dependency does not exist.
Distinguish source-declared calls, provider identity, deployment bindings, and observed runtime execution.
Reuse canonical edges when they establish the same directed relationship.
Add reviewed relationships for supported semantics that current extractors cannot express.
Record conflicting relationships visibly rather than overwriting extracted facts.

## Publish and reconcile

Build the graph with the investigated context.
Inspect the main architecture overview, relationship queries, and selected node neighborhoods.
Check every initial claim and every new discovery against their canonical IDs and source evidence.
Check layer order, library roles, uncertain boundaries, and investigation filters.
Compare the baseline and final relationship coverage using claim dispositions, not inflated node counts.
Keep source changes visible. Reinvestigate stale conclusions before updating their hashes.
Report remaining evidence gaps with their next action and owner, where known.
