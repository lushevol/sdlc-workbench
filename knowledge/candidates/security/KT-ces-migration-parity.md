---
type: KnowledgeTopic
id: KT-ces-migration-parity
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: conversation:ces-entitlement-migration-20261102:coverage-automation-20261103
  revision: user-clarification-20261103-1
  sha256: 10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57
generated:
  by: agent:codex
  at: '2026-11-03T07:30:09Z'
verified: []
classification: security
scope: Intended permission preservation and comparison scope for the EMS2 production to CES UAT migration.
summary: Compare mapped entitlement definitions and every scoped account's permission content. Keep FMO Portal Admin outside the production comparison.
related:
- KT-sdk-and-entitlements
- CES-MIGRATION
open_questions:
- Which authoritative source defines the complete legacy data field and value restrictions for each profile?
- Which reviewed scope identifies CES-only management permissions outside the migrated business permissions?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# CES migration permission preservation

## Scope

This topic defines intended permission preservation from EMS2 production to CES UAT.
It covers mapped entitlement definitions and permission content for all scoped accounts.
The [user clarification](../../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) controls this scope from 3 November 2026.
The owning [migration task](../../../tasks/ces-entitlement-migration-20261102/01-intake.md#current-task-state) retains source observations, implementation, and execution evidence separately.

## Summary

The migration must preserve permission meaning after the EMS2 and CES concepts are mapped.
Assess entitlement completeness separately from account permission completeness.
Two supplied account examples do not limit the required account population.
FMO Portal Admin has a separate, lower-priority non-production comparison under the user's clarification.

## Documented knowledge

### Mapping between authorization concepts

| EMS2 concept | CES concept | Required comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition and its assigned accounts. |
| Entity | Application | Preserve application scope when comparing permission names. |
| Subject | Feature | Compare each subject through its explicit feature mapping. |
| Action | Action | Compare the permitted operation within the mapped feature. |

Source: [exact mapping clarification](../../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
Names shared by different applications do not establish equivalent permissions.
Numeric source identifiers can differ without changing mapped permission meaning.
The existing [entity-name intent](KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration) retains its separate source and scope.

### Entitlement preservation

The intended migration has no missing mapped entitlements or permission gaps.
Compare entitlement definitions before treating catalog totals as evidence of completeness.
Compare each mapped application, entitlement, feature, and action relationship.
Different entitlements can produce the same combined effective permissions.
That combined result does not establish equal entitlement definitions or assignments.

### Account permission preservation

The comparison must include all accounts discovered within the selected entity scope.
Expand cells or response collections that contain several account IDs.
Count each distinct account once in the overall account denominator.
Retain application and entitlement scope when comparing assignments and effective permissions.
Compare applicable data restrictions through authoritative definitions and resolved values.
A matching data profile name alone does not establish equivalent data access.

### Coverage and active differences

Record fully matched migrated content in the coverage totals.
Remove that content from the active difference list.
Keep missing content, additional content, unresolved mappings, and unavailable comparisons visible.
An unavailable account comparison does not establish equal permissions or missing permissions.
Keep the expected population visible when an account comparison is unavailable.

### FMO scope exception

The user's clarification places FMO Portal Admin outside the production migration comparison.
Keep its non-production comparison separate and lower in priority.
Do not add FMO's non-production content to production coverage denominators.
Retain the [dated clarification](../../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) when applying this exception.
Future production scope requires a sourced update.

## Connections

- [SDK and entitlements](KT-sdk-and-entitlements.md) defines the existing entity-name migration and SDK compatibility intent.
- [Migration intake](../../../tasks/ces-entitlement-migration-20261102/01-intake.md) records the current requirement and unresolved evidence.
- [Canonical coverage cases](../../../tasks/ces-entitlement-migration-20261102/06-test-cases.md) define observable comparisons separately from execution results.

## Evidence limits

The source establishes user-stated intent and comparison scope.
The user's statement about no entitlement gaps is an expectation, not retained execution proof.
This candidate does not establish completed migration, current account assignments, or deployed permission equality.
The FMO exception does not verify its current launch or provisioning state.
No human review, knowledge publication, migration acceptance, or deployment approval is recorded.

## Open questions

| Question | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Which source defines legacy data field and value restrictions? | Complete data-scope equality remains unassessed without that source. | unknown | Bind each legacy profile to authoritative restriction definitions. |
| Which CES-only management grants fall outside migration scope? | Additional grants need an explicit classification before equal-content acceptance. | unknown | Record the reviewed business scope and its source. |
