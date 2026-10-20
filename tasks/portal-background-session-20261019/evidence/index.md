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
> **GO-LIVE HOLD: resolve build errors and acceptance gaps.**
> Action: review the [build findings](../test-execution-report.md#unit-execution-and-build-readiness), then assign recovery and workspace acceptance decisions.
> Consequence: local browser passes cannot close production release.
> Owner: unknown application, business, and release owners. Evidence: [current conclusions](../test-execution-report.md#findings).

## Necessary: start here

- [Single E2E execution report](../test-execution-report.md): all 22 current cases, earlier run provenance, failures, and release blockers.
- [Report consolidation record](report-consolidation-20261020.json): removed report, hashes, Git recovery locators, and repaired references.
- [Issue intake](../intake.md): current understanding, user answers, open decisions, and proposed acceptance criteria.
- [Behavior and E2E coverage](../coverage.md): committed corrections, passing controlled regressions, executable browser cases, and remaining gaps.
- This index: useful evidence only. [The earlier task manifest](manifest.json) records the previous cleanup and deletion history.

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
