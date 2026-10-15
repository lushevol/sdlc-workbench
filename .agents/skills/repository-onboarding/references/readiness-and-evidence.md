# Readiness rubric and evidence contract

## Readiness dimensions

Use `ready`, `partial`, `missing`, or `not-applicable`. Each decision needs a concise rationale and at least one path reference for `ready`/`partial` when practical.

| Dimension | Ready when |
|---|---|
| Repository identity | Checkout readable; commit SHA or a disclosed revision limitation recorded |
| Purpose and ownership | Scope, owned functionality and major non-goals are documented and corroborated |
| Agent instructions | `AGENTS.md` or equivalent provides navigation, constraints and safe verification |
| Build and tests | Build/test commands documented and validated by execution **only if authorized**; otherwise at most `partial` |
| Interface contracts | Relevant provided/consumed APIs, events or UI integration boundaries are discoverable and versioned |
| Functional mapping | Business capabilities -> components -> path patterns with evidence, not merely directory guesses |
| Dependency visibility | Major internal and external dependencies identified with certainty labels |
| Evidence governance | Claims traceable to paths/lines/revision; gaps, conflicts and approval status explicit |

P0 blockers usually include no trustworthy checkout/revision, no meaningful ownership/entrypoint discovery, or inability to find safe verification commands for a code-changing workflow. P1 includes missing component maps/contract inventory and ambiguous edges. P2 includes optional dependency indexing or improved documentation. **Classify severity based on actual impact, not blindly on a table.**

## `repo-onboarding.json` format

This machine-checkable report is **not** an ADE-wide canonical schema. It is a staging/evidence artifact. Example:

```json
{
  "schema_version": "1.0",
  "repository": {"id": "settlement-service", "path": "<local absolute repo path>", "revision": "<40-character SHA or unknown>"},
  "claims": [
    {
      "id": "CMP-001",
      "category": "component",
      "statement": "An exception controller exists and delegates to the exception service.",
      "status": "verified",
      "evidence": [
        {"path": "src/main/java/example/ExceptionController.java", "start_line": 12, "end_line": 38, "kind": "source"}
      ]
    },
    {
      "id": "DEP-002",
      "category": "external-dependency",
      "statement": "A Kafka topic appears to be consumed by the service in production.",
      "status": "inferred",
      "reason": "Only a local configuration declaration was found; runtime binding was not observed.",
      "evidence": [
        {"path": "src/main/resources/application.yml", "start_line": 20, "end_line": 24, "kind": "configuration"}
      ]
    },
    {
      "id": "GAP-003",
      "category": "verification",
      "statement": "Production consumption is not verified.",
      "status": "unknown",
      "reason": "No runtime observation or approved integration test was available.",
      "evidence": []
    }
  ]
}
```

Allowed claim statuses: `verified`, `inferred`, `conflicting`, `unknown`. Allowed evidence kinds: `source`, `test`, `contract`, `configuration`, `documentation`, `runtime-artifact`.

- `verified`: the **literal narrow claim** is directly evidenced. Existence of an event listener is verifiable from source; active production consumption is not.
- `inferred`: a plausible interpretation requiring review; give evidence and a `reason`.
- `conflicting`: two or more sources disagree; cite both and explain the contradiction in `reason`.
- `unknown`: evidence insufficient; provide `reason` rather than guessing.
- Evidence paths must be relative to the checkout, point to actual files, and carry inclusive 1-based line numbers.
- When the revision is `unknown`, validation of an exact revision is impossible and the report cannot pass the full readiness gate.
- Do not write sensitive source excerpts into the report. Line references are sufficient.
- For runtime observations, if evidence exists outside the repository (CI artifact, external log), describe it in `assessment.md`; the basic validator accepts only within-repository artifact files.

## Example `assessment.md` sections

```markdown
# Repository onboarding assessment
- Repository / checkout / revision / scan date
- Purpose and non-goals
- Deployables and framework overview
- Functional components (ID, business function, path patterns, claim IDs)
- Contracts and external dependencies (verified vs candidate)
- Readiness table (dimension, status, evidence, gap)
- P0 blockers and acceptance criteria
- P1 / P2 improvements
- Conflicting evidence and unresolved questions
- Proposed registry changes and accountable reviewer
- Validation result and unexecuted checks
```
