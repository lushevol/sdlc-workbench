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

# Crosscut source inspection

> **No critical conclusions require user attention or action.**

This inspection supports proposed UI quality cases.
It does not establish defects through execution.

## Scope and source binding

MFE Base revision: `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
The [source manifest](source-manifest.json) records inspected file hashes.
The cases cite exact source lines from this revision.

| Surface | Inspected source | Observed source behavior | Coverage consequence |
| --- | --- | --- | --- |
| Header | [AppBar](../../../repos/ui/mfe-base/src/components/AppBar/index.tsx#L48) | Contains tile, theme, time, avatar, and feedback controls. | Probe keyboard access and constrained viewports. |
| Workspace label | [TabItem](../../../repos/ui/mfe-base/src/components/TabItem/index.tsx#L40) | Uses a text input with an accessible label. | Probe keyboard editing, Unicode, and long labels. |
| Dialog | [Dialog controller](../../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L69) | Sets dimensions from pointer movement. | Probe resizing and control reachability. |
| Dialog layout | [Position calculation](../../../repos/ui/mfe-base/src/components/Dialog/common/useController.ts#L161) | Calculates a position from body dimensions. | Probe viewport changes after opening. |
| Form field | [Field controller](../../../repos/ui/mfe-base/src/components/TableDetail/common/Field.useController.tsx#L24) | Schedules field changes after 300 milliseconds. | Probe immediate Save, Reset, Close, and rapid field changes. |
| Form consumer | [Tile detail controller](../../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L38) | Copies the current record for each field callback. | Probe overlapping callbacks for different fields. |
| Error message | [Snackbar](../../../repos/ui/mfe-base/src/components/Snackbar/index.tsx#L59) | Passes message markup through DOMPurify. | Probe hostile markup and retained safe text. |
| Support email | [FallbackError](../../../repos/ui/mfe-base/src/components/FallbackError/index.tsx#L31) | Inserts the error stack into a mailto URL. | Propose redaction and URL encoding assertions. |
| Export | [Table toolbar](../../../repos/ui/mfe-base/src/components/Table/index.tsx#L14) | Uses the DataGrid export toolbar. | Propose spreadsheet formula safety checks. |
| Profile | [Profile](../../../repos/ui/mfe-base/src/components/Profile/index.tsx#L203) | Displays identity fields and an external photo. | Probe missing fields, long names, and photo failures. |

## Inspected assertion boundary

The [Snackbar test](../../../repos/ui/mfe-base/src/components/Snackbar/index.test.tsx#L12) checks presence and ordinary message text.
It does not assert sanitizer safety, keyboard access, or scrolling behavior.
This task did not execute that test.

## Authority and execution limits

Accessibility, browser support, and supported viewport policies were unavailable in the bounded local review.
Each related assertion is proposed.
Browser names and viewport sizes define fixture inputs.
They do not establish supported product configurations.

The fixture dialog permits controlled shared-component probes.
Record that substitution separately from an application workflow during execution.
No browser, spreadsheet application, external photo host, or mail client was opened.
No performance service-level target is invented.

## Next actions

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Proposed accessibility and browser cases in the [catalog](../test-cases.md#coverage-navigation) | Business acceptance needs applicable product policy. | unknown | Confirm supported browser, viewport, and accessibility criteria. |
| Form callback source above | Source alone cannot confirm user-visible data loss. | unknown | Execute controlled field timing probes. |
| Shared-component and dependency probes above | These probes need controlled fixtures. | unknown | Bind fixtures and retained observations before execution. |
