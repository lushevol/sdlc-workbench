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

# Review current BFF administration bindings

> **Critical conclusions: Action required**
>
> **Correct contradictory case definitions before accepting Tile-reference coverage.**
> Action: Resolve the [case conflicts](#case-definition-conflicts). Consequence: Their executions cannot establish their stated Tile behavior.
> Owner: unknown. Evidence: The linked canonical definitions and [binding selection](../../../../e2e/audit-specs/bff-admin.spec.ts#L13).
>
> **Complete the remaining assertions before accepting the affected steps.**
> Action: Complete the [Given assertions](#p2-several-given-steps-record-declarations-without-asserting-their-values). Consequence: Incorrect setup can receive a passing step result.
> Owner: Codex harness maintainer. Evidence: The assertion links below.

## Comparison and limits

This review compares two untracked harness additions against Workbench HEAD `908f88117032e2a3a0e2c4db0c75f5dce630a643`.
Both files have no tracked implementation at that HEAD.
The review inspected the current files, run-061 source snapshots, and affected helpers.
The current BFF source revision is `834b4155232222347220e47139a502ee43a9cbdf`.
The canonical catalog is unchanged during this review.
No database operation or application edit occurred during this review.

The parent owns the active run-061 execution and final result reconciliation.
This review makes no passing-execution claim for that run.
Static source predictions remain separate from retained execution results.
The local bootstrap replaces external identities and selected production configuration.
The [build manifest](current-bff-build/attempt-06/source-build-manifest.json) records excluded source patterns.
These limits prevent claims about complete deployed integration.

| Inspected input | SHA-256 |
| --- | --- |
| [Current BFF spec](../../../../e2e/audit-specs/bff-admin.spec.ts) | `0c57a644516095c6a7c56c7227dc2f4c891fcb9283c168f2b99a4b007b956f18` |
| [Run-061 BFF spec](../audit-run-20261022/application/run-061/source-snapshots/e2e/audit-specs/bff-admin.spec.ts) | `418f5da9614176e2589c2ebaede221fb4924ed4b546e614ee18bfb94122a28cb` |
| [BFF helper](../../../../e2e/support/bff-admin-app.ts) | `1ad2903ac525032902eb1af2ccc9d192c1561201e4663204d7642882eea5ce4a` |
| [Admin helper](../../../../e2e/support/admin-app.ts) | `1cbc6a5995570abf017bcf7950b7055744cd50335b9b239a50781f05c0409f55` |
| [Canonical catalog](../../test-cases.md) | `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4` |
| [Migration execution](current-bff-build/attempt-06/migration-execution.json) | `ddde58accddb1dbcfae25a4946718f3d94348f0cb9d300fccce4f240e95b752f` |
| [Tile controller](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java) | `ee98fe6f1d416e6646bf26ed950a47927218b4b56c96aff77f02c21afcc8ed79` |

## Binding corrections and remaining work

### Resolved in source: Latest-version response assertions

Definitions: [BFF-ADM-083](../../test-cases.md#bff-adm-083), [BFF-ADM-086](../../test-cases.md#bff-adm-086), and [BFF-ADM-089](../../test-cases.md#bff-adm-089).
Each final step requires the latest version of record 101.
The [run-061 binding](../audit-run-20261022/application/run-061/source-snapshots/e2e/audit-specs/bff-admin.spec.ts#L55) checked only `response.ok()`.
A successful response with stale values would pass that step.
The [current binding](../../../../e2e/audit-specs/bff-admin.spec.ts#L55) compares the changed value and update timestamp with persisted record 101.
This source correction requires a subsequent retained execution.

Owner: Codex harness maintainer.
Next action: Retain the corrected assertion execution after the active batch completes.
Focused validation: Reject HTTP 200 responses containing OLD or an empty list.

### Resolved in source: Audit image screenshot visibility

Definition: [BFF-ADM-097](../../test-cases.md#bff-adm-097).
The [run-061 binding](../audit-run-20261022/application/run-061/source-snapshots/e2e/audit-specs/bff-admin.spec.ts#L75) scrolled only until the target cell existed.
DataGrid can retain offscreen cells through column overscan.
`toHaveText()` does not require the cell to appear inside the screenshot viewport.
That step frame could therefore omit the checked value.
The [current binding](../../../../e2e/audit-specs/bff-admin.spec.ts#L75) scrolls the cell into view and requires visibility.
This source correction requires a subsequent retained execution.

Owner: Codex harness maintainer.
Next action: Inspect the corrected frame for grid clipping and readable values.
Focused validation: Both image assertions must show their respective column header, audit row 5001, and full value.
The existing [Admin helper](../../../../e2e/support/admin-app.ts#L156) provides a stronger starting pattern.

### P2: Several Given steps record declarations without asserting their values

The [baseline branch](../../../../e2e/audit-specs/bff-admin.spec.ts#L22) records a snapshot without comparing the declared field.
The [reference branch](../../../../e2e/audit-specs/bff-admin.spec.ts#L23) records Category rows without checking its label or Import Map.
The [entitlement branch](../../../../e2e/audit-specs/bff-admin.spec.ts#L56) records only the declaration.
The [seed builder](../../../../e2e/support/bff-admin-app.ts#L48) now reads most baseline fields.
It still hardcodes `filterRule:null` while several definitions declare an empty string.
Service normalization can explain this representation, but the step does not check that explanation.

Owner: Codex harness maintainer.
Next action: Assert each declared baseline field, reference identifier, owner, and relevant entitlement at its canonical step.
Document any deliberate UI-empty to persisted-null normalization with the [source rule](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L202).
Focused validation: A deliberately incorrect label, reference owner, or entitlement must fail its Given step.

## Case definition conflicts

These are retained definition defects rather than demonstrated product failures.
The current selection derives the resource from each controlled-fixture declaration.
Following the written steps therefore selects Import Map for all four cases below.

| Definition | Conflict | Consequence | Next action |
| --- | --- | --- | --- |
| [BFF-ADM-076](../../test-cases.md#bff-adm-076) | Purpose requires a Tile update. Steps edit Import Map 301 and later require Tile reference columns. | The selected resource cannot establish Tile reference authorization. | Replace the conflicting steps with explicit Tile controls in a reviewed successor definition. |
| [BFF-ADM-077](../../test-cases.md#bff-adm-077) | Purpose requires Tile creation. Steps create an Import Map. | An added `importMap` property does not turn that request into Tile creation. | Align the fixture, form, operation, and assertions with the intended entity. |
| [BFF-ADM-079](../../test-cases.md#bff-adm-079) | Purpose requires a missing Tile reference. Steps create an Import Map after deleting map 201. | The deletion does not test a Tile submission. | Define the selected Tile reference and submit the Tile form. |
| [BFF-ADM-082](../../test-cases.md#bff-adm-082) | Purpose requires Tile activation. Steps verify Import Map 301 while declaring Import Map 201 inactive. | The selected entity does not establish Tile activation protection. | Align the verified entity and referenced map with the intended relationship. |

Owner: unknown for the intended behavior; Codex harness maintainer for binding corrections after definition alignment.
Preserve the current catalog hash and dependent attempts when a successor definition is created.
Do not present these runs as passing coverage of the stated Tile purposes.

## Corrections confirmed by source inspection

The helper now separates the initial grid from the expected persisted state after controlled ownership changes.
The [mutation method](../../../../e2e/support/bff-admin-app.ts#L37) refreshes that expected state.
This removes the earlier false mismatch after intentional ownership changes.

The bootstrap uses distinct identifiers 9900, 9901, and 9902.
These identifiers avoid collision with stale foreign row 901.
The [stale fixture](../../../../e2e/support/bff-admin-app.ts#L54) now includes an actual foreign audit row.
The [error helper](../../../../e2e/support/bff-admin-app.ts#L116) also considers audit responses.
These corrections support [BFF-ADM-063](../../test-cases.md#bff-adm-063), [BFF-ADM-068](../../test-cases.md#bff-adm-068), and [BFF-ADM-073](../../test-cases.md#bff-adm-073).
Execution still determines the actual authorization outcomes.

The grid snapshot resets horizontal scrolling before its comparison.
The submit helper waits for a new create or update response.
The creation clock applies only to the Create New event.
The [097 setup](../../../../e2e/audit-specs/bff-admin.spec.ts#L74) creates its audit row through the actual BFF update operation.
It does not inject the expected audit image values.

## Migration evidence and case 032

[BFF-ADM-032](../../test-cases.md#bff-adm-032) requires the inspected migration DDL.
The [migration manifest](current-bff-build/attempt-06/migration-manifest.json) lists all eleven migration files through V1_1_0.
It records unchanged SQL bytes and PostgreSQL 18.4.
The [execution record](current-bff-build/attempt-06/migration-execution.json) reports exit code 0 for every migration.
This supersedes the earlier concern about using only an initial schema or generated JPA DDL.

The [case branch](../../../../e2e/audit-specs/bff-admin.spec.ts#L24) captures current column metadata.
It does not independently report a migration revision.
The final report must link the migration manifest and execution record beside this case.
The local bootstrap adds required database roles and schema before applying the retained SQL.
These records establish the local migration setup, not production database equivalence.

## Initial administration module restoration

The bootstrap tile stores the resource without a leading slash and stores an empty tile path.
The initial workspace uses `@fm/base`, a slash-prefixed resource, and tile `/`.
The [drawer builder](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L145) supplies those prefixes.
The differing stored and UI strings therefore do not establish a restoration defect.

The bootstrap map still names `http://localhost:8122/MicroWebUI_base.js`.
The current prepared bundle uses `http://127.0.0.1:8122/base.js`.
Owner: Codex harness maintainer.
Next action: Align the fixture URL with the current bundle before testing a fresh dynamic load.
This mismatch does not explain a sign-in failure before module restoration.

The retained [run-057 error context](../audit-run-20261022/application/run-057/playwright-artifacts/bff-admin-BFF-ADM-001-curr-46b77-istration-through-actual-UI/error-context.md#L57) remains on Sign In.
Its message states: `Invalid username and password combination or SSO service is unavailable.`
That attempt failed before administration module visibility.
It cannot establish a restoration failure.

## Source prediction for audit images

The [Tile controller](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L238) assigns the light value to `imageDarkTheme`.
The next line assigns the dark value to `imageLightTheme`.
This predicts swapped audit values for distinct light and dark inputs.
Owner: unknown business repository maintainer.
Next action: Retain the actual [BFF-ADM-097](../../test-cases.md#bff-adm-097) result and its visible cell evidence.
Do not change the business source to make the audit pass.

## Validation

The focused automated check verified local link targets, input hashes, and required report fields.
The [validation record](bff-binding-review-check.json) retains its checks and limits.
The review ran no new application test and consumed no database fixture.
The report preserves prior attempts and canonical definitions.
ASD review remains pending.
