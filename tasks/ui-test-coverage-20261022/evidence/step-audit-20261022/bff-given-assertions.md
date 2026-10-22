---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Required BFF Given assertions

> **Critical conclusions: Action required**
>
> **Separate new-form defaults from existing database records.**
> Action: Apply the comparisons below after the frozen run completes.
> Consequence: Duplicate seed values and missing stale rows currently stop intended probes.
> Owner: Codex harness maintainer.
> Evidence: [Case 035 diagnosis](run-062-diagnoses/BFF-ADM-035.json), [case 062 diagnosis](run-062-diagnoses/BFF-ADM-062.json), and [case 078 diagnosis](run-062-diagnoses/BFF-ADM-078.json).

This plan changes harness assertions after the current source freeze.
It authorizes no business repository change.
The [canonical catalog](../../test-cases.md) remains the definition source.
Its SHA-256 is `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4`.
The [binding review](bff-binding-review.md) identifies the original gaps.
These comparisons are proposed harness corrections and have no execution result yet.

## Record identity

Select rows by their declared primary key.
Require exactly one matching row before comparing its fields.
Do not use `snapshot()[0]` as entity identity.
Do not require an existing business row when a creation case declares only initial grid contents.

| Entity | Persisted key | Response key | UI identity |
| --- | --- | --- | --- |
| Category | `application_category_id` | `applicationCategoryId` | DataGrid row `data-id` equals the declared identifier. |
| Import Map | `import_map_id` | `importMapId` | DataGrid row `data-id` equals the declared identifier. |
| Tile | `application_tile_id` | `applicationTileId` | DataGrid row `data-id` equals the declared identifier. |

## Actor, owner, and entitlement

Capture decoded claim projections from the actual login response.
Never save raw signed tokens in the report.
Decode access `sub` and the entitlement payload's `entitlements` JSON map.
The [actual validator](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L42) consumes those claims.
Decoding alone does not verify a signature.
Successful actual BFF authorization remains separate evidence of token acceptance.

| Given declaration | Minimum exact comparison |
| --- | --- |
| Actor uses subject `admin-a`, `admin-b`, `admin-c`, or `admin-s`. | Access claim `sub` equals the declared subject. Returned UI user information identifies that same subject. |
| Actor has `FMO_ADMIN`. | Parsed admin entity keys include exactly the declared owner role for the fixture actor. |
| Actor has `SUPER_USER only`. | Parsed admin entity keys contain `SUPER_USER`; they exclude `FMO_ADMIN` and `OTHER_ADMIN`. |
| Actor has no `OTHER_ADMIN` entitlement. | Parsed role keys contain no `OTHER_ADMIN` entry. Retain the projected role list. |
| Grid record N belongs to role R. | The persisted target row has `ems2_role === R`. The corresponding data-response row has `ems2Role === R`. Require the declared UI row. |
| Stored `updatedBy` equals subject S. | Select the declared record by key and require `updated_by === S`. Preserve case sensitivity. |

Use the configured admin entity name when parsing entitlement keys.
The current bootstrap supplies `FMO PORTAL ADMIN` through its [controlled identity service](current-bff-build/attempt-06/LocalSessionApplication.java#L159).
Retain the entity name and role projection beside the actor assertion.

## Baseline values

Treat `baseline fixture data defines` as new-form input defaults for creation cases.
Save one exact baseline object with its canonical step numbers.
The object must preserve empty strings, tabs, quotes, and character counts.
Existing seed rows must use distinct unique values unless a duplicate case explicitly requires a collision.
For edit cases, assert declared existing row values separately from proposed submitted values.

| UI field | Form or response property | Persisted property |
| --- | --- | --- |
| Category Label | `label` | `label` |
| Module Name | `keyName` | `key_name` |
| Path | `path` | `path` |
| Tile Name | `title` | `title` |
| Module Path | `module` | `module` |
| Tile Path | `tile` | `tile` |
| Role Entities | `ems2Entities` | `ems2_entities` |
| Filter Rule | `filterRule` | `filter_rule` |
| Entry Name | `entryName` | `entry_name` |

Require each filled control to have the submitted input value.
Wait for its delayed state update before starting another dependent field action.
The [source field controller](../../../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L19) delays state propagation by 300 milliseconds.
Retain the outbound property comparison when the canonical submit step occurs.
That comparison checks the form binding separately from the service result.

Record an empty Filter Rule input as the exact string `""`.
Record persisted normalization independently as `filter_rule:null` when observed.
The [service rule](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L202) normalizes blank rules.
Do not claim that the input string and database null are the same value.

## References and selected filters

| Given declaration | Minimum exact comparison |
| --- | --- |
| Category 101 has label `category-a`. | Require one persisted Category 101 with `label === 'category-a'`. |
| Import Map 201 has Module Name `container-a`. | Require one persisted Import Map 201 with `key_name === 'container-a'`. |
| Both references belong to `FMO_ADMIN`. | Require `ems2_role === 'FMO_ADMIN'` on both reference rows. |
| Tile category filter uses Category 101. | Require the filter control value `category-a`; resolve that unique option to response `applicationCategoryId === 101`. |
| Baseline Tile uses Category 101 and Import Map 201. | For a declared existing Tile, compare its persisted foreign keys. For a new form, retain expected selected IDs separately. |
| Category or Import Map reference is inactive. | Select the declared reference by key and require `is_active === false`. |
| Reference 102 or 202 belongs to `OTHER_ADMIN`. | Require the declared foreign key row and `ems2_role === 'OTHER_ADMIN'`. Compare every other declared reference owner with `FMO_ADMIN`. |
| Container `container-a` is selected. | Require the visible combobox value. At submit, require `importMap.importMapId === 201`, except for an explicit substitution case. |
| Interceptor substitutes a foreign or null reference. | Record the expected transformation. At submit, assert the actual outgoing nested property and actual BFF response separately. |

Require the Container state update before filling the next field.
Rapid field updates can overwrite the delayed selected reference.
Do not repair a missing reference by silently rewriting a normal outbound request.
Use request substitution only where the canonical case explicitly declares it.

## Duplicate, stale, and removal fixtures

| Fixture | Minimum exact comparison |
| --- | --- |
| Existing duplicate Category 102 | Require its key, declared `label`, and owner. Before creation, require exactly one matching persisted label. |
| Existing duplicate Import Map 102 | Require its key, declared `key_name`, path, and owner. Before creation, require exactly one matching persisted Module Name. |
| Foreign stale grid row 901 | Require persisted owner `OTHER_ADMIN`, declared marker value, and actual audit row ownership. Require one controlled UI row 901. |
| SUPER_USER stale detail | Supply record 101 through the declared controlled stale fixture. Keep actual signed entitlements restricted to `SUPER_USER`. |
| Controlled ownership change | Require SQL update count 1. Read the target by key and compare `ems2_role === 'OTHER_ADMIN'`. Refresh expected persistence only after this declared mutation. |
| Controlled reference removal | Require no unrelated seeded Tile or audit row to prevent deletion. Require delete count 1 and subsequent reference count 0. |

Keep database foreign-key constraints active during reference-removal probes.
For creation-only cases, an empty target grid can provide a valid initial snapshot.
Preserve the administration bootstrap under its distinct Category and Import Map identifiers.
The [case 078 diagnosis](run-062-diagnoses/BFF-ADM-078.json) records the current accidental foreign-key blocker.

## Validation and limits

This document defines minimum comparisons and expected data keys.
It adds no executable assertion during the source freeze.
A later run must retain the actual compared values and each canonical step screenshot.
Policy conflicts and undefined agreed messages remain separate acceptance limits.
The [review validation](bff-run-062-review-check.json) checks document links, retained hashes, and diagnosis reconciliation.
ASD review remains pending.
