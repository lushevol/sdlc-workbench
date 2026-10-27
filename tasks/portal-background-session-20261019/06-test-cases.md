---
artifact_kind: test-case
id: TEST-session-canonical-20261021
version: 15
status: draft
owner: unknown
source_refs:
  - SRC-ut-release-principle-20261027
  - SRC-mfe-base-delivery-confidence-20261026
  - SRC-session-sequential-minor-fixes-20261025
  - SRC-session-active-cutoff-fix-request-20261024
  - SRC-session-robot-modules-20261021
  - SRC-session-canonical-inputs-20261021
  - SRC-session-minor-inventory-20261020
  - SRC-session-branch-refresh-20261021
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
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

# Session issue: canonical test cases

> **Critical conclusions: Action required**
>
> **Production remains blocked by missing release evidence. Both introduced regressions are corrected locally.**
> Action: complete the [release closure inventory](10-delivery-confidence-20261026.md#detailed-go-live-closure-inventory).
> Consequence: passing local checks cannot establish production suitability. Owner: unknown release owner.
> Evidence: [current unit execution](evidence/four-checks-20261027/coverage/test-only-final-2/execution.json) and [current assessment](10-delivery-confidence-20261026.md).
>
> Existing activity failures retain their recorded backlog disposition.
> The [latest triage](10-release-confidence-triage-20261026.md) supersedes earlier release scope statements below.
> The [delivery stage](10-delivery-confidence-20261026.md) records the new verification and independent reviews.
> Source: [current high-priority request](evidence/delivery-confidence-20261026/user-input.md#exact-user-input).
>
> The [unit-test request](evidence/delivery-confidence-20261026/ut-release-principle-user-input-20261027.md#exact-user-input) prefers unchanged application code.
> Genuine failures required minimal runtime correction. The pre-remediation candidate assertions remain unchanged.
> The [renewed review](evidence/renewed-review-20261027/codex/review.md#test-assertion-history) identifies changed main-baseline assertions.
> [DEL-21](#del-21), [DEL-22](#del-22), [DEL-23](#del-23), and [DEL-24](#del-24) protect the correction.
> The [current stage](10-delivery-confidence-20261026.md#final-four-check-verification-27-october-2026) records its source and execution state.

Current candidate: `e0030f5cf920b715f5831faf7df86cb9789b6d0f`. Its runtime matches `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303`.
The [current browser reconciliation](evidence/four-checks-20261027/e2e/reconciliation.json) records final-runtime results and pending cases.
Historical results below retain their original source identities.
Prior original business cases: **13 passed, 6 failed, 0 blocked**.
[E2E-12](#e2e-12) is diagnostic; [E2E-21](#e2e-21) and [E2E-22](#e2e-22) are observations.
These three cases remain outside the nineteen business-case totals.
Seven failures changed to passed: [E2E-04](#e2e-04), [E2E-05](#e2e-05), [E2E-07](#e2e-07), [E2E-09](#e2e-09), [E2E-10](#e2e-10), [E2E-13](#e2e-13), and [E2E-17](#e2e-17).
The [historical comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) binds each result and its execution scope.

<details>
<summary>Historical conclusions before the sequential corrections</summary>

These conclusions describe earlier candidates. Current results above supersede their runtime status claims.
Historical issue 1 means the active-cutoff correction at `ae8213f`.
Current issue 1 means the session-ownership correction at `5a397ec`.
The UAT lifetime and configuration remain unverified release boundaries.

> **🚨 Critical conclusions: Action required**
>
> **Issue 1 has a committed source correction. E2E-06 changed from FAILED to PASSED. E2E-07 remains FAILED after a valid natural run.**
> Action: correct prompt visibility during pending renewal, then rerun E2E-07.
> Consequence: natural background recovery remains unmet. Existing release blockers remain.
> Owner: unknown application owner; Codex for verification.
> Evidence: [current comparison](08-active-cutoff-fix-20261024.md), [E2E-07 result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json), and [committed source](evidence/active-cutoff-fix-20261024/commit-binding.json).
>
> **The UAT photograph shows almost eight hours before access expiry.**
> Action: verify the effective BFF lifetime and its configuration source.
> Consequence: thirty minutes cannot reach the photographed access deadline.
> Owner: unknown authentication owner. Evidence: [photograph analysis](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json).
> UAT refresh expiry and clock agreement remain unverified.
>
> **The historical minor candidate has two P2 regressions that can end usable sessions.**
> Action: assess [active-session cutoff](#review-f01), [stale response before sign-in](#review-f03a), and [stale response after sign-in](#review-f03b).
> Consequence: active access can end, or recovery can clear a fresh session.
> Owner: unknown application owner; user for scope decisions. Evidence: each linked case retains separate old and new results.
> Controlled checks do not establish production failure frequency.
>
> **⚠️ Delayed background recovery remains an inherited failure.**
> Action: retain the defect until the [delayed-recovery assertions](#review-delayed-hide) pass.
> Consequence: usable late refresh credentials can leave Extend disabled and cause logout.
> Owner: unknown application owner. Evidence: [browser probe](#probe-delayed-refresh) and [paired controlled results](#review-delayed-scheduled).
> An expected-failure runner pass does not establish passing recovery.

</details>

**🧭 Choose the evidence you need:**

| Read this | Purpose | Execution boundary |
| --- | --- | --- |
| [Current review cases](#current-branch-review-cases) | Compare active cutoff, stale credentials, timer behavior, and delayed recovery. | Controlled checks at the selected old and new revisions. |
| [Browser case catalog](#catalog-navigation) | Read the 22 retained browser case definitions. | [Current comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json); historical results remain below each case. |
| [Supplemental browser probes](#supplemental-browser-probes) | Separate delayed delivery from immediate natural recovery. | Two distinct investigations with separate controls. |
| [Robot and JavaScript source](#current-robot-and-javascript-source) | Find the executable module for one browser case. | Modularized suite business execution remains **NOT_RUN**. |
| [Real-world session cases](#real-world-session-cases) | Check configured lifetimes, actual Blotter inactivity, and remote execution boundaries. | Hidden measurement **FAILED** its fixed-expiry assertion. Schedule, mismatch detection, and shortened-expiry controls passed. |
| [Current correction report](08-minor-fixes-rerun-20261025.md) | Read both fixes and remaining failures. | Source and local execution evidence do not establish release approval. |

## Objective and traceability

Use this file as the single current source for readable test steps and assertions.
Definition version 1 applies to every case below. Stable case IDs remain independent of executable function names.
The [execution report](test-execution-report.md) summarizes results and links these definitions.
The [prior review](code-review-minor-20261021.md) explains earlier change impact and network sequences.
Existing outcomes retain their original implementation and test bindings. New Blotter observation cases have separate execution bindings.

The requirement remains [candidate version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).
No acceptance waiver or policy change is recorded. The [frozen aliases](#frozen-regression-aliases) map earlier proposed scopes.
The [input hashes](evidence/canonical-gherkin-20261021/inputs.json) identify the requirement, intake, reports, and active checkout.

The [issue 1 correction request](evidence/active-cutoff-fix-20261024/user-request.txt) adds two controlled regression definitions.
See [replacement and later recovery](#review-f01-recovery) and [manual renewal near refresh expiry](#review-f01-manual).
The original 22 browser definitions and their executable assertions remain unchanged for the comparison.
Their prior execution links preserve the historical baseline. Use the [current comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) for final-candidate outcomes.

| Case group | Test level | Implementation and assertion binding | Outcome source |
| --- | --- | --- | --- |
| E2E cases | Local browser and BFF integration | Runtime `6d4c37c839b99d14ea41fd936da1a36cda526b17`; test engine `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. | [22-case inventory](evidence/minor-branch-rerun-20261020/case-inventory.json) and [browser manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json). |
| Supplemental probes | Local browser and BFF investigation | Same runtime; each probe links its separate retained driver and source binding. | [Delayed delivery](#probe-delayed-refresh) and [immediate recovery](#probe-natural-immediate). |
| Current review cases | Controlled component, service, or static validation | Baseline `f025513f696476a9cc8162681410cbd21e029bcb`; candidate HEAD `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. Runtime remains `6d4c37c839b99d14ea41fd936da1a36cda526b17`. | [Fresh review reconciliation](evidence/code-review-refresh-20261021/summary.json). |

## Current Robot and JavaScript source

The [Robot suite](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot) keeps all 22 cases in one file.
Each case has one stable selection tag and a link to its canonical definition below.
The [entry point](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs) preserves the existing Browser keywords.
Each execution module owns one case. The three activity modules share [unchanged activity assertions](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/activity.cjs).

Current test-engine revision: `975af64c55303ee4a138968813ef4e85570f96d2`.
The [source binding](evidence/robot-case-modules-20261021/case-mapping.json) records all module hashes, case mappings, and the prior revision.
The [offline checks](evidence/robot-case-modules-20261021/offline-checks.json) preserve all 41 original functions, except the documented result-provenance adaptation.
The [installed Browser discovery](evidence/robot-case-modules-20261021/browser-discovery.json) confirms all 21 keyword interfaces.
**Modularized Robot suite execution: `NOT_RUN`.** Historical browser results below use their original source revisions.

The two supplemental probes and eight review cases retain their separate drivers. They are not additional Robot cases.
Definition version 1 remains unchanged. Catalog version 3 clarifies navigation, execution status, and local references.

| Case definition | Robot case | Current execution module |
| --- | --- | --- |
| [E2E-01](#e2e-01) | [E2E-01](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L16) | [e2e-01.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-01.cjs) |
| [E2E-02](#e2e-02) | [E2E-02](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L21) | [e2e-02.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-02.cjs) |
| [E2E-03](#e2e-03) | [E2E-03](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L26) | [e2e-03.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-03.cjs) |
| [E2E-04](#e2e-04) | [E2E-04](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L31) | [e2e-04.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-04.cjs) |
| [E2E-05](#e2e-05) | [E2E-05](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L37) | [e2e-05.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-05.cjs) |
| [E2E-06](#e2e-06) | [E2E-06](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L43) | [e2e-06.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-06.cjs) |
| [E2E-07](#e2e-07) | [E2E-07](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L49) | [e2e-07.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-07.cjs) |
| [E2E-08](#e2e-08) | [E2E-08](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L55) | [e2e-08.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-08.cjs) |
| [E2E-09](#e2e-09) | [E2E-09](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L60) | [e2e-09.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-09.cjs) |
| [E2E-10](#e2e-10) | [E2E-10](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L66) | [e2e-10.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-10.cjs) |
| [E2E-11](#e2e-11) | [E2E-11](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L72) | [e2e-11.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-11.cjs) |
| [E2E-12](#e2e-12) | [E2E-12](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L77) | [e2e-12.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-12.cjs) |
| [E2E-13](#e2e-13) | [E2E-13](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L82) | [e2e-13.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-13.cjs) |
| [E2E-14](#e2e-14) | [E2E-14](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L88) | [e2e-14.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-14.cjs) |
| [E2E-15](#e2e-15) | [E2E-15](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L94) | [e2e-15.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-15.cjs) |
| [E2E-16](#e2e-16) | [E2E-16](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L99) | [e2e-16.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-16.cjs) |
| [E2E-17](#e2e-17) | [E2E-17](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L104) | [e2e-17.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-17.cjs) |
| [E2E-18](#e2e-18) | [E2E-18](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L110) | [e2e-18.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-18.cjs) |
| [E2E-19](#e2e-19) | [E2E-19](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L115) | [e2e-19.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-19.cjs) |
| [E2E-20](#e2e-20) | [E2E-20](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L121) | [e2e-20.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-20.cjs) |
| [E2E-21](#e2e-21) | [E2E-21](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L127) | [e2e-21.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-21.cjs) |
| [E2E-22](#e2e-22) | [E2E-22](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L133) | [e2e-22.cjs](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-22.cjs) |

Select one case with `--include E2E-15`. The [execution guide](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#execution) gives the complete command.

## Preconditions and fixtures

### Browser terms and common setup

| Term or entity | Exact meaning |
| --- | --- |
| Portal user | The synthetic authenticated user in the isolated local portal/BFF fixture. No production identity is used. |
| Driver | The retained native Edge automation process. It sends the actions stated in each case. |
| Home | Visible element `[aria-label="workspaces"]` in the retained browser fixture. [Setup](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L45). |
| Access token A | The access credential present before the named action. Later letters identify returned credentials within that case. |
| Refresh token R | The separate refresh credential used by `POST /api/auth/v2/sso/relogin`. It cannot directly authorize protected access. |
| Stored access | The value of `localStorage.SET_TOKEN`. References to `SET_TOKEN` mean this exact browser storage key. |
| Stored refresh | The value of `localStorage.SET_REFRESH_TOKEN`, when present. Its absence does not prove memory cleanup or provider revocation. |
| Extension | `POST /api/auth/v2/sso/extend`, using current access. A successful local response supplies renewed access. |
| Acquisition | `POST /api/auth/v2/sso/refreshtoken`, obtaining refresh credentials. |
| Manual renewal | `POST /api/auth/v2/sso/relogin`, using refresh credentials after Extend activation. |
| Pending renewal | A tracked extension or relogin operation without a completed response. Each case names the controlled operation. |
| Timeout prompt | Visible `#timeout-dialog-title` in suite cases. The delayed probe separately uses `[role="dialog"]`. |
| Extend | Recovery button `[data-testid="Extend_Btn"]` in the browser fixture. Review cases use its accessible name in JSDOM. |
| Sign in | Visible button matching `button[data-testid$="_login"]` in the browser fixture. |
| Protected validation | Read-only portal authentication validation at `/api/auth/v2/sso/validate`. It does not establish downstream business authorization. |
| Protected request field | JSON field `singleUIAuthorization`, compared with the exact access stored before navigation. |
| Successful HTTP status | The Playwright `response.ok()` predicate: status 200 through 299, unless a case requires an exact status. |
| Usable credential | A credential accepted by the named local operation. A future expiry alone does not prove usability. |

Browser cases use real elapsed time. The fast fixture has 60-second access and 144-second refresh lifetimes.
Natural fixtures have 900-second access and 13,524-second refresh lifetimes.
These values are test data. They do not define production session policy.
Each wait starts at its preceding action unless the case names another origin.
The [environment report](test-execution-report.md#browser-environment-and-suite-completeness) records versions, visibility controls, substitutions, and omitted boundaries.

Each retained attempt uses an independent native Edge process and fresh context.
The [runner](evidence/minor-branch-rerun-20261020/run-expanded.py.snapshot) manages processes and durable results.
The [Robot suite](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L1) declares per-test setup and browser teardown.
The retained reruns invoke the linked JavaScript assertions through their own runner. They do not claim Robot command execution.
Synthetic provider adapters and toolkit stubs limit integration claims. Case-specific transport controls appear below.
Cleanup closes the case browser and releases held responses or transport overrides within that attempt.

## Procedure and assertions

### Catalog navigation

The original and extended browser cases share one definition sequence below.
Each case contains ordered scenario checkpoints within one execution. Later checkpoints retain the same browser, credentials, and controlled responses.
A checkpoint starts at its named action group. Its Given condition requires all preceding checkpoints and assertions in that case.
Do not restart setup between checkpoints. This notation preserves intermediate assertions in execution order.
Each section links its criterion, executable assertion, and retained result separately.
The [current review cases](#current-branch-review-cases) preserve comparisons with the selected baseline.
The [frozen alias table](#frozen-regression-aliases) links earlier TC identifiers without rewriting historical intake.

### E2E-01

**Continuous mouse activity renews access**

Definition version: `1`. Criterion: [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L137).

Use the fast fixture: 60-second access and 144-second refresh lifetimes. These values define test data, not production policy.

```gherkin
Feature: Renew access during trusted portal activity
  Scenario: Continuous mouse activity renews access
    Given the signed-in portal user has portal Home visible
    And setup activity has settled after 6 seconds and zero pending renewals
    And the installed access token A has at least 30 seconds before expiry
    And the driver records the existing renewal and trusted mousemove counts
    When the driver moves the native pointer to x=120+(index modulo 50), y=150+(index modulo 30)
    And the driver repeats that action for 15 seconds with requested 100-millisecond pauses
    Then trusted mousemove events number at least floor(emitted actions divided by 2)
    And at least one successful renewal response arrives before that 15-second interval ends
    And at least one accepted response access expiry exceeds token A's baseline expiry
    And the Timeout prompt is absent
  Scenario: E2E-01 checkpoint 2
    Given the same E2E-01 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When all activity renewals settle within 10 seconds
    Then SET_TOKEN contains an access token
  Scenario: E2E-01 checkpoint 3
    Given the same E2E-01 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads the current SET_TOKEN and navigates to portal root /
    Then the validation response arrives within 30 seconds with a successful HTTP status
    And its request field singleUIAuthorization equals the current SET_TOKEN read before navigation
    And the validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [activity assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231), [trusted input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/result.json).
Prior execution stopped at the interval-renewal assertion. Later expiry, prompt, and protected-validation assertions were not reached. Driver overhead affects input cadence.

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-mouse-20261025T093811/artifacts/activity-mouse-1792921100995/result.json). Scope: `NATIVE_BROWSER`.

### E2E-02

**Continuous keyboard activity renews access**

Definition version: `1`. Criterion: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L144).

Use the fast fixture: 60-second access and 144-second refresh lifetimes. These values define test data, not production policy. The input selector is `input[aria-label="Workspace Name"]`.

```gherkin
Feature: Renew access during trusted portal activity
  Scenario: Continuous keyboard activity renews access
    Given the signed-in portal user has portal Home visible
    And setup activity has settled after 6 seconds and zero pending renewals
    And the installed access token A has at least 30 seconds before expiry
    And the driver records the existing renewal and trusted keydown counts
    When the driver alternates ArrowRight and ArrowLeft in the portal Workspace Name input
    And the driver repeats that action for 15 seconds with requested 100-millisecond pauses
    Then trusted keydown events number at least floor(emitted actions divided by 2)
    And at least one successful renewal response arrives before that 15-second interval ends
    And at least one accepted response access expiry exceeds token A's baseline expiry
    And the Timeout prompt is absent
  Scenario: E2E-02 checkpoint 2
    Given the same E2E-02 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When all activity renewals settle within 10 seconds
    Then SET_TOKEN contains an access token
  Scenario: E2E-02 checkpoint 3
    Given the same E2E-02 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads the current SET_TOKEN and navigates to portal root /
    Then the validation response arrives within 30 seconds with a successful HTTP status
    And its request field singleUIAuthorization equals the current SET_TOKEN read before navigation
    And the validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [activity assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231), [trusted input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/result.json).
Prior execution stopped at the interval-renewal assertion. Later expiry, prompt, and protected-validation assertions were not reached. Cross-origin frame keyboard propagation remains untested.

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-keyboard-20261025T093844/artifacts/activity-keyboard-1792921132198/result.json). Scope: `NATIVE_BROWSER`.

### E2E-03

**Continuous scroll activity renews access**

Definition version: `1`. Criterion: [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L151).

Use the fast fixture: 60-second access and 144-second refresh lifetimes. These values define test data, not production policy. The panel selector is `[role=tabpanel]:not([hidden]) .tabmain`.

```gherkin
Feature: Renew access during trusted portal activity
  Scenario: Continuous scroll activity renews access
    Given the signed-in portal user has portal Home visible
    And setup activity has settled after 6 seconds and zero pending renewals
    And the installed access token A has at least 30 seconds before expiry
    And the driver records the existing renewal and trusted scroll counts
    When the driver hovers the visible workspace tab panel and alternates native vertical wheel movements of +100 and -100 pixels
    And the driver repeats that action for 15 seconds with requested 100-millisecond pauses
    Then trusted scroll events number at least floor(emitted actions divided by 2)
    And at least one successful renewal response arrives before that 15-second interval ends
    And at least one accepted response access expiry exceeds token A's baseline expiry
    And the Timeout prompt is absent
  Scenario: E2E-03 checkpoint 2
    Given the same E2E-03 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When all activity renewals settle within 10 seconds
    Then SET_TOKEN contains an access token
  Scenario: E2E-03 checkpoint 3
    Given the same E2E-03 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads the current SET_TOKEN and navigates to portal root /
    Then the validation response arrives within 30 seconds with a successful HTTP status
    And its request field singleUIAuthorization equals the current SET_TOKEN read before navigation
    And the validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [activity assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231), [trusted input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/result.json).
Prior execution stopped at the interval-renewal assertion. Later expiry, prompt, and protected-validation assertions were not reached. This case covers the configured portal panel only.

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-scroll-20261025T093917/artifacts/activity-scroll-1792921163908/result.json). Scope: `NATIVE_BROWSER`.

### E2E-04

**Pending Extend closes the Timeout prompt only after successful renewal**

Definition version: `1`. Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173), and [TC-01](intake.md#L263).

Use the fast fixture. Hold the actual relogin request before dispatch for 1,500 milliseconds. Forward it without token fabrication.

```gherkin
Feature: Complete refresh-based renewal before closing the Timeout prompt
  Scenario: Hold Extend pending and then complete actual renewal
    Given the portal user has allowed access token A to expire
    And the Timeout prompt and Extend button are visible
    And refresh token R came from the actual authentication service
    And refresh token R has more than 30 seconds before expiry
    And the prompt closure counter equals zero
    When the driver holds POST /api/auth/v2/sso/relogin before service dispatch
    And the portal user clicks Extend
    Then the held relogin request exists within 10 seconds
  Scenario: E2E-04 checkpoint 2
    Given the same E2E-04 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver holds that request for 1,500 milliseconds
    Then the Timeout prompt remains visible
    And the prompt closure counter remains zero
  Scenario: E2E-04 checkpoint 3
    Given the same E2E-04 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver forwards the held request to the actual authentication service
    Then the service responds successfully within 30 seconds
    And its single-ui-authorization response header contains an unexpired access token B
  Scenario: E2E-04 checkpoint 4
    Given the same E2E-04 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver delivers that actual response to the portal
    Then the Timeout prompt becomes hidden within 10 seconds
    And the prompt closure counter equals one
    And SET_TOKEN contains exactly token B
  Scenario: E2E-04 checkpoint 5
    Given the same E2E-04 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And its request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [idle preconditions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267), [held renewal assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/result.json).
The prior run closed the prompt while the request remained held. Service forwarding and later assertions were not reached.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-pending-20261025T092741/artifacts/pending-renewal-1792920465568/result.json). Scope: `NATIVE_BROWSER`.

### E2E-05

**A transport failure leaves Extend available for actual-service retry**

Definition version: `1`. Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L180) and [TC-02](intake.md#L264).

Use the fast fixture. Abort only the first relogin request. Hold the retry for 1,500 milliseconds before actual service dispatch.

```gherkin
Feature: Retry refresh-based renewal after transport failure
  Scenario: Reject the first Extend request and complete a retry
    Given expired access token A has opened the Timeout prompt
    And refresh token R is service-issued with more than 30 seconds before expiry
    And Extend is visible and the prompt closure counter equals zero
    When the driver aborts only the first POST /api/auth/v2/sso/relogin with transport error failed
    And the portal user clicks Extend
    Then that controlled abort occurs within 10 seconds
    And Extend becomes enabled within 10 seconds
    And the Timeout prompt remains visible
    And the prompt closure counter remains zero
  Scenario: E2E-05 checkpoint 2
    Given the same E2E-05 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the portal user clicks Extend again
    And the driver holds the retry request before dispatch for 1,500 milliseconds
    Then the retry request exists within 10 seconds
    And the Timeout prompt remains visible with zero closures
  Scenario: E2E-05 checkpoint 3
    Given the same E2E-05 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver forwards the retry to the actual authentication service
    Then the service responds successfully within 30 seconds
    And single-ui-authorization contains unexpired access token B
  Scenario: E2E-05 checkpoint 4
    Given the same E2E-05 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver delivers that actual response
    Then the Timeout prompt becomes hidden within 10 seconds
    And exactly one prompt closure is recorded
    And SET_TOKEN contains exactly token B
  Scenario: E2E-05 checkpoint 5
    Given the same E2E-05 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [first rejection assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L320), [idle preconditions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267), [retry completion](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/result.json).
The prior run closed the prompt after failure. Retry assertions were not reached. A transport abort does not establish provider rejection.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-retry-20261025T093024/artifacts/rejected-renewal-retry-1792920631883/result.json). Scope: `NATIVE_BROWSER`.

### E2E-06

**Continued activity crosses the initial refresh expiry in real time**

Definition version: `1`. Partial criterion probe: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158). The four-hour controlled-clock assertion remains separate.

Use the fast fixture and real wall time. Mouse activity occurs every requested 10 seconds through initial refresh expiry plus 30 seconds.

```gherkin
Feature: Continue the session beyond the initial refresh deadline
  Scenario: Cross the initial refresh expiry without sign-in or navigation
    Given the portal user has portal Home visible with valid access token A
    When a covering page hides portal Home
    Then the actual service issues refresh token R within 10 seconds
  Scenario: E2E-06 checkpoint 2
    Given the same E2E-06 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver restores portal Home and closes the covering page
    And the driver records token R's hash and original expiry
    Then expiry plus 30 seconds lies within the configured 18,000-second execution limit
  Scenario: E2E-06 checkpoint 3
    Given the same E2E-06 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver emits native mouse movement every requested 10 seconds until that boundary
    Then each activity check finds the Timeout prompt absent
    And each activity check finds portal Home visible and Sign In absent
    And the actual service completes at least one renewal during that interval
    And the latest returned access expiry exceeds the original refresh expiry
    And the latest refresh token hash differs from token R's original hash
    And the replacement refresh expiry exceeds token R's original expiry
    And zero additional login response records occur during the activity interval
    And zero additional main-frame navigations occur during the activity interval
    And zero prompt_opened lifecycle events occur during the activity interval
  Scenario: E2E-06 checkpoint 4
    Given the same E2E-06 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [boundary and continuity assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L601), [mouse input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json).
The prior run lost portal Home. Later boundary assertions were not reached. The script does not implement four controlled hours. It counts login responses, not attempted login requests.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-cross-20261025T113902/artifacts/activity-cross-refresh-expiry-1792928349090/result.json). Scope: `NATIVE_BROWSER`.

### E2E-07

**A naturally hidden session supports held Extend after thirty minutes**

Definition version: `1`. Criteria: [TC-03](intake.md#L265), [TC-06](intake.md#L268), [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166), and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173).

Use natural-fixture credentials: 900-second access and 13,524-second refresh lifetimes. Both sessions use identical revisions and settings.

```gherkin
Feature: Recover a naturally hidden portal session with a visible idle control
  Scenario: Compare hidden recovery and visible expiry after 1,800 seconds
    Given the subject portal user is signed in with valid access token A
    And a separate browser context opens a signed-in control session
    When the driver puts the control page in front and hides the subject
    Then the hidden subject obtains actual refresh token R within 10 seconds
  Scenario: E2E-07 checkpoint 2
    Given the same E2E-07 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When 1,800 real seconds pass without page evaluation or activity from the driver
    Then the driver records elapsed wall time and both session lifecycle records
    And the control Timeout prompt is visible
    And the control records no hidden visibilitychange event
  Scenario: E2E-07 checkpoint 3
    Given the same E2E-07 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver brings the hidden subject to the front
    Then the driver records whether the subject has an observed freeze event
    And subject refresh token R has more than 30 seconds before expiry
    And the subject Timeout prompt becomes visible within 10 seconds
  Scenario: E2E-07 checkpoint 4
    Given the same E2E-07 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver resets the subject prompt closure counter to zero
    And the user clicks Extend while the driver holds relogin before dispatch
    Then the relogin request exists within 10 seconds
  Scenario: E2E-07 checkpoint 5
    Given the same E2E-07 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver holds that request for 1,500 milliseconds
    Then the subject Timeout prompt remains visible with zero closures
  Scenario: E2E-07 checkpoint 6
    Given the same E2E-07 execution has completed checkpoints 1 through 5 with every prior assertion satisfied
    When the driver forwards the request to the actual authentication service
    Then the service responds successfully within 30 seconds
    And single-ui-authorization contains unexpired access token B
  Scenario: E2E-07 checkpoint 7
    Given the same E2E-07 execution has completed checkpoints 1 through 6 with every prior assertion satisfied
    When the driver delivers that actual response
    Then the subject Timeout prompt becomes hidden within 10 seconds
    And exactly one prompt closure is recorded
    And SET_TOKEN contains exactly token B
  Scenario: E2E-07 checkpoint 8
    Given the same E2E-07 execution has completed checkpoints 1 through 7 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [paired natural recovery](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L643), [held renewal](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/result.json).
The prior run observed freeze and 1,800,011 hidden milliseconds. It failed before held relogin dispatch. No-freeze runs cannot prove frozen-tab recovery. The script records freeze; it does not require freeze for a passing hidden-case verdict. This scenario does not cover natural return without usable refresh. The separate [immediate-response supplement](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/supplemental/result.json) passed with narrower completion-order limits.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-natural-20261025T114548/artifacts/natural-background-paired-control-1792928754518/result.json). Scope: `NATIVE_BROWSER`. Observed freeze: `true`. Native timestamps establish at least `1,800,694` hidden milliseconds.
The earlier sleep sample remains `1,799,958` milliseconds. [Timing analysis](evidence/minor-fixes-20261025/setup/natural-timing-analysis.json) retains this distinction.
The measurement uses wall-clock timestamps. No monotonic-duration receipt was retained.

### E2E-08

**Repeated mouse activity shares one pending extension request**

Definition version: `1`. Scope: supporting boundary. No separate approved acceptance criterion exists.

Use the fast fixture. Hold actual activity extension before dispatch while native mouse activity continues for 12 seconds.

```gherkin
Feature: Share a pending activity extension for the same access token
  Scenario: Hold one extension during repeated native mouse movement
    Given portal Home is visible after 6 seconds and zero pending setup renewals
    And access token A has more than 30 seconds before expiry
    When the driver holds POST /api/auth/v2/sso/extend before dispatch
    And the driver moves the native pointer repeatedly for 12 seconds with requested 100-millisecond pauses
    Then exactly one extension request is held
    And zero failed extension requests are recorded after the activity interval starts
  Scenario: E2E-08 checkpoint 2
    Given the same E2E-08 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver forwards that held request to the actual authentication service
    Then the actual service responds successfully within 30 seconds
    And its single-ui-authorization header contains access token B
  Scenario: E2E-08 checkpoint 3
    Given the same E2E-08 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver delivers that actual response
    Then SET_TOKEN equals token B within 10 seconds
  Scenario: E2E-08 checkpoint 4
    Given the same E2E-08 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver removes the hold and waits 6 seconds
    And pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [single pending request assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L706), [setup](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677), [mouse input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/result.json).
The prior run held zero extension requests. It did not demonstrate duplicate requests or cancellations. Later service-completion assertions were not reached.

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-single-20261025T094856/artifacts/slow-activity-single-flight-1792921749121/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.

### E2E-09

**Rapid native Extend activations share one renewal**

Definition version: `1`. Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166) and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173).

Use the fast fixture. Hold relogin before dispatch. Attempt the second activation at the rendered Extend button center.

```gherkin
Feature: Prevent duplicate refresh-based renewal from rapid Extend activation
  Scenario: Attempt two pointer activations while one renewal is pending
    Given expired access token A has opened the Timeout prompt
    And actual refresh token R has more than 30 seconds before expiry
    And Extend is visible and the prompt closure counter equals zero
    When the driver holds POST /api/auth/v2/sso/relogin before dispatch
    And the portal user clicks Extend
    Then exactly one relogin request is held within 10 seconds
    And Extend remains rendered with a measurable bounding box
  Scenario: E2E-09 checkpoint 2
    Given the same E2E-09 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver clicks the center of that box with a native pointer event
    And the driver waits 500 milliseconds
    Then exactly one relogin request remains held
    And Extend is disabled
    And the Timeout prompt remains visible
    And the prompt closure counter remains zero
  Scenario: E2E-09 checkpoint 3
    Given the same E2E-09 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver forwards the shared request to the actual authentication service
    Then the service responds successfully within 30 seconds
    And its single-ui-authorization header contains unexpired access token B
  Scenario: E2E-09 checkpoint 4
    Given the same E2E-09 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver delivers that actual response
    Then the Timeout prompt becomes hidden within 10 seconds
    And exactly one prompt closure is recorded
    And SET_TOKEN equals exactly token B
  Scenario: E2E-09 checkpoint 5
    Given the same E2E-09 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [rapid pointer and shared completion assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L337), [idle preconditions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/result.json).
The prior run timed out obtaining the Extend bounding box. The second activation and duplicate-request assertions were not reached.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-rapid-20261025T093141/artifacts/rapid-extend-single-flight-1792920708096/result.json). Scope: `NATIVE_BROWSER`.

### E2E-10

**Keyboard Enter activates Extend with completion-aware prompt closure**

Definition version: `1`. Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166) and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173).

Use the fast fixture. Focus Extend explicitly. Hold actual relogin for 1,500 milliseconds before service dispatch.

```gherkin
Feature: Renew through the focused Extend button with Enter
  Scenario: Activate Extend with the keyboard and wait for actual completion
    Given expired access token A has opened the Timeout prompt
    And actual refresh token R has more than 30 seconds before expiry
    And Extend is visible and the prompt closure counter equals zero
    When the driver holds POST /api/auth/v2/sso/relogin before dispatch
    And the driver focuses Extend and presses native keyboard Enter
    Then the held relogin request exists within 10 seconds
  Scenario: E2E-10 checkpoint 2
    Given the same E2E-10 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver holds that request for 1,500 milliseconds
    Then the Timeout prompt remains visible
    And the prompt closure counter remains zero
  Scenario: E2E-10 checkpoint 3
    Given the same E2E-10 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver forwards that request to the actual authentication service
    Then the service responds successfully within 30 seconds
    And its single-ui-authorization header contains unexpired access token B
  Scenario: E2E-10 checkpoint 4
    Given the same E2E-10 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the driver delivers that actual response
    Then the Timeout prompt becomes hidden within 10 seconds
    And exactly one prompt closure is recorded
    And SET_TOKEN contains exactly token B
  Scenario: E2E-10 checkpoint 5
    Given the same E2E-10 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [keyboard activation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L378), [idle preconditions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267), [held completion assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [FAILED](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/result.json).
The prior run closed the prompt during the hold. Actual service completion and later assertions were not reached.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-keyboardExtend-20261025T093257/artifacts/keyboard-extend-activation-1792920784140/result.json). Scope: `NATIVE_BROWSER`.

### E2E-11

**Later mouse activity retries an extension after transport failure**

Definition version: `1`. Scope: supporting boundary. No separate approved acceptance criterion exists.

Use the fast fixture. Abort only the first activity extension. A later native mouse action uses the actual service.

```gherkin
Feature: Retry activity extension after a controlled transport failure
  Scenario: Fail one extension and renew on the next mouse action
    Given portal Home is visible after 6 seconds and zero pending setup renewals
    And access token A has more than 30 seconds before expiry
    When the driver aborts only the first POST /api/auth/v2/sso/extend with transport error failed
    And the driver emits one native mouse movement
    Then the controlled abort occurs within 15 seconds
    And an extension failure is recorded within 10 seconds
    And the Timeout prompt remains absent while access is valid
  Scenario: E2E-11 checkpoint 2
    Given the same E2E-11 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver removes the abort route and emits another native mouse movement
    Then at least one actual successful renewal arrives within 15 seconds
    And SET_TOKEN contains an access token
  Scenario: E2E-11 checkpoint 3
    Given the same E2E-11 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver waits 6 seconds and pending renewals settle within 10 seconds
    And the driver reads current SET_TOKEN and navigates to portal root /
    Then validation arrives within 30 seconds with a successful HTTP status
    And request field singleUIAuthorization equals that current SET_TOKEN
    And validation response JSON field result equals true
    And portal Home becomes visible within 10 seconds
```

Assertion implementation: [activity retry assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L386), [setup](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677), [native mouse input](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219), and [protected validation](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Prior retained execution: [PASSED](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/artifacts/result.json).
The controlled transport-abort and later actual-service retry assertions passed. Provider rejection remains outside this fixture. The script checks token presence after retry; it does not assert exact retry-header installation.

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-activityRetry-20261025T094929/artifacts/activity-renewal-retry-1792921778226/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.

### E2E-12

**Reject a negative extension body with an actual successful authorization header.**

Scope: Supporting diagnostic boundary. No approved criterion defines this contradictory response combination.
The deployed service contract for `result=false` with usable authorization remains unconfirmed.

Setup and controls: Use the fast fixture with access A valid for more than 30 seconds.
Wait six seconds, then allow ten seconds for setup renewal requests to finish.
Intercept one actual extension response and preserve its status and authorization header.
Replace only its JSON body with `{"result": false}`.

```gherkin
Feature: Diagnostic handling of a contradictory activity extension response
  Scenario: Preserve access after a negative body, then allow an actual successful retry
    Given the portal user has valid access A with more than 30 seconds remaining
    And Home is visible and setup renewal requests have finished
    And the next activity extension response keeps its actual successful status and authorization header B
    But the test transport replaces that response body with {"result": false}
    When the portal user moves the pointer once inside Home
    Then the browser receives the extension response within 15 seconds with body.result equal to false
    And that response has a successful HTTP status and actual authorization header B
  Scenario: E2E-12 checkpoint 2
    Given the same E2E-12 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When that request finishes within 10 seconds and the test waits one additional second
    Then stored access remains exactly A
    And the Timeout prompt is hidden
  Scenario: E2E-12 checkpoint 3
    Given the same E2E-12 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test removes the body override
    And the portal user moves the pointer again inside Home
    Then an actual extension response arrives within 15 seconds with successful HTTP status and body.result equal to true
    And its authorization header C has a future expiry
    And stored access becomes exactly C within 10 seconds
    And C differs from A
  Scenario: E2E-12 checkpoint 4
    Given the same E2E-12 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test waits six seconds and waits up to 10 seconds for renewal requests to finish
    And the portal user opens the protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status and body.result equal to true
    And its request carries the exact access stored immediately before that operation
    And Home is visible within 10 seconds
```

Prior retained execution: `DIAGNOSTIC_FAILED`. The controlled negative body installed its returned authorization header.
The successful retry and protected validation assertions were not reached.
This result does not establish a deployed production contract violation.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L416); assertions [419](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L419); [426](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L426); [435](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L435); [439](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L439); [440](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L440); [445](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L445); [446](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L446); [448](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L448); [451](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L451); [452](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L452).
Helpers: [helper at 187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187); [helper at 219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219); [helper at 677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/result.json).

Current candidate `c42e760`: [DIAGNOSTIC_FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-inconsistent-20261025T095004/artifacts/inconsistent-activity-response-rejected-1792921809974/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.
This diagnostic remains outside business-case totals.

### E2E-13

**Ignore physical activity while the Timeout prompt is open.**

Scope: Supporting boundary. No standalone approved criterion defines prompt activity exclusion.

Setup and controls: Use the fast fixture and wait for the Timeout prompt after access expiry.
Confirm observed refresh R has more than 30 seconds remaining.
Reset the observed prompt closure count to zero.
Count and abort each activity extension request during the physical input sequence.
The modal can consume physical events before Home receives them.

```gherkin
Feature: Activity while the Timeout prompt is visible
  Scenario: Activity keeps the prompt open and explicit Extend completes renewal
    Given the Timeout prompt and Extend button are visible
    And actual refresh R has more than 30 seconds remaining
    And the observed prompt closure count is zero
    When the portal user performs six pointer movements, six Tab or Shift+Tab presses, and six wheel movements
    And the test requests 100-millisecond pauses between each combined input iteration
    And the test waits six seconds
    Then the activity extension request count is zero
    And the authentication request failure count has not increased
    And the Timeout prompt remains visible with zero closures
  Scenario: E2E-13 checkpoint 2
    Given the same E2E-13 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test removes the extension interceptor
    And the portal user clicks Extend
    And the test holds the relogin request before dispatch for 1500 milliseconds
    Then relogin starts within 10 seconds
    And the Timeout prompt remains visible with zero closures
  Scenario: E2E-13 checkpoint 3
    Given the same E2E-13 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test forwards the held relogin request to the actual service
    Then the service responds within 30 seconds with successful HTTP status and usable access B
  Scenario: E2E-13 checkpoint 4
    Given the same E2E-13 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test delivers that actual response to the browser
    Then the Timeout prompt is hidden within 10 seconds and has closed exactly once
    And stored access is exactly B
  Scenario: E2E-13 checkpoint 5
    Given the same E2E-13 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the test waits six seconds and waits up to 10 seconds for renewal requests to finish
    And the portal user opens the protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status and body.result equal to true
    And its request carries the exact access stored immediately before that operation
    And Home is visible within 10 seconds
```

Prior retained execution: `FAILED` because the prompt closed during the later held relogin request.
The preceding activity exclusion assertions completed. Later service forwarding and protected validation were not reached.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L461); assertions [480](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L480); [481](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L481); [482](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L482); [483](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L483).
Helpers: [helper at 267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267); [helper at 277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277); [helper at 187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-promptActivity-20261025T093414/artifacts/prompt-ignores-activity-1792920861525/result.json). Scope: `NATIVE_BROWSER`.

### E2E-14

**Clear stored credentials through Logout in the idle Timeout prompt.**

Scope: Supporting logout boundary. No standalone approved criterion defines these cleanup assertions.

Setup: Use the fast fixture and wait for the Timeout prompt after access expiry.
Confirm observed refresh R has more than 30 seconds remaining.
Record the number of relogin responses before Logout.

```gherkin
Feature: Logout from the idle Timeout prompt
  Scenario: Logout removes retained browser credentials without relogin
    Given the Timeout prompt and its Logout button are visible
    And actual refresh R has more than 30 seconds remaining
    When the portal user clicks Logout in that prompt
    Then the browser sends a logout request within 10 seconds
    And the Sign In button is visible within 15 seconds
  Scenario: E2E-14 checkpoint 2
    Given the same E2E-14 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test waits 500 milliseconds
    Then localStorage.SET_TOKEN is absent
    And sessionStorage.SET_TOKEN is absent
    And localStorage.SET_REFRESH_TOKEN is absent
    And sessionStorage.SET_REFRESH_TOKEN is absent
    And Home is hidden
    And the Timeout prompt is hidden
    And the relogin response count has not increased
```

Prior retained execution: `PASSED`. The observed logout request and all listed browser storage assertions completed.
The source checks the relogin response count, although its final assertion label says `reloginRequests`.
Storage absence does not establish cleanup of memory-only refresh credentials or provider revocation.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L493); assertions [502](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L502); [509](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L509); [515](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L515); [516](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L516); [517](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L517).
Helpers: [helper at 267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-idleLogout-20261025T095025/artifacts/idle-prompt-logout-1792921830430/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.

### E2E-15

**Acquire one refresh credential during a short background switch.**

Scope: Supporting visibility boundary. This case does not assert natural browser suspension.

Setup: Use the fast fixture while access A remains valid.
Wait six seconds, then allow ten seconds for setup renewal requests to finish.
Record the refresh response count before the switch.

```gherkin
Feature: A brief background switch before access expiry
  Scenario: Acquire refresh once and preserve authenticated access on return
    Given Home is visible with valid access A
    And setup renewal requests have finished
    When the test opens a covering page at about:blank and brings it to the foreground
    Then the portal document becomes hidden within 10 seconds
    And actual refresh R is observed within 10 seconds
    And tracked extension or relogin requests finish within 10 seconds
  Scenario: E2E-15 checkpoint 2
    Given the same E2E-15 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test waits 500 milliseconds
    Then the refresh response count has increased by exactly one
  Scenario: E2E-15 checkpoint 3
    Given the same E2E-15 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test restores the portal page to the foreground and closes the covering page
    Then the portal document becomes visible within 10 seconds
  Scenario: E2E-15 checkpoint 4
    Given the same E2E-15 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test waits one second
    Then the Timeout prompt is hidden
    And Home is visible
    And the Sign In button is hidden
  Scenario: E2E-15 checkpoint 5
    Given the same E2E-15 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the test waits six seconds and waits up to 10 seconds for renewal requests to finish
    And the portal user opens the protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status and body.result equal to true
    And its request carries the exact access stored immediately before that operation
    And Home is visible within 10 seconds
```

Prior retained execution: `PASSED`, including actual protected validation.
The counter counts refresh responses. It does not independently count requests or prove browser suspension.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L523); assertions [536](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L536); [541](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L541); [542](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L542); [543](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L543).
Helpers: [helper at 677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677); [helper at 187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-visibility-20261025T114220/artifacts/quick-visibility-refresh-1792928551414/result.json). Scope: `NATIVE_BROWSER`.

### E2E-16

**Use renewed access during reload and acquire new refresh credentials.**

Scope: Supporting reload boundary. No standalone approved criterion defines the complete reload sequence.

Setup: Use the fast fixture with Home visible and an initial stored access token A.
Wait six seconds, then allow ten seconds for setup renewal requests to finish.
Record login requests from immediately before reload until protected validation completes.
Reset only the observer's refresh variable before reload. Do not edit application credentials.

```gherkin
Feature: Reload after successful activity renewal
  Scenario: Validate the retained renewed access and install actual validation response access
    Given Home has stored access A and setup renewal requests have finished
    When the portal user moves the pointer once inside Home
    Then an actual access renewal completes within 15 seconds
    And stored access B exists and differs from A
  Scenario: E2E-16 checkpoint 2
    Given the same E2E-16 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the observer resets its refresh variable and starts recording login requests
    And the portal user reloads the page
    Then the reload validation response arrives within 30 seconds
    And its request body.singleUIAuthorization is exactly B
    And its HTTP status is successful and body.result is true
    And its actual authorization header C has a future expiry
    And stored access becomes exactly C within 10 seconds
    And Home is visible within 30 seconds
    And the Sign In button is hidden
  Scenario: E2E-16 checkpoint 3
    Given the same E2E-16 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test ensures refresh acquisition after reload, hiding and restoring the portal only if acquisition is still needed
    Then an actual successful refresh response after reload provides observed refresh R
    And R has more than 30 seconds remaining
  Scenario: E2E-16 checkpoint 4
    Given the same E2E-16 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test waits six seconds and waits up to 10 seconds for renewal requests to finish
    And the portal user opens the protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status and body.result equal to true
    And its request carries the exact access stored immediately before that operation
    And Home is visible within 10 seconds
    And zero additional login requests occurred during reload and protected validation
```

Prior retained execution: `PASSED`. Actual validation rotated access and the portal installed the returned token.
This case proves refresh reacquisition after reload. It does not prove refresh credential persistence.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L554); assertions [557](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L557); [562](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L562); [575](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L575); [576](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L576); [577](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L577); [578](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L578); [580](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L580); [584](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L584); [585](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L585); [590](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L590); [592](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L592).
Helpers: [helper at 677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677); [helper at 219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219); [helper at 683](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L683); [helper at 187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-reload-20261025T114249/artifacts/reload-preserves-renewed-session-1792928577405/result.json). Scope: `NATIVE_BROWSER`.

### E2E-17

**Cancel pending manual renewal when the user chooses Logout.**

Scope: Supporting cancellation boundary. No standalone approved criterion defines the complete late response sequence.

Setup: Use the fast fixture and wait for the Timeout prompt after access expiry.
Confirm observed refresh R has more than 30 seconds remaining.
Forward relogin to the actual service, then hold its successful response before browser delivery.
The release attempt can fail when the browser already cancelled its request.

```gherkin
Feature: Logout during manual renewal
  Scenario: A held relogin response cannot restore access after Logout
    Given the Timeout prompt and Extend button are visible
    And actual refresh R has more than 30 seconds remaining
    When the portal user clicks Extend
    Then the actual authentication service receives relogin within 10 seconds
    And its held response has successful HTTP status and an authorization header
    And the Timeout prompt remains visible before Logout
  Scenario: E2E-17 checkpoint 2
    Given the same E2E-17 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the portal user clicks Logout in the Timeout prompt
    Then the Sign In button is visible within 10 seconds
    And localStorage.SET_TOKEN is absent
    And the browser reports cancellation of the pending relogin request within 10 seconds
  Scenario: E2E-17 checkpoint 3
    Given the same E2E-17 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test attempts delivery of the held actual response
    And the test records whether delivery completed or the browser rejected the cancelled request
    And the test waits 1500 milliseconds
    Then localStorage.SET_TOKEN remains absent
    And Home remains hidden
```

Prior retained execution: `FAILED` because the prompt closed before the Logout action.
Logout cancellation and late response restoration assertions were not reached.
This result does not prove token restoration after logout.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L758); assertions [773](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L773); [776](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L776); [780](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L780); [781](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L781).
Helpers: [helper at 267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267); [helper at 740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740); [helper at 748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-manualLogout-20261025T093538/artifacts/pending-manual-logout-cancellation-1792920945026/result.json). Scope: `NATIVE_BROWSER`.

### E2E-18

**Cancel pending activity renewal when logout removes Home.**

Scope: Supporting cancellation boundary. Logout and Home removal occur together in this fixture.

Setup: Use the fast fixture and finish setup renewal requests.
Forward an activity extension to the actual service, then hold its successful response before browser delivery.
Do not isolate this result as an arbitrary component unmount test.

```gherkin
Feature: Logout while an activity extension response is held
  Scenario: A held activity response cannot restore Home after logout
    Given Home is visible and setup renewal requests have finished
    When the portal user moves the pointer once inside Home
    Then the actual extension service receives the request within 15 seconds
    And its held response has successful HTTP status and an authorization header
  Scenario: E2E-18 checkpoint 2
    Given the same E2E-18 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the portal user opens the user menu
    And chooses the logout menu action
    And confirms Logout
    Then the Sign In button is visible within 10 seconds
    And the browser reports cancellation of the pending extension request within 10 seconds
  Scenario: E2E-18 checkpoint 3
    Given the same E2E-18 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test attempts delivery of the held actual extension response
    And the test records whether delivery completed or the browser rejected the cancelled request
    And the test waits 1500 milliseconds
    Then localStorage.SET_TOKEN remains absent
    And Home remains hidden
```

Prior retained execution: `FAILED` while waiting for extension cancellation after logout.
The test did not deliver the late response or reach the access restoration assertions.
This result does not prove token restoration after logout.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L790); assertions [809](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L809); [810](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L810).
Helpers: [helper at 677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677); [helper at 219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219); [helper at 698](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L698); [helper at 740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740); [helper at 748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/result.json).

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-activityLogout-20261025T095133/artifacts/pending-activity-home-unmount-cancellation-1792921899213/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.

### E2E-19

**Preserve manual renewal access when an older activity response arrives late.**

Scope: Supporting request ordering boundary. No standalone approved criterion defines the entire ordering sequence.

Setup: Use the fast fixture, acquire actual refresh R, and finish setup renewal requests.
R must have more than 30 seconds remaining at acquisition.
Forward an activity extension to the actual service and hold its successful response across access expiry.

```gherkin
Feature: Ordering between activity extension and manual renewal
  Scenario: An older activity response does not replace later manual renewal access
    Given Home has actual refresh R and setup renewal requests have finished
    When the portal user moves the pointer once inside Home
    Then an actual successful extension response with authorization header B is held within 15 seconds
  Scenario: E2E-19 checkpoint 2
    Given the same E2E-19 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When access expires and the Timeout prompt appears
    Then refresh R has more than 30 seconds remaining
    And the browser reports cancellation of the earlier extension request within 10 seconds
  Scenario: E2E-19 checkpoint 3
    Given the same E2E-19 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the portal user clicks Extend
    And the test holds its relogin request before dispatch for 1500 milliseconds
    Then relogin starts within 10 seconds
    And the Timeout prompt remains visible with zero closures
  Scenario: E2E-19 checkpoint 4
    Given the same E2E-19 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test forwards relogin to the actual service and delivers its successful response
    Then the response arrives within 30 seconds with usable access C
    And the Timeout prompt is hidden within 10 seconds and has closed exactly once
    And stored access is exactly C
    And C differs from the earlier extension access B
  Scenario: E2E-19 checkpoint 5
    Given the same E2E-19 execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the test attempts delivery of the older held extension response
    And the test waits 1500 milliseconds
    Then stored access remains exactly C
    And the prompt closure count remains exactly one
  Scenario: E2E-19 checkpoint 6
    Given the same E2E-19 execution has completed checkpoints 1 through 5 with every prior assertion satisfied
    When the test waits six seconds and waits up to 10 seconds for renewal requests to finish
    And the portal user opens the protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status and body.result equal to true
    And its request carries the exact access stored immediately before that operation
    And Home is visible within 10 seconds
```

Prior retained execution: `FAILED` because opening the prompt did not cancel the earlier extension within ten seconds.
Manual success, distinct token comparison, late delivery, and overwrite assertions were not reached.
The failure does not establish that an older response overwrote newer access.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L820); assertions [842](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L842); [845](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L845); [846](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L846).
Helpers: [helper at 683](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L683); [helper at 677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677); [helper at 267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267); [helper at 277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277); [helper at 740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740); [helper at 748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748); [helper at 187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/result.json).

Current candidate `c42e760`: [FAILED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-late-20261025T114319/artifacts/late-activity-after-manual-success-1792928610202/result.json). Scope: `NATIVE_BROWSER`.

### E2E-20

**Reject an actual credential after its natural expiry.**

Criterion: [TC-05](intake.md#L267), frozen intake Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`.
This fixture tests expiry, not provider revocation.

Setup: Use the fast fixture and capture actual initial access A.
Use the configured read-only protected validation request.
Keep the actual wall clock and service tokens unchanged.

```gherkin
Feature: Actual expired access denial
  Scenario: The protected validation service rejects naturally expired access
    Given the portal user has actual initial access A
    When the portal user opens the configured protected validation operation
    Then its response arrives within 30 seconds with successful HTTP status
    And the captured request method is GET, HEAD, or POST for this configured read-only operation
  Scenario: E2E-20 checkpoint 2
    Given the same E2E-20 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test calculates the time until A expires plus 1500 milliseconds
    Then that wait is at most 1200 seconds
  Scenario: E2E-20 checkpoint 3
    Given the same E2E-20 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test waits that calculated duration using the actual wall clock
    Then A has expired
  Scenario: E2E-20 checkpoint 4
    Given the same E2E-20 execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the test copies the captured operation method, headers, and payload
    And replaces its authorization header with exact expired access A
    And replaces body.singleUIAuthorization with exact expired access A
    And sends that request through the browser context HTTP client
    Then the actual service responds within 30 seconds with HTTP 401 or HTTP 403
```

Prior retained execution: `PASSED`. The initial operation returned HTTP 200; the expired credential request returned HTTP 401.
The request occurred 1524 milliseconds after the actual token expiry.
The denial request uses the browser context HTTP client, not a second portal UI operation.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L856); assertions [863](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L863); [865](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L865); [868](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L868); [870](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L870); [879](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L879); [887](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L887).
Helpers: [helper at 209](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L209).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/artifacts/result.json).

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-expired-20261025T095205/artifacts/TC-05-actual-expired-credential-denial-1792921935621/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.

### E2E-21

**Observe a 30-minute background return when refresh acquisition fails.**

Scope: [TC-04](intake.md#L266), frozen intake Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`.
This case records observations only. Missing-refresh recovery acceptance remains unresolved under `O-001`.
No approved outcome selects continued access, a retry prompt, or Sign In.

Setup and controls: Use the natural fixture in a new isolated browser context.
Abort each actual refresh acquisition request before it receives a credential.
Do not fabricate refresh credentials or remove application memory credentials.

```gherkin
Feature: Observation of background return without refresh credentials
  Scenario: Record the return state without inventing a recovery acceptance policy
    Given a new isolated portal context signs in with actual valid access A
    And its transport aborts every refresh acquisition request and counts each attempt
    When the test brings another portal page to the foreground
    Then the isolated subject document becomes hidden within 10 seconds
    And the configured background duration is at least 1800 seconds
  Scenario: E2E-21 checkpoint 2
    Given the same E2E-21 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test leaves the subject hidden for the configured 1800 seconds using the actual wall clock
    When the test returns the subject page to the foreground and waits 1500 milliseconds
    Then no successful refresh credential has been observed for the subject
    And at least one actual refresh acquisition was blocked
    And the result records elapsed time, retained access summary, and authentication responses and failures
    And the result records Home, Sign In, and Timeout prompt visibility
    And the result records lifecycle events and whether a freeze event occurred
    And the verification level is OBSERVATION_ONLY
    And no recovery outcome acceptance verdict is assigned
```

Prior retained execution: `OBSERVATION_ONLY`; the runner's operational status was `PASSED`.
The subject remained hidden for 1801814 milliseconds and recorded a freeze event.
One acquisition was blocked. Sign In was visible; retained access was absent.
The controlled acquisition failure does not establish the original production cause.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L893); assertions [909](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L909); [916](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L916); [917](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L917).
Helpers: [helper at 45](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L45).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/artifacts/result.json).

Current candidate `c42e760`: [NOT_RERUN](evidence/minor-fixes-20261025/issue-2/not-rerun.json). This observation remains outside business totals.

### E2E-22

**Observe saved workspace descriptors after sign-out and sign-in.**

Scope: [TC-07](intake.md#L269), frozen intake Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`.
This case records observations only. Populated workspace restoration acceptance remains unresolved under `O-004`.

Setup: Use the fast fixture and the same configured user credentials for both sign-in actions.
The retained setup clicks Add Workspace once, producing at least two UI-created workspaces in total.
This fixture does not create application tiles or populated application parameters.

```gherkin
Feature: Observation of workspace descriptors across reauthentication
  Scenario: Compare stored workspace descriptors without inventing a restoration acceptance policy
    Given the portal user is signed in and Home is visible
    When the portal user clicks Add Workspace using the configured setup action
    And the test waits 500 milliseconds
    Then at least two UI-created workspaces exist
  Scenario: E2E-22 checkpoint 2
    Given the same E2E-22 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the test records the stored workspace descriptors before logout
    And the portal user opens the user menu, chooses logout, and confirms Logout
    Then the Sign In button is visible within 10 seconds
  Scenario: E2E-22 checkpoint 3
    Given the same E2E-22 execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the test records descriptors after logout
    And the portal user signs in with the same configured credentials
    Then Home is visible within 30 seconds
    And the test records descriptors after sign-in
    And each descriptor records workspace ID and container ID, container, module, tile, and parameter hash
    And the result records descriptor equality, entitlement hash equality, and user identity hash equality
    And the result records whether two workspaces contain populated application parameters
    And the verification level is OBSERVATION_ONLY
    And no restoration outcome acceptance verdict is assigned
```

Prior retained execution: `OBSERVATION_ONLY`; setup and reauthentication completed.
Two empty descriptors matched after sign-in. Entitlement and user identity hashes also matched.
The script records these comparisons but does not assert an unresolved restoration policy.
Populated application parameters, in-memory edits, and cross-origin application contents remain untested.

Source: [case function](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L946); assertions [956](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L956).
Helpers: [helper at 929](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L929); [helper at 698](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L698); [helper at 119](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L119).
Execution: [run](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/artifacts/result.json).

Current candidate `c42e760`: [OBSERVATION_ONLY](evidence/minor-fixes-20261025/issue-2/browser/issue-2-workspace-20261025T095318/artifacts/TC-07-workspace-descriptor-observation-1792922003938/result.json). Scope: `DOM_SERVICE_ONLY_LOCKED_MAC`.
Physical UI and native lifecycle remain unverified while macOS is locked.
This observation remains outside business-case totals.

## Supplemental browser probes

These probes are separate from the 22-case suite. Their definitions preserve their distinct response conditions.

### PROBE-DELAYED-REFRESH

**Delayed actual refresh delivery must preserve manual Extend recovery**

Definition version: `1`. Scope: supplemental delayed-credential boundary, outside the original 22-case suite.
Related requirement context: [TC-03](intake.md#L265) and the [delayed-refresh unit assertion](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json).
This controlled transport probe does not implement the natural suspension condition in that intake case.

Use the fast fixture with 60-second access and 144-second refresh lifetimes.
Fetch one actual refresh response while access remains valid. Hold browser delivery until the subject returns after access expiry.
Keep response bytes and clocks unchanged. Capture credentials as hashes and expiry values only.

```gherkin
Feature: Preserve manual recovery when usable refresh arrives after access expiry
  Scenario: Deliver a successful refresh response after returning with expired access
    Given portal Home is visible and SET_TOKEN contains access token A
    And token A has at least 30 seconds before expiry
    When a covering page hides the subject portal
    And the driver fetches POST /api/auth/v2/sso/refreshtoken but holds browser delivery
    Then the held actual response exists within 15 seconds
    And its HTTP status equals 200
    And access token A remains valid when the service response arrives
    And the response single-ui-refresh header contains refresh token R with an expiry
  Scenario: PROBE-DELAYED-REFRESH checkpoint 2
    Given the same PROBE-DELAYED-REFRESH execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When real time passes through token A's expiry plus at least 25 milliseconds
    And the driver brings the subject portal to the front
    And the driver records the Timeout prompt, Extend state, lifecycle, and logout requests
    And the driver records whether token R remains unexpired before release
    And the driver releases the unchanged actual refresh response
    And the driver waits 200 milliseconds and records whether Extend is visible and enabled
    And the driver clicks Extend only when that recorded state permits a native click
    And the driver waits 3 seconds and captures the final portal state
    Then at least one POST /api/auth/v2/sso/relogin request was sent
    And portal Home is visible
    And SET_TOKEN contains an unexpired access token
    And the Timeout prompt is absent
```

Driver and verdict implementation: [runDelayedRefresh](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/delayed-refresh-runner.d9923d569ee7.mjs.snapshot#L87).
Final predicate: [manualRenewalSucceeded](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/delayed-refresh-runner.d9923d569ee7.mjs.snapshot#L161).
Exact fixture binding: [source binding](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json).
Execution: [FAILED result](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json) and [retained timing analysis](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json).

The latest run held delivery for 58.537 seconds. Refresh remained unexpired for 84.627 seconds after delivery.
Extend remained disabled. No click or relogin request occurred. Logout completed and Sign In replaced portal Home.
The pass predicate checks relogin request presence, usable stored access, portal visibility, and prompt absence.
It does not assert actual relogin response success, exact returned-token installation, or protected validation.
Natural freezing and deployed provider behavior remain untested. Raw `heldRefresh.requestAt` is invalid; use other retained timing fields.

### PROBE-NATURAL-IMMEDIATE

**Thirty-minute natural background recovery without held responses**

Definition version: `1`. Scope: supplemental recovery probe, outside the original 22-case suite.
Related criteria: [TC-03](intake.md#L265) and [TC-06](intake.md#L268).
This probe records closure ordering. It does not assert [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166).

Use natural-fixture credentials: 900-second access and 13,524-second refresh lifetimes.
Use separate native browser contexts for the hidden subject and visible idle control.
Hold no authentication response. Override no clock or document visibility state.

```gherkin
Feature: Recover a naturally hidden portal with immediate actual authentication responses
  Scenario: Renew after 1,800 real hidden seconds and validate protected portal access
    Given the subject portal user has SET_TOKEN containing authenticated access token A
    And a separate control session uses identical source revisions and fixture settings
    When the driver brings the control session to the front and hides the subject
    Then actual refresh token R arrives within 10 seconds
    And token R remains valid beyond 1,800 seconds plus 30 seconds
  Scenario: PROBE-NATURAL-IMMEDIATE checkpoint 2
    Given the same PROBE-NATURAL-IMMEDIATE execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the driver waits 1,800 real seconds without page polling or service requests
    Then the driver records elapsed wall time and the control lifecycle
    And the control Timeout prompt is visible
    And the control records no hidden visibilitychange event during the interval
  Scenario: PROBE-NATURAL-IMMEDIATE checkpoint 3
    Given the same PROBE-NATURAL-IMMEDIATE execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the driver brings the subject to the front
    Then the subject Timeout prompt becomes visible within 10 seconds
    And token R has more than 30 seconds before expiry
    And the driver records the subject lifecycle and whether a freeze event occurred
  Scenario: PROBE-NATURAL-IMMEDIATE checkpoint 4
    Given the same PROBE-NATURAL-IMMEDIATE execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the portal user clicks Extend without any route hold
    Then POST /api/auth/v2/sso/relogin responds within 30 seconds with HTTP status 200
    And its response JSON field result equals true
    And single-ui-authorization contains token B with more than 30 seconds before expiry
    And SET_TOKEN equals exactly token B within 10 seconds
    And portal Home becomes visible within 10 seconds
    And Sign In is absent
  Scenario: PROBE-NATURAL-IMMEDIATE checkpoint 5
    Given the same PROBE-NATURAL-IMMEDIATE execution has completed checkpoints 1 through 4 with every prior assertion satisfied
    When the driver waits 6 seconds and renewal requests settle within 10 seconds
    And the driver saves subject lifecycle before further navigation
    And the driver records prompt closure and relogin response observation timestamps
    And the driver reads current SET_TOKEN and navigates to portal root / on the same origin
    Then validation arrives within 30 seconds with HTTP status 200
    And validation response JSON field result equals true
    And its request field singleUIAuthorization equals that current SET_TOKEN
    And portal Home becomes visible within 10 seconds
    And Sign In remains absent
    And zero additional login responses occur from Extend activation through protected validation
```

Assertion implementation: [natural background preconditions](evidence/minor-branch-rerun-20261020/supplemental-natural-immediate.cjs.snapshot#L91),
[actual relogin and exact installation](evidence/minor-branch-rerun-20261020/supplemental-natural-immediate.cjs.snapshot#L126),
and [protected validation](evidence/minor-branch-rerun-20261020/supplemental-natural-immediate.cjs.snapshot#L154).
Execution: [PASSED result](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/supplemental/result.json),
[complete run](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/run.json), and [interval integrity check](evidence/minor-branch-rerun-20261020/integrity-review.json).

The latest run retained 1,800,011 hidden milliseconds with freeze and resume events. Actual relogin and protected validation passed.
The prompt closed 54 milliseconds before the relogin response callback. This result does not verify pending-prompt completion ordering.
The script records freeze, but does not require freeze for its passing verdict. The retained interval separately supports observed freeze.
The driver counts login responses after Extend activation. It does not retain a complete login-request inventory.
The protected assertion covers local portal authentication only. Downstream business authorization remains outside this fixture.

## Current branch review cases

These definitions use version 1. Their test level is controlled component or service integration, unless stated otherwise.
The [current review inputs](evidence/code-review-refresh-20261021/inputs.json) bind the selected branch and requirement.

### Review terms and controlled environment

| Term | Exact meaning |
| --- | --- |
| Old revision | `mfe-base` commit `f025513f696476a9cc8162681410cbd21e029bcb`, the selected `main` merge base. |
| New revision | `mfe-base` commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` on `feature/session-refresh-minor`. |
| New runtime | Runtime bytes from `6d4c37c839b99d14ea41fd936da1a36cda526b17`. Commit `6e34da3` changes two test files only. |
| Actor | The Jest investigation controls fake time, UI events, and synthetic Axios responses. No live identity provider participates. |
| Access token | The synthetic `single-ui-authorization` response credential stored in `getHooksBase().store.token`. |
| Refresh token | The synthetic `single-ui-refresh` response credential stored in `getHooksBase().store.refreshToken`. |
| Access expiry | `getHooksBase().store.expiredIn`, expressed in epoch seconds. The tests compare expiry with controlled epoch milliseconds. |
| Acquisition | `POST /api/auth/v2/sso/refreshtoken`, invoked by Home scheduling or the named direct service call. |
| Access extension | `POST /api/auth/v2/sso/extend`. Its fixture returns access, not replacement refresh credentials. |
| Recovery | `POST /api/auth/v2/sso/relogin`. The request carries `Single-UI-Refresh`. |
| Timeout | The real Timeout component mounted in JSDOM. The recovery control has the accessible name `Extend`. |
| Authentication remains | `store.token` remains present. This observation alone does not establish downstream authorization. |
| Session A and session B | Distinct fixture sessions with `sessionId` values `session-A` and `session-B`. They identify successive authentication sessions. |
| Revocation | The Axios adapter records session-A logout and rejects its later refresh recovery with HTTP 401. |

The [execution setup](evidence/code-review-refresh-20261021/execution-setup.json) binds exported source, injected diagnostic hashes, and installed dependencies.
The [source integrity record](evidence/code-review-refresh-20261021/integrity.json) binds final checked bytes.
Tests use JSDOM, fake clocks, synthetic JWTs, and controlled Axios adapters.
Installed dependencies were shared. Historical dependency installations were not recreated.

Lifecycle cases start at `2026-09-21T00:00:00Z`. Race cases start at `2026-10-21T00:00:00Z`.
All timing below uses the fake clock. These test intervals do not establish production session policy.
Each case clears browser storage and restores adapters, timers, and request signals after execution.
The [lifecycle cleanup](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot#L66-L70) and [race cleanup](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L34-L39) define that isolation.
No new execution occurred while this catalog was written.

### REVIEW-F01

Title: preserve active access across the initial refresh expiry.
Definition version: 1. Level: controlled Home and Timeout integration.
Intent: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), candidate requirement version 4.
Original mapping: [E2E-06](#e2e-06) checks the related shortened browser boundary.
This controlled case reaches the exact four-hour fixture boundary. It does not replace the browser case.
Finding: [F-01](code-review-minor-20261021.md#f-01-p2-preserve-active-access-across-the-refresh-deadline).

Setup: seed access expiry at start plus 15 minutes and refresh expiry at start plus four hours.
Keep the page visible. The adapter returns a new access token for each extension.
The fixture performs no replacement acquisition during this case.

```gherkin
Feature: Session issue verification for REVIEW-F01
  Scenario: REVIEW-F01 Active access survives the initial refresh expiry
    Given the controlled Home session has access valid for 15 minutes
    And its initial refresh token expires four hours after the lifecycle clock starts
    And each access-extension response supplies access valid for another 15 minutes
    When the actor advances the clock by ten minutes and dispatches one mouse movement
    And the actor advances the clock by five quiet seconds to complete the extension
    And the actor repeats that activity cycle until 23 extension requests complete
    Then the extension request count equals 23
    And the installed access expiry exceeds the initial refresh expiry
  Scenario: REVIEW-F01 checkpoint 2
    Given the same REVIEW-F01 execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the actor advances to the initial refresh expiry and then advances one second
    Then the SSO logout request count equals zero
    And the Home session still has an installed access token
```

Reading order:

1. Seed the two expiry times and configure successful extension responses.
2. Repeat the ten-minute wait, one mouse movement, and five-second wait 23 times.
3. Check extension count and access validity before the initial refresh deadline.
4. Cross the initial refresh deadline and inspect logout count and authentication state.

Assertion map: the [executable characterization](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot#L73-L94) checks count, expiry, authentication, and logout.
Its final assertions intentionally compare old and new actual results. They do not assert candidate acceptance.

| Result | Old revision | New revision |
| --- | --- | --- |
| Extension count | 23 | 23 |
| Access valid across initial refresh expiry | Yes | Yes |
| SSO logout requests | Zero | One |
| Authentication after the extra second | Present | Cleared; Sign in visible |
| Intended assertions | Passed under the controlled setup | Failed |

Evidence: [old actual values](evidence/code-review-refresh-20261021/lifecycle-baseline-active_cutoff/actual.json), [new actual values](evidence/code-review-refresh-20261021/lifecycle-candidate-active_cutoff/actual.json), and [paired reconciliation](evidence/code-review-refresh-20261021/summary.json).
Limit: equal initial refresh credentials isolate expiry handling. The case does not compare tab-hide acquisition.
Owner: unknown application owner. Next action: correct active-access termination and repeat this paired case.

### REVIEW-F02

Title: replace eligible refresh credentials when the acquisition callback runs one millisecond late.
Definition version: 1. Level: controlled Home hook integration.
Finding: [F-02](code-review-minor-20261021.md#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late).
Intent: review inference from the existing acquisition path. A separate approved timer-tolerance criterion is unavailable.
Original test mapping: retained diagnostic `F02`; no equivalent original browser case exists.

Setup: seed 15-minute access and a refresh token with two hours of validity.
The replacement fixture has four hours of validity. Keep the page visible.
After Home schedules acquisition, make `Date.now()` report one millisecond beyond the scheduled clock.
The intended request-count assertion below remains a review expectation, pending owner confirmation.

```gherkin
Feature: Session issue verification for REVIEW-F02
  Scenario: REVIEW-F02 Acquisition remains eligible one millisecond after its target
    Given visible Home has access valid for 15 minutes and refresh valid for two hours
    And Home schedules acquisition 25000 milliseconds before access expiry
    And the adapter can return a replacement refresh token valid for four hours
    When the actor offsets the reported clock by one millisecond
    And the actor delivers the scheduled acquisition callback
    Then access has exactly 24999 milliseconds of remaining validity
    And exactly one refresh-acquisition request reaches the adapter
    And the stored refresh token equals the adapter's replacement credential
    And the stored refresh credential remains unexpired
    And Home's showTimeout state equals false
```

Reading order:

1. Render Home with the seeded access and refresh credentials.
2. Schedule acquisition, then add the one-millisecond reporting offset.
3. Deliver the callback at its original target and inspect requests and state.

Assertion map: [diagnostic assertions](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L42-L76) check all recorded predicates.
Their branch-dependent assertions characterize the adverse candidate result.

| Result | Old revision | New revision |
| --- | --- | --- |
| Remaining access validity | 24,999 milliseconds | 24,999 milliseconds |
| Acquisition requests | One | Zero |
| Replacement installed | Yes | No |
| Stored refresh remains unexpired | Yes | Yes |
| Timeout state | False | False |

Evidence: [old actual values](evidence/code-review-refresh-20261021/races-baseline-f02/actual.json), [new actual values](evidence/code-review-refresh-20261021/races-candidate-f02/actual.json).
Limit: this retained-refresh initial state is synthetic for the old Home journey. No user recovery failure is established.
Owner: unknown application owner. Next action: confirm timer tolerance or retain the P3 robustness issue.

### REVIEW-F03A

Title: isolate a new sign-in from a prior refresh response delivered before sign-in.
Definition version: 1. Level: controlled reducer, interceptor, and service integration.
Finding: [F-03A](code-review-minor-20261021.md#case-f-03a-the-old-response-arrives-before-the-new-sign-in).
Intent: review inference from the inspected session boundary. An approved late-response criterion is unavailable.
Original test mapping: retained diagnostic `F03` with `delivery=before-login`.
The original [E2E-17](#e2e-17) and [E2E-18](#e2e-18) cover related cancellation boundaries, not this complete sign-in sequence.

Setup: session A has 15-minute access. Hold its pending refresh response with four-hour refresh validity.
Normal username/password sign-in returns session-B access. Replacement acquisition returns session-B refresh.
Recovery with session-A refresh after logout returns HTTP 401. Recovery with session-B refresh returns session-B access.
These responses and revocation are adapter fixtures, not observed provider responses.

```gherkin
Feature: Session issue verification for REVIEW-F03A
  Scenario: REVIEW-F03A Recovery uses the new session after old refresh arrives before sign-in
    Given session A has valid access and one pending refresh-acquisition request
    And the adapter holds session A's refresh response
    When the actor sends session-A logout and clears local session storage
    Then stored access and refresh credentials are both absent
  Scenario: REVIEW-F03A checkpoint 2
    Given the same REVIEW-F03A execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the actor releases session A's held response
    And the actor signs in through the login service to create session B
    And the actor invokes refresh acquisition 25 seconds before session-B access expiry
    And the actor invokes recovery at session-B access expiry
    Then the recovery request's Single-UI-Refresh identifies session B
    And the installed access token equals the adapter's recovered session-B access
    And session B's access token remains present
```

Reading order:

1. Hold session-A acquisition, complete logout, and verify local credentials are absent.
2. Deliver the old response, then sign in to session B.
3. Invoke acquisition at the 25-second lead and recovery at access expiry.
4. Inspect the recovery header and installed access credential.

Assertion map: [service sequence and assertions](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L78-L148).
The final executable assertions characterize candidate failure. The intended Gherkin remains a review expectation.

| Result | Old revision | New revision |
| --- | --- | --- |
| Refresh session after new sign-in | Absent | Session A |
| Replacement requests after sign-in | One | Zero |
| Recovery header session | Session B | Session A |
| New session recovery | Access installed | HTTP 401 fixture clears session B |

Evidence: [old actual values](evidence/code-review-refresh-20261021/races-baseline-f03-before/actual.json), [new actual values](evidence/code-review-refresh-20261021/races-candidate-f03-before/actual.json).
Limit: acquisition and recovery are direct service calls. Home timer delivery and live provider behavior are excluded.
Owner: unknown application owner. Next action: reject ended-session credentials or replace them before new-session recovery.

### REVIEW-F03B

Title: isolate a new sign-in from a prior refresh response delivered after sign-in.
Definition version: 1. Level: controlled reducer, interceptor, and service integration.
Finding: [F-03B](code-review-minor-20261021.md#case-f-03b-the-old-response-arrives-after-the-new-sign-in).
Intent and fixtures: use the defined [session-boundary expectation](#review-f03a).
Original test mapping: retained diagnostic `F03` with `delivery=after-login`.

```gherkin
Feature: Session issue verification for REVIEW-F03B
  Scenario: REVIEW-F03B Recovery uses the new session after old refresh arrives after sign-in
    Given session A has valid access and one held refresh-acquisition response
    And the adapter models session revocation and recovery as defined for REVIEW-F03A
    When the actor sends session-A logout and clears local session storage
    Then stored access and refresh credentials are both absent
  Scenario: REVIEW-F03B checkpoint 2
    Given the same REVIEW-F03B execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the actor signs in through the login service to create session B
    And the actor releases session A's held response
    And the actor invokes refresh acquisition 25 seconds before session-B access expiry
    And the actor invokes recovery at session-B access expiry
    Then the recovery request's Single-UI-Refresh identifies session B
    And the installed access token equals the adapter's recovered session-B access
    And session B's access token remains present
```

Reading order:

1. Hold session-A acquisition and complete logout.
2. Sign in to session B, then deliver the held session-A response.
3. Invoke acquisition at the 25-second lead and recovery at access expiry.
4. Inspect the recovery header and installed access credential.

Assertion map: [the after-login branch](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L112-L148) checks the same recovery predicates.

| Result | Old revision | New revision |
| --- | --- | --- |
| Late session-A refresh installed | Yes | Yes |
| Replacement requests after sign-in | One | Zero |
| Recovery header session | Session B | Session A |
| New session recovery | Access installed | HTTP 401 fixture clears session B |

Evidence: [old actual values](evidence/code-review-refresh-20261021/races-baseline-f03-after/actual.json), [new actual values](evidence/code-review-refresh-20261021/races-candidate-f03-after/actual.json).
Limit: old and new handlers can accept the late response. The changed replacement rule worsens this existing race.
Owner: unknown application owner. Next action: validate stale-response rejection and current-session recovery together.

### REVIEW-F03-CONTROL

Title: characterize both revisions without a replacement opportunity.
Definition version: 1. Level: controlled service integration. Status: observation control, not a business acceptance case.
Finding mapping: [F-03C](code-review-minor-20261021.md#case-f-03c-neither-version-gets-the-replacement-opportunity).
Original test mapping: diagnostic `F03`, `delivery=after-login`, `NO_NEXT_ACQUISITION=1`.
Setup: use [REVIEW-F03B](#review-f03b). Suppress only its acquisition call before recovery.

```gherkin
Feature: Session issue verification for REVIEW-F03-CONTROL
  Scenario: REVIEW-F03-CONTROL Neither revision receives a replacement opportunity
    Given session A's refresh response remains held while the actor ends session A
    And the adapter revokes session A and creates session B through normal login
    When the actor releases session A's response after session-B sign-in
    And the actor advances directly to session-B access expiry without replacement acquisition
    And the actor invokes recovery
    Then the count of replacement requests after sign-in equals zero
    And the recovery request's Single-UI-Refresh identifies session A
    And the adapter rejects that recovery with HTTP 401
    And session B's access token is absent after the response
```

Reading order:

1. Complete the after-login delivery order from the preceding case.
2. Omit the single acquisition call and advance directly to recovery.
3. Inspect request count, rejected refresh session, and cleared access.

Assertion map: [control switch and final assertions](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L123-L148).
Both revisions produce zero replacement requests and clear session B after rejected session-A recovery.
Evidence: [old actual values](evidence/code-review-refresh-20261021/races-baseline-f03-control/actual.json), [new actual values](evidence/code-review-refresh-20261021/races-candidate-f03-control/actual.json).
Limit: omitting a direct call models no replacement opportunity. It does not prove browser freezing.
Owner: unknown application owner. Next action: retain this unchanged failure when interpreting the two preceding comparisons.

### REVIEW-DELAYED-SCHEDULED

Title: enable manual recovery when scheduled refresh delivery follows access expiry.
Definition version: 1. Level: controlled Home, Timeout, and service integration.
Intent: [required background-recovery scope](change-review.md#request-and-source-facts) and successful manual renewal under [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176).
The exact late-delivery expectation is a source-backed review expectation. The candidate requirement has publication review pending.
Original mapping: [TC-03](intake.md#L265), [TC-06](intake.md#L268), and the separate [PROBE-DELAYED-REFRESH](#probe-delayed-refresh) investigation.

Setup: start visible Home with 15-minute access and no refresh credential.
Use the common scheduled acquisition path. The adapter holds its four-hour refresh response beyond access expiry.
The adapter can supply the named renewed access credential through recovery.

```gherkin
Feature: Session issue verification for REVIEW-DELAYED-SCHEDULED
  Scenario: REVIEW-DELAYED-SCHEDULED A usable late refresh permits manual recovery
    Given visible Home has access valid for 15 minutes and no refresh credential
    When the actor advances to 25 seconds before access expiry
    Then exactly one acquisition request reaches the adapter
    And no refresh credential is stored while its response remains held
  Scenario: REVIEW-DELAYED-SCHEDULED checkpoint 2
    Given the same REVIEW-DELAYED-SCHEDULED execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the actor advances to access expiry
    Then the Timeout dialog is visible
  Scenario: REVIEW-DELAYED-SCHEDULED checkpoint 3
    Given the same REVIEW-DELAYED-SCHEDULED execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the actor releases the held usable refresh response
    Then the stored refresh credential equals that response's refresh credential
    And the Extend control is enabled for manual recovery
  Scenario: REVIEW-DELAYED-SCHEDULED checkpoint 4
    Given the same REVIEW-DELAYED-SCHEDULED execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the actor selects Extend
    Then the installed access credential equals the adapter's renewed access credential
    And the Timeout dialog is absent after recovery completes
```

Reading order:

1. Start scheduled acquisition with no refresh credential and hold its response.
2. Cross access expiry and inspect Timeout.
3. Deliver usable refresh, select Extend, and inspect installed access and dialog closure.

Assertion map: [paired characterization](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot#L96-L125) asserts current failure in both revisions.
The [required recovery assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L372-L378) separately expects installed access and dialog closure.
The latter uses hide-triggered acquisition, defined in [REVIEW-DELAYED-HIDE](#review-delayed-hide).

| Result | Old revision | New revision |
| --- | --- | --- |
| Usable refresh installed after expiry | Yes | Yes |
| Extend after delivery | Disabled | Disabled |
| Recovery requests | Zero | Zero |
| State after another second | One logout; access cleared | One logout; access cleared |
| Required manual recovery | Failed | Failed |

Evidence: [old actual values](evidence/code-review-refresh-20261021/lifecycle-baseline-delayed_recovery/actual.json), [new actual values](evidence/code-review-refresh-20261021/lifecycle-candidate-delayed_recovery/actual.json).
Limit: the paired case proves downstream parity. It does not compare acquisition when a real browser becomes hidden.
Owner: unknown application owner; user for acceptance. Next action: retain inherited-defect status while assessing required recovery.

### REVIEW-DELAYED-HIDE

Title: renew access when hide-triggered refresh arrives after access expiry.
Definition version: 1. Level: controlled Home and Timeout integration.
Intent: [required background-recovery scope](change-review.md#request-and-source-facts) and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176).
Original test mapping: `[KNOWN-DEFECT]` case at the new revision. Related browser scopes are [E2E-07](#e2e-07) and [PROBE-DELAYED-REFRESH](#probe-delayed-refresh).

Setup: use 15-minute access, no refresh credential, a 25-second acquisition lead, and a held refresh response.
The test changes JSDOM visibility and fake time. It does not suspend or freeze a real browser.

```gherkin
Feature: Session issue verification for REVIEW-DELAYED-HIDE
  Scenario: REVIEW-DELAYED-HIDE Manual Extend installs access after late hide-triggered acquisition
    Given Home has 15-minute access and no refresh credential
    And the acquisition response remains held in the adapter
    When the actor advances to 26 seconds before access expiry and marks the document hidden
    Then exactly one acquisition request reaches the adapter
    And the store has no refresh credential
  Scenario: REVIEW-DELAYED-HIDE checkpoint 2
    Given the same REVIEW-DELAYED-HIDE execution has completed checkpoints 1 through 1 with every prior assertion satisfied
    When the actor sets the fake clock to access expiry and marks the document visible
    Then the Timeout dialog is visible
  Scenario: REVIEW-DELAYED-HIDE checkpoint 3
    Given the same REVIEW-DELAYED-HIDE execution has completed checkpoints 1 through 2 with every prior assertion satisfied
    When the actor releases the usable refresh response
    Then the store contains the response refresh credential
  Scenario: REVIEW-DELAYED-HIDE checkpoint 4
    Given the same REVIEW-DELAYED-HIDE execution has completed checkpoints 1 through 3 with every prior assertion satisfied
    When the actor selects Extend
    Then the stored access credential equals the adapter's renewed access credential
    And the Timeout dialog is absent
```

Reading order:

1. Hide the document 26 seconds before access expiry and hold the acquisition response.
2. Set access expiry time, show the document, and release the held response.
3. Select Extend and check renewed access and Timeout removal.

Assertion map: [setup and characterization](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L325-L368), [intended assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L372-L378).
Current outcome: `it.failing` records the known failure. A runner pass does not mean recovery passed.
Current executable characterization finds `isOnLogout=true` and disabled Extend after the response arrives.
Evidence: [current suite execution](evidence/code-review-refresh-20261021/suite-suite-suite/run.json), [current test results](evidence/code-review-refresh-20261021/suite-suite-suite/result.json).
Old result for this hide-specific sequence: `NOT_RUN` in the fresh review. Use the separate scheduled pair for downstream parity.
Owner: unknown application owner. Next action: remove `failing` only when the intended recovery assertions pass after correction.

### REVIEW-F04

Title: compile complete workspace-change event fixtures.
Definition version: 1. Level: static test-interface validation. This case defines no business behavior.
Finding: [resolved F-04](code-review-minor-20261021.md#f-04-resolved-event-fixture-type-errors).
Original mapping: two `handleChange` callers in the existing Home test fixture.

Setup: create button targets with parent and grandparent DOM nodes.
The grandparent IDs are `deleteWorkspace-1` and `editWorkspace-1`.
Use complete `React.SyntheticEvent` values through `workspaceChangeEvent`.

```gherkin
Feature: Session issue verification for REVIEW-F04
  Scenario: REVIEW-F04 Repaired event fixtures match the typed Home interface
    Given each workspace-change fixture supplies a complete React.SyntheticEvent
    And its target has the DOM ancestry required by handleChange
    When the actor typechecks the new revision with declaration and incremental output disabled
    Then the TypeScript process exits with code zero
    And no TS2322 event-fixture errors appear
```

Reading order:

1. Inspect the complete event helper and both callers.
2. Run `tsc --noEmit --emitDeclarationOnly false --incremental false --pretty false` against the selected export.
3. Check exit code and compiler output.

Assertion source: [event fixture and callers](../../repos/ui/mfe-base/src/pages/Home/index.test.tsx#L180-L211).
Old runtime-candidate result: two event-fixture TS2322 errors before test repair.
New result: compiler exit zero at test-only commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Evidence: [repair record](evidence/baseline-reassessment-20261021/test-repairs/repair-summary.json), [current compiler execution](evidence/code-review-refresh-20261021/types-corrected/run.json).
The compiler receipt records the empty output hash.
Limit: compilation verifies interface compatibility. It does not verify runtime session recovery or production packaging.
Owner: Codex for the authorized test-only repair. Next action: none for the resolved fixture errors.

## UAT Blotter investigation cases

These observation cases investigate the [reported symptom](evidence/uat-blotter-browser-20261021/user-request.txt).
They do not establish UAT deployment parity or approve session policy.
Definition version: 1. Level: local browser integration with actual MFE session code.
Actor: synthetic local user with fixture catalog permissions. Entity: one isolated portal session.
The browser uses a fresh native Edge profile and real elapsed time.
Local identity, catalog, entitlements, and business data replace unavailable external systems.
Access and refresh lifetimes come from each retained service setup. No browser clock is advanced.
CDP and a passive DOM observer remain attached. Natural browser freezing remains outside these assertions.
Each case closes its browser and removes its disposable profile after immediate result retention.

### UAT-BLOTTER-VISIBLE

Purpose: distinguish a missing popup from ordinary credential expiry in a fresh Blotter session.
Setup: mount only Cashflow Blotter. Record settled access expiry after initialization.

```gherkin
Feature: Local Blotter session timing observation

Scenario: A fresh visible Blotter session reaches its fixed access deadline
  Given Cashflow Blotter is mounted in the only populated workspace
  And the synthetic user has valid access and usable refresh credentials
  When the actor leaves the visible portal untouched until five seconds after settled access expiry
  Then no successful extension changes access expiry during the measured interval
  And the DOM observer records a Timeout dialog after settled access expiry
  And the Timeout dialog remains visible at the final observation
```

Reading order:

1. Sign in with the disclosed fixture catalog and mount Blotter.
2. Record settled expiry, mounted components, and request activity.
3. Leave the visible portal untouched across expiry.
4. Inspect the dialog and credential metadata.

Assertion implementation: [retained driver](evidence/uat-blotter-browser-20261021/browser/blotter-visible-01/runner.mjs.snapshot).
Actual result: **PASSED**, three assertions. [Execution](evidence/uat-blotter-browser-20261021/browser/blotter-visible-01/result.json).
Business intent remains the [candidate criteria](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

### UAT-BLOTTER-HIDDEN

Purpose: test return from a genuinely hidden Blotter browser tab.
Setup: use the fresh-session setup from [UAT-BLOTTER-VISIBLE](#uat-blotter-visible).

```gherkin
Feature: Local Blotter session timing observation

Scenario: A fresh hidden Blotter session reconciles fixed expiry
  Given Cashflow Blotter is mounted with valid access and usable refresh credentials
  When the actor activates a separate blank browser tab
  And the actor waits until five seconds after settled access expiry
  And the actor activates the portal tab
  Then the retained visibility event records the portal as hidden during the wait
  And no successful extension changes access expiry during the measured interval
  And the DOM observer records a Timeout dialog
  And the Timeout dialog is visible within five seconds after return
```

Reading order:

1. Sign in and mount Blotter.
2. Activate a separate blank tab and retain the visibility event.
3. Wait across access expiry without browser input.
4. Return to Blotter and inspect the dialog.

Assertion implementation: [retained driver](evidence/uat-blotter-browser-20261021/browser/blotter-hidden-01/runner.mjs.snapshot).
Actual result: **PASSED**, four assertions. [Execution](evidence/uat-blotter-browser-20261021/browser/blotter-hidden-01/result.json).

### UAT-BLOTTER-PRIOR-TILE

Purpose: test whether an actual previously visited tile renews while Blotter is selected.
Setup: retain actual Dashboard polling. Use access lifetime greater than its two-minute polling interval.
Dashboard is a conditional control. The user did not report opening Dashboard in the affected session.

```gherkin
Feature: Local Blotter session timing observation

Scenario: A hidden mounted Dashboard can move expiry while Blotter is selected
  Given the actor has visited Dashboard and then selected Cashflow Blotter
  And Dashboard remains mounted in a hidden workspace panel
  When the actor hides the portal browser tab across the original access deadline
  Then retained request initiators identify successful Dashboard polling and session extension
  And access expiry moves beyond its original deadline
  And no Timeout dialog is recorded before the renewed deadline

Scenario: Removing Dashboard permits a fixed-expiry comparison
  Given the actor has completed the retained Dashboard phase
  When the actor removes Dashboard and leaves Blotter untouched across settled access expiry
  Then recurring Dashboard requests stop
  And the DOM observer records the Timeout dialog
```

Reading order:

1. Visit Dashboard and select Blotter.
2. Hide the browser tab across the original access deadline.
3. Correlate query initiators, successful extensions, and changed expiry.
4. Remove Dashboard and observe the next fixed deadline.

Assertion implementation: [retained driver](evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/runner.mjs.snapshot).
Actual result: **FAILED**, five of seven assertions passed. [Execution](evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/result.json).
The [retained-Dashboard phase](evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/dashboard-retained-phase.json) passed all four assertions.
Native pointer activity contaminated the removal phase. Its fixed-expiry and final-dialog comparisons failed.
The [contamination checkpoint](evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/removal-contamination-checkpoint.json) retains this invalid control.
This case does not establish that Dashboard caused the reported UAT incident.

### UAT-BLOTTER-LATE-RETURN

Purpose: model return after both real credential deadlines expire while the portal remains hidden.
Setup: use valid access and acquired refresh credentials from the local BFF. Reject no authentication request.
This short lifetime control represents the deadline order. It does not establish UAT lifetimes or natural freezing.

```gherkin
Feature: Local Blotter session timing observation

Scenario: Timeout can open and close before a late return to Blotter
  Given Cashflow Blotter is mounted with valid access and usable refresh credentials
  When the actor activates a separate blank browser tab
  And the actor waits until five seconds after refresh expiry
  And the actor activates the portal tab
  Then the retained visibility event records the portal as hidden during the wait
  And the DOM observer records Timeout opening after access expiry
  And the DOM observer records Timeout closing before the actor returns
  And the Sign in screen replaces Home
  And local access storage is cleared
```

Reading order:

1. Sign in, mount Blotter, and acquire refresh through the actual visibility handler.
2. Hide the portal tab and leave both credential deadlines unchanged.
3. Wait across refresh expiry with real elapsed time.
4. Return and inspect the retained dialog sequence and final screen.

Assertion implementation: [retained driver](evidence/uat-blotter-browser-20261021/browser/blotter-late-return-01/runner.mjs.snapshot).
Actual result: **PASSED**, six assertions. [Execution](evidence/uat-blotter-browser-20261021/browser/blotter-late-return-01/result.json).
The dialog opened and closed while hidden. The final screen showed Sign in after actual refresh expiry.

### UAT-BLOTTER-NO-REFRESH

Purpose: distinguish never-created Timeout from a brief dialog followed by automatic logout.
Setup: mount Blotter and reject refresh acquisition through a disclosed local network fixture.

```gherkin
Feature: Local Blotter session timing observation

Scenario: Missing refresh credentials cause a brief Timeout and automatic logout
  Given Cashflow Blotter is mounted with valid access and no refresh credential
  And the local network fixture rejects refresh acquisition
  When the actor leaves the portal untouched across settled access expiry
  Then the DOM observer records a Timeout dialog
  And the Sign in screen replaces Home after automatic logout
  And local access storage is cleared
```

Reading order:

1. Sign in and mount Blotter with rejected refresh acquisition.
2. Observe DOM changes across expiry.
3. Inspect the final screen and access storage.

Assertion implementation: [unexecuted branch in retained driver](evidence/uat-blotter-browser-20261021/browser/blotter-late-return-01/runner.mjs.snapshot).
Actual result: **NOT_RUN**. The investigation prioritized actual acquired-refresh expiry.
The missing-refresh branch remains unverified. Owner: Codex for any authorized follow-up execution.

### UAT-BLOTTER-480-SCHEDULE

Purpose: check actual BFF issuance and the Home timer for a 480 minute access lifetime.
Actor: the synthetic local user. Entity: one fresh native Edge portal session with only Cashflow Blotter.
Setup: use isolated ports 8128 and 8129. Keep the browser clock unchanged.
The local BFF uses actual authentication, JWT, and session code with a 480 minute access setting.
Pass-through timer instrumentation records scheduling and cancellation. It preserves native timer execution.

```gherkin
Feature: Local Blotter session timing observation

Scenario: A 480 minute access credential schedules the matching Home popup timer
  Given the real local BFF issues an access credential with a 480 minute configured lifetime
  And Cashflow Blotter is mounted in the only populated workspace
  When the actor acquires refresh through native tab visibility changes
  And the actor leaves the visible portal untouched for fifteen real seconds
  Then each recorded access credential has exp minus iat equal to 28800 seconds
  And the active Home popup timer uses access exp multiplied by 1000 minus scheduling time
  And the recorded timer delay differs from that calculation by no more than 1000 milliseconds
  And the active Home popup timer remains pending at final observation
  And the refresh expiry timer is identified separately from the access popup timer
  And no Timeout dialog appears during the measured fifteen seconds
```

Reading order:

1. Sign in through the isolated actual BFF and mount the actual Blotter module.
2. Acquire refresh through native visibility changes and record credential metadata.
3. Compare the Home popup timer delay with the actual access expiry.
4. Observe fifteen real seconds and inspect timer state and dialog events.

Assertion implementation: the [retained driver snapshot](evidence/uat-blotter-browser-20261021/browser/blotter-480-schedule-03/runner.mjs.snapshot).
Actual result: **PASSED**, six assertions. [Execution](evidence/uat-blotter-browser-20261021/browser/blotter-480-schedule-03/result.json).
The access lifetime equals 28,800 seconds. The active access-popup delay equals 28,799,107 milliseconds.
The refresh timer is separate. No Timeout appears during the 15,017-millisecond observation.
Earlier [invalid precondition](evidence/uat-blotter-browser-20261021/browser/blotter-480-schedule-01/result.json) and [timer classification failure](evidence/uat-blotter-browser-20261021/browser/blotter-480-schedule-02/result.json) remain retained.
This case does not wait eight hours. It does not verify eventual timer firing or UAT deployment parity.

## Real-world session cases

These cases extend the [UAT investigation](#uat-blotter-investigation-cases) without replacing its retained definitions or results.
Definition version: 1. Level: source-backed configuration checks and actual browser integration observations.

Actor: one authorized portal user with Cashflow Blotter read access. Entity: one isolated authenticated portal session.
Local mode uses synthetic identity and disclosed business responses. Remote mode uses the authorized environment's actual services.

The [photograph](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json) shows a long remaining deadline, not an approved thirty-minute cutoff.
The [configuration audit](evidence/uat-blotter-browser-20261021/uat-screenshot/review-config-audit.json) separates packaged overrides from effective deployment evidence.

**The thirty-minute case failed its fixed-expiry assertion.** The [result](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json#L8251-L8285) blocks a clean fixed-expiry conclusion.
Owner: test harness maintainer. Next action: require a settled activity boundary before another fixed-expiry comparison.
Schedule, mismatch detection, and shortened-expiry controls passed with the current driver.

Earlier reusable runs retain their own driver hashes and outcomes below.
Historical passes do not validate later runner changes.
Stage-one results bind test repository commit `9314355b75771d756784ca872480848b9d206deb`.
Its runner SHA-256 is `3e8efa57860725f0804839588c07612d0ea8c2f5ab5de0d4bfd245923c777784`.

The current runner SHA-256 is `69967bd8d3c3cf9975d0a4d25e391d61c4367fd947d7158b911e9082167d20b1`.
Its test repository commit is `37b7365aca2203021e7014112b9d15cf00f7455b`.
The [exact comparison](evidence/real-world-tests-20261022/fixture-retention-only-comparison.json) identifies one fixture-evidence retention change. Timing and assertion bytes are unchanged.
The thirty-minute case executed stage one only. It was not rerun after this retention change.

The [offline regression receipt](evidence/real-world-tests-20261022/fixture-retention-offline-regressions.json) records 25 passing tests for the current source.

Approval of access, refresh, idle, and absolute limits remains unresolved. Owner: unknown authentication owner.
Next action: retain approved policy and effective configuration before assigning a business acceptance verdict.

### Real-world setup and observation boundaries

Use a new native Edge profile and the actual Base, Ratan Container, and Cashflow Blotter modules.
Record module revisions or hashes, loaded URLs, configuration hashes, browser settings, and all declared substitutions.

Keep credentials private. Retain credential hashes, claim values, numeric types, issuer, and clock metadata without raw credentials.
Use host monotonic time and wall-clock time. Keep the browser clock and application polling intervals unchanged.

Retain screenshots before hiding and after return. Do not foreground a hidden page for a screenshot.
Retain each completed case before cleanup. Save the measured start and pending deadline before extended waits.
Sequence native focus and input actions across cases. Mark a no-input control invalid if trusted activity changes.

The before-return checkpoint ends timing measurement. The returned-final checkpoint records the separate UI state after native return.

The [timing guidance](../../.agents/skills/verify-implementation/references/browser-investigation.md#verify-timing-inputs-and-deployment-settings) defines evidence boundaries.
Use [source inspection](evidence/uat-blotter-browser-20261021/source-hypotheses.json) for unchanged expiry and embedded-module paths.
Its Base revision is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; supplied consumer revisions remain unknown.

| Component | Identity and scope | Evidence and remaining check |
| --- | --- | --- |
| Home workspace tablist | `[aria-label="workspaces"]` in the portal document. | [Home source](../../repos/ui/mfe-base/src/pages/Home/index.tsx#L61-L65). Verify runtime uniqueness in each target. |
| Cashflow Blotter module | `[data-testid$="_Cashflow"]` and its `.ag-root-wrapper` grid marker in the selected workspace. | [Prior actual-module driver](evidence/uat-blotter-browser-20261021/browser/blotter-visible-01/runner.mjs.snapshot). The CSS grid marker is an implementation locator. |
| Timeout dialog | `[aria-labelledby="timeout-dialog-title"]` in the portal document. | [Dialog source](../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L14-L26). Verify runtime uniqueness and visibility. |
| Portal browser tab | The runner-owned native tab at the authorized target origin. | Record its identity separately from the runner-owned `about:blank` tab. |
| Native tab handles | The driver holds portal handle `page` and blank handle `blank` in the native browser window. | [Runner authentication and measurement](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/runner.mjs). These are driver identities, not accessible labels. |
| Workspace navigation | Target-specific tab and removal controls in the workspace tablist. | [Tab identities](../../repos/ui/mfe-base/src/components/TabPanel/index.tsx#L44-L49). Remote setup must inspect exact identities before use. |

The [new runner](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/runner.mjs) resides in the independent test repository.
Both entry points use the [timing helper](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/timing.cjs).
`timingProfile.expectedAccessLifetimeSeconds` declares the expected lifetime. The runner rejects a conflicting duplicate `profile.expectedAccessSeconds`.
These new bindings remain `UNVERIFIED` until their exact assertions and hashes receive inspection.
The historical twenty-two-case Robot suite retains its separate source and execution bindings.

### RW-CONFIG-PREFLIGHT

Purpose: establish the lifetime and clock inputs before interpreting a missing Timeout dialog.
This is a prerequisite observation for the browser profiles. It defines no new business timing policy.

Setup: retain the chosen target, actual issued access, available refresh, source declarations, and sanitized runtime setting evidence.
Use the BFF issuer and Base conversion paths identified by the [configuration audit](evidence/uat-blotter-browser-20261021/uat-screenshot/review-config-audit.json).
Run the [declaration auditor](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/config-audit.cjs) before interpreting the runtime preflight.

It reads selected JWT settings only. It retains minute values, second conversions, source lines, file hashes, and declared differences.
The [repository result](evidence/real-world-tests-20261022/source-config-audit-v2.json) records `CONFLICT`: access defaults declare `900` seconds; launch options declare `28800` seconds.
The [execution receipt](evidence/real-world-tests-20261022/source-config-audit-execution-v2.json) records passing conflict detection. Effective UAT configuration remains `NOT_BOUND`.

The auditor marks detected unsupported declaration forms `UNRESOLVED`. It does not evaluate complete YAML or shell semantics.
The [offline checks](evidence/real-world-tests-20261022/offline-combined-checks-v2.json) retain 24 passing tests, including unsupported-declaration regressions.

```gherkin
Feature: Observe actual session timing inputs
  @RW-CONFIG-PREFLIGHT
  Scenario: RW-CONFIG-PREFLIGHT distinguishes declared settings from observed issuance
    Given the authorized portal user has signed in through the selected authentication service
    And the profile declares its expected access lifetime, tolerance, and measurement units
    When the auditor compares selected JWT declarations from application.yml and app.conf
    And the driver records credential metadata and the browser clock
    Then access iat and exp have finite numeric values in epoch seconds
    And the difference between observed and expected access lifetimes does not exceed the declared tolerance in seconds
    And computed remaining access time equals access exp multiplied by 1000 minus browser capture time
    And the source audit contains minute values, second conversions, declaration lines, source hashes, and differences for selected JWT settings
    And unavailable runtime property sources and service clock offsets remain unknown
    And the evidence contains no raw access or refresh credential

  @RW-CONFIG-MISMATCH
  Scenario: RW-CONFIG-MISMATCH rejects a fifteen minute expectation against eight hour issuance
    Given the selected local service issues access valid for 28800 seconds
    And the profile incorrectly expects access valid for 900 seconds with zero tolerance
    When the driver compares actual issuance with the declared profile
    Then the preflight result is FAILED
    And the retained mismatch records expected 900 seconds and actual 28800 seconds
    And no idle measurement starts
```

Reading order:

1. Run the declaration auditor against the selected `application.yml` and `app.conf`. Retain its new output without replacing earlier evidence.
2. Sign in and capture claim values, types, clocks, and loaded-module identities.
3. Compare observed issuance with the explicitly declared profile value.
4. Retain disagreements and unavailable effective-setting evidence before continuing.

Required assertion binding: `real-world/runner.mjs --case RW-CONFIG-PREFLIGHT`. Inspection status: `UNVERIFIED`.
The existing Robot entry point retains its separate execution binding.
Stage-one preflight passed within the [schedule control](evidence/real-world-tests-20261022/rw-480-schedule-02/result.json).
This control observed access validity of `28800` seconds. It does not bind effective UAT configuration.

Current-driver preflight passed within the [schedule control](evidence/real-world-tests-20261022/rw-480-schedule-03/result.json).
The [current negative control](evidence/real-world-tests-20261022/rw-negative-900-03/result.json) retains raw **FAILED**, with 17 of 18 checks passing.
Its [classification](evidence/real-world-tests-20261022/rw-negative-900-03/negative-control-classification.json) records **PASSED** for detecting expected `900` versus actual `28800` seconds.
No idle measurement started after this mismatch.

The [current stack receipt](evidence/real-world-tests-20261022/rw-negative-900-03-stack/stack-result.json) retains the local Java source by hash only.
Its source contains private fixture values. Observed issuance and retained stack settings support the current lifetime comparison.
The earlier [Java snapshot](evidence/real-world-tests-20261022/rw-negative-900-01-stack/binding-001-LocalSessionApplication.java) contains redacted bytes.
The [redaction receipt](evidence/real-world-tests-20261022/redaction-receipt-01.json) preserves its original source hash and redaction boundary.

The stage-one [negative control](evidence/real-world-tests-20261022/rw-negative-900-02/result.json) retains raw **FAILED**, with 17 of 18 checks passing.
Its [classification](evidence/real-world-tests-20261022/rw-negative-900-02/negative-control-classification.json) records **PASSED** for detecting expected `900` versus actual `28800` seconds.
No idle measurement started after this mismatch.

The earlier [negative run](evidence/real-world-tests-20261022/rw-negative-900-01/result.json) retains raw **FAILED**, with 17 of 18 checks passing.
The separate [mismatch classification](evidence/real-world-tests-20261022/negative-control-classification.json) records **PASSED** for detecting the expected disagreement.
Its driver SHA-256 is `a511e2079b5d98460ac0a545cacf6cc76c4c1488a07d3f447b7cad296ca046f9`.

A declared revision or configuration value alone does not prove deployed bytes or effective settings.
A mismatch blocks the dependent profile. Missing property-source evidence blocks deployment parity, not all local observation.

### RW-480-SCHEDULE

Purpose: repeat [UAT-BLOTTER-480-SCHEDULE](#uat-blotter-480-schedule) through the reusable runner with explicit timing provenance.
Setup: actual local BFF access lifetime `480` minutes. Expected issued lifetime: `28800` seconds.
Mount only Cashflow Blotter. Record refresh expiry separately; do not assume refresh outlives access.

Use pass-through instrumentation that preserves native timers and records scheduling, replacement, cancellation, and callback identity.
The `1000` millisecond tolerance is a disclosed measurement bound. It defines no business response limit.

```gherkin
Feature: Observe the configured long session schedule
  @RW-480-SCHEDULE
  Scenario: RW-480-SCHEDULE observes a 480 minute access deadline without advancing time
    Given RW-CONFIG-PREFLIGHT records access exp minus iat as 28800 seconds
    And data grid ".ag-root-wrapper" is mounted in the only populated Cashflow Blotter workspace
    When the driver observes the active Home access-popup timer
    And the driver leaves the visible portal untouched for 15000 real milliseconds
    Then the active access-popup callback is identified separately from the refresh-expiry callback
    And the access-popup delay differs from exp multiplied by 1000 minus scheduling time by at most 1000 milliseconds
    And the active access-popup timer remains pending at final observation
    And the trusted activity counters have zero change during the measured interval
    And the measured document's timeOrigin equals its baseline value
    And retained main-frame navigation and page-replacement event counts each equal zero
    And the passive observer records zero timeout_opened events during the measured interval
```

Reading order:

1. Run the preflight against the disclosed 480-minute local service profile.
2. Mount Blotter and finish any setup visibility actions before the measurement starts.
3. Identify the actual access and refresh callbacks. Compare their separate deadlines.
4. Observe fifteen seconds, then retain active timers, activity counters, and dialog history.

Required assertion binding: `real-world/runner.mjs --case RW-480-SCHEDULE`. Inspection status: `UNVERIFIED`.
Stage-one result: [**PASSED**](evidence/real-world-tests-20261022/rw-480-schedule-02/result.json), with 34 of 34 checks passing.
The executed runner belongs to stage-one commit `9314355b75771d756784ca872480848b9d206deb`.
Current-driver result: [**PASSED**](evidence/real-world-tests-20261022/rw-480-schedule-03/result.json), with 34 of 34 checks passing.

The earlier [reusable run](evidence/real-world-tests-20261022/rw-480-schedule-01/result.json) records **PASSED**, with 33 of 33 checks passing.
Its driver SHA-256 is `a2acdaf074bf4bdbd012933094db5584eb10d3fc29306d479b690b6a99ab8506`.

The [original observation](#uat-blotter-480-schedule) remains a separate historical execution.
This case verifies scheduling only. It does not verify eight-hour firing, natural suspension, UAT settings, or approved policy.

### RW-BLOTTER-HIDDEN-30M

Purpose: observe the reported thirty-minute absence with actual Blotter code and unchanged elapsed time.
Setup: use the 480-minute local profile. Require both observed credential deadlines after the planned thirty-minute end.

Mount only Cashflow Blotter. Acquire refresh through actual application behavior before recording the settled measurement baseline.
Retain a start checkpoint before the wait. Use passive lifecycle and dialog observation; disclose attached automation.

No assertion requires a Timeout dialog at thirty minutes. No source establishes that cutoff as approved policy.

```gherkin
Feature: Observe actual Blotter inactivity
  @RW-BLOTTER-HIDDEN-30M
  Scenario: RW-BLOTTER-HIDDEN-30M observes thirty real minutes before either credential deadline
    Given RW-CONFIG-PREFLIGHT passes for the declared 480 minute local profile
    And data grid ".ag-root-wrapper" is mounted in the only populated Cashflow Blotter workspace
    And settled access and refresh deadlines are later than the planned observation end
    When the driver selects tab "blank" in the native browser window
    And the driver waits for at least 1800000 real milliseconds without portal input
    And the driver selects tab "page" in the native browser window
    Then host monotonic time and wall-clock time each record at least 1800000 milliseconds during the wait
    And the measured document's timeOrigin equals its baseline value
    And retained main-frame navigation and page-replacement event counts each equal zero
    And retained visibility events record no visible transition between hiding and return
    And trusted portal activity counters have zero change during the hidden wait
    And no successful extension moves access expiry during the hidden wait
    And settled access expiry remains unchanged at final observation
    And access and refresh deadlines remain later than final observation
    And the passive observer records zero timeout_opened events during the measured interval
    And data grid ".ag-root-wrapper" in the Cashflow Blotter workspace remains visible after return
```

Reading order:

1. Run preflight, mount only Blotter, and record settled access and refresh deadlines.
2. Record trusted activity counters and the actual hidden transition.
3. Retain the pending deadline, then wait thirty real minutes without browser actions.
4. Return and compare lifecycle history, renewals, credential deadlines, dialog history, and the mounted grid.

Required assertion binding: `real-world/runner.mjs --case RW-BLOTTER-HIDDEN-30M`. Inspection status: `UNVERIFIED`.
Stage-one result: [**FAILED**](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json), with 33 of 34 checks passing.
Its driver SHA-256 is `3e8efa57860725f0804839588c07612d0ea8c2f5ab5de0d4bfd245923c777784`.

The [measurement](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json#L8730-L8731) records `1800122` wall-clock milliseconds and `1800175.70875` monotonic milliseconds.
One successful extension response arrived `365` milliseconds after measurement start. It moved access expiry by `10` seconds.
No later extension response occurred during the measured interval.

The [queued-extension finding](evidence/real-world-tests-20261022/run03-queued-extension-finding.json) strongly supports a pending setup mouse debounce as the immediate cause.
The Home callback fired `336` milliseconds after measurement started. The extension request followed `7` milliseconds later.
The observer did not retain direct callback-to-request stack correlation. Alternative container callers remain possible.

Owner: test harness maintainer. Next action: settle pending activity before any future fixed-expiry observation.

Trusted input, document continuity, hidden visibility, and absent pre-deadline Timeout checks passed.
The retained lifecycle data includes a `freeze` event. CDP and passive observation remained attached.
The [fixed-expiry assertion](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json#L8251-L8285) remains failed. No assertion or expectation was relaxed.

The earlier [long run](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-01/result.json) retains **INTERRUPTED** before the thirty-minute measurement completed.
Its driver SHA-256 is `0d8fcf289bf51d4bb5a4ce41339e616f079304c7bb5fffb5cee07275beb6d556`.
Failed deadline or no-input preconditions invalidate this profile's fixed-expiry comparison.
Hidden visibility does not prove natural freezing. Local service substitutions do not establish UAT deployment parity.

### RW-SHORT-IDLE

Purpose: exercise real expiry branches without replacing the long-lifetime or thirty-minute observations.
Setup: disclose shortened access and refresh values in the retained local service configuration.
Use actual service issuance and real browser time. Keep application clocks and Dashboard polling intervals unchanged.

Set `expiryGraceMs` to `5000`. Require refresh validity for another `5000` milliseconds after the planned measurement ends.
Expected outcomes characterize inspected implementation. They do not approve logout, recovery, or inactivity policy.

```gherkin
Feature: Exercise session expiry with disclosed shortened lifetimes
  @RW-SHORT-IDLE
  Scenario: RW-SHORT-IDLE observes fixed access expiry in a clean hidden Blotter session
    Given RW-CONFIG-PREFLIGHT passes for the disclosed shortened local profile
    And data grid ".ag-root-wrapper" is mounted in the only populated Cashflow Blotter workspace
    And the planned observation ends 5000 milliseconds after settled access expiry
    And refresh expiry is later than the planned observation end plus 5000 milliseconds
    When the driver selects tab "blank" in the native browser window without further portal input
    And the driver waits until 5000 milliseconds after settled access expiry
    And the driver selects tab "page" in the native browser window
    Then retained visibility events record no visible transition between hiding and return
    And the measured document's timeOrigin equals its baseline value
    And retained main-frame navigation and page-replacement event counts each equal zero
    And trusted activity counters have zero change during the measured interval
    And no successful extension moves the settled access deadline
    And the passive observer records timeout_opened after the settled access deadline
    And dialog "Your session has been expired" in the portal document is visible at final observation

```

Reading order:

1. Record exact shortened values, actual issuance, settled deadlines, and the selected profile.
2. Hide the actual portal across access expiry without trusted input or other native-browser activity.
3. Compare dialog history with final display state. Retain the profile before the next session starts.

Required assertion binding: `real-world/runner.mjs --case RW-SHORT-IDLE`. This binding supports the hidden profile only.
Automation binding status: `UNVERIFIED`.
Stage-one result: [**PASSED**](evidence/real-world-tests-20261022/rw-short-idle-01/result.json), with 30 of 30 checks passing.
The executed runner belongs to stage-one commit `9314355b75771d756784ca872480848b9d206deb`.
Current-driver result: [**PASSED**](evidence/real-world-tests-20261022/rw-short-idle-02/result.json), with 30 of 30 checks passing.

The [prior short controls](#uat-blotter-visible), [hidden control](#uat-blotter-hidden), and [late-return control](#uat-blotter-late-return) keep their historical bindings.
Visible and late-return profiles in the new runner remain deferred: **NOT_RUN; automation binding unavailable**.
They must preserve the linked historical assertions, including Timeout opening and closing before a late return.

The prior-tile and clean-removal profiles remain deferred: **NOT_RUN; automation binding unavailable**.
They reuse [UAT-BLOTTER-PRIOR-TILE](#uat-blotter-prior-tile), including its retained failed removal comparison.

Required preconditions include actual Dashboard polling at `120000` milliseconds and access lifetime greater than that interval.
The retained-tile phase must correlate Dashboard query initiators, successful extensions, moved expiry, and absent pre-deadline Timeout.
The clean-removal phase must show zero later Dashboard queries, zero trusted input changes, fixed access expiry, and Timeout after expiry.

Save each phase before changing mounted state. Keep contaminated controls invalid rather than weakening their assertions.
Owner: test automation owner unknown. Next action: implement and inspect both profile bindings before scheduling their clean repeat.

### RW-REMOTE-NO-STUBS

Purpose: prepare the same observations for an authorized UAT target without local response replacements.
Setup: remote mode, private credential environment variables, inspected target-specific setup actions, and actual portal permissions.
Record the real deployment identities and available effective-setting evidence. Mark missing deployment or policy evidence unknown.
Use the actual identity, catalog, entitlements, business responses, and embedded module bundles from the target.
The runner must register no route interception and seed no browser storage in remote mode.

```gherkin
Feature: Observe an authorized remote portal without local substitutions
  @RW-REMOTE-NO-STUBS
  Scenario: RW-REMOTE-NO-STUBS preserves the selected environment's actual boundaries
    Given the authorized portal user can sign in to the declared remote target
    And inspected setup actions identify the actual Cashflow Blotter workspace
    When the driver signs in through the target's actual authentication service
    And the driver completes the configured read-only setup actions
    And the driver records the timing preflight and mounted applications
    Then the runner registers zero request interception routes
    And the runner performs zero storage-seeding operations
    And the measured document's timeOrigin equals its baseline value
    And retained main-frame navigation and page-replacement event counts each equal zero
    And data grid ".ag-root-wrapper" in the Cashflow Blotter workspace is visible
    And retained claim metadata identifies the observed issuance and independent credential deadlines
    And unavailable effective configuration sources and deployment hashes remain unknown
    And the report makes no thirty-minute timeout or deployment-parity claim without matching evidence
```

Reading order:

1. Inspect the remote target, selected actions, permissions, and deployment evidence within granted access.
2. Sign in and mount actual Blotter without local response, token, or storage substitutions.
3. Retain the preflight, module inventory, request identities, and explicit evidence limits.
4. Select a further timing profile only when its observed deadline and isolation preconditions hold.

Required assertion binding: `real-world/runner.mjs --case RW-REMOTE-NO-STUBS --config FILE` with remote mode.
Inspection status: `UNVERIFIED`. Actual result: **NOT_RUN**. This definition does not claim live UAT access or execution.

Concrete remote setup component type, identity, and scope remain unavailable. These gaps block specification readiness for remote setup.
Owner: unknown environment owner. Next action: provide authorized target settings and retain the first actual remote observation.

## Frozen regression aliases

The frozen intake contains seven proposed scopes. This table links their current definitions without changing the intake bytes.
The [frozen intake](intake.md) binds Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`.
Its SHA-256 is `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`.

| Frozen alias | Current canonical cases | Scope and evidence limit |
| --- | --- | --- |
| [TC-01](intake.md#L263) | [E2E-04](#e2e-04), [E2E-09](#e2e-09), [E2E-10](#e2e-10) | Pending, rapid, and keyboard Extend. Each preserves its own assertion chain. |
| [TC-02](intake.md#L264) | [E2E-05](#e2e-05) | Rejected Extend and retry. No broader rejection policy is added. |
| [TC-03](intake.md#L265) | [E2E-07](#e2e-07), [PROBE-NATURAL-IMMEDIATE](#probe-natural-immediate), [PROBE-DELAYED-REFRESH](#probe-delayed-refresh) | Natural suspension, immediate recovery, and delayed delivery are separate conditions. The delayed probe does not establish natural freezing. |
| [TC-04](intake.md#L266) | [E2E-21](#e2e-21) | Missing-refresh observation only. The complete proposed natural-suspension variant and its acceptance policy remain unavailable. |
| [TC-05](intake.md#L267) | [E2E-20](#e2e-20), [REVIEW-F03A](#review-f03a), [REVIEW-F03B](#review-f03b), [REVIEW-F03-CONTROL](#review-f03-control) | The browser checks expired credentials. Race cases model revocation through an adapter. Live global revocation remains unverified. |
| [TC-06](intake.md#L268) | [E2E-07](#e2e-07), [PROBE-NATURAL-IMMEDIATE](#probe-natural-immediate) | Visible and hidden controls retain separate credential and lifecycle conditions. |
| [TC-07](intake.md#L269) | [E2E-22](#e2e-22) | Current evidence compares empty workspace descriptors. Populated restoration and application-edit restoration remain unverified. |

## Execution binding

The [case mapping](evidence/canonical-gherkin-20261021/case-mapping.json) links each executable binding to its canonical heading.
It preserves the retained test revisions. It does not change executable assertions or historical result files.

```yaml
execution_status: NOT_RUN
repository_id: mfe-base
repository_revision: 6e34da31961eb6bce4ef6c3daea83a2f7bd48e85
test_revision: 7a504c13a8d51bb52af5cc89bd4af88d1988da94
environment_identity: Documentation synchronization; no new execution
actual_results: null
retained_execution_refs:
  - evidence/minor-branch-rerun-20261020/browser-manifest.json
  - evidence/code-review-refresh-20261021/summary.json
```

**`NOT_RUN` above describes documentation synchronization.** It does not replace the retained case outcomes.
Each case links its actual result and exact source revision.
Review diagnostics characterize adverse behavior. Their runner passes do not convert unmet intended assertions into passing acceptance.

## Facts, inferences, and unresolved questions

The [scope request](evidence/minor-branch-rerun-20261020/user-request.txt) requires background recovery and considers broader renewal deferrals.
The [latest implementation clarification](evidence/code-review-refresh-20261021/clarification.json) explains debounce, expiry, and logout cancellation.
It changes no business policy. Requirement candidate version 4 and the frozen intake remain unchanged.

Production frequency, actual deployment settings, and downstream authorization remain unverified.
Touch activity and cross-origin activity remain outside the retained assertions.
Missing-refresh recovery policy and populated workspace restoration remain unresolved.
Owner: unknown business owner. Next action: define these outcomes before assigning acceptance verdicts to observation cases.

## Issue 1 correction regressions: 24 October 2026

These cases extend [REVIEW-F01](#review-f01) with replacement credentials and later recovery.
Definition version: `1`. Level: controlled Home, Timeout, reducer, and Axios integration in JSDOM.
Intent: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), candidate requirement version 4.
The [stage inputs](evidence/active-cutoff-fix-20261024/inputs.json) bind the original source and authorized correction.
The [candidate source binding](evidence/active-cutoff-fix-20261024/setup/source-binding.json) identifies the working implementation.
These cases do not replace the original browser [E2E-06](#e2e-06).

Actor: the Jest driver. Access, refresh, expiry, acquisition, and recovery use the [review glossary](#current-branch-review-cases).
The controlled clock starts at `2026-09-21T00:00:00Z`.
The adapter returns synthetic JWT credentials. It does not call a live identity provider.
Each case clears storage, aborts pending requests, restores the adapter, and restores timers after execution.

### REVIEW-F01-RECOVERY

Title: replace expired refresh credentials and retain later manual recovery.
Setup: start visible Home with 15-minute access. Hide and restore Home immediately to acquire refresh token R.
Token R expires four hours after the clock starts. Each successful extension issues 15-minute access.
The adapter returns replacement refresh token R2 when the initial refresh expires.
R2 differs from R and expires four hours after its fixture construction.

```gherkin
Feature: Preserve active access and later recovery
  Scenario: REVIEW-F01-RECOVERY
    Given the controlled session has valid access and refresh token R
    When the driver completes 23 ten-minute activity cycles with five-second extension delays
    Then exactly 23 extension requests complete
    And the installed access expiry exceeds token R's expiry
    When the driver advances to token R's expiry
    Then exactly two refresh-acquisition requests have occurred
    And the second acquisition body contains the current access token
    And installed refresh token equals R2 and differs from R
    And the installed access token and access expiry remain unchanged
    And the Timeout dialog is absent and isOnLogout equals false
    When the driver advances one additional second
    Then logout and relogin request counts both equal zero
    And the session workspace remains present
    When the driver advances to the retained access expiry
    Then the Timeout dialog is present and Extend is enabled
    When the driver selects Extend and the adapter returns valid access token B
    Then exactly one relogin request carries refresh token R2
    And installed access token equals B
    And the Timeout dialog is absent and logout request count equals zero
```

Assertions: [integrated regression](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L542).
Retained execution: [focused Jest result](evidence/active-cutoff-fix-20261024/unit/focused-result.json).
Limit: synthetic credentials and controlled time establish these integration predicates only.
Owner: unknown application owner. Next action: inspect the unchanged [browser boundary assertions](#e2e-06) and matching candidate execution.

### REVIEW-F01-MANUAL

Title: preserve access renewed immediately before the initial refresh expiry.
Setup: start the same 15-minute access and four-hour refresh fixture.
Hide Home, acquire refresh token R, and restore Home at minute 239 using the suspended-clock control.
The manual relogin response issues access valid through minute 254.
The next acquisition returns refresh token R2, which expires at minute 479.

```gherkin
Feature: Preserve manual renewal near the refresh boundary
  Scenario: REVIEW-F01-MANUAL
    Given Home returns at minute 239 with expired access and usable refresh token R
    When the driver selects Extend and relogin succeeds
    Then the Timeout dialog is absent
    And the installed access expiry equals start time plus 254 minutes
    When the driver advances one minute and one additional second
    Then exactly two refresh-acquisition requests have occurred
    And exactly one relogin request has occurred
    And installed refresh token equals R2 and differs from R
    And installed access token equals the successful manual response token
    And isOnLogout equals false and the Timeout dialog is absent
    And logout request count equals zero and the session workspace remains present
```

Assertions: [manual-boundary regression](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L637).
Retained execution: [focused Jest result](evidence/active-cutoff-fix-20261024/unit/focused-result.json).
Limit: suspension is simulated. No natural browser freeze or downstream authorization is established.
Owner: unknown application owner. Next action: retain this assertion when reviewing later session changes.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Delayed browser probe](#probe-delayed-refresh) and [controlled recovery](#review-delayed-hide). | Required recovery remains unmet. Current runner passes include the known failure. | unknown application owner | Correct recovery, then rerun the intended assertions. |
| [Active cutoff](#review-f01), [race before sign-in](#review-f03a), and [race after sign-in](#review-f03b). | Two distinct regression causes can terminate usable sessions. | unknown application owner | Review targeted corrections and repeat the paired comparisons. |
| [Contradictory response diagnostic](#e2e-12). | Production contract acceptance cannot be inferred. | unknown service owner | Confirm the response contract before treating this diagnostic as acceptance. |
| [Missing-refresh observation](#e2e-21) and [workspace observation](#e2e-22). | Policy and populated-state outcomes remain unverified. | unknown business owner | Define expectations and populated fixtures before assigning acceptance results. |

## Sources

| Source ID | Locator | Exact revision or identity | Authority and limits |
| --- | --- | --- | --- |
| SRC-session-active-cutoff-fix-request-20261024 | [Exact user request](evidence/active-cutoff-fix-20261024/user-request.txt) and [stage inputs](evidence/active-cutoff-fix-20261024/inputs.json). | User message, 24 October 2026; exact hashes in stage inputs. | Authorizes issue 1 correction and E2E comparison. It supplies no deployment approval. |
| SRC-session-robot-modules-20261021 | [Current case map](evidence/robot-case-modules-20261021/case-mapping.json), [offline checks](evidence/robot-case-modules-20261021/offline-checks.json), and [Browser discovery](evidence/robot-case-modules-20261021/browser-discovery.json). | Test engine `975af64c55303ee4a138968813ef4e85570f96d2`. | Harness organization and interface checks only. No new business execution. |
| SRC-session-canonical-inputs-20261021 | [Inputs and hashes](evidence/canonical-gherkin-20261021/inputs.json), [mapping](evidence/canonical-gherkin-20261021/case-mapping.json), and [validation](evidence/canonical-gherkin-20261021/validation.json). | Definition version 1; Workbench rule commit `1acd009`. | Authoring provenance only. No new test execution or acceptance approval. |
| SRC-session-minor-inventory-20261020 | [Inventory](evidence/minor-branch-rerun-20261020/case-inventory.json) and [retained assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot). | Test engine `7a504c13a8d51bb52af5cc89bd4af88d1988da94`; source SHA-256 `94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984`. | Inspected test expectations. They do not establish approved business policy. |
| SRC-session-branch-refresh-20261021 | [Current review inputs](evidence/code-review-refresh-20261021/inputs.json), [execution setup](evidence/code-review-refresh-20261021/execution-setup.json), and [reconciliation](evidence/code-review-refresh-20261021/summary.json). | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; runtime `6d4c37c839b99d14ea41fd936da1a36cda526b17`. | Current local source and controlled execution. Production behavior remains unverified. |
| Requirement candidate version 4 | [Criteria](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Git `d6adcff452f1329d99528f0f7e8a6450a27ddc8c`; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`. | Candidate intent; pending human review. No new waiver or publication. |
| Frozen intake | [Original task](intake.md) and [regression aliases](#frozen-regression-aliases). | Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. | Preserved proposed scopes. Current case definitions appear only in this catalog. |

## Session ownership regressions: 25 October 2026

These cases verify session isolation with actual Home, reducers, service calls, and Axios interceptors.
The controlled adapter holds responses. It does not establish provider revocation or PROD frequency.
Each case uses fifteen-minute access and refresh expiry after one second.
Home starts visible. Its refresh-expiry callback starts acquisition after that second.
Synthetic credentials contain subject, issuance, and expiry claims. Storage and timers reset between cases.
Assertions: [sessionOwnership.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx).
Execution: [seven failed-to-passed changes and two passing controls](evidence/minor-fixes-20261025/issue-1/summary.json).
The [commit binding](evidence/minor-fixes-20261025/issue-1/commit-binding.json) identifies exact implementation bytes.

### OWN-01

```gherkin
Feature: Session ownership
  Scenario: OWN-01 Discard stale success before fresh login
    Given Home has started session A refresh acquisition
    When the user logs out
    And session A refresh succeeds before session B login
    Then refresh state remains empty
    When session B login succeeds
    Then session B has no session A refresh credential
```

### OWN-02

```gherkin
Feature: Session ownership
  Scenario: OWN-02 Discard stale success after fresh login
    Given Home has started session A refresh acquisition
    When the user logs out
    And session B login succeeds
    And session A refresh succeeds
    Then session B access remains installed
    And refresh state contains no session A credential
```

### OWN-03

```gherkin
Feature: Session ownership
  Scenario: OWN-03 Discard stale invalid-token error
    Given Home has started session A refresh acquisition
    When the user logs out
    And session B login succeeds
    And session A refresh fails with TOKEN_INVALID_EXPIRED
    Then session B access remains installed
    And no stale error message is installed
```

### OWN-04

```gherkin
Feature: Session ownership
  Scenario: OWN-04 Discard success from login-pending work
    Given Home has started session A refresh acquisition
    When fresh login starts
    Then the previous refresh credential is cleared
    When another acquisition starts before login completes
    And session B login succeeds
    And the login-pending acquisition succeeds
    Then session B access remains installed
    And refresh state remains empty
```

### OWN-05

```gherkin
Feature: Session ownership
  Scenario: OWN-05 Discard error from login-pending work
    Given Home has started session A refresh acquisition
    When fresh login starts
    And another acquisition starts before login completes
    And session B login succeeds
    And the login-pending acquisition fails with TOKEN_INVALID_EXPIRED
    Then session B access remains installed
    And refresh state remains empty
    And no stale error message is installed
```

### OWN-06

```gherkin
Feature: Session ownership
  Scenario: OWN-06 Accept ordinary access rotation
    Given Home has started session A refresh acquisition
    When an activity extension rotates session A access
    And the pending refresh succeeds
    Then the rotated access remains installed
    And the returned refresh credential is installed
```

### OWN-07

```gherkin
Feature: Session ownership
  Scenario: OWN-07 Preserve current-session invalidation
    Given Home has started session A refresh acquisition
    When that current-session request fails with TOKEN_INVALID_EXPIRED
    Then access and refresh state are cleared
    And the error message is "Expired Session, please login again."
```

### OWN-08

```gherkin
Feature: Session ownership
  Scenario: OWN-08 Capture ownership before asynchronous dispatch
    Given Home has valid session A access
    When acquisition starts and logout runs without an asynchronous yield
    And the acquisition succeeds
    Then access and refresh state remain empty
```



## Minor correction browser cases: 25 October 2026

> **Run these cases after each matching correction. Passing local cases cannot establish PROD configuration parity.**
> Owner: Codex for execution; application owner remains unknown.
> Evidence: [authorized request](evidence/minor-fixes-20261025/user-request.txt) and [runner plan](evidence/minor-fixes-20261025/setup/browser-rerun-plan.json).

These cases extend the existing [ownership](#review-f03b) and [delayed recovery](#review-delayed-scheduled) definitions.
The [task-owned assertions](evidence/minor-fixes-20261025/setup/sessionRenewal.minor-fixes.cjs.snapshot) retain every original E2E assertion.
Native Edge uses an isolated profile and real wall-clock time. Each case saves results and screenshots immediately.
Held delivery controls the race. It cannot establish production frequency or natural freezing.

### FIX-OWNERSHIP-BROWSER-SUCCESS

Definition version: 1. Level: native browser and actual local authentication service.
Intent: reject ended-session refresh credentials under [REVIEW-F03B](#review-f03b).
Setup: use the natural local profile. Refresh lifetime exceeds the existing three-hour reuse threshold.
Assertions: `assertStaleRefreshSuccessIsIsolated` in the [retained extension](evidence/minor-fixes-20261025/setup/sessionRenewal.minor-fixes.cjs.snapshot).

```gherkin
Feature: Reject refresh credentials from an ended session
  Scenario: Fresh login receives its own refresh credentials after stale delivery
    Given session A has usable access in the authenticated portal
    When the actor hides the portal and holds its actual refresh response before browser delivery
    And the actor returns to the portal and completes explicit Logout
    And the actor signs in to create session B
    And the actor releases session A's held refresh response
    Then session B's access credential remains installed
    And the authenticated portal remains visible
    When the actor hides and restores the portal
    Then session B sends its own refresh acquisition request
    And the actual service returns usable session-B refresh credentials
    And the portal's protected validation succeeds with installed session-B access
```

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-staleSuccess-20261025T114442/artifacts/stale-refresh-success-isolation-1792928690586/result.json). Scope: `NATIVE_BROWSER`.

### FIX-OWNERSHIP-BROWSER-ERROR

Definition version: 1. Level: native browser and actual local authentication service.
Intent: ended-session errors cannot clear the fresh session under [REVIEW-F03B](#review-f03b).
Assertions: `assertStaleRefreshErrorIsIsolated` in the [retained extension](evidence/minor-fixes-20261025/setup/sessionRenewal.minor-fixes.cjs.snapshot).

```gherkin
Feature: Reject authentication errors from an ended session
  Scenario: Fresh login survives an ended session's delayed rejection
    Given session A has usable access in the authenticated portal
    When the actor hides the portal and holds its refresh request before service dispatch
    And the actor returns to the portal and completes explicit Logout
    And the actor signs in to create session B
    And the actor sends session A's held request to the actual service
    Then the service returns HTTP 401 for ended session A
    When the actor delivers that response to the browser
    Then session B's access credential remains installed
    And the authenticated portal remains visible
    When the actor hides and restores the portal
    Then session B completes its own refresh acquisition
    And the portal's protected validation succeeds with installed session-B access
```

Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-staleError-20261025T114505/artifacts/stale-refresh-error-isolation-1792928715555/result.json). Scope: `NATIVE_BROWSER`.

### FIX-DELAYED-BROWSER-SCHEDULED

Definition version: 1. Level: native browser and actual local authentication service.
Intent: [REVIEW-DELAYED-SCHEDULED](#review-delayed-scheduled), [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166), and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173).
Assertions: `assertDelayedScheduledRefreshRecovery` in the [retained extension](evidence/minor-fixes-20261025/setup/sessionRenewal.minor-fixes.cjs.snapshot).
Setup: use the fast local profile. Access lifetime is one minute. Acquisition starts 25 seconds before expiry.

```gherkin
Feature: Recover after delayed scheduled refresh delivery
  Scenario: Pending acquisition permits manual recovery after access expiry
    Given visible Home has usable access and no refresh credential
    When Home starts its scheduled refresh acquisition
    And the actor holds the actual successful refresh response before browser delivery
    And current access expires
    Then the Timeout prompt remains visible
    And Extend is disabled while acquisition remains pending
    And explicit Logout remains enabled
    When the actor delivers the refresh response one second after access expiry
    Then Extend becomes enabled
    When the actor selects Extend and holds its actual renewal request
    Then the Timeout prompt remains visible while renewal is pending
    When the actual service completes renewal with usable access
    Then the prompt closes exactly once
    And the portal's protected validation succeeds with installed renewed access
```

This shortened control does not replace [E2E-07](#e2e-07), which requires 30 real minutes of hidden time.
Current candidate `c42e760`: [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-delayed-20261025T093649/artifacts/delayed-scheduled-refresh-recovery-1792921019457/result.json). Scope: `NATIVE_BROWSER`.
The three added browser cases remain outside the original nineteen business-case totals.

### OWN-09

```gherkin
Feature: Session ownership
  Scenario: OWN-09 Replace pending acquisition across login generations
    Given Home has started session A refresh acquisition
    When fresh login starts with session A access still stored
    And another acquisition starts
    Then a second request starts without sharing the ended generation
    And the previous request signal is aborted
```

## Pending renewal regressions: 25 October 2026

These cases use actual Home, Timeout, service calls, reducers, and Axios interceptors with a controlled deferred adapter.
The fixture uses a fake clock, thirty-second access, and four-hour refresh credentials.
Each case clears storage and restores timers and the adapter.
The closure spy counts calls that close Timeout.
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx).
Execution: [twelve failed-to-passed changes and one passing control](evidence/minor-fixes-20261025/issue-2/candidate-summary.json).
The [final binding](evidence/minor-fixes-20261025/issue-2/commit-binding.json) records implementation and test revisions.

### PEND-01

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-01 Wait for actual manual renewal
    Given Timeout has a usable refresh credential and zero closures
    When the user selects Extend
    And the adapter holds the relogin response
    Then Timeout remains visible with zero closures
    When relogin returns usable access
    Then that access is installed
    And Timeout closes exactly once
```

### PEND-02

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-02 Retry after transport failure
    Given Timeout has a usable refresh credential
    When Extend fails with a retryable HTTP 503 response
    Then Timeout remains visible
    And Extend becomes available again
    When the user retries and relogin returns usable access
    Then the new access is installed
    And Timeout closes exactly once
```

### PEND-03

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-03 Reject missing renewal access
    Given Timeout has a usable refresh credential
    When Extend returns HTTP 200 without an access header
    Then previous access and its expiry remain unchanged
    And Timeout remains visible with zero closures
    And Extend remains available for retry
    When the user retries and relogin returns usable access
    Then the returned access and its expiry are installed
    And Timeout closes exactly once
```

### PEND-04

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-04 Reject malformed renewal access
    Given Timeout has a usable refresh credential
    When Extend returns HTTP 200 with access header "not-a-jwt"
    Then previous access and its expiry remain unchanged
    And Timeout remains visible with zero closures
    And Extend remains available for retry
    When the user retries and relogin returns usable access
    Then the returned access and its expiry are installed
    And Timeout closes exactly once
```

### PEND-05

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-05 Reject expired renewal access
    Given Timeout has a usable refresh credential
    When Extend returns HTTP 200 with access expiry equal to the current wall clock
    Then previous access and its expiry remain unchanged
    And Timeout remains visible with zero closures
    And Extend remains available for retry
    When the user retries and relogin returns usable access
    Then the returned access and its expiry are installed
    And Timeout closes exactly once
```

### PEND-06

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-06 Reject access without issuance data
    Given Timeout has a usable refresh credential
    When Extend returns HTTP 200 with future access expiry but no issuance claim
    Then previous access and its expiry remain unchanged
    And Timeout remains visible with zero closures
    And Extend remains available for retry
    When the user retries and relogin returns usable access
    Then the returned access and its expiry are installed
    And Timeout closes exactly once
```

### PEND-07

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-07 Share rapid manual activation
    Given Timeout has a usable refresh credential
    When the user activates Extend three times while its response is held
    Then exactly one relogin request starts
    And Timeout remains visible until usable access arrives
```

### PEND-08

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-08 Allow explicit Logout during manual renewal
    Given Timeout has a usable refresh credential
    And Extend has one held relogin response
    When the user selects Logout
    Then the relogin request signal is aborted
    When the existing one-second logout delay ends
    Then access and refresh state are cleared
    And late renewal cannot restore the session
```

### PEND-09

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-09 Recover after scheduled late delivery
    Given Home has valid access and no refresh credential
    When scheduled acquisition starts before access expiry
    And the adapter holds its response across access expiry
    Then Timeout remains visible
    And logout has not started
    When acquisition returns a usable refresh credential
    Then Extend becomes available
    When Extend returns usable access
    Then access is installed
    And Timeout closes exactly once
```

### PEND-10

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-10 Protect fresh login from delayed Logout
    Given Timeout belongs to session A
    When the user selects Logout
    And session B login succeeds before the one-second logout delay ends
    And the old logout delay ends
    Then session B access remains installed
    And the old callback does not close session B state
```

### PEND-11

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-11 Allow explicit Logout during acquisition
    Given Home acquisition is pending when access expires
    And Timeout is visible
    When the user selects Logout
    Then the acquisition request signal is aborted
    When the existing one-second logout delay ends
    Then access and refresh state are cleared
    And late acquisition cannot restore refresh state
```


### PEND-12

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-12 Recheck recovery expiry before sending renewal
    Given Timeout rendered an available Extend button with a usable refresh credential
    When wall-clock time moves beyond the refresh recovery cutoff without running timers
    And the user activates that rendered Extend button
    Then no relogin request starts
    And no successful prompt closure is recorded
```

### PEND-13

```gherkin
Feature: Pending renewal and recovery
  Scenario: PEND-13 Keep the existing fallback after failed acquisition
    Given acquisition is pending when access expires
    And Timeout is visible without usable refresh credentials
    When acquisition fails with a retryable HTTP 503 response
    And the existing one-second logout delay ends
    Then exactly one logout request starts
    And no relogin request starts
    And access and refresh state are cleared
    And Timeout closes exactly once
```


## Delivery confidence cases: 26 October 2026

Test assertions match MFE Base commit `b8d4f1b837c6388452fbdc540f311257e805f932`.
Runtime bytes remain identical to `c42e7609c4e14eb53de32702e4bd3424a223988a`.
Definition version: 1. These cases refine the [current delivery request](evidence/delivery-confidence-20261026/user-input.md#exact-user-input).
The prior catalog bytes remain in the [preserved snapshot](evidence/delivery-confidence-20261026/unit/canonical-cases-before.md.snapshot).
The [draft criteria](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md) preserve source lineage and authority limits.
The [assertion mapping](evidence/delivery-confidence-20261026/unit/traceability.json) binds definitions, source, predicates, and results separately.

### Delivery fixture and observation points

The actor is an authenticated portal operator. The controlled adapter supplies service responses without provider execution.
Ownership cases use fifteen-minute initial access, one-second refresh expiry, and twenty-minute replacement access.
Pending-renewal cases use thirty-second initial access and four-hour refresh credentials.
A fake clock starts at `2026-10-25T00:00:00Z`. The existing recovery cutoff precedes refresh expiry by two seconds.
Shared-client cases start at `2026-10-26T00:00:00Z`. Their access and refresh lifetimes are sixty seconds and four hours.
Synthetic credentials contain `sub`, `iat`, and `exp`. Their signatures are placeholders.
The store, local storage, request count, response promise, and prompt-closure spy provide separate observation points.
Each case clears storage and restores adapters. Component cases also restore timers and visibility state.
Workspace cases use actual Home validation, dispatchers, and reducers. Empty container lists require no catalog entitlement.
The tests mock analytics. Shared-client cases replace transport only.
[DEL-06](#del-06) and [DEL-07](#del-07) hold the adapter beyond the real sixty-second Axios timeout.
These cases verify component settlement. The controlled adapter omits native transport timeout behavior.
The cancellation case uses the public Axios service with an `AbortSignal` and no replacement request.
No current UI gesture establishing final cancellation was demonstrated. The exported service boundary is directly exercised.

### DEL-01

Entra login clears refresh before completion. Test level: controlled component integration.
Criterion: [DC-AC-01](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-01).
Assertions: [sessionOwnership.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx#L299).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-01
    Given Home has session A access and its previous refresh credential
    When the operator starts Entra sign-in through authentication version 3
    Then refresh state is empty before the held login response completes
    And session A access remains installed while login is pending
    When login returns session B access
    Then session B access is installed
    And refresh state remains empty
```

### DEL-02

Newest fresh login survives stale login success. Test level: controlled component integration.
Criterion: [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02).
Assertions: [sessionOwnership.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx#L312).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-02
    Given two version 2 sign-in requests overlap
    When the newer request installs twenty-minute session B access
    And the older request returns session A access
    Then access and persisted access equal session B access
    And access expiry equals the session B expiry
    And refresh state and error state are empty
```

### DEL-03

Newest fresh login survives stale login rejection. Test level: controlled component integration.
Criterion: [DC-AC-02](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-02).
Assertions: [sessionOwnership.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionOwnership.test.tsx#L312).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-03
    Given two version 2 sign-in requests overlap
    When the newer request installs twenty-minute session B access
    And the older request rejects with HTTP 401 and TOKEN_INVALID_EXPIRED
    Then access and persisted access equal session B access
    And access expiry equals the session B expiry
    And refresh state and error state are empty
```

### DEL-04

Stale manual success cannot replace fresh login. Test level: controlled component integration.
Criterion: [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03).
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L287).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-04
    Given Timeout has a usable refresh credential and zero successful closures
    And session A manual renewal is held
    When replacement login returns twenty-five-minute session B access
    And the held renewal returns session A renewed access
    Then access and persisted access equal session B access
    And expiry equals the session B expiry
    And refresh state and error state are empty
    And successful closure count equals zero
    And logout request count equals zero
```

### DEL-05

Stale manual rejection cannot end fresh login. Test level: controlled component integration.
Criterion: [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03).
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L287).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-05
    Given Timeout has a usable refresh credential and zero successful closures
    And session A manual renewal is held
    When replacement login returns twenty-five-minute session B access
    And the held renewal rejects with HTTP 401 and TOKEN_INVALID_EXPIRED
    Then access and persisted access equal session B access
    And expiry equals the session B expiry
    And refresh state and error state are empty
    And successful closure count equals zero
    And logout request count equals zero
```

### DEL-06

Held manual renewal survives the recovery deadline. Test level: controlled component integration.
Criterion: [DC-AC-04](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-04).
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L315).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-06
    Given the operator has selected Extend while refresh credentials are usable
    And the relogin response is held
    When the controlled clock advances four hours
    Then Timeout remains visible with zero successful closures
    And logout request count equals zero
    When the response returns access issued now and expiring twenty minutes later
    Then returned access and its expiry are installed
    And Timeout disappears with exactly one successful closure
    And logout request count equals zero
```

### DEL-07

Late failed manual renewal uses the expiry fallback. Test level: controlled component integration.
Criterion: [DC-AC-05](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-05).
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L331).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-07
    Given the operator has selected Extend while refresh credentials are usable
    And the relogin response is held
    When the controlled clock advances four hours
    And the held request rejects with HTTP 503
    And the existing one-second logout delay ends
    Then relogin request count equals one
    And logout request count equals one
    And access and refresh state are empty
    And successful closure count equals one for logout completion
```

### DEL-08

Current manual rejection still clears authentication. Test level: controlled component integration.
Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).
Assertions: [sessionPending.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx#L344).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-08
    Given Timeout has a usable refresh credential
    When the operator selects Extend
    And the current relogin request rejects with HTTP 401 and TOKEN_INVALID_EXPIRED
    Then access and refresh state are empty
    And persisted access is absent
    And the error equals "Expired Session, please login again."
    And the fixture displays "Signed out"
    And successful renewal closure count equals zero
```

### DEL-09

Ordinary protected request preserves headers and data. Test level: controlled component integration.
Criterion: [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07).
Assertions: [sessionCompatibility.test.ts](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L71).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-09
    Given the shared client has session access and operator identity "operator-a"
    When the caller requests "/api/portfolio/positions"
    Then the authorization header equals current access
    And the userId header equals "operator-a"
    And the content type equals "application/json"
    When transport returns HTTP 200 and position "position-a" with amount 17
    Then the caller receives that position data and HTTP 200
    And access and refresh state remain unchanged
    And loading equals false
```

### DEL-10

Access rotation preserves a pending protected response. Test level: controlled component integration.
Criterion: [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08).
Assertions: [sessionCompatibility.test.ts](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L85).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-10
    Given a protected positions request remains pending
    When an activity extension installs access expiring after 120 seconds
    And the original positions request returns position "position-a"
    Then the original caller receives that position and HTTP 200
    And the rotated access remains installed
    And the previous refresh credential remains installed
```

### DEL-11

Current ordinary error remains visible without logout. Test level: controlled component integration.
Criterion: [DC-AC-07](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-07).
Assertions: [sessionCompatibility.test.ts](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L101).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-11
    Given the shared client has current access and refresh credentials
    When the positions request rejects with HTTP 401 and "Position data unavailable"
    Then the caller receives a rejected response with HTTP 401
    And the global error equals "Position data unavailable"
    And access and refresh state remain unchanged
    And loading equals false
```

### DEL-12

Current protected expiry still clears authentication. Test level: controlled component integration.
Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).
Assertions: [sessionCompatibility.test.ts](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L112).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-12
    Given the shared client has current access and refresh credentials
    And persisted access equals current access
    When the positions request rejects with HTTP 401 and TOKEN_INVALID_EXPIRED
    Then the caller receives a rejected response with HTTP 401
    And access and refresh state are empty
    And persisted access is absent
    And the error equals "Expired Session, please login again."
```

### DEL-13

Excluded endpoints retain their existing error behavior. Test level: controlled component integration.
Criterion: [DC-AC-09](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-09).
Assertions: [sessionCompatibility.test.ts](../../repos/ui/mfe-base/src/hooks/service/sessionCompatibility.test.ts#L124).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario Outline: DEL-13
    Given the shared client has current credentials and error notice "Existing notice"
    When the <endpoint> request rejects with HTTP 401 and TOKEN_INVALID_EXPIRED
    Then the caller receives a rejected response with HTTP 401
    And access and refresh state remain unchanged
    And the global error remains "Existing notice"
    And loading equals false

    Examples:
      | endpoint                   |
      | /api/analytics/event       |
      | /api/sse/events            |
      | /api/auth/v2/sso/logout     |
```

### DEL-14

Final cancellation clears the current loading state. Test level: controlled component integration.
Criterion: [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10).
Assertions: [cancellationPreservation.test.ts](../../repos/ui/mfe-base/src/hooks/service/cancellationPreservation.test.ts#L13).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

Final correction: [eight original browser predicates pass](evidence/ut-remediation-20261027/final-cancellation-browser/comparison.json).
The initial setup failure is separate. The successful rerun preserves the original case assertions.

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-14
    Given one current-session positions request has started with an AbortSignal
    And loading equals true
    And no replacement request starts
    When the caller aborts that signal
    Then the caller receives ERR_CANCELED
    And current access remains unchanged
    And error state remains empty
    And loading equals false
```

Browser assertion: [public Service cancellation and PageLoader checks](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/deliveryConfidence.cjs#L7).
Main browser result: [loader clears](evidence/delivery-confidence-20261026/browser/main/main-cancelledLoader-20261026T153205/case-summary.json).
Candidate browser result: [loader remains visible](evidence/delivery-confidence-20261026/browser/candidate-headless/candidate-cancelledLoader-20261026T153330/case-summary.json).
The browser uses a held local diagnostic route. It fabricates no response.
Its direct public API invocation does not establish an ordinary user journey or PROD frequency.

### DEL-15

Stale workspace selection preserves the current workspace. Test level: controlled component integration.
Criterion: [DC-AC-11](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-11).
Assertions: [workspacePreservation.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L27).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-15
    Given workspaces "workspace-a" and "workspace-b" have empty container lists
    And "workspace-a" is selected
    When a tab event selects unavailable index 99
    Then "workspace-a" remains selected
    And the workspace identifiers remain "workspace-a" and "workspace-b"
```

### DEL-16

Deleting the first selected workspace selects the next workspace. Test level: controlled component integration.
Criterion: [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12).
Assertions: [workspacePreservation.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L36).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-16
    Given workspaces "workspace-a" and "workspace-b" have empty container lists
    And "workspace-a" is selected
    When the operator deletes "workspace-a"
    Then the workspace list contains only "workspace-b"
    And "workspace-b" is selected
    And stored workspace descriptors equal the remaining workspace
```

### DEL-17

Deleting a later selected workspace retains previous selection. Test level: controlled component integration.
Criterion: [DC-AC-12](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-12).
Assertions: [workspacePreservation.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L45).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-17
    Given workspaces "workspace-a" and "workspace-b" have empty container lists
    When the operator selects "workspace-b"
    And the operator deletes "workspace-b"
    Then the workspace list contains only "workspace-a"
    And "workspace-a" is selected
```

### DEL-18

Unavailable saved workspaces retain the blank fallback. Test level: controlled component integration.
Criterion: [DC-AC-13](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-13).
Assertions: [workspacePreservation.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/workspacePreservation.test.tsx#L56).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-18
    Given saved workspace "unavailable" references an unavailable tile
    And catalog entries and entitlements are empty
    When Home validates the saved workspace
    Then workspace validation reports ready
    And exactly one workspace remains
    And its identifier differs from "unavailable"
    And its label equals "Workspace 1"
    And its container list is empty
    And that blank workspace is selected
```

### BROWSER-SHARING-PENDING

Test level: browser and local service. Definition version: 1.
Criterion: [DC-AC-14](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-14).
Source: [existing supporting sharing case](#e2e-08).
The fixture holds an already dispatched activity extension. It avoids the original case's zero-dispatch failure.
The actual shortened BFF fixture uses sixty-second access and 144-second refresh lifetimes.
The second activity waits 6,500 milliseconds after the first request is held.
Assertions: [supplemental browser source](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/deliveryConfidence.cjs#L54).
Main result: [sharing failure](evidence/delivery-confidence-20261026/browser/main/main-sharingPending-20261026T153220/case-summary.json).
Candidate result: [sharing failure](evidence/delivery-confidence-20261026/browser/candidate-headless/candidate-sharingPending-20261026T153346/case-summary.json).
The first request-count assertion fails before response adoption and protected validation.
Those later assertions remain unexecuted in both comparisons.

```gherkin
Feature: MFE Base delivery preservation
  Scenario: BROWSER-SHARING-PENDING
    Given one activity extension is already pending in the local portal
    When another mouse event reaches the dispatcher after its five-second scheduling delay
    Then activity extension request count remains one
    And the original request remains uncanceled
    When the original response returns usable access
    Then that returned access enters session state
    And protected validation succeeds
```

### DEL-19

Retain loading during overlapping cancellation. Test level: controlled service integration. Definition version: 1.
Criterion: [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15).
Assertions: [cancellationPreservation.test.ts](../../repos/ui/mfe-base/src/hooks/service/cancellationPreservation.test.ts#L37).
Results: [final candidate cases](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).
This safety control protects against clearing another current request's loader during a cancellation correction.

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-19
    Given current-session positions request A has an AbortSignal
    And replacement positions request B is pending
    And loading equals true
    When the caller aborts request A
    Then request A returns ERR_CANCELED
    And loading remains true
    And access remains unchanged
    And error state remains empty
    When request B returns HTTP 200 and position "replacement-position"
    Then request B returns that position and HTTP 200
    And loading equals false
```


### DEL-20

Preserve recovery after a scheduled acquisition callback runs one millisecond late.
Test level: controlled Home, Timeout, service, and reducer integration. Definition version: 1.
Criterion: [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16).
Earlier timing observation: [REVIEW-F02](#review-f02).
Assertions: [sessionTimingPreservation.test.tsx](../../repos/ui/mfe-base/src/pages/Home/common/sessionTimingPreservation.test.tsx#L58).
Main execution: [matching baseline case](evidence/delivery-confidence-20261026/unit/main-late-timer/results.json).
Candidate execution: [complete final suite](evidence/delivery-confidence-20261026/unit/candidate-final-verified/results.json).
The [independent paired observations](evidence/delivery-confidence-20261026/independent-review/late-timer-candidate-observation.json) retain acquisition and logout events.

The fake clock starts at `2026-10-26T00:00:00Z` with the document visible.
Access and existing refresh both expire sixty seconds later. This is a declared synthetic near-expiry state.
The controlled Axios adapter returns a four-hour replacement refresh immediately after acquisition.
The test asserts identical initial credential values and expiry before clock displacement.
[Candidate observations](evidence/delivery-confidence-20261026/unit/candidate-final-verified/case-observations/DEL-20.json) retain initial, pre-expiry, expiry, and final state.
[Main observations](evidence/delivery-confidence-20261026/unit/main-final-preservation/case-observations/DEL-20.json) use the same executable test.
The [final default-lifetime variant](evidence/ut-remediation-20261027/final-timer-control/comparison.json) passes ten unchanged assertions.
Its final observations match retained main. Extend availability is an observation in that variant.
The test replaces no Home, Timeout, interceptor, dispatcher, or reducer behavior.
Cleanup restores the adapter, timers, visibility, and storage.
This case measures the controlled component chain. It does not measure natural browser jitter or production frequency.

```gherkin
Feature: MFE Base delivery preservation
  Scenario: DEL-20
    Given visible Home has access and existing refresh expiring after sixty seconds
    And acquisition is scheduled twenty-five seconds before access expiry
    When wall-clock time advances one millisecond without executing timers
    And the scheduled callback runs after another 35,000 milliseconds
    And initial expiry occurs after another 25,000 milliseconds
    And the existing one-second logout interval ends
    Then the fixture does not display "Signed out"
    And exactly one refresh acquisition has started
    And the replacement four-hour refresh remains installed
    And the manual Extend control was enabled at expiry
    And the expiry prompt remains visible
    And the logout request count equals zero
```

### DEL-21

Retain loading when a silent request settles beside pending work.
Test level: controlled shared-client integration. Definition version: 1.
Scope: [corrected patch](evidence/ut-remediation-20261027/proposal-v3.patch), based on `b8d4f1b837c6388452fbdc540f311257e805f932`.
Criteria: [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10) and [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15).
The proposal adds assertions without removing or changing existing assertions.
The [source binding](evidence/ut-remediation-20261027/proposal-v3-binding.json) identifies the changed test and runtime bytes.
Results: [complete corrected execution](evidence/ut-remediation-20261027/full-proposal-03/results.json).

```gherkin
Feature: Preserve shared-client loading during correction
  Scenario: DEL-21
    Given session A has one pending loading-enabled positions request
    And loading equals true
    When a second request starts with show-loading equal to "false"
    Then loading remains true
    When the silent request returns HTTP 200 and position "silent-position"
    Then its caller receives that response
    And loading remains true
    When the caller aborts the first request
    Then the first request returns ERR_CANCELED
    And loading equals false
    And access remains "session-a"
    And error state remains empty
```

### DEL-22

Retain the new session's loading when an ended-session request is canceled.
Test level: controlled shared-client integration. Definition version: 1.
Scope: [corrected patch](evidence/ut-remediation-20261027/proposal-v3.patch), based on `b8d4f1b837c6388452fbdc540f311257e805f932`.
Criterion: [DC-AC-15](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-15).
Ownership controls: [DEL-02](#del-02) and [DEL-03](#del-03).
The [source binding](evidence/ut-remediation-20261027/proposal-v3-binding.json) identifies the changed test and runtime bytes.
Results: [complete corrected execution](evidence/ut-remediation-20261027/full-proposal-03/results.json).

```gherkin
Feature: Preserve shared-client loading during correction
  Scenario: DEL-22
    Given session A has one pending loading-enabled positions request
    When session A ends and session B becomes current
    And session B starts a loading-enabled request
    Then loading equals true
    When the caller aborts session A's request
    Then that request returns ERR_CANCELED
    And loading remains true
    And access remains "session-b"
    And error state remains empty
    When session B's request returns HTTP 200 and position "current-position"
    Then its caller receives that response
    And loading equals false
```

### DEL-23

Clear loading when a supported response transformer throws without request configuration.
Test level: controlled shared-client integration. Definition version: 1.
Criterion: [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10).
Scope: [corrected patch](evidence/ut-remediation-20261027/proposal-v3.patch), based on `b8d4f1b837c6388452fbdc540f311257e805f932`.
Assertions: [preserved test source](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/cancellationPreservation.test.ts#L146).
Comparison: [paired probe](evidence/ut-remediation-20261027/configless-error-comparison.json).
The first proposal failed this new assertion. The [red execution](evidence/ut-remediation-20261027/configless-error-red/execution.json) preserves that failure.
The [complete corrected execution](evidence/ut-remediation-20261027/full-proposal-03/execution.json) passes this assertion and all original tests.
Unavailable request identity prevents ownership attribution. The fallback preserves the previous global cleanup behavior.
No inspected business caller uses this transformer. Production frequency remains unknown.

```gherkin
Feature: Preserve loading cleanup for supported response transforms
  Scenario: DEL-23
    Given session A starts a loading-enabled positions request
    And its response transformer throws Error with message "Invalid positions payload"
    When the adapter returns HTTP 200 and position "position"
    Then the caller receives a rejection
    And error state contains "Invalid positions payload"
    And loading equals false
    And access remains "session-a"
    When the caller starts another positions request without the failing transformer
    Then its caller receives HTTP 200 and position "position"
    And exactly two requests have reached the adapter
    And loading equals false
```

### DEL-24

Release completed loading work when response interpretation throws.
Test level: controlled shared-client integration. Definition version: 1.
Criterion: [DC-AC-10](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-10).
Assertions: [preserved test](evidence/ut-remediation-20261027/proposal-v3-sources/src/hooks/service/cancellationPreservation.test.ts#L169).
Comparison: [baseline and trial](evidence/ut-remediation-20261027/response-handler-comparison.json).
Failure: [trial assertion](evidence/ut-remediation-20261027/response-handler-red/execution.json).
Passing result: [complete execution](evidence/ut-remediation-20261027/full-proposal-03/execution.json).

Setup: session A has valid access. The adapter returns malformed `userInfo` for authentication validation.

1. Send validation through the actual shared client.
2. Observe the parser rejection.
3. Send a successful positions request through the same client.

| Result type | Expected or observed loading |
| --- | --- |
| Intended correction | Completed requests leave no loading entry. A parser rejection preserves authentication. |
| Original baseline | Loading remains true after parsing fails. The next successful request clears it. |
| Trial v2 | Loading remains true after parsing fails and after the next successful request. |
| Corrected v3 | Loading becomes false after rejection and remains false after subsequent success. |

The adapter deliberately returns malformed data. No production malformed response or incident frequency is established.
The correction also improves immediate cleanup beyond the baseline's delayed recovery.
The `finally` wrapper guarantees release of completed work. It preserves the parser rejection.

```gherkin
Feature: Release loading after response interpretation fails
  Scenario: DEL-24
    Given session A starts authentication validation through the shared client
    And the adapter returns HTTP 200 with malformed userInfo equal to "{"
    When the actual response handler interprets that response
    Then the caller receives SyntaxError
    And loading equals false
    And access remains "session-a"
    When the caller sends a positions request that returns HTTP 200 and position "position"
    Then its caller receives that position and HTTP 200
    And exactly two requests have reached the adapter
    And loading equals false
```

## Final-candidate coverage completion: 27 October 2026

The [latest instruction](evidence/user-input-20261027-complete-four-checks.txt) authorizes these verification cases.
The definitions extend existing criteria. They introduce no new production duration or activity policy.

### FOUR-AC4-BROWSER

Title: retain the portal through four controlled hours of accepted activity.
Level: controlled browser integration with the actual MFE, root composition, DOM, store, and HTTP interceptors.
Intent: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), requirement candidate version 5.
Actor: Playwright drives headless Edge. The fixture controls browser time and authentication responses.
Setup: perform local sign-in through the actual form and retain its noncredential response fields.
Return synthetic access credentials valid for fifteen minutes and initial refresh credentials valid for two hours.
The response fixture replaces refresh credentials after their expiry while current access remains usable.
The driver emits trusted mouse movement every ten controlled minutes and permits the existing five-second debounce.
All runtime source remains unchanged. Token verification and live identity-provider behavior are outside this controlled case.

1. Sign in through the rendered local portal form.
2. Pause the installed browser clock after setup.
3. Seed initial refresh through the exported shared service and its actual response interceptor.
4. Advance ten controlled minutes before each trusted mouse movement.
5. Run the debounce clock and wait for the successful extension response.
6. Continue until the controlled clock reaches exactly four hours from the assertion baseline.
7. Inspect authentication, prompt transitions, navigation, refresh replacement, and successful renewal counts.

```gherkin
Feature: Preserve accepted activity across elapsed session duration
  Scenario: FOUR-AC4-BROWSER
    Given the rendered portal has fifteen-minute access and two-hour initial refresh credentials
    And authentication responses issue usable credentials for the current controlled clock
    When accepted trusted mouse activity renews access before every access deadline
    And the controlled browser clock advances through exactly four hours
    Then each activity cycle completes a successful extension
    And current access remains usable
    And the initial refresh token expires within the interval
    And the portal installs a different usable refresh token
    And the portal records zero timeout prompt openings
    And the portal records zero additional fresh-login requests
    And the portal records zero logout or manual-relogin requests
    And the portal records zero additional main-frame navigations
    And the authenticated workspace remains visible
```

Assertions and retained execution: [controlled browser evidence](evidence/four-checks-20261027/ac4-browser/).
This case establishes the declared controlled predicates. It does not establish four hours of live BFF acceptance.
The [renewed coverage audit](11-behavior-traceability-20261027.md#original-criteria-observable-result-and-gap) identifies a missing criterion predicate.
Neither this Gherkin nor its runner directly asserts the absence of every fresh SSO prompt.
The passing execution therefore supports selected controls. Complete AC-4 coverage remains partial.

## Final coverage boundary cases: 27 October 2026

These cases add assertions around reachable guards. They change no runtime implementation.
Definitions use runtime commit `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303` and the [completion instruction](evidence/user-input-20261027-complete-four-checks.txt).
The [instrumented inventory](evidence/four-checks-20261027/coverage/coverage-analysis.json) identifies the initial gaps.
The [assertion source](../../repos/ui/mfe-base/src/components/Timeout/common/coverageBoundaries.test.tsx) isolates the actual Timeout controller.
Its service, context, dispatcher, and analytics collaborators are controlled doubles. JWT parsing, epoch operations, and timers remain actual.
The [Home assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx) retain their existing hook fixture and mocked acquisition service.
These tests establish their asserted controller outcomes. They establish no browser, transport, or production result.

### FOUR-COV-01

Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-01
    Given the actual Timeout controller receives refresh token "Bearer e30.ew==.test"
    When its actual JWT parser encounters malformed JSON
    Then Extend eligibility equals false
    And logout-start dispatch occurs exactly once with true
    When the existing one-second logout delay ends
    Then the logout collaborator is called exactly once
    And prompt closure occurs exactly once with false
```

### FOUR-COV-02

Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-02
    Given Timeout has usable refresh credentials and the current session epoch
    When its logout callback starts twice before the one-second delay ends
    Then logout-start dispatch occurs exactly once
    And no logout collaborator call occurs before that delay ends
    When the one-second delay ends
    Then the logout collaborator is called exactly once
    And prompt closure occurs exactly once
```

### FOUR-COV-03

Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-03
    Given the current Timeout logout callback has started its one-second delay
    When another session epoch replaces the current epoch
    And access becomes "session-b"
    And the old one-second delay ends
    Then the logout collaborator is not called
    And prompt closure does not occur
    And access remains "session-b"
```

### FOUR-COV-04

Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-04
    Given a callback belongs to an earlier rendered Timeout session
    When another session epoch becomes current
    And the retained logout callback runs
    Then the replacement session epoch does not change
    And logout-start dispatch does not occur
    And the logout collaborator is not called
    And prompt closure does not occur
```

### FOUR-COV-05

Criterion: [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-05
    Given Timeout starts one manual renewal with a controlled pending relogin promise
    And loading equals true
    When the Timeout controller unmounts
    And that relogin promise resolves successfully
    Then prompt closure does not occur
    And the logout collaborator is not called
    And the relogin collaborator has exactly one call
```

### FOUR-COV-06

Criterion: [DC-AC-03](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-03).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-06
    Given Timeout starts one manual renewal with a controlled pending relogin promise
    When another session epoch replaces the current epoch
    And access becomes "session-b"
    And the old relogin promise resolves successfully
    Then prompt closure does not occur
    And the logout collaborator is not called
    And access remains "session-b"
```

### FOUR-COV-07

Criterion: [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08).

```gherkin
Feature: Preserve Home acquisition boundaries
  Scenario: FOUR-COV-07
    Given visible Home has access expiring after fifteen minutes
    And its refresh token contains a JSON object without an exp property
    When Home mounts
    Then no acquisition call occurs immediately
    When 875000 milliseconds pass
    Then exactly one acquisition collaborator call occurs
    And the expiry prompt remains closed
    And access remains "access-token"
```

### FOUR-COV-08

Criterion: [DC-AC-08](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-08).

```gherkin
Feature: Preserve Home acquisition boundaries
  Scenario: FOUR-COV-08
    Given visible Home has access expiring after fifteen minutes
    And its refresh token contains the JSON value null
    When Home mounts
    Then no acquisition call occurs immediately
    When 875000 milliseconds pass
    Then exactly one acquisition collaborator call occurs
    And the expiry prompt remains closed
    And access remains "access-token"
```

### FOUR-COV-09

Criterion: [DC-AC-16](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-16).

```gherkin
Feature: Preserve Home acquisition boundaries
  Scenario: FOUR-COV-09
    Given visible Home has scheduled acquisition twenty-five seconds before access expiry
    When document visibility becomes hidden without delivering its visibility notification
    And 875000 milliseconds pass
    Then no acquisition collaborator call occurs
    And the expiry prompt remains closed
    And access remains "access-token"
```

### FOUR-COV-10

Criterion: [DC-AC-06](evidence/delivery-confidence-20261026/unit/acceptance-criteria.md#dc-ac-06).

```gherkin
Feature: Preserve Timeout boundary guards
  Scenario: FOUR-COV-10
    Given the current Timeout logout callback has started its one-second delay
    And logout-start dispatch occurred exactly once
    When the Timeout controller unmounts
    And the one-second delay ends without another session epoch
    Then the logout collaborator is called exactly once
    And prompt closure does not occur
```
