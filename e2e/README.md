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

The current areas are login, portal navigation, session expiration, Category administration, and the CN cashflow blotter.
The Category page supplies the first representative administration area.
The [cashflow guide](CASHFLOW_BLOTTER.md) maps its search, grid, details, workflow, and generated form controls.
Remote trade and unnet internals need separate runtime inspection.
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

## Select and run tests

Run commands from the Workbench source root.
This guide covers Playwright. Use [Robot testing](../docs/ROBOT_TESTING.md#run-ratan-business-cases-directly) for the independent test engine.

| Target | Command or configuration | Required application |
| --- | --- | --- |
| Synthetic POM tests in `specs/` | `npm run e2e:test` | None; tests use local fixtures. |
| Application cases in `audit-specs/` | `audit.config.ts` with `E2E_AUDIT_TEST_DIR=./audit-specs` | Prepared isolated local stack on port 8128. |
| Named POM actions and flows | `npm run e2e:ai -- ...` | `--fixture` or an explicitly configured application. |

The default test command selects `specs/` only.
`npm run e2e:check` adds type checks and static validation before those fixture tests.
Neither command executes the full canonical business catalog.
If static validation reports `source-bytes-changed`, preserve the diagnostic and compare the cited revision with selected source.
Resolve affected source bindings before claiming current-source support. Fixture passes do not resolve a stale source contract.

```sh
# Discover current fixture tests without executing assertions.
npm run e2e:test -- --list --reporter=line

# Run all default fixture tests.
npm run e2e:test

# Run one file, or one matching case with a visible browser.
npm run e2e:test -- session-extension.spec.ts
E2E_HEADED=1 npm run e2e:test -- --grep 'AUTH-078' --workers=1

# Select and trigger tests interactively.
E2E_HEADED=1 npm run e2e:test -- --ui

# Open the default HTML report.
node node_modules/@playwright/test/cli.js show-report e2e/playwright-report
```

Failure artifacts use `e2e/test-results/`.
Preserve required outputs before another default execution replaces them.
Use the [audit configuration](#screenshot-audit-runs) when durable per-case evidence is required.

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

Capture preparatory states before a setup helper replaces them with the asserted state.
Wait for the specific UI content required by the step before capture.
For multiple pages, use `audit.labelPage(page, label)` and the `audit.step` capture options.
Set `targetPage` to the page that performs the action or displays the asserted state.
Use `audit.observePage` for safe nonvisual context before and after each screenshot.
Session timing observations include the controlled clock, cutoff, and button state without credential values.
An unchanged screen can correctly produce identical image bytes across several steps.
Use these observations to explain nonvisual changes without altering application pixels.

The [report generator](scripts/summarize-audit.py) shows the latest result first.
Earlier attempts remain in collapsed history with their original evidence.
Report generation does not execute cases or change their outcomes.
`COMPLETE` measures step screenshot bindings only.
`CONTEXT_RECORDED` means machine capture observations exist. It does not establish human visual review.
The gallery identifies captured pages and repeated image bytes separately from local execution outcomes.
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
The reporter refuses an output that already contains a run.

```sh
E2E_AUDIT_TEST_DIR=./specs E2E_AUDIT_SCOPE=SYNTHETIC_HARNESS \
  E2E_AUDIT_OUTPUT="tasks/ui-test-coverage-20261022/evidence/manual-execution/harness-$(date -u +%Y%m%dT%H%M%S)" \
  node --import tsx --import ./e2e/browser-config.ts \
  node_modules/@playwright/test/cli.js test --config=e2e/audit.config.ts
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

### Prepare the local application stack

The [launcher](scripts/local-audit-stack.py) starts existing service commands from a private JSON configuration.
It does not build application source or install missing dependencies.
Check each service's working directory, command, ports, and readiness URLs before launch.
Record the selected application revisions, build hashes, and disclosed substitutions under the owning task.
Verify actual build identities separately. Configuration `sourceBindings` do not enforce or prove those identities.

This checkout can use `.workbench/ui-audit-stack-attempt03.json` as a prepared configuration template.
It references saved application builds and machine-specific dependencies.
Those builds can differ from the current repository revisions.
Prepare matching builds and service configuration when the requested revision differs.
Another machine needs its own prepared service configuration.

Both the launcher's evidence directory and `runtimeDirectory` must be new.
The following commands copy the prepared configuration and select a fresh runtime directory:

```sh
export E2E_RUN_ID="$(date -u +%Y%m%dT%H%M%S)"
export E2E_STACK_TEMPLATE=.workbench/ui-audit-stack-attempt03.json
export E2E_STACK_CONFIG=".workbench/ui-audit-$E2E_RUN_ID/stack.json"

python3 - <<'PY'
from pathlib import Path
import json
import os

source = Path(os.environ['E2E_STACK_TEMPLATE']).resolve()
target = Path(os.environ['E2E_STACK_CONFIG']).resolve()
config = json.loads(source.read_text())
target.parent.mkdir(parents=True, exist_ok=False)
config['runtimeDirectory'] = str(target.parent / 'runtime')
target.write_text(json.dumps(config, indent=2) + '\n')
PY

python3 e2e/scripts/local-audit-stack.py \
  --config "$E2E_STACK_CONFIG" \
  --output "tasks/ui-test-coverage-20261022/evidence/manual-execution/stack-$E2E_RUN_ID"
```

Replace the task evidence path when another task owns execution.
Keep the launcher terminal open. Wait for its `RUNNING` message before application tests start.
The prepared configuration checks ports 8122, 8124, 8125, 8128, and 8129.
The launcher refuses occupied ports. Inspect ownership before stopping or reusing any existing service.
After testing, press Ctrl+C in the launcher terminal to stop its owned service groups.
Retain `stack-lifecycle.json`, startup failures, and cleanup results.

### Trigger application audit cases

Open another terminal at the Workbench source root.
Set the application directory and execution scope explicitly.
Selecting `audit.config.ts` alone still selects synthetic fixture tests.

```sh
export E2E_AUDIT_TEST_DIR=./audit-specs
export E2E_AUDIT_SCOPE=ACTUAL_APPLICATION_LOCAL_SERVICES

# List application cases without starting browsers or the audit evidence reporter.
node --import tsx --import ./e2e/browser-config.ts \
  node_modules/@playwright/test/cli.js test \
  --config=e2e/audit.config.ts --list --reporter=line

# Use a new task evidence directory before every execution.
export E2E_AUDIT_OUTPUT="tasks/ui-test-coverage-20261022/evidence/manual-execution/application-$(date -u +%Y%m%dT%H%M%S)"

# Execute one named case with a visible browser.
E2E_HEADED=1 node --import tsx --import ./e2e/browser-config.ts \
  node_modules/@playwright/test/cli.js test \
  --config=e2e/audit.config.ts login-environment.spec.ts \
  --grep 'AUTH-001 ' --workers=1

# Open the selected run's report.
node node_modules/@playwright/test/cli.js show-report "$E2E_AUDIT_OUTPUT/html-report"
```

Replace the filename and `--grep` value for another case.
Remove both selectors to execute all discovered application tests within the requested scope.
Refresh `E2E_AUDIT_OUTPUT` before each execution.
Use [setup](../docs/SETUP.md#root-playwright-pom-harness) for optional Firefox and WebKit compatibility assets.
`E2E_COMPAT_BROWSER` affects the compatibility audit only.

The output contains `run-inputs.json`, `playwright-report.json`, `html-report/`, source snapshots, and per-case `cases/` evidence.
Inspect each case's assertions and retained result before reporting verified behavior.
Report passes, failures, skips, blocked cases, and partial execution separately.
Discovery and a zero process exit code do not establish that every canonical case passed.

## Ask AI to execute cases

Name the runner, case IDs or suite, target environment, application revision, and owning task.
Use existing task authorization and configuration when available.
The agent must investigate missing inputs before asking for clarification.
Material missing target details can block execution after that investigation.

Example request for fixtures:

> Read `e2e/README.md`. Run the root fixture tests with existing Chromium assets.
> Retain per-case evidence under the owning task. Report assertion results and execution limits.

For durable fixture evidence, select `audit.config.ts`, `E2E_AUDIT_TEST_DIR=./specs`, and `E2E_AUDIT_SCOPE=SYNTHETIC_HARNESS`.
Set a new `E2E_AUDIT_OUTPUT` under the owning task before execution.

Example request for application cases:

> Read `e2e/README.md`. Run `AUTH-001` against the prepared local application stack for `ui-test-coverage-20261022`.
> Confirm the selected application build identities first. Retain each completed case before continuing.
> Report failures, skips, blocked cases, substitutions, and cleanup results.

Inspect the current worktree and preserve unrelated changes before execution.
Bind results to exact test, application, configuration, and environment identities.
Keep failed assertions and unavailable prerequisites visible.
Execution evidence does not establish business acceptance or deployment authorization.
