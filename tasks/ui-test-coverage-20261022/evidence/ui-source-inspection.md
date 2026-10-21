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

# UI source inspection

> **Review proposed expectations before acceptance.**
> Action: confirm the proposed outcomes in the canonical catalog.
> Consequence: these expectations cannot establish business acceptance before review.
> Owner: unknown application owner. Evidence: [source-risk observations](#source-risk-observations).

This inspection produced 156 UI case designs.
Of these, 144 use implementation behavior, and twelve propose outcomes or conditional integrations.
No new business case ran.
Implementation evidence does not establish approved intent or deployed parity.

## Source binding

The inspected MFE revision is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
The checkout has one pre-existing change: `tsconfig.tsbuildinfo`.
All 63 inspected file hashes match the recorded Git revision.
The [source receipt](ui-source-inspection.json) records paths, SHA-256 hashes, and inspected assertion locators.

| Surface | Exact source | Scope and limits |
| --- | --- | --- |
| Workspace tabs | [Home](../../../repos/ui/mfe-base/src/pages/Home/index.tsx#L62), [controller](../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36) | Add, rename, select, remove, refresh, and validate restored tabs. |
| Workspace persistence | [Reducer](../../../repos/ui/mfe-base/src/hooks/reducer/workspaces.reducers.ts#L8) | Saved browser state. Concurrent browser policies remain unproved. |
| Catalog grouping | [Grouping](../../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L20), [entry controls](../../../repos/ui/mfe-base/src/components/Tile/index.tsx#L35) | Global defaults, regional actions, disabled states, and image choices. |
| Module composition | [Container](../../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L8), [fallback](../../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L11) | Dynamic import, loading, failure isolation, and support email. |
| External opening | [URL parameters](../../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L15), [FDC3](../../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L46) | Controlled URL and intent fixtures. Real external desktop integration remains unexecuted. |
| Admin screens | [Routes](../../../repos/ui/mfe-base/src/admin/Routing.tsx#L11), [grid](../../../repos/ui/mfe-base/src/components/Table/index.tsx#L26) | Category, Import Map, Tile, record modes, pagination, and audits. |
| Admin fields | [Field controls](../../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L14) | Text, numeric, autocomplete, select, and inherited disabled state. |
| Preferences | [Theme](../../../repos/ui/mfe-base/src/components/Switch/common/useController.ts#L26), [clock](../../../repos/ui/mfe-base/src/components/SwitchTime/common/useController.ts#L14) | Local preferences and controlled time display. |
| Profile | [Profile](../../../repos/ui/mfe-base/src/components/Profile/index.tsx#L142) | Identity, functional roles, data entitlement roles, and action chips. |

Source links identify implementation. They do not identify approved business requirements.
The URL launch hook is not called by the inspected production Home component.
[UI-MFE-011](../test-cases.md#ui-mfe-011) and [UI-MFE-012](../test-cases.md#ui-mfe-012) require a conditional hook fixture.
They are proposed integration cases. They do not predict default shell routing.
The canonical catalog must retain this distinction.

## Inspected assertions

| Assertion source | Assertion inspected | Limit |
| --- | --- | --- |
| [Grouping assertion](../../../repos/ui/mfe-base/src/components/Drawer/MenuItem.test.tsx#L211) | Mocked Tile call count and grouped entry properties. | It does not execute actual card navigation. |
| [Partial availability assertion](../../../repos/ui/mfe-base/src/components/Drawer/MenuItem.test.tsx#L282) | A mixed group receives `disabled: false`. | It does not test a disabled Global default click. |
| [Tile metadata assertion](../../../repos/ui/mfe-base/src/components/Tile/index.test.tsx#L125) | Indonesia label and icon exist. | It does not prove end-to-end regional permissions. |
| [Workspace marker assertion](../../../repos/ui/mfe-base/src/components/TabItem/index.test.tsx#L64) | Indonesia marker and tab controls exist. | It does not prove persistence or removal selection. |
| [Container assertion](../../../repos/ui/mfe-base/src/pages/Home/common/Container.test.tsx#L30) | `screen` is defined. | It does not assert the loaded module or displayed business data. |
| [Category assertion](../../../repos/ui/mfe-base/src/admin/Category/index.test.tsx#L387) | `screen` is defined. | It does not prove create, update, verify, or deactivate outcomes. |
| [Import Map assertion](../../../repos/ui/mfe-base/src/admin/ImportMap/index.test.tsx#L584) | `screen` is defined. | It does not prove admin record outcomes. |
| [Tile admin assertion](../../../repos/ui/mfe-base/src/admin/Tile/index.test.tsx#L995) | `screen` is defined. | It does not prove category filtering or admin record outcomes. |

These assertions were inspected without execution.
Historical [Jest output](../../portal-background-session-20261019/evidence/code-review-refresh-20261021/suite-suite-suite/run.json) describes its own source and execution conditions.
It cannot establish passing execution for this new catalog.
Historical [session comparisons](../../portal-background-session-20261019/evidence/code-review-refresh-20261021/summary.json) cover separate session conditions.

## Source-risk observations

These observations propose test coverage. They are not confirmed defects or old/new comparisons.

| Source observation | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| A mixed group can use a disabled Global entry as its default. [Source](../../../repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx#L20). | A card-body click needs a separate entitlement assertion. | unknown | Review the proposed disabled-default case. |
| Reset copies the original row without preserving its dialog mode. [Source](../../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L15). | Action availability after Reset needs explicit coverage. | unknown | Review proposed edit and new-record Reset outcomes. |
| Owner uses an explicit disabled flag based on SUPER_USER. [Source](../../../repos/ui/mfe-base/src/components/TableDetail/Field.tsx#L34). | That flag can override record-level read-only mode. | unknown | Review Owner protection during verification. |
| Category fetch callbacks update shared rows after responses arrive. [Source](../../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L103). | Response ordering needs controlled UI cases. | unknown | Review pending-request and category-clearing outcomes. |
| Container selection resolves its record through Module Name. [Source](../../../repos/ui/mfe-base/src/admin/common/utils/importmap.ts#L55). | Duplicate labels need a defined selection policy. | unknown | Review the proposed ID-labelled options. |
| Audit opens only when returned rows exist. [Source](../../../repos/ui/mfe-base/src/admin/common/Main/index.tsx#L40). | Empty history needs a defined visible result. | unknown | Review the proposed empty state. |

Shared field propagation uses a 300-millisecond delay.
The main author covers immediate-save and reset races separately.
No performance service level is inferred from that implementation timer.
