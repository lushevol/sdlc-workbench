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

# Browser compatibility execution

> **Critical conclusion: All four browser cases fail at the same exact workspace-name comparison.**
> Action: Review the extra trailing space before accepting compatibility coverage. Consequence: The later profile steps remain unexecuted.
> Owner: unknown for the business application. Evidence: The [retained results](results.json) and [title construction](../../../../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L14).

## Final retained results

The [browser specification](../../../../../e2e/audit-specs/browser-compatibility.spec.ts) selects each engine through `E2E_COMPAT_BROWSER`.
The shared audit configuration keeps its Chromium default.
The specification configures worker options at the file scope.
It preserves the exact `Cashflow` value comparison.
All four final runs use specification SHA-256 `5b09e9f52e7b7a70ce78a1fa472d6dce1f7831bc8395efe258a5e2361c83cac2`.

| Definition | Browser | Version | Final run | Outcome |
| --- | --- | --- | --- | --- |
| [UX-059](../../../test-cases.md#ux-059) | Playwright Chromium | 156.0.8078.4 | [run-067](../../audit-run-20261022/application/run-067/run-result.json) | FAIL at step 8 |
| [UX-060](../../../test-cases.md#ux-060) | Installed Microsoft Edge | 155.0.4283.62 | [run-051-edge-final](../../audit-run-20261022/application/run-051-edge-final/run-result.json) | FAIL at step 8 |
| [UX-061](../../../test-cases.md#ux-061) | Playwright Firefox | 157.0 | [run-064-final](../../audit-run-20261022/application/run-064-final/run-result.json) | FAIL at step 8 |
| [UX-062](../../../test-cases.md#ux-062) | Playwright WebKit | 27.2 | [run-065-final](../../audit-run-20261022/application/run-065-final/run-result.json) | FAIL at step 8 |

Each case passes steps 1 through 7.
Step 8 expects the exact string `Cashflow`.
The selected workspace input contains `Cashflow `, including one trailing U+0020 character.
The [drawer implementation](../../../../../repos/ui/mfe-base/src/components/Drawer/common/MenuItem.useController.ts#L14) always inserts a space before the optional subtitle.
The controlled tile omits that subtitle.
The same result across engines does not establish a browser-specific cause.

Each final case retains nine named frames.
Executed steps 1 through 8 each have one screenshot.
The final failure frame is additional evidence.
Steps 9 through 13 remain `NOT_EXECUTED` and have no claimed screenshots.
These runs do not establish the later profile behavior.

## Firefox transport correction

The [first Firefox run](../../audit-run-20261022/application/run-064/run-result.json) received HTTP 503 for its initial localhost navigation.
Its trace includes `Proxy-Connection: close` and `NS_ERROR_NET_ERROR_RESPONSE`.
The [two-context experiment](firefox-transport-probe.json) compares default transport with `network.proxy.type=0`.
Default transport repeats HTTP 503.
Explicit direct transport receives HTTP 200 from the local application and its assets.

The final specification applies that Firefox preference only to this isolated compatibility audit.
The existing external-request blocker remains active.
The record includes proxy variable names without recording proxy hosts or credentials.
The [final Firefox result](../../audit-run-20261022/application/run-064-final/run-result.json) then reaches the same workspace-name assertion as the other browsers.
The transport correction does not change application behavior or weaken the expected value.

The [initial Edge setup](../../audit-run-20261022/application/run-051/run-result.json) also remains available.
Playwright rejected worker-scoped options inside a describe group.
No canonical case step executed in that setup attempt.
The final specification moves those options to the file scope.

## Evidence checks and limits

The [machine review](results.json) checks all final case artifact hashes.
It confirms one specification hash across all four final runs.
It also confirms a screenshot for each executed canonical step.
Three frames received visual review: Firefox login, Firefox failure, and WebKit failure.
Their visible states and exact hashes remain in the machine review.

The controlled Cashflow module displays its explicit fixture marker.
These runs do not use the business Cashflow tenant or a deployed identity provider.
Firefox and WebKit use Playwright automation builds.
WebKit execution does not establish Safari product compatibility.
TypeScript validation passes.
The final audit must retain the failures and the unexecuted profile steps.
