# Operational runbook

## Purpose

Give operators repeatable diagnosis, recovery, and escalation steps for a defined service.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Read the service boundary, access grants, deployment configuration, and actual operating procedures.
- Name the signal, threshold, time window, and owner for each alert.
- Keep service objectives separate from requirement performance targets.
- Use commands only after checking their environment, permissions, and effects.
- Define recovery checks, stop conditions, and escalation before operational use.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: operational-runbook
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

# {{service_runbook_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Service scope

| Service ID | Capability IDs | Repository IDs | Environment | Responsible owner |
| --- | --- | --- | --- | --- |
| {{service_id}} | {{capability_ids}} | {{repository_ids}} | {{environment}} | unknown |

## Preconditions and access

{{required_access_tools_configuration_and_change_permissions}}

## Objectives and alerts

| Signal | Definition and data source | Target or trigger | Window | Owner | Response |
| --- | --- | --- | --- | --- | --- |
| {{signal}} | {{measurement}} | {{approved_target_or_unknown}} | {{window}} | unknown | {{runbook_step}} |

## Diagnosis

| Step | Input or condition | Read operation | Expected observation | Next step |
| --- | --- | --- | --- | --- |
| {{step_id}} | {{condition}} | {{verified_read_operation}} | {{observation}} | {{next_step}} |

## Recovery

| Trigger | Authorized action | Stop condition | Recovery check | Evidence to retain |
| --- | --- | --- | --- | --- |
| {{trigger}} | {{reviewed_action}} | {{stop_condition}} | {{observable_check}} | {{evidence}} |

## Escalation and communication

{{responsible_role_contact_reference_decision_limit_and_authorized_communication_path}}

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
artifact_kind: operational-runbook
id: "SAMPLE-RUNBOOK-001"
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

# Invoice service operations

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Service scope

| Service ID | Capability IDs | Repository IDs | Environment | Responsible owner |
| --- | --- | --- | --- | --- |
| SAMPLE-SVC-001 | SAMPLE-CAP-001 | SAMPLE-REPO-001 | unknown | unknown |

## Preconditions and access

No operational access, registered tool grant, or deployment identity is available.
Operational execution remains NOT_RUN.

## Objectives and alerts

| Signal | Definition and data source | Target or trigger | Window | Owner | Response |
| --- | --- | --- | --- | --- | --- |
| Invoice request failures | Proposed failed-request count; telemetry source unknown. | unknown | unknown | unknown | Establish an approved alert and diagnosis path. |

SAMPLE-NFR-001 proposes a test performance target.
It does not establish a production service objective.

## Diagnosis

| Step | Input or condition | Read operation | Expected observation | Next step |
| --- | --- | --- | --- | --- |
| D1 | Reported invoice access failure. | Obtain retained request evidence through an authorized read tool. | Request identity, environment, timestamp, and outcome. | Identify the affected boundary before recovery. |

## Recovery

| Trigger | Authorized action | Stop condition | Recovery check | Evidence to retain |
| --- | --- | --- | --- | --- |
| unknown | null; no reviewed recovery procedure. | Missing access or deployment identity. | Recheck applicable acceptance assertions after approved recovery. | Actual action and assertion results; currently null. |

## Escalation and communication

Responsible role and contact reference remain unknown.
No communication is authorized by this sample.

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only. | No deployed service or operational procedure is established. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Proposed design | The invoice service checks access. | SAMPLE-ARCH-001 in illustrative source SAMPLE-SRC-001. | Identifies a proposed diagnosis boundary. | unknown | Confirm the deployed boundary from actual evidence. |
| Unknown | Production objectives and recovery steps are missing. | Approved operational sources are absent. | Operators cannot use this sample for recovery. | unknown | Obtain reviewed operating procedures. |
````

## Completion checks

- Each action names its permissions, target environment, and effects.
- Alert targets have approved sources and measurement windows.
- Recovery has stop conditions and observable checks.
- Contacts identify actual responsible roles before use.
- Operational evidence stays separate from proposed design.
