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

# Canonical execution preflight

> **Critical conclusions: Complete business execution requires missing bindings.**
>
> Action: Bind real application setup and assertions before claiming complete results.
> Consequence: All 521 cases start this run as `BLOCKED_NOT_EXECUTED`.
> Owner: unknown. Evidence: [frozen preflight](case-preflight.jsonl), [summary](summary.json), and [binding manifest](../../../../../e2e/traceability/bindings.json).

This preflight records the execution starting point.
It does not replace later case results or establish application behavior.
Later execution can supersede a preflight status without changing these snapshot bytes.

The [canonical catalog](../../../test-cases.md) contains 521 cases and 1,596 assertions.
The source snapshot is Workbench commit `961f08c`.
The [input manifest](summary.json) records exact definition and mapping hashes.
Each [case record](case-preflight.jsonl) retains its canonical line, definition hash, step count, assertion count, and mapping status.

| Mapping state | Cases | Starting execution state |
| --- | --- | --- |
| Partial POM support | 210 | `NOT_RUN` |
| No POM support | 283 | `NOT_RUN` |
| Failed canonical UI gate | 28 | `NOT_RUN` |
| Complete real application binding | 0 | Unavailable |

The [traceability check](traceability-check.json) passed.
The [Gherkin quality check](quality-check.json) returned `FAIL` because required reviews, mappings, and component definitions remain unresolved.
Its current output exactly matched the [retained quality result](../../refinement/quality-results.json).
The evidence record retains the command, output hash, counts, and existing output locator.
No browser case ran through these static commands.

## Screenshot plan

The preflight identifies 1,175 conservative setup and UI observation frames across all case definitions.
The [frame plans](case-preflight.jsonl) reference exact canonical step lines and component identifiers.
They do not duplicate the Gherkin definitions or invent additional expected behavior.
They require each observable UI state before another event replaces it.
They also identify lifecycle events that can remove volatile evidence.

Actual execution must retain screenshots with case IDs, step references, timestamps, file hashes, and results.
Capture the actual failure state before teardown when an assertion fails.
Non-UI assertions require separate machine evidence.
A screenshot cannot establish request counts, token equality, timing, service responses, or authorization.
No business screenshot was captured by this inventory task.

## First feasible binding candidates

These candidates use existing login POM targets.
They still require a real React bundle and a verified runtime configuration.
They are investigation candidates, not executed cases.

| Candidate | Setup and missing binding |
| --- | --- |
| [AUTH-001](../../../test-cases.md#auth-001) | LOCAL login controls and native password masking. Add five explicit assertions. |
| [AUTH-002](../../../test-cases.md#auth-002) | DEV environment configuration. Assert the three credential controls. |
| [AUTH-003](../../../test-cases.md#auth-003) | SIT environment configuration. Assert the three credential controls. |
| [AUTH-004](../../../test-cases.md#auth-004) | UAT environment configuration. Assert the three credential controls. |
| [AUTH-005](../../../test-cases.md#auth-005) | PRE-PROD environment configuration. Assert the three credential controls. |
| [AUTH-006](../../../test-cases.md#auth-006) | PROD configuration without the query parameter. Assert hidden credentials and visible SSO. |
| [AUTH-007](../../../test-cases.md#auth-007) | PROD configuration with `show_normal_login=Y`. Assert visible credentials. |
| [AUTH-008](../../../test-cases.md#auth-008) | PROD configuration with `show_normal_login=y`. Assert visible credentials. |
| [AUTH-009](../../../test-cases.md#auth-009) | PROD configuration with `show_normal_login=N`. Assert hidden credentials and visible SSO. |
| [AUTH-010](../../../test-cases.md#auth-010) | PROD configuration with `show_normal_login=true`. Assert hidden credentials and visible SSO. |
| [AUTH-011](../../../test-cases.md#auth-011) | PROD configuration with `show_normal_login=1`. Assert hidden credentials and visible SSO. |
| [AUTH-012](../../../test-cases.md#auth-012) | PROD configuration with an empty query value. Assert hidden credentials and visible SSO. |
| [AUTH-013](../../../test-cases.md#auth-013) | LOCAL page with empty username. Add login POST counting and visible-control assertions. |
| [AUTH-014](../../../test-cases.md#auth-014) | LOCAL page with empty password. Add login POST counting and visible-control assertions. |
| [AUTH-015](../../../test-cases.md#auth-015) | LOCAL page with empty credentials. Add login POST counting and visible-control assertions. |

The existing session workflow maps [AUTH-078](../../../test-cases.md#auth-078) only through a synthetic substitute.
Actual authentication, fixed token expiry, controlled time, and application fixture equivalence remain missing.
The candidate cannot establish a complete business result through fixture execution.
