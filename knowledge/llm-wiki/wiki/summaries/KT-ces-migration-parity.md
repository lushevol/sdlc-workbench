---
type: "Summary"
description: "Defines intended EMS2-to-CES permission parity, per-tile migration, and frontend compatibility rules."
doc_type: short
full_text: "sources/KT-ces-migration-parity.md"
---

# CES Migration Permission Preservation

## Overview

This topic defines the intended preservation of permission meaning when migrating from EMS2 production to CES UAT, covering mapped entitlement definitions and permission content for all scoped accounts. It also sets frontend compatibility and independent per-tile migration intent for `mfe-base`, the shared Ratan container, and their upper applications.

Scope is controlled by a series of user clarifications dated 3–9 November 2026. The document is a `candidate` draft and records user-stated intent, not verified execution.

## EMS2-to-CES concept mapping

| EMS2 concept | CES concept | Comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare mapped definition and assigned accounts |
| Entity | Application | Preserve application scope when comparing names |
| Subject | Feature | Compare through explicit feature mapping |
| Action | Action | Compare permitted operation within mapped feature |

Names shared across different applications do not establish equivalent permissions, and numeric source identifiers may differ without changing mapped meaning. See [[concepts/ems2-to-ces-permission-mapping]].

## Preservation requirements

### Entitlement and account parity

The intended migration has no missing mapped entitlements or permission gaps, but that is an expectation, not retained proof. Entitlement definitions must be compared before catalog totals are treated as completeness evidence. Different entitlements can yield the same combined effective permissions without proving equal definitions or assignments. See [[summaries/KT-sdk-and-entitlements]].

Account comparisons must include every account in the selected entity scope, expand multi-ID cells, and count each distinct account once. Application and entitlement scope must be retained, and data restrictions must be compared through authoritative definitions and resolved values—not profile names alone.

### Coverage and FMO exception

Fully matched migrated content moves into coverage totals and out of the active difference list; missing, additional, unresolved, and unavailable comparisons stay visible. An unavailable comparison proves neither equality nor missing permissions.

FMO Portal Admin is excluded from the production comparison and tracked as a separate, lower-priority non-production item. Its content must not enter production coverage denominators.

## Frontend compatibility and per-tile migration

The primary objective is compatibility with existing upper-application APIs, adapting provider-specific identities and permission data internally. Non-unique roles are the known compatibility gap; this does not prove every other API is compatible.

### Independent tile provider selection

Each tile selects its entitlement provider independently. An EMS2 tile keeps existing admission logic; a CES tile uses CES admission logic, configured application identity, and CES permission structure. Moving one tile to CES must not force changes on unrelated tiles. In the migration contract, `EMS2 (CES)` denotes the CES path with wire value `EMS3`. See [[concepts/per-tile-provider-selection]] and [[concepts/portal-entry-and-tile-authorization]].

### Provider-union hasPermission

Existing `hasPermission(code)` calls may accept a mapped grant from either EMS2 or CES. The check must log which provider supplied an accepted grant and must not require a new caller scope argument. This shared functional check is separate from tile admission. See [[concepts/permission-check-provider-union]].

### Role multiplicity and CES role-owned writes

Multiple assigned CES roles must not be collapsed into one proven role, and callers expecting a scalar role require a sourced business mapping. CES saved-view and filter writes that require one owner role stay disabled until an ownership rule is agreed; no primary role may be selected and no comma-joined role names may be submitted as a scalar owner. Existing EMS2 role-owned writes keep their behavior. See [[concepts/ces-role-multiplicity]].

## CES entity fields

Two new fields are required on EMS3 entities: `roleList` and `applicationId`. The table also records clarified values for the existing `name` and `applicationName` fields; those two existing fields are retained rather than introduced as additional new fields.

| Field | Required value | Meaning |
| --- | --- | --- |
| `roleList` | CES `entitlements.entitlement_name` values | Application-scoped assignment names |
| `applicationId` | CES application `itam_id` (e.g. `"51358"`) | CES application identity |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name for EMS2 `X_RATANONE` |
| `applicationName` | `RATAN` | Legacy team/display label |

CES `user_data.app_name` supplies the CES authorization name, not the legacy team label. These additions must not remove existing fields or change EMS2 decisions, and they do not resolve scalar role semantics. See [[entities/ratan]].

## Acceptance criteria

- **FE-ROLE-WRITE-AC-001** — Zero CES role-owned write requests or fabricated scalar owners before an ownership rule exists; zero rule-induced EMS2 decision changes.
- **FE-COMPAT-AC-001** — Zero contradictory decisions for mapped feature/action permissions through existing caller APIs.
- **FE-COMPAT-AC-002** — Each tile admits through its selected provider with zero unrelated-application admissions.
- **FE-COMPAT-AC-003** — One tile may switch provider with zero forced changes on other tiles and zero required call-signature changes.
- **FE-COMPAT-AC-004** — `hasPermission(code)` returns the union of EMS2 and CES grants across four cases, with no extra arguments and provider-source logs for accepted decisions.
- **BFF-ENTITY-AC-001** — `roleList` contains the application's entitlement names with zero names imported from another application.
- **BFF-ENTITY-AC-002** — `applicationId`, `name`, and `applicationName` match declared values with zero legacy substitutions.
- **BFF-ENTITY-AC-003** — Additive metadata changes zero EMS2 decisions and removes zero existing fields.

## Evidence limits and open questions

The source establishes intent and comparison scope only. It does not prove completed migration, deployed permission equality, implemented BFF behavior, or log collection. No human review or migration acceptance is recorded.

Open questions:

1. Which authoritative source defines legacy data field and value restrictions per profile?
2. Which CES-only management permissions fall outside migrated business permissions?
3. How must multiple CES roles map to existing caller role contracts and role-dependent business rules?
4. Which reviewed mappings cover each upper-application API and its CES permission inputs?

## Related pages

- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/permission-check-provider-union]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[entities/ems2]]
- [[entities/ces]]
- [[entities/ems3]]
- [[entities/ratan]]
- [[entities/mfe-base]]

## Related Concepts
- [[concepts/ems2-entitlement-provisioning]]
- [[concepts/entitlement-retrieval]]
- [[concepts/identity-provider-delegation]]
- [[concepts/application-ownership]]
- [[concepts/shared-dependency-governance]]

## Entities
- [[entities/mfe-ratan-container]]
- [[entities/single-ui-bff]]
- [[entities/single-ui-sdk]]
- [[entities/ratan-auth-server]]
- [[entities/fmo-post-trade-portal]]
