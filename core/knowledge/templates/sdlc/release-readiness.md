# Release readiness assessment

## Purpose

Assess release evidence, unresolved risks, and required human decisions before deployment.

## AI instructions

1. Required inputs: release scope, artifact identities, exact revisions, reviewed readiness conditions, and responsible owners.
2. Required inputs: retained test results, acceptance decisions, deployment plans, rollback evidence, and unresolved defects.
3. Identify the evidence required for each readiness condition.
4. Keep missing evidence pending. Do not infer readiness from a document checklist.
5. Keep the readiness assessment separate from deployment authorization.
6. Include a confidence score, technical release status, and prioritized actions that raise the score.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "release-readiness"
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

# {{readiness_title}}

## Release scope

- Release ID: {{release_id}}
- Included requirement IDs: {{requirement_ids}}
- Deliverable identities: {{package_or_service_ids}}
- Exact revisions: {{revision_inventory_or_null}}
- Intended environment: {{environment_identity_or_unknown}}
- Exclusions: {{excluded_scope_and_reason}}

## Readiness conditions

| Condition | Required evidence | Actual evidence | State | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| {{measurable_reviewed_condition}} | {{evidence_requirement}} | {{evidence_ref_or_null}} | pending | unknown | {{specific_next_action}} |

## Execution evidence

```yaml
execution_status: NOT_RUN
repository_revision: null
test_revision: null
actual_results: null
retained_execution_refs: []
acceptance_decision_ref: null
rollback_execution_status: NOT_RUN
rollback_results: null
```

## Risks and exceptions

| Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- |
| {{risk_evidence_or_gap}} | {{release_impact}} | unknown | {{resolution_or_mitigation}} | null |

## Confidence score and release status

| Dimension | Score (0-5) | Status | Critical | Evidence and rationale | Owner | Action to increase confidence | Target score/status | Expected release-status effect | Closure evidence |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| {{applicable_dimension}} | {{0_to_5}} | {{SUPPORTED_LIMITED_FAILED_UNKNOWN_NOT_APPLICABLE}} | {{true_or_false}} | {{evidence_and_limit}} | unknown | {{specific_action}} | {{target_score_and_status}} | {{expected_release_status_effect}} | {{evidence_required_to_close}} |

```yaml
evidence_confidence_score: 0
confidence_level: UNDETERMINED
evidence_confidence: UNDETERMINED
confidence_score_basis: null
release_status: BLOCKED
can_go: false
confidence_increasing_actions:
  - id: RC-ACT-001
    priority: P0
    owner: unknown
    current_score: 0
    current_status: UNKNOWN
    action: "{{specific_action}}"
    evidence_to_close: "{{closure_evidence}}"
    target_score: 4
    target_status: SUPPORTED
    expected_release_status_effect: "{{expected_release_status_effect}}"
    reassess_when: "{{reassessment_trigger}}"
```

The score supports the stated recommendation. It does not predict incident probability.
Only `GO` means the release can proceed technically. `CONDITIONAL`, `NO_GO`, and `BLOCKED` require further action.
Human deployment authorization remains separate.

## Readiness conclusion and authorization

```yaml
readiness_state: pending
readiness_decision: null
reviewer: null
reviewed_at: null
decision_evidence: null
deployment_authorization: null
authorizing_actor: null
authorized_at: null
audit_event_ref: null
```

- Evidence limits: {{limits_that_prevent_a_readiness_claim}}
- Remaining work: {{specific_evidence_or_decisions_required}}

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
artifact_kind: "release-readiness"
id: "SAMPLE-READY-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REL-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001, SAMPLE-UAT-001, SAMPLE-DEPLOY-001]
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

# Invoice portal release readiness

## Release scope

- Release ID: SAMPLE-REL-001.
- Included requirement IDs: SAMPLE-REQ-001, SAMPLE-REQ-002, and SAMPLE-NFR-001.
- Deliverable identities: SAMPLE-SVC-001 is proposed. No built artifact identity exists.
- Exact revisions: null
- Intended environment: unknown
- Exclusions: Staff access lacks a supplied rule.

## Readiness conditions

| Condition | Required evidence | Actual evidence | State | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Review the release requirements | Actual human review records | null | pending | unknown | Identify the owner and obtain review |
| Observe both access criteria | Inspected assertions and retained results for SAMPLE-TEST-001 and SAMPLE-TEST-002 | null | pending | unknown | Inspect revisions and execute tests |
| Assess the proposed response time target | Reviewed limit and retained performance measurement | null | pending | unknown | Review conditions and collect measurements |
| Obtain business acceptance | Actual acceptance decision for the reviewed scope | null | pending | unknown | Complete SAMPLE-UAT-001 |
| Review deployment and recovery procedures | Reviewed procedures and recovery evidence | null | pending | unknown | Complete SAMPLE-DEPLOY-001 |

## Execution evidence

```yaml
execution_status: NOT_RUN
repository_revision: null
test_revision: null
actual_results: null
retained_execution_refs: []
acceptance_decision_ref: null
rollback_execution_status: NOT_RUN
rollback_results: null
```

## Risks and exceptions

| Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- |
| All readiness evidence is null | The assessment cannot establish release readiness | unknown | Collect and review the required evidence | null |

## Readiness conclusion and authorization

```yaml
readiness_state: pending
readiness_decision: null
reviewer: null
reviewed_at: null
decision_evidence: null
deployment_authorization: null
authorizing_actor: null
authorized_at: null
audit_event_ref: null
```

- Evidence limits: No implementation revision, retained result, acceptance decision, or deployment authorization exists.
- Remaining work: Review the proposed conditions, collect evidence, and record actual readiness and authorization decisions.

## Facts, inferences, and unresolved questions

- Facts: SAMPLE-REL-001 remains proposed. No deployment, rollback, acceptance, or publication has occurred.
- Inferences: The listed conditions could organize a future readiness review.
- Unresolved questions: The release owner, actual deliverable, target environment, and authorization process are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | Release readiness remains pending | unknown | Identify responsible owners and collect reviewed readiness evidence |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Release scope names exact deliverables and revisions when known.
- Each readiness condition cites required and actual evidence separately.
- Each applicable dimension has a score, status, owner, and confidence-increasing action.
- The score and release status answer technical confidence and go/no-go separately from authorization.
- Unresolved risks identify evidence, consequence, owner, and next action.
- Readiness conclusions do not substitute for deployment authorization.
- Decisions cite actual reviewers and retained decision evidence.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
