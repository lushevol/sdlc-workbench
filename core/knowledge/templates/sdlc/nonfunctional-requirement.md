# Nonfunctional requirement

## Purpose

Specify one measurable quality attribute under explicit operating conditions.
Keep proposed thresholds separate from actual measurement results.

## AI instructions

1. Obtain the quality concern, business source, measurement scope, workload, environment, metric, and acceptance threshold.
2. Define timing boundaries, population, duration, warmup, sampling, exclusions, aggregation, and error handling.
3. Separate load conditions from the business target.
4. Write Gherkin criteria with numeric targets and units.
5. Replace the structured value placeholder with an unquoted YAML number.
6. Mark unresolved methodology and environment details as blockers to reproducible measurement.
7. Do not invent benchmarks, capacity, production objectives, execution results, or human approval.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "nonfunctional-requirement"
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

# {{nonfunctional_requirement_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Source facts and rationale

- Quality attribute: {{attribute}}
- Affected capability or service IDs: {{resource_ids}}
- Business rationale: {{rationale_and_source}}
- Source facts: {{supported_facts}}
- Evidence limit: {{limit}}

## Proposed quality requirement

- Requirement ID: {{requirement_id}}
- Required behavior: {{measurable_quality_statement}}
- Applicability: {{operations_users_and_context}}

## Measurement contract

| Parameter | Required value | Basis or unresolved detail |
| --- | --- | --- |
| Metric and aggregation | {{metric_and_aggregation}} | {{basis}} |
| Comparison and target | {{operator_target_unit}} | {{target_source}} |
| Measurement population | {{included_operations}} | {{population_source}} |
| Start boundary | {{start_event}} | {{instrumentation_requirement}} |
| End boundary | {{end_event}} | {{instrumentation_requirement}} |
| Concurrent load | {{concurrency_and_unit}} | {{load_source}} |
| Workload and arrival pattern | {{data_mix_request_pattern_or_unknown}} | {{basis_or_resolution_action}} |
| Warmup | {{duration_and_unit}} | {{basis}} |
| Measurement duration | {{duration_and_unit}} | {{basis}} |
| Environment and configuration | {{exact_identity_or_null}} | {{missing_details_or_source}} |
| Dataset and access state | {{dataset_identity_and_conditions}} | {{basis}} |
| Sampling and percentile method | {{collection_and_calculation_method_or_unknown}} | {{resolution_action}} |
| Exclusions | {{excluded_observations_and_reason}} | {{basis}} |
| Errors and invalid runs | {{error_reporting_and_validity_rules_or_unknown}} | {{resolution_action}} |
| Evidence retention | {{raw_observations_configuration_and_revisions}} | {{location_or_unknown}} |

## Acceptance criteria

```gherkin
@{{requirement_id}} @{{acceptance_criterion_id}}
Feature: {{quality_outcome}}

  Scenario: {{measurable_quality_scenario}}
    Given {{precise_environment_dataset_and_workload}}
    And {{warmup_condition}}
    When {{load_and_measurement_duration}}
    Then {{metric}} is {{comparison}} {{target}} {{unit}}
    And {{required_measurement_evidence}}
```

```yaml
acceptance_criteria:
  - id: "{{acceptance_criterion_id}}"
    given: >-
      Given {{precise_environment_dataset_and_workload}}
      And {{warmup_condition}}
    when: "When {{load_and_measurement_duration}}"
    then: >-
      Then {{metric}} is {{comparison}} {{target}} {{unit}}
      And {{required_measurement_evidence}}
    measure:
      metric: "{{metric}}"
      operator: "{{equals_or_at_least_or_at_most_or_less_than_or_greater_than}}"
      value: "{{numeric_target_replace_with_unquoted_number}}"
      unit: "{{unit}}"
```

## Verification plan and current results

| Criterion ID | Proposed method | Test and tool IDs | Current result | Execution reference |
| --- | --- | --- | --- | --- |
| {{criterion_id}} | {{method}} | {{test_and_tool_ids_or_unknown}} | {{NOT_RUN_or_evidenced_result}} | {{reference_or_null}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Human review

- Required review scope: {{target_conditions_and_validity_rules}}
- Actual decision reference: {{reference_or_null}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "nonfunctional-requirement"
id: "SAMPLE-NFR-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-SVC-001, SAMPLE-NFR-AC-001]
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

# Authorized invoice response time

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Source facts and rationale

- Quality attribute: Service response time.
- Affected capability or service IDs: SAMPLE-CAP-001 and SAMPLE-SVC-001.
- Business rationale: Define a response target for authorized invoice viewing in the sample.
- Source facts: The context proposes a response target and load conditions.
- Evidence limit: No production objective or measurement result exists.

## Proposed quality requirement

- Requirement ID: SAMPLE-NFR-001.
- Required behavior: The 95th percentile response time shall be 500 milliseconds or less under the stated sample conditions.
- Applicability: Successful authorized invoice requests to the proposed invoice service.

## Measurement contract

| Parameter | Required value | Basis or unresolved detail |
| --- | --- | --- |
| Metric and aggregation | 95th percentile response time | Proposed metric in sample-v1 |
| Comparison and target | <= 500 milliseconds | Illustrative target; real use requires business review. |
| Measurement population | Successful authorized invoice requests only | Denied and failed requests do not enter this percentile. |
| Start boundary | Service receives the request. | Instrumentation remains undefined. |
| End boundary | Service completes its response. | Instrumentation remains undefined. |
| Concurrent load | 20 concurrent customers | Illustrative load in sample-v1 |
| Workload and arrival pattern | unknown | Define request pacing and invoice mix before measurement. |
| Warmup | 2 minutes | Exclude warmup observations from the measurement window. |
| Measurement duration | 10 minutes after warmup | Proposed duration in sample-v1 |
| Environment and configuration | null | No environment, code revision, or deployment identity exists. |
| Dataset and access state | Authenticated customers with owned invoices; dataset identity is unknown. | Define sufficient customers and invoices before execution. |
| Sampling and percentile method | unknown | Specify collection completeness and percentile calculation before execution. |
| Exclusions | Warmup, denied requests, and failed requests | Retain excluded observations separately; they remain relevant to result interpretation. |
| Errors and invalid runs | unknown | Define error reporting and run validity before execution. |
| Evidence retention | Raw observations, exclusions, configuration, code revision, and tool revision | Retention location remains unknown. |

## Acceptance criteria

```gherkin
@SAMPLE-NFR-001 @SAMPLE-NFR-AC-001
Feature: Authorized invoice response time

  Scenario: Measure authorized responses under the sample load
    Given an identified environment serves authenticated customers with owned invoices
    And the approved measurement method defines sampling and run validity
    And 20 concurrent customers complete a two-minute warmup
    When 20 concurrent customers request owned invoices for 10 minutes
    Then the 95th percentile successful authorized response time is at most 500 milliseconds
    And timing starts when the service receives each request
    And timing ends when the service completes each response
    And raw observations and excluded requests are retained
```

```yaml
acceptance_criteria:
  - id: SAMPLE-NFR-AC-001
    given: >-
      Given an identified environment serves authenticated customers with owned invoices
      And the approved measurement method defines sampling and run validity
      And 20 concurrent customers complete a two-minute warmup
    when: "When 20 concurrent customers request owned invoices for 10 minutes"
    then: >-
      Then the 95th percentile successful authorized response time is at most 500 milliseconds
      And timing starts when the service receives each request
      And timing ends when the service completes each response
      And raw observations and excluded requests are retained
    measure:
      metric: 95th percentile response time
      operator: at_most
      value: 500
      unit: milliseconds
```

## Verification plan and current results

| Criterion ID | Proposed method | Test and tool IDs | Current result | Execution reference |
| --- | --- | --- | --- | --- |
| SAMPLE-NFR-AC-001 | Measure responses using the completed measurement contract. | unknown | NOT_RUN | null |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Measurement method and environment are undefined. | The context supplies no configuration or percentile algorithm. | Results would not be reproducible. | unknown | Define instrumentation, calculation, workload, and environment identities. |
| Run validity rules are missing. | The context supplies no error threshold. | A percentile could conceal a failed workload. | unknown | Obtain reviewed error reporting and validity rules. |

## Human review

- Required review scope: Target, load, measurement boundaries, exclusions, and run validity.
- Actual decision reference: null.
````

## Completion checks

- Define a numeric target, comparison, and unit.
- State population, load, warmup, duration, and timing boundaries.
- Define sampling, aggregation, exclusions, and invalid-run handling.
- Identify environment, dataset, implementation, and tool revisions before measurement.
- Match Gherkin, structured criteria, and measurement contract values.
- Use a supported operator and an unquoted number in each structured measure.
- Keep measured results NOT_RUN until retained observations exist.
- Obtain required human review before publication.
