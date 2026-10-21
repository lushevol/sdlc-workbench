---
artifact_kind: test-execution-report
id: EXEC-session-renewal-browser-20261020
version: 6
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

> **Critical conclusions: Action required**
>
> **Delayed background recovery remains unfixed.**
> Action: correct the [delayed-recovery case](test-cases.md#review-delayed-hide), then repeat its assertions.
> Consequence: late usable refresh credentials leave Extend disabled and permit logout.
> Owner: unknown application owner. Evidence: [browser probe](test-cases.md#probe-delayed-refresh) and [paired results](test-cases.md#review-delayed-scheduled).
>
> **Two P2 regressions remain on the reduced branch.**
> Action: assess [active-session cutoff](test-cases.md#review-f01), [stale response before sign-in](test-cases.md#review-f03a), and [stale response after sign-in](test-cases.md#review-f03b).
> Consequence: valid active access can end, or recovery can clear a fresh session.
> Owner: unknown application owner; user for scope decisions. Evidence: each linked case retains exact comparison results.
>
> **No criterion waiver is recorded.**
> Action: decide any named deferral from its retained failure and limit. Owner: user.
> Consequence: broader acceptance remains open. Evidence: [disposition recommendations](#failure-limits-and-recommended-dispositions).

## Current issue synchronization

The current branch is `feature/session-refresh-minor` at `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Runtime remains `6d4c37c839b99d14ea41fd936da1a36cda526b17`. The later commit changes tests only.
The [canonical catalog](test-cases.md) contains all current Gherkin definitions and explicit assertions.
Its [source bindings](evidence/canonical-gherkin-20261021/case-mapping.json) link executable cases back to those definitions.
No new test execution occurred during this documentation synchronization.
The later [Robot synchronization](test-cases.md#current-robot-and-javascript-source) adds stable case tags and 22 execution modules.
Test-engine revision `975af64c55303ee4a138968813ef4e85570f96d2` passes [offline compatibility checks](evidence/robot-case-modules-20261021/offline-checks.json).
The new organization has business execution status `NOT_RUN`. Historical browser verdicts and their source bindings remain unchanged.

| Evidence scope | Latest retained result | Definition and evidence |
| --- | --- | --- |
| 22 browser cases, 20 October | Five passed; fourteen failed; one diagnostic failed; two observations. Collection is complete. | [Case outcomes](#assertions-and-outcomes), [manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json), and [canonical definitions](test-cases.md#procedure-and-assertions). |
| Immediate background recovery | Local recovery and protected validation passed after 1,800,011 milliseconds hidden. Pending-prompt acceptance remains unverified. | [Immediate probe](test-cases.md#probe-natural-immediate). |
| Delayed background recovery | Browser recovery failed. Both controlled baseline and candidate also failed. | [Browser probe](test-cases.md#probe-delayed-refresh), [paired scheduled case](test-cases.md#review-delayed-scheduled), and [hide-triggered case](test-cases.md#review-delayed-hide). |
| Current Jest, 21 October | 116 suites; 413 runner passes, including one expected failure. | [Run](evidence/code-review-refresh-20261021/suite-suite-suite/run.json). The [expected-failure definition](test-cases.md#review-delayed-hide) remains unmet. |
| Current TypeScript, 21 October | Passed. The two historical event-fixture errors were repaired. | [Resolved case](test-cases.md#review-f04) and [compiler run](evidence/code-review-refresh-20261021/types-corrected/run.json). |
| Current review comparison | Two P2 regressions and one P3 scheduling issue remain. The latter shows no user-visible difference in its controlled check. | [Current review](code-review-minor-20261021.md#review-findings) and [paired evidence](evidence/code-review-refresh-20261021/summary.json). |
| Full production build | `NOT_RUN`. | [Historical build boundary](#unit-execution-and-build-readiness). No deployment verification is established. |

The earlier unit failure and compiler errors below remain historical evidence.
Their runner statuses do not override the latest checks or establish successful recovery.
The [current review](code-review-minor-20261021.md#continuous-activity-and-network-actions) explains activity debounce and the network gap.

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
AC links open exact candidate-version-4 Gherkin. Historical TC links preserve the frozen proposed scopes.
The [alias table](test-cases.md#frozen-regression-aliases) maps those scopes to current definitions and coverage limits.

Source definitions do not establish approval. Some proposed case scopes have no independent approved BDD.

| Definition set | Exact definition links | Scope and limits |
| --- | --- | --- |
| Acceptance criteria | [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140); [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147); [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154); [AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162); [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176); [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183) | Candidate requirement version 4. [AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) specifies four controlled hours. |
| Proposed regression scopes | [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263); [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264); [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265); [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266); [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267); [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268); [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) | Frozen intake. Missing-refresh and populated workspace policies remain unresolved. |

## Case mapping

Each case ID links its retained definition. The outcome table links its BDD, executed assertions, and evidence separately.

[Current 22-case inventory](evidence/minor-branch-rerun-20261020/case-inventory.json) supplies exact 7a source and helper line mappings.

## Assertions and outcomes

All inspected functions below belong to the retained `7a504c1` test module.
The current inventory supplies assertion locations, helper functions, and per-function hashes.
The full module SHA-256 is recorded below. Definition links bind exact requirement or frozen-intake revisions.
[AC-4-live-boundary](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) tests the shortened refresh boundary. It does not test the exact four-hour criterion.
`OBSERVATION_ONLY` and diagnostic outcomes do not establish business acceptance.
For failed cases, later assertions remain unestablished. A cancellation failure alone does not prove token resurrection or overwrite.

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [E2E-01](test-cases.md#e2e-01) / `mouse` | [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); asserts 234,242,255,256,257,258,261<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:256](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L256) | Trusted mouse activity renews access within 15 seconds and passes protected validation. | `At least one successful renewal must finish within the 15-second continuous-activity interval.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/result.json) |
| [E2E-02](test-cases.md#e2e-02) / `keyboard` | [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147) | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); asserts 234,242,255,256,257,258,261<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:256](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L256) | Trusted keyboard activity renews access within 15 seconds and passes protected validation. | `At least one successful renewal must finish within the 15-second continuous-activity interval.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/result.json) |
| [E2E-03](test-cases.md#e2e-03) / `scroll` | [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154) | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L231); asserts 234,242,255,256,257,258,261<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:256](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L256) | Trusted scroll activity renews access within 15 seconds and passes protected validation. | `At least one successful renewal must finish within the 15-second continuous-activity interval.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/result.json) |
| [E2E-04](test-cases.md#e2e-04) / `pending` | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176); [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263) | [assertPendingRenewalCompletes:313](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L313); asserts delegated<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:290](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L290) | Pending renewal closes zero prompts; actual success closes once and passes protected validation. | `The prompt must remain visible while renewal is pending.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/result.json) |
| [E2E-05](test-cases.md#e2e-05) / `retry` | [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183); [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264) | [assertRejectedRenewalCanRetry:320](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L320); asserts 329,330<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:329](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L329) | Transport failure preserves the prompt; actual retry installs access and closes once. | `Rejected renewal must leave the prompt visible.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/result.json) |
| [E2E-06](test-cases.md#e2e-06) / `cross` | [AC-4-live-boundary](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) | [assertActivityCrossesRefreshExpiry:601](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L601); asserts 614,624,625,626,628,629,630,631,632,633,636<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:625](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L625) | Activity crosses initial refresh expiry without sign-in or prompt and passes protected validation. | `The authenticated portal must remain available.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json) |
| [E2E-07](test-cases.md#e2e-07) / `natural` | [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265); [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268); [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [assertNaturalBackgroundRecovery:643](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L643); asserts 653,661,662,668<br>[openPortalSession:45](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L45)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:290](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L290) | After 1,800 seconds, hidden recovery completes renewal while the visible idle control expires. | `The prompt must remain visible while renewal is pending.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/result.json) |
| [E2E-08](test-cases.md#e2e-08) / `single` | Supporting boundary; no separate criterion | [assertSlowActivitySharesRequest:706](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L706); asserts 709,721,722,726<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:721](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L721) | Repeated activity shares one pending extension with zero cancellations and installs actual renewed access. | `The same access token must share one pending extension during repeated activity.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/result.json) |
| [E2E-09](test-cases.md#e2e-09) / `rapid` | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [assertRapidExtendSharesRequest:337](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L337); asserts 348,353,354,355,356,359,361,366,368<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:347](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L347) | Two pointer attempts create one relogin; pending closure count is zero and successful closure count is one. | `locator.boundingBox: Timeout 30000ms exceeded.<br>Call log:<br>[2m  - waiting for locator('[data-testid="Extend_Btn"]')[22m<br>` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/result.json) |
| [E2E-10](test-cases.md#e2e-10) / `keyboardExtend` | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169); [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [assertKeyboardExtendActivation:378](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L378); asserts delegated<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:290](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L290) | Enter activates Extend; actual renewal installs access and closes the prompt once. | `The prompt must remain visible while renewal is pending.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/result.json) |
| [E2E-11](test-cases.md#e2e-11) / `activityRetry` | Supporting boundary; no separate criterion | [assertActivityFailureCanRetry:386](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L386); asserts 389,402,407<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187) | A failed activity extension preserves available access; later activity renews against the actual service. | Recorded assertions: `[{"failedActivityAttempts":1,"successfulActivityRetries":1,"promptVisibleAfterFailure":false}]` | PASSED | [run](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-activityRetry-20261020T143426/artifacts/result.json) |
| [E2E-12](test-cases.md#e2e-12) / `inconsistent` | Supporting boundary; no separate criterion | [assertInconsistentActivityResponseRejected:416](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L416); asserts 419,426,435,439,440,445,446,448,451,452<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:439](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L439) | A negative body preserves access; a distinct successful retry installs its actual token. | `A result=false extension response must not install its authorization header.<br>+ actual - expected` Later assertions remain unestablished. | DIAGNOSTIC_FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/result.json) |
| [E2E-13](test-cases.md#e2e-13) / `promptActivity` | Supporting boundary; no separate criterion | [assertPromptIgnoresActivity:461](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L461); asserts 480,481,482,483<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:290](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L290) | Prompt activity starts zero extensions and closes zero prompts; actual Extend later succeeds. | `The prompt must remain visible while renewal is pending.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/result.json) |
| [E2E-14](test-cases.md#e2e-14) / `idleLogout` | Supporting boundary; no separate criterion | [assertIdlePromptLogout:493](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L493); asserts 502,509,515,516,517<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267) | Idle logout clears stored access, leaves no persisted refresh, and returns to sign-in without relogin. | Recorded assertions: `[{"logoutRequestObserved":true,"storedAccessCleared":true,"persistedRefreshAbsentAfterLogout":true,"signInVisibleAfterLogout":true,"reloginRequests":0}]` | PASSED | [run](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json) |
| [E2E-15](test-cases.md#e2e-15) / `visibility` | Supporting boundary; no separate criterion | [assertQuickVisibilityRefresh:523](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L523); asserts 536,541,542,543<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187) | A short hidden switch receives one refresh response and preserves authentication on return. | Recorded assertions: `[{"hiddenRefreshRequests":1,"promptVisibleOnReturn":false,"authenticatedOnReturn":true}]` | PASSED | [run](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-visibility-20261020T143735/artifacts/result.json) |
| [E2E-16](test-cases.md#e2e-16) / `reload` | Supporting boundary; no separate criterion | [assertReloadPreservesRenewedSession:554](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L554); asserts 557,562,575,576,577,578,580,584,585,590,592<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[acquireRefresh:683](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L683)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187) | Reload validation uses the exact pre-reload renewed token and installs its actual usable response token.<br>Refresh reacquisition and protected validation succeed with zero additional login requests. | Recorded assertions: `[{"preReloadRenewedAccessUsedForValidation":true,"validationSucceeded":true,"validationResponseAccessInstalled":true,"validationRotatedAccess":true,"additionalLoginRequests":0,"refreshReacquiredAfterReload":true,"signInVisibleAfterReload":false}]` | PASSED | [run](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-reload-20261020T143756/artifacts/result.json) |
| [E2E-17](test-cases.md#e2e-17) / `manualLogout` | Supporting boundary; no separate criterion | [assertPendingManualLogoutCancels:758](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L758); asserts 773,776,780,781<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[retainLateResponse:740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740)<br>[releaseLateResponse:748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748)<br>[first failure:773](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L773) | Logout cancels pending manual renewal; late success restores neither access nor the portal. | `Pending renewal must keep the timeout prompt visible.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/result.json) |
| [E2E-18](test-cases.md#e2e-18) / `activityLogout` | Supporting boundary; no separate criterion | [assertPendingActivityLogoutCancels:790](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L790); asserts 809,810<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[emitActivity:219](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L219)<br>[standardLogout:698](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L698)<br>[retainLateResponse:740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740)<br>[releaseLateResponse:748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748)<br>[first failure:806](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L806) | Logout unmounts Home, cancels pending activity renewal, and prevents late access restoration. | `Logout or Home unmount must cancel the pending extension request.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/result.json) |
| [E2E-19](test-cases.md#e2e-19) / `late` | Supporting boundary; no separate criterion | [assertLateActivityCannotReplaceManualSuccess:820](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L820); asserts 842,845,846<br>[acquireRefresh:683](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L683)<br>[settleSetup:677](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L677)<br>[idlePrompt:267](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267)<br>[completeHeldRenewal:277](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L277)<br>[retainLateResponse:740](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L740)<br>[releaseLateResponse:748](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L748)<br>[protectedRequest:187](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L187)<br>[first failure:837](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L837) | Manual renewal survives an older activity response with exactly one prompt closure. | `Opening the timeout prompt must cancel the earlier activity extension.` Later assertions remain unestablished. | FAILED | [run](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/result.json) |
| [E2E-20](test-cases.md#e2e-20) / `expired` | [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267) | [assertActualExpiredCredentialDenied:856](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L856); asserts 863,865,868,870,879,887<br>[triggerProtectedOperation:209](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L209) | The actual service rejects a naturally expired credential with HTTP 401 or 403. | Recorded assertions: `[{"criterion":"[TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267)","expiredAccess":{"sha256":"f16b9c2b4819ee9450f083ef61a97eea92df4480773488f6439a034356fd826c","exp":1792506690,"iat":1792506630},"actualExpiryElapsedMs":1524,"initialStatus":200,"deniedStatus":401,"operationScope":"PORTAL_AUTHENTICATION_VALIDATION"}]` | PASSED | [run](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-expired-20261020T143026/artifacts/result.json) |
| [E2E-21](test-cases.md#e2e-21) / `missing` | [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) | [observeBackgroundWithoutRefresh:893](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L893); asserts 909,916,917<br>[openPortalSession:45](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L45) | Record return state after 1,800 seconds with blocked refresh acquisition and no observed refresh. | Hidden 1801814 ms; blocked acquisitions 1; sign-in visible True; refresh observed False. No approved recovery verdict exists. Full lifecycle remains in the linked result. | OBSERVATION_ONLY | [run](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-missing-20261020T141956/artifacts/result.json) |
| [E2E-22](test-cases.md#e2e-22) / `workspace` | [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) | [observeWorkspaceDescriptorsAfterSignIn:946](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L946); asserts 956<br>[workspaceSummary:929](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L929)<br>[standardLogout:698](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L698)<br>[signInIfNeeded:119](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L119) | Create two workspaces and record descriptor comparison after sign-out and same-user sign-in. | Two empty workspace descriptors compared after reauthentication. Comparison: `{"descriptorIdentityAndParametersSame":true,"entitlementsSame":true,"sameUser":true}` Application edits remain untested. | OBSERVATION_ONLY | [run](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/run.json)<br>[result](evidence/minor-branch-rerun-20261020/browser/minor-workspace-20261020T143133/artifacts/result.json) |

### Failure limits and recommended dispositions

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
The prompt closed 54 milliseconds before the relogin response callback. This does not establish [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169).
It cannot substitute for [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169) pending-prompt behavior or erase the delayed-refresh failure.
Owner: unknown application owner. Review its retained predicates and the full-interval integrity check.

## Unit execution and build readiness

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

The compiler errors occur at `src/pages/Home/index.test.tsx:183:30` and `:184:30`.
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

## Retained evidence inventory

| Evidence ID | Locator | SHA-256 | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| MINOR-MANIFEST | [browser-manifest.json](evidence/minor-branch-rerun-20261020/browser-manifest.json) | `2cc915c3bc18b89e8a6c477e72be66fe1d180599c98a0dd278417c6d0406d524` | MINOR-session-browser-20261020 | Current 22 cases, attempts, setup failures, and supplemental references. |
| MINOR-INVENTORY | [case-inventory.json](evidence/minor-branch-rerun-20261020/case-inventory.json) | `9584c7462c48f21cc1dae2c730c3bec786a1a27cc17aedad94392ccb6e4e86bd` | MINOR-session-browser-20261020 | All definitions bind the current 7a module and helper assertion lines. |
| MINOR-ASSESSMENT | [acceptance-assessment.json](evidence/minor-branch-rerun-20261020/acceptance-assessment.json) | `7607e73646e858dd36323c3d92782478a4e1df8d49bbeba0083612b754f53c8e` | MINOR-session-browser-20261020 | Decision recommendations only. Its execution checkpoint can precede this manifest. |
| MINOR-STAGE | [stage-baseline.json](evidence/minor-branch-rerun-20261020/stage-baseline.json) | `10f78c9ef846ddaaf61d877421e557f5d6824e166be220da506c37d6161899ae` | MINOR-session-browser-20261020 | Read-only evidence collection scope. No acceptance waiver or release approval. |
| MINOR-FIXTURE | [fixture-binding.json](evidence/minor-branch-rerun-20261020/fixture-binding.json) | `91917910ab1ba6de7e5229c0587911ccd36fcb8181118b78361eedb0b8446359` | MINOR-session-browser-20261020 | Local runtime sources, services, substitutions, profiles, and driver hashes. |
| MINOR-IMPACT | [source-impact-review.json](evidence/minor-branch-rerun-20261020/source-impact-review.json) | `8cb3d56d536b7179410caf78ee1c4f0f499a138a11d933880780233b870e474a` | MINOR-session-browser-20261020 | Exact source relationships. Predictions remain separate from observed results. |
| MINOR-UNIT | [analysis.json](evidence/minor-branch-rerun-20261020/unit/analysis.json) | `333f55e0602d959f452803b92f099319451be6ab3248c906260ed682c06c31c5` | MINOR-session-browser-20261020 | Current unit failure and two compiler diagnostics. |
| MINOR-UNIT-INPUTS | [execution-inputs.json](evidence/minor-branch-rerun-20261020/unit/execution-inputs.json) | `50135cfab83457dbf80eb66b0dd43a61df17858e11e1d86691eabc09f9f1fab0` | MINOR-session-browser-20261020 | Before-source hashes and installed runtime versions. |
| MINOR-UNIT-RUN | [full-run.json](evidence/minor-branch-rerun-20261020/unit/full-run.json) | `747a173105b4649dd28068e30fd64952023316308ae292f58894fea869015184` | MINOR-session-browser-20261020 | Exact unit command, result, timing, and after-source hashes. |
| MINOR-UNIT-RESULT | [full-result.json](evidence/minor-branch-rerun-20261020/unit/full-result.json) | `05da4712cbf0238d40230c3ec0d8ae1351d22902791babd0983a4363a60fcccb` | MINOR-session-browser-20261020 | All current Jest outcomes, including the retained failure. |
| MINOR-TYPE-RUN | [typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/typecheck-run.json) | `aad026b903a8c3cdeeb3cacea369027ca41e4df42649384bcc31ca99fb5357ab` | MINOR-session-browser-20261020 | Exact compiler command, result, timing, and after-source hashes. |
| MINOR-INITIAL-TYPE-RUN | [initial-baseline-typecheck-run.json](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json) | `7a5b3509c10dee342c0adf7c24320c90a7d7142c2fa4aa2ff3615c883e1ae2e6` | MINOR-session-browser-20261020 | Initial source with current dependencies. No environment files copied. |
| MINOR-DELAYED | [analysis.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json) | `8b7d4a4cd30eeac1be80bfbc209b96882237e594cbdbca1a0f2aa079310af671` | MINOR-session-browser-20261020 | Supplemental failure. Invalid raw requestAt timestamp explicitly excluded. |
| MINOR-DELAYED-SOURCE | [source-binding.json](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json) | `fea9d9310b43f2d1b3acd770d54c48eb4eb274c944eed9a562971d1a08e8aea7` | MINOR-session-browser-20261020 | Separate driver snapshots and source binding. |
| MINOR-PRIOR-DOCS | [manifest.json](evidence/minor-branch-rerun-20261020/prior-documents/manifest.json) | `0684068855b71fb6221b05c8cf8bee4018f03b8bb3409bdda799d146670b21ea` | MINOR-session-browser-20261020 | Immutable prior document bytes from an unpublished local commit. |

Per-case run, result, and screenshot hashes remain in the browser manifest. Every completed case retains its original bytes.

## Browser evidence bindings

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

## Historical execution summaries

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

| Source ID | Locator | Exact revision | SHA-256 | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-robot-modules-20261021 | [Current case map](evidence/robot-case-modules-20261021/case-mapping.json), [offline checks](evidence/robot-case-modules-20261021/offline-checks.json), and [Browser discovery](evidence/robot-case-modules-20261021/browser-discovery.json). | Test engine `975af64c55303ee4a138968813ef4e85570f96d2`. | Individual source hashes recorded in the case map. | unknown; Source organization and keyword compatibility only. Business cases were not rerun. |
| SRC-session-canonical-inputs-20261021 | [Catalog inputs](evidence/canonical-gherkin-20261021/inputs.json) and [case mapping](evidence/canonical-gherkin-20261021/case-mapping.json). | Workbench rule commit `1acd009`; selected revisions recorded in inputs. | Hashes recorded in inputs and validation. | unknown; Current definition and navigation stage. No new runtime execution. |
| SRC-session-branch-refresh-20261021 | [Fresh review inputs](evidence/code-review-refresh-20261021/inputs.json) and [reconciliation](evidence/code-review-refresh-20261021/summary.json). | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. | Exact hashes in execution setup and integrity records. | unknown; Controlled comparison, current Jest, and compiler evidence. No fresh browser or production execution. |
| SRC-session-minor-manifest-20261020 | [browser-manifest.json](evidence/minor-branch-rerun-20261020/browser-manifest.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `2cc915c3bc18b89e8a6c477e72be66fe1d180599c98a0dd278417c6d0406d524` | unknown; Current 22 cases, attempts, setup failures, and supplemental references. |
| SRC-session-minor-inventory-20261020 | [case-inventory.json](evidence/minor-branch-rerun-20261020/case-inventory.json) | 6d4c37c839b99d14ea41fd936da1a36cda526b17 | `9584c7462c48f21cc1dae2c730c3bec786a1a27cc17aedad94392ccb6e4e86bd` | unknown; All definitions bind the current 7a module and helper assertion lines. |
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
| SRC-session-review-intent-v4 | [knowledge/candidates/requirements/REQ-active-session-renewal.md](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) | d6adcff452f1329d99528f0f7e8a6450a27ddc8c | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` | unknown; pending human review; no business approval inferred. |
| Frozen intake | [tasks/portal-background-session-20261019/intake.md](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263) | cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c | `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948` | unknown; pending human review; no business approval inferred. |
| Current E2E module | [retained 7a source](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot) | 7a504c13a8d51bb52af5cc89bd4af88d1988da94 | `94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984` | unknown; inspected assertions establish only their recorded predicates. |
| Previous report v3 | [local immutable snapshot](evidence/minor-branch-rerun-20261020/prior-documents/test-execution-report.v3.52f733b.md.snapshot) | 52f733b1379cfccdd198c589b6b5db553fdd153c | `f47e94d80abc33801d59abdac7cb7bdc66950b8ddb1f35d006534de5612e4c37` | unknown; unpublished local source revision; historical scope only. |

### Automated document checks

The renderer checked required headings, 22 unique case IDs, revision bindings, manifest counts, and retained receipt hashes.
It checked prior snapshot hashes and the exact current test snapshot hash.
These checks do not establish business acceptance or full ASD-STE100 compliance.
ASD review remains pending. Reviewer and review time remain null.
The [historical checks](evidence/minor-branch-rerun-20261020/final-validation.json) retain that stage's lint, workspace validation, and document hashes.
The [catalog synchronization checks](evidence/canonical-gherkin-20261021/validation.json) apply to this revision and the current definitions.
