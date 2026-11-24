# Deployment and rollback plan

## Purpose

Define authorized deployment, verification, stop conditions, and recovery procedures.

## AI instructions

1. Required inputs: immutable deliverable identities, exact revisions, target environment, change scope, and service owners.
2. Required inputs: approved runbook commands, access authorization, readiness evidence, recovery objectives, and data protection requirements.
3. Replace template command placeholders with approved commands, or null when commands are unavailable.
4. Keep unavailable structured command values null. Missing runbooks prevent this draft from authorizing execution.
5. Define observable stop conditions and recovery checks from reviewed criteria.
6. Keep deployment and rollback results null until retained execution exists.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "deployment-rollback"
id: "{{stable_artifact_id}}"
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

# {{deployment_plan_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and dependencies

- Release ID: {{release_id}}
- Deliverable identities and hashes: {{immutable_artifact_inventory_or_unknown}}
- Exact repository revision: null.
- Target environment: {{environment_identity_or_unknown}}
- Affected services and contracts: {{service_ids_and_contract_ids}}
- Dependency checks: {{dependency_checks_and_sources}}

## Preconditions and authority

| Precondition | Required evidence | Current evidence | State |
| --- | --- | --- | --- |
| {{reviewed_precondition}} | {{evidence_requirement}} | null | pending |

```yaml
deployment_authorization: null
authorizing_actor: null
authorized_at: null
readiness_decision_ref: null
```

## Procedure and command references

| Phase | Procedure reference | Observable completion condition | Responsible owner |
| --- | --- | --- | --- |
| Prepare | {{approved_preparation_runbook_locator}} | {{preparation_result}} | unknown |
| Deploy | {{approved_deployment_runbook_locator}} | {{deployment_result}} | unknown |
| Verify | {{approved_verification_runbook_locator}} | {{criterion_results_and_limits}} | unknown |
| Roll back | {{approved_rollback_runbook_locator}} | {{recovery_results_and_limits}} | unknown |

```yaml
deployment_command: "{{deployment_command_from_approved_runbook}}"
verification_command: "{{verification_command_from_approved_runbook}}"
rollback_command: "{{rollback_command_from_approved_runbook}}"
```

## Stop conditions and recovery

| Trigger | Required observation | Stop or recovery action | Decision owner |
| --- | --- | --- | --- |
| {{reviewed_trigger}} | {{observable_result_and_limit}} | {{approved_action_reference}} | unknown |

- Data backup and restoration: {{approved_procedure_or_unknown}}
- Migration and compatibility: {{applicable_plan_or_reasoned_not_applicable}}
- Recovery objective: {{reviewed_duration_or_unknown}}
- Escalation: {{contact_role_and_authorized_channel_or_unknown}}

## Execution and retained evidence

```yaml
deployment_status: NOT_RUN
rollback_status: NOT_RUN
verification_status: NOT_RUN
repository_revision: null
test_revision: null
deployment_identity: null
actual_results: null
rollback_results: null
retained_execution_refs: []
```

## Evidence limits

- Limits: {{missing_procedures_or_authorization_or_execution}}
- Remaining preparation: {{specific_next_actions}}

## Facts, inferences, and unresolved questions

- Facts: {{source_supported_facts}}
- Inferences: {{inferences_and_basis_or_none}}
- Unresolved questions: {{questions_and_resolution_owner}}

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| {{evidence_or_explicit_gap}} | {{consequence}} | unknown | {{specific_next_action}} |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_evidence_limits}} |
````

## Illustrative sample

This sample describes proposed invoice portal work.
It records no actual approval or execution.

````markdown
---
artifact_kind: "deployment-rollback"
id: "SAMPLE-DEPLOY-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REL-001, SAMPLE-SVC-001, SAMPLE-CONTRACT-001, SAMPLE-READY-001, SAMPLE-TEST-001, SAMPLE-TEST-002]
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

# Invoice portal deployment and rollback

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and dependencies

- Release ID: SAMPLE-REL-001.
- Deliverable identities and hashes: unknown. No built artifact exists in the context.
- Exact repository revision: null.
- Target environment: unknown.
- Affected services and contracts: SAMPLE-SVC-001 and SAMPLE-CONTRACT-001 are proposed.
- Dependency checks: The proposed invoice store requires inspection. No runtime dependency is established.

## Preconditions and authority

| Precondition | Required evidence | Current evidence | State |
| --- | --- | --- | --- |
| Review exact artifact and target environment | Immutable artifact identity and inspected configuration | null | pending |
| Review readiness and authorize deployment | Actual readiness decision and authorization record | null | pending |
| Review deployment and recovery procedures | Approved runbook and recovery evidence | null | pending |

```yaml
deployment_authorization: null
authorizing_actor: null
authorized_at: null
readiness_decision_ref: null
```

## Procedure and command references

| Phase | Procedure reference | Observable completion condition | Responsible owner |
| --- | --- | --- | --- |
| Prepare | unknown | Artifact identity and target environment match the reviewed scope | unknown |
| Deploy | unknown | Target environment reports the reviewed artifact identity | unknown |
| Verify | unknown | Both access tests produce their reviewed expected results | unknown |
| Roll back | unknown | Recovery checks satisfy reviewed criteria for the restored artifact | unknown |

```yaml
deployment_command: null
verification_command: null
rollback_command: null
```

Command values remain null because no approved runbook is available. This draft cannot authorize execution.

## Stop conditions and recovery

| Trigger | Required observation | Stop or recovery action | Decision owner |
| --- | --- | --- | --- |
| Proposed access criterion mismatch | A retained result differs from SAMPLE-AC-001 or SAMPLE-AC-002 | Stop progression and assess recovery through a reviewed procedure | unknown |

- Data backup and restoration: unknown. No approved procedure exists.
- Migration and compatibility: unknown. The context supplies no migration scope or compatibility assessment.
- Recovery objective: unknown. No reviewed duration exists.
- Escalation: unknown. No responsible operational contact exists.

## Execution and retained evidence

```yaml
deployment_status: NOT_RUN
rollback_status: NOT_RUN
verification_status: NOT_RUN
repository_revision: null
test_revision: null
deployment_identity: null
actual_results: null
rollback_results: null
retained_execution_refs: []
```

## Evidence limits

- Limits: No deployment authorization, executable procedure, actual deployment identity, or recovery result exists.
- Remaining preparation: Obtain approved runbooks, identify owners, review recovery conditions, and record deployment authorization.

## Facts, inferences, and unresolved questions

- Facts: The context states that no deployment or rollback has occurred.
- Inferences: An access criterion mismatch could inform a proposed stop condition after human review.
- Unresolved questions: Deployment procedures, recovery objectives, data protection requirements, and owners remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | This draft cannot authorize or demonstrate a deployment | unknown | Obtain approved procedures, exact artifact identity, and actual authorization |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Artifact identity, exact revision, and target environment are explicit.
- Replace command placeholders with approved commands, or null when commands are unavailable.
- Stop conditions and recovery checks cite reviewed observable criteria.
- Data protection, migration, compatibility, and escalation have evidence or explicit gaps.
- Deployment authorization and retained execution remain separate.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
