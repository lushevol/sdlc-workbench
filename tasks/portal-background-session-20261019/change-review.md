---
artifact_kind: change-request
id: CHANGE-session-post-review-20261020
version: 5
status: draft
owner: unknown
source_refs:
  - SRC-session-baseline-reassessment-20261021
  - SRC-mfe-code-review-20261021
  - SRC-session-minor-stage-20261020
  - SRC-session-review-intent-v4
  - SRC-session-minor-impact-20261020
  - SRC-session-minor-unit-20261020
  - SRC-session-minor-browser-20261020
  - SRC-session-minor-integrity-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - REVIEW-session-renewal-20261020
  - IMPACT-session-renewal-20261020
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

> **Critical conclusions: Action required**
>
> **Two P2 regressions remain; test-only repairs pass.**
> Action: address [active-session cutoff](code-review-minor-20261021.md#f-01-p2-preserve-active-access-across-the-refresh-deadline) and [stale-credential reuse](code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: valid active access can end, and recovery can clear a fresh session.
> Owner: unknown application owner. Evidence: [paired lifecycle](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) and [race outcomes](evidence/baseline-reassessment-20261021/races/analysis.json).
> Controlled fixtures establish behavior differences. They do not measure production frequency.
>
> **Delayed recovery is inherited and remains unfixed.**
> Action: retain the limitation when deciding required background behavior.
> Consequence: Extend stays disabled after late credentials arrive; both compared revisions logout.
> Owner: unknown application owner; user for acceptance decisions. Evidence: [baseline comparison](evidence/baseline-reassessment-20261021/lifecycle/analysis.json).
> The final [413 runner passes](evidence/baseline-reassessment-20261021/full-unit-run-002/run.json) include one expected failure.

## Request and source facts

The user created `feature/session-refresh-minor` to reduce application changes and system impact.
The selected runtime revision is `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Test-only repairs are committed as `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.

The user requires background-session recovery and will consider broader renewal deferrals after execution.
The [direct request and clarification](evidence/minor-branch-rerun-20261020/user-request.txt) establish this scope.
No individual criterion waiver exists. The [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains version 4.

## Stage boundary and readiness

| Field | Current stage |
| --- | --- |
| Named phase | Test-only repair and paired baseline assessment; earlier browser execution remains historical. |
| Readiness | `READY` for this named phase. |
| Assessor and time | Codex; exact current timestamps in [stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json). |
| Rationale | User authorized test-only repairs and before/after comparison. Exact source and controlled fixtures support the completed phase. |
| Frozen intake | [Original issue](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| MFE comparison | Baseline `f025513f696476a9cc8162681410cbd21e029bcb` → runtime `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Test source | MFE test commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; [executed and committed hashes](evidence/baseline-reassessment-20261021/commit-binding.json). Historical browser tests remain `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. |
| Local modifications | Existing `tsconfig.tsbuildinfo` modification remains outside scope. |
| Blocked actions | Runtime corrections, criterion waivers, release approval, and knowledge publication remain outside this request. |
| Resolution owner | User for scope decisions; unknown application and release owners. |

The [current inputs](evidence/baseline-reassessment-20261021/stage-inputs.json) retain exact identities and authorization.
The [earlier stage baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json) retains the prior runtime-reduction comparison.
This readiness permits evidence collection. It does not establish passing behavior or production approval.

## Proposed change

The branch changes are already implemented by the user.
The current stage repairs two test files and compares uncertain cases with baseline behavior. Application runtime remains unchanged.
The [source assessment](evidence/minor-branch-rerun-20261020/source-impact-review.json) distinguishes removed corrections from retained background behavior.
Three runtime files differ from the initial baseline. Their smaller diff does not establish passing recovery.

## Scope and affected artifacts

| Artifact | Selected version | Stage effect | Evidence and limit | Owner |
| --- | --- | --- | --- | --- |
| `mfe-base` | `6d4c37c839b99d14ea41fd936da1a36cda526b17` | Execute exact selected source. | [Baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json); local fixtures limit deployment claims. | unknown application owner |
| `ratan-test-engine` | `7a504c13a8d51bb52af5cc89bd4af88d1988da94` | Rerun all 22 existing cases without changing assertions. | [Case definitions and BDD navigation](test-execution-report.md#definitions-and-bdd-navigation). | unknown test owner |
| `single-ui-bff` | `85d7cc03eb12710d6facf581987fd4ae24fc9844` | Reuse authorized local controller and session fixtures. | Fixture timeouts and synthetic provider adapters remain explicit. | unknown service owner |

## User impact

Background recovery is the required journey.
Continuous activity, prompt completion, retry, and concurrency failures require separate impact assessments.
A failure remains a failure until an explicit, source-backed scope decision addresses it.
The [execution report](test-execution-report.md) links each result to its exact definition and retained evidence.

## System impact

Direct source inspection covered authentication, Home lifecycle, request, and timeout paths.
Two controlled P2 regressions remain. The inherited delayed-recovery failure has lower incremental release importance.
The [source assessment](evidence/minor-branch-rerun-20261020/source-impact-review.json) records inspected callers and omitted boundaries.
Machine environment values remain outside retained evidence.

## Options and consequences

| Option | Consequence | Required decision |
| --- | --- | --- |
| Require the full existing BDD scope. | Any criterion failure remains an acceptance blocker. | User scope decision after execution. |
| Retain background recovery and defer named broader behavior. | Reduced code may retain specific known adverse behavior. | Explicitly name each deferred criterion and consequence. |
| Change application source. | Could correct failures and expand implementation impact. | Separate application-change authorization after assessment. |

## Proposed acceptance and validation

| Scope | Definition | Required evidence | Current result |
| --- | --- | --- | --- |
| Required background recovery | [Original proposed cases](intake.md#proposed-regression-cases). | Natural 30-minute recovery and delayed delivery evidence. | Immediate-response recovery passed. Delayed refresh recovery failed. [Separate probes](test-execution-report.md#required-background-recovery-and-supplemental-investigations). |
| All existing browser cases | [Linked case mapping](test-execution-report.md#case-mapping). | All 22 outcomes, screenshots, expected predicates, and failures. | Complete: five passed, fourteen failed, one diagnostic failed, and two observations. |
| Supplemental immediate recovery | [User priority](evidence/minor-branch-rerun-20261020/user-request.txt). | Separate natural run without a held relogin response. | Passed actual renewal and protected validation after 1,800,011 milliseconds hidden. Pending-prompt criteria remain unverified. |
| Current unit and compiler checks | [Test repair](evidence/baseline-reassessment-20261021/test-repairs/repair-summary.json). | Executed hashes, committed bytes, commands, and assertion results. | [Full Jest](evidence/baseline-reassessment-20261021/full-unit-run-002/run.json): 116 suites, 413 passes including one expected failure. [Typecheck](evidence/baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json): exit zero. Production build remains `NOT_RUN`. |

## Implementation and release proposal

- Application implementation: preserve runtime bytes; retain the authorized test-only repair commit.
- Scope decision: assess failures before accepting any named deferral.
- Release proposal: none; local execution cannot establish production approval.
- Runtime duration: natural cases require at least 30 minutes of actual hidden time.

## Sources and evidence limits

| Source ID | Locator | Revision or hash | Authority and limit |
| --- | --- | --- | --- |
| SRC-mfe-code-review-20261021 | [Initial review inputs](evidence/code-review-20261021/inputs.json). | MFE `6d4c37c839b99d14ea41fd936da1a36cda526b17`; Workbench review version 1 at `b4f2e22`. | Historical four findings; current reassessment supersedes their disposition. Owner unknown. |
| SRC-session-baseline-reassessment-20261021 | [Current branch review](code-review-minor-20261021.md#review-findings), [binding](evidence/baseline-reassessment-20261021/commit-binding.json). | Baseline and runtime above; test commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. | Two P2 regressions, one P3 scheduling issue, resolved type errors, and inherited delayed recovery. Controlled execution limits remain explicit. |
| SRC-session-minor-stage-20261020 | [Stage baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json). | Exact revisions and hashes above. | Direct user scope and source identities; no acceptance waiver. |
| SRC-session-review-intent-v4 | [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`. | Existing measurable intent; publication review pending. |
| Previous stage record | [Preserved stage version 1](evidence/minor-branch-rerun-20261020/prior-documents/change-review.v1.52f733b.md.snapshot). | SHA-256 `6c8bdbc8ee3ca13696b9544f729e0c449f73b3594193a9bb1aa17558795a3de8`. | Historical broader implementation assessment; does not verify the new branch. |
| SRC-session-minor-impact-20261020 | [source-impact-review.json](evidence/minor-branch-rerun-20261020/source-impact-review.json). | SHA-256 `8cb3d56d536b7179410caf78ee1c4f0f499a138a11d933880780233b870e474a`. | unknown; Exact source comparison; original browser predictions are not execution verdicts. |
| SRC-session-minor-unit-20261020 | [analysis.json](evidence/minor-branch-rerun-20261020/unit/analysis.json). | SHA-256 `333f55e0602d959f452803b92f099319451be6ab3248c906260ed682c06c31c5`. | unknown; 411 passing unit tests and one failure; two type errors relative to initial baseline. |
| SRC-session-minor-browser-20261020 | [browser-manifest.json](evidence/minor-branch-rerun-20261020/browser-manifest.json). | SHA-256 `2cc915c3bc18b89e8a6c477e72be66fe1d180599c98a0dd278417c6d0406d524`. | unknown; All 22 retained outcomes. Supplemental probes remain separate. |
| SRC-session-minor-integrity-20261020 | [integrity-review.json](evidence/minor-branch-rerun-20261020/integrity-review.json). | SHA-256 `c3e98a8f24bec1cf449c0f59427c21b3d9129630e9a88a7d2075e983974aaf0b`. | unknown; Durable hashes and source bindings pass with explicit observation limits. |

## Unknowns and blockers

| Question | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Which broader failures will the user defer? | No automatic acceptance waiver applies. | user | Review exact observed failures and consequences. |
| Is delayed-refresh logout acceptable within required background recovery? | A usable refresh response arrived, but manual recovery remained disabled and logout followed. | user and unknown authentication owner | Review the [failed native probe](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json). Decide a targeted correction or explicit fallback policy. |
| Which deployment settings and provider paths apply? | Local passes cannot establish production behavior. | unknown release owner | Bind representative environment evidence before release decisions. |

## Stage evidence and completion

| Stage | Evidence | Current state | Remaining action |
| --- | --- | --- | --- |
| Source comparison | [Source assessment](evidence/minor-branch-rerun-20261020/source-impact-review.json). | Complete. | Static predictions remain separate from observed failures. |
| Unit and compiler repair | [Current checks](evidence/baseline-reassessment-20261021/full-unit-run-002/run.json), [compiler](evidence/baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json). | Complete; compiler passes, 413 checks include one expected failure. | Runtime recovery remains unfixed; no further test-only action. |
| Browser execution | [Single execution report](test-execution-report.md). | All 22 cases and two separate probes complete. | Review failed predicates and scope consequences. |
| Acceptance assessment | [Linked assessment](evidence/minor-branch-rerun-20261020/acceptance-assessment.json). | Complete recommendations; no approved waivers. | User decisions remain pending. Required background recovery still has a reproduced failure. |

## Requested decision and actual disposition

The user authorized fresh tests on the smaller branch.
The user requires background-session recovery and will consider deferring broader renewal behavior.
No named failure has been accepted. Requirement version 4 remains unchanged.
The recommendation is to defer broader renewal only through explicit criterion decisions.
Correct or explicitly decide the delayed-refresh background outcome before accepting the required recovery scope.
Record any later criterion-specific decision before updating business intent or acceptance claims.

## Saved execution and interruption recovery

Completed cases, screenshots, and source bindings are committed in checkpoint `bd36532`.
The [integrity review](evidence/minor-branch-rerun-20261020/integrity-review.json) reconciles all cases and immutable checkpoints.
The [checkpoint rule](../README.md#save-case-evidence-and-resume-checkpoints) requires immediate durable retention before further work.
The [cleanup record](evidence/minor-branch-rerun-20261020/runtime-cleanup.json) confirms that only owned fixture services stopped.

## Initial branch code review: 21 October 2026

The user requested code review of `repos/ui/mfe-base`.
The [new review](code-review-minor-20261021.md#change-identity) compares `main` with the unchanged selected branch head.
This comparison differs from the earlier runtime reduction comparison. Both exact endpoint identities remain recorded.
The initial review reported four findings. The reassessment below supersedes that disposition.

Focused Jest execution returned 113 passes and one known delayed-refresh failure across six suites.
TypeScript returned two `TS2322` errors from existing callers of the changed event interface.
The [execution records](evidence/code-review-20261021/inputs.json) bind the environment and inspected inputs.
The [final integrity check](evidence/code-review-20261021/integrity.json) records preservation of source, intake, and the existing generated-cache change.

| Phase | Status | Rationale, limits, owner, and next action |
| --- | --- | --- |
| Local branch review and focused validation | `READY`; complete. | Historical initial review completed. Current paired evidence narrows the findings; application owner remains unknown. |
| Acceptance and release | Not assessed by this review. | Existing failures and unresolved waiver decisions remain open. User and unknown release owner retain those decisions. |

No new business clarification or knowledge publication occurred.
The frozen intake remained unchanged during the initial review. The subsequent test-only repair is recorded below.

## Test repair and baseline reassessment: 21 October 2026

The [new user request](evidence/baseline-reassessment-20261021/user-request.txt) authorizes test-only repairs and comparison with original behavior.
The [stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json) bind exact revisions, runtime hashes, and the frozen intake hash.
The [test repair commit](evidence/baseline-reassessment-20261021/commit-binding.json) changes only two test files.
All 283 recorded runtime and configuration files retain their original hashes. Intake and pre-existing build-cache bytes remain preserved.

| Case | Baseline comparison | Final disposition | Evidence |
| --- | --- | --- | --- |
| Active-session cutoff | Baseline survives 23 successful extensions; candidate logs out with valid access. | Introduced P2 regression. | [Lifecycle pair](evidence/baseline-reassessment-20261021/lifecycle/analysis.json). |
| Stale refresh around fresh sign-in | Existing response race gains persistence and replacement suppression; candidate recovery fails where baseline recovers. | Worsened P2 regression; narrow the cause. | [Three paired controls](evidence/baseline-reassessment-20261021/races/analysis.json). |
| Timer one millisecond late | Candidate skips replacement; both retain usable refresh. | Downgrade P2 to P3; user recovery delta unproved. | [Timing pair](evidence/baseline-reassessment-20261021/races/analysis.json). |
| Delayed refresh recovery | Both disable Extend and logout. | Inherited limitation; lower incremental release importance. | [Delayed pair](evidence/baseline-reassessment-20261021/lifecycle/analysis.json). |
| Event-fixture typing | Complete SyntheticEvent fixtures replace incomplete fabricated targets. | F-04 resolved; compiler passes. | [Repair summary](evidence/baseline-reassessment-20261021/test-repairs/repair-summary.json). |

Full Jest passed 116 suites and 413 checks: 412 ordinary checks and one explicit expected failure.
The [expected-failure assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L370-L379) preserves the desired recovery outcome.
It classifies a known defect; it does not correct or verify recovery.
The [initial full runner error](evidence/baseline-reassessment-20261021/full-unit/run.json) remains retained; its signal 11 cause is unconfirmed.
The [worker retry](evidence/baseline-reassessment-20261021/full-unit-run-002/run.json) completed with exit zero.

| Phase | Status | Rationale, owner, and next action |
| --- | --- | --- |
| Test-only repair and paired baseline assessment | `READY`; complete. | Exact endpoints and controlled fixtures support the recorded conclusions. Codex completed tests and assessment. |
| Runtime correction or production release | Outside this request. | Two P2 regressions remain. Unknown application and release owners must address or assess them before unrestricted rollout. |

The [living review](code-review-minor-20261021.md) is now version 3. This stage record is version 5.
Their prior versions remain in Workbench Git `b4f2e22`. Historical browser results retain their original source identities and limits.
The [progress record](evidence/baseline-reassessment-20261021/progress.json) reconciles all completed comparisons and retained failures.

No production failure probability is inferred from these controlled cases.
Existing failures receive lower change-review priority without any criterion waiver.
No business policy changed. Requirement version 4 and publication review remain unchanged.

[Earlier document validation](evidence/baseline-reassessment-20261021/final-validation.json) passed with eight warnings.
Unknown owners, pending business review, unresolved decisions, and pending ASD review remain explicit.

## Gap case clarification and reusable rules: 21 October 2026

The [latest request](evidence/gap-case-steps-20261021/user-request.txt) asks for clear ASD-STE100 case steps and a permanent comparison rule.
The [living case descriptions](code-review-minor-20261021.md#read-the-case-steps) now give setup, numbered actions, required results, and separate old and new observations.
[Case F-03A](code-review-minor-20261021.md#case-f-03a-the-old-response-arrives-before-the-new-sign-in) and [Case F-03B](code-review-minor-20261021.md#case-f-03b-the-old-response-arrives-after-the-new-sign-in) explain the worsened behavior.
[Case F-03C](code-review-minor-20261021.md#case-f-03c-neither-version-gets-the-replacement-opportunity) isolates the unchanged failure.
No case priority, requirement, application source, or retained execution result changes during this clarification.

| Phase | Status | Rationale, owner, and next action |
| --- | --- | --- |
| Evidence-backed case clarification and rule maintenance | `READY`; complete. | Existing paired results support the case steps. Codex updated the descriptions and reusable rules. |
| Runtime correction and release assessment | Outside this clarification. | Two P2 regressions remain. Application and release owners remain unknown. |

The [task comparison rule](../README.md#compare-behavior-for-gap-analysis) applies to future requirement-to-implementation gap analyses.
The [shared procedure](../../.agents/skills/verify-implementation/references/behavior-review.md#compare-old-and-new-behavior) requires exact revisions and equivalent conditions.
Its [case format](../../.agents/skills/verify-implementation/references/behavior-review.md#describe-each-gap-case) requires clear ASD-STE100 setup, numbered actions, and observable results.
An existing failure can have lower incremental release importance. Its unmet requirement remains separate.

[Current checks](evidence/gap-case-steps-20261021/validation.json) cover document contracts, local links, source line bounds, skill metadata, and preserved intake bytes.
No new business execution was necessary. The case descriptions use the retained paired results.
Review version 2 and stage version 4 remain in Workbench Git `6804507458dab19f50cded43da8af4b3b91560e9`.
Business review and ASD writing review remain pending.
