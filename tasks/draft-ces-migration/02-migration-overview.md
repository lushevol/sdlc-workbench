# RATAN EMS2 → CES Migration Overview

**Status date:** 30 October 2026<br>
**Audience:** Settlement, Trade Control, FlowZero, and integration owners<br>
**UAT sign-off target:** 6 November 2026<br>
**Production go-live target:** 28 November 2026

> **Critical status:** Local Auth Service and Single UI BFF changes are present. UAT, production provisioning, and live login behavior remain unverified. The current Auth Service still has an EMS2 JWT data-role dependency. The zero-EMS2 exit condition is not met.

## Target state

- All RATAN user, tile, data, and service authorization uses CES.
- CES application: `RATAN_ENTITLEMENT_RULE` (`itam_id` `51358`).
- `RATAN_FUNC` and `RATAN_DATA_ENTITLEMENT` are CES features under this application.
- Blotter features, including `RATAN_STRATEGIC_CASHFLOW_BLOTTER` and `RATAN_TRADE_BLOTTER`, use CES feature/action pairs.
- No direct or indirect EMS2 runtime dependency remains after cutover.
- The Single UI BFF and MFBase keep their existing external response and storage contracts where possible.

## Latest readiness

| Area | Latest status | Required action before sign-off |
|---|---|---|
| Auth Service functional authorization | **Implemented locally** with CES primary, dual-read, and CES-only modes. | Verify the deployed revision and equivalent user permissions. |
| Auth Service data authorization | **Open dependency.** JWT data-role lookup still reads EMS2 in the inspected source. | Replace or approve the remaining data-role path. |
| Single UI BFF | **Implemented locally.** Login routes and response envelope remain stable. CES-backed entities may omit EMS2 numeric IDs and role provenance. | Verify login, tile visibility, action checks, and role-dependent consumers. |
| MFBase | **Compatibility preserved.** Storage keys remain unchanged. CES raw IDs, profiles, and policies are not stored. | Test consumers that require numeric IDs or role names. |
| CES feature consolidation | **Defined.** `RATAN_FUNC` and `RATAN_DATA_ENTITLEMENT` are features under `RATAN_ENTITLEMENT_RULE`. | Confirm feature/action assignments for users and service accounts. |
| User account synchronization | **Reported complete** for UAT and production, with incremental synchronization. | Confirm current CES synchronization and representative assignments. |
| Service accounts | **Production status unverified.** CES-only service authorization is the target. | Verify every caller, account, permission, and denied-call case. |
| Tile migration | **Per-tile switching available locally.** Final CES selection for every tile is unverified. | Inventory all tiles and set each final source to CES. |
| Live verification | **Not run.** No deployed browser or real API evidence is available. | Execute DEV smoke tests, UAT regression, and service tests. |

## Critical milestones

Dates below are the current working targets. The 13 November, 27 November, and 4 December dates need owner confirmation.

| Date | Milestone | Exit evidence |
|---|---|---|
| **30 October** | Freeze the dependency inventory, CES mappings, test users, service accounts, and owners. | Approved inventory and test plan. |
| **6 November** | Complete DEV verification, UAT regression, service integration checks, and performance comparison. | Settlement, Trade Control, FlowZero, and integration sign-offs. |
| **13 November** | Proposed CES production provisioning target. | CES CR confirms accounts, features, profiles, and assignments. |
| **27 November** | Complete CR approvals and production go/no-go review. | Approved release decision, rollback plan, and monitoring plan. |
| **28 November** | Production cutover to CES. | All tiles and service calls use CES; smoke checks pass. |
| **4 December** | Proposed cleanup and handover. | EMS2 dependency report is closed; monitoring and support ownership is recorded. |

## Required work before UAT sign-off

1. Confirm the application, feature, action, role, and data mappings for each migrated tile.
2. Replace or formally resolve the Auth Service EMS2 data-role read.
3. Bind the deployed Auth SDK, Auth Service, and BFF revisions to the release inventory.
4. Verify login, tile visibility, launch, business actions, data filters, and denied cases.
5. Verify service-account calls through the central Auth Service.
6. Record test results, defects, owners, and business sign-offs.

## External dependencies

External systems call RATAN-exposed APIs using their assigned service accounts. Integration owners must confirm CES permissions and verify each dependency.

### RATAN APIs called by external systems

Replace the placeholders below with confirmed details. Add rows for every additional API and external caller.

| API reference | RATAN API / purpose | HTTP method and path | External calling system | Service account | Integration POC | Verification status |
|---|---|---|---|---|---|---|
| API-01 | TBD | `TBD /<RATAN-API-01>` | TBD | TBD | TBD | Not run |
| API-02 | TBD | `TBD /<RATAN-API-02>` | TBD | TBD | TBD | Not run |
| API-03 | TBD | `TBD /<RATAN-API-03>` | TBD | TBD | TBD | Not run |
| API-04 | TBD | `TBD /<RATAN-API-04>` | TBD | TBD | TBD | Not run |

### Test-user verification results

All business testers and integration testers must record their results here before the **6 November UAT sign-off**.
Use one row per test account, API or workflow, environment, and run. Add rows for every tester and service account.
Record allowed and denied access separately. Use status **Not run**, **Pass**, **Fail**, or **Blocked**.

| Test user / service account | Team / external system | Environment | API reference / workflow | Expected result | Actual result | Status | Verified by / date | Defect / follow-up |
|---|---|---|---|---|---|---|---|---|
| TBD | Settlement | TBD | TBD | TBD | — | Not run | — | — |
| TBD | Trade Control | TBD | TBD | TBD | — | Not run | — | — |
| TBD | FlowZero | TBD | TBD | TBD | — | Not run | — | — |
| TBD | TBD external system | TBD | API-01 | TBD | — | Not run | — | — |
| TBD | TBD external system | TBD | API-02 | TBD | — | Not run | — | — |
| TBD | TBD external system | TBD | API-03 | TBD | — | Not run | — | — |
| TBD | TBD external system | TBD | API-04 | TBD | — | Not run | — | — |

## Responsibilities

| Owner group | Responsibility |
|---|---|
| Settlement, Trade Control, FlowZero | Provide test users, execute business regression, and sign off UAT. |
| Integration owners | Identify service callers, verify allowed and denied calls, and sign off service readiness. |
| Portal and Auth owners | Complete mappings, remove the remaining EMS2 path, and verify deployed revisions. |
| CES team | Confirm production provisioning, profiles, assignments, and CR timing. |
| Release owner | Approve go/no-go, rollback, monitoring, and final cutover. |

## Exit criteria

- All critical user workflows and permissions pass regression.
- All migrated tiles use CES in the final release configuration.
- All internal, upstream, and downstream service calls use CES authorization.
- No unresolved critical or high-severity migration defect remains.
- The Auth Service data-role dependency and all other EMS2 paths are removed or formally accepted with an approved exception.
- Settlement, Trade Control, FlowZero, integration owners, and the release owner provide sign-off.

Detailed field mappings and JSON samples are in [EMS2_to_CES_Before_and_After.md](EMS2_to_CES_Before_and_After.md). Source findings and evidence limits are in the [migration evidence index](evidence/index.md).
