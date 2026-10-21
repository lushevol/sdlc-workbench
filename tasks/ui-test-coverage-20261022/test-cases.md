---
artifact_kind: test-case
id: TEST-UI-COVERAGE-20261022
version: 1
status: draft
owner: unknown
source_refs: [UI-SRC-USER, UI-SRC-MFE, UI-SRC-BFF, UI-SRC-KNOWLEDGE]
related_ids: [UI-COVERAGE-20261022, UI-COVERAGE-AC-001, UI-COVERAGE-AC-002, UI-COVERAGE-AC-003]
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

# Single UI user-view test cases

> **Critical conclusions: Review required before business acceptance**
>
> **These cases define coverage. They establish no passing execution.**
> Action: Bind fixtures, assertions, and target versions before execution. Consequence: Business verification and release approval remain blocked.
> Owner: unknown. Evidence: [execution binding](#execution-binding) and [source manifest](evidence/source-manifest.json).
>
> **Draft sources contain conflicting portal-entry rules.**
> Action: Select the applicable rule before accepting entitlement cases. Consequence: Conflicting expectations cannot both establish acceptance.
> Owner: unknown. Evidence: [knowledge decisions](evidence/knowledge-inspection.md#open-rule-decisions).

## Objective and traceability

This catalog contains 521 independently identified UI scenarios.
Each case has definition version 1 and execution status `NOT_RUN`.
This file is the single definition source for this task.
The [intake](intake.md#acceptance-criteria) defines catalog-quality criteria, rather than new product policies.
Each case maps its assertions to those criteria and its linked behavior sources.

| Expectation basis | Meaning | Acceptance boundary |
| --- | --- | --- |
| IMPLEMENTATION | Predicts the inspected source behavior. | Characterization requires execution. It does not establish approved intent. |
| DOCUMENTED | A retained domain source states the expectation. | Sources remain draft. Applicability and human review remain open. |
| PROPOSED | A risk or boundary motivates the assertion. | The owner must approve the expected behavior before business acceptance. |

Priorities are proposed test-design priorities.
P0 covers entry, credentials, permission boundaries, or critical session continuity.
P1 covers principal workflows, administration, state integrity, and recovery.
P2 covers additional usability, compatibility, and presentation probes.
These priorities do not establish release severity.

## Preconditions and fixtures

Use isolated, synthetic test data and a disposable BFF database or controlled BFF responses.
Run the real shell and record each substituted dependency.
Use tenant fixtures only where the case requires them.
A tenant marker is visible text from a controlled container. It does not establish an existing business screen.

| Fixture | Definition |
| --- | --- |
| UI-USER-01 | Authenticated test user with the case-specific tile entitlements. |
| Admin A / B / C | admin-a, admin-b, admin-c. Entity FMO PORTAL ADMIN; owner role FMO_ADMIN. Use distinct maker/checker users. |
| Admin S | Synthetic administration user with entity FMO PORTAL ADMIN and role SUPER_USER. |
| User A / user-a | Synthetic session-test user. Credentials and token state are stated in each case. |
| USER-A | Synthetic non-admin user. fullName and userId equal USER-A. Access remains valid during non-session cases. |
| ADMIN-A | Synthetic administration user with FMO PORTAL ADMIN role TEST_OWNER. Isolate each case. |
| Alice | Synthetic domain-policy user. Entity, subject, and action assignments are case-specific. |
| T-GLOBAL | Tile title Test Tile, subtitle Demo, entry Global, container @fm/test_container, module /test, tile /tile-global. |
| T-ID | Same tile title and subtitle. Entry Indonesia and tile route /tile-id distinguish it. |
| W1 | Workspace labelled Workspace 1. Cases override its initial container state. |
| W2 / W3 | Distinct workspaces with visible markers Panel Two and Panel Three. |
| WS-A | Session fixture workspace. Record its visible state marker before the session action. |
| T1 / T2 | Distinct disposable tile records for shared-form timing probes. |
| T-TRADE | Synthetic tile requiring entity E-TRADE and subject S-VIEW. |
| T-CASH | Synthetic tile requiring entity E-CASH and subject S-VIEW. |
| T-REPORT | Synthetic tile declaring entities E-RR-A and E-RR-B, with an empty subject. |
| Source A / Target B | Controlled tenant fixtures for intents and context. Their contracts require confirmation before execution. |
| T-CACHE | Controlled tenant build with visible base, container, and tile version markers. |
| Counter | Controlled container button with an adjacent numeric value. Use it to detect remounting. |
| FixturePass1! | Synthetic password. It is not a real system credential. |

Each case starts from fresh browser storage unless its steps require existing state.
Keep account and record fixtures separate between cases.
Grant administration roles only in the relevant isolated case.
Record locale, time zone, browser version, viewport, effective lifetimes, and clock mode before future execution.
Timing inputs define probes. They do not establish deployed session policy.
Use a controlled clock only when the case declares it.
Real sleep, browser suspension, and hidden-tab timers require separate observations.

### UI fixture extension

Each screen uses its own isolated fixture records.

Use an isolated local browser profile and a disposable test BFF database or controlled endpoint responses.

Authenticate fixture user UI-USER-01. Keep access valid throughout each non-session case.

Fixture tile T-GLOBAL uses @fm/test_container, module /test, tile /tile-global, title Test Tile, subtitle Demo, and entryName Global.

Fixture tile T-ID uses the same title and subtitle, tile /tile-id, and entryName Indonesia.

The controlled test container renders its tile identifier and parameters as visible text. It contains a Counter control for state checks.

Workspace W1 is labelled Workspace 1. W2 and W3 contain distinct visible markers Panel Two and Panel Three.

Use real shell controls. Endpoint and test-container substitutions must be recorded before future execution.

T-GLOBAL and T-ID declare entity TEST_ENTITY and subject TEST_SUBJECT. UI-USER-01 holds TEST_ENTITY with subject TEST_SUBJECT.

UI-ADMIN-01 has user.id UI-ADMIN-01 and entity FMO PORTAL ADMIN with roleName TEST_OWNER. Controlled endpoint fixtures permit the named operation.

UI-SUPER-01 has user.id UI-SUPER-01 and entity FMO PORTAL ADMIN with roleName SUPER_USER.

Category record 101 has label Fixture Category, orderNo 7, owner TEST_OWNER, active false, and applicationCategoryId 101.

Import Map record 101 has keyName @fm/test, path https://assets.example.test/v1.js, owner TEST_OWNER, active false, and importMapId 101.

Tile record 101 has title Fixture Tile, subtitle Demo, module /test, tile /test-entry, entryName Global, owner TEST_OWNER, and active false.

Tile record 101 references applicationCategoryId 81 labelled Fixture Category and importMapId 71 with keyName @fm/test.

Tile record 101 has imageDarkTheme darkIcons/icon01.svg, imageLightTheme lightIcons/icon01.svg, template false, and emailSupport support@example.test.

Unless the case overrides values, admin timestamps are 2026-10-22T00:05:00Z and actor fields identify UI-ADMIN-01.

Admin create/update cases use controlled complete success responses. They do not prove BFF validation or permissions.

All cases inherit this cleanup: restore fixtures, clocks, handlers, browser storage, and disposable records.
Close the case browser context after evidence is saved.
No live external service access is required to review this catalog.

## Coverage navigation

| Coverage group | Cases | First case |
| --- | --- | --- |
| [Login](#group-login) | 28 | [AUTH-001](#auth-001) |
| [SSO](#group-sso) | 8 | [AUTH-029](#auth-029) |
| [Identity](#group-identity) | 6 | [AUTH-037](#auth-037) |
| [Refresh](#group-refresh) | 26 | [AUTH-043](#auth-043) |
| [Activity](#group-activity) | 7 | [AUTH-069](#auth-069) |
| [Expiry](#group-expiry) | 18 | [AUTH-076](#auth-076) |
| [Suspension](#group-suspension) | 8 | [AUTH-085](#auth-085) |
| [Logout](#group-logout) | 13 | [AUTH-102](#auth-102) |
| [Multi-tab](#group-multi-tab) | 3 | [AUTH-115](#auth-115) |
| [BFF boundary](#group-bff-boundary) | 22 | [AUTH-118](#auth-118) |
| [SSO security](#group-sso-security) | 5 | [AUTH-140](#auth-140) |
| [Workspaces](#group-workspaces) | 28 | [UI-SHL-001](#ui-shl-001) |
| [Tile catalog](#group-tile-catalog) | 20 | [UI-CAT-001](#ui-cat-001) |
| [Module composition](#group-module-composition) | 15 | [UI-MFE-001](#ui-mfe-001) |
| [Preferences and profile](#group-preferences-and-profile) | 9 | [UI-PREF-001](#ui-pref-001) |
| [Administration: Category](#group-administration-category) | 14 | [UI-ADM-CAT-001](#ui-adm-cat-001) |
| [Administration: Import Map](#group-administration-import-map) | 14 | [UI-ADM-MAP-001](#ui-adm-map-001) |
| [Administration: Tile](#group-administration-tile) | 14 | [UI-ADM-TIL-001](#ui-adm-til-001) |
| [Administration fields](#group-administration-fields) | 8 | [UI-ADM-FLD-001](#ui-adm-fld-001) |
| [Tile administration filters](#group-tile-administration-filters) | 15 | [UI-ADM-SEL-001](#ui-adm-sel-001) |
| [Administration grids and audits](#group-administration-grids-and-audits) | 9 | [UI-ADM-GRD-001](#ui-adm-grd-001) |
| [Proposed source-risk coverage](#group-proposed-source-risk-coverage) | 10 | [UI-RISK-001](#ui-risk-001) |
| [Entitlement policy](#group-entitlement-policy) | 8 | [KNOW-001](#know-001) |
| [Entitlement policy conflict](#group-entitlement-policy-conflict) | 3 | [KNOW-007](#know-007) |
| [Entitlement policy boundary](#group-entitlement-policy-boundary) | 2 | [KNOW-010](#know-010) |
| [Tenant permission boundary](#group-tenant-permission-boundary) | 4 | [KNOW-011](#know-011) |
| [Interoperability intent and context](#group-interoperability-intent-and-context) | 17 | [KNOW-018](#know-018) |
| [Conditional OpenFin POC](#group-conditional-openfin-poc) | 6 | [KNOW-033](#know-033) |
| [Documented cache and version lifecycle](#group-documented-cache-and-version-lifecycle) | 12 | [KNOW-041](#know-041) |
| [Accessibility](#group-accessibility) | 22 | [UX-001](#ux-001) |
| [Responsive layout](#group-responsive-layout) | 14 | [UX-023](#ux-023) |
| [Security and text](#group-security-and-text) | 11 | [UX-037](#ux-037) |
| [Data resilience](#group-data-resilience) | 3 | [UX-048](#ux-048) |
| [Form timing](#group-form-timing) | 8 | [UX-051](#ux-051) |
| [Browser compatibility](#group-browser-compatibility) | 4 | [UX-059](#ux-059) |
| [Dependency resilience](#group-dependency-resilience) | 2 | [UX-063](#ux-063) |
| [Grid and regional boundaries](#group-grid-and-regional-boundaries) | 8 | [UX-065](#ux-065) |
| [Admin validation](#group-admin-validation) | 26 | [BFF-ADM-001](#bff-adm-001) |
| [Admin uniqueness](#group-admin-uniqueness) | 4 | [BFF-ADM-027](#bff-adm-027) |
| [Admin storage boundary](#group-admin-storage-boundary) | 16 | [BFF-ADM-031](#bff-adm-031) |
| [Admin persistence](#group-admin-persistence) | 12 | [BFF-ADM-047](#bff-adm-047) |
| [Admin authority](#group-admin-authority) | 15 | [BFF-ADM-059](#bff-adm-059) |
| [Admin references](#group-admin-references) | 9 | [BFF-ADM-074](#bff-adm-074) |
| [Admin concurrency](#group-admin-concurrency) | 9 | [BFF-ADM-083](#bff-adm-083) |
| [Admin URL security](#group-admin-url-security) | 5 | [BFF-ADM-092](#bff-adm-092) |
| [Admin audit fidelity](#group-admin-audit-fidelity) | 1 | [BFF-ADM-097](#bff-adm-097) |

Boundary values and malformed inputs appear within the relevant cases.
Apply each applicable principal journey to the declared browser, role, and network variants.
The [coverage inventory](evidence/case-inventory.json) contains IDs, counts, and execution states.
It contains no second case definition.

## Procedure and assertions

Read the source and fixture limits before each case.
Perform each listed action in order.
A `Then` assertion states an intended observation. It is not an actual result.
Source links identify the behavior basis. Execution links remain separate.
`Create`, `Update`, `Verified`, and `Deactivate` are the detail-form action labels.
`Verify` is the row action that opens verification.
Refresh the grid before checking persisted values or inactive status after a rejected action.
For persistence probes, save the received request payload. Do not force expected response values.
For security probes, record UI-origin request substitutions where the UI cannot supply the invalid value.

### Group: Login

<a id="group-login"></a>

#### AUTH-001

**Render the local sign-in form**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!

Behavior basis: [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-001 @IMPLEMENTATION
Feature: Login
  Scenario: Render the local sign-in form
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!
    When User A opens the portal
    Then the page displays Username, Password, Sign In, and Sign In With SSO
    And the password input masks entered characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-002

**Render credential login in DEV**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser uses the DEV environment fixture with empty storage

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-002 @IMPLEMENTATION
Feature: Login
  Scenario: Render credential login in DEV
    Given User A, an entitled portal user uses an isolated browser context
    And the browser uses the DEV environment fixture with empty storage
    When User A opens the portal
    Then the login page displays Username, Password, and Sign In
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-003

**Render credential login in SIT**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser uses the SIT environment fixture with empty storage

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-003 @IMPLEMENTATION
Feature: Login
  Scenario: Render credential login in SIT
    Given User A, an entitled portal user uses an isolated browser context
    And the browser uses the SIT environment fixture with empty storage
    When User A opens the portal
    Then the login page displays Username, Password, and Sign In
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-004

**Render credential login in UAT**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser uses the UAT environment fixture with empty storage

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-004 @IMPLEMENTATION
Feature: Login
  Scenario: Render credential login in UAT
    Given User A, an entitled portal user uses an isolated browser context
    And the browser uses the UAT environment fixture with empty storage
    When User A opens the portal
    Then the login page displays Username, Password, and Sign In
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-005

**Render credential login in PRE-PROD**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser uses the PRE-PROD environment fixture with empty storage

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-005 @IMPLEMENTATION
Feature: Login
  Scenario: Render credential login in PRE-PROD
    Given User A, an entitled portal user uses an isolated browser context
    And the browser uses the PRE-PROD environment fixture with empty storage
    When User A opens the portal
    Then the login page displays Username, Password, and Sign In
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-006

**Hide credential login by default in PROD**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser uses the PROD environment fixture without show_normal_login

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-006 @IMPLEMENTATION
Feature: Login
  Scenario: Hide credential login by default in PROD
    Given User A, an entitled portal user uses an isolated browser context
    And the browser uses the PROD environment fixture without show_normal_login
    When User A opens the portal
    Then Username, Password, and Sign In are absent
    And Sign In With SSO remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-007

**Enable the PROD credential form with Y**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=Y

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-007 @IMPLEMENTATION
Feature: Login
  Scenario: Enable the PROD credential form with Y
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=Y
    When User A opens the portal
    Then Username, Password, and Sign In are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-008

**Enable the PROD credential form with y**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=y

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-008 @IMPLEMENTATION
Feature: Login
  Scenario: Enable the PROD credential form with y
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=y
    When User A opens the portal
    Then Username, Password, and Sign In are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-009

**Keep PROD credentials hidden for parameter N**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=N

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-009 @IMPLEMENTATION
Feature: Login
  Scenario: Keep PROD credentials hidden for parameter N
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=N
    When User A opens the portal
    Then only Sign In With SSO is available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-010

**Keep PROD credentials hidden for parameter true**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=true

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-010 @IMPLEMENTATION
Feature: Login
  Scenario: Keep PROD credentials hidden for parameter true
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=true
    When User A opens the portal
    Then only Sign In With SSO is available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-011

**Keep PROD credentials hidden for parameter 1**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=1

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-011 @IMPLEMENTATION
Feature: Login
  Scenario: Keep PROD credentials hidden for parameter 1
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=1
    When User A opens the portal
    Then only Sign In With SSO is available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-012

**Keep PROD credentials hidden for parameter empty**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the PROD fixture URL contains ?show_normal_login=

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-012 @IMPLEMENTATION
Feature: Login
  Scenario: Keep PROD credentials hidden for parameter empty
    Given User A, an entitled portal user uses an isolated browser context
    And the PROD fixture URL contains ?show_normal_login=
    When User A opens the portal
    Then only Sign In With SSO is available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-013

**Prevent submission with missing username**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL form contains username '' and password 'FixturePass1!'

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-013 @IMPLEMENTATION
Feature: Login
  Scenario: Prevent submission with missing username
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL form contains username '' and password 'FixturePass1!'
    When User A selects Sign In
    Then the login page remains visible
    And no login request is sent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-014

**Prevent submission with missing password**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL form contains username 'user-a' and password ''

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-014 @IMPLEMENTATION
Feature: Login
  Scenario: Prevent submission with missing password
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL form contains username 'user-a' and password ''
    When User A selects Sign In
    Then the login page remains visible
    And no login request is sent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-015

**Prevent submission with missing both**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL form contains username '' and password ''

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-015 @IMPLEMENTATION
Feature: Login
  Scenario: Prevent submission with missing both
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL form contains username '' and password ''
    When User A selects Sign In
    Then the login page remains visible
    And no login request is sent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-016

**Submit valid credentials once**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>); [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>)

```gherkin
@AUTH-016 @IMPLEMENTATION
Feature: Login
  Scenario: Submit valid credentials once
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!
    When User A enters user-a / FixturePass1!
    And User A selects Sign In
    Then Home workspace WS-A becomes visible after the successful fixture response
    And the login form is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-017

**Submit with Enter in Username**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both inputs contain valid credentials and focus is in Username

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-017 @IMPLEMENTATION
Feature: Login
  Scenario: Submit with Enter in Username
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both inputs contain valid credentials and focus is in Username
    When User A presses Enter
    Then Home workspace WS-A becomes visible after the successful fixture response
    And one credential login request is observed
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-018

**Submit with Enter in Password**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both inputs contain valid credentials and focus is in Password

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-018 @IMPLEMENTATION
Feature: Login
  Scenario: Submit with Enter in Password
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both inputs contain valid credentials and focus is in Password
    When User A presses Enter
    Then Home workspace WS-A becomes visible after the successful fixture response
    And one credential login request is observed
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-019

**Trim username boundary whitespace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; username is entered as "  user-a  "

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-019 @IMPLEMENTATION
Feature: Login
  Scenario: Trim username boundary whitespace
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; username is entered as "  user-a  "
    When User A submits valid credentials
    Then the login request username equals user-a
    And Home workspace WS-A becomes visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-020

**Characterize password whitespace trimming**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; password is entered as "  FixturePass1!  "

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-020 @IMPLEMENTATION
Feature: Login
  Scenario: Characterize password whitespace trimming
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; password is entered as "  FixturePass1!  "
    When User A selects Sign In
    Then the request password equals FixturePass1!
    And Home workspace WS-A becomes visible after the accepting fixture response
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Current source trims password whitespace. The intended password policy requires owner confirmation.

#### AUTH-021

**Prevent submission of whitespace-only credentials**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both form inputs contain three spaces and the service rejects empty credentials

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-021 @IMPLEMENTATION
Feature: Login
  Scenario: Prevent submission of whitespace-only credentials
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; both form inputs contain three spaces and the service rejects empty credentials
    When User A selects Sign In
    Then the login form remains visible
    And no credential login request is sent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The current controlled inputs trim whitespace into empty strings. Business password whitespace policy remains unproved.

#### AUTH-022

**Show a generic rejected-login message**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login service returns AuthenticationException for invalid credentials

Behavior basis: [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-022 @IMPLEMENTATION
Feature: Login
  Scenario: Show a generic rejected-login message
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login service returns AuthenticationException for invalid credentials
    When User A enters user-a / WrongPass
    And User A selects Sign In
    Then the login form remains visible
    And the page displays Invalid username and password combination or SSO service is unavailable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-023

**Recover after an invalid password**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the first submission receives AuthenticationException and the second receives valid login data

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-023 @IMPLEMENTATION
Feature: Login
  Scenario: Recover after an invalid password
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the first submission receives AuthenticationException and the second receives valid login data
    When User A submits WrongPass
    And User A replaces the password with FixturePass1!
    And User A selects Sign In
    Then the previous error is cleared on the second attempt
    And Home workspace WS-A becomes visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-024

**Disable the sign-in controls during a pending request**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login response is held pending

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-024 @IMPLEMENTATION
Feature: Login
  Scenario: Disable the sign-in controls during a pending request
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login response is held pending
    When User A submits credentials
    Then Sign In displays a spinner and is disabled
    And Sign In With SSO is disabled while loading is true
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-025

**Prevent duplicate login from rapid repeated input**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login response is held pending

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>)

```gherkin
@AUTH-025 @PROPOSED
Feature: Login
  Scenario: Prevent duplicate login from rapid repeated input
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login response is held pending
    When User A presses Enter repeatedly and selects Sign In rapidly
    Then at most one successful authentication transition occurs
    And the user sees one Home page and no stale login error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The button disables during loading. Keyboard handlers have no explicit loading guard; request deduplication is not established.

#### AUTH-026

**Recover sign-in controls after Network Error**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with Network Error

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-099:6](<../../repos/ui/mfe-base/src/hooks/service/config.ts#L6>)

```gherkin
@AUTH-026 @IMPLEMENTATION
Feature: Login
  Scenario: Recover sign-in controls after Network Error
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with Network Error
    When User A selects Sign In
    Then the login page remains visible
    And the sign-in spinner stops and Sign In is enabled
    And a service error is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-027

**Recover sign-in controls after 60000-millisecond timeout**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with 60000-millisecond timeout

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-099:6](<../../repos/ui/mfe-base/src/hooks/service/config.ts#L6>)

```gherkin
@AUTH-027 @IMPLEMENTATION
Feature: Login
  Scenario: Recover sign-in controls after 60000-millisecond timeout
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with 60000-millisecond timeout
    When User A selects Sign In
    Then the login page remains visible
    And the sign-in spinner stops and Sign In is enabled
    And a service error is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-028

**Recover sign-in controls after HTTP 503 with no response body**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with HTTP 503 with no response body

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-099:6](<../../repos/ui/mfe-base/src/hooks/service/config.ts#L6>)

```gherkin
@AUTH-028 @IMPLEMENTATION
Feature: Login
  Scenario: Recover sign-in controls after HTTP 503 with no response body
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; the login request fails with HTTP 503 with no response body
    When User A selects Sign In
    Then the login page remains visible
    And the sign-in spinner stops and Sign In is enabled
    And a service error is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: SSO

<a id="group-sso"></a>

#### AUTH-029

**Follow the environment SSO destination**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!

Behavior basis: [UI-SRC-116:43](<../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43>); [UI-SRC-118:134](<../../repos/ui/mfe-base/src/utils/common.ts#L134>)

```gherkin
@AUTH-029 @IMPLEMENTATION
Feature: SSO
  Scenario: Follow the environment SSO destination
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!
    When User A selects Sign In With SSO
    Then the browser navigates to the SSO URL returned by the environment configuration
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-030

**Exchange an Entra callback code**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the login URL contains ?code=ENTRA-CODE-A without iss or client_id; Entra accepts the fixture code

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-018:202](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L202>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-030 @IMPLEMENTATION
Feature: SSO
  Scenario: Exchange an Entra callback code
    Given User A, an entitled portal user uses an isolated browser context
    And the login URL contains ?code=ENTRA-CODE-A without iss or client_id; Entra accepts the fixture code
    When User A opens the callback URL
    Then Home workspace WS-A becomes visible
    And the exchange uses /auth/v3/sso/login
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-031

**Exchange a legacy MFA callback code**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the login URL contains code=MFA-CODE-A, iss=ISSUER-A, and client_id=CLIENT-A; MFA accepts the fixture code

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-031 @IMPLEMENTATION
Feature: SSO
  Scenario: Exchange a legacy MFA callback code
    Given User A, an entitled portal user uses an isolated browser context
    And the login URL contains code=MFA-CODE-A, iss=ISSUER-A, and client_id=CLIENT-A; MFA accepts the fixture code
    When User A opens the callback URL
    Then Home workspace WS-A becomes visible
    And the exchange uses /auth/v2/sso/login
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-032

**Route callback with only iss=ISSUER-A**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the login URL contains code=MFA-CODE-A and iss=ISSUER-A; the legacy endpoint accepts the fixture

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>)

```gherkin
@AUTH-032 @IMPLEMENTATION
Feature: SSO
  Scenario: Route callback with only iss=ISSUER-A
    Given User A, an entitled portal user uses an isolated browser context
    And the login URL contains code=MFA-CODE-A and iss=ISSUER-A; the legacy endpoint accepts the fixture
    When User A opens the callback URL
    Then the exchange uses /auth/v2/sso/login
    And Home workspace WS-A becomes visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-033

**Route callback with only client_id=CLIENT-A**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the login URL contains code=MFA-CODE-A and client_id=CLIENT-A; the legacy endpoint accepts the fixture

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>)

```gherkin
@AUTH-033 @IMPLEMENTATION
Feature: SSO
  Scenario: Route callback with only client_id=CLIENT-A
    Given User A, an entitled portal user uses an isolated browser context
    And the login URL contains code=MFA-CODE-A and client_id=CLIENT-A; the legacy endpoint accepts the fixture
    When User A opens the callback URL
    Then the exchange uses /auth/v2/sso/login
    And Home workspace WS-A becomes visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-034

**Reject an expired or reused SSO code**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the callback contains code=USED-CODE-A and the authentication provider rejects the code

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-018:202](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L202>)

```gherkin
@AUTH-034 @IMPLEMENTATION
Feature: SSO
  Scenario: Reject an expired or reused SSO code
    Given User A, an entitled portal user uses an isolated browser context
    And the callback contains code=USED-CODE-A and the authentication provider rejects the code
    When User A opens the callback URL
    Then the login page remains visible
    And a generic authentication failure is visible
    And no authenticated workspace becomes available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-035

**Remove callback parameters after entitlement checking**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the callback login succeeds with entitled entity ENTITY-A and drawer DRAWER-A

Behavior basis: [UI-SRC-119:141](<../../repos/ui/mfe-base/src/utils/login.ts#L141>)

```gherkin
@AUTH-035 @IMPLEMENTATION
Feature: SSO
  Scenario: Remove callback parameters after entitlement checking
    Given User A, an entitled portal user uses an isolated browser context
    And the callback login succeeds with entitled entity ENTITY-A and drawer DRAWER-A
    When the Home entitlement check completes
    Then the browser path becomes / without the code query
    And workspace WS-A remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-036

**Reject SSO users without matching entitlements**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: callback login returns entity ENTITY-X while every supplied drawer requires ENTITY-A

Behavior basis: [UI-SRC-119:141](<../../repos/ui/mfe-base/src/utils/login.ts#L141>)

```gherkin
@AUTH-036 @IMPLEMENTATION
Feature: SSO
  Scenario: Reject SSO users without matching entitlements
    Given User A, an entitled portal user uses an isolated browser context
    And callback login returns entity ENTITY-X while every supplied drawer requires ENTITY-A
    When the Home entitlement check completes
    Then the login page replaces Home
    And No entitlements found. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: Identity

<a id="group-identity"></a>

#### AUTH-037

**Display the authenticated profile name**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: login returns subject user-a and oud.fullName="Alex Example"

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>)

```gherkin
@AUTH-037 @IMPLEMENTATION
Feature: Identity
  Scenario: Display the authenticated profile name
    Given User A, an entitled portal user uses an isolated browser context
    And login returns subject user-a and oud.fullName="Alex Example"
    When the login response is accepted
    Then the profile identifies Alex Example rather than another fixture user
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-038

**Use the username when directory fullName is absent**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the directory returns no fullName for user-a; the BFF fixture follows its fallback path

Behavior basis: [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>); [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>)

```gherkin
@AUTH-038 @IMPLEMENTATION
Feature: Identity
  Scenario: Use the username when directory fullName is absent
    Given User A, an entitled portal user uses an isolated browser context
    And the directory returns no fullName for user-a; the BFF fixture follows its fallback path
    When User A completes login
    Then the profile identifies user-a
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-039

**Render an Unicode directory name**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: login returns oud.fullName="Álex 王"

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>)

```gherkin
@AUTH-039 @PROPOSED
Feature: Identity
  Scenario: Render an Unicode directory name
    Given User A, an entitled portal user uses an isolated browser context
    And login returns oud.fullName="Álex 王"
    When User A completes login
    Then the profile displays Álex 王 without replacement characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-040

**Escape markup in a directory name**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: login returns oud.fullName="<img src=x onerror=alert(1)>"

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>)

```gherkin
@AUTH-040 @PROPOSED
Feature: Identity
  Scenario: Escape markup in a directory name
    Given User A, an entitled portal user uses an isolated browser context
    And login returns oud.fullName="<img src=x onerror=alert(1)>"
    When User A opens the profile
    Then the name appears as text
    And no script or image error handler executes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-041

**Reject a malformed successful login payload**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the login service returns HTTP 200 with userInfo="not-json"

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-041 @PROPOSED
Feature: Identity
  Scenario: Reject a malformed successful login payload
    Given User A, an entitled portal user uses an isolated browser context
    And the login service returns HTTP 200 with userInfo="not-json"
    When User A submits valid credentials
    Then the UI does not expose an authenticated workspace
    And the UI presents a recoverable error instead of a blank page
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-042

**Reject a success response without an access credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the login service returns result=true and userInfo for user-a without Single-UI-Authorization

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-042 @PROPOSED
Feature: Identity
  Scenario: Reject a success response without an access credential
    Given User A, an entitled portal user uses an isolated browser context
    And the login service returns result=true and userInfo for user-a without Single-UI-Authorization
    When User A submits valid credentials
    Then the login form remains visible
    And an authentication error is visible
    And no authenticated workspace is shown
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.
### Group: Refresh

<a id="group-refresh"></a>

#### AUTH-043

**Prepare recovery before access expiry in a never-hidden page**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-043 @IMPLEMENTATION
Feature: Refresh
  Scenario: Prepare recovery before access expiry in a never-hidden page
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists
    When the visible page reaches T+875 seconds
    Then one refresh acquisition occurs
    And WS-A remains visible with no expiration dialog
    And the access expiry remains T+900 seconds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-044

**Do not acquire before the visible deadline**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-044 @IMPLEMENTATION
Feature: Refresh
  Scenario: Do not acquire before the visible deadline
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists
    When the visible page reaches T+874.999 seconds
    Then no refresh acquisition occurs
    And WS-A remains visible without an expiration dialog
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-045

**Acquire recovery credentials when the page hides**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; controlled time is T+60 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-045 @IMPLEMENTATION
Feature: Refresh
  Scenario: Acquire recovery credentials when the page hides
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; controlled time is T+60 seconds
    When User A switches to another browser tab
    Then one refresh acquisition occurs
    And returning before expiry still displays WS-A without an expiration dialog
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-046

**Cancel the visible acquisition timer while hidden**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the page hides at T+60 seconds and acquisition completes

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-046 @IMPLEMENTATION
Feature: Refresh
  Scenario: Cancel the visible acquisition timer while hidden
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the page hides at T+60 seconds and acquisition completes
    When controlled time passes T+875 seconds while hidden
    Then no second acquisition occurs from the visible timer
    And returning before T+900 keeps WS-A visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-047

**Re-arm acquisition after returning early**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; hide acquisition fails transiently at T+60 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-047 @IMPLEMENTATION
Feature: Refresh
  Scenario: Re-arm acquisition after returning early
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; hide acquisition fails transiently at T+60 seconds
    When User A returns at T+120 seconds and waits until T+875 seconds
    Then a refresh acquisition can occur at the visible deadline
    And WS-A remains visible without an expiration dialog before T+900
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-048

**Ignore duplicate visibility notifications**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the browser is hidden and one acquisition is pending

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-048 @IMPLEMENTATION
Feature: Refresh
  Scenario: Ignore duplicate visibility notifications
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the browser is hidden and one acquisition is pending
    When the browser delivers three hidden visibility notifications
    Then only one actual hide transition triggers acquisition
    And the Home session remains recoverable after the accepted response
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-049

**Share overlapping acquisition triggers**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; a hide acquisition is pending

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-049 @IMPLEMENTATION
Feature: Refresh
  Scenario: Share overlapping acquisition triggers
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; a hide acquisition is pending
    When User A shows and hides the page before the response arrives
    Then the existing request remains pending without cancellation
    And WS-A remains visible without an expiration dialog after acquisition completes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-050

**Refresh reuse boundary at 10800.001 seconds**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A has 600 seconds remaining; refresh R has 10800.001 seconds remaining

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-050 @IMPLEMENTATION
Feature: Refresh
  Scenario: Refresh reuse boundary at 10800.001 seconds
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A has 600 seconds remaining; refresh R has 10800.001 seconds remaining
    When User A hides and restores the page
    Then no refresh acquisition occurs
    And WS-A remains visible without a forced sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-051

**Refresh reuse boundary at 10800 seconds**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A has 600 seconds remaining; refresh R has 10800 seconds remaining

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-051 @IMPLEMENTATION
Feature: Refresh
  Scenario: Refresh reuse boundary at 10800 seconds
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A has 600 seconds remaining; refresh R has 10800 seconds remaining
    When User A hides and restores the page
    Then one refresh acquisition occurs
    And WS-A remains visible without a forced sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-052

**Refresh reuse boundary at 10799.999 seconds**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A has 600 seconds remaining; refresh R has 10799.999 seconds remaining

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-052 @IMPLEMENTATION
Feature: Refresh
  Scenario: Refresh reuse boundary at 10799.999 seconds
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A has 600 seconds remaining; refresh R has 10799.999 seconds remaining
    When User A hides and restores the page
    Then one refresh acquisition occurs
    And WS-A remains visible without a forced sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-053

**Evaluate reuse against the current clock on each trigger**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A has 600 seconds remaining; refresh R initially has 10801 seconds remaining

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-053 @IMPLEMENTATION
Feature: Refresh
  Scenario: Evaluate reuse against the current clock on each trigger
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A has 600 seconds remaining; refresh R initially has 10801 seconds remaining
    When User A hides and restores the page
    And the clock advances 1 second
    And User A hides and restores the page
    Then the first transition reuses R and the second permits replacement
    And WS-A remains visible without an expiration dialog
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-054

**Recover acquisition with missing token**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has missing token

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-054 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with missing token
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has missing token
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-055

**Recover acquisition with malformed JWT payload**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has malformed JWT payload

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-055 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with malformed JWT payload
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has malformed JWT payload
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-056

**Recover acquisition with missing exp**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has missing exp

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-056 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with missing exp
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has missing exp
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-057

**Recover acquisition with exp=null**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has exp=null

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-057 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with exp=null
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has exp=null
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-058

**Recover acquisition with exp as a string**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has exp as a string

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-058 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with exp as a string
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has exp as a string
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-059

**Recover acquisition with exp=non-finite number**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible with 600 seconds of valid access; its refresh credential has exp=non-finite number

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-059 @IMPLEMENTATION
Feature: Refresh
  Scenario: Recover acquisition with exp=non-finite number
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible with 600 seconds of valid access; its refresh credential has exp=non-finite number
    When a supported acquisition trigger runs
    Then the malformed credential does not block a replacement request
    And WS-A remains visible after the replacement succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Helper assertion inspection supports acquisition tolerance. UI-level malformed-token handling also requires execution; Timeout decodes without a catch.

#### AUTH-060

**Retry acquisition after a transient request failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; first hide acquisition fails with Network Error

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>); [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-060 @IMPLEMENTATION
Feature: Refresh
  Scenario: Retry acquisition after a transient request failure
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; first hide acquisition fails with Network Error
    When User A restores the page
    And User A hides the page again before access expiry
    Then the second transition can request replacement recovery credentials
    And WS-A remains visible after the second request succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-061

**Retry after cancelled acquisition**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the first refresh request is cancelled

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-061 @IMPLEMENTATION
Feature: Refresh
  Scenario: Retry after cancelled acquisition
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the first refresh request is cancelled
    When a later real hide occurs before expiry
    Then the cancelled request does not block the new request
    And WS-A remains visible without an expiration dialog after replacement completes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-062

**Acquire with a newer access credential**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; acquisition for access A is pending and a successful extension supplies access B

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-062 @IMPLEMENTATION
Feature: Refresh
  Scenario: Acquire with a newer access credential
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; acquisition for access A is pending and a successful extension supplies access B
    When User A hides the page again
    Then the old request is cancelled and the new request uses access B
    And the accepted B response preserves the current Home session
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-063

**Ignore a late cancelled acquisition response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the cancelled request belongs to access A and the current request belongs to access B

Behavior basis: [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-063 @PROPOSED
Feature: Refresh
  Scenario: Ignore a late cancelled acquisition response
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; the cancelled request belongs to access A and the current request belongs to access B
    When the access-A request resolves after cancellation
    Then the stale response does not replace the current session credential
    And WS-A remains associated with the current authenticated session
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-101:82](<../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The unit test adapter enforces cancellation. UI execution must verify the actual transport cancellation boundary.

#### AUTH-064

**Preserve manual recovery when hiding with 1 milliseconds of access**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A has valid refresh R and access A with 1 milliseconds remaining

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-064 @IMPLEMENTATION
Feature: Refresh
  Scenario: Preserve manual recovery when hiding with 1 milliseconds of access
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A has valid refresh R and access A with 1 milliseconds remaining
    When User A hides the page and returns after access expiry
    Then no late replacement acquisition occurs
    And the expiration dialog remains extendable with R
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-065

**Preserve manual recovery when hiding with 24999 milliseconds of access**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A has valid refresh R and access A with 24999 milliseconds remaining

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-065 @IMPLEMENTATION
Feature: Refresh
  Scenario: Preserve manual recovery when hiding with 24999 milliseconds of access
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A has valid refresh R and access A with 24999 milliseconds remaining
    When User A hides the page and returns after access expiry
    Then no late replacement acquisition occurs
    And the expiration dialog remains extendable with R
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-066

**Acquire missing recovery when Home mounts after the scheduled deadline**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: Home first mounts with access A expiring in 10 seconds and no refresh credential

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-066 @IMPLEMENTATION
Feature: Refresh
  Scenario: Acquire missing recovery when Home mounts after the scheduled deadline
    Given User A, an entitled portal user uses an isolated browser context
    And Home first mounts with access A expiring in 10 seconds and no refresh credential
    When Home becomes ready
    Then one acquisition occurs while access is valid
    And the expiration dialog can recover WS-A with Extend after access expires
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-067

**Do not replay missed acquisition after suspension**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: Home WS-A has access A expiring at T+900 seconds and no refresh credential; the page hides before T+875; hide acquisition fails

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>)

```gherkin
@AUTH-067 @IMPLEMENTATION
Feature: Refresh
  Scenario: Do not replay missed acquisition after suspension
    Given User A, an entitled portal user uses the isolated case fixture
    And User A uses an isolated browser context
    And Home WS-A has access A expiring at T+900 seconds and no refresh credential; the page hides before T+875; hide acquisition fails
    When User A returns to the page at T+890 seconds
    And the controlled clock reaches T+900 seconds
    And the existing logout delay completes
    Then no catch-up visible timer acquisition occurs
    And the login page replaces Home because no recovery credential exists
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-068

**Replace the obsolete acquisition schedule after access rotation**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; access A rotates to access B expiring at T+1200 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-109:90](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90>)

```gherkin
@AUTH-068 @IMPLEMENTATION
Feature: Refresh
  Scenario: Replace the obsolete acquisition schedule after access rotation
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; access A rotates to access B expiring at T+1200 seconds
    When the old T+875 acquisition deadline passes
    Then the old timer does not run
    And WS-A stays visible until the access-B deadline applies
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: Activity

<a id="group-activity"></a>

#### AUTH-069

**Renew access after a paused mouse movement**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; time is T+60 seconds

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-069 @IMPLEMENTATION
Feature: Activity
  Scenario: Renew access after a paused mouse movement
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; time is T+60 seconds
    When User A moves the mouse once and then pauses for 5 seconds
    Then one access extension occurs at T+65 seconds
    And WS-A remains visible and no expiration dialog opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-070

**Debounce repeated mouse movements**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; time is T+60 seconds

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>)

```gherkin
@AUTH-070 @IMPLEMENTATION
Feature: Activity
  Scenario: Debounce repeated mouse movements
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; time is T+60 seconds
    When User A moves the mouse every second for 6 seconds
    And User A stops moving for 5 seconds
    Then no extension runs during the moving interval
    And one extension runs after the final 5-second pause
    And WS-A remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-071

**Activity cutoff with 30000 milliseconds at return**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A has valid refresh R and access A with 30000 milliseconds remaining

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>)

```gherkin
@AUTH-071 @IMPLEMENTATION
Feature: Activity
  Scenario: Activity cutoff with 30000 milliseconds at return
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A has valid refresh R and access A with 30000 milliseconds remaining
    When User A moves the mouse and then waits 5 seconds
    Then one extension request occurs
    And no automatic relogin occurs
    And WS-A remains visible until its effective access deadline
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:510](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-072

**Activity cutoff with 29999 milliseconds at return**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A has valid refresh R and access A with 29999 milliseconds remaining

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>)

```gherkin
@AUTH-072 @IMPLEMENTATION
Feature: Activity
  Scenario: Activity cutoff with 29999 milliseconds at return
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A has valid refresh R and access A with 29999 milliseconds remaining
    When User A moves the mouse and then waits 5 seconds
    Then no extension request occurs
    And no automatic relogin occurs
    And WS-A remains visible until its effective access deadline
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:510](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-073

**Do not restore expired access from mouse movement**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser sleeps until T+1800 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>)

```gherkin
@AUTH-073 @IMPLEMENTATION
Feature: Activity
  Scenario: Do not restore expired access from mouse movement
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser sleeps until T+1800 seconds
    When User A restores the browser and moves the mouse
    Then the expiration dialog is visible
    And no activity extension or automatic relogin occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:510](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-074

**Proposed keyboard-only session activity**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A expires at T+900 seconds; User A types at T+60 seconds without mouse movement

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>)

```gherkin
@AUTH-074 @PROPOSED
Feature: Activity
  Scenario: Proposed keyboard-only session activity
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A expires at T+900 seconds; User A types at T+60 seconds without mouse movement
    When User A enters text into the active workspace
    And the controlled clock advances 5 seconds
    Then WS-A remains visible without an expiration dialog
    And a session extension uses the keyboard activity under the proposed policy
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed keyboard activity parity uses the existing five-second mouse debounce. Owner approval is missing.

#### AUTH-075

**Proposed touch-only session activity**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; access A expires at T+900 seconds; User A touches a control at T+60 seconds without mouse events

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>)

```gherkin
@AUTH-075 @PROPOSED
Feature: Activity
  Scenario: Proposed touch-only session activity
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; access A expires at T+900 seconds; User A touches a control at T+60 seconds without mouse events
    When User A activates the workspace control by touch
    And the controlled clock advances 5 seconds
    Then WS-A remains visible without an expiration dialog
    And a session extension uses touch activity under the proposed policy
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed touch activity parity uses the existing five-second mouse debounce. Device support and owner approval remain unknown.
### Group: Expiry

<a id="group-expiry"></a>

#### AUTH-076

**Display the access-expiration dialog exactly at expiry**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds

Behavior basis: [UI-SRC-109:90](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90>); [UI-SRC-094:16](<../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L16>)

```gherkin
@AUTH-076 @IMPLEMENTATION
Feature: Expiry
  Scenario: Display the access-expiration dialog exactly at expiry
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds
    When the controlled clock reaches T+900 seconds
    Then one dialog shows Your session has been expired
    And Extend and Logout are visible
    And no relogin occurs without selecting Extend
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-077

**Keep Home usable immediately before access expiry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds

Behavior basis: [UI-SRC-109:90](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90>)

```gherkin
@AUTH-077 @IMPLEMENTATION
Feature: Expiry
  Scenario: Keep Home usable immediately before access expiry
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds
    When the controlled clock reaches T+899.999 seconds
    Then no expiration dialog is visible
    And WS-A remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-078

**Recover manually from access expiry**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin service accepts refresh R

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-105:18](<../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L18>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-078 @IMPLEMENTATION
Feature: Expiry
  Scenario: Recover manually from access expiry
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin service accepts refresh R
    When User A selects Extend
    Then the expiration dialog closes
    And WS-A remains available with the new access credential
    And one relogin uses refresh R
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:215](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-079

**Stop silent recovery while the expiration dialog is open**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>)

```gherkin
@AUTH-079 @IMPLEMENTATION
Feature: Expiry
  Scenario: Stop silent recovery while the expiration dialog is open
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds
    When User A hides and restores the browser without selecting Extend
    Then the expiration dialog remains visible
    And no hide-triggered acquisition or automatic relogin occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-080

**Log out from the expiration dialog**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-080 @IMPLEMENTATION
Feature: Expiry
  Scenario: Log out from the expiration dialog
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds
    When User A selects Logout and the controlled clock advances 1 second
    Then the login page replaces Home
    And the expiration dialog disappears
    And local and session access credentials are absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-081

**Log out at expiry when recovery credentials are missing**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; acquisition failed and time has reached T+900 seconds

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-081 @IMPLEMENTATION
Feature: Expiry
  Scenario: Log out at expiry when recovery credentials are missing
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at controlled time T+900 seconds and no refresh credential exists; acquisition failed and time has reached T+900 seconds
    When the expiration component mounts and the controlled clock advances 1 second
    Then the login page replaces Home
    And no manual relogin occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-082

**Preserve the fixed refresh cutoff during activity**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; repeated access renewals extend access beyond T+13524 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-082 @IMPLEMENTATION
Feature: Expiry
  Scenario: Preserve the fixed refresh cutoff during activity
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; repeated access renewals extend access beyond T+13524 seconds
    When the controlled clock reaches T+13524 seconds
    Then logout starts despite valid access
    And the login page appears after the existing 1-second logout delay
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-083

**Respect the dialog refresh cutoff lead**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-094:16](<../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L16>)

```gherkin
@AUTH-083 @IMPLEMENTATION
Feature: Expiry
  Scenario: Respect the dialog refresh cutoff lead
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds
    When the controlled clock reaches T+598 seconds
    Then Extend becomes disabled as logout starts
    And the login page appears at T+599 seconds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The existing dialog starts logout two seconds before refresh expiry and waits one second. This is source characterization.

#### AUTH-084

**Keep Extend available immediately before the dialog cutoff**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-094:16](<../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L16>)

```gherkin
@AUTH-084 @IMPLEMENTATION
Feature: Expiry
  Scenario: Keep Extend available immediately before the dialog cutoff
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds
    When the controlled clock reaches T+597.999 seconds
    Then Extend is enabled
    And the expiration dialog is still visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-093

**Do not renew once logout has started**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; User A already selected Logout

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>)

```gherkin
@AUTH-093 @IMPLEMENTATION
Feature: Expiry
  Scenario: Do not renew once logout has started
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; User A already selected Logout
    When the page hides and the pending activity timer fires
    Then Extend remains disabled
    And no new refresh acquisition, extension, or relogin occurs
    And the login page replaces Home
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-094

**Do not postpone refresh cutoff through a last-minute manual Extend**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds and relogin supplies access valid until T+1500 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>)

```gherkin
@AUTH-094 @IMPLEMENTATION
Feature: Expiry
  Scenario: Do not postpone refresh cutoff through a last-minute manual Extend
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; refresh R expires at T+600 seconds and relogin supplies access valid until T+1500 seconds
    When User A selects Extend at T+540 seconds and then waits past T+600 seconds
    Then the dialog initially closes after relogin
    And the original refresh cutoff still starts logout
    And the login page replaces Home
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-095

**Handle a relogin rejection**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; relogin returns TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>)

```gherkin
@AUTH-095 @IMPLEMENTATION
Feature: Expiry
  Scenario: Handle a relogin rejection
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; relogin returns TOKEN_INVALID_EXPIRED
    When User A selects Extend
    Then the login page replaces Home
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-096

**Keep recovery available after relogin network failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin request fails with Network Error

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-096 @PROPOSED
Feature: Expiry
  Scenario: Keep recovery available after relogin network failure
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin request fails with Network Error
    When User A selects Extend
    Then a service error is visible
    And the expiration dialog remains visible with enabled Extend and Logout buttons
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: relogin returns no request promise. The dialog closes before the asynchronous response; desired recovery needs owner review.

#### AUTH-097

**Prevent stale relogin after logout**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; a relogin response is pending and logout subsequently clears the session

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-097 @PROPOSED
Feature: Expiry
  Scenario: Prevent stale relogin after logout
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; a relogin response is pending and logout subsequently clears the session
    When the old relogin response arrives
    Then the login page remains visible
    And the stale response does not restore Home
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-098

**Prevent double recovery from rapid Extend activation**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; relogin response is pending

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-098 @PROPOSED
Feature: Expiry
  Scenario: Prevent double recovery from rapid Extend activation
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; relogin response is pending
    When User A rapidly activates Extend twice
    Then at most one effective recovery transition occurs
    And Home shows one authenticated session without stale error state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-099

**Constrain malformed refresh credentials in the timeout dialog**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: access A is expired and refresh R contains invalid JSON

Behavior basis: [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>)

```gherkin
@AUTH-099 @PROPOSED
Feature: Expiry
  Scenario: Constrain malformed refresh credentials in the timeout dialog
    Given User A, an entitled portal user uses an isolated browser context
    And access A is expired and refresh R contains invalid JSON
    When the timeout component mounts
    Then the login page replaces Home
    And an authentication error is visible
    And no authenticated workspace remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-100

**Handle the clock moving forward across expiry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>)

```gherkin
@AUTH-100 @IMPLEMENTATION
Feature: Expiry
  Scenario: Handle the clock moving forward across expiry
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds
    When the controlled browser clock jumps beyond both credential expiries and visibility changes to visible
    Then logout starts
    And the login page replaces Home after the existing logout delay
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-101

**Define behavior for a browser clock moving backward**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; server time remains correct

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>)

```gherkin
@AUTH-101 @PROPOSED
Feature: Expiry
  Scenario: Define behavior for a browser clock moving backward
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; server time remains correct
    When the browser clock moves backward 1 hour and the next protected service rejects expiry
    Then the login page replaces Home on TOKEN_INVALID_EXPIRED
    And the browser does not silently restore rejected credentials
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.
### Group: Suspension

<a id="group-suspension"></a>

#### AUTH-085

**Log out after browser suspension lasting 13524 seconds**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 13524 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-085 @IMPLEMENTATION
Feature: Suspension
  Scenario: Log out after browser suspension lasting 13524 seconds
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 13524 seconds
    When User A restores the browser and the logout delay completes
    Then the login page replaces Home
    And Extend cannot recover the expired refresh credential
    And no automatic access extension occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-086

**Log out after browser suspension lasting 4 hours**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 4 hours

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-086 @IMPLEMENTATION
Feature: Suspension
  Scenario: Log out after browser suspension lasting 4 hours
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 4 hours
    When User A restores the browser and the logout delay completes
    Then the login page replaces Home
    And Extend cannot recover the expired refresh credential
    And no automatic access extension occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-087

**Log out after browser suspension lasting 4 hours and 1 millisecond**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 4 hours and 1 millisecond

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-087 @IMPLEMENTATION
Feature: Suspension
  Scenario: Log out after browser suspension lasting 4 hours and 1 millisecond
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 4 hours and 1 millisecond
    When User A restores the browser and the logout delay completes
    Then the login page replaces Home
    And Extend cannot recover the expired refresh credential
    And no automatic access extension occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-088

**Log out after browser suspension lasting 8 hours**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 8 hours

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-088 @IMPLEMENTATION
Feature: Suspension
  Scenario: Log out after browser suspension lasting 8 hours
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 8 hours
    When User A restores the browser and the logout delay completes
    Then the login page replaces Home
    And Extend cannot recover the expired refresh credential
    And no automatic access extension occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-089

**Log out after browser suspension lasting 24 hours**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 24 hours

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-089 @IMPLEMENTATION
Feature: Suspension
  Scenario: Log out after browser suspension lasting 24 hours
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser suspends for 24 hours
    When User A restores the browser and the logout delay completes
    Then the login page replaces Home
    And Extend cannot recover the expired refresh credential
    And no automatic access extension occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-090

**Restore before access expiry and continue working**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser hides at T+60 seconds and returns at T+120 seconds

Behavior basis: [UI-SRC-109:60](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60>); [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-103:8](<../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8>)

```gherkin
@AUTH-090 @IMPLEMENTATION
Feature: Suspension
  Scenario: Restore before access expiry and continue working
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser hides at T+60 seconds and returns at T+120 seconds
    When User A moves the mouse and pauses 5 seconds
    Then WS-A remains visible
    And access renews while refresh R remains the same
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:510](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-091

**Restore after access expiry but before refresh expiry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser returns at T+1800 seconds

Behavior basis: [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-093:25](<../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25>)

```gherkin
@AUTH-091 @IMPLEMENTATION
Feature: Suspension
  Scenario: Restore after access expiry but before refresh expiry
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; the browser returns at T+1800 seconds
    When User A restores the page
    Then the expiration dialog is visible
    And WS-A is recoverable only through an explicit Extend action
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:510](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-092

**Use the latest expiry after background access rotation**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; access B replaces A while the page is hidden and expires at T+1800 seconds

Behavior basis: [UI-SRC-109:90](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90>); [UI-SRC-109:104](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-092 @IMPLEMENTATION
Feature: Suspension
  Scenario: Use the latest expiry after background access rotation
    Given User A, an entitled portal user uses an isolated browser context
    And the Home page contains workspace WS-A; access A expires at T+900 seconds and refresh R expires at T+13524 seconds; access B replaces A while the page is hidden and expires at T+1800 seconds
    When User A restores at T+1000 seconds
    Then the old A expiry does not open the expiration dialog
    And WS-A remains visible under B
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: Logout

<a id="group-logout"></a>

#### AUTH-102

**Cancel logout without losing work**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open

Behavior basis: [UI-SRC-076:21](<../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21>); [UI-SRC-077:24](<../../repos/ui/mfe-base/src/components/Survey/index.tsx#L24>)

```gherkin
@AUTH-102 @IMPLEMENTATION
Feature: Logout
  Scenario: Cancel logout without losing work
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open
    When User A selects Cancel
    Then the confirmation closes
    And WS-A and its current state remain visible
    And no logout request occurs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-103

**Confirm logout from the profile flow**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open

Behavior basis: [UI-SRC-076:21](<../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-103 @IMPLEMENTATION
Feature: Logout
  Scenario: Confirm logout from the profile flow
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open
    When User A selects Logout and waits 1 second
    Then the login page replaces Home
    And access, refresh, identity, and expiration state are cleared
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-104

**Open feedback without logging out**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; the feedback popup is allowed

Behavior basis: [UI-SRC-076:21](<../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21>); [UI-SRC-077:24](<../../repos/ui/mfe-base/src/components/Survey/index.tsx#L24>)

```gherkin
@AUTH-104 @IMPLEMENTATION
Feature: Logout
  Scenario: Open feedback without logging out
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; the feedback popup is allowed
    When User A selects Share Feedback
    Then the feedback destination opens
    And the confirmation closes
    And WS-A remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-105

**Open feedback and log out**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; the feedback popup is allowed

Behavior basis: [UI-SRC-076:21](<../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21>); [UI-SRC-077:24](<../../repos/ui/mfe-base/src/components/Survey/index.tsx#L24>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-105 @IMPLEMENTATION
Feature: Logout
  Scenario: Open feedback and log out
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; the feedback popup is allowed
    When User A selects Share Feedback & Logout and waits 1 second
    Then the feedback destination opens
    And the login page replaces Home
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-106

**Finish logout when feedback popup is blocked**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; the browser blocks new windows

Behavior basis: [UI-SRC-076:21](<../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-106 @PROPOSED
Feature: Logout
  Scenario: Finish logout when feedback popup is blocked
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; the browser blocks new windows
    When User A selects Share Feedback & Logout and waits 1 second
    Then the login page replaces Home
    And the blocked popup does not keep the user authenticated
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-107

**Clear local authentication when BFF logout fails**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; BFF logout fails

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-107 @IMPLEMENTATION
Feature: Logout
  Scenario: Clear local authentication when BFF logout fails
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; BFF logout fails
    When User A selects Logout and waits 1 second
    Then the login page replaces Home
    And the local access credential is removed
    And no logout transport error blocks local sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-108

**Clear local authentication when downstream /ssiplus/imeta/logout fails**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; downstream /ssiplus/imeta/logout fails

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-108 @IMPLEMENTATION
Feature: Logout
  Scenario: Clear local authentication when downstream /ssiplus/imeta/logout fails
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; downstream /ssiplus/imeta/logout fails
    When User A selects Logout and waits 1 second
    Then the login page replaces Home
    And the local access credential is removed
    And no logout transport error blocks local sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-109

**Clear local authentication when both logout requests fail**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; both logout requests fail

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-109 @IMPLEMENTATION
Feature: Logout
  Scenario: Clear local authentication when both logout requests fail
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; both logout requests fail
    When User A selects Logout and waits 1 second
    Then the login page replaces Home
    And the local access credential is removed
    And no logout transport error blocks local sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-110

**Clear local authentication when both requests remain pending**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible for user-a and the Leave Now? confirmation is open; both requests remain pending

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-110 @IMPLEMENTATION
Feature: Logout
  Scenario: Clear local authentication when both requests remain pending
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible for user-a and the Leave Now? confirmation is open; both requests remain pending
    When User A selects Logout and waits 1 second
    Then the login page replaces Home
    And the local access credential is removed
    And no logout transport error blocks local sign-out
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-111

**Invalidate replay of a logged-out session**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: user-a completed BFF logout for session SESSION-A; a captured access fixture for SESSION-A still has future expiry

Behavior basis: [UI-SRC-018:365](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365>); [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-111 @IMPLEMENTATION
Feature: Logout
  Scenario: Invalidate replay of a logged-out session
    Given User A, an entitled portal user uses an isolated browser context
    And user-a completed BFF logout for session SESSION-A; a captured access fixture for SESSION-A still has future expiry
    When the browser attempts session validation with that fixture
    Then the login page remains visible
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-112

**Begin a fresh session after logout**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: user-a completed logout and the login page is visible

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>); [UI-SRC-100:37](<../../repos/ui/mfe-base/src/hooks/service/index.ts#L37>)

```gherkin
@AUTH-112 @IMPLEMENTATION
Feature: Logout
  Scenario: Begin a fresh session after logout
    Given User A, an entitled portal user uses an isolated browser context
    And user-a completed logout and the login page is visible
    When User A signs in again and then hides the page
    Then Home WS-A becomes visible
    And new recovery credentials belong to the new session
    And the previous refresh credential is not reused
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-108:572](<../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-113

**Do not restore old access from browser Back**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: user-a completed logout and previously visited Home

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-113 @PROPOSED
Feature: Logout
  Scenario: Do not restore old access from browser Back
    Given User A, an entitled portal user uses an isolated browser context
    And user-a completed logout and previously visited Home
    When User A selects browser Back
    Then the authenticated workspace remains unavailable
    And the login page is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-114

**Do not restore old access after page reload**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: user-a completed logout and the login page is visible

Behavior basis: [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>); [UI-SRC-118:50](<../../repos/ui/mfe-base/src/utils/common.ts#L50>)

```gherkin
@AUTH-114 @IMPLEMENTATION
Feature: Logout
  Scenario: Do not restore old access after page reload
    Given User A, an entitled portal user uses an isolated browser context
    And user-a completed logout and the login page is visible
    When User A reloads the page
    Then the login page remains visible
    And WS-A is not restored from browser storage
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: Multi-tab

<a id="group-multi-tab"></a>

#### AUTH-115

**Define logout propagation across browser tabs**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: tabs TAB-A and TAB-B share the same origin and initially show user-a under SESSION-A

Behavior basis: [UI-SRC-018:365](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-115 @PROPOSED
Feature: Multi-tab
  Scenario: Define logout propagation across browser tabs
    Given User A, an entitled portal user uses an isolated browser context
    And tabs TAB-A and TAB-B share the same origin and initially show user-a under SESSION-A
    When User A completes logout in TAB-A
    Then TAB-B blocks the next protected action when SESSION-A is rejected
    And TAB-B shows the expired-session login state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Immediate cross-tab propagation is not established. The acceptance point is the next rejected protected operation.

#### AUTH-116

**Keep different browser contexts independent**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: browser contexts CTX-A and CTX-B use distinct sessions SESSION-A and SESSION-B for user-a

Behavior basis: [UI-SRC-018:365](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>)

```gherkin
@AUTH-116 @PROPOSED
Feature: Multi-tab
  Scenario: Keep different browser contexts independent
    Given User A, an entitled portal user uses an isolated browser context
    And browser contexts CTX-A and CTX-B use distinct sessions SESSION-A and SESSION-B for user-a
    When User A logs out in CTX-A
    Then CTX-A shows the login page
    And CTX-B remains usable when its separate session validates
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-117

**Prevent a late old-user response from replacing a new-user session**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: user-a request is pending; the browser logs out and signs in as user-b before that response arrives

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>); [UI-SRC-117:20](<../../repos/ui/mfe-base/src/services/index.ts#L20>)

```gherkin
@AUTH-117 @PROPOSED
Feature: Multi-tab
  Scenario: Prevent a late old-user response from replacing a new-user session
    Given User A, an entitled portal user uses an isolated browser context
    And user-a request is pending; the browser logs out and signs in as user-b before that response arrives
    When the old user-a response completes
    Then the visible profile remains user-b
    And user-a data and entitlements do not replace user-b state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.
### Group: BFF boundary

<a id="group-bff-boundary"></a>

#### AUTH-118

**Handle validation with missing access credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with missing access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-118 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with missing access credential
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with missing access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-119

**Handle validation with malformed access credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with malformed access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-119 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with malformed access credential
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with malformed access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-120

**Handle validation with invalid signature**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with invalid signature; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-120 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with invalid signature
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with invalid signature; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-121

**Handle validation with expired access credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with expired access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-121 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with expired access credential
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with expired access credential; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-122

**Handle validation with wrong issuer**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with wrong issuer; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-122 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with wrong issuer
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with wrong issuer; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-123

**Handle validation with revoked session identifier**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the browser attempts to restore WS-A with revoked session identifier; the BFF rejects validation with TOKEN_INVALID_EXPIRED

Behavior basis: [UI-SRC-018:252](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-123 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle validation with revoked session identifier
    Given User A, an entitled portal user uses an isolated browser context
    And the browser attempts to restore WS-A with revoked session identifier; the BFF rejects validation with TOKEN_INVALID_EXPIRED
    When the validation response reaches the UI
    Then the login page replaces Home
    And Expired Session, please login again. is visible
    And no protected workspace is restored
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-124

**Handle manual recovery with missing refresh credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has missing refresh credential and the BFF rejects it

Behavior basis: [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-124 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle manual recovery with missing refresh credential
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has missing refresh credential and the BFF rejects it
    When User A selects Extend
    Then the login page replaces Home
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-125

**Handle manual recovery with access token supplied as refresh**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has access token supplied as refresh and the BFF rejects it

Behavior basis: [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-125 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle manual recovery with access token supplied as refresh
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has access token supplied as refresh and the BFF rejects it
    When User A selects Extend
    Then the login page replaces Home
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-126

**Handle manual recovery with expired refresh credential**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has expired refresh credential and the BFF rejects it

Behavior basis: [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-126 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle manual recovery with expired refresh credential
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has expired refresh credential and the BFF rejects it
    When User A selects Extend
    Then the login page replaces Home
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-127

**Handle manual recovery with revoked refresh session**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has revoked refresh session and the BFF rejects it

Behavior basis: [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-028:87](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87>); [UI-SRC-026:28](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-127 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Handle manual recovery with revoked refresh session
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the recovery request has revoked refresh session and the BFF rejects it
    When User A selects Extend
    Then the login page replaces Home
    And Expired Session, please login again. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-128

**Display service authorization denial without misclassifying expiry**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; a protected user action returns HTTP 403 with message="Access denied"

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-128 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Display service authorization denial without misclassifying expiry
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; a protected user action returns HTTP 403 with message="Access denied"
    When User A performs that protected action
    Then Access denied is visible
    And the action does not show success
    And the session is not cleared solely because the status is 403
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-129

**Distinguish a bare 401 from the expiry marker**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; a protected user action returns HTTP 401 with an empty body

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-129 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Distinguish a bare 401 from the expiry marker
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; a protected user action returns HTTP 401 with an empty body
    When User A performs the action
    Then a service-unavailable error is visible
    And WS-A remains visible because the error lacks TOKEN_INVALID_EXPIRED
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: This characterizes the current error mapper. The intended unauthorized-session policy requires review.

#### AUTH-130

**Do not expose raw credentials in UI errors**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: a protected request fails with a response containing a synthetic credential-looking string

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-130 @PROPOSED
Feature: BFF boundary
  Scenario: Do not expose raw credentials in UI errors
    Given User A, an entitled portal user uses an isolated browser context
    And a protected request fails with a response containing a synthetic credential-looking string
    When the error is rendered
    Then the page does not display the synthetic secret
    And the user receives a safe service error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Current mapper renders response strings directly. Redaction and allowed error content need owner review.

#### AUTH-131

**Render an API string error as user-visible text**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible and a request returns plain text "Fixture service unavailable"

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-131 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Render an API string error as user-visible text
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible and a request returns plain text "Fixture service unavailable"
    When User A performs the controlled action
    Then Fixture service unavailable is visible
    And the global loading indicator stops
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-132

**Use message before errorMessage for structured errors**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; a failed request returns message="Primary error" and errorMessage="Secondary error"

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-132 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Use message before errorMessage for structured errors
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; a failed request returns message="Primary error" and errorMessage="Secondary error"
    When the failed response is handled
    Then Primary error is visible
    And Secondary error is not the displayed primary message
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-133

**Suppress cancellation errors**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible and a controlled request is aborted with ERR_CANCELED

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-133 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Suppress cancellation errors
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible and a controlled request is aborted with ERR_CANCELED
    When the cancellation is handled
    Then no new cancellation snackbar is shown
    And the global loading state ends
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-134

**Keep analytics failures from interrupting the user**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; an /api/analytics/ request fails

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-134 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Keep analytics failures from interrupting the user
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; an /api/analytics/ request fails
    When User A performs a UI action that sends analytics
    Then WS-A remains visible
    And no analytics transport error appears as a user error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-135

**Keep SSE transport failures out of the global error**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: WS-A is visible; an /api/sse/ request fails

Behavior basis: [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-135 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Keep SSE transport failures out of the global error
    Given User A, an entitled portal user uses an isolated browser context
    And WS-A is visible; an /api/sse/ request fails
    When the failure is handled
    Then WS-A remains visible
    And no SSE transport error appears as a global user error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.

#### AUTH-136

**Do not let telemetry failure prevent login**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: authentication succeeds but BFF login analytics insert throws an exception

Behavior basis: [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>)

```gherkin
@AUTH-136 @PROPOSED
Feature: BFF boundary
  Scenario: Do not let telemetry failure prevent login
    Given User A, an entitled portal user uses an isolated browser context
    And authentication succeeds but BFF login analytics insert throws an exception
    When User A submits valid credentials
    Then Home is available when authentication is accepted
    And telemetry failure does not invalidate the user login
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Current analytics call is inside the login try block. A failure can return AuthenticationException; desired isolation requires owner review.

#### AUTH-137

**Reject stale entitlement visibility after a new login**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: user-a previously had ENTITY-A; the next accepted login returns no entities and no drawers

Behavior basis: [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-119:141](<../../repos/ui/mfe-base/src/utils/login.ts#L141>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-137 @PROPOSED
Feature: BFF boundary
  Scenario: Reject stale entitlement visibility after a new login
    Given User A, an entitled portal user uses an isolated browser context
    And user-a previously had ENTITY-A; the next accepted login returns no entities and no drawers
    When User A signs in under the new response
    Then old ENTITY-A applications are absent
    And the page does not expose the prior user catalog
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: handleDrawers updates only nonempty arrays. No complete empty-catalog policy is established.

#### AUTH-138

**Keep removed permissions unavailable after recovery**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin response removes ENTITY-A and its drawer

Behavior basis: [UI-SRC-018:335](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335>); [UI-SRC-119:65](<../../repos/ui/mfe-base/src/utils/login.ts#L65>); [UI-SRC-104:25](<../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25>)

```gherkin
@AUTH-138 @PROPOSED
Feature: BFF boundary
  Scenario: Keep removed permissions unavailable after recovery
    Given User A, an entitled portal user uses an isolated browser context
    And the expiration dialog is open for WS-A; access A is expired and refresh R expires at T+600 seconds; the relogin response removes ENTITY-A and its drawer
    When User A selects Extend
    Then ENTITY-A applications are unavailable after recovery
    And the profile remains user-a
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Proposed expectation requires owner review. No inspected source establishes this as approved policy.

#### AUTH-139

**Define handling when entitlement service is unavailable during login**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; authentication succeeds but entitlement retrieval fails

Behavior basis: [UI-SRC-018:161](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>)

```gherkin
@AUTH-139 @IMPLEMENTATION
Feature: BFF boundary
  Scenario: Define handling when entitlement service is unavailable during login
    Given User A, an entitled portal user uses an isolated browser context
    And the LOCAL login page is open with empty browser storage and valid fixture credentials user-a / FixturePass1!; authentication succeeds but entitlement retrieval fails
    When User A submits valid credentials
    Then the login page remains visible
    And Invalid username and password combination or SSO service is unavailable. is visible
    And no partial authenticated catalog is shown
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Characterizes inspected source. Business acceptance and deployed configuration remain unproved.
### Group: SSO security

<a id="group-sso-security"></a>

#### AUTH-140

**Reject a callback with mismatched OAuth state**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: a controlled SSO attempt stores state STATE-A and returns a callback with state=STATE-B

Behavior basis: [UI-SRC-115:20](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L20>)

```gherkin
@AUTH-140 @PROPOSED
Feature: SSO security
  Scenario: Reject a callback with mismatched OAuth state
    Given User A, an entitled portal user uses an isolated browser context
    And a controlled SSO attempt stores state STATE-A and returns a callback with state=STATE-B
    When User A opens the callback
    Then the login page remains visible
    And the callback does not open an authenticated workspace
    And the UI shows a recoverable authentication error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The inspected callback does not read state. OAuth state storage, enforcement, and ownership remain unproved.

#### AUTH-141

**Reject an unsolicited SSO callback**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the browser has no pending SSO attempt; a callback contains a valid code obtained from a different browser session

Behavior basis: [UI-SRC-115:20](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L20>)

```gherkin
@AUTH-141 @PROPOSED
Feature: SSO security
  Scenario: Reject an unsolicited SSO callback
    Given User A, an entitled portal user uses an isolated browser context
    And the browser has no pending SSO attempt; a callback contains a valid code obtained from a different browser session
    When User A opens that callback
    Then the UI does not establish a session for the other browser identity
    And the UI presents a recoverable authentication error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: SSO session-binding enforcement is unresolved. This proposes login-CSRF protection rather than asserting existing behavior.

#### AUTH-142

**Reject a callback error without replaying an old code**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the callback URL contains error=access_denied and no code; no user session exists

Behavior basis: [UI-SRC-115:20](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L20>)

```gherkin
@AUTH-142 @IMPLEMENTATION
Feature: SSO security
  Scenario: Reject a callback error without replaying an old code
    Given User A, an entitled portal user uses an isolated browser context
    And the callback URL contains error=access_denied and no code; no user session exists
    When User A opens that callback
    Then the login page remains visible
    And the UI offers Sign In With SSO for a fresh attempt
    And no old callback code is exchanged
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The source processes only a nonempty code parameter. Dedicated provider-error text is not established.

#### AUTH-143

**Use a new SSO attempt after provider cancellation**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: User A, an entitled portal user.

Setup: the identity provider cancels attempt SSO-A and returns to the login page

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-143 @IMPLEMENTATION
Feature: SSO security
  Scenario: Use a new SSO attempt after provider cancellation
    Given User A, an entitled portal user uses an isolated browser context
    And the identity provider cancels attempt SSO-A and returns to the login page
    When User A selects Sign In With SSO again
    Then the browser starts a fresh identity-provider navigation
    And no authenticated Home is shown before the new attempt succeeds
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: Navigation behavior is source-backed. Provider state handling and deployed identity integration remain unproved.

#### AUTH-144

**Do not authenticate from a client-forged entitlement token**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: User A, an entitled portal user.

Setup: the browser modifies the decoded entitlements fixture to grant ADMIN without a valid issuer signature

Behavior basis: [UI-SRC-115:38](<../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38>)

```gherkin
@AUTH-144 @PROPOSED
Feature: SSO security
  Scenario: Do not authenticate from a client-forged entitlement token
    Given User A, an entitled portal user uses an isolated browser context
    And the browser modifies the decoded entitlements fixture to grant ADMIN without a valid issuer signature
    When User A attempts to open an admin action
    Then the admin operation is denied by the server
    And the UI does not report a successful admin change
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Reset injected responses, controlled clocks, and fixture session records.

Limits: The browser decodes entitlements for UI state. Server validation must be verified through an admin fixture; client hiding is insufficient.
### Group: Workspaces

<a id="group-workspaces"></a>

#### UI-SHL-001

**Empty workspace offers tile discovery**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 has no containers

Behavior basis: [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>); [UI-SRC-067:11](<../../repos/ui/mfe-base/src/components/Empty/index.tsx#L11>)

```gherkin
@UI-SHL-001 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Empty workspace offers tile discovery
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 has no containers
    When open W1
    Then W1 shows Start customizing your workspace and a Find tile button
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-002

**Find tile opens drawer**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 is empty and the drawer is closed

Behavior basis: [UI-SRC-067:11](<../../repos/ui/mfe-base/src/components/Empty/index.tsx#L11>); [UI-SRC-066:9](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L9>)

```gherkin
@UI-SHL-002 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Find tile opens drawer
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 is empty and the drawer is closed
    When click Find tile
    Then the right drawer shows Tile Options
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-003

**Add a blank workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. only W1 exists with label Workspace 1

Behavior basis: [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>); [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-SHL-003 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Add a blank workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And only W1 exists with label Workspace 1
    When click Add Workspace
    Then two workspace tabs exist
    And the selected tab is labelled Workspace 2
    And the selected panel shows Find tile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-004

**Number a workspace after a numbered label**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the last tab is labelled Workspace 7

Behavior basis: [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-SHL-004 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Number a workspace after a numbered label
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the last tab is labelled Workspace 7
    When click Add Workspace
    Then the added tab is labelled Workspace 8
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-005

**Number a workspace after a custom label**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. two tabs exist and the last is labelled Operations

Behavior basis: [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-SHL-005 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Number a workspace after a custom label
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And two tabs exist and the last is labelled Operations
    When click Add Workspace
    Then the added tab is labelled Workspace 3
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-006

**Switch active workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 and W2 exist and W1 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>); [UI-SRC-083:6](<../../repos/ui/mfe-base/src/components/TabPanel/index.tsx#L6>)

```gherkin
@UI-SHL-006 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Switch active workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 and W2 exist and W1 is selected
    When select W2
    Then W2 is selected
    And Panel Two is visible
    And W1 content is hidden
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-007

**Keep mounted container state across tab switches**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 test container counter is 4 and W2 exists

Behavior basis: [UI-SRC-083:6](<../../repos/ui/mfe-base/src/components/TabPanel/index.tsx#L6>)

```gherkin
@UI-SHL-007 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Keep mounted container state across tab switches
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 test container counter is 4 and W2 exists
    When select W2
    And select W1
    Then W1 still shows counter value 4
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-008

**Double-click starts workspace rename**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>); [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-008 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Double-click starts workspace rename
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 is selected
    When double-click W1 tab
    Then the Workspace Name input for W1 has focus
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-009

**Rename workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the Workspace Name input for W1 has focus

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>); [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-009 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Rename workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the Workspace Name input for W1 has focus
    When replace its value with Operations Morning
    Then the tab input shows Operations Morning
    And the tab tooltip shows Operations Morning
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-010

**Restore renamed workspace after reload**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 was renamed Operations Morning and saved storage is valid

Behavior basis: [UI-SRC-098:6](<../../repos/ui/mfe-base/src/hooks/reducer/workspaces.reducers.ts#L6>); [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-010 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Restore renamed workspace after reload
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 was renamed Operations Morning and saved storage is valid
    When reload the shell
    Then the restored W1 tab shows Operations Morning
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-011

**Keep at least one workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 is the only workspace

Behavior basis: [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>); [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-011 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Keep at least one workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 is the only workspace
    When inspect the W1 tab
    Then no delete button is shown for W1
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-012

**Remove selected middle workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1, W2, and W3 exist and W2 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-012 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Remove selected middle workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1, W2, and W3 exist and W2 is selected
    When click the delete control on W2
    Then two tabs remain
    And W1 becomes selected
    And Panel Two is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-013

**Remove selected first workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 and W2 exist and W1 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-013 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Remove selected first workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 and W2 exist and W1 is selected
    When click the delete control on W1
    Then only W2 remains
    And Panel Two is visible
    And the delete control is absent on W2
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-014

**Remove tab before selected workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1, W2, and W3 exist and W3 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-014 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Remove tab before selected workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1, W2, and W3 exist and W3 is selected
    When click the delete control on W1
    Then W3 remains selected
    And Panel Three remains visible
    And W1 is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-015

**Remove tab after selected workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1, W2, and W3 exist and W1 is selected

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-015 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Remove tab after selected workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1, W2, and W3 exist and W1 is selected
    When click the delete control on W3
    Then W1 remains selected
    And W3 is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-016

**Restore workspace deletion after reload**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 and W2 existed and W2 was deleted

Behavior basis: [UI-SRC-098:6](<../../repos/ui/mfe-base/src/hooks/reducer/workspaces.reducers.ts#L6>)

```gherkin
@UI-SHL-016 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Restore workspace deletion after reload
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 and W2 existed and W2 was deleted
    When reload the shell
    Then W2 is absent from the restored tabs
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-017

**Place first tile in empty workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 is empty and Test Tile is enabled in the drawer

Behavior basis: [UI-SRC-058:36](<../../repos/ui/mfe-base/src/components/AppBar/common/useController.ts#L36>)

```gherkin
@UI-SHL-017 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Place first tile in empty workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 is empty and Test Tile is enabled in the drawer
    When click Test Tile
    Then the tab count remains one
    And W1 is labelled Test Tile Demo
    And the controlled container displays /tile-global
    And the drawer closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-018

**Open tile from occupied workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 contains Panel One and the drawer shows Test Tile

Behavior basis: [UI-SRC-058:36](<../../repos/ui/mfe-base/src/components/AppBar/common/useController.ts#L36>)

```gherkin
@UI-SHL-018 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Open tile from occupied workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 contains Panel One and the drawer shows Test Tile
    When click Test Tile
    Then two tabs exist
    And the new tab is selected
    And Panel One remains available in W1
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-019

**Open same tile twice**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 already contains Test Tile

Behavior basis: [UI-SRC-058:36](<../../repos/ui/mfe-base/src/components/AppBar/common/useController.ts#L36>); [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-SHL-019 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Open same tile twice
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 already contains Test Tile
    When open Test Tile again through the drawer
    Then two Test Tile Demo tabs exist
    And the newly added tab is selected
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-020

**Show refresh only for registered active tab**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 registers a refresh callback and W2 does not

Behavior basis: [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>); [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-020 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Show refresh only for registered active tab
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 registers a refresh callback and W2 does not
    When select W1
    Then W1 shows one refresh control
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-021

**Hide refresh for unregistered workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W2 has no registered refresh callback

Behavior basis: [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>); [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-021 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Hide refresh for unregistered workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W2 has no registered refresh callback
    When select W2
    Then W2 has no refresh control
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-022

**Refresh active workspace without adding tabs**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 refresh callback changes visible data from Version 1 to Version 2

Behavior basis: [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>); [UI-SRC-112:10](<../../repos/ui/mfe-base/src/pages/Home/common/util.ts#L10>)

```gherkin
@UI-SHL-022 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Refresh active workspace without adding tabs
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 refresh callback changes visible data from Version 1 to Version 2
    When click W1 refresh
    Then W1 shows Version 2
    And the workspace count is unchanged
    And W1 remains selected
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-023

**Preserve authorized restored workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. saved W1 refers to T-GLOBAL and UI-USER-01 has its matching entity and subject

Behavior basis: [UI-SRC-118:291](<../../repos/ui/mfe-base/src/utils/common.ts#L291>); [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-023 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Preserve authorized restored workspace
    Given saved W1 refers to T-GLOBAL and UI-USER-01 has its matching entity and subject
    When load the shell
    Then the restored W1 tab and /tile-global content are available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-024

**Remove restored workspace after access removal**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. saved W1 refers to a tile without matching user entity or subject; saved W2 is empty

Behavior basis: [UI-SRC-118:291](<../../repos/ui/mfe-base/src/utils/common.ts#L291>); [UI-SRC-109:36](<../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36>)

```gherkin
@UI-SHL-024 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Remove restored workspace after access removal
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And saved W1 refers to a tile without matching user entity or subject; saved W2 is empty
    When load the shell
    Then W1 is absent
    And W2 remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-025

**Replace wholly invalid restored workspaces**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. all saved workspaces refer to removed tiles

Behavior basis: [UI-SRC-118:291](<../../repos/ui/mfe-base/src/utils/common.ts#L291>)

```gherkin
@UI-SHL-025 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Replace wholly invalid restored workspaces
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And all saved workspaces refer to removed tiles
    When load the shell
    Then exactly one empty workspace is shown
    And Find tile is available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-026

**Restore template workspace**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. saved W1 refers to a catalog tile with isTemplate true and no matching entitlement

Behavior basis: [UI-SRC-118:291](<../../repos/ui/mfe-base/src/utils/common.ts#L291>)

```gherkin
@UI-SHL-026 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Restore template workspace
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And saved W1 refers to a catalog tile with isTemplate true and no matching entitlement
    When load the shell
    Then W1 remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-027

**Show Indonesia marker on workspace tab**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 first container has entryName Indonesia

Behavior basis: [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-027 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Show Indonesia marker on workspace tab
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 first container has entryName Indonesia
    When select W1
    Then W1 tab shows an image with alt text Indonesia icon
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-SHL-028

**Omit Indonesia marker for Global tab**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 first container has entryName Global

Behavior basis: [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UI-SHL-028 @IMPLEMENTATION
Feature: Workspaces
  Scenario: Omit Indonesia marker for Global tab
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 first container has entryName Global
    When select W1
    Then W1 tab has no Indonesia icon
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Tile catalog

<a id="group-tile-catalog"></a>

#### UI-CAT-001

**Open drawer from application bar**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the drawer is closed

Behavior basis: [UI-SRC-059:18](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L18>); [UI-SRC-066:9](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L9>)

```gherkin
@UI-CAT-001 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Open drawer from application bar
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the drawer is closed
    When activate New Tile
    Then Tile Options is visible in the right drawer
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-002

**Close drawer without selecting a tile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. Tile Options is open

Behavior basis: [UI-SRC-066:9](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L9>)

```gherkin
@UI-CAT-002 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Close drawer without selecting a tile
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And Tile Options is open
    When click outside the drawer
    Then Tile Options closes
    And no workspace is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-003

**Render categories and labels**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. catalog categories Settlement and Confirmations each contain one tile

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>)

```gherkin
@UI-CAT-003 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Render categories and labels
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And catalog categories Settlement and Confirmations each contain one tile
    When open Tile Options
    Then Settlement is visible
    And Confirmations is visible
    And each category shows its fixture tile title
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-004

**Combine regional entries into one card**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL and T-ID have identical title Test Tile and subtitle Demo

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>)

```gherkin
@UI-CAT-004 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Combine regional entries into one card
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL and T-ID have identical title Test Tile and subtitle Demo
    When open Tile Options
    Then exactly one Test Tile card is shown
    And the card shows Global and Indonesia entry buttons
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-005

**Keep distinct subtitles in separate cards**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. two Test Tile records have subtitles Demo and Live

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>)

```gherkin
@UI-CAT-005 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Keep distinct subtitles in separate cards
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And two Test Tile records have subtitles Demo and Live
    When open Tile Options
    Then two Test Tile cards show distinct Demo and Live subtitles
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-006

**Prefer Global as card default**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-ID precedes T-GLOBAL in the same group

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-065:6](<../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L6>)

```gherkin
@UI-CAT-006 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Prefer Global as card default
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-ID precedes T-GLOBAL in the same group
    When click the Test Tile card body
    Then the controlled container displays /tile-global
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-007

**Use first entry when Global is absent**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. two grouped entries have entryName Indonesia and Singapore, in that order

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-065:6](<../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L6>)

```gherkin
@UI-CAT-007 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Use first entry when Global is absent
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And two grouped entries have entryName Indonesia and Singapore, in that order
    When click the Test Tile card body
    Then the controlled container displays the Indonesia entry tile identifier
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-008

**Launch explicit Indonesia entry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL and T-ID share one card

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>); [UI-SRC-065:6](<../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L6>)

```gherkin
@UI-CAT-008 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Launch explicit Indonesia entry
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL and T-ID share one card
    When click its Indonesia entry button
    Then the controlled container displays /tile-id
    And exactly one workspace opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-009

**Trim regional display labels**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-ID has entryName with surrounding spaces

Behavior basis: [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-009 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Trim regional display labels
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-ID has entryName with surrounding spaces
    When open Tile Options
    Then the entry button text is Indonesia
    And the entry icon alt text is Indonesia icon
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-010

**Recognize Global case without changing displayed case**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. one grouped entry uses entryName gLoBaL

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-010 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Recognize Global case without changing displayed case
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And one grouped entry uses entryName gLoBaL
    When click the card body
    Then the controlled container displays that Global entry tile identifier
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-011

**Hide metadata on a single unnamed entry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. one tile has entryName null

Behavior basis: [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-011 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Hide metadata on a single unnamed entry
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And one tile has entryName null
    When open Tile Options
    Then its card shows an add button
    And the button has no regional name or icon
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-012

**Show metadata for several unnamed entries**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. two grouped entries both have entryName null

Behavior basis: [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-012 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Show metadata for several unnamed entries
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And two grouped entries both have entryName null
    When open Tile Options
    Then the grouped card shows two separate add buttons
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-013

**Disable a fully unavailable group**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. every entry in the Test Tile group has disabled true

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-013 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Disable a fully unavailable group
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And every entry in the Test Tile group has disabled true
    When click the disabled card body
    And attempt to activate each disabled entry button
    Then no workspace opens
    And all entry buttons are disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-014

**Disable only an unavailable regional entry**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL is enabled and T-ID is disabled

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-014 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Disable only an unavailable regional entry
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL is enabled and T-ID is disabled
    When open Tile Options
    Then Global is enabled
    And Indonesia is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-015

**Entry click does not bubble into default launch**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. Global and Indonesia are enabled in one card

Behavior basis: [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-015 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Entry click does not bubble into default launch
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And Global and Indonesia are enabled in one card
    When click Indonesia
    Then only /tile-id opens
    And no /tile-global workspace is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-016

**Show tile image for active theme**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. Test Tile supplies dark and light image paths

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-CAT-016 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Show tile image for active theme
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And Test Tile supplies dark and light image paths
    When switch from dark to light theme
    And open Tile Options
    Then the Test Tile card uses the light image path
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-017

**Fallback to dark image when light image is absent**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. Test Tile supplies only imageDarkTheme

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>)

```gherkin
@UI-CAT-017 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Fallback to dark image when light image is absent
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And Test Tile supplies only imageDarkTheme
    When open the drawer in light theme
    Then the Test Tile card uses imageDarkTheme
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-018

**Transfer tile parameters to container**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL has parameters {"desk":"SG","includeClosed":false}

Behavior basis: [UI-SRC-065:6](<../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L6>); [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>)

```gherkin
@UI-CAT-018 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Transfer tile parameters to container
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL has parameters {"desk":"SG","includeClosed":false}
    When open T-GLOBAL
    Then the test container displays desk SG and includeClosed false
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-019

**Use empty parameters when omitted**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL has no parameters

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>)

```gherkin
@UI-CAT-019 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Use empty parameters when omitted
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL has no parameters
    When open T-GLOBAL
    Then the test container displays an empty parameter object
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-CAT-020

**Show empty drawer without invented tiles**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the catalog has no categories

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-066:9](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L9>)

```gherkin
@UI-CAT-020 @IMPLEMENTATION
Feature: Tile catalog
  Scenario: Show empty drawer without invented tiles
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the catalog has no categories
    When open Tile Options
    Then Tile Options remains visible
    And no tile cards are shown
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Module composition

<a id="group-module-composition"></a>

#### UI-MFE-001

**Show loading splash during module load**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the test container import is held pending

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>)

```gherkin
@UI-MFE-001 @IMPLEMENTATION
Feature: Module composition
  Scenario: Show loading splash during module load
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the test container import is held pending
    When open Test Tile
    Then the selected panel shows the splash until the import resolves
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-002

**Replace splash after module load**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the test container import is pending in W1

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>)

```gherkin
@UI-MFE-002 @IMPLEMENTATION
Feature: Module composition
  Scenario: Replace splash after module load
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the test container import is pending in W1
    When resolve the controlled import
    Then W1 shows the controlled container marker
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-003

**Contain a module import failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the Test Tile import rejects with fixture error MODULE-LOAD-01

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-069:10](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L10>)

```gherkin
@UI-MFE-003 @IMPLEMENTATION
Feature: Module composition
  Scenario: Contain a module import failure
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the Test Tile import rejects with fixture error MODULE-LOAD-01
    When open Test Tile
    Then the panel shows There is a problem in this Tile
    And the application bar remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-004

**Contain a render exception**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the test container throws fixture error RENDER-01

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-069:10](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L10>)

```gherkin
@UI-MFE-004 @IMPLEMENTATION
Feature: Module composition
  Scenario: Contain a render exception
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the test container throws fixture error RENDER-01
    When open Test Tile
    Then the panel shows There is a problem in this Tile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-005

**Offer configured support contact**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the failed tile has emailSupport support@example.test

Behavior basis: [UI-SRC-069:10](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L10>)

```gherkin
@UI-MFE-005 @IMPLEMENTATION
Feature: Module composition
  Scenario: Offer configured support contact
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the failed tile has emailSupport support@example.test
    When inspect its fallback
    Then Contact PSS is visible
    And its mailto target begins mailto:support@example.test
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-006

**Omit absent support contact**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the failed tile and current workspace have no support email

Behavior basis: [UI-SRC-069:10](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L10>); [UI-SRC-068:5](<../../repos/ui/mfe-base/src/components/FallbackError/common/useController.ts#L5>)

```gherkin
@UI-MFE-006 @IMPLEMENTATION
Feature: Module composition
  Scenario: Omit absent support contact
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the failed tile and current workspace have no support email
    When inspect its fallback
    Then Contact PSS is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-007

**Keep another tile usable after failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. W1 shows tile fallback and W2 contains Panel Two

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-114:32](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L32>)

```gherkin
@UI-MFE-007 @IMPLEMENTATION
Feature: Module composition
  Scenario: Keep another tile usable after failure
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And W1 shows tile fallback and W2 contains Panel Two
    When select W2
    Then Panel Two is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-008

**Open Import Map admin module internally**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. an enabled admin tile uses @fm/base and module /importmap

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-045:10](<../../repos/ui/mfe-base/src/admin/Routing.tsx#L10>)

```gherkin
@UI-MFE-008 @IMPLEMENTATION
Feature: Module composition
  Scenario: Open Import Map admin module internally
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And an enabled admin tile uses @fm/base and module /importmap
    When open the admin tile
    Then Create New Import Map is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-009

**Open Category admin module internally**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. an enabled admin tile uses @fm/base and module /category

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-045:10](<../../repos/ui/mfe-base/src/admin/Routing.tsx#L10>)

```gherkin
@UI-MFE-009 @IMPLEMENTATION
Feature: Module composition
  Scenario: Open Category admin module internally
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And an enabled admin tile uses @fm/base and module /category
    When open the admin tile
    Then Create New Category is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-010

**Open Tile admin module internally**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. an enabled admin tile uses @fm/base and module /tile

Behavior basis: [UI-SRC-107:7](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L7>); [UI-SRC-045:10](<../../repos/ui/mfe-base/src/admin/Routing.tsx#L10>)

```gherkin
@UI-MFE-010 @IMPLEMENTATION
Feature: Module composition
  Scenario: Open Tile admin module internally
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And an enabled admin tile uses @fm/base and module /tile
    When open the admin tile
    Then Application Category and Create New Tile are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-011

**Open authorized URL tile with parameters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the catalog contains T-GLOBAL and the URL specifies its container, module, tile, and parameters {"desk":"SG"} Mount useParameters in a controlled integration fixture. The inspected production Home component does not call this hook.

Behavior basis: [UI-SRC-111:12](<../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L12>)

```gherkin
@UI-MFE-011 @PROPOSED
Feature: Module composition
  Scenario: Open authorized URL tile with parameters
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the catalog contains T-GLOBAL and the URL specifies its container, module, tile, and parameters {"desk":"SG"}
    When load that URL
    Then the test container displays desk SG
    And the browser address is replaced with /
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Conditional hook-integration probe. Current Home does not call useParameters. This is not a prediction of default shell routing. Owner unknown; confirm supported URL launch before acceptance.

#### UI-MFE-012

**Reject unauthorized URL tile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the URL references a catalog tile without user entity and subject access Mount useParameters in a controlled integration fixture. The inspected production Home component does not call this hook.

Behavior basis: [UI-SRC-111:12](<../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L12>)

```gherkin
@UI-MFE-012 @PROPOSED
Feature: Module composition
  Scenario: Reject unauthorized URL tile
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the URL references a catalog tile without user entity and subject access
    When load that URL
    Then no workspace for that tile opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Conditional hook-integration probe. Current Home does not call useParameters. This is not a prediction of default shell routing. Owner unknown; confirm supported URL launch before acceptance.

#### UI-MFE-013

**Open externally requested entitled trade tile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. FDC3 is enabled and an entitled /trade fixture tile exists

Behavior basis: [UI-SRC-110:46](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L46>); [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-MFE-013 @IMPLEMENTATION
Feature: Module composition
  Scenario: Open externally requested entitled trade tile
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And FDC3 is enabled and an entitled /trade fixture tile exists
    When send scb.ViewLaunch with scb.fmptp.trade.query and tradeId TR-001
    Then the test tile displays ViewTradeDetails and tradeId TR-001
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-014

**Open externally requested cashflow filters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. FDC3 is enabled and an entitled /cashflow_cn fixture tile exists

Behavior basis: [UI-SRC-110:46](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L46>); [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-MFE-014 @IMPLEMENTATION
Feature: Module composition
  Scenario: Open externally requested cashflow filters
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And FDC3 is enabled and an entitled /cashflow_cn fixture tile exists
    When send scb.ViewLaunch with scb.fmptp.cashflows and tradeId TR-001
    Then the test tile displays filter field Trade_Id, operator EQ, and value TR-001
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-MFE-015

**Show unauthorized external launch error**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. FDC3 is enabled and /trade is absent from the catalog

Behavior basis: [UI-SRC-110:46](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L46>); [UI-SRC-097:99](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L99>)

```gherkin
@UI-MFE-015 @IMPLEMENTATION
Feature: Module composition
  Scenario: Show unauthorized external launch error
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And FDC3 is enabled and /trade is absent from the catalog
    When send scb.ViewLaunch for tradeId TR-001
    Then the shell shows Tile trade is unauthorized or does not exist
    And no trade workspace opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Preferences and profile

<a id="group-preferences-and-profile"></a>

#### UI-PREF-001

**Switch shell theme to light**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the shell uses dark theme

Behavior basis: [UI-SRC-078:22](<../../repos/ui/mfe-base/src/components/Switch/common/useController.ts#L22>); [UI-SRC-059:18](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L18>)

```gherkin
@UI-PREF-001 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Switch shell theme to light
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the shell uses dark theme
    When activate the theme switch
    Then the shell uses light theme
    And the application bar uses the light logo asset
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-002

**Restore saved theme**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. light theme was selected and fixture storage is retained

Behavior basis: [UI-SRC-078:22](<../../repos/ui/mfe-base/src/components/Switch/common/useController.ts#L22>)

```gherkin
@UI-PREF-002 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Restore saved theme
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And light theme was selected and fixture storage is retained
    When reload the shell
    Then light theme remains selected
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-003

**Switch clock from UTC to local**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the controlled time is 2026-10-22T00:05:00Z and browser timezone is Asia/Singapore; clock mode is UTC

Behavior basis: [UI-SRC-080:13](<../../repos/ui/mfe-base/src/components/SwitchTime/common/useController.ts#L13>)

```gherkin
@UI-PREF-003 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Switch clock from UTC to local
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the controlled time is 2026-10-22T00:05:00Z and browser timezone is Asia/Singapore; clock mode is UTC
    When activate the clock switch
    Then the application bar clock shows 08:05 Local
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-004

**Switch clock from local to UTC**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the controlled time is 2026-10-22T00:05:00Z and browser timezone is Asia/Singapore; clock mode is local

Behavior basis: [UI-SRC-080:13](<../../repos/ui/mfe-base/src/components/SwitchTime/common/useController.ts#L13>)

```gherkin
@UI-PREF-004 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Switch clock from local to UTC
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the controlled time is 2026-10-22T00:05:00Z and browser timezone is Asia/Singapore; clock mode is local
    When activate the clock switch
    Then the application bar clock shows 00:05 UTC
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-005

**Update minute display**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. the real interval is controlled and initial time is 2026-10-22T00:05:00Z

Behavior basis: [UI-SRC-080:13](<../../repos/ui/mfe-base/src/components/SwitchTime/common/useController.ts#L13>)

```gherkin
@UI-PREF-005 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Update minute display
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And the real interval is controlled and initial time is 2026-10-22T00:05:00Z
    When advance the controlled clock 60 seconds
    Then the UTC application bar clock shows 00:06 UTC
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-006

**Show user profile identity**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. UI-USER-01 has fullName Test User, OUD userId U001, title Analyst, emailId ui@example.test, and country SG

Behavior basis: [UI-SRC-072:142](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L142>)

```gherkin
@UI-PREF-006 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Show user profile identity
    Given UI-USER-01 has fullName Test User, OUD userId U001, title Analyst, emailId ui@example.test, and country SG
    When click the avatar with tooltip User Profiles
    And click Click to view user profile details
    Then the profile displays Test User, U001, Analyst, ui@example.test, and SG
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-007

**Separate data entitlement profile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. entities include RATAN_DATA_ENTITLEMENT and FMO PORTAL ADMIN

Behavior basis: [UI-SRC-072:142](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L142>)

```gherkin
@UI-PREF-007 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Separate data entitlement profile
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And entities include RATAN_DATA_ENTITLEMENT and FMO PORTAL ADMIN
    When click the avatar with tooltip User Profiles
    And click Click to view user profile details
    Then Functional User Profile contains FMO PORTAL ADMIN
    And Entitlement User Profile contains RATAN_DATA_ENTITLEMENT
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-008

**Omit absent data entitlement section**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. entities contain FMO PORTAL ADMIN and no RATAN_DATA_ENTITLEMENT

Behavior basis: [UI-SRC-072:142](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L142>)

```gherkin
@UI-PREF-008 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Omit absent data entitlement section
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And entities contain FMO PORTAL ADMIN and no RATAN_DATA_ENTITLEMENT
    When click the avatar with tooltip User Profiles
    And click Click to view user profile details
    Then Entitlement User Profile is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-PREF-009

**Expand role subjects and actions**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. entity Test Entity has applicationName Test App, roleName Viewer, subject Test Subject, and entitlement action READ

Behavior basis: [UI-SRC-072:75](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L75>)

```gherkin
@UI-PREF-009 @IMPLEMENTATION
Feature: Preferences and profile
  Scenario: Expand role subjects and actions
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And entity Test Entity has applicationName Test App, roleName Viewer, subject Test Subject, and entitlement action READ
    When click the avatar with tooltip User Profiles
    And click Click to view user profile details
    And expand Test App :: Test Entity :: Viewer
    And expand Test Subject
    Then the profile shows Action: and a READ chip
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Administration: Category

<a id="group-administration-category"></a>

#### UI-ADM-CAT-001

**Render Category grid fields**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-CAT-001 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Render Category grid fields
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When inspect the grid
    Then the grid exposes columns Category Label, Owner, Verified?, Order No
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-002

**Open new Category form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-CAT-002 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Open new Category form
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When click Create New Category
    Then a new-record dialog is visible
    And Create, Reset, and Close are visible
    And Verified? is false
    And Created By and Updated By show UI-ADMIN-01
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-003

**Create Category with returned values**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the create response is a record with applicationCategoryId 102 and Category Label Changed Category

Behavior basis: [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-053:1](<../../repos/ui/mfe-base/src/admin/common/utils/category.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-CAT-003 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Create Category with returned values
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the create response is a record with applicationCategoryId 102 and Category Label Changed Category
    When click Create New Category
    And populate the new form using the complete admin fixture record
    And set Category Label to Changed Category
    And advance the controlled field propagation clock by 300 milliseconds
    And click Create
    Then the grid shows exactly one record with Record Id 102 and Category Label Changed Category
    And the create dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-004

**Open Category edit dialog**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-CAT-004 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Open Category edit dialog
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When click Edit on record 101
    Then the edit dialog shows Category Label Fixture Category
    And Update, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-005

**Update Category without adding a row**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the update response returns record 101 with Category Label Changed Category

Behavior basis: [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-053:1](<../../repos/ui/mfe-base/src/admin/common/utils/category.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-CAT-005 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Update Category without adding a row
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the update response returns record 101 with Category Label Changed Category
    When click Edit on record 101
    And set Category Label to Changed Category
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then record 101 shows Category Label Changed Category
    And the grid row count is unchanged
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-006

**Enable Verify for inactive Category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-CAT-006 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Enable Verify for inactive Category
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When inspect record 101 actions
    Then Verify is enabled
    And Deactivate is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-007

**Enable Deactivate for active Category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-CAT-007 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Enable Deactivate for active Category
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER
    When inspect record 101 actions
    Then Verify is disabled
    And Deactivate is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-008

**Open Category verification mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-CAT-008 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Open Category verification mode
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When click Verify on record 101
    Then Category Label is disabled
    And Verified, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-009

**Show verified Category response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the verify response returns record 101 with active true

Behavior basis: [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-053:1](<../../repos/ui/mfe-base/src/admin/common/utils/category.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-CAT-009 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Show verified Category response
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the verify response returns record 101 with active true
    When click Verify on record 101
    And click Verified
    Then record 101 shows Verified? as true
    And Verify is disabled for record 101
    And Deactivate is enabled for record 101
    And the verification dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-010

**Open Category deactivation mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-CAT-010 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Open Category deactivation mode
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER
    When click Deactivate on record 101
    Then Category Label is disabled
    And Deactivate, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-011

**Show deactivated Category response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER; the deactivate response returns record 101 with active false

Behavior basis: [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-053:1](<../../repos/ui/mfe-base/src/admin/common/utils/category.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-CAT-011 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Show deactivated Category response
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Category Label Fixture Category; its owner is TEST_OWNER; the deactivate response returns record 101 with active false
    When click Deactivate on record 101
    And click Deactivate in the record dialog
    Then record 101 shows Verified? as false
    And Verify is enabled for record 101
    And Deactivate is disabled for record 101
    And the deactivation dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-012

**Close Category edit without saving**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the edit dialog has unsaved Category Label Changed Category

Behavior basis: [UI-SRC-037:12](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L12>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-CAT-012 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Close Category edit without saving
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the edit dialog has unsaved Category Label Changed Category
    When click Close
    Then the grid still shows record 101 with Category Label Fixture Category
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-013

**Use read-only metadata in Category form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-CAT-013 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Use read-only metadata in Category form
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER
    When open Edit on record 101
    Then Record Id, Created At, Created By, Updated At, Updated By, and Verified? are disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-CAT-014

**Load Category audit history**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the audit response contains audit IDs 9001 and 9002 for applicationCategoryId 101

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-052:10](<../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L10>)

```gherkin
@UI-ADM-CAT-014 @IMPLEMENTATION
Feature: Administration: Category
  Scenario: Load Category audit history
    Given the Category admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Category Label Fixture Category; its owner is TEST_OWNER; the audit response contains audit IDs 9001 and 9002 for applicationCategoryId 101
    When click Audit on record 101
    Then Audit dialog is visible
    And audit rows 9001 and 9002 are shown
    And both rows refer to record 101
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Administration: Import Map

<a id="group-administration-import-map"></a>

#### UI-ADM-MAP-001

**Render Import Map grid fields**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-MAP-001 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Render Import Map grid fields
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When inspect the grid
    Then the grid exposes columns Module Name, Path, Owner, Verified?
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-002

**Open new Import Map form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-MAP-002 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Open new Import Map form
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When click Create New Import Map
    Then a new-record dialog is visible
    And Create, Reset, and Close are visible
    And Verified? is false
    And Created By and Updated By show UI-ADMIN-01
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-003

**Create Import Map with returned values**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the create response is a record with importMapId 102 and Path https://assets.example.test/v2.js

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-054:1](<../../repos/ui/mfe-base/src/admin/common/utils/importmap.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-MAP-003 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Create Import Map with returned values
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the create response is a record with importMapId 102 and Path https://assets.example.test/v2.js
    When click Create New Import Map
    And populate the new form using the complete admin fixture record
    And set Path to https://assets.example.test/v2.js
    And advance the controlled field propagation clock by 300 milliseconds
    And click Create
    Then the grid shows exactly one record with Record Id 102 and Path https://assets.example.test/v2.js
    And the create dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-004

**Open Import Map edit dialog**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-MAP-004 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Open Import Map edit dialog
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When click Edit on record 101
    Then the edit dialog shows Path https://assets.example.test/v1.js
    And Update, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-005

**Update Import Map without adding a row**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the update response returns record 101 with Path https://assets.example.test/v2.js

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-054:1](<../../repos/ui/mfe-base/src/admin/common/utils/importmap.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-MAP-005 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Update Import Map without adding a row
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the update response returns record 101 with Path https://assets.example.test/v2.js
    When click Edit on record 101
    And set Path to https://assets.example.test/v2.js
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then record 101 shows Path https://assets.example.test/v2.js
    And the grid row count is unchanged
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-006

**Enable Verify for inactive Import Map**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-MAP-006 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Enable Verify for inactive Import Map
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When inspect record 101 actions
    Then Verify is enabled
    And Deactivate is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-007

**Enable Deactivate for active Import Map**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-MAP-007 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Enable Deactivate for active Import Map
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When inspect record 101 actions
    Then Verify is disabled
    And Deactivate is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-008

**Open Import Map verification mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-MAP-008 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Open Import Map verification mode
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When click Verify on record 101
    Then Path is disabled
    And Verified, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-009

**Show verified Import Map response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the verify response returns record 101 with active true

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-054:1](<../../repos/ui/mfe-base/src/admin/common/utils/importmap.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-MAP-009 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Show verified Import Map response
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the verify response returns record 101 with active true
    When click Verify on record 101
    And click Verified
    Then record 101 shows Verified? as true
    And Verify is disabled for record 101
    And Deactivate is enabled for record 101
    And the verification dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-010

**Open Import Map deactivation mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-MAP-010 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Open Import Map deactivation mode
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When click Deactivate on record 101
    Then Path is disabled
    And Deactivate, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-011

**Show deactivated Import Map response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the deactivate response returns record 101 with active false

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-054:1](<../../repos/ui/mfe-base/src/admin/common/utils/importmap.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-MAP-011 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Show deactivated Import Map response
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the deactivate response returns record 101 with active false
    When click Deactivate on record 101
    And click Deactivate in the record dialog
    Then record 101 shows Verified? as false
    And Verify is enabled for record 101
    And Deactivate is disabled for record 101
    And the deactivation dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-012

**Close Import Map edit without saving**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the edit dialog has unsaved Path https://assets.example.test/v2.js

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-MAP-012 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Close Import Map edit without saving
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the edit dialog has unsaved Path https://assets.example.test/v2.js
    When click Close
    Then the grid still shows record 101 with Path https://assets.example.test/v1.js
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-013

**Use read-only metadata in Import Map form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER

Behavior basis: [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-MAP-013 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Use read-only metadata in Import Map form
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER
    When open Edit on record 101
    Then Record Id, Created At, Created By, Updated At, Updated By, and Verified? are disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-MAP-014

**Load Import Map audit history**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the audit response contains audit IDs 9001 and 9002 for importMapId 101

Behavior basis: [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-052:10](<../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L10>)

```gherkin
@UI-ADM-MAP-014 @IMPLEMENTATION
Feature: Administration: Import Map
  Scenario: Load Import Map audit history
    Given the Import Map admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Path https://assets.example.test/v1.js; its owner is TEST_OWNER; the audit response contains audit IDs 9001 and 9002 for importMapId 101
    When click Audit on record 101
    Then Audit dialog is visible
    And audit rows 9001 and 9002 are shown
    And both rows refer to record 101
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Administration: Tile

<a id="group-administration-tile"></a>

#### UI-ADM-TIL-001

**Render Tile grid fields**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-TIL-001 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Render Tile grid fields
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When inspect the grid
    Then the grid exposes columns Tile Name, Description, Container, Module Path, Tile Path, Entry Name
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-002

**Open new Tile form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-TIL-002 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Open new Tile form
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When click Create New Tile
    Then a new-record dialog is visible
    And Create, Reset, and Close are visible
    And Verified? is false
    And Created By and Updated By show UI-ADMIN-01
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-003

**Create Tile with returned values**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the create response is a record with applicationTileId 102 and Tile Name Changed Tile

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-056:1](<../../repos/ui/mfe-base/src/admin/common/utils/tile.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-TIL-003 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Create Tile with returned values
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the create response is a record with applicationTileId 102 and Tile Name Changed Tile
    When click Create New Tile
    And populate the new form using the complete admin fixture record
    And set Tile Name to Changed Tile
    And advance the controlled field propagation clock by 300 milliseconds
    And click Create
    Then the grid shows exactly one record with Record Id 102 and Tile Name Changed Tile
    And the create dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-004

**Open Tile edit dialog**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-TIL-004 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Open Tile edit dialog
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When click Edit on record 101
    Then the edit dialog shows Tile Name Fixture Tile
    And Update, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-005

**Update Tile without adding a row**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the update response returns record 101 with Tile Name Changed Tile

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-056:1](<../../repos/ui/mfe-base/src/admin/common/utils/tile.ts#L1>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-TIL-005 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Update Tile without adding a row
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the update response returns record 101 with Tile Name Changed Tile
    When click Edit on record 101
    And set Tile Name to Changed Tile
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then record 101 shows Tile Name Changed Tile
    And the grid row count is unchanged
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-006

**Enable Verify for inactive Tile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-TIL-006 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Enable Verify for inactive Tile
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When inspect record 101 actions
    Then Verify is enabled
    And Deactivate is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-007

**Enable Deactivate for active Tile**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-TIL-007 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Enable Deactivate for active Tile
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When inspect record 101 actions
    Then Verify is disabled
    And Deactivate is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-008

**Open Tile verification mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-TIL-008 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Open Tile verification mode
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When click Verify on record 101
    Then Tile Name is disabled
    And Verified, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-009

**Show verified Tile response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the verify response returns record 101 with active true

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-056:1](<../../repos/ui/mfe-base/src/admin/common/utils/tile.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-TIL-009 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Show verified Tile response
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the verify response returns record 101 with active true
    When click Verify on record 101
    And click Verified
    Then record 101 shows Verified? as true
    And Verify is disabled for record 101
    And Deactivate is enabled for record 101
    And the verification dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-010

**Open Tile deactivation mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-TIL-010 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Open Tile deactivation mode
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When click Deactivate on record 101
    Then Tile Name is disabled
    And Deactivate, Reset, and Close are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-011

**Show deactivated Tile response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the deactivate response returns record 101 with active false

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-056:1](<../../repos/ui/mfe-base/src/admin/common/utils/tile.ts#L1>); [UI-SRC-051:9](<../../repos/ui/mfe-base/src/admin/common/Actions/index.tsx#L9>)

```gherkin
@UI-ADM-TIL-011 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Show deactivated Tile response
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is active and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the deactivate response returns record 101 with active false
    When click Deactivate on record 101
    And click Deactivate in the record dialog
    Then record 101 shows Verified? as false
    And Verify is enabled for record 101
    And Deactivate is disabled for record 101
    And the deactivation dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-012

**Close Tile edit without saving**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the edit dialog has unsaved Tile Name Changed Tile

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>); [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-TIL-012 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Close Tile edit without saving
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the edit dialog has unsaved Tile Name Changed Tile
    When click Close
    Then the grid still shows record 101 with Tile Name Fixture Tile
    And the edit dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-013

**Use read-only metadata in Tile form**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-TIL-013 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Use read-only metadata in Tile form
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected
    When open Edit on record 101
    Then Record Id, Created At, Created By, Updated At, Updated By, and Verified? are disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-TIL-014

**Load Tile audit history**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN role TEST_OWNER.

Setup: Apply the shared fixture definitions. the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the audit response contains audit IDs 9001 and 9002 for applicationTileId 101

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-052:10](<../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L10>)

```gherkin
@UI-ADM-TIL-014 @IMPLEMENTATION
Feature: Administration: Tile
  Scenario: Load Tile audit history
    Given the Tile admin screen is open for UI-ADMIN-01; fixture record 101 is inactive and has Tile Name Fixture Tile; its owner is TEST_OWNER; Application Category Fixture Category is selected; the audit response contains audit IDs 9001 and 9002 for applicationTileId 101
    When click Audit on record 101
    Then Audit dialog is visible
    And audit rows 9001 and 9002 are shown
    And both rows refer to record 101
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Administration fields

<a id="group-administration-fields"></a>

#### UI-ADM-FLD-001

**Preserve category ordering value**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 has a Category create dialog; response record 102 contains orderNo 7

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-053:1](<../../repos/ui/mfe-base/src/admin/common/utils/category.ts#L1>)

```gherkin
@UI-ADM-FLD-001 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Preserve category ordering value
    Given UI-ADMIN-01 has a Category create dialog; response record 102 contains orderNo 7
    When click Create New Category
    And enter Category Label Fixture Category
    And enter Order No 7
    And advance the controlled field propagation clock by 300 milliseconds
    And click Create
    Then record 102 displays Order No 7
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-002

**Use admin owner by default**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 has FMO PORTAL ADMIN role TEST_OWNER

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-FLD-002 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Use admin owner by default
    Given UI-ADMIN-01 has FMO PORTAL ADMIN role TEST_OWNER
    When open a new Category form
    Then Owner displays TEST_OWNER
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-003

**Restrict Owner for ordinary admin**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 has role TEST_OWNER and record 101 is visible

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-FLD-003 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Restrict Owner for ordinary admin
    Given UI-ADMIN-01 has role TEST_OWNER and record 101 is visible
    When open Edit on record 101
    Then Owner is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-004

**Allow SUPER_USER to edit Owner**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-SUPER-01; FMO PORTAL ADMIN SUPER_USER.

Setup: Apply the shared fixture definitions. UI-SUPER-01 has FMO PORTAL ADMIN role SUPER_USER and record 101 is visible

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-FLD-004 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Allow SUPER_USER to edit Owner
    Given UI-SUPER-01 has FMO PORTAL ADMIN role SUPER_USER and record 101 is visible
    When open Edit on record 101
    Then Owner is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-005

**Retain new import map after no-result response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 has a new Import Map form with Module Name @fm/test and Path https://assets.example.test/v1.js; create returns an empty data object {}

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>)

```gherkin
@UI-ADM-FLD-005 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Retain new import map after no-result response
    Given UI-ADMIN-01 has a new Import Map form with Module Name @fm/test and Path https://assets.example.test/v1.js; create returns an empty data object {}
    When click Create after field propagation settles
    Then the new Import Map dialog remains open
    And no row for the fixture module is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-006

**Retain import map edit after no-result response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 is editing record 101; update returns an empty data object {}

Behavior basis: [UI-SRC-042:12](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L12>)

```gherkin
@UI-ADM-FLD-006 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Retain import map edit after no-result response
    Given UI-ADMIN-01 is editing record 101; update returns an empty data object {}
    When click Update after field propagation settles
    Then the Import Map edit dialog remains open
    And the original grid row remains unchanged
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-007

**Retain tile create after no-result response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 has a new Tile form; create returns an empty data object {}

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-ADM-FLD-007 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Retain tile create after no-result response
    Given UI-ADMIN-01 has a new Tile form; create returns an empty data object {}
    When click Create after field propagation settles
    Then the new Tile dialog remains open
    And no fixture tile row is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.

#### UI-ADM-FLD-008

**Retain tile edit after no-result response**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER unless SUPER_USER is named.

Setup: Apply the shared fixture definitions. UI-ADMIN-01 is editing Tile record 101; update returns an empty data object {}

Behavior basis: [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-ADM-FLD-008 @IMPLEMENTATION
Feature: Administration fields
  Scenario: Retain tile edit after no-result response
    Given UI-ADMIN-01 is editing Tile record 101; update returns an empty data object {}
    When click Update after field propagation settles
    Then the Tile edit dialog remains open
    And the original grid row remains unchanged
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Source-predicted UI behavior only. An empty response is controlled. Business acceptance is not established.
### Group: Tile administration filters

<a id="group-tile-administration-filters"></a>

#### UI-ADM-SEL-001

**Disable tile create without category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Tile admin is open with no category selected

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-049:14](<../../repos/ui/mfe-base/src/admin/Tile/index.tsx#L14>)

```gherkin
@UI-ADM-SEL-001 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Disable tile create without category
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Tile admin is open with no category selected
    When inspect its controls
    Then Create New Tile is disabled
    And refresh is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-002

**Expose All with several categories**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. category response contains Fixture Category and Other Category

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-SEL-002 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Expose All with several categories
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category response contains Fixture Category and Other Category
    When open Application Category options
    Then All, Fixture Category, and Other Category are available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-003

**Omit All for one category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. category response contains only Fixture Category

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-SEL-003 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Omit All for one category
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category response contains only Fixture Category
    When open Application Category options
    Then Fixture Category is available and All is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-004

**Allow tile create for concrete category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. category response contains Fixture Category

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-049:14](<../../repos/ui/mfe-base/src/admin/Tile/index.tsx#L14>)

```gherkin
@UI-ADM-SEL-004 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Allow tile create for concrete category
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category response contains Fixture Category
    When select Fixture Category
    Then Create New Tile is enabled
    And refresh is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-005

**Disable tile create for All**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. two categories exist

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-049:14](<../../repos/ui/mfe-base/src/admin/Tile/index.tsx#L14>)

```gherkin
@UI-ADM-SEL-005 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Disable tile create for All
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And two categories exist
    When select All
    Then Create New Tile is disabled
    And refresh is enabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-006

**Show selected category tile rows**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category response has Tile A only; Other Category response has Tile B only

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-SEL-006 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Show selected category tile rows
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category response has Tile A only; Other Category response has Tile B only
    When select Fixture Category
    Then Tile A is visible
    And Tile B is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-007

**Clear selected category and grid**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category is selected and Tile A is visible

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-SEL-007 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Clear selected category and grid
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category is selected and Tile A is visible
    And the new tile fetch after clearing is held pending
    When clear the Application Category input
    Then the category input is empty
    And Create New Tile is disabled
    And the displayed tile rows are cleared
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. The empty grid assertion applies only while the follow-up request is pending. A later response can replace rows.

#### UI-ADM-SEL-008

**Default new tile to selected category**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category is selected

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-ADM-SEL-008 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Default new tile to selected category
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category is selected
    When click Create New Tile
    Then the new Tile form shows Aplication Category Fixture Category
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-009

**Map container selection to referenced record**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. import map options contain @fm/test with importMapId 71; Tile create form is open

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-ADM-SEL-009 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Map container selection to referenced record
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And import map options contain @fm/test with importMapId 71; Tile create form is open
    When select Container @fm/test
    And advance the controlled field propagation clock by 300 milliseconds
    And click Create
    Then the new grid row shows Container @fm/test and Container Record Id 71
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-010

**Map category selection to referenced record**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. category options contain Fixture Category ID 81 and Other Category ID 82; Tile edit form is open

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-ADM-SEL-010 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Map category selection to referenced record
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category options contain Fixture Category ID 81 and Other Category ID 82; Tile edit form is open
    When select Aplication Category Other Category
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then the updated row refers to Aplication Category Record Id 82
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-011

**Set Is Template true**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Tile edit form is open with Is Template? false

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-SEL-011 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Set Is Template true
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Tile edit form is open with Is Template? false
    When select true in Is Template?
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then the updated grid row shows Is Template? true
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-012

**Set Is Template false**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Tile edit form is open with Is Template? true

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-SEL-012 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Set Is Template false
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Tile edit form is open with Is Template? true
    When select false in Is Template?
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    Then the updated grid row shows Is Template? false
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-SEL-013

**Preserve multiline role data**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Tile edit form is open and response preserves Role Entities lines ENTITY_A and ENTITY_B

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-SEL-013 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Preserve multiline role data
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Tile edit form is open and response preserves Role Entities lines ENTITY_A and ENTITY_B
    When enter Role Entities as two lines: ENTITY_A and ENTITY_B
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    And click Edit on the saved tile row
    Then the Role Entities input contains exactly ENTITY_A\nENTITY_B, where \n denotes one line break
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. This UI-only fixture accepts the supplied payload. It does not establish BFF validation; Filter Rule parsing has separate boundary cases.

#### UI-ADM-SEL-014

**Preserve multiline filter rule**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Tile edit form is open and controlled update preserves Filter Rule {"country":"SG"} on one line and {"desk":"OPS"} on another

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>)

```gherkin
@UI-ADM-SEL-014 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Preserve multiline filter rule
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Tile edit form is open and controlled update preserves Filter Rule {"country":"SG"} on one line and {"desk":"OPS"} on another
    When enter Filter Rule as two lines: {"country":"SG"} and {"desk":"OPS"}
    And advance the controlled field propagation clock by 300 milliseconds
    And click Update
    And click Edit on the saved tile row
    Then the Filter Rule input contains exactly {"country":"SG"}\n{"desk":"OPS"}, where \n denotes one line break
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. This UI-only fixture accepts the supplied payload. It does not establish BFF validation; Filter Rule parsing has separate boundary cases.

#### UI-ADM-SEL-015

**Refresh tile filter data**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category is selected and Tile A is visible; refreshed tile response contains Tile B only

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-049:14](<../../repos/ui/mfe-base/src/admin/Tile/index.tsx#L14>)

```gherkin
@UI-ADM-SEL-015 @IMPLEMENTATION
Feature: Tile administration filters
  Scenario: Refresh tile filter data
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category is selected and Tile A is visible; refreshed tile response contains Tile B only
    When click the Tile screen refresh control
    Then Tile B is visible
    And Tile A is absent
    And Fixture Category remains selected
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Administration grids and audits

<a id="group-administration-grids-and-audits"></a>

#### UI-ADM-GRD-001

**Use default grid page size**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category response contains records 101 through 125

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-GRD-001 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Use default grid page size
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category response contains records 101 through 125
    When open Category admin
    Then the first page contains 20 rows
    And five rows remain on the next page
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. Assert the pagination range and page-size control. Do not count virtualized DOM rows.

#### UI-ADM-GRD-002

**Change grid page size**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category response contains 75 rows

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-GRD-002 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Change grid page size
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category response contains 75 rows
    When select page size 50
    Then the first page contains 50 rows
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. Assert the pagination range and page-size control. Do not count virtualized DOM rows.

#### UI-ADM-GRD-003

**Navigate grid pages**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category response contains records 101 through 125 in ascending ID order

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-GRD-003 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Navigate grid pages
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category response contains records 101 through 125 in ascending ID order
    When select the second page
    Then records 121 through 125 are visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. Assert the pagination range and page-size control. Do not count virtualized DOM rows.

#### UI-ADM-GRD-004

**Use 100-row page size**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category response contains 105 rows

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-GRD-004 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Use 100-row page size
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category response contains 105 rows
    When select page size 100
    Then the first page contains 100 rows
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established. Assert the pagination range and page-size control. Do not count virtualized DOM rows.

#### UI-ADM-GRD-005

**Close audit and reopen another record**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. record 101 audit shows row 9001; record 102 audit response contains row 9002

Behavior basis: [UI-SRC-052:10](<../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L10>); [UI-SRC-035:8](<../../repos/ui/mfe-base/src/admin/Category/common/useAudit.tsx#L8>)

```gherkin
@UI-ADM-GRD-005 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Close audit and reopen another record
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And record 101 audit shows row 9001; record 102 audit response contains row 9002
    When close Audit
    And click Audit on record 102
    Then 9002 is visible
    And 9001 is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-GRD-006

**Keep grid selection separate from row opening**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category record 101 is visible

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>)

```gherkin
@UI-ADM-GRD-006 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Keep grid selection separate from row opening
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category record 101 is visible
    When click its Category Label cell
    Then no edit or verification dialog opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-GRD-007

**Use disabled action buttons during save**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category Create is pending in a controlled response

Behavior basis: [UI-SRC-086:22](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L22>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-ADM-GRD-007 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Use disabled action buttons during save
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category Create is pending in a controlled response
    When inspect the create dialog
    Then Create is in loading state
    And Reset and Close are in loading state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-GRD-008

**Apply UTC display to admin dates**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. clock mode is UTC; record updatedAt is 2026-10-22T00:05:00Z

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-GRD-008 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Apply UTC display to admin dates
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And clock mode is UTC; record updatedAt is 2026-10-22T00:05:00Z
    When open the admin record grid
    Then Updated At displays the fixture instant in UTC
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.

#### UI-ADM-GRD-009

**Update admin dates with local mode**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. browser timezone is Asia/Singapore; record updatedAt is 2026-10-22T00:05:00Z and clock mode is UTC

Behavior basis: [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-ADM-GRD-009 @IMPLEMENTATION
Feature: Administration grids and audits
  Scenario: Update admin dates with local mode
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And browser timezone is Asia/Singapore; record updatedAt is 2026-10-22T00:05:00Z and clock mode is UTC
    When switch the clock mode to local
    Then Updated At displays the fixture instant as 08:05 local time
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Implementation-derived regression expectation. Business approval and deployed parity are not established.
### Group: Proposed source-risk coverage

<a id="group-proposed-source-risk-coverage"></a>

#### UI-RISK-001

**Do not launch a disabled Global default**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. T-GLOBAL is disabled and T-ID is enabled in one card

Behavior basis: [UI-SRC-064:19](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L19>); [UI-SRC-092:25](<../../repos/ui/mfe-base/src/components/Tile/index.tsx#L25>)

```gherkin
@UI-RISK-001 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Do not launch a disabled Global default
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And T-GLOBAL is disabled and T-ID is enabled in one card
    When click the card body
    Then no disabled Global workspace opens
    And Indonesia remains available through its enabled button
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-002

**Restore edit action after Reset**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Category record 101 edit form has unsaved changes

Behavior basis: [UI-SRC-055:13](<../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L13>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-RISK-002 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Restore edit action after Reset
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Category record 101 edit form has unsaved changes
    When click Reset
    Then the original Category Label returns
    And Update remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-003

**Reset a new record to initial values**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. a new Category form has Category Label Unsaved

Behavior basis: [UI-SRC-055:13](<../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L13>); [UI-SRC-084:4](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L4>)

```gherkin
@UI-RISK-003 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Reset a new record to initial values
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And a new Category form has Category Label Unsaved
    When click Reset
    Then Category Label returns to its initial empty value
    And Create remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-004

**Protect Owner in verification for SUPER_USER**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-SUPER-01; FMO PORTAL ADMIN SUPER_USER.

Setup: Apply the shared fixture definitions. UI-SUPER-01 has role SUPER_USER and record 101 is open in verify mode

Behavior basis: [UI-SRC-087:12](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L12>); [UI-SRC-036:15](<../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L15>); [UI-SRC-041:15](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L15>); [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-RISK-004 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Protect Owner in verification for SUPER_USER
    Given UI-SUPER-01 has role SUPER_USER and record 101 is open in verify mode
    When inspect Owner
    Then Owner is disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-005

**Keep latest category after response reordering**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category and Other Category requests can be controlled independently

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-RISK-005 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Keep latest category after response reordering
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category and Other Category requests can be controlled independently
    When select Fixture Category
    And select Other Category
    And resolve the Other Category response
    And resolve the Fixture Category response
    Then Other Category stays selected
    And only Other Category rows are shown
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-006

**Keep category state consistent after clearing during fetch**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. Fixture Category request is pending

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>)

```gherkin
@UI-RISK-006 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Keep category state consistent after clearing during fetch
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And Fixture Category request is pending
    When clear the category
    And resolve the pending Fixture Category response
    Then the category input stays empty
    And the grid stays empty
    And Create New Tile stays disabled
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-007

**Handle duplicate module options without ambiguity**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. two import map records 71 and 72 both use Module Name @fm/test

Behavior basis: [UI-SRC-046:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L14>); [UI-SRC-047:14](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L14>)

```gherkin
@UI-RISK-007 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Handle duplicate module options without ambiguity
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And two import map records 71 and 72 both use Module Name @fm/test
    When open the Container selector
    Then the Container selector shows both @fm/test options with their distinct record IDs 71 and 72
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed UX choice only. Owner unknown. Duplicate-label policy needs owner review. No defect or changed behavior is established. No old/new browser comparison was performed.

#### UI-RISK-008

**Handle empty audit history visibly**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. record 101 has an empty audit response

Behavior basis: [UI-SRC-052:10](<../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L10>); [UI-SRC-035:8](<../../repos/ui/mfe-base/src/admin/Category/common/useAudit.tsx#L8>)

```gherkin
@UI-RISK-008 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Handle empty audit history visibly
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And record 101 has an empty audit response
    When click Audit on record 101
    Then the UI displays an explicit empty audit state for record 101
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-009

**Keep unaffected audit history during response reordering**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Apply the shared fixture definitions. record 101 and record 102 audit responses can be controlled independently

Behavior basis: [UI-SRC-035:8](<../../repos/ui/mfe-base/src/admin/Category/common/useAudit.tsx#L8>)

```gherkin
@UI-RISK-009 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Keep unaffected audit history during response reordering
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And record 101 and record 102 audit responses can be controlled independently
    When click Audit on record 101
    And click Audit on record 102
    And resolve record 102 audit response
    And resolve record 101 audit response
    Then the Audit dialog identifies record 102
    And only record 102 audit rows are shown
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.

#### UI-RISK-010

**Show unknown admin route outcome**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated user.

Setup: Apply the shared fixture definitions. an admin tile points to module /unknown

Behavior basis: [UI-SRC-045:10](<../../repos/ui/mfe-base/src/admin/Routing.tsx#L10>)

```gherkin
@UI-RISK-010 @PROPOSED
Feature: Proposed source-risk coverage
  Scenario: Show unknown admin route outcome
    Given UI-USER-01; authenticated user uses the isolated case fixture
    And an admin tile points to module /unknown
    When open that tile
    Then the selected panel shows an explicit unsupported module message
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close added workspaces. Restore fixture storage, endpoint responses, and disposable records.

Limits: Proposed expectation. Owner unknown. Acceptance is blocked until the owner confirms this outcome. No old/new browser comparison was performed.
### Group: Entitlement policy

<a id="group-entitlement-policy"></a>

#### KNOW-001

**Entity-only eligibility permits a matching registered tenant**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>); [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-001 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Entity-only eligibility permits a matching registered tenant
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has only E-RR-B in EMS2
    And T-REPORT has entities E-RR-A,E-RR-B and an empty subject
    When Alice signs in
    And Alice opens the application catalog
    Then T-REPORT is visible exactly once
    And T-TRADE and T-CASH are absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-002

**Subject-required tile needs the matching subject**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>)

```gherkin
@KNOW-002 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Subject-required tile needs the matching subject
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-TRADE with subject S-VIEW
    And T-TRADE requires E-TRADE and S-VIEW
    When Alice opens the application catalog
    Then T-TRADE is visible exactly once
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-003

**Matching entity with a different subject denies the tile**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>)

```gherkin
@KNOW-003 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Matching entity with a different subject denies the tile
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-TRADE with subject S-EDIT only
    And T-TRADE requires S-VIEW
    When Alice opens the application catalog
    Then T-TRADE is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-004

**Matching subject under another entity does not grant tile access**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>)

```gherkin
@KNOW-004 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Matching subject under another entity does not grant tile access
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-CASH with subject S-VIEW only
    And T-TRADE requires E-TRADE and S-VIEW
    When Alice opens the application catalog
    Then T-TRADE is absent
    And T-CASH is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-005

**Empty subject skips subject matching for an eligible entity**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>); [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-005 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Empty subject skips subject matching for an eligible entity
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-RR-A and no subjects
    And T-REPORT has entities E-RR-A,E-RR-B and an empty subject
    When Alice opens the application catalog
    Then T-REPORT is visible exactly once
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-006

**An unrelated entity does not satisfy entity-only eligibility**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>); [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-006 @DOCUMENTED
Feature: Entitlement policy
  Scenario: An unrelated entity does not satisfy entity-only eligibility
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-TRADE only
    And T-REPORT has entities E-RR-A,E-RR-B and an empty subject
    When Alice opens the application catalog
    Then T-REPORT is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-008

**A shared subject does not bypass each tile entity condition**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>)

```gherkin
@KNOW-008 @DOCUMENTED
Feature: Entitlement policy
  Scenario: A shared subject does not bypass each tile entity condition
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-TRADE with S-VIEW only
    And Both T-TRADE and T-CASH require S-VIEW under their own entity
    When Alice opens the application catalog
    Then T-TRADE is visible exactly once
    And T-CASH is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-009

**Any configured report entity can grant entity-only tile access**

Version: 1. Level: System UI design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-009 @DOCUMENTED
Feature: Entitlement policy
  Scenario: Any configured report entity can grant entity-only tile access
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-RR-A only
    And T-REPORT permits E-RR-A,E-RR-B and has an empty subject
    When Alice opens the application catalog
    Then T-REPORT is visible exactly once
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.
### Group: Entitlement policy conflict

<a id="group-entitlement-policy-conflict"></a>

#### KNOW-007

**User without a registered entity cannot enter the portal**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>); [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-007 @DOCUMENTED
Feature: Entitlement policy conflict
  Scenario: User without a registered entity cannot enter the portal
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-UNREGISTERED only
    And The catalog contains T-TRADE,T-CASH,T-REPORT
    When Alice attempts portal sign-in
    Then The authenticated workspace is absent
    And No tenant tile or business data is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: Draft principles require a registered entity. The older tile-security proposal permits all SC accounts. Owner unknown must select the applicable portal-entry rule. Acceptance is blocked.

#### KNOW-015

**Empty entity configuration cannot become implicit guest access**

Version: 1. Level: System UI design. Priority: P0. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>); [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-015 @PROPOSED
Feature: Entitlement policy conflict
  Scenario: Empty entity configuration cannot become implicit guest access
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has no tenant entities
    And T-REPORT has an empty entity list and empty subject
    When Alice attempts to open T-REPORT
    Then No T-REPORT protected data is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The older security proposal permits empty roles. SSDR guest access was struck through. Owner unknown must resolve empty-entity policy before acceptance.

#### KNOW-017

**Unregistered temporary guest has no implied entitlement**

Version: 1. Level: System UI design. Priority: P0. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-017 @PROPOSED
Feature: Entitlement policy conflict
  Scenario: Unregistered temporary guest has no implied entitlement
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has no registered portal entity
    And A synthetic local guest flag is present in browser storage
    When Alice attempts to open T-REPORT
    Then No report data is visible
    And The local flag does not create an accessible tenant tile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The source strikes through the guest proposal. No supported guest workflow is established.
### Group: Entitlement policy boundary

<a id="group-entitlement-policy-boundary"></a>

#### KNOW-010

**Multiple matching entities do not duplicate one tile**

Version: 1. Level: System UI design. Priority: P1. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-010 @PROPOSED
Feature: Entitlement policy boundary
  Scenario: Multiple matching entities do not duplicate one tile
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice has E-RR-A and E-RR-B
    And T-REPORT permits both entities and has an empty subject
    When Alice opens the application catalog
    Then The catalog contains exactly one T-REPORT card
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-014

**Permission loss between tile discovery and open is rejected**

Version: 1. Level: System UI design. Priority: P0. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-004:14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>); [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-014 @PROPOSED
Feature: Entitlement policy boundary
  Scenario: Permission loss between tile discovery and open is rejected
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice sees T-TRADE in the catalog
    And EMS2 permission is revoked before the next tile-open authorization check
    When Alice selects T-TRADE
    Then Protected T-TRADE data is absent
    And The UI shows a denied or expired-access state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: Revocation timing, cache expiry, and exact message are unresolved. Owner unknown must define the enforcement point.
### Group: Tenant permission boundary

<a id="group-tenant-permission-boundary"></a>

#### KNOW-011

**Portal tile access does not grant protected tenant data**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-011 @DOCUMENTED
Feature: Tenant permission boundary
  Scenario: Portal tile access does not grant protected tenant data
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice can open T-TRADE
    And The controlled tenant response denies trade TR-1001 with HTTP 403
    When Alice opens TR-1001 from T-TRADE
    Then No TR-1001 business fields are visible
    And The tenant shows its configured access-denied state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: Tile-security text assigns data permissions to tenant applications. Exact tenant error wording and enforcement need that application source and owner.

#### KNOW-012

**Read permission does not imply tenant edit permission**

Version: 1. Level: System UI design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-012 @DOCUMENTED
Feature: Tenant permission boundary
  Scenario: Read permission does not imply tenant edit permission
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice can open T-TRADE and read TR-1001
    And The tenant fixture denies editing TR-1001
    When Alice attempts to edit TR-1001 through the tenant UI
    Then The edit is denied by the tenant UI
    And The displayed TR-1001 values remain unchanged
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: Tile-security text separates data access and editing permissions. Specific tenant controls are outside mfe-base and single-ui-bff. Integration fixture substitutes them.

#### KNOW-013

**Catalog deep link does not replace tenant authorization**

Version: 1. Level: System UI design. Priority: P0. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-005:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>)

```gherkin
@KNOW-013 @PROPOSED
Feature: Tenant permission boundary
  Scenario: Catalog deep link does not replace tenant authorization
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And Alice lacks data permission for TR-1001
    And A saved T-TRADE link addresses TR-1001
    When Alice opens the saved link
    Then No protected TR-1001 values are visible
    And The tenant access-denied state is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: The cited domain sources are draft candidates without recorded human approval. Expectation needs source applicability review before business acceptance.

#### KNOW-016

**Delegated SSDR authorization still denies an unentitled report**

Version: 1. Level: System UI design. Priority: P0. Basis: `PROPOSED`.

Actor: Test user Alice; assigned entitlements stated in this case..

Setup: Isolated UI integration environment. Synthetic catalog: Trade tile T-TRADE (entity E-TRADE, subject S-VIEW), Cashflow tile T-CASH (entity E-CASH, subject S-VIEW), Report tile T-REPORT (entities E-RR-A,E-RR-B; empty subject). No production identities or records. Use fresh browser storage and controlled catalog, EMS2, and tenant responses. Capture UI before and after each action.

Behavior basis: [UI-SRC-003:13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>)

```gherkin
@KNOW-016 @PROPOSED
Feature: Tenant permission boundary
  Scenario: Delegated SSDR authorization still denies an unentitled report
    Given Test user Alice; assigned entitlements stated in this case. uses the isolated case fixture
    And The reviewed test branch selects delegated SSDR authorization
    And Alice lacks SSDR report permission for REPORT-1001
    When Alice opens REPORT-1001 through T-REPORT
    Then REPORT-1001 data is absent
    And The SSDR denial state is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces. Restore catalog, entitlements, and browser storage to the baseline.

Limits: SSDR delegation is an unselected documented alternative. This case is conditional on an owner-approved choice.
### Group: Interoperability intent and context

<a id="group-interoperability-intent-and-context"></a>

#### KNOW-018

**Intent navigation activates the target tile**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-018 @DOCUMENTED
Feature: Interoperability intent and context
  Scenario: Intent navigation activates the target tile
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Source A is the active tile
    And Target B is registered for the agreed test intent
    When Alice clicks Send trade context for TR-1001 in Source A
    Then Target B becomes the active visible tile
    And Source A is no longer the foreground tile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-019

**Intent context becomes target initial data**

Version: 1. Level: System UI integration design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-019 @DOCUMENTED
Feature: Interoperability intent and context
  Scenario: Intent context becomes target initial data
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Source A holds tradeId TR-1001
    And The test context contract maps tradeId to the Target B trade identifier
    When Alice clicks Send trade context in Source A
    Then Target B shows tradeId TR-1001
    And Target B does not show TR-1002
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-020

**Target context is isolated between two portal users**

Version: 1. Level: System UI integration design. Priority: P0. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-020 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Target context is isolated between two portal users
    Given Alice and Bob use separate browser profiles
    And Alice holds TR-1001 in Source A; Bob holds TR-1002
    When Alice sends TR-1001 to Target B
    Then Alice sees TR-1001 in Target B
    And Bob does not see TR-1001 in his Target B
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-021

**Intent cannot open a target forbidden to the caller**

Version: 1. Level: System UI integration design. Priority: P0. Basis: `DOCUMENTED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-021 @DOCUMENTED
Feature: Interoperability intent and context
  Scenario: Intent cannot open a target forbidden to the caller
    Given Alice can open Source A but lacks Target B access
    And Target B is registered for the agreed test intent
    When Alice clicks Send trade context in Source A
    Then Target B business data is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The guide assigns access control to Portal. Exact denial wording and enforcement point remain undefined. Controlled tenant modules substitute real caller/provider applications.

#### KNOW-022

**Missing provider registration leaves the source usable**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-022 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Missing provider registration leaves the source usable
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Source A is active
    And No provider is registered for the agreed test intent
    When Alice clicks Send trade context in Source A
    Then Source A remains usable
    And No blank Target B workspace replaces the source
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-023

**Registered provider without a handler cannot show completed handoff**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-023 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Registered provider without a handler cannot show completed handoff
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Target B registration exists but its handler is absent
    When Alice clicks Send trade context in Source A
    Then The UI does not show a completed TR-1001 handoff
    And Source A remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-024

**Target module load failure is recoverable**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-024 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Target module load failure is recoverable
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Target B is registered
    And Its controlled module request returns HTTP 404
    When Alice clicks Send trade context in Source A
    Then No TR-1001 data is shown as loaded
    And The portal navigation remains usable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-025

**A delayed first intent cannot overwrite a newer target context**

Version: 1. Level: System UI integration design. Priority: P0. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-025 @PROPOSED
Feature: Interoperability intent and context
  Scenario: A delayed first intent cannot overwrite a newer target context
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Target B delays its TR-1001 response
    And Source A can send TR-1002 after TR-1001
    When Alice sends TR-1001
    And Alice sends TR-1002
    And The fixture releases the delayed TR-1001 response after TR-1002
    Then Target B displays TR-1002
    And Target B does not revert to TR-1001
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-026

**Invalid required context does not load unrelated data**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-026 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Invalid required context does not load unrelated data
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The agreed test contract requires a nonempty tradeId
    And Source A sends a context without tradeId
    When Alice clicks Send trade context
    Then Target B does not display an arbitrary trade
    And A context rejection state is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-027

**Context type mismatch is visible to the caller**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-027 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Context type mismatch is visible to the caller
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Target B accepts the agreed test context version 1
    And Source A sends version 2 with an incompatible tradeId field
    When Alice clicks Send trade context
    Then No TR-1001 handoff is shown as completed
    And Source A remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-028

**Target permission check applies after context handoff**

Version: 1. Level: System UI integration design. Priority: P0. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-028 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Target permission check applies after context handoff
    Given Alice can open Target B but cannot read TR-1001
    And Target B receives tradeId TR-1001
    When Alice sends TR-1001 from Source A
    Then Target B does not reveal TR-1001 protected fields
    And Target B shows its data-access denial state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-029

**Optional provider failure status is not shown as success**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-029 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Optional provider failure status is not shown as success
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The agreed fixture contract returns result status FAILED
    When Alice triggers the provider action in Source A
    Then The caller UI displays FAILED
    And The caller UI does not display a completed action state
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-030

**Closing a pending target prevents a late context from reopening it**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-030 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Closing a pending target prevents a late context from reopening it
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Target B has a pending TR-1001 context response
    When Alice closes Target B
    And The fixture releases the pending response
    Then Target B remains closed
    And No orphan workspace is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-031

**A repeated context has a stable business result**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-031 @PROPOSED
Feature: Interoperability intent and context
  Scenario: A repeated context has a stable business result
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The test contract defines duplicate TR-1001 handoff as navigation only
    When Alice sends TR-1001 twice
    Then Every visible Target B instance identifies TR-1001
    And No tenant business record is created by navigation
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: Duplicate workspace policy is undefined. This case checks data consistency, not a specific tab count. The fixture contract must distinguish navigation from mutating business actions.

#### KNOW-032

**An unrelated active workspace does not receive target context**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-032 @PROPOSED
Feature: Interoperability intent and context
  Scenario: An unrelated active workspace does not receive target context
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Unrelated tile Other C is active
    And Source A sends context to Target B through the agreed portal intent
    When Alice sends TR-1001 from Source A
    Then Target B shows TR-1001
    And Other C displays its original context
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-039

**Closing a source removes its context listener effects**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-039 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Closing a source removes its context listener effects
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And Source A registered a fixture context listener
    When Alice closes Source A
    And A fixture publisher sends TR-1001 to that closed source
    Then Source A remains closed
    And No duplicate target workspace opens from the closed source
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-040

**Context agreement preserves leading zero trade identifiers**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-001:5](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>)

```gherkin
@KNOW-040 @PROPOSED
Feature: Interoperability intent and context
  Scenario: Context agreement preserves leading zero trade identifiers
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The agreed fixture contract defines tradeId as a string
    And Source A holds tradeId 000123
    When Alice sends that context to Target B
    Then Target B displays exactly 000123
    And Target B does not display 123
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.
### Group: Conditional OpenFin POC

<a id="group-conditional-openfin-poc"></a>

#### KNOW-033

**POC openTile intent opens the named configured tile**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `DOCUMENTED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-006:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

```gherkin
@KNOW-033 @DOCUMENTED
Feature: Conditional OpenFin POC
  Scenario: POC openTile intent opens the named configured tile
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The selected POC uses fmchannel.fmoportal
    And The registered fixture target is container FixtureContainer, module /fixture, tile /target
    When Alice selects the fixture action that raises openTile with those identifiers
    Then The opened workspace renders the /target fixture marker
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: This is a conditional POC case. No production OpenFin adoption or schema approval is established. The source launch example also uses OpenTile, which conflicts with the listener naming.

#### KNOW-034

**POC changeTheme payload changes the portal theme**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `DOCUMENTED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-006:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

```gherkin
@KNOW-034 @DOCUMENTED
Feature: Conditional OpenFin POC
  Scenario: POC changeTheme payload changes the portal theme
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The selected POC uses the fmchannel changeTheme request
    And The portal starts in light theme
    When Alice triggers a fixture changeTheme request with theme dark
    Then The portal shows the dark theme fixture marker
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: Conditional POC case. The request schema and target runtime require owner confirmation.

#### KNOW-035

**POC unknown intent does not open an unrelated tile**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-006:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

```gherkin
@KNOW-035 @PROPOSED
Feature: Conditional OpenFin POC
  Scenario: POC unknown intent does not open an unrelated tile
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The fixture sends request unknownAction on fmchannel
    When Alice triggers the fixture action
    Then No unrelated tenant tile opens
    And The current workspace remains usable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-036

**POC channel isolation prevents unintended tile changes**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-006:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

```gherkin
@KNOW-036 @PROPOSED
Feature: Conditional OpenFin POC
  Scenario: POC channel isolation prevents unintended tile changes
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The portal listens on fmchannel
    And A fixture publisher uses otherchannel
    When Alice publishes an openTile context on otherchannel
    Then No target tile opens in the portal
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.

#### KNOW-037

**Mixed FDC3 library handoff exposes a recoverable failure**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-007:8](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L8>)

```gherkin
@KNOW-037 @PROPOSED
Feature: Conditional OpenFin POC
  Scenario: Mixed FDC3 library handoff exposes a recoverable failure
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The selected test matrix uses fdc3-2.1 sender and openfin-fdc3 receiver
    And Compatibility is not established
    When Alice triggers the fixture cross-library handoff
    Then The caller does not show completed navigation unless the target renders TR-1001
    And The caller UI remains usable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: Historical POC reports incompatible broadcast libraries. The new case proposes an observable failure contract. Supported current library versions require owner confirmation.

#### KNOW-038

**Intent naming mismatch cannot silently open the wrong tile**

Version: 1. Level: System UI integration design. Priority: P2. Basis: `PROPOSED`.

Actor: Alice; tenant user allowed to open Source A and Target B unless stated otherwise..

Setup: Isolated portal with controlled Source A and Target B tenant modules. Source A exposes fixture action Send trade context. Target B renders its received tradeId and context version. Synthetic trade IDs TR-1001 and TR-1002 contain no production data. Fresh browser profile and fixture catalog. Agree the test intent/context contract before execution. Capture UI before each action.

Behavior basis: [UI-SRC-006:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

```gherkin
@KNOW-038 @PROPOSED
Feature: Conditional OpenFin POC
  Scenario: Intent naming mismatch cannot silently open the wrong tile
    Given Alice; tenant user allowed to open Source A and Target B unless stated otherwise. uses the isolated case fixture
    And The fixture publishes OpenTile
    And The selected listener accepts fmchannel.fmoportal only
    When Alice triggers the fixture navigation
    Then No unrelated tile opens
    And The caller does not display a completed target handoff
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close fixture workspaces and provider listeners. Restore catalog, module versions, and browser storage.

Limits: The cited interoperability material records intent or POC behavior, without a current approved production contract. Controlled tenant modules substitute real caller/provider applications. Owner unknown must confirm source applicability and selected message schema.
### Group: Documented cache and version lifecycle

<a id="group-documented-cache-and-version-lifecycle"></a>

#### KNOW-041

**First load renders the complete selected tenant version**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-041 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: First load renders the complete selected tenant version
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser cache is empty
    And The fixture server serves portal, container, and tile build V1
    When Alice opens fixture tile T-CACHE
    Then T-CACHE displays base V1, container V1, and tile V1 markers
    And No missing-chunk error is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-042

**Refresh discovers an updated tile entry**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-042 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: Refresh discovers an updated tile entry
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And T-CACHE V1 has populated the browser cache
    And The server replaces the tile entry and chunks with V2
    When Alice refreshes the portal
    And Alice opens T-CACHE
    Then T-CACHE displays tile V2
    And Tile V1 content is absent
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-043

**Refresh reuses an unchanged version without blank content**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-043 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: Refresh reuses an unchanged version without blank content
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And T-CACHE V1 has populated the browser cache
    And The server still serves V1 entries and assets
    When Alice refreshes the portal
    And Alice opens T-CACHE
    Then T-CACHE displays V1 content
    And No missing-chunk error is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-044

**A container entry update is discovered on refresh**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-044 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: A container entry update is discovered on refresh
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has cached container V1
    And The server updates only the container entry and its referenced chunks to V2
    When Alice refreshes the portal
    And Alice opens T-CACHE
    Then The tile displays container V2 and tile V1 markers
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-045

**A base entry update is discovered on refresh**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-045 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: A base entry update is discovered on refresh
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has cached base V1
    And The server updates the base entry and its referenced chunks to V2
    When Alice refreshes the portal
    Then The portal displays base V2
    And The portal navigation remains available
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-046

**Logout and re-entry load the selected current build**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-046 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: Logout and re-entry load the selected current build
    Given Alice has opened T-CACHE V1
    And The fixture server now serves T-CACHE V2
    When Alice signs out
    And Alice signs in
    And Alice opens T-CACHE
    Then T-CACHE displays V2
    And No V1 marker is shown as the active tile version
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-047

**A stale entry with a removed chunk has a recovery path**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-047 @PROPOSED
Feature: Documented cache and version lifecycle
  Scenario: A stale entry with a removed chunk has a recovery path
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser holds a V1 entry
    And The referenced V1 chunk returns HTTP 404
    When Alice opens T-CACHE
    Then The UI does not claim T-CACHE finished loading
    And The portal navigation remains usable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-048

**Failed asset revalidation does not render mixed business content**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-048 @PROPOSED
Feature: Documented cache and version lifecycle
  Scenario: Failed asset revalidation does not render mixed business content
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser holds V1 tile data
    And The V2 entry response fails during refresh
    When Alice refreshes
    And Alice opens T-CACHE
    Then The UI does not combine a V1 trade identifier with V2 trade fields
    And A load failure is visible if no consistent version can render
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-049

**Lazy content uses the new referenced chunk after refresh**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `DOCUMENTED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-049 @DOCUMENTED
Feature: Documented cache and version lifecycle
  Scenario: Lazy content uses the new referenced chunk after refresh
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has cached V1 lazy-search assets
    And V2 entry references a new V2 lazy-search chunk
    When Alice refreshes T-CACHE
    And Alice opens the fixture lazy search panel
    Then The search panel displays its V2 marker
    And The panel does not display its V1 marker
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-050

**An updated CSS reference does not leave the tile unstyled**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-050 @PROPOSED
Feature: Documented cache and version lifecycle
  Scenario: An updated CSS reference does not leave the tile unstyled
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has cached V1 tile assets
    And V2 references a new CSS asset with the fixture V2 appearance marker
    When Alice refreshes
    And Alice opens T-CACHE
    Then The tile displays the V2 appearance marker
    And The tile labels and controls remain visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-051

**An updated image reference displays the new tile asset**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-051 @PROPOSED
Feature: Documented cache and version lifecycle
  Scenario: An updated image reference displays the new tile asset
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has cached image V1
    And V2 entry references image V2
    When Alice refreshes
    And Alice opens T-CACHE
    Then The fixture tile displays image V2
    And No broken image indicator is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.

#### KNOW-052

**Rollback refresh returns a consistent earlier tenant build**

Version: 1. Level: System UI integration design. Priority: P1. Basis: `PROPOSED`.

Actor: Alice; authenticated tenant user with T-CACHE access..

Setup: Isolated fixture tenant T-CACHE. Base, container, tile, and lazy panel render V1/V2 markers. The harness controls entry URLs, chunk URLs, cache headers, and asset failures. Markers are test instrumentation, not product controls. Use a dedicated browser cache and fixture server. Keep business data constant across builds. Record entries, asset identity, and the active UI version.

Behavior basis: [UI-SRC-002:1](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

```gherkin
@KNOW-052 @PROPOSED
Feature: Documented cache and version lifecycle
  Scenario: Rollback refresh returns a consistent earlier tenant build
    Given Alice; authenticated tenant user with T-CACHE access. uses the isolated case fixture
    And The browser has loaded T-CACHE V2
    And The server restores the complete V1 entry and V1 referenced assets
    When Alice refreshes
    And Alice opens T-CACHE
    Then The tile displays a consistent V1 marker set
    And No V2 business fields remain in the active fixture tile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore V1 server assets. Clear the dedicated cache and browser storage.

Limits: The cache guide documents design intent. Its Implementation section is empty. Current deployment headers, cache naming, and activation behavior are unverified. No accepted UI latency budget is established. Do not apply historical performance numbers as pass limits.
### Group: Accessibility

<a id="group-accessibility"></a>

#### UX-001

**Reach all shell controls with the keyboard**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open with the Tile Options drawer closed

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-001 @PROPOSED
Feature: Accessibility
  Scenario: Reach all shell controls with the keyboard
    Given USER-A has Home open with the Tile Options drawer closed
    When USER-A uses Tab from the page start through the header controls
    Then each visible header control receives visible keyboard focus once before focus enters the workspace
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-002

**Open Tile Options without a pointer**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has keyboard focus on the Tile Options opener

Behavior basis: [UI-SRC-066:12](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L12>)

```gherkin
@UX-002 @PROPOSED
Feature: Accessibility
  Scenario: Open Tile Options without a pointer
    Given USER-A has keyboard focus on the Tile Options opener
    When USER-A presses Enter
    Then the Tile Options drawer is visible and focus is inside the drawer
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-003

**Close Tile Options and restore focus**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A opened Tile Options with the keyboard

Behavior basis: [UI-SRC-066:12](<../../repos/ui/mfe-base/src/components/Drawer/index.tsx#L12>)

```gherkin
@UX-003 @PROPOSED
Feature: Accessibility
  Scenario: Close Tile Options and restore focus
    Given USER-A opened Tile Options with the keyboard
    When USER-A presses Escape
    Then the Tile Options drawer is closed
    And keyboard focus returns to its opener
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-004

**Select a workspace with the keyboard**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home and Cashflow workspaces open

Behavior basis: [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UX-004 @PROPOSED
Feature: Accessibility
  Scenario: Select a workspace with the keyboard
    Given USER-A has Home and Cashflow workspaces open with keyboard focus on the Home tab
    When USER-A presses ArrowRight
    And USER-A presses Enter
    Then Cashflow is the selected workspace
    And the Cashflow content region is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-005

**Rename a workspace using keyboard input**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has the Cashflow workspace and keyboard focus on Workspace Name

Behavior basis: [UI-SRC-082:40](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L40>)

```gherkin
@UX-005 @PROPOSED
Feature: Accessibility
  Scenario: Rename a workspace using keyboard input
    Given USER-A has the Cashflow workspace and keyboard focus on Workspace Name
    When USER-A replaces the label with Cashflow Review
    Then the workspace label equals Cashflow Review
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-006

**Announce the selected workspace**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home and Cashflow workspaces open

Behavior basis: [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UX-006 @PROPOSED
Feature: Accessibility
  Scenario: Announce the selected workspace
    Given USER-A has Home and Cashflow workspaces open
    When USER-A selects Cashflow
    And USER-A inspects the workspace accessibility tree
    Then the accessibility tree identifies Cashflow as the selected workspace
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-007

**Expose descriptive names for icon controls**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a workspace with refresh and delete controls visible

Behavior basis: [UI-SRC-082:54](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L54>)

```gherkin
@UX-007 @PROPOSED
Feature: Accessibility
  Scenario: Expose descriptive names for icon controls
    Given USER-A has a workspace with refresh and delete controls visible
    When USER-A inspects the workspace controls in the accessibility tree
    Then the refresh control has the accessible name refresh
    And the delete control has the accessible name delete
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-008

**Toggle theme using the keyboard**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has dark theme and focus on Theme Switch

Behavior basis: [UI-SRC-079:21](<../../repos/ui/mfe-base/src/components/Switch/index.tsx#L21>)

```gherkin
@UX-008 @PROPOSED
Feature: Accessibility
  Scenario: Toggle theme using the keyboard
    Given USER-A has dark theme and focus on Theme Switch
    When USER-A presses Space
    Then the theme label equals light
    And the Theme Switch checked state equals true
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-009

**Announce theme state**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has light theme enabled

Behavior basis: [UI-SRC-079:21](<../../repos/ui/mfe-base/src/components/Switch/index.tsx#L21>)

```gherkin
@UX-009 @PROPOSED
Feature: Accessibility
  Scenario: Announce theme state
    Given USER-A has light theme enabled
    When USER-A inspects Theme Switch in the accessibility tree
    Then Theme Switch exposes its current checked state as true
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-010

**Open User Profile using the keyboard**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has keyboard focus on the avatar opener

Behavior basis: [UI-SRC-060:34](<../../repos/ui/mfe-base/src/components/Avatar/index.tsx#L34>)

```gherkin
@UX-010 @PROPOSED
Feature: Accessibility
  Scenario: Open User Profile using the keyboard
    Given USER-A has keyboard focus on the avatar opener
    When USER-A presses Enter to open the avatar menu
    And USER-A moves focus to the profile entry
    And USER-A presses Enter
    Then User Profile is visible
    And focus is inside User Profile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-011

**Contain keyboard focus in User Profile**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has User Profile open

Behavior basis: [UI-SRC-062:77](<../../repos/ui/mfe-base/src/components/Dialog/index.tsx#L77>)

```gherkin
@UX-011 @PROPOSED
Feature: Accessibility
  Scenario: Contain keyboard focus in User Profile
    Given USER-A has User Profile open
    When USER-A cycles forward and backward through all dialog controls
    Then keyboard focus stays inside User Profile until the dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-012

**Restore focus after closing User Profile**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A opened User Profile from the avatar menu

Behavior basis: [UI-SRC-060:102](<../../repos/ui/mfe-base/src/components/Avatar/index.tsx#L102>)

```gherkin
@UX-012 @PROPOSED
Feature: Accessibility
  Scenario: Restore focus after closing User Profile
    Given USER-A opened User Profile from the avatar menu
    When USER-A activates the dialog close control
    Then User Profile is closed
    And focus returns to the avatar menu opener
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-013

**Expose an accessible dialog title**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has User Profile open

Behavior basis: [UI-SRC-062:77](<../../repos/ui/mfe-base/src/components/Dialog/index.tsx#L77>)

```gherkin
@UX-013 @PROPOSED
Feature: Accessibility
  Scenario: Expose an accessible dialog title
    Given USER-A has User Profile open
    When USER-A inspects the dialog accessibility tree
    Then the dialog accessible name equals User Profile
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-014

**Label administration inputs**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has the Tile detail form open

Behavior basis: [UI-SRC-087:94](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L94>)

```gherkin
@UX-014 @PROPOSED
Feature: Accessibility
  Scenario: Label administration inputs
    Given ADMIN-A has the Tile detail form open
    When ADMIN-A inspects Tile Name and Description in the accessibility tree
    Then the title input accessible name equals Tile Name
    And the subtitle input accessible name equals Description
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-015

**Announce read-only administration fields**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has a tile verification form open

Behavior basis: [UI-SRC-087:102](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L102>)

```gherkin
@UX-015 @PROPOSED
Feature: Accessibility
  Scenario: Announce read-only administration fields
    Given ADMIN-A has a tile verification form open
    When ADMIN-A inspects the disabled form fields
    Then every disabled form field exposes its disabled state in the accessibility tree
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-016

**Select an autocomplete value with the keyboard**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has the tile form open with Aplication Category focused

Behavior basis: [UI-SRC-087:30](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L30>)

```gherkin
@UX-016 @PROPOSED
Feature: Accessibility
  Scenario: Select an autocomplete value with the keyboard
    Given ADMIN-A has the tile form open with Aplication Category focused
    When ADMIN-A types Cash into Aplication Category
    And ADMIN-A presses ArrowDown to highlight Cashflow
    And ADMIN-A presses Enter
    Then the category input displays Cashflow
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-017

**Traverse an administration grid**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A sees category rows C1 and C2 in the category grid

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-017 @PROPOSED
Feature: Accessibility
  Scenario: Traverse an administration grid
    Given ADMIN-A sees category rows C1 and C2 with keyboard focus on the C1 Category Label cell
    When ADMIN-A presses ArrowDown
    Then the focused row identifies C2 and its Category Label
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-018

**Announce a failed save**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has a tile form open and the save fixture returns a controlled error

Behavior basis: [UI-SRC-075:52](<../../repos/ui/mfe-base/src/components/Snackbar/index.tsx#L52>)

```gherkin
@UX-018 @PROPOSED
Feature: Accessibility
  Scenario: Announce a failed save
    Given ADMIN-A has a tile form open and the save fixture returns a controlled error
    When ADMIN-A submits the tile
    Then an error message appears in the accessibility tree
    And the message identifies the failed save without relying on color
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-019

**Preserve a visible focus indicator in dark theme**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has dark theme and the shell open

Behavior basis: [UI-SRC-079:21](<../../repos/ui/mfe-base/src/components/Switch/index.tsx#L21>)

```gherkin
@UX-019 @PROPOSED
Feature: Accessibility
  Scenario: Preserve a visible focus indicator in dark theme
    Given USER-A has dark theme and the shell open
    When USER-A moves keyboard focus to each header control
    Then each focused control has a visible focus indicator
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-020

**Preserve a visible focus indicator in light theme**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has light theme and the shell open

Behavior basis: [UI-SRC-079:21](<../../repos/ui/mfe-base/src/components/Switch/index.tsx#L21>)

```gherkin
@UX-020 @PROPOSED
Feature: Accessibility
  Scenario: Preserve a visible focus indicator in light theme
    Given USER-A has light theme and the shell open
    When USER-A moves keyboard focus to each header control
    Then each focused control has a visible focus indicator
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-021

**Identify state without status colors**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A sees one verified category and one unverified category

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-021 @PROPOSED
Feature: Accessibility
  Scenario: Identify state without status colors
    Given ADMIN-A sees one verified category and one unverified category
    When ADMIN-A inspects the Verified? cells without color information
    Then the two cells provide distinguishable text or accessible state labels
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-022

**Read long messages without losing content**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A receives an error message containing 2000 fixture characters

Behavior basis: [UI-SRC-075:75](<../../repos/ui/mfe-base/src/components/Snackbar/index.tsx#L75>)

```gherkin
@UX-022 @PROPOSED
Feature: Accessibility
  Scenario: Read long messages without losing content
    Given USER-A receives an error message containing 2000 fixture characters
    When USER-A scrolls the visible error message
    Then the first and final fixture characters are readable without changing the message
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.
### Group: Responsive layout

<a id="group-responsive-layout"></a>

#### UX-023

**Operate the shell at 320 by 568 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 320 by 568 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-023 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 320 by 568 CSS pixels
    Given USER-A has Home open at a 320 by 568 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-024

**Operate the shell at 375 by 812 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 375 by 812 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-024 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 375 by 812 CSS pixels
    Given USER-A has Home open at a 375 by 812 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-025

**Operate the shell at 768 by 1024 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 768 by 1024 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-025 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 768 by 1024 CSS pixels
    Given USER-A has Home open at a 768 by 1024 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-026

**Operate the shell at 1024 by 768 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 1024 by 768 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-026 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 1024 by 768 CSS pixels
    Given USER-A has Home open at a 1024 by 768 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-027

**Operate the shell at 1366 by 768 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 1366 by 768 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-027 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 1366 by 768 CSS pixels
    Given USER-A has Home open at a 1366 by 768 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-028

**Operate the shell at 1920 by 1080 CSS pixels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at a 1920 by 1080 CSS pixel viewport

Behavior basis: [UI-SRC-059:35](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L35>)

```gherkin
@UX-028 @PROPOSED
Feature: Responsive layout
  Scenario: Operate the shell at 1920 by 1080 CSS pixels
    Given USER-A has Home open at a 1920 by 1080 CSS pixel viewport
    When USER-A opens Tile Options
    And USER-A closes Tile Options
    And USER-A opens the avatar menu
    Then each open panel has reachable controls
    And the menu items remain readable without overlapping each other
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed viewport probe. Supported device sizes require owner confirmation.

#### UX-029

**Operate header controls at 200 percent zoom**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at 1366 by 768 CSS pixels before 200 percent browser zoom

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-029 @PROPOSED
Feature: Responsive layout
  Scenario: Operate header controls at 200 percent zoom
    Given USER-A has Home open at 1366 by 768 CSS pixels before 200 percent browser zoom
    When USER-A sets browser zoom to 200 percent
    And USER-A opens the avatar menu
    Then the avatar menu remains reachable
    And the Logout entry is readable and operable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed zoom probe. No accessibility conformance level is established.

#### UX-030

**Operate header controls at 400 percent zoom**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Home open at 1366 by 768 CSS pixels before 400 percent browser zoom

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-030 @PROPOSED
Feature: Responsive layout
  Scenario: Operate header controls at 400 percent zoom
    Given USER-A has Home open at 1366 by 768 CSS pixels before 400 percent browser zoom
    When USER-A sets browser zoom to 400 percent
    And USER-A opens the avatar menu
    Then the avatar menu remains reachable
    And the Logout entry is readable and operable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed zoom probe. No accessibility conformance level is established.

#### UX-031

**Keep form actions reachable in a short viewport**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has a 1000 by 600 tile form open in a 1024 by 600 CSS pixel viewport

Behavior basis: [UI-SRC-086:67](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L67>)

```gherkin
@UX-031 @PROPOSED
Feature: Responsive layout
  Scenario: Keep form actions reachable in a short viewport
    Given ADMIN-A has the edit form for tile T1 open in a 1024 by 600 CSS pixel viewport
    When ADMIN-A scrolls the form to its actions
    Then Update, Reset and Close are reachable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-032

**Keep a dialog reachable after viewport resize**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has User Profile open at 1366 by 768 CSS pixels

Behavior basis: [UI-SRC-061:161](<../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L161>)

```gherkin
@UX-032 @PROPOSED
Feature: Responsive layout
  Scenario: Keep a dialog reachable after viewport resize
    Given USER-A has User Profile open at 1366 by 768 CSS pixels
    When USER-A resizes the viewport to 768 by 600 CSS pixels
    Then the User Profile title and close control remain reachable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-033

**Recover a dragged dialog from the viewport edge**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a draggable fixture dialog open

Behavior basis: [UI-SRC-061:55](<../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L55>)

```gherkin
@UX-033 @PROPOSED
Feature: Responsive layout
  Scenario: Recover a dragged dialog from the viewport edge
    Given USER-A has a draggable fixture dialog open
    When USER-A drags the title towards the top-left viewport edge
    Then the title remains reachable so USER-A can move or close the dialog
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-034

**Constrain an aggressively reduced dialog**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a resizable fixture dialog open

Behavior basis: [UI-SRC-061:69](<../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L69>)

```gherkin
@UX-034 @PROPOSED
Feature: Responsive layout
  Scenario: Constrain an aggressively reduced dialog
    Given USER-A has a resizable fixture dialog open
    When USER-A drags the resize handle 800 CSS pixels up and left
    Then the dialog content remains reachable by scrolling
    And the close control remains operable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-035

**Restore content after maximizing a dialog**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has User Profile open over a scrollable workspace

Behavior basis: [UI-SRC-061:104](<../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L104>)

```gherkin
@UX-035 @PROPOSED
Feature: Responsive layout
  Scenario: Restore content after maximizing a dialog
    Given USER-A has User Profile open over a scrollable workspace
    When USER-A maximizes User Profile
    And USER-A restores the dialog size
    And USER-A closes User Profile
    Then the workspace can scroll again after the restored dialog closes
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-036

**Scroll a long tab strip without losing controls**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has 30 uniquely named fixture workspaces open

Behavior basis: [UI-SRC-082:24](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L24>)

```gherkin
@UX-036 @PROPOSED
Feature: Responsive layout
  Scenario: Scroll a long tab strip without losing controls
    Given USER-A has 30 uniquely named fixture workspaces open
    When USER-A selects the final workspace
    Then the final workspace label and its available controls are reachable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.
### Group: Security and text

<a id="group-security-and-text"></a>

#### UX-037

**Escape hostile workspace names**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has the Cashflow workspace label field focused

Behavior basis: [UI-SRC-082:40](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L40>)

```gherkin
@UX-037 @PROPOSED
Feature: Security and text
  Scenario: Escape hostile workspace names
    Given USER-A has the Cashflow workspace label field focused
    When USER-A enters <img src=x onerror=alert(1)>
    Then the literal label is displayed as text
    And no alert dialog opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-038

**Escape hostile category labels**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A can edit category C1 in the isolated fixture

Behavior basis: [UI-SRC-087:94](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L94>)

```gherkin
@UX-038 @PROPOSED
Feature: Security and text
  Scenario: Escape hostile category labels
    Given ADMIN-A can edit category C1 in the isolated fixture
    When ADMIN-A enters <script>alert(1)</script> into the category label
    And ADMIN-A activates Update
    And ADMIN-A reloads the category grid
    Then the label appears as text when returned by the fixture
    And no script alert opens
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-039

**Sanitize hostile error markup**

Version: 1. Level: UI system test design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has an error fixture containing <img src=x onerror=alert(1)>

Behavior basis: [UI-SRC-075:59](<../../repos/ui/mfe-base/src/components/Snackbar/index.tsx#L59>)

```gherkin
@UX-039 @IMPLEMENTATION
Feature: Security and text
  Scenario: Sanitize hostile error markup
    Given USER-A has an error fixture containing <img src=x onerror=alert(1)>
    When USER-A triggers the fixture error message
    Then the message does not open a script alert
    And the surrounding shell remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: DOMPurify is present in source. Existing Snackbar tests assert rendering only; this hostile-markup case has not run.

#### UX-040

**Retain safe message text after sanitization**

Version: 1. Level: UI system test design. Priority: P2. Basis: `IMPLEMENTATION`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has an error fixture containing <b>Save failed</b>

Behavior basis: [UI-SRC-075:59](<../../repos/ui/mfe-base/src/components/Snackbar/index.tsx#L59>)

```gherkin
@UX-040 @IMPLEMENTATION
Feature: Security and text
  Scenario: Retain safe message text after sanitization
    Given USER-A has an error fixture containing <b>Save failed</b>
    When USER-A triggers the fixture error message
    Then the visible message text contains Save failed
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Source uses DOMPurify. No browser execution establishes formatting or sanitizer configuration.

#### UX-041

**Avoid exposing credentials in a support link**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a controlled tile error whose stack contains a synthetic credential marker SECRET-TEST

Behavior basis: [UI-SRC-069:31](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L31>)

```gherkin
@UX-041 @PROPOSED
Feature: Security and text
  Scenario: Avoid exposing credentials in a support link
    Given USER-A has a controlled tile error whose stack contains a synthetic credential marker SECRET-TEST
    When USER-A opens Contact PSS with a mail-client capture fixture
    Then the draft email body does not contain SECRET-TEST
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed redaction assertion. Current source places the stack in a mailto URL; do not use real credentials.

#### UX-042

**Encode a support email subject and body**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a tile error with stack text line1 & line2 # ? and a configured support recipient

Behavior basis: [UI-SRC-069:31](<../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L31>)

```gherkin
@UX-042 @PROPOSED
Feature: Security and text
  Scenario: Encode a support email subject and body
    Given USER-A has a tile error with stack text line1 & line2 # ? and a configured support recipient
    When USER-A activates Contact PSS with a mail-client capture fixture
    Then the draft recipient equals the configured support recipient
    And the draft body preserves the complete fixture stack text as one body value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-043

**Protect a CSV export from spreadsheet formulas**

Version: 1. Level: UI export integration design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A sees category labels =1+1, +1+1, -1+1 and @SUM(1) in an isolated grid

Behavior basis: [UI-SRC-086:14](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L14>)

```gherkin
@UX-043 @PROPOSED
Feature: Security and text
  Scenario: Protect a CSV export from spreadsheet formulas
    Given ADMIN-A sees category labels =1+1, +1+1, -1+1 and @SUM(1) in an isolated grid
    When ADMIN-A exports the grid and opens the artifact in a controlled spreadsheet viewer
    Then each fixture label appears as text and does not evaluate as a formula
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed export safety assertion. Inspect the configured DataGrid exporter before acceptance; no spreadsheet application is opened now.

#### UX-044

**Keep Unicode workspace labels intact**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has Workspace Name focused

Behavior basis: [UI-SRC-082:40](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L40>)

```gherkin
@UX-044 @PROPOSED
Feature: Security and text
  Scenario: Keep Unicode workspace labels intact
    Given USER-A has Workspace Name focused
    When USER-A enters Cashflow 東京 😀
    Then the visible workspace label equals Cashflow 東京 😀
    And the full label is available in its tooltip
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-045

**Do not drop IME composition text**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A is composing 東京 through an IME in Tile Name

Behavior basis: [UI-SRC-087:110](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L110>)

```gherkin
@UX-045 @PROPOSED
Feature: Security and text
  Scenario: Do not drop IME composition text
    Given ADMIN-A is composing 東京 through an IME in Tile Name
    When ADMIN-A completes composition and leaves the input
    Then Tile Name displays 東京 without duplicated or missing characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-046

**Keep a long unbroken label operable**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a workspace label containing 512 letter A characters

Behavior basis: [UI-SRC-082:30](<../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L30>)

```gherkin
@UX-046 @PROPOSED
Feature: Security and text
  Scenario: Keep a long unbroken label operable
    Given USER-A has a workspace label containing 512 letter A characters
    When USER-A opens its label tooltip
    Then the full 512-character label is available
    And the workspace delete and refresh controls remain reachable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-047

**Handle bidirectional label characters**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has a tile fixture named ABC followed by U+202E and DEF

Behavior basis: [UI-SRC-087:94](<../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L94>)

```gherkin
@UX-047 @PROPOSED
Feature: Security and text
  Scenario: Handle bidirectional label characters
    Given ADMIN-A has a tile fixture named ABC followed by U+202E and DEF
    When ADMIN-A opens the tile detail form
    Then the field preserves the original character sequence
    And adjacent field labels and action controls keep their original reading order
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.
### Group: Data resilience

<a id="group-data-resilience"></a>

#### UX-048

**Render missing optional profile fields**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a profile with no title, emailId, country, or photo

Behavior basis: [UI-SRC-072:203](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L203>)

```gherkin
@UX-048 @PROPOSED
Feature: Data resilience
  Scenario: Render missing optional profile fields
    Given USER-A has a profile with no title, emailId, country, or photo
    When USER-A opens User Profile
    Then User Profile stays visible
    And missing optional fields do not render the literal strings undefined or null
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-049

**Render long profile names**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a fullName containing 200 characters

Behavior basis: [UI-SRC-072:203](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L203>)

```gherkin
@UX-049 @PROPOSED
Feature: Data resilience
  Scenario: Render long profile names
    Given USER-A has a fullName containing 200 characters
    When USER-A opens User Profile
    Then the complete name is readable by wrapping or scrolling
    And the close control remains reachable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-050

**Keep profile content when the photo fails**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has a profile photo URL that returns HTTP 404

Behavior basis: [UI-SRC-072:287](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L287>)

```gherkin
@UX-050 @PROPOSED
Feature: Data resilience
  Scenario: Keep profile content when the photo fails
    Given USER-A has a profile photo URL that returns HTTP 404
    When USER-A opens User Profile
    Then the fullName and userId remain visible
    And the photo failure does not replace the whole profile with a tile error
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.
### Group: Form timing

<a id="group-form-timing"></a>

#### UX-051

**Save before the field callback can run**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-051 @PROPOSED
Feature: Form timing
  Scenario: Save before the field callback can run
    Given ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture
    When ADMIN-A replaces Tile Name with New
    And ADMIN-A activates Update before the 300-millisecond callback runs
    And ADMIN-A flushes pending field callbacks
    And ADMIN-A reloads the grid
    And ADMIN-A reopens T1
    Then the grid shows Tile Name New for T1
    And the reopened T1 field displays New
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed intent. The field schedules a 300-millisecond state callback; a browser assertion must confirm the race. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-052

**Preserve an edit saved after 100 milliseconds**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-052 @PROPOSED
Feature: Form timing
  Scenario: Preserve an edit saved after 100 milliseconds
    Given ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture
    When ADMIN-A replaces Tile Name with New
    And ADMIN-A advances the controlled clock by 100 milliseconds
    And ADMIN-A activates Update
    And ADMIN-A flushes pending field callbacks
    And ADMIN-A reloads the grid
    And ADMIN-A reopens T1
    Then the grid shows Tile Name New for T1
    And the reopened T1 field displays New
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed intent. The field schedules a 300-millisecond state callback; a browser assertion must confirm the race. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-053

**Preserve an edit saved after 299 milliseconds**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-053 @PROPOSED
Feature: Form timing
  Scenario: Preserve an edit saved after 299 milliseconds
    Given ADMIN-A has tile T1 open with Tile Name Old and an isolated successful save fixture
    When ADMIN-A replaces Tile Name with New
    And ADMIN-A advances the controlled clock by 299 milliseconds
    And ADMIN-A activates Update
    And ADMIN-A flushes pending field callbacks
    And ADMIN-A reloads the grid
    And ADMIN-A reopens T1
    Then the grid shows Tile Name New for T1
    And the reopened T1 field displays New
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed intent. The field schedules a 300-millisecond state callback; a browser assertion must confirm the race. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-054

**Save an edit after the state callback**

Version: 1. Level: UI system test design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with Tile Name Old Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-054 @IMPLEMENTATION
Feature: Form timing
  Scenario: Save an edit after the state callback
    Given ADMIN-A has tile T1 open with Tile Name Old
    When ADMIN-A replaces Tile Name with New
    And ADMIN-A advances the controlled clock by 301 milliseconds
    And ADMIN-A activates Update
    And ADMIN-A flushes pending field callbacks
    And ADMIN-A reloads the grid
    And ADMIN-A reopens T1
    Then the grid shows Tile Name New for T1
    And the reopened T1 field displays New
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Source characterization after the callback. Scheduling differences require a controlled clock; not executed. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-055

**Reset during a pending field update**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with persisted Tile Name Old Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-055 @PROPOSED
Feature: Form timing
  Scenario: Reset during a pending field update
    Given ADMIN-A has tile T1 open with persisted Tile Name Old
    When ADMIN-A types New into Tile Name
    And ADMIN-A advances the controlled clock by 100 milliseconds
    And ADMIN-A activates Reset
    And ADMIN-A flushes all pending field callbacks
    Then Tile Name returns to Old
    And Tile Name remains Old after all pending field callbacks finish
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-056

**Close a form before its field callback**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with persisted Tile Name Old Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-056 @PROPOSED
Feature: Form timing
  Scenario: Close a form before its field callback
    Given ADMIN-A has tile T1 open with persisted Tile Name Old
    When ADMIN-A types New into Tile Name
    And ADMIN-A advances the controlled clock by 100 milliseconds
    And ADMIN-A closes T1
    And ADMIN-A opens T2
    And ADMIN-A flushes all pending field callbacks
    Then the T2 form keeps its own fixture values after all pending T1 callbacks finish
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-057

**Keep two rapid field edits**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has tile T1 open with Tile Name Old and Description Before Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-047:38](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L38>)

```gherkin
@UX-057 @PROPOSED
Feature: Form timing
  Scenario: Keep two rapid field edits
    Given ADMIN-A has tile T1 open with Tile Name Old and Description Before
    When ADMIN-A changes Tile Name to New
    And ADMIN-A advances the controlled clock by 100 milliseconds
    And ADMIN-A changes Description to After
    And ADMIN-A flushes all pending field callbacks
    Then Tile Name remains New after field callbacks finish
    And Description remains After after field callbacks finish
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance. Controlled scheduling probes require a separate natural-browser timing investigation.

#### UX-058

**Keep the final value during fast typing**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: ADMIN-A.

Setup: Use the isolated fixture in the catalog. ADMIN-A has Tile Name focused in the T1 form Use a controlled event loop. Measure milliseconds from the final input event. Flush pending callbacks at each stated checkpoint. The save fixture persists the actual received request payload. Reload returns that persisted payload without forcing expected field values.

Behavior basis: [UI-SRC-088:24](<../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24>)

```gherkin
@UX-058 @PROPOSED
Feature: Form timing
  Scenario: Keep the final value during fast typing
    Given ADMIN-A has Tile Name focused in the T1 form
    When ADMIN-A types A, AB and ABC at 50-millisecond intervals
    And ADMIN-A flushes all pending field callbacks
    And ADMIN-A activates Update
    And ADMIN-A reopens T1
    Then the reopened T1 Tile Name equals ABC
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance. Controlled scheduling probes require a separate natural-browser timing investigation.
### Group: Browser compatibility

<a id="group-browser-compatibility"></a>

#### UX-059

**Open a tile and profile in Chromium**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A starts a clean Chromium browser context with the same fixture data

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-059 @PROPOSED
Feature: Browser compatibility
  Scenario: Open a tile and profile in Chromium
    Given USER-A starts a clean Chromium browser context with the same fixture data
    When USER-A signs in
    And USER-A opens the Cashflow tile
    And USER-A opens the avatar menu
    And USER-A opens User Profile
    Then User Profile shows USER-A
    And the Cashflow workspace tab remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed browser probe. Record actual Chromium version before execution; supported browser policy is unknown.

#### UX-060

**Open a tile and profile in Microsoft Edge**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A starts a clean Microsoft Edge browser context with the same fixture data

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-060 @PROPOSED
Feature: Browser compatibility
  Scenario: Open a tile and profile in Microsoft Edge
    Given USER-A starts a clean Microsoft Edge browser context with the same fixture data
    When USER-A signs in
    And USER-A opens the Cashflow tile
    And USER-A opens the avatar menu
    And USER-A opens User Profile
    Then User Profile shows USER-A
    And the Cashflow workspace tab remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed browser probe. Record actual Microsoft Edge version before execution; supported browser policy is unknown.

#### UX-061

**Open a tile and profile in Firefox**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A starts a clean Firefox browser context with the same fixture data

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-061 @PROPOSED
Feature: Browser compatibility
  Scenario: Open a tile and profile in Firefox
    Given USER-A starts a clean Firefox browser context with the same fixture data
    When USER-A signs in
    And USER-A opens the Cashflow tile
    And USER-A opens the avatar menu
    And USER-A opens User Profile
    Then User Profile shows USER-A
    And the Cashflow workspace tab remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed browser probe. Record actual Firefox version before execution; supported browser policy is unknown.

#### UX-062

**Open a tile and profile in WebKit**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A starts a clean WebKit browser context with the same fixture data

Behavior basis: [UI-SRC-059:48](<../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48>)

```gherkin
@UX-062 @PROPOSED
Feature: Browser compatibility
  Scenario: Open a tile and profile in WebKit
    Given USER-A starts a clean WebKit browser context with the same fixture data
    When USER-A signs in
    And USER-A opens the Cashflow tile
    And USER-A opens the avatar menu
    And USER-A opens User Profile
    Then User Profile shows USER-A
    And the Cashflow workspace tab remains visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed browser probe. Record actual WebKit version before execution; supported browser policy is unknown.
### Group: Dependency resilience

<a id="group-dependency-resilience"></a>

#### UX-063

**Keep the shell usable when analytics is unavailable**

Version: 1. Level: UI system test design. Priority: P1. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has the shell open and all analytics requests return HTTP 503

Behavior basis: [UI-SRC-061:18](<../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L18>)

```gherkin
@UX-063 @PROPOSED
Feature: Dependency resilience
  Scenario: Keep the shell usable when analytics is unavailable
    Given USER-A has the shell open and all analytics requests return HTTP 503
    When USER-A opens User Profile
    And USER-A closes User Profile
    Then User Profile opens and closes
    And the shell remains visible without an analytics error replacing it
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.

#### UX-064

**Keep visible UI state when a browser extension blocks photos**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: USER-A.

Setup: Use the isolated fixture in the catalog. USER-A has authenticated shell data and a request-blocking fixture for both profile photo hosts

Behavior basis: [UI-SRC-060:27](<../../repos/ui/mfe-base/src/components/Avatar/index.tsx#L27>)

```gherkin
@UX-064 @PROPOSED
Feature: Dependency resilience
  Scenario: Keep visible UI state when a browser extension blocks photos
    Given USER-A has authenticated shell data and a request-blocking fixture for both profile photo hosts
    When USER-A opens the avatar menu
    And USER-A activates the profile entry
    Then the menu shows USER-A identity text
    And User Profile remains operable
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture snapshot and close this case browser context.

Limits: Proposed quality expectation. Owner unknown; approve the assertion before business acceptance.
### Group: Grid and regional boundaries

<a id="group-grid-and-regional-boundaries"></a>

#### UX-065

**Sort category grid labels in ascending order**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid has C1 label Alpha and C2 label Beta

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-065 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Sort category grid labels in ascending order
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid has C1 label Alpha and C2 label Beta
    When select ascending sort on Category Label
    Then the grid shows Alpha before Beta
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-066

**Sort category grid labels in descending order**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid has C1 label Alpha and C2 label Beta

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-066 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Sort category grid labels in descending order
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid has C1 label Alpha and C2 label Beta
    When select descending sort on Category Label
    Then the grid shows Beta before Alpha
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-067

**Filter the category grid to zero matches**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid has only C1 Alpha and C2 Beta

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-067 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Filter the category grid to zero matches
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid has only C1 Alpha and C2 Beta
    When set Category Label filter to equals Missing
    Then the grid shows its no-matching-rows state
    And the pagination range contains zero matched rows
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-068

**Clear a category grid filter**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid has C1 Alpha and C2 Beta with a no-match filter active

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-068 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Clear a category grid filter
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid has C1 Alpha and C2 Beta with a no-match filter active
    When remove the Category Label filter
    Then the grid exposes both C1 and C2 through its pagination range
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-069

**Hide and restore a grid column**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid shows Owner with TEST_OWNER

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-069 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Hide and restore a grid column
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid shows Owner with TEST_OWNER
    When hide the Owner column through column controls
    And restore the Owner column
    Then the Owner header and TEST_OWNER cell are visible again
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-070

**Export normal category grid identities**

Version: 1. Level: UI export integration design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER.

Setup: Use controlled data and a fresh browser context. category grid contains only C1 Alpha and C2 Beta

Behavior basis: [UI-SRC-086:43](<../../repos/ui/mfe-base/src/components/Table/index.tsx#L43>)

```gherkin
@UX-070 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Export normal category grid identities
    Given UI-ADMIN-01; FMO PORTAL ADMIN TEST_OWNER uses the isolated case fixture
    And category grid contains only C1 Alpha and C2 Beta
    When activate the grid export action
    And read the generated CSV artifact
    Then the export contains C1 Alpha and C2 Beta once each
    And the header fields align with the exported values
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-071

**Display an unknown regional entry name**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated portal user.

Setup: Use controlled data and a fresh browser context. Tile Options contains a fixture tile with entryName Mars

Behavior basis: [UI-SRC-064:20](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L20>)

```gherkin
@UX-071 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Display an unknown regional entry name
    Given UI-USER-01; authenticated portal user uses the isolated case fixture
    And Tile Options contains a fixture tile with entryName Mars
    When open Tile Options
    Then the entry label Mars is readable
    And no Indonesia icon identifies the Mars entry
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.

#### UX-072

**Distinguish duplicate regional entry labels**

Version: 1. Level: UI system test design. Priority: P2. Basis: `PROPOSED`.

Actor: UI-USER-01; authenticated portal user.

Setup: Use controlled data and a fresh browser context. Tile Options has two enabled Test Tile entries named Indonesia with different tile routes

Behavior basis: [UI-SRC-064:20](<../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L20>)

```gherkin
@UX-072 @PROPOSED
Feature: Grid and regional boundaries
  Scenario: Distinguish duplicate regional entry labels
    Given UI-USER-01; authenticated portal user uses the isolated case fixture
    And Tile Options has two enabled Test Tile entries named Indonesia with different tile routes
    When open Tile Options
    Then the two entries expose distinguishable route or record identifiers
    And each entry can be selected independently
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Restore the fixture and close the browser context.

Limits: Proposed boundary assertion. Confirm behavior before acceptance. Grid counts use data/page ranges rather than virtualized DOM row counts.
### Group: Admin validation

<a id="group-admin-validation"></a>

#### BFF-ADM-001

**Reject empty Import Map Module Name on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Module Name is empty

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-001 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Import Map Module Name on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Module Name is empty
    When Admin A selects Create
    Then the form remains open
    And Please provide the value for the Module Name or Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-002

**Reject empty Import Map Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Path is empty

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-002 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Import Map Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Path is empty
    When Admin A selects Create
    Then the form remains open
    And Please provide the value for the Module Name or Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-003

**Reject embedded spaces in Import Map Module Name on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has Module Name=container a; the other required field is valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-003 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Import Map Module Name on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has Module Name=container a; the other required field is valid
    When Admin A selects Create
    Then the form remains open
    And You should not enter any space character on the Module Name or Path. is visible
    And the invalid version does not appear in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-004

**Reject embedded spaces in Import Map Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has Path=https://fixture.example/container a.js; the other required field is valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-004 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Import Map Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has Path=https://fixture.example/container a.js; the other required field is valid
    When Admin A selects Create
    Then the form remains open
    And You should not enter any space character on the Module Name or Path. is visible
    And the invalid version does not appear in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-005

**Reject empty Import Map Module Name on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map update form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Module Name is empty

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-005 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Import Map Module Name on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map update form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Module Name is empty
    When Admin A selects Update
    Then the form remains open
    And Please provide the value for the Module Name or Path is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-006

**Reject empty Import Map Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map update form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Path is empty

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-006 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Import Map Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map update form uses Module Name=container-a and Path=https://fixture.example/container-a.js; Path is empty
    When Admin A selects Update
    Then the form remains open
    And Please provide the value for the Module Name or Path is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-007

**Reject embedded spaces in Import Map Module Name on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map update form has Module Name=container a; the other required field is valid

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-007 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Import Map Module Name on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map update form has Module Name=container a; the other required field is valid
    When Admin A selects Update
    Then the form remains open
    And You should not enter any space character on the Module Name or Path. is visible
    And the invalid version does not appear in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-008

**Reject embedded spaces in Import Map Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map update form has Path=https://fixture.example/container a.js; the other required field is valid

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-008 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Import Map Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map update form has Path=https://fixture.example/container a.js; the other required field is valid
    When Admin A selects Update
    Then the form remains open
    And You should not enter any space character on the Module Name or Path. is visible
    And the invalid version does not appear in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-009

**Reject empty Tile Title on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Title is empty; other required fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-009 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Title on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Title is empty; other required fields are valid
    When Admin A selects Create
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-010

**Reject empty Tile Module Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Module Path is empty; other required fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-010 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Module Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Module Path is empty; other required fields are valid
    When Admin A selects Create
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-011

**Reject empty Tile Tile Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Tile Path is empty; other required fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-011 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Tile Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form references Category 101 and Import Map 201 owned by FMO_ADMIN; Tile Path is empty; other required fields are valid
    When Admin A selects Create
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-012

**Reject embedded spaces in Tile Module Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form references Category 101 and Import Map 201; Module Path=module a; all remaining fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-012 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Tile Module Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form references Category 101 and Import Map 201; Module Path=module a; all remaining fields are valid
    When Admin A selects Create
    Then the form remains open
    And You should not enter any space character on the Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-013

**Reject embedded spaces in Tile Tile Path on create**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form references Category 101 and Import Map 201; Tile Path=tile a; all remaining fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-013 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Tile Tile Path on create
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form references Category 101 and Import Map 201; Tile Path=tile a; all remaining fields are valid
    When Admin A selects Create
    Then the form remains open
    And You should not enter any space character on the Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-014

**Reject empty Tile Title on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Title is empty; other required fields are valid

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-014 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Title on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Title is empty; other required fields are valid
    When Admin A selects Update
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-015

**Reject empty Tile Module Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Module Path is empty; other required fields are valid

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-015 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Module Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Module Path is empty; other required fields are valid
    When Admin A selects Update
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-016

**Reject empty Tile Tile Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Tile Path is empty; other required fields are valid

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-016 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject empty Tile Tile Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile update form references Category 101 and Import Map 201 owned by FMO_ADMIN; Tile Path is empty; other required fields are valid
    When Admin A selects Update
    Then the form remains open
    And Please provide the value for the Title or Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-017

**Reject embedded spaces in Tile Module Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile update form references Category 101 and Import Map 201; Module Path=module a; all remaining fields are valid

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-017 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Tile Module Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile update form references Category 101 and Import Map 201; Module Path=module a; all remaining fields are valid
    When Admin A selects Update
    Then the form remains open
    And You should not enter any space character on the Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-018

**Reject embedded spaces in Tile Tile Path on update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile update form references Category 101 and Import Map 201; Tile Path=tile a; all remaining fields are valid

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-018 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject embedded spaces in Tile Tile Path on update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile update form references Category 101 and Import Map 201; Tile Path=tile a; all remaining fields are valid
    When Admin A selects Update
    Then the form remains open
    And You should not enter any space character on the Module Path or Tile Path. is visible
    And the grid contains no saved version with the invalid value
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-019

**Proposed rejection of non-ASCII or control whitespace in Module Name**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has Module Name='container\ta'; all remaining fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-019 @PROPOSED
Feature: Admin validation
  Scenario: Proposed rejection of non-ASCII or control whitespace in Module Name
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has Module Name='container\ta'; all remaining fields are valid
    When Admin A selects Create
    Then the form remains open
    And a field validation error identifies the unsafe whitespace
    And no new Import Map row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source checks literal U+0020 after trim. Tab and U+00A0 policy remains unknown.

#### BFF-ADM-020

**Proposed rejection of non-ASCII or control whitespace in Path**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has Path='https://fixture.example/a\xa0b.js'; all remaining fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-020 @PROPOSED
Feature: Admin validation
  Scenario: Proposed rejection of non-ASCII or control whitespace in Path
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has Path='https://fixture.example/a\xa0b.js'; all remaining fields are valid
    When Admin A selects Create
    Then the form remains open
    And a field validation error identifies the unsafe whitespace
    And no new Import Map row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source checks literal U+0020 after trim. Tab and U+00A0 policy remains unknown.

#### BFF-ADM-021

**Reject Tile Filter Rule not-json**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is 'not-json'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-021 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule not-json
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is 'not-json'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.

#### BFF-ADM-022

**Reject Tile Filter Rule []**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is '[]'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-022 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule []
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is '[]'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.

#### BFF-ADM-023

**Reject Tile Filter Rule null**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is 'null'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-023 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule null
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is 'null'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.

#### BFF-ADM-024

**Reject Tile Filter Rule {}**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is '{}'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-024 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule {}
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is '{}'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.

#### BFF-ADM-025

**Reject Tile Filter Rule {"filterType":"UNKNOWN"}**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is '{"filterType":"UNKNOWN"}'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-025 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule {"filterType":"UNKNOWN"}
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is '{"filterType":"UNKNOWN"}'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.

#### BFF-ADM-026

**Reject Tile Filter Rule {"filterType":null}**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Tile form references Category 101 and Import Map 201; Filter Rule is '{"filterType":null}'; other required fields are valid

Behavior basis: [UI-SRC-027:201](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201>); [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-026 @IMPLEMENTATION
Feature: Admin validation
  Scenario: Reject Tile Filter Rule {"filterType":null}
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Tile form references Category 101 and Import Map 201; Filter Rule is '{"filterType":null}'; other required fields are valid
    When Admin A selects Create
    Then the Tile form remains open
    And a service error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Filter Rule validation throws RuntimeException. A dedicated field error is not established; UI error text needs execution.
### Group: Admin uniqueness

<a id="group-admin-uniqueness"></a>

#### BFF-ADM-027

**Reject a duplicate Category Label**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the database already contains Category Label=shared-a; the new Category form uses that same value and other fields are valid

Behavior basis: [UI-SRC-015:80](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L80>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-027 @IMPLEMENTATION
Feature: Admin uniqueness
  Scenario: Reject a duplicate Category Label
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the database already contains Category Label=shared-a; the new Category form uses that same value and other fields are valid
    When Admin A selects Create
    Then Record not created. is visible
    And the Category grid contains only the existing shared-a record
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-028

**Reject a duplicate Category Label during update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: two Category records have different identifiers; one has Category Label=shared-a; Admin A edits the other record to shared-a

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-028 @IMPLEMENTATION
Feature: Admin uniqueness
  Scenario: Reject a duplicate Category Label during update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And two Category records have different identifiers; one has Category Label=shared-a; Admin A edits the other record to shared-a
    When Admin A selects Update
    Then Record not updated. is visible
    And the grid does not show a successful duplicate-name update
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-029

**Reject a duplicate Import Map Module Name**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the database already contains Import Map Module Name=shared-a; the new Import Map form uses that same value and other fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-029 @IMPLEMENTATION
Feature: Admin uniqueness
  Scenario: Reject a duplicate Import Map Module Name
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the database already contains Import Map Module Name=shared-a; the new Import Map form uses that same value and other fields are valid
    When Admin A selects Create
    Then Record not created. is visible
    And the Import Map grid contains only the existing shared-a record
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-030

**Reject a duplicate Import Map Module Name during update**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: two Import Map records have different identifiers; one has Import Map Module Name=shared-a; Admin A edits the other record to shared-a

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-030 @IMPLEMENTATION
Feature: Admin uniqueness
  Scenario: Reject a duplicate Import Map Module Name during update
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And two Import Map records have different identifiers; one has Import Map Module Name=shared-a; Admin A edits the other record to shared-a
    When Admin A selects Update
    Then Record not updated. is visible
    And the grid does not show a successful duplicate-name update
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.
### Group: Admin storage boundary

<a id="group-admin-storage-boundary"></a>

#### BFF-ADM-031

**Category Category Label schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Category create form sets Category Label to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-015:80](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L80>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-031 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Category Category Label schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Category create form sets Category Label to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Category row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-032

**Category Category Label schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Category create form sets Category Label to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-015:80](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L80>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-032 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Category Category Label schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Category create form sets Category Label to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Category row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-033

**Import Map Module Name schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Import Map create form sets Module Name to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-033 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Import Map Module Name schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Import Map create form sets Module Name to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Import Map row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-034

**Import Map Module Name schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Import Map create form sets Module Name to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-034 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Import Map Module Name schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Import Map create form sets Module Name to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Import Map row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-035

**Import Map Path schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Import Map create form sets Path to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-035 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Import Map Path schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Import Map create form sets Path to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Import Map row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-036

**Import Map Path schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Import Map create form sets Path to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-036 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Import Map Path schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Import Map create form sets Path to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Import Map row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-037

**Tile Title schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Title to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-037 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Title schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Title to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Tile row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-038

**Tile Title schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Title to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-038 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Title schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Title to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Tile row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-039

**Tile Module Path schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Module Path to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-039 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Module Path schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Module Path to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Tile row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-040

**Tile Module Path schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Module Path to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-040 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Module Path schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Module Path to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Tile row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-041

**Tile Tile Path schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Tile Path to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-041 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Tile Path schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Tile Path to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Tile row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-042

**Tile Tile Path schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Tile Path to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-042 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Tile Path schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Tile Path to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Tile row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-043

**Tile Entry Name schema boundary at 255 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Entry Name to exactly 255 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-030:1](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_0__application_tile_modify.sql#L1>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-043 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Entry Name schema boundary at 255 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Entry Name to exactly 255 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Tile row
    And the returned field contains exactly 255 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-044

**Tile Entry Name schema boundary at 256 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile create form sets Entry Name to exactly 256 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-030:1](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_0__application_tile_modify.sql#L1>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-044 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile Entry Name schema boundary at 256 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile create form sets Entry Name to exactly 256 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Tile row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The 255-character limit comes from migration DDL. It is not an independently approved business limit. No deployed-schema parity is established.

#### BFF-ADM-045

**Tile EMS2 Entities schema boundary at 32000 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile form sets EMS2 Entities to exactly 32000 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-045 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile EMS2 Entities schema boundary at 32000 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile form sets EMS2 Entities to exactly 32000 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid shows the created Tile row
    And the persisted value contains exactly 32000 characters
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-046

**Tile EMS2 Entities schema boundary at 32001 characters**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the prepared database follows the inspected schema; the Tile form sets EMS2 Entities to exactly 32001 ASCII a characters; all other fields are valid

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-046 @IMPLEMENTATION
Feature: Admin storage boundary
  Scenario: Tile EMS2 Entities schema boundary at 32001 characters
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the prepared database follows the inspected schema; the Tile form sets EMS2 Entities to exactly 32001 ASCII a characters; all other fields are valid
    When Admin A selects Create
    Then the grid does not add a new Tile row
    And Record not created. is visible
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.
### Group: Admin persistence

<a id="group-admin-persistence"></a>

#### BFF-ADM-047

**Deny Category create when creation is disabled**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Category create form has valid fields; fmaaProperties.creationEnabled=false

Behavior basis: [UI-SRC-023:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-047 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Deny Category create when creation is disabled
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Category create form has valid fields; fmaaProperties.creationEnabled=false
    When Admin A selects Create
    Then Adding new record is not permitted. Record not created. is visible
    And the Category grid does not add a row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-034:220](<../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v1/ApplicationCategoryServiceTest.java#L220>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-048

**Handle Category database save failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Category create form has valid fields; the repository save throws a controlled database exception

Behavior basis: [UI-SRC-023:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-048 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Category database save failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Category create form has valid fields; the repository save throws a controlled database exception
    When Admin A selects Create
    Then Record not created. is visible
    And the grid does not add a successful Category row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-049

**Handle Category update database failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A edits existing Category record 101; repository save throws a controlled database exception

Behavior basis: [UI-SRC-023:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-049 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Category update database failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A edits existing Category record 101; repository save throws a controlled database exception
    When Admin A selects Update
    Then Record not updated. is visible
    And the grid does not display the rejected Category values as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-050

**Reconcile Category after audit write fails**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Category primary save succeeds but its audit write fails; the UI receives an error

Behavior basis: [UI-SRC-023:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java#L40>); [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-050 @PROPOSED
Feature: Admin persistence
  Scenario: Reconcile Category after audit write fails
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Category primary save succeeds but its audit write fails; the UI receives an error
    When Admin A reloads the admin data
    Then the grid displays the actual persisted record once
    And the UI does not create a second record merely to resolve the failed audit response
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Primary save precedes audit create. No encompassing controller transaction is declared; actual rollback and retry semantics require investigation.

#### BFF-ADM-051

**Deny Import Map create when creation is disabled**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has valid fields; fmaaProperties.creationEnabled=false

Behavior basis: [UI-SRC-025:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java#L42>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-051 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Deny Import Map create when creation is disabled
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has valid fields; fmaaProperties.creationEnabled=false
    When Admin A selects Create
    Then Adding new record is not permitted. Record not created. is visible
    And the Import Map grid does not add a row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-052

**Handle Import Map database save failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map create form has valid fields; the repository save throws a controlled database exception

Behavior basis: [UI-SRC-025:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java#L42>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-052 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Import Map database save failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map create form has valid fields; the repository save throws a controlled database exception
    When Admin A selects Create
    Then Record not created. is visible
    And the grid does not add a successful Import Map row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-053

**Handle Import Map update database failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A edits existing Import Map record 101; repository save throws a controlled database exception

Behavior basis: [UI-SRC-025:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java#L42>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-053 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Import Map update database failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A edits existing Import Map record 101; repository save throws a controlled database exception
    When Admin A selects Update
    Then Record not updated. is visible
    And the grid does not display the rejected Import Map values as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-054

**Reconcile Import Map after audit write fails**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Import Map primary save succeeds but its audit write fails; the UI receives an error

Behavior basis: [UI-SRC-025:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java#L42>); [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-054 @PROPOSED
Feature: Admin persistence
  Scenario: Reconcile Import Map after audit write fails
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Import Map primary save succeeds but its audit write fails; the UI receives an error
    When Admin A reloads the admin data
    Then the grid displays the actual persisted record once
    And the UI does not create a second record merely to resolve the failed audit response
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Primary save precedes audit create. No encompassing controller transaction is declared; actual rollback and retry semantics require investigation.

#### BFF-ADM-055

**Deny Tile create when creation is disabled**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form has valid fields; fmaaProperties.creationEnabled=false

Behavior basis: [UI-SRC-024:61](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java#L61>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-055 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Deny Tile create when creation is disabled
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form has valid fields; fmaaProperties.creationEnabled=false
    When Admin A selects Create
    Then Adding new record is not permitted. Record not created. is visible
    And the Tile grid does not add a row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-056

**Handle Tile database save failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile create form has valid fields; the repository save throws a controlled database exception

Behavior basis: [UI-SRC-024:61](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java#L61>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-056 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Tile database save failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile create form has valid fields; the repository save throws a controlled database exception
    When Admin A selects Create
    Then Record not created. is visible
    And the grid does not add a successful Tile row
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-057

**Handle Tile update database failure**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A edits existing Tile record 101; repository save throws a controlled database exception

Behavior basis: [UI-SRC-024:61](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java#L61>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-057 @IMPLEMENTATION
Feature: Admin persistence
  Scenario: Handle Tile update database failure
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A edits existing Tile record 101; repository save throws a controlled database exception
    When Admin A selects Update
    Then Record not updated. is visible
    And the grid does not display the rejected Tile values as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-058

**Reconcile Tile after audit write fails**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile primary save succeeds but its audit write fails; the UI receives an error

Behavior basis: [UI-SRC-024:61](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java#L61>); [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-058 @PROPOSED
Feature: Admin persistence
  Scenario: Reconcile Tile after audit write fails
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile primary save succeeds but its audit write fails; the UI receives an error
    When Admin A reloads the admin data
    Then the grid displays the actual persisted record once
    And the UI does not create a second record merely to resolve the failed audit response
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Primary save precedes audit create. No encompassing controller transaction is declared; actual rollback and retry semantics require investigation.
### Group: Admin authority

<a id="group-admin-authority"></a>

#### BFF-ADM-059

**Reject self-verification of Category**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Category record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-059 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject self-verification of Category
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Category record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Category record 101 remains inactive in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-060

**Reject case-only self-verification of Category**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Category record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-060 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject case-only self-verification of Category
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Category record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Category record 101 remains inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-061

**Reject Category update after ownership changes**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Category record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-061 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Category update after ownership changes
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Category record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission
    When Admin A selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted change as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-062

**Reject Category update from SUPER_USER without matching owner**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin S, user admin-s with only SUPER_USER.

Setup: Category record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-062 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Category update from SUPER_USER without matching owner
    Given Admin S, user admin-s with only SUPER_USER uses an isolated browser context with valid access and entitlement credentials
    And Category record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture
    When Admin S selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted update as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The BFF compares exact record owner with the derived role. A global SUPER_USER bypass is not implemented by this branch.

#### BFF-ADM-063

**Protect foreign-owner Category audit data**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901

Behavior basis: [UI-SRC-015:105](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L105>); [UI-SRC-027:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L42>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-063 @PROPOSED
Feature: Admin authority
  Scenario: Protect foreign-owner Category audit data
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901
    When Admin A opens Audit
    Then the UI displays an access-denied error
    And no audit fields from record 901 appear
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The audit reader validates credentials but does not compare the requested record owner. Record-level read policy remains unresolved.

#### BFF-ADM-064

**Reject self-verification of Import Map**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Import Map record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-064 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject self-verification of Import Map
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Import Map record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Import Map record 101 remains inactive in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-032:544](<../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ImportMapControllerTest.java#L544>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-065

**Reject case-only self-verification of Import Map**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Import Map record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-065 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject case-only self-verification of Import Map
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Import Map record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Import Map record 101 remains inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-066

**Reject Import Map update after ownership changes**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Import Map record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-066 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Import Map update after ownership changes
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Import Map record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission
    When Admin A selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted change as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-067

**Reject Import Map update from SUPER_USER without matching owner**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin S, user admin-s with only SUPER_USER.

Setup: Import Map record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-067 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Import Map update from SUPER_USER without matching owner
    Given Admin S, user admin-s with only SUPER_USER uses an isolated browser context with valid access and entitlement credentials
    And Import Map record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture
    When Admin S selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted update as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The BFF compares exact record owner with the derived role. A global SUPER_USER bypass is not implemented by this branch.

#### BFF-ADM-068

**Protect foreign-owner Import Map audit data**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901

Behavior basis: [UI-SRC-017:141](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L141>); [UI-SRC-027:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L42>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-068 @PROPOSED
Feature: Admin authority
  Scenario: Protect foreign-owner Import Map audit data
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901
    When Admin A opens Audit
    Then the UI displays an access-denied error
    And no audit fields from record 901 appear
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The audit reader validates credentials but does not compare the requested record owner. Record-level read policy remains unresolved.

#### BFF-ADM-069

**Reject self-verification of Tile**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Tile record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-069 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject self-verification of Tile
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Tile record 101 is inactive and updatedBy=admin-a; Admin A opens its Verify dialog
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Tile record 101 remains inactive in the grid
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: [UI-SRC-031:631](<../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java#L631>)

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-070

**Reject case-only self-verification of Tile**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Tile record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-070 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject case-only self-verification of Tile
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Tile record 101 is inactive and updatedBy=ADMIN-A; the authenticated subject is admin-a
    When Admin A selects Verified
    Then Maker and Checker should be different user. is visible
    And Tile record 101 remains inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-071

**Reject Tile update after ownership changes**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Tile record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-071 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Tile update after ownership changes
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Tile record 101 under FMO_ADMIN; a controlled fixture changes its owner to OTHER_ADMIN before submission
    When Admin A selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted change as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-072

**Reject Tile update from SUPER_USER without matching owner**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin S, user admin-s with only SUPER_USER.

Setup: Tile record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-072 @IMPLEMENTATION
Feature: Admin authority
  Scenario: Reject Tile update from SUPER_USER without matching owner
    Given Admin S, user admin-s with only SUPER_USER uses an isolated browser context with valid access and entitlement credentials
    And Tile record 101 has owner FMO_ADMIN; Admin S has only SUPER_USER and reaches its existing detail through a controlled stale fixture
    When Admin S selects Update
    Then You do not have access to this record. is visible
    And the grid does not display the attempted update as saved
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The BFF compares exact record owner with the derived role. A global SUPER_USER bypass is not implemented by this branch.

#### BFF-ADM-073

**Protect foreign-owner Tile audit data**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901

Behavior basis: [UI-SRC-016:180](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L180>); [UI-SRC-027:42](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L42>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-073 @PROPOSED
Feature: Admin authority
  Scenario: Protect foreign-owner Tile audit data
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A has no OTHER_ADMIN role; a controlled UI-origin audit request identifies OTHER_ADMIN record 901
    When Admin A opens Audit
    Then the UI displays an access-denied error
    And no audit fields from record 901 appear
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The audit reader validates credentials but does not compare the requested record owner. Record-level read policy remains unresolved.
### Group: Admin references

<a id="group-admin-references"></a>

#### BFF-ADM-074

**Reject a Tile update with foreign-owner Category 102**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Tile 301 belongs to FMO_ADMIN; its form submits Category 102 owned by OTHER_ADMIN while all other references belong to FMO_ADMIN

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-074 @IMPLEMENTATION
Feature: Admin references
  Scenario: Reject a Tile update with foreign-owner Category 102
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Tile 301 belongs to FMO_ADMIN; its form submits Category 102 owned by OTHER_ADMIN while all other references belong to FMO_ADMIN
    When Admin A selects Update
    Then You do not have access to this record. is visible
    And the grid retains the previously loaded Tile references
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-075

**Protect Tile creation from foreign-owner Category 102**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A uses a controlled UI-origin request substitution to select Category 102 owned by OTHER_ADMIN for a new Tile

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-075 @PROPOSED
Feature: Admin references
  Scenario: Protect Tile creation from foreign-owner Category 102
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A uses a controlled UI-origin request substitution to select Category 102 owned by OTHER_ADMIN for a new Tile
    When Admin A selects Create
    Then an access-denied error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The Tile create branch loads references but does not call checkEms2Role. UI option filtering does not prove server enforcement.

#### BFF-ADM-076

**Reject a Tile update with foreign-owner Import Map 202**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Tile 301 belongs to FMO_ADMIN; its form submits Import Map 202 owned by OTHER_ADMIN while all other references belong to FMO_ADMIN

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-076 @IMPLEMENTATION
Feature: Admin references
  Scenario: Reject a Tile update with foreign-owner Import Map 202
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Tile 301 belongs to FMO_ADMIN; its form submits Import Map 202 owned by OTHER_ADMIN while all other references belong to FMO_ADMIN
    When Admin A selects Update
    Then You do not have access to this record. is visible
    And the grid retains the previously loaded Tile references
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-077

**Protect Tile creation from foreign-owner Import Map 202**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A uses a controlled UI-origin request substitution to select Import Map 202 owned by OTHER_ADMIN for a new Tile

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-077 @PROPOSED
Feature: Admin references
  Scenario: Protect Tile creation from foreign-owner Import Map 202
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A uses a controlled UI-origin request substitution to select Import Map 202 owned by OTHER_ADMIN for a new Tile
    When Admin A selects Create
    Then an access-denied error is visible
    And no new Tile row appears
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The Tile create branch loads references but does not call checkEms2Role. UI option filtering does not prove server enforcement.

#### BFF-ADM-078

**Handle a missing Tile reference for Category 101**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile form holds Category 101 in its selected options; a controlled fixture removes that reference before save

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-078 @IMPLEMENTATION
Feature: Admin references
  Scenario: Handle a missing Tile reference for Category 101
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile form holds Category 101 in its selected options; a controlled fixture removes that reference before save
    When Admin A selects Create
    Then a service error is visible
    And the Tile form remains open
    And no successful Tile row is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-079

**Handle a missing Tile reference for Import Map 201**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile form holds Import Map 201 in its selected options; a controlled fixture removes that reference before save

Behavior basis: [UI-SRC-016:118](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-079 @IMPLEMENTATION
Feature: Admin references
  Scenario: Handle a missing Tile reference for Import Map 201
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile form holds Import Map 201 in its selected options; a controlled fixture removes that reference before save
    When Admin A selects Create
    Then a service error is visible
    And the Tile form remains open
    And no successful Tile row is added
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-080

**Validate a cleared Tile reference without a server exception**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the Tile edit form references Category 101 and Import Map 201; Admin A clears Import Map

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-020:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L6>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-080 @PROPOSED
Feature: Admin references
  Scenario: Validate a cleared Tile reference without a server exception
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the Tile edit form references Category 101 and Import Map 201; Admin A clears Import Map
    When Admin A selects Update
    Then the form remains open
    And an Import Map required-field error is visible
    And no Tile update is reported as successful
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Missing nested references can reach unchecked dereferences. A field-level validation contract is not established.

#### BFF-ADM-081

**Protect activation when Tile references inactive Category 101**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin B, user admin-b with FMO_ADMIN.

Setup: Tile 301 is inactive; Category 101 is inactive; Admin B is a different maker/checker subject

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-022:24](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/repository/ApplicationCategoryRepo.java#L24>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-081 @PROPOSED
Feature: Admin references
  Scenario: Protect activation when Tile references inactive Category 101
    Given Admin B, user admin-b with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Tile 301 is inactive; Category 101 is inactive; Admin B is a different maker/checker subject
    When Admin B selects Verified
    Then the UI displays an inactive-reference error
    And Tile 301 remains inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The verify branch checks owner and maker identity. It does not establish an active-parent prerequisite; business policy is unknown.

#### BFF-ADM-082

**Protect activation when Tile references inactive Import Map 201**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin B, user admin-b with FMO_ADMIN.

Setup: Tile 301 is inactive; Import Map 201 is inactive; Admin B is a different maker/checker subject

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-027:183](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183>); [UI-SRC-022:24](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/repository/ApplicationCategoryRepo.java#L24>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-082 @PROPOSED
Feature: Admin references
  Scenario: Protect activation when Tile references inactive Import Map 201
    Given Admin B, user admin-b with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Tile 301 is inactive; Import Map 201 is inactive; Admin B is a different maker/checker subject
    When Admin B selects Verified
    Then the UI displays an inactive-reference error
    And Tile 301 remains inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The verify branch checks owner and maker identity. It does not establish an active-parent prerequisite; business policy is unknown.
### Group: Admin concurrency

<a id="group-admin-concurrency"></a>

#### BFF-ADM-083

**Protect Category from stale edit overwrite**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Category record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-019:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java#L6>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-083 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Category from stale edit overwrite
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Category record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE
    When Admin A selects Update
    Then the UI shows a stale-record error
    And reloading shows value NEW
    And Admin A can reload the latest record before retry
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: No DTO version or entity @Version was found. Current source does not establish optimistic concurrency or stale-update rejection.

#### BFF-ADM-084

**Protect Category verification from a concurrent maker change**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin B, user admin-b with FMO_ADMIN.

Setup: Admin B opens Verify for inactive Category record 101; Admin A saves a new version before verification

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-019:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java#L6>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-084 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Category verification from a concurrent maker change
    Given Admin B, user admin-b with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B opens Verify for inactive Category record 101; Admin A saves a new version before verification
    When Admin B selects Verified
    Then the UI shows a stale-verification error
    And the new unreviewed values remain inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The controller reloads the current record but receives no reviewed version identifier. Approval of unseen changes is not prevented by an explicit version check.

#### BFF-ADM-085

**Protect duplicate Category verification**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin C, user admin-c with FMO_ADMIN.

Setup: Admin B and Admin C open Verify for the same inactive Category; Admin B verifies first

Behavior basis: [UI-SRC-015:40](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40>); [UI-SRC-019:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java#L6>); [UI-SRC-037:48](<../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-085 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect duplicate Category verification
    Given Admin C, user admin-c with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B and Admin C open Verify for the same inactive Category; Admin B verifies first
    When Admin C selects Verified
    Then the UI reports that the record is already active
    And reloading still shows the record active
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Checker mode against an already active record enters the maker branch in the current controller. Intended conflict handling is unknown.

#### BFF-ADM-086

**Protect Import Map from stale edit overwrite**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Import Map record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-021:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfImportMap.java#L6>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-086 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Import Map from stale edit overwrite
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Import Map record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE
    When Admin A selects Update
    Then the UI shows a stale-record error
    And reloading shows value NEW
    And Admin A can reload the latest record before retry
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: No DTO version or entity @Version was found. Current source does not establish optimistic concurrency or stale-update rejection.

#### BFF-ADM-087

**Protect Import Map verification from a concurrent maker change**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin B, user admin-b with FMO_ADMIN.

Setup: Admin B opens Verify for inactive Import Map record 101; Admin A saves a new version before verification

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-021:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfImportMap.java#L6>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-087 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Import Map verification from a concurrent maker change
    Given Admin B, user admin-b with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B opens Verify for inactive Import Map record 101; Admin A saves a new version before verification
    When Admin B selects Verified
    Then the UI shows a stale-verification error
    And the new unreviewed values remain inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The controller reloads the current record but receives no reviewed version identifier. Approval of unseen changes is not prevented by an explicit version check.

#### BFF-ADM-088

**Protect duplicate Import Map verification**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin C, user admin-c with FMO_ADMIN.

Setup: Admin B and Admin C open Verify for the same inactive Import Map; Admin B verifies first

Behavior basis: [UI-SRC-017:60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60>); [UI-SRC-021:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfImportMap.java#L6>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-088 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect duplicate Import Map verification
    Given Admin C, user admin-c with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B and Admin C open Verify for the same inactive Import Map; Admin B verifies first
    When Admin C selects Verified
    Then the UI reports that the record is already active
    And reloading still shows the record active
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Checker mode against an already active record enters the maker branch in the current controller. Intended conflict handling is unknown.

#### BFF-ADM-089

**Protect Tile from stale edit overwrite**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Admin A opens Tile record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-020:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L6>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-089 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Tile from stale edit overwrite
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Admin A opens Tile record 101 with value OLD; Admin B saves value NEW before Admin A submits STALE
    When Admin A selects Update
    Then the UI shows a stale-record error
    And reloading shows value NEW
    And Admin A can reload the latest record before retry
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: No DTO version or entity @Version was found. Current source does not establish optimistic concurrency or stale-update rejection.

#### BFF-ADM-090

**Protect Tile verification from a concurrent maker change**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin B, user admin-b with FMO_ADMIN.

Setup: Admin B opens Verify for inactive Tile record 101; Admin A saves a new version before verification

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-020:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L6>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-090 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect Tile verification from a concurrent maker change
    Given Admin B, user admin-b with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B opens Verify for inactive Tile record 101; Admin A saves a new version before verification
    When Admin B selects Verified
    Then the UI shows a stale-verification error
    And the new unreviewed values remain inactive
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The controller reloads the current record but receives no reviewed version identifier. Approval of unseen changes is not prevented by an explicit version check.

#### BFF-ADM-091

**Protect duplicate Tile verification**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin C, user admin-c with FMO_ADMIN.

Setup: Admin B and Admin C open Verify for the same inactive Tile; Admin B verifies first

Behavior basis: [UI-SRC-016:46](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46>); [UI-SRC-020:6](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L6>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-091 @PROPOSED
Feature: Admin concurrency
  Scenario: Protect duplicate Tile verification
    Given Admin C, user admin-c with FMO_ADMIN uses an isolated browser context with valid access and entitlement credentials
    And Admin B and Admin C open Verify for the same inactive Tile; Admin B verifies first
    When Admin C selects Verified
    Then the UI reports that the record is already active
    And reloading still shows the record active
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Checker mode against an already active record enters the maker branch in the current controller. Intended conflict handling is unknown.
### Group: Admin URL security

<a id="group-admin-url-security"></a>

#### BFF-ADM-092

**Proposed unsafe Import Map Path rejection for javascript**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Import Map form uses Module Name=container-a and Path=javascript:alert(1)

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-092 @PROPOSED
Feature: Admin URL security
  Scenario: Proposed unsafe Import Map Path rejection for javascript
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Import Map form uses Module Name=container-a and Path=javascript:alert(1)
    When Admin A selects Create
    Then the form remains open
    And a Path validation error is visible
    And no active import map can load the supplied path
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source checks blanks and spaces, not schemes or allowed hosts. Approved URL policy is unavailable.

#### BFF-ADM-093

**Proposed unsafe Import Map Path rejection for data**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Import Map form uses Module Name=container-a and Path=data:text/javascript,alert(1)

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-093 @PROPOSED
Feature: Admin URL security
  Scenario: Proposed unsafe Import Map Path rejection for data
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Import Map form uses Module Name=container-a and Path=data:text/javascript,alert(1)
    When Admin A selects Create
    Then the form remains open
    And a Path validation error is visible
    And no active import map can load the supplied path
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source checks blanks and spaces, not schemes or allowed hosts. Approved URL policy is unavailable.

#### BFF-ADM-094

**Proposed unsafe Import Map Path rejection for https**

Version: 1. Level: UI E2E design. Priority: P0. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Import Map form uses Module Name=container-a and Path=https://unapproved.example/module.js

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-094 @PROPOSED
Feature: Admin URL security
  Scenario: Proposed unsafe Import Map Path rejection for https
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Import Map form uses Module Name=container-a and Path=https://unapproved.example/module.js
    When Admin A selects Create
    Then the form remains open
    And a Path validation error is visible
    And no active import map can load the supplied path
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source checks blanks and spaces, not schemes or allowed hosts. Approved URL policy is unavailable.

#### BFF-ADM-095

**Protect an existing import-map namespace from a reserved key collision**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `IMPLEMENTATION`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Import Map form uses Module Name=react and a valid fixture URL while an active react record exists

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-029:50](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-102:6](<../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-095 @IMPLEMENTATION
Feature: Admin URL security
  Scenario: Protect an existing import-map namespace from a reserved key collision
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Import Map form uses Module Name=react and a valid fixture URL while an active react record exists
    When Admin A selects Create
    Then Record not created. is visible
    And the existing react mapping remains unchanged
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: Source-backed characterization only. A controlled database follows the inspected migrations; deployed schema and business approval are unproved.

#### BFF-ADM-096

**Prevent duplicate import-map prefix in the module name**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: the new Import Map form uses Module Name=@fm/container-a and a valid fixture URL

Behavior basis: [UI-SRC-017:107](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107>); [UI-SRC-042:61](<../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-096 @PROPOSED
Feature: Admin URL security
  Scenario: Prevent duplicate import-map prefix in the module name
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And the new Import Map form uses Module Name=@fm/container-a and a valid fixture URL
    When Admin A selects Create
    Then the form displays a namespace validation error
    And the grid does not add a mapping named @fm/@fm/container-a
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The active mapping builder prefixes non-reserved keys with @fm/. Input namespace policy is unresolved.
### Group: Admin audit fidelity

<a id="group-admin-audit-fidelity"></a>

#### BFF-ADM-097

**Preserve distinct theme images in Tile audit**

Version: 1. Level: UI E2E design. Priority: P1. Basis: `PROPOSED`.

Actor: Admin A, user admin-a with the FMO_ADMIN owner role.

Setup: Tile 301 has Image Light Theme=light-a.png and Image Dark Theme=dark-a.png; a maker update succeeds

Behavior basis: [UI-SRC-016:215](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L215>); [UI-SRC-047:64](<../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64>); [UI-SRC-084:8](<../../repos/ui/mfe-base/src/components/Table/ModalAction.tsx#L8>)

```gherkin
@BFF-ADM-097 @PROPOSED
Feature: Admin audit fidelity
  Scenario: Preserve distinct theme images in Tile audit
    Given Admin A, user admin-a with the FMO_ADMIN owner role uses an isolated browser context with valid access and entitlement credentials
    And Tile 301 has Image Light Theme=light-a.png and Image Dark Theme=dark-a.png; a maker update succeeds
    When Admin A opens Audit for Tile 301
    Then the audit Light Theme field displays light-a.png
    And the audit Dark Theme field displays dark-a.png
```

Assertion mapping: Every `Then` maps to [UI-COVERAGE-AC-001](intake.md#ui-coverage-ac-001).

Source mapping: [UI-COVERAGE-AC-002](intake.md#ui-coverage-ac-002). Inspected assertion links: Unavailable for this new case.

Identity mapping: [UI-COVERAGE-AC-003](intake.md#ui-coverage-ac-003).

Execution: `NOT_RUN`. Actual result: null. Retained execution: null.

Cleanup: Close the browser context. Restore the controlled database and admin credentials. Remove only records created by this case.

Limits: The source assigns imageLightTheme into the audit dark field and imageDarkTheme into the light field. This is a source-predicted discrepancy, not a reproduction.

## Execution binding

```yaml
execution_status: NOT_RUN
repository_revisions:
  mfe-base: 6e34da31961eb6bce4ef6c3daea83a2f7bd48e85
  single-ui-bff: 834b4155232222347220e47139a502ee43a9cbdf
  workbench: 8dd076eac24c1b18b2f44245b3220ebcaf8537e3
new_executable_assertion_locations: []
environment_identity: null
execution_id: null
actual_results: null
retained_execution_refs: []
```

Historical tests and executions retain their original case definitions and revision bindings.
The [source inspections](evidence/index.md) describe those limits.
They do not establish a result for any new case.
Save each future completed case immediately under this task's evidence directory.
Record source hashes, fixture identity, assertions, actual observations, and artifact hashes.

## Facts, inferences, and unresolved questions

Fact: The catalog derives from inspected local sources and retained domain documents.
Inference: The selected partitions expose consequential UI failure modes.
Unknown: Approved policy, deployment parity, supported browsers, and current performance budgets require owner confirmation.
Unknown: Conditional tenant, OpenFin, and cache fixtures are not bound to an execution environment.
Counts identify case definitions. They do not measure distinct business rules or guarantee independent coverage gain.
[AUTH-036](#auth-036) characterizes source behavior. [KNOW-007](#know-007) records a related draft policy with conflicting authority.
No finite catalog proves coverage of every possible combination.
The defined cases cover distinct state, boundary, failure, recovery, and interaction partitions.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Knowledge authority and conflicts](evidence/knowledge-inspection.md#open-rule-decisions) | Affected business acceptance remains blocked. | unknown | Confirm applicable policies and versioned integration contracts. |
| [Crosscut proposals](evidence/crosscut-inspection.md#authority-and-execution-limits) | Quality assertions require applicable product targets. | unknown | Review browser, accessibility, and viewport expectations. |
| [Execution binding](#execution-binding) | No business behavior is verified by this catalog. | unknown | Bind approved cases to executable UI assertions and retain results. |

## Sources

| Source ID | Locator | Exact revision | Authority and limits |
| --- | --- | --- | --- |
| UI-SRC-USER | User chat dated 2026-10-22 | 2026-10-22 | Authorizes local case design. No business approval or runtime result. |
| UI-SRC-MFE | [MFE source inspection](evidence/ui-source-inspection.md) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | Implementation characterization. |
| UI-SRC-BFF | [Session source inspection](evidence/session-source-inspection.md) and [admin boundaries](evidence/admin-boundary-inspection.md) | `834b4155232222347220e47139a502ee43a9cbdf` | Implementation characterization. |
| UI-SRC-KNOWLEDGE | [Knowledge source inspection](evidence/knowledge-inspection.md) | `8dd076eac24c1b18b2f44245b3220ebcaf8537e3` | Draft intent and retained snapshot authority limits. |
| Per-file source IDs | [Source manifest](evidence/source-manifest.json) | Exact revisions and SHA-256 values per source | Links identify evidence. They do not establish approval or execution. |
