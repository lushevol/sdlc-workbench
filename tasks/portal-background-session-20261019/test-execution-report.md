---
artifact_kind: test-execution-report
id: EXEC-session-renewal-browser-20261020
version: 7
status: draft
owner: unknown
source_refs:
  - SRC-session-robot-modules-20261021
  - SRC-session-canonical-inputs-20261021
  - SRC-session-branch-refresh-20261021
  - SRC-session-minor-manifest-20261020
  - SRC-session-minor-inventory-20261020
  - SRC-session-minor-stage-20261020
  - SRC-session-minor-fixture-20261020
  - SRC-session-minor-impact-20261020
  - SRC-session-minor-unit-20261020
  - SRC-session-minor-assessment-20261020
  - SRC-session-minor-delayed-refresh-20261020
  - SRC-session-review-intent-v4
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

# Session renewal execution and current issue status

> **⚠️ Critical conclusions: Action required**
>
> **🔴 Two P2 regressions can end a usable session.**
> Action: assess [active-session cutoff](test-cases.md#review-f01) and [stale-credential reuse](code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: valid access can end, or recovery can clear a fresh session. Owner: unknown application owner.
> Evidence: [current paired results](evidence/code-review-refresh-20261021/summary.json). The active-cutoff case requires an unreplaced refresh token.
>
> **🟠 Delayed background recovery still fails in both versions.**
> Action: retain this limitation when deciding required recovery. Consequence: late usable credentials leave Extend disabled and permit logout.
> Owner: unknown application owner; user for acceptance decisions. Evidence: [browser probe](test-cases.md#probe-delayed-refresh) and [old/new comparison](test-cases.md#review-delayed-scheduled).
>
> **👤 No criterion waiver is recorded.**
> Action: decide any named deferral from its [failure and limit](#failure-limits-and-recommended-dispositions). Owner: user.
> Consequence: broader acceptance remains open. Passing unit checks include one expected failure.

## Current issue synchronization

**Read the [current review](code-review-minor-20261021.md) for findings and the [stage record](change-review.md) for decisions.**
This report owns retained browser outcomes. The [canonical catalog](test-cases.md) owns case steps and assertions.
No new business execution occurred during this document edit.

| Scope | Status and limit | Evidence |
| --- | --- | --- |
| 🔎 Latest review and checks, 21 October | Two P2 regressions and one P3 issue remain. Compiler passes; 413 runner passes include one expected failure. | [Review and checks](code-review-minor-20261021.md#fresh-branch-review-21-october-2026), [paired results](evidence/code-review-refresh-20261021/summary.json). No fresh browser or production execution. |
| 🧪 Retained browser execution, 20 October | Five passed; fourteen failed; one diagnostic failed; two observations. All 22 cases completed. | [Outcomes](#assertions-and-outcomes), [manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json). Runtime `6d4c37c839b99d14ea41fd936da1a36cda526b17`; tests `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. |
| 🧩 Reorganized executable tests | Offline checks pass. Business execution is `NOT_RUN` at `975af64c55303ee4a138968813ef4e85570f96d2`. | [Current Robot source](test-cases.md#current-robot-and-javascript-source), [offline checks](evidence/robot-case-modules-20261021/offline-checks.json). Earlier browser results retain their original source identities. |
| ⏳ Production build and deployment | Full production build is `NOT_RUN`. Deployment behavior remains unverified. | [Build boundary](#unit-execution-and-build-readiness). No release approval is recorded. |

The branch head is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; its later changes affect tests only.
Runtime remains `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
The [separate recovery probes](#required-background-recovery-and-supplemental-investigations) compare immediate and delayed response delivery.
The earlier unit failure and compiler errors remain [historical evidence](#unit-execution-and-build-readiness).

## Stage boundary and readiness

This report records the selected minor branch and preserves earlier results as historical evidence.
The [stage baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json) permits source review and local evidence collection.
It does not approve application changes, acceptance waivers, production release, or knowledge publication.
The [acceptance assessment](evidence/minor-branch-rerun-20261020/acceptance-assessment.json) records recommendations and decision limits.
Its execution checkpoint can precede this report. Current case verdicts come from the retained browser manifest.
Requirement candidate version 4 and its pending human review remain unchanged.

| Named phase | Readiness | Owner and next action |
| --- | --- | --- |
| Authorized local evidence collection | READY | unknown test owner. Collection is complete. Review each retained result. |
| Implementation change | Not authorized in this stage | unknown application owner. Review the concrete failures before an authorized correction. |
| Production release | No approval recorded | unknown release owner. Resolve required behavior, build, acceptance, and deployment evidence. |

Risk remains high for previously tested acceptance predicates. The smaller branch removes or changes relevant safeguards.
Source predictions do not establish execution outcomes. The [impact review](evidence/minor-branch-rerun-20261020/source-impact-review.json) separates them.

## Run identity and provenance

```yaml
{
  "execution_id": "MINOR-session-browser-20261020",
  "execution_status": "COMPLETED_WITH_FAILURES",
  "repository_id": "mfe-base",
  "repository_revision": "6d4c37c839b99d14ea41fd936da1a36cda526b17",
  "application_branch": "feature/session-refresh-minor",
  "test_repository": "ratan-test-engine",
  "test_revision": "7a504c13a8d51bb52af5cc89bd4af88d1988da94",
  "test_source_sha256": "94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984",
  "service_repository": "single-ui-bff",
  "service_revision": "85d7cc03eb12710d6facf581987fd4ae24fc9844",
  "environment_identity": "Local fast portal/BFF 8103/8091; natural portal/BFF 8101/8088",
  "started_at": "2026-10-20T14:19:53.272Z",
  "completed_at": "2026-10-20T14:50:16.940Z",
  "command_or_tool_reference": "evidence/minor-branch-rerun-20261020/run-expanded.py.snapshot",
  "process_exit_status": null,
  "actual_results": {
    "DIAGNOSTIC_FAILED": 1,
    "FAILED": 14,
    "OBSERVATION_ONLY": 2,
    "PASSED": 5
  },
  "retained_execution_refs": [
    "evidence/minor-branch-rerun-20261020/browser-manifest.json"
  ]
}
```

Each retained attempt has its own status and exit context. No aggregate process exit status is asserted.

## Browser environment and suite completeness

- Inventory: [22 executable assertion bindings](evidence/minor-branch-rerun-20261020/case-inventory.json); test revision `7a504c13a8d51bb52af5cc89bd4af88d1988da94`.
- Original cases: 7; 7 FAILED.
- Additional cases: 15; 1 DIAGNOSTIC_FAILED, 7 FAILED, 2 OBSERVATION_ONLY, 5 PASSED.
- Application: `6d4c37c839b99d14ea41fd936da1a36cda526b17`; branch `feature/session-refresh-minor`.
- Service: `85d7cc03eb12710d6facf581987fd4ae24fc9844`. The local fixture reuses actual BFF authentication classes.
- Browser: native Microsoft Edge `155.0.4283.62`, Chromium engine, macOS, fresh native profiles.
- Connection: CDP `noDefaults=true`, native default contexts. Each test context uses an independent Edge process.
- Launch arguments: per-attempt `nativeContexts[].args` in retained run records. Background network, sync, and updater features are disabled.
- Visibility: real covering tabs and native activation. The driver does not override document visibility or force freezing.
- Clock: real wall time. Fast credentials use 60-second access and 144-second refresh lifetimes.
- Natural credentials use 900-second access and 13,524-second refresh lifetimes. Long cases target 1,800 hidden seconds.
- Fixtures: local toolkit stubs, disabled federation remotes, and synthetic identity and integration adapters.
- Transport controls: selected cases hold, abort, or replace responses. Each case retains its controls and limits.
- Protected operation: portal authentication validation at `/api/auth/v2/sso/validate`. Downstream business authorization remains untested.
- Runtime binding: 339 copied source files match the selected application commit.
- Unit binding: 346 selected inputs match the commit and remained unchanged.
- The pre-existing `tsconfig.tsbuildinfo` modification remained unchanged. Environment file values were neither inspected nor retained.
- Missing executions: none. Owner: unknown test owner. Complete authorized collection.

20 native startup attempts ended before application entry.
Their machine status is `NOT_RUN_SETUP_FAILED`; the error is `Native Edge exited during startup.`
These attempts are setup failures. They are excluded from functional case counts.
The [manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json) preserves their identities, timestamps, and driver hashes.
Inspect and smoke operations are excluded from the 22 declared cases.

Passing local predicates do not establish production integration. Exact four-hour renewal, touch, and cross-origin journeys remain untested.
Multiple native contexts do not establish coordinated sessions across multiple authenticated tabs.

## Definitions and BDD navigation

Current test steps and assertions have one source: [the canonical catalog](test-cases.md#procedure-and-assertions).
AC links open the unchanged local candidate-version-4 Gherkin. TC links open the unchanged frozen intake.
The [source table](#sources) retains their exact Git revisions and SHA-256 hashes.
The [alias table](test-cases.md#frozen-regression-aliases) maps those scopes to current definitions and coverage limits.

Source definitions do not establish approval. Some proposed case scopes have no independent approved BDD.

| Definition set | Exact definition links | Scope and limits |
| --- | --- | --- |
| Acceptance criteria | [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140); [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147); [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154); [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162); [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176); [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183) | Candidate requirement version 4. [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) specifies four controlled hours. |
| Proposed regression scopes | [TC-01](intake.md#L263); [TC-02](intake.md#L264); [TC-03](intake.md#L265); [TC-04](intake.md#L266); [TC-05](intake.md#L267); [TC-06](intake.md#L268); [TC-07](intake.md#L269) | Frozen intake. Missing-refresh and populated workspace policies remain unresolved. |

## Case mapping

Each case links its canonical definition, inspected assertions, and retained execution separately.
The catalog contains the full expected result and criterion mapping. This report summarizes actual outcomes.

[Executed 22-case inventory](evidence/minor-branch-rerun-20261020/case-inventory.json) supplies exact 7a source and helper line mappings.

## Assertions and outcomes

**These outcomes describe the 20 October browser run. They do not describe a new execution of the reorganized tests.**
All inspected functions below belong to retained test revision `7a504c1`.
The [execution inventory](evidence/minor-branch-rerun-20261020/case-inventory.json) preserves full assertion mappings and hashes.
[AC-4-live-boundary](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) tests the shortened refresh boundary. It does not test the exact four-hour criterion.
`OBSERVATION_ONLY` and diagnostic outcomes do not establish business acceptance.
For failed cases, later assertions remain unestablished. A cancellation failure alone does not prove token resurrection or overwrite.

| Case and journey | Outcome | Observed result and limit | Assertions and execution |
| --- | --- | --- | --- |
| [E2E-01](test-cases.md#e2e-01) / `mouse` | ❌ `FAILED` | Mouse activity did not meet the 15-second renewal assertion. Later assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); [run](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/result.json) |
| [E2E-02](test-cases.md#e2e-02) / `keyboard` | ❌ `FAILED` | Keyboard activity did not meet the 15-second renewal assertion. Later assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); [run](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/result.json) |
| [E2E-03](test-cases.md#e2e-03) / `scroll` | ❌ `FAILED` | Scroll activity did not meet the 15-second renewal assertion. Later assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); [run](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/result.json) |
| [E2E-04](test-cases.md#e2e-04) / `pending` | ❌ `FAILED` | The prompt closed while renewal remained held. Actual completion was not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L313); [run](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/result.json) |
| [E2E-05](test-cases.md#e2e-05) / `retry` | ❌ `FAILED` | The prompt closed after failure. Actual-service retry was not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L320); [run](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/result.json) |
| [E2E-06](test-cases.md#e2e-06) / `cross` | ❌ `FAILED` | Portal Home became unavailable at the shortened refresh boundary. The four-hour criterion remains untested. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L601); [run](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json) |
| [E2E-07](test-cases.md#e2e-07) / `natural` | ❌ `FAILED` | After 1,800,011 hidden milliseconds, the pending-prompt assertion failed before service forwarding. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L643); [run](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/result.json) |
| [E2E-08](test-cases.md#e2e-08) / `single` | ❌ `FAILED` | Zero extension requests were held. Request sharing and cancellation were not demonstrated. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L706); [run](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/result.json) |
| [E2E-09](test-cases.md#e2e-09) / `rapid` | ❌ `FAILED` | The Extend bounding-box wait timed out before the second activation. Later assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L337); [run](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/result.json) |
| [E2E-10](test-cases.md#e2e-10) / `keyboardExtend` | ❌ `FAILED` | The prompt closed during held keyboard-triggered renewal. Actual completion was not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L378); [run](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/result.json) |
| [E2E-11](test-cases.md#e2e-11) / `activityRetry` | ✅ `PASSED` | One controlled activity failure and one successful retry were observed. Provider rejection remains untested. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L386); [run](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/artifacts/result.json) |
| [E2E-12](test-cases.md#e2e-12) / `inconsistent` | 🟠 `DIAGNOSTIC_FAILED` | The negative response body installed its authorization header. The deployed contract remains unconfirmed. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L416); [run](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/result.json) |
| [E2E-13](test-cases.md#e2e-13) / `promptActivity` | ❌ `FAILED` | Prompt activity started no extension. Later held renewal closed the prompt before completion. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L461); [run](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/result.json) |
| [E2E-14](test-cases.md#e2e-14) / `idleLogout` | ✅ `PASSED` | Logout was observed; stored access cleared; persisted refresh was absent; Sign in appeared. Provider revocation remains unproved. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L493); [run](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json) |
| [E2E-15](test-cases.md#e2e-15) / `visibility` | ✅ `PASSED` | One hidden refresh request completed. Authentication remained available after a short tab switch. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L523); [run](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/artifacts/result.json) |
| [E2E-16](test-cases.md#e2e-16) / `reload` | ✅ `PASSED` | Reload validation rotated and installed access. Refresh reacquisition succeeded with zero additional login requests. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L554); [run](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/artifacts/result.json) |
| [E2E-17](test-cases.md#e2e-17) / `manualLogout` | ❌ `FAILED` | The prompt closed before explicit Logout. Cancellation and late-response assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L758); [run](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/result.json) |
| [E2E-18](test-cases.md#e2e-18) / `activityLogout` | ❌ `FAILED` | The extension did not cancel after logout within the asserted wait. Late-response assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L790); [run](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/result.json) |
| [E2E-19](test-cases.md#e2e-19) / `late` | ❌ `FAILED` | Opening Timeout did not cancel the earlier extension. Overwrite assertions were not reached. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L820); [run](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/result.json) |
| [E2E-20](test-cases.md#e2e-20) / `expired` | ✅ `PASSED` | Protected validation returned HTTP 200 initially and HTTP 401 after access expired. Provider revocation remains untested. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L856); [run](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/artifacts/result.json) |
| [E2E-21](test-cases.md#e2e-21) / `missing` | 👁️ `OBSERVATION_ONLY` | After 1,801,814 hidden milliseconds, Sign in appeared without refresh. No approved recovery verdict exists. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L893); [run](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/artifacts/result.json) |
| [E2E-22](test-cases.md#e2e-22) / `workspace` | 👁️ `OBSERVATION_ONLY` | Two empty workspace descriptors matched after reauthentication. Populated application edits remain untested. | [Assertions](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L946); [run](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/artifacts/result.json) |

### Failure limits and recommended dispositions

<details>
<summary>Show all 22 case limits and recommended actions</summary>

These recommendations do not waive criteria. Each accepted disposition remains null in the acceptance assessment.
The user must approve any scope change before knowledge or acceptance changes.
The primary background scope remains required.

| Case | Consequence and evidence limit | Owner | Recommended next action |
| --- | --- | --- | --- |
| [E2E-01](test-cases.md#e2e-01) | Expiry advancement, prompt absence, and protected validation were not reached. | unknown | Review a criterion-specific deferral with the user; approval remains pending. |
| [E2E-02](test-cases.md#e2e-02) | Expiry advancement, prompt absence, and protected validation were not reached. | unknown | Review a criterion-specific deferral with the user; approval remains pending. |
| [E2E-03](test-cases.md#e2e-03) | A recorded extension response does not prove interval acceptance. Expiry advancement and protected validation were not reached. | unknown | Review a criterion-specific deferral with the user; approval remains pending. |
| [E2E-04](test-cases.md#e2e-04) | The run stopped before forwarding the held request. Actual completion, exact installation, and protected validation were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-05](test-cases.md#e2e-05) | The actual-service retry, successful installation, and protected validation were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-06](test-cases.md#e2e-06) | Replacement-refresh, navigation, transient-prompt, and protected-validation assertions were not reached. The exact four-hour criterion remains untested. | unknown | Review a criterion-specific deferral with the user; approval remains pending. |
| [E2E-07](test-cases.md#e2e-07) | The run stopped before service forwarding, installation, and protected validation. It does not disprove the separate immediate-service recovery. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-08](test-cases.md#e2e-08) | Duplicate-request, cancellation, actual-completion, and protected-validation assertions were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-09](test-cases.md#e2e-09) | The boundingBox wait timed out before the second pointer attempt. Request-sharing, completion, and protected-validation assertions were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-10](test-cases.md#e2e-10) | Actual completion, exact installation, and protected validation were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-11](test-cases.md#e2e-11) | The first failure was controlled transport abort. Provider rejection and downstream authorization remain outside scope. | unknown | Retain the narrow predicate result. Keep disclosed integration limits. |
| [E2E-12](test-cases.md#e2e-12) | The combination lacks a confirmed deployed contract. Actual retry and protected validation were not reached. | unknown | Confirm the deployed service contract before using this diagnostic for acceptance. |
| [E2E-13](test-cases.md#e2e-13) | The modal can consume native events before Home. Later completion, exact installation, and protected validation were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-14](test-cases.md#e2e-14) | Absent persisted refresh does not prove memory cleanup or provider revocation. | unknown | Retain the narrow predicate result. Keep disclosed integration limits. |
| [E2E-15](test-cases.md#e2e-15) | This case does not establish natural freezing, 30-minute recovery, or downstream authorization. | unknown | Retain the narrow predicate result. Keep disclosed integration limits. |
| [E2E-16](test-cases.md#e2e-16) | Refresh reacquisition does not prove memory-only refresh persistence. Downstream authorization remains outside scope. | unknown | Retain the narrow predicate result. Keep disclosed integration limits. |
| [E2E-17](test-cases.md#e2e-17) | Explicit Logout, cancellation, late delivery, and token-resurrection assertions were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-18](test-cases.md#e2e-18) | Late delivery and token-resurrection assertions were not reached. The cleanup-path HTTP401 does not establish token resurrection. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-19](test-cases.md#e2e-19) | Manual renewal, distinct-token comparison, late delivery, and overwrite assertions were not reached. | unknown | Review the failed predicate. Preserve the regression before an authorized correction. |
| [E2E-20](test-cases.md#e2e-20) | The captured read-only HTTP request does not establish provider revocation or downstream authorization. | unknown | Retain the narrow predicate result. Keep disclosed integration limits. |
| [E2E-21](test-cases.md#e2e-21) | The controlled acquisition abort does not establish the original production cause. The result remains observation-only. | unknown | Define policy or populated fixtures before an acceptance verdict. |
| [E2E-22](test-cases.md#e2e-22) | Empty descriptors do not prove populated parameters, application state, entitlements, or in-memory edit restoration. | unknown | Define policy or populated fixtures before an acceptance verdict. |

</details>

## Required background recovery and supplemental investigations

The following probes are separate from the 22-case suite.
They assess different transport conditions. Their results cannot replace an original failed assertion.

### Delayed refresh delivery: FAILED

Definition and assertion mapping: [PROBE-DELAYED-REFRESH](test-cases.md#probe-delayed-refresh).

The actual service returned HTTP 200 while access remained valid.
The driver held browser delivery for 58.537 seconds without overriding clocks.
Service response time: `2026-10-20T14:25:12.836Z`.
Browser delivery time: `2026-10-20T14:26:11.373Z`.
The page returned after access expiry. It displayed the timeout prompt with Extend disabled.
The returned refresh credential had 84.627 seconds remaining at delivery.
Extend remained disabled after delivery. No relogin request occurred.
The actual logout request returned HTTP 200. Sign-in appeared and stored access was absent.
This local browser result reproduced the controlled unit failure.

Evidence: [analysis](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json), [raw run](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/run.json),
[derived result](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json), and [separate driver and source binding](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json).
Captures: [before](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/before.png), [return](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/return.png),
and [after](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/after.png).

Consequence: delayed successful refresh delivery does not preserve usable manual renewal under this fixture.
Owner: unknown application owner. Next action: review pending-refresh and timeout state before an authorized correction.
Inference: timeout starts logout while usable refresh credentials remain in transit.
Source inspection supports this inference. The probe does not establish natural freezing or production provider behavior.
No click was sent to the disabled Extend control.
Raw `heldRefresh.requestAt` contains an invalid epoch timestamp. Its bytes remain unchanged; ignore that field.
Timing conclusions use service response, browser delivery, lifecycle, network, and credential expiry records.

### Thirty-minute recovery without held responses: PASSED

Definition and assertion mapping: [PROBE-NATURAL-IMMEDIATE](test-cases.md#probe-natural-immediate).

This independent probe uses real background time without holding the refresh response.
Evidence: [run](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/run.json); [result](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/supplemental/result.json)
The probe recovered after 1,800,011 milliseconds hidden, with freeze and resume events.
Actual relogin installed the returned access token. Protected validation returned HTTP 200 and `result=true`.
The [integrity review](evidence/minor-branch-rerun-20261020/integrity-review.json) confirms the complete hidden interval.
No additional successful login response was observed. A complete login-request inventory was not retained.
The prompt closed 54 milliseconds before the relogin response callback. This does not establish [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169).
It cannot substitute for [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169) pending-prompt behavior or erase the delayed-refresh failure.
Owner: unknown application owner. Review its retained predicates and the full-interval integrity check.

## Unit execution and build readiness

<details>
<summary>Show historical unit commands, failures, compiler errors, and build limits</summary>

This section preserves the 20 October execution. Use [current synchronization](#current-issue-synchronization) for the latest unit and compiler results.

| Check | Historical result | Retained evidence and limit |
| --- | --- | --- |
| Full existing Jest suite | 411 passed; 1 failed; 412 tests. Exit 1. | 115 passing suites; 1 failed. [result](evidence/minor-branch-rerun-20261020/unit/full-result.json); [command and provenance](evidence/minor-branch-rerun-20261020/unit/full-run.json); [log](evidence/minor-branch-rerun-20261020/unit/full.log) |
| Declared build:types check | FAILED; 2 TS2322 diagnostics. Exit 2. | [command and provenance](evidence/minor-branch-rerun-20261020/unit/typecheck-run.json); [diagnostics](evidence/minor-branch-rerun-20261020/unit/typecheck.log). Emission and incremental writes disabled. |
| Initial f025 source comparison | PASSED with the same current installed dependencies; exit 0. | [isolated comparison](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json); [log](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck.log). Historical dependencies were not recreated. |
| Full production build | NOT_RUN | Declared command: `npm run build`. `.storybook` is absent. Production configuration suitability remains unknown. |

Exact retained commands:

```sh
npm test -- --config jest.config.ts --runInBand --forceExit --json --outputFile=/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/portal-background-session-20261019/evidence/minor-branch-rerun-20261020/unit/full-result.json --coverageDirectory=/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/mfe-minor-jest-y05v605q/coverage --cacheDirectory=/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/mfe-minor-jest-y05v605q/cache
npm run build:types -- --noEmit --emitDeclarationOnly false --incremental false
```

The failed unit journey holds a hide refresh response until access expiry, then attempts manual Extend.
Assertion: `src/pages/Home/common/sessionLifecycle.test.tsx:364` at `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Expected: renewed response access in the store. Actual: the initial access token remained.
Source-backed inference: timeout starts logout without refresh credentials, disables Extend, and ignores later refresh arrival.
The supplemental actual-browser probe reproduced this failure within the local fixture.
Evidence: [unit analysis and exact source receipts](evidence/minor-branch-rerun-20261020/unit/analysis.json).

The historical compiler errors occurred at `src/pages/Home/index.test.tsx:183:30` and `:184:30`.
Exact diagnostic: `Type '{ parentElement: { parentElement: { id: string; }; }; }' is not assignable to type 'EventTarget'.`
Both diagnostics are unchanged from immediate parent `f21654a` by source identity.
They are change-derived relative to initial baseline `f025513`, which passed the isolated comparison.
`handleChange` changed from implicit `any` to `React.SyntheticEvent` at `f21654a`.
The old fabricated targets no longer satisfy that parameter type.
No separate immediate-parent compiler execution occurred. Historical dependency installation remains untested.

Unit limits: JSDOM, fake timers, controlled Axios, reused dependencies, and private toolkit `0.0.7-local-mock`.
`--forceExit` bounds existing open handles. It does not establish clean process shutdown.
The local webpack fixture excludes the production type checker.
Browser completion therefore does not establish declared typecheck or full-build readiness.
No source correction occurred in that browser stage. The later [test-only repair](test-cases.md#review-f04) resolved the compiler errors.

</details>

## Retained evidence inventory

<details>
<summary>Show retained evidence identities and SHA-256 hashes</summary>

| Evidence ID | Locator | SHA-256 | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| MINOR-MANIFEST | [browser-manifest.json](evidence/minor-branch-rerun-20261020/browser-manifest.json) | `2cc915c3bc18b89e8a6c477e72be66fe1d180599c98a0dd278417c6d0406d524` | MINOR-session-browser-20261020 | Retained 20 October cases, attempts, setup failures, and supplemental references. |
| MINOR-INVENTORY | [case-inventory.json](evidence/minor-branch-rerun-20261020/case-inventory.json) | `9584c7462c48f21cc1dae2c730c3bec786a1a27cc17aedad94392ccb6e4e86bd` | MINOR-session-browser-20261020 | Executed definitions bind the retained 7a module and helper assertion lines. |
| MINOR-ASSESSMENT | [acceptance-assessment.json](evidence/minor-branch-rerun-20261020/acceptance-assessment.json) | `7607e73646e858dd36323c3d92782478a4e1df8d49bbeba0083612b754f53c8e` | MINOR-session-browser-20261020 | Decision recommendations only. Its execution checkpoint can precede this manifest. |
| MINOR-STAGE | [stage-baseline.json](evidence/minor-branch-rerun-20261020/stage-baseline.json) | `10f78c9ef846ddaaf61d877421e557f5d6824e166be220da506c37d6161899ae` | MINOR-session-browser-20261020 | Read-only evidence collection scope. No acceptance waiver or release approval. |
| MINOR-FIXTURE | [fixture-binding.json](evidence/minor-branch-rerun-20261020/fixture-binding.json) | `91917910ab1ba6de7e5229c0587911ccd36fcb8181118b78361eedb0b8446359` | MINOR-session-browser-20261020 | Local runtime sources, services, substitutions, profiles, and driver hashes. |
| MINOR-IMPACT | [source-impact-review.json](evidence/minor-branch-rerun-20261020/source-impact-review.json) | `8cb3d56d536b7179410caf78ee1c4f0f499a138a11d933880780233b870e474a` | MINOR-session-browser-20261020 | Exact source relationships. Predictions remain separate from observed results. |
| MINOR-UNIT | [analysis.json](evidence/minor-branch-rerun-20261020/unit/analysis.json) | `333f55e0602d959f452803b92f099319451be6ab3248c906260ed682c06c31c5` | MINOR-session-browser-20261020 | Historical unit failure and two compiler diagnostics, before the test-only repair. |
| MINOR-UNIT-INPUTS | [execution-inputs.json](evidence/minor-branch-rerun-20261020/unit/execution-inputs.json) | `50135cfab83457dbf80eb66b0dd43a61df17858e11e1d86691eabc09f9f1fab0` | MINOR-session-browser-20261020 | Before-source hashes and installed runtime versions. |
| MINOR-UNIT-RUN | [full-run.json](evidence/minor-branch-rerun-20261020/unit/full-run.json) | `747a173105b4649dd28068e30fd64952023316308ae292f58894fea869015184` | MINOR-session-browser-20261020 | Exact unit command, result, timing, and after-source hashes. |
| MINOR-UNIT-RESULT | [full-result.json](evidence/minor-branch-rerun-20261020/unit/full-result.json) | `05da4712cbf0238d40230c3ec0d8ae1351d22902791babd0983a4363a60fcccb` | MINOR-session-browser-20261020 | Historical Jest outcomes, including the retained failure. |
| MINOR-TYPE-RUN | [typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/typecheck-run.json) | `aad026b903a8c3cdeeb3cacea369027ca41e4df42649384bcc31ca99fb5357ab` | MINOR-session-browser-20261020 | Exact compiler command, result, timing, and after-source hashes. |
| MINOR-INITIAL-TYPE-RUN | [initial-baseline-typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json) | `7a5b3509c10dee342c0adf7c24320c90a7d7142c2fa4aa2ff3615c883e1ae2e6` | MINOR-session-browser-20261020 | Initial source with current dependencies. No environment files copied. |
| MINOR-DELAYED | [analysis.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json) | `8b7d4a4cd30eeac1be80bfbc209b96882237e594cbdbca1a0f2aa079310af671` | MINOR-session-browser-20261020 | Supplemental failure. Invalid raw requestAt timestamp explicitly excluded. |
| MINOR-DELAYED-SOURCE | [source-binding.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json) | `fea9d9310b43f2d1b3acd770d54c48eb4eb274c944eed9a562971d1a08e8aea7` | MINOR-session-browser-20261020 | Separate driver snapshots and source binding. |
| MINOR-PRIOR-DOCS | [manifest.json](evidence/minor-branch-rerun-20261020/prior-documents/manifest.json) | `0684068855b71fb6221b05c8cf8bee4018f03b8bb3409bdda799d146670b21ea` | MINOR-session-browser-20261020 | Immutable prior document bytes from an unpublished local commit. |

Per-case run, result, and screenshot hashes remain in the browser manifest. Every completed case retains its original bytes.

</details>

## Browser evidence bindings

<details>
<summary>Show screenshot timestamps, hashes, and assertion bindings</summary>

| Case and step | Capture time and phase | Screenshot or trace | SHA-256 | Assertion or request evidence | Supported claim and limit |
| --- | --- | --- | --- | --- | --- |
| [E2E-01](test-cases.md#e2e-01) / mouse | 2026-10-20T14:21:25.881Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/after.png) | `ea8fceb7608c65b1cfa7092ed804bc0c7bb0ae8c29e6aaaa225333c9d881f549` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-02](test-cases.md#e2e-02) / keyboard | 2026-10-20T14:21:53.299Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/after.png) | `6bbdb87242de94ca38f412f40c98bbbde340697bdcb75744964879da06e744f5` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-03](test-cases.md#e2e-03) / scroll | 2026-10-20T14:22:20.287Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/after.png) | `ea8fceb7608c65b1cfa7092ed804bc0c7bb0ae8c29e6aaaa225333c9d881f549` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-04](test-cases.md#e2e-04) / pending | 2026-10-20T14:23:26.894Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/after.png) | `4cbf83b840d853e93df0ac3a56e19083f458dbf90ebd4e280ecb96476407aae6` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-05](test-cases.md#e2e-05) / retry | 2026-10-20T14:24:32.561Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/after.png) | `bb8f0cfbc2858c0ec022fd8fe44ac7f9cb125eb8733ae6cecf6cdef433cc2067` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-06](test-cases.md#e2e-06) / cross | 2026-10-20T14:27:09.054Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/after.png) | `420f63b52721efb28f78717332a22d79a7d7e40fe4a804b6dbf0f111b05903a5` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-07](test-cases.md#e2e-07) / natural | 2026-10-20T14:50:10.359Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/after.png) | `f3f43e9c146c06d186a284cce71cd129ca318231b6d1be694ed2ec849bc8bc65` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-08](test-cases.md#e2e-08) / single | 2026-10-20T14:27:34.481Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/after.png) | `7b1e03e1a2fc006466e653f65dc6d41d3abc50e40665777979d7895bef755751` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-09](test-cases.md#e2e-09) / rapid | 2026-10-20T14:33:17.488Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/after.png) | `ac013116c26f9ed81c6055fc726df11c2b14e186e6cfa89b418c47b7802dca4f` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-10](test-cases.md#e2e-10) / keyboardExtend | 2026-10-20T14:34:24.802Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/after.png) | `1b6c131f6d8b5b2bdc123bea2941611493919587c09b946090f865150ce6a2a2` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-11](test-cases.md#e2e-11) / activityRetry | 2026-10-20T14:34:53.271Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/artifacts/after.png) | `9e2b229b5c0f894bbdf1d059708318c1311e8698f0b3bfe5b96f06c3a598fc13` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-12](test-cases.md#e2e-12) / inconsistent | 2026-10-20T14:35:12.238Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/after.png) | `eb9a6866d985275086dc17559a76b93394baf7b1c37a195a5ca5cccc1f49384e` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-13](test-cases.md#e2e-13) / promptActivity | 2026-10-20T14:36:26.323Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/after.png) | `3e0ceae7eefdd856173b40b5c1347f4d76f4c8ad29c222a7677cecf1dbc7341d` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-14](test-cases.md#e2e-14) / idleLogout | 2026-10-20T14:37:33.047Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/after.png) | `b42f85cbc98f2a38a5181fcbaa6d46c670df143ac49b3974e8325c453a5ee169` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-15](test-cases.md#e2e-15) / visibility | 2026-10-20T14:37:54.161Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/artifacts/after.png) | `05fcc262b3fb2bb00b1e107d2ef5d91ffd7001ec5bdc80a8a45f9982bc7c267f` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-16](test-cases.md#e2e-16) / reload | 2026-10-20T14:38:17.831Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/artifacts/after.png) | `3be182804fa79a0121b61d23ae85a9724f75e26dfb9434f4b87e685b48e1e42f` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-17](test-cases.md#e2e-17) / manualLogout | 2026-10-20T14:28:39.706Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/after.png) | `65a183f37413316b5345e8f31877b2b616f5aeccdeabe86a774acb6a44b44b48` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-18](test-cases.md#e2e-18) / activityLogout | 2026-10-20T14:29:08.705Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/after.png) | `b42f85cbc98f2a38a5181fcbaa6d46c670df143ac49b3974e8325c453a5ee169` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-19](test-cases.md#e2e-19) / late | 2026-10-20T14:30:24.243Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/after.png) | `e705002f3bf717ddd4d44d165e29d1c28f1745cf34af2803a8dfc7aa10f91273` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-20](test-cases.md#e2e-20) / expired | 2026-10-20T14:31:31.531Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/artifacts/after.png) | `75d6e170dafc15ff5340066c13830e8980823c68463f777a5ff954ca001761dd` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-21](test-cases.md#e2e-21) / missing | 2026-10-20T14:50:16.881Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/artifacts/after.png) | `a87cd94ac343df9ff07fa19acb308b19b06552f826cdec6e3db729c45078567b` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| [E2E-22](test-cases.md#e2e-22) / workspace | 2026-10-20T14:31:41.853Z / after | [after](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/artifacts/after.png) | `9db5771eb3a30f851c3894f9b6610295628b3a905dab7a924a2db1d970f15d3f` | [assertions and request records](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/artifacts/result.json) | Visible state only. Verdict also requires the retained assertion and request evidence. |
| SUPP-delayedRefresh / before | See full lifecycle timestamps / before | [before](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/before.png) | `e8a53374c67572ec84eb1124d11721e39a6f51dc1707906373297ef306e329c2` | [response and control state](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json) | Controlled delivery timing. No natural freeze claim. |
| SUPP-delayedRefresh / return | See full lifecycle timestamps / return | [return](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/return.png) | `37da5b295489a96f9cd232ea2fb0b653f6799196172c10b18832624f77e0e1c4` | [response and control state](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json) | Controlled delivery timing. No natural freeze claim. |
| SUPP-delayedRefresh / after | See full lifecycle timestamps / after | [after](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/after.png) | `078919b51eab0e4d93dc61d2cfe9cdd2e2bfef5e2df13cf5c67300cf7aa95478` | [response and control state](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json) | Controlled delivery timing. No natural freeze claim. |
| SUPP-naturalImmediate | See separate retained run | [run and capture references](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/run.json) | See manifest receipts | [result](evidence/minor-branch-rerun-20261020/browser/minor-naturalImmediate-20261020T142234/supplemental/result.json) | No held response. Separate from the 22 cases. |

The manifest lists every retained capture. Failure screenshots without capture timestamps do not establish exact event time.

</details>

## Historical execution summaries

<details>
<summary>Show results from earlier application revisions</summary>

Earlier runs used different application bytes. They do not verify the selected minor branch.
The retained prior report preserves their complete tables, failure explanations, evidence limits, and source identities.

| Historical run | Scoped outcomes | Retained evidence |
| --- | --- | --- |
| Original 14 cases | 12 passing local predicates and two observations. All 14 machine runs completed PASSED. | [14-case manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json); SHA-256 `75ddf4bde85430d78d67e0e1de11bc739a7ead32a7c85ea76fdae441942b570d`. Runtime `4da985a`; tests `66595b8`. |
| Earlier expanded 22 cases | 19 PASSED; one DIAGNOSTIC_PASSED; two OBSERVATION_ONLY. 25 attempts include three resolved harness failures. | [earlier 22-case manifest](evidence/expanded-e2e-20261020/browser-manifest.json); SHA-256 `bf27397a7d92a4ca1a2d515312853d34d62f6fda149ce3dbddf59ac8abaa1d3b`. Runtime `9dcf201`; actual test revisions `6de6fe8` and `7a504c1`. |
| Prior report version 3 | Historical unit result: 451 passing tests. Historical typecheck: four diagnostics. These are not current minor results. | [immutable prior report](evidence/minor-branch-rerun-20261020/prior-documents/test-execution-report.v3.52f733b.md.snapshot); Git `52f733b1379cfccdd198c589b6b5db553fdd153c`; SHA-256 `f47e94d80abc33801d59abdac7cb7bdc66950b8ddb1f35d006534de5612e4c37`. |

The earlier natural and missing-refresh attempts failed visibility setup before their intended hidden interval.
Real covering tabs corrected that setup. Their failed attempts remain in the earlier expanded manifest.
The earlier reload attempt required identical tokens after validation. Actual BFF validation legitimately rotates access.
The corrected assertion binds the request token and returned usable token separately.
The final reload rerun passed at `7a504c1`.
Earlier natural lifecycle capture lost its full freeze array during protected reload. Historical evidence states that limitation.
The prior document snapshot comes from local commit `52f733b`, which was unpublished at retention.
No remote link is asserted for that commit. The immutable local snapshot and hash preserve its bytes.

</details>

## Verification conclusion

- Behavior claim: the delayed-refresh local recovery journey failed. Required background recovery remains open.
- Current browser checkpoint: 1 DIAGNOSTIC_FAILED; 14 FAILED; 2 OBSERVATION_ONLY; 5 PASSED. The 22-case collection is complete.
- Covered conditions: only completed predicates in the outcome table, under the recorded local fixture.
- Uncovered conditions: pending predicates, post-failure assertions, exact four-hour behavior, deployed integrations, and production configuration.
- Acceptance limits: candidate deferrals remain unapproved. Observation and diagnostic outcomes do not close acceptance.
- Current unit and compiler checks pass. Delayed recovery remains an expected failure. The full production build remains unexecuted.
- Production release: no approval or deployed verification is recorded.

## Facts, inferences, and unresolved questions

- Fact: the selected minor application sources differ from the previously tested expanded runtime.
- Fact: the delayed-refresh browser probe logged out after delivery of a real successful refresh response.
- Historical fact: 20 October Jest retained one failure, and the compiler retained two errors.
- Current fact: [Jest and compiler checks pass](#current-issue-synchronization). The known delayed-recovery defect remains expected to fail.
- Fact: no accepted criterion waiver exists. Requirement candidate version 4 remains unchanged.
- Inference: pending-refresh and timeout state handling cause the delayed recovery failure. Source and independent executions support this explanation.
- Unknown: production impact under actual provider latency, browser freezing, deployed toolkit, and downstream authorization.
- Unknown: approved missing-refresh recovery and populated workspace restoration outcomes.
- Unknown: which broader renewal criteria the user will defer. Owner: unknown business owner.
- Next action: review failures and scope recommendations before an authorized implementation or acceptance change.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Delayed refresh](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json) and [unit regression](evidence/minor-branch-rerun-20261020/unit/analysis.json) | Usable refresh arrives after the manual recovery control becomes disabled. Required background scope remains open. | unknown application owner | Review timeout and pending-refresh state. Preserve both failures before an authorized correction. |
| [Current original case failures](evidence/minor-branch-rerun-20261020/browser-manifest.json) | Failed prompt or cancellation predicates leave later token and protected-operation safeguards unestablished. | unknown application owner | Review the first failed predicate. Do not infer unexecuted resurrection or overwrite behavior. |
| [Broader renewal deferral recommendations](evidence/minor-branch-rerun-20261020/acceptance-assessment.json) | Broader renewal acceptance remains open. No waiver or knowledge change exists. | unknown business owner | Approve or reject each proposed deferral after reviewing its observed failure. |
| [Historical TS2322 diagnostics](evidence/minor-branch-rerun-20261020/unit/typecheck.log) and [resolved case](test-cases.md#review-f04) | Test-only repairs resolved both event-fixture errors. Current typecheck passes. | Codex for test-only repair | None for these resolved errors. Keep production build readiness separate. |
| [Full build NOT_RUN](evidence/minor-branch-rerun-20261020/unit/analysis.json) | Production build readiness remains unestablished. The Storybook configuration is absent. | unknown build owner | Provide the configured build environment and retain the complete build result. |
| [Missing-refresh and workspace observation definitions](evidence/minor-branch-rerun-20261020/case-inventory.json) | Policy and populated application state acceptance remain unresolved. | unknown business and workspace owners | Define recovery policy and populated fixtures. Keep observation verdicts until explicit criteria exist. |
| [Local substitutions and protected validation scope](evidence/minor-branch-rerun-20261020/fixture-binding.json) | Local browser predicates do not establish deployed provider or downstream business behavior. | unknown integration owner | Bind a deployed environment and exercise the affected integration boundaries. |

## Sources

<details>
<summary>Show exact source revisions, hashes, and authority limits</summary>

| Source ID | Locator | Exact revision | SHA-256 | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-robot-modules-20261021 | [Current case map](evidence/robot-case-modules-20261021/case-mapping.json), [offline checks](evidence/robot-case-modules-20261021/offline-checks.json), and [Browser discovery](evidence/robot-case-modules-20261021/browser-discovery.json). | Test engine `975af64c55303ee4a138968813ef4e85570f96d2`. | Individual source hashes recorded in the case map. | unknown; Source organization and keyword compatibility only. Business cases were not rerun. |
| SRC-session-canonical-inputs-20261021 | [Catalog inputs](evidence/canonical-gherkin-20261021/inputs.json) and [case mapping](evidence/canonical-gherkin-20261021/case-mapping.json). | Workbench rule commit `1acd009`; selected revisions recorded in inputs. | Hashes recorded in inputs and validation. | unknown; Current definition and navigation stage. No new runtime execution. |
| SRC-session-branch-refresh-20261021 | [Fresh review inputs](evidence/code-review-refresh-20261021/inputs.json) and [reconciliation](evidence/code-review-refresh-20261021/summary.json). | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. | Exact hashes in execution setup and integrity records. | unknown; Controlled comparison, current Jest, and compiler evidence. No fresh browser or production execution. |
| SRC-session-minor-manifest-20261020 | [browser-manifest.json](evidence/minor-branch-rerun-20261020/browser-manifest.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `2cc915c3bc18b89e8a6c477e72be66fe1d180599c98a0dd278417c6d0406d524` | unknown; Retained 20 October cases, attempts, setup failures, and supplemental references. |
| SRC-session-minor-inventory-20261020 | [case-inventory.json](evidence/minor-branch-rerun-20261020/case-inventory.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `9584c7462c48f21cc1dae2c730c3bec786a1a27cc17aedad94392ccb6e4e86bd` | unknown; Executed definitions bind the retained 7a module and helper assertion lines. |
| SRC-session-minor-assessment-20261020 | [acceptance-assessment.json](evidence/minor-branch-rerun-20261020/acceptance-assessment.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `7607e73646e858dd36323c3d92782478a4e1df8d49bbeba0083612b754f53c8e` | unknown; Decision recommendations only. Its execution checkpoint can precede this manifest. |
| SRC-session-minor-stage-20261020 | [stage-baseline.json](evidence/minor-branch-rerun-20261020/stage-baseline.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `10f78c9ef846ddaaf61d877421e557f5d6824e166be220da506c37d6161899ae` | unknown; Read-only evidence collection scope. No acceptance waiver or release approval. |
| SRC-session-minor-fixture-20261020 | [fixture-binding.json](evidence/minor-branch-rerun-20261020/fixture-binding.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `91917910ab1ba6de7e5229c0587911ccd36fcb8181118b78361eedb0b8446359` | unknown; Local runtime sources, services, substitutions, profiles, and driver hashes. |
| SRC-session-minor-impact-20261020 | [source-impact-review.json](evidence/minor-branch-rerun-20261020/source-impact-review.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `8cb3d56d536b7179410caf78ee1c4f0f499a138a11d933880780233b870e474a` | unknown; Exact source relationships. Predictions remain separate from observed results. |
| SRC-session-minor-unit-20261020 | [analysis.json](evidence/minor-branch-rerun-20261020/unit/analysis.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `333f55e0602d959f452803b92f099319451be6ab3248c906260ed682c06c31c5` | unknown; Historical unit failure and two compiler diagnostics, before the test-only repair. |
| SRC-session-minor-unit-inputs-20261020 | [execution-inputs.json](evidence/minor-branch-rerun-20261020/unit/execution-inputs.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `50135cfab83457dbf80eb66b0dd43a61df17858e11e1d86691eabc09f9f1fab0` | unknown; Before-source hashes and installed runtime versions. |
| SRC-session-minor-unit-run-20261020 | [full-run.json](evidence/minor-branch-rerun-20261020/unit/full-run.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `747a173105b4649dd28068e30fd64952023316308ae292f58894fea869015184` | unknown; Exact unit command, result, timing, and after-source hashes. |
| SRC-session-minor-unit-result-20261020 | [full-result.json](evidence/minor-branch-rerun-20261020/unit/full-result.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `05da4712cbf0238d40230c3ec0d8ae1351d22902791babd0983a4363a60fcccb` | unknown; Historical Jest outcomes, including the retained failure. |
| SRC-session-minor-type-run-20261020 | [typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/typecheck-run.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `aad026b903a8c3cdeeb3cacea369027ca41e4df42649384bcc31ca99fb5357ab` | unknown; Exact compiler command, result, timing, and after-source hashes. |
| SRC-session-minor-initial-type-run-20261020 | [initial-baseline-typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json) | f025513f696476a9cc8162681410cbd21e029bcb | `7a5b3509c10dee342c0adf7c24320c90a7d7142c2fa4aa2ff3615c883e1ae2e6` | unknown; Initial source with current dependencies. No environment files copied. |
| SRC-session-minor-delayed-refresh-20261020 | [analysis.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `8b7d4a4cd30eeac1be80bfbc209b96882237e594cbdbca1a0f2aa079310af671` | unknown; Supplemental failure. Invalid raw requestAt timestamp explicitly excluded. |
| SRC-session-minor-delayed-source-20261020 | [source-binding.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `fea9d9310b43f2d1b3acd770d54c48eb4eb274c944eed9a562971d1a08e8aea7` | unknown; Separate driver snapshots and source binding. |
| SRC-session-minor-prior-docs-20261020 | [manifest.json](evidence/minor-branch-rerun-20261020/prior-documents/manifest.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `0684068855b71fb6221b05c8cf8bee4018f03b8bb3409bdda799d146670b21ea` | unknown; Immutable prior document bytes from an unpublished local commit. |
| SRC-session-review-intent-v4 | [knowledge/candidates/requirements/REQ-active-session-renewal.md](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) | d6adcff452f1329d99528f0f7e8a6450a27ddc8c | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` | unknown; pending human review; no business approval inferred. |
| Frozen intake | [tasks/portal-background-session-20261019/intake.md](intake.md#L263) | cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c | `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948` | unknown; pending human review; no business approval inferred. |
| Executed E2E module, 20 October | [retained 7a source](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot) | 7a504c13a8d51bb52af5cc89bd4af88d1988da94 | `94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984` | unknown; inspected assertions establish only their recorded predicates. |
| Previous report v3 | [local immutable snapshot](evidence/minor-branch-rerun-20261020/prior-documents/test-execution-report.v3.52f733b.md.snapshot) | 52f733b1379cfccdd198c589b6b5db553fdd153c | `f47e94d80abc33801d59abdac7cb7bdc66950b8ddb1f35d006534de5612e4c37` | unknown; unpublished local source revision; historical scope only. |

</details>

### Automated document checks

The historical renderer checked headings, case IDs, revision bindings, manifest counts, and receipt hashes.
It checked prior snapshot hashes and the exact executed test snapshot hash.
These checks do not establish business acceptance or full ASD-STE100 compliance.
ASD review remains pending. Reviewer and review time remain null.
The [historical checks](evidence/minor-branch-rerun-20261020/final-validation.json) retain that stage's lint, workspace validation, and document hashes.
The [catalog synchronization checks](evidence/canonical-gherkin-20261021/validation.json) apply to that earlier authoring stage and definition bindings.

This readability edit passed artifact lint, local path checks, source line bounds, and diff checks.
All 21 headings and 22 outcome classifications remain unchanged.
Four lint warnings remain: unknown owner, pending business review, unresolved content, and pending ASD writing review.
