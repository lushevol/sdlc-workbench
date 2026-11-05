---
artifact_kind: change-request
id: CR-CES-FRONTEND-ENTITLEMENT-IMPACT
version: 1
status: draft
owner: unknown
source_refs: [USER-FRONTEND-20261105, BFF-MAIN, BFF-CANDIDATE, MFE-BASE, RATAN-CONTAINER, LOGIN-CAPTURE, TILE-DUMP]
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

# CES migration: required frontend entitlement changes

> **The shared Ratan helper denies captured CES grants. Update its application-scoped permission lookup.**
> Action: implement the resolver and reconcile role-dependent consumers before frontend migration acceptance.
> Consequence: export, private-view, query-builder, and some page checks can deny granted access.
> Owner: unknown. Evidence: [original-module probe](evidence/frontend-entitlement-impact-20261105/ratan-container.json).

| Essential result | Evidence boundary |
| --- | --- |
| Shared helper resolves 1/31 captured CES grants; 30 fail. | Original TypeScript execution with capture-fed hooks. No browser execution. |
| Helper resolves 0/24 grants whose features have exact tile-dump references. | Counts include all database rows. They do not establish deployed business scope. |
| All 41 captured CES tiles fit the portal's generic entity/subject predicate. | Source-predicate replay; no original-module or browser tile execution. |
| Nine existing base tests pass across four files. | Focused subset. Some tests contain no assertions. No complete unit-suite claim. |
| Application changes remain proposed. | No application source changed. No release or acceptance decision is made. |

## Request and source facts

Assessment: 6 November 2026, Asia/Singapore. Assessor: Codex.
The [request](evidence/frontend-entitlement-impact-20261105/user-input.md#exact-user-input) arrived on 5 November and authorizes required-change identification.
The user identifies the CSV as a database dump.
The user identifies the JSON as a real login capture for account `1481696`.
Capture environment, build, and time remain unknown.
Entry route: existing implementation with supplied database and runtime evidence.

The [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json) records 113 database rows: 45 EMS3 and 68 EMS2.
All 45 EMS3 rows use app ID `51358` and app name `RATAN_ENTITLEMENT_RULE`.
Their legacy `ems2_entities` values retain `X_RATANONE`.
The login contains 61 tiles: 41 EMS3 and 20 EMS2.
Its CES aggregate contains 21 features and 31 feature/action pairs.
CES role names and legacy numeric identifiers are null.
The entitlement token contains the key `RATAN_ENTITLEMENT_RULE:null`. This suffix is not an assigned role.

The [existing name clarification](evidence/user-input-20261030-field-equivalence.txt) establishes the migration name correspondence.
The [permission intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts) requires application scope.
Matching feature names across different applications cannot establish equivalent permissions.

## Stage boundary and readiness

- Stage: bounded frontend compatibility impact analysis, completed within the inspected scope.
- Readiness: `READY` for this analysis handoff and scoped engineering design.
- Rationale: exact BFF sources and both frontend consumers establish the required compatibility surfaces.
- Existing intake: [01-intake.md](01-intake.md), preserved unchanged. Its hash appears in the [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
- BFF comparison: local `main...HEAD`; `main` equals the merge base. No remote fetch occurred.
- Business roles and blank-feature admission need contract decisions before their dependent implementation acceptance.
- Business acceptance, knowledge publication, and deployment retain their separate pending states.
- Full frontend implementation readiness is not established by this analysis.

## Proposed change

### FE-01: Replace identity-specific shared permission dispatch

Priority: P2. Confidence: high. Owner: unknown.
Location: [authenticator.ts](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L38-L105).
Setup and numbered steps: [TC-FE-CES-001](06-test-cases.md#tc-fe-ces-001).

Required result: preserve mapped, application-scoped grants through the migration.
Old source path: `X_RATANONE` selects exact subject/action lookup.
New input: `RATAN_ENTITLEMENT_RULE` reaches legacy entity-name substring matching.
Most feature names do not match that application name. The helper returns false despite a captured grant.
The sole passing pair has feature name `RATAN_ENTITLEMENT_RULE`, which accidentally matches the application name.
A synthetic name-only control resolves all 31 grants. This is not an actual EMS2 baseline.

Next action: introduce one resolver for application, feature, action, and applicable provider context.
Keep EMS2 compatibility during mixed rollout. Use reviewed configuration for application correspondence.
Keep existing feature/action constants when their CES meanings match.
Merge duplicate rows within the selected application. Do not merge grants across unrelated applications.
Do not use a global feature search or substring matching to select an application.

The [shared export](../../repos/ui/mfe-ratan-container/src/root.tsx#L12) reaches [cashflow consumers](../../repos/ui/mfe-cashflow-blotter/src/Root/import/ratanutils/index.ts#L6-L7).
Update the shared container and verify its deployed import-map consumers together.

### FE-02: Reconcile roles independently from action grants

Priority: P2 for contract work. Confidence: high for absent roles; downstream impact remains conditional. Owner: unknown.
Location: [getUser](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L6-L35).
Observation: [TC-FE-CES-005](06-test-cases.md#tc-fe-ces-005).

Old source path: `X_RATANONE.roleName` supplies a scalar role.
New input: the CES aggregate has no role name. `getUser().role` is unavailable.
[Saved views](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L21-L38) use role values for assignee and ownership filters.
[Saved filters](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts#L22-L39) also consume role values.
[Exception checks](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L319-L335) contain `PSS_RO` restrictions.
No live API result establishes those downstream consequences.

Next action: define the required role/profile contract with BFF and CES evidence.
Support multiple assigned roles only after their semantics are established.
Do not derive `PSS_RO`, maker/checker, or admin roles from the effective action union.
The [admin role helper](../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L10) remains tied to `FMO PORTAL ADMIN`.
That entity remains EMS2 in this capture. Its CES migration requires coordinated backend authorization changes.

### FE-03: Align portal tile admission with the CES contract

Priority: P2 for supported configuration compatibility. Current sample impact is not demonstrated. Owner: unknown.
Location: [validateTile](../../repos/ui/mfe-base/src/utils/common.ts#L260-L311).
Cases: [TC-FE-CES-002](06-test-cases.md#tc-fe-ces-002) and [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003).

Old contract: drawer subjects and grants both use EMS2 subjects.
New contract: BFF authorizes `entitlement_app_feature`, but drawer `subject` still contains `ems2_subject`.
The [BFF drawer builder](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L208-L225) changes granted tile entities to CES app names.
The [portal validator](../../repos/ui/mfe-base/src/utils/common.ts#L265-L290) still requires a matching nonblank legacy subject.
[Direct launch](../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L66-L85) and workspace retention reuse that check.

All 41 captured CES tiles have matching, nonblank subjects. Their generic predicates succeed.
The base `X_RATANONE` occurrence is a legacy fallback, not this sample's failure cause.
A different or blank legacy subject can contradict a valid BFF CES grant.
Next action: use one reviewed CES admission decision across drawer launch, direct launch, and workspace restoration.
For feature-controlled tiles, use current authorized drawer membership or an explicit normalized grant contract.
Deny tiles absent from the current authorized catalog. Reconcile template and blank-feature rules separately.

The candidate BFF bypasses CES lookup when the configured feature is blank.
That behavior can return a tile with empty entities. It is not approved by this source analysis.
The prior [empty-subject intent](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule) still requires an entitled configured entity.
CSV tile `192` is inactive and absent from this login. It does not establish a current login failure.
Do not expand blank-feature access until this policy difference is reconciled.

### FE-04: Add CES tile configuration and audit controls

Priority: P2. Confidence: high. Owner: unknown.
Locations: [tile editor](../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L232-L259) and [audit view](../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx#L124-L137).
Proposed validation: [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004).

Old UI: administrators configure legacy entity, subject, and ownership fields.
New BFF interfaces add `entitlementSource`, `entitlementAppId`, `entitlementAppName`, and `entitlementAppFeature`.
The current UI cannot create or change these CES routing values, or inspect them during checker review.
Next action: add all four fields to create, edit, detail, and audit controls.
Use display label `CES` with wire value `EMS3`. Supported wire values are `EMS2` and `EMS3`.
Match [backend validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L22-L74).
App ID is one value, limited to 64 characters.
App names and features support English-comma lists, limited to 512 characters each.
EMS3 requires app ID and app name. Blank features need the policy decision described above.

Existing fetched-row edits preserve hidden fields through whole-row spreading.
No current ordinary-edit source reset is established.
The BFF defaults an actually omitted source to EMS2. Retain explicit metadata round-trip assertions.
Backend CSV contracts also add four fields. Extend actual CSV consumers if identified.
No CSV UI was found in the inspected base TypeScript sources. No new CSV UI is required by this request.

### FE-05: Correct shared response types and provider propagation

Priority: P3 contract maintenance. Confidence: high. Owner: unknown.
Location: [response models](../../repos/ui/mfe-base/src/hooks/model/root.ts#L42-L80).

Old models require numeric identifiers, application names, and role names.
New CES entities, subjects, and actions carry null legacy identifiers.
Next action: make these fields nullable or optional according to the actual response contract.
Add `entitlementSource` to subject and tile models. Preserve it in route and container props.
Keep provider selection separate from the feature/action meaning and business ownership role.
The existing [login decoder](../../repos/ui/mfe-base/src/utils/login.ts#L65-L95) already accepts the normalized envelope.
No new login endpoint or frontend CES HTTP client is required.

### FE-06: Update analytics profile extraction

Priority: P3. Confidence: high for source behavior. Owner: unknown.
Location: [profile extraction](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts#L7-L44).
Old extraction searches entitlement-token keys for `X_RATANONE`.
The new key yields no profile through that lookup.
Next action: use the reviewed role/profile contract, or report profile unavailability explicitly.
No session disruption or analytics delivery failure was demonstrated.

## Scope and affected artifacts

| Artifact | Exact source identity | Risk and basis |
| --- | --- | --- |
| BFF baseline | `834b4155232222347220e47139a502ee43a9cbdf` | Baseline contract, read from local `main`. |
| BFF candidate | `d93455b6533bc017ab6bc42b0b585b804e1e96a1`, 5 November | High compatibility risk: authorization identities and tile semantics change. |
| Base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a`, clean `main` | Conditional launch risk and confirmed admin management gaps. |
| Ratan container | Filesystem copy; [file hashes](evidence/frontend-entitlement-impact-20261105/ratan-container.json) | Confirmed local permission failures. Independent application revision is unknown. |
| Captures | [SHA-256 bindings](evidence/frontend-entitlement-impact-20261105/capture-summary.json) | One account and unspecified environment cannot establish enterprise coverage. |

All accountable implementation owners remain unknown.
The BFF review covers frontend-facing migration paths, not every change among the 54 changed paths.

## User impact

[FE-01](#fe-01-replace-identity-specific-shared-permission-dispatch) can disable granted business controls through a shared helper.
[FE-02](#fe-02-reconcile-roles-independently-from-action-grants) can change saved-content queries when role-dependent features are enabled.
[FE-03](#fe-03-align-portal-tile-admission-with-the-ces-contract) can make launch paths disagree for supported configuration boundaries.
[FE-04](#fe-04-add-ces-tile-configuration-and-audit-controls) prevents frontend management and review of CES routing.
Browser impact, frequency, forced logout, and deployed reachability remain unverified.
These observations establish no automatic production release hold.

## System impact

The BFF normalizes CES applications, features, and actions into the existing entity/subject/action envelope.
[Mapper evidence](evidence/frontend-entitlement-impact-20261105/bff-contract.json) binds old and new source hashes.
Migration modes permit mixed providers. Frontend permission resolution must preserve selected scope.
The [resolver boundary case](06-test-cases.md#tc-fe-ces-006) addresses duplicate rows and unrelated applications.
Static consumer inspection does not establish the deployed shared-module version or effective migration mode.

## Options and consequences

| Option | Consequence | Assessment |
| --- | --- | --- |
| Replace only the string `X_RATANONE`. | Can restore sample action lookup, but leaves roles, mixed scope, types, and admin gaps. | Insufficient migration scope. |
| Add a shared scoped resolver and explicit contracts. | Preserves both providers and separates tile, action, role, and data responsibilities. | Recommended design. |
| Add direct CES calls in each frontend. | Duplicates BFF responsibilities and adds unsupported interfaces. | No source-backed need. |

## Proposed acceptance and validation

Approved frontend AC denominator: **UNKNOWN**. Six proposed case definitions do not establish approved requirements.

### AC-to-test mapping

| Available intent or proposed boundary | Canonical cases | Assertion and execution state |
| --- | --- | --- |
| Preserve scoped permission meaning. | [TC-FE-CES-001](06-test-cases.md#tc-fe-ces-001), [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006) | Original-module failure retained; cross-app boundary `NOT_RUN`. |
| Preserve reviewed tile admission. | [TC-FE-CES-002](06-test-cases.md#tc-fe-ces-002), [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003) | Capture predicates match; changed-feature integration `NOT_RUN`. |
| Manage CES metadata; preserve role attribution. | [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004), [TC-FE-CES-005](06-test-cases.md#tc-fe-ces-005) | Admin assertions unavailable; absent-role observation retained. |

### AC-to-code-change mapping

| Denominator | Mapping | Conformance limit |
| --- | --- | --- |
| Approved frontend AC inventory: unknown. | [Proposed changes](#proposed-change) identify exact current code and required effects. | No frontend implementation change exists. No conformance percentage applies. |
| Relevant existing BFF contract. | [BFF source and assertion map](evidence/frontend-entitlement-impact-20261105/bff-contract.json). | Implementation evidence does not approve blank-feature or role policy. |

### Code-change-to-test mapping

| Change population | Direct assertion evidence | Result |
| --- | --- | --- |
| New frontend application changes: 0. | None. | Empty denominator; not 100% coverage. |
| Inspected BFF migration interfaces. | Mapper, application-name, blank-feature, and tile-create assertions in [BFF evidence](evidence/frontend-entitlement-impact-20261105/bff-contract.json). | Assertions inspected; BFF suite `NOT_RUN`. |
| Required unchanged base paths. | [Nine existing tests](evidence/frontend-entitlement-impact-20261105/mfe-base-tests.json). | All pass. No captured CES assertion chain or complete-suite result. |

Definition, assertion, conformance, and passing execution remain separate.
Before acceptance, run equivalent EMS2/CES cases through login, renewal, direct launch, workspace restoration, and actual business controls.
Include denied actions, mixed providers, multiple applications, role-dependent APIs, and admin maker/checker round trips.

## Implementation and release proposal

Implement the shared resolver and response models first.
Add admin routing controls and unify the reviewed tile admission contract.
Resolve named roles before changing role-dependent APIs or restrictions.
Update telemetry after the role/profile contract is known.
Verify the actual deployed import map and consuming microfrontends.
No implementation estimate, release date, or deployment authorization is supplied.

## Sources and evidence limits

- [Preserved request](evidence/frontend-entitlement-impact-20261105/user-input.md#exact-user-input).
- [Original database dump](<ces migration/application_tile_1105.csv>) and [login capture](<ces migration/login-response.json>).
- [Capture hashes and derived facts](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
- [BFF contract and comparison identities](evidence/frontend-entitlement-impact-20261105/bff-contract.json).
- [Base source and assertions](evidence/frontend-entitlement-impact-20261105/mfe-base.json).
- [Container source, probe, and classifications](evidence/frontend-entitlement-impact-20261105/ratan-container.json).

Original supplied captures remain local and untracked. No token-bearing payload is added to this analysis commit.
Fresh checkouts need those supplied files to reproduce capture-dependent probes.
The probe substitutes the hooks store and executes no browser, backend API, or live authorization service.
Missing database tiles can reflect assignment or activity. They do not establish an entitlement defect.
No new business rule is inferred from the capture. Existing knowledge meaning remains unchanged.

## Unknowns and blockers

| Remaining dependency | Consequence | Owner and next action |
| --- | --- | --- |
| Named-role/profile contract and multiple-role rules. | Role-dependent implementation acceptance remains blocked. | unknown; obtain assigned-role evidence and reviewed mappings. |
| Blank-feature admission versus existing configured-entity intent. | That access-policy decision remains unresolved. | unknown; reconcile policy before expanding admission. |
| Target builds, migration mode, import maps, and runtime evidence. | Deployed impact and full migration acceptance remain unverified. | unknown; bind actual UAT execution to exact artifacts. |

## Stage evidence and completion

Source inspection and compact capture analysis are complete within the declared scope.
The [container probe](evidence/frontend-entitlement-impact-20261105/ratan-container.json) confirms a local compatibility failure.
Its passing diagnostic assertions describe failing required permission behavior.
The [base test result](evidence/frontend-entitlement-impact-20261105/mfe-base-tests.json) records nine passing existing tests.
[Document and integrity checks](evidence/frontend-entitlement-impact-20261105/validation.json) record final automated validation separately.
Browser execution and complete applicable application suites remain `NOT_RUN`.

## Requested decision and actual disposition

Requested output: identify required changes in both frontends from the BFF migration and supplied captures.
Actual disposition: complete analysis with source-backed proposals and conditional contract dependencies.
Application implementation: unchanged. Intent review: existing intent plus explicitly proposed compatibility design.
Execution: controlled helper probe, source-predicate analysis, and nine existing base tests only.
Business acceptance, knowledge publication, and release authorization: pending and outside this analysis.
