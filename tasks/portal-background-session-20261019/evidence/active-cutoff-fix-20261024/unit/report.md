---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Issue 1 controlled regression proof

**Keep delayed recovery open. Its required assertion still fails. Owner: unknown application owner. Correct it before claiming complete recovery.**
The [normal-test diagnostic](candidate-known-defect-normal-result.json) preserves this failure separately from Jest's expected-failure count.

The [user request](../user-request.txt) authorizes the issue 1 correction and E2E comparison.
This report records supporting unit and controlled integration checks.

## Results

Five corrected assertions fail with original Home bytes and pass with candidate Home bytes.
The [source binding](regression-source-binding.json) records hashes, fixtures, and comparison revision.
Both fixtures use identical candidate assertions and other source files.
Only the baseline fixture receives Home bytes from `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Neither fixture changes the active browser runtime or application checkout.

| Execution | Ordinary passes | Expected failures | Ordinary failures | Exit |
| --- | --- | --- | --- | --- |
| [Original Home with corrected assertions](baseline-home-focused-result.json) | 73 | 1 | 5 | 1 |
| [Candidate focused suite](candidate-focused-result.json) | 78 | 1 | 0 | 0 |
| [Candidate full suite](candidate-full-result.json) | 412 | 1 | 0 | 0 |
| [Known defect with normal `it`](candidate-known-defect-normal-result.json) | 0 | 0 | 1 | 1 |

Jest reports the expected-failure case as passed when its required assertion fails.
Its full-suite total is therefore `413 passed`, including that one unmet recovery assertion.
The [separate diagnostic](candidate-known-defect-normal-execution.json) changes only the isolated wrapper from `it.failing` to `it`.
The diagnostic filters out 30 other integration cases.

## Corrected assertions

| Assertion | Source | Original Home | Candidate Home |
| --- | --- | --- | --- |
| Valid access survives refresh expiry and requests replacement. | [Hook assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L328-L345) | Failed | Passed |
| Repeated access renewals survive initial refresh expiry. | [Hook assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L430-L450) | Failed | Passed |
| Resume with valid access and expired refresh requests replacement without an alert. | [Hook assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionRefresh.test.tsx#L453-L464) | Failed | Passed |
| Active access survives replacement and later manual recovery uses that replacement. | [Integration assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L542-L609) | Failed | Passed |
| Manual Extend before initial refresh expiry preserves access across replacement. | [Integration assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L637-L670) | Failed | Passed |

The original [REVIEW-F01](../../../06-test-cases.md#review-f01) defines active-access continuity without replacement acquisition.
[REVIEW-F01-RECOVERY](../../../06-test-cases.md#review-f01-recovery) adds replacement acquisition and later manual recovery.
[REVIEW-F01-MANUAL](../../../06-test-cases.md#review-f01-manual) defines manual renewal immediately before initial refresh expiry.
These controlled cases do not replace browser E2E evidence.

The unchanged [delayed-response case](../../../06-test-cases.md#review-delayed-hide) remains outside the issue 1 correction.
Its [required assertion](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L370-L378) still fails under normal `it` execution.

## Checks and limits

The [final checks](final-checks.json) confirm all tested candidate bytes still match the application checkout.
The preexisting compiler-cache hash remains unchanged.
Application `git diff --check` exits zero.
The [TypeScript source comparison](typescript-source-comparison.json) passes for both fixtures with zero diagnostics.
Both commands disable file emission, declaration-only emission, and incremental compilation.
The [initial setup conflict](typescript-comparison.json) remains retained: inherited declaration-only emission conflicts with `--noEmit`.
The later comparison overrides that option equally for both fixtures.

The [full log](candidate-full.log) records 116 passing suites and a Jest open-handle warning.
The runner eventually exits zero without `--forceExit`.
No action terminated the browser runtime.

The tests use jsdom, fake timers, controlled JWT payloads, and Axios adapter responses.
They verify the named predicates in that controlled environment.
They do not prove production lifetimes, provider behavior, token revocation, or browser timing.
The [machine summary](regression-summary.json) preserves the five result transitions and counting rules.

## Reproduction

The [regression runner](run-regression-proof.py) copies source into separate ignored fixtures before execution.
The [known-defect runner](run-known-defect-proof.py) exposes the inherited assertion in another fixture.
Those runners refuse to overwrite existing fixtures.
The [TypeScript runner](run-typescript-proof.py) compares both copied source fixtures without emission.
Retained execution records contain exact commands and timestamps.

- [Original Home focused execution](baseline-home-focused-execution.json).
- [Candidate focused execution](candidate-focused-execution.json).
- [Candidate full execution](candidate-full-execution.json).
- [Known-defect execution](candidate-known-defect-normal-execution.json).

Automated checks verify counts, byte identity, preserved cache, TypeScript compilation, links, and whitespace errors.
The ASD writing review remains pending.
