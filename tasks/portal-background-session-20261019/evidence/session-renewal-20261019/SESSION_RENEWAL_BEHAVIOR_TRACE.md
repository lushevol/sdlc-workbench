---
artifact_kind: traceability-record
id: TRACE-active-session-renewal-pilot
version: 1
status: draft
owner: unknown
source_refs: [REQ-active-session-renewal-v2, SRC-pilot-ac4eca4f02906add, SRC-auth-stage-e0f59ba3eabb5a6d]
related_ids: [REQ-active-session-renewal, AC-5, AC-6, AC-7, mfe-base, single-ui-authentication, single-ui-web, single-ui-sso-token-family]
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

# Session renewal traceability pilot

## Scope and identities

- Capability IDs: single-ui-authentication.
- Requirement IDs: REQ-active-session-renewal, version 2.
- Repository IDs: mfe-base.
- Service and contract IDs: single-ui-web and single-ui-sso-token-family.
- Scope limit: AC-5 through AC-7 cover prompt completion and failure handling.
- Exclusions: AC-1 through AC-4, browser execution, backend behavior, and deployment.

## Requirement and criterion declarations

| Requirement ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| REQ-active-session-renewal | AC-5 | Pending renewal produces zero successful prompt closures | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-6 | Successful renewal closes the prompt exactly once after completion | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-7 | Rejected renewal produces zero successful closures and permits retry | document-version:2 | candidate; pending |

| Behavior ID | Version | Criterion ID | Actor | Required verification level | Negative case |
| --- | --- | --- | --- | --- | --- |
| REQ-active-session-renewal:BEH-05 | 1 | AC-5 | Portal user | browser_backend | BEH-07 |
| REQ-active-session-renewal:BEH-06 | 1 | AC-6 | Portal user | browser_backend | BEH-07 |
| REQ-active-session-renewal:BEH-07 | 1 | AC-7 | Portal user | browser_backend | rejected request |

The inventory preserves each complete Given, When, Then, and measurement declaration.

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| REQ-active-session-renewal | has criterion | AC-5 | knowledge/candidates/requirements/REQ-active-session-renewal.md#L90-L98 | declaration; CONFIRMED | Candidate intent |
| AC-5 | mapped source predicate | TEST-harness-timeout-pending-success | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | inspected mapping; CONFIRMED | Controlled predicate only |
| TEST-harness-timeout-pending-success | asserts through | ASSERT-session-renewal-pending | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | inspected assertion | Browser and backend excluded |
| REQ-active-session-renewal | has criterion | AC-6 | knowledge/candidates/requirements/REQ-active-session-renewal.md#L99-L107 | declaration; CONFIRMED | Candidate intent |
| AC-6 | mapped source predicate | TEST-harness-timeout-pending-success | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | inspected mapping; CONFIRMED | Controlled predicate only |
| TEST-harness-timeout-pending-success | asserts through | ASSERT-session-renewal-success | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | inspected assertion | Browser and backend excluded |
| REQ-active-session-renewal | has criterion | AC-7 | knowledge/candidates/requirements/REQ-active-session-renewal.md#L108-L116 | declaration; CONFIRMED | Candidate intent |
| AC-7 | mapped source predicate | TEST-harness-timeout-rejection-retry | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L218-L225 | inspected mapping; CONFIRMED | Controlled predicate only |
| TEST-harness-timeout-rejection-retry | asserts through | ASSERT-session-renewal-retry | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L218-L225 | inspected assertion | Browser and backend excluded |

## Inspected implementation and assertions

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-5 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | src/components/Timeout/common/useController.ts#L58-L71; src/hooks/service/index.ts#L35-L46 | TEST-harness-timeout-pending-success | sha256:c7c84a92ca652ca5e70d704fe357662dd944a2521ff8cbf823568d6b9a23dc4d | ASSERT-session-renewal-pending; knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | Before promise resolution, loading is true and the close list remains empty. |
| AC-6 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | src/components/Timeout/common/useController.ts#L58-L71; src/hooks/service/index.ts#L35-L46 | TEST-harness-timeout-pending-success | sha256:c7c84a92ca652ca5e70d704fe357662dd944a2521ff8cbf823568d6b9a23dc4d | ASSERT-session-renewal-success; knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | After controlled request success, the close list equals [false] and loading is false. |
| AC-7 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | src/components/Timeout/common/useController.ts#L58-L71; src/hooks/service/index.ts#L35-L46 | TEST-harness-timeout-rejection-retry | sha256:c7c84a92ca652ca5e70d704fe357662dd944a2521ff8cbf823568d6b9a23dc4d | ASSERT-session-renewal-retry; knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L218-L225 | Rejected renewal keeps the close list empty; a controlled successful retry closes once. |

Jest cases have inspected assertions at the selected commit.
Their retained execution state remains NOT_RUN.

| Criterion ID | Jest assertion location | Execution state |
| --- | --- | --- |
| AC-5 | src/components/Timeout/common/useController.test.tsx#L82-L95 | NOT_RUN |
| AC-6 | src/components/Timeout/common/useController.test.tsx#L82-L95 | NOT_RUN |
| AC-7 | src/components/Timeout/common/useController.test.tsx#L98-L116 | NOT_RUN |

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-5 | ASSERT-session-renewal-pending | EXEC-session-renewal-committed-characterization | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Controlled predicate PASSED | PASSED | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json; Timeout stays open while pending and closes after success | Business behavior NOT_VERIFIED; React, browser, and backend excluded |
| AC-6 | ASSERT-session-renewal-success | EXEC-session-renewal-committed-characterization | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Controlled predicate PASSED | PASSED | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json; Timeout stays open while pending and closes after success | Business behavior NOT_VERIFIED; React, browser, and backend excluded |
| AC-7 | ASSERT-session-renewal-retry | EXEC-session-renewal-committed-characterization | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Controlled predicate PASSED | PASSED | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json; Timeout rejection remains retryable and successful retry clears expiry timer | Business behavior NOT_VERIFIED; React, browser, and backend excluded |

The pending and success fixtures omit a refreshToken value.
The retry fixture uses controlled refresh credentials.
These limits prevent complete verification of the requirement conditions.
The result omits a harness hash.
The manifest and matching check names link the retained harness to the result.

The inventory records each fixture, invocation, helper chain, result pointer, and test level.
Three selected behaviors have inspected implementation links.
Three selected behaviors have controlled assertion results.
Zero selected behaviors have required browser/backend execution or human approval.
These metrics use three selected behaviors as their denominator.
The complete requirement declares seven criteria.

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| GAP-human-review | knowledge/candidates/requirements/REQ-active-session-renewal.md#frontmatter | Candidate intent cannot support approved behavior verification. | unknown | Record authorized human review of all seven criteria. |
| GAP-jest-execution | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json#limits | Inspected Jest assertions have no retained matching runner result. | unknown | Execute the saved Jest cases in a provisioned repository. |
| GAP-browser-backend-execution | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json#limits | Browser, token validity, backend renewal, and four-hour behavior remain unverified. | unknown | Execute applicable scenarios in the supported business environment. |
| GAP-usable-refresh-condition | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216 | Pending and success harness fixtures omit the usable-refresh-token condition. | unknown | Add a relevant integration fixture in the owning business repository. |
| GAP-original-test-byte-binding | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json#source_sha256 | The result records implementation hashes but omits its original harness hash. | unknown | Retain original harness and configuration hashes in future execution records. |

## Facts, inferences, and unresolved questions

- Facts: All five committed execution source hashes match the selected Git revision.
- Facts: The older retained result has one stale Timeout source hash.
- Facts: Both historical result files remain unchanged.
- Inferences: Matching hashes support reuse only for the disclosed controlled predicates.
- Unresolved questions: Business ownership, full human review, and supported environment execution remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Drift checks](../evidence/skill-adoption/pilot-drift-checks.json) retain one historical mismatch | The older pass cannot verify the selected source bytes | unknown | Use matching committed evidence; retain the older result |
| Three selected criteria have controlled assertion results | Zero selected criteria have recorded approval or browser/backend execution | unknown | Complete human review and supported environment execution |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-renewal-intent-2026-10-15 | knowledge/raw/session-renewal-intent-2026-10-15.txt | request-2026-10-15 | d3976f80aaeba02b2397d9731a142767225d2a3ee6dcd1a2de351d3d748217e9 | unknown; Retained agent evidence; no human approval or business execution. |
| SRC-session-activity-and-idle-intent | knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt | reply-2026-10-15 | a9654884d2ff9f2f27a3185268b251694b51145d50aa7bee6ab2d75c911e90e3 | unknown; Retained agent evidence; no human approval or business execution. |
| SRC-pilot-ac4eca4f02906add | knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | c7c84a92ca652ca5e70d704fe357662dd944a2521ff8cbf823568d6b9a23dc4d | unknown; Retained agent evidence; no human approval or business execution. |
| SRC-pilot-fc8e4d4a5788f1d3 | knowledge/raw/execution/session-renewal-pilot-2026-10-15/mfe-session-pilot-characterization-root-result.json | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 85c042b8f8cce4202aaefa19cadc2cafe18857557a7d0a6a1fa9e65507351ff5 | unknown; Retained agent evidence; no human approval or business execution. |
| SRC-auth-stage-e0f59ba3eabb5a6d | knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 8ffc1eb5ebf798c9eb2793447127e852eb7dd7c2dc73749482a35311d3649fe8 | unknown; Retained agent evidence; no human approval or business execution. |
| SRC-code-e9cbeed1e6e9e41eefa0 | knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 9c9fed8b70bb8a5913210663a11974928d167b4e8676bf413483f3101db2c2b1 | unknown; Exact supplied Git bytes; source owner unknown. |
| SRC-code-052150dd1cefc2cc9f1b | knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 72182d3bb36584e00982377e0137dd6effb527a4c2a24a8ffd89fcaf44b6cf13 | unknown; Exact supplied Git bytes; source owner unknown. |
| SRC-code-9ca360db38625ec7f8d1 | knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | b6f04007994e2a77f1952cb7a4829f57bb5e7e6818ca40d03b4f6f21940dae79 | unknown; Exact supplied Git bytes; source owner unknown. |
| REQ-active-session-renewal-v2 | knowledge/candidates/requirements/REQ-active-session-renewal.md | document-version:2 | 572528b0a218e20e8ccbbbf4c07a9efc2be4a66302520b957ea0b80a0fbcb4d3 | unknown; Candidate requested intent; full requirement review remains pending. |
