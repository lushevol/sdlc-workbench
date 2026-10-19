---
type: Requirement
id: illustrative-requirement
version: 1
owner: replace-owner
governance_state: candidate
status: draft
sources:
- resource: illustrative://fixture/one-item
  revision: example-v1
  sha256: 15826082e182d7add64f52f46a81d453de0ccabf0d3732dfd29fdc9bd12ea6e9
generated:
  by: illustrative-template
  at: '2026-10-14T00:00:00Z'
verified: []
description: Return one item for one valid request.
rationale: Use a bounded fixture to demonstrate an observable result.
acceptance_criteria:
- id: AC-1
  given: Given one valid fixture request
  when: When the fixture processes the request
  then: Then the response contains exactly one item
  measure:
    metric: response item count
    operator: equals
    value: 1
    unit: count
---
# Illustrative Requirement

This example records no business asset or approval. Replace each example value before use.

## Description

Return one item for one valid request.

## Rationale

Use a bounded fixture to demonstrate an observable result.

## Acceptance criteria

```gherkin
Scenario: Return one fixture item
  Given one valid fixture request
  When the fixture processes the request
  Then the response contains exactly one item
```

Measure the response item count. The expected value is 1.
