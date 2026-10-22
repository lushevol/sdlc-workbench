---
artifact_kind: pull-request-review
id: REVIEW-session-renewal-20261020
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-review-diff-4da985a
  - SRC-session-review-inspection-20261020
  - SRC-session-review-consumers-20261020
  - SRC-session-renewal-integrated-run002
  - SRC-session-browser-final-manifest-20261020
  - SRC-session-review-intent-v4
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - TRACE-session-renewal-correction-20261020
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

# Session renewal code review

## Change identity

| Field | Value |
| --- | --- |
| PR locator | null; no PR identity was supplied. |
| Repository ID | `mfe-base` |
| Base commit | `2af6b83a08b072014e08ea37ec6d333c4aaab2b3` |
| Head commit | `4da985a9fa302d7f1ecc04a81b2924b49410ce6a` |
| Requirements and decisions | `REQ-active-session-renewal`, version 4, AC-1–AC-7; candidate, publication review pending. |
| Change state | Committed on `feature/session-refresh`; deployment and merge states are unknown. |

The user requested suggestions without application changes.
This review makes no application changes.
The [intake](intake.md) remains frozen under the user's instruction.
The [earlier coverage report](coverage.md) supplies context and retained execution evidence.

## Problem and behavior

Trigger: Continuous portal activity, or manual Extend after access expiry.
Before: Repeated input could postpone renewal. Manual Extend could close before its HTTP request completed.
After: Activity retains its first five-second deadline. Manual Extend awaits a usable renewal response.
Reason: Requirement version 4 requires continued eligible renewal and completion before successful prompt closure.

The change also renews near-expiry refresh credentials during eligible visible activity.
Valid access no longer expires solely because the original refresh credential expires.
Cancellation protects the inspected logout, timeout, unmount, and obsolete-request paths.
These source facts do not establish deployed behavior.

## Change scope and risks

The exact diff changes eight application files and four test files.
It contains 1,079 inserted lines and 229 deleted lines.
The [retained diff](evidence/post-change-review-20261020/code-review/change.diff) fixes the complete comparison scope.
The [inspection record](evidence/post-change-review-20261020/code-review/inspection.json) binds 37 inspected source and assertion files.
All inspected Git-backed files match their selected commits.

All MFE locations below use head `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.

| File or symbol | Exact diff location | Change | Callers, importers, and interfaces inspected | Risk and mitigation |
| --- | --- | --- | --- | --- |
| Home activity control | `src/pages/Home/common/useController.ts:74`, `:85`, `:97`, `:103` | Eligibility guard, five-second throttle, and refresh replacement. | Home bindings; extension helper; shared store; real-controller lifecycle assertions; final native Edge cases. | Medium: deployed service and embedded propagation remain unverified. |
| Home lifecycle control | `src/pages/Home/common/useController.ts:155`, `:206`, `:233` | Reconcile access expiry; replace refresh credentials after recent activity; cancel obsolete extension. | Visibility events; Timeout mounting; reducer expiry updates; cleanup; final natural and cancellation runs. | Medium: local lifecycle evidence does not establish deployed policy. |
| Home event bindings | `src/pages/Home/index.tsx:56` | Add keyboard and captured scroll events. | Root descendants; React portal Timeout; actual Home tests; controller test wrapper; final native Edge cases. | Medium: embedded cross-origin propagation and deployed behavior remain unknown. |
| Manual completion | `src/components/Timeout/common/useController.ts:127` | Await renewal; preserve retry; suppress duplicate attempts. | Timeout buttons; LoadingButton disabling; service completion; shared authentication state. | Medium: expiry and logout can cancel pending work. |
| Timeout interface | `src/components/Timeout/index.tsx:29`, `:34`, `:44` | Show retry error; keep Logout available during renewal. | LoadingButton implementation; controller state; completion assertions. | Low: confirm visible error and button states in the browser. |
| Relogin result | `src/hooks/service/index.ts:91` | Return `Promise<boolean>` after real response completion. | Timeout caller; request header interceptor; Axios response chain; public `Service` export. | Medium: shared exported behavior changes from immediate return to completion. |
| Relogin response predicate | `src/hooks/service/util/relogin.response.ts:5`; `src/hooks/service/util/succes.response.handler.ts:27` | Reject failed, cancelled, logged-out, malformed, or expired responses before authentication updates. | JWT parser; login handlers; reducer; actual BFF relogin contract. | Medium: deployment/header compatibility remains unverified. |
| Activity request lifecycle | `src/hooks/service/util/extend.ts:13`, `:43` | Share same-access requests; abort obsolete credentials; return pending promise. | Home; public `ExtendService`; two supplied consumer copies. | Medium: concurrent consumer activity and renewal traffic need measurement. |
| Regression assertions | Four changed test files in the retained diff. | Add completion, long activity, cancellation, retry, and request-sharing assertions. | Fixtures, adapters, helper chains, and retained Run 002 bindings. | Controlled execution excludes natural browser freezing and deployed service responses. |

Compatibility and data impact: HTTP endpoint names, request bodies, and token header names remain unchanged.
The new response predicate requires numeric `iat` and future `exp` values.
The inspected BFF generates both claims and returns the expected authorization header.

`Service.relogin` now returns `Promise<boolean>`.
`ExtendService.extendToken` now returns a pending promise or `undefined`.
The two inspected external consumers ignore that return value.
Their inspected calls remain compatible.
Their independent Git revisions remain unknown because they are supplied filesystem copies.

The unchanged shared request interceptor still attaches refresh credentials to relogin requests.
The unchanged response error handler can clear authentication for `TOKEN_INVALID_EXPIRED`.
The unchanged logout service clears local authentication without awaiting remote logout completion.
This review makes no global revocation claim.

No database schema, storage key, or workspace serialization change appears in this diff.
Runtime authentication still updates existing token storage through unchanged login handlers.
Recovery: A source revert is available. It restores the earlier defects and does not prove deployed session recovery.

## Validation evidence

| Requirement or check | Command or inspected assertion | Revision and environment | Retained evidence | Actual result | Claim limit |
| --- | --- | --- | --- | --- | --- |
| Exact comparison | `git diff --no-ext-diff --binary BASE HEAD` | The exact commits above. | Retained diff and inspection record. | 12 changed files; all selected Git-backed bytes match. | Source inspection only. |
| AC-1–AC-3 | Lifecycle tests `:779`–`:803` send repeated input and assert three extensions plus renewed access. | Head; JSDOM; controlled Axios transport. | [Run 002](evidence/correction-20261020/integrated/run-002/verification.json). | Passing retained assertions. | The test wrapper uses the real controller, rather than the complete Home document. |
| AC-4 | Lifecycle test `:615`–`:654` crosses initial refresh expiry over four controlled hours. | Head; 240 extensions; fixture credentials. | Run 002; [commit binding](evidence/correction-20261020/integrated/run-002/commit-binding.json). | Passing retained assertions. | Finite controlled execution cannot prove indefinite or natural lifecycle behavior. |
| AC-5–AC-7 | Completion tests `:127`–`:190` assert pending state, success, rejected transport, and retry. | Head; real response handlers; controlled adapter. | Run 002. | Passing retained assertions. | Provider revocation and deployed error mapping remain unverified. |
| Request cancellation | Completion tests `:205`–`:240`; extension tests `:68`–`:103`. | Head; explicit AbortController assertions and late responses. | Run 002. | Passing retained assertions. | Browser transport races require separate execution. |
| Integrated regression | Exact command appears in [inputs](evidence/correction-20261020/integrated/run-002/inputs.json). | Head; prepared runtime; disclosed toolkit substitutions. | Run 002; assertion result and commit binding. | 167 tests passed across 13 suites. | This review reuses matching retained results. It does not claim another execution. |
| External consumer assertions | Cashflow middleware test checks one mocked `ExtendTokenService` call. | Filesystem copy; exact hash retained. | [Consumer excerpts](evidence/post-change-review-20261020/code-review/consumer-excerpts.txt). | Inspected only; NOT_RUN. | The mock does not establish integration or renewal success. |
| New browser work | Separate post-change execution record. | Native Edge target and local service revisions are bound in the final manifest. | Fourteen final-source cases passed locally; TC-04 and TC-07 remain observation-only. | PASSED for local browser scope. | [Execution report](test-execution-report.md); [final manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). PROD and deployed-consumer applicability remain unknown. |

## Review findings

No confirmed new application defect was established within this exact comparison.
The suggestions below identify unresolved risks and verification gaps.
All suggestions remain unapplied.
They do not claim a demonstrated production failure.
Priority denotes review urgency, rather than measured incident severity.

| Finding ID and priority | Evidence location | Consequence | Owner | Next action | Resolution evidence |
| --- | --- | --- | --- | --- | --- |
| R-001; P2; integration risk | `extend.ts:43`; public export `root.tsx:73`; consumer excerpts `apiSessionExtendMiddleware.ts:12` and `graphql.ts:166`. | API completion can request renewal outside Home activity and visibility checks. Idle evidence can depend on loaded application traffic. | unknown: portal and embedded-application owners. | Confirm which API traffic counts as activity. Execute visible-idle and hidden controls with representative embedded queries. | Open; no deployed consumer run exists. |
| R-002; P2; browser verification gap | `Home/index.tsx:56`; lifecycle wrapper `sessionLifecycle.test.tsx:62` and assertions `:779`–`:803`; final native Edge manifest. | Controlled input success alone did not prove Home propagation, natural freezing, or request races. The final local browser suite now covers those listed paths. Embedded consumer propagation and deployed applicability remain open. | unknown: session and embedded-application owners. | Retain representative embedded traffic and bind deployed module revisions. | Partially resolved for local browser scope; see [execution report](test-execution-report.md). |
| R-003; P3; capacity risk | `Home/common/useController.ts:17`, `:103`–`:111`; lifecycle assertions `:796`; extension request sharing `extend.ts:16`–`:20`. | Continuous input can produce approximately 720 activity extensions per hour, per eligible session. Additional external calls can increase traffic. | unknown: authentication service owner. | Measure extension counts and response latency under continuous activity. Compare results with an owner-approved capacity limit. | Open; no capacity limit or load execution was supplied. |

R-001 describes an unchanged integration path through the changed shared helper.
It is not attributed to a new visibility bypass in this commit.
R-003 estimates the five-second steady cadence with prompt successful responses.
Pending requests share work. Failed requests and service latency can reduce that rate.
No capacity violation is claimed without an approved limit and matching measurements.

The two-second refresh-expiry lead remains unchanged in the manual prompt timer.
A pending renewal can therefore cancel before the nominal refresh expiry.
Existing tests preserve this behavior explicitly.
The session owner should confirm that policy before changing its boundary.
This review does not classify the inherited lead as a confirmed defect.

## Review disposition

Reviewer: null.
Decision: pending.
Review date: null.
Reviewed commits: `2af6b83a08b072014e08ea37ec6d333c4aaab2b3` → `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.
Review scope limits: Local source and matching controlled and native-browser executions only. Consumer revisions, deployment bindings, and PROD behavior remain unknown.
Merge or publication authority: null.

A human review decision remains required.
Zero confirmed findings do not establish release readiness or complete defect closure.
Absent-credential recovery, application-edit retention, and PROD applicability remain outside this correction's confirmed scope.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SRC-session-review-diff-4da985a | [Change diff](evidence/post-change-review-20261020/code-review/change.diff) | Exact base and head above. | `f6c59e333ca899de96f13de7a1cf05a2d71f12927b0569e4c2151cd4cbf7b43f` | unknown; exact Git comparison; all 12 changed files inspected. |
| SRC-session-review-inspection-20261020 | [Inspection record](evidence/post-change-review-20261020/code-review/inspection.json) | MFE head; BFF `85d7cc03eb12710d6facf581987fd4ae24fc9844`. | Per-file SHA256 values in the record. | unknown; direct source inspection; no deployment authority. |
| SRC-session-review-consumers-20261020 | [Consumer excerpts](evidence/post-change-review-20261020/code-review/consumer-excerpts.txt) | null; supplied filesystem copies. | Full-file SHA256 values in the inspection record. | unknown; local integration evidence; source origin and deployment unknown. |
| SRC-session-renewal-integrated-run002 | Run 002 inputs, results, and commit binding above. | MFE head; 21 source and assertion hashes match. | Retained execution hashes. | Controlled component execution only; native browser evidence is listed separately. |
| SRC-session-browser-final-manifest-20261020 | [Final browser manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). | Test engine `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; MFE `4da985a`; BFF `85d7cc0`. | Per-case hashes in manifest. | Local native Edge execution; no deployment or PROD authority. |
| SRC-session-review-intent-v4 | [Requirement version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | Version 4. | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` | Direct user intent; candidate publication remains pending. |

Facts: The change adds activity throttling, refresh replacement, completion handling, and cancellation guards.
Facts: The matched controlled regression passed 167 tests.
Facts: Native Edge execution passed 14 final-source cases. TC-04 and TC-07 remain observation-only because their policies remain unresolved.
Facts: Two supplied consumer copies call the changed public extension helper.
Inferences: The source addresses the demonstrated eligible-renewal failures under the tested conditions.
Unresolved questions: Which deployed consumers and session policies apply? Owner unknown; obtain deployment and policy evidence.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| R-001 | Changed public helper plus unchanged consumer excerpts. | Embedded API traffic can alter idle-session observations. | unknown: portal and embedded-application owners. | Confirm activity policy and execute representative idle controls. | open |
| R-002 | Actual Home bindings differ from the controlled lifecycle wrapper. | The final local browser suite verifies physical event propagation, natural freeze observation, and listed browser races. Embedded consumers and deployment remain unverified. | unknown: session and embedded-application owners. | Retain representative embedded traffic and deployed revision evidence. | partially resolved |
| R-003 | Five-second throttle and three-extension controlled assertion. | Continuous activity increases renewal traffic. | unknown: authentication service owner. | Measure request rate and latency against an approved capacity limit. | open |
