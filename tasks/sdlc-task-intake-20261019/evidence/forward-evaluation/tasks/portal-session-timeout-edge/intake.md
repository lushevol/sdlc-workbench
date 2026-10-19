---
artifact_kind: defect-report
id: DEFECT-PORTAL-SESSION-EDGE-20261019
version: 1
status: draft
owner: unknown
source_refs: [SRC-REQUEST, SRC-REQ, SRC-INTENT, SRC-ACTIVITY, SRC-PRIOR, SRC-EVENTS, SRC-HOME, SRC-TIMEOUT, SRC-HTTP, SRC-BFF]
related_ids: [REQ-active-session-renewal, single-ui-authentication, single-ui-web, single-ui-bff-api, mfe-base, single-ui-bff]
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

# Portal session ends after a background tab interval

## Classification and scope

- Defect ID: DEFECT-PORTAL-SESSION-EDGE-20261019.
- Confirmation: Reported incident; retained local failure inspected. This evaluation performed no reproduction.
- Requirement / criterion: REQ-active-session-renewal v2; idle-renewal description and AC-5 through AC-7.
- Affected users: Prior intake reports nearly all users, nearly every time. Measured counts remain unavailable.
- Severity: unassessed. Reported interruption and rework lack measured impact and classification rules.
- Priority: unassessed. No owner decision was found.

The request reports Microsoft Edge, another browser tab, and return after about 30 minutes.
The request reports automatic logout without an extension opportunity.
SRC-REQUEST records these supplied symptoms. It contains no observed production trace.

SRC-PRIOR retains earlier answers about the same symptom.
It records PROD, an awake computer, connected network, and active use of another Edge tab.
It excludes device sleep, network or VPN changes, and another SSO session expiry as reported conditions.
It reports frequent sign-in, workspace loss after sign-in, and rework.
These are attributed prior reports. Their original chat records were not accessed during this evaluation.

This task evaluates intake procedure. Its source workspace remains separate from this isolated task root.
The evaluation permits local source and retained evidence inspection only.
It prohibits browser execution, services, network calls, production actions, and portal fix design or implementation.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Portal change proposal and impact analysis | NEEDS_CLARIFICATION | Deployment parity and missing-credential recovery intent remain unresolved. SRC-REQ and SRC-EVENTS support investigation only. | Change proposal, portal design, implementation, and causal PROD claims | unknown; resolve Q-NEW-1 through Q-NEW-3 |

- Assessor: agent:codex, isolated forward evaluation.
- Assessment time: 2026-10-19T15:32:20.633744+00:00.
- Expected behavior: Retain refresh-based renewal after inactivity with usable credentials. Keep the prompt open while renewal remains pending.
- Expected behavior authority: SRC-INTENT, SRC-ACTIVITY, and candidate SRC-REQ AC-5 through AC-7.
- Approval to implement: not established. The supplied evaluation explicitly excludes portal changes.
- Evidence index: evidence/index.md.
- Business review: pending. Intake readiness does not grant approval.

Continued source review remains permitted within the evaluation restrictions.
No status in this task permits a downstream SDLC phase.
Unknown deployed revisions did not prevent the completed local source inspection.

### Existing knowledge review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and retrieval limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Knowledge index, candidate map, requirement index, session topic | SRC-KINDEX, SRC-CINDEX, SRC-RINDEX, SRC-TOPIC; exact hashes in source inventory | Linked session requirement and source navigation | Local files inspected; no registered knowledge resource in current status | Current deployment mapping |
| Requirement and original reply bytes | SRC-REQ v2; SRC-INTENT request-2026-10-15; SRC-ACTIVITY reply-2026-10-15 | Active renewal; retain idle renewal; AC-5 through AC-7 | Documented user intent exists. Publication approval remains pending | Missing-refresh and suspension recovery conditions |
| Historical V1 design lines 102-153 | SRC-V1; source inventory hash | Extend while refresh remains valid | Historical proposal contains 105-minute and 225-minute refresh duration statements | Effective token policy cannot use these examples alone |
| Prior defect intake and harness correction | SRC-PRIOR v4; SRC-HARNESS v5 | Earlier symptom answers and evidence limits | Secondary records retain prior answers. No original chat or production trace was accessed | Deployment identity and incident lifecycle |
| Registry metadata and source workspace status | SRC-REPOS, SRC-CAPS, SRC-SERVICES, SRC-REGSOURCES; retained status | Declared authentication capability, web service, BFF API, repositories, token contract | Declarations identify candidate relationships. They do not prove deployed integration | Effective environment bindings and accountable owners |

No source review found grounds to repeat the general session-policy question.
Another tab's activity does not establish portal-document activity under AC-1 through AC-4.
AC-5 through AC-7 require usable refresh credentials.
Run 001 starts without refresh credentials. This difference prevents treating that run as a failed execution of those complete criteria.

## Reproduction conditions

```yaml
repository_id: mfe-base
repository_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: null
environment_identity: retained-local-run-001; no new execution
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: [SRC-EVENTS]
reported_environment:
  deployment: PROD, attributed prior report
  deployed_revisions: null
  browser_version: null
  operating_system: null
timing_and_actions:
  timezone: null
  login_at: null
  last_action_at: null
  hidden_at: null
  returned_at: null
  elapsed_time: about 30 minutes, reported
  action_sequence: [Sign in, use another Edge tab, return, observe automatic logout]
browser_lifecycle:
  tab_visibility: background interval reported; original lifecycle unmeasured
  browser_sleep_or_discard: null
  device_sleep_or_lock: prior report excludes device sleep; lock unknown
  effective_settings_and_extensions: null
session_and_connectivity:
  expected_session_policy_ref: REQ-active-session-renewal v2; description and AC-5 through AC-7
  observed_token_lifetimes: null
  network_or_vpn_changes: prior report excludes changes; no production telemetry inspected
  sso_state: prior report excludes another SSO session expiry
reproduction_controls:
  foreground_control: no valid continuously visible portal control in reviewed reports
  mocks_and_instrumentation: retained local run uses instrumentation and synthetic external boundaries
  untested_differences: [Deployed revisions, effective token settings, original Edge lifecycle, identity provider state]
```

The revision above identifies retained local source. It does not identify production deployment.
Retained Run 001 records local Edge 155.0.4283.60 on macOS 26.5 arm64.
Its local settings enable sleeping tabs after 15 minutes. Original user settings remain unknown.
The local run used synthetic external services, process keys, H2, and a toolkit stub.
No new test engine, browser, service, or external connector operation ran.

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Sign in and use another Edge tab | Record deployment, session claims, visibility, and timing | Reported sequence only; original trace unavailable |
| 2 | Return after about 30 minutes | Apply documented renewal only when credential conditions hold | Reported logout without extension |
| 3 | Inspect retained local events | Keep local outcomes separate from incident proof | Freeze, late refresh, missing refresh state, automatic logout, HTTP 401, then CLEAR |

## Hypothesis and impact

- Hypothetical mismatch: Browser suspension can bypass the expected renewal opportunity before refresh credentials become available.
- Observed impact: Retained local authentication state clears. Original production impact remains reported.
- Suspected cause: Hidden-tab suspension is plausible. Production causation remains unresolved.
- Evidence limits: No new reproduction, production mapping, valid foreground control, or incident telemetry was obtained.

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| H-1 | A frozen hidden tab delays refresh beyond access expiry | SRC-EVENTS sequences 10-16; SRC-HOME lines 87-100 | Production lifecycle unknown; no valid foreground portal control | Supported locally; unresolved for PROD | unknown; correlate incident lifecycle with deployed source |
| H-2 | Missing refresh state selects automatic logout before a renewal response | SRC-TIMEOUT lines 25-41; SRC-EVENTS sequences 18-22 | Candidate AC-5 assumes usable refresh credentials; recovery policy unresolved | Supported locally; policy boundary open | unknown; resolve Q-NEW-3 |
| H-3 | Network loss, device sleep, or another SSO expiry caused the reported incident | No supporting production observation inspected | SRC-PRIOR Q-007 and Q-007a exclude these conditions as reported | Unsupported in reported conditions | unknown; retain exclusions unless contrary evidence appears |
| H-4 | A 30-minute timeout policy intentionally logs users out | Only approximate elapsed time is reported | SRC-INTENT and SRC-ACTIVITY retain renewal intent; no current 30-minute policy found | Unsupported by bounded review | unknown; inspect effective settings through Q-NEW-1 |

## Resolution and regression

- Proposed investigation: Resolve deployment identity, incident lifecycle evidence, and the missing-credential recovery rule.
- Evidence plan: Compare exact deployed source with retained snapshots. Retain timestamped, redacted lifecycle and request evidence when access permits.
- Fix scope: unknown. This evaluation does not design or implement a portal correction.
- Regression test: pending. Existing prompt criteria guide investigation; background recovery lacks a complete approved predicate.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

Future execution must separate visible and hidden portal controls with matching credential states.
Its records must disclose clocks, mocks, observers, settings, source revisions, and assertion identities.
No future execution is authorized by this evaluation.

The following scenarios restate candidate AC-5 through AC-7. They establish no passing result or publication approval.

```gherkin
Feature: Recorded idle renewal prompt behavior

  Scenario: AC-5 pending renewal
    Given an idle-expiry prompt and a usable refresh token
    When the user selects renewal and its request remains pending
    Then the prompt has zero successful closure transitions before renewal succeeds

  Scenario: AC-6 successful renewal
    Given an idle-expiry prompt and a usable refresh token
    When the requested renewal succeeds
    Then the prompt closes exactly once after completion

  Scenario: AC-7 rejected renewal
    Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
    When the request rejects
    Then the prompt has zero successful closure transitions and permits another renewal attempt
```

## Facts, inferences, and unresolved questions

- Facts: SRC-REQUEST reports Edge, another tab, about 30 minutes, and logout without extension.
- Documented intent: Raw replies retain active and idle renewal. Candidate prompt criteria have explicit credential conditions.
- Retained local facts: Sequence 19 selects automatic logout at 08:23:06.398Z. Sequence 22 records HTTP 401 at 08:23:06.477Z.
- Inference: The retained local mechanism can explain the symptom. It cannot establish production causation.
- Unresolved questions: Q-NEW-1 through Q-NEW-3 remain pending. Their resolution owners are unknown.

### Answer and question log

No questions were sent to the user. Pending questions remain in this task.

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| Supplied Q-KNOWN-1 | Browser, actions, interval, and symptom | Edge; another tab; about 30 minutes; logout without extension | SRC-REQUEST | answered | unknown | Preserve reported facts; avoid duplicate questions |
| Prior Q-KNOWN-2 | Environment, scale, and impact | PROD; nearly all users, nearly every time; workspace loss and rework | SRC-PRIOR Q-001, Q-006, Q-006a | answered qualitatively; secondary source | unknown | Preserve scale limits; no quantified severity claim |
| Prior Q-KNOWN-3 | Awake device, connected network, and active second tab | Yes, all three | SRC-PRIOR Q-007 | answered as reported; secondary source | unknown | Do not re-ask; inspect tab suspension separately |
| Prior Q-KNOWN-4 | Device sleep, VPN/network changes, another SSO session expiry | None reported | SRC-PRIOR Q-007a | answered as reported; secondary source | unknown | Retain exclusions unless contrary evidence appears |
| Review Q-KNOWN-5 | General session intent | Retain active renewal and refresh-token renewal after inactivity | SRC-INTENT; SRC-ACTIVITY; SRC-REQ | answered; publication review pending | unknown | Reuse intent; preserve credential conditions |
| Round 1 Q-NEW-1 | Which incident deployment revisions, effective token settings, and Edge version/settings apply? | unknown | Registry and report review do not resolve effective deployment | pending; not sent | unknown | Mapping can change the affected path; obtain deployment and browser records |
| Round 1 Q-NEW-2 | Which incident timestamps and redacted lifecycle/request records establish freeze, resume, credential presence, and response order? | unknown | SRC-PRIOR has no retained production trace | pending; not sent | unknown | A local mechanism cannot establish incident cause; retain operational evidence when permitted |
| Round 1 Q-NEW-3 | Which recovery outcome applies when refresh credentials are absent, or refresh remains pending after return? | unknown | SRC-REQ AC-5 through AC-7 assume usable refresh credentials | pending; not sent | unknown | Different recovery intent changes correction scope; obtain the narrow owner decision |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| SRC-REQ and exact raw replies already record session intent | A general policy question would repeat available information | unknown | Use the known intent and ask only Q-NEW-3 |
| SRC-EVENTS and exact retained source support a local delayed-refresh chain | The mechanism supports investigation without proving production causation | unknown | Resolve Q-NEW-1 and Q-NEW-2 |
| SRC-HARNESS corrects the original report's capture attribution and test total | Original report conclusions cannot be reused without those limits | unknown | Preserve unresolved return-capture attribution and unsupported earlier count |
| Candidate criteria assume usable refresh credentials; Run 001 lacks them | That run cannot verify the complete candidate prompt criteria | unknown | Resolve Q-NEW-3 before a correction proposal |
| Robot fragments wait for the prompt and click Extend; browser setup can reuse stored context | Inspected fragments do not assert pending renewal, exact closure count, or production parity | unknown | Inspect the complete setup and assertions before any verification claim |

## Sources

All source bytes remain in their original locations.
The inventory records exact locators, hashes, inspection scopes, and authority limits.
Source checkout HEAD was `84a2b84eea0cc588659fcc912f44c0705571c587` during discovery.
Modified guide bytes require their recorded hashes; HEAD alone does not identify them.

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-REQUEST | `/private/tmp/workbench-intake-forward-20261019/tasks/portal-session-timeout-edge/evidence/request.json` | evaluation-request-20261019 | `0c160a6cbe13b62d7b7f1e6e21c6609b4cc8e2332042806ebd1bdf1a08b739f4` | unknown; Exact supplied evaluation scenario and restrictions |
| SRC-REQ | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/candidates/requirements/REQ-active-session-renewal.md` | v2 | `572528b0a218e20e8ccbbbf4c07a9efc2be4a66302520b957ea0b80a0fbcb4d3` | unknown; v2; candidate; recorded intent, no human publication review |
| SRC-INTENT | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/session-renewal-intent-2026-10-15.txt` | request-2026-10-15 | `d3976f80aaeba02b2397d9731a142767225d2a3ee6dcd1a2de351d3d748217e9` | unknown; request-2026-10-15; retained user reply |
| SRC-ACTIVITY | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt` | reply-2026-10-15 | `a9654884d2ff9f2f27a3185268b251694b51145d50aa7bee6ab2d75c911e90e3` | unknown; reply-2026-10-15; retained user reply |
| SRC-PRIOR | `/Users/lushevol/code/github/ratan-release-impact/workbench/docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md` | v4 | `d4fd02b24034daf435beb64b7115a0cdf0cb34cec0c8f7eee95987d03b69e8db` | unknown; v4; secondary retained prior answers; original chat unavailable here |
| SRC-EVENTS | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/execution/portal-session-local-2026-10-19/run-001/browser/browser-events-001.json` | local-run-001-2026-10-19 | `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193` | unknown; local-run-001-2026-10-19; instrumented synthetic external boundaries |
| SRC-EDGE | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/execution/portal-session-local-2026-10-19/setup/edge-runtime-settings.json` | local-setup-2026-10-19 | `82709fc1619d0165c38f20389741616078250280f99efb510098573d3f40ceef` | unknown; local-setup-2026-10-19; not original PROD browser settings |
| SRC-HOME | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/pages/Home/common/useController.ts.snapshot` | f025513f696476a9cc8162681410cbd21e029bcb | `d7f9cb147cf75ba83e164926ccbb64154a9c25ea7d9908248618ed8d366041cc` | unknown; f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes |
| SRC-TIMEOUT | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/components/Timeout/common/useController.ts.snapshot` | f025513f696476a9cc8162681410cbd21e029bcb | `d1e40e3d9c804870b33c239908024e3faab9c2e185cad3b1866a950cd0976bb8` | unknown; f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes |
| SRC-HTTP | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/hooks/service/index.ts.snapshot` | f025513f696476a9cc8162681410cbd21e029bcb | `f25c800dc21f83b730a831f5c9c765dbeaa6b874d37b2c90ff97ca7108e98b45` | unknown; f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes |
| SRC-BFF | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot` | 85d7cc03eb12710d6facf581987fd4ae24fc9844 | `b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a` | unknown; 85d7cc03eb12710d6facf581987fd4ae24fc9844; retained source bytes |
| SRC-HARNESS | `/Users/lushevol/code/github/ratan-release-impact/workbench/docs/reviews/PORTAL_SESSION_HARNESS_REVIEW.md` | v5 | `2d5890a8081c909a547e97247cfe5a82316e29d05fba89b4f1a8645132cd6f8d` | unknown; v5; historical evidence corrections; not portal correction |
| SRC-ROBOT | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/ratan-test-engine/432f898f59fb06414bc14152d6e463a6a1f4eac2/Tests/ratan/workspace/ui/BAU-UI-RP.robot.L185-L204.snapshot` | 432f898f59fb06414bc14152d6e463a6a1f4eac2 | `981fd0d1224ada4786dd164e812ac70157ee3a5e5906d18f1f96fc29b7c205b4` | unknown; 432f898f59fb06414bc14152d6e463a6a1f4eac2; prompt wait and click; complete suite uninspected |
| SRC-BROWSERHELPER | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/code/ratan-test-engine/432f898f59fb06414bc14152d6e463a6a1f4eac2/Resources/keywords/playwright.resource.L93-L142.snapshot` | 432f898f59fb06414bc14152d6e463a6a1f4eac2 | `c2cfbfd93cfb6a26bee50994b6634927e05afa03e532822f1aaadb375c1f0a60` | unknown; 432f898f59fb06414bc14152d6e463a6a1f4eac2; browser can reuse recent stored context |
| SRC-V1 | `/Users/lushevol/code/github/ratan-release-impact/workbench/knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md` | Historical proposal | `66fa08bf2807a8ae864f8cdda0856b531fceffe11dd655b2bde45ce322ee2ac7` | unknown; Historical proposal; 105/225-minute conflict; no current policy authority |

Full procedural and inspected-source inventory: evidence/source-inventory.json.
