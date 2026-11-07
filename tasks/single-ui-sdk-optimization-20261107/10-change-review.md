---
artifact_kind: change-request
id: SDK-OPT-CHANGE-20261107
version: 1
status: draft
owner: unknown
source_refs: [SDK-OPT-INPUT, SDK-OPT-BASE]
related_ids: [SDK-OPT-20261107]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Simplify the CES permission mapper

> **No critical conclusions require user attention or action.**

## Request and source facts

- Requester: human user in Codex.
- Request: [optimize the latest SDK change](evidence/user-input.md#exact-user-input) using Ponytail full mode.
- Baseline: SDK `fd9a157e260850b6d9efa10da3223950ea61133a`, implemented on 1 November 2026.
- Entry route: existing implementation. Optimization registered on 7 November 2026.
- Rationale: simplify private mapping logic while preserving behavior.

## Stage boundary and readiness

- Stage: local refactoring and complete SDK test execution.
- Readiness: READY within the [frozen intake scope](01-intake.md#selected-affected-scope-and-risk).
- Assessor: Codex, 7 November 2026, Asia/Singapore.
- Frozen intake Git: `00ca372335962067299f41ece0cda2785f539340`.
- Frozen intake SHA-256: `2040e41872caa6fc36275754a23c4f07835de87da31da43d26066799dfb6c022`.
- Compared implementation: baseline above to SDK `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`.
- Intake integrity: the frozen hash matches before and after implementation.
- Blocked actions: none within local optimization. Artifact publication and deployment are outside scope.
- Owner and next action: Codex; complete the evidence handoff.

## Proposed change

Both changes are implemented in [AuthorizationImpl](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java).

| Aspect | Current baseline | Replacement | Basis |
| --- | --- | --- | --- |
| <a id="opt-c1"></a>OPT-C1: Role aliases | Check membership, then retrieve the alias. | Retrieve once; skip missing aliases. | Configuration validation forbids null aliases. |
| <a id="opt-c2"></a>OPT-C2: Subject actions | Store lists as objects and cast them back. | Store typed action lists internally. | Every inserted subject value is a string list. |

## Scope and affected artifacts

| Artifact | Version | Effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| Private `mapRoles` | Baseline above plus scoped diff. | Two local simplifications. | [Source](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java). | Low change risk; permission errors remain consequential. | Codex |
| Tests, fixtures, properties, exports, and dependencies | Same baseline. | No changes required. | [Baseline hashes](evidence/baseline-result.json). | Existing assertions cover the selected boundaries. | Codex |

## User impact

SDK callers retain the same public methods and permission-map structure.
Selected roles preserve action order, duplicates, and mutable lists.
Excluded roles and invalid responses retain their existing failure behavior.
No user-visible behavior change is intended.

## System impact

`AuthConfiguration` and direct callers construct the same SDK service.
The public `AuthorizationService` interface remains compatible.
Each selected alias now requires one retrieval after configuration validation.
The local subject map no longer requires an unchecked cast.
No throughput or latency gain is claimed without measurement.

## Options and consequences

Keep DTOs, compatibility constructors, and mutable configuration behavior.
Removing these contracts could break unknown external consumers.
Indexing configuration or caching tokens would add lifecycle and compatibility risk without a demonstrated need.

## Proposed acceptance and validation

Reuse the existing canonical cases and all 44 SDK tests.
Do not add duplicate cases for unchanged behavior.

| Criterion | Required validation | Current result | Evidence |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | Complete suite, exact assertions, and final diff inspection. | Baseline and candidate pass; 44/44 tests each. | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json). |

### AC-to-test coverage

| Criterion | Canonical cases | Assertion basis | Coverage |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | [SDK-TC-001](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-001), [SDK-TC-002](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002), [SDK-TC-004](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004), [SDK-TC-007](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-007) | [Authorization assertions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java). | 1/1 scoped criteria have direct assertions. |

### AC-to-code-change coverage

| Criterion | Changed units | Required unchanged behavior | Coverage |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | [OPT-C1](#opt-c1) and [OPT-C2](#opt-c2). | Validation, scoping, collisions, action order, duplicate actions, and mutable output. | 1/1 scoped criteria traced; no added product behavior. |

### Code-change-to-test coverage

| Changed unit | Direct assertion chain | Execution |
| --- | --- | --- |
| [OPT-C1](#opt-c1) | [Selected and excluded aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:130), [null aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:140), [excluded malformed roles](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:272), and [invalid aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:404). | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json) pass. |
| [OPT-C2](#opt-c2) | [Exact maps, duplicates, and empty roles](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:60), [feature/subject aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:150), and [subject collisions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:429). | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json) pass. |

Both changed units have direct assertion links: 2/2.
These links do not establish full migration conformance or production parity.
All 44 tests remain in the execution denominator.

## Implementation and release proposal

- Implementation: one production file; no new dependencies or public interfaces.
- Release: no publication or deployment is proposed.
- Reversal: revert the isolated SDK optimization commit.
- Bounded exploration: not applicable; this is an authorized behavior-preserving refactor.

## Sources and evidence limits

| Source | Locator | Identity and authority | Limit |
| --- | --- | --- | --- |
| SDK-OPT-INPUT | [Exact user input](evidence/user-input.md#exact-user-input) | Human request, 7 November 2026. | Optimization authority only. |
| SDK-OPT-BASE | [Baseline result](evidence/baseline-result.json) | SDK revision and exact source/test hashes. | Controlled local execution. |
| Prior design | [Migration design](../single-ui-sdk-ces-migration-20261101/10-change-review.md#selected-compatibility-design) | Preserved migration constraints. | Live entitlement parity remains unverified. |

## Unknowns and blockers

The fresh [offline packaging attempt](evidence/packaging-result.json) stops before tests because formatter-plugin dependencies are absent.
This limits packaging verification. It does not establish an SDK defect.
Owner: unknown for build-environment maintenance; prepare the missing artifacts before the next full lifecycle run.
Live CES/FMAA and deployed consumers remain unverified.
These limits do not block the selected local refactor.
Accountable integration owner: unknown; verify actual consumers before adoption.

## Stage evidence and completion

| Stage | Evidence | Current result | Next action |
| --- | --- | --- | --- |
| Impact and source inspection | [Frozen intake](01-intake.md#selected-affected-scope-and-risk). | Complete. | Preserve selected boundaries. |
| Code review | Scoped diff and independent agent inspection. | No actionable findings. | None within the selected scope. |
| SDK execution | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json). | 44/44 tests pass in both runs; zero failures, errors, or skips. | None within the selected scope. |
| Browser execution | Library-only change; no UI code. | Not applicable. | Use SDK HTTP and Spring assertions. |

## Requested decision and actual disposition

- Actual authorization: simplify and verify the latest SDK change.
- Implementation: SDK commit `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`; one changed production file.
- Execution: baseline and candidate pass all 44 tests. The full offline lifecycle remains blocked by missing plugin dependencies.
- Business acceptance and live migration parity: not assessed.
- Knowledge meaning: unchanged; no domain record update is required.

### Verification reconciliation

The first candidate invocation executed zero tests. Its existing XML reports were stale.
The [runner-failure record](evidence/candidate-runner-failure.json) excludes those reports from passing evidence.
The cause of that discovery failure remains unknown. No application failure was established.
The candidate then compiled and passed in an isolated checkout with matching source hashes.
The first packaging invocation omitted a module argument. The [corrected attempt](evidence/packaging-result.json) records the actual dependency block.

The independent source review found no actionable defect.
Null and empty alias maps retain role names. Excluded aliases still skip grant validation.
Typed values retain mutable maps and lists, action order, and duplicates.
No concurrent configuration mutation or custom stateful map behavior was evaluated.

No new test was needed because existing assertions cover both transformations and their relevant boundaries.
No new feature, dependency, token cache, configuration index, or public contract was introduced.

[Document checks](evidence/document-checks.json) record automated results and pending human reviews.
