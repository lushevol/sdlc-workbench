---
artifact_kind: requirement
id: UI-COVERAGE-20261022
version: 1
status: draft
owner: unknown
source_refs: [UI-SRC-USER, UI-SRC-MFE, UI-SRC-BFF, UI-SRC-KNOWLEDGE]
related_ids: [TEST-UI-COVERAGE-20261022]
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

# Single UI user-view test coverage

> **Critical conclusions: Review required before business acceptance**
>
> **The catalog contains 521 designed cases. None ran in this task.**
> Action: Review expected behavior and bind execution fixtures. Consequence: The catalog cannot establish business verification or release approval.
> Owner: unknown. Evidence: [catalog](test-cases.md#coverage-navigation) and [inventory](evidence/case-inventory.json).
>
> **Draft knowledge contains conflicting portal-entry rules.**
> Action: Confirm the applicable entitlement rule. Consequence: Affected acceptance assertions remain blocked.
> Owner: unknown. Evidence: [knowledge decisions](evidence/knowledge-inspection.md#open-rule-decisions).

## Description

As a Single UI test designer, I need comprehensive UI cases for supported journeys and consequential edge conditions.
The user requested maximum practical coverage from `mfe-base`, `single-ui-bff`, and `knowledge`.
The [canonical catalog](test-cases.md) defines Gherkin setup, actions, observable UI assertions, fixtures, and cleanup.
The [inventory](evidence/case-inventory.json) records counts and unexecuted states.

## Rationale

The user requested UI test cases, including edge cases, in the chat dated 2026-10-22.
Source-backed partitions make the expected behavior reviewable.
Proposed assertions expose missing policy without presenting it as approved intent.
No finite case catalog guarantees every possible input or interaction combination.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Login, SSO, session activity, expiry, recovery, logout, and browser lifecycle. | Live identity-provider or production execution. | This request defines cases. |
| Workspaces, tile catalog, regional entries, module loading, profile, and preferences. | Internal behavior of uninspected tenant applications. | Controlled tenant fixtures expose shell contracts only. |
| Category, Import Map, Tile administration, fields, filters, grids, audits, and BFF rejection effects. | Application implementation changes. | No behavior change was requested. |
| Entitlements, intents, context, cache versions, accessibility, security, layout, and browser probes. | Approved performance budgets or universal compatibility claims. | Applicable current policies remain unavailable. |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Review the source-backed case catalog | READY | Source bindings, case definitions, and limits support review. Review will resolve proposed expectations. | Business acceptance and release approval remain unsupported. Execution needs fixture binding and separate authorization. | unknown; review expectations and assign case owners. |

- Assessor: Codex. Assessment date: 2026-10-22, Asia/Singapore.
- Expected behavior authority: implementation characterization, draft domain sources, and explicit proposals. None establishes business approval.
- Existing authorization: the user requested local analysis and case authoring.
- Evidence index: [retained evidence](evidence/index.md).
- Business review: pending. Readiness applies only to catalog review.
- Deferred policies do not block catalog review. They remain explicit review subjects and block affected business acceptance.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Test designer | UI-COVERAGE-RULE-001 | A source defines a UI behavior. | Link its case to the inspected revision and explicit UI assertion. | [Catalog sources](test-cases.md#sources). |
| Test designer | UI-COVERAGE-RULE-002 | An expectation lacks approved policy. | Label its basis and acceptance limit. | [Expectation basis](test-cases.md#objective-and-traceability). |
| Portal and administration users | Case-specific | Entitlements and fixture states vary by case. | Use the named actor and permission state in each case. | [Fixture definitions](test-cases.md#preconditions-and-fixtures). |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| mfe-base | Defines shell, UI state, administration, and HTTP consumers. | [UI inspection](evidence/ui-source-inspection.md#source-binding). | Current deployment parity is unknown. |
| single-ui-bff | Defines identity, session, and catalog service outcomes. | [Session inspection](evidence/session-source-inspection.md#scope-and-revisions) and [admin boundaries](evidence/admin-boundary-inspection.md#scope-and-revisions). | External identity and effective deployment settings are unknown. |
| Domain sources | Define draft business intent and integration proposals. | [Knowledge inspection](evidence/knowledge-inspection.md#authority-and-source-identity). | Applicability, ownership, and human approval remain open. |
| Controlled fixtures | Supply tenant markers and deterministic dependency failures. | [Shared setup](test-cases.md#preconditions-and-fixtures). | Fixtures must be implemented or bound before execution. |

## Acceptance criteria

These criteria assess this catalog. They do not define new product policies.

### UI-COVERAGE-AC-001

Every case must contain an explicit UI assertion.

### UI-COVERAGE-AC-002

Every case must link at least one behavior source or proposed-risk surface.

### UI-COVERAGE-AC-003

Every case ID must be unique.

```gherkin
@UI-COVERAGE-20261022
Feature: Reviewable UI case catalog
  @UI-COVERAGE-AC-001
  Scenario: Every case states an observable UI result
    Given the designer has completed a case definition
    When the catalog is checked
    Then the case contains at least 1 explicit UI assertion

  @UI-COVERAGE-AC-002
  Scenario: Every case identifies its evidence basis
    Given the designer has completed a case definition
    When the catalog is checked
    Then the case contains at least 1 linked behavior source or proposed-risk surface

  @UI-COVERAGE-AC-003
  Scenario: Every case has a unique identity
    Given the designer has completed the catalog
    When the case IDs are checked
    Then the duplicate case ID count equals 0
```

```yaml
acceptance_criteria:
  - id: UI-COVERAGE-AC-001
    given: Given the designer has completed a case definition
    when: When the catalog is checked
    then: Then the case contains at least 1 explicit UI assertion
    measure:
      metric: explicit UI assertion count per case
      operator: at_least
      value: 1
      unit: assertions per case
  - id: UI-COVERAGE-AC-002
    given: Given the designer has completed a case definition
    when: When the catalog is checked
    then: Then the case contains at least 1 linked behavior source or proposed-risk surface
    measure:
      metric: linked behavior source count per case
      operator: at_least
      value: 1
      unit: sources per case
  - id: UI-COVERAGE-AC-003
    given: Given the designer has completed the catalog
    when: When the case IDs are checked
    then: Then the duplicate case ID count equals 0
    measure:
      metric: duplicate case ID count
      operator: equals
      value: 0
      unit: IDs
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| [UI-COVERAGE-AC-001](#ui-coverage-ac-001) | Check Gherkin clauses and review observable results. | Local catalog; synthetic fixtures. | One catalog revision. | [Document checks](evidence/document-checks.json). |
| [UI-COVERAGE-AC-002](#ui-coverage-ac-002) | Resolve links, line locators, and source hashes. | Exact local revisions. | One source binding per file. | [Source manifest](evidence/source-manifest.json). |
| [UI-COVERAGE-AC-003](#ui-coverage-ac-003) | Compare case IDs and inventory entries. | Local catalog and inventory. | One catalog revision. | [Document checks](evidence/document-checks.json). |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| [UI-COVERAGE-AC-001](#ui-coverage-ac-001) | [Catalog](test-cases.md#procedure-and-assertions) | [Source manifest](evidence/source-manifest.json). | New executable mappings remain unavailable unless a case links an inspected assertion. | All new cases NOT_RUN. |
| [UI-COVERAGE-AC-002](#ui-coverage-ac-002) | [Catalog sources](test-cases.md#sources) | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; BFF `834b4155232222347220e47139a502ee43a9cbdf`. | [Inspected assertions](evidence/ui-source-inspection.md#inspected-assertions). | Prior executions retain separate bindings. |
| [UI-COVERAGE-AC-003](#ui-coverage-ac-003) | [Case inventory](evidence/case-inventory.json) | Workbench baseline `8dd076eac24c1b18b2f44245b3220ebcaf8537e3`. | Catalog-quality checks only. | [Document checks](evidence/document-checks.json). |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| UI-SRC-USER | User chat dated 2026-10-22. | 2026-10-22 | null | User; authorizes scope. | No execution or product policy approval. |
| UI-SRC-MFE | [UI inspection](evidence/ui-source-inspection.md). | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | [Per-file hashes](evidence/source-manifest.json). | unknown; implementation evidence. | Existing tsconfig.tsbuildinfo change remains untouched. |
| UI-SRC-BFF | [Session inspection](evidence/session-source-inspection.md). | `834b4155232222347220e47139a502ee43a9cbdf` | [Per-file hashes](evidence/source-manifest.json). | unknown; implementation evidence. | Mocked collaborators do not establish deployment behavior. |
| UI-SRC-KNOWLEDGE | [Knowledge inspection](evidence/knowledge-inspection.md). | `8dd076eac24c1b18b2f44245b3220ebcaf8537e3` | [Snapshot identities and hashes](evidence/source-manifest.json). | unknown; draft sources. | No recorded human approval. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | The catalog contains 521 designed cases. | [Inventory](evidence/case-inventory.json). | Source review can proceed. | unknown | Review case expectations. |
| Inference | Selected partitions expose consequential UI failure modes. | [Case groups](test-cases.md#coverage-navigation). | Runtime evidence is still required. | unknown | Prioritize approved assertions for execution. |
| Unknown | Supported browsers, accessibility criteria, and viewport policy are unavailable. | [Quality limits](evidence/crosscut-inspection.md#authority-and-execution-limits). | Proposed quality assertions cannot establish acceptance. | unknown | Confirm applicable targets. |
| Unknown | Current identity, deployment, and tenant contracts are unbound. | [Source limits](test-cases.md#facts-inferences-and-unresolved-questions). | Environment-specific verification remains blocked. | unknown | Record environment and contract identities before execution. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Candidate indexes, domain records, and cited source snapshots. | [Manifest](evidence/source-manifest.json). | Entitlements, intents, context, cache, and session rules. | Draft; no approved authority inferred. | Entry policy, integration schema, and deployment applicability. |
| MFE components, consumers, and actual test assertions. | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. | [UI cases](test-cases.md#group-workspaces). | Source characterization; some tests assert presence only. | New UI outcomes remain unexecuted. |
| BFF authentication and session sources and assertions. | BFF `834b4155232222347220e47139a502ee43a9cbdf`. | [Authentication cases](test-cases.md#group-login). | Mocked service tests remain distinct from UI behavior. | Effective deployed settings remain unavailable. |
| Existing session reports and retained runs. | [Prior-run limits](evidence/knowledge-inspection.md#retained-execution-limits). | Existing session coverage informs new cases. | Historical fixtures and revisions apply only to their own cases. | No new case inherits a prior passing status. |

This request makes no implementation change and attributes no introduced regression.
Old/new comparison is therefore not applicable to this case-design stage.
Source-risk observations remain test proposals rather than confirmed defects.

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1; UI-Q-001 | Which inputs define scope? | mfe-base, single-ui-bff, and knowledge. | User chat dated 2026-10-22. | answered | User | Completed local review. |
| 1; UI-Q-002 | Which entity rule governs portal entry? | Draft sources conflict. | [Knowledge decisions](evidence/knowledge-inspection.md#open-rule-decisions). | unresolved | unknown | Acceptance remains blocked; select the applicable policy. |
| 1; UI-Q-003 | Which quality targets govern acceptance? | Current approved browser and accessibility policies are unavailable. | [Crosscut limits](evidence/crosscut-inspection.md#authority-and-execution-limits). | unresolved | unknown | Review proposed targets before acceptance. |

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| UI-Q-001 | not applicable | Scope answer changes no domain rule. | not applicable | not applicable | No publication change. |
| UI-Q-002 | Candidate entitlement sources. | No selected policy or material clarification was supplied. | pending | [Open decisions](evidence/knowledge-inspection.md#open-rule-decisions). | Draft; unknown; resolve policy before publication. |
| UI-Q-003 | No approved quality policy found within the bounded source review. | No target was invented. | pending | [Crosscut proposals](evidence/crosscut-inspection.md#next-actions). | Unresolved; unknown; obtain applicable targets. |

### Intake investigation plan

- Current state: source-backed design is complete. All new business executions remain NOT_RUN.
- Evidence collected: exact source revisions, hashes, existing assertions, retained-run limits, and canonical UI cases.
- Method and controls: local static inspection. No live browser or external connector call was required.
- Retention: [evidence index](evidence/index.md). Existing source snapshots and audit history remain unchanged.
- Next decision: review expected behavior and execution feasibility. No application change or release decision is authorized by this catalog.
