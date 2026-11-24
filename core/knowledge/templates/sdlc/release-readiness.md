# Release readiness assessment

## Purpose

Assess release evidence, unresolved risks, and required human decisions before deployment.

## AI instructions

1. Required inputs: release scope, artifact identities, exact revisions, reviewed readiness conditions, and responsible owners.
2. Required inputs: retained test results, acceptance decisions, deployment plans, rollback evidence, and unresolved defects.
3. Identify the evidence required for each readiness condition.
4. Keep missing evidence pending. Do not infer readiness from a document checklist.
5. Keep the readiness assessment separate from deployment authorization.
6. Require every applicable candidate unit test to pass, with zero failures and complete declared suite execution.
7. Include a confidence score, technical release status, and prioritized actions that raise the score.
8. Include runtime log evidence as a key metric and independent scorecard dimension.
9. During UAT, collect and analyze remote-system logs for essential paths. Local logs support local development only.

Use the [runtime log evidence procedure](../../../../.agents/skills/release-confidence/references/runtime-log-evidence.md) for inventories, denominators, bindings, and limits.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

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

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

Runtime log evidence assessed: {{qualifying_observations}}/{{required_observations_or_NA}}.
Source environment: {{actual_log_environment_and_source_kind_or_unknown}}. Passing runtime behavior: {{passing_observations}}/{{required_observations_or_NA}}.

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
| All applicable unit tests pass with zero failures and complete execution | Declared inventory, command, revisions, environment, counts, and retained result | null | pending | unknown | Execute the complete applicable suite; resolve genuine failures without weakening checks |
| Remote UAT runtime log evidence is collected and analyzed for essential paths | Declared observations, remote queries, retained logs, candidate bindings, assertion results, and anomaly review | null | pending | unknown | Collect and assess remote evidence; keep local pilot results separate |
| {{measurable_reviewed_condition}} | {{evidence_requirement}} | {{evidence_ref_or_null}} | pending | unknown | {{specific_next_action}} |

## Execution evidence

```yaml
execution_status: NOT_RUN
repository_revision: null
test_revision: null
actual_results: null
retained_execution_refs: []
unit_test_status: NOT_RUN
unit_test_inventory_ref: null
unit_test_command: null
unit_test_total: null
unit_test_passed: null
unit_test_failed: null
unit_test_skipped: null
unit_test_expected_failures: null
unit_test_runner_errors: null
unit_test_completed: false
unit_test_result_ref: null
runtime_log_evidence:
  assessment_status: NOT_RUN
  environment: null
  source_kind: null
  source_ref: null
  observation_inventory_ref: null
  query_and_window_ref: null
  artifact_and_configuration_ref: null
  collection_completeness_ref: null
  retained_logs_refs: []
  per_observation_results_ref: null
  required_observations: null
  definition_supported: null
  acquired: null
  bound: null
  analyzed: null
  evidence_assessed: null
  passing_behavior: null
  anomaly_register_ref: null
  limits: []
acceptance_decision_ref: null
rollback_execution_status: NOT_RUN
rollback_results: null
```

Set unit-test readiness to passing only when all applicable tests pass with zero failures and complete execution.
Keep skipped tests, runner-level expected failures, runner errors, and unavailable results explicit.
Do not hide failures through test removal, narrowed scope, or weakened assertions.
Report each runtime-log numerator against `required_observations`. Use `N/A` when its denominator is zero or unknown.
Full evidence assessment can include failed behavior. Local evidence cannot establish remote UAT readiness.

## Risks and exceptions

| Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- |
| {{risk_evidence_or_gap}} | {{release_impact}} | unknown | {{resolution_or_mitigation}} | null |

## Confidence score and release status

| Dimension | Score (0-5) | Status | Critical | Evidence and rationale | Owner | Action to increase confidence | Target score/status | Expected release-status effect | Closure evidence |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime log evidence | 0 | UNKNOWN | true | Required remote UAT evidence is not recorded | unknown | Collect and assess candidate-bound remote logs | 4/SUPPORTED | Resolve the required UAT evidence gap, then reassess | Inspected observation inventory, remote logs, bindings, assertion results, and anomaly review |
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

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

Runtime log evidence assessed: N/A. The required observation inventory and remote UAT logs are unavailable.
Passing runtime behavior: N/A. No actual application execution is recorded.

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
| All applicable unit tests pass | Complete declared suite, zero failures, matching revisions, and retained results | null | pending | unknown | Execute the applicable suite and investigate failures |
| Assess essential paths with remote UAT logs | Declared observation inventory, remote logs, candidate bindings, assertions, and anomaly review | null | pending | unknown | Configure remote collection and assess UAT observations |
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
runtime_log_evidence:
  assessment_status: NOT_RUN
  environment: unknown
  source_kind: null
  observation_inventory_ref: null
  required_observations: null
  evidence_assessed: null
  passing_behavior: null
  limits:
    - No remote UAT logs or observation results exist for this illustrative sample.
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
- Runtime log evidence appears as a key metric with explicit observation counts and separate passing outcomes.
- UAT evidence identifies remote log systems, queries, deployment bindings, collection limits, and retained results.
- Local development logs remain separate from the required remote UAT evidence.
- The score and release status answer technical confidence and go/no-go separately from authorization.
- Unresolved risks identify evidence, consequence, owner, and next action.
- Readiness conclusions do not substitute for deployment authorization.
- Decisions cite actual reviewers and retained decision evidence.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
