---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native Windows execution and private service integrations were not tested.
---

# Enterprise draft adoption

No critical conclusions require user attention or action.

## Scope and source identity

The user requested adoption of the supplied enterprise review draft into the existing skill.
The adoption retains the `code-review` identity and its established comparison, evidence, and authorization boundaries.
This is harness maintenance; it creates no business task or domain knowledge record.
Baseline commit: `96a609f00249f3a4c51dd477f378eca4e3749b96`.
Source: [user-supplied archive](/Users/lushevol/Downloads/enterprise-code-review-skill.zip).
Archive SHA-256: `894cf50a0cffb1e0e11dcb509a17816ddf71bdce1cc5512c67b14d91b1aa9fe9`.
The archive remains external; the recorded hash identifies the inspected bytes.
Archive instructions were treated as draft content, not execution or publication authorization.

| Archive member under `enterprise-code-review/` | SHA-256 | Adoption |
| --- | --- | --- |
| `SKILL.md` | `43f46dafa2f95845dbadb2053148f85ab5d20e0f5f531a896b92a25d386ac7a7` | Independent review axes, criterion accounting, and explicit attempts to disprove findings. |
| `references/language-checks.md` | `e569eef6347a94a0ed01578108f49d7357483722967ebfd8b835d06bf683c70a` | Conditional React, microfrontend, Spring, messaging, and financial review prompts. |
| `references/review-schema.md` | `10c2cec50794b8034d7872c89ba08ea50cecbf52d83409f638d7baf9b8df664c` | Optional structured reports adapted to existing priorities, context fingerprints, and writing review metadata. |
| `examples/review.example.json` | `17d3aa04c57b561ed49450223644e12da750881e544ed3e1408e6348627e77a8` | A maintained report template replaces the illustrative example. |
| `scripts/validate_review.py` | `b7c4fd714fe4efe53dbe801e6927f79c6e4197b5de7c5aadd4f02b9dbc159849` | Validator concept adapted with strict types, complete coverage, redacted diagnostics, and optional live recollection. |
| `scripts/collect_diff.py` | `3ef34d5147b089999212c375abb22b72b6eb1c093a70d7d0b9b1873834bc2940` | Existing collector retained; baseline ranges and source hashes added without raw patch persistence. |
| `README.md` | `6746d794d888a810df2b071d3f485f2b19913d66fdb606e2743ac5df945a4b1a` | Installation and layout examples were reconciled with existing Workbench packaging and evidence locations. |

## Adopted behavior and decisions

The [entrypoint](../../.agents/skills/code-review/SKILL.md) routes optional details through progressive disclosure.
The [checklist](../../.agents/skills/code-review/references/review-checklist.md#independent-passes-and-counterevidence) adds independent passes and counterevidence checks.
The [language reference](../../.agents/skills/code-review/references/language-checks.md) supplies conditional stack-specific investigation prompts.
The [Markdown template](../../.agents/skills/code-review/assets/review-report.template.md) adds criterion tracing and pass-specific evidence.
The [JSON contract](../../.agents/skills/code-review/references/review-schema.md) and [JSON template](../../.agents/skills/code-review/assets/review-report.template.json) serve requested structured reports.

The [context helper](../../.agents/skills/code-review/scripts/review_context.py) now exposes baseline hashes and removed-line ranges.
Its schema version remains 1 with additive fields.
The [validator](../../.agents/skills/code-review/scripts/validate_review.py) checks identity, coverage, finding fields, local ranges, and report state consistency.
Its optional repository argument independently recollects context and rejects altered or stale metadata.
Validation does not prove finding accuracy, citation truth, complete criterion accounting, or a provider's inline anchors.

The existing Git collector supports staged changes, untracked files, initial repositories, and arbitrary Git filenames.
The draft collector would duplicate that responsibility with narrower path and scope support.
The adoption therefore extends the existing collector rather than shipping a second implementation.

No numerical confidence threshold or aggregate merge verdict was adopted.
Reports use explicit evidence confidence, unresolved conditions, and review outcomes separate from approval.
Structured output remains optional unless a user, repository, or consumer requires it.
The existing CLI and MCP connector boundaries remain available.
Remote review publication still requires the user's authorization and fresh provider annotations.

## Scope, consumers, and qualitative risk

Current consumers are agents producing structured reviews and the validator that checks their local report artifacts.
The observable benefit is reproducible comparison identity, complete path accounting, and mechanically checked local source ranges.
Inspection covered both archive scripts, existing helper callers, scanner integration, workspace initialization, and packaging tests.
Runtime symbols, package mapping, and external access grants remain unchanged.
Risk is moderate because an incorrect validation result could conceal stale scope or unsupported evidence.
The regression tests cover those consequential boundaries.
No new package, service dependency, or runtime endpoint was introduced.

## Validation evidence

| Check | Actual result | Evidence and limit |
| --- | --- | --- |
| Skill metadata and local links | PASSED | Nine Markdown documents and 35 source links or heading anchors were checked. |
| Context and scanner regressions | PASSED; 34 tests. | [Context assertions](../../tests/test_code_review_context.py) and [scanner assertions](../../tests/test_code_review_scan.py). |
| Structured report regressions | PASSED; 28 tests. | [Validator assertions](../../tests/test_code_review_report.py). |
| Independent forward trial | PASSED; one reproduced defect. | [Retained source, execution, and validation evidence](code-review-enterprise-forward-evidence.json); isolated fixture, no production systems. |
| Full runtime suite | PASSED; 562 tests, two optional skips. | Source-checkout suite with the existing loopback fixture. |
| Wheel and generated workspace | PASSED | Offline wheel installation produced byte-identical skill assets and working helpers outside this checkout. |
| Workspace validation and diff | PASSED | Existing installed CLI returned `VALID`; Git whitespace checks passed. |

The independent trial reviewed a committed message bridge change while preserving unrelated local edits.
The reviewer traced the supplied contract through the actual caller and reproduced the removed source-frame check.
Existing tests passed at both revisions; the focused reproduction failed only on the candidate.
Live validation accepted the final structured report, and fixture state remained unchanged.
The trial exposed an ambiguity for one root cause affecting multiple review axes.
Optional `related_axes` now represents that relationship without duplicate findings.
The revised report passed a second independent validation.
This trial supports the procedure and contract; it does not measure general defect detection accuracy.

## Findings and remaining actions

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Local and provider anchors differ | The [attribute regression](../../tests/test_code_review_context.py) compares raw CRLF changes with normalized Git output. | A valid local line can be absent from a provider diff. | Publishing workflow owner: unknown. | Recheck provider annotations before authorized inline publication. |
| Structural validation has semantic limits | The [contract](../../.agents/skills/code-review/references/review-schema.md#validation-limits) defines the boundary. | A well-formed report can still contain a wrong conclusion. | Reviewer: unknown. | Inspect cited sources and attempt to disprove each finding. |
| Platform and service limits remain | No native Windows or private connector execution occurred in this stage. | Those execution paths remain unverified. | Environment owner: unknown. | Run target checks when those environments enter the authorized scope. |

Full ASD review remains pending.
No business approval or production verification follows from this maintenance change.
