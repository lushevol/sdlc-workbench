# Incident report / postmortem

## Purpose

Record incident impact, evidence, causal analysis, and corrective actions.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Use actual retained observations for real incident claims.
- Label hypotheses and hypothetical timelines explicitly.
- Separate the trigger, contributing conditions, and confirmed cause.
- Give every corrective action an owner, due condition, and measurable completion criterion.
- Preserve original logs and source identities.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: incident-postmortem
id: "{{artifact_id}}"
version: 1
status: draft
owner: unknown
source_refs: []
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# {{incident_title}}

## Incident state and impact

| Incident state | Service and environment | Start | End | Affected users or operations | Measurement source |
| --- | --- | --- | --- | --- | --- |
| {{status}} | {{service_and_environment}} | {{timestamp_or_null}} | {{timestamp_or_null}} | {{measured_impact_or_unknown}} | {{retained_evidence}} |

## Timeline

| Time | Observation or action | Evidence | Actor |
| --- | --- | --- | --- |
| {{timestamp}} | {{event}} | {{retained_reference}} | {{actual_actor_or_unknown}} |

## Response and recovery

Response/tool execution status: {{NOT_RUN_or_evidenced_status}}.
{{actual_actions_results_recovery_checks_and_evidence_limits}}

## Cause analysis

| Classification | Claim | Evidence | Alternatives or missing evidence |
| --- | --- | --- | --- |
| {{confirmed_cause_contributing_condition_or_hypothesis}} | {{claim}} | {{source}} | {{limits}} |

## Corrective actions

| ID | Action | Consequence addressed | Owner | Due condition | Measurable completion | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {{action_id}} | {{action}} | {{consequence}} | unknown | {{condition}} | {{observable_result}} | {{required_evidence}} |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{actual_owner_and_authority_or_unknown}} | {{evidence_limit}} |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| {{fact_inference_or_unknown}} | {{statement}} | {{source_or_missing_evidence}} | {{effect}} | unknown | {{action}} |
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: incident-postmortem
id: "SAMPLE-INCIDENT-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Hypothetical invoice access incident

## Incident state and impact

| Incident state | Service and environment | Start | End | Affected users or operations | Measurement source |
| --- | --- | --- | --- | --- | --- |
| Hypothetical example. | SAMPLE-SVC-001; environment unknown. | null | null | unknown | null |

This sample explores a possible denial of permitted invoice access.
It records no actual incident.

## Timeline

| Time | Observation or action | Evidence | Actor |
| --- | --- | --- | --- |
| null | Hypothetical customer report of denied owned-invoice access. | Scenario premise only; no log exists. | unknown |
| null | Proposed check of request identity and access decision. | No action executed. | unknown |

## Response and recovery

Response/tool execution status: NOT_RUN.
No response or recovery action occurred.
Actual results and recovery evidence remain null.

## Cause analysis

| Classification | Claim | Evidence | Alternatives or missing evidence |
| --- | --- | --- | --- |
| Hypothesis | An incorrect ownership mapping could deny access. | No implementation evidence; hypothetical explanation only. | Identity, policy, and request-routing failures remain possible. |

## Corrective actions

| ID | Action | Consequence addressed | Owner | Due condition | Measurable completion | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-ACTION-001 | Investigate request identity and the access assertion. | A permitted request could be denied. | unknown | Before selecting a corrective change. | Each causal claim has supporting evidence or remains a hypothesis. | Exact revisions, retained observations, and assertion results. |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only. | No actual incident or observations exist. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Proposed intent | SAMPLE-REQ-001 permits owned-invoice access. | Illustrative source SAMPLE-SRC-001. | Defines the hypothetical expected behavior only. | unknown | Obtain the actual access policy. |
| Unknown | No incident observations exist. | Logs, timestamps, impact counts, and deployment identity are absent. | No cause or impact can be confirmed. | unknown | Collect actual evidence before incident analysis. |
````

## Completion checks

- Impact values come from retained evidence.
- Timeline entries identify actual timestamps or explicit unknowns.
- Hypotheses remain separate from confirmed causes.
- Corrective actions have owners and measurable completion criteria.
- No inferred cause is reported as a confirmed defect.
