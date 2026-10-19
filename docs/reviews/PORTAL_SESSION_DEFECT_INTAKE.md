---
artifact_kind: defect-report
id: DEFECT-portal-background-session-20261019
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-portal-intake-reporter
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
  - SRC-portal-run001-review-6b95269bba2c54ca89
  - SRC-portal-run001-review-6bb4b44e8782aedac0
  - SRC-portal-local-d08eca66d6d7927aaa
  - SRC-portal-local-b41c647cf1c7bb26a0
  - SRC-portal-local-e9ea73b748a7c4c086
  - SRC-portal-local-bd6b128e6441085c98
  - SRC-portal-local-a3c4f7a97404e81afb
related_ids:
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
- Confirmation: Reported PROD symptom and demonstrated local failure. Approved session-policy mismatch remains unresolved.
- Requirement / criterion: unknown. The session policy owner must supply approved intent.
- Affected users: The reporter described one experience. The affected population and occurrence count remain unknown.
- Severity: unassessed. Business impact and classification rules remain unknown.
- Priority: unassessed. No owner decision is recorded.

The reporter used Microsoft Edge and moved to another tab after portal activity.
The reporter returned around 30 minutes later and saw logout without an extension opportunity.
SRC-portal-intake-reporter supplies these reported facts through the delegated task.
The original report supplies no retained PROD browser trace.

The [existing reproduction report](PORTAL_BACKGROUND_SESSION_REPRODUCTION.md) describes the local execution.
This intake reuses its retained evidence. It records no new portal execution.
The related capability and service IDs identify the candidate investigation scope.
Their catalog declarations alone do not prove a deployed relationship.

### Intake readiness and authority

| Investigation scope | Readiness | Basis and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Inspect retained local source and execution | READY_WITH_LIMITS | Reported expectation, observed logout, environment, timing, actions, interruption impact, and evidence plan are recorded below. | PROD conclusions and policy claims | unknown; review source and retained event order |
| Design a controlled local follow-up | READY_WITH_LIMITS | Local reproduction is authorized. The first runs lack a valid foreground portal control. | Policy-dependent pass criteria | unknown; define paired controls before execution |
| Reproduce in PROD or change portal runtime | NEEDS_CLARIFICATION | Access, deployed revisions, approved policy, and change authority remain unavailable. | PROD execution and business runtime changes | unknown; identify owners and obtain the missing decisions |

- Expected behavior: Proposed expectation: Provide a usable extension when policy permits renewal, or explain why sign-in is required.
- Expected behavior authority: unknown. Q-005 requests the session rule and its source.
- Approval to implement: The delegated task authorizes Workbench intake improvements and local investigation.
- Portal runtime implementation approval: not established in this intake.
- Business review: pending. Intake readiness does not grant approval.

## Reproduction conditions

```yaml
repository_id: mfe-base
repository_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: null
environment_identity: all-local-portal-edge-run-001
reproduction_status: OBSERVED_LOCAL_FAILURE
execution_id: portal-edge-background-001
actual_results: Late refresh, HTTP 401 TOKEN_INVALID_EXPIRED, automatic logout, CLEAR, and Sign In
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
  device_sleep_or_lock: null
  effective_settings_and_extensions: "Local sleep setting: 15 minutes; original PROD settings and extensions unknown"
session_and_connectivity:
  expected_session_policy_ref: null
  observed_token_lifetimes: "Local access: 15 minutes; login refresh state absent"
  network_or_vpn_changes: null
  sso_state: "Synthetic local identity boundaries; original PROD state unknown"
reproduction_controls:
  foreground_control: "No valid foreground portal control retained"
  mocks_and_instrumentation: "Synthetic external services, H2, process keys, toolkit stub, and event instrumentation"
  untested_differences:
    - Effective PROD revisions and session configuration
    - Original browser policy, memory pressure, device sleep, network, VPN, and SSO state
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
| 5 | Observe refresh and timeout state | Proposed behavior: Keep the outcome consistent with the approved policy | Automatic logout begins at 08:23:06.398Z; HTTP 401 arrives at 08:23:06.477Z |
| 6 | Observe the returned page | Record the result without asserting PROD parity | Authentication clears at 08:23:06.478Z; the accessibility record shows Sign In |

## Hypothesis and impact

- Hypothetical mismatch: An eligible session might lose its extension path. Eligibility remains a policy question.
- Observed impact: Local authentication ends. The reporter described a PROD sign-in interruption.
- Data loss, transaction impact, affected users, frequency, and recovery duration: unknown; see Q-006.
- Suspected PROD cause: The demonstrated local mechanism could explain the report. PROD causation remains unconfirmed.
- Evidence limits: Local substitutions and unknown deployed settings prevent PROD equivalence claims.

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| H-001 | Tab freeze delays renewal and triggers the missing-refresh logout branch | Run 001 events 12–23 and inspected source snapshots | PROD lifecycle and revision mapping absent | Supported locally; open for PROD | unknown; compare effective deployment and lifecycle evidence |
| H-002 | Approved idle or absolute expiry requires sign-in | Session policy has not been supplied | Local access expiry alone does not establish approved policy | Open | unknown; answer Q-005 |
| H-003 | Device sleep, network change, or external SSO expiry contributes to the reported outcome | These conditions are currently unknown | Local observations do not establish the original user's conditions | Open | unknown; answer Q-007 |

## Resolution and regression

- Proposed investigation: Resolve policy and impact questions while reviewing the retained local failure chain.
- Fix scope: Candidate paths include MFE lifecycle handling, timeout state, refresh requests, and the BFF refresh contract.
- Regression test: Pending owner review and exact assertion revisions. Proposed scenarios follow.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

### Evidence plan

1. Check retained bytes against existing manifest hashes. Read source snapshots at their exact revisions.
2. Compare raw event timestamps with the causal review. Use timestamps when list order conflicts.
3. Obtain the approved idle, absolute-expiry, renewal, warning, and recovery rules from the policy owner.
4. Obtain deployed revisions and effective settings before assessing PROD parity.
5. Design paired foreground and hidden-tab local controls with the same revisions and disposable fixtures.
6. Record login, visibility, freeze, resume, refresh target, request, response, logout, and visible recovery state.
7. Retain control results, configuration identities, source hashes, and instrumentation limits without token secrets.
8. Keep each later execution separate. Add evidence under existing retention rules without replacing earlier bytes.

The current stage reviews existing evidence only. It does not run these follow-up portal controls.
Policy-dependent scenarios remain proposed. Their conditions do not define a new production session policy.

```gherkin
Feature: Resolve session recovery after a background interval

  Scenario: Preserve renewal while an eligible refresh is pending
    Given an owner-approved policy permits renewal after the tested background interval
    And the local fixture has a 900-second access lifetime and valid renewal credentials
    And the tab resumes after access expiry with one refresh request pending
    When the timeout control evaluates that pending refresh
    Then exactly 0 automatic logout decisions occur before the refresh result
    And exactly 0 logout-state transitions occur while that refresh remains pending
    And a successful refresh leaves exactly 1 authenticated session

  Scenario: Reject renewal when approved expiry requires sign-in
    Given the owner-approved absolute expiry has passed
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
```

The 900-second lifetime and 1,865,955-millisecond interval come from Run 001.
The scenarios specify proposed regression observations. They have no step definitions or passing execution evidence.
The owner must confirm credential eligibility, recovery behavior, and measurable warning limits before implementation.

## Facts, inferences, and unresolved questions

- Facts: The reporter described PROD, Edge, another tab, about 30 minutes, and no usable extension.
- Facts: Run 001 records freeze, delayed refresh, immediate logout selection, HTTP 401, authentication clear, and Sign In.
- Facts: Run 002 corroborates the background chain. It supplies no valid foreground portal control.
- Inference: The local mechanism is a plausible explanation for the reported symptom.
- Unknowns: Approved policy, effective PROD configuration, original browser lifecycle, impact, and responsible owner identities remain unresolved.

### Answer and question log

Known answers are retained below. Questions Q-005 through Q-007 were submitted in this chat on 19 October 2026.
No answers were available when this intake was prepared.

| ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | Which environment and browser? | PROD; Microsoft Edge | SRC-portal-intake-reporter | answered | unknown | Do not re-ask; keep original versions unknown |
| Q-002 | Which actions and elapsed time preceded logout? | Portal activity, another Edge tab, return around 30 minutes later | SRC-portal-intake-reporter | answered | unknown | Do not re-ask; seek exact timing only if material |
| Q-003 | Was an extension opportunity available? | The reporter saw logout without an opportunity | SRC-portal-intake-reporter | answered | unknown | Preserve as reported; compare local control behavior |
| Q-004 | Is local reproduction authorized? | Yes; the unavailable toolkit mock is authorized | SRC-portal-intake-reporter | answered | unknown | Continue within local scope and disclose substitutions |
| Q-005 | Which session rule applies after about 30 minutes in another tab? | unknown | Current chat question; no answer yet | pending | unknown; session policy owner required | Define renewal eligibility, expiry limits, warning, and recovery |
| Q-006 | Which work or data was affected, and who confirms policy and deployed revisions? | unknown | Current chat question; no answer yet | pending | unknown | Establish impact, severity basis, responsible owners, and deployment mapping |
| Q-007 | Did device sleep, network or VPN changes, or SSO expiry occur? | unknown | Current chat question; no answer yet | pending | unknown; reporter input required | Refine competing explanations and local control conditions |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Q-005 has no policy source | Approved session-policy mismatch cannot be classified | unknown | Supply the applicable policy and owner decision |
| Q-006 has no business impact details or owner identities | Severity and priority remain unassessed | unknown | Confirm affected work, frequency, population, and responsible owners |
| Run 001 records automatic logout before the refresh response | The local timeout selects logout while renewal remains pending | unknown | Review proposed pending-refresh criteria against policy |
| PROD revisions and original lifecycle evidence are unavailable | The local mechanism cannot establish PROD causation | unknown | Obtain deployment identity and permitted operational evidence |
| Neither retained run supplies a valid foreground portal control | The local comparison lacks a baseline for visibility effects | unknown | Execute paired controls after test design review |
| Causal review list order puts expiry before the earlier refresh target | List order can mislead timeline interpretation | unknown | Use raw timestamps and preserve the original review bytes |

## Sources

Paths below are relative to this Workbench root unless stated otherwise.
Execution revisions identify retained local runs. They do not identify PROD deployments.
The [raw manifest](../../knowledge/raw/manifest.yaml) resolves existing source IDs and hashes.

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-portal-intake-reporter | Codex source chat `01a152fa-aff2-7582-aaf4-8e7b4d9c7f2f`; supplied delegation, known answers and authorization | null | null | unknown; reported experience and delegated authorization; no direct PROD trace or policy approval |
| SRC-portal-run001-d1f015546cc4cb277d | `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/browser/browser-events-001.json` | local-run-001-2026-10-19 | `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193` | unknown; instrumented local observations only |
| SRC-portal-run002-06b888608f75bf62a4 | `knowledge/raw/execution/portal-session-local-2026-10-19/run-002/browser/browser-events-001.json` | local-run-002-2026-10-19 | `516512a5fc833446ffb7e310b6b2b863fef4994caa02ec1158a34b7dcde1f172` | unknown; second background observation; no foreground portal control |
| SRC-portal-run001-review-6b95269bba2c54ca89 | `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/causal-review.json` | local-run-001-review-2026-10-19 | `f9b53633fc2fb5e89c6095561fb4441acab95e84eb59799116b1715f82ab542c` | unknown; derived local review; timeline list order requires timestamp checking |
| SRC-portal-run001-review-6bb4b44e8782aedac0 | `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/sign-in.ax.full.txt` | local-run-001-review-2026-10-19 | `18a2616ee57c125ea843815598568c378f0e2edc8872d105189d550693c486a4` | unknown; local accessibility record shows Sign In |
| SRC-portal-local-d08eca66d6d7927aaa | `knowledge/raw/execution/portal-session-local-2026-10-19/setup/edge-runtime-settings.json` | local-setup-2026-10-19 | `82709fc1619d0165c38f20389741616078250280f99efb510098573d3f40ceef` | unknown; local Edge settings; no original user settings |
| SRC-portal-local-b41c647cf1c7bb26a0 | `knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/pages/Home/common/useController.ts.snapshot:87-100` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source schedules refresh 25 seconds before access expiry |
| SRC-portal-local-e9ea73b748a7c4c086 | `knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/components/Timeout/common/useController.ts.snapshot:25-41` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source selects logout when refresh state is absent |
| SRC-portal-local-bd6b128e6441085c98 | `knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/hooks/service/index.ts.snapshot:27-43` | f025513f696476a9cc8162681410cbd21e029bcb | See raw manifest | unknown; source sends access state in the refresh request |
| SRC-portal-local-a3c4f7a97404e81afb | `knowledge/raw/code/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot:303-324` | 85d7cc03eb12710d6facf581987fd4ae24fc9844 | See raw manifest | unknown; source validates access before refresh issuance; no approved business intent |
