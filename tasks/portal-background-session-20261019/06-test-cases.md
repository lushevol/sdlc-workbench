---
artifact_kind: test-case
id: TEST-session-canonical-20261021
version: 19
status: draft
owner: unknown
source_refs:
  - SRC-comprehensive-renewal-20261028
  - SRC-session-review-e2e-20261028
  - SRC-session-document-standard-20261028
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

Current invocation: [comprehensive renewal and security request](evidence/user-input-20261028-comprehensive-renewal.txt).
Read the [new expansion](#comprehensive-renewal-expansion), [use cases](03-use-cases-renewal.md), and [security review](07-security-review-renewal.md).
Earlier execution results retain their original source identities.
The [focused review probes](#focused-review-e2e-probes-28-october-2026) define nine proposed diagnostics.

> **Critical conclusions: Action required**
>
> **Production remains blocked by missing release evidence. Both earlier runtime regressions are corrected locally.**
> Action: complete the [release closure inventory](10-issue-catalog.md#readiness-conditions).
> Consequence: passing local checks cannot establish production suitability. Owner: unknown release owner.
> Evidence: [current unit execution](evidence/four-checks-20261027/coverage/test-only-final-2/execution.json) and [current assessment](10-release-readiness.md#execution-evidence).
>
> **The stale dialog blocks a valid replacement session in the controlled browser flow.**
> Action: establish caller applicability and correct dialog ownership when applicable. Owner: unknown application owner.
> Consequence: visible recovery actions cannot recover that session. Evidence: [actual comparison](evidence/review-e2e-20261028/final-focused/browser-summary.json).
>
> Existing activity failures retain their recorded backlog disposition.
> The [final release handoff](10-release-readiness.md) controls the current release scope.
> The [delivery stage](10-release-readiness.md#execution-evidence) records the new verification and independent reviews.
> Source: [current high-priority request](evidence/delivery-confidence-20261026/user-input.md#exact-user-input).
>
> The [unit-test request](evidence/delivery-confidence-20261026/ut-release-principle-user-input-20261027.md#exact-user-input) prefers unchanged application code.
> Genuine failures required minimal runtime correction. The pre-remediation candidate assertions remain unchanged.
> The [renewed review](evidence/renewed-review-20261027/codex/review.md#test-assertion-history) identifies changed main-baseline assertions.
> [DEL-21](#del-21), [DEL-22](#del-22), [DEL-23](#del-23), and [DEL-24](#del-24) protect the correction.
> The [current stage](10-release-readiness.md#execution-evidence) records its source and execution state.

Assessed candidate: `e0030f5cf920b715f5831faf7df86cb9789b6d0f`. Its runtime matches `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303`.
The [current browser reconciliation](evidence/four-checks-20261027/e2e/reconciliation.json) records all 27 completed final-runtime cases.
Historical results below retain their original source identities.
Prior original business cases: **13 passed, 6 failed, 0 blocked**.
[E2E-12](#e2e-12) is diagnostic; [E2E-21](#e2e-21) and [E2E-22](#e2e-22) are observations.
These three cases remain outside the nineteen business-case totals.
Seven failures changed to passed: [E2E-04](#e2e-04), [E2E-05](#e2e-05), [E2E-07](#e2e-07), [E2E-09](#e2e-09), [E2E-10](#e2e-10), [E2E-13](#e2e-13), and [E2E-17](#e2e-17).
The [historical comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) binds each result and its execution scope.



**🧭 Choose the evidence you need:**

| Read this | Purpose | Execution boundary |
| --- | --- | --- |
| [Current review cases](#current-branch-review-cases) | Compare active cutoff, stale credentials, timer behavior, and delayed recovery. | Controlled checks at the selected old and new revisions. |
| [Browser case catalog](#catalog-navigation) | Read the 22 retained browser case definitions. | [Current comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json); historical results remain below each case. |
| [Supplemental browser probes](#supplemental-browser-probes) | Separate delayed delivery from immediate natural recovery. | Two distinct investigations with separate controls. |
| [Robot and JavaScript source](#current-robot-and-javascript-source) | Find the executable module for one browser case. | Modularized suite business execution remains **NOT_RUN**. |
| [Real-world session cases](#real-world-session-cases) | Check configured lifetimes, actual Blotter inactivity, and remote execution boundaries. | Hidden measurement **FAILED** its fixed-expiry assertion. Schedule, mismatch detection, and shortened-expiry controls passed. |
| [Current correction report](10-release-readiness.md#execution-evidence) | Read both fixes and remaining failures. | Source and local execution evidence do not establish release approval. |

## Objective and traceability

Use this file as the single current source for readable test steps and assertions.
Definition version 1 applies to every case below. Stable case IDs remain independent of executable function names.
The [execution report](10-release-readiness.md#execution-evidence) summarizes results and links these definitions.
The [prior review](10-issue-catalog.md#findings) explains earlier change impact and network sequences.
Existing outcomes retain their original implementation and test bindings. New Blotter observation cases have separate execution bindings.

The requirement remains [candidate version 5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).
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
The [environment report](10-release-readiness.md#execution-evidence) records versions, visibility controls, substitutions, and omitted boundaries.

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
Finding: [F-01](10-issue-catalog.md#findings).

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
Finding: [F-02](10-issue-catalog.md#findings).
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
Finding: [F-03A](10-issue-catalog.md#findings).
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
Finding: [F-03B](10-issue-catalog.md#findings).
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
Finding mapping: [F-03C](10-issue-catalog.md#findings).
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
Intent: [required background-recovery scope](10-release-readiness.md#current-task-state) and successful manual renewal under [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176).
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
Intent: [required background-recovery scope](10-release-readiness.md#current-task-state) and [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176).
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
Finding: [resolved F-04](10-issue-catalog.md#findings).
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

| Source ID | Locator | Exact revision | SHA-256 | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SRC-session-review-e2e-20261028 | [Preserved source](evidence/user-input-20261028-review-e2e-proof.txt) | `user-message-20261028` | `c2e4d53fc0f9a4ae6af1fbeda1aa1bde263f5c413e04e784799279e49a94c0a3` | unknown; User authorization for review verification and procedure updates. It grants no business approval. |
| SRC-session-document-standard-20261028 | [Preserved source](evidence/user-input-20261028-sdlc-document-standard.txt) | `user-message-20261028` | `219a53e653ac81e918d7124c9404c2f535650d73a8ae5744059c6599f91195e6` | unknown; User authorization for document naming, content, and template checks only. |
| SRC-ut-release-principle-20261027 | [Preserved source](evidence/delivery-confidence-20261026/ut-release-principle-user-input-20261027.md) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `f46bdf9bef9aac054f1c42d41e670cfd0d78415f7a46005d6b4d45f9db1d5022` | unknown; User instruction for passing unit tests and correction constraints; no deployment approval. |
| SRC-mfe-base-delivery-confidence-20261026 | [Preserved source](evidence/delivery-confidence-20261026/user-input.md) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `1836615b609b9fe74b19e72665423ae19b9bcb153fae10cdf1ab0b3abbf05047` | unknown; Preserved delivery-review request; no assertion of zero impact or acceptance. |
| SRC-session-sequential-minor-fixes-20261025 | [Preserved source](evidence/minor-fixes-20261025/user-request.txt) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `925b69f64daa287132fcf8d1f8229e23c18087d4c4adab78507e2c6796e4e8af` | unknown; User authorization for the two scoped corrections and sequential verification. |
| SRC-session-active-cutoff-fix-request-20261024 | [Preserved source](evidence/active-cutoff-fix-20261024/user-request.txt) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `87fc6619df147d4395323b336e40d37700e9ad292ca343c8dae432afaed0758d` | unknown; User authorization for the bounded cutoff correction and comparison. |
| SRC-session-robot-modules-20261021 | [Preserved source](evidence/robot-case-modules-20261021/case-mapping.json) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `25a0e2e8acbff6b1fdd266cfcb159c19ec2a02541f7524f88f330494ea7c0fab` | unknown; Generated module mapping; business execution and acceptance remain separate. |
| SRC-session-canonical-inputs-20261021 | [Preserved source](evidence/canonical-gherkin-20261021/inputs.json) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `b33f2c75eb5a87d3e39eaf4aed83921512415eac475f1bd63f39265abe1ecae7` | unknown; Generated definition provenance and source identities; no business approval. |
| SRC-session-minor-inventory-20261020 | [Preserved source](evidence/minor-branch-rerun-20261020/case-inventory.json) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `9584c7462c48f21cc1dae2c730c3bec786a1a27cc17aedad94392ccb6e4e86bd` | unknown; Retained case inventory; approved intent and matching execution remain separate. |
| SRC-session-branch-refresh-20261021 | [Preserved source](evidence/code-review-refresh-20261021/inputs.json) | `2346134ab60601f3c46f893ae3fc67d83b59d8ea` | `cc66ba3f40c33931b37e9093701494715fa17b3e16b32a209e64c180ee938618` | unknown; Inspected source identities for the earlier review; production applicability is unproved. |

Historical requirement version 4 is preserved in the [exact definition snapshot](evidence/knowledge-status-20261026/REQ-active-session-renewal-v4.md#acceptance-criteria).
Its SHA-256 is `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`.
The frozen intake remains linked through [intake.md](intake.md). Historical source and execution scopes remain explicit in each case.

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
The [renewed coverage audit](09-coverage.md#final-candidate-coverage-27-october-2026) identifies a missing criterion predicate.
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

## Focused review E2E probes: 28 October 2026

The [current instruction](evidence/user-input-20261028-review-e2e-proof.txt) authorizes actual verification of review issues and tangible impact.
These proposed diagnostics investigate [review findings](10-issue-catalog.md#findings). They do not add approved business acceptance criteria.
The [case audit](evidence/review-e2e-20261028/case-audit.json) records exact source locators, predictions, and reachability limits.

Current definition version: 2. The [version 1 snapshot](evidence/review-e2e-20261028/canonical-review-v1.md.snapshot) preserves the original proposed controls and predicates.
Its SHA-256 is `ed8dc6aeae5cf811341399f60c2be52779747d3591cb214c651961d4a4e276ca`.
Version 2 uses actual elapsed time and separates distinct-user hypotheses from same-user session observations.
Historical case sections above retain their definitions and execution bindings.

### Review E2E fixture and observation points

| Item | Defined state or observation point |
| --- | --- |
| Comparison | Baseline `f025513f696476a9cc8162681410cbd21e029bcb`; candidate `e0030f5cf920b715f5831faf7df86cb9789b6d0f`. |
| Actor | One synthetic local portal user with permission to open Home. The current runs use this same identity. |
| Sessions A and B | Separate local BFF login results for that user. Different credentials do not establish different user identities. |
| Browser | Installed headless Edge executes the actual exported source, React components, reducers, and shared Axios handlers. |
| Public API action | The driver imports `@fm/base` and calls exported Service or LoginUtil functions inside the page. |
| In-place login | Public `Service.postService` sends fresh login while Home remains mounted. Production caller reachability remains unknown. |
| Direct replacement | Public `LoginUtil.setAuthorization` installs B access without fresh-login interception. Production caller reachability remains unknown. |
| Home | Portal tablist with accessible name `workspaces`. |
| Timeout dialog | Dialog named `Your session has been expired`; title ID `timeout-dialog-title`. |
| Extend and Logout | Buttons `Extend_Btn` and `Logout_Btn` inside the Timeout dialog. |
| PageLoader | Rendered test ID `MicroWebUI_base_Loader_Page`; pointer checks inspect the element above the target center. |
| Credential observations | Compare hashed live `Hooks.getHooks().store` values and captured response access. Never retain raw tokens. |
| Acquisition | `POST /api/auth/v2/sso/refreshtoken`; each hold states whether service dispatch or browser delivery is delayed. |
| Renewal | `POST /api/auth/v2/sso/relogin`; correlate requests, provider decisions, installed access, and dialog states separately. |
| Validation | A read-only `/api/auth/v2/sso/validate` request uses installed access and checks HTTP status plus JSON `result`. |
| Clock | Actual elapsed browser time; local access normally lasts 60 seconds. No controlled-clock advance occurs. |
| Synthetic credentials | Opaque headers or JWTs with omitted claims exercise validation. Changed JWT payloads have invalid signatures. |
| Isolation | Separate browser contexts and output folders. Release held routes and close owned contexts after retention. |

The [Timeout UI](../../repos/ui/mfe-base/src/components/Timeout/index.tsx) defines the dialog and button identities.
The [public exports](../../repos/ui/mfe-base/src/root.tsx) define Service, Hooks, and LoginUtil.
The [runner inventory](evidence/review-e2e-20261028/runner-inventory.json) identifies available setup sources and dependencies.
The [source binding](evidence/review-e2e-20261028/source-binding.json) identifies exported comparison sources. Served-byte evidence must match the executed build.

Assertion bindings: [main review runner](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/reviewE2e.mjs) and [loader probe](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/reviewFindings.cjs).
Contract assertions: [malformed-response runner](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/reviewContractE2e.cjs) and [near-deadline delivery control](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/reviewDeadlineControl.cjs).
Its `run` function binds opaque and missing-`iat` controls to [REVIEW-E2E-02](#review-e2e-02).
The near-deadline control completes the usable-access assertion in [REVIEW-E2E-17](#review-e2e-17).
The longer response hold instead reaches timeout before delivery. It cannot verify delivered-token rejection.
The [result matrix](evidence/review-e2e-20261028/results.json) retains twenty primary observations across nine paired review cases.
Execution status is case-specific. Proposed variants remain `NOT_RUN` without matching retained assertions and execution.
Retain DOM states, credential hashes, correlated requests, screenshot hashes, and exact assertion-source identity for each executed variant.

### REVIEW-E2E-01

Finding: [REVIEW-01](10-issue-catalog.md#review-01). Purpose: test the replacement-session dialog block.
Sessions A and B belong to the same local user. B must install within the old Logout delay.
The in-place public API login is a controlled consumer action. A reachable production UI trigger remains unknown.

```gherkin
@REVIEW-E2E-01
Feature: Observe dialog ownership after replacement login
  Scenario: Same-user replacement login completes during the old Timeout logout delay
    Given session A has expired access and the Timeout dialog is visible
    When the actor clicks the button labeled "Logout" inside the Timeout dialog
    And the driver completes same-user session B login through the public API
    Then B access installs within 1000 milliseconds of the Logout click
    When at least 1500 milliseconds pass after replacement completion
    Then candidate installed access remains B access
    And local BFF validation accepts that installed access
    And the candidate Timeout dialog remains visible
    And the candidate button "Extend_Btn" is disabled inside the Timeout dialog
    And the candidate button "Logout_Btn" is enabled inside the Timeout dialog
    When the actor clicks that enabled candidate Logout button
    And at least 1300 milliseconds pass
    Then the candidate Timeout dialog remains visible
    And candidate installed access remains B access
    And the baseline dialog and credential outcomes are retained separately
```

Tangible-impact predicate: valid replacement access remains behind a dialog with disabled Extend and an ineffective Logout action.
The run does not retain an assertion that no additional logout request starts.
Owner: unknown application owner. Next action: identify actual consumer reachability before assigning production impact.

### REVIEW-E2E-02

Finding: [REVIEW-02](10-issue-catalog.md#review-02). Purpose: compare unsupported renewal shapes with valid-response recovery.
Run opaque-access and missing-`iat` variants separately. The inspected local BFF normally supplies usable `iat` and `exp` claims.
Header substitution tests client validation. A modified JWT signature is invalid; provider occurrence remains unproved.

```gherkin
@REVIEW-E2E-02
Feature: Observe renewal response validation
  Scenario Outline: A controlled renewal returns an unsupported access shape
    Given session A has expired access and usable refresh credentials
    And the Timeout dialog is visible
    And the driver substitutes the renewal authorization header with "<shape>"
    When the actor clicks the button labeled "Extend" inside the Timeout dialog
    Then the real relogin response and substituted access hash are retained
    And the candidate does not install the substituted access
    And the candidate Timeout dialog remains visible
    And baseline installed-access and dialog outcomes are retained separately
    When the driver removes the response substitution
    And the actor clicks the enabled candidate Extend button
    Then candidate installed access equals the valid local BFF response access
    And the candidate Timeout dialog is hidden
    And local BFF validation accepts the installed access

    Examples:
      | shape |
      | opaque-access |
      | jwt-without-iat |
```

The candidate valid control retries the same prompt. Baseline uses a fresh context when the malformed response closes that prompt.
Tangible impact is limited to the substituted response. The separate valid control cannot prove recovery within a broken baseline context.
Owner: unknown authentication owner. Next action: bind the deployed provider token contract before classifying rejection as a defect.

### REVIEW-E2E-03

Finding: [REVIEW-03](10-issue-catalog.md#review-03). Purpose: test recovery after failed in-place fresh login.
Source clears refresh when fresh login starts. Immediate automatic reacquisition can restore recovery before access expires.
This case records both transitions. It does not require failed recovery to obtain a passing diagnostic result.

```gherkin
@REVIEW-E2E-03
Feature: Observe failed replacement-login recovery
  Scenario: A controlled fresh login fails before session A expires
    Given session A has valid access A and usable refresh R_A
    And Home is visible
    When the driver sends an in-place fresh-login request through the public API
    And the driver returns controlled HTTP 401 for that login
    Then the failed request reaches the actual shared interceptor
    And the immediate access and refresh hashes are retained
    And local BFF validation checks the still-valid installed access
    And acquisition requests after refresh clearing are retained
    When actual time passes beyond A expiry
    Then the Timeout dialog appears with Extend enabled after automatic refresh reacquisition
    When the actor clicks the button labeled "Extend" inside the Timeout dialog
    Then local BFF validation accepts the resulting installed access
    And the Timeout dialog is hidden
    And Home is visible
```

Tangible impact requires failed recovery. Successful reacquisition and Extend leave the failed-recovery hypothesis unconfirmed for this fixture.
Owner: unknown application owner. Next action: identify an actual caller and compare its supported login-failure behavior.

### REVIEW-E2E-04

Finding: [REVIEW-04](10-issue-catalog.md#review-04). Purpose: separate same-user credential mixing from a distinct-user identity switch.
The executed control uses two sessions for one user. The distinct-user identity-switch hypothesis remains `NOT_RUN`.

```gherkin
@REVIEW-E2E-04
Feature: Observe direct same-user credential replacement
  Scenario: A public token utility installs B access while same-user A refresh can remain
    Given same-user session A has usable access A and refresh R_A
    And a separate raw local BFF login returns same-user access B
    When the driver calls public LoginUtil.setAuthorization with B access
    Then installed access differs from captured A access
    And the result retains whether refresh still equals R_A
    And baseline refresh retention is retained separately
    When the driver requests renewal through the public API
    Then the relogin outcome and resulting installed access hash are retained
    And local BFF validation checks the resulting installed access
    And final Home or Timeout visibility is retained
    And this same-user result does not verify a distinct-user identity switch
```

Distinct-user variant: install another user's B access, renew through retained R_A, and assert the resulting identity and visible impact.
That variant remains `NOT_RUN`. No supported direct-replacement caller or cross-user production occurrence is established.
Owner: unknown consumer owner. Next action: bind distinct test identities and an actual caller before testing the identity-switch claim.

### REVIEW-E2E-05

Finding: [REVIEW-05](10-issue-catalog.md#review-05). Purpose: test pending-acquisition controls and explicit failed settlement.
Hold acquisition before BFF dispatch. Release it with controlled HTTP 503 after actual access expiry.
This run does not assert natural Axios timeout behavior or an indefinite wait.

```gherkin
@REVIEW-E2E-05
Feature: Observe recovery while refresh acquisition is pending
  Scenario: Access expires while a held acquisition remains pending
    Given a public refresh acquisition request is held before local BFF dispatch
    When actual time passes beyond session A access expiry
    Then the candidate Timeout dialog is visible
    And the candidate button "Extend_Btn" is disabled inside the Timeout dialog
    And the candidate button "Logout_Btn" remains enabled inside the Timeout dialog
    When the driver releases acquisition with controlled HTTP 503
    And at least 1700 milliseconds pass
    Then the settled dialog, button states, and credential state are retained
    When the actor clicks Logout if the settled dialog remains available
    And at least 1400 milliseconds pass
    Then candidate Sign In controls are visible
    And candidate installed access is empty
    And baseline pending and settled states are retained separately
```

Tangible impact is the observed pending wait and final recovery route. Available Logout limits the blocking claim.
Owner: unknown application owner. Next action: use a separate lifecycle run for natural timeout or browser suspension claims.

### REVIEW-E2E-06

Finding: [REVIEW-06](10-issue-catalog.md#review-06). Purpose: compare missing-refresh-expiry fallback behavior.
Remove `exp` from a genuine refresh JWT through the public setter. This invalidates its signature.
Abort later acquisition to preserve the malformed fixture. The inspected local BFF does not issue this token shape.

```gherkin
@REVIEW-E2E-06
Feature: Observe fallback for an unusable refresh expiry
  Scenario: Access expires with a deliberately malformed refresh token
    Given session A has valid access and a modified refresh JWT without "exp"
    And later acquisition responses cannot replace that malformed refresh fixture
    When actual time passes beyond access expiry
    Then the candidate final Sign In controls are visible after fallback
    And candidate installed access becomes empty
    And final refresh state and correlated authentication requests are retained
    And the baseline dialog, Extend state, and installed access are retained separately
```

Tangible impact is sign-in fallback in the malformed fixture. No failure with valid local-provider refresh is established.
Owner: unknown authentication owner. Next action: bind provider guarantees and the intended malformed-credential policy.

### REVIEW-E2E-07

Finding: [REVIEW-07](10-issue-catalog.md#review-07). Purpose: test recovery after near-expiry mounting with usable refresh.
Use actual local login and refresh. Wait until access has about 20 seconds remaining.
Public `LoginUtil.setAuthorization('')` unmounts Home. Public setters then restore the saved real refresh and access.
Candidate retains usable refresh at remount. Baseline `SET_TOKEN` clears it and can start a replacement acquisition.
Keep that baseline precondition difference visible. It is not an equal usable-refresh-at-mount comparison.
The earlier 42-second login-response hold exercises another setup. It cannot satisfy this remount variant's predicates.

```gherkin
@REVIEW-E2E-07
Feature: Observe near-expiry remounting and completed recovery
  Scenario: A controlled public utility remounts Home with usable refresh near access expiry
    Given session A has genuine local BFF access and refresh
    When actual time passes until about twenty seconds of access remain
    And the driver calls public LoginUtil.setAuthorization with an empty string
    Then Home unmounts and the Sign In controls appear
    When the driver restores saved refresh through public LoginUtil.setRefreshToken
    And the driver restores saved access through public LoginUtil.setAuthorization
    Then Home remounts with access time remaining greater than zero and less than 25000 milliseconds
    And candidate refresh still equals the saved usable refresh
    And candidate acquisition count does not increase during the first 350 milliseconds after remount
    And baseline refresh clearing and replacement acquisition are retained separately
    When actual time passes until the Timeout dialog appears
    And the actor clicks the button labeled "Extend" inside the Timeout dialog
    Then local BFF renewal completes with usable access
    And candidate installed access equals the renewal response access
    And the candidate Timeout dialog is hidden
    And Home is visible
    And local BFF validation accepts the installed access
```

Tangible-impact test: completed recovery would disprove a recovery block for this controlled usable-refresh fixture.
Status remains `NOT_RUN` until this exact remount variant has matching retained execution.
Owner: unknown application owner. Next action: investigate natural mounting and missing-refresh conditions separately.

### REVIEW-E2E-12

Finding: [REVIEW-12](10-issue-catalog.md#review-12). Purpose: measure visible loader behavior after stale request cleanup.
Use a held public Service loading request. Return controlled HTTP 401 with `errorMessage` equal to `TOKEN_INVALID_EXPIRED`.
The actual error handler clears credentials and advances the epoch. Login mounting can publish later loading cleanup.
This auth-error route differs from the Timeout Logout hypothesis. Preserve that boundary beside the result.

```gherkin
@REVIEW-E2E-12
Feature: Observe loader cleanup after authentication invalidation
  Scenario: An expired loading request settles after its session epoch changes
    Given session A has valid access and visible Home
    And shared loading state equals false
    When the driver starts a public Service loading request and holds its response
    Then shared loading state equals true
    And PageLoader is rendered in the portal
    When the driver releases controlled HTTP 401 with errorMessage "TOKEN_INVALID_EXPIRED"
    Then the original request rejects
    And installed access becomes empty
    And the result retains immediate shared loading and PageLoader states
    When at least two actual seconds pass after settlement
    Then final Sign In visibility, shared loading state, and PageLoader visibility are retained
    And a hit test records whether PageLoader covers the Sign In input center
    And a trial pointer action records whether that Sign In control is actionable
    And persistent blocking is recorded only when final loader and pointer evidence both support it
    And baseline state transitions are retained separately
```

Tangible impact requires persistent pointer blocking. A transient state or registry return alone cannot establish it.
Owner: unknown application owner. Next action: compare this authentication-error flow with a separately identified stale-completion caller.

### REVIEW-E2E-17

Finding: [REVIEW-17](10-issue-catalog.md#review-17). Purpose: separate provider validation, response delivery, and returned-access usability.
Response-hold variant: obtain an actual BFF renewal response before refresh expiry, then hold browser delivery beyond that expiry.
Local returned access normally lasts 60 seconds. It can expire while the longer refresh deadline remains pending.
Rejecting already expired access can conform to the inspected client contract. Late delivery does not require unconditional acceptance.

```gherkin
@REVIEW-E2E-17
Feature: Observe renewal response delivery after the refresh deadline
  Scenario: Browser receives an earlier provider decision after refresh expiry
    Given session A has expired access and refresh usable before its recorded expiry
    And the Timeout dialog is visible
    When the actor clicks the button labeled "Extend" inside the Timeout dialog
    And the driver obtains the actual local BFF relogin decision before refresh expiry
    And the driver holds browser delivery until after that refresh expiry
    Then provider decision time, refresh deadline, and returned access expiry are retained
    And request timeout or cancellation before delivery is retained
    When the driver releases the held response
    Then the returned access usability at delivery is recorded
    And candidate installed access and Timeout state are retained
    And local BFF validation checks any resulting installed access
    And baseline response, credential, and UI outcomes are retained separately
```

Proposed usable-access assertion: if returned access remains valid, successful installation must close the dialog and pass BFF validation.
The observation runner does not require acceptance or rejection. `COMPLETED` identifies execution, not conformance.
A hold beyond Axios timeout can settle the request before delivery. Such a result cannot prove delivered-token validation.
Retain the pre-release route, credentials, and request outcome beside that boundary.

Proposed assertion variant: `EXPIRED_RETURNED_ACCESS_REJECTION`. Status: `NOT_RUN` until its direct predicates have matching retained execution.
This expectation comes from inspected client validation. It is not approved session policy.

```gherkin
@REVIEW-E2E-17-EXPIRED
Feature: Check the proposed expired-access response contract
  Scenario: An accepted renewal access token expires before browser delivery
    Given the local BFF accepted renewal before refresh expiry
    And returned access was usable when the provider responded
    And actual time now exceeds that returned access expiry
    And the correlated renewal request remains pending without timeout or cancellation
    When the driver delivers the held successful response
    Then candidate installed access does not equal the expired response access
    And the previous installed access hash remains unchanged
    And final Timeout visibility and both button states are retained
```

Keep dialog controls and final recovery visible. These source-derived diagnostics do not supply a business policy decision.
Request-hold variant: defer provider dispatch beyond refresh expiry, then retain the actual BFF rejection or acceptance.
The request-hold variant does not prove the response-hold variant. Keep their identities and outcomes separate.
Owner: unknown authentication owner. Next action: bind deployed provider policy before applying either result to deployment.

## Comprehensive renewal expansion

Definition version: 1 for every new RN case. Earlier definitions and results remain preserved.

> **Critical conclusions: A logout revocation gap is reproduced in the isolated BFF integration.**
> Action: review and correct revocation before security acceptance. Consequence: copied refresh credentials can remain usable.
> Owner: unknown service owner. Evidence: [security review](07-security-review-renewal.md#findings-and-actions).

The [request](evidence/user-input-20261028-comprehensive-renewal.txt) authorizes this expansion.
The [strategy](05-test-strategy-renewal.md) states its scope and finite coverage limits.
The [coverage record](09-renewal-coverage.md) separates definitions, assertions, source conformance, and execution.

### Renewal fixture and oracles

User A and User B are synthetic portal users with distinct session identifiers and entitlements.
WA, WB, and W-A/W-B identify fixture workspaces. A case states their permissions before each protected action.
Access credentials authorize protected requests. Refresh credentials authorize the service relogin operation.
The shell epoch identifies local session ownership. It does not establish server revocation.
Use isolated accounts, local services, and controlled responses. Never execute these attacks against production.
Record request ID, workspace ID, session owner, clock, endpoint, authorization result, and state transitions.
Replace real credentials with labels in exported evidence. Reset fixture accounts and close contexts after each case.
Abort owned operations, close sockets, and verify cleanup after each experiment. Keep policy-specific cleanup expectations separate.
A successful renewal requires usable returned access and protected validation. Dialog closure alone is insufficient.
UI controls use the source-defined timeout dialog and Extend or Logout buttons.
Runtime uniqueness remains unverified except within the three new browser probes.
See [workspace fixtures](evidence/comprehensive-renewal-20261028/workspace-transport-fixtures.json) and [component inventory](evidence/comprehensive-renewal-20261028/workspace-transport-components.json).
Source observations are regression checks. Proposed security invariants require applicable owner review.
Policy-open cases record observations. Their business acceptance remains blocked.
Case priorities are test-planning proposals. They do not replace recorded business backlog priorities.

### Expansion navigation

| Family | New definitions | Case links |
| --- | --- | --- |
| activity | 15 | [RN-A001](#rn-a001), [RN-A002](#rn-a002), [RN-A003](#rn-a003), [RN-A004](#rn-a004), [RN-A005](#rn-a005), [RN-A006](#rn-a006), [RN-A007](#rn-a007), [RN-A008](#rn-a008), [RN-A009](#rn-a009), [RN-A010](#rn-a010), [RN-A011](#rn-a011), [RN-A012](#rn-a012), [RN-A013](#rn-a013), [RN-A014](#rn-a014), [RN-A015](#rn-a015) |
| browser-contexts | 14 | [RN-D001](#rn-d001), [RN-D002](#rn-d002), [RN-D003](#rn-d003), [RN-D004](#rn-d004), [RN-D005](#rn-d005), [RN-D006](#rn-d006), [RN-D007](#rn-d007), [RN-D008](#rn-d008), [RN-D009](#rn-d009), [RN-D010](#rn-d010), [RN-D011](#rn-d011), [RN-D012](#rn-d012), [RN-D013](#rn-d013), [RN-D014](#rn-d014) |
| executed-renewal-probes | 3 | [RN-X001](#rn-x001), [RN-X002](#rn-x002), [RN-X003](#rn-x003) |
| failure | 12 | [RN-F001](#rn-f001), [RN-F002](#rn-f002), [RN-F003](#rn-f003), [RN-F004](#rn-f004), [RN-F005](#rn-f005), [RN-F006](#rn-f006), [RN-F007](#rn-f007), [RN-F008](#rn-f008), [RN-F009](#rn-f009), [RN-F010](#rn-f010), [RN-F011](#rn-f011), [RN-F012](#rn-f012) |
| lifecycle | 12 | [RN-H001](#rn-h001), [RN-H002](#rn-h002), [RN-H003](#rn-h003), [RN-H004](#rn-h004), [RN-H005](#rn-h005), [RN-H006](#rn-h006), [RN-H007](#rn-h007), [RN-H008](#rn-h008), [RN-H009](#rn-h009), [RN-H010](#rn-h010), [RN-H011](#rn-h011), [RN-H012](#rn-h012) |
| loading | 20 | [RN-Q001](#rn-q001), [RN-Q002](#rn-q002), [RN-Q003](#rn-q003), [RN-Q004](#rn-q004), [RN-Q005](#rn-q005), [RN-Q006](#rn-q006), [RN-Q007](#rn-q007), [RN-Q008](#rn-q008), [RN-Q009](#rn-q009), [RN-Q010](#rn-q010), [RN-Q011](#rn-q011), [RN-Q012](#rn-q012), [RN-Q013](#rn-q013), [RN-Q014](#rn-q014), [RN-Q015](#rn-q015), [RN-Q016](#rn-q016), [RN-Q017](#rn-q017), [RN-Q018](#rn-q018), [RN-Q019](#rn-q019), [RN-Q020](#rn-q020) |
| loop | 11 | [RN-L001](#rn-l001), [RN-L002](#rn-l002), [RN-L003](#rn-l003), [RN-L004](#rn-l004), [RN-L005](#rn-l005), [RN-L006](#rn-l006), [RN-L007](#rn-l007), [RN-L008](#rn-l008), [RN-L009](#rn-l009), [RN-L010](#rn-l010), [RN-L011](#rn-l011) |
| manual | 12 | [RN-M001](#rn-m001), [RN-M002](#rn-m002), [RN-M003](#rn-m003), [RN-M004](#rn-m004), [RN-M005](#rn-m005), [RN-M006](#rn-m006), [RN-M007](#rn-m007), [RN-M008](#rn-m008), [RN-M009](#rn-m009), [RN-M010](#rn-m010), [RN-M011](#rn-m011), [RN-M012](#rn-m012) |
| payload | 18 | [RN-P001](#rn-p001), [RN-P002](#rn-p002), [RN-P003](#rn-p003), [RN-P004](#rn-p004), [RN-P005](#rn-p005), [RN-P006](#rn-p006), [RN-P007](#rn-p007), [RN-P008](#rn-p008), [RN-P009](#rn-p009), [RN-P010](#rn-p010), [RN-P011](#rn-p011), [RN-P012](#rn-p012), [RN-P013](#rn-p013), [RN-P014](#rn-p014), [RN-P015](#rn-p015), [RN-P016](#rn-p016), [RN-P017](#rn-p017), [RN-P018](#rn-p018) |
| race | 20 | [RN-R001](#rn-r001), [RN-R002](#rn-r002), [RN-R003](#rn-r003), [RN-R004](#rn-r004), [RN-R005](#rn-r005), [RN-R006](#rn-r006), [RN-R007](#rn-r007), [RN-R008](#rn-r008), [RN-R009](#rn-r009), [RN-R010](#rn-r010), [RN-R011](#rn-r011), [RN-R012](#rn-r012), [RN-R013](#rn-r013), [RN-R014](#rn-r014), [RN-R015](#rn-r015), [RN-R016](#rn-r016), [RN-R017](#rn-r017), [RN-R018](#rn-r018), [RN-R019](#rn-r019), [RN-R020](#rn-r020) |
| security | 55 | [RN-S001](#rn-s001), [RN-S002](#rn-s002), [RN-S003](#rn-s003), [RN-S004](#rn-s004), [RN-S005](#rn-s005), [RN-S006](#rn-s006), [RN-S007](#rn-s007), [RN-S008](#rn-s008), [RN-S009](#rn-s009), [RN-S010](#rn-s010), [RN-S011](#rn-s011), [RN-S012](#rn-s012), [RN-S013](#rn-s013), [RN-S014](#rn-s014), [RN-S015](#rn-s015), [RN-S016](#rn-s016), [RN-S017](#rn-s017), [RN-S018](#rn-s018), [RN-S019](#rn-s019), [RN-S020](#rn-s020), [RN-S021](#rn-s021), [RN-S022](#rn-s022), [RN-S023](#rn-s023), [RN-S024](#rn-s024), [RN-S025](#rn-s025), [RN-S026](#rn-s026), [RN-S027](#rn-s027), [RN-S028](#rn-s028), [RN-S029](#rn-s029), [RN-S030](#rn-s030), [RN-S031](#rn-s031), [RN-S032](#rn-s032), [RN-S033](#rn-s033), [RN-S034](#rn-s034), [RN-S035](#rn-s035), [RN-S036](#rn-s036), [RN-S037](#rn-s037), [RN-S038](#rn-s038), [RN-S039](#rn-s039), [RN-S040](#rn-s040), [RN-S041](#rn-s041), [RN-S042](#rn-s042), [RN-S043](#rn-s043), [RN-S044](#rn-s044), [RN-S045](#rn-s045), [RN-S046](#rn-s046), [RN-S047](#rn-s047), [RN-S048](#rn-s048), [RN-S049](#rn-s049), [RN-S050](#rn-s050), [RN-S051](#rn-s051), [RN-S052](#rn-s052), [RN-S053](#rn-s053), [RN-S054](#rn-s054), [RN-S055](#rn-s055) |
| timing | 17 | [RN-B001](#rn-b001), [RN-B002](#rn-b002), [RN-B003](#rn-b003), [RN-B004](#rn-b004), [RN-B005](#rn-b005), [RN-B006](#rn-b006), [RN-B007](#rn-b007), [RN-B008](#rn-b008), [RN-B009](#rn-b009), [RN-B010](#rn-b010), [RN-B011](#rn-b011), [RN-B012](#rn-b012), [RN-B013](#rn-b013), [RN-B014](#rn-b014), [RN-B015](#rn-b015), [RN-B016](#rn-b016), [RN-B017](#rn-b017) |
| transports | 30 | [RN-T001](#rn-t001), [RN-T002](#rn-t002), [RN-T003](#rn-t003), [RN-T004](#rn-t004), [RN-T005](#rn-t005), [RN-T006](#rn-t006), [RN-T007](#rn-t007), [RN-T008](#rn-t008), [RN-T009](#rn-t009), [RN-T010](#rn-t010), [RN-T011](#rn-t011), [RN-T012](#rn-t012), [RN-T013](#rn-t013), [RN-T014](#rn-t014), [RN-T015](#rn-t015), [RN-T016](#rn-t016), [RN-T017](#rn-t017), [RN-T018](#rn-t018), [RN-T019](#rn-t019), [RN-T020](#rn-t020), [RN-T021](#rn-t021), [RN-T022](#rn-t022), [RN-T023](#rn-t023), [RN-T024](#rn-t024), [RN-T025](#rn-t025), [RN-T026](#rn-t026), [RN-T027](#rn-t027), [RN-T028](#rn-t028), [RN-T029](#rn-t029), [RN-T030](#rn-t030) |
| workspaces | 32 | [RN-W001](#rn-w001), [RN-W002](#rn-w002), [RN-W003](#rn-w003), [RN-W004](#rn-w004), [RN-W005](#rn-w005), [RN-W006](#rn-w006), [RN-W007](#rn-w007), [RN-W008](#rn-w008), [RN-W009](#rn-w009), [RN-W010](#rn-w010), [RN-W011](#rn-w011), [RN-W012](#rn-w012), [RN-W013](#rn-w013), [RN-W014](#rn-w014), [RN-W015](#rn-w015), [RN-W016](#rn-w016), [RN-W017](#rn-w017), [RN-W018](#rn-w018), [RN-W019](#rn-w019), [RN-W020](#rn-w020), [RN-W021](#rn-w021), [RN-W022](#rn-w022), [RN-W023](#rn-w023), [RN-W024](#rn-w024), [RN-W025](#rn-w025), [RN-W026](#rn-w026), [RN-W027](#rn-w027), [RN-W028](#rn-w028), [RN-W029](#rn-w029), [RN-W030](#rn-w030), [RN-W031](#rn-w031), [RN-W032](#rn-w032) |

### RN-A001

**Continuous mouse movement reaches the requested renewal target**

Use case: [UC-R01](03-use-cases-renewal.md#uc-r01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Continuous mouse movement reaches the requested renewal target
  @target @RN-A001
  Scenario: RN-A001
    Given User A has access valid for at least 30 seconds in workspace WA
    And the fixture uses successful renewal responses and the controlled clock
    When User A generates mouse movement every 100 milliseconds for 15 seconds
    Then the recorded successful renewal count is at least 1 before the 15-second interval ends
    And a protected validation request with the installed access credential returns result true
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-A002

**Continuous keyboard input reaches the requested renewal target**

Use case: [UC-R01](03-use-cases-renewal.md#uc-r01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Continuous keyboard input reaches the requested renewal target
  @target @RN-A002
  Scenario: RN-A002
    Given User A has access valid for at least 30 seconds in workspace WA
    And the fixture uses successful renewal responses and the controlled clock
    When User A generates keyboard input every 100 milliseconds for 15 seconds
    Then the recorded successful renewal count is at least 1 before the 15-second interval ends
    And a protected validation request with the installed access credential returns result true
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-A003

**Continuous scroll activity reaches the requested renewal target**

Use case: [UC-R01](03-use-cases-renewal.md#uc-r01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Continuous scroll activity reaches the requested renewal target
  @target @RN-A003
  Scenario: RN-A003
    Given User A has access valid for at least 30 seconds in workspace WA
    And the fixture uses successful renewal responses and the controlled clock
    When User A generates scroll activity every 100 milliseconds for 15 seconds
    Then the recorded successful renewal count is at least 1 before the 15-second interval ends
    And a protected validation request with the installed access credential returns result true
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-A004

**User A alternates pointer, keyboard, and scroll input**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187), [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194), [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A alternates pointer, keyboard, and scroll input
  @target @RN-A004
  Scenario: RN-A004
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A alternates pointer, keyboard, and scroll input
    When the fixture repeats the input sequence every 100 milliseconds for 15 seconds
    Then the successful renewal count is at least 1 during that interval
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-A005

**User A uses keyboard navigation without pointer input**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A uses keyboard navigation without pointer input
  @target @RN-A005
  Scenario: RN-A005
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A uses keyboard navigation without pointer input
    When User A continues keyboard input every 100 milliseconds for 15 seconds
    Then the successful renewal count is at least 1 during that interval
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-A006

**User A scrolls a same-origin nested application pane**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A scrolls a same-origin nested application pane
  @target @RN-A006
  Scenario: RN-A006
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A scrolls a same-origin nested application pane
    When User A sends scroll input every 100 milliseconds for 15 seconds inside that pane
    Then the successful renewal count is at least 1 during that 15-second interval
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-A007

**User A edits inside a cross-origin iframe**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A edits inside a cross-origin iframe
  @policy_open @RN-A007
  Scenario: RN-A007
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A edits inside a cross-origin iframe
    When User A types continuously for 15 seconds inside the iframe
    Then the trace distinguishes iframe input from shell-received input
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A008

**User A reads without input**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A reads without input
  @observed @RN-A008
  Scenario: RN-A008
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A reads without input
    When the controlled clock advances past access expiry
    Then the timeout observation records the access-expired state
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-A009

**User A generates only WebSocket heartbeats**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A generates only WebSocket heartbeats
  @policy_open @RN-A009
  Scenario: RN-A009
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A generates only WebSocket heartbeats
    When the controlled clock advances past access expiry
    Then the trace records 0 pointer, keyboard, and scroll events
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A010

**User A generates synthetic script events**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A generates synthetic script events
  @policy_open @RN-A010
  Scenario: RN-A010
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A generates synthetic script events
    When the fixture dispatches 100 synthetic activity events
    Then the trace records the trusted flag for all 100 events
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A011

**User A uses a touch screen**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A uses a touch screen
  @policy_open @RN-A011
  Scenario: RN-A011
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A uses a touch screen
    When User A swipes the application pane for 15 seconds
    Then the trace records which shell event types the browser emits
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A012

**User A uses an input method editor**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A uses an input method editor
  @policy_open @RN-A012
  Scenario: RN-A012
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A uses an input method editor
    When User A composes and commits text in workspace WA
    Then the trace records composition and keyboard events separately
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A013

**User A holds one keyboard key**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A holds one keyboard key
  @target @RN-A013
  Scenario: RN-A013
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A holds one keyboard key
    When the fixture emits repeat key events every 100 milliseconds for 15 seconds
    Then the successful renewal count is at least 1 during that interval
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-A014

**User A moves the pointer every 4900 milliseconds**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A moves the pointer every 4900 milliseconds
  @policy_open @RN-A014
  Scenario: RN-A014
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A moves the pointer every 4900 milliseconds
    When the fixture continues activity through two access deadlines
    Then the trace records pending activity timers and successful renewals at both deadlines
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Activity eligibility or acceptance for this input context needs owner review; record observations only.

### RN-A015

**User A moves the pointer then stops**

Use case: [UC-R02](03-use-cases-renewal.md#uc-r02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: User A moves the pointer then stops
  @observed @RN-A015
  Scenario: RN-A015
    Given User A has a valid session in WA with at least 30 seconds of access remaining
    And User A moves the pointer then stops
    When the controlled clock advances 5000 milliseconds after the last movement
    Then the source-observation trace records the scheduled activity callback exactly once
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Target assertion; existing continuous-activity failures remain visible.

### RN-B001

**Activity request boundary at 24999 milliseconds**

Use case: [UC-R03](03-use-cases-renewal.md#uc-r03). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [extend.ts](evidence/comprehensive-renewal-20261028/sources/d936faf94727/extend.ts#L8-L30). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Activity request boundary at 24999 milliseconds
  @observed @RN-B001
  Scenario: RN-B001
    Given User A has access remaining 24999 milliseconds
    And logout is false and the activity endpoint is isolated
    When the fixture invokes the shared activity renewal function once
    Then the activity POST count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B002

**Activity request boundary at 25000 milliseconds**

Use case: [UC-R03](03-use-cases-renewal.md#uc-r03). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [extend.ts](evidence/comprehensive-renewal-20261028/sources/d936faf94727/extend.ts#L8-L30). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Activity request boundary at 25000 milliseconds
  @observed @RN-B002
  Scenario: RN-B002
    Given User A has access remaining 25000 milliseconds
    And logout is false and the activity endpoint is isolated
    When the fixture invokes the shared activity renewal function once
    Then the activity POST count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B003

**Activity request boundary at 25001 milliseconds**

Use case: [UC-R03](03-use-cases-renewal.md#uc-r03). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [extend.ts](evidence/comprehensive-renewal-20261028/sources/d936faf94727/extend.ts#L8-L30). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Activity request boundary at 25001 milliseconds
  @observed @RN-B003
  Scenario: RN-B003
    Given User A has access remaining 25001 milliseconds
    And logout is false and the activity endpoint is isolated
    When the fixture invokes the shared activity renewal function once
    Then the activity POST count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B004

**Manual recovery deadline offset -1 milliseconds**

Use case: [UC-R04](03-use-cases-renewal.md#uc-r04). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L75-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual recovery deadline offset -1 milliseconds
  @observed @RN-B004
  Scenario: RN-B004
    Given the controlled clock is 1 milliseconds before the refresh expiry minus 2000 milliseconds
    And User A sees the timeout dialog and has no renewal pending
    When the fixture invokes the timeout controller renewal action once
    Then the relogin request count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B005

**Manual recovery deadline offset 0 milliseconds**

Use case: [UC-R04](03-use-cases-renewal.md#uc-r04). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L75-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual recovery deadline offset 0 milliseconds
  @observed @RN-B005
  Scenario: RN-B005
    Given the controlled clock is 0 milliseconds at the refresh expiry minus 2000 milliseconds
    And User A sees the timeout dialog and has no renewal pending
    When the fixture invokes the timeout controller renewal action once
    Then the relogin request count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B006

**Manual recovery deadline offset 1 milliseconds**

Use case: [UC-R04](03-use-cases-renewal.md#uc-r04). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L75-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual recovery deadline offset 1 milliseconds
  @observed @RN-B006
  Scenario: RN-B006
    Given the controlled clock is 1 milliseconds after the refresh expiry minus 2000 milliseconds
    And User A sees the timeout dialog and has no renewal pending
    When the fixture invokes the timeout controller renewal action once
    Then the relogin request count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B007

**Refresh reuse boundary offset -1 milliseconds**

Use case: [UC-R05](03-use-cases-renewal.md#uc-r05). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Refresh reuse boundary offset -1 milliseconds
  @observed @RN-B007
  Scenario: RN-B007
    Given User A has refresh validity of 10799999 milliseconds
    And the fixture records POST calls independently of promise settlement
    When the fixture invokes getRefreshToken once
    Then the refresh-token acquisition POST count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B008

**Refresh reuse boundary offset 0 milliseconds**

Use case: [UC-R05](03-use-cases-renewal.md#uc-r05). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Refresh reuse boundary offset 0 milliseconds
  @observed @RN-B008
  Scenario: RN-B008
    Given User A has refresh validity of 10800000 milliseconds
    And the fixture records POST calls independently of promise settlement
    When the fixture invokes getRefreshToken once
    Then the refresh-token acquisition POST count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B009

**Refresh reuse boundary offset 1 milliseconds**

Use case: [UC-R05](03-use-cases-renewal.md#uc-r05). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Refresh reuse boundary offset 1 milliseconds
  @observed @RN-B009
  Scenario: RN-B009
    Given User A has refresh validity of 10800001 milliseconds
    And the fixture records POST calls independently of promise settlement
    When the fixture invokes getRefreshToken once
    Then the refresh-token acquisition POST count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B010

**a scheduled acquisition callback is 1 millisecond late with access still valid**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: a scheduled acquisition callback is 1 millisecond late with access still valid
  @observed @RN-B010
  Scenario: RN-B010
    Given User A has a controlled session in WA
    And a scheduled acquisition callback is 1 millisecond late with access still valid
    And the document is visible with no prompt, logout, or acquisition pending
    And refresh remains valid for one hour
    When the fixture delivers the callback
    Then the acquisition POST count equals 1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B011

**a scheduled acquisition callback arrives after access expiry**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: a scheduled acquisition callback arrives after access expiry
  @observed @RN-B011
  Scenario: RN-B011
    Given User A has a controlled session in WA
    And a scheduled acquisition callback arrives after access expiry
    When the fixture delivers the callback
    Then the acquisition POST count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B012

**the browser becomes hidden before the scheduled callback**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the browser becomes hidden before the scheduled callback
  @observed @RN-B012
  Scenario: RN-B012
    Given User A has a controlled session in WA
    And the browser becomes hidden before the scheduled callback
    When the fixture delivers the callback while hidden
    Then the scheduled acquisition POST count equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B013

**access has expired while the browser is suspended**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: access has expired while the browser is suspended
  @observed @RN-B013
  Scenario: RN-B013
    Given User A has a controlled session in WA
    And access has expired while the browser is suspended
    When the fixture resumes the browser and dispatches visibilitychange
    Then the timeout state equals visible
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B014

**the system clock moves backward by 10 minutes**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the system clock moves backward by 10 minutes
  @policy_open @RN-B014
  Scenario: RN-B014
    Given User A has a controlled session in WA
    And the system clock moves backward by 10 minutes
    When the fixture reconciles the session on visibility return
    Then the trace records absolute access expiry and the effective clock before any renewal decision
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B015

**the system clock moves forward by 24 hours**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the system clock moves forward by 24 hours
  @observed @RN-B015
  Scenario: RN-B015
    Given User A has a controlled session in WA
    And the system clock moves forward by 24 hours
    When the fixture reconciles the session on visibility return
    Then the timeout state equals visible
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B016

**the timezone changes from UTC to Asia/Singapore without changing epoch time**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the timezone changes from UTC to Asia/Singapore without changing epoch time
  @observed @RN-B016
  Scenario: RN-B016
    Given User A has a controlled session in WA
    And the timezone changes from UTC to Asia/Singapore without changing epoch time
    When the fixture reconciles the session
    Then the computed access deadline equals its pre-change epoch timestamp
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-B017

**access and refresh expire at the same epoch timestamp**

Use case: [UC-R06](03-use-cases-renewal.md#uc-r06). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: access and refresh expire at the same epoch timestamp
  @observed @RN-B017
  Scenario: RN-B017
    Given User A has a controlled session in WA
    And access and refresh expire at the same epoch timestamp
    When the controlled clock reaches that timestamp
    Then the acquisition POST count after that timestamp equals 0
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-M001

**the relogin response is held pending**

Use case: [UC-R07](03-use-cases-renewal.md#uc-r07). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin response is held pending
  @target @RN-M001
  Scenario: RN-M001
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin response is held pending
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    Then the successful dialog closure count equals 0 while the request is pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M002

**the relogin response supplies usable future access**

Use case: [UC-R07](03-use-cases-renewal.md#uc-r07). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin response supplies usable future access
  @target @RN-M002
  Scenario: RN-M002
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin response supplies usable future access
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    Then the successful dialog closure count equals 1 after response completion
    And the next protected validation returns result true using the installed access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M003

**the relogin response rejects while refresh remains usable**

Use case: [UC-R07](03-use-cases-renewal.md#uc-r07). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin response rejects while refresh remains usable
  @target @RN-M003
  Scenario: RN-M003
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin response rejects while refresh remains usable
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    Then the successful dialog closure count equals 0
    And the controller permits another renewal attempt after rejection
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M004

**the first relogin rejects and the second response supplies usable access**

Use case: [UC-R07](03-use-cases-renewal.md#uc-r07). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the first relogin rejects and the second response supplies usable access
  @target @RN-M004
  Scenario: RN-M004
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the first relogin rejects and the second response supplies usable access
    When the fixture performs two ordered manual renewal attempts
    Then the relogin POST count equals 2
    And the successful dialog closure count equals 1 after the second response
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M005

**the first relogin is pending**

Use case: [UC-R07](03-use-cases-renewal.md#uc-r07). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the first relogin is pending
  @target @RN-M005
  Scenario: RN-M005
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the first relogin is pending
    When the fixture activates the Extend button 20 times before settlement
    Then the relogin POST count equals 1
    And the successful dialog closure count equals 0 before settlement
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M006

**the relogin response remains pending**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin response remains pending
  @observed @RN-M006
  Scenario: RN-M006
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin response remains pending
    When User A activates the timeout dialog logout action
    Then the pending relogin signal is aborted
    And a later relogin response installs 0 credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M007

**the relogin response remains pending**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin response remains pending
  @observed @RN-M007
  Scenario: RN-M007
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin response remains pending
    When the fixture unmounts the timeout controller
    Then the later response causes 0 dialog closure callbacks on the unmounted controller
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M008

**the relogin request fails after the recovery deadline**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin request fails after the recovery deadline
  @observed @RN-M008
  Scenario: RN-M008
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin request fails after the recovery deadline
    When the fixture delivers the rejection
    Then the next manual renewal action sends 0 relogin POSTs
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M009

**the relogin request starts before the recovery deadline and succeeds after it**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the relogin request starts before the recovery deadline and succeeds after it
  @observed @RN-M009
  Scenario: RN-M009
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the relogin request starts before the recovery deadline and succeeds after it
    When the fixture delivers a response with usable access
    Then the source-observation trace records whether pending renewal suppresses local logout
    And the next protected validation uses the actual installed access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI label; runtime accessible name and uniqueness need verification. Late-response acceptance needs service-time policy review.

### RN-M010

**an access-only acquisition promise is pending when the timeout mounts**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: an access-only acquisition promise is pending when the timeout mounts
  @observed @RN-M010
  Scenario: RN-M010
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And an access-only acquisition promise is pending when the timeout mounts
    When the fixture delivers acquisition settlement without credentials
    Then the trace distinguishes promise settlement from credential installation
    And the successful renewal count equals 0 without usable returned access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M011

**the timeout controller belongs to session A and session B replaces A**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the timeout controller belongs to session A and session B replaces A
  @observed @RN-M011
  Scenario: RN-M011
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the timeout controller belongs to session A and session B replaces A
    When User A activates the stale controller renewal action
    Then the stale controller sends 0 relogin requests for session B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-M012

**the timeout controller belongs to session A and session B replaces A**

Use case: [UC-R08](03-use-cases-renewal.md#uc-r08). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the timeout controller belongs to session A and session B replaces A
  @observed @RN-M012
  Scenario: RN-M012
    Given User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise
    And the timeout controller belongs to session A and session B replaces A
    When User A activates the stale controller logout action
    Then the stale controller starts 0 logout requests for session B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived UI action; new end-to-end binding and target execution remain unavailable.

### RN-P001

**Relogin rejects missing access header**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects missing access header
  @observed @RN-P001
  Scenario: RN-P001
    Given User A has a pending manual relogin with no logout requested
    And the response supplies no access credential
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P002

**Relogin rejects empty access header**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects empty access header
  @observed @RN-P002
  Scenario: RN-P002
    Given User A has a pending manual relogin with no logout requested
    And the response supplies an empty string
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P003

**Relogin rejects unreadable access payload**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects unreadable access payload
  @observed @RN-P003
  Scenario: RN-P003
    Given User A has a pending manual relogin with no logout requested
    And the response supplies the string not-a-jwt
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P004

**Relogin rejects missing exp**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects missing exp
  @observed @RN-P004
  Scenario: RN-P004
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload without exp
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P005

**Relogin rejects string exp**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects string exp
  @observed @RN-P005
  Scenario: RN-P005
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload with exp as a numeric string
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P006

**Relogin rejects expired exp**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects expired exp
  @observed @RN-P006
  Scenario: RN-P006
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload exp one second before the controlled clock
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P007

**Relogin rejects exp at current time**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects exp at current time
  @observed @RN-P007
  Scenario: RN-P007
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload exp equal to the controlled clock
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P008

**Relogin rejects missing iat**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects missing iat
  @observed @RN-P008
  Scenario: RN-P008
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload without iat
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P009

**Relogin rejects zero iat**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects zero iat
  @observed @RN-P009
  Scenario: RN-P009
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload with iat equal to 0
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P010

**Relogin rejects negative iat**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects negative iat
  @observed @RN-P010
  Scenario: RN-P010
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload with iat equal to -1
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P011

**Relogin rejects iat equals exp**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects iat equals exp
  @observed @RN-P011
  Scenario: RN-P011
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload with iat equal to exp
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P012

**Relogin rejects iat exceeds exp**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects iat exceeds exp
  @observed @RN-P012
  Scenario: RN-P012
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a payload with iat greater than exp
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P013

**Relogin rejects nonfinite exp multiplication**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Relogin rejects nonfinite exp multiplication
  @observed @RN-P013
  Scenario: RN-P013
    Given User A has a pending manual relogin with no logout requested
    And the response supplies a numeric exp whose millisecond conversion overflows
    When the fixture delivers the relogin response through the real response interceptor
    Then the successful dialog closure count equals 0
    And the response installs 0 access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P014

**valid lowercase header**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: valid lowercase header
  @observed @RN-P014
  Scenario: RN-P014
    Given User A has a pending manual renewal
    And the response contains a valid access token in single-ui-authorization
    When the fixture delivers the response
    Then the trace records the selected header value and installed expiry
    And a service-side protected validation records the accepted identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P015

**valid title-case header**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: valid title-case header
  @observed @RN-P015
  Scenario: RN-P015
    Given User A has a pending manual renewal
    And the response contains a valid access token in Single-UI-Authorization
    When the fixture delivers the response
    Then the trace records the selected header value and installed expiry
    And a service-side protected validation records the accepted identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P016

**missing refresh on successful access renewal**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: missing refresh on successful access renewal
  @policy_open @RN-P016
  Scenario: RN-P016
    Given User A has a pending manual renewal
    And the response contains valid renewed access without a replacement refresh token
    When the fixture delivers the response
    Then the trace records the selected header value and installed expiry
    And a service-side protected validation records the accepted identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P017

**future issued-at**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: future issued-at
  @policy_open @RN-P017
  Scenario: RN-P017
    Given User A has a pending manual renewal
    And the response contains a future iat that is less than exp
    When the fixture delivers the response
    Then the trace records the selected header value and installed expiry
    And a service-side protected validation records the accepted identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-P018

**conflicting access header casing**

Use case: [UC-R09](03-use-cases-renewal.md#uc-r09). Level: `component-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: conflicting access header casing
  @policy_open @RN-P018
  Scenario: RN-P018
    Given User A has a pending manual renewal
    And the response contains different access values under lowercase and title-case header names
    When the fixture delivers the response
    Then the trace records the selected header value and installed expiry
    And a service-side protected validation records the accepted identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R001

**Late renewal success: logs out A before response delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal success: logs out A before response delivery
  @proposed_security @RN-R001
  Scenario: RN-R001
    Given session A owns one held renewal request
    And the held response outcome is success
    When the fixture logs out A before response delivery
    And the fixture delivers the held response
    Then the late success installs 0 credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R002

**Late renewal failure: logs out A before response delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal failure: logs out A before response delivery
  @proposed_security @RN-R002
  Scenario: RN-R002
    Given session A owns one held renewal request
    And the held response outcome is failure
    When the fixture logs out A before response delivery
    And the fixture delivers the held response
    Then the late failure changes 0 current authentication fields
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R003

**Late renewal success: replaces A with authenticated session B before response delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal success: replaces A with authenticated session B before response delivery
  @proposed_security @RN-R003
  Scenario: RN-R003
    Given session A owns one held renewal request
    And the held response outcome is success
    When the fixture replaces A with authenticated session B before response delivery
    And the fixture delivers the held response
    Then the final installed identity equals B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R004

**Late renewal failure: replaces A with authenticated session B before response delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal failure: replaces A with authenticated session B before response delivery
  @proposed_security @RN-R004
  Scenario: RN-R004
    Given session A owns one held renewal request
    And the held response outcome is failure
    When the fixture replaces A with authenticated session B before response delivery
    And the fixture delivers the held response
    Then the final installed identity equals B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R005

**Late renewal success: aborts the request before response delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal success: aborts the request before response delivery
  @proposed_security @RN-R005
  Scenario: RN-R005
    Given session A owns one held renewal request
    And the held response outcome is success
    When the fixture aborts the request before response delivery
    And the fixture delivers the held response
    Then the response installs 0 credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R006

**Late renewal success: starts a fresh login while renewal is pending**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal success: starts a fresh login while renewal is pending
  @proposed_security @RN-R006
  Scenario: RN-R006
    Given session A owns one held renewal request
    And the held response outcome is success
    When the fixture starts a fresh login while renewal is pending
    And the fixture delivers the held response
    Then the old renewal installs 0 credentials after the login epoch changes
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R007

**Late renewal failure: starts a fresh login while renewal is pending**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal failure: starts a fresh login while renewal is pending
  @proposed_security @RN-R007
  Scenario: RN-R007
    Given session A owns one held renewal request
    And the held response outcome is failure
    When the fixture starts a fresh login while renewal is pending
    And the fixture delivers the held response
    Then the old failure clears 0 fields in the new login epoch
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R008

**Late renewal success: completes A to B to A account switching before delivery**

Use case: [UC-R10](03-use-cases-renewal.md#uc-r10). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Late renewal success: completes A to B to A account switching before delivery
  @proposed_security @RN-R008
  Scenario: RN-R008
    Given session A owns one held renewal request
    And the held response outcome is success
    When the fixture completes A to B to A account switching before delivery
    And the fixture delivers the held response
    Then the old response changes 0 fields in the replacement A session
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R009

**1 simultaneous acquisition callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L177). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 1 simultaneous acquisition callers share one pending operation
  @observed @RN-R009
  Scenario: RN-R009
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    When the fixture invokes 1 acquisition callers before settlement
    Then the refresh-token acquisition POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R010

**2 simultaneous acquisition callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L177). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 2 simultaneous acquisition callers share one pending operation
  @observed @RN-R010
  Scenario: RN-R010
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    When the fixture invokes 2 acquisition callers before settlement
    Then the refresh-token acquisition POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R011

**8 simultaneous acquisition callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L177). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 8 simultaneous acquisition callers share one pending operation
  @observed @RN-R011
  Scenario: RN-R011
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    When the fixture invokes 8 acquisition callers before settlement
    Then the refresh-token acquisition POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R012

**64 simultaneous acquisition callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L177). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 64 simultaneous acquisition callers share one pending operation
  @observed @RN-R012
  Scenario: RN-R012
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    When the fixture invokes 64 acquisition callers before settlement
    Then the refresh-token acquisition POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R013

**2 simultaneous manual callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L29-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 2 simultaneous manual callers share one pending operation
  @observed @RN-R013
  Scenario: RN-R013
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    And all manual calls use the same mounted Timeout controller extend action
    When the fixture invokes 2 same-controller extend actions before settlement
    Then the relogin POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R014

**20 simultaneous manual callers share one pending operation**

Use case: [UC-R11](03-use-cases-renewal.md#uc-r11). Level: `component-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L29-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: 20 simultaneous manual callers share one pending operation
  @observed @RN-R014
  Scenario: RN-R014
    Given User A has unchanged access identity and session epoch
    And refresh reuse does not suppress acquisition
    And the first response remains pending
    And all manual calls use the same mounted Timeout controller extend action
    When the fixture invokes 20 same-controller extend actions before settlement
    Then the relogin POST count equals 1
    And all accepted callers observe the same final installed identity
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R015

**an old acquisition is pending when access changes**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: an old acquisition is pending when access changes
  @observed @RN-R015
  Scenario: RN-R015
    Given User A has an isolated session
    And an old acquisition is pending when access changes
    When the fixture requests acquisition for the new access
    Then the old abort signal equals aborted and the new request owner equals current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R016

**an old aborted request settles after a new request starts**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: an old aborted request settles after a new request starts
  @observed @RN-R016
  Scenario: RN-R016
    Given User A has an isolated session
    And an old aborted request settles after a new request starts
    When the fixture settles the old request
    Then the pending-request pointer still identifies the new request
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R017

**two acquisition callers have different session epochs**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: two acquisition callers have different session epochs
  @observed @RN-R017
  Scenario: RN-R017
    Given User A has an isolated session
    And two acquisition callers have different session epochs
    When the fixture delivers responses in reverse order
    Then only the current epoch response can install credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R018

**the timeout timer and renewal success have the same due time**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the timeout timer and renewal success have the same due time
  @policy_open @RN-R018
  Scenario: RN-R018
    Given User A has an isolated session
    And the timeout timer and renewal success have the same due time
    When the fixture runs both possible delivery orders
    Then each order records closure count, logout count, and final owner separately
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R019

**a protected response and a relogin response finish together**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: a protected response and a relogin response finish together
  @policy_open @RN-R019
  Scenario: RN-R019
    Given User A has an isolated session
    And a protected response and a relogin response finish together
    When the fixture runs both possible response orders
    Then the final owner remains A and the trace records the final access expiry
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-R020

**a stale unauthorized response arrives after successful renewal**

Use case: [UC-R12](03-use-cases-renewal.md#uc-r12). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L29-L135). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: a stale unauthorized response arrives after successful renewal
  @policy_open @RN-R020
  Scenario: RN-R020
    Given User A has an isolated session
    And a stale unauthorized response arrives after successful renewal
    When the fixture delivers the unauthorized response
    Then the trace records whether the renewed session is cleared by the old response
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-L001

**Repeat success for 1 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat success for 1 cycles
  @observed @RN-L001
  Scenario: RN-L001
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 1 ordered success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L002

**Repeat success for 2 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat success for 2 cycles
  @observed @RN-L002
  Scenario: RN-L002
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 2 ordered success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L003

**Repeat success for 10 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat success for 10 cycles
  @observed @RN-L003
  Scenario: RN-L003
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 10 ordered success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L004

**Repeat success for 1000 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat success for 1000 cycles
  @observed @RN-L004
  Scenario: RN-L004
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 1000 ordered success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L005

**Repeat failure then success for 2 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat failure then success for 2 cycles
  @observed @RN-L005
  Scenario: RN-L005
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 2 ordered failure then success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L006

**Repeat failure then success for 10 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat failure then success for 10 cycles
  @observed @RN-L006
  Scenario: RN-L006
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 10 ordered failure then success cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L007

**Repeat logout then login for 100 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat logout then login for 100 cycles
  @proposed_security @RN-L007
  Scenario: RN-L007
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 100 ordered logout then login cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L008

**Repeat mount then unmount for 100 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat mount then unmount for 100 cycles
  @observed @RN-L008
  Scenario: RN-L008
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 100 ordered mount then unmount cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L009

**Repeat hide then show for 100 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat hide then show for 100 cycles
  @observed @RN-L009
  Scenario: RN-L009
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 100 ordered hide then show cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L010

**Repeat workspace switch for 100 cycles**

Use case: [UC-R13](03-use-cases-renewal.md#uc-r13). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L24-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Repeat workspace switch for 100 cycles
  @observed @RN-L010
  Scenario: RN-L010
    Given User A uses a fresh isolated browser context
    And the fixture records request owners, credentials, callbacks, timers, and listeners
    When the fixture completes 100 ordered workspace switch cycles
    And the fixture settles all accepted work after the final cycle
    Then the final installed identity equals the final authenticated fixture identity
    And the number of unresolved owned network operations equals 0
    And each successful manual recovery has exactly 1 closure transition
    And the final mounted listener and timer counts equal the recorded mounted baseline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.

### RN-L011

**Four-hour requested target crosses initial refresh expiry**

Use case: [UC-R14](03-use-cases-renewal.md#uc-r14). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Four-hour requested target crosses initial refresh expiry
  @target @RN-L011
  Scenario: RN-L011
    Given User A has accepted activity before every access deadline
    And the initial refresh expires within four controlled hours
    And renewal responses remain successful
    When the fixture advances through four controlled hours of continued activity
    Then the fresh SSO prompt count caused solely by an earlier elapsed-time maximum equals 0
    And the protected validation at the end returns result true
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Controlled four-hour fixture. This cannot prove indefinite execution or production timing.

### RN-H001

**the browser enters back-forward cache with a pending renewal**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the browser enters back-forward cache with a pending renewal
  @policy_open @RN-H001
  Scenario: RN-H001
    Given User A uses a synthetic account and isolated target
    And the browser enters back-forward cache with a pending renewal
    When the browser restores WA from back-forward cache
    Then the trace records restored session owner before the first protected request
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H002

**the browser reloads during a pending manual renewal**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the browser reloads during a pending manual renewal
  @policy_open @RN-H002
  Scenario: RN-H002
    Given User A uses a synthetic account and isolated target
    And the browser reloads during a pending manual renewal
    When the browser loads the shell from persisted state
    Then the first protected request records the restored credential owner and service validation result
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H003

**the renderer crashes with renewal pending**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the renderer crashes with renewal pending
  @policy_open @RN-H003
  Scenario: RN-H003
    Given User A uses a synthetic account and isolated target
    And the renderer crashes with renewal pending
    When the browser restores the session after renderer restart
    Then the trace records 0 deliveries from the terminated renderer
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H004

**the device sleeps before the acquisition deadline**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the device sleeps before the acquisition deadline
  @policy_open @RN-H004
  Scenario: RN-H004
    Given User A uses a synthetic account and isolated target
    And the device sleeps before the acquisition deadline
    When the device resumes after access expiry
    Then the trace records actual elapsed time and timeout state before any protected mutation
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H005

**the device loses network during renewal**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the device loses network during renewal
  @policy_open @RN-H005
  Scenario: RN-H005
    Given User A uses a synthetic account and isolated target
    And the device loses network during renewal
    When the network returns while refresh remains usable
    Then the next explicit renewal attempt records its request, returned access, and protected validation
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H006

**the device changes VPN during renewal**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the device changes VPN during renewal
  @policy_open @RN-H006
  Scenario: RN-H006
    Given User A uses a synthetic account and isolated target
    And the device changes VPN during renewal
    When the browser retries an explicit renewal on the new network
    Then the trace records service origin and accepted identity for the retry
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H007

**the browser is offline past refresh expiry**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the browser is offline past refresh expiry
  @proposed_security @RN-H007
  Scenario: RN-H007
    Given User A uses a synthetic account and isolated target
    And the browser is offline past refresh expiry
    When the browser reconnects to the service
    Then the protected service accepts 0 expired credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H008

**the browser disables persistent storage**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the browser disables persistent storage
  @policy_open @RN-H008
  Scenario: RN-H008
    Given User A uses a synthetic account and isolated target
    And the browser disables persistent storage
    When the browser attempts renewal with storage writes blocked
    Then the trace records each storage exception and whether access is installed
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H009

**the local storage quota is exhausted**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the local storage quota is exhausted
  @policy_open @RN-H009
  Scenario: RN-H009
    Given User A uses a synthetic account and isolated target
    And the local storage quota is exhausted
    When the browser receives successful renewed access
    Then the trace records the installed in-memory state and storage error separately
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H010

**the tab is duplicated during manual renewal**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the tab is duplicated during manual renewal
  @policy_open @RN-H010
  Scenario: RN-H010
    Given User A uses a synthetic account and isolated target
    And the tab is duplicated during manual renewal
    When the duplicate tab requests a protected resource
    Then each request records its own tab owner and service authorization result
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H011

**the user has a normal and private browser window with distinct fixture sessions**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the user has a normal and private browser window with distinct fixture sessions
  @policy_open @RN-H011
  Scenario: RN-H011
    Given User A uses a synthetic account and isolated target
    And the user has a normal and private browser window with distinct fixture sessions
    When both windows renew their isolated sessions
    Then a credential write in the normal context changes exactly 0 credential hashes in the private context
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-H012

**the user has two independent devices**

Use case: [UC-R15](03-use-cases-renewal.md#uc-r15). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L110-L205). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: the user has two independent devices
  @policy_open @RN-H012
  Scenario: RN-H012
    Given User A uses a synthetic account and isolated target
    And the user has two independent devices
    When device A logs out while device B renews
    Then the trace records the service revocation scope separately for each device
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.

### RN-F001

**Manual renewal rejects after HTTP 401**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after HTTP 401
  @target @RN-F001
  Scenario: RN-F001
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with HTTP 401
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F002

**Manual renewal rejects after HTTP 403**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after HTTP 403
  @target @RN-F002
  Scenario: RN-F002
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with HTTP 403
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F003

**Manual renewal rejects after HTTP 429 with Retry-After**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after HTTP 429 with Retry-After
  @target @RN-F003
  Scenario: RN-F003
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with HTTP 429 with Retry-After
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F004

**Manual renewal rejects after HTTP 500**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after HTTP 500
  @target @RN-F004
  Scenario: RN-F004
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with HTTP 500
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F005

**Manual renewal rejects after HTTP 503**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after HTTP 503
  @target @RN-F005
  Scenario: RN-F005
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with HTTP 503
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F006

**Manual renewal rejects after connection reset**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after connection reset
  @target @RN-F006
  Scenario: RN-F006
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with connection reset
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F007

**Manual renewal rejects after DNS failure**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after DNS failure
  @target @RN-F007
  Scenario: RN-F007
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with DNS failure
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F008

**Manual renewal rejects after TLS validation failure**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after TLS validation failure
  @target @RN-F008
  Scenario: RN-F008
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with TLS validation failure
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F009

**Manual renewal rejects after client timeout**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after client timeout
  @target @RN-F009
  Scenario: RN-F009
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with client timeout
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F010

**Manual renewal rejects after explicit request cancellation**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L149-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Manual renewal rejects after explicit request cancellation
  @target @RN-F010
  Scenario: RN-F010
    Given User A sees the timeout dialog with refresh usable beyond the test interval
    And the isolated service rejects relogin with explicit request cancellation
    When User A clicks the button labeled Extend inside the dialog named "Your session has been expired"
    And the fixture delivers the rejection
    Then the successful dialog closure count equals 0
    And the next explicit retry remains available while refresh remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.

### RN-F011

**Renewal never settles**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L90-L169). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal never settles
  @target @RN-F011
  Scenario: RN-F011
    Given User A has a pending manual renewal
    And the service fixture never settles that request
    When the controlled clock advances through the original recovery deadline
    Then the successful dialog closure count equals 0
    And the trace records pending state and logout availability at the deadline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: A maximum request duration and pending-state recovery policy remain undefined.

### RN-F012

**Malformed success releases its loader without proving renewal**

Use case: [UC-R16](03-use-cases-renewal.md#uc-r16). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L37-L89). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Malformed success releases its loader without proving renewal
  @observed @RN-F012
  Scenario: RN-F012
    Given User A has a pending manual renewal as the only loading request
    And the service returns HTTP 200 without usable access
    When the fixture delivers the response through the real interceptor
    Then the successful dialog closure count equals 0
    And the installed usable-access count from that response equals 0
    And the shared loader is not visible after the request settles
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: New definition; executable binding and target execution remain unavailable.

### RN-W001

**Renewal preserves two populated workspaces**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal preserves two populated workspaces
  @observed @RN-W001
  Scenario: RN-W001
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected and W-B loaded but hidden
    And the fixture records both workspace IDs and parameter hashes
    When the current session completes one successful renewal
    Then the workspace ID list equals its pre-renewal list
    And the selected workspace ID equals W-A
    And each container parameter hash equals its pre-renewal value
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W002

**Renewal starts before any module has loaded**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal starts before any module has loaded
  @observed @RN-W002
  Scenario: RN-W002
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected
    And the module import for W-A is held in Suspense
    When the current session completes one successful renewal
    And the driver releases the held module import
    Then W-A mounts exactly one module instance
    And the module protected request uses current access
    And the protected fixture principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W003

**Renewal while an inactive workspace first loads**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal while an inactive workspace first loads
  @observed @RN-W003
  Scenario: RN-W003
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active and W-B never visited
    And the fixture holds the W-B module import
    When User A selects tab ID workspaces-tab-W-B inside the workspaces tablist
    And the session completes one successful renewal
    And the driver releases the W-B module import
    Then the selected workspace ID equals W-B
    And the W-B module protected request uses current access
    And W-A retains its original descriptor hash
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W004

**Switch back during a held module import**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Switch back during a held module import
  @observed @RN-W004
  Scenario: RN-W004
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active and W-B import held
    When User A selects tab ID workspaces-tab-W-B inside the workspaces tablist
    And User A selects tab ID workspaces-tab-W-A inside the workspaces tablist
    And the session completes one successful renewal
    And the driver releases the W-B import
    Then the selected workspace ID equals W-A
    And W-B is hidden
    And W-B is associated with its own workspace ID
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W005

**Rapid workspace switching during renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Rapid workspace switching during renewal
  @proposed_security @RN-W005
  Scenario: RN-W005
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has populated W-A and W-B
    And one renewal response is held
    When User A alternates the W-A and W-B workspace tabs for ten switches
    And the driver releases the renewal response
    Then the final selected ID equals the final selected tab ID
    And each rendered trade or position row belongs to its configured workspace
    And the protected fixture accepts the installed current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W006

**Add workspace during pending renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Add workspace during pending renewal
  @observed @RN-W006
  Scenario: RN-W006
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A and W-B
    And one renewal response is held
    When User A clicks button Add Workspace in the workspaces tablist
    And the driver releases the renewal response
    Then the workspace count equals three
    And the two original workspace IDs remain present
    And the added workspace ID differs from both original IDs
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W007

**Delete inactive workspace during pending renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Delete inactive workspace during pending renewal
  @observed @RN-W007
  Scenario: RN-W007
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected and W-B inactive
    And one renewal response is held
    When User A clicks icon button delete with ID deleteWorkspace-W-B in workspace tab W-B
    And the driver releases the renewal response
    Then the workspace list contains W-A and excludes W-B
    And the selected workspace ID equals W-A
    And the protected fixture accepts current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W008

**Delete active first workspace during pending renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Delete active first workspace during pending renewal
  @observed @RN-W008
  Scenario: RN-W008
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected before W-B
    And one renewal response is held
    When User A clicks icon button delete with ID deleteWorkspace-W-A in workspace tab W-A
    And the driver releases the renewal response
    Then the workspace list contains only W-B
    And the selected workspace ID equals W-B
    And the persisted workspace descriptor list contains only W-B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W009

**Delete active last workspace during pending renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Delete active last workspace during pending renewal
  @observed @RN-W009
  Scenario: RN-W009
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-B selected after W-A
    And one renewal response is held
    When User A clicks icon button delete with ID deleteWorkspace-W-B in workspace tab W-B
    And the driver releases the renewal response
    Then the workspace list contains only W-A
    And the selected workspace ID equals W-A
    And renewal completion does not recreate W-B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W010

**Rename workspace during pending renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Rename workspace during pending renewal
  @observed @RN-W010
  Scenario: RN-W010
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected
    And one renewal response is held
    When User A fills textbox Workspace Name with ID edit-W-A with Renewal Draft
    And the driver releases the renewal response
    Then W-A label equals Renewal Draft
    And W-A ID equals its original ID
    And W-A container parameter hash equals its original hash
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W011

**Refresh one module during renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Refresh one module during renewal
  @observed @RN-W011
  Scenario: RN-W011
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A selected and W-B mounted
    And W-A exposes its supported module refresh callback
    When User A clicks icon button refresh with ID refreshWorkspace-W-A in workspace tab W-A
    And the session completes one successful renewal
    Then the W-A refresh callback invocation count equals one
    And the next protected W-A request uses current access
    And W-B descriptor hash equals its prior value
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W012

**Previously loaded hidden workspace sends requests**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [drawer.ts](evidence/comprehensive-renewal-20261028/sources/cfedf4c4f8c1/drawer.ts#L47-L67); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Previously loaded hidden workspace sends requests
  @observed @RN-W012
  Scenario: RN-W012
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A selected W-B once and returned to W-A
    And W-B remains mounted in a hidden tabpanel
    When the W-B fixture sends one protected data request after successful renewal
    Then the request credential identity equals current access
    And the response principal equals User A
    And W-A remains the selected workspace
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W013

**Permission removal affects hidden workspace**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Permission removal affects hidden workspace
  @proposed_security @RN-W013
  Scenario: RN-W013
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active and W-B hidden
    And the authorization fixture removes User A access to W-B before renewal
    When the session receives refreshed permission data
    And the W-B fixture sends a protected request
    Then the protected service returns no W-B protected records
    And the service authorization event records a denial for User A and W-B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W014

**Account switch cannot expose prior workspace data**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Account switch cannot expose prior workspace data
  @proposed_security @RN-W014
  Scenario: RN-W014
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has populated W-A and W-B
    And User B lacks permission to trade X
    When User A logs out
    And User B signs in using a separate synthetic identity
    Then no protected response to User B contains trade X
    And the server authorization log contains zero User B grants for trade X
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W015

**Populated workspace descriptors across reauthentication**

Use case: [UC-W04](03-use-cases-renewal.md#uc-w04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Populated workspace descriptors across reauthentication
  @policy_open @RN-W015
  Scenario: RN-W015
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A and W-B with distinct module parameters
    And the fixture records descriptor and unsaved-edit hashes
    When User A logs out
    And User A signs in again
    Then the result records before and after workspace IDs and descriptor hashes
    And the result records unsaved-edit hashes separately from persisted descriptors
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: O-004 does not define populated workspace or unsaved-edit restoration after reauthentication.

Acceptance: BLOCKED. Policy gap: O-004 does not define populated workspace or unsaved-edit restoration after reauthentication.

### RN-W016

**Unsaved form input across in-session renewal**

Use case: [UC-W04](03-use-cases-renewal.md#uc-w04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Unsaved form input across in-session renewal
  @policy_open @RN-W016
  Scenario: RN-W016
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a source-bound unsaved form in W-A
    And the fixture records its unsaved text and server record version
    When the session completes one successful renewal
    Then the result records before and after form values
    And the server record version and mutation count are retained
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Unsaved application form preservation across renewal has no inspected business acceptance rule.

Acceptance: BLOCKED. Policy gap: Unsaved application form preservation across renewal has no inspected business acceptance rule.

### RN-W017

**Module import rejects while renewal succeeds**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Module import rejects while renewal succeeds
  @observed @RN-W017
  Scenario: RN-W017
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A import pending
    And the fixture can reject only that module import
    When the session completes one successful renewal
    And the driver rejects the W-A module import
    Then the protected fixture accepts current access
    And the W-A import rejection is retained separately from the renewal outcome
    And the W-B workspace descriptor remains present
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W018

**Module import resolves after logout**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Module import resolves after logout
  @proposed_security @RN-W018
  Scenario: RN-W018
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has the W-A import held
    When User A clicks button Logout in the session dialog
    And the driver releases the W-A module import
    Then no protected service accepts ended-session access from W-A
    And no protected fixture record is returned after logout completes
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W019

**Catalog validation delays Home readiness**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Catalog validation delays Home readiness
  @observed @RN-W019
  Scenario: RN-W019
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has saved W-A and W-B
    And the fixture holds catalog or entitlement validation
    When the access deadline passes
    And the driver releases catalog validation
    Then the result records Home readiness and dialog visibility in order
    And the protected service records no acceptance of expired access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W020

**Removed workspace receives delayed response**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Removed workspace receives delayed response
  @proposed_security @RN-W020
  Scenario: RN-W020
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a W-B data response held
    And W-A is selected
    When User A clicks icon button delete with ID deleteWorkspace-W-B in workspace tab W-B
    And the driver releases the W-B data response
    Then the workspace list excludes W-B
    And no W-A row changes to a W-B-only fixture record
    And the removed workspace receives zero new visible panels
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W021

**Same module in two workspaces retains routing**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Same module in two workspaces retains routing
  @proposed_security @RN-W021
  Scenario: RN-W021
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A and W-B contain the same module with distinct parameter IDs
    And both modules issue uniquely tagged requests
    When the session completes one successful renewal
    And the driver delivers the W-B response before the W-A response
    Then W-A displays only W-A-tagged data
    And W-B displays only W-B-tagged data
    And each request principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W022

**Expired session prompt covers workspace navigation**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Expired session prompt covers workspace navigation
  @target @RN-W022
  Scenario: RN-W022
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A and W-B
    And access has expired while refresh remains usable
    When User A clicks button Extend in dialog Your session has been expired
    And the driver holds the renewal response
    Then the dialog successful closure count equals zero
    And the result records selected workspace ID and protected request outcomes during the hold
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W023

**Renewal success returns to selected workspace**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal success returns to selected workspace
  @target @RN-W023
  Scenario: RN-W023
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-B selected
    And dialog Your session has been expired is visible with usable refresh
    When User A clicks button Extend in dialog Your session has been expired
    And the fixture completes renewal with usable access
    Then the dialog closes exactly once after completion
    And the selected workspace ID equals W-B
    And the protected fixture accepts installed access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W024

**Renewal failure keeps workspace retry available**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal failure keeps workspace retry available
  @target @RN-W024
  Scenario: RN-W024
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-B selected
    And dialog Your session has been expired is visible with usable refresh
    When User A clicks button Extend in dialog Your session has been expired
    And the fixture rejects the renewal request before recovery expires
    Then the dialog successful closure count equals zero
    And the Extend button permits another renewal attempt
    And the selected workspace ID equals W-B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W025

**Workspace restoration after browser crash**

Use case: [UC-W04](03-use-cases-renewal.md#uc-w04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Workspace restoration after browser crash
  @policy_open @RN-W025
  Scenario: RN-W025
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has populated W-A and W-B
    And the fixture records saved descriptors and unsaved application state
    When the driver terminates the isolated browser process
    And the driver reopens the portal origin
    Then the result records restored workspace descriptors separately from unsaved state
    And the protected service records the identity used by the reopened portal
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Crash recovery and unsaved-state restoration policy remains unavailable.

Acceptance: BLOCKED. Policy gap: Crash recovery and unsaved-state restoration policy remains unavailable.

### RN-W026

**Duplicate workspace labels retain ID isolation**

Use case: [UC-W03](03-use-cases-renewal.md#uc-w03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Duplicate workspace labels retain ID isolation
  @proposed_security @RN-W026
  Scenario: RN-W026
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A and W-B share label Positions
    And their module parameter IDs differ
    When the session completes one successful renewal
    And the driver selects tab ID workspaces-tab-W-B
    Then the selected workspace ID equals W-B
    And the W-B visible data matches the W-B parameter ID
    And the W-A descriptor hash remains unchanged
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-W027

**Workspace selection index changes during renewal**

Use case: [UC-W01](03-use-cases-renewal.md#uc-w01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/2c6b5fa605b4/index.tsx#L24-L76). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Workspace selection index changes during renewal
  @observed @RN-W027
  Scenario: RN-W027
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A selects W-C after W-A and W-B
    And one renewal response is held
    When User A clicks icon button delete with ID deleteWorkspace-W-A in workspace tab W-A
    And the driver releases the renewal response
    Then the selected workspace ID equals W-C
    And the selected tab resolves through W-C ID after index shifting
    And the workspace list excludes W-A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W028

**OpenFin launch arrives during renewal**

Use case: [UC-W05](03-use-cases-renewal.md#uc-w05). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useOpenfin.ts](evidence/comprehensive-renewal-20261028/sources/3abe3884f3fd/useOpenfin.ts#L19-L94); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: OpenFin launch arrives during renewal
  @policy_open @RN-W028
  Scenario: RN-W028
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active
    And an isolated FDC3 adapter is installed
    And renewal is pending with old access expired
    When the adapter emits one cashflow view-launch intent for fixture trade X
    Then the result records the intent, dispatch time, workspace ID, and credential identity
    And the protected service records whether trade X access was authorized
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: External FDC3 intent eligibility and queuing during expired access remain undefined.

Acceptance: BLOCKED. Policy gap: External FDC3 intent eligibility and queuing during expired access remain undefined.

### RN-W029

**Mouse activity in an active populated workspace**

Use case: [UC-W06](03-use-cases-renewal.md#uc-w06). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [REQ-active-session-renewal.md](evidence/comprehensive-renewal-20261028/sources/3db69ca6827b/REQ-active-session-renewal.md#L165-L242). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Mouse activity in an active populated workspace
  @target @RN-W029
  Scenario: RN-W029
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active with at least 30 seconds of access remaining
    And the driver can deliver native mouse movements inside W-A
    When User A moves the mouse every 100 milliseconds for 15 seconds
    Then at least one completed renewal is accepted before the interval ends
    And the protected fixture accepts the installed current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W030

**Keyboard activity in a child module**

Use case: [UC-W06](03-use-cases-renewal.md#uc-w06). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [REQ-active-session-renewal.md](evidence/comprehensive-renewal-20261028/sources/3db69ca6827b/REQ-active-session-renewal.md#L165-L242). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Keyboard activity in a child module
  @target @RN-W030
  Scenario: RN-W030
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a source-bound textbox in active W-A
    And at least 30 seconds of access remain
    When User A enters keyboard input every 100 milliseconds for 15 seconds
    Then at least one completed renewal is accepted before the interval ends
    And the protected fixture accepts the installed current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W031

**Scroll activity inside a workspace grid**

Use case: [UC-W06](03-use-cases-renewal.md#uc-w06). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201)

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [REQ-active-session-renewal.md](evidence/comprehensive-renewal-20261028/sources/3db69ca6827b/REQ-active-session-renewal.md#L165-L242). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Scroll activity inside a workspace grid
  @target @RN-W031
  Scenario: RN-W031
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a source-bound scrollable grid in active W-A
    And at least 30 seconds of access remain
    When User A scrolls the grid every 100 milliseconds for 15 seconds
    Then at least one completed renewal is accepted before the interval ends
    And the protected fixture accepts the installed current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-W032

**Read-only monitoring of inactive workspace updates**

Use case: [UC-W06](03-use-cases-renewal.md#uc-w06). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Read-only monitoring of inactive workspace updates
  @policy_open @RN-W032
  Scenario: RN-W032
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A active and W-B hidden
    And W-B receives passive server notifications without user interaction
    When the controlled clock crosses the access deadline while notifications continue
    Then the result records renewal counts and access-validation outcomes
    And the result records that no native user input occurred
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Passive server notifications and hidden-workspace activity eligibility remain undefined.

Acceptance: BLOCKED. Policy gap: Passive server notifications and hidden-workspace activity eligibility remain undefined.

### RN-Q001

**Two workspaces keep shared loading until both requests finish**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Two workspaces keep shared loading until both requests finish
  @observed @RN-Q001
  Scenario: RN-Q001
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A and W-B mounted
    And W-A and W-B each start one loading-enabled request
    When the W-A request completes
    And the driver keeps the W-B request held
    Then global loading equals true
    And the W-A completed result is retained
    And W-B remains pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q002

**Final workspace request completion clears loading after renewal**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Final workspace request completion clears loading after renewal
  @observed @RN-Q002
  Scenario: RN-Q002
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one held loading-enabled W-A request
    And the session completes one successful renewal
    When the driver completes the W-A request
    Then global loading equals false
    And the next protected fixture request uses current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q003

**Silent renewal cannot clear a workspace loader**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Silent renewal cannot clear a workspace loader
  @observed @RN-Q003
  Scenario: RN-Q003
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a held loading-enabled W-A request
    When the current session completes one successful renewal
    Then global loading remains true
    And the W-A request remains pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q004

**Cancel one workspace request while another remains pending**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Cancel one workspace request while another remains pending
  @observed @RN-Q004
  Scenario: RN-Q004
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has held loading-enabled requests from W-A and W-B
    When the driver aborts the W-A request
    Then the W-A request rejects with cancellation
    And global loading remains true
    And the W-B request remains pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q005

**Cancel final workspace request after renewal**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Cancel final workspace request after renewal
  @observed @RN-Q005
  Scenario: RN-Q005
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one held loading-enabled W-A request
    And the session completes one successful renewal
    When the driver aborts the W-A request
    Then the request rejects with cancellation
    And global loading equals false
    And current access remains installed
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q006

**Old-session request cannot clear replacement-session loader**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Old-session request cannot clear replacement-session loader
  @observed @RN-Q006
  Scenario: RN-Q006
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A session A has one held loading-enabled request
    And a fresh login installs session B
    And session B starts a held loading-enabled W-B request
    When the driver delivers session A response
    Then session A response is rejected as ended-session work
    And global loading remains true
    And session B token identity remains unchanged
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q007

**Old-session cancellation cannot clear replacement loader**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Old-session cancellation cannot clear replacement loader
  @observed @RN-Q007
  Scenario: RN-Q007
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A session A has one held loading-enabled request
    And a fresh login installs session B
    And session B has one held loading-enabled request
    When the driver aborts session A request
    Then global loading remains true
    And session B request remains pending
    And session B credential identity remains unchanged
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q008

**Response parsing error releases final loader**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Response parsing error releases final loader
  @observed @RN-Q008
  Scenario: RN-Q008
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one loading-enabled response using a supported response transform
    When the fixture returns a payload that makes the transform throw
    Then the caller receives a rejected result
    And global loading equals false
    And the access credential identity remains unchanged
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q009

**Response parsing error preserves another pending loader**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Response parsing error preserves another pending loader
  @observed @RN-Q009
  Scenario: RN-Q009
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has two loading-enabled requests pending
    And one request uses a supported transform that throws
    When the fixture completes only the throwing response
    Then the caller receives a rejected result
    And global loading remains true
    And the second request remains pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q010

**Renewal failure does not complete a workspace request**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal failure does not complete a workspace request
  @observed @RN-Q010
  Scenario: RN-Q010
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a loading-enabled W-A request held
    And the renewal endpoint can return a synthetic network failure
    When the renewal endpoint fails
    Then the W-A request remains pending
    And global loading remains true
    And the W-A caller receives zero successful completions
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q011

**Expired-token error during loading retains actual cleanup sequence**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Expired-token error during loading retains actual cleanup sequence
  @observed @RN-Q011
  Scenario: RN-Q011
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one held loading-enabled request
    And the fixture can return TOKEN_INVALID_EXPIRED
    When the fixture returns the expired-token error
    Then the result records credential clearing and session epoch changes
    And the result records global loading and PageLoader states before and after login rendering
    And the caller receives a rejected result
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q012

**Workspace request completes after Logout starts**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Workspace request completes after Logout starts
  @proposed_security @RN-Q012
  Scenario: RN-Q012
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one held protected W-A request
    And the session dialog is visible
    When User A clicks button Logout in dialog Your session has been expired
    And the driver delivers the W-A response
    Then the response does not install ended-session credentials
    And no new protected W-A fixture row appears after logout completes
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-Q013

**Module loading and request loading remain independent**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [Container.tsx](evidence/comprehensive-renewal-20261028/sources/c724d38617a9/Container.tsx#L10-L35); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Module loading and request loading remain independent
  @observed @RN-Q013
  Scenario: RN-Q013
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a W-A module import held
    And W-B starts one loading-enabled request
    When the driver completes the W-B request
    Then global loading equals false
    And W-A import remains pending
    And the result records W-A Suspense fallback state separately
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q014

**Loader false header preserves current credential assignment**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Loader false header preserves current credential assignment
  @observed @RN-Q014
  Scenario: RN-Q014
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a current valid access credential
    And W-A uses the shared HTTP client
    When W-A sends a protected request with show-loading header equal to false
    Then the outbound authorization header identifies current access
    And global loading remains false when no other request is pending
    And the response principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q015

**Loader query suppression does not bypass authentication**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Loader query suppression does not bypass authentication
  @observed @RN-Q015
  Scenario: RN-Q015
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has current valid access
    And W-A uses the shared HTTP client
    When W-A sends a protected request with query loader=false
    Then the outbound authorization header identifies current access
    And the protected service authenticates User A
    And global loading remains false when no other request is pending
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q016

**Concurrent workspace loaders settle in every order**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Concurrent workspace loaders settle in every order
  @observed @RN-Q016
  Scenario: RN-Q016
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A starts three loading-enabled requests with unique IDs
    And the fixture defines all six completion orders
    When the driver completes requests in the selected order
    Then global loading equals true after the first and second completions
    And global loading equals false after the third completion
    And each caller receives only its own request ID
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q017

**Navigation removes a loading module during pending renewal**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/492b70185cf2/index.tsx#L13-L46); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Navigation removes a loading module during pending renewal
  @proposed_security @RN-Q017
  Scenario: RN-Q017
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has W-A loading and W-B available
    And W-A mutation operation M-1 is not yet submitted
    When User A selects the W-B workspace tab
    And the session completes one successful renewal
    Then the service mutation count for M-1 equals zero
    And the selected workspace ID equals W-B
    And no W-A data appears in the W-B panel
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-Q018

**Retry after loading error uses current access**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L8-L51); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Retry after loading error uses current access
  @observed @RN-Q018
  Scenario: RN-Q018
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a W-A request that failed with a synthetic network error
    And the session completes one successful renewal
    When the driver invokes the source-bound W-A retry action once
    Then the retried request authorization identity equals current access
    And the protected fixture principal equals User A
    And the retry request count equals one
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-Q019

**Renewal wait does not resubmit a financial mutation**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal wait does not resubmit a financial mutation
  @proposed_security @RN-Q019
  Scenario: RN-Q019
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A submits mutation M-1 once from W-A
    And the service commits M-1 but holds its response
    When the session completes one successful renewal
    And the driver releases M-1 response
    Then the server commit count for M-1 equals one
    And the client submission count for M-1 equals one
    And the mutation audit principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-Q020

**Progress events are observed separately from activity policy**

Use case: [UC-W02](03-use-cases-renewal.md#uc-w02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L9-L42); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Progress events are observed separately from activity policy
  @policy_open @RN-Q020
  Scenario: RN-Q020
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a long loading-enabled request
    And the fixture emits progress events without native user input
    When the controlled clock crosses the access deadline
    Then the result records progress events, renewal outcomes, and credential identities
    And the result records zero native user-input events
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Transfer progress eligibility as session activity is not defined.

Acceptance: BLOCKED. Policy gap: Transfer progress eligibility as session activity is not defined.

### RN-T001

**GraphQL reconnect reads renewed access**

Use case: [UC-T01](03-use-cases-renewal.md#uc-t01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: GraphQL reconnect reads renewed access
  @observed @RN-T001
  Scenario: RN-T001
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has an established GraphQL subscription
    And the session completes one successful renewal
    When the fixture disconnects the GraphQL socket
    And the client reconnects
    Then the new connection handshake identity equals current access
    And the server authenticates User A on the new connection
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-T002

**STOMP reconnect reads renewed storage access**

Use case: [UC-T01](03-use-cases-renewal.md#uc-t01). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: STOMP reconnect reads renewed storage access
  @observed @RN-T002
  Scenario: RN-T002
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has an established cashflow STOMP connection
    And renewal replaces SET_TOKEN with current access
    When the fixture rejects the old STOMP connection
    And the client reconnects
    Then the new CONNECT header identity equals current SET_TOKEN access
    And the server authenticated principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-T003

**Existing socket across access expiry**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Existing socket across access expiry
  @policy_open @RN-T003
  Scenario: RN-T003
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has an authenticated established GraphQL socket
    And no native user input occurs
    When the controlled clock crosses tE
    And the server emits one protected fixture message
    Then the result records socket close events and message delivery with timestamps
    And the result records the connection principal and access-expiry boundary
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Established-socket authorization lifetime and mid-connection reauthentication requirements need transport-owner review.

Acceptance: BLOCKED. Policy gap: Established-socket authorization lifetime and mid-connection reauthentication requirements need transport-owner review.

### RN-T004

**STOMP heartbeat alone across expiry**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: STOMP heartbeat alone across expiry
  @policy_open @RN-T004
  Scenario: RN-T004
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has an established STOMP connection
    And only STOMP heartbeats occur
    When the controlled clock crosses tE
    Then the result records heartbeat count and renewal count separately
    And the result records access-validation results and socket closure events
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: STOMP heartbeats are not defined as eligible human activity.

Acceptance: BLOCKED. Policy gap: STOMP heartbeats are not defined as eligible human activity.

### RN-T005

**Protected server messages alone across expiry**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Protected server messages alone across expiry
  @policy_open @RN-T005
  Scenario: RN-T005
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A receives GraphQL subscription messages
    And no native user input occurs
    When the controlled clock crosses tE
    Then the result records delivered message IDs and renewal outcomes
    And the result records zero native user-input events
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Server-pushed data is not defined as eligible human activity.

Acceptance: BLOCKED. Policy gap: Server-pushed data is not defined as eligible human activity.

### RN-T006

**Socket reconnect after local logout**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Socket reconnect after local logout
  @proposed_security @RN-T006
  Scenario: RN-T006
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has an established GraphQL socket
    And the server can force a disconnect
    When User A logs out
    And the server disconnects the socket
    Then no reconnect authenticates with usable ended-session credentials
    And the protected server returns zero authorized protected messages after logout
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T007

**STOMP delayed retry after local logout**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: STOMP delayed retry after local logout
  @proposed_security @RN-T007
  Scenario: RN-T007
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has one pending STOMP reconnect callback
    When User A logs out
    And the driver releases the queued reconnect callback
    Then the server records no successful ended-session authentication
    And zero protected fixture messages reach a signed-out UI
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T008

**Socket reconnect after account change**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Socket reconnect after account change
  @proposed_security @RN-T008
  Scenario: RN-T008
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a socket and a pending reconnect
    And User B lacks User A trade entitlement
    When User A logs out
    And User B signs in
    And the driver releases reconnect
    Then the handshake principal is User B or the handshake is denied
    And the delivered protected message count for User A-only trade X equals zero
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T009

**Queued socket callback after account change**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Queued socket callback after account change
  @proposed_security @RN-T009
  Scenario: RN-T009
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A socket callback holds a message containing User A-only trade X
    When User B signs in
    And the driver delivers the held callback
    Then User B UI contains zero trade X records
    And no User B mutation is triggered by the User A callback
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T010

**Reconnect during pending manual renewal**

Use case: [UC-T01](03-use-cases-renewal.md#uc-t01). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reconnect during pending manual renewal
  @proposed_security @RN-T010
  Scenario: RN-T010
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has expired access and usable refresh
    And manual renewal and socket reconnect are held
    When the fixture completes manual renewal
    And the driver releases the socket reconnect
    Then the new handshake uses the installed current access
    And the protected service principal equals User A
    And the dialog closes once after renewal completion
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T011

**Two workspace subscriptions use distinct topics**

Use case: [UC-T03](03-use-cases-renewal.md#uc-t03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Two workspace subscriptions use distinct topics
  @proposed_security @RN-T011
  Scenario: RN-T011
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A and W-B have authorized but distinct subscription topics
    And both sockets reconnect after renewal
    When the server sends message A to W-A topic
    And the server sends message B to W-B topic
    Then W-A receives only message A
    And W-B receives only message B
    And both handshakes identify User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T012

**Same URL reconnect isolation across workspaces**

Use case: [UC-T03](03-use-cases-renewal.md#uc-t03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Same URL reconnect isolation across workspaces
  @proposed_security @RN-T012
  Scenario: RN-T012
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A and W-B have subscriptions using the same GraphQL URL
    And the fixture records individual connection IDs
    When the server repeatedly disconnects only W-A
    Then the result retains separate retry counts per connection
    And W-B receives its expected fixture message without duplicate delivery
    And the result identifies any URL-shared retry effects
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T013

**STOMP destination deduplication on reconnect**

Use case: [UC-T03](03-use-cases-renewal.md#uc-t03). Level: `browser-e2e`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: STOMP destination deduplication on reconnect
  @observed @RN-T013
  Scenario: RN-T013
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A subscribes twice to one destination using the same client UID
    When the fixture completes the second connection callback
    And the server publishes message N-1 once
    Then the client subscription map contains one entry for that destination
    And the previous subscription receives one unsubscribe call
    And the result records callback and acknowledgement counts for N-1
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN.

### RN-T014

**Reconnect message delivery requires deduplication review**

Use case: [UC-T04](03-use-cases-renewal.md#uc-t04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reconnect message delivery requires deduplication review
  @policy_open @RN-T014
  Scenario: RN-T014
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A received message N-1 before disconnect
    And the fixture replays N-1 after reconnect
    When the server delivers the replayed message
    Then the result records callback counts and UI row counts for N-1
    And the result records acknowledgement identities
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Exactly-once UI delivery and reconnect replay policy is unavailable.

Acceptance: BLOCKED. Policy gap: Exactly-once UI delivery and reconnect replay policy is unavailable.

### RN-T015

**Missed-message recovery after renewal reconnect**

Use case: [UC-T04](03-use-cases-renewal.md#uc-t04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Missed-message recovery after renewal reconnect
  @policy_open @RN-T015
  Scenario: RN-T015
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A disconnects after message N-1
    And the server publishes N-2 while disconnected
    When the session renews
    And the socket reconnects
    Then the result records whether N-2 is replayed or recovered by a query
    And the result retains message sequence numbers and data-query requests
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Missed-message replay, resynchronization, and permitted data-loss policy is unavailable.

Acceptance: BLOCKED. Policy gap: Missed-message replay, resynchronization, and permitted data-loss policy is unavailable.

### RN-T016

**STOMP invalid JSON does not cross identity boundaries**

Use case: [UC-T03](03-use-cases-renewal.md#uc-t03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: STOMP invalid JSON does not cross identity boundaries
  @proposed_security @RN-T016
  Scenario: RN-T016
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a connected STOMP subscription
    And the server can send malformed message JSON
    When the server sends malformed JSON
    And the session completes one successful renewal
    Then no synthetic mutation is committed from malformed input
    And the credential identity remains the renewed identity
    And the result records the parse error and acknowledgement count
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T017

**Socket unauthorized topic is rejected after renewal**

Use case: [UC-T03](03-use-cases-renewal.md#uc-t03). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Socket unauthorized topic is rejected after renewal
  @proposed_security @RN-T017
  Scenario: RN-T017
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A is denied fixture topic restricted-B
    And current access is usable
    When the client subscribes to restricted-B after renewal
    Then the server grants zero subscriptions to restricted-B
    And zero protected restricted-B payloads reach the client
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T018

**Revocation reaches an established socket**

Use case: [UC-T02](03-use-cases-renewal.md#uc-t02). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Revocation reaches an established socket
  @proposed_security @RN-T018
  Scenario: RN-T018
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a socket authenticated before entitlement revocation
    When the authorization fixture revokes User A access to topic X
    And the server attempts to emit protected topic X data
    Then the authorization log records no post-revocation grant for topic X
    And the result measures any delivered post-revocation messages separately
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T019

**WebSocket connection credentials avoid URL leakage**

Use case: [UC-T01](03-use-cases-renewal.md#uc-t01). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: WebSocket connection credentials avoid URL leakage
  @proposed_security @RN-T019
  Scenario: RN-T019
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A establishes GraphQL and STOMP test connections
    And network capture redacts all credential values
    When the session renews
    And both clients reconnect
    Then request URLs contain zero access or refresh credential values
    And navigation history contains zero access or refresh credential values
    And the handshake identity is recorded only as a hash
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T020

**Socket authentication failure is not renewal success**

Use case: [UC-T01](03-use-cases-renewal.md#uc-t01). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Socket authentication failure is not renewal success
  @proposed_security @RN-T020
  Scenario: RN-T020
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A socket reconnect receives an authentication rejection
    And a separate renewal response is held
    When the fixture delivers the socket error
    Then successful renewal count remains zero before renewal completion
    And the result records the socket error separately from the renewal promise
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T021

**Long poll started before renewal completes after renewal**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Long poll started before renewal completes after renewal
  @proposed_security @RN-T021
  Scenario: RN-T021
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A starts protected long poll P-1 with old current access
    And the fixture holds its response
    When the session completes one successful renewal
    And the fixture releases P-1 response
    Then the result binds P-1 response to its request credential and principal
    And no protected response is attributed to another principal
    And a new poll uses installed current access
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T022

**Long poll crosses a logout boundary**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Long poll crosses a logout boundary
  @proposed_security @RN-T022
  Scenario: RN-T022
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has protected long poll P-1 held
    When User A logs out
    And the fixture releases P-1 response
    Then the ended-session response is rejected by the shared client
    And zero P-1 protected rows appear after logout completes
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T023

**SSE stream authentication lifecycle inventory**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: SSE stream authentication lifecycle inventory
  @policy_open @RN-T023
  Scenario: RN-T023
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And the target owner identifies a real protected SSE consumer or records that none is available
    And the isolated SSE peer records principal and event IDs
    When the session renews while that stream is open
    Then the result records consumer identity, stream lifetime, and event IDs
    And the result records authentication at stream establishment and after any reconnect
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: No EventSource consumer or SSE authentication renewal contract was established in inspected shell sources.

Acceptance: BLOCKED. Policy gap: No EventSource consumer or SSE authentication renewal contract was established in inspected shell sources.

### RN-T024

**SSE Last-Event-ID does not grant another identity access**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: SSE Last-Event-ID does not grant another identity access
  @proposed_security @RN-T024
  Scenario: RN-T024
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has last-event identifier E-A
    And User B lacks access to User A stream
    When User B opens the isolated SSE peer with Last-Event-ID equal to E-A
    Then the server returns zero User A-only events to User B
    And the server authorization record identifies User B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T025

**Large download across renewal**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Large download across renewal
  @policy_open @RN-T025
  Scenario: RN-T025
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A starts isolated protected download D-1
    And the fixture records expected content hash and download principal
    When the session completes one successful renewal
    And the download finishes
    Then the result records received byte count and content hash
    And the result records request principal and any restart requests
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Download continuation, partial-content resume, and restart policy is unavailable.

Acceptance: BLOCKED. Policy gap: Download continuation, partial-content resume, and restart policy is unavailable.

### RN-T026

**Upload is committed once across renewal**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Upload is committed once across renewal
  @proposed_security @RN-T026
  Scenario: RN-T026
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A uploads synthetic file F-1 using operation ID U-1
    And the server holds the final acknowledgement
    When the session completes one successful renewal
    And the server releases the acknowledgement
    Then the server commit count for U-1 equals one
    And the stored file hash equals the fixture hash
    And the audit principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T027

**Upload cancellation across logout**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Upload cancellation across logout
  @proposed_security @RN-T027
  Scenario: RN-T027
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has a partial isolated upload U-2
    And the fixture has not committed U-2
    When User A logs out
    And the driver attempts to resume U-2 with ended-session credentials
    Then the server accepts zero resume requests using ended-session access
    And the result records U-2 final commit count and temporary-object disposition
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T028

**Worker retains no ended-session authority**

Use case: [UC-T06](03-use-cases-renewal.md#uc-t06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Worker retains no ended-session authority
  @proposed_security @RN-T028
  Scenario: RN-T028
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And an isolated worker has a held protected request from session A
    And the fixture records worker and request identities
    When session A logs out
    And the driver releases the worker callback
    Then the server accepts zero new requests with ended-session authority
    And no ended-session result installs session credentials in the UI
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T029

**Service worker cached protected response after account change**

Use case: [UC-T06](03-use-cases-renewal.md#uc-t06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Service worker cached protected response after account change
  @proposed_security @RN-T029
  Scenario: RN-T029
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A accessed synthetic protected response R-A
    And the isolated target has a declared service worker or records that none is available
    When User A logs out
    And User B signs in
    And the driver requests the same protected resource offline
    Then User B receives zero User A-only protected records
    And the result records service-worker presence and response cache provenance
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-T030

**TLS interruption is distinct from session rejection**

Use case: [UC-T05](03-use-cases-renewal.md#uc-t05). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [graphql.ts](evidence/comprehensive-renewal-20261028/sources/599f6e52a683/graphql.ts#L126-L240); [stomp.ts](evidence/comprehensive-renewal-20261028/sources/181b11c48c6f/stomp.ts#L26-L141); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: TLS interruption is distinct from session rejection
  @proposed_security @RN-T030
  Scenario: RN-T030
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has protected socket and long-request connections
    And the fixture can cause a TLS connection failure without changing credentials
    When the fixture interrupts the connections
    Then the client records zero successful renewals from connection failure
    And no fallback request transmits credentials over plaintext HTTP or WS
    And the result records transport errors separately from authentication rejections
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D001

**Two same-origin tabs renew concurrently**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Two same-origin tabs renew concurrently
  @policy_open @RN-D001
  Scenario: RN-D001
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A opens B-A and B-B in one isolated browser profile
    And both tabs have one shared stored access identity
    And the fixture can hold both renewal responses
    When both tabs trigger their own renewal
    And the driver delivers the responses in reverse request order
    Then the result records each tab provider credential hash and the final stored credential hash
    And the protected service records validation of each tab credential
    And the result records renewal request count per tab
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Cross-tab renewal coordination and response-order precedence are not defined.

Acceptance: BLOCKED. Policy gap: Cross-tab renewal coordination and response-order precedence are not defined.

### RN-D002

**Renewal in one tab leaves another tab idle**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Renewal in one tab leaves another tab idle
  @policy_open @RN-D002
  Scenario: RN-D002
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A opens B-A and B-B on one origin
    And B-B has no native user activity
    When B-A completes one successful renewal
    And the clock crosses B-B original access expiry
    Then the result records each tab provider and storage credential hashes
    And the result records each tab dialog state and protected validation outcome
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Cross-tab credential synchronization and idle-policy scope are not defined.

Acceptance: BLOCKED. Policy gap: Cross-tab credential synchronization and idle-policy scope are not defined.

### RN-D003

**Logout in one tab affects another active tab**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Logout in one tab affects another active tab
  @policy_open @RN-D003
  Scenario: RN-D003
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A opens B-A and B-B on one origin
    And B-B has an active protected workspace
    When User A logs out from B-A
    And B-B attempts one protected request
    Then the result records storage changes and provider credentials separately for each tab
    And the result records B-B protected response and principal
    And the result records any cross-tab logout notification
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Global versus local logout scope lacks an inspected target acceptance contract.

Acceptance: BLOCKED. Policy gap: Global versus local logout scope lacks an inspected target acceptance contract.

### RN-D004

**Separate browser profiles retain isolated identities**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Separate browser profiles retain isolated identities
  @proposed_security @RN-D004
  Scenario: RN-D004
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A uses browser profile P-A
    And User B uses separate profile P-B
    And User B lacks User A trade access
    When User A completes one successful renewal
    And User B requests User A-only trade X
    Then P-B stores zero User A credentials
    And the server returns zero trade X records to User B
    And the P-A protected principal equals User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D005

**Private browser context cannot inherit regular context access**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Private browser context cannot inherit regular context access
  @proposed_security @RN-D005
  Scenario: RN-D005
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A is authenticated in regular browser context C-A
    And private context C-B has empty isolated storage
    When the driver opens the portal in C-B
    Then C-B contains zero User A access or refresh credentials
    And C-B receives zero User A protected records before its own authentication
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D006

**Duplicate tab with copied session storage**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Duplicate tab with copied session storage
  @policy_open @RN-D006
  Scenario: RN-D006
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A uses B-A with populated W-A
    And the browser duplicate-tab operation copies browser-defined state
    When the driver duplicates B-A into B-B
    And B-A completes one successful renewal
    Then the result records storage types and credential hashes in both tabs
    And the result records workspace IDs and protected validation results in B-B
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Browser duplicate-tab storage semantics and workspace duplication policy require a supported-browser contract.

Acceptance: BLOCKED. Policy gap: Browser duplicate-tab storage semantics and workspace duplication policy require a supported-browser contract.

### RN-D007

**Back navigation after logout exposes no accepted protected request**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Back navigation after logout exposes no accepted protected request
  @proposed_security @RN-D007
  Scenario: RN-D007
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A visited W-A before logout
    And the fixture can restore browser history or back-forward cache
    When User A logs out
    And the driver navigates Back to the prior portal entry
    Then the protected service accepts zero ended-session requests
    And the result records whether a restored page displays cached protected content
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D008

**Focus returns after another tab changed identity**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Focus returns after another tab changed identity
  @proposed_security @RN-D008
  Scenario: RN-D008
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And B-A contains User A workspace state
    And B-B on the same origin signs in as User B
    And User B lacks User A trade access
    When the driver focuses B-A
    And B-A sends a protected request
    Then the server returns zero User A-only trade X records to User B
    And the result records B-A provider identity and storage identity separately
    And no mismatched principal is accepted as User A
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D009

**Close the renewal-owning browser tab**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Close the renewal-owning browser tab
  @policy_open @RN-D009
  Scenario: RN-D009
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And B-A and B-B share an origin
    And B-A has a held renewal request
    When the driver closes B-A
    And the driver releases its server-side response
    Then the result records whether B-B observes any credential installation
    And the result records B-B validation and dialog state
    And the server records whether the closed-tab request completed
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Cross-tab renewal ownership after tab closure is not defined.

Acceptance: BLOCKED. Policy gap: Cross-tab renewal ownership after tab closure is not defined.

### RN-D010

**Multiple portal windows contend for storage**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Multiple portal windows contend for storage
  @policy_open @RN-D010
  Scenario: RN-D010
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A opens two portal windows on one origin
    And each window contains two populated workspaces
    When both windows complete renewal in controlled opposite response orders
    Then the result records credential hashes per provider and shared storage
    And the result records selected workspace IDs in both windows
    And the server records each request principal
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Multi-window storage synchronization and workspace persistence policy are not defined.

Acceptance: BLOCKED. Policy gap: Multi-window storage synchronization and workspace persistence policy are not defined.

### RN-D011

**Cross-origin iframe interaction across expiry**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Cross-origin iframe interaction across expiry
  @policy_open @RN-D011
  Scenario: RN-D011
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A embeds a declared cross-origin child fixture
    And the child has no permission to read parent storage
    And native input occurs only inside the child
    When the clock crosses parent access expiry
    Then the result records parent renewal outcomes and child-origin input events
    And the child reads zero parent credential values
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Cross-origin child input eligibility needs an explicit parent-child activity contract.

Acceptance: BLOCKED. Policy gap: Cross-origin child input eligibility needs an explicit parent-child activity contract.

### RN-D012

**Same-origin iframe does not confuse session principal**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Same-origin iframe does not confuse session principal
  @proposed_security @RN-D012
  Scenario: RN-D012
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And W-A embeds an isolated same-origin child fixture
    And the child holds a session A response
    When a fresh session B login completes
    And the driver releases the child response
    Then the session B installed credential identity remains unchanged
    And no session A response is treated as a session B protected result
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Proposed security or data-integrity invariant; owner review remains pending. No new business AC is asserted.

### RN-D013

**Browser restart after persisted credentials expire**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [useController.ts](evidence/comprehensive-renewal-20261028/sources/4c8ad5b55b0e/useController.ts#L32-L299); [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L24-L155); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L20-L59). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Browser restart after persisted credentials expire
  @policy_open @RN-D013
  Scenario: RN-D013
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And User A has saved workspace descriptors
    And all persisted access and refresh credentials expire before restart
    When the driver restarts the isolated browser
    And the driver opens the portal
    Then the server accepts zero expired-credential requests
    And the result records sign-in, dialog, and workspace states separately
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Absent-credential recovery and persisted-workspace restoration remain unresolved.

Acceptance: BLOCKED. Policy gap: Absent-credential recovery and persisted-workspace restoration remain unresolved.

### RN-D014

**Two portal roots in one document expose component scope gaps**

Use case: [UC-W07](03-use-cases-renewal.md#uc-w07). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L19-L127); [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L17-L48); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L59); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L111). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Two portal roots in one document expose component scope gaps
  @policy_open @RN-D014
  Scenario: RN-D014
    Given the isolated synthetic User A fixture and cleanup procedure are configured
    And the isolated host embeds two portal root instances
    And each root has its own source-bound workspaces tablist
    When one root completes renewal
    And the other root reaches access expiry
    Then the result records each root provider credential hash and dialog state
    And the result records duplicate test IDs and accessibility labels
    And the server records each request principal
    And the result marks business acceptance BLOCKED and links the unresolved policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Source-derived component identity; runtime uniqueness and automation binding remain UNVERIFIED. Definition only; execution_status=NOT_RUN. Acceptance BLOCKED: Multiple portal roots per document are not established as a supported composition.

Acceptance: BLOCKED. Policy gap: Multiple portal roots per document are not established as a supported composition.

### RN-S001

**Reject refresh replay after valid-access logout**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject refresh replay after valid-access logout
  @observed @RN-S001
  Scenario: RN-S001
    Given Synthetic user A has unexpired access A and refresh A
    When A submits POST /v2/sso/logout with access A
    And A submits POST /v2/sso/relogin with refresh A
    Then The logout response has result true
    And The relogin response has HTTP status 401
    And The relogin response issues zero access credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S002

**Reject refresh replay after expired-access logout**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L23-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject refresh replay after expired-access logout
  @proposed_security @RN-S002
  Scenario: RN-S002
    Given Synthetic user A has expired access A and unexpired refresh A
    When A submits POST /v2/sso/logout with access A
    And A submits POST /v2/sso/relogin with refresh A
    Then The relogin response issues zero access credentials
    And The session revocation observation identifies the logout outcome
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `FAILED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S003

**Record logout failure when the revocation store fails**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Record logout failure when the revocation store fails
  @policy_open @RN-S003
  Scenario: RN-S003
    Given A has renewable credentials
    And The isolated revocation repository rejects writes
    When A submits logout
    And A attempts relogin with the copied refresh credential
    Then The recorded response and revocation-store result identify the failed write
    And The security result reports whether renewed access was issued
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Logout failure semantics and retry policy are unresolved. Acceptance is blocked; record observations without inventing an error code.

### RN-S004

**Revoke the session when logout has no access but retains refresh**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L23-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Revoke the session when logout has no access but retains refresh
  @policy_open @RN-S004
  Scenario: RN-S004
    Given A has only an unexpired refresh credential
    When A requests logout
    And A replays the copied refresh credential
    Then The security result records whether revocation occurred
    And The security result records the relogin status and issued-access count
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No-refresh logout or provider revocation contract is unavailable. Acceptance is blocked.

### RN-S005

**Discard renewal success delivered after client logout**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Discard renewal success delivered after client logout
  @proposed_security @RN-S005
  Scenario: RN-S005
    Given A has a relogin response held before client delivery
    When A selects Logout
    And The fixture releases the held relogin success
    Then The browser access credential remains absent
    And The browser authenticated user remains absent
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S006

**Reject server renewal after the session enters the deny list**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject server renewal after the session enters the deny list
  @observed @RN-S006
  Scenario: RN-S006
    Given A has valid refresh A
    And The server deny list contains A session identifier
    When A submits POST /v2/sso/relogin with refresh A
    Then The response has HTTP status 401
    And The response issues zero access credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S007

**Resolve simultaneous server logout and relogin**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Resolve simultaneous server logout and relogin
  @policy_open @RN-S007
  Scenario: RN-S007
    Given A has valid refresh A
    And The fixture can hold the revocation write and renewal validation
    When A submits logout
    And A submits relogin
    And The fixture releases both operations in each order
    Then The result records the validation and revocation commit order
    And The result records every issued access credential and its session identifier
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Revocation linearization and treatment of already accepted renewal are unresolved. Acceptance is blocked.

### RN-S008

**Reject revoked access when acquiring refresh**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject revoked access when acquiring refresh
  @observed @RN-S008
  Scenario: RN-S008
    Given The deny list contains the session identifier in otherwise valid access A
    When A submits POST /v2/sso/refreshtoken with access A
    Then The response has HTTP status 401
    And The response issues zero refresh credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S009

**Characterize replay of a replaced refresh credential**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Characterize replay of a replaced refresh credential
  @policy_open @RN-S009
  Scenario: RN-S009
    Given A has refresh R1
    And A obtains refresh R2 for the same session
    When A submits relogin with R1
    Then The record identifies whether R1 remains accepted
    And The record identifies both refresh expiry values
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Single-use rotation and replay detection are not specified. Do not assume replacement revokes R1. Acceptance is blocked.

### RN-S010

**Propagate revocation across service replicas**

Use case: [UC-S01](03-use-cases-renewal.md#uc-s01). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/09d8595302dd/JwtTokenUtil.java#L82-L103). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Propagate revocation across service replicas
  @policy_open @RN-S010
  Scenario: RN-S010
    Given A has valid refresh A
    And Two isolated replicas share the declared revocation system
    When A logs out through replica 1
    And A submits relogin through replica 2
    Then Replica 2 issues zero access credentials after the declared revocation completion point
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: The revocation completion point and replica consistency contract are unresolved. Acceptance is blocked.

### RN-S011

**Reject expired refresh**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject expired refresh
  @observed @RN-S011
  Scenario: RN-S011
    Given An isolated issuer supplies an RSA-valid refresh credential expired before server receipt
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S012

**Reject a modified refresh signature**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject a modified refresh signature
  @observed @RN-S012
  Scenario: RN-S012
    Given An isolated issuer supplies a refresh credential with one modified signature byte
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S013

**Reject access credentials in the refresh slot**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject access credentials in the refresh slot
  @observed @RN-S013
  Scenario: RN-S013
    Given An isolated issuer supplies an RSA-valid access credential in Single-UI-Refresh
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S014

**Reject entitlement credentials in the refresh slot**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject entitlement credentials in the refresh slot
  @observed @RN-S014
  Scenario: RN-S014
    Given An isolated issuer supplies an RSA-valid entitlement credential in Single-UI-Refresh
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S015

**Reject a foreign issuer with a valid test signature**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject a foreign issuer with a valid test signature
  @observed @RN-S015
  Scenario: RN-S015
    Given An isolated issuer supplies an RSA-valid credential with issuer foreign-test-issuer
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S016

**Reject unsigned refresh credentials**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject unsigned refresh credentials
  @observed @RN-S016
  Scenario: RN-S016
    Given An isolated issuer supplies a JWT with alg none and an empty signature
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S017

**Reject a malformed refresh envelope**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject a malformed refresh envelope
  @observed @RN-S017
  Scenario: RN-S017
    Given An isolated issuer supplies a two-segment malformed JWT in Single-UI-Refresh
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S018

**Reject expired access during refresh acquisition**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject expired access during refresh acquisition
  @observed @RN-S018
  Scenario: RN-S018
    Given An isolated issuer supplies an RSA-valid access credential expired before server receipt
    When A submits POST /v2/sso/refreshtoken
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S019

**Reject refresh credentials during access-based acquisition**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject refresh credentials during access-based acquisition
  @observed @RN-S019
  Scenario: RN-S019
    Given An isolated issuer supplies an RSA-valid refresh credential as singleUIAuthorization
    When A submits POST /v2/sso/refreshtoken
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S020

**Reject a future not-before claim**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject a future not-before claim
  @observed @RN-S020
  Scenario: RN-S020
    Given An isolated issuer supplies an RSA-valid refresh credential whose nbf exceeds server time
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access or refresh credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S021

**Reject missing refresh input**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `observed`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject missing refresh input
  @observed @RN-S021
  Scenario: RN-S021
    Given The request has no Single-UI-Refresh header
    When A submits POST /v2/sso/relogin
    Then The response has HTTP status 401
    And The response issues zero access credentials
```

Assertion binding: See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.

Execution: `PASSED`. Limits: Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.

Results: [retained execution](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

### RN-S022

**Characterize a correctly signed refresh without expiry**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383); [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/c5cb0cb4a7a0/JwtTokenUtil.java#L87-L98). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Characterize a correctly signed refresh without expiry
  @policy_open @RN-S022
  Scenario: RN-S022
    Given The isolated issuer signs a refresh credential without exp
    When A submits POST /v2/sso/relogin
    Then The result records HTTP status and issued-access count
    And The result records whether expiry was required by the verifier
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: BFF generation includes exp. Required-claim validation for other signed issuers is unresolved. Acceptance is blocked.

### RN-S023

**Reject conflicting duplicate refresh headers**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject conflicting duplicate refresh headers
  @proposed_security @RN-S023
  Scenario: RN-S023
    Given The isolated HTTP client submits two distinct Single-UI-Refresh headers for users A and B
    When The client submits POST /v2/sso/relogin
    Then The service issues zero access credentials under the proposed ambiguous-input rule
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S024

**Preserve retry after malformed renewal success**

Use case: [UC-S02](03-use-cases-renewal.md#uc-s02). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Preserve retry after malformed renewal success
  @proposed_security @RN-S024
  Scenario: RN-S024
    Given A sees an idle-expiry dialog with usable refresh A
    And The next relogin returns HTTP 200 with an expired access JWT
    When A selects the Extend button in the timeout dialog
    Then The dialog has zero successful closure transitions
    And The expired access credential is not installed
    And The dialog permits another attempt while refresh A remains usable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S025

**Discard old refresh success after account replacement**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Discard old refresh success after account replacement
  @proposed_security @RN-S025
  Scenario: RN-S025
    Given The fixture holds refresh acquisition for user A
    And A fresh login establishes distinct user B
    When The fixture releases A refresh response
    Then The browser refresh credential does not become A refresh
    And The authenticated user remains B
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S026

**Discard old refresh rejection after account replacement**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Discard old refresh rejection after account replacement
  @proposed_security @RN-S026
  Scenario: RN-S026
    Given The fixture holds a failing refresh acquisition for user A
    And A fresh login establishes distinct user B
    When The fixture releases A rejection
    Then The browser access credential remains B access
    And The current user remains B
    And The old error does not clear B authentication
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S027

**Discard old protected success after account replacement**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Discard old protected success after account replacement
  @proposed_security @RN-S027
  Scenario: RN-S027
    Given The fixture holds a protected user A response
    And A fresh login establishes user B
    When The fixture releases A protected response
    Then The A protected payload does not become visible in B workspace
    And The A payload is rejected or discarded by the consuming assertion
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S028

**Protect session B from old timeout callbacks**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Protect session B from old timeout callbacks
  @proposed_security @RN-S028
  Scenario: RN-S028
    Given An old dialog retains Logout and Extend callbacks from A
    And A fresh login establishes B
    When The fixture invokes A retained Logout callback
    And The fixture invokes A retained Extend callback
    Then The session generation remains B generation
    And Zero B logout requests result from A callbacks
    And Zero old dialog closures change B state
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S029

**Detect mixed credentials after direct token replacement**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [login.ts](evidence/comprehensive-renewal-20261028/sources/364c29cab3c1/login.ts#L13-L84); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Detect mixed credentials after direct token replacement
  @policy_open @RN-S029
  Scenario: RN-S029
    Given A has A access and A refresh
    And A verified external caller can dispatch SET_TOKEN directly
    When The caller dispatches B access
    And The client attempts relogin
    Then The security record identifies the retained refresh subject
    And The security record identifies the relogin subject and visible user
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: No supported non-test direct account-switch caller was found. Caller applicability and replacement policy remain unresolved. Acceptance is blocked.

### RN-S030

**Order two concurrent fresh logins**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L110). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Order two concurrent fresh logins
  @proposed_security @RN-S030
  Scenario: RN-S030
    Given The fixture holds successful logins for distinct users A and B
    When The client starts login A
    And The client starts login B
    And The fixture delivers B then A
    Then The later login response cannot overwrite the selected generation
    And The final access subject and user subject are identical
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S031

**Avoid sending session A headers with session B payload**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Avoid sending session A headers with session B payload
  @proposed_security @RN-S031
  Scenario: RN-S031
    Given A has access A
    And The fixture starts a fresh login as B
    When A protected request starts during the transition
    Then The request observation records its generation and authorization subject
    And The protected payload contains zero user A data in a B authenticated view
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S032

**Isolate a failed account-switch attempt**

Use case: [UC-S03](03-use-cases-renewal.md#uc-s03). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37); [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Isolate a failed account-switch attempt
  @policy_open @RN-S032
  Scenario: RN-S032
    Given A has renewable session A
    And The next login as B rejects
    When The client submits login B
    And The client opens A idle recovery
    Then The record identifies current access and refresh subjects
    And The record identifies whether A remains renewable
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Account-switch failure semantics are unresolved. Existing same-user retry evidence does not prove cross-user behavior. Acceptance is blocked.

### RN-S033

**Reject credential-free cross-origin renewal**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject credential-free cross-origin renewal
  @proposed_security @RN-S033
  Scenario: RN-S033
    Given A lower-trust local origin has no portal access or refresh credential
    When The origin submits POST /v2/sso/relogin
    Then The response issues zero access credentials
    And The requesting origin reads zero portal credential headers
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S034

**Characterize cookie-only cross-origin renewal**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Characterize cookie-only cross-origin renewal
  @policy_open @RN-S034
  Scenario: RN-S034
    Given The browser has portal cookies
    And A lower-trust local origin has no explicit refresh credential
    When The origin submits a credentialed fetch to relogin
    Then The record identifies preflight response and actual request delivery
    And The record identifies whether access credentials were issued or exposed
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Effective deployment CORS, cookie, and CSRF configuration is unknown. Acceptance is blocked.

### RN-S035

**Prevent credential forwarding to an external destination**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Prevent credential forwarding to an external destination
  @proposed_security @RN-S035
  Scenario: RN-S035
    Given A uses the shared HTTP service
    And The fixture supplies an HTTPS destination outside declared API origins
    When The caller sends a protected request to the external destination
    Then The external fixture receives zero portal access or refresh credential headers
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S036

**Reject a hostile Origin during WebSocket setup**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject a hostile Origin during WebSocket setup
  @proposed_security @RN-S036
  Scenario: RN-S036
    Given A has valid credentials
    And A lower-trust local origin targets the authorized socket endpoint
    When The origin attempts a WebSocket upgrade
    Then The socket accepts zero authenticated subscriptions under the proposed Origin rule
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S037

**Reject forged skip-header authentication**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject forged skip-header authentication
  @proposed_security @RN-S037
  Scenario: RN-S037
    Given A test SDK service has a configured skip header
    And An untrusted client can reach its public route
    When The client sends the skip header without a JWT
    Then The protected business handler is invoked zero times under the proposed gateway trust rule
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: SDK skip headers are configuration-driven. Trusted gateway stripping and actual deployment exposure remain unknown.

### RN-S038

**Require authorization after workspace restoration**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Require authorization after workspace restoration
  @proposed_security @RN-S038
  Scenario: RN-S038
    Given User B lacks access to application X
    And A stored workspace descriptor names application X
    When B restores the workspace
    And B calls a protected X operation directly
    Then The service returns zero X business records to B
    And The shell exposes zero usable X controls under the proposed permission rule
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S039

**Reject tampered identity headers**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118); [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject tampered identity headers
  @proposed_security @RN-S039
  Scenario: RN-S039
    Given User A has valid access A
    And The client adds userId B and userInfo for B
    When The client sends a protected request
    Then The service authorization subject equals A
    And The response contains zero B-only records
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S040

**Prevent framing of the authenticated renewal prompt**

Use case: [UC-S04](03-use-cases-renewal.md#uc-s04). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Prevent framing of the authenticated renewal prompt
  @proposed_security @RN-S040
  Scenario: RN-S040
    Given A hostile local origin frames the portal
    When A opens the framed page
    Then The frame receives no usable authenticated renewal controls under the proposed frame policy
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Effective shell CSP and frame policy require target validation. SDK headers alone do not establish portal policy.

### RN-S041

**Clear access credentials after explicit logout**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [common.ts](evidence/comprehensive-renewal-20261028/sources/3b6a12d1577f/common.ts#L38-L79); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L23-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Clear access credentials after explicit logout
  @proposed_security @RN-S041
  Scenario: RN-S041
    Given A has browser access and refresh credentials
    When A selects Logout
    And The logout flow completes locally
    Then The current shell access and refresh credentials are absent
    And LocalStorage and sessionStorage contain zero access-credential entries
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S042

**Do not expose prior-user workspace data after account switch**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [common.ts](evidence/comprehensive-renewal-20261028/sources/3b6a12d1577f/common.ts#L38-L79); [login.ts](evidence/comprehensive-renewal-20261028/sources/364c29cab3c1/login.ts#L13-L84). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Do not expose prior-user workspace data after account switch
  @proposed_security @RN-S042
  Scenario: RN-S042
    Given User A loaded A-only business record R in workspace W
    And A logs out and B signs in without permission for R
    When B restores W
    Then The rendered W view contains zero values from R
    And B receives zero successful protected reads for R
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S043

**Characterize cross-tab logout propagation**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [common.ts](evidence/comprehensive-renewal-20261028/sources/3b6a12d1577f/common.ts#L38-L79); [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Characterize cross-tab logout propagation
  @policy_open @RN-S043
  Scenario: RN-S043
    Given Two tabs hold A access
    And Tab 1 and tab 2 have independent session generations
    When A logs out in tab 1
    And Tab 2 sends a protected request
    Then The record identifies tab 2 UI identity and server authorization result
    And The record identifies the logout propagation interval
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Cross-tab UI clearing and revocation propagation deadlines are unresolved. Acceptance is blocked.

### RN-S044

**Exclude credentials from sanitized diagnostics**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Exclude credentials from sanitized diagnostics
  @proposed_security @RN-S044
  Scenario: RN-S044
    Given The fixture forces one refresh acquisition failure containing synthetic credential canaries
    When A captures browser console, network summary, and exported diagnostics
    Then The exported diagnostics contain zero raw access or refresh credential canaries
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S045

**Keep credentials out of URLs and browser history**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Keep credentials out of URLs and browser history
  @proposed_security @RN-S045
  Scenario: RN-S045
    Given A renews and reconnects an authenticated application
    When A inspects request URLs, navigation history, and referrer captures
    Then The captured URLs contain zero raw access or refresh credentials
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S046

**Prevent shared cache reuse of renewed responses**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `service-integration`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtAuthenticationController.java](evidence/comprehensive-renewal-20261028/sources/00c9ced7e545/JwtAuthenticationController.java#L315-L383). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Prevent shared cache reuse of renewed responses
  @proposed_security @RN-S046
  Scenario: RN-S046
    Given A renews through an isolated caching proxy
    And B shares that proxy but has another identity
    When B sends the same renewal path with B credentials
    Then B receives zero cached A credential headers or A business records
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S047

**Characterize injected same-origin script exposure**

Use case: [UC-S05](03-use-cases-renewal.md#uc-s05). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [common.ts](evidence/comprehensive-renewal-20261028/sources/3b6a12d1577f/common.ts#L38-L79). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Characterize injected same-origin script exposure
  @policy_open @RN-S047
  Scenario: RN-S047
    Given A has synthetic credentials stored by the shell
    And A test extension executes a same-origin diagnostic script
    When The script reads browser storage and request configuration
    Then The record identifies which credential canaries are accessible
    And The record states XSS prevention controls and their observed policy state
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: The shell stores access in JavaScript-readable storage. No XSS injection was demonstrated. Security architecture acceptance is blocked pending owner review.

### RN-S048

**Reject stream deliveries after server revocation**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [JwtTokenUtil.java](evidence/comprehensive-renewal-20261028/sources/09d8595302dd/JwtTokenUtil.java#L82-L103). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Reject stream deliveries after server revocation
  @policy_open @RN-S048
  Scenario: RN-S048
    Given A has an authenticated stream and a recorded revocation completion point
    When The server revokes A
    And The fixture publishes A-only message M after that point
    Then A receives zero M deliveries after the reviewed revocation deadline
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Stream server source and revocation deadline are unavailable. Acceptance is blocked.

### RN-S049

**Use current credentials when reconnecting after renewal**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Use current credentials when reconnecting after renewal
  @proposed_security @RN-S049
  Scenario: RN-S049
    Given A stream disconnected while refresh-based renewal changed access A1 to A2
    When The client reconnects the stream
    Then The observed connection uses A2
    And The observed connection uses zero A1 credentials
    And Exactly one subscription exists for the fixture subscription key
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S050

**Do not restore a logged-out connection through retry**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L23-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Do not restore a logged-out connection through retry
  @proposed_security @RN-S050
  Scenario: RN-S050
    Given A has a queued stream reconnect callback
    When A logs out
    And The fixture executes the queued reconnect callback
    Then Zero authenticated connections are created
    And Zero protected subscriptions are accepted
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-S051

**Withdraw subscription permission on renewal**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Withdraw subscription permission on renewal
  @policy_open @RN-S051
  Scenario: RN-S051
    Given A initially has permission for topic X
    And The renewal response removes X permission
    When A renews
    And The fixture publishes X message M
    Then The security record identifies whether X remains subscribed
    And The security record identifies every M delivery
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Topic entitlement refresh and permission-withdrawal contract are unresolved. Acceptance is blocked.

### RN-S052

**Bound retries after repeated authorization rejection**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Bound retries after repeated authorization rejection
  @proposed_security @RN-S052
  Scenario: RN-S052
    Given The stream server rejects every reconnect with an authorization error
    And The fixture declares a retry budget of 3 attempts
    When A runs the reconnect experiment through all scheduled attempts
    Then The observed reconnect count is at most 3 in this fixture
    And Zero subscriptions are accepted
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Three attempts is an experiment parameter, not an approved production retry limit.

### RN-S053

**Prevent replaying a completed financial write after renewal**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L10-L37). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Prevent replaying a completed financial write after renewal
  @proposed_security @RN-S053
  Scenario: RN-S053
    Given A submits synthetic mutation M with operation identifier OP-1
    And The server commits M before the client receives an authentication-related failure
    When The client renews
    And The client retries M
    Then The service commit count for OP-1 equals 1 under the proposed idempotency rule
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Mutation retry and idempotency contracts require service-specific source. No production write is authorized.

### RN-S054

**Enforce upload authorization after credential change**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `service-integration`. Evidence class: `policy-open`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [AuthTokenFilter.java](evidence/comprehensive-renewal-20261028/sources/dd0c58c0f226/AuthTokenFilter.java#L59-L118). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Enforce upload authorization after credential change
  @policy_open @RN-S054
  Scenario: RN-S054
    Given A uploads synthetic object O
    And A loses O upload permission before completion
    When The client renews
    And The upload completion request arrives
    Then The result records authorization subject, permission decision, and committed object count
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Long upload authorization and revocation timing are unresolved. Acceptance is blocked.

### RN-S055

**Discard buffered user A messages after login as B**

Use case: [UC-S06](03-use-cases-renewal.md#uc-s06). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18); [index.ts](evidence/comprehensive-renewal-20261028/sources/dd7a772b8b6f/index.ts#L23-L35). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Discard buffered user A messages after login as B
  @proposed_security @RN-S055
  Scenario: RN-S055
    Given The fixture buffers user A message M in the stream client
    And A logs out and B signs in
    When The fixture releases M to the consumer callback
    Then The B view displays zero values from M
    And The B message store contains zero A records
```

Assertion binding: UNVERIFIED for this new definition; existing test links require direct predicate comparison.

Execution: `NOT_RUN`. Limits: Defined adversarial check. No passing execution is inferred. Synthetic identities and isolated services only.

### RN-X001

**Six manual recovery cycles preserve three workspaces**

Use case: [UC-X01](03-use-cases-renewal.md#uc-x01). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223), [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L79-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L15-L54); [renewal-loop-e2e.mjs](evidence/comprehensive-renewal-20261028/sources/209e83f359a0/renewal-loop-e2e.mjs#L55-L63). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Six manual recovery cycles preserve three workspaces
  @target @RN-X001
  Scenario: RN-X001
    Given User A uses the isolated local portal fixture with three empty workspaces
    And the browser clock is controlled and renewal responses use synthetic credentials
    And the fixture records initial workspace IDs and prompt closure transitions
    When User A reaches access expiry in each of six controlled cycles
    And User A selects the button labeled "Extend" in the dialog named "Your session has been expired" in the portal
    And the renewal endpoint returns a retryable 503 response
    And User A selects the button labeled "Extend" inside the dialog named "Your session has been expired" again in the portal
    And the renewal endpoint returns valid synthetic access
    Then each failed attempt leaves the dialog named "Your session has been expired" visible with zero successful closure transitions in the portal
    And each successful attempt installs changed usable access and closes the dialog named "Your session has been expired" exactly once in the portal
    And all six cycles preserve the initial three workspace IDs
    And the renewal request count equals 12
```

Assertion binding: See the exact browser runner and results below.

Execution: `PASSED`. Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

Results: [retained execution](evidence/comprehensive-renewal-20261028/rn-x001/result.json).

### RN-X002

**Twenty-five click events share one pending manual renewal**

Use case: [UC-X02](03-use-cases-renewal.md#uc-x02). Level: `browser-e2e`. Evidence class: `target`.

Criteria: [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223)

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L79-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L15-L54); [renewal-loop-e2e.mjs](evidence/comprehensive-renewal-20261028/sources/209e83f359a0/renewal-loop-e2e.mjs#L64-L68). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Twenty-five click events share one pending manual renewal
  @target @RN-X002
  Scenario: RN-X002
    Given User A uses the isolated local portal fixture with three empty workspaces
    And the browser clock is controlled and renewal responses use synthetic credentials
    And the fixture records initial workspace IDs and prompt closure transitions
    And the manual renewal response remains held
    When User A reaches access expiry
    And User A delivers 25 click events to the button labeled "Extend" in the dialog named "Your session has been expired" in the portal
    And the fixture releases one valid renewal response
    Then the pending renewal request count equals 1
    And the dialog named "Your session has been expired" has zero successful closure transitions in the portal
    And the released response installs usable access and closes the dialog named "Your session has been expired" exactly once in the portal
    And all three workspace IDs equal their initial values
```

Assertion binding: See the exact browser runner and results below.

Execution: `PASSED`. Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

Results: [retained execution](evidence/comprehensive-renewal-20261028/rn-x002/result.json).

### RN-X003

**Logout rejects late completion from pending manual renewal**

Use case: [UC-X03](03-use-cases-renewal.md#uc-x03). Level: `browser-e2e`. Evidence class: `proposed-security`.

Criteria: No separate approved criterion; see the stated evidence class.

Source: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L79-L155); [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L15-L54); [renewal-loop-e2e.mjs](evidence/comprehensive-renewal-20261028/sources/209e83f359a0/renewal-loop-e2e.mjs#L70-L74). Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).

```gherkin
Feature: Logout rejects late completion from pending manual renewal
  @proposed_security @RN-X003
  Scenario: RN-X003
    Given User A uses the isolated local portal fixture with three empty workspaces
    And the browser clock is controlled and renewal responses use synthetic credentials
    And the fixture records initial workspace IDs and prompt closure transitions
    And the manual renewal response remains held
    When User A reaches access expiry
    And User A selects the button labeled "Extend" in the dialog named "Your session has been expired" in the portal
    And User A selects the button labeled "Logout" inside the dialog named "Your session has been expired" while renewal remains pending in the portal
    And the fixture attempts late success delivery
    And the controlled clock advances through the existing 1000 millisecond logout delay
    Then the logout state becomes true while renewal remains pending
    And late delivery does not restore authentication
    And the final session access credential is absent
    And the held manual renewal request count equals 1
```

Assertion binding: See the exact browser runner and results below.

Execution: `PASSED`. Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

Results: [retained execution](evidence/comprehensive-renewal-20261028/rn-x003/result.json).

### RN-C001

**Pairwise interaction design**

Use case: [UC-C01](03-use-cases-renewal.md#uc-c01). Level: planned browser and service integration.
Evidence class: proposed-security. Execution: `NOT_RUN`. Each row has one independent context.
Begin a renewal attempt, then apply lifecycle, ownership, and response events in the named order.
A guarded action can send zero POST requests. Record that outcome without fabricating a response.
The transport factor names a concurrent connection. It does not declare that transport eligible user activity.
The fixture creates the named loading state before the renewal attempt.
All source and policy limits from the linked individual cases also apply.

```gherkin
Feature: Renewal interaction invariants
  @proposed_security @RN-C001
  Scenario Outline: RN-C001
    Given User A has <workspaces> isolated workspaces with loading state <loading>
    And access has <access_ms> milliseconds remaining and refresh state equals <refresh>
    And the concurrent transport equals <transport> and network schedule equals <network>
    When the fixture attempts renewal through <trigger>
    And the fixture applies ownership change <ownership>
    And the fixture applies lifecycle change <lifecycle>
    And the fixture settles accepted requests with <response> using delivery order <delivery>
    Then obsolete-epoch responses install exactly 0 credentials
    And unauthorized protected business mutations equal 0
    And each business operation identifier has at most 1 committed mutation
    Examples:
      | row_id | workspaces | loading | trigger | access_ms | refresh | response | ownership | lifecycle | transport | delivery | network |
      | PAIR-001 | 8 | idle | activity | 25000 | valid-four-hours | timeout | replace-with-B | hidden-after-start | stomp | reverse | slow |
      | PAIR-002 | 2 | mixed-outcomes | manual | 0 | valid-two-seconds | timeout | logout-A | resume-before-delivery | sse | same-tick | online |
      | PAIR-003 | 1 | one-request | activity | 24999 | expired | rejected | logout-A | visible | graphql-websocket | fifo | reconnect-before-delivery |
      | PAIR-004 | 1 | two-requests | refresh-acquisition | 60000 | missing | usable | replace-with-B | unmount-after-start | http | same-tick | online |
      | PAIR-005 | 8 | two-requests | refresh-acquisition | 0 | revoked | malformed | unchanged-A | visible | sse | reverse | slow |
      | PAIR-006 | 2 | idle | manual | 24999 | revoked | malformed | replace-with-B | hidden-after-start | long-poll | fifo | reconnect-before-delivery |
      | PAIR-007 | 8 | one-request | manual | 60000 | valid-four-hours | timeout | unchanged-A | unmount-after-start | file-transfer | fifo | online |
      | PAIR-008 | 2 | mixed-outcomes | refresh-acquisition | 25000 | expired | rejected | unchanged-A | resume-before-delivery | http | same-tick | reconnect-before-delivery |
      | PAIR-009 | 8 | two-requests | activity | 24999 | valid-two-seconds | usable | logout-A | resume-before-delivery | file-transfer | reverse | reconnect-before-delivery |
      | PAIR-010 | 1 | one-request | manual | 0 | missing | rejected | unchanged-A | hidden-after-start | long-poll | reverse | slow |
      | PAIR-011 | 1 | idle | refresh-acquisition | 24999 | expired | malformed | logout-A | unmount-after-start | stomp | same-tick | online |
      | PAIR-012 | 2 | two-requests | manual | 25000 | missing | usable | replace-with-B | visible | stomp | fifo | slow |
      | PAIR-013 | 1 | mixed-outcomes | activity | 60000 | revoked | malformed | replace-with-B | resume-before-delivery | graphql-websocket | same-tick | online |
      | PAIR-014 | 2 | mixed-outcomes | activity | 60000 | valid-two-seconds | timeout | logout-A | unmount-after-start | long-poll | reverse | slow |
      | PAIR-015 | 2 | mixed-outcomes | manual | 0 | valid-four-hours | usable | unchanged-A | hidden-after-start | graphql-websocket | same-tick | slow |
      | PAIR-016 | 2 | one-request | refresh-acquisition | 60000 | valid-two-seconds | rejected | replace-with-B | hidden-after-start | stomp | fifo | online |
      | PAIR-017 | 8 | idle | activity | 24999 | missing | timeout | unchanged-A | unmount-after-start | sse | same-tick | reconnect-before-delivery |
      | PAIR-018 | 1 | idle | refresh-acquisition | 25000 | valid-four-hours | rejected | replace-with-B | visible | file-transfer | same-tick | online |
      | PAIR-019 | 8 | two-requests | activity | 0 | expired | timeout | logout-A | visible | http | reverse | slow |
      | PAIR-020 | 8 | one-request | refresh-acquisition | 25000 | revoked | usable | logout-A | hidden-after-start | sse | same-tick | online |
      | PAIR-021 | 8 | mixed-outcomes | refresh-acquisition | 60000 | expired | rejected | replace-with-B | visible | sse | fifo | reconnect-before-delivery |
      | PAIR-022 | 8 | idle | refresh-acquisition | 0 | valid-four-hours | timeout | replace-with-B | resume-before-delivery | graphql-websocket | fifo | reconnect-before-delivery |
      | PAIR-023 | 1 | two-requests | activity | 25000 | valid-two-seconds | malformed | replace-with-B | unmount-after-start | graphql-websocket | reverse | reconnect-before-delivery |
      | PAIR-024 | 8 | one-request | refresh-acquisition | 25000 | expired | malformed | replace-with-B | resume-before-delivery | long-poll | reverse | online |
      | PAIR-025 | 2 | two-requests | manual | 24999 | valid-four-hours | malformed | logout-A | resume-before-delivery | http | fifo | slow |
      | PAIR-026 | 2 | mixed-outcomes | refresh-acquisition | 0 | missing | malformed | replace-with-B | resume-before-delivery | file-transfer | reverse | slow |
      | PAIR-027 | 1 | two-requests | activity | 0 | revoked | rejected | unchanged-A | unmount-after-start | stomp | same-tick | online |
      | PAIR-028 | 1 | idle | activity | 60000 | expired | usable | logout-A | hidden-after-start | file-transfer | reverse | reconnect-before-delivery |
      | PAIR-029 | 2 | mixed-outcomes | refresh-acquisition | 24999 | valid-four-hours | usable | unchanged-A | visible | long-poll | same-tick | online |
      | PAIR-030 | 1 | idle | manual | 60000 | valid-two-seconds | timeout | unchanged-A | hidden-after-start | http | reverse | online |
      | PAIR-031 | 2 | mixed-outcomes | refresh-acquisition | 60000 | revoked | timeout | replace-with-B | resume-before-delivery | stomp | fifo | reconnect-before-delivery |
      | PAIR-032 | 1 | two-requests | activity | 60000 | missing | usable | logout-A | hidden-after-start | graphql-websocket | fifo | reconnect-before-delivery |
      | PAIR-033 | 1 | one-request | refresh-acquisition | 24999 | valid-four-hours | usable | replace-with-B | resume-before-delivery | sse | reverse | online |
      | PAIR-034 | 1 | one-request | activity | 24999 | revoked | usable | unchanged-A | resume-before-delivery | http | fifo | reconnect-before-delivery |
      | PAIR-035 | 2 | two-requests | manual | 25000 | expired | timeout | replace-with-B | unmount-after-start | long-poll | fifo | reconnect-before-delivery |
      | PAIR-036 | 1 | idle | manual | 60000 | valid-two-seconds | timeout | logout-A | visible | sse | fifo | reconnect-before-delivery |
      | PAIR-037 | 2 | mixed-outcomes | manual | 25000 | revoked | rejected | logout-A | hidden-after-start | file-transfer | fifo | reconnect-before-delivery |
```

[Measured pair coverage](evidence/comprehensive-renewal-20261028/combinations.json): 797 / 797 declared factor-value pairs.
The selected 37 rows represent a 1,866,240-row Cartesian design population.
This measures design coverage. It establishes no passing execution or security assurance.

### RN-C002

**Enumerate the selected four-factor risk subset**

Use case: [UC-C01](03-use-cases-renewal.md#uc-c01). Evidence class: proposed-security. Execution: `NOT_RUN`.
Use one workspace, idle loading, valid four-hour refresh, visible lifecycle, HTTP, and an online FIFO fixture.
This subset enumerates every declared trigger, access boundary, response, and ownership combination.

```gherkin
Feature: Renewal risk interactions
  @proposed_security @RN-C002
  Scenario Outline: RN-C002
    Given User A has access remaining <access_ms> milliseconds in the fixed risk fixture
    When the fixture attempts renewal through <trigger>
    And the fixture applies ownership change <ownership>
    And the fixture settles accepted requests with <response>
    Then obsolete-epoch responses install exactly 0 credentials
    And unauthorized protected business mutations equal 0
    Examples:
      | row_id | trigger | access_ms | response | ownership |
      | RISK-001 | manual | 60000 | usable | unchanged-A |
      | RISK-002 | manual | 60000 | usable | logout-A |
      | RISK-003 | manual | 60000 | usable | replace-with-B |
      | RISK-004 | manual | 60000 | rejected | unchanged-A |
      | RISK-005 | manual | 60000 | rejected | logout-A |
      | RISK-006 | manual | 60000 | rejected | replace-with-B |
      | RISK-007 | manual | 60000 | timeout | unchanged-A |
      | RISK-008 | manual | 60000 | timeout | logout-A |
      | RISK-009 | manual | 60000 | timeout | replace-with-B |
      | RISK-010 | manual | 60000 | malformed | unchanged-A |
      | RISK-011 | manual | 60000 | malformed | logout-A |
      | RISK-012 | manual | 60000 | malformed | replace-with-B |
      | RISK-013 | manual | 25000 | usable | unchanged-A |
      | RISK-014 | manual | 25000 | usable | logout-A |
      | RISK-015 | manual | 25000 | usable | replace-with-B |
      | RISK-016 | manual | 25000 | rejected | unchanged-A |
      | RISK-017 | manual | 25000 | rejected | logout-A |
      | RISK-018 | manual | 25000 | rejected | replace-with-B |
      | RISK-019 | manual | 25000 | timeout | unchanged-A |
      | RISK-020 | manual | 25000 | timeout | logout-A |
      | RISK-021 | manual | 25000 | timeout | replace-with-B |
      | RISK-022 | manual | 25000 | malformed | unchanged-A |
      | RISK-023 | manual | 25000 | malformed | logout-A |
      | RISK-024 | manual | 25000 | malformed | replace-with-B |
      | RISK-025 | manual | 24999 | usable | unchanged-A |
      | RISK-026 | manual | 24999 | usable | logout-A |
      | RISK-027 | manual | 24999 | usable | replace-with-B |
      | RISK-028 | manual | 24999 | rejected | unchanged-A |
      | RISK-029 | manual | 24999 | rejected | logout-A |
      | RISK-030 | manual | 24999 | rejected | replace-with-B |
      | RISK-031 | manual | 24999 | timeout | unchanged-A |
      | RISK-032 | manual | 24999 | timeout | logout-A |
      | RISK-033 | manual | 24999 | timeout | replace-with-B |
      | RISK-034 | manual | 24999 | malformed | unchanged-A |
      | RISK-035 | manual | 24999 | malformed | logout-A |
      | RISK-036 | manual | 24999 | malformed | replace-with-B |
      | RISK-037 | manual | 0 | usable | unchanged-A |
      | RISK-038 | manual | 0 | usable | logout-A |
      | RISK-039 | manual | 0 | usable | replace-with-B |
      | RISK-040 | manual | 0 | rejected | unchanged-A |
      | RISK-041 | manual | 0 | rejected | logout-A |
      | RISK-042 | manual | 0 | rejected | replace-with-B |
      | RISK-043 | manual | 0 | timeout | unchanged-A |
      | RISK-044 | manual | 0 | timeout | logout-A |
      | RISK-045 | manual | 0 | timeout | replace-with-B |
      | RISK-046 | manual | 0 | malformed | unchanged-A |
      | RISK-047 | manual | 0 | malformed | logout-A |
      | RISK-048 | manual | 0 | malformed | replace-with-B |
      | RISK-049 | refresh-acquisition | 60000 | usable | unchanged-A |
      | RISK-050 | refresh-acquisition | 60000 | usable | logout-A |
      | RISK-051 | refresh-acquisition | 60000 | usable | replace-with-B |
      | RISK-052 | refresh-acquisition | 60000 | rejected | unchanged-A |
      | RISK-053 | refresh-acquisition | 60000 | rejected | logout-A |
      | RISK-054 | refresh-acquisition | 60000 | rejected | replace-with-B |
      | RISK-055 | refresh-acquisition | 60000 | timeout | unchanged-A |
      | RISK-056 | refresh-acquisition | 60000 | timeout | logout-A |
      | RISK-057 | refresh-acquisition | 60000 | timeout | replace-with-B |
      | RISK-058 | refresh-acquisition | 60000 | malformed | unchanged-A |
      | RISK-059 | refresh-acquisition | 60000 | malformed | logout-A |
      | RISK-060 | refresh-acquisition | 60000 | malformed | replace-with-B |
      | RISK-061 | refresh-acquisition | 25000 | usable | unchanged-A |
      | RISK-062 | refresh-acquisition | 25000 | usable | logout-A |
      | RISK-063 | refresh-acquisition | 25000 | usable | replace-with-B |
      | RISK-064 | refresh-acquisition | 25000 | rejected | unchanged-A |
      | RISK-065 | refresh-acquisition | 25000 | rejected | logout-A |
      | RISK-066 | refresh-acquisition | 25000 | rejected | replace-with-B |
      | RISK-067 | refresh-acquisition | 25000 | timeout | unchanged-A |
      | RISK-068 | refresh-acquisition | 25000 | timeout | logout-A |
      | RISK-069 | refresh-acquisition | 25000 | timeout | replace-with-B |
      | RISK-070 | refresh-acquisition | 25000 | malformed | unchanged-A |
      | RISK-071 | refresh-acquisition | 25000 | malformed | logout-A |
      | RISK-072 | refresh-acquisition | 25000 | malformed | replace-with-B |
      | RISK-073 | refresh-acquisition | 24999 | usable | unchanged-A |
      | RISK-074 | refresh-acquisition | 24999 | usable | logout-A |
      | RISK-075 | refresh-acquisition | 24999 | usable | replace-with-B |
      | RISK-076 | refresh-acquisition | 24999 | rejected | unchanged-A |
      | RISK-077 | refresh-acquisition | 24999 | rejected | logout-A |
      | RISK-078 | refresh-acquisition | 24999 | rejected | replace-with-B |
      | RISK-079 | refresh-acquisition | 24999 | timeout | unchanged-A |
      | RISK-080 | refresh-acquisition | 24999 | timeout | logout-A |
      | RISK-081 | refresh-acquisition | 24999 | timeout | replace-with-B |
      | RISK-082 | refresh-acquisition | 24999 | malformed | unchanged-A |
      | RISK-083 | refresh-acquisition | 24999 | malformed | logout-A |
      | RISK-084 | refresh-acquisition | 24999 | malformed | replace-with-B |
      | RISK-085 | refresh-acquisition | 0 | usable | unchanged-A |
      | RISK-086 | refresh-acquisition | 0 | usable | logout-A |
      | RISK-087 | refresh-acquisition | 0 | usable | replace-with-B |
      | RISK-088 | refresh-acquisition | 0 | rejected | unchanged-A |
      | RISK-089 | refresh-acquisition | 0 | rejected | logout-A |
      | RISK-090 | refresh-acquisition | 0 | rejected | replace-with-B |
      | RISK-091 | refresh-acquisition | 0 | timeout | unchanged-A |
      | RISK-092 | refresh-acquisition | 0 | timeout | logout-A |
      | RISK-093 | refresh-acquisition | 0 | timeout | replace-with-B |
      | RISK-094 | refresh-acquisition | 0 | malformed | unchanged-A |
      | RISK-095 | refresh-acquisition | 0 | malformed | logout-A |
      | RISK-096 | refresh-acquisition | 0 | malformed | replace-with-B |
      | RISK-097 | activity | 60000 | usable | unchanged-A |
      | RISK-098 | activity | 60000 | usable | logout-A |
      | RISK-099 | activity | 60000 | usable | replace-with-B |
      | RISK-100 | activity | 60000 | rejected | unchanged-A |
      | RISK-101 | activity | 60000 | rejected | logout-A |
      | RISK-102 | activity | 60000 | rejected | replace-with-B |
      | RISK-103 | activity | 60000 | timeout | unchanged-A |
      | RISK-104 | activity | 60000 | timeout | logout-A |
      | RISK-105 | activity | 60000 | timeout | replace-with-B |
      | RISK-106 | activity | 60000 | malformed | unchanged-A |
      | RISK-107 | activity | 60000 | malformed | logout-A |
      | RISK-108 | activity | 60000 | malformed | replace-with-B |
      | RISK-109 | activity | 25000 | usable | unchanged-A |
      | RISK-110 | activity | 25000 | usable | logout-A |
      | RISK-111 | activity | 25000 | usable | replace-with-B |
      | RISK-112 | activity | 25000 | rejected | unchanged-A |
      | RISK-113 | activity | 25000 | rejected | logout-A |
      | RISK-114 | activity | 25000 | rejected | replace-with-B |
      | RISK-115 | activity | 25000 | timeout | unchanged-A |
      | RISK-116 | activity | 25000 | timeout | logout-A |
      | RISK-117 | activity | 25000 | timeout | replace-with-B |
      | RISK-118 | activity | 25000 | malformed | unchanged-A |
      | RISK-119 | activity | 25000 | malformed | logout-A |
      | RISK-120 | activity | 25000 | malformed | replace-with-B |
      | RISK-121 | activity | 24999 | usable | unchanged-A |
      | RISK-122 | activity | 24999 | usable | logout-A |
      | RISK-123 | activity | 24999 | usable | replace-with-B |
      | RISK-124 | activity | 24999 | rejected | unchanged-A |
      | RISK-125 | activity | 24999 | rejected | logout-A |
      | RISK-126 | activity | 24999 | rejected | replace-with-B |
      | RISK-127 | activity | 24999 | timeout | unchanged-A |
      | RISK-128 | activity | 24999 | timeout | logout-A |
      | RISK-129 | activity | 24999 | timeout | replace-with-B |
      | RISK-130 | activity | 24999 | malformed | unchanged-A |
      | RISK-131 | activity | 24999 | malformed | logout-A |
      | RISK-132 | activity | 24999 | malformed | replace-with-B |
      | RISK-133 | activity | 0 | usable | unchanged-A |
      | RISK-134 | activity | 0 | usable | logout-A |
      | RISK-135 | activity | 0 | usable | replace-with-B |
      | RISK-136 | activity | 0 | rejected | unchanged-A |
      | RISK-137 | activity | 0 | rejected | logout-A |
      | RISK-138 | activity | 0 | rejected | replace-with-B |
      | RISK-139 | activity | 0 | timeout | unchanged-A |
      | RISK-140 | activity | 0 | timeout | logout-A |
      | RISK-141 | activity | 0 | timeout | replace-with-B |
      | RISK-142 | activity | 0 | malformed | unchanged-A |
      | RISK-143 | activity | 0 | malformed | logout-A |
      | RISK-144 | activity | 0 | malformed | replace-with-B |
```

The 144 examples exhaust this declared subset. Other interactions remain outside that claim.

### RN-O001

**Enumerate late-session response orderings**

Use case: [UC-C02](03-use-cases-renewal.md#uc-c02). Evidence class: proposed-security. Execution: `NOT_RUN`.
Events start-A and start-B create requests under their respective session epochs.
Events logout-A and login-B invalidate A and establish B. Event reply-B installs usable B access.
Event reply-A delivers the specified old response. Each sequence uses a new context.

```gherkin
Feature: Late response ordering isolation
  @proposed_security @RN-O001
  Scenario Outline: RN-O001
    Given User A has a valid session and User B has separate synthetic credentials
    And the old response outcome equals <old_response>
    When the fixture executes event sequence <events>
    Then the final installed credential subject equals B
    And A response deliveries after logout change exactly 0 B authentication fields
    Examples:
      | row_id | old_response | events |
      | ORDER-001 | usable | start-A > logout-A > login-B > start-B > reply-B > reply-A |
      | ORDER-002 | rejected | start-A > logout-A > login-B > start-B > reply-B > reply-A |
      | ORDER-003 | malformed | start-A > logout-A > login-B > start-B > reply-B > reply-A |
      | ORDER-004 | usable | start-A > logout-A > login-B > start-B > reply-A > reply-B |
      | ORDER-005 | rejected | start-A > logout-A > login-B > start-B > reply-A > reply-B |
      | ORDER-006 | malformed | start-A > logout-A > login-B > start-B > reply-A > reply-B |
      | ORDER-007 | usable | start-A > logout-A > login-B > reply-A > start-B > reply-B |
      | ORDER-008 | rejected | start-A > logout-A > login-B > reply-A > start-B > reply-B |
      | ORDER-009 | malformed | start-A > logout-A > login-B > reply-A > start-B > reply-B |
      | ORDER-010 | usable | start-A > logout-A > reply-A > login-B > start-B > reply-B |
      | ORDER-011 | rejected | start-A > logout-A > reply-A > login-B > start-B > reply-B |
      | ORDER-012 | malformed | start-A > logout-A > reply-A > login-B > start-B > reply-B |
      | ORDER-013 | usable | start-A > reply-A > logout-A > login-B > start-B > reply-B |
      | ORDER-014 | rejected | start-A > reply-A > logout-A > login-B > start-B > reply-B |
      | ORDER-015 | malformed | start-A > reply-A > logout-A > login-B > start-B > reply-B |
```

The 15 rows exhaust this six-event partial order with three old-response outcomes.
They do not exhaust arbitrary session histories or infinite loops.
