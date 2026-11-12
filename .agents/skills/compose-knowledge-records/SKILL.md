---
name: compose-knowledge-records
description: Compose connected domain knowledge candidates and navigation from supported intent claims using Workbench schemas and templates.
---

# Compose knowledge records

## Inputs

Use supported intent claims, exact retained source revisions, current selections, applicability findings, and recorded unknowns.
Confirm authorization to write candidates. A document review produces findings and a topic proposal without governed writes.
Use the [knowledge contract](../../../knowledge/README.md), [schemas and templates](../../../core/knowledge/README.md).

## Select and compose

| Type | Purpose |
| --- | --- |
| `KnowledgeTopic` | Domain terms, intended workflows, and target-rule context. |
| `Architecture` | Intended components, responsibilities, interfaces, and dependencies. |
| `Requirement` | Confirmed intended behavior with measurable acceptance criteria. |
| `Decision` | An actual choice, alternatives, rationale, and consequences. |
| `RepositoryProfile` | Intended repository responsibilities and contracts. |
| `GovernanceFinding` | A consequential unresolved issue; stored outside domain knowledge. |

1. Use the selected shipped template and its schema.
   Group by project question; one source can support several topics and several sources can support one topic.
2. Preserve source revision, hash, original ranges, purpose, authority, uncertainty, and intended applicability beside claims.
   A filtered view supplies convenient input; citations still bind to original retained sources.
3. Save new domain drafts under `knowledge/candidates/<classification>/` with stable IDs.
   Use `governance_state: candidate`, `status: draft`, and `verified: []` until actual review changes the state.
   Mark an unavailable owner `unknown`.
4. Reuse unchanged records. Increment the version when content or scope changes.
   Preserve unresolved predecessors and findings; do not overwrite their history to hide conflicts.
   Reconcile the plan's affected closure, including former dependents of withdrawn claims.
   Record supported no-change outcomes separately; do not rewrite records only to advance an observed source hash.
5. Create or update `knowledge/candidates/index.md` with topic purpose, state, links, and evidence limits.
   Keep reusable `knowledge/index.md` free from live project records.
6. Use declared registry IDs only for inspected relationships.
   Declarations do not establish runtime integration or execution permission.

Knowledge describes requirements, intent, and ideal target behavior.
Retain domain rules, contracts, decisions, and intended business-system architecture.
Exclude Workbench maintenance, raw sources, code copies, fixtures, execution results, reports, and intermediate files from canonical knowledge.
Keep implementation facts, deployment status, observations, and conformance results outside canonical intent.
Store `GovernanceFinding` records under `evidence/knowledge/findings/`.
Keep logs, captures, assertions, investigation reports, and old/new gap Markdown under the owning task.
Keep harness checkpoints in ignored working storage or required retained evidence.
When useful, link stable gap IDs from reports and navigation without importing their results as intent.

Requirements need matching structured criteria and readable Gherkin scenarios with explicit assertions.
Separate business thresholds from controlled test fixtures.
Keep unsupported criteria outside the confirmed acceptance list; record missing business limits instead of inventing numbers.

## Checkable output and stop conditions

Return classified candidate paths, stable IDs/versions, connected index entries, exact source bindings, and unresolved scope.
Check the chosen schemas and citations before handing off.
Stop affected meaning changes when material ambiguity or missing authority remains unresolved.
Use [prepare-knowledge-transition](../prepare-knowledge-transition/SKILL.md), [review-knowledge-claims](../review-knowledge-claims/SKILL.md),
and [record-knowledge-audit](../record-knowledge-audit/SKILL.md) before declaring changed records complete.
Writing candidates supplies no human approval or evidence of implemented behavior.
Return exact output paths for the caller's `sources complete` receipt after final review and integrity checks.
