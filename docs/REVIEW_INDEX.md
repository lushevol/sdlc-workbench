# Shared review evidence index

The review index connects existing criteria, changes, cases, assertions, results, and assessments through retained evidence references.
It creates a derived view. Original evidence remains in its owning task or established source location.

## Validate an index

```sh
ai-sdlc --workspace PATH assurance index-schema
ai-sdlc --workspace PATH assurance index --input review-index.json
ai-sdlc --workspace PATH assurance index --input review-index.json --require-current
```

Inputs must remain inside the selected workspace.
The schema command needs no workspace configuration.
Validation does not start test runners or contact external systems.

## Contract and references

Use schema version `1` and stable IDs.
Keep the scope ID separate from any ADO release identity.
Use explicit completeness declarations for criteria, changed behavior, and cases.
`COMPLETE`, `SELECTED`, and `UNKNOWN` describe declared inventory scope.
The validator does not establish semantic completeness.

| Collection | Purpose |
| --- | --- |
| `artifacts` | Retained workspace paths and SHA-256 identities, with optional exact repository bindings. |
| `criteria` | Intended behavior definitions and declared required test levels. |
| `changes` | Changed business behavior, maintenance, test-only changes, and required unchanged implementation. |
| `cases` | Canonical case definitions. |
| `assertions` | Explicit case-to-assertion references and reviewed predicate scope. |
| `links` | Direct AC-to-case, AC-to-change, and change-to-case evidence. |
| `executions` | Original runner statuses, normalized outcomes, environment identity, characterization, and limits. |
| `assessment` | Optional recorded recommendation, certainty, review state, and issue dispositions. |

An artifact records its own bytes through `sha256`.
Repository bindings use a repository ID, full Git revision, and repository-relative source path together.
Keep current checkout modifications separate from retained evidence at a selected revision.
Each locator identifies an artifact and an optional line range or heading anchor.
Referenced IDs must resolve to the correct collection.

Keep direct assertion links separate from shared criterion associations.
Two records referring to the same AC do not establish a change-to-test assertion chain.
Mark selected predicate evidence explicitly. A file-level link does not prove every changed behavior.
Retain limits when approved criteria or complete change inventories remain unavailable.

## Interpret results

Contract validity checks structure, references, confined paths, and supported locators.
Freshness checks retained artifact hashes and declared source bindings.
Missing evidence remains unknown. Changed evidence remains stale.
`--require-current` fails when evidence is stale or unknown.

The result retains `verification: NOT_VERIFIED`.
Valid references do not establish intended behavior, passing execution, deployed identity, approval, or production readiness.
Declared completeness and reviewed relationship meaning remain separate responsibilities.
Unknown environment identities must remain unknown.

Preserve original runner status separately from the normalized outcome.
A characterization pass describes observed behavior. It does not establish that intended business behavior passed.
Failed, partial, blocked, not-run, and error outcomes must remain visible.
Recorded assessment decisions retain their own source and review state.
The index does not generate business approval or waive failed applicable unit tests.

## Ownership and distribution

Keep runtime implementation in `core/review_index.py` through the installed `ai_sdlc_workbench` package.
The installed schema is `core/schemas/review-index.schema.json` in the source checkout.
Generated workspaces receive this guide. They do not receive runtime source or project evidence.
Use the [behavior review guide](BEHAVIOR_REVIEW.md) for the existing immutable baseline workflow.
Use the [traceability template](../core/knowledge/templates/sdlc/traceability-record.md) for human review records.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
