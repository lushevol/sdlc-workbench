---
artifact_kind: requirement
id: SDK-OPT-20261107
version: 1
status: draft
owner: unknown
source_refs: [SDK-OPT-INPUT]
related_ids: []
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

# Simplify the latest Single UI SDK change

> **No critical conclusions require user attention or action.**

## Description

Simplify the latest SDK migration using Ponytail full mode.
Preserve observable behavior, public interfaces, validation, and error handling.
The [user request](evidence/user-input.md#exact-user-input) authorizes optimization and local verification.

## Rationale

Remove unnecessary work and duplication within the latest change.
Do not invent a new entitlement policy.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Latest migration, affected callers, tests, and required documentation. | New product behavior, deployment, or publishing. | The user requested optimization. |

### Entry route and evidence state

- Entry route: [existing implementation](../README.md#enter-with-existing-implementation).
- Repository: `repos/libraries/single-ui-sdk-starter/`.
- Original migration: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` to `fd9a157e260850b6d9efa10da3223950ea61133a`.
- Implementation date: 1 November 2026. Task registration: 7 November 2026.
- Local state: untracked `diff` exists. Preserve it.

| Dimension | Current state and evidence |
| --- | --- |
| Implementation | Migration exists at `fd9a157e260850b6d9efa10da3223950ea61133a`. |
| Intent review | The user requests behavior-preserving optimization. Prior product acceptance remains unknown. |
| Execution outcome | [Baseline](evidence/baseline-result.json): 44 tests pass; zero failures, errors, or skips. |
| Business acceptance | Pending. Local refactoring does not establish product acceptance. |

Bounded exploration is not applicable. This request supplies an existing implementation and permits its optimization.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Apply and verify the mapper simplification | READY | Source, callers, assertions, and the passing baseline support this bounded refactor. | No local optimization blocker. Deployment remains outside scope. | Codex; simplify the private mapper. |

Assessed by Codex on 7 November 2026, Asia/Singapore.
Live CES access cannot change the equivalence of these local transformations.
Live service acceptance remains separate.

### Selected affected scope and risk

Change only private `AuthorizationImpl.mapRoles` logic.
Resolve configured role aliases once and type the internal subject map as `Map<String, List<String>>`.
Preserve validation order, mutable outputs, action order, duplicates, filters, collisions, and failure classification.
No public signature, configuration, DTO, fixture, dependency, or export change is required.

The bean factory and direct tests construct `AuthorizationImpl`.
No registered external service imports this SDK authorization interface in the inspected Java sources.
Unknown external consumers remain possible.
The BFF uses its own authorization interface.
Implementation risk is low because both changes are local transformations.
Incorrect permission mapping has consequential security effects, so all authorization tests remain enabled.

- Expected behavior authority: [user input](evidence/user-input.md#exact-user-input), limited to optimization.
- Existing authorization: local source edits, checks, and stage commits under project instructions.
- Evidence index: [task evidence](evidence/index.md).
- Business review: pending. Readiness does not grant approval.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| SDK consumer | OPT-RULE-1 | Optimization changes implementation. | Preserve public results, failure semantics, and security boundaries. | [User input](evidence/user-input.md#exact-user-input) and Ponytail. |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| SDK migration | Defines the candidate behavior baseline. | Git revision `fd9a157e260850b6d9efa10da3223950ea61133a`. | Inspect affected interfaces before editing. |

## Acceptance criteria

```gherkin
@SDK-OPT-20261107 @OPT-AC-1
Feature: Preserve SDK behavior during optimization

  Scenario: Run affected SDK tests after simplification
    Given the latest SDK migration and its affected tests
    When the authorized simplification is applied and those tests execute
    Then all applicable assertions pass with zero failures
    And public interfaces and validation remain compatible
```

```yaml
acceptance_criteria:
  - id: OPT-AC-1
    given: Given the latest SDK migration and its affected tests
    when: When the authorized simplification is applied and those tests execute
    then: Then all applicable assertions pass with zero failures and compatible public interfaces and validation
    measure:
      metric: affected test failures
      operator: equals
      value: 0
      unit: failures
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| OPT-AC-1 | Inspect the diff and execute applicable assertions. | Local SDK tooling and existing synthetic fixtures. | One complete declared suite for each source state. | Exact revisions, commands, assertion counts, and outcomes. |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| [OPT-AC-1](#acceptance-criteria) | Existing SDK structure | SDK at `fd9a157e260850b6d9efa10da3223950ea61133a` | [Map assertions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java) | [Baseline](evidence/baseline-result.json) |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SDK-OPT-INPUT | [Exact request](evidence/user-input.md#exact-user-input) | Chat, 7 November 2026 | See evidence index. | Human user; optimization authority. | No new business policy or release approval. |
| SDK-BASELINE | SDK Git history | `fd9a157e260850b6d9efa10da3223950ea61133a` | Git object | Repository author; implementation evidence. | Not independent intent or live behavior evidence. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact; high confidence | Typed subject values remove an unchecked cast. | [Mapper source](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java). | Preserve the public map shape. | Codex | Apply the local refactor. |
| Fact; high confidence | Alias validation forbids null values. One lookup can identify excluded roles. | Same mapper source and [assertions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java). | Preserve allowlist behavior. | Codex | Verify null, empty, selected, and excluded aliases. |
| Limit | Full packaging previously required unavailable formatter dependencies. | [Prior SDK review](../ces-entitlement-migration-20261102/10-change-review-sdk-function-coverage.md). | Packaging evidence needs a fresh attempt. | Codex | Run complete local tests and attempt packaging. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| SDK source, configuration, DTOs, tests, and registered Java callers | `fd9a157e260850b6d9efa10da3223950ea61133a`; [baseline hashes](evidence/baseline-result.json) | [OPT-AC-1](#acceptance-criteria) | Exact implementation and assertion evidence. | No local refactor blocker. |
| [Existing migration design](../single-ui-sdk-ces-migration-20261101/10-change-review.md#selected-compatibility-design) | Workbench `29427f84d` | Order, duplicates, role isolation, and failure behavior. | Prior task evidence supports preserved constraints. | Live parity remains outside this optimization. |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1; OPT-Q-1 | Which change should be optimized? | Latest SDK migration. | [User input](evidence/user-input.md#exact-user-input) and Git log. | answered | Codex | Inspect this commit and preserve untracked material. |

### Knowledge-update log

No domain knowledge change is proposed. This task preserves existing behavior.

### Intake investigation plan

- Source, callers, assertions, and prior evidence were inspected before editing.
- The complete baseline suite passes with the prepared offline Maven cache.
- Reuse existing [canonical cases](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#procedure-and-assertions).
- Retain compact results and exact identities under this task.
- Freeze this intake after lint. Record implementation and verification in the stage review.
