---
artifact_kind: defect-report
id: DEFECT-portal-background-session-20261019
version: 6
status: draft
owner: unknown
source_refs:
  - SRC-task-portal-consolidation-20261019
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
related_ids:
  - REQ-active-session-renewal
  - REPORT-portal-background-session-reproduction-20261019
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

## Classification and scope

- Defect ID: DEFECT-portal-background-session-20261019.
- Confirmation: Reported PROD symptom and demonstrated local failure. PROD cause and deployment parity remain unresolved.
- Requirement / criterion: REQ-active-session-renewal, idle-renewal description and AC-5 through AC-7. Credential conditions apply.
- Affected users: The reporter states nearly all users, nearly every time. No measured population or occurrence count is retained.
- Severity: unassessed. Repeated sign-in, workspace loss, and rework are reported. Quantified impact and classification rules remain unknown.
- Priority: unassessed. No owner decision is recorded.

The reporter used Microsoft Edge and moved to another tab after portal activity.
The reporter returned around 30 minutes later and saw logout without an extension opportunity.
The reporter confirms the computer stayed awake, the network stayed connected, and another Edge tab was actively used.
The follow-up excludes device sleep, network or VPN changes, and another SSO session expiry as reported conditions.
It reports lost workspaces after sign-in and the need to repeat work.
SRC-portal-intake-reporter identifies the source conversation for reported facts.
SRC-portal-intake-followup-20261019 records direct replies from the original intake chat.
The original report supplies no retained PROD browser trace.

The [existing reproduction report](<evidence/reports/PORTAL_BACKGROUND_SESSION_REPRODUCTION.md.txt>) describes the local execution.
This intake reuses its retained evidence. It records no new portal execution.
The [task manifest](evidence/manifest.json) records canonical evidence paths and hashes.
The [relocation map](evidence/organization-20261020/relocation-map.json) resolves historical locations.
The current task changes documentation and evidence organization only.
Qualitative change risk is medium because snapshot locators and current references must remain consistent.
No existing runtime symbol or business interface changes.
The related capability and service IDs identify the candidate investigation scope.
Their catalog declarations alone do not prove a deployed relationship.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Continue intake evidence collection | READY_WITH_LIMITS | Local failure and documented intent support focused investigation. Credential recovery and paired controls remain unresolved. | All downstream SDLC phases | unknown; collect paired controls and resolve missing-credential recovery |
| Portal correction proposal and impact analysis | NEEDS_CLARIFICATION | Missing-credential recovery, PROD mapping, and workspace impact can change correction scope. | Correction design, implementation, closure, and PROD causation claims | unknown; resolve material gaps before reassessment |
| PROD reproduction | NEEDS_CLARIFICATION | No authorized connection or deployed identity is available. | PROD execution | unknown; obtain permitted access and exact deployment records |

The assessor is Codex, the intake agent.
Assessment date: 2026-10-19.
Evidence references: C-001 through C-012 in the [evidence index](evidence/index.md).
The issue remains open for intake evidence collection.
This consolidation does not authorize a downstream correction handoff.

- Evidence index: [Task evidence](evidence/index.md).
- Verification summary: [Evidence review](verification.md).
- Task record: Version 6 adds authorized evidence relocation to the earlier consolidation and harness corrections.
- History: The earlier [intake](<evidence/reports/PORTAL_SESSION_DEFECT_INTAKE.md.txt>) remains unchanged.

- Expected behavior: Retain renewal after inactivity with usable refresh credentials. Keep the prompt open during renewal; close after success.
- Expected behavior authority: Recorded user intent in REQ-active-session-renewal v2 and its raw replies. Publication review remains pending.
- Approval to implement: The user authorized local preparation, reproduction, toolkit substitution, and harness improvements.
- Current request: Consolidate the issue, understanding, and verification evidence under this task.
- Portal runtime implementation approval: not established in this intake.
- Business review: pending. Intake readiness does not grant approval.

### Existing knowledge review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and retrieval limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Candidate index, session topic, and linked REQ-active-session-renewal | v2; SRC-portal-session-requirement-v2 | Description retains idle renewal. AC-5–AC-7 govern pending, successful, and failed renewal prompts. | Documented user intent; candidate review pending. AC-5 and AC-6 assume a usable refresh token. | Run 001 starts without that credential. Background recovery needs a separate regression. |
| Original user replies and raw manifest | request-2026-10-15; reply-2026-10-15 | Continued activity renewal; keep refresh-token renewal | Exact retained replies support intent. They do not establish effective PROD configuration. | No new server timeout value is specified. |
| Historical session designs V0 and V1 | SRC-confluence-aa082f0221001faa; V0 reviewed through the session topic | V1 proposes Extend after access expiry while refresh remains valid. | Historical proposals conflict on refresh duration: 105 and 225 minutes. V0 also contains competing limits. | Do not select a current refresh lifetime from these examples. |
| Current workspace status and local knowledge files | Local review, 2026-10-19 | No knowledge resource is registered; direct local review was used. | Scope includes indexes, linked requirement, topic, raw replies, and cited design sections. | No PROD source was accessed. |

Activity in another browser tab does not establish portal-document activity under AC-1 through AC-4.
Browser suspension remains a separate boundary in the requirement.
Known intent supports investigation without asking the user to repeat the session rule.

### Workspace restoration source check

The reported workspace loss has a separate evidence boundary.
The local execution records no second login and no before-and-after workspace content comparison.
It therefore cannot verify the reported loss after sign-in.

The following implementation locators use MFE revision `f025513f696476a9cc8162681410cbd21e029bcb`.
The existing source-byte manifest records the inspected files and hashes.

| Claim | Evidence class | Exact locator | Limit |
| --- | --- | --- | --- |
| Workspace changes persist descriptors through both browser stores. | Inspected implementation | `src/hooks/reducer/workspaces.reducers.ts:8-18`; `src/utils/common.ts:46-49` | Persistence of descriptors does not establish persistence of application edits. |
| Logout cleanup excludes workspace keys from localStorage. `CLEAR` leaves workspace fields. | Inspected implementation | `src/utils/common.ts:51-77`; `src/hooks/reducer/root0.reducers.ts:36-45` | This excludes direct descriptor deletion by these paths. Other paths require inspection. |
| Initial state restores descriptors from localStorage. | Inspected implementation | `src/hooks/model/root.ts:125-127,146-147` | Successful post-login restoration remains unexecuted in the retained run. |
| Home validates saved workspaces and persists the resulting list. | Inspected implementation | `src/pages/Home/common/useController.ts:186-199`; `src/utils/common.ts:291-309` | Catalog or entitlement rejection could explain descriptor loss. This remains a hypothesis. |

Unsaved application edits need application-specific retention criteria and evidence.
The checked knowledge describes workspace creation and closure, without an approved restoration guarantee.
Current repository and service catalogs also leave accountable owners and effective PROD deployment identities unknown.

## Reproduction conditions

```yaml
repository_id: mfe-base
repository_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: null
environment_identity: all-local-portal-edge-run-001
reproduction_status: OBSERVED_LOCAL_FAILURE
execution_id: portal-edge-background-001
actual_results: Late refresh, HTTP 401 TOKEN_INVALID_EXPIRED, automatic logout, and CLEAR; returned-page capture phase unresolved
retained_execution_refs:
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
related_repository_revisions:
  mfe-root-config: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  single-ui-bff: 85d7cc03eb12710d6facf581987fd4ae24fc9844
reported_environment:
  deployment: PROD
  deployed_revisions: null
  browser: Microsoft Edge
  browser_version: null
  operating_system: null
local_environment:
  browser_version: 155.0.4283.60
  chromium_version: 155.0.8059.80
  operating_system: macOS 26.5 arm64
  root_origin: http://localhost:8001
  mfe_origin: http://127.0.0.1:8002
  bff_endpoint: http://127.0.0.1:8088/api/auth
timing_and_actions:
  timezone: UTC
  login_at: "2026-10-19T07:51:33.352Z"
  last_action_at: null
  hidden_at: "2026-10-19T07:52:00.367Z"
  returned_at: "2026-10-19T08:23:06.318Z"
  elapsed_time: "1865955 ms hidden until visible; 1865951 ms hidden until resume"
  reported_elapsed_time: about 30 minutes in another Edge tab
  action_sequence:
    - Local login and workspace creation
    - Switch to another Edge tab
    - Leave the portal hidden without DevTools
    - Return without selecting Extend
browser_lifecycle:
  tab_visibility: hidden, then freeze, then resume and visible
  browser_sleep_or_discard: "Local discard snapshot: sleeping (memory pressure)"
  device_sleep_or_lock: "Reporter confirms computer stayed awake; lock state not supplied"
  effective_settings_and_extensions: "Local sleep setting: 15 minutes; original PROD settings and extensions unknown"
session_and_connectivity:
  expected_session_policy_ref: "REQ-active-session-renewal v2; description and AC-5 through AC-7"
  observed_token_lifetimes: "Local access: 15 minutes; login refresh state absent"
  network_or_vpn_changes: "Reporter excludes network and VPN changes; no PROD telemetry retained"
  sso_state: "Reporter excludes another SSO session expiry; local identity boundaries are synthetic"
reproduction_controls:
  foreground_control: "No valid foreground portal control retained"
  mocks_and_instrumentation: "Synthetic external services, H2, process keys, toolkit stub, and event instrumentation"
  untested_differences:
    - Effective PROD revisions and session configuration
    - Original browser policy, memory pressure, lock, and measured PROD identity state
    - Full toolkit behavior and appearance
```

Run 001 uses retained instrumentation, not a versioned regression test.
The evidence plan must identify exact assertion and test revisions before a corrected behavior can pass.
The user authorized the unavailable `@sctoolkit/webkit` mock through the supplied delegation.
No DEV, UAT, STAGING, or PROD connectivity exists for this task.

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Sign in locally and create a workspace | Record issued state and expiry without retaining secrets | Access expiry is 08:06:33Z; refresh state is absent |
| 2 | Switch to another Edge tab at 07:52:00.367Z | Record visibility and lifecycle transitions | Freeze occurs at 07:55:25.884Z |
| 3 | Keep the portal hidden across the refresh target | Test condition: Observe behavior after a missed callback | Refresh target 08:06:08Z passes before access expiry |
| 4 | Resume at 08:23:06.318Z | Proposed policy-dependent behavior: Resolve renewal eligibility before choosing the recovery outcome | Callback runs at 08:23:06.349Z, 1,018,349 ms late |
| 5 | Observe refresh and timeout state | Apply recorded renewal intent with explicit credential eligibility | Automatic logout begins at 08:23:06.398Z; HTTP 401 arrives at 08:23:06.477Z |
| 6 | Observe the returned page | Record the result without asserting PROD parity | Authentication clears at 08:23:06.478Z; Run 001 capture phase remains unresolved |

The [harness review](<evidence/reports/PORTAL_SESSION_HARNESS_REVIEW.md.txt>) records corrections to the earlier evidence attribution.
Run 001's Sign In capture lacks an unambiguous post-return phase binding.
Its retention map describes a capture before the scenario.
This limit does not change the retained lifecycle, request, or authentication-state events.

### Observed local chronology

All times below are UTC on 19 October 2026.
The raw event timestamps establish this sequence.
The original causal review reverses its first two `race_order` entries.

| Event | UTC time | Evidence and interpretation |
| --- | --- | --- |
| Login response | 07:51:33.352 | Access lifetime is 900 seconds; refresh state is absent |
| Portal hidden | 07:52:00.367 | Lifecycle event |
| Tab freeze | 07:55:25.884 | Lifecycle event; local discard snapshot reports sleeping under memory pressure |
| Refresh target | 08:06:08.000 | Scheduled 25 seconds before access expiry |
| Access expiry | 08:06:33.000 | Access becomes expired while the tab remains frozen |
| Resume | 08:23:06.318 | Natural browser lifecycle event |
| Visible | 08:23:06.322 | Hidden-to-visible interval is 1,865,955 milliseconds |
| Delayed callback | 08:23:06.349 | Callback runs 1,018,349 milliseconds after its target |
| Refresh request | 08:23:06.352 | Request uses expired access; refresh state remains absent |
| Missing-refresh logout branch | 08:23:06.398 | Timeout chooses automatic logout before the response |
| Logout state | 08:23:06.420 | `isOnLogout=true` |
| Refresh response | 08:23:06.477 | HTTP 401 `TOKEN_INVALID_EXPIRED` |
| Authentication clear | 08:23:06.478 | Access and refresh state become absent |

The natural browser run uses no fake clock, forced freeze, or shortened access lifetime.
A separate service fixture deliberately uses expired access. It does not establish browser recovery.
See C-013 in the evidence index for that fixture.
The observer adds synchronous storage writes. Small write latency remains possible.
It adds no timers, polling, or background requests.
No Extend event exists in the record.
The evidence cannot exclude a brief click window before disabled buttons rendered.

### Readiness of investigation tools

| Earlier concern | Retained result | Current limit |
| --- | --- | --- |
| Edge installation | Edge 155.0.4283.60 ran the original portal investigation | Current installed version and live services were not rechecked during consolidation |
| Frontend and BFF readiness | Original setup retains health, build, and smoke results | Synthetic boundaries prevent environment equivalence claims |
| Unavailable toolkit | The user authorized a local stub | Full toolkit appearance and behavior remain untested |
| Reusable browser environment | Playwright 1.64.1 passed final Edge, Chromium, and offline installation checks | macOS arm64 tooling checks only; two-second smokes do not repeat portal reproduction |
| Original Robot engine | Browser wrapper uses Playwright 1.49.1; shared launch lacks Edge channel selection | The optional environment is separate; engine installation remains independent |

Edge installation is no longer the sole historical blocker.
The correction still needs credential recovery decisions and controlled follow-up evidence.
PROD causation also needs deployment and effective configuration records.

## Hypothesis and impact

- Hypothetical mismatch: A background session loses the documented renewal path before a refresh credential becomes available.
- Observed impact: Local authentication ends. The reporter described a PROD sign-in interruption.
- Reported business impact: Users repeat sign-in and lose workspaces after sign-in. They must repeat workspace work.
- Reported scope: Nearly all users, nearly every time. These statements are qualitative and have no measured denominator.
- Workspace loss is user-reported. Its contents, persistence boundary, transaction impact, and recovery duration remain unmeasured.
- Suspected PROD cause: The demonstrated local mechanism could explain the report. PROD causation remains unconfirmed.
- Evidence limits: Local substitutions and unknown deployed settings prevent PROD equivalence claims.

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| H-001 | Tab freeze delays renewal and triggers the missing-refresh logout branch | Run 001 events 12–23 and inspected source snapshots | PROD lifecycle and revision mapping absent | Supported locally; open for PROD | unknown; compare effective deployment and lifecycle evidence |
| H-002 | Idle expiry with missing or unusable refresh credentials requires sign-in | Run 001 has no refresh credential; historical designs contain expiry limits | Recorded intent permits renewal with usable refresh credentials. It does not define missing-credential recovery after suspension. | Eligible renewal intent known; missing-credential recovery open | unknown; inspect issuance and effective configuration |
| H-003 | Device sleep, network or VPN changes, or another SSO session expiry causes the reported outcome | No direct PROD lifecycle trace | Reporter excludes all these events. Local tab freeze occurs independently. | Contradicted by reported conditions; telemetry unavailable | unknown; inspect portal tab lifecycle and retained evidence |
| H-004 | Reauthentication loses workspace restoration state | Reporter describes workspace loss after sign-in and rework | Local session traces do not assert workspace contents before and after sign-in | Open; reported impact | unknown; inspect workspace storage and restoration at exact revisions |

## Resolution and regression

- Proposed investigation: Trace the recorded renewal intent through credential issuance, tab suspension, and timeout recovery.
- Fix scope: Candidate paths include MFE lifecycle handling, timeout state, refresh requests, and the BFF refresh contract.
- Regression test: Pending owner review and exact assertion revisions. Proposed scenarios follow.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

### Evidence plan

1. Check retained bytes against existing manifest hashes. Read source snapshots at their exact revisions.
2. Compare raw event timestamps with the causal review. Use timestamps when list order conflicts.
3. Use the recorded idle-renewal intent. Inspect credential eligibility and effective timeout configuration separately.
4. Obtain deployed revisions and effective settings before assessing PROD parity.
5. Design paired foreground and hidden-tab local controls with the same revisions and disposable fixtures.
6. Record login, visibility, freeze, resume, refresh target, request, response, logout, and visible recovery state.
7. Retain control results, configuration identities, source hashes, and instrumentation limits without token secrets.
8. Keep each later execution separate. Add evidence under existing retention rules without replacing earlier bytes.
9. Trace workspace storage and restoration separately. Compare workspace identities and contents before logout and after sign-in.

The current stage reviews existing evidence only. It does not run these follow-up portal controls.
Use task-local evidence paths for future runs. Preserve existing raw snapshots and audit events.
New background scenarios remain proposed. They extend the documented renewal intent without defining new production timeout values.

```gherkin
Feature: Resolve session recovery after a background interval

  Scenario: Preserve renewal while an eligible refresh is pending
    Given REQ-active-session-renewal retains refresh-based renewal after inactivity
    And the local fixture has a 900-second access lifetime and valid renewal credentials
    And the tab resumes after access expiry with one refresh request pending
    When the timeout control evaluates that pending refresh
    Then exactly 0 automatic logout decisions occur before the refresh result
    And exactly 0 logout-state transitions occur while that refresh remains pending
    And a successful refresh leaves exactly 1 authenticated session

  Scenario: Reject renewal when credentials are unusable
    Given access and refresh credentials are expired or revoked
    And the tab resumes with expired access credentials
    When the refresh request returns HTTP 401 TOKEN_INVALID_EXPIRED
    Then exactly 0 authenticated protected requests succeed with those credentials
    And exactly 1 sign-in recovery action is available on the returned page

  Scenario: Compare foreground and hidden-tab renewal
    Given paired local sessions share exact revisions, configuration, and disposable fixture conditions
    And one portal stays visible while the other remains hidden for 1865955 milliseconds
    When the hidden portal returns and both sessions complete their renewal decisions
    Then exactly 2 execution records identify their lifecycle events and renewal outcomes
    And exactly 0 results claim PROD equivalence without deployed revision and policy evidence

  Scenario: Restore eligible saved workspace descriptors after sign-in
    Given 2 saved workspace descriptors have valid catalog entries and unchanged user entitlements
    And their workspace identifiers and parameters are retained before logout
    When authentication cleanup completes and the same user signs in again
    Then exactly 2 descriptors restore with the same identifiers and parameters
    And exactly 0 eligible saved descriptors are removed during Home validation
```

The 900-second lifetime and 1,865,955-millisecond interval come from Run 001.
The scenarios specify proposed regression observations. They have no step definitions or passing execution evidence.
The two-workspace fixture tests source-supported descriptor restoration. Full application edit retention needs separate criteria.
The follow-up must test credential eligibility, recovery behavior, and warning observations before validating a correction.

## Facts, inferences, and unresolved questions

- Facts: The reporter described PROD, Edge, another tab, about 30 minutes, and no usable extension.
- Facts: The reporter confirms awake device, connected network, active use of another tab, and frequent widespread logout.
- Reported facts: Users sign in more frequently, lose workspaces after sign-in, and repeat work.
- Reported facts: No device sleep, network or VPN change, or another SSO session expiry occurred.
- Documented intent: Existing knowledge retains renewal after inactivity through refresh credentials. Candidate publication review remains pending.
- Facts: Run 001 records freeze, delayed refresh, immediate logout selection, HTTP 401, and authentication clear.
- Facts: Run 002 corroborates the background chain. It supplies no valid foreground portal control.
- Inference: The local mechanism is a plausible explanation for the reported symptom.
- Unknowns: Effective PROD configuration, original tab lifecycle, measured impact, and responsible owner identities remain unresolved.

### Answer and question log

Known answers and the latest replies are retained below.
The initial Q-005 missed an existing knowledge source. The source review above corrects that intake error.

| ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | Which environment and browser? | PROD; Microsoft Edge | SRC-portal-intake-reporter | answered | unknown | Do not re-ask; keep original versions unknown |
| Q-002 | Which actions and elapsed time preceded logout? | Portal activity, another Edge tab, return around 30 minutes later | SRC-portal-intake-reporter | answered | unknown | Do not re-ask; seek exact timing only if material |
| Q-003 | Was an extension opportunity available? | The reporter saw logout without an opportunity | SRC-portal-intake-reporter | answered | unknown | Preserve as reported; compare local control behavior |
| Q-004 | Is local reproduction authorized? | Yes; the unavailable toolkit mock is authorized | SRC-portal-intake-reporter | answered | unknown | Continue within local scope and disclose substitutions |
| Q-005 | What should happen after return, and where is the session rule? | “these requirements (system intends) can be find in knowledge, I don’t need to explain again.” | SRC-portal-intake-reporter; latest reply; requirement and raw sources above | intent resolved; suspension boundary open | unknown | Use documented idle renewal and AC-5–AC-7; inspect missing-credential recovery separately |
| Q-006 | How many users, how often, and what appeared on return? | “nearly all users, very often nearly each time, when they came back, the system auto logged out.” | SRC-portal-intake-reporter; earlier reply | answered qualitatively | unknown | Preserve reported scale; see Q-006a for subsequently reported workspace loss |
| Q-007 | Was the computer awake, network connected, and another Edge tab actively used? | “Yes, all three” | SRC-portal-intake-reporter; latest reply | answered | unknown | Exclude device sleep and disconnection as reported conditions; inspect tab suspension separately |
| Q-005a | Which session rule applies after about 30 minutes in another tab? | “You can get the answer from knowledge right, that's how the harness working” | SRC-portal-intake-followup-20261019; first answer | resolved through linked knowledge | unknown | Use REQ-active-session-renewal and cited raw intent; do not re-ask |
| Q-006a | What work or data did logout affect, and who confirms policy and revisions? | “users have to resign in more frequently, and lost their workspaces after sign in have to rework. You can get answer from knowledge.” | SRC-portal-intake-followup-20261019; second answer | impact answered qualitatively; registry ownership and deployment identity unresolved | unknown | Record repeated sign-in, workspace loss, and rework; inspect restoration separately |
| Q-007a | Did device sleep, network or VPN changes, or another SSO session expiry occur? | “none of these happened.” | SRC-portal-intake-followup-20261019; third answer | answered as reported | unknown | Do not re-ask these conditions without conflicting evidence; retain the tab-freeze hypothesis |

### Additional supplied decisions

| ID | Supplied detail | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- |
| Q-008 | Local frontend and backend preparation may proceed | Source conversation; user preparation instruction | authorized | unknown | Reuse retained local setup evidence |
| Q-009 | No DEV, UAT, STAGING, or PROD connectivity exists | Source conversation; package access reply | answered | unknown | Keep investigation local; disclose environment substitutions |
| Q-010 | Use the sibling project as an installation reference; toolkit mock is acceptable | Source conversation; package access reply | authorized | unknown | Preserve toolkit substitution provenance |
| Q-011 | Start each issue from a template; drill ambiguities before downstream work | Source conversation; SDLC process instruction | recorded | unknown | Apply task intake and preserve answers |
| Q-012 | Use `repos/` for implementation and test sources | Source conversation; correction of `reports/` | answered | unknown | Keep reports as investigation summaries |
| Q-013 | Create this issue under Task with understanding and verification evidence | [Current request](evidence/task-request.txt) | completed by consolidation | unknown | Maintain this task as the continuing issue record |

### Open material questions

These items remain unresolved after the bounded knowledge and source review.
They do not prevent this documentation consolidation.
They block the correction handoff shown above.

| ID | Question | Evidence already reviewed | Owner | Consequence and next action |
| --- | --- | --- | --- | --- |
| O-001 | What recovery applies when suspension outlasts access validity before any refresh credential exists? | Requirement description, AC-5–AC-7, raw replies, historical V1, Run 001 issuance | unknown | Recovery scope can change; confirm this boundary without repeating general session policy |
| O-002 | Which deployed revisions, effective lifetimes, browser settings, and lifecycle events match PROD? | Local manifests, catalogs, reported conditions | unknown | PROD causation remains unconfirmed; obtain authorized deployment and operational records |
| O-003 | Does an equivalent visible portal renew under the same credential conditions? | Both retained runs use background conditions | unknown | Visibility comparison remains incomplete; execute paired local controls |
| O-004 | Which workspace descriptors or application edits disappear after sign-in? | Reporter answers and exact workspace implementation locators | unknown | Recovery scope remains unclear; capture before-and-after identifiers, parameters, and contents |
| O-005 | Who owns severity, priority, implementation, and business review? | Current repository and service catalogs | unknown | Accountability remains unresolved; identify owners and impact classification rules |
| O-006 | What measured incident counts, lost-work duration, and transaction impact exist? | Qualitative reporter answers only | unknown | Severity lacks measured impact; collect permitted operational evidence |
| O-007 | Which original extensions, lock state, browser version, and fleet policies applied? | Reported awake device and local Edge settings | unknown | Browser applicability remains limited; retain original environment identity when available |


### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| Q-005 general inactivity renewal | REQ-active-session-renewal v2 | Existing raw intent describes general inactivity renewal; suspended-tab recovery remains unspecified | ALREADY_CURRENT; v2 AC-5–AC-7; no new rule | Existing requirement provenance; no new governance change | Candidate; unknown; resolve O-001 before correction |
| Task evidence ownership | Knowledge storage contract and source manifest before relocation | Organization request assigns incident evidence to this task | UPDATED; guidance and 58 snapshot paths; AC-OWN-1 and AC-OWN-2 | AUD-20261020-RAW-portal-task-relocation-v2; organization report | No business publication; Codex; retain canonical task paths |
| Clarification feedback | Shared knowledge and intake procedures before this stage | Organization request requires knowledge updates after completed clarification | UPDATED; shared skills and intake templates; AC-FEEDBACK-1 | Organization report; no domain governance change | No business publication; Codex; apply the rule before handoff |
| O-001 missing-credential recovery | Session requirement boundary; REQ-active-session-renewal v2 | No completed clarification establishes recovery after suspension without refresh | OPEN; pending; no new criterion | Original open-question log; no governance change | Candidate; unknown; complete clarification and update knowledge |

The [organization request](organization-request.md) records the user's storage and knowledge-feedback instructions.
The [migration report](organization-verification.md) records that work and its checks.
This organizational work does not resolve the original portal defect.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Requirement v2 and raw replies record idle renewal | Repeating the policy question delayed intake and obscured intent | unknown | Search linked knowledge and source bytes before each new question round |
| Q-006 reports widespread frequent logout without measured counts | Severity and priority lack a classification basis | unknown | Use the qualitative impact now; obtain measured impact when available |
| Q-006a reports workspace loss and rework after sign-in | The impact extends beyond sign-in interruption | unknown | Trace workspace persistence and restoration with before-and-after content checks |
| Run 001 records automatic logout before the refresh response | The local timeout selects logout while renewal remains pending | unknown | Review proposed pending-refresh criteria against policy |
| PROD revisions and original lifecycle evidence are unavailable | The local mechanism cannot establish PROD causation | unknown | Obtain deployment identity and permitted operational evidence |
| Neither retained run supplies a valid foreground portal control | The local comparison lacks a baseline for visibility effects | unknown | Execute paired controls after test design review |
| Causal review list order puts expiry before the earlier refresh target | List order can mislead timeline interpretation | unknown | Use raw timestamps and preserve the original review bytes |
| The Run 001 retention map identifies the Sign In capture before the scenario | Post-return visual attribution remains unresolved | unknown | Preserve the limit and bind future captures to run, time, navigation, origin, and phase |

## Sources

Paths below are relative to this Workbench root unless stated otherwise.
Execution revisions identify retained local runs. They do not identify PROD deployments.
The [raw manifest](../../knowledge/raw/manifest.yaml) resolves existing source IDs and hashes.

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-task-portal-consolidation-20261019 | [Request](evidence/task-request.txt), [manifest](evidence/manifest.json), and [verification review](verification.md) | task-consolidation-2026-10-19 | See task manifest | Codex; evidence organization and review; no fresh portal execution or business approval |
| SRC-portal-intake-reporter | Codex source chat `01a152fa-aff2-7582-aaf4-8e7b4d9c7f2f`; supplied delegation, known answers and authorization | null | null | unknown; reported experience and delegated authorization; no direct PROD trace or policy approval |
| SRC-portal-intake-followup-20261019 | Original intake chat `01a15450-d00a-7d32-91ee-34e5a648cb59`, 19 October 2026; direct reply to `request_user_input_async` call `call_16d1d19ecdb64b27a4778a3c08d02291`, answer items 0–2 | user-reply-2026-10-19 | null | user report; confirms impact and excluded conditions; no retained PROD telemetry or deployment identity |
| SRC-session-renewal-intent-2026-10-15 | `knowledge/raw/session-renewal-intent-2026-10-15.txt` | request-2026-10-15 | `d3976f80aaeba02b2397d9731a142767225d2a3ee6dcd1a2de351d3d748217e9` | unknown; recorded user intent; publication review pending |
| SRC-session-activity-and-idle-intent | `knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt` | reply-2026-10-15 | `a9654884d2ff9f2f27a3185268b251694b51145d50aa7bee6ab2d75c911e90e3` | unknown; exact replies retain activity and refresh renewal |
| SRC-portal-session-requirement-v2 | [Active session renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md), description and AC-5–AC-7 | v2 | `572528b0a218e20e8ccbbbf4c07a9efc2be4a66302520b957ea0b80a0fbcb4d3` | unknown; candidate synthesis of recorded user intent; background suspension remains separate |
| SRC-confluence-aa082f0221001faa | [Raw V1](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>), lines 133–141 | sha256:66fa08bf2807a8ae864f8cdda0856b531fceffe11dd655b2bde45ce322ee2ac7 | `66fa08bf2807a8ae864f8cdda0856b531fceffe11dd655b2bde45ce322ee2ac7` | unknown; historical proposal supports Extend while refresh is valid; duration conflict remains |
| SRC-portal-run001-d1f015546cc4cb277d | `tasks/portal-background-session-20261019/evidence/portal/run-001/browser/browser-events-001.json` | local-run-001-2026-10-19 | `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193` | unknown; instrumented local observations only |
| SRC-portal-run002-06b888608f75bf62a4 | `tasks/portal-background-session-20261019/evidence/portal/run-002/browser/browser-events-001.json` | local-run-002-2026-10-19 | `516512a5fc833446ffb7e310b6b2b863fef4994caa02ec1158a34b7dcde1f172` | unknown; second background observation; no foreground portal control |
| SRC-portal-run001-review-6b95269bba2c54ca89 | `tasks/portal-background-session-20261019/evidence/portal/run-001/reviews/causal-review.json` | local-run-001-review-2026-10-19 | `f9b53633fc2fb5e89c6095561fb4441acab95e84eb59799116b1715f82ab542c` | unknown; derived local review; timeline list order requires timestamp checking |
| SRC-portal-run001-review-6bb4b44e8782aedac0 | `tasks/portal-background-session-20261019/evidence/portal/run-001/reviews/sign-in.ax.full.txt` | local-run-001-review-2026-10-19 | `18a2616ee57c125ea843815598568c378f0e2edc8872d105189d550693c486a4` | unknown; Sign In content is visible; post-return capture phase remains unresolved |
| SRC-portal-run001-review-e3ccceebbcd3c2d0f8 | `tasks/portal-background-session-20261019/evidence/portal/run-001/retention-map-v2.json` | local-run-001-review-2026-10-19 | `6d5adf0446935383c119b228d6791c486d9613a91b9a96b7b033f85738a52369` | unknown; retention metadata identifies the capture before the scenario |
| SRC-portal-local-d08eca66d6d7927aaa | `tasks/portal-background-session-20261019/evidence/portal/setup/edge-runtime-settings.json` | local-setup-2026-10-19 | `82709fc1619d0165c38f20389741616078250280f99efb510098573d3f40ceef` | unknown; local Edge settings; no original user settings |
| SRC-portal-local-51b499197b9cb44755 | `tasks/portal-background-session-20261019/evidence/portal/setup/local-mfe/source-byte-manifest.json`; exact-revision Git reads for workspace locators above | f025513f696476a9cc8162681410cbd21e029bcb | `ee1f2db9d84706479ddc91963720163a1131c446a9f30df439e7324bdc1b981e` | unknown; eight inspected source hashes match the retained manifest; no post-login workspace execution |
| SRC-portal-local-b41c647cf1c7bb26a0 | `tasks/portal-background-session-20261019/evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/pages/Home/common/useController.ts.snapshot:87-100` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source schedules refresh 25 seconds before access expiry |
| SRC-portal-local-e9ea73b748a7c4c086 | `tasks/portal-background-session-20261019/evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/components/Timeout/common/useController.ts.snapshot:25-41` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source selects logout when refresh state is absent |
| SRC-portal-local-bd6b128e6441085c98 | `tasks/portal-background-session-20261019/evidence/source-snapshots/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/hooks/service/index.ts.snapshot:27-43` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source sends access state in the refresh request |
| SRC-portal-local-a3c4f7a97404e81afb | `tasks/portal-background-session-20261019/evidence/source-snapshots/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot:303-324` | 85d7cc03eb12710d6facf581987fd4ae24fc9844 | See raw manifest | unknown; source validates access before refresh issuance; no approved business intent |
