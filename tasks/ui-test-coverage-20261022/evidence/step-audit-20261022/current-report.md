---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Current local UI audit

> **Critical conclusions: Review required before business acceptance**
>
> **The local audit records 420 passes, 72 failures, two active blockers, and 27 user exclusions.**
> Action: Review failed predicates and their fixture limits. Consequence: Passing local predicates cannot establish deployed business acceptance.
> Owner: unknown business test owner. Evidence: The [case gallery](../audit-run-20261022/report-002/index.html) and [case ledger](../audit-run-20261022/report-002/case-results.csv).
>
> **Two active cases cannot complete their remaining steps.**
> Action: Resolve the [authorization binding](#remaining-active-prerequisites) and [native CSV import](#remaining-active-prerequisites).
> Consequence: Their later assertions remain unexecuted. Owner: unknown authorization owner; audit execution owner for native import.
> Evidence: The retained blockers below.

## Scope and results

The user selected the isolated local application.
The [canonical catalog](../../test-cases.md#coverage-navigation) contains 521 cases and 4,873 Gherkin steps.
Its SHA-256 is `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4`.
The [frozen preflight](../audit-run-20261022/inventory/summary.json) binds this catalog and its original case inventory.
All 494 active cases have retained application attempts.
The user excluded 27 cases with unavailable tenant, intent/context, or native OpenFin prerequisites.
The [scope decision](user-scope-exclusions.json) identifies every exclusion and preserves the answer `skip them`.

| Latest local result | Cases |
| --- | ---: |
| PASS | 420 |
| FAIL | 72 |
| BLOCKED_NOT_EXECUTED | 2 |
| SKIPPED_BY_USER | 27 |
| Total canonical cases | 521 |

These statuses describe inspected local predicates.
Failures include proposed policy differences and contradictory definitions.
They do not all establish approved business defects.
Execution, screenshot completeness, definition quality, and business acceptance remain separate measures.
The frozen definition review remains historical.

The final BFF suite records 72 passes and 25 failures across 97 cases.
The [final BFF triage](bff-final-triage.json) links each failure to assertions, requests, persisted results, and screenshots.
The [frontend review](source-consumption-review.md#frontend-failure-triage) explains material interpretation limits.
The [authentication and knowledge reconciliation](auth-and-knowledge-final-validation.json) checks the final selected runs independently.

## Findings that require investigation

| Observed behavior | Evidence and consequence | Owner and next action |
| --- | --- | --- |
| Foreign audit requests returned protected fixture rows with HTTP 200. | [BFF-ADM-063](../../test-cases.md#bff-adm-063), [BFF-ADM-068](../../test-cases.md#bff-adm-068), and [BFF-ADM-073](../../test-cases.md#bff-adm-073); [retained observations](bff-final-triage.json). Declared stale READ overlays expose the trigger rows. Actual audit authorization remains under test. | Owner: unknown BFF owner. Investigate audit authorization before acceptance. |
| Repeated verification deactivated records that another checker had activated. | [BFF-ADM-085](../../test-cases.md#bff-adm-085), [BFF-ADM-088](../../test-cases.md#bff-adm-088), and [BFF-ADM-091](../../test-cases.md#bff-adm-091); [persisted observations](bff-final-triage.json). The second request returned HTTP 200. | Owner: unknown BFF owner. Review checker state validation and concurrency policy. |
| Stale updates overwrote newer values. Stale verification accepted changed records. | [BFF-ADM-083](../../test-cases.md#bff-adm-083), [BFF-ADM-084](../../test-cases.md#bff-adm-084), [BFF-ADM-086](../../test-cases.md#bff-adm-086), [BFF-ADM-087](../../test-cases.md#bff-adm-087), [BFF-ADM-089](../../test-cases.md#bff-adm-089), and [BFF-ADM-090](../../test-cases.md#bff-adm-090); [independent readbacks](bff-final-triage.json). | Owner: unknown BFF owner. Define the required stale-write and stale-verification rules. |
| Every tested browser rejected the exact title comparison because `Cashflow ` contains a trailing space. | [Browser comparison](browser-compatibility/results.json) and [review](browser-compatibility/review.md). Chromium, Edge, Firefox, and WebKit reached the same failed assertion. | Owner: unknown UI owner. Resolve the title rule before changing the exact assertion. |

The [BFF binding review](bff-binding-review.md) identifies entity conflicts in four definitions.
Those conflicts cannot establish their intended Tile behavior.
Undefined agreed messages remain unresolved acceptance limits.
No business application source was changed during this audit.

## Why the earlier report showed FAIL and PASS

The [earlier AUTH-084 page](../audit-run-20261022/report-001/cases/AUTH-084.html) displayed two attempts in chronological order.
Its [ledger](../audit-run-20261022/report-001/case-results.json) records run-005 as FAIL and later run-006 as PASS.
The upper section therefore showed the earlier failure.
The lower section showed the later passing attempt.

The [new gallery](../audit-run-20261022/report-002/index.html) shows the latest result first.
Earlier attempts remain in labelled, collapsed history.
A collapsed historical definition review explains any separate quality failure.
Definition quality does not change the actual execution outcome.
The [generator](../../../../e2e/scripts/summarize-audit.py) preserves earlier failures and source identities.
The [report regressions](validation/report-regressions.log) check these distinctions.
The original report remains unchanged.

## Screenshots for every executed step

The [audit fixture](../../../../e2e/support/audit-fixture.ts) captures a fresh frame after each executed canonical step.
Each frame retains its step number, exact text, source line, timestamp, path, and SHA-256.
Each case page displays its complete canonical timeline beside its frames.
A failed step keeps the actual failure screenshot.
Later steps remain `NOT_EXECUTED` and claim no execution screenshots.
Excluded cases claim no screenshots.

Screenshots establish visible state.
Separate retained observations support request, storage, timing, and persistence claims.
The [report validator](../../../../e2e/scripts/validate-audit-report.py) checks catalog bindings, hashes, PNG files, statuses, and HTML history.
Complete screenshot evidence does not imply complete approved business acceptance.
The [sample visual review](screenshot-qa.json) records nine reviewed frames with exact hashes.
The [browser review](browser-compatibility/review.md) retains additional browser samples.
The [SSO cancellation review](canonical-binding-review/review.md) retains three reviewed provider and return frames.
These samples do not establish visual review of every retained frame.

Latest attempts retain screenshots for all 4,478 executed canonical steps.
All steps executed in 432 cases.
Sixty failed cases and two blocked cases stopped before their final steps.
The 27 excluded cases claim no execution.
Across retained actual application attempts, the gallery contains 14,351 named frames.

## Remaining active prerequisites

| Case | Completed work | Blocked work and next action |
| --- | --- | --- |
| [KNOW-014](../../test-cases.md#know-014) | Steps 1–8 ran against the current local catalog and captured screenshots. | The approved open-authorization operation, protected fields, and denial state remain undefined. Owner: unknown. Define these bindings before steps 9–10. See [blocker evidence](../audit-run-20261022/application/run-080/). |
| [UX-043](../../test-cases.md#ux-043) | Steps 1–2 exported all four formula-shaped labels and captured screenshots. | Numbers recognized the exact CSV but did not complete native import. Owner: audit execution owner. Restore import controls before steps 3–5. See [native investigation](CSVviewer/native-investigation.md), [API limits](CSVviewer/native-api-review.json), and [latest blocker](../audit-run-20261022/application/run-076/cases/ux-043-captured-csv-retains-a-spreadsheet-viewer-prerequisite-6accac80f419-attempt-1/execution-blocker.json). |

The report keeps these active blockers separate from the 27 user exclusions.
No screenshot or passing result was invented for unexecuted steps.

## Corrections and source limits

Harness corrections addressed fixture collisions, delayed UI state, stale READ fixtures, and request comparisons.
The [binding correction review](canonical-binding-review/review.md) records real SSO cancellation before retry.
It also records the corrected application recovery observer.
The [source review](source-consumption-review.md) preserves historical source drift and reuse limits.
The keyboard fixture now follows the canonical Cashflow panel position.
The assertions remain unchanged.

Frontend attempts use the actual MFE with controlled service and tenant responses where declared.
Current local BFF attempts use revision `834b4155232222347220e47139a502ee43a9cbdf`.
The [build manifest](current-bff-build/attempt-06/source-build-manifest.json) records the isolated bootstrap.
The [migration execution](current-bff-build/attempt-06/migration-execution.json) records all eleven unchanged SQL migrations.
The [final runtime snapshot](current-bff-build/final-runtime/manifest.json) records compiled classes, dependencies, bootstrap, logs, and health.
The bootstrap uses cached Spring Boot 3 dependencies and controlled external identities.
Production Boot 4 wiring and external identity integration remain unverified.
WebKit automation results do not establish installed Safari compatibility.

## Validation and retention

The [validation ledger](validation/checks.json) retains successful checks and environmental failures from earlier attempts.
The project interpreter passed 611 runtime tests with two skips after localhost listener access was available.
The wheel build passed with the existing project interpreter.
Twenty-four report and consumed-source regressions passed.
TypeScript checking, static POM contracts, and installed workspace validation passed.
The latest synthetic POM run passed all [24 checks](../audit-run-20261022/harness/run-002/run-result.json).
Synthetic checks do not count as application case passes.

The gallery separates 26 historical attempts with synthetic scope labels from actual application outcomes.
Their original paths, results, and traces remain retained.
The validator also records eleven contradictory historical step bindings.
Those superseded bindings contribute no current step evidence.
The [initial validation](validation/report-002-validation-initial.json) preserves the original failed checks.
The [final validation](validation/report-002-validation.json) identifies these historical findings and checks current bindings separately.

Final screenshot totals and report validation are recorded in the [generated summary](../audit-run-20261022/report-002/audit-summary.json).
Retained failed, interrupted, blocked, and superseded attempts remain available.
The report preserves exact implementation and fixture boundaries.
