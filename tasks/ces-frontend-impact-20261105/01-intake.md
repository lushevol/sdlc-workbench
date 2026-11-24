---
artifact_kind: requirement
id: CES-FRONTEND-IMPACT-20261105
version: 1
status: draft
owner: unknown
source_refs: [USER-001, BFF-001, BASE-001, CONTAINER-001, INTENT-001]
related_ids: [CES-MIGRATION]
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

# CES frontend migration impact intake

> **Critical conclusions: Frontend grant selection and tile validation require adaptation before CES adoption.**
> Action: review the [required changes](05-impact-analysis.md#proposed-change).
> Consequence: mapped grants can fail frontend checks despite an authorized BFF drawer.
> Owner: unknown. Evidence: [controlled observations](evidence/contract-probe-summary.json).

## Description

The user requests required changes for `mfe-base` and `mfe-ratan-container` from the BFF CES migration.
Compare the current BFF branch with local `main`.
Deliver source-linked changes, compatibility boundaries, validation needs, and material unknowns.

## Rationale

The [exact request](evidence/user-input.md#exact-user-input) is the first-priority source for this analysis scope.
Existing migration intent requires permission preservation after explicit concept mapping.
Read the [preserved clarification](../../knowledge/evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
That source does not establish current deployment or complete permission equality.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| BFF main-to-candidate contracts and frontend consumers | Application fixes | The user requests identification. |
| Entry, workspace restoration, deep links, action checks, role-dependent consumers, and tile configuration | Release authorization | No release decision was requested. |
| Existing assertions and controlled helper observations | Live CES or production execution | Static impact analysis can proceed without external mutation or credentials. |

### Entry route and evidence state

Entry procedure: [existing implementation](../README.md#enter-with-existing-implementation).

- Entry route: existing implementation supplied by repository name and comparison target.
- Registration date: 5 November 2026, Asia/Singapore.
- BFF baseline: `834b4155232222347220e47139a502ee43a9cbdf`, local `main`.
- BFF candidate: `267081800cc28b6af0f8e080fa67c2d5f14d3a26`, branch `codex/apply-service-diffs-20261027`.
- Candidate commit date: 4 November 2026, 21:30:24 +08:00.
- Base baseline: `f025513f696476a9cc8162681410cbd21e029bcb`, local `main`.
- Base inspected HEAD: `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
- Base local edits and container filesystem identities: [source manifest](evidence/source-manifest.json).
- Earlier implementation approval and deployment: unknown.

| Dimension | Current state and evidence |
| --- | --- |
| Implementation | BFF migration exists. Frontend changes remain recommendations. |
| Intent review | User authorizes analysis. Detailed CES role and application mappings remain partly unresolved. |
| Execution outcome | Four controlled helper observations retained; no application suite or browser execution. |
| Business acceptance | Pending; no decision recorded. |

Bounded exploration coding is not applicable.
The probes execute existing function bodies without changing application behavior.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Source-based frontend impact analysis | READY | Exact local revisions and relevant consumers support this decision. Live deployment cannot change these source differences. | Application implementation and release are outside this decision. | unknown; review the analysis. |

- Assessor: agent:codex, 5 November 2026, Asia/Singapore.
- Expected behavior authority: current user request for analysis; existing intent remains subject to its recorded review limits.
- Existing authorization: inspect source and identify changes; preserve unrelated edits.
- Evidence index: [task evidence](evidence/index.md).
- Business review: pending. Readiness does not grant approval.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Frontend maintainer | ANALYSIS-01 | BFF migration changes consumed entitlement contracts. | Identify source-backed frontend work and its limits. | [User request](evidence/user-input.md#exact-user-input) |
| Portal user | Existing migration intent | EMS2 permissions map to CES application, entitlement, feature, and action. | Preserve permission meaning within the mapped scope. | [Prior clarification](../../knowledge/evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) |

This intake does not create new role, multi-application, or data-authorization policy.

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| CES-MIGRATION | Existing migration investigation | [Prior intake](../ces-entitlement-migration-20261102/01-intake.md) | Live mapping and deployment remain unavailable. |
| BFF-001 | Supplies normalized frontend grants and drawers | [BFF comparison](evidence/bff-contract-analysis.md) | App-ID and role identity need explicit treatment. |
| BASE-001 | Supplies shared hooks, tile context, and interfaces | [Base analysis](evidence/mfe-base-analysis.md) | Effective provider is not a distinct response field. |
| CONTAINER-001 | Supplies shared application permission helpers | [Container analysis](evidence/mfe-ratan-container-analysis.md) | No independent Git or deployed artifact identity. |

## Acceptance criteria

These criteria concern the requested analysis deliverable.
They do not approve product permission rules.

```gherkin
@CES-FRONTEND-IMPACT-20261105
Feature: Identify frontend changes from the BFF entitlement migration
  @ANALYSIS-AC-01
  Scenario: Bind all selected repositories to available source identity
    Given the selected BFF comparison and two frontend sources
    When the impact analysis completes
    Then the evidence manifest identifies all 3 selected repositories
    And missing independent Git history is explicit

  @ANALYSIS-AC-02
  Scenario: Retain evidence for each recommended change
    Given the recommended frontend change inventory
    When the impact analysis completes
    Then zero recommendations lack a source link and consequence
    And each recommendation identifies an owner or states unknown
```

```yaml
acceptance_criteria:
  - id: ANALYSIS-AC-01
    given: Given the selected BFF comparison and two frontend sources
    when: When the impact analysis completes
    then: Then the evidence manifest identifies all 3 selected repositories
    measure:
      metric: selected repositories with recorded source identity
      operator: equals
      value: 3
      unit: repositories
  - id: ANALYSIS-AC-02
    given: Given the recommended frontend change inventory
    when: When the impact analysis completes
    then: Then zero recommendations lack a source link and consequence
    measure:
      metric: recommendations without source and consequence
      operator: equals
      value: 0
      unit: recommendations
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| [ANALYSIS-AC-01](#acceptance-criteria) | Inspect repository identities and filesystem hashes. | Local source checkout. | One retained source snapshot. | [Manifest](evidence/source-manifest.json) |
| [ANALYSIS-AC-02](#acceptance-criteria) | Review each change row and its linked evidence. | Authored impact report. | One completed report. | [Required changes](05-impact-analysis.md#proposed-change) |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| [ANALYSIS-AC-01](#acceptance-criteria) | Not applicable; analysis output. | [Source manifest](evidence/source-manifest.json) | Identity and hash checks in [validation](evidence/validation.json). | [Validation](evidence/validation.json) |
| [ANALYSIS-AC-02](#acceptance-criteria) | Not applicable; analysis output. | [Required changes](05-impact-analysis.md#proposed-change) | Manual evidence review; automated link checks. | [Validation](evidence/validation.json) |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| USER-001 | [User input](evidence/user-input.md) | 2026-11-05 | [Manifest](evidence/source-manifest.json) | User; current analysis scope. | No deployment authorization. |
| BFF-001 | [BFF analysis](evidence/bff-contract-analysis.md) | Baseline and candidate above | [Manifest](evidence/source-manifest.json) | Owner unknown; implementation evidence. | Local refs; no remote refresh. |
| BASE-001 | [Base analysis](evidence/mfe-base-analysis.md) | HEAD and baseline above | [Hashes](evidence/mfe-base-source-hashes.json) | Owner unknown; implementation evidence. | Local edits preserved. |
| CONTAINER-001 | [Container analysis](evidence/mfe-ratan-container-analysis.md) | Filesystem copy | [Hashes](evidence/container-source-hashes.json) | Owner unknown; implementation evidence. | No independent Git history. |
| INTENT-001 | [Migration clarification](../../knowledge/evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md) | user-clarification-20261103-1 | [Knowledge manifest](../../knowledge/evidence/manifest.yaml) | Explicit user scope and mapping intent. | No deployed parity proof. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | Existing frontend helpers reject controlled migrated payloads. | [Probe summary](evidence/contract-probe-summary.json) | Required compatibility changes are identified. | unknown | Implement after scope and contract review. |
| Unknown | CES role/profile mapping for sharing and read-only restrictions. | [Container role consumers](evidence/mfe-ratan-container-analysis.md#rc-03-resolve-role-dependent-filters-views-and-exception-gates) | Role-dependent implementation needs a decision. | unknown | Define the authoritative profile contract. |
| Unknown | Whether app names are unique across selected app IDs. | [BFF identity limit](evidence/bff-contract-analysis.md#conditional-application-identity-limitation) | Name-only action resolution may be insufficient. | unknown | Confirm uniqueness or expose app IDs. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Knowledge index and [SDK topic](../../knowledge/records/candidates/security/KT-sdk-and-entitlements.md) | Version 8; candidate | Permission preservation and renamed application. | Candidate intent; cited clarification inspected. | Role equivalence remains unknown. |
| [CES parity topic](../../knowledge/records/candidates/security/KT-ces-migration-parity.md) | Version 1; candidate | Explicit concept mapping. | Original user clarification inspected. | Live data restriction equivalence unavailable. |
| [Prior frontend investigation](../ces-entitlement-migration-20261102/evidence/frontend-analysis-20261030.md) | 30 October 2026 | Consumer discovery. | Secondary evidence; current BFF is newer. | Current source supersedes old field names. |
| Graph coverage operation | [Retained coverage](evidence/graph-coverage.json) | Relationship discovery only. | STALE for current BFF and SDK. | Direct current source used; graph not rebuilt. |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1; SCOPE-01 | Compare which BFF source? | Current branch against local main. | [Current request](evidence/user-input.md#exact-user-input) and [manifest](evidence/source-manifest.json) | Answered for local analysis. | agent:codex | Exact deployed revisions remain outside scope. |
| 1; ROLE-01 | Which CES profile replaces legacy role behavior? | Unknown. | [Inspected consumers](evidence/mfe-ratan-container-analysis.md#rc-03-resolve-role-dependent-filters-views-and-exception-gates) | Pending for implementation. | unknown | Obtain a profile or capability contract. |
| 1; APP-01 | Are returned application names globally unique? | Unknown. | [BFF identity limit](evidence/bff-contract-analysis.md#conditional-application-identity-limitation) | Pending for implementation. | unknown | Confirm uniqueness or extend provider identity. |

These questions do not block the requested impact identification.
No clarification question was sent because available evidence supports that analysis.

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| This analysis | None | No new domain intent was supplied or resolved. | Not applicable; implementation gaps remain task evidence. | Not applicable | Existing candidate publication state preserved. |

### Intake investigation plan

- Current state: inspected BFF contracts and frontend source consumers.
- Evidence needed: exact source comparison, affected helpers, assertions, and compatibility limits.
- Method: read-only source tracing and four controlled helper probes.
- Retention: [evidence index](evidence/index.md), source hashes, non-Git snapshots, and per-case results.
- Next decision: review [required changes](05-impact-analysis.md#proposed-change); resolve role and application identity before dependent implementation.
