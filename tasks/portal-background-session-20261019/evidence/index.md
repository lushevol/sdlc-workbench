---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal defect: key evidence

> **Critical conclusions: Action required**
>
> **Two P2 regressions remain after baseline comparison.**
> Action: address [active-session cutoff](../code-review-minor-20261021.md#f-01-p2-preserve-active-access-across-the-refresh-deadline) and [stale-credential reuse](../code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: valid active access can end; recovery can clear a fresh session.
> Owner: unknown application owner. Evidence: [lifecycle pairs](baseline-reassessment-20261021/lifecycle/analysis.json) and [race pairs](baseline-reassessment-20261021/races/analysis.json).
> These controlled checks do not measure production failure frequency.
>
> **Delayed recovery is inherited and remains unfixed.**
> Action: retain its limitation when deciding required background behavior.
> Consequence: late credentials cannot enable Extend. The [passing unit run](baseline-reassessment-20261021/full-unit-run-002/run.json) includes one expected failure.
> Owner: unknown application owner; user for acceptance decisions. Evidence: [paired delayed outcomes](baseline-reassessment-20261021/lifecycle/analysis.json).

## Necessary: start here

- [Current branch review, version 3](../code-review-minor-20261021.md#review-findings): two P2 regressions, one P3 scheduling issue, and resolved event-fixture errors.
- [Current stage, version 5](../change-review.md#gap-case-clarification-and-reusable-rules-21-october-2026): clear case steps and the reusable comparison rule.
- [Case steps](../code-review-minor-20261021.md#read-the-case-steps): setup, numbered actions, separate old and new observations, and six controlled conditions.
- [Current clarification inputs](gap-case-steps-20261021/inputs.json): exact versions, preserved baseline evidence, and requested rule changes.
- [Current document and rule checks](gap-case-steps-20261021/validation.json): links, line bounds, authoring contracts, and skill metadata.
- [Current stage inputs](baseline-reassessment-20261021/stage-inputs.json): authorization, exact revisions, preserved hashes, and previous review identity.
- [Lifecycle comparison](baseline-reassessment-20261021/lifecycle/analysis.json): introduced active cutoff; unchanged delayed-refresh failure.
- [Race comparison](baseline-reassessment-20261021/races/analysis.json): four paired conditions; existing response race worsens through credential persistence and reuse.
- [Test-only repair](baseline-reassessment-20261021/test-repairs/repair-summary.json): complete event fixtures and explicit known-defect assertions.
- [Full unit run](baseline-reassessment-20261021/full-unit-run-002/run.json): 116 suites, 413 checks, including one expected failure.
- [Final compiler run](baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json): exit zero; earlier type errors are resolved.
- [Commit binding](baseline-reassessment-20261021/commit-binding.json): MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; two test files changed; runtime and frozen intake preserved.
- [Earlier document checks](baseline-reassessment-20261021/final-validation.json): authoring lint and local references pass; ASD review remains pending.
- [Progress reconciliation](baseline-reassessment-20261021/progress.json): completed cases, initial failures, runner error, and final checks.
- [Historical initial review checks](code-review-20261021/inputs.json): initial Jest failure and two type errors; current repair supersedes their status.
- [Historical browser report](../test-execution-report.md): 22 minor-branch outcomes, separate recovery probes, and linked criterion definitions.
- [Historical rerun manifest](minor-branch-rerun-20261020/browser-manifest.json): retained screenshots and checkpoint commit `bd36532`.
- [Historical integrity review](minor-branch-rerun-20261020/integrity-review.json): original source identities and observation limits.
- [BDD and case definitions](../test-execution-report.md#definitions-and-bdd-navigation): exact linked criteria, test scopes, and historical source revisions.
- [Report consolidation record](report-consolidation-20261020.json): removed report, hashes, recovery locators, and repaired references.
- [Frozen issue intake](../intake.md): original issue understanding; current conclusions appear in the stage record.
- [Earlier behavior coverage](../coverage.md): previous implementation checks and their source identities.
- [Earlier task manifest](manifest.json): prior cleanup and deletion history. This reassessment deletes no evidence.

The test repair does not update historical browser outcomes or waive failed behavior criteria.
The first full unit attempt ended with a [runner error](baseline-reassessment-20261021/full-unit/run.json); its cause remains unconfirmed.
Previous review version 1 and stage version 3 remain in Workbench Git `b4f2e22`.

## Earlier correction stage

- [User clarification and authorization](correction-20261020/user-request.txt): continuous activity must retain session renewal.
- MFE baseline: `2af6b83`, including the user's pending-refresh correction.
- Corrections: MFE `4da985a`. Browser cases: test-engine `62f1685`. Full commits appear in the source inventory.

| Evidence ID | Claim or question | Locator | Revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| C-014 | Which corrected bytes were checked? | [Source inventory](correction-20261020/source-inventory.json) | Exact requirement, MFE, BFF, and test-engine revisions | Per-file hashes in inventory | Static identity and source binding. No deployment claim. |
| C-015 | Did the corrections pass regressions? | [Final integrated result](correction-20261020/integrated/run-002/verification.json), [commit binding](correction-20261020/integrated/run-002/commit-binding.json) | MFE `4da985a`; final Run 002 | Result and source hashes in binding | 167 tests passed in 13 suites. Controlled transport, credentials, and JSDOM; no live E2E. |
| C-016 | Did the new tests detect the baseline? | [Baseline failures](correction-20261020/manual-renewal/baseline-results.json), [active-renewal evidence](correction-20261020/active-renewal/verification.json) | MFE baseline `2af6b83`; exact run inputs retained | Per-run hashes and source inputs | All 12 new manual regressions failed baseline. Four controlled hours include 240 successful extensions. |
| C-017 | Which E2E cases and gaps exist? | [Mapping](correction-20261020/e2e/coverage.json), [checks](correction-20261020/e2e/validation.json), [binding](correction-20261020/e2e/commit-binding.json) | Test-engine `62f1685` | Four source hashes and static-check record hash in binding | Seven cases; static checks passed. Dry-run failed setup. Actual E2E remains NOT_RUN. |
| C-018 | Are the final documents consistent? | [Final checks](correction-20261020/final-checks.json) | Selected final document hashes | Input hashes in check record | Document checks remain separate from business execution and pending human review. |

## Important: historical defect evidence

| Evidence ID | Claim or question | Locator | Revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| C-003 | What happened locally? | [Run 001 events](portal/run-001/browser/browser-events-001.json), [BFF log](portal/run-001/bff/local-bff-runtime.stdout.log) | 19 October 2026 UTC; exact revisions in intake | Manifest | Freeze, late issuance, missing-refresh logout, then HTTP 401 and authentication clear. |
| C-004 | Is there another observation? | [Run 002 events](portal/run-002/browser/browser-events-001.json), [return text](portal/run-002/browser/return.ax.full.txt) | Separate local run; 19 October 2026 | Manifest | Another background run. No matching foreground control. |
| C-005 | Can the setup and observer be checked? | [Setup retention map](portal/retention-map.json), [instrumentation manifest](portal/setup/instrumented-mfe/instrumentation-manifest.json), [observer review](portal/run-001/reviews/observer-review.json) | Exact retained source and setup bytes | Manifest | Local substitutions and observer effects remain explicit. Historical paths resolve through the relocation map. |
| C-006 | Which code explains the failure? | [Source snapshots](source-snapshots), [source receipt](source-inspection.json) | MFE `f025513f`; BFF `85d7cc03`; full commits in intake | Manifest and raw source manifest | Exact source supports the local mechanism. It does not establish PROD deployment. |
| C-007 | What did earlier tests cover? | [Assertion receipt](source-inspection.json), [test-engine inspection](browser-setup/test-engine-inspection.json) | Historical assertion revisions recorded in each receipt | Manifest | Earlier inspection found coverage gaps. No business test ran during that review. |
| C-013 | How do credential paths differ? | [Expired-token fixture result](portal/run-001/expired-fixture/expired-result.json) | Separate controlled fixture on port 8089 | Manifest | Access-based refresh fails; valid-refresh relogin succeeds. No natural browser recovery assertion. |

[Verification detail](../verification.md) supplies assertion boundaries and execution limits.
Stable source IDs, revisions, and hashes remain in the [raw source manifest](../../../evidence/knowledge/manifest.yaml).
[Existing session intent](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md) remains candidate knowledge with pending publication review.

## Important: authentication investigation

- [Runtime baseline](authentication/ARCH-authentication-runtime-baseline.md): earlier source and assertion investigation, with its original evidence limits.
- [Verification findings](../../../evidence/knowledge/findings/GF-session-renewal-verification-gates.md): unresolved execution and policy boundaries.
- [Migration map](../../../evidence/knowledge/migration-20261020/cleanup.json): current locators, retained hashes, removed paths, and recovery revisions.

The map resolves historical source paths inside unchanged evidence.
Task captures remain evidence. They do not establish approved domain rules or corrected behavior.

## Important: retained screenshots

- [Edge browser smoke](browser-final/edge/returned.png): synthetic interaction and two-second visibility check, after returning to the fixture.
- [Result](browser-final/edge/result.json), [snapshot](browser-final/edge/snapshot.yaml), [trace](browser-final/edge/trace.zip), and [hashes](browser-final/edge/manifest.json) preserve its execution context.
- [Portal Sign In](portal/run-001/reviews/sign-in-context.jpg): actual local portal context. Capture time and phase remain unresolved.

Neither image establishes portal unit-test execution. No attributed screenshot proves the thirty-minute returned-page result.

## Important: provenance and earlier checks

- [Historical relocation map](organization-20261020/relocation-map.json), [prior source manifest](organization-20261020/manifest-before.yaml), and [authorization](organization-20261020/request.txt): preserved unchanged.
- [Earlier document checks](defect-document-checks-20261020.json): checks before the domain-only knowledge migration.
- [Earlier task manifest](manifest.json): Necessary and Important file inventory before the domain-only knowledge migration.

## Unimportant: removed from the task

Removed material includes duplicate browser trials, unrelated harness logs, superseded reports, and repeated authoring or organization checks.
The earlier task cleanup kept 74 of 252 files and removed 178 files. It preserved registered snapshots and audit history.
The historical relocation map describes its original migration. Use the current manifest to resolve later deletions through Git.
That cleanup changed no business policy, portal runtime, or corrected behavior.
