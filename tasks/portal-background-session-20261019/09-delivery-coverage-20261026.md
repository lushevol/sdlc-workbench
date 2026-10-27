---
artifact_kind: traceability-record
id: TRACE-session-delivery-20261026
version: 4
status: draft
owner: unknown
source_refs:
  - SRC-ut-release-principle-20261027
  - SRC-session-delivery-confidence-20261026
related_ids:
  - REQ-active-session-renewal
  - TEST-session-canonical-20261021
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

# Delivery coverage: main and candidate

**Production remains blocked. Three original acceptance criteria fail and one is only partially verified.**
Action: complete target, artifact, recovery, and release decisions. Owner: unknown release owner.
Consequence: local coverage does not establish production suitability or complete behavior equivalence.
Evidence: [corrected behavioral mappings](evidence/renewed-review-20261027/traceability/corrected-traceability.json) and [browser inventory](evidence/four-checks-20261027/e2e/reconciliation.json).

## Final candidate coverage: 27 October 2026

The [completion instruction](evidence/user-input-20261027-complete-four-checks.txt) authorizes these checks.
The [scope answer](evidence/user-input-20261027-backlog-scope.txt) retains the earlier backlog disposition for inherited failures.
Base: `f025513f696476a9cc8162681410cbd21e029bcb`. Final test commit: `e0030f5cf920b715f5831faf7df86cb9789b6d0f`.
Runtime bytes match `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303`. The [binding](evidence/four-checks-20261027/application-binding.json) verifies 408 committed files.
The unrelated incremental build cache remains excluded. The two later files add test assertions only.
The [separate unit result](evidence/four-checks-20261027/coverage/test-only-final-2/execution.json) satisfies the existing delivery principle.
Unit code coverage is not the behavioral coverage measure requested here.

These inventories contain seven original criteria, sixteen proposed refinements, and twelve changed runtime paths.
Original requirement version 5 retains version 4 predicate meaning. Business review remains pending.
The [corrected machine-readable matrices](evidence/renewed-review-20261027/traceability/corrected-traceability.json) retain direct assertion chains and individual result bindings.
The [prior matrices](evidence/four-checks-20261027/coverage/final-2-traceability-with-boundaries.json) remain historical.
The [latest request](evidence/user-input-20261027-review-e2e-traceability.txt) asks for behavior traceability, rather than unit code coverage.
The [browser inventory](evidence/four-checks-20261027/e2e/reconciliation.json) records all 27 planned cases and eight failures.
The [four-hour controlled comparison](evidence/four-checks-20261027/ac4-browser/comparison.json) passes renewal, login-request, and navigation controls.
It does not directly observe every possible fresh SSO prompt. AC-4 remains PARTIAL.
Synthetic authentication and controlled time limit that result. They do not establish production parity or live server acceptance.

| Scope and measure | Qualified / denominator | Limit |
| --- | --- | --- |
| Original criteria linked to canonical cases | 7/7, 100% | A case link alone does not establish complete criterion coverage. |
| Original criteria with complete canonical assertions | 6/7, 85.71% | The AC-4 case does not state a direct no-fresh-SSO-prompt assertion. |
| Original criteria with complete inspected fixture assertions | 6/7, 85.71% | AC-4 lacks a complete direct fresh SSO prompt observer. |
| Original criteria with all selected local predicates passing | 3/7, 42.86% | AC-5 through AC-7 pass. AC-1 through AC-3 fail. AC-4 remains partial. |
| Original criteria mapped to changed implementation | 5/7, 71.43% | Keyboard and scroll activity handlers remain absent. |
| Proposed criteria linked to cases | 16/16, 100% | Definitions remain proposed. A link is not full assertion coverage. |
| Proposed criteria with complete case definitions and inspected assertions | 14/16, 87.50% | DC-AC-10 and DC-AC-15 do not explicitly test preservation of refresh credentials. |
| Proposed criteria with all selected predicates passing | 13/16, 81.25% | DC-AC-14 fails. DC-AC-10 and DC-AC-15 only partially assert authentication preservation. |
| Changed runtime paths with selected direct test chains | 12/12, 100% | This is path reach. Complete behavior assertion coverage remains UNKNOWN/12. |
| Changed runtime paths with complete passing behavior evidence | UNKNOWN/12 | Failed sharing, the fresh SSO observer, and deployed consumers limit the claim. |

Additional unsupported behavior remains UNKNOWN where a complete intent or deployed-consumer inventory is unavailable.
No finite execution proves indefinite activity. No result establishes complete behavioral equivalence.

### Requirement-to-acceptance-criterion matrix

| Scope | Defined criteria | Coverage and gaps |
| --- | --- | --- |
| [Active session renewal requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), candidate version 5 | [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187), [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194), [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201), [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208), [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230). | One identified requirement has seven explicit criteria. Wider requirement completeness is UNKNOWN. Human review remains pending. |
| [Background-session defect](01-intake.md#problem-description) | The seven criteria above and [sixteen proposed refinements](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md). | PARTIAL. Absent-credential recovery and reported workspace loss remain unresolved. Production applicability remains unknown. |

The requirement record does not establish an approved complete inventory of every affected behavior.
Therefore an overall requirement-to-criterion percentage is UNKNOWN.

### Final AC-to-test matrix: original requirement

The cases link definitions separately from assertion source and retained execution. Failure prevents later predicates from executing.

| Criterion and observable predicate | Canonical case | Assertion source | Result and gap |
| --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187): Mouse movement each 100 ms renews during 15 s | [E2E-01](06-test-cases.md#e2e-01) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/activity.cjs) | FAIL on candidate; inherited. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194): Keyboard activity each 100 ms renews during 15 s | [E2E-02](06-test-cases.md#e2e-02) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/activity.cjs) | FAIL on candidate; inherited. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201): Scroll activity each 100 ms renews during 15 s | [E2E-03](06-test-cases.md#e2e-03) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/activity.cjs) | FAIL on candidate; inherited. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208): Accepted activity crosses four controlled hours without fresh SSO | [FOUR-AC4-BROWSER](06-test-cases.md#four-ac4-browser) | [controlled browser assertions](evidence/four-checks-20261027/ac4-browser/run.mjs) | PARTIAL: controlled renewal and zero login requests/navigation pass. No complete direct fresh SSO prompt observer exists. [result](evidence/four-checks-20261027/ac4-browser/candidate-attempt-02/result.json). |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216): Pending manual renewal has zero successful closures | [E2E-04](06-test-cases.md#e2e-04) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-04.cjs) | PASS in local pending-renewal fixture. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223): Successful renewal closes exactly once | [E2E-04](06-test-cases.md#e2e-04) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-04.cjs) | PASS in local successful-renewal fixture. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230): Rejected renewal retains prompt and permits retry | [E2E-05](06-test-cases.md#e2e-05) | [browser assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-05.cjs) | PASS in local rejection fixture. [case outcome](evidence/four-checks-20261027/e2e/reconciliation.json). |

### Final AC-to-test matrix: proposed refinements

Each row names the defined predicates. The linked mapping retains direct assertion locations and result hashes.
Related guard cases remain in the code-to-test view. They are not substitutes for the criterion scenario.
PASS below concerns only the selected local fixtures. The production environment and business review remain outside that result.

| Criterion and selected predicates | Canonical cases | Assertions and execution | Result |
| --- | --- | --- | --- |
| [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01): session A refresh state is empty before the fresh-login response arrives | [OWN-04](06-test-cases.md#own-04), [OWN-05](06-test-cases.md#own-05), [DEL-01](06-test-cases.md#del-01) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx#L229); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/9b3a7c4631ae.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02): session B access and expiry remain unchanged; no error from the first request enters session B | [DEL-02](06-test-cases.md#del-02), [DEL-03](06-test-cases.md#del-03) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx#L313); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/10fdfdb6ea08.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03): session B access and expiry remain unchanged; session A completion records zero successful prompt closures; session A completion starts zero logout requests | [DEL-04](06-test-cases.md#del-04), [DEL-05](06-test-cases.md#del-05) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L288); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/48366ceda2d4.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04): zero automatic logout requests start; the returned access and expiry enter the current session; the prompt closes exactly once | [DEL-06](06-test-cases.md#del-06) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L315); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/d4937566e74d.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05): exactly one logout request starts; access and refresh state are empty | [DEL-07](06-test-cases.md#del-07) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L331); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/ebd7eb9be2b9.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06): access and refresh state are empty; persisted access is absent; the session error equals "Expired Session, please login again." | [OWN-07](06-test-cases.md#own-07), [DEL-08](06-test-cases.md#del-08), [DEL-12](06-test-cases.md#del-12) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L112); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/551751ad51fb.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07): its request carries the existing access and user identity; its caller receives the unchanged response data and status; its caller receives that rejection; the global error contains the service message; authentication state remains unchanged | [DEL-09](06-test-cases.md#del-09), [DEL-11](06-test-cases.md#del-11) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L71); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/dd9f335fa47b.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08): the caller receives the protected response; the rotated access remains installed; session A refresh credentials remain unchanged | [DEL-10](06-test-cases.md#del-10) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L85); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/91995878e5eb.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-09](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-09): current access and refresh state remain unchanged; the existing error notice remains unchanged; loading equals false | [DEL-13](06-test-cases.md#del-13) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L125); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/50b78229405f.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10): the caller receives ERR_CANCELED; loading equals false; authentication state remains unchanged | [DEL-14](06-test-cases.md#del-14) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/cancellationPreservation.test.ts#L13); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/00f0d80ad70b.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PARTIAL: access is preserved; refresh preservation is not explicitly asserted. |
| [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11): workspace A remains selected; the workspace identifiers remain A and B | [DEL-15](06-test-cases.md#del-15) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L27); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/b016a67999db.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12): the remaining available workspace becomes selected; stored workspace descriptors contain only that remaining workspace | [DEL-16](06-test-cases.md#del-16), [DEL-17](06-test-cases.md#del-17) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L36); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/47b11f238f34.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13): exactly one blank workspace remains; that workspace is selected; its label equals "Workspace 1"; its container list is empty | [DEL-18](06-test-cases.md#del-18) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L56); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/870a388ca242.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |
| [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14): exactly one activity renewal request exists; the original request remains uncanceled; that access enters session state; a protected validation request succeeds | [BROWSER-SHARING-PENDING](06-test-cases.md#browser-sharing-pending) | [sharing assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/deliveryConfidence.cjs#L69); [browser result](evidence/four-checks-20261027/e2e/reconciliation.json) | FAIL; two requests, expected one. |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15): loading remains true while request B remains pending; its caller receives the response; loading equals false; authentication state remains unchanged | [DEL-19](06-test-cases.md#del-19) | [inspected assertions](../../repos/ui/mfe-base/src/hooks/service/cancellationPreservation.test.ts#L37); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/ab64987775af.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PARTIAL: access is preserved; refresh preservation is not explicitly asserted. |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16): replacement refresh state remains installed; the expiry prompt remains visible with manual renewal available; no automatic logout request starts | [DEL-20](06-test-cases.md#del-20) | [inspected assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionTimingPreservation.test.tsx#L58); [result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/320c79e0331b.json); [all chains](evidence/renewed-review-20261027/traceability/corrected-traceability.json) | PASS in selected unit fixtures. |

### Final AC-to-code matrix

The proposed refinements use direct inspected source relationships. A mapping does not establish semantic conformance.

| Criterion | Changed implementation or required unchanged path | Conformance limit |
| --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | [DC-CH-09](#final-dc-ch-09) | Mouse debounce remains unchanged and postpones continuous renewal; FAIL. |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | No mapped changed implementation; required path is absent. | Keyboard renewal handler is absent; MISSING. |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | No mapped changed implementation; required path is absent. | Scroll renewal handler is absent; MISSING. |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | [DC-CH-05](#final-dc-ch-05), [DC-CH-09](#final-dc-ch-09) | Four-hour renewal and no-login-request/navigation controls pass. Fresh SSO prompt observation remains partial. |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | [DC-CH-01](#final-dc-ch-01), [DC-CH-05](#final-dc-ch-05) | Pending-renewal fixture passes; target behavior remains unverified. |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | [DC-CH-01](#final-dc-ch-01), [DC-CH-07](#final-dc-ch-07) | Successful-renewal fixture passes; target behavior remains unverified. |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | [DC-CH-01](#final-dc-ch-01), [DC-CH-06](#final-dc-ch-06) | Rejection and retry fixture passes; target behavior remains unverified. |
| [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01) | [DC-CH-03](#final-dc-ch-03), [DC-CH-04](#final-dc-ch-04), [DC-CH-07](#final-dc-ch-07), [DC-CH-08](#final-dc-ch-08), [DC-CH-11](#final-dc-ch-11) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02) | [DC-CH-06](#final-dc-ch-06), [DC-CH-07](#final-dc-ch-07), [DC-CH-08](#final-dc-ch-08), [DC-CH-11](#final-dc-ch-11) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03) | [DC-CH-01](#final-dc-ch-01), [DC-CH-02](#final-dc-ch-02), [DC-CH-05](#final-dc-ch-05), [DC-CH-07](#final-dc-ch-07) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04) | [DC-CH-01](#final-dc-ch-01), [DC-CH-02](#final-dc-ch-02), [DC-CH-05](#final-dc-ch-05), [DC-CH-09](#final-dc-ch-09) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05) | [DC-CH-01](#final-dc-ch-01), [DC-CH-02](#final-dc-ch-02), [DC-CH-05](#final-dc-ch-05) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06) | [DC-CH-01](#final-dc-ch-01), [DC-CH-06](#final-dc-ch-06), [DC-CH-07](#final-dc-ch-07), [DC-CH-10](#final-dc-ch-10), [DC-CH-11](#final-dc-ch-11) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07) | [DC-CH-04](#final-dc-ch-04), [DC-CH-06](#final-dc-ch-06), [DC-CH-07](#final-dc-ch-07), [DC-CH-08](#final-dc-ch-08) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08) | [DC-CH-03](#final-dc-ch-03), [DC-CH-11](#final-dc-ch-11) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-09](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-09) | [DC-CH-06](#final-dc-ch-06), [DC-CH-12](#final-dc-ch-12); inherited endpoint exclusions | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [DC-CH-04](#final-dc-ch-04), [DC-CH-06](#final-dc-ch-06), [DC-CH-07](#final-dc-ch-07), [DC-CH-08](#final-dc-ch-08), [DC-CH-12](#final-dc-ch-12) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11) | [DC-CH-09](#final-dc-ch-09) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12) | [DC-CH-09](#final-dc-ch-09) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13) | [DC-CH-09](#final-dc-ch-09) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14) | [DC-CH-09](#final-dc-ch-09), [unchanged extend helper](../../repos/ui/mfe-base/src/hooks/service/util/extend.ts) | FAIL: the helper aborts a prior pending extension. |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DC-CH-06](#final-dc-ch-06), [DC-CH-11](#final-dc-ch-11), [DC-CH-12](#final-dc-ch-12) | Selected mapping inspected; complete conformance remains unknown. |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [DC-CH-05](#final-dc-ch-05), [DC-CH-09](#final-dc-ch-09) | Selected mapping inspected; complete conformance remains unknown. |

### Final code-change-to-test matrix

Each row links a changed runtime path to direct assertion chains. Complete behavioral coverage remains unknown.
A path-linked test does not automatically assert every criterion listed in that row.
The [full mapping](evidence/renewed-review-20261027/traceability/corrected-traceability.json) lists each source hash and case checkpoint.

| Change and source | Linked proposed criteria | Direct canonical cases and assertion chain | Matching execution and gaps |
| --- | --- | --- | --- |
| <a id="final-dc-ch-01"></a>DC-CH-01; [source](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts) | [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03), [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04), [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05), [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06) | [DEL-04](06-test-cases.md#del-04), [DEL-05](06-test-cases.md#del-05), [DEL-06](06-test-cases.md#del-06), [DEL-07](06-test-cases.md#del-07), [DEL-08](06-test-cases.md#del-08), [FOUR-COV-01](06-test-cases.md#four-cov-01), [FOUR-COV-02](06-test-cases.md#four-cov-02), [FOUR-COV-03](06-test-cases.md#four-cov-03), [FOUR-COV-04](06-test-cases.md#four-cov-04), [FOUR-COV-05](06-test-cases.md#four-cov-05), [FOUR-COV-06](06-test-cases.md#four-cov-06), [FOUR-COV-10](06-test-cases.md#four-cov-10). Actual Home renders actual Timeout; actual relogin interceptors and reducers run. Assertions check pending UI, success closure, retry, deadline and logout. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/48366ceda2d4.json); complete behavior remains unknown. |
| <a id="final-dc-ch-02"></a>DC-CH-02; [source](../../repos/ui/mfe-base/src/components/Timeout/index.tsx) | [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03), [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04), [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05) | [DEL-04](06-test-cases.md#del-04), [DEL-05](06-test-cases.md#del-05), [DEL-06](06-test-cases.md#del-06), [DEL-07](06-test-cases.md#del-07). Actual rendered Extend/Logout controls invoke actual Timeout controller. DOM disabled/visible assertions and service counts establish those selected UI predicates. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/48366ceda2d4.json); complete behavior remains unknown. |
| <a id="final-dc-ch-03"></a>DC-CH-03; [source](../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts) | [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01), [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08) | [OWN-06](06-test-cases.md#own-06), [DEL-10](06-test-cases.md#del-10). Actual SET_TOKEN reducer runs after access rotation. Assertions check retained refresh, updated access and accepted same-session response. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/8b5f8f90ee78.json); complete behavior remains unknown. |
| <a id="final-dc-ch-04"></a>DC-CH-04; [source](../../repos/ui/mfe-base/src/hooks/service/config.ts) | [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01), [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07), [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [OWN-04](06-test-cases.md#own-04), [DEL-01](06-test-cases.md#del-01), [DEL-09](06-test-cases.md#del-09), [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19). Actual exported Axios client executes its registered synchronous interceptors. Immediate empty-refresh assertions check ownership timing; deferred adapter assertions check current request loading. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/9b3a7c4631ae.json); complete behavior remains unknown. |
| <a id="final-dc-ch-05"></a>DC-CH-05; [source](../../repos/ui/mfe-base/src/hooks/service/index.ts) | [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03), [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04), [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05), [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [PEND-01](06-test-cases.md#pend-01), [DEL-06](06-test-cases.md#del-06), [DEL-07](06-test-cases.md#del-07), [DEL-20](06-test-cases.md#del-20). Actual acquisition/relogin helpers call actual shared client with controlled transport. Assertions check pending promise settlement, credentials, recovery and prompt closure. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/0e22ba0afea2.json); complete behavior remains unknown. |
| <a id="final-dc-ch-06"></a>DC-CH-06; [source](../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts) | [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02), [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06), [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07), [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10), [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DEL-03](06-test-cases.md#del-03), [DEL-05](06-test-cases.md#del-05), [DEL-11](06-test-cases.md#del-11), [DEL-13](06-test-cases.md#del-13), [DEL-14](06-test-cases.md#del-14), [DEL-22](06-test-cases.md#del-22), [DEL-23](06-test-cases.md#del-23). Controlled adapter rejects through actual Axios error interceptor. Actual reducer/store assertions check preserved current identity, messages, loading and invalidation. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/425894cb62ef.json); complete behavior remains unknown. |
| <a id="final-dc-ch-07"></a>DC-CH-07; [source](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts) | [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01), [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02), [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03), [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06), [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07), [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [OWN-04](06-test-cases.md#own-04), [DEL-02](06-test-cases.md#del-02), [DEL-04](06-test-cases.md#del-04), [DEL-09](06-test-cases.md#del-09), [DEL-10](06-test-cases.md#del-10), [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-24](06-test-cases.md#del-24). Actual Axios success interceptor parses controlled responses and updates actual reducers. Assertions check stale rejection, access, refresh, returned payload, loading and parser-failure cleanup. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/9b3a7c4631ae.json); complete behavior remains unknown. |
| <a id="final-dc-ch-08"></a>DC-CH-08; [source](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts) | [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01), [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02), [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07), [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [OWN-04](06-test-cases.md#own-04), [OWN-05](06-test-cases.md#own-05), [DEL-01](06-test-cases.md#del-01), [DEL-09](06-test-cases.md#del-09), [DEL-21](06-test-cases.md#del-21). Actual synchronous request interceptor runs before service call returns. Assertions check immediately cleared old refresh, protected request headers and silent-request loading isolation. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/9b3a7c4631ae.json); complete behavior remains unknown. |
| <a id="final-dc-ch-09"></a>DC-CH-09; [source](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts) | [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04), [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11), [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12), [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13), [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14), [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [DEL-15](06-test-cases.md#del-15), [DEL-16](06-test-cases.md#del-16), [DEL-17](06-test-cases.md#del-17), [DEL-18](06-test-cases.md#del-18), [DEL-20](06-test-cases.md#del-20), [FOUR-COV-07](06-test-cases.md#four-cov-07), [FOUR-COV-08](06-test-cases.md#four-cov-08), [FOUR-COV-09](06-test-cases.md#four-cov-09), [BROWSER-SHARING-PENDING](06-test-cases.md#browser-sharing-pending). Actual Home hook/effects/handlers run. Real store and localStorage assertions check selected workspace and persistence. DEL-20 runs actual service and reducers around the delayed timer. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/b016a67999db.json); pending-sharing browser assertion fails. |
| <a id="final-dc-ch-10"></a>DC-CH-10; [source](../../repos/ui/mfe-base/src/utils/common.ts) | [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06) | [OWN-01](06-test-cases.md#own-01), [OWN-02](06-test-cases.md#own-02), [OWN-03](06-test-cases.md#own-03), [DEL-12](06-test-cases.md#del-12). Actual authentication cleanup increments epoch and clears store/persistence. Late controlled responses exercise actual stale guards; assertions check current credentials and rejected old data. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/a30bc6cbf8ad.json); complete behavior remains unknown. |
| <a id="final-dc-ch-11"></a>DC-CH-11; [source](../../repos/ui/mfe-base/src/utils/sessionEpoch.ts) | [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01), [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02), [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06), [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08), [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [OWN-06](06-test-cases.md#own-06), [OWN-07](06-test-cases.md#own-07), [DEL-02](06-test-cases.md#del-02), [DEL-03](06-test-cases.md#del-03), [DEL-10](06-test-cases.md#del-10), [DEL-22](06-test-cases.md#del-22). Actual epoch operations feed request/response guards. Same-session rotation and cross-session response/cancellation assertions distinguish access changes from session replacement. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/8b5f8f90ee78.json); complete behavior remains unknown. |
| <a id="final-dc-ch-12"></a>DC-CH-12; [source](../../repos/ui/mfe-base/src/hooks/service/util/requestLoading.ts) | [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10), [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19), [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-23](06-test-cases.md#del-23), [DEL-24](06-test-cases.md#del-24). Actual shared client executes actual loading registry and reducers. Assertions check final cleanup, overlapping work, silent work, epoch replacement and configless/parser failures. | [unit result](evidence/four-checks-20261027/coverage/test-only-final-2/cases/00f0d80ad70b.json); complete behavior remains unknown. |

The [user-directed backlog](evidence/user-input-20261027-backlog-scope.txt) retains inherited activity and sharing failures.
The earlier correction passes its direct unit tests. This does not prove zero impact across deployed consumers.
Owner: unknown application owner. Next action: review retained failures and complete target integration evidence.


<details>
<summary>Historical coverage before the final candidate</summary>

The following sections retain their recorded revisions and outcomes. They are historical, including prior failures and unavailable checks.
The current tables above supersede any current-state wording below.


## Unit remediation coverage: 27 October 2026

Candidate: `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303`. Base: `b8d4f1b837c6388452fbdc540f311257e805f932`.
The [patch binding](evidence/ut-remediation-20261027/proposal-v3-binding.json) identifies five runtime paths and one test path.
All 407 bound files match the application commit. [Evidence reconciliation](evidence/ut-remediation-20261027/evidence-reconciliation-v3.json) retains exact counts.
The inventories below contain three selected verification criteria and five changed runtime units.
They assess the UT correction. They do not replace the broader original requirement inventory below.

### AC-to-test: unit correction

| Criterion | Canonical cases | Direct assertions and passing execution | Limit |
| --- | --- | --- | --- |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19), [DEL-21](06-test-cases.md#del-21), [DEL-23](06-test-cases.md#del-23), [DEL-24](06-test-cases.md#del-24) | [Public-client assertions](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/cancellationPreservation.test.ts); [complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). | [Final DOM closure passes](evidence/ut-remediation-20261027/final-cancellation-browser/comparison.json). Missing configuration retains prior global cleanup semantics. |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DEL-22](06-test-cases.md#del-22), [DEL-02](06-test-cases.md#del-02), [DEL-03](06-test-cases.md#del-03) | [Cancellation ownership assertions](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/cancellationPreservation.test.ts#L110); [complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). | Ownership requires retained request configuration. |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [DEL-20](06-test-cases.md#del-20) | [Unchanged timer assertions](evidence/ut-remediation-20261027/proposal-sources/src/pages/Home/common/sessionTimingPreservation.test.tsx#L58); [complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). | Controlled equal-expiry state. [Default-lifetime variant passes](evidence/ut-remediation-20261027/final-timer-control/comparison.json). Natural jitter remains unmeasured. |

### AC-to-code-change: unit correction

| Criterion | Changed units and source | Reviewed behavior |
| --- | --- | --- |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [Loading registry](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/requestLoading.ts), [request handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/success.request.handler.ts), [success handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/succes.response.handler.ts), [error handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/error.response.handler.ts). | Final work clears loading. Other identified pending work retains loading. |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [Loading registry](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/requestLoading.ts), [request handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/success.request.handler.ts), [success handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/succes.response.handler.ts), [error handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/error.response.handler.ts). | Epoch transitions discard old tracking. Identified stale results cannot clear current loading. |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [Home scheduler](evidence/ut-remediation-20261027/proposal-v3-sources/src/pages/Home/common/useController.ts#L134). | Scheduled delivery bypasses only the lead-time cutoff. Other validity and visibility guards remain. |

### Code-change-to-test: unit correction

| Changed runtime unit | Direct assertion chain | Passing execution |
| --- | --- | --- |
| [Loading registry](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/requestLoading.ts) | Actual shared client, actual interceptors, actual store and reducers; [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19), [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-23](06-test-cases.md#del-23), [DEL-24](06-test-cases.md#del-24). | [Complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). |
| [Request handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/success.request.handler.ts) | The same public-client chain asserts pending loading, silent requests, and session replacement. [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-24](06-test-cases.md#del-24). | [Complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). |
| [Success handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/succes.response.handler.ts) | Controlled adapter completion invokes the actual success interceptor. [DEL-19](06-test-cases.md#del-19), [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-24](06-test-cases.md#del-24). | [Complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). |
| [Error handler](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/util/error.response.handler.ts) | Actual cancellation and transform rejection invoke the actual error interceptor. [DEL-14](06-test-cases.md#del-14), [DEL-22](06-test-cases.md#del-22), [DEL-23](06-test-cases.md#del-23). | [Complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). |
| [Home scheduler](evidence/ut-remediation-20261027/proposal-v3-sources/src/pages/Home/common/useController.ts#L134) | Actual Home, Timeout, service, and reducers assert recovery and zero logout. [DEL-20](06-test-cases.md#del-20). | [Complete result](evidence/ut-remediation-20261027/full-proposal-03/results.json). |

Selected criterion definitions, assertion mappings, changed-unit mappings, and passing UT evidence each cover 3/3 criteria.
Changed-unit direct assertion links cover 5/5 units. Complete behavioral coverage remains UNKNOWN/5 units.
All 461 discovered tests pass. Original 457 cases remain; four preservation cases were added.
These fractions establish neither complete requirement conformance nor measured line coverage.
The historical tables below retain the original comparison and its original failures.

## Scope and identities

Main: `f025513f696476a9cc8162681410cbd21e029bcb`.
Runtime candidate: `c42e7609c4e14eb53de32702e4bd3424a223988a`.
Comparison: full branch from the main merge base. The original selection contains thirty changed paths.
Eleven paths contain runtime changes. Twelve paths contain tests. Seven paths contain configuration or tooling support.
Later test-only changes retain the same runtime bytes. Final commit bindings appear in [the delivery report](10-delivery-confidence-20261026.md).
No remote tracking ref or deployed main artifact is bound.

Capability: Single UI authentication and workspace composition. Contracts: shared HTTP client and SSO token family.
The [current request](evidence/delivery-confidence-20261026/user-input.md#exact-user-input) authorizes expanded criteria, tests, and review.
The [requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains candidate version 5.
Its seven target predicates retain version 4 meaning. Publication review remains pending.
The additional sixteen criteria refine defect verification and preservation. They remain proposed, with human review pending.

## Requirement and criterion declarations

The [original requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) defines seven criteria.
The [additional criteria](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md) define sixteen bounded verification expectations.
The [exact mapping](evidence/delivery-confidence-20261026/unit/traceability.json) binds every additional criterion to assertions, hashes, and results.
The [canonical catalog](06-test-cases.md#delivery-confidence-cases-26-october-2026) owns the readable cases.
No passing test creates business approval.

## Coverage inventories and summary

`TC >= AC = Code Change` describes behavior coverage and equivalence. Artifact counts do not establish that relationship.
The tables keep definition, assertion, execution, implementation mapping, and conformance separate.

| Inventory and metric | Qualified / denominator | Evidence limit |
| --- | --- | --- |
| Original AC definitions with complete cases | 6/7 | Exact four-hour AC-4 remains unavailable. |
| Original ACs with inspected complete assertions | 6/7 | Partial duration checks cannot replace AC-4. |
| Original ACs with conforming source and qualified passing execution | 3/7 | AC-5, AC-6, and AC-7 pass. Three activity criteria fail. AC-4 remains unverified. |
| Original ACs mapped to changed implementation | 5/7 | Keyboard and scroll renewal handlers remain absent. |
| Proposed criteria with definitions | 16/16 | Human business review remains pending. |
| Proposed criteria with inspected assertion chains | 16/16 | A failed earlier assertion leaves later predicates unexecuted. |
| Proposed criteria with qualified passing execution | 13/16 | DC-AC-10 and DC-AC-16 regress. DC-AC-14 also fails on main. |
| Changed runtime paths inspected and mapped to selected assertions | 11/11 | This measures path reach, not complete behavior equivalence. |
| Changed runtime paths with complete behavior assertion coverage | UNKNOWN/11 | AC-4 and deployed consumer boundaries remain incomplete. |
| Changed runtime paths with complete passing behavior evidence | UNKNOWN/11 | Two regressions and incomplete inventories prevent a complete claim. |
| Instrumented line or branch coverage | NOT_MEASURED | Jest ran with coverage disabled. No coverage percentage is inferred. |

### AC-to-test coverage: original requirement

| Criterion | Canonical cases | Assertions and retained execution | Outcome |
| --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | [E2E-01](06-test-cases.md#e2e-01) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | FAIL; inherited continuous-mouse behavior |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | [E2E-02](06-test-cases.md#e2e-02) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | FAIL; keyboard handler missing on both refs |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | [E2E-03](06-test-cases.md#e2e-03) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | FAIL; scroll handler missing on both refs |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | [E2E-06](06-test-cases.md#e2e-06) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | PARTIAL; exact four-hour criterion NOT_VERIFIED |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | [E2E-04](06-test-cases.md#e2e-04), [PEND-01](06-test-cases.md#pend-01) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | PASS within pending-renewal fixture |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | [E2E-04](06-test-cases.md#e2e-04), [E2E-09](06-test-cases.md#e2e-09), [E2E-10](06-test-cases.md#e2e-10) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | PASS within successful-renewal fixtures |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | [E2E-05](06-test-cases.md#e2e-05), [PEND-02](06-test-cases.md#pend-02) | [Original assertion source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs); [current comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | PASS within rejection and retry fixtures |

### AC-to-test coverage: additional proposed criteria

| Criterion | Canonical cases | Inspected assertions | Retained execution | Outcome |
| --- | --- | --- | --- | --- |
| [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01) | [OWN-04](06-test-cases.md#own-04), [OWN-05](06-test-cases.md#own-05), [DEL-01](06-test-cases.md#del-01) | [OWN-04 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L235); [OWN-05 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L235); [DEL-01 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L301) | [OWN-04 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/9e9e57da5210.json); [OWN-05 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/a20f6f6ef143.json); [DEL-01 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/d97b5576e534.json) | PASS |
| [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02) | [DEL-02](06-test-cases.md#del-02), [DEL-03](06-test-cases.md#del-03) | [DEL-02 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L320); [DEL-03 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L320) | [DEL-02 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/fea527462346.json); [DEL-03 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/5777cfdd30d0.json) | PASS |
| [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03) | [DEL-04](06-test-cases.md#del-04), [DEL-05](06-test-cases.md#del-05) | [DEL-04 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L295); [DEL-05 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L295) | [DEL-04 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/7aa373ff5fc4.json); [DEL-05 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/77ca2e2cf71c.json) | PASS |
| [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04) | [PEND-01](06-test-cases.md#pend-01), [DEL-06](06-test-cases.md#del-06) | [PEND-01 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L152); [DEL-06 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L319) | [PEND-01 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/0a48b7166581.json); [DEL-06 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/92b92c89fea7.json) | PASS |
| [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05) | [DEL-07](06-test-cases.md#del-07) | [DEL-07 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L336) | [DEL-07 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/dbf8390c9989.json) | PASS |
| [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06) | [OWN-07](06-test-cases.md#own-07), [DEL-08](06-test-cases.md#del-08), [DEL-12](06-test-cases.md#del-12) | [OWN-07 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L271); [DEL-08 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionPending.test.tsx#L353); [DEL-12 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/sessionCompatibility.test.ts#L117) | [OWN-07 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/e93de9866bf9.json); [DEL-08 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/8f19c392c3e1.json); [DEL-12 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/58aa54594726.json) | PASS |
| [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07) | [DEL-09](06-test-cases.md#del-09), [DEL-11](06-test-cases.md#del-11) | [DEL-09 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/sessionCompatibility.test.ts#L74); [DEL-11 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/sessionCompatibility.test.ts#L105) | [DEL-09 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/628e875c60b7.json); [DEL-11 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/75205f94e20b.json) | PASS |
| [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08) | [OWN-06](06-test-cases.md#own-06), [DEL-10](06-test-cases.md#del-10) | [OWN-06 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionOwnership.test.tsx#L262); [DEL-10 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/sessionCompatibility.test.ts#L93) | [OWN-06 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/4a178088d463.json); [DEL-10 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/89f20acbf979.json) | PASS |
| [DC-AC-09](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-09) | [DEL-13](06-test-cases.md#del-13) | [DEL-13 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/sessionCompatibility.test.ts#L130) | [DEL-13 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/74ae43c966f1.json); [DEL-13 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/b5df8a1edbb1.json); [DEL-13 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/f9760938d84c.json) | PASS |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [DEL-14](06-test-cases.md#del-14) | [DEL-14 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/cancellationPreservation.test.ts#L28) | [DEL-14 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/8320607cf0ad.json) | FAIL |
| [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11) | [DEL-15](06-test-cases.md#del-15) | [DEL-15 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/workspacePreservation.test.tsx#L30) | [DEL-15 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/2cef20001513.json) | PASS |
| [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12) | [DEL-16](06-test-cases.md#del-16), [DEL-17](06-test-cases.md#del-17) | [DEL-16 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/workspacePreservation.test.tsx#L40); [DEL-17 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/workspacePreservation.test.tsx#L49) | [DEL-16 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/8fdac4344add.json); [DEL-17 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/7abe16c178d5.json) | PASS |
| [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13) | [DEL-18](06-test-cases.md#del-18) | [DEL-18 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/workspacePreservation.test.tsx#L62) | [DEL-18 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/fe87417c3ad3.json) | PASS |
| [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14) | [BROWSER-SHARING-PENDING](06-test-cases.md#browser-sharing-pending) | [BROWSER-SHARING-PENDING assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/deliveryConfidence.cjs#L69) | [BROWSER-SHARING-PENDING result](evidence/delivery-confidence-20261026/browser/candidate-headless/candidate-sharingPending-20261026T153346/case-summary.json) | FAIL on both refs; completion assertions NOT_REACHED |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DEL-19](06-test-cases.md#del-19) | [DEL-19 assertions](evidence/delivery-confidence-20261026/unit/sources/src/hooks/service/cancellationPreservation.test.ts#L54) | [DEL-19 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/a60496c2d561.json) | PASS |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [DEL-20](06-test-cases.md#del-20) | [DEL-20 assertions](evidence/delivery-confidence-20261026/unit/sources/src/pages/Home/common/sessionTimingPreservation.test.tsx#L70) | [DEL-20 result](evidence/delivery-confidence-20261026/unit/candidate-final-verified/cases/a3829c1c265e.json) | FAIL |

## Relationship evidence

### AC-to-code-change coverage

Each changed-path ID below resolves to its source, behavior, and direct assertion chain.
Required unchanged implementation remains distinct from changed implementation.

| Criterion | Changed implementation | Required unchanged path or missing implementation | Conformance |
| --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | [DC-CH-09](#dc-ch-09) | Mouse debounce and extension helper remain unchanged. | FAIL |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | No changed implementation | Keyboard renewal handler missing. | FAIL |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | No changed implementation | Scroll renewal handler missing. | FAIL |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | [DC-CH-05](#dc-ch-05), [DC-CH-09](#dc-ch-09) | Exact duration fixture missing. | NOT_VERIFIED |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | [DC-CH-01](#dc-ch-01), [DC-CH-05](#dc-ch-05) | BFF relogin validates refresh credentials. | PASS in declared fixture |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | [DC-CH-01](#dc-ch-01), [DC-CH-07](#dc-ch-07) | Returned access must remain usable. | PASS in declared fixture |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | [DC-CH-01](#dc-ch-01), [DC-CH-06](#dc-ch-06) | Existing server credential rejection remains. | PASS in declared fixture |
| [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01) | [DC-CH-03](#dc-ch-03), [DC-CH-07](#dc-ch-07), [DC-CH-08](#dc-ch-08), [DC-CH-11](#dc-ch-11) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02) | [DC-CH-07](#dc-ch-07), [DC-CH-08](#dc-ch-08), [DC-CH-11](#dc-ch-11) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03) | [DC-CH-01](#dc-ch-01), [DC-CH-05](#dc-ch-05), [DC-CH-07](#dc-ch-07), [DC-CH-11](#dc-ch-11) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04) | [DC-CH-01](#dc-ch-01), [DC-CH-05](#dc-ch-05) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05) | [DC-CH-01](#dc-ch-01) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06) | [DC-CH-06](#dc-ch-06), [DC-CH-07](#dc-ch-07), [DC-CH-10](#dc-ch-10), [DC-CH-11](#dc-ch-11) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07) | [DC-CH-04](#dc-ch-04), [DC-CH-06](#dc-ch-06), [DC-CH-07](#dc-ch-07), [DC-CH-08](#dc-ch-08) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08) | [DC-CH-03](#dc-ch-03), [DC-CH-07](#dc-ch-07), [DC-CH-11](#dc-ch-11) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-09](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-09) | [DC-CH-06](#dc-ch-06) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) | [DC-CH-04](#dc-ch-04), [DC-CH-06](#dc-ch-06) | No additional business policy is approved. | FAIL |
| [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11) | [DC-CH-09](#dc-ch-09) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12) | [DC-CH-09](#dc-ch-09) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13) | [DC-CH-09](#dc-ch-09) | Existing validateWorkspace fallback remains unchanged; Home adds a defensive guard. | Matches the inspected proposed fixture |
| [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14) | [DC-CH-09](#dc-ch-09) | Required sharing is in unchanged extend.ts; Home debounce remains unchanged. | FAIL |
| [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15) | [DC-CH-04](#dc-ch-04), [DC-CH-06](#dc-ch-06) | No additional business policy is approved. | Matches the inspected proposed fixture |
| [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16) | [DC-CH-01](#dc-ch-01), [DC-CH-05](#dc-ch-05), [DC-CH-09](#dc-ch-09) | No additional business policy is approved. | FAIL |

The new preservation failures remain separate from inherited activity and sharing failures.
Source conformance above concerns stated fixtures. Complete business acceptance remains pending.

## Inspected implementation and assertions

### Code-change-to-test coverage

These links come from inspected setup, invocation, and predicates. Shared criterion links alone do not establish test coverage.
All paths use the runtime candidate above. The [source manifest](evidence/delivery-confidence-20261026/claude/source-manifest.json) retains hashes.
The [unit mapping](evidence/delivery-confidence-20261026/unit/traceability.json) retains helper chains and per-case checkpoints.

| Change unit and exact source | Changed behavior | Direct cases and assertion chain | Evidence and limitation |
| --- | --- | --- | --- |
| <a id="dc-ch-01"></a>DC-CH-01; [useController.ts](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L23) | Pending credential settlement, renewal completion, retry, logout, and epoch guards. | [DEL-04](06-test-cases.md#del-04), [DEL-05](06-test-cases.md#del-05), [DEL-06](06-test-cases.md#del-06), [DEL-07](06-test-cases.md#del-07), [DEL-08](06-test-cases.md#del-08); Home/Timeout → relogin → actual interceptors → controlled adapter → real reducer and closure assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-02"></a>DC-CH-02; [index.tsx](../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L14) | Extend eligibility and explicit Logout availability. | [E2E-04](06-test-cases.md#e2e-04), [E2E-09](06-test-cases.md#e2e-09), [E2E-10](06-test-cases.md#e2e-10), [E2E-17](06-test-cases.md#e2e-17); Actual rendered controls and local BFF; detailed browser receipts retain execution scope. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-03"></a>DC-CH-03; [root0.reducers.ts](../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts#L6) | Preserve refresh credentials during ordinary access rotation. | [OWN-06](06-test-cases.md#own-06), [DEL-10](06-test-cases.md#del-10); SET_TOKEN dispatch → actual reducer → retained refresh and updated expiry assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-04"></a>DC-CH-04; [config.ts](../../repos/ui/mfe-base/src/hooks/service/config.ts#L18) | Stamp ownership synchronously at request creation. | [OWN-04](06-test-cases.md#own-04), [DEL-01](06-test-cases.md#del-01), [DEL-09](06-test-cases.md#del-09), [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19); Real Axios client/interceptors → request adapter → immediate state and cancellation predicates. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-05"></a>DC-CH-05; [index.ts](../../repos/ui/mfe-base/src/hooks/service/index.ts#L35) | Join acquisition, guard cleanup, expose pending settlement, and return relogin completion. | [PEND-01](06-test-cases.md#pend-01), [DEL-06](06-test-cases.md#del-06), [DEL-07](06-test-cases.md#del-07), [DEL-20](06-test-cases.md#del-20); Actual helper → controlled adapter → current credential and prompt assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-06"></a>DC-CH-06; [error.response.handler.ts](../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L7) | Ignore stale or cancelled work before current-state mutation. | [DEL-03](06-test-cases.md#del-03), [DEL-05](06-test-cases.md#del-05), [DEL-11](06-test-cases.md#del-11), [DEL-13](06-test-cases.md#del-13), [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19); Real error interceptor → reducer; final cancellation FAILS. Concurrent replacement control PASSES. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-07"></a>DC-CH-07; [succes.response.handler.ts](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L34) | Reject obsolete responses, validate relogin access, and reset fresh-login refresh state. | [OWN-04](06-test-cases.md#own-04), [DEL-02](06-test-cases.md#del-02), [DEL-04](06-test-cases.md#del-04), [DEL-09](06-test-cases.md#del-09), [DEL-10](06-test-cases.md#del-10); Real response interceptor → login handlers → reducer/persistence and stale-session assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-08"></a>DC-CH-08; [success.request.handler.ts](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L10) | Invalidate prior identity at fresh-login request start and stamp its epoch. | [OWN-04](06-test-cases.md#own-04), [OWN-05](06-test-cases.md#own-05), [DEL-01](06-test-cases.md#del-01), [DEL-09](06-test-cases.md#del-09); Real synchronous request interceptor → immediate refresh-empty and header assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-09"></a>DC-CH-09; [useController.ts](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L103) | Schedule lifecycle acquisition and refresh replacement; add workspace guards. | [DEL-15](06-test-cases.md#del-15), [DEL-16](06-test-cases.md#del-16), [DEL-17](06-test-cases.md#del-17), [DEL-18](06-test-cases.md#del-18), [DEL-20](06-test-cases.md#del-20), [E2E-15](06-test-cases.md#e2e-15); Actual Home effect and workspace handlers → real store. Delayed scheduled acquisition FAILS. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-10"></a>DC-CH-10; [common.ts](../../repos/ui/mfe-base/src/utils/common.ts#L72) | Invalidate the epoch before authentication cleanup. | [OWN-01](06-test-cases.md#own-01), [OWN-02](06-test-cases.md#own-02), [OWN-03](06-test-cases.md#own-03), [DEL-12](06-test-cases.md#del-12); Actual logout cleanup → state reset → old response rejection assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |
| <a id="dc-ch-11"></a>DC-CH-11; [sessionEpoch.ts](../../repos/ui/mfe-base/src/utils/sessionEpoch.ts#L1) | Represent session identity independently from access rotation. | [OWN-06](06-test-cases.md#own-06), [OWN-07](06-test-cases.md#own-07), [DEL-02](06-test-cases.md#del-02), [DEL-03](06-test-cases.md#del-03), [DEL-10](06-test-cases.md#del-10); Real epoch operations → request/response guards → current-state assertions. | [Unit assertions/results](evidence/delivery-confidence-20261026/unit/traceability.json); [browser receipts](evidence/delivery-confidence-20261026/browser/comparison.json). Complete boundary coverage remains limited. |

### Supporting and test-only changes

The original seven support paths contain four environment files, ESLint configuration, and two ignore files.
The [configuration evaluation](evidence/delivery-confidence-20261026/independent-review/build-config-effects.json) records their current consumers and limits.
Production-mode public-path selection uses loopback HTTP. The selected development remote has no inspected application import.
The body-limit parser reads one byte. No supported JSON-body business route was found in the static server.
These observations need target configuration binding. They establish no measured deployed failure.
Twelve original test paths and later test-only changes remain outside the eleven runtime-path denominator.
The [main assertion comparison](evidence/delivery-confidence-20261026/unit/main-assertion-comparison.json) records five legacy assertion differences.
Four differences concern missing exports in old mocks. One success fixture omits the required returned access credential.
The warning-mode diagnostic remains separate from a clean passing suite.

## Retained execution and verification

The [unit summary](evidence/delivery-confidence-20261026/unit/summary.json) identifies the final complete run and exact source bindings.
The final unit inventory contains 457 tests. Results: 455 pass and two fail.
Main's unchanged suite passes 317 tests. Its forced-exit limitation remains explicit.
The candidate exits naturally without forced termination. Open-handle diagnostics still identify delayed cleanup origins.
The [browser comparison](evidence/delivery-confidence-20261026/browser/comparison.json) separates current runs, historical reuse, and unavailable observations.
The [supplemental comparison](evidence/delivery-confidence-20261026/browser/supplemental-comparison.json) binds public-client cancellation and inherited sharing results.
The [Claude reconciliation](evidence/delivery-confidence-20261026/claude/claude-validation.md) separates accepted claims, rejected claims, and remaining limits.

## Coverage gaps

- Exact controlled-clock AC-4 remains unavailable. Its complete duration cannot be inferred from shorter boundary checks.
- Natural suspension reuses matching historical evidence. It is not counted as a fresh current execution.
- The absent-refresh observation is not rerun. It supplies no missing policy answer.
- Additional criteria remain proposed. No business review or publication approval is inferred.
- Deployed consumers, artifact identity, effective configuration, recovery, and operator records remain unavailable.
- Timer coincidence and callback lateness are controlled fixture conditions. Natural occurrence and frequency remain unmeasured.

## Facts, inferences, and unresolved questions

Facts: two preservation assertions pass on main and fail on the candidate.
Facts: the sharing probe fails after reaching its pending boundary on both revisions.
Inference: the two new source changes can cause the demonstrated consequences in matching deployed conditions.
Unknowns: deployed frequency, external final-cancellation callers, and natural coincident-expiry frequency.
These limits prevent a universal no-impact claim. They do not convert demonstrated failures into passing cases.

## Findings

| Finding | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Final cancellation retains loading. | A supported public-client call leaves PageLoader rendered. | unknown application owner | Pass [DEL-14](06-test-cases.md#del-14) while preserving [DEL-19](06-test-cases.md#del-19) and stale-session isolation. |
| Delayed scheduled acquisition loses recovery. | Equal credential expiry produces logout in the controlled candidate fixture. | unknown application owner | Pass [DEL-20](06-test-cases.md#del-20) and retain visibility/no-replay controls. |
| Full behavior equality remains incomplete. | A complete delivery conformance claim remains unsupported. | unknown application owner | Resolve failures and exact duration evidence within the agreed delivery scope. |

## Sources

- [Preserved user request](evidence/delivery-confidence-20261026/user-input.md#exact-user-input).
- [Additional criterion and assertion mapping](evidence/delivery-confidence-20261026/unit/traceability.json).
- [Independent full-branch review](evidence/delivery-confidence-20261026/independent-review/review.md).
- [Source and provider identities](evidence/delivery-confidence-20261026/claude/execution.json).
- [Supporting source bindings](evidence/delivery-confidence-20261026/codex-review/supporting-sources.json).

</details>
