---
artifact_kind: incident-postmortem
id: REVIEW-portal-session-harness-20261019
version: 1
status: draft
owner: unknown
source_refs:
  - HARNESS-SRC-REPORT
  - HARNESS-SRC-CAUSAL
  - HARNESS-SRC-RETENTION
  - HARNESS-SRC-RUN002
related_ids:
  - REPORT-portal-background-session-reproduction-20261019
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

# Portal session harness review and evidence corrections

## Incident state and impact

| Incident state | Service and environment | Start | End | Affected users or operations | Measurement source |
| --- | --- | --- | --- | --- | --- |
| Local mechanism observed; portal fix remains open. | Local portal and BFF; no production access. | 2026-10-19T07:51:33.352Z | 2026-10-19T08:23:07.423Z | One retained local run; production population unknown. | HARNESS-SRC-CAUSAL |

This review covers harness practices and evidence quality.
It supplements the [original report](PORTAL_BACKGROUND_SESSION_REPRODUCTION.md).
It does not close the portal defect or approve session policy.
The original report and raw evidence remain unchanged.

## Timeline

| Time | Observation or action | Evidence | Actor |
| --- | --- | --- | --- |
| 2026-10-19T08:06:08Z | Scheduled refresh target passes while the tab remains frozen. | HARNESS-SRC-CAUSAL, `observed_timing.target_refresh_utc` | Local application |
| 2026-10-19T08:06:33Z | Access token expires. | HARNESS-SRC-CAUSAL, `observed_timing.access_expiry_utc` | Local token policy |
| 2026-10-19T08:23:06.349Z | Delayed refresh callback runs. | HARNESS-SRC-CAUSAL, `observed_timing.refresh_callback_utc` | Local application |
| 2026-10-19T08:23:06.398Z | Timeout selects logout with refresh state absent. | HARNESS-SRC-CAUSAL, `observed_timing.timeout_missing_refresh_utc` | Local application |
| 2026-10-19T08:23:06.477Z | Refresh response reports HTTP 401. | HARNESS-SRC-CAUSAL, `observed_timing.refresh_401_utc` | Local BFF |
| 2026-10-19T08:23:06.478Z | Authentication state clears. | HARNESS-SRC-CAUSAL, `observed_timing.clear_utc` | Local application |

The original causal review reverses the first two events in its `race_order` array.
Its timestamp fields support the corrected order above.
This correction does not change the raw record.

## Response and recovery

Response/tool execution status: Local investigation retained; portal recovery correction NOT_RUN.

The user requested reusable intake and browser setup improvements through separate chats.
The issue intake chat owns clarification tracking and investigation readiness.
The browser setup chat owns test-engine assessment and optional Playwright provisioning.
These tasks retain their own validation and completion evidence.

This stage adds the [browser investigation procedure](../../.agents/skills/verify-implementation/references/browser-investigation.md).
The procedure addresses observer effects, lifecycle conditions, comparisons, chronology, and capture provenance.
The verification skill links this procedure for future browser incidents.
The affected scope is authoring guidance and this review.
Qualitative implementation risk is low; no runtime symbol changes are included.

## Cause analysis

| Classification | Claim | Evidence | Alternatives or missing evidence |
| --- | --- | --- | --- |
| Observed local mechanism | A frozen tab missed refresh; resume initiated logout before the rejected refresh response. | HARNESS-SRC-CAUSAL and raw browser events. | Production configuration and approved recovery policy remain unknown. |
| Evidence correction | The original report's claim of 478 successful tests lacks a matching retained log. | HARNESS-SRC-REPORT, Verification conclusion; retained evidence inventory. | The conversation handoff states 479 total, one error, and two skips. |
| Evidence correction | That handoff implies 476 successful tests, rather than 478. | Arithmetic: 479 minus one error minus two skips. | This arithmetic cannot replace the missing original execution log. |
| Evidence limit | Run 001's Sign In capture does not establish its post-return phase. | HARNESS-SRC-RETENTION describes capture before the scenario. | Capture timing conflicts with the original report's returned-page attribution. |
| Evidence limit | Run 002 repeats the background condition. | HARNESS-SRC-RUN002 identifies a second background portal. | No matching continuously visible portal control was completed. |

Treat the earlier test-success total as unsupported execution evidence.
Treat Run 001's returned-page capture attribution as unresolved.
Run 002 retains a separately identified return accessibility capture.
That capture does not repair Run 001's missing phase binding.
The observed lifecycle, request, and state sequence remains available within its local limits.

## Corrective actions

| ID | Action | Consequence addressed | Owner | Due condition | Measurable completion | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| HARNESS-01 | Use the existing defect template at intake and track material answers. | Informal intake can lose decisions and unresolved conditions. | unknown | Before the next issue investigation handoff. | A populated issue records questions, sources, hypotheses, and scoped readiness. | Dedicated issue intake task. |
| HARNESS-02 | Provide optional isolated browser tooling after test-engine inspection. | Browser availability and lifecycle fidelity can block reproduction. | unknown | Before relying on the new environment. | Retain actual launch, tab visibility, trace, versions, and installation results. | Dedicated browser setup task. |
| HARNESS-03 | Apply the linked browser investigation procedure. | Observer effects and invalid comparisons can weaken conclusions. | unknown | Before the next lifecycle experiment. | The run records settings, observer effects, actual comparison conditions, and capture bindings. | Verification skill and new reference. |
| HARNESS-04 | Preserve result logs and report test statuses separately. | Missing logs and skipped-case counts can overstate completion. | unknown | At each subsequent validation handoff. | Retained command, interpreter, exit code, and original totals support every reported count. | New procedure and this correction. |
| HARNESS-05 | Complete a matching foreground portal comparison when validating a correction. | Repeated background failures do not establish foreground behavior. | unknown | During portal correction verification. | Retained visibility confirms the intended condition throughout the selected interval. | Future execution required. |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| HARNESS-SRC-REPORT | [Original report](PORTAL_BACKGROUND_SESSION_REPRODUCTION.md) | `621096a` | `2a287e9a876b7229e70d3ce07ea47bde63aa782f6401473c9400d493e49c3ed2` | unknown; agent-derived report. | Contains the corrected claims described above; human review pending. |
| HARNESS-SRC-CAUSAL | [Causal review](../../knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/causal-review.json) | `621096a` | `f9b53633fc2fb5e89c6095561fb4441acab95e84eb59799116b1715f82ab542c` | unknown; retained local analysis. | Its first two `race_order` entries reverse timestamp order. |
| HARNESS-SRC-RETENTION | [Run 001 retention supplement](../../knowledge/raw/execution/portal-session-local-2026-10-19/run-001/retention-map-v2.json) | `621096a` | `6d5adf0446935383c119b228d6791c486d9613a91b9a96b7b033f85738a52369` | unknown; artifact provenance record. | Describes the Sign In capture as preceding the scenario. |
| HARNESS-SRC-RUN002 | [Run 002 retention map](../../knowledge/raw/execution/portal-session-local-2026-10-19/run-002/retention-map.json) | `621096a` | `3490eceea5f520431939ed1eb4ae6aa4f80cc91cd5b072a2912879e2afaecf7a` | unknown; artifact provenance record. | Second background portal; no foreground comparison. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | Original audited bytes remain available. | Original report, raw evidence, and audit event. | Corrections can preserve review history. | unknown | Read this supplement with the original report. |
| Unknown | The approved session and recovery policy is unavailable. | Session-policy owner or authoritative requirement. | Local mechanism evidence cannot select the final business rule. | unknown | Resolve the policy through issue intake. |
| Unknown | Production settings and the reporter's browser state remain unavailable. | Authorized deployment and browser records. | Local execution cannot establish production parity. | unknown | Obtain these records when access becomes available. |
| Unknown | Original Workbench test output was not retained with this incident. | Matching command output. | The earlier test count cannot establish successful execution. | unknown | Keep the correction and retain future outputs. |
| Unknown | Run 001 capture time and phase cannot be resolved from retained metadata. | Original capture receipt or timestamp. | Returned-page attribution remains unresolved. | unknown | Preserve the limit; bind future captures at collection. |

The [validation record](../evidence/portal-session-harness-20261019/checks.json) records the automated checks.
Artifact lint passed with four warnings for unknown ownership, unresolved values, and pending reviews.
Business review and ASD writing review remain pending.
