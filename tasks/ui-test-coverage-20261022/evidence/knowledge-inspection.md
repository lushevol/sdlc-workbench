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

# Domain knowledge case inspection

> **Critical conclusions: Action required**
>
> **Review source applicability before business acceptance.**
> Action: Confirm the applicable rules and conditional integration contracts. Consequence: Business acceptance remains blocked for affected cases.
> Owner: unknown. Evidence: [Candidate authority limits](../../../knowledge/candidates/index.md#coverage-and-review-limits).
>
> **Portal-entry rules conflict between retained sources.**
> Action: Select the applicable entity requirement. Consequence: The no-entity login assertion cannot establish acceptance.
> Owner: unknown. Evidence: [Draft principles](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>) and [older security proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>).

## Contribution

The [canonical domain cases](../test-cases.md#group-entitlement-policy) contains 52 UI case designs.
It contains 23 documented expectations and 29 proposed expectations.
Every case remains `NOT_RUN` and `OWNER_REVIEW_REQUIRED`.
Documented means a retained source states the expectation. It does not establish approval, deployment, or passing execution.

| Coverage | Case count | Principal evidence |
| --- | --- | --- |
| Entity, subject, and tenant permission boundaries | 17 | [Draft principles](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>), [tile security proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L5>), and [SSDR alternatives](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L13>) |
| Portal intents and conditional OpenFin POC | 23 | [Intent navigation](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L5>), [POC contract](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>), and [reported compatibility issue](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L8>) |
| Cache and version lifecycle | 12 | [Cache design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L7>) |

All integration cases require controlled fixtures.
Source A, Target B, T-CACHE, trade identifiers, and build markers are synthetic test entities.
They do not establish existing product controls or external tenant behavior.
The caller and provider contracts require owner confirmation before integration execution.

## Authority and source identity

The [knowledge map](../../../knowledge/candidates/index.md) identifies every domain record as candidate and draft.
The records have unknown owners and no recorded human approval.
The source manifest preserves raw snapshot identities and local hashes.
Original page revisions, authors, and applicability remain unresolved.

The [source manifest](source-manifest.json) retains 22 inspected knowledge source identities and hashes.
All recorded raw snapshot hashes match their existing manifest entries.
The Workbench revision is `8dd076eac24c1b18b2f44245b3220ebcaf8537e3`.
The inspected MFE revision is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
The MFE worktree contains an unrelated `tsconfig.tsbuildinfo` modification.
This contribution changes no repository implementation or existing evidence.

## Inspected assertions

The [dispatcher unit assertions](../../../repos/ui/mfe-base/src/hooks/dispathcer/index.test.ts#L19) inspect workspace payloads and preserved parameters.
They also check tile-presence access helpers for populated and empty drawers.
These assertions do not verify a rendered target, provider handler, or tenant data permission.
No new case inherits their passing status.

The [dispatcher implementation](../../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L152) selects a matching drawer tile and forwards parameters.
It reports unauthorized or missing tiles when no match exists.
This is source evidence. It does not prove runtime integration or accepted authorization policy.

The [container tests](../../../repos/ui/mfe-base/src/pages/Home/common/Container.test.tsx#L15) primarily assert that `screen` exists.
The [analytics test](../../../repos/ui/mfe-base/src/analytics/index.test.tsx#L73) also asserts that `screen` exists.
The [older dispatcher tests](../../../repos/ui/mfe-base/src/hooks/dispathcer/index.test.tsx#L254) use the same assertion.
Those assertions cannot establish the new UI outcomes.

## Retained execution limits

The [prior Blotter summary](../../portal-background-session-20261019/evidence/uat-blotter-browser-20261021/summary.json) retains five executed local cases.
It records four passes, one failure, and one additional unexecuted case.
Its fixtures replace identity, catalog, entitlement, and business responses.
Natural browser freezing, device sleep, and UAT property origin remain unverified.

The [prior-tile result](../../portal-background-session-20261019/evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/result.json) retains failed assertions.
Native pointer activity contaminated its removal control.
The new catalog must preserve that uncertainty.
This contribution ran no browser, service, unit, or production tests.

## Open rule decisions

| Decision | Evidence and consequence | Owner | Next action |
| --- | --- | --- | --- |
| Portal entry with no registered entity | Draft principles reject entry. The older security proposal permits all SC accounts. Acceptance cannot select both. | unknown | Select and record the applicable rule. |
| Empty entity configuration | The older proposal permits empty roles. The SSDR guest proposal is struck through. Implicit access remains unresolved. | unknown | Define empty-entity behavior and negative assertions. |
| SSDR subject skipping and delegation | The discussion contains alternatives without retained selection or approval. | unknown | Confirm the selected tenant rule and permission owner. |
| Intent and context schema | The guide has empty code blocks. The POC mixes `OpenTile` and `fmchannel.fmoportal`. | unknown | Agree one versioned contract and supported runtime. |
| Cache deployment behavior | The cache document has an empty Implementation section. Current headers and build naming remain unverified. | unknown | Bind the design to deployment evidence before acceptance. |
| UI performance limits | Historical targets are drafts. Current accepted limits are absent from the bounded review. | unknown | Obtain reviewed budgets before adding performance pass limits. |

No resolved material domain clarification occurred.
This contribution therefore creates no knowledge publication or governance audit event.
