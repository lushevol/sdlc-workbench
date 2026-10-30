---
artifact_kind: interface-contract
id: CES-OUTPUT-MAPPING
version: 3
status: draft
owner: unknown
source_refs: [USER-ENDPOINT-20261030, USER-FIELD-20261030, EMS2-GRANTS, CES-ROLE-DETAILS, CES-CATALOG, CES-EFFECTIVE, ENDPOINT-CONSUMERS]
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
    - Source correspondence does not establish approved role equivalence or passing business execution.
---

# EMS2 to CES field, ID, and structure mapping

> **The effective endpoint alone cannot supply the numeric IDs shown from other CES responses.**
> Action: use name-based permissions or supply an authoritative ID crosswalk when consumers require numeric IDs.
> Consequence: a complete numeric legacy projection cannot be reconstructed from this response alone.
> Owner: unknown. Evidence: [endpoint-only scope](#using-only-the-effective-user-endpoint).
>
> **Keep regenerated IDs and role assignments separate from the confirmed rename.**
> Action: use the field correspondence below and retain each provider's identifier namespace.
> Consequence: treating an EMS2 grant ID as a CES role ID would connect different objects.
> Owner: unknown. Evidence: [field mapping](#field-correspondence-and-cardinality) and [role distinction](#role-definition-versus-user-assignment).

Latest high-priority scope: [single effective-endpoint question](evidence/user-input-20261030-effective-endpoint-only.txt), 30 October 2026.

Prior high-priority source: [field-equivalence request and rename clarification](evidence/user-input-20261030-field-equivalence.txt), 30 October 2026.
The user confirms **EMS2 `X_RATANONE` was renamed to CES `RATAN_ENTITLEMENT_RULE`**.
This supersedes the earlier unresolved name correspondence within this scope.
It does not establish that old numeric IDs remain valid in CES.

The earlier broader mapping remains recoverable at Workbench commit `d6df12199`, using this same document path.
Original intake, samples, and earlier evidence remain unchanged.

## Contract identity and boundary

| Field | Value |
| --- | --- |
| Contract ID and type | CES-OUTPUT-MAPPING; HTTP response field correspondence. |
| Contract maturity | Confirmed name migration and inspected source structures; role equivalence remains qualified. |
| Provider IDs | EMS2 and CES; external registry identities unresolved. |
| Consumer IDs | RATAN migration readers; Auth Server and Single UI BFF consume these provider models. |
| Repository ID | Not applicable to the primary evidence; this comparison uses supplied API response bytes. |
| Source path and lines | [Field facts and JSON pointers](evidence/field-equivalence-facts-20261030.json). Samples contain one JSON line each. |
| Full Git commit | Sample capture revisions unavailable. SHA-256 identifies each retained source file. |
| Documentation gap | Numeric migration crosswalk and complete approved role/assignment equivalence remain unavailable. |

Scope: `RATAN_STRATEGIC_CASHFLOW_BLOTTER` and `RATAN_TRADE_BLOTTER` within the confirmed application rename.
Confidence: HIGH for exact field values and the user-stated name migration.
One-to-one conclusions below apply to the named objects and inspected samples only.

## Operations and delivery

| Operation | Transport and address | Trigger | Side effects | Ordering, retry, timeout, and idempotency |
| --- | --- | --- | --- | --- |
| EMS2 grant retrieval | Supplied entitlement-list dump; exact capture parameters unavailable. | Inspect entity, subject, role, action, and grant IDs. | Read-only local inspection. | Delivery contract not established by retained samples. |
| CES assigned-role details | Supplied user-role response with `featureActionDtos`. | Inspect application, feature, action, and assigned role IDs. | Read-only local inspection. | Capture environment and time unknown. |
| CES application catalog | Supplied catalog for `51358/RATAN_ENTITLEMENT_RULE`. | Locate the corresponding role definition. | Read-only local inspection. | Catalog membership differs from effective response semantics. |
| CES effective grants | Supplied application/user response. | Inspect flattened effective permissions. | Read-only local inspection. | Role provenance and numeric IDs are omitted from each permission pair. |

## Inputs

| Name and location | Type or schema | Required | Validation and limits | Example |
| --- | --- | --- | --- | --- |
| EMS2 grant | Object under `[userId].entitlements[]`. | For legacy field comparison. | One row contains one subject, role, and action combination. | `/1481696/entitlements/60`. |
| CES assigned-role details | Array of role objects. | For feature and action IDs. | Every role owns a `featureActionDtos[]` array. | `/5/featureActionDtos/3`. |
| CES catalog | Array of entitlement definitions. | For corresponding `FMO_OPS_BOM` role. | Same-name definition does not establish user assignment. | `/56`, ID `593`. |
| CES effective response | Array of account/application objects. | For flattened output comparison. | Grants contain names without numeric IDs. | `/0/entitlements/role_entitlements`. |

## Authentication and authorization

This document maps provider response fields; it does not change authorization policy.
The user confirms the application rename.
No new permission assignment, role approval, or deployed enforcement was established.

## Outputs

### Using only the effective user endpoint

Requested endpoint: `/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userid}`.
The [supplied response](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json) returns effective name-based grants.
It supports permission checks for its returned application scope without requiring permission-object numeric IDs.
Its completeness for other applications or account attributes is not established.

This is a source-backed answer, not a live CES request or API version guarantee.

| Required information | Available from this endpoint's supplied response? | Mapping or implication |
| --- | --- | --- |
| User identity | Yes: `user_data.user_id`. | Preserve its string value. |
| CES application name | Yes: `user_data.app_name`. | `RATAN_ENTITLEMENT_RULE`; user-confirmed legacy name is `X_RATANONE`. |
| External application/ITAM reference | Yes: `user_data.itam_id`, value `"51358"`. | This does not provide internal `appUID` or the EMS2 entity ID. |
| Subject/feature name | Yes: `entitlements.role_entitlements[].feature`. | Group identical feature names into subject-like containers when needed. |
| Action name | Yes: each grant's `action`. | Pair with feature and application scope for permission evaluation. |
| Assigned role names | Yes: `entitlements.entitlement_name[]`. | Keep the collection. Do not select the first role arbitrarily. |
| Subject/feature, role, action, or grant numeric IDs | No fields in the supplied effective grants. | Do not copy numeric IDs from earlier examples into this endpoint's output. |
| Internal CES application ID | No `appUID` in this response. | The earlier value `10` comes from the role-detail response. |
| Grant-to-role relationship | Not returned for each pair. | Assigned role names do not identify which role supplied a particular grant. |
| Data policies, profiles, and field/value filters | Yes in the supplied response. | Preserve their separate structures. Profile names require reviewed legacy-role equivalence. |
| Full account status, account type, or account owner | Not supplied as equivalent account fields. | Existing account-dependent flows need another authoritative source or a revised contract. |

The response contains user and application references, plus profile/policy owner references.
Its missing IDs are the permission-object IDs discussed in the preceding comparison.

#### Endpoint-only permission examples

| Blotter | Returned pair | Name-based human permission |
| --- | --- | --- |
| `RATAN_STRATEGIC_CASHFLOW_BLOTTER` | `{"feature":"RATAN_STRATEGIC_CASHFLOW_BLOTTER","action":"F_Export_Data"}`. | `RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Export_Data`. |
| `RATAN_TRADE_BLOTTER` | `{"feature":"RATAN_TRADE_BLOTTER","action":"F_Export_Data"}`. | `RATAN_TRADE_BLOTTER:F_Export_Data`. |

Both pairs occur in the effective sample.
The projection uses the current [Auth conversion rule](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:147).
The numeric IDs `176`, `172`, `208`, and role `593` cannot be derived from these pairs alone.

A proposed permission key is `(itam_id, app_name, feature, action)`.
This keeps application scope while allowing IDs to remain absent.
Names require controlled rename handling; this proposal does not establish immutable identifiers.

#### Compatibility choices

1. Prefer the returned names for permission decisions when consumers support those fields.
2. Preserve the complete role-name collection and apply reviewed mappings for role-dependent operations.
3. Make absent numeric IDs explicit through a revised optional-field contract or a compatible adapter.
4. Replace rendering keys with scoped name-based keys where that consumer permits the change.
5. Use a maintained authoritative crosswalk if unchanged consumers genuinely require numeric IDs.
6. Obtain CES detail data when exact CES numeric identity or per-role provenance is mandatory and no crosswalk exists.

These are design options. No consumer changes were made.
A hash or sequence number would create a local identifier, not recover the missing CES or EMS2 identity.

The current BFF already groups CES features into subjects and copies action names.
It leaves entity, role, subject, and action numeric IDs unset in that projection.
It also leaves `roleName` unset, which is a separate compatibility concern.
Source: [BFF mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62).

Most inspected permission checks use names, but numeric fields are not universally unused.
Frontend entitlement types require numeric fields, and the Profile view uses entity/subject IDs for rendering.
Admin flows depend on `roleName` and entity-to-role mappings.
Source: [current consumer investigation](evidence/effective-endpoint-consumers-20261030.json).

Therefore, this endpoint can support name-based effective authorization for the returned scope.
It cannot independently reconstruct the complete ID-based EMS2 structure or every existing role-dependent contract.

### Field correspondence and cardinality

CES detail paths below are relative to an assigned-role object in the response array.
EMS2 paths are relative to one grant row.

| EMS2 field | EMS2 structure/type | CES equivalent | CES structure/type | One-to-one? |
| --- | --- | --- | --- | --- |
| `subject.entity.name` | String inside repeated entity object; `X_RATANONE`. | `appName`; also `featureActionDtos[].features.applicationDto.appName` and `featureActionDtos[].actions.applicationDto.appName`. | String; `RATAN_ENTITLEMENT_RULE`. Effective response uses `user_data.app_name`. | **Yes, the name correspondence is user-confirmed for this migration.** |
| `subject.entity.id` | Integer; `11274101`. Entity also repeats under role and action. | Nearest internal application identity: `appUID`; also `featureActionDtos[].features.applicationDto.appUID` and `featureActionDtos[].actions.applicationDto.appUID`. | Integer; `10`. Separate external `appId` is string `"51358"`; effective response uses `itam_id`. | One corresponding application scope is observed. **IDs differ and are not interchangeable.** No universal numeric crosswalk is established. |
| `subject` | Object: `id`, `name`, `longName`, `entity`. | `featureActionDtos[].features`. | Object: `featureId`, `featureName`, `applicationDto`. | One logical subject corresponds to one feature in each named example. Fields and nesting differ. |
| `subject.name` | String. | `featureActionDtos[].features.featureName`. | String. Effective/catalog grants shorten this to `feature`. | **Yes for both requested blotter names.** |
| `subject.id` | Integer. | `featureActionDtos[].features.featureId`. | Integer. | **One logical ID pair per requested blotter is observed; values are regenerated.** It is not an identity-preserving numeric copy. |
| `role` | Object: `id`, `name`, entity reference, and metadata. Repeated per grant row. | Assigned-role object, or catalog entitlement definition. | Object: role ID/name plus a collection of feature/action pairs. | Role definitions correspond conceptually, but source rows are regrouped. Complete role and assignment equivalence is unproved. |
| `role.name` | String; `FMO_OPS_BOM`. | Detail `entitlementName`; catalog `entitlement_name`. | String. Effective response exposes a list, `entitlement_name[]`. | A same-name `FMO_OPS_BOM` definition exists. **Do not infer the sample user's CES assignment from that definition.** |
| `role.id` | Integer; `11274177`. | Detail `entitlementId`; catalog `entitlement_id`. | String in assigned-role samples; integer in catalog. Same-name catalog role ID is `593`. | **Candidate definition correspondence: `11274177 → 593`.** Numeric identity is not preserved. Complete equivalence requires review. |
| `action.name` | String. | `featureActionDtos[].actions.actionName`. | String. Effective/catalog grants shorten this to `action`. | **Yes for the matching action names within the two same-role blotter definitions.** |
| `action.id` | Integer. | `featureActionDtos[].actions.actionId`. | Integer. | Logical action correspondence is observed; numeric values differ. Example: `11274984 → 193`. |
| Grant-row `id` | Integer identifying the EMS2 entitlement combination. | No corresponding grant ID in the supplied effective pair. | CES role-detail pairs contain feature/action objects; effective pairs contain two names. | **No demonstrated one-to-one field. CES `entitlementId` identifies a role, not this grant row.** |
| `subject.longName` | String; slash-prefixed subject path. | No separate field in supplied CES feature objects. | `featureName` remains available. | No direct field equivalent demonstrated. |

### Concrete blotter mappings

The CES feature/action IDs come from the assigned-role detail response.
The corresponding `FMO_OPS_BOM` role ID comes from the application catalog.
These are separate response views of the same sampled application scope.

| Field | Strategic cashflow: EMS2 → CES | Trade blotter: EMS2 → CES |
| --- | --- | --- |
| Entity/application name | `X_RATANONE → RATAN_ENTITLEMENT_RULE`. | `X_RATANONE → RATAN_ENTITLEMENT_RULE`. |
| Entity/internal application ID | `11274101 → appUID 10`. | `11274101 → appUID 10`. |
| Separate CES external application reference | `appId: "51358"`. This is not the old entity ID. | `appId: "51358"`. This is not the old entity ID. |
| Subject/feature name | `RATAN_STRATEGIC_CASHFLOW_BLOTTER → RATAN_STRATEGIC_CASHFLOW_BLOTTER`. | `RATAN_TRADE_BLOTTER → RATAN_TRADE_BLOTTER`. |
| Subject/feature ID | `11274215 → 176`. | `11274226 → 172`. |
| Same-name role definition | `FMO_OPS_BOM → FMO_OPS_BOM`. | `FMO_OPS_BOM → FMO_OPS_BOM`. |
| Role/catalog entitlement ID | `11274177 → 593`. | `11274177 → 593`. |
| Portal-access action name | `ACCESS_FMO_POST_TRADE_PORTAL` in both. | `ACCESS_FMO_POST_TRADE_PORTAL` in both. |
| Portal-access action ID | `11274984 → 193`. | `11274984 → 193`. |
| Export action ID | `11274960 → 208`; name remains `F_Export_Data`. | `11274960 → 208`; name remains `F_Export_Data`. |
| EMS2 portal-access grant-row ID | `410988`; no direct CES grant-ID equivalent demonstrated. | `411003`; no direct CES grant-ID equivalent demonstrated. |
| Matching same-role action sets | **20 EMS2 actions = 20 CES catalog actions**, by exact name. | **6 EMS2 actions = 6 CES catalog actions**, by exact name. |

### Structure transformation

EMS2 stores one grant row with nested subject, role, action, and repeated entity references.
CES role details group multiple feature/action pairs beneath one role object.
CES effective output flattens granted pairs across assigned roles.

| View | Structure | Cardinality and information retained |
| --- | --- | --- |
| EMS2 grants | `userId → entitlements[] → {id, subject, role, action}`. | Many grant rows repeat the same role and entity. |
| CES role details | `[{entitlementId, entitlementName, appName, appUID, featureActionDtos:[{features, actions}]}]`. | One role contains many feature/action pairs. Pair objects retain feature/action IDs and role provenance. |
| CES catalog | `[{entitlement_id, entitlement_name, role_entitlements:[{feature, action}], user_ids}]`. | One role definition contains many name-based pairs. Feature/action IDs are absent from this view. |
| CES effective grants | `[{user_data, entitlements:{entitlement_name:[], role_entitlements:[{feature, action}]}}]`. | Many assigned roles contribute to the flattened pair collection. Individual pairs omit role and numeric IDs. |

Therefore, the entire EMS2 and CES JSON responses do **not** map one-to-one by row or nesting.
Selected business objects correspond, but IDs, types, grouping, and retained information differ.

### Role definition versus user assignment

The EMS2 sample grants these blotter permissions under role `FMO_OPS_BOM`, ID `11274177`.
The CES catalog contains `FMO_OPS_BOM`, ID `593`, at pointer `/56`.
Its strategic-cashflow and trade action sets match the sampled EMS2 grant sets exactly.

However, the supplied CES user's assigned-role detail contains `NON_FMO_RO`, ID `"601"`.
That role supplies the sampled strategic and trade feature IDs and four actions for each blotter.
The supplied user's CES assignments do not include `FMO_OPS_BOM`.

**`FMO_OPS_BOM → NON_FMO_RO` is not a demonstrated migration mapping.**
The role-definition comparison and the user-assignment comparison answer different questions.

Across all features, the EMS2 `FMO_OPS_BOM` sample has 63 unique feature/action pairs.
CES catalog role `593` has 68, including five additional validation-exception pairs.
Thus, matching the two requested blotters does not establish whole-role equivalence.

### Exact sample locators

| Fact | Source | JSON pointer |
| --- | --- | --- |
| EMS2 strategic portal-access row | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json). | `/1481696/entitlements/60`. |
| EMS2 trade portal-access row | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json). | `/1481696/entitlements/61`. |
| CES strategic feature `176`, portal action `193` | [CES role details](api/-fmces-v1-entitlement-user-1481696.json). | `/5/featureActionDtos/3`. |
| CES trade feature `172`, portal action `193` | [CES role details](api/-fmces-v1-entitlement-user-1481696.json). | `/5/featureActionDtos/14`. |
| CES same-name role `593` | [CES application catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). | `/56`. |
| CES effective name-only grants | [CES effective response](api/-fmces-v1-entitlement-user-response-1481696.json). | `/0/entitlements/role_entitlements`. |

## Errors

No error response was supplied for these mapping examples.
Missing IDs in effective output are a response-shape limitation, not evidence of an API failure.
Unsupported numeric identity assumptions must remain unresolved rather than receiving invented defaults.

## Compatibility and verification

The static same-role comparison uses exact subject/feature and action names within application scope.
It compares 20 strategic actions and six trade actions without case folding or inferred synonyms.
Results and hashes are retained in [field facts](evidence/field-equivalence-facts-20261030.json).

These checks establish source correspondence, not runtime access or approved role equivalence.
Business execution: NOT_RUN. No implementation or application tests changed.

| Check | Result evidence | Limit |
| --- | --- | --- |
| Raw values, JSON pointers, ID types, and same-role set comparison | [Field-equivalence facts](evidence/field-equivalence-facts-20261030.json). | Independent capture times and environments remain unknown. |
| Document lint, references, and source hashes | [Current stage checks](evidence/field-equivalence-checks-20261030.json). | Syntax and provenance checks do not prove permission equivalence. |
| Knowledge successor and source provenance | [Workspace validation](evidence/field-equivalence-knowledge-validation-20261030.json). | Candidate knowledge remains unpublished; no deployment or human approval inferred. |

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| USER-ENDPOINT-20261030 | [Endpoint-only question](evidence/user-input-20261030-effective-endpoint-only.txt). | User question, 30 October 2026. | [Endpoint checks](evidence/effective-endpoint-checks-20261030.json). | User; current hypothetical source scope. |
| ENDPOINT-CONSUMERS | [Current consumer investigation](evidence/effective-endpoint-consumers-20261030.json). | Exact local revisions and file hashes. | Per-file SHA-256 in the investigation. | Owner unknown; current implementation evidence only. |
| USER-FIELD-20261030 | [Preserved request](evidence/user-input-20261030-field-equivalence.txt). | User clarification, 30 October 2026. | [Current checks](evidence/field-equivalence-checks-20261030.json). | User; highest-priority source for the confirmed rename and requested scope. |
| EMS2-GRANTS | [EMS2 grant dump](api/:ems2:rest:entitlements:entitlementList%20.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Owner unknown; exact observed values only. |
| CES-ROLE-DETAILS | [CES assigned-role details](api/-fmces-v1-entitlement-user-1481696.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Owner unknown; feature/action IDs and current sampled assignments. |
| CES-CATALOG | [CES catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Owner unknown; role definitions and listed membership. |
| CES-EFFECTIVE | [CES effective response](api/-fmces-v1-entitlement-user-response-1481696.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Owner unknown; flattened effective name pairs. |

### Knowledge-update log

| Clarification | Affected record | Recorded change | Provenance and audit | State and remaining limit |
| --- | --- | --- | --- | --- |
| Confirmed entity/application rename | [KT-sdk-and-entitlements v7](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration). | `X_RATANONE → RATAN_ENTITLEMENT_RULE`. | Source `SRC-ces-entity-rename-20261030`; [new audit event](../../evidence/knowledge/audit/AUD-20261030-KT-sdk-and-entitlements-v7.yaml). | Candidate/draft; no numeric ID, role, execution, or publication approval inferred. |

The endpoint-only question adds an implementation hypothesis, without changing business rules or the confirmed rename.
No further governed knowledge update is required for this question.
Endpoint-specific checks: [response and consumer evidence](evidence/effective-endpoint-checks-20261030.json).

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| FIELD-01 | [Latest user clarification](evidence/user-input-20261030-field-equivalence.txt). | Earlier uncertainty about the entity/application name is resolved. | User supplied clarification; record owner unknown. | Use the confirmed rename within this migration scope. | RESOLVED |
| FIELD-02 | [Catalog role and assigned-role details](evidence/field-equivalence-facts-20261030.json). | Corresponding role definitions do not prove equivalent account assignments or whole-role behavior. | unknown | Reconcile the five additional pairs and intended user role assignments before acceptance. | OPEN |
| FIELD-03 | [ID paths and structures](evidence/field-equivalence-facts-20261030.json). | Legacy identifiers cannot be reused as CES identifiers. Flattened grants lose direct role provenance. | unknown | Use a scoped ID crosswalk and the appropriate CES detail view when consumers need IDs. | OPEN |
