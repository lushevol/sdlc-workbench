---
artifact_kind: "defect-report"
id: "portal-intake-repair"
version: 1
status: draft
owner: unknown
source_refs: [SRC-ISSUE]
related_ids: []
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

# Reported portal logout after another tab stays active

## Classification and scope

- Defect ID: portal-intake-repair
- Confirmation: Suspected. SRC-ISSUE reports the symptom. No reproduction has run.
- Requirement / criterion: unknown; source discovery has not started.
- Affected users: unknown.
- Severity: unassessed; impact evidence is unavailable.
- Priority: unassessed; no priority decision was supplied.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Implementation planning | NEEDS_CLARIFICATION | Policy, implementation, environment, and impact remain unknown. Only the reported symptom is available. | Downstream SDLC work; no behavior baseline or reproduction evidence exists. | unknown; Discover registered sources and grants with workspace status after this trial stops. |

- Expected behavior: unknown. No expectation or session policy was supplied.
- Expected behavior authority: unknown; review available sources before asking an owner.
- Approval to implement: not established. This bounded trial authorizes intake repair only.
- Evidence index: not applicable at this checkpoint; no domain investigation artifact exists.
- Business review: pending. Intake readiness does not grant approval.

### Existing knowledge review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and retrieval limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Not started. This trial stops before source discovery. | null; no domain source was read. | unknown; no search has run. | No domain review occurred. A search miss is not asserted. | Expected session policy, environment, and precise timing remain unknown. |

## Reproduction conditions

```yaml
repository_id: "unknown"
repository_revision: null
test_revision: null
environment_identity: null
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: []
reported_environment:
  deployment: null
  deployed_revisions: null
  browser_version: null
  operating_system: null
timing_and_actions:
  timezone: null
  login_at: null
  last_action_at: null
  hidden_at: null
  returned_at: null
  elapsed_time: "reported approximate 30 minutes; no measured interval"
  action_sequence:
    - "Reported: another browser tab stays active before the portal logs out."
browser_lifecycle:
  tab_visibility: null
  browser_sleep_or_discard: null
  device_sleep_or_lock: null
  effective_settings_and_extensions: null
session_and_connectivity:
  expected_session_policy_ref: null
  observed_token_lifetimes: null
  network_or_vpn_changes: null
  sso_state: null
reproduction_controls:
  foreground_control: null
  mocks_and_instrumentation: null
  untested_differences: []
```

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Reported: another browser tab stays active for about 30 minutes. | unknown; policy review is pending. | null |

## Hypothesis and impact

- Hypothetical mismatch: unknown; expected behavior is unavailable.
- Observed impact: SRC-ISSUE reports a logout. No direct observation or business impact measurement exists.
- Suspected cause: unknown; no source or runtime investigation occurred.
- Evidence limits: Tab visibility, elapsed timing, browser lifecycle, policy, connectivity, and implementation remain unknown.

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| H-001 | unknown; no cause is proposed before source discovery. | SRC-ISSUE reports timing only. | No cause check has run. | open | unknown; Discover registered sources and grants with workspace status after this trial stops. |

## Resolution and regression

- Proposed investigation: Discover registered sources and tool grants with workspace status.
- Evidence plan: After discovery, review relevant policy and source revisions. Retain new evidence under this task. No execution is authorized here.
- Fix scope: unknown; no implementation interface was inspected.
- Regression test: pending; the reported symptom is unconfirmed and expected policy is unknown.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

Regression criteria remain proposed until the responsible owner confirms expected policy.
Replace numeric limits only from evidence or an explicitly proposed test condition.

```gherkin
Feature: Pending session policy baseline

  Scenario: Pending policy baseline for the reported tab condition
    Given the environment and approved session policy remain unknown
    When another browser tab stays active for the reported approximate 30 minutes
    Then the required session outcome and exact limit remain unknown
```

## Facts, inferences, and unresolved questions

- Facts: SRC-ISSUE states, "The portal logs out after another browser tab stays active for about 30 minutes."
- Inferences: none. The reported sequence does not establish a cause.
- Unresolved questions: Policy, environment, precise actions, timing, and impact remain unknown. Resolution owner: unknown.

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 0 / Q-001 | Supplied symptom | The portal logs out after another browser tab stays active for about 30 minutes. | SRC-ISSUE; delegated trial scenario. | answered; reported only | unknown | The report supports intake creation. Discover sources before further analysis. |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| SRC-ISSUE provides only a reported symptom. No policy or direct reproduction evidence exists. | Implementation planning remains blocked. | unknown | Discover registered sources and grants after the bounded trial stops. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-ISSUE | Delegated trial scenario message, quoted in Facts and the question log. | null | null; the message has no supplied content hash. | unknown; Reported symptom only. No approved policy, direct observation, or business approval is established. |
