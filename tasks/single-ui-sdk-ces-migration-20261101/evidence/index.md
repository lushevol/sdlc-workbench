# SDK CES migration evidence

> **SDK 3.0.0 passes local verification; complete permission compatibility remains unproved.**
> Action: compare reviewed assignments and compile actual consumers before acceptance.
> Consequence: local tests cannot establish deployed permission equality.
> Owner: unknown. Evidence: [execution report](../08-test-execution-report.md) and [sample comparison](role-compatibility-design.md#sample-comparisons).

The [current stage](../10-change-review.md) supersedes the frozen intake's implementation readiness assessment.
The [implementation clarification](user-clarification-implementation.md) authorizes compatibility work, version `3.0.0`, caller-supplied FMAA tokens, and tests.

## Current implementation confidence

| Claim | Confidence | Evidence | Material limit |
| --- | --- | --- | --- |
| Local SDK implementation and packaging pass. | HIGH. | [Final source manifest](candidate-run-04/inputs.json), [results](candidate-run-04/result.json), and [build log](candidate-run-04/build.log). | CES responses use mock transport. |
| Existing map and Java caller work for equivalent assignments. | HIGH within the paired case. | [Compatibility result](compatibility-run-01/result.json) and [probe](CompatibilityProbe.java). | One controlled fixture and baseline API; not all historical artifacts. |
| Full deployed permission equivalence. | MEDIUM; not established. | [Detailed comparison](role-compatibility-design.md#sample-comparisons). | Supplied assignments differ; CES catalog includes five extra grants. |
| All deployed consumers can adopt the artifact unchanged. | UNKNOWN. | [Consumer findings](consumer-scope.md#confirmed-consumers-and-compatibility). | Exact deployed inventory and consumer builds are unavailable. |

## Current evidence

| Item | Evidence | Result and limit |
| --- | --- | --- |
| Intended behavior | [Exact clarification](user-clarification-implementation.md). | User-selected version, token ownership, compatibility goal, and tests. |
| Current handoff | [Change review](../10-change-review.md). | Implementation complete; acceptance and deployment remain separate. |
| Canonical cases | [Case catalog](../06-test-cases.md). | Twelve canonical cases. |
| Execution | [Execution report](../08-test-execution-report.md). | 44 unit tests pass with zero failures, errors, or skips. |
| Traceability | [Coverage record](../09-coverage.md). | Criteria-to-test, criteria-to-change, and change-to-test mappings. |
| Final offline build | [Inputs](candidate-run-04/inputs.json), [results](candidate-run-04/result.json), [environment](candidate-run-04/environment.txt). | Exact pre-run hashes; no source changed during execution. |
| Paired baseline/candidate case | [Inputs](compatibility-run-01/inputs.json), [baseline](compatibility-run-01/baseline-result.json), [candidate](compatibility-run-01/candidate-result.json). | One caller compiled against baseline passes under both classpaths. |
| Compiled public API | [API comparison](public-api-comparison.json). | No missing public members across 23 baseline classes; historical releases remain unbound. |
| Independent review | [Code review](sdk-code-review.md). | Two corrected findings and retained before/after contexts. |
| Knowledge intent update | [Knowledge record update](knowledge-update.md). | Candidate version 8; no publication approval. |
| Document checks | [Artifact lint](implementation-artifact-lint.json) and [link checks](implementation-document-checks.json). | Structural lint and all selected paths/fragments pass; human reviews remain pending. |
| Workspace validation | [Result](implementation-workspace-validation.json). | VALID. This does not verify business behavior. |

## Prior evidence and limits

The [frozen intake](../01-intake.md) preserves the original assessment and living question history.
Its old implementation blockers do not override the later [stage readiness](../10-change-review.md#stage-boundary-and-readiness).
The [source manifest](source-manifest.json) binds original inspected revisions.
The [SDK scope](sdk-scope.md), [CES reference](ces-reference.md), and [consumer scope](consumer-scope.md) remain source evidence.
The [initial request](user-input.md) and [confidence follow-up](user-followup-confidence.md) retain exact user wording.
The [baseline build](baseline-build-result.json) passed with zero tests. That result establishes compilation only.
Earlier baseline logs preserve offline, network, and JDK setup failures.
[Run 01](candidate-run-01/result.json) failed test compilation. The ambiguous Spring test setup was corrected.
[Run 02](candidate-run-02/result.json) passed 41 tests, then failed packaging because artifacts were unavailable.
[Run 03](candidate-run-03/result.json) completed connected preparation and packaging with 44 passing tests.
Runs 02 and 03 lack pre-run manifests. Run 04 is the authoritative final source-bound execution.
Prior [intake lint](intake-lint.json), [document checks](document-checks.json), and [confidence checks](document-checks-confidence.json) remain historical.

## Remaining acceptance evidence

The application owner must supply actual CES configuration and current FMAA tokens.
Verify the assigned-role endpoint, HTTPS trust, refresh behavior, and failure policy in the target environment.
Compare synchronized EMS2/CES assignments, including service accounts and required data roles.
Compile actual consumers and verify permitted and denied actions before adoption.
These evidence gaps do not establish a production incident or forced logout.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Document checks do not establish business verification or publication approval.
```
