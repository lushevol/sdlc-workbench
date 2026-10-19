---
artifact_kind: traceability-record
id: TRACE-session-renewal-correction-20261020
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-renewal-clarification-20261020
  - SRC-MFE-session-correction-4da985a
  - SRC-session-renewal-integrated-run002
  - SRC-session-renewal-e2e-source
  - SRC-session-e2e-final-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - REPORT-portal-task-evidence-review-20261019
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

# Session renewal behavior and E2E coverage

## Scope and identities

This report compares seven requirement criteria with the corrected source, inspected assertions, and retained execution.
It succeeds the earlier [verification detail](verification.md) for this correction stage.
Earlier browser runs remain evidence of the original local failure.
They do not establish corrected behavior.

- Requirement: [REQ-active-session-renewal v4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md), AC-1–AC-7.
- Defect: [DEFECT-portal-background-session-20261019](intake.md), scoped correction readiness `READY`.
- Repositories: `mfe-base`, `single-ui-bff`, and `ratan-test-engine`.
- MFE comparison: `2af6b83a08b072014e08ea37ec6d333c4aaab2b3` → `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.
- E2E commit: `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`, based on `62f1685a609bce6735bb0c9cec5fe0ee4311e194`.
- BFF inspection: `85d7cc03eb12710d6facf581987fd4ae24fc9844`. No BFF source changed.
- Capability: `single-ui-authentication`. Contracts: `single-ui-sso-token-family` and `single-ui-shared-http`.
- Exclusions: PROD confirmation, cross-origin application activity, application-edit retention, and recovery without usable credentials.

The user confirmed continuous eligible renewal and authorized these corrections.
The requirement remains a candidate. Publication review remains pending.
Risk is medium because request completion can race expiry, logout, and credential rotation.

## Requirement and criterion declarations

Behavior IDs use the prefix `REQ-active-session-renewal:BEH-`.
The suffix matches the criterion number.
Behaviors 01–03 and 05–07 retain version 1. Behavior 04 uses version 2 after the clarification.

| Criterion | Measurable behavior | Intent source | Review state |
| --- | --- | --- | --- |
| AC-1 | Repeated mouse activity produces successful renewal within the controlled 15-second interval. | Requirement v4; original user intent. | Candidate; pending publication. |
| AC-2 | Repeated keyboard activity produces successful renewal within the controlled 15-second interval. | Requirement v4; original user intent. | Candidate; pending publication. |
| AC-3 | Repeated scroll activity produces successful renewal within the controlled 15-second interval. | Requirement v4; original user intent. | Candidate; pending publication. |
| AC-4 | Four controlled activity hours cross initial refresh expiry with zero elapsed-time-only SSO prompts. | Requirement v4; clarification Q-010. | Candidate; pending publication. |
| AC-5 | Pending eligible renewal causes zero successful prompt closures. | Requirement v4, unchanged AC-5. | Candidate; pending publication. |
| AC-6 | Successful eligible renewal closes the prompt exactly once after completion. | Requirement v4, unchanged AC-6. | Candidate; pending publication. |
| AC-7 | Rejected renewal causes zero successful closures and permits another attempt. | Requirement v4, unchanged AC-7. | Candidate; pending publication. |

These intervals are fixtures. They introduce no production timeout value.

## Relationship evidence

| From | Relationship | To | Evidence class and grade | Limit |
| --- | --- | --- | --- | --- |
| User clarification Q-010 | Defines | AC-4 behavior version 2 | Documented intent; CONFIRMED. | No publication approval or execution proof. |
| AC-1–AC-4 | Implemented through | Home activity and extension paths | Inspected implementation; CONFIRMED. | Local native-browser predicates pass; deployed service behavior remains unknown. |
| AC-5–AC-7 | Implemented through | Timeout → relogin → response handler | Inspected implementation; CONFIRMED. | Transport and time are controlled in component tests. |
| Seven criteria | Asserted through | Controlled component tests | Inspected assertions; CONFIRMED. | Component assertions do not establish E2E coverage. |
| New E2E cases | Call through | Browser extension → actual configured portal/service | Inspected assertions and native Edge execution; CONFIRMED locally. | Deployment binding and external consumer integration remain unknown. |

## Inspected implementation and assertions

All corrected MFE locations below belong to commit `4da985a`.
Exact file hashes and repository revisions are recorded in the [source inventory](evidence/correction-20261020/source-inventory.json).

| Criteria | Baseline behavior gap | Corrected implementation | Inspected assertions |
| --- | --- | --- | --- |
| AC-1 | Each mouse event reset the five-second delay. Continuous movement could postpone renewal. | [Home controller](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L97) retains the first activity deadline. | [Lifecycle tests](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L779) send activity every 100 milliseconds. They assert actual token replacement. |
| AC-2 | Home had no keyboard activity binding. | [Home](../../repos/ui/mfe-base/src/pages/Home/index.tsx#L56) binds `onKeyDown` to eligible activity. | The lifecycle fixture and final native Edge case cover keyboard input. Deployment and embedded propagation remain open. |
| AC-3 | Home had no scroll activity binding. | Home binds `onScrollCapture` to eligible activity. | The lifecycle fixture and final native Edge case cover scroll input. Cross-origin frames remain outside scope. |
| AC-4 | Initial refresh expiry opened timeout during successful continued activity. | Home replaces near-expiry refresh credentials during eligible activity. Valid access survives the initial refresh deadline. | [Four-hour fixture](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L615) asserts 240 successful extensions and no login, relogin, or logout. |
| AC-5 | `relogin()` returned before HTTP completion. The prompt could close while renewal remained pending. | [Relogin](../../repos/ui/mfe-base/src/hooks/service/index.ts#L91) returns the real completion promise. [Timeout](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L127) awaits success. | [Completion tests](../../repos/ui/mfe-base/src/components/Timeout/renewalCompletion.test.tsx#L127) hold the adapter response. They assert zero early closures. |
| AC-6 | Prompt closure did not establish usable renewed access. | [Response predicate](../../repos/ui/mfe-base/src/hooks/service/util/relogin.response.ts) checks usable claims before authentication state changes. Timeout closes once after success. | Completion tests assert one closure and renewed token state. Malformed responses preserve prior authentication state. |
| AC-7 | Failure could close the prompt and remove the retry opportunity. | Timeout retains the prompt, clears pending state, and exposes a retry message. | [Rejection test](../../repos/ui/mfe-base/src/components/Timeout/renewalCompletion.test.tsx#L151) fails the request, retries, and installs renewed access. |

Supporting defects also affected these paths.
Repeated activity could cancel an earlier slow extension.
A late activity response could overwrite successful manual renewal.
[Extension single-flight handling](../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L13) preserves an eligible pending request.
Home cancels obsolete activity requests when timeout opens, logout starts, or Home unmounts.
Assertions cover late responses, cancellation, credential rotation, idle expiry, and pending refresh acquisition.

The BFF validates access before refresh issuance and validates refresh before relogin.
It returns successful token-bearing responses or HTTP 401 for inspected invalid-token paths.
A hypothetical `/extend` response with `result=false` and renewed authorization was not established by this implementation.
No confirmed defect is claimed for that unsupported response combination.

## Retained execution and verification

| Scope | Actual result | Retained evidence | Claim and limit |
| --- | --- | --- | --- |
| Manual completion regressions against baseline `2af6b83` | All 12 new cases failed. | [Baseline results](evidence/correction-20261020/manual-renewal/baseline-results.json). | Confirms regression sensitivity within the controlled component setup. |
| Final integrated MFE check | 167 tests passed across 13 suites. | [Run 002](evidence/correction-20261020/integrated/run-002/verification.json), [assertion results](evidence/correction-20261020/integrated/run-002/jest-result.json). | Real source executes with JSDOM, controlled Axios transport, and fixture credentials. |
| Final source binding | All 21 inspected code/test hashes match commit `4da985a`. | [Commit binding](evidence/correction-20261020/integrated/run-002/commit-binding.json). | No source changed during execution. Runtime and toolkit substitutions remain explicit. |
| E2E source binding | Final suite/configuration/guide hashes match test-engine commit `66595b8`. | [Final validation](evidence/post-change-review-20261020/e2e-code/final-validation.json). | Final native runs use source SHA-256 `41d3ee...a8b3`. |
| Earlier integrated run | Passed before a type-import compatibility edit. | [Earlier result](evidence/correction-20261020/integrated/verification.json). | Superseded for the edited test bytes. Use Run 002 for final claims. |
| Robot and JavaScript checks | Final syntax, export, Robot parse, and whitespace checks passed. | [Final E2E validation](evidence/post-change-review-20261020/e2e-code/final-validation.json). | Static checks do not replace native browser execution. |
| Actual E2E execution | Fourteen final-source native Edge cases passed. | [Execution report](test-execution-report.md); [final manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). | TC-04 and TC-07 are observation-only. Local services and shortened lifetimes do not establish PROD behavior. |
| PROD correction verification | NOT_RUN. | Intake O-002. | No authorized deployment mapping or PROD execution exists. |

The prepared dependency runtime was reused. No packages were installed for this correction.
The authorized toolkit stub remains a test substitution.
The four-hour fixture cannot establish indefinite renewal or actual browser suspension.
The final native runs establish local browser predicates. They do not establish PROD behavior or unresolved policy outcomes.
Document lint passed with 12 warnings across the three selected reports.
The warnings retain unknown owners, unresolved values, and pending business and writing reviews.
Workspace validation passed without findings.

## Coverage gaps

The primary denominator contains exactly seven active criteria, AC-1–AC-7.
Additional defect boundaries appear below and do not inflate that denominator.
The [Robot suite](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot) contains fourteen executable cases.
Its [extension](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs) contains their assertions and evidence capture.

| Metric | Numerator / denominator | Limit |
| --- | --- | --- |
| Criteria with inspected implementation links | 7 / 7 | Static source mapping; no deployment claim. |
| Criteria with controlled component assertions | 7 / 7 | Input fixtures and controlled service transport. |
| Criteria with proposed E2E predicates within stated fixture limits | 7 / 7 | AC-4 has a short live boundary case; its four-hour controlled fixture remains component-only. |
| Criteria with retained actual E2E execution | 7 / 7 | Each criterion has a native browser predicate. The exact four-hour AC-4 duration remains absent from E2E. |

| Gap ID and category | Evidence and consequence | Owner | Next action |
| --- | --- | --- | --- |
| E2E-01: execution | Native Edge covers physical activity, protected validation, cancellation, and late-response paths in the local fixture. | unknown: target environment owner. | Bind deployed frontend, gateway, BFF, and consumer revisions before release decisions. |
| E2E-02: assertion scope | The live AC-4 boundary crosses initial refresh expiry. The exact four-hour controlled duration remains component-only. | unknown: session test owner. | Add aligned service-clock support if a four-hour browser criterion is required. |
| E2E-03: natural lifecycle | Final natural run recorded `freezeObserved: true` with a paired visible control and retained captures. | unknown: browser test owner. | Rebind the case to the deployed target if production lifecycle evidence is required. |
| E2E-04: negative credentials | Actual expired-credential denial passed. Revoked-session and provider-rejection behavior remain absent. | unknown: authentication test owner. | Add authorized revocation and provider-rejection fixtures with explicit outcomes. |
| REQ-01: missing recovery policy | O-001 remains open when all usable credentials are absent. An acceptance result cannot be inferred from eligible renewal. | unknown: session policy owner. | Define that specific recovery outcome. Then add its measurable scenario and test code. |
| REQ-02: workspace scope | TC-07 compares two descriptors and entitlements after same-user sign-in, but remains observation-only. Populated application-edit retention remains unverified. | unknown: workspace owner. | Supply populated descriptors and define the required retention boundary. |
| E2E-05: embedded activity | The requirement excludes cross-origin activity without separate integration evidence. Portal handlers cannot observe those events directly. | unknown: embedded application owner. | Inspect the integration contract before extending the activity scope. |
| E2E-06: request races | Native cases cover slow single-flight activity, logout and unmount cancellation, and late activity after manual renewal. | unknown: session test owner. | Keep provider-revocation and cross-consumer races as separate integration scope. |

AC-1–AC-3 use 100-millisecond host sleeps between browser actions.
Runner overhead prevents an exact 100-millisecond event cadence.
The [case inventory](evidence/post-change-review-20261020/e2e-code/case-inventory.json) records each assertion and its fixture limits.

## Facts, inferences, and unresolved questions

Facts: The MFE correction passed the retained controlled regressions at the committed source hashes.
Facts: New E2E code checks renewal completion, retry, token use, cancellation, request sharing, and a protected-response predicate.
Facts: Native Edge execution passed 14 final-source cases. TC-04 and TC-07 are observation-only.
Inference: Earlier refresh acquisition and correct completion handling should prevent the demonstrated eligible-credential failure path.
Limit: Local natural Edge suspension recovery does not establish production lifecycle behavior.
Unknowns: PROD applicability, absent-credential recovery, workspace application-edit retention, and service capacity remain unresolved.

## Findings

| Finding and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| I-01: AC-1–AC-3 activity gaps corrected in `4da985a`; controlled and native input assertions pass. | Continuous input no longer postpones the first renewal deadline. Keyboard and scroll have portal bindings. | Codex: implementation stage completed. | Bind deployed portal and embedded consumer revisions. |
| I-02: AC-4 cutoff corrected; the controlled four-hour case and live boundary case pass. | Initial refresh expiry no longer forces an otherwise renewable active session to log out in the local fixture. | Codex: implementation stage completed. | Bind deployed frontend, gateway, and BFF evidence. |
| I-03: AC-5–AC-7 completion corrected; baseline regressions fail, controlled assertions pass, and browser race cases pass. | Pending and failed renewals preserve the prompt. Valid success closes once. | Codex: implementation stage completed. | Resolve provider-revocation and absent-credential policy. |
| G-01: Material policy and deployment boundaries remain open. | These corrections do not establish full defect closure or release readiness. | unknown: business and environment owners. | Resolve the listed scope decisions before release decisions. |

## Sources

| Source ID | Locator | Revision or hash | Authority and limits |
| --- | --- | --- | --- |
| SRC-session-renewal-clarification-20261020 | [User request](evidence/correction-20261020/user-request.txt). | `cce729b9225850ceb9e671e0922af1d2e1666488a36b897f43d304334322c9ba`. | Direct user intent and implementation authorization. No publication approval. |
| SRC-MFE-session-correction-4da985a | Registered `mfe-base` checkout; source inventory above. | `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`. | Inspected implementation and assertions. No deployment mapping. |
| SRC-session-renewal-integrated-run002 | Integrated Run 002 results and commit binding above. | Retained input, result, and source hashes. | Controlled component execution only. |
| SRC-session-renewal-e2e-source | Registered test-engine session suite and extension above. | `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; final source hash `41d3ee...a8b3`. | Inspected executable code and native Edge execution. TC-04 and TC-07 remain observation-only. |
| SRC-session-e2e-final-20261020 | [Final browser manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). | MFE `4da985a`; BFF `85d7cc0`; test engine `66595b8`. | Local native Edge evidence; no PROD claim. |
| SRC-session-renewal-original-evidence | [Earlier verification](verification.md) and [evidence index](evidence/index.md). | Original exact revisions and immutable retained hashes. | Explains the original local failure. Does not verify the correction. |
