---
artifact_kind: traceability-record
id: IMPACT-session-renewal-20261020
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-impact-intent-v4
  - SRC-session-impact-source-20261020
  - SRC-session-impact-diff-4da985a
  - SRC-session-impact-consumers-20261020
  - SRC-session-impact-integrated-run002
  - SRC-session-browser-final-manifest-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - REVIEW-session-renewal-20261020
  - single-ui-authentication
  - single-ui-sso-token-family
  - single-ui-shared-http
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

# Session renewal change impact

## Scope and identities

This report analyzes the implemented correction from the user's view and the system's view.
The exact MFE comparison is `2af6b83a08b072014e08ea37ec6d333c4aaab2b3` → `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.
The source diff changes eight application files and four test files.
No application file changes are proposed or applied by this analysis.
The [intake](intake.md) remains frozen. Later review decisions belong to the current stage record.

| Identity | Scope |
| --- | --- |
| Capability | `single-ui-authentication` |
| Requirement | `REQ-active-session-renewal`, version 4, AC-1–AC-7. |
| Changed repository | `mfe-base`; exact base and head above. |
| Unchanged service inspection | `single-ui-bff`, commit `85d7cc03eb12710d6facf581987fd4ae24fc9844`. |
| Inspected external consumers | `mfe-ratan-container` and `mfe-cashflow-blotter`; supplied filesystem copies with unknown independent revisions. |
| Services | `single-ui-web` and `single-ui-bff-api`; declared catalog identities, without deployment proof. |
| Contracts | `single-ui-sso-token-family`, `single-ui-shared-http`, and `single-ui-base-module`. |
| Test evidence | Existing controlled Run 002; new browser outcomes belong to the post-change execution report. |
| Exclusions | PROD confirmation, cross-origin activity integration, absent-credential recovery policy, and unspecified application-edit retention. |

[Impact evidence](evidence/post-change-review-20261020/impact/impact-evidence.json) retains source hashes and ten inspected relationships.
[Discovery evidence](evidence/post-change-review-20261020/impact/discovery.json) records the local catalog and available resources.
Direct source inspection establishes these relationships. No numerical graph risk score is claimed.
Overall qualitative risk is medium because authentication completion, cancellation, event scheduling, and public consumers share state.

## Requirement and criterion declarations

| Requirement ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| `REQ-active-session-renewal` | AC-1 | Continuous mouse activity produces successful renewal during the 15-second fixture. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-2 | Continuous keyboard activity produces successful renewal during the 15-second fixture. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-3 | Continuous scroll activity produces successful renewal during the 15-second fixture. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-4 | Four controlled activity hours cross initial refresh expiry without elapsed-time-only fresh SSO. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-5 | Pending manual renewal causes zero successful prompt closures. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-6 | Valid manual renewal closes the prompt exactly once after completion. | Version 4. | Candidate; pending publication. |
| `REQ-active-session-renewal` | AC-7 | Failed renewal preserves the prompt and permits another eligible attempt. | Version 4. | Candidate; pending publication. |

These intervals describe fixtures. They do not define a new production policy duration.
The requirement retains credential validity and revocation boundaries.
It does not define recovery after every usable credential is lost.

## User view

The affected actor is a signed-in portal user.
The changed journeys involve active work, idle renewal, failed renewal, logout, and background return.
The consequence below follows inspected source unless controlled execution is explicitly cited.
Real-browser execution remains separate.

| Journey and trigger | Previous behavior | Changed behavior and observable consequence | Evidence and confidence | Owner and next action |
| --- | --- | --- | --- | --- |
| Continuous mouse, keyboard, or scroll activity. | Mouse events reset the pending deadline. Keyboard and scroll had no Home bindings. | Eligible events retain the first five-second deadline. Keyboard and scroll use the same renewal path. | Confirmed source change; AC-1–AC-3 controlled assertions pass. | unknown: portal owner. Execute physical input in the complete Home document. |
| Continued activity crosses initial refresh expiry. | The original refresh deadline could open timeout despite renewed valid access. | Recent eligible visible activity can replace refresh credentials. Initial refresh expiry alone no longer forces valid access into timeout. | Confirmed source change; four controlled hours and 240 extensions pass. | unknown: session owner. Execute the live boundary and confirm deployment identity. |
| User selects Extend; request remains pending. | The dialog could close before the request completed. | Extend waits. The dialog stays visible, and duplicate renewal attempts are suppressed. | Confirmed source change; pending transport assertion passes. | unknown: session test owner. Capture pending state in the real browser. |
| Manual Extend succeeds. | Early closure did not establish usable renewed access. | A usable token response precedes successful closure. The successful close occurs once. | Confirmed source change; token state and one-close assertions pass. | unknown: session test owner. Confirm protected UI work uses the renewed credentials. |
| Eligible renewal has a transport failure. | The prompt could close before failure became known. | The dialog shows a retry message and allows another eligible attempt. | Confirmed for controlled HTTP 503 and resolved failure responses. Revocation recovery remains separate. | unknown: authentication owner. Run transport retry and provider-rejection cases with explicit expected results. |
| User selects Logout during renewal. | Request completion was not owned by the prompt lifecycle. | Logout remains available. Cancellation prevents the inspected late response from restoring access. | Confirmed source change; controlled logout and late-response assertions pass. | unknown: session test owner. Run delayed-renewal logout in the real browser. |
| User stops activity or returns from background. | Original refresh expiry could terminate otherwise valid renewed access. | Valid access remains usable until its own expiry. The existing idle prompt still uses eligible refresh credentials. | Confirmed source change; controlled idle and return assertions pass. Natural freezing remains unverified. | unknown: session owner. Run visible-idle and natural-background controls. |
| User expects the workspace to remain after renewal. | Workspace-loss details remain unspecified. | No workspace serialization or descriptor mutation appears in this diff. Complete edit retention is not established. | Confirmed diff boundary; no application-edit acceptance result exists. | unknown: workspace owner. Identify lost descriptors and edits before defining retention acceptance. |

The complete Home document can contain child handlers and embedded applications.
Portal keyboard and scroll bindings do not establish cross-origin event propagation.
The two inspected API-completion consumers can also request extension without Home activity checks.
A representative idle control must therefore record embedded application traffic.
This is an existing integration boundary, not a confirmed new defect.

## System view

All MFE source locations below belong to head `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.
The detailed [source inventory](evidence/post-change-review-20261020/code-review/inspection.json) contains the exact hashes.
The inspected Git-backed source bytes match the selected commits.

| System area | Changed behavior and affected path | Interface or unchanged path inspected | Effect class and risk | Verification or next action |
| --- | --- | --- | --- | --- |
| Input scheduling | `Home/common/useController.ts:103` retains the first activity deadline. | Actual Home bindings `Home/index.tsx:56`; controller eligibility `:74`. | Confirmed scheduling change; medium timing risk. | Physical mouse, keyboard, and scroll cases must confirm propagation. |
| Request rate | Five-second activity windows can issue about 720 extensions per hour, per eligible session. | `ACTIVITY_INTERVAL_MS` at `Home/common/useController.ts:17`; three extensions asserted over 15 seconds. | Source-derived estimate; possible capacity effect. No capacity violation is established. | Measure request count and latency against an owner-approved limit. |
| Access extension concurrency | `hooks/service/util/extend.ts:13` shares same-access requests and aborts obsolete credentials. | Axios cancellation; request configuration; authentication response handlers. | Confirmed local request lifecycle change; medium race risk. | Run slow repeated activity and obsolete-response cases in the browser. |
| Manual completion contract | `hooks/service/index.ts:91` returns `Promise<boolean>` after HTTP processing. | Timeout caller; public `Service` export at `root.tsx:35`; shared Axios instance. | Confirmed return contract change; compatibility beyond inspected consumers remains unknown. | Verify deployed package consumers. Keep the returned boolean distinct from raw HTTP status. |
| Response acceptance | `relogin.response.ts:5` requires usable claims and rejects cancellation, logout, or explicit failure. | Shared success handler; JWT parsing; token storage; reducers; BFF response generation. | Confirmed relogin filter; medium authentication-state risk. | Run valid, malformed, missing-header, rejected, and late-response browser predicates. |
| Refresh replacement | `Home/common/useController.ts:85` requests replacement near refresh expiry during eligible visible activity. | Existing `getRefreshToken`; valid-access BFF route; three-hour credential reuse policy. | Confirmed new call path; medium rotation and clock-boundary risk. | Cross initial refresh expiry with continued input and verify replacement-token use. |
| Cancellation and cleanup | Home aborts extension at timeout, logout, and unmount. Timeout aborts its owned relogin. | Shared controllers; LoadingButton disabling; store logout state; late Axios responses. | Confirmed guards; browser transport order remains unverified. | Execute cancellation and late-response cases with retained request correlations. |
| Public extension consumers | `extendToken` is exported through `root.tsx:73`. Cashflow middleware and GraphQL completion call it. | `apiSessionExtendMiddleware.ts:12`; `graphql.ts:166`; both ignore the return value. | Confirmed source relationships; unknown deployment revision. Existing call statements remain compatible. | Run representative embedded traffic and idle controls. Confirm deployed module versions. |
| BFF HTTP contract | No BFF file changes. Existing extend, refresh, and relogin endpoints remain in use. | `JwtAuthenticationController.java:275`, `:303`, `:328`; `JwtTokenUtil.java:48`. | Confirmed unchanged source contract; no service deployment conclusion. | Bind frontend, gateway, and BFF runtime revisions before E2E claims. |
| Error propagation | The unchanged error handler clears authentication for `TOKEN_INVALID_EXPIRED`. | `error.response.handler.ts:30`; routing switches away from Home when access is cleared. | Confirmed inherited rejection path; absent-credential recovery policy remains unresolved. | Separate transport retry from expired or revoked credential outcomes. |
| State and persistence | Renewed access uses existing reducers and token storage. No schema or key changes appear. | `utils/login.ts:13`; `utils/common.ts:46`; shared reducers; workspace code. | Confirmed diff boundary; application-edit preservation remains unverified. | Inspect state before and after renewal. Confirm the required workspace-retention scope. |
| Deployment | No release, gateway configuration, or environment policy changes appear. | Registered identities and local source hashes only. | Unknown deployment applicability. | Obtain exact deployed revisions and settings from the environment owner. |

The steady-rate estimate assumes continuous eligible input and prompt successful responses.
Pending requests share work. Latency, failures, hidden periods, and invalid credentials can reduce the activity-driven rate.
API-completion callers can add requests outside that cadence.
No service capacity threshold was supplied.

The BFF validates credentials and session state before token-bearing success.
Its inspected extension path can refresh the absolute-idle claim when needed.
This supports the source analysis of continued eligible renewal.
It does not prove provider availability, revoked-session behavior, or deployed policy.

The manual prompt retains its existing two-second refresh-expiry lead.
The preserved boundary can cancel a pending renewal before nominal credential expiry.
An owner must approve any policy change to that boundary.
The review supplies this observation without applying a correction.

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| Requirement AC-1–AC-3 | Implements through | Home bindings → controller → extension helper. | Exact head; paths above; retained diff and native Edge cases. | Inspected source and local browser relationship. | Deployment and embedded propagation remain unverified. |
| Requirement AC-4 | Implements through | Activity refresh replacement and access-expiry reconciliation. | Home controller `:85`, `:155`, `:206`. | Inspected source relationship. | Finite tests cannot prove indefinite operation. |
| Requirement AC-5–AC-7 | Implements through | Timeout → relogin promise → response predicate. | Timeout `:127`; service `:91`; predicate `:5`. | Inspected source relationship. | Credential revocation differs from transport failure. |
| Public `ExtendService` | Consumed by | Cashflow query middleware. | Hashed consumer excerpts and import binding. | Inspected filesystem-copy relationship. | Independent source revision and deployed use unknown. |
| Public `ExtendService` | Consumed by | Ratan GraphQL completion. | Hashed consumer excerpts and import binding. | Inspected filesystem-copy relationship. | Independent source revision and deployed use unknown. |
| MFE authentication routes | Implemented by | Unchanged BFF authentication controller. | BFF commit and route locations above. | Inspected source contract. | Source compatibility does not prove runtime routing. |
| Controlled assertions | Executed in | Integrated Run 002. | Input hashes and commit binding. | Matching retained execution. | JSDOM, fixture credentials, and controlled transport. |

## Inspected implementation and assertions

The [code review](code-review.md) lists every changed area and the relevant unchanged interfaces.
The [earlier coverage report](coverage.md) retains the seven-criterion assertion mapping.
This analysis reuses those locators and results without creating a duplicate coverage numerator.

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-1–AC-3 | `mfe-base` | `4da985a` | Home bindings `:56`; activity control `:103`. | Lifecycle input cases. | Same full head above. | `sessionLifecycle.test.tsx:779` | Three extensions and renewed access after repeated input. |
| AC-4 | `mfe-base` | `4da985a` | Refresh replacement `:85`; expiry reconciliation `:155`. | Four-hour fixture. | Same full head above. | `sessionLifecycle.test.tsx:615` | 240 extensions, refresh replacement, and zero fresh-login or logout requests. |
| AC-5–AC-7 | `mfe-base` | `4da985a` | Timeout completion `:127`; relogin service `:91`. | Manual completion cases. | Same full head above. | `renewalCompletion.test.tsx:127` | No premature closure; one valid success; retry after rejected transport. |
| Supporting cancellation | `mfe-base` | `4da985a` | Extension helper `:13`; Home cleanup `:233`. | Late-response cases. | Same full head above. | `renewalCompletion.test.tsx:205`; `extendRequest.test.ts:68`. | Cancellation prevents obsolete response effects; same-access requests share one operation. |

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-1–AC-7 and supporting regressions | Inspected cases above and earlier coverage mapping. | Integrated Run 002. | `4da985a9fa302d7f1ecc04a81b2924b49410ce6a` | 167 tests passed; 13 suites passed. | PASSED, controlled execution. | [Results](evidence/correction-20261020/integrated/run-002/verification.json); [binding](evidence/correction-20261020/integrated/run-002/commit-binding.json). | Only matched controlled predicates passed. |
| Actual browser behavior | Native Edge execution record supplies per-case predicates. | `native-edge-post-change-20261020`. | MFE `4da985a`; test engine `66595b8`; BFF `85d7cc0`. | Fourteen final-source cases passed locally; TC-04 and TC-07 remain observation-only. | PASSED, local browser execution. | [Execution report](test-execution-report.md); [final manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). | Local services and shortened lifetimes do not establish PROD behavior or indefinite renewal. |

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Complete Home and embedded consumers to browser outcomes. | Native Edge cases cover the complete Home document and protected portal operation. External consumer tests still mock the helper. | Physical Home inputs, lifecycle races, and protected validation are locally verified. Embedded consumer traffic and cross-origin propagation remain unverified. | unknown: portal and embedded-application owners. | Execute representative embedded idle controls and bind deployed consumer revisions. |
| Local commits to deployed modules and settings. | Exact local source exists. Deployment mapping is absent. | PROD applicability and release readiness remain unknown. | unknown: environment owner. | Record deployed frontend, BFF, gateway, and policy identities. |
| Activity cadence to service capacity. | Five-second source interval; no approved service load limit. | Increased traffic has an unmeasured capacity effect. | unknown: authentication owner. | Retain request counts and latency. Obtain the applicable capacity limit. |
| Lost workspace state to an approved preservation rule. | Workspace-loss descriptors remain unspecified. | These token corrections cannot establish complete state-retention acceptance. | unknown: workspace owner. | Identify affected descriptors and application edits. Define measurable retention checks. |
| No usable credentials to an expected recovery outcome. | Existing open recovery question and rejection cleanup path. | Renewal tests cannot establish acceptance after every credential expires or is revoked. | unknown: session policy owner. | Resolve that specific recovery policy before adding acceptance assertions. |

## Facts, inferences, and unresolved questions

Facts: The exact correction changes activity scheduling, credential replacement, manual completion, and cancellation.
Facts: The unchanged public extension export has two inspected consumer copies.
Facts: The retained controlled regression matches the selected MFE commit and passes 167 tests.
Facts: Native Edge execution passed 14 final-source cases. TC-04 and TC-07 are observation-only because their policies remain unresolved.
Inference: These changes address the demonstrated eligible-renewal paths within the inspected conditions.
Possible effects: Renewal traffic increases during continuous input. Embedded API traffic can affect idle observations.
Unknowns: Deployed revisions, capacity limits, missing-credential recovery, and application-edit retention remain unresolved.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| I-01: Activity bindings, throttle, and final mouse, keyboard, and scroll runs. | Continuous portal input now renews without resetting the first deadline in the local browser fixture. | unknown: portal owner. | Bind the deployed portal revision and retain representative embedded activity evidence. |
| I-02: Refresh replacement, four-hour controlled execution, and final live-boundary run. | The initial refresh deadline no longer ends otherwise eligible active renewal in the local fixture. | unknown: session owner. | Bind the deployed frontend, gateway, and BFF revisions. |
| I-03: Awaited relogin, response predicate, cancellation assertions, and final browser race cases. | Pending and failed transport preserve eligible retry. Late cancelled responses do not restore inspected authentication state. | unknown: authentication owner. | Resolve provider-revocation and no-credential policies before extending acceptance. |
| I-04: Shared extension export and two API-completion consumers. | Idle observations can depend on loaded module traffic. | unknown: portal and application owners. | Confirm activity policy and retain traffic during idle controls. |
| I-05: Five-second source cadence and absent capacity threshold. | Request-rate impact remains unmeasured. | unknown: authentication service owner. | Measure service load and latency against an approved limit. |
| I-06: Missing deployment, recovery, and workspace acceptance links. | The correction does not establish full defect closure or release readiness. | unknown: environment and business owners. | Resolve each named boundary and review the complete browser results. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-impact-intent-v4 | [Requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | Version 4. | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` | Direct user intent; candidate publication pending. |
| SRC-session-impact-source-20261020 | [Impact evidence](evidence/post-change-review-20261020/impact/impact-evidence.json) | Exact MFE head; BFF `85d7cc03eb12710d6facf581987fd4ae24fc9844`. | Per-file SHA256 values retained. | unknown; local source facts and explicit effect classifications. |
| SRC-session-impact-diff-4da985a | [Retained exact diff](evidence/post-change-review-20261020/code-review/change.diff) | Exact MFE base and head above. | `f6c59e333ca899de96f13de7a1cf05a2d71f12927b0569e4c2151cd4cbf7b43f` | unknown; complete selected comparison; no deployment claim. |
| SRC-session-impact-consumers-20261020 | [Consumer excerpts](evidence/post-change-review-20261020/code-review/consumer-excerpts.txt) | null; supplied filesystem copies. | Full-file hashes in impact evidence. | unknown; static call relationships; independent origins unknown. |
| SRC-session-impact-integrated-run002 | Existing Run 002 inputs, results, and commit binding above. | Exact selected MFE head. | Execution and source hashes retained. | Controlled component execution only; native browser evidence is listed separately. |
| SRC-session-browser-final-manifest-20261020 | [Final browser manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). | Test engine `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; MFE `4da985a`; BFF `85d7cc0`. | Per-case hashes in manifest. | Local native Edge execution; no PROD claim. |
