# UX-043 native viewer investigation

**UX-043 remains blocked at step 3. The audit owner must resolve native import before spreadsheet assertions can run.**

The CSV path is recognized. Numbers does not complete native import through the available CUA controls.

[UX-043](../../../test-cases.md#ux-043) requires imported text cells and an enabled spreadsheet evaluator.
This investigation continues retained run-050 evidence. It does not establish a new Playwright attempt.

- Owner: Audit execution owner.
- Consequence: Steps 4 and 5 remain unexecuted.
- Next action: Enable reliable Numbers import, then inspect value, formula, type, and a separate arithmetic control.
- Evidence: [Native action ledger](native-investigation.json), [native frame](numbers-path-sheet-blocked.png), and [accessibility state](numbers-path-sheet-blocked-ax.txt).
- Input: [Exact retained CSV](run-050-export-exact.csv) and [source linkage](investigation-inputs.json).

The native API recognizes the exact CSV path and its containing folder.
Return, click, double click, typing, and exposed suggestion actions did not complete import.
The native screenshot shows a file-navigation sheet. It does not show imported cells.

No cell value, formula, data type, or evaluator result was observed.
No formula control was entered. No original CSV bytes were changed.

The native tool documentation states:

> Use `cua_repl` (JavaScript) for all UI actions.
> Do not use other technologies besides `cua_repl` for computer interactions, unless specifically requested by the user (e.g. AppleScript, `osascript`, JXA, System Events, CGEvent synthesis).

The investigation did not use AppleScript or a command-line application opener.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
