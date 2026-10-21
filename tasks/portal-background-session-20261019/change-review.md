---
artifact_kind: change-request
id: CHANGE-session-post-review-20261020
version: 8
status: draft
owner: unknown
source_refs:
  - SRC-session-uat-timeout-inquiry-20261021
  - SRC-session-branch-refresh-20261021
  - SRC-session-baseline-reassessment-20261021
  - SRC-session-minor-stage-20261020
  - SRC-session-review-intent-v4
  - SRC-session-minor-browser-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - REVIEW-session-minor-20261021
  - EXEC-session-renewal-browser-20261020
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

# Reduced session-change assessment

> **Action required: confirm automatic renewal during the UAT idle failure.**
> The user reports an untouched background tab with Cashflow Dashboard open.
> The dashboard can renew access through automatic queries. This can prevent the idle dialog.
> Action: correlate dashboard queries, `/sso/extend`, and access expiry in UAT.
> Consequence: UAT cause confirmation and idle-timeout acceptance remain blocked.
> Owner: unknown application owner. Evidence: [UAT inquiry](#uat-timeout-inquiry-21-october-2026).
> Source inspection supports this mechanism. No UAT network capture establishes causation.

> **🔴 Action required: two P2 regressions remain.**
> Correct [active-session cutoff](code-review-minor-20261021.md#f-01-p2-preserve-active-access-across-the-refresh-deadline) and [stale-credential reuse](code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: active access can end; stale credentials can clear a fresh session.
> Owner: unknown application owner. Evidence: [paired results](evidence/code-review-refresh-20261021/summary.json).
>
> **👤 Decision required: delayed recovery and broader deferrals remain open.**
> Decide whether to correct delayed recovery or explicitly accept a named fallback.
> Name each broader criterion proposed for deferral. Acceptance remains open until those decisions are recorded.
> Owner: user and unknown authentication owner. Evidence: [failed recovery](test-cases.md#review-delayed-scheduled) and [scope request](evidence/minor-branch-rerun-20261020/user-request.txt).
> Controlled local evidence does not establish production frequency or release approval.

## Read this first

| Status | Key point | Details |
| --- | --- | --- |
| UAT idle failure | Dashboard polling can renew access without human activity. Causation remains unconfirmed. | [UAT inquiry](#uat-timeout-inquiry-21-october-2026). |
| 🔴 Two P2 regressions | Active cutoff is conditional. Stale-response reuse can end a fresh session. | [Current findings](code-review-minor-20261021.md#review-findings). |
| 🟠 Inherited recovery defect | Both versions logout after delayed credentials arrive. | [Old/new comparison](code-review-minor-20261021.md#inherited-delayed-refresh-recovery). |
| 🟡 P3 timer issue | Request count changes. No user-visible difference was demonstrated. | [Timer finding](code-review-minor-20261021.md#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late). |
| ✅ Local checks complete | Compiler passes. 413 runner passes include one expected failure. | [Latest checks](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). |
| ⏳ Acceptance open | No criterion waiver or release approval is recorded. | [Decisions and blockers](#unknowns-and-blockers). |

Use [case definitions](test-cases.md#catalog-navigation) for steps and assertions.
Use the [execution report](test-execution-report.md#assertions-and-outcomes) for historical browser outcomes.
Use the [evidence index](evidence/index.md) for source records and historical documents.

## Request and source facts

The user reported a missing timeout dialog after deploying the MFE to UAT on 21 October 2026.
The reported wait includes a return after approximately thirty minutes. This is a user observation, without retained UAT execution.
The user identifies the latest `feature/session-refresh-minor` commit and an untouched background tab containing Cashflow Dashboard.
The exact deployed artifact, dashboard version, and effective session settings remain unverified.
The user asks whether this behavior is expected and whether previous review identified it.
The [UAT inquiry](evidence/uat-timeout-inquiry-20261021/user-request.txt) preserves the report and clarification answers.

The user selected `feature/session-refresh-minor` to reduce application changes.
The [scope request](evidence/minor-branch-rerun-20261020/user-request.txt) requires background recovery and permits discussion of broader deferrals after execution.
The [latest code-review request](evidence/code-review-refresh-20261021/inputs.json) authorized review and local validation against `main`.
The current documentation request changes presentation and local navigation only.
No business criterion changed. The [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains version 4, pending publication review.

## Stage boundary and readiness

| Field | Current assessment |
| --- | --- |
| Named phase | Local branch review against main; complete. |
| Readiness | `READY` for that named review phase only. |
| Assessor and time | Codex; timestamps in [review inputs](evidence/code-review-refresh-20261021/inputs.json). |
| Rationale | Exact source review and fresh paired checks support the completed review. |
| Baseline | `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Runtime candidate | `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Reviewed head | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; later changes repair tests only. |
| Frozen intake | [Original issue](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| Preservation | [Review integrity](evidence/code-review-refresh-20261021/integrity.json) retains source, refs, intake, and pre-existing build-cache hashes. |
| Pending actions | Runtime correction requires separate scope. Acceptance decisions and release approval remain open. |
| Owners | User for scope decisions; unknown application, authentication, and release owners. |

Review readiness does not establish acceptance, successful recovery, or production readiness.
Documentation checks and preserved evidence hashes appear in the [clarity checks](evidence/document-clarity-20261021/validation.json).

## Proposed change

The application changes were already implemented when review began.
The earlier [test repair](evidence/baseline-reassessment-20261021/commit-binding.json) changed two test files and preserved runtime bytes.
The latest review made no application changes. Runtime suggestions remain unapplied.
This documentation revision removes repeated explanations and distinguishes current status from historical results.

## Scope and affected artifacts

| Artifact | Exact source | Effect and limit | Owner |
| --- | --- | --- | --- |
| `mfe-base` | Runtime and reviewed head above. | Local review covers authentication, Home lifecycle, request, and Timeout paths. | unknown application owner |
| Executed browser tests | `ratan-test-engine` `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. | 22 cases completed on 20 October. Results retain their original assertions. | unknown test owner |
| Reorganized Robot modules | `ratan-test-engine` `975af64c55303ee4a138968813ef4e85570f96d2`. | [Offline checks passed](evidence/robot-case-modules-20261021/offline-checks.json). Business execution remains `NOT_RUN`. | unknown test owner |
| Local BFF fixtures | `85d7cc03eb12710d6facf581987fd4ae24fc9844`. | Synthetic provider adapters limit integration claims. | unknown service owner |
| Task documents | Current stage, review, execution report, catalog, and index. | Low editorial risk. Frozen documents and retained execution bytes remain unchanged. | Codex |

## UAT timeout inquiry: 21 October 2026

**The missing dialog is consistent with automatic dashboard renewal. It is not established as intended idle behavior.**
The [user report](evidence/uat-timeout-inquiry-20261021/user-request.txt) identifies Cashflow Dashboard in an untouched background tab.
The latest local MFE head is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Its runtime remains `6d4c37c839b99d14ea41fd936da1a36cda526b17`. The user reports deploying the latest minor branch.
No retained UAT artifact proves those bytes. The supplied dashboard has no established independent Git revision.

### Claims and evidence

| Claim | Class | Evidence | Limit and next action |
| --- | --- | --- | --- |
| The dashboard repeats queries after each iteration, with a 120-second delay. | Inspected implementation | [Loop](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Dashboard/components/Dashboard/index.tsx#L20), [interval](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Dashboard/components/Dashboard/const.ts#L1), [queries](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Dashboard/Main/hooks/useDashboardDataQuery.ts#L47). | Local supplied copy. Confirm the deployed dashboard version. |
| Completed dashboard queries can request session extension without human activity or visibility checks. | Inspected implementation | [Installed middleware](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Dashboard/Main/store-redux/index.ts#L42), [query completion](../../repos/ui/mfe-cashflow-blotter/src/Root/rtk-query/apiSessionExtendMiddleware.ts#L7), [binding](../../repos/ui/mfe-cashflow-blotter/src/Root/import/index.ts#L16), [base helper](../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8). | Extension still requires eligible access and a successful service response. |
| Successful extension replaces access expiry and resets the dialog deadline. | Inspected implementation | [Response handling](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25), [expiry parsing](../../repos/ui/mfe-base/src/utils/login.ts#L26), [Home timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90). | UAT request outcomes and effective expiry remain unavailable. |
| Automatic renewal likely explains this reported UAT condition. | Inference | The reported dashboard matches the inspected chain above. [Source receipt](evidence/uat-timeout-inquiry-20261021/analysis.json). | Capture queries, successful extension responses, and changing expiry before confirming causation. Owner: unknown application owner. |
| Previous review identified this risk, but did not verify or resolve the deployed condition. | Documented review | [R-001](code-review.md#review-findings), [impact boundary](impact-analysis.md#user-view). | These documents cover broader runtime `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`. The integration risk remained open. |
| A local idle browser case displayed the dialog. | Observed execution | [Case definition](test-cases.md#e2e-14), [visibility assertion](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L267), [retained event](evidence/minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json#L106). | Shortened local lifetimes; runtime `6d4c37c`. No representative dashboard polling or UAT parity was established. |

The prior review caught the risk category. It did not catch this specific UAT failure through representative execution.
The latest minor findings concern different failures. They do not establish a diagnosis for the missing dialog.
This inquiry adds the concrete two-minute dashboard path. It does not establish a new approved activity policy.

### Intended, old, and new behavior

Setup: use equivalent eligible access credentials and the supplied dashboard query-completion chain.
These steps describe the source comparison. They record no new test execution.

1. Open Cashflow Dashboard in the portal.
2. Leave the portal tab untouched in the background.
3. Allow successful dashboard queries and session-extension responses.
4. Compare access expiry with the dialog deadline.

| Result | Evidence and boundary |
| --- | --- |
| Intended | The [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#description) retains renewal after inactivity. API traffic classification remains an [open review action](code-review.md#review-findings). No new timeout threshold is inferred. |
| Old | Baseline `f025513f696476a9cc8162681410cbd21e029bcb` schedules the dialog from access expiry. Its unchanged helper permits query-triggered extension. Successful renewal can therefore postpone the dialog. This is a source prediction. |
| New | Head `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` retains that timer and extension path. Visibility reconciliation checks credential expiry. It does not measure elapsed human inactivity. This is a source prediction. |
| Reported UAT | The user reports no dialog after approximately thirty minutes. No retained traffic proves which credentials were renewed. |
| Classification | The inspected renewal mechanism is inherited. A new regression causing this UAT symptom remains unproved. |

### Decision and evidence limits

The source explanation and review-history answer are complete for the inspected scope.
UAT causal confirmation remains `READY_WITH_LIMITS` for further evidence collection only.
Owner: unknown application owner. Next action: bind deployed modules and correlate dashboard queries with renewal and access expiry.
Acceptance of idle timeout remains blocked until representative execution resolves this condition.
No application correction or criterion waiver is recorded.
Knowledge update: not applicable. The answers describe incident conditions and change no domain rule.
The [receipt](evidence/uat-timeout-inquiry-20261021/analysis.json) retains source hashes, excerpts, claim classes, and discovery limits.

## User impact

| Condition | Before and after | Consequence and evidence |
| --- | --- | --- |
| Initial refresh expires while renewed access remains valid. | Baseline keeps access. Candidate logs out if refresh remains unreplaced. | Sign-in interrupts active work. [REVIEW-F01](test-cases.md#review-f01). |
| An ended session returns a late refresh response. | Candidate persistence and reuse prevent replacement in two controlled conditions. | Recovery can clear a fresh session. [REVIEW-F03A](test-cases.md#review-f03a), [REVIEW-F03B](test-cases.md#review-f03b). |
| Usable refresh arrives after access expires. | Both versions leave Extend disabled and logout. | Required delayed recovery remains unmet. [REVIEW-DELAYED-SCHEDULED](test-cases.md#review-delayed-scheduled). |
| Acquisition callback runs one millisecond late. | Baseline sends one request. Candidate sends zero. | No user-visible difference was demonstrated. [REVIEW-F02](test-cases.md#review-f02). |

The [network explanation](code-review-minor-20261021.md#continuous-activity-and-network-actions) defines mouse activity and the five-second delay.
Aborting a pending refresh can reduce the stale-response race. It cannot correct active cutoff without a pending request.

## System impact

Lifecycle timers, credential persistence, and late responses cross authentication boundaries. The qualitative review risk remains medium.
The [inspection inventory](evidence/code-review-20261021/inspection.json) and [fresh inputs](evidence/code-review-refresh-20261021/inputs.json) retain affected consumers.
Controlled fixtures establish behavior differences. Deployed settings, provider behavior, and production failure frequency remain unverified.

## Options and consequences

| Option | Consequence | Decision owner |
| --- | --- | --- |
| Require all existing criteria. | Each unmet criterion remains an acceptance blocker. | user |
| Defer named broader criteria. | Specific adverse behavior remains accepted only through an explicit recorded decision. | user |
| Correct the demonstrated runtime defects. | Implementation scope and regression evidence must address the selected conditions. | user and unknown application owner |

## Proposed acceptance and validation

| Scope | Retained result | Definition and evidence |
| --- | --- | --- |
| Required background recovery | Immediate-response probe passed; delayed-response probe failed. | [Immediate case](test-cases.md#probe-natural-immediate), [delayed case](test-cases.md#probe-delayed-refresh). |
| 22 browser cases | Five passed; fourteen failed; one diagnostic failed; two observations. | [Browser outcomes](test-execution-report.md#assertions-and-outcomes). |
| Latest local checks | 116 suites; 413 runner passes, including one expected failure. Compiler passes. | [Latest validation](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). |
| Production build and deployment | `NOT_RUN`; local checks do not establish production parity. | [Build boundary](test-execution-report.md#unit-execution-and-build-readiness). |

## Implementation and release proposal

Runtime corrections remain unapplied. No production release is proposed by this review.
Required natural browser cases use at least 30 minutes of actual hidden time.
A later implementation stage must bind its exact source and repeat the affected assertions.

## Sources and evidence limits

| Source ID | Locator | Identity and limit |
| --- | --- | --- |
| SRC-session-uat-timeout-inquiry-20261021 | [Report and answers](evidence/uat-timeout-inquiry-20261021/user-request.txt), [source receipt](evidence/uat-timeout-inquiry-20261021/analysis.json). | Latest minor branch reported in UAT; source explanation only. No retained UAT traffic confirms causation. |
| SRC-session-branch-refresh-20261021 | [Inputs](evidence/code-review-refresh-20261021/inputs.json), [reconciliation](evidence/code-review-refresh-20261021/summary.json). | Exact endpoints above; fresh local review only. |
| SRC-session-review-intent-v4 | [Requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`; publication review pending. |
| SRC-session-minor-stage-20261020 | [Scope request](evidence/minor-branch-rerun-20261020/user-request.txt), [stage baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json). | Original authorization and source hashes; no criterion waiver. |
| SRC-session-baseline-reassessment-20261021 | [Stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json), [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json). | Test-only repair and paired comparisons; controlled fixtures. |
| SRC-session-minor-browser-20261020 | [Browser manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json). | 22 retained outcomes, screenshots, hashes, and separate probes. |
| Prior stage record | [Immutable stage version 1](evidence/minor-branch-rerun-20261020/prior-documents/change-review.v1.52f733b.md.snapshot). | SHA-256 `6c8bdbc8ee3ca13696b9544f729e0c449f73b3594193a9bb1aa17558795a3de8`; historical broader implementation. |

## Unknowns and blockers

| Decision or missing evidence | Blocked action | Owner | Next action |
| --- | --- | --- | --- |
| Reported UAT idle failure lacks correlated deployment and traffic evidence. | UAT cause confirmation and representative idle acceptance. | unknown application owner | Correlate dashboard queries, successful extension, and access expiry. [Inquiry](#uat-timeout-inquiry-21-october-2026). |
| Required delayed recovery remains failed. | Acceptance of the full required background scope. | user and unknown authentication owner | Decide a targeted correction or an explicit fallback policy. [Failed probe](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json). |
| Broader criterion deferrals are unnamed. | Acceptance waiver claims. | user | Review [failure recommendations](test-execution-report.md#failure-limits-and-recommended-dispositions) and name each decision. |
| Deployed settings, provider paths, and build evidence are unavailable. | Production readiness and release approval. | unknown release owner | Bind representative deployment and build evidence before a release decision. |

## Stage evidence and completion

| Stage | Status | Evidence and remaining action |
| --- | --- | --- |
| Local review and comparative checks | `READY`; complete. | [Latest review](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). Runtime defects remain open. |
| Browser evidence collection | `READY`; complete for the historical selected runtime. | [Execution report](test-execution-report.md). Review failures before acceptance. |
| Documentation clarity | Complete after the linked checks. | [Validation](evidence/document-clarity-20261021/validation.json). Full ASD review remains pending. |
| Acceptance and release | No approval recorded. | Resolve the [named blockers](#unknowns-and-blockers). |

## Requested decision and actual disposition

The user requested a smaller change and evidence before deciding broader deferrals.
No named failure is accepted. No criterion waiver is recorded.
Correct or explicitly decide delayed recovery before accepting the required background scope.
The two demonstrated P2 regressions remain open. Unrestricted production rollout is not recommended.

## Saved execution and interruption recovery

Checkpoint `bd36532` retains completed browser cases and screenshots.
The [integrity review](evidence/minor-branch-rerun-20261020/integrity-review.json) reconciles their source bindings and checkpoints.
The [progress record](evidence/baseline-reassessment-20261021/progress.json) preserves completed comparisons, failures, and the initial runner error.

## Initial branch code review: 21 October 2026

**📚 Historical:** the initial review reported four findings and two compiler errors.
The [initial inputs](evidence/code-review-20261021/inputs.json) retain those results.
The later repair resolves the compiler finding. Current findings supersede the original four-open-findings conclusion.

## Test repair and baseline reassessment: 21 October 2026

**📚 Historical:** the [authorized test repair](evidence/baseline-reassessment-20261021/user-request.txt) changed two test files.
The [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json) preserves all 283 recorded runtime and configuration hashes.
The [paired lifecycle results](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) distinguish active cutoff from inherited delayed recovery.
The [race results](evidence/baseline-reassessment-20261021/races/analysis.json) distinguish added, worsened, and unchanged conditions.

## Gap case clarification and reusable rules: 21 October 2026

**📚 Historical:** the [case-step request](evidence/gap-case-steps-20261021/user-request.txt) required readable old/new comparisons.
The [canonical catalog](test-cases.md#current-branch-review-cases) now owns detailed case steps and assertions.
The [comparison rule](../README.md#compare-behavior-for-gap-analysis) applies to later gap analyses.
This clarification changed no business criterion or observed result.

## Fresh branch review: 21 October 2026

**✅ Latest completed code review:** all 15 changed paths received source review.
The [review](code-review-minor-20261021.md#fresh-branch-review-21-october-2026) owns execution details and limits.
The [clarification answers](evidence/code-review-refresh-20261021/clarification.json) explain active cutoff, response aborts, inherited recovery, and timer impact.
No application edit or business-rule change occurred during that review.
