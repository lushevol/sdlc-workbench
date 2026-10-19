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

# Full session-renewal pilot

## Scope and source

The user requested continued pilot work on 19 October 2026.
The user selected UAT1 for business testing.
The business reviewer remains unknown.
The Workbench source baseline is `141bf45`.
The assessed MFE implementation is `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.

The independent MFE checkout still uses `dddb76c8e8ba8ea66bb941feaad562740fdb8346`.
Exact revision reads and an isolated export supplied pilot evidence.
This stage preserves the unrelated `TODO` file and existing test-engine `CLAUDE.md` changes.

## Confirmed Workbench timeout defect

The existing UAT1 session case permits 960 seconds for the expiry prompt.
The workspace schema rejected timeouts above 300 seconds.
The provider timeout helper already supported 3600 seconds.
This mismatch prevented a scoped 1800-second test workspace from loading.

The workspace schema now supports up to 3600 seconds.
The canonical workspace timeout remains 30 seconds.
The [Robot guide](../ROBOT_TESTING.md) documents separate workspaces for long scenarios.
No dependency, credential, or business runtime source changed.

Affected interfaces include workspace loading, CLI and MCP dispatch, and provider execution contexts.
Qualitative risk is moderate because explicitly configured operations can run longer.
Existing default behavior remains unchanged.
One regression checks actual dispatch and retained results with an 1800-second timeout.
Another regression rejects a value above 3600 seconds before dispatch.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Schema cap 300 conflicts with provider cap 3600 | The existing long session case could not load. | Workbench maintainers; individual unknown | Keep configuration and provider limits aligned through regression checks. |

## Runtime and distribution checks

The [runtime suite](../evidence/session-renewal-full-20261019/runtime-tests.txt) completed 479 tests without failures; two tests were skipped.
The [wheel build](../evidence/session-renewal-full-20261019/wheel-build.txt) passed with installed build dependencies and `--no-build-isolation`.
An isolated installed environment passed 27 [wheel checks](../evidence/session-renewal-full-20261019/wheel-check.json) outside the source checkout.
Four additional [timeout checks](../evidence/session-renewal-full-20261019/timeout-wheel-check.json) passed through that installed runtime.
Those fixtures do not establish UAT1 behavior.

## Remaining verification gates

The requirement remains a candidate with no recorded human approval.
All seven business criteria remain `NOT_VERIFIED`.
Controlled source characterization, assertion inspection, and live business verification have separate evidence boundaries.
