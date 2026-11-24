# Test case

## Purpose

Specify reproducible conditions, actions, assertions, and evidence requirements for one test.

## AI instructions

1. Required inputs: requirement and criterion IDs, fixture specification, interface contract, and expected results.
2. Required inputs: environment identity, test procedure, and inspected code and test revisions when available.
3. Link each expected result to a specific criterion.
4. Inspect assertion code before identifying an assertion as implemented.
5. Keep actual results null until execution evidence exists.

Follow the [canonical Gherkin rules](../../../../tasks/README.md#canonical-gherkin-test-cases) whenever refinement or verification defines cases.
For a task catalog, use these fields within stable case sections in `tasks/<task-id>/06-test-cases.md`.
Link consumers to each case heading. Do not create a duplicate standalone definition.
Always include readable Gherkin with explicit assertions. A procedure table or executable keyword alone is insufficient.
Define each actor, entity, domain term, and custom step keyword through setup or an exact glossary link.
For UI E2E cases, use the [Gherkin quality skill](../../../../.agents/skills/gherkin-quality/SKILL.md).
Keep business intent, exact UI targets, observable assertions, and automation bindings separate.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "test-case"
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

# {{test_case_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Objective and traceability

- Test ID: {{test_id}}
- Requirement: {{requirement_id}}
- Acceptance criterion: {{criterion_id}}
- Test level: {{test_level}}
- Expected behavior source: {{source_ref_and_section}}

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| {{actor_or_resource_or_dependency}} | {{required_state}} | {{fixture_or_setup_evidence_ref}} |

- Environment specification: {{document_id_and_locator}}
- Isolation: {{isolation_requirement}}
- Cleanup: {{cleanup_procedure_locator}}

## Procedure and assertions

```gherkin
@{{test_id}}
Feature: {{required_behavior}}
  Scenario: {{case_title_with_named_entity_and_outcome}}
    Given {{named_actor_entity_and_explicit_initial_state}}
    When {{actor_performs_one_exact_action}}
    Then {{named_observation_equals_expected_value_with_required_limit}}
    And {{additional_explicit_assertion_if_applicable}}
```

Keep numbered steps aligned with the Gherkin sequence.

| Step | Action | Expected observable result | Criterion ID | Actual result |
| --- | --- | --- | --- | --- |
| {{step_number}} | {{exact_action}} | {{expected_value_and_limit}} | {{criterion_id}} | null |

## Execution binding

```yaml
execution_status: NOT_RUN
repository_id: "{{repository_id}}"
repository_revision: null
test_revision: null
assertion_locations: []
environment_identity: null
execution_id: null
actual_results: null
retained_execution_refs: []
```

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
artifact_kind: "test-case"
id: "SAMPLE-TEST-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-AC-001, SAMPLE-CONTRACT-001, SAMPLE-ENV-001]
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

# Customer views an owned invoice

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Objective and traceability

- Test ID: SAMPLE-TEST-001.
- Requirement: SAMPLE-REQ-001.
- Acceptance criterion: SAMPLE-AC-001.
- Test level: Proposed service interface test.
- Expected behavior source: SAMPLE-SRC-001#proposed-behavior.

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| Customer A | Authenticated | null |
| Invoice INV-001 | Owned by customer A | null |
| SAMPLE-SVC-001 | Available in an isolated test environment | null |

- Environment specification: SAMPLE-ENV-001 in test-data-environment.md.
- Isolation: Use the fictional fixture in an isolated test environment.
- Cleanup: unknown. An authorized procedure is required before execution.

## Procedure and assertions

```gherkin
@SAMPLE-TEST-001
Feature: Customer views an owned invoice
  Scenario: Customer A receives invoice INV-001
    Given customer A is authenticated
    And customer A owns invoice INV-001
    And invoice service SAMPLE-SVC-001 is available in the isolated test environment
    When customer A requests GET /invoices/INV-001 from invoice service SAMPLE-SVC-001
    Then the response contains exactly one invoice
    And the returned invoice identifier equals INV-001
```

| Step | Action | Expected observable result | Criterion ID | Actual result |
| --- | --- | --- | --- | --- |
| 1 | Customer A requests invoice INV-001 | Exactly one invoice appears in the response | SAMPLE-AC-001 | null |
| 2 | Inspect the returned invoice identifier | The identifier equals INV-001 | SAMPLE-AC-001 | null |

## Execution binding

```yaml
execution_status: NOT_RUN
repository_id: SAMPLE-REPO-001
repository_revision: null
test_revision: null
assertion_locations: []
environment_identity: null
execution_id: null
actual_results: null
retained_execution_refs: []
```

## Facts, inferences, and unresolved questions

- Facts: SAMPLE-AC-001 requires one invoice with identifier INV-001.
- Inferences: Inspecting the service response could check both expected values.
- Unresolved questions: Authentication setup, executable assertions, environment identity, and cleanup instructions are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | This case cannot establish verified behavior | unknown | Inspect the implementation and record a reproducible setup procedure |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Preconditions identify actor state, data state, dependencies, and environment.
- Gherkin specifies ordered conditions, actions, and explicit observable assertions.
- Actors, entities, custom keywords, data fields, and relevant timing have one clear meaning.
- Consumer documents link the single canonical case definition.
- Procedure steps specify observable values and criterion links.
- Actual results remain separate from expected results.
- Execution evidence identifies exact code and test revisions when available.
- Cleanup and isolation requirements have an owner or an explicit gap.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
