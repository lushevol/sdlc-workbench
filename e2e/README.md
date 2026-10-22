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

# Root Playwright POM

This harness makes source-backed UI operations executable and discoverable by AI.
It links the [521 canonical UI cases](../tasks/ui-test-coverage-20261022/test-cases.md) through explicit bindings.
The frozen catalog preserves its original design and review states.
The [execution stage](../tasks/ui-test-coverage-20261022/execution-stage.md) links current results and environment limits.
The `specs/` tests check synthetic POM fixtures.
The `audit-specs/` tests execute selected local application predicates with disclosed service and runtime fixtures.

The current areas are login, portal navigation, session expiration, and Category administration.
The Category page supplies the first representative administration area.
Settlement and trade pages remain outside this stage because inspected source does not establish their controls.
The harness stays under root `e2e/` and does not modify the business test engine.

## Structure and ownership

| Layer | Source | Responsibility |
| --- | --- | --- |
| Component objects | [components](components/) | Own scoped locators, concrete interactions, and UI observations. |
| Page objects | [pages](pages/) | Compose logical portal areas and reusable components. |
| UI contracts | [ui-contracts.ts](catalog/ui-contracts.ts) | Share identities and exact source references with POM consumers. |
| Action catalog | [actions.ts](catalog/actions.ts) | Bind descriptions and preconditions to typed POM functions. |
| Business flow | [session extension](flows/session-extension.flow.ts) | Check independent UI, credential, request, and response predicates. |
| CLI | [runner.ts](ai/runner.ts) | Dispatch allowlisted commands in one context per invocation. |
| Discovery | [discovery.ts](support/discovery.ts) | Inspect targets, capture accessibility state, and count visible controls. |
| Traceability | [binding guide](traceability/README.md) | Link canonical definitions without copying their Gherkin. |
| Tests | [specs](specs/) | Check POM mechanics and consequential failure boundaries. |
| Application audit | [audit specs](audit-specs/) | Execute canonical steps and retain actual local application evidence. |
| Audit capture | [audit fixture](support/audit-fixture.ts) | Save each executed canonical step with a fresh screenshot. |

The catalog references POM operations and shared UI contracts.
It contains no selector implementation or dynamic code evaluation.
Runtime inspections report target counts, visibility, enabled state, and mismatch reasons.
Actions require a unique visible target before interaction.
POM methods also check the containing scope.

## Setup

Use Node 22.12+ or Node 24 and the exact root lockfile.
See [setup](../docs/SETUP.md#root-playwright-pom-harness) for connected and offline installation.
See [dependency analysis](../docs/DEPENDENCIES.md#root-playwright-pom-harness) for versions and download hosts.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run e2e:check
```

The npm scripts initialize browser paths before Playwright loads.
The default browser uses existing full Chromium assets under `adapters/browser/.browsers`.
An explicit `PLAYWRIGHT_BROWSERS_PATH` overrides that location.
Set `E2E_BROWSER=msedge` to select installed Edge.
Set `E2E_HEADED=1` to show the browser.
Startup never installs browsers or checks for updates.

## Discovery and execution

Run these commands from the source root:

```sh
# List action metadata without contacting an application.
npm run e2e:ai -- actions list

# Check source contracts and canonical bindings without launching a browser.
npm run e2e:ai -- validate

# Inspect the deterministic local fixture.
npm run e2e:ai -- inspect --fixture --area portal

# Complete one registered UI click. Authentication remains unverified.
npm run e2e:ai -- action session.extend --fixture --allow-session-change

# Check the synthetic renewal and independent authentication predicates.
npm run e2e:ai -- run session-extension --fixture --allow-session-change

# Inspect, run, and inspect again in one context.
npm run e2e:ai -- sequence --fixture --allow-session-change --steps-file e2e/ai/session-extension.sequence.json
```

Each separate invocation creates a fresh browser context.
Use [the sequence file](ai/session-extension.sequence.json) for dependent operations.
Sequence steps support `inspect`, `validate`, `action`, and `run` only.
Unknown operations fail before any sequence interaction.
Session operations require the explicit session option.
The option does not establish external-system authorization.

Supported action IDs are `session.extend`, `session.logout`, `portal.avatar.open`, `portal.profile.open`, and `category.create.open`.
The catalog also supports `portal.theme.light` and `portal.theme.dark`.
Category form submission remains outside the dispatcher.
Record-specific Category and workspace operations remain available through their typed POM APIs.

For an authorized application investigation, supply its actual build prefix and explicit URL:

```sh
npm run e2e:ai -- inspect --url http://localhost:3000 --prefix ACTUAL_PREFIX --area portal
npm run e2e:ai -- validate --url http://localhost:3000 --prefix ACTUAL_PREFIX --area category
```

These examples require a running, accessible application.
The runner creates no application server and imports no existing browser profile.
Application authentication and deterministic business fixtures require environment-specific setup through the exported POM APIs.
Missing authentication leaves protected targets unavailable.
Do not insert real credentials into tracked files or command arguments.

`validate` with a target checks the selected area's current DOM state.
A missing or ambiguous area root fails validation.
Absent conditional controls leave validation `unverified` and produce a nonzero exit code.
An inspection can pass while reporting unavailable actions because inspection records state only.
Static validation checks source metadata and bindings; it does not establish runtime compatibility.

## Session assertions

The real expiration dialog is named `Your session has been expired`.
Its buttons are `Extend` and `Logout`.
The illustrative proposal labels were replaced with these inspected identities.
Accessibility capture uses `page.locator('body').ariaSnapshot()`.

The [session flow](flows/session-extension.flow.ts) checks these separate predicates:

1. The expiration dialog is absent after activation.
2. Exactly one relogin POST occurs within the observation window.
3. The relogin header matches an independently observed refresh credential fingerprint.
4. Renewal returns HTTP 200 and an access credential.
5. The installed access credential matches the renewal response.
6. The requested workspace remains visible.
7. A controlled validation POST sends the installed access credential.
8. That response returns HTTP 200 and `result: true`.

The flow uses the actual service path and JSON field from [the MFE service](../repos/ui/mfe-base/src/services/index.ts).
It reports hashes for observed credentials.
Dialog closure alone never sets `sessionValid: true`.
The validation result establishes portal authentication only.
It does not establish an extended lifetime or downstream business authorization.
MFE keeps the refresh credential in React state.
The flow does not assume a refresh token exists in browser storage.
Supply `--refresh-sha256` from authorized setup evidence for configured application flows.
Without that evidence, the refresh comparison and overall flow remain `unverified`.
The synthetic fixture supplies its known fingerprint automatically.

The [fixture](fixtures/portal.fixture.ts) opens the warning immediately and holds renewal until release.
It requires no inactivity sleep or external service.
It substitutes a source-shaped DOM and mocked responses for React and BFF execution.
The [AUTH-078 binding](traceability/bindings.json) records remaining setup and execution gaps.

## Evidence and quality checks

CLI fixture commands save `result.json` and `trace.zip` under ignored `e2e/results/<run>/`.
Use `--out PATH` to choose another evidence directory.
Application commands save structured summaries without traces or authentication state.
They omit accessibility text by default.
`--capture-ui` explicitly includes the current accessibility snapshot and discovered control identities.
Such snapshots can contain displayed application data.

Playwright specs retain failure traces, screenshots, and an HTML report in ignored E2E output directories.

Application audits use [audit.config.ts](audit.config.ts) and an explicit `E2E_AUDIT_OUTPUT` directory.
They require the isolated local stack and its disclosed fixtures.
Never reuse a retained output directory.
The audit captures a fresh screenshot after every executed canonical Gherkin step.
It saves the failed step before marking later steps `NOT_EXECUTED`.
Request, storage, persistence, and timing assertions retain separate JSON evidence.
Screenshots establish visible state only.

The [report generator](scripts/summarize-audit.py) shows the latest result first.
Earlier attempts remain in collapsed history with their original evidence.
Report generation does not execute cases or change their outcomes.
Those supplied specs contain synthetic data only.
Keep actual business execution evidence under the owning task.
Do not infer passing business behavior from a passing harness check.

Static validation checks 42 instantiated contracts against exact MFE source bytes and line ranges.
It fails when cited files differ or are unavailable.
The source checker currently expects the registered checkout at `repos/ui/mfe-base`.
Runtime verification remains `unverified` after a source check.
The [traceability checker](scripts/check-traceability.mjs) validates all canonical case hashes and mapped source references.
Its symbol checks establish text presence, not semantic equivalence or code execution.

Runtime coverage is a visible DOM control census for one page state.
It reports identifiable controls and controls matched by a unique visible POM target.
It also reports unmapped and unidentified controls.
The identity heuristic does not compute the complete accessible name.
Hidden states, virtual rows, and iframe contents remain outside the count.
No full-site coverage percentage or deployed UI result is claimed.

Run [the AI skill](ai/SKILL.md) for supported discovery and investigation steps.
See [validation evidence](VALIDATION.md) for the tested platform and remaining limits.

## Screenshot audit runs

The [audit configuration](audit.config.ts) retains named frames, traces, assertions, and per-case results.
Each completed result is saved before the reporter processes another event.
Set `E2E_AUDIT_OUTPUT` to a new directory under the owning task's evidence directory.
The reporter refuses an existing run directory.

```sh
E2E_AUDIT_OUTPUT=tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/harness/new-run node --import tsx --import ./e2e/browser-config.ts node_modules/@playwright/test/cli.js test --config=e2e/audit.config.ts
```

The default suite checks synthetic POM mechanics.
Use `E2E_AUDIT_TEST_DIR=./audit-specs` for the actual frontend investigation suite.
Set `E2E_AUDIT_SCOPE=ACTUAL_APPLICATION_LOCAL_SERVICES` for that suite.
The actual suite requires the documented isolated application on localhost port 8128.
It uses controlled authentication responses and declared browser fixtures.
Clock cases declare emulated time explicitly.
These results do not establish current BFF acceptance or deployment parity.

The [execution stage](../tasks/ui-test-coverage-20261022/execution-stage.md) records authorization and evidence limits.
The [audit report](../tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/report.md) records results and blocked cases.
The [summary script](scripts/summarize-audit.py) creates the portable case ledger and screenshot gallery.
Screenshots establish visible state only.
Use the recorded assertion steps for request, storage, and timing claims.
