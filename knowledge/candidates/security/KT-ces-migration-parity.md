---
type: KnowledgeTopic
id: KT-ces-migration-parity
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: conversation:ces-entitlement-migration-20261102:coverage-automation-20261103
  revision: user-clarification-20261103-1
  sha256: 10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57
- resource: conversation:ces-entitlement-migration-20261102:frontend-compatibility-20261106
  revision: user-clarification-20261106-1
  sha256: 02c662aa4bec9100be1778de01ae67771f30550da86061619bf490f670c99ba2
previous_version: 1
previous_content_sha256: f4dbb8c6c0a6292417067be7b54c440c3bd48b122a8a5d648aadb49e1fd76419
previous_revision: 31e508f75443916633cb196d013129ad82a65974
generated:
  by: agent:codex
  at: '2026-11-05T16:43:03.427770+00:00'
verified: []
classification: security
scope: Intended permission preservation, frontend compatibility, independent tile migration, and comparison scope for EMS2 to CES.
summary: Preserve mapped permissions and upper-application APIs where possible. Select the provider per tile. Keep role multiplicity explicit.
related:
- KT-sdk-and-entitlements
- CES-MIGRATION
open_questions:
- Which authoritative source defines the complete legacy data field and value restrictions for each profile?
- Which reviewed scope identifies CES-only management permissions outside the migrated business permissions?
- How must multiple CES roles map to existing upper-application role contracts and role-dependent business rules?
- Which approved mappings define compatibility for each upper-application API and its CES permission inputs?
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
The [frontend clarification](../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input) adds frontend compatibility and independent tile routing intent.
It applies from 6 November 2026 to `mfe-base`, the shared Ratan container, and their upper applications.
The owning [migration task](../../../tasks/ces-entitlement-migration-20261102/01-intake.md#current-task-state) retains source observations, implementation, and execution evidence separately.

## Summary

The migration must preserve permission meaning after the EMS2 and CES concepts are mapped.
Assess entitlement completeness separately from account permission completeness.
Two supplied account examples do not limit the required account population.
FMO Portal Admin has a separate, lower-priority non-production comparison under the user's clarification.
Preserve upper-application APIs where possible while changing authorization internals for the selected tile.
Do not require one batch migration of every tile.
Treat role multiplicity as an explicit compatibility concern, separate from mapped feature/action permission meaning.

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

### Frontend compatibility and per-tile migration

The [frontend decision](../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input) prioritizes compatibility with existing upper-application APIs.
Apply this objective to `mfe-base` and shared container APIs.
Preserve established caller contracts where possible. Adapt provider-specific identities and permission data internally.
The user identifies non-unique roles as the known compatibility gap.
This statement does not establish that every other API is compatible.
Keep each unresolved mapping visible before claiming complete compatibility.

Do not treat a combined effective permission set as one assigned role.
Preserve the distinction between assigned roles and effective feature/action permissions.
The contract for callers that expect one role requires a sourced business mapping.
Do not select an arbitrary role or infer a named role from effective action membership.

### Independent tile provider selection

Each tile must select its entitlement provider independently.
An EMS2 tile must retain its existing authorization logic.
A CES tile must use the new authorization logic, configured application identity, and CES permission structure.
Treat the CES application as the new entity identity within that selected scope.
Do not force unrelated tiles to change provider when one tile moves to CES.
Preserve application scope within both provider paths.

The [source interpretation](../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#interpretation-for-this-stage) distinguishes plain `EMS2` from the final `EMS2 (CES)` phrase.
The latter denotes the CES path. The migration contract uses `EMS3` as its CES wire value.
The exact user quotation remains unchanged in the source.
This interpretation does not merge legacy EMS2 and CES provider choices.

### Intended frontend acceptance criteria

These criteria make the user objective measurable within reviewed mappings.
They define target behavior. They do not establish complete API compatibility or passing execution.
Role-dependent business mappings remain unresolved below.

#### FE-COMPAT-AC-001

Preserve existing upper-application permission API behavior for mapped feature/action decisions.

```gherkin
Feature: Preserve upper-application permission contracts
  Scenario: Preserve a mapped decision through the existing caller API
    Given an upper application uses an existing base or shared container permission API
    And a reviewed application, feature, and action mapping defines an allowed or denied decision
    And the tile selects EMS2 or CES
    When the upper application requests that mapped permission through its existing API
    Then the API returns the mapped allowed or denied decision
    And the caller can use its existing call contract within that reviewed mapping
    And the number of contradictory decisions equals 0
```

Measure: zero contradictory decisions across the declared mapped permission cases.
Record compatibility exceptions before accepting affected caller behavior.
An unknown role mapping cannot satisfy this criterion through a fabricated scalar role.

#### FE-COMPAT-AC-002

Route each tile through its selected provider and application scope.

```gherkin
Feature: Select the entitlement provider per tile
  Scenario: Preserve independent legacy and CES authorization paths
    Given one tile selects EMS2 and another tile selects CES
    And each tile has its reviewed application and permission configuration
    When the system evaluates access for both tiles
    Then the EMS2 tile uses its existing EMS2 authorization rules
    And the CES tile uses its configured CES application and new permission structure
    And the number of grants transferred from an unrelated application equals 0
```

Measure: two selected provider paths follow their defined rules, with zero cross-application grants.
The value two defines this comparison case. It does not limit the supported tile population.

#### FE-COMPAT-AC-003

Change one tile independently while keeping role multiplicity separate from permission equivalence.

```gherkin
Feature: Migrate tiles independently
  Scenario: Change one tile without forcing the remaining tiles to migrate
    Given a declared set of tiles uses its reviewed provider selections
    And one selected tile changes from EMS2 to CES
    And CES assignments can contain multiple roles
    When the system applies that selected tile's provider change
    Then the number of provider selections changed on other tiles equals 0
    And the number of authorization decisions changed on other tiles solely by that switch equals 0
    And multiple role assignments are not represented as one proven assigned role
```

Measure: zero forced provider changes or switch-induced authorization changes on other tiles.
Acceptance of role-dependent callers needs the unresolved business mapping below.

## Connections

- [SDK and entitlements](KT-sdk-and-entitlements.md) defines the existing entity-name migration and SDK compatibility intent.
- [Migration intake](../../../tasks/ces-entitlement-migration-20261102/01-intake.md) records the current requirement and unresolved evidence.
- [Frontend analysis](../../../tasks/ces-entitlement-migration-20261102/05-impact-analysis-frontend-entitlements.md) retains implementation comparisons and compatibility evidence separately.
- [Canonical coverage cases](../../../tasks/ces-entitlement-migration-20261102/06-test-cases.md) define observable comparisons separately from execution results.

## Evidence limits

The source establishes user-stated intent and comparison scope.
The user's statement about no entitlement gaps is an expectation, not retained execution proof.
This candidate does not establish completed migration, current account assignments, or deployed permission equality.
The FMO exception does not verify its current launch or provisioning state.
The frontend clarification supplies intended behavior, not complete compatibility or an approved scalar role mapping.
No human review, knowledge publication, migration acceptance, or deployment approval is recorded.

## Open questions

| Question | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Which source defines legacy data field and value restrictions? | Complete data-scope equality remains unassessed without that source. | unknown | Bind each legacy profile to authoritative restriction definitions. |
| Which CES-only management grants fall outside migration scope? | Additional grants need an explicit classification before equal-content acceptance. | unknown | Record the reviewed business scope and its source. |
| How must multiple CES roles map to existing caller role contracts? | Role-dependent behavior lacks an accepted mapping. | unknown | Define role selection or collection semantics for each affected business use. |
| Which reviewed mappings cover each upper-application API? | Full compatibility cannot follow from the user objective alone. | unknown | Define the application, feature, action, and caller contract mapping before acceptance. |
