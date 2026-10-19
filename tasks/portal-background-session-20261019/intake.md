---
artifact_kind: defect-report
id: DEFECT-portal-background-session-20261019
version: 10
status: draft
owner: unknown
source_refs:
  - SRC-portal-intake-reporter
  - SRC-portal-intake-followup-20261019
  - SRC-session-renewal-intent-2026-10-15
  - SRC-session-activity-and-idle-intent
  - SRC-portal-session-requirement-v2
  - SRC-confluence-aa082f0221001faa
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
  - SRC-portal-run001-review-6b95269bba2c54ca89
  - SRC-portal-run001-review-6bb4b44e8782aedac0
  - SRC-portal-run001-review-e3ccceebbcd3c2d0f8
  - SRC-portal-local-d08eca66d6d7927aaa
  - SRC-portal-local-51b499197b9cb44755
  - SRC-portal-local-b41c647cf1c7bb26a0
  - SRC-portal-local-e9ea73b748a7c4c086
  - SRC-portal-local-bd6b128e6441085c98
  - SRC-portal-local-a3c4f7a97404e81afb
  - SRC-portal-sign-in-context-20261020
related_ids:
  - REQ-active-session-renewal
  - REPORT-portal-task-evidence-review-20261019
  - single-ui-authentication
  - single-ui-web
  - single-ui-bff-api
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

# Portal logout after a background tab interval

## Problem description

Users report automatic logout after returning to the portal from another Edge tab after approximately 30 minutes.
They report no usable opportunity to extend the session.
They also report repeated sign-in, lost workspaces after sign-in, and rework.

| Summary | Current assessment |
| --- | --- |
| Status | Open. The user-supplied local patch is applied. Correction tests could not start because dependencies are absent. |
| Scope and impact | PROD; nearly all users, nearly every time, according to the reporter. Counts and lost-work duration remain unmeasured. |
| Confirmation | Local authentication failure demonstrated. PROD cause and workspace loss remain unverified. |
| Expected behavior | Existing intent retains idle renewal with usable refresh credentials. Suspension without a refresh credential remains undefined. |
| Severity / priority / business owner | Unassessed / unassessed / unknown. Obtain classification rules and an accountable owner. |
| This change | User-supplied session patch and evidence. Risk: medium because authentication timing and cancellation change. |

This is the main issue record. Detailed evidence remains in the [evidence index](evidence/index.md).
[Verification detail](verification.md) records assertions and capture limits.
Version 9 repairs evidence links after the domain-only knowledge migration.
The [earlier manifest](evidence/manifest.json) records the previous task cleanup.
The [migration map](../../evidence/knowledge/migration-20261020/cleanup.json) records current locators, retained hashes, and additional deletions.
Registered snapshots and existing audit events remain unchanged.

## Existing knowledge and code facts

### Documented intent and authority

| Source | Established understanding | Authority and limit |
| --- | --- | --- |
| [REQ-active-session-renewal v3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | Eligible portal activity supports renewal. Inactivity retains renewal through usable refresh credentials. | Recorded user intent; candidate publication review remains pending. Browser suspension is a separate condition. |
| Requirement AC-5–AC-7 | Pending renewal has zero successful prompt closures. Success closes once. Failure preserves another attempt. | AC-5 and AC-6 assume usable refresh credentials. These criteria do not settle Run 001's absent-credential boundary. |
| [Raw renewal intent](evidence/authentication/requests/session-renewal-intent-2026-10-15.txt) and [activity reply](evidence/authentication/requests/session-activity-and-idle-intent-2026-10-15.txt) | Continued activity renewal and retained idle refresh are explicit. | Read directly. They specify no new server timeout or deployed configuration. |
| Historical V1, SRC-confluence-aa082f0221001faa | Extend is proposed while refresh remains valid. | Historical refresh-duration examples conflict: 105 versus 225 minutes. They cannot establish current PROD policy. |

Activity in another browser tab does not establish activity inside the portal document.
The requirement's isolated pilot uses revision `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.
Run 001 uses the different MFE revision below. Pilot characterization does not establish this run's recovery behavior.

### Inspected implementation and tests

| Exact source | Fact | Evidence limit |
| --- | --- | --- |
| [MFE Home controller](evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/pages/Home/common/useController.ts.snapshot#L87), lines 87–100 | Schedules refresh issuance 25 seconds before access expiry. | Browser timers cannot execute while the tab remains frozen. |
| [MFE Timeout controller](evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/components/Timeout/common/useController.ts.snapshot#L25), lines 25–41 | Selects automatic logout when refresh state is absent. | This local path does not establish the required business recovery policy. |
| [BFF authentication controller](evidence/source-snapshots/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot#L303), lines 303–355 | Refresh issuance validates access. Relogin separately accepts valid refresh credentials. | Expired access cannot obtain refresh through the inspected issuance endpoint. |
| [MFE error handler](evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/hooks/service/util/error.response.handler.ts.snapshot#L29), lines 29–31 | Clears authentication for `TOKEN_INVALID_EXPIRED`. | The local logout decision precedes that response. |
| Workspace reducers, initial state, cleanup, and Home validation | Persist and restore descriptors; logout preserves localStorage workspace keys but clears sessionStorage. Home filters descriptors through catalog and entitlements. | No retained execution compares workspaces before logout and after sign-in. Application edits need separate evidence. |
| Timeout, Home, reducer, BFF, and Robot assertions | Inspected tests cover buttons, immediate responses, defaults, mocks, and tooling. | Bounded inspection found no natural-freeze recovery assertion or post-login workspace comparison. Tests were not rerun here. |

[Source inspection](evidence/source-inspection.json) records exact test locators and hashes.
[The test-engine inspection](evidence/browser-setup/test-engine-inspection.json) records the bounded Robot search.
Repository and service declarations identify investigation scope. They do not establish deployment parity.

### Source references

| Source group | Locator and revision | Hash and authority |
| --- | --- | --- |
| User reports | SRC-portal-intake-reporter: current source chat `01a152fa-aff2-7582-aaf4-8e7b4d9c7f2f`. Follow-up: `01a15450-d00a-7d32-91ee-34e5a648cb59`, 19 October 2026. | Chat has no file hash. User-reported experience and local authorization; no PROD telemetry. |
| Requirement and raw intent | Linked above; requirement v3 and replies dated 15 October 2026. | Requirement SHA-256: `fba6856c384db06ec76b6f8e96e635b35d5cde4ab469f56161861770961a431c`. Raw hashes resolve in the [source manifest](../../evidence/knowledge/manifest.yaml). |
| Implementation | MFE `f025513f696476a9cc8162681410cbd21e029bcb`; root config `83091d85beff5306ca0cd643955d8ea6ed0a2d93`; BFF `85d7cc03eb12710d6facf581987fd4ae24fc9844`. | Exact source snapshots and hashes resolve through [the evidence index](evidence/index.md), C-006. Owners unknown; local source evidence only. |
| Tests | MFE and BFF revisions above; Robot `a639c6a92b2f125e2e99a0ca282ad7178e8c2c40`. | Source receipt and test-engine inspection above. Owners unknown; assertion inspection does not establish passing execution. |
| Runs and screenshot | Local runs dated 19 October 2026. Screenshot retained 20 October 2026; capture phase unknown. | Linked below and indexed with hashes. Owners unknown; local observations only. |

All frontmatter source IDs resolve through this table, the evidence index, or the source manifest.
The knowledge search covered candidate indexes, the session topic, linked requirements, raw replies, and cited historical designs.
No PROD source was accessed. Existing knowledge answers the general session-policy question.

## User clarifications

| IDs | Focused question or supplied detail | Recorded answer | Answer source and consequence |
| --- | --- | --- | --- |
| Q-001–Q-003 | Environment, browser, tab, elapsed interval, and extension opportunity? | PROD; Edge; another browser tab; about 30 minutes; automatic logout without a usable extension chance. | SRC-portal-intake-reporter; answered. Original versions remain unknown. |
| Q-005 | What session behavior is intended? | “these requirements (system intends) can be find in knowledge, I don’t need to explain again.” | Reporter reply; answered through the knowledge review above. Do not repeat this general question. |
| Q-006 | Population, frequency, and returned state? | “nearly all users, very often nearly each time, when they came back, the system auto logged out.” | Reporter reply; qualitative impact only. |
| Q-007 | Computer awake, network connected, another Edge tab actively used? | “Yes, all three” | Reporter reply; answered. Inspect browser-tab suspension separately from device sleep. |
| Q-006a | Work affected after sign-in? | “users have to resign in more frequently, and lost their workspaces after sign in have to rework.” | Follow-up call `call_16d1d19ecdb64b27a4778a3c08d02291`, item 1. Workspace contents remain unverified. |
| Q-007a | Device sleep, network/VPN changes, or another SSO session expiry? | “none of these happened.” | Same follow-up call, item 2; reported exclusions without PROD telemetry. |
| Q-004, Q-008–Q-009 | Local preparation, toolkit substitution, and environment access? | Local reproduction and frontend/backend setup authorized. Missing `@sctoolkit/webkit` mock authorized. No DEV/UAT/STAGING/PROD connectivity. | Reporter instructions; authorization is local. Do not infer permission or connectivity for PROD execution. |

### Material open questions

| ID | Unresolved question and evidence | Consequence | Owner and next action |
| --- | --- | --- | --- |
| O-001 | What recovery applies after suspension crosses access expiry before refresh issuance? Existing intent covers usable refresh credentials. | Expected correction behavior remains undefined for the demonstrated failure. | unknown; resolve this specific boundary from authority or focused clarification. |
| O-002 | Which PROD revisions, effective token settings, and lifecycle events apply? No deployment trace exists. | PROD causation remains unconfirmed. | unknown; obtain permitted deployment and operational evidence. |
| O-004 | Which workspace descriptors or application edits disappear? Only qualitative impact is reported. | Workspace restoration scope remains unclear. | unknown; compare identifiers, parameters, and contents before logout and after sign-in. |

Supporting gaps remain: O-003 paired visible control; O-005 accountable owners; O-006 measured impact; O-007 original browser policies and versions.
These supporting gaps remain open. They must not be replaced with assumed values.

### Knowledge feedback

| Question | Record and outcome | Owner and next action |
| --- | --- | --- |
| Q-005 | REQ-active-session-renewal v3 retains general idle renewal. This clarification added no new business rule. | unknown; use its documented intent and preserve pending publication review. |
| O-001 / O-004 | Suspension recovery and application-edit retention remain unresolved. No clarification supports a knowledge-policy change. | unknown; clarify first, then update affected knowledge, criteria, and append-only audit records before handoff. |

## Reproduction and verification

This update reviews retained runs. It performs no new browser or business-service execution.

| Environment | Retained local identity and limits |
| --- | --- |
| Browser and platform | Edge 155.0.4283.60; Chromium 155.0.8059.80; macOS 26.5 arm64. Original PROD versions remain unknown. |
| Services | Root `http://localhost:8001`; MFE `http://127.0.0.1:8002`; BFF `http://127.0.0.1:8088/api/auth`. |
| Boundaries | H2, synthetic external services, process keys, authorized toolkit stub, and event instrumentation. No environment parity claim. |
| Timing controls | Natural elapsed time; no fake clock, forced freeze, or shortened access lifetime. Observer storage writes can add latency. |
| Comparison | Both retained portal runs use background conditions. No matching continuously visible portal control exists. |

### Steps and retained results

All timestamps are UTC on 19 October 2026.

| Step | Action or condition | Expected result or decision boundary | Recorded result | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Sign in locally and create a workspace. | Local fixture: successful authentication; retain issued metadata. | Login succeeds at 07:51:33.352. Access lifetime is 900 seconds; refresh state is absent. | Run 001 events 4–10. |
| 2 | Switch to another Edge tab. | Observation objective: retain visibility and lifecycle transitions. | Portal becomes hidden at 07:52:00.367 and freezes at 07:55:25.884. | Events 11–12. |
| 3 | Keep the portal hidden across access expiry. | Home schedules issuance before expiry; suspension can prevent timely execution. | Refresh target 08:06:08.000 and access expiry 08:06:33.000 pass during freeze. | Event 10 and token metadata. |
| 4 | Return after 31 minutes, 5.955 seconds hidden. | Recovery without refresh credentials: O-001 OPEN. | Resume at 08:23:06.318; visible at .322; delayed callback at .349. Callback is 1,018,349 milliseconds late. | Events 13–16. |
| 5 | Observe renewal and timeout decisions. | AC-5–AC-7 apply to eligible renewal; absent-credential outcome remains OPEN. | Missing-refresh logout at 08:23:06.398; logout state at .420; HTTP 401 at .477; authentication clear at .478. | Events 19–23; BFF log lines 199, 205–208. |
| 6 | Inspect returned UI evidence. | Evidence objective: bind returned state to run, time, and capture phase. | Run 002 accessibility text includes `Expired Session, please login again.` Run 001 screenshot phase remains unresolved. | Links below. |

[Run 001 raw events](evidence/portal/run-001/browser/browser-events-001.json) establish the chronology.
SHA-256: `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193`.
[The BFF log](evidence/portal/run-001/bff/local-bff-runtime.stdout.log) corroborates expired-access rejection.
[Run 002 events](evidence/portal/run-002/browser/browser-events-001.json) add another background observation.
[Run 002 returned accessibility text](evidence/portal/run-002/browser/return.ax.full.txt) supplies the expiry message.

### Screenshot evidence

[Existing local portal Sign In capture](evidence/portal/run-001/reviews/sign-in-context.jpg).
Capture phase remains unresolved. This image does not establish the returned-page outcome.
Related accessibility-capture metadata describes a pre-scenario capture. No retained binding establishes this screenshot’s phase.
File modification times cannot resolve capture time.
The retained file preserves original JPEG bytes. Its provenance and hash are in [the manifest](evidence/manifest.json).
A correctly attributed return screenshot remains missing.
[The retained Edge smoke screenshot](evidence/browser-final/edge/returned.png) shows synthetic browser interaction after a two-second tab switch.
Its [result](evidence/browser-final/edge/result.json) and trace establish tooling behavior only. It is not portal unit-test evidence.

The separate expired-token service fixture uses port 8089 and deliberately expires access one minute earlier.
It returns 401 for access-based refresh/Extend and 200 for valid-refresh relogin.
It does not establish natural browser recovery. See evidence index C-013.
Edge and local services supported the original run. Present service readiness was not rechecked during this documentation stage.

## Root cause analysis

**Local cause: supported by retained events and inspected source. PROD applicability: inference only.**

The frozen tab misses the access-based refresh-issuance timer.
Access expires before the callback executes, and no refresh credential exists.
On resume, the timeout controller selects automatic logout from the absent refresh state.
The BFF then rejects refresh issuance because access has expired. The error handler clears authentication.

| Finding and evidence | Consequence | Owner and next action |
| --- | --- | --- |
| Home schedules issuance near access expiry; Run 001 freezes across that deadline. | Refresh issuance depends on a timer that suspension can delay beyond validity. | unknown; assess credential availability and resume recovery after O-001 is resolved. |
| Timeout selects logout at .398; HTTP 401 arrives at .477. | The logout decision precedes the rejection. The response is not the first logout trigger. | unknown; evaluate timeout and renewal coordination. |
| No Extend event exists. Logout state begins 98 milliseconds after visibility returns. | The run supports automatic logout. It cannot exclude a brief rendered click window. | unknown; bind future UI captures to lifecycle timestamps and rendered controls. |
| Device sleep and connectivity changes are excluded by the reporter. Local tab freeze is recorded. | Device sleep is unnecessary for the demonstrated local failure. | unknown; inspect original tab lifecycle before claiming PROD causation. |
| Run 001 has no refresh credential. Existing AC-5–AC-6 assume a usable credential. | Existing prompt criteria do not define the entire correction. | unknown; resolve O-001 before design. |

The historical causal review reverses two timeline entries. Raw timestamps take precedence; original bytes remain unchanged.
Missing returned promises in renewal helpers form a separate prompt-completion concern.
No user-selected Extend occurs in Run 001, so that concern is not its demonstrated cause.
Workspace persistence exists in source. The reported workspace loss remains a separate, unverified impact hypothesis.

## Proposed fix and acceptance criteria

The preliminary direction is to make eligible renewal survive delayed browser callbacks and coordinate timeout decisions with renewal completion.
The final design depends on credential policy. No design may assume an absent or expired credential remains usable.
Candidate scope includes MFE lifecycle handling, timeout state, credential issuance, and the BFF refresh contract.
Workspace restoration needs separate confirmation before it enters the correction scope.

With usable refresh credentials, the proposed result is an available Extend action and a prompt that reflects request completion.
Success closes the prompt once. Failure leaves another attempt available under the existing credential-expiry policy.
Recovery without refresh credentials remains OPEN. This document proposes no new PROD timeout value.

### Source-backed preliminary criteria

The following scenarios restate REQ-active-session-renewal v3 AC-5–AC-7.
They are acceptance candidates for this defect, with no corrected execution evidence.

```gherkin
Feature: Preserve the eligible session-renewal prompt

  Scenario: AC-5 waits for renewal completion
    Given an idle-expiry prompt and a usable refresh token
    When the user selects Extend and the request remains pending
    Then exactly 0 successful prompt closures occur before renewal succeeds

  Scenario: AC-6 closes after success
    Given an idle-expiry prompt and a usable refresh token
    When the requested renewal succeeds
    Then the prompt closes exactly 1 time after completion

  Scenario: AC-7 permits another attempt after rejection
    Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
    When the request rejects
    Then exactly 0 successful prompt closures occur
    And another renewal attempt remains available
```

### Proposed regression cases

All correction tests below are `NOT_RUN`. IDs are task-local proposed cases, without executable step definitions.

| Case | Conditions and assertions | Expected behavior source or decision |
| --- | --- | --- |
| TC-01 | Hold Extend pending, then succeed. Assert zero early closures and exactly one closure after success. | AC-5–AC-6; also assert authenticated state after completion. |
| TC-02 | Reject Extend. Assert zero successful closures and availability of another attempt. | AC-7; retain applicable refresh-expiry policy. |
| TC-03 | Natural Edge suspension across 900-second access expiry with usable refresh. Assert TC-01/TC-02 outcomes. | Proposed lifecycle extension; use the Run 001 lifetime as a fixture, not PROD policy. |
| TC-04 | Repeat suspension with refresh absent at return. Record credential state and recovery outcome. | O-001 OPEN; define the acceptance result before implementation. |
| TC-05 | Use expired or revoked credentials. Assert zero authenticated protected requests succeed with those credentials. | Inspected BFF validation boundary; confirm final security criteria during design. |
| TC-06 | Pair visible and hidden portal sessions with identical revisions and settings. Retain lifecycle, requests, and attributed return screenshots. | Investigation control; evaluate each result against its credential conditions. |
| TC-07 | Reauthenticate with two eligible saved workspace descriptors and unchanged entitlements. Compare identifiers and parameters before/after. | Proposed restoration criterion below. Application edits remain outside this fixture. |

```gherkin
Feature: Restore eligible saved workspace descriptors

  Scenario: Proposed descriptor restoration after sign-in
    Given 2 saved workspace descriptors have valid catalog entries and unchanged user entitlements
    And their identifiers and parameters are retained before logout
    When the same user signs in after authentication cleanup
    Then exactly 2 descriptors restore with the same identifiers and parameters
```

The two-descriptor fixture is proposed from inspected persistence paths. It does not establish an approved application-edit retention guarantee.
Resolution evidence: null. Retest: `NOT_RUN`. Closure decision: null.

### Phase readiness

| Named next phase | Status and basis | Blocked action | Assessor, owner, and next action |
| --- | --- | --- | --- |
| Continued intake investigation | READY_WITH_LIMITS; local chain and documented intent support focused evidence collection. | No downstream handoff. | Codex, 20 October 2026; owner unknown; resolve O-001/O-004 and collect paired controls. |
| Correction proposal and impact analysis | NEEDS_CLARIFICATION; absent-credential recovery and workspace scope can change the design. | Correction design, implementation, and closure. | Codex, 20 October 2026; owner unknown; clarify material boundaries, then update knowledge and reassess. |
| PROD cause confirmation | NEEDS_CLARIFICATION; no authorized connectivity or deployment mapping exists. | PROD execution and definitive PROD causation claims. | Codex, 20 October 2026; owner unknown; obtain permitted deployment and lifecycle evidence. |

The user authorized local reproduction, preparation, substitution, and harness improvements.
The earlier documentation request authorized no business-runtime fix. The later patch request below supplies local application authority.
Business review and publication review remain pending.
[Document checks](evidence/defect-document-checks-20261020.json) cover structure and evidence integrity. They establish no passing business behavior.
## User-supplied patch application, 20 October 2026

The user explicitly requested application of `repos/ui/mfe-base/diff` in this chat.
This authorization permits the supplied local changes and necessary compatibility reconciliation.
It does not resolve the broader incident's open business questions.

| Item | Scoped assessment |
| --- | --- |
| Next stage | Apply the supplied patch locally, inspect the result, and run available checks. |
| Readiness | READY for this bounded application. The supplied patch defines the requested result. |
| Scope | Home session timing, refresh-request reuse, access-token reducer, regression tests, and pipeline version. |
| Risk | Medium. Authentication timing and cancellation can affect continued sessions. |
| Existing differences | Pipeline version is already `2.1.4`. Service wrappers already support newer Axios types. |
| Reconciliation | Keep the existing pipeline version and compatible service wrapper signatures. Apply the supplied session changes. |
| Evidence | [Patch application receipt](evidence/patch-application-20261020.json). |
| Limits | Local application does not establish PROD parity, incident closure, or business-policy approval. |
| Assessor / owner | Codex / unknown. |
| Next action | Install repository dependencies through the established setup, then run the recorded tests and type check. |
| Knowledge update | Not applicable. This request supplies implementation bytes and clarifies no domain policy. |

The earlier phase decisions still apply to broader correction design and incident closure.

Patch fidelity checks passed. The pipeline already has the requested version.
The service retains its existing Axios wrapper interfaces.
Jest and TypeScript could not start because `cross-env` and `tsc` are absent.
No automated business assertions ran. The validation receipt records both command failures.
