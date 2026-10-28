---
artifact_kind: test-execution-report
id: EXEC-comprehensive-session-renewal
version: 1
status: draft
owner: unknown
source_refs: [SRC-comprehensive-renewal-20261028]
related_ids: [REQ-active-session-renewal, PLAN-comprehensive-session-renewal]
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

# Session renewal: focused execution and assertion coverage

> **The separate security probe reproduced an inherited logout revocation defect.**
> Action: correct [SEC-01](07-security-review-renewal.md#sec-01) before security acceptance.
> Consequence: frontend passes cannot establish complete logout revocation. Owner: unknown authentication owner.
> Evidence: [failed replay assertion](evidence/comprehensive-renewal-20261028/expired-logout-case.json).

> **Critical conclusions: Broad security and target acceptance remain unverified.**
> Action: execute the proposed transport and target security cases before acceptance. Consequence: these local passes cannot establish absolute security.
> Owner: unknown application and security owners. Evidence: [execution limits](evidence/comprehensive-renewal-20261028/assertion-map.json).
>
> **The current source does not implement all three continuous activity targets.**
> Action: preserve the recorded backlog disposition and complete those targets when scheduled.
> Consequence: passing renewal recovery tests do not establish activity conformance. Owner: unknown application owner.
> Evidence: [criterion comparison](evidence/comprehensive-renewal-20261028/assertion-map.json).

## Run identity and provenance

The [user request](evidence/user-input-20261028-comprehensive-renewal.txt) authorizes case generation and a security assessment.
The [bounded stage](05-test-strategy-renewal.md#entry-and-completion-conditions) authorizes isolated local verification.
Execution used immutable committed source. Existing business worktree edits were excluded and preserved.
The counts below cover the frontend unit and browser selection. The separate controller security suite has one failed case.
See the [security execution](07-security-review-renewal.md#security-verification) and [combined coverage](09-renewal-coverage.md).

```yaml
execution_id: comprehensive-renewal-20261028
execution_status: COMPLETED
repository_id: mfe-base
repository_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
test_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
environment_identity: local-source-bound-portal-and-synthetic-authentication
started_at: "2026-10-28T15:50:32.388000+00:00"
completed_at: "2026-10-28T15:57:35.560Z"
command_or_tool_reference: evidence/comprehensive-renewal-20261028/run-local-browser.py
process_exit_status: 0
actual_results:
  unit_passed: 157
  unit_total: 157
  unit_suites: 10
  new_browser_passed: 3
  new_browser_total: 3
  browser_assertions: 56
  failed: 0
  skipped: 0
  unit_runner_errors: 0
retained_execution_refs:
  - evidence/comprehensive-renewal-20261028/focused-unit-results.json
  - evidence/comprehensive-renewal-20261028/loading-workspace-unit-results.json
  - evidence/comprehensive-renewal-20261028/new-e2e-summary.json
```

These results cover the declared selection. The full application unit suite was not rerun.
[Unit execution metadata](evidence/comprehensive-renewal-20261028/unit-execution.json) retains commands, suite identities, counts, timestamps, and result hashes.
The first browser attempt failed during fixture setup. It remains retained and does not establish an application defect.
See [the setup diagnosis](evidence/comprehensive-renewal-20261028/browser-attempt1/fixture-failure.json) and [initial results](evidence/comprehensive-renewal-20261028/browser-attempt1/new-e2e-summary.json).

## Browser environment and suite completeness

- Additional case inventory: [new canonical definitions](06-test-cases.md#rn-x001), [rapid clicks](06-test-cases.md#rn-x002), and [pending logout](06-test-cases.md#rn-x003).
- Final additional results: three passed, zero failed, zero skipped, zero blocked.
- Original broad business cases: not rerun in this stage. Their historical results retain their original source bindings.
- Browser: Microsoft Edge 156.0.4314.50, headless Chromium, macOS, isolated context per case.
- [Launch arguments](evidence/comprehensive-renewal-20261028/new-e2e-summary.json) disable update and background network facilities.
- Clock: controlled browser time. Expiry advances use fast-forward. This does not reproduce physical device suspension.
- Composition: actual portal shell, Home, Timeout, Axios, provider, reducers, and workspace descriptor flows.
- Substitutions: existing local BFF identity fixture, toolkit replacement, synthetic renewal credentials, and synthetic authentication responses.
- Workspace scope: three empty workspace descriptors. Embedded application state and real application transactions remain untested.
- [Source maps](evidence/comprehensive-renewal-20261028/served-source-binding.json) match all twelve changed runtime paths and the unchanged Home view.
- [Final integrity and cleanup](evidence/comprehensive-renewal-20261028/execution-cleanup.json) records zero modified snapshot sources and stopped test services.

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [RN-X001](06-test-cases.md#rn-x001) | [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | [Runner](evidence/comprehensive-renewal-20261028/renewal-loop-e2e.mjs) | Six failure/retry/success cycles preserve three workspace IDs | 44 assertions passed; 12 renewal requests | PASSED | [Result](evidence/comprehensive-renewal-20261028/rn-x001/result.json) |
| [RN-X002](06-test-cases.md#rn-x002) | [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | [Runner](evidence/comprehensive-renewal-20261028/renewal-loop-e2e.mjs) | 25 click events produce one held renewal and one closure | Eight assertions passed | PASSED | [Result](evidence/comprehensive-renewal-20261028/rn-x002/result.json) |
| [RN-X003](06-test-cases.md#rn-x003) | Proposed session ownership invariant | [Runner](evidence/comprehensive-renewal-20261028/renewal-loop-e2e.mjs) | Logout clears access despite late renewal completion | Four assertions passed | PASSED | [Result](evidence/comprehensive-renewal-20261028/rn-x003/result.json) |
| Selected existing component and service assertions | Renewal, ownership, timing, workspace, and loading boundaries | [Exact mapping](evidence/comprehensive-renewal-20261028/assertion-map.json) | All 157 selected tests pass | 157 tests passed across ten suites | PASSED | [Session results](evidence/comprehensive-renewal-20261028/focused-unit-results.json), [loading/workspace results](evidence/comprehensive-renewal-20261028/loading-workspace-unit-results.json) |

## Coverage inventories and summary

The intent inventory contains seven target criteria in requirement version five.
The [assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) records exact requirement bytes, line ranges, sources, and test hashes.
The comparison includes twelve runtime paths between the recorded baseline and candidate commits.
This path inventory does not count every changed atomic predicate.
Tests and configuration changes remain visible through the Git comparison. They are outside this runtime-path denominator.

| Metric | Qualified / total | Meaning and limit |
| --- | --- | --- |
| AC with inspected direct assertion definitions | 7 / 7 | Assertions exist for each exact target. This does not establish passing execution. |
| AC with complete matching selected execution | 3 / 7 | Manual recovery targets pass in the disclosed synthetic-credential boundary. |
| AC with partial execution | 1 / 7 | The initial refresh-expiry boundary passes component checks. A new exact four-hour browser run was not executed. |
| Changed runtime paths with a selected direct assertion chain | 12 / 12 | At least one inspected chain per path. Complete branch and predicate coverage remain unknown. |
| Changed runtime paths with full predicate execution | UNKNOWN / 12 | Full changed-predicate inventory remains unavailable. |
| Broader security behavior verified | UNKNOWN | An approved complete security acceptance inventory is unavailable. |

### AC to test case coverage

| Target criterion | Canonical case | Direct assertion evidence | Matching execution | Gap and limit |
| --- | --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | [E2E-01](06-test-cases.md#e2e-01) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | NOT_RUN | Continuous mouse debounce prevents the exact target. |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | [E2E-02](06-test-cases.md#e2e-02) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | NOT_RUN | No keyboard renewal binding exists. |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | [E2E-03](06-test-cases.md#e2e-03) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | NOT_RUN | No scroll renewal binding exists. |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | [E2E-04](06-test-cases.md#e2e-04) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | PARTIAL | Exact new four-hour browser interval remains NOT_RUN. |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | [RN-X002](06-test-cases.md#rn-x002) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | PASSED | Synthetic credentials; provider and target behavior remain unverified. |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | [RN-X002](06-test-cases.md#rn-x002) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | PASSED | Synthetic credentials; provider and target behavior remain unverified. |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | [RN-X001](06-test-cases.md#rn-x001) | [Exact assertion locations and hashes](evidence/comprehensive-renewal-20261028/assertion-map.json) | PASSED | Synthetic credentials; provider and target behavior remain unverified. |

### AC to code change coverage

| Target criterion | Changed or unchanged source | Conformance | Evidence and limit |
| --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | Home activity binding and service extension | CONTRADICTORY | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | Home activity binding and service extension | MISSING | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | Home activity binding and service extension | MISSING | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | Home reconciliation and refresh acquisition | PARTIAL | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | Timeout completion guards and renewal response validation | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | Timeout completion guards and renewal response validation | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | Timeout completion guards and renewal response validation | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | [Exact old/new source hashes](evidence/comprehensive-renewal-20261028/assertion-map.json); accepted target policy remains separate |

### Code change to test case coverage

Baseline: `f025513f696476a9cc8162681410cbd21e029bcb`.
Candidate: `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
Each row identifies a selected direct assertion chain. No row establishes complete predicate coverage.

| Change ID | Changed runtime path | Assertion chain | Matching selection | Limit |
| --- | --- | --- | --- | --- |
| CH-RN-01 | `src/components/Timeout/common/useController.ts` | PEND-01/PEND-02/PEND-08 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-02 | `src/components/Timeout/index.tsx` | PEND-07/PEND-08 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-03 | `src/hooks/reducer/root0.reducers.ts` | OWN-01/OWN-02 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-04 | `src/hooks/service/config.ts` | DEL-14/DEL-19 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-05 | `src/hooks/service/index.ts` | pending-sharing/retry/replacement | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-06 | `src/hooks/service/util/error.response.handler.ts` | OWN-03 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-07 | `src/hooks/service/util/requestLoading.ts` | DEL-14/DEL-19/DEL-21/DEL-22/DEL-23/DEL-24 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-08 | `src/hooks/service/util/succes.response.handler.ts` | PEND-03/PEND-04/PEND-05/PEND-06 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-09 | `src/hooks/service/util/success.request.handler.ts` | OWN-08/OWN-09 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-10 | `src/pages/Home/common/useController.ts` | SR11 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-11 | `src/utils/common.ts` | OWN-01/OWN-02/OWN-03 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |
| CH-RN-12 | `src/utils/sessionEpoch.ts` | OWN-01/OWN-02/OWN-03 | [Exact mapping and retained result](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected predicates only; full equivalence unknown |

## Retained evidence inventory

| Evidence | Locator | Integrity or availability limit |
| --- | --- | --- |
| Pinned source and dependency paths | [Source binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json) | SHA-256 values identify exact archived bytes; existing dependencies were reused |
| Served module source | [Map binding](evidence/comprehensive-renewal-20261028/served-source-binding.json) | Thirteen selected source files match; no production artifact claim |
| Unit selections | [Session suite](evidence/comprehensive-renewal-20261028/focused-unit-results.json), [loading/workspace suite](evidence/comprehensive-renewal-20261028/loading-workspace-unit-results.json) | Complete declared selections; full suite not rerun |
| New browser suite | [Summary](evidence/comprehensive-renewal-20261028/new-e2e-summary.json) | Three cases; final source and runner hashes retained |
| First setup failure | [Diagnosis](evidence/comprehensive-renewal-20261028/browser-attempt1/fixture-failure.json) | Synthetic access reached the real fixture validator before route correction |
| Cleanup | [Completion](evidence/comprehensive-renewal-20261028/execution-cleanup.json) | Only stage-owned process groups stopped |

## Browser evidence bindings

| Case and phase | Screenshot | Request and assertion evidence | Supported claim and limit |
| --- | --- | --- | --- |
| [RN-X001](06-test-cases.md#rn-x001), six cycles complete | [Capture](evidence/comprehensive-renewal-20261028/rn-x001/six-cycles-complete.png) | [Result and hash](evidence/comprehensive-renewal-20261028/rn-x001/result.json) | Shell remains authenticated after bounded cycles; empty workspace descriptors only |
| [RN-X002](06-test-cases.md#rn-x002), held renewal | [Capture](evidence/comprehensive-renewal-20261028/rn-x002/pending-after-rapid-clicks.png) | [Result and hash](evidence/comprehensive-renewal-20261028/rn-x002/result.json) | Actual pending dialog remains visible; synthetic service response |
| [RN-X002](06-test-cases.md#rn-x002), successful renewal | [Capture](evidence/comprehensive-renewal-20261028/rn-x002/held-renewal-complete.png) | [Result and hash](evidence/comprehensive-renewal-20261028/rn-x002/result.json) | Installed access and closure assertions pass; provider validation bypassed |
| [RN-X003](06-test-cases.md#rn-x003), logout during pending | [Capture](evidence/comprehensive-renewal-20261028/rn-x003/logout-during-pending.png) | [Result and hash](evidence/comprehensive-renewal-20261028/rn-x003/result.json) | Logout remains available during held recovery |
| [RN-X003](06-test-cases.md#rn-x003), logged out | [Capture](evidence/comprehensive-renewal-20261028/rn-x003/logged-out.png) | [Result and hash](evidence/comprehensive-renewal-20261028/rn-x003/result.json) | Late delivery cannot restore local access; global server revocation untested |

Each result records the actual capture timestamp and SHA-256. Screenshots complement the explicit state and request assertions.

## Verification conclusion

The declared unit selection passes all 157 tests. The three new browser cases pass all 56 explicit assertions.
These results support bounded manual recovery, retry, click deduplication, workspace descriptor preservation, and logout ownership.
They do not prove embedded workspace data retention, actual transport behavior, deployment compatibility, or complete security.
Continuous mouse, keyboard, and scroll targets still lack conforming implementation. Their recorded backlog direction remains unchanged.
Behavioral equality is `NOT_ESTABLISHED` for the complete requirement and security scope.

## Facts, inferences, and unresolved questions

The [source binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json) identifies all excluded worktree edits.
The source maps and unchanged snapshot hashes establish the selected frontend execution identity.
Source maps cannot authenticate a production artifact or deployment composition.
Transport policy, representative workload limits, and global revocation acceptance require additional evidence and owner review.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Activity comparison](evidence/comprehensive-renewal-20261028/assertion-map.json) | Existing continuous activity targets remain unmet | unknown application owner | Preserve backlog direction and verify the exact target when implemented |
| [Execution limits](evidence/comprehensive-renewal-20261028/new-e2e-summary.json) | Synthetic local passes cannot establish target security | unknown security owner | Run approved real-provider and transport cases in an isolated representative target |
| [Initial fixture diagnosis](evidence/comprehensive-renewal-20261028/browser-attempt1/fixture-failure.json) | Initial browser attempt did not execute intended recovery assertions | unknown verification owner | Use the corrected route fixture; retain the failed attempt |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-comprehensive-renewal-20261028 | [Exact user request](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | c82745858b57709daa801bd5730939b076123ec630ecfe3ff581d2b6db1001e4 | User; case generation and assessment authorization |
| REQ-active-session-renewal | [Candidate target](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) | version 5 | 3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359 | unknown owner; publication review pending |
| SRC-renewal-runtime | [Immutable source binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json) | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf` | Per-file hashes in manifest | Local candidate only; dirty edits excluded |
| SRC-renewal-assertions | [Direct map](evidence/comprehensive-renewal-20261028/assertion-map.json) | candidate and test-engine revisions within map | Per-file hashes in map | Inspected exact assertions; complete business equivalence remains unknown |
