---
artifact_kind: requirement
id: REVIEW-CES-TILES-20261109
version: 1
status: draft
owner: unknown
source_refs: [user-input-20261109]
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

# Review service migration and independent tile rollout

**No critical conclusions require user attention or action.**

## Description

The [user request](evidence/user-input.md#exact-user-input) authorizes code review of two services and independent BFF tile rollout analysis.
The registered `ratan-auth-server` checkout contains the requested RatanOne authentication service.
No application fixes, remote writes, or deployment are authorized.

## Scope

Entry route: bounded exploration of existing implementation.
Compare each current migration branch with its local `main` merge base.
Both selected service worktrees are clean at registration.
BFF candidate: `95480c0e2563bc2a5a639bca1f22ecedb61936c2`; baseline: `834b4155232222347220e47139a502ee43a9cbdf`.
Authentication candidate: `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5`; baseline: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Record full revisions and fingerprints in retained review context.
Implementation dates precede this intake. Earlier business acceptance and deployment remain unknown.
Affected paths include login, refresh, token grants, authorization routing, tile configuration, and data entitlements.
Risk is high for authorization isolation and session availability.

## Rationale

The user needs review findings and the conditions for partial migration.
Shared authentication and authorization can affect multiple tile journeys.

## Actors and business rules

| Actor | Rule | Source and limit |
| --- | --- | --- |
| Reviewer | Inspect both requested service comparisons. | [User request](evidence/user-input.md#exact-user-input). |
| Reviewer | Assess independent BFF tile rollout. | [User request](evidence/user-input.md#exact-user-input). |
| Application owner | Decide corrections and business acceptance. | Owner and acceptance remain unknown. Review does not grant deployment authority. |

## Dependencies

| Dependency | Evidence required | Limit |
| --- | --- | --- |
| Service source and tests | Exact revisions and retained assertions. | Local copies do not establish deployed versions. |
| CES, EMS2, Redis, FMAA, database | Source contracts and controlled test doubles. | No live execution is planned. |
| Corporate Maven artifacts | Existing cache and local build tools. | Missing private dependencies can block full suites. |

## Acceptance criteria

These are review outcomes. They are not new business behavior requirements.

```gherkin
Feature: Service migration review
  @REVIEW-AC-001
  Scenario: REVIEW-AC-001 Inspect both migration comparisons
    Given the exact baseline and candidate revisions for each selected service
    When the reviewer traces changed behavior through callers and tests
    Then the report contains 2 repository comparisons with findings, triggers, and consequences
    And the report states unavailable checks and evidence limits

  @REVIEW-AC-002
  Scenario: REVIEW-AC-002 Assess independent tile rollout
    Given BFF tile configuration and both entitlement providers
    When one tile selects CES and another selects EMS2
    Then the report contains 1 tile rollout assessment with effective routing and grant isolation
    And the report states configuration and operational constraints
```

```yaml
acceptance_criteria:
  - id: REVIEW-AC-001
    given: Given the exact baseline and candidate revisions for each selected service
    when: When the reviewer traces changed behavior through callers and tests
    then: Then the report contains 2 repository comparisons with findings, triggers, and consequences
    measure:
      metric: repository_comparisons
      operator: equals
      value: 2
      unit: comparisons
  - id: REVIEW-AC-002
    given: Given BFF tile configuration and both entitlement providers
    when: When one tile selects CES and another selects EMS2
    then: Then the report contains 1 tile rollout assessment with effective routing and grant isolation
    measure:
      metric: tile_rollout_assessments
      operator: equals
      value: 1
      unit: assessments
```

## Measurement conditions

| Criterion | Method | Conditions | Evidence |
| --- | --- | --- | --- |
| [REVIEW-AC-001](#acceptance-criteria) | Inspect both migration comparisons. | Local source and available cached libraries; one bounded review. | [Evidence index](evidence/index.md). |
| [REVIEW-AC-002](#acceptance-criteria) | Inspect routing and the retained tile inventory. | Synthetic provider responses; no current database claim. | [Evidence index](evidence/index.md). |

## Traceability

| Criterion | Review output | Implementation identity | Execution |
| --- | --- | --- | --- |
| [REVIEW-AC-001](#acceptance-criteria) | [Code review](10-change-review.md). | Both exact comparisons above. | Controlled probes are recorded separately. |
| [REVIEW-AC-002](#acceptance-criteria) | [Tile assessment](09-tile-rollout.md). | BFF exact candidate above. | Controlled probes are recorded separately. |

## Sources

| Source | Locator | Revision and authority | Limit |
| --- | --- | --- | --- |
| User request | [Exact input](evidence/user-input.md#exact-user-input). | User message, 2026-11-09. | Review authorization only. |
| Service implementations | [BFF context](evidence/single-ui-bff-context.json), [auth context](evidence/ratan-auth-server-context.json). | Exact comparisons above and file hashes. | Deployment identity is unknown. |
| Supplied tile export | [Canonical CSV](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv). | SHA-256 `23b23415ebe9def55b854f36e85465b54add2356d5b9fc165cb8c54a15647486`. | Environment and extraction time are unknown. |

## Evidence and open questions

No missing policy blocks the bounded review. Business conformance remains outside the review-output criteria.
Current source and controlled results will support findings. They cannot supply human acceptance.
The [evidence index](evidence/index.md) identifies completed cases and unavailable checks.

### Existing knowledge and evidence review

The prior [BFF field review](../ces-entitlement-migration-20261102/10-change-review-bff-entity-fields.md) supplies migration context.
Current service source must support each retained behavior claim.
The supplied tile export can support a historical configuration inventory only.

### Answer and question log

Repository discovery resolves `ratanone-auth-server` to the registered `ratan-auth-server` checkout and its Maven artifact.
No clarification request is needed for read-only review boundaries.

### Investigation and evidence plan

Inspect the complete diffs, affected unchanged callers, existing test assertions, and relevant source contracts.
Use existing local verification tools and focused controlled probes when useful.
Store compact claim-bearing results once. Keep routine build logs in ignored or temporary storage.
Bind retained results to exact source, assertions, fixture identity, and stated environment limits.
Do not access live services or expose credential values.
Stop when both comparisons and rollout boundaries have evidence-backed dispositions.
Retain findings and useful probes. Do not alter reviewed production source.

## Knowledge-update log

No user clarification changes business intent. No knowledge publication is requested.
Existing candidate knowledge and prior reports can guide inspection. Exact source owns behavior claims.

## Readiness decision

- Named phase: bounded local code review and tile rollout investigation.
- Status: `READY`.
- Assessor: Codex, 2026-11-09, Asia/Singapore.
- Authorization: [exact user request](evidence/user-input.md#exact-user-input).
- Rationale: repository identities, comparison endpoints, permitted actions, and measurable outputs are available.
- Product policy uncertainty cannot change these read-only review boundaries.
- Blocked actions: application changes, deployment, and business acceptance remain outside scope.
- Accountable business owner: unknown. Review execution owner: Codex.
