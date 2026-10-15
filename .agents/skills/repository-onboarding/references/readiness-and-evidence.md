# Readiness and evidence contract

## Readiness dimensions

Use `ready`, `partial`, `missing`, or `not-applicable` for each dimension.
Give a rationale, supporting claim IDs, evidence limits, and any required action.

| Dimension | Ready when |
| --- | --- |
| Repository identity | The checkout root and exact Git revision are available. |
| Purpose and ownership | Source corroborates repository responsibility and known ownership; non-goals and ownership gaps remain explicit. |
| Agent instructions | Applicable guidance supports navigation, constraints, and permitted verification commands. |
| Build and tests | Authorized execution and inspected assertions support reproducibility within a stated environment. |
| Interface contracts | Relevant provided and consumed interfaces have versioned source evidence. |
| Functional mapping | Inspected source connects business functions to components, entrypoints, and tests. |
| Dependency visibility | Inspected relationships distinguish declarations, inferences, and observed runtime links. |
| Evidence governance | Claims retain exact citations, conflicts, revision limits, and review status. |

Documented commands without retained execution support at most `partial` build readiness.
A missing Git revision prevents the exact-evidence gate from passing.
For a non-code asset, explain each `not-applicable` choice.
Do not mark missing evidence as inapplicable merely to improve readiness.

Classify P0 blockers by their effect on the requested workflow.
Examples include unreadable source, unknown implementation ownership, or missing verification commands for code changes.
P1 improvements address consequential mapping or contract gaps.
P2 options need a demonstrated benefit before implementation.
Give every finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Write measurable Gherkin scenarios for proposed acceptance criteria.

## Structured report

`repo-onboarding.json` is a skill-local staging report.
It is not a Workbench catalog or governed knowledge record.
Its `schema_version` remains the string `"1.0"`.
Canonical catalogs instead use integer `schema_version: 1`.

```json
{
  "schema_version": "1.0",
  "repository": {
    "id": "<confirmed repository ID or unknown>",
    "path": "<absolute local checkout root>",
    "revision": "<full 40-character or 64-character commit ID or unknown>"
  },
  "claims": [
    {
      "id": "CMP-001",
      "category": "component",
      "statement": "The inspected controller delegates the request to a service method.",
      "status": "observed",
      "evidence": [
        {"path": "<actual repository-relative source path>", "start_line": 12, "end_line": 18, "kind": "source"}
      ]
    },
    {
      "id": "DEP-002",
      "category": "external-dependency",
      "statement": "The configured listener might consume the declared topic.",
      "status": "inferred",
      "reason": "Configuration declares a topic, but no retained runtime observation establishes consumption.",
      "evidence": [
        {"path": "<actual configuration path>", "start_line": 20, "end_line": 24, "kind": "configuration"}
      ]
    },
    {
      "id": "GAP-003",
      "category": "verification",
      "statement": "Production consumption remains unknown.",
      "status": "unknown",
      "reason": "No applicable runtime observation or retained integration execution was available.",
      "evidence": []
    }
  ],
  "output_review": {
    "standard": "ASD-STE100",
    "automated_check": "PENDING",
    "asd_review": "PENDING",
    "reviewer": null,
    "reviewed_at": null,
    "limitations": [
      "Automated checks do not check the complete approved dictionary or grammar rules."
    ]
  }
}
```

Replace illustrative statements, paths, ranges, and revision before use.
Set `automated_check` from checks actually performed and record each check result in the assessment.
The evidence helper does not validate ASD metadata or semantic accuracy.
Only a complete writing review can set `asd_review: PASSED`.

## Claim and evidence rules

- `observed`: direct evidence supports a narrow source observation.
  This status establishes neither knowledge approval nor passing business execution.
- `inferred`: evidence supports a possible interpretation; include a nonempty string `reason`.
- `conflicting`: cite at least two disagreeing sources and explain the conflict in `reason`.
- `unknown`: supply a nonempty string `reason` instead of guessing.

Claims need unique nonempty IDs, categories, and statements.
Observed and inferred claims need evidence.
Allowed evidence kinds are `source`, `test`, `contract`, `configuration`, `documentation`, and `runtime-artifact`.
Paths use POSIX separators and identify regular files inside the checkout.
Use inclusive line ranges beginning at 1.
Symlinks and paths outside the checkout cannot supply this helper's evidence.

The helper checks that HEAD matches the report revision.
It checks each cited file's bytes against the committed Git blob.
Ignored, untracked, and changed evidence files fail validation.
Unrelated checkout changes can remain when all cited bytes match the declared commit.
Git checkout transformations, including automatic CRLF conversion, can prevent a byte match.
Record that limit and inspect committed bytes without running repository filters.
An unknown revision cannot pass exact evidence validation.
Record that limit while preserving the assessment.

Runtime observations outside the repository need their own retained identity and review in `assessment.md`.
The helper accepts only files within the repository.
A source citation to a test does not prove that its assertions passed.
A runtime artifact's presence does not authenticate its reported result.

## Findings and proposal review

For each proposal, record its file, record ID, supporting claims, review state, and known or unknown review owner.
Keep unconfirmed identifiers and fields in this review table rather than inventing catalog values.
Distinguish documented intent from source implementation and runtime observations.
Keep unresolved questions visible through later ingestion and governance review.
