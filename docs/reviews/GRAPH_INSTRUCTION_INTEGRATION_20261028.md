# Initial instruction integration into dependency graphs

No critical conclusions require user attention or action.

High-priority intent: [exact user input](../evidence/graph-instruction-integration-20261028/user-input-20261028.txt), 28 October 2026.

The user wants initial instructions to guide investigation and enrich the final relationship graph.
Those instructions can be incomplete, outdated, or incorrect.
This work updates the reusable skill and applies that workflow to the current repositories.

## Result

The main graph now includes all 23 investigated relationships.
Seventeen have source support. One remains inferred. Three remain unverified. Two remain outside scope.
The investigation adds six relationships beyond the initial explanation.
Four existing canonical edges retain their identities. Nineteen reviewed edges represent additional relationships and explicit boundaries.
The main diagram shows four ordered MFE layers.
The original instructions remain available below the graph in a collapsed evidence section.

The [applied context](../../relationships/service-dependencies/architecture-context.json) retains 46 source identities and 18 architectural subjects.
The [investigation evidence](../evidence/graph-instruction-integration-20261028/relationship-investigation.json) retains revisions, hashes, source ranges, and dirty states.
The [verification receipt](../evidence/graph-instruction-integration-20261028/final-verification.json) binds the generated graph and manifest checksums.

## Reusable workflow

The [skill](../../.agents/skills/service-dependencies-graph/SKILL.md) now directs agents through source investigation before final generation.
The [procedure](../../.agents/skills/service-dependencies-graph/references/architecture/initial-instruction-investigation.md) treats user instructions as search seeds.
It requires discovery beyond those seeds and reconciliation against current sources.

The [context contract](../../.agents/skills/service-dependencies-graph/references/architecture/user-architecture-context.md) records each investigation conclusion and supporting citations.
Source-supported claims require code evidence for each bound repository endpoint.
A user statement alone cannot create a confirmed relationship.
Structural checks do not replace the agent's source interpretation.

Existing source edges receive investigation metadata without losing their assertion or resolution states.
New reviewed edges retain their specific relationship kind, rationale, evidence, and uncertainty.
Provider matching stays separate from investigation assessments.
The relationship query includes inbound and unbound architectural relationships.

The viewer filters investigation results and evidence origin independently from provider status.
Its inspector shows source ranges, revisions, hashes, and investigation reasoning.
Its layer lanes distinguish Root Config, Base, Container, and Tile.
The SDK displays its library role. Its original generic canonical classifier remains available in the inspector.

## Source findings

| Finding | Consequence | Owner and next action |
| --- | --- | --- |
| Root Config registers Base. Container loads the Cashflow tile. | The graph connects these MFE layers with source support. | Skill maintainer: retain exact references during regeneration. |
| Base selects its container through runtime properties. | The specific Base-to-RATAN-container link remains inferred. | Deployment owner unknown: inspect active routing data when required. |
| Nginx templates contain gateway routes and direct service exceptions. | The graph includes query-service and data-ambassador boundaries. | Deployment owner unknown: supply rendered upstreams for deployment claims. |
| Current Auth source implements EMS3 delegation. | The older absence finding cannot describe current sources. | Skill maintainer: retain the current implementation references. |
| BFF implements Entra token exchange and separate EMS3 calls. | These dependencies appear independently from Auth delegation. | Skill maintainer: keep Entra identity-platform exchange separate from reported SPN authentication. |
| SDK validates the BFF token issuer contract. | The graph represents a token contract, without claiming an SDK HTTP call. | Skill maintainer: preserve the library role and relationship kind. |

The investigation evidence links the exact source observations for these findings.
API Gateway implementation remains excluded under the user's stated boundary.
DNS, effective gateway routes, and active deployment bindings remain unverified.
No runtime execution or business acceptance is claimed.

## Comparison against current raw extraction

Both columns use the same current repository sources.
Counts from older graphs also reflect source changes, so they cannot measure this enhancement alone.

| Dimension | Raw extraction | Extraction with investigated context |
| --- | ---: | ---: |
| Repositories | 9 | 9 |
| Nodes | 6,497 | 6,507 |
| Edges | 17,799 | 17,818 |
| Evidence records | 17,813 | 17,981 |
| Initial and discovered claims with explicit dispositions | 0 | 23 |
| Reused canonical edges annotated | 0 | 4 |
| Added reviewed relationships | 0 | 19 |

Current interceptor changes invalidate eight old BFF canonical edge references.
The extractor reports `UNINSPECTED_REQUEST_INTERCEPTOR` for those request paths.
Source inspection supports the logical Base-to-BFF contract, while the extractor cannot resolve its transport path.
The integrated relationship preserves this distinction.
The [first failed build](../evidence/graph-instruction-integration-20261028/build.log) records rejection of a stale edge reference.
The [published build](../evidence/graph-instruction-integration-20261028/build-published.log) records successful reconstruction against current references.

## Scope and risk

Changes remain inside the graph skill, project context, and maintenance evidence.
No business repository implementation changed.
The pre-existing untracked `core/release-report/` directory remains outside this change.

Risk is moderate because canonical enrichment affects projections, snapshot queries, and viewer aggregation.
Source inspection covered the build pipeline, graph collections, projections, snapshot readers, viewer model, and renderer callers.
Regressions cover provenance, stale evidence, endpoint bindings, preserved source facts, external boundaries, filters, and mixed assessments.
Version `1.0.0` retains its previous annotation behavior.

## Validation

The [skill suite](../evidence/graph-instruction-integration-20261028/skill-tests-final.log) passes 163 tests.
The [Workbench suite](../evidence/graph-instruction-integration-20261028/workbench-tests-final.log) executes 660 tests with zero failures or errors.
Its two optional native connector checks remain skipped.
The initial sandbox run could not bind local mock servers.
The complete suite then ran with local socket access and unchanged assertions.

The graph build, semantic validation, source freshness, context freshness, and relationship reconciliation pass.
The [rendered-script probe](../evidence/graph-instruction-integration-20261028/generated-viewer-probe.log) checks all 23 claims in the main graph.
It also checks layer lanes, investigation filters, and the evidence inspector.
The existing local-file browser security rejection remains respected.
Visual layout review remains unavailable; DOM checks do not establish visual quality.

The [wheel build](../evidence/graph-instruction-integration-20261028/wheel-build-final.log) uses installed build dependencies without network downloads.
The initial isolated build could not download setuptools through the sandbox.
The [wheel smoke](../evidence/graph-instruction-integration-20261028/wheel-smoke.json) checks an isolated wheel extraction and fresh workspace.
It verifies shipped investigation resources and executes the shipped architecture integration tests.
Only macOS with existing Python dependencies was tested.
The [workspace validator](../evidence/graph-instruction-integration-20261028/workspace-validation.json) and [skill validator](../evidence/graph-instruction-integration-20261028/skill-validation.log) pass.

## Editable instruction entry point, 28 October 2026

High-priority source: [exact user question](../evidence/graph-instruction-integration-20261028/user-input-instruction-location-20261028.txt).

The user can edit [initial-instructions.md](../../relationships/service-dependencies/initial-instructions.md) when adding repositories or correcting architecture hints.
The skill reads these notes before graph generation and directs source investigation when they change.
The agent maintains the reviewed JSON context. A build command alone does not investigate the Markdown notes.
The historical architecture source remains unchanged.

Scope is limited to documentation and skill instructions. Risk is low because runtime interfaces and generated artifacts remain unchanged.
The affected consumers are the skill entry point, investigation workflow, and relationship guide.
The [validation receipt](../evidence/graph-instruction-integration-20261028/instruction-entry-validation.json) records passing link, skill, workspace, and diff checks.
Runtime code and generated artifacts remain unchanged. Runtime tests and graph regeneration were outside this documentation stage.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
