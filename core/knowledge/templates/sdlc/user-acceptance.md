# User acceptance record

## Purpose

Record business acceptance scope, evidence, exceptions, and an actual human decision.

## AI instructions

1. Required inputs: business requirements, measurable acceptance criteria, acceptance owner, and reviewed scope.
2. Required inputs: test procedures, exact tested revisions, environment identity, retained results, and unresolved exceptions.
3. Use the agreed Gherkin scenarios as acceptance examples.
4. Keep acceptance pending until an identified human records a decision.
5. Do not treat test execution, knowledge review, or document maturity as business acceptance.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "user-acceptance"
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

# {{acceptance_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and participants

- Release ID: {{release_id}}
- Included requirements: {{requirement_ids}}
- Exclusions: {{excluded_behavior_and_reason}}
- Business owner: unknown
- Intended reviewer: null
- Acceptance procedure: {{reviewed_procedure_locator_or_unknown}}

## Acceptance examples

```gherkin
Feature: {{acceptance_capability}}

  @{{requirement_id}} @{{criterion_id}} @{{test_id}}
  Scenario: {{acceptance_example}}
    Given {{initial_business_condition}}
    When {{business_action}}
    Then {{observable_expected_result_and_limit}}
```

## Results and evidence

| Criterion ID | Test ID | Exact tested revision | Environment identity | Expected result | Actual result | Execution status | Retained evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{criterion_id}} | {{test_id}} | null | null | {{expected_result}} | null | NOT_RUN | null |

## Exceptions

| Exception ID | Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- | --- |
| {{exception_id_or_none}} | {{evidence_or_gap}} | {{acceptance_impact}} | unknown | {{resolution_action}} | null |

## Human acceptance decision

```yaml
acceptance_state: pending
decision: null
reviewer: null
reviewed_at: null
approval: null
decision_evidence: null
accepted_scope: null
conditions: []
audit_event_ref: null
```

## Evidence limits

- Limits: {{missing_execution_or_review_or_scope_evidence}}
- Required follow-up: {{specific_evidence_needed_before_acceptance}}

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
artifact_kind: "user-acceptance"
id: "SAMPLE-UAT-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REL-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-AC-001, SAMPLE-AC-002, SAMPLE-TEST-001, SAMPLE-TEST-002]
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

# Invoice portal user acceptance

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and participants

- Release ID: SAMPLE-REL-001.
- Included requirements: SAMPLE-REQ-001 and SAMPLE-REQ-002.
- Exclusions: Staff access lacks a supplied rule.
- Business owner: unknown
- Intended reviewer: null
- Acceptance procedure: unknown. No reviewed procedure exists.

## Acceptance examples

```gherkin
Feature: Accept invoice access behavior

  @SAMPLE-REQ-001 @SAMPLE-AC-001 @SAMPLE-TEST-001
  Scenario: Customer accepts owned invoice access
    Given customer "A" is authenticated
    And customer "A" owns invoice "INV-001"
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice
    And the invoice identifier is "INV-001"

  @SAMPLE-REQ-002 @SAMPLE-AC-002 @SAMPLE-TEST-002
  Scenario: Customer accepts denied invoice access
    Given customer "B" is authenticated
    And customer "B" has no permission to view invoice "INV-001"
    When customer "B" requests invoice "INV-001"
    Then the response contains zero invoices
    And the response message is "Access denied"
```

## Results and evidence

| Criterion ID | Test ID | Exact tested revision | Environment identity | Expected result | Actual result | Execution status | Retained evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | SAMPLE-TEST-001 | null | null | One invoice; identifier INV-001 | null | NOT_RUN | null |
| SAMPLE-AC-002 | SAMPLE-TEST-002 | null | null | Zero invoices; message "Access denied" | null | NOT_RUN | null |

## Exceptions

| Exception ID | Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-UAT-GAP-001 | Neither acceptance test has executed | Acceptance lacks observed behavior | unknown | Retain test results and request actual business review | null |

## Human acceptance decision

```yaml
acceptance_state: pending
decision: null
reviewer: null
reviewed_at: null
approval: null
decision_evidence: null
accepted_scope: null
conditions: []
audit_event_ref: null
```

## Evidence limits

- Limits: No exact tested revision, execution result, business reviewer, or acceptance decision exists.
- Required follow-up: Identify the owner, review the scope, execute the tests, and record the human decision.

## Facts, inferences, and unresolved questions

- Facts: The sample context states that no acceptance has occurred.
- Inferences: The two supplied access examples could support a future acceptance review.
- Unresolved questions: The business owner, reviewed procedure, and acceptance reviewer remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | Business acceptance remains pending | unknown | Obtain retained results and an actual human acceptance decision |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Acceptance examples match measurable criteria and reviewed scope.
- Execution results identify exact revisions, environment, and retained evidence.
- Each exception has evidence, consequence, owner, and next action.
- The decision identifies the actual reviewer, decision, scope, and evidence.
- Record real governance decisions through a new audit event.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
