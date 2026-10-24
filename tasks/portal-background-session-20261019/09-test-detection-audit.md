---
artifact_kind: traceability-record
id: TRACE-session-test-detection-20261024
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-coverage-detection-request-20261024
  - SRC-session-coverage-detection-inputs-20261024
  - SRC-session-cutoff-audit-20261024
  - SRC-session-stale-audit-20261024
  - SRC-session-delayed-audit-20261024
related_ids:
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
  - ASSESS-session-refresh-release-20261022
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

# Test coverage and earlier detection of the three session issues

> **All three issues were known before the 22 October release-confidence assessment. They remain unresolved.**
> Action: correct requirement assertions, add the missing session-race coverage, and verify the runtime corrections.
> Consequence: passing Jest totals cannot establish correct behavior. Positive PROD handoff remains blocked.
> Owner: unknown application and test owners.
> Evidence: [cutoff audit](evidence/coverage-detection-audit-20261024/active-cutoff-audit.json), [stale-session audit](evidence/coverage-detection-audit-20261024/stale-session-audit.json), and [delayed-recovery audit](evidence/coverage-detection-audit-20261024/delayed-recovery-audit.json).

## Scope and identities

The [high-priority request](evidence/coverage-detection-audit-20261024/user-request.txt) asks about unit tests, test cases, E2E execution, and earlier discovery.
"In advance" means before the release assessment, with earlier review and execution dates identified below.
The records establish detection before that assessment. They do not establish detection before the implementation commit.
The current canonical catalog was synchronized after the original executions.
Its present coverage does not prove that these Gherkin definitions existed before implementation.

| Identity | Selected scope |
| --- | --- |
| Capability | `single-ui-authentication`. |
| Requirement | [Candidate version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), pending publication review. |
| Application | `mfe-base`; `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. |
| Runtime used in original browser evidence | `6d4c37c839b99d14ea41fd936da1a36cda526b17`; relevant runtime bytes match the selected candidate. |
| Baseline comparison | `f025513f696476a9cc8162681410cbd21e029bcb`. It is not an established PROD baseline. |
| Test engine | Original browser assertions: `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. Current checkout: `37b7365aca2203021e7014112b9d15cf00f7455b`. |
| Services and contracts | Local `single-ui-bff-api`; `single-ui-sso-token-family` and shared HTTP boundaries. Actual PROD composition remains unknown. |
| Canonical catalog | [Case definitions](06-test-cases.md); exact SHA-256 in [audit inputs](evidence/coverage-detection-audit-20261024/inputs.json). |
| Audit operations | Existing source, assertions, results, and Git history inspected. No new business execution or application edit. |

The [inputs](evidence/coverage-detection-audit-20261024/inputs.json) preserve frozen-intake, requirement, worktree, and source identities.
Earlier passing results for broader candidate `4da985a9fa302d7f1ecc04a81b2924b49410ce6a` do not close these reduced-candidate failures.

## Requirement and criterion declarations

| Requirement or expectation | Criterion | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| [Active-session renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) | [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) | Continued eligible activity crosses initial refresh expiry with zero elapsed-time-only fresh SSO prompts. | Candidate version 4. | pending |
| Session isolation | [Review inference](07-code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse) | Recovery uses the current session's credentials and does not clear a fresh session through stale work. | Exact case catalog and reviewed candidate below. | No separate approved late-response criterion. |
| Required background recovery | [Delayed scheduled case](06-test-cases.md#review-delayed-scheduled), [delayed hide case](06-test-cases.md#review-delayed-hide) | Usable late refresh delivery permits manual renewal. | Existing task scope and case definitions. | No fallback acceptance recorded. |

The supplied release intent granted no named criterion waiver.
An inferred isolation expectation remains separate from published business policy.

## Relationship evidence

| From | Relationship | To | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) | Intended check | [REVIEW-F01](06-test-cases.md#review-f01) | [Case assertions and comparison](06-test-cases.md#L1381-L1396). | confirmed definition and inspection | Exact four-hour fixture is controlled integration. |
| [REVIEW-F01](06-test-cases.md#review-f01) | Related browser check | [E2E-06](06-test-cases.md#e2e-06) | [Inspected browser driver](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L601-L639). | confirmed assertion mapping | Shortened timing; later predicates were not reached. |
| Session isolation | Before-login delivery | [REVIEW-F03A](06-test-cases.md#review-f03a) | [Race assertions](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L78-L148). | confirmed inspection | Adapter models session rejection. |
| Session isolation | After-login delivery | [REVIEW-F03B](06-test-cases.md#review-f03b) | [Race assertions](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L78-L148). | confirmed inspection | Same controlled integration boundary. |
| [REVIEW-F03-CONTROL](06-test-cases.md#review-f03-control) | Limits baseline claim | Both revisions fail when replacement is suppressed. | [Control actual values](evidence/code-review-refresh-20261021/races-baseline-f03-control/actual.json). | observed controlled execution | Baseline is not immune to all stale responses. |
| [Delayed hide case](06-test-cases.md#review-delayed-hide) | Browser probe | [PROBE-DELAYED-REFRESH](06-test-cases.md#probe-delayed-refresh) | [Probe result](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json). | confirmed executed mapping | Supplemental probe lies outside the original 22-case suite. |

## Inspected implementation and assertions

"UT/Jest suite" includes isolated hook tests and component integration tests. Neither is native browser E2E.
Current test locations below use MFE commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.

| Issue | UT/Jest assertions | Canonical test cases | Coverage judgment |
| --- | --- | --- | --- |
| [Active cutoff](10-release-confidence.md#rc-01-active-access-can-end) | [Hook assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L328-L342), [repeated-renewal assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L428-L447), and [lifecycle assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L542-L569). | [REVIEW-F01](06-test-cases.md#review-f01) and [E2E-06](06-test-cases.md#e2e-06). | Covered as characterization. The unit assertions expect Timeout or logout despite valid access. They contradict the required continuity. |
| [Stale-session recovery](10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session) | [Acquisition cancellation](../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L205-L233) and [completed logout/sign-in](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L654-L691). | [REVIEW-F03A](06-test-cases.md#review-f03a), [REVIEW-F03B](06-test-cases.md#review-f03b), and [control](06-test-cases.md#review-f03-control). | Ordinary tests omit the exact cross-session late-response sequence. Later controlled diagnostics reproduce both delivery orders. |
| [Delayed recovery](10-release-confidence.md#rc-03-required-delayed-recovery-remains-unmet) | [Known failure and characterization](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L325-L378). | [Scheduled delivery](06-test-cases.md#review-delayed-scheduled), [hide delivery](06-test-cases.md#review-delayed-hide), and [browser probe](06-test-cases.md#probe-delayed-refresh). | The intended recovery assertion exists. It originally failed. Current `it.failing` deliberately treats that expected failure as a runner pass. |

The stale-session cancellation test starts a second acquisition before delivering the old response.
The defect can reuse stale refresh state before replacement acquisition starts.
The completed logout/sign-in test has no pending old response crossing the session boundary.
Therefore, neither related test covers the complete reported race.

## Retained execution and verification

| Issue | Execution and exact tested revision | Actual result | Verification claim and limit |
| --- | --- | --- | --- |
| Active cutoff | [Browser E2E-06](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json); MFE `6d4c37c839b99d14ea41fd936da1a36cda526b17`; test engine `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. | `FAILED`: authenticated Home disappeared. Refresh expired while latest access remained valid. | Related browser failure. Replacement-refresh and final protected-request assertions were not reached. Exact boundary attribution comes from the paired diagnostic. |
| Active cutoff | [Paired baseline](evidence/code-review-refresh-20261021/lifecycle-baseline-active_cutoff/actual.json), [candidate](evidence/code-review-refresh-20261021/lifecycle-candidate-active_cutoff/actual.json); MFE baseline and selected candidate. | Baseline: zero logout and retained access. Candidate: one logout and cleared access. | Controlled fake-clock Home/Timeout integration confirms the regression. Diagnostic runner passes because it expects these different actual values. |
| Stale-session recovery | [Before-login candidate](evidence/code-review-refresh-20261021/races-candidate-f03-before/actual.json), [after-login candidate](evidence/code-review-refresh-20261021/races-candidate-f03-after/actual.json); selected MFE candidate. | Both use session A's refresh for session B. Modeled rejection clears session B. | Exact controlled service/reducer/interceptor reproduction. No exact browser E2E execution was found. |
| Stale-session browser boundary | Related [E2E-17](06-test-cases.md#e2e-17), [E2E-18](06-test-cases.md#e2e-18); [22-case results](evidence/minor-branch-rerun-20261020/browser-manifest.json). | Both fail before late-response restoration assertions. | Neither supplies fresh-login plus old-refresh reuse coverage. Their incomplete assertions cannot close the gap. |
| Delayed recovery | [Supplemental Edge result](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json); MFE `6d4c37c839b99d14ea41fd936da1a36cda526b17`. | `FAILED`: usable refresh arrives, Extend remains disabled, relogin count is zero, and logout follows. | Exact delayed-delivery browser probe. Local BFF and identity fixtures, controlled response withholding, and real wall time apply. Natural freezing is not proven. |
| Delayed recovery | [Paired baseline](evidence/code-review-refresh-20261021/lifecycle-baseline-delayed_recovery/actual.json), [candidate](evidence/code-review-refresh-20261021/lifecycle-candidate-delayed_recovery/actual.json). | Both revisions retain disabled Extend and eventually log out. | Inherited failure. The current candidate does not correct it. |
| Full current Jest suite | [Retained result](evidence/code-review-refresh-20261021/suite-suite-suite/result.json); selected MFE candidate. | 116 suites; 413 runner passes. This includes the known delayed-recovery expected failure. | The total includes adverse characterization and expected failure. It is not 413 passing requirement checks. |

The [prior test-level answer](evidence/blocker-e2e-origin-20261023/answer.md) already separates integration diagnostics from exact browser reproduction.
This audit adds assertion and detection chronology. It does not upgrade the earlier execution level.

### Were the issues found in advance?

All times below use Singapore time. Result timestamps and Git retention dates serve different purposes.
They establish the inspected sequence. They do not authenticate the first human discovery.

| Date and time | Evidence available then | Meaning |
| --- | --- | --- |
| 20 October, 01:55 | Minor implementation commit `f21654a6602195fcdd74dd3ec79a0d36a502d8c5` includes the active-cutoff expectations and delayed-recovery assertion. | Tests existed with the change. No inspected precommit result proves these defects were blocked before introduction. |
| 20 October, 22:15–22:16 | Original delayed-recovery Jest assertion fails. [Execution details](evidence/coverage-detection-audit-20261024/delayed-recovery-audit.json). | Required delayed recovery was already exposed as a failure. |
| 20 October, 22:25–22:26 | [Delayed browser probe](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json) fails. | The late-delivery failure is visible in native Edge. |
| 20 October, 22:27 | [E2E-06 result](evidence/minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json) fails. | Related active-cutoff evidence exists before the next day's source classification. |
| 21 October, 07:23–07:29 | [Source inspection](evidence/code-review-20261021/inspection.json) records active cutoff and stale-session findings. Commit `b4f2e22f1f3f22046b3a5828db885e411186a0ec` retains the review. | Both defects were identified before release-confidence work. The stale-session finding initially relies on source inference. |
| 21 October, 08:20–08:22 | [Lifecycle comparison](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) and [race execution audit](evidence/coverage-detection-audit-20261024/stale-session-audit.json) confirm old/new outcomes. | Exact controlled execution confirms active cutoff, stale-session failure, and inherited delayed recovery. |
| 21 October, 08:32 | MFE test-only commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; [binding](evidence/baseline-reassessment-20261021/commit-binding.json). | The delayed-recovery assertion becomes `it.failing`. Runtime remains unchanged. |
| 21 October, 12:19 | Canonical catalog synchronized in Workbench commit `4e420912`; [history check](evidence/coverage-detection-audit-20261024/validation.json). | Current Gherkin definitions follow the original executions. They document intended assertions and observed failures. |
| 22 October, 23:15 | [Release-assessment inputs](evidence/release-confidence-20261022/assessment-inputs.json). | The assessment reuses known unresolved failures. It does not discover all three for the first time. |

Thus, earlier testing and review found all three before the release assessment.
The evidence does not support a claim that complete protective coverage existed before implementation.
No inspected CI or deployment record establishes an automatic blocking decision for these results.
The [audit checks](evidence/coverage-detection-audit-20261024/validation.json) verify links, source hashes, retained predicates, and selected history.
They do not execute the application. Owner and review warnings remain open.

## Coverage gaps

| Missing or incorrect protection | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Active-cutoff unit expectations contradict intended continuity. | [Inspected SR11 assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L328-L342). | A defect can produce a green test. | unknown application and test owners | Correct the runtime and use continuity assertions. Preserve historical adverse evidence. |
| Complete cross-session regression is absent from ordinary UT. | [Stale-session audit](evidence/coverage-detection-audit-20261024/stale-session-audit.json). | Cancellation tests miss stale credential reuse across fresh sign-in. | unknown test owner | Add before-login and after-login late delivery regressions from the canonical definitions. |
| Exact stale-session browser case is absent. | [Browser scope audit](evidence/coverage-detection-audit-20261024/stale-session-audit.json). | Browser integration remains unverified for that complete race. | unknown test owner | Implement and execute both fresh-login delivery orders with explicit credential and authentication assertions. |
| Delayed recovery remains an expected failure. | [Known-defect assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L370-L377). | A green runner summary hides unresolved conformance unless the marker is reviewed. | unknown application and test owners | Correct recovery, prove intended assertions pass, then remove `it.failing`. |
| Supplemental probe is outside the original 22-case suite. | [Probe binding](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json). | Running only that suite can omit the exact late-delivery condition. | unknown test owner | Include the canonical delayed-delivery case in the maintained regression selection. |

## Facts, inferences, and unresolved questions

Facts: all three issues have retained evidence before the release assessment.
Facts: canonical cases exist for each issue. Coverage exists at different levels and with different assertion meanings.
Facts: current runtime remains unfixed. No new business tests ran for this audit.
Inference: reliance on green Jest totals would conceal these known limitations.
Unknown: earliest discovery outside inspected history, current PROD occurrence, CI blocking behavior, and actual deployment decisions.
The business rules, candidate requirement, frozen intake, and historical results remain unchanged.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Current failure assessment](10-release-confidence.md#findings). | Positive PROD recommendation remains blocked despite earlier detection. | unknown application and release owners | Complete corrections and retain matching passing evidence. |
| [Three audit records](evidence/coverage-detection-audit-20261024/validation.json). | Assertion presence must not be counted as protective coverage or passing behavior. | unknown test owner | Report the assertion direction, test level, execution result, and known failures together. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-coverage-detection-request-20261024 | [Exact input](evidence/coverage-detection-audit-20261024/user-request.txt). | User message, 24 October 2026. | [Inputs](evidence/coverage-detection-audit-20261024/inputs.json). | User; high-priority audit request, without a policy change. |
| SRC-session-coverage-detection-inputs-20261024 | [Audit inputs](evidence/coverage-detection-audit-20261024/inputs.json). | Selected commits above. | [Validation](evidence/coverage-detection-audit-20261024/validation.json). | Codex capture; source identity and preservation only. |
| SRC-session-cutoff-audit-20261024 | [Cutoff audit](evidence/coverage-detection-audit-20261024/active-cutoff-audit.json). | MFE candidate, baseline, test and history identities within the record. | Individual source SHA-256 values in the record. | Codex inspection; known assertion and shortened-browser limits. |
| SRC-session-stale-audit-20261024 | [Stale-session audit](evidence/coverage-detection-audit-20261024/stale-session-audit.json). | MFE candidate, baseline, test and history identities within the record. | Individual source SHA-256 values in the record. | Codex inspection; no exact browser reproduction. |
| SRC-session-delayed-audit-20261024 | [Delayed-recovery audit](evidence/coverage-detection-audit-20261024/delayed-recovery-audit.json). | Original runtime, current test revision, and probe identities within the record. | Individual source SHA-256 values in the record. | Codex inspection; controlled delivery and local identity fixtures. |
