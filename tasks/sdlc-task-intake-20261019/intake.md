---
artifact_kind: requirement
id: REQ-task-intake-20261019
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-task-intake-request-20261019
  - SRC-task-intake-clarification-20261019
  - SRC-task-intake-template-20261019
  - SRC-task-intake-authoring-20261019
  - SRC-task-intake-skill-20261019
  - SRC-task-intake-example-20261019
related_ids:
  - DEFECT-portal-background-session-20261019
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Retain evidence and resolve material intake gaps before downstream work

## Description

As a project user, I need each requirement or issue to start in its own root task folder.
The agent must select a template and resolve material understanding gaps before downstream work.
The agent must retain new investigation evidence under that task.
The task must state the supported next stage and any evidence limits.

## Rationale

The user requires evidence before progression to the next SDLC stage.
The [exact request](evidence/request.txt) supplies the workflow intent.
Prior portal intake supplies a concrete consumer for source review and question retention.
Existing documents and source snapshots must retain their locations and history.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Create `tasks/<task-id>/` before discovery for a received requirement or issue. | Copy business repository runtime into Workbench. | Repository independence remains required. |
| Select the requirement or defect template and preserve stable identity. | Publish approved knowledge from intake readiness. | Publication requires separate human review. |
| Review domain knowledge, repository code, tests, reports, and investigation results. | Treat reports or tests as approved business intent. | Each source has separate authority and limits. |
| Ask focused questions after source review. Retain answers and unresolved gaps. | Repeat known policy questions without a source conflict. | Existing sources and answers can resolve questions. |
| Collect relevant browser, service, and test evidence during intake. | Infer PROD access from catalog declarations. | Live execution needs applicable authorization and supported access. |
| Retain task evidence and a scoped readiness decision. | Claim unobserved behavior or a complete cause from partial evidence. | Readiness and runtime verification remain separate. |

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Intake agent | RULE-task-folder | A new issue or requirement arrives. | Create its task folder before discovery. Select the matching template. | SRC-task-intake-request-20261019 |
| Intake agent | RULE-task-sources | The task needs context. | Inspect knowledge, repos code, tests, reports, and investigation results. Record source limits. | SRC-task-intake-request-20261019 |
| Intake agent | RULE-task-drilling | A material ambiguity remains after source inspection. | Ask focused questions. Preserve the answer, evidence, consequence, owner, and next action. | SRC-task-intake-request-20261019; SRC-task-intake-skill-20261019 |
| Intake agent | RULE-task-investigation | Available documents cannot establish current behavior. | Collect relevant authorized browser, service, or test evidence during intake. | SRC-task-intake-request-20261019 |
| Intake agent | RULE-task-retention | A task collects new evidence. | Save that evidence under the same task. Link existing immutable sources in place. | SRC-task-intake-request-20261019; SRC-task-intake-authoring-20261019 |
| Intake agent | RULE-task-gate | A material understanding gap affects the named next stage. | Set NEEDS_CLARIFICATION and block that downstream stage. Continue independent intake investigation. | SRC-task-intake-request-20261019; SRC-task-intake-skill-20261019 |
| Intake agent | RULE-task-handoff | Evidence resolves material understanding gaps for a named next stage. | Record supported readiness, evidence limits, and blocked claims. Keep approvals separate. | SRC-task-intake-request-20261019; SRC-task-intake-skill-20261019 |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| SRC-task-intake-template-20261019 | Supplies this task's authoring form. | Requirement Template block. | None identified for this draft. |
| SRC-task-intake-skill-20261019 | Supplies existing intake guidance. | Source review, questions, hypotheses, and scoped readiness. | Guidance must state task retention before discovery. |
| SRC-task-intake-authoring-20261019 | Separates authored documents and governed knowledge. | Workbench storage and validation sections. | Approval remains pending. |
| DEFECT-portal-background-session-20261019 | Supplies an existing consumer and evidence pattern. | Existing portal intake. | Existing evidence remains at its retained locations. |

## Acceptance criteria

```gherkin
@REQ-task-intake-20261019
Feature: Evidence-supported task intake

  @AC-task-intake-1
  Scenario: Receive a requirement or issue
    Given a received requirement or issue has no existing task intake
    When the agent starts intake
    Then exactly one task folder exists under the workspace root tasks directory before discovery
    And that folder contains an intake based on the matching existing template

  @AC-task-intake-2
  Scenario: Retain evidence under the task
    Given an intake collects new evidence and cites existing sources
    When the agent updates its evidence index
    Then zero collected evidence items lack a task-local retained file or an explicit retention limit
    And existing immutable sources keep their original locations and hashes

  @AC-task-intake-3
  Scenario: Resolve understanding through available sources and questions
    Given the task requires domain intent and implementation context
    When the agent assesses the named next stage
    Then zero relevant source classes lack an inspection result or an explicit availability limit
    And material questions retain answers or unresolved findings

  @AC-task-intake-4
  Scenario: Prevent downstream progression with a material gap
    Given a material understanding gap affects the named next stage
    When the agent records readiness
    Then zero downstream actions start within that blocked scope
    And readiness is NEEDS_CLARIFICATION with an owner and next action
    And independent intake evidence collection can continue

  @AC-task-intake-5
  Scenario: Support a bounded intake handoff
    Given retained evidence resolves understanding for a named next stage
    When the agent records READY
    Then zero unresolved material understanding blockers affect that named next stage
    And the handoff states evidence, limits, and blocked claims
    And knowledge publication and implementation approvals remain separate
```

```yaml
acceptance_criteria:
  - id: AC-task-intake-1
    given: Given a received requirement or issue has no existing task intake
    when: When the agent starts intake
    then: Then exactly one task folder exists before discovery and contains the selected intake template
    measure:
      metric: task folder count for the received item
      operator: equals
      value: 1
      unit: count
  - id: AC-task-intake-2
    given: Given an intake collects new evidence and cites existing sources
    when: When the agent updates its evidence index
    then: Then zero collected evidence items lack a task-local file or an explicit retention limit
    measure:
      metric: evidence items without retention or an explicit limit
      operator: equals
      value: 0
      unit: count
  - id: AC-task-intake-3
    given: Given the task requires domain intent and implementation context
    when: When the agent assesses the named next stage
    then: Then zero relevant source classes lack an inspection result or an explicit availability limit
    measure:
      metric: relevant source classes without an assessment
      operator: equals
      value: 0
      unit: count
  - id: AC-task-intake-4
    given: Given a material understanding gap affects the named next stage
    when: When the agent records readiness
    then: Then zero downstream actions start within that blocked scope
    measure:
      metric: downstream actions started within the blocked scope
      operator: equals
      value: 0
      unit: count
  - id: AC-task-intake-5
    given: Given retained evidence resolves understanding for a named next stage
    when: When the agent records READY
    then: Then zero unresolved material understanding blockers affect that named next stage
    measure:
      metric: unresolved material understanding blockers for the named next stage
      operator: equals
      value: 0
      unit: count
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| AC-task-intake-1 | Inspect task path and execution order. Check selected template sections. | Current checkout and a received task. | Per received item. Performance limits are not requested. | Task path and isolated trial action order. See verification.md for the recorded ordering limit. |
| AC-task-intake-2 | Compare evidence index, retained files, source hashes, and retention limits. | Same task and its cited sources. | Each evidence update. Load is not specified. | Evidence index, packaging checks, and actual file hashes. See verification.md. |
| AC-task-intake-3 | Inspect source assessments and the question log. | Relevant knowledge, reports, code, tests, and investigations. | Before each named handoff. Load is not applicable. | Isolated trial source inventory, prior-answer reuse, questions, and limits. See verification.md. |
| AC-task-intake-4 | Inspect the blocked scope and subsequent actions. | An intake with a material gap. | Until the gap is resolved. Load is not applicable. | Isolated trial blocks downstream work. Its action history retains the decision. See verification.md. |
| AC-task-intake-5 | Compare the named stage with evidence and unresolved questions. | An intake with sufficient bounded evidence. | At each handoff. Load is not applicable. | This task records scoped READY with request and clarification evidence. No universal agent-compliance claim is made. |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| AC-task-intake-1 | tasks/README.md and shared intake guidance | Workbench working bytes; packaging-final.json records exact hashes. | See verification.md for assertions and procedure limits. | evidence/runtime-tests-retry.log and retained procedure trial |
| AC-task-intake-2 | tasks/README.md and shared intake guidance | Workbench working bytes; packaging-final.json records exact hashes. | See verification.md for assertions and procedure limits. | evidence/runtime-tests-retry.log and retained procedure trial |
| AC-task-intake-3 | tasks/README.md and shared intake guidance | Workbench working bytes; packaging-final.json records exact hashes. | See verification.md for assertions and procedure limits. | evidence/runtime-tests-retry.log and retained procedure trial |
| AC-task-intake-4 | tasks/README.md and shared intake guidance | Workbench working bytes; packaging-final.json records exact hashes. | See verification.md for assertions and procedure limits. | evidence/runtime-tests-retry.log and retained procedure trial |
| AC-task-intake-5 | tasks/README.md and shared intake guidance | Workbench working bytes; packaging-final.json records exact hashes. | See verification.md for assertions and procedure limits. | evidence/runtime-tests-retry.log and retained procedure trial |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SRC-task-intake-request-20261019 | [evidence/request.txt](evidence/request.txt) | User message received 2026-10-19; local exact-text snapshot. | `f94891ee30e34d8094492d6b5130c74d4fa2a5537b10eb44ebdb6e41d95d07d4` | User request; workflow intent. | No independent production behavior or execution proof. |
| SRC-task-intake-clarification-20261019 | [evidence/clarification.txt](evidence/clarification.txt) | User answer received 2026-10-19; local exact-text snapshot. | `a31c89d399de19dc9654667c7ff9d79279e3d9cb15469cc3344e68d6ace9b1f6` | User clarification; code and test source location. | Does not authorize unrelated external access or prove execution. |
| SRC-task-intake-template-20261019 | [../../knowledge/templates/sdlc/requirement.md](../../knowledge/templates/sdlc/requirement.md) | 84a2b84eea0cc588659fcc912f44c0705571c587 | `683b026efac19a21bbf0d799e9333e612dcfb6ccd56ecb4ae15aa353297c9510` | Project source; inspected instructions or prior intake. | Source bytes do not establish passing execution or human approval. |
| SRC-task-intake-authoring-20261019 | [../../knowledge/templates/sdlc/README.md](../../knowledge/templates/sdlc/README.md) | 84a2b84eea0cc588659fcc912f44c0705571c587 | `751196a1ee10a1aa52d11af564df367e255e7045b9c8febf2f92a09ffa06a8b9` | Project source; inspected instructions or prior intake. | Source bytes do not establish passing execution or human approval. |
| SRC-task-intake-skill-20261019 | [../../.agents/skills/analyze-requirement/SKILL.md](../../.agents/skills/analyze-requirement/SKILL.md) | 84a2b84eea0cc588659fcc912f44c0705571c587 | `7a9722cf8cbab5a5bccf3576ccf86ed54cec1cef71d81ed9fd710370cd41a1ce` | Project source; inspected instructions or prior intake. | Source bytes do not establish passing execution or human approval. |
| SRC-task-intake-example-20261019 | [../../docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md](<../portal-background-session-20261019/evidence/reports/PORTAL_SESSION_DEFECT_INTAKE.md.txt>) | 84a2b84eea0cc588659fcc912f44c0705571c587 | `d4fd02b24034daf435beb64b7115a0cdf0cb34cec0c8f7eee95987d03b69e8db` | Project source; inspected instructions or prior intake. | Source bytes do not establish passing execution or human approval. |

Hashes record bytes inspected during intake.
Git-source hashes match the stated revision through `git show`.
Later edits require a separate source revision entry.
The existing portal intake was inspected only for its source review, readiness, and reproduction sections.

## Evidence and open questions

### Facts, inferences, and unresolved questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | The user requires a task folder before discovery. | SRC-task-intake-request-20261019 | Task creation starts intake. | unknown | Add explicit guidance and checks. |
| Fact | The request names knowledge, reports, and investigation results. | Exact request lines 5–9. | All relevant evidence classes need assessment. | unknown | Inspect each relevant source class. |
| Fact | The request allows browser, service, and test investigation to clarify current behavior. | Exact request lines 13–17. | Intake can include evidence collection. | unknown | Apply only relevant authorized tools. |
| Fact | Knowledge approval and passing runtime evidence remain separate. | SRC-task-intake-authoring-20261019 | Readiness cannot publish approved knowledge. | unknown | Preserve separate review fields. |
| Inference | “drilling with stock” requests focused evidence-based clarification. | Request context and existing intake skill. | Preserve the phrase without inventing a named method. | unknown | Use focused questions and source review. |
| Fact | The user confirms repos/ supplies code and tests. | SRC-task-intake-clarification-20261019 | The material source-location ambiguity is resolved. | unknown | Use repositories in place. Retain new evidence under the task. |
| Fact | Scaffold and offline assertions were inspected and executed. | verification.md and evidence/source-review.json | Selected distribution boundaries passed. Agent-procedure limits remain explicit. | Codex | Retain the scoped verification evidence. |

### Question log

| Question ID | Material question | Answer | Answer source | Status | Resolution owner | Consequence | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q-task-intake-1 | Does “reports directory” mean reports, repositories under repos, or another registered asset? | “Yes, use repos/ for code and tests” | SRC-task-intake-clarification-20261019 | RESOLVED | User clarification recorded. | Code and test discovery uses repos/. | Update workflow guidance and retain repositories in place. |

### Hypotheses

| Hypothesis | Supporting evidence | Contradicting evidence | Status | Next action |
| --- | --- | --- | --- | --- |
| “reports directory” may mean repository source and test assets. | The request describes codebase and test cases. | The request initially said reports. | RESOLVED by explicit repos/ clarification. | Use the confirmed source location. |

### Intake readiness

Assessor: Codex.
Assessment time: `2026-10-19T15:26:23Z`.
Business owner: unknown.
Only READY permits the named downstream handoff.
READY_WITH_LIMITS permits intake evidence collection only.

| Named scope | Readiness | Supporting evidence and limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Update agent workflow guidance and workspace scaffolding. | READY | The exact request and repos/ clarification resolve material understanding gaps for this change. | Claims about runtime verification, production behavior, or knowledge approval. | Codex; completed the scoped workflow and retained validation evidence. |

The readiness gate applies through agent guidance. This task does not request a runtime state machine.
Implementation checks are recorded in [verification.md](verification.md). They do not establish business approval.
No new business browser or service execution occurred. Local Workbench tests and procedure trials supplied implementation evidence.
Existing portal evidence remains linked in place.
This task records requested intent, not business approval or knowledge publication.
