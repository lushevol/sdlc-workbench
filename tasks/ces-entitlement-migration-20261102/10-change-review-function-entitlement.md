---
artifact_kind: change-request
id: CR-CES-FUNCTION-ENTITLEMENT-20261117
version: 1
status: draft
owner: unknown
source_refs: [USER-FUNCTION-20261117, USER-FUNCTION-ANSWERS-20261117, USER-FUNCTION-TIMING-20261117, MATRIX-X-RATANONE, MATRIX-RATAN-FUNC]
related_ids: [CES-MIGRATION, CES-COVERAGE-CASES]
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
    - Automated checks do not establish complete writing review.
---

# CES function entitlement value tests

> **Each account has one functional profile; incompatible assignments must be rejected.**
> Action: bind the new-field response and classify historical exceptions. Owner: unknown.
> Consequence: affected executions need those inputs. Evidence: [user answers](evidence/function-entitlement-20261117/user-clarifications.md).

## Request and source facts

The user reports CES agreement to add `function_entitlement` on 17 November 2026.
The request covers value tests and discussion. API schema validation is excluded.
The [exact input](evidence/function-entitlement-20261117/user-input.md#exact-user-input) defines six initial behaviors.
The existing [case catalog](06-test-cases.md#function-entitlement-value-tests) owns all new case definitions.
The [discussion answers](evidence/function-entitlement-20261117/user-clarifications.md) require exactly one functional profile per assigned account.
An account without a functional assignment still has an empty value.
CES must reject incompatible assignments. General accounts include Generic, System, and Service accounts.
Test both immediate correctness and propagation duration. Report those outcomes separately.
The [latest timing answer](evidence/function-entitlement-20261117/user-timing-target.md#exact-answer) selects five seconds as the test target.
The CES NFR remains unconfirmed. Use CES confirmation as the recorded test clock origin.

Entry route: requirements first for test specification.
The [prior CES request](evidence/frontend-entitlement-impact-20261105/ces-api-role-resolution-request-20261110.md) proposed different identification options.
The latest user message governs this test scope. It does not confirm a deployed implementation.
No inspected sample contains the new field. Actual field location and candidate build remain unknown.

## Stage boundary and readiness

- Stage: draft value cases for discussion, authorized by the user request.
- Readiness for drafting: `READY`; unresolved branches remain explicitly conditional.
- Readiness for affected test execution: `NEEDS_CLARIFICATION`.
- Frozen intake: [01-intake.md](01-intake.md), unchanged from revision `0620f12083a6f1df08130b7d8091cb90b633ada8`.
- Intake SHA-256: `75f6060533f55ebda9931bef064c4ff63a2596ab4597b657d38ae55b06bf6bfa`.
- Prior case definition: version 15; SHA-256 `0bda012e41531b05553caa4193c7a9375744d5e70e8a03126485a5e30e0e0c61`.
- Compared implementation: unavailable; no new-field implementation was supplied.
- Assessor: Codex, 2026-11-17, Asia/Singapore.
- Blocked actions: executing policy-dependent cases before resolving their expected values.
- Owner and next action: unknown; resolve the questions below and bind the target CES release.
- Intake integrity: verified during [document checks](evidence/function-entitlement-20261117/validation.json).

## Proposed change

| Aspect | Earlier evidence | Current proposed verification | Basis |
| --- | --- | --- | --- |
| Functional profile identity | Effective responses mix functional, common, and data role names. | Compare only `function_entitlement` with independently approved functional profiles. | [User request](evidence/function-entitlement-20261117/user-input.md#exact-user-input) |
| Human accounts | Matrix contains X_RATANONE profiles. | Verify exact assigned names for every scoped account and every approved profile. | [X_RATANONE matrix](<ces migration/X_RATANONE_security_matrix_prod.xlsx>) |
| General accounts | Matrix contains SYS_RO and SYS_OPS. | Compare values with the corresponding RATAN_FUNC assignment. | [RATAN_FUNC matrix](<ces migration/RATAN_FUNC_security_matrix_prod.xlsx>) |
| Lifecycle changes | New-field update behavior is unobserved. | Verify switch, onboarding, last-role removal, and re-onboarding values. | [Canonical cases](06-test-cases.md#function-entitlement-value-tests) |
| Additional coverage | Current request names six initial cases. | Discuss isolation, data-only accounts, freshness, exact names, and repeated assignment. | Proposed test extensions; review pending. |

## Scope and affected artifacts

| Artifact | Exact version | Effect | Risk and basis | Owner |
| --- | --- | --- | --- | --- |
| [Case catalog](06-test-cases.md#function-entitlement-value-tests) | Version 16 | Append value cases; preserve historical definitions. | Low; documentation change. | unknown |
| [Source inspection](evidence/function-entitlement-20261117/source-inspection.json) | Workbook hashes and cells | Retain counts, role definitions, and exceptions without account identities. | Historical conversion data can disagree with current assignments. | unknown |
| CES API | Release unknown | Verification target only. | Wrong expected values could conceal an incorrect role projection. | unknown |

## User impact

Incorrect profile names can misidentify role-dependent consumer behavior.
These cases verify returned values and incompatible-assignment rejection. They establish no downstream business acceptance.
The new field does not settle saved-item ownership or existing scalar-role consumer policy.
Owner: unknown. Next action: review those consumer rules separately when integration is requested.

## System impact

No application source, dependency, endpoint, or account assignment changes in this stage.
Existing effective-response fixtures contain no verified new-field values.
No assertion binding or execution exists for the new cases.
No API schema, datatype, required-field, or whole-response comparison is requested.

## Options and consequences

| Option | Consequence | Disposition |
| --- | --- | --- |
| One functional profile per assigned account. | Multi-profile acceptance cases are inapplicable. | Confirmed by the user. |
| Return several functional profiles. | Contradicts the confirmed single-profile rule. | Rejected as an expected outcome. |
| Check incompatible output values only. | Cannot prove CES prevents invalid assignments. | Insufficient for confirmed case 6. |
| Also test assignment rejection. | Requires controlled provisioning attempts and unchanged-value assertions. | Confirmed for test specification; no execution performed. |

## Proposed acceptance and validation

The [traceability table](06-test-cases.md#function-entitlement-traceability) maps all six requested behaviors to cases.
The [additional cases](06-test-cases.md#tc-func-007) remain proposals for discussion.
All new cases have execution status `NOT_RUN` and unavailable automation bindings.
Expected values must come from approved assignments, independently of the field under test.
API errors cannot count as an empty entitlement or a passing value comparison.

## Implementation and release proposal

- Implementation: none requested.
- Target CES release, environment, and build: unknown.
- Test estimate: unknown until account access and automation bindings are confirmed.
- Reversal: revert this scoped documentation commit if required.
- Bounded exploration: not applicable; the request concerns specifications and discussion.

## Sources and evidence limits

| Source ID | Locator | Revision or hash | Authority and limits |
| --- | --- | --- | --- |
| USER-FUNCTION-20261117 | [Exact input](evidence/function-entitlement-20261117/user-input.md#exact-user-input) | 2026-11-17; hash in validation | User instruction; reported CES agreement, not runtime proof. |
| USER-FUNCTION-ANSWERS-20261117 | [Exact discussion answers](evidence/function-entitlement-20261117/user-clarifications.md) | 2026-11-17; hash in validation | User intent; no execution or publication approval. |
| USER-FUNCTION-TIMING-20261117 | [Exact timing answer](evidence/function-entitlement-20261117/user-timing-target.md#exact-answer) | 2026-11-17; hash in validation | User-selected five-second test target; CES NFR unconfirmed. |
| MATRIX-X-RATANONE | [Workbook](<ces migration/X_RATANONE_security_matrix_prod.xlsx>) | `e6e6da5a43b1303593c74da3703f8066bcf58a10abe3f729f8ea6aa204678d63` | Historical PROD-labelled conversion snapshot; current applicability unverified. |
| MATRIX-RATAN-FUNC | [Workbook](<ces migration/RATAN_FUNC_security_matrix_prod.xlsx>) | `f0bb7982136da01bf78b323374f1e53602ceca1df11e6b0c261b8e441786f4ac` | Historical PROD-labelled conversion snapshot; current applicability unverified. |

The [inspection](evidence/function-entitlement-20261117/source-inspection.json) records exact workbook cells and bounded searches.
No network request or business test ran. No credentials are copied into this stage.

## Unknowns and blockers

| ID | Question and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| FUNC-Q1, resolved | Exactly one functional profile per account. [Exact answer](evidence/function-entitlement-20261117/user-clarifications.md#func-q1-exact-question-and-answer). | Remove simultaneous-profile and partial-removal cases. | User answer; implementation owner unknown | Preserve the one-profile invariant. |
| FUNC-Q2, resolved | Also verify CES rejects incompatible assignments. [Exact answer](evidence/function-entitlement-20261117/user-clarifications.md#func-q2-exact-question-and-answer). | Add rejected human-to-general and general-to-human assignments. | User answer; implementation owner unknown | Query again and assert the original value stays unchanged. |
| FUNC-Q3, resolved for tests | Test immediate reads and propagation within five seconds. [Latest answer](evidence/function-entitlement-20261117/user-timing-target.md#exact-answer). | CES NFR remains unconfirmed; confirmation time is the test clock convention. | User answer; CES NFR owner unknown | Measure both results separately; retain the NFR limitation. |
| FUNC-Q4, resolved | General includes Generic, System, and Service. [Exact answer](evidence/function-entitlement-20261117/user-clarifications.md#func-q3-and-func-q4-exact-question-and-answer). | All three classes require RATAN_FUNC coverage. | User answer; implementation owner unknown | Classify historical exceptions separately. |
| FUNC-Q5 | Which actual new-field response defines the empty value and exact field location? | Assertions cannot distinguish an intended empty value from an unavailable acquisition. | unknown | Bind a sanitized CES response before automation; no schema validation required. |
| FUNC-Q6 | How must the two historical exceptions below be remediated? | Their prior values contradict the current intended account rule. | unknown | Record corrected source assignments or a separately approved exception. |

Two historical rows conflict with the latest account rule:

| Source cells | Historical assignment | Required disposition |
| --- | --- | --- |
| X_RATANONE `UserEntitlement!A508:G508` | Generic account assigned EMS2_ADMIN, absent from the workbook role catalog. | Confirm correction or explicit administrative exception. |
| RATAN_FUNC `UserEntitlement!A11:G11` | User account assigned SYS_RO. | Confirm correction or explicit account-class exception. |

Do not omit these rows or count them as passing. Keep unresolved rows visible in coverage.
Resolved answers remain binding. A continuation supplies no missing response binding or exception decision.

### Knowledge-update log

The [existing parity candidate](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#open-questions) retains unresolved consumer projection and saved-item ownership.
The new answers resolve functional-profile cardinality, cross-account rejection, general-account classes, and the five-second test target.
The [reconciliation record](evidence/function-entitlement-20261117/knowledge-reconciliation.json) binds the updated candidate, sources, checks, and audit evidence.
The candidate remains unpublished. Wiki refresh and business execution remain separate from this test discussion.

| Answer scope | Record change | Criteria and audit | Remaining state |
| --- | --- | --- | --- |
| Single profile, account classes, lifecycle, rejection, and timing target | [KT-ces-migration-parity](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#current-functional-profile-value-rule), version 6 to version 7 | [Profile](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#func-profile-ac-001), [lifecycle](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#func-profile-ac-002), [rejection](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#func-profile-ac-003), [immediate read](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#func-profile-ac-004), [five seconds](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#func-profile-ac-005); [new candidate audit](../../knowledge/evidence/audit/AUD-20261117-KT-ces-migration-parity-v7.yaml) | Candidate. Empty representation and CES NFR remain unresolved; consumer ownership remains separate. |

## Stage evidence and completion

| Stage | Evidence | Result | Remaining action |
| --- | --- | --- | --- |
| Source inspection | [Workbook facts](evidence/function-entitlement-20261117/source-inspection.json) | Local inspection complete. | Confirm current matrix applicability. |
| Case drafting | [Canonical definitions](06-test-cases.md#function-entitlement-value-tests) | Six requested cases and nine proposed additions saved. | Review additional cases and historical source exceptions. |
| Document checks | [Validation](evidence/function-entitlement-20261117/validation.json) | See actual retained result. | Resolve material questions before execution. |
| Business execution | No execution evidence | `NOT_RUN` | Bind release, data, timing, and automation. |

## Requested decision and actual disposition

- Requested decision: review the additional scenarios and classify historical source exceptions.
- Decision owner: unknown.
- Actual decision: one profile, account-class separation, rejection coverage, both timing checks, and five-second target confirmed by the linked answers.
- Implementation: not performed.
- Intent review: six user-supplied behaviors; additional expectations remain proposed.
- Execution: `NOT_RUN`.
- Business acceptance and deployment: not established.
