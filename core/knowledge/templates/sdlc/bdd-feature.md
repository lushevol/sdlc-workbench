# BDD feature specification

## Purpose

Describe business behavior through concrete Gherkin examples and explicit evidence links.

## AI instructions

1. Required inputs: requirement IDs, criterion IDs, reviewed rule sources, and proposed test IDs.
2. Required inputs: actors, initial conditions, actions, observable outcomes, and relevant limits.
3. Use Given for conditions, When for one business action, and Then for observable results.
4. Tag each scenario with its requirement, criterion, and planned test IDs.
5. Do not invent roles, permissions, status codes, or thresholds.

Follow the [canonical Gherkin rules](../../../../tasks/README.md#canonical-gherkin-test-cases) for task case definitions and consumer links.
Keep one current definition source. Define ambiguous domain terms, step keywords, and entity identities before handoff.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "bdd-feature"
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

# {{feature_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and business rules

- Capability: {{capability_id_and_description}}
- Included behavior: {{supported_behavior}}
- Exclusions: {{unsupported_behavior_and_reason}}

| Rule ID | Rule statement | Source reference | Review state |
| --- | --- | --- | --- |
| {{rule_id}} | {{source_supported_rule}} | {{source_ref_and_section}} | pending |

## Gherkin specification

```gherkin
Feature: {{business_capability}}

  @{{success_requirement_id}} @{{success_criterion_id}} @{{success_test_id}}
  Scenario: {{successful_example_title}}
    Given {{actor_and_relevant_initial_state}}
    When {{single_business_action}}
    Then {{observable_result}}
    And {{observable_limit_or_additional_result}}

  @{{rejection_requirement_id}} @{{rejection_criterion_id}} @{{rejection_test_id}}
  Scenario: {{rejected_example_title}}
    Given {{actor_and_rejection_condition}}
    When {{single_business_action}}
    Then {{observable_rejection_result}}
    And {{observable_limit_or_additional_result}}
```

## Scenario traceability

| Scenario | Requirement | Criterion | Test ID | Assertion location | Exact test revision | Execution status |
| --- | --- | --- | --- | --- | --- | --- |
| {{scenario_title}} | {{requirement_id}} | {{criterion_id}} | {{test_id}} | {{assertion_location_or_null}} | {{revision_or_null}} | NOT_RUN |

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
artifact_kind: "bdd-feature"
id: "SAMPLE-FEATURE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-AC-001, SAMPLE-AC-002, SAMPLE-TEST-001, SAMPLE-TEST-002]
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

# View invoices

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and business rules

- Capability: SAMPLE-CAP-001 covers invoice viewing.
- Included behavior: An authenticated customer requests invoice INV-001.
- Exclusions: Staff access lacks a supplied rule.

| Rule ID | Rule statement | Source reference | Review state |
| --- | --- | --- | --- |
| SAMPLE-RULE-001 | An authenticated customer can view an owned invoice | SAMPLE-SRC-001#proposed-behavior | pending |
| SAMPLE-RULE-002 | The service denies access when the customer lacks permission | SAMPLE-SRC-001#proposed-behavior | pending |
| SAMPLE-RULE-003 | Denied access returns no invoice content | SAMPLE-SRC-001#proposed-behavior | pending |

## Gherkin specification

```gherkin
Feature: View invoices

  @SAMPLE-REQ-001 @SAMPLE-AC-001 @SAMPLE-TEST-001
  Scenario: Customer views an owned invoice
    Given customer "A" is authenticated
    And customer "A" owns invoice "INV-001"
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice
    And the invoice identifier is "INV-001"

  @SAMPLE-REQ-002 @SAMPLE-AC-002 @SAMPLE-TEST-002
  Scenario: Customer requests an invoice without permission
    Given customer "B" is authenticated
    And customer "B" has no permission to view invoice "INV-001"
    When customer "B" requests invoice "INV-001"
    Then the response contains zero invoices
    And the response message is "Access denied"
```

## Scenario traceability

| Scenario | Requirement | Criterion | Test ID | Assertion location | Exact test revision | Execution status |
| --- | --- | --- | --- | --- | --- | --- |
| Customer views an owned invoice | SAMPLE-REQ-001 | SAMPLE-AC-001 | SAMPLE-TEST-001 | null | null | NOT_RUN |
| Customer requests an invoice without permission | SAMPLE-REQ-002 | SAMPLE-AC-002 | SAMPLE-TEST-002 | null | null | NOT_RUN |

## Facts, inferences, and unresolved questions

- Facts: The context defines ownership, denied access, invoice counts, and the denial message.
- Inferences: These examples represent the supplied access conditions.
- Unresolved questions: The business reviewer and executable assertion locations are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | These scenarios express proposed intent only | unknown | Review the examples and implement assertions at an inspected revision |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Every scenario has real Given, When, and Then steps.
- Tags identify stable requirement, criterion, and test IDs.
- Each Then result can be observed and measured.
- Examples match cited rules without adding business policy.
- Executable assertions and retained executions remain separate evidence.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
