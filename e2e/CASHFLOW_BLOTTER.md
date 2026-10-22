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

# Cashflow blotter page object

The [page object](pages/cashflow-blotter.page.ts) covers the inspected CN blotter and its OpenSearch entry.
It composes [shared controls](components/cashflow/control-scope.ts), [grids](components/cashflow/data-grid.component.ts), [builders](components/cashflow/builders.ts), and [dialogs](components/cashflow/dialogs.ts).
Runtime coverage of a deployed application remains unverified.

## Requested scope and implementation risk

Source: [user message in Codex chat, 22 October 2026](traceability/cashflow-blotter-request.json).

> create playwright POM for cashflow blotter, must cover all interact-able components.

This change maintains the test harness.
It adds no business behavior, dependency, credential, or transaction execution.
The affected consumers are typed Playwright tests and future authorized UI investigations.
Qualitative risk is moderate because fields, permissions, portals, and virtual grids change control availability.

## Control coverage

| Area | Page object entry | Supported controls |
| --- | --- | --- |
| Quick search | `quickSearch` | Cashflow, trade, original trade, currency, taxonomy, counterparty, booking entity, beneficiary, state, and substate fields. |
| Search variants | `quickSearch.chooseVariant`, `setAmount`, `setDateRange` | Conditional field variants, four amount operators, range endpoints, date endpoints, Search, and Clear Filters. |
| Quick filters | `quickFilter`, `chooseQuickFilter` | Nine filters, options, multiple selection through repeated option actions, and Clear All. |
| Presets | `preset` | Today and next business day counters for operator and verification states. |
| Search layout | `hideSearchBar`, `showSearchBar` | Hide and show controls. |
| Saved searches | `selectSavedFilter`, `clearSavedFilter`, `searchBuilder` | Selector, create, duplicate, save, delete, private state, search, and filter list. |
| Query rules | `searchBuilder.query` | Nested groups, combinators, fields, operators, remove actions, and generated value editors. |
| Query values | `CashflowQueryRule` | Text, numbers, lists, dates, times, ranges, regular expressions, switches, checkboxes, and radio controls. |
| Value popups | `relativeDatePopup`, `regularExpressionPopup`, `calendar` | Relative dates, offsets, expression flags, calendar controls, and options within explicit popup scopes. |
| Saved views | `selectSavedView`, `clearSavedView`, `viewBuilder` | Selector, name, roles, private state, save, remove, close, categories, field labels, and field search. |
| View columns | `viewBuilder` | Available fields, displayed fields, delete controls, drag targets, and keyboard movement. |
| Main grid | `grid` | Row and header selection, cells, sorting, resizing, column filters, scrolling, tooltips, context menus, and double-click. |
| Footer | `footer`, page methods | Load next, load size, resize, alerts, filter tags, grid filter clearing, export, and upload. |
| Export | `dialogs.exportFile()` | Filename, CSV/XLSX selection, Export, and header controls. |
| Notifications | `notificationReconnectButton`, `dialogs.details().refreshButton` | Reconnect and stale cashflow refresh. |
| Comment workflows | `dialogs.comment(action)` | Hold, fail, settle, release, suppression, affirmation, comments, submit, reject, and selected cashflow identifiers. |
| Netting | `dialogs.netting()`, `previewAffirmation('netting')` | Preview grids, close, affirmation fields, and submit. |
| Splitting | `dialogs.splitting(mode)`, `previewAffirmation('splitting')` | Parent and child grids, indexed amounts, delete, SSI lookup, affirmation, and confirmation. |
| SSI lookup | `dialogs.lookupSsi()` | Vostro and Nostro sections, records, forms, reset, pagination, and submit. |
| Bulk exceptions | `dialogs.bulkExceptions(role)` | Eligible rows, select all, insufficient records, comments, dates, affirmation, submit, approve, and reject. |
| Settlement method | `dialogs.settlementMethod()` | Eligible records, insufficient records, trade identifiers, comments, and submit. |
| Cashflow details | `dialogs.details()` | Four tabs, entity buttons, trade navigation, children, history, accounting, exceptions, Swift messages, copy, and export. |
| Exception forms | `details().vostro`, `details().nostro` | 71 unique Vostro field identities and 11 Nostro identities, including conditional fields. |
| Dialog controls | `CashflowDialog` | Close, maximize/restore, title drag target, and resize handle. |
| Confirmations | `dialogs.confirmation(title)`, `rejectExceptionsPopup()` | Explicitly scoped buttons and fields. |

The inventories preserve source declarations, exact paths, line ranges, and SHA-256 fingerprints:

- [Main controls and menu actions](traceability/cashflow-main-inventory.json).
- [Workflow controls and generated SSI fields](traceability/cashflow-dialog-inventory.json).
- [Shared toolkit controls](traceability/cashflow-shared-inventory.json).

The inventories distinguish source evidence from runtime uniqueness.
Five blank SSI layout declarations are permanently hidden and have no editable field identity.
`cashflowSsiFields` exports the 82 meaningful identities.
Generated controls also remain accessible through scoped `testId`, `label`, `field`, `combobox`, and role methods.
Use `hover` for tooltips, `press` for keyboard controls, and `dragTo` for explicit drag targets.

## Use the page object

Supply the actual build prefix and an authenticated Playwright page.
The constructor does not navigate, authenticate, or choose business data.

```ts
import { CashflowBlotterPage } from './pages/cashflow-blotter.page.js';

const blotter = new CashflowBlotterPage(page, actualBuildPrefix);
await blotter.expectVisible();
await blotter.quickSearch.fillText('Cashflow ID', knownCashflowId);
await blotter.quickSearch.search();
await blotter.grid.expectCellText(knownCashflowId, 'Cashflow.Cashflow_Id', knownCashflowId);

await blotter.quickSearch.setAmount('between', '100.00', '200.00');
await blotter.openViewBuilder();
await blotter.viewBuilder.fill(blotter.viewBuilder.searchFields, 'Payment');
await blotter.viewBuilder.click(blotter.viewBuilder.closeButton);
```

Supply `instanceRoot` when several tiles share a prefix.
Constructors also accept explicit component roots for already identified dialogs and panels.
Every interaction checks scope visibility, target uniqueness, and enabled state.
Hidden file inputs receive separate upload checks.

Options resolve through the opener's ARIA association.
AntD virtual options resolve through their associated dropdown.
Supply an explicit observed popup when the application has no usable ARIA association.
The POM never chooses an unrelated option by its page-wide text.

Main grid rows use `Cashflow_Id` and `col-id` identities.
Nested grids can lack stable row keys.
Use `rowByDisplayedCell` and `cellInRow` for an exact displayed identifier in those grids.
Virtual rows and columns must be rendered before interaction.
Splitting controls use source-defined row indexes.
Query rule and group methods require explicit indexes because the inspected source supplies no stable rule identity.

## Evidence limits

Remote trade and unnet component implementations are absent from the registered source copies.
Their launch controls have source evidence.
Use `dialogs.external(observedRoot)` for inspected remote controls.
Owner: unknown. Next action: inspect those remote builds before claiming complete runtime coverage.
This limit prevents a complete claim about remote dialog internals.

AG Grid, AntD, MUI, and drag library DOM contracts require validation against the selected application build.
Filesystem copies have no independent Git revision.
The source checker therefore uses exact hashes and preserves `revision: null`.
Separate dashboards, static maintenance pages, and group management are outside the blotter entry.
The unused accounting Republish component remains excluded because the current details screen does not render it.

## Validation

Run these commands from the Workbench root:

```sh
npm run e2e:typecheck
node e2e/scripts/check-cashflow-sources.mjs
npm run e2e:test
```

The [source checker](scripts/check-cashflow-sources.mjs) verifies inventory hashes and bounded source references.
The canonical harness cases live in [control tests](specs/cashflow-blotter.spec.ts), [page tests](specs/cashflow-page.spec.ts), and [dialog tests](specs/cashflow-dialogs.spec.ts).
Each case states Given, When, and Then conditions and contains explicit assertions.
These tests exercise synthetic DOM controls and browser file transfers.
They do not execute the React bundle or establish passing business workflows.
See the [retained validation](validation/cashflow-blotter-20261022.json) for results, revisions, and execution limits.
