---
type: KnowledgeTopic
id: KT-ces-migration-parity
version: 6
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
- resource: conversation:ces-entitlement-migration-20261102:bff-entity-fields-20261106
  revision: user-request-20261106-1
  sha256: 99f96926ace55ca7a89a6cf74ff2213ff097e76f2d760bc3f1c81c63bce2831c
- resource: conversation:ces-entitlement-migration-20261102:application-identity-20261106
  revision: user-clarification-20261106-1
  sha256: f90fafa768952c94b2bf3f4ef11c27b1d40828d9efab9b07b55b35fc86f472eb
- resource: conversation:ces-entitlement-migration-20261102:role-owned-writes-20261106
  revision: user-clarification-20261106-1
  sha256: 1daa1ada473bca8f7cc99fdbad2bb19d0ab0621883c3c660e0be1b9e334048d8
- resource: conversation:ces-entitlement-migration-20261102:provider-union-20261109
  revision: user-clarification-20261109-1
  sha256: 8c72705ccf11915baf40f2de503343c09ca7681c79f7780f23a75c019e01b57d
previous_version: 5
previous_content_sha256: 4c04e07ef6e963137528d807c41f071c066b692f5461bf8ea4ae38719b3022f5
previous_revision: 0047479bec4c29edf0dd9d9a484020998a6c523d
generated:
  by: agent:codex
  at: '2026-11-09T15:49:06.049328+00:00'
verified: []
classification: security
scope: Intended permission preservation, frontend compatibility, independent tile migration, and comparison scope for EMS2 to CES.
summary: Preserve upper-application APIs. Select tile admission per provider. Allow mapped EMS2 or CES grants through hasPermission and log their source.
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
The [user clarification](../../../evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) controls this scope from 3 November 2026.
The [frontend clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input) adds frontend compatibility and independent tile routing intent.
It applies from 6 November 2026 to `mfe-base`, the shared Ratan container, and their upper applications.
The [BFF field request](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) defines additive CES entity metadata from 6 November 2026.
The [application identity clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input) separates the legacy team label from CES application identity.
The [provider-union clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-gap-clarification-20261109.json) applies from 9 November 2026.
It permits existing `hasPermission(code)` calls to accept mapped EMS2 or CES grants, with provider-source logs.
The owning [migration task](../../../../tasks/ces-entitlement-migration-20261102/01-intake.md#current-task-state) retains source observations, implementation, and execution evidence separately.

## Summary

The migration must preserve permission meaning after the EMS2 and CES concepts are mapped.
Assess entitlement completeness separately from account permission completeness.
Two supplied account examples do not limit the required account population.
FMO Portal Admin has a separate, lower-priority non-production comparison under the user's clarification.
Preserve upper-application APIs where possible while selecting tile admission through its configured provider.
Allow mapped EMS2 or CES grants through existing `hasPermission(code)` calls.
Log the provider used without requiring an additional caller scope parameter.
Do not require one batch migration of every tile.
Treat role multiplicity as an explicit compatibility concern, separate from mapped feature/action permission meaning.
Expose CES entitlement names through `roleList` and the corresponding application identifier through `applicationId`.
These fields do not select a scalar role for existing callers.
Keep CES role-owned writes pending until an ownership rule is agreed.

## Documented knowledge

### Mapping between authorization concepts

| EMS2 concept | CES concept | Required comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition and its assigned accounts. |
| Entity | Application | Preserve application scope when comparing permission names. |
| Subject | Feature | Compare each subject through its explicit feature mapping. |
| Action | Action | Compare the permitted operation within the mapped feature. |

Source: [exact mapping clarification](../../../evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
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
Retain the [dated clarification](../../../evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) when applying this exception.
Future production scope requires a sourced update.

### Frontend compatibility and per-tile migration

The [frontend decision](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input) prioritizes compatibility with existing upper-application APIs.
Apply this objective to `mfe-base` and shared container APIs.
Preserve established caller contracts where possible. Adapt provider-specific identities and permission data internally.
The user identifies non-unique roles as the known compatibility gap.
This statement does not establish that every other API is compatible.
Keep each unresolved mapping visible before claiming complete compatibility.

Do not treat a combined effective permission set as one assigned role.
Preserve the distinction between assigned roles and effective feature/action permissions.
The contract for callers that expect one role requires a sourced business mapping.
Do not select an arbitrary role or infer a named role from effective action membership.

### Interim rule for CES role-owned writes

The [ownership decision](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-implementation-20261106/user-role-owned-writes-20261106.md#exact-user-answer) applies from 6 November 2026.
It covers CES saved-view and filter writes that require one owner role.
Keep these CES write paths unavailable until an ownership rule is agreed.
Do not select a primary CES role or submit comma-joined role names as a scalar owner.
Preserve existing EMS2 role-owned write behavior.
This interim rule does not define CES query visibility, role-query rules, or multiple-role exclusion policy.

#### FE-ROLE-WRITE-AC-001

Defer CES role-owned writes while their ownership rule remains unresolved.

```gherkin
Feature: Defer CES role-owned writes pending an ownership rule
  Scenario Outline: Keep a CES role-owned write pending
    Given a <item> uses CES authorization
    And writing the item requires one owner role
    And no agreed CES ownership rule exists
    When the user attempts to save the item
    Then the number of role-owned write requests sent equals 0
    And the number of CES roles selected as the scalar owner equals 0
    And the number of comma-joined role owners submitted equals 0

    Examples:
      | item       |
      | saved view |
      | filter     |

  Scenario: Preserve an existing EMS2 role-owned write
    Given a saved view or filter uses EMS2 authorization
    And its established EMS2 rules allow a role-owned write
    When the user saves the item
    Then its owner selection follows the existing EMS2 rules
    And the number of EMS2 write decisions changed solely by the CES pending rule equals 0
```

Measure: zero CES role-owned requests or fabricated scalar owners before agreement, with zero rule-induced EMS2 decision changes.
This criterion defines interim write behavior. It does not supply the missing CES ownership rule.

### Independent tile provider selection

Each tile must select its entitlement provider independently.
An EMS2 tile must retain its existing admission logic.
A CES tile must use CES admission logic, configured application identity, and CES permission structure.
Treat the CES application as the new entity identity within that selected scope.
Do not force unrelated tiles to change provider when one tile moves to CES.
Preserve application scope within both provider paths.

The [source interpretation](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#interpretation-for-this-stage) distinguishes plain `EMS2` from the final `EMS2 (CES)` phrase.
The latter denotes the CES path. The migration contract uses `EMS3` as its CES wire value.
The exact user quotation remains unchanged in the source.
This interpretation does not merge legacy EMS2 and CES tile admission choices.

The [latest provider clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-gap-clarification-20261109.json) permits either provider to satisfy an existing `hasPermission(code)` call.
Keep that shared functional check separate from tile admission.
Use reviewed application, feature, and action mappings when reading either provider.
Log which provider supplied an accepted grant.
Do not require upper applications to pass a new scope argument.
This rule does not select a scalar role or resolve saved-item ownership.

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

Admit each tile through its selected provider and application scope.

```gherkin
Feature: Select the admission provider per tile
  Scenario: Preserve independent legacy and CES tile admission
    Given one tile selects EMS2 and another tile selects CES
    And each tile has its reviewed application and permission configuration
    When the system evaluates whether to admit both tiles
    Then the EMS2 tile uses its existing EMS2 admission rules
    And the CES tile uses its configured CES application and permission structure
    And the number of admissions using only an unrelated application's grant equals 0
```

Measure: two tile admission paths follow their selected provider, with zero unrelated-application admissions.
The value two defines this comparison case. It does not limit the supported tile population.
This criterion does not restrict the shared provider-union permission check below.

#### FE-COMPAT-AC-003

Change one tile admission provider independently while keeping role multiplicity separate from permission equivalence.

```gherkin
Feature: Migrate tiles independently
  Scenario: Change one tile without forcing the remaining tiles to migrate
    Given a declared set of tiles uses its reviewed provider selections
    And one selected tile changes from EMS2 to CES
    And CES assignments can contain multiple roles
    When the system applies that selected tile's provider change
    Then the number of provider selections changed on other tiles equals 0
    And the number of upper-application permission call signatures changed solely by that switch equals 0
    And multiple role assignments are not represented as one proven assigned role
```

Measure: zero forced provider changes on other tiles and zero required permission call signature changes.
Acceptance of role-dependent callers needs the unresolved business mapping below.

#### FE-COMPAT-AC-004

Accept a mapped grant from either provider through the existing API and log its source.

```gherkin
Feature: Preserve hasPermission during provider migration
  Scenario Outline: Read either provider without changing the caller
    Given a reviewed application, feature, and action mapping exists for the requested code
    And EMS2 has <ems2_grant> matching grant
    And CES has <ces_grant> matching grant
    When the upper application calls hasPermission with only that code
    Then the returned boolean equals <expected>
    And the number of required additional caller arguments equals 0
    And an accepted decision has at least 1 log identifying a provider that supplied its matching grant

    Examples:
      | ems2_grant | ces_grant | expected |
      | 1          | 0         | true     |
      | 0          | 1         | true     |
      | 1          | 1         | true     |
      | 0          | 0         | false    |
```

Measure: four boolean results match the grant union, with zero additional arguments and provider logs for accepted decisions.
These four examples define the union cases. They do not limit accounts, applications, or permission codes.
The denial example requires no accepted-grant log because neither provider supplies a matching grant.

### CES entity role and application fields

The [BFF field decision](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) requires two additive fields on EMS3 entities.
`roleList` must contain the corresponding CES `entitlements.entitlement_name` values.
`applicationId` must contain the corresponding CES application's `itam_id` value.
The requested example identifies that application as `51358`.
Keep the role list bound to its corresponding application.
Do not use another application's entitlement names to populate that entity.

The [identity clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input) retains `applicationName` as the legacy team name.
For the clarified mapping, preserve these three field meanings:

| Field | Required value | Meaning |
| --- | --- | --- |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name corresponding to EMS2 `X_RATANONE`. |
| `applicationName` | `RATAN` | Legacy team/display application name. |
| `applicationId` | `"51358"` | Corresponding CES `itam_id`. |

CES `user_data.app_name` supplies the CES authorization name. It does not supply the legacy team label.
Do not replace the team label with the CES application name or application ID.
The clarified values apply to this RATAN mapping. They do not establish labels for other CES applications.

Retain existing entity fields and EMS2 authorization behavior within the compatibility objective.
These additive fields expose assignment names and application identity. They do not resolve scalar role semantics.
Do not infer feature/action ownership from a role name alone.
The [role contract question](#open-questions) remains open for callers that require one role.

#### BFF-ENTITY-AC-001

Expose CES entitlement names as an application-scoped role list.

```gherkin
Feature: Expose CES assignment names
  Scenario: Preserve multiple entitlement names in the corresponding EMS3 entity
    Given a CES application's entitlements.entitlement_name contains "role-a" and "role-b"
    And another application contains "role-c"
    When the BFF returns the first application's EMS3 entity
    Then its roleList contains "role-a" and "role-b"
    And its roleList contains 0 names taken solely from another application
```

Measure: two supplied entitlement names remain present, with zero names imported from another application.
The two names define this case. They do not limit the number of assigned entitlements.

#### BFF-ENTITY-AC-002

Keep the CES application identifier separate from its authorization name and legacy team label.

```gherkin
Feature: Expose CES application identity
  Scenario: Preserve the requested application identifier
    Given the corresponding CES application has itam_id "51358"
    And its CES name "RATAN_ENTITLEMENT_RULE" corresponds to EMS2 entity "X_RATANONE"
    And its legacy team applicationName is "RATAN"
    When the BFF returns that application's EMS3 entity
    Then applicationId equals "51358"
    And name equals "RATAN_ENTITLEMENT_RULE"
    And applicationName equals "RATAN"
    And the number of entity identifiers substituted for that applicationId equals 0
```

Measure: all three returned fields equal their declared values, with zero legacy identifier substitutions.
The example value identifies this case. It does not restrict other CES applications.

#### BFF-ENTITY-AC-003

Keep the additive metadata separate from legacy authorization and scalar role policy.

```gherkin
Feature: Keep additive CES metadata compatible
  Scenario: Preserve the EMS2 path while adding CES entity metadata
    Given a mixed-provider response contains an EMS2 entity and an EMS3 entity
    And the EMS2 entity has a declared legacy authorization decision
    When the BFF adds roleList and applicationId for the EMS3 entity
    Then the number of legacy EMS2 decisions changed solely by these additions equals 0
    And the number of existing entity fields removed by these additions equals 0
    And multiple CES entitlement names do not establish one selected scalar role
```

Measure: zero legacy decision changes and zero removed existing entity fields caused by these additions.
A separate sourced business mapping must define any later scalar role projection.

## Connections

- [SDK and entitlements](KT-sdk-and-entitlements.md) defines the existing entity-name migration and SDK compatibility intent.
- [Migration intake](../../../../tasks/ces-entitlement-migration-20261102/01-intake.md) records the current requirement and unresolved evidence.
- [Frontend analysis](../../../../tasks/ces-entitlement-migration-20261102/05-impact-analysis-frontend-entitlements.md) retains implementation comparisons and compatibility evidence separately.
- [Canonical coverage cases](../../../../tasks/ces-entitlement-migration-20261102/06-test-cases.md) define observable comparisons separately from execution results.

## Evidence limits

The source establishes user-stated intent and comparison scope.
The user's statement about no entitlement gaps is an expectation, not retained execution proof.
This candidate does not establish completed migration, current account assignments, or deployed permission equality.
The FMO exception does not verify its current launch or provisioning state.
The frontend clarification supplies intended behavior, not complete compatibility or an approved scalar role mapping.
The BFF field decision defines target metadata. It does not establish implemented, tested, or deployed response behavior.
The identity clarification defines this RATAN mapping. It does not establish a complete cross-application team-label catalog.
The ownership decision defers CES role-owned writes. It does not define CES ownership, query, or exclusion semantics.
The provider-union clarification changes permission-check intent. It does not prove implementation or deployed log collection.
Its expectation about returned legacy entities remains an implementation question, separate from this intended rule.
No human review, knowledge publication, migration acceptance, or deployment approval is recorded.

## Open questions

| Question | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Which source defines legacy data field and value restrictions? | Complete data-scope equality remains unassessed without that source. | unknown | Bind each legacy profile to authoritative restriction definitions. |
| Which CES-only management grants fall outside migration scope? | Additional grants need an explicit classification before equal-content acceptance. | unknown | Record the reviewed business scope and its source. |
| How must multiple CES roles map to existing caller role contracts? | CES role-owned writes remain pending; other role semantics lack an accepted mapping. | unknown | Define each role-dependent contract before enabling the affected CES behavior. |
| Which reviewed mappings cover each upper-application API? | Full compatibility cannot follow from the user objective alone. | unknown | Define the application, feature, action, and caller contract mapping before acceptance. |
