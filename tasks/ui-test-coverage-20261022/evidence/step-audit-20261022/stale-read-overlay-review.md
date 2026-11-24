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

# Review controlled stale READ fixtures

> **Use the declared stale READ fixture to reach the real authorization check.**
> Action: Apply the narrow fixture described below. Consequence: The case can characterize server rejection after stale UI exposure.
> Owner: Codex harness maintainer. Evidence: The [canonical setups](#canonical-authority) and [controller checks](#actual-server-boundary).

## Canonical authority

[BFF-ADM-062](../../test-cases.md#bff-adm-062) explicitly permits a controlled stale Category fixture.
[BFF-ADM-067](../../test-cases.md#bff-adm-067) explicitly permits a controlled stale Import Map fixture.
[BFF-ADM-072](../../test-cases.md#bff-adm-072) explicitly permits a controlled stale Tile fixture.
Each setup requires subject `admin-s`, role `SUPER_USER only`, and persisted row 101 owned by `FMO_ADMIN`.
Each final assertion requires the exact denial and unchanged grid values.
The canonical catalog SHA-256 is `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4`.

[BFF-ADM-063](../../test-cases.md#bff-adm-063), [BFF-ADM-068](../../test-cases.md#bff-adm-068), and [BFF-ADM-073](../../test-cases.md#bff-adm-073) provide related stale-grid precedents.
Their stale rows support real audit rejection checks.
The [existing helper](../../../../e2e/support/bff-admin-app.ts#L97) already overlays those READ responses.
This review does not require a new business interpretation or a changed canonical definition.

## Actual server boundary

The [Category update controller](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40) validates entitlements and loads persisted row ownership.
The [Import Map update controller](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60) follows the same ownership boundary.
The [Tile update controller](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46) also loads both persisted references.
The [Tile role check](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183) compares the submitted identity role with all three persisted owners.
These sources are revision `834b4155232222347220e47139a502ee43a9cbdf`.
Source inspection predicts rejection; retained execution must establish the actual outcome.

## Fixture boundary and assertions

1. Seed the actual Category, Import Map, or Tile row 101 with owner `FMO_ADMIN`.
2. Authenticate `admin-s` through the local signed identity fixture with only `SUPER_USER`.
3. Overlay only the declared READ visibility response with the actual persisted row.
4. For Tile, expose required reference READ data without changing persisted identifiers or owners.
5. Keep the browser update body, signed tokens, real BFF update operation, and actual response unchanged.
6. Assert the exact denial: `You do not have access to this record.`
7. Independently compare persisted values and the displayed grid against their initial snapshots.
8. Retain the READ overlay description, actual update request, response status, response body, and per-step screenshots.

The final report must identify the controlled READ overlay beside each result.
That result concerns update rejection after stale visibility.
It does not establish normal `SUPER_USER` read access or ordinary row discovery.
Retain earlier precondition failures as historical evidence.
Do not grant `FMO_ADMIN`, change persisted ownership, or fabricate a denial response to reach the expected result.

## Review limits

This review is read-only and does not implement the proposed fixture.
It does not establish a passing case or full deployed authorization behavior.
The isolated bootstrap substitutes external identity systems and selected production configuration.
The [build manifest](current-bff-build/attempt-06/source-build-manifest.json) records those source exclusions.
Application changes remain outside this characterization stage.
