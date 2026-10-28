# Manual E2E run walkthrough

No critical conclusions require user attention or action.

The [user request](user-input.txt) is the high-priority source for this inquiry.
The user requests manual trigger instructions for the test engine and E2E folder.
These instructions cover terminal commands on the current macOS checkout.
No business cases were executed for this walkthrough.

## Choose the runner

| Location | Runner | Selection | Execution boundary |
| --- | --- | --- | --- |
| `repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/` | Robot Framework and Browser | `--include E2E-15` | 22 session cases against configured services. |
| `repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/` | Robot Framework | Suite, test name, or tag | Generated business suites need private environment configuration. |
| `e2e/specs/` | Playwright | File or `--grep` | 46 synthetic harness tests in five files. |
| `e2e/audit-specs/` | Playwright audit configuration | File or `--grep` | 501 discovered local application tests in 31 files. |

Discovery counts describe the current source. They do not establish passing behavior or complete business coverage.
See [test-engine inspection](test-engine-inspection.md) for source locators and hashes.
See [inspection records](inspection.json) for root source identities and performed checks.

## Run the test-engine session cases

Use the test engine's own environment. Its canonical setup uses Python 3.13 and uv.
The [setup guide](../../../../repos/testing/ratan-test-engine/docs/WORKBENCH.md#isolated-setup) defines the locked profile.

```sh
cd /Users/lushevol/code/github/ratan-release-impact/workbench/repos/testing/ratan-test-engine

# First-time dependency setup, when needed.
uv sync --locked --python 3.13

# Initialize Browser assets only when they are unavailable.
.venv/bin/rfbrowser init

# Check dependencies and parse the selected suite without executing it.
.venv/bin/python scripts/workbench.py doctor --profile full
.venv/bin/python scripts/workbench.py parse Tests/ratan/plugin/ui/session/session_renewal.robot
```

Browser initialization can download assets. Test startup does not install them.
The [suite](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L8) defaults to installed Edge and a visible window.

Create the private session configuration once:

```sh
mkdir -p .workbench/session-renewal
cp -n Tests/ratan/plugin/ui/session/config.example.json .workbench/session-renewal/config.json
```

Edit that configuration before execution. Inspect `targetUrl`, selectors, source revisions, and the expected token lifetime.
The example URL uses port 8003. Its 900-second access lifetime is an example assertion input.
Set both values from the selected target's evidence.
Set `artifactDir` to a fresh directory for each run.
Supply `SESSION_E2E_USERNAME` and `SESSION_E2E_PASSWORD` through your private process environment.
Start the portal and its authentication service before executing cases.
The Robot command does not start those services.

Run one short case:

```sh
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-001 \
  --include E2E-15 \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot
```

Replace `E2E-15` with the required case tag.
Robot also supports `--test "exact test name"`.
The [case map](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#case-map-and-assertion-limits) links IDs, names, and assertions.

Run the short batch:

```sh
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-002 \
  --exclude long-running --exclude diagnostic \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot
```

Expiry cases require explicit opt-in. They wait for real expiry and can take hours.
Keep visibility cases in a visible browser.

```sh
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-003 \
  --exclude diagnostic \
  --variable SESSION_ALLOW_LONG_RUNNING:True \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot
```

This command includes short and long cases. Add `--include E2E-04` to select one expiry case.
Keep diagnostic cases separate through `--include diagnostic`.
Selecting a case does not bypass its setup or timing gate.

Open `report.html` or `log.html` in the selected Robot output directory.
Robot also writes `output.xml` there.
The configured `artifactDir` holds case JSON and screenshots.
See [session execution](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#execution) for the full procedure.

## Run other test-engine suites

Generated UI and API suites use different configuration from the hand-written session suite.
They import private `env_${ENV}_${SECRET}.yaml` files.
Use the correct environment, certificate, account, and test data for the chosen case.
Some cases create records or change business state.

This example selects one existing HOLD case. Replace the environment identifiers with your configured values.

```sh
.venv/bin/python -m robot \
  --outputdir .workbench/business-ui/run-001 \
  --variable ENV:uat2 --variable SECRET:secret --variable LANG:0 \
  --test "CN-UI-E2E-HOLD-OO1-OO1" \
  Tests/ratan/workspace/ui/CN-UI-E2E-HOLD.robot
```

Replace the suite path to run another UI or API file.
Omit `--test` to run every case in that file.
Use `--include TAG` for tag selection.
Running existing suites does not require workbook regeneration or report-upload utilities.
The [engine inspection](test-engine-inspection.md) links the import paths and selected case.

The Workbench `ratan-test-engine` resource currently registers only `offline-smoke`.
That wrapper does not expose these business suites.
Use the direct Robot commands above for those suites.

Native `RW-*` observations use a separate Node runner.
Use their [configuration and execution guide](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/README.md#execute-cases).

## Run the root E2E fixture tests

Return to the Workbench root. Use Node 22.12+ or Node 24.
The [setup guide](../../../../docs/SETUP.md#root-playwright-pom-harness) covers connected and offline installation.

```sh
cd /Users/lushevol/code/github/ratan-release-impact/workbench

# First-time package setup, when needed.
npm ci --ignore-scripts --no-audit --no-fund

# Provision Chromium only when matching browser assets are unavailable.
PLAYWRIGHT_BROWSERS_PATH="$PWD/adapters/browser/.browsers" \
  node node_modules/@playwright/test/cli.js install chromium --no-shell

# Discover tests without executing them.
npm run e2e:test -- --list

# Run all default fixture tests.
npm run e2e:test

# Run one file.
npm run e2e:test -- session-extension.spec.ts

# Run one matching test with a visible browser.
E2E_HEADED=1 npm run e2e:test -- --grep 'AUTH-078' --workers=1

# Open the interactive Playwright test picker.
E2E_HEADED=1 npm run e2e:test -- --ui

# Run type checks, static bindings, and all default fixture tests.
npm run e2e:check
```

Use `E2E_BROWSER=msedge` to select installed Edge instead of provisioned Chromium.
These fixture tests do not require a running portal.
The [default configuration](../../../../e2e/playwright.config.ts#L6) selects `e2e/specs/` only.
It does not select `e2e/audit-specs/`.

Open the default HTML report with:

```sh
node node_modules/@playwright/test/cli.js show-report e2e/playwright-report
```

Failure artifacts are under `e2e/test-results/`.
Preserve required outputs before another default run replaces them.

## Run the root application audit cases

These cases require the prepared isolated local application at `http://localhost:8128`.
Several suites also require the local BFF and module servers.
They use disclosed service fixtures and controlled clocks where their definitions specify them.
Their results do not establish deployed environment parity.

The current machine has `.workbench/ui-audit-stack-attempt03.json` and its prepared service entry points.
That configuration uses saved application builds. It does not build or select today's repository HEAD automatically.
Its old runtime directory already exists. The launcher requires a fresh runtime directory.

To rerun that prepared local stack, create a configuration copy with a new runtime directory:

```sh
cd /Users/lushevol/code/github/ratan-release-impact/workbench
python3 - <<'PY'
from datetime import datetime, timezone
from pathlib import Path
import json

root = Path.cwd()
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
config = json.loads((root / '.workbench/ui-audit-stack-attempt03.json').read_text())
config['runtimeDirectory'] = str(root / '.workbench' / ('manual-ui-runtime-' + stamp))
target = root / '.workbench/manual-ui-stack.json'
target.write_text(json.dumps(config, indent=2) + '\n')
print(target)
PY

python3 e2e/scripts/local-audit-stack.py \
  --config .workbench/manual-ui-stack.json \
  --output "tasks/ui-test-coverage-20261022/evidence/manual-run-20261028/stack-$(date -u +%Y%m%dT%H%M%S)"
```

Keep this terminal running. Wait for the launcher's `RUNNING` message.
It checks readiness on ports 8122, 8124, 8125, 8128, and 8129.
It refuses occupied ports. Stop an existing owned stack before starting another.
This preparation copies configuration only. It does not recreate missing builds on another machine.
Update the service configuration and source bindings when a different application revision is required.

In a second terminal, select the application suite and a fresh output directory:

```sh
cd /Users/lushevol/code/github/ratan-release-impact/workbench
export E2E_AUDIT_TEST_DIR=./audit-specs
export E2E_AUDIT_SCOPE=ACTUAL_APPLICATION_LOCAL_SERVICES

# List application cases. This does not need the stack to be running.
node --import tsx --import ./e2e/browser-config.ts \
  node_modules/@playwright/test/cli.js test \
  --config=e2e/audit.config.ts --list --reporter=line

# Choose a fresh directory for each execution.
export E2E_AUDIT_OUTPUT="tasks/ui-test-coverage-20261022/evidence/manual-run-20261028/application-$(date -u +%Y%m%dT%H%M%S)"

# Run one case with a visible browser.
E2E_HEADED=1 node --import tsx --import ./e2e/browser-config.ts \
  node_modules/@playwright/test/cli.js test \
  --config=e2e/audit.config.ts login-environment.spec.ts \
  --grep 'AUTH-001 ' --workers=1

# Open that run's report.
node node_modules/@playwright/test/cli.js show-report "$E2E_AUDIT_OUTPUT/html-report"
```

Remove the file and `--grep` arguments to run all discovered application tests.
Keep `--workers=1` for a simple manual investigation.
Compatibility cases also require their selected Firefox or WebKit assets.
Use a new `E2E_AUDIT_OUTPUT` before every execution.
The audit reporter rejects an output that already contains a run.
After execution, press Ctrl+C in the stack terminal to stop its owned services.

Audit outputs include `html-report/`, `playwright-report.json`, source snapshots, and per-case evidence under `cases/`.
Each completed case saves its result before the next reporter event.
See [audit instructions](../../../../e2e/README.md#screenshot-audit-runs) and [audit configuration](../../../../e2e/audit.config.ts#L12).

## Confidence and limits

Command selection has high confidence from current configuration, suite declarations, and successful Playwright discovery.
Service startup remains unverified in this inquiry.
File existence does not establish successful compilation, readiness, authentication, or passing business assertions.
The Workbench CLI is available at `.venv/bin/ai-sdlc`, although it is absent from the current shell PATH.
No local knowledge resource is registered. Direct source inspection supplied the command evidence.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
