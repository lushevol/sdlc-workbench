---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Robot testing

The Workbench can execute registered Robot Framework suites through `testing.robot`.
CLI and MCP use the same provider, grants, and retained action records.
ADE refers to this Workbench integration in the Ratan setup instructions.
The test repository keeps its independent source, dependencies, and Git history.

## Configure a resource

Install Robot Framework in the test repository's Python environment.
The Workbench runtime does not require Robot Framework as a package dependency.
Register named suites in `registry/tools.yaml`.

```yaml
schema_version: 1
tools:
  - id: ratan-test-engine
    kind: testing
    provider: testing.robot
    environment: local-offline
    config:
      path: repos/testing/ratan-test-engine
      python: .venv/bin/python
      suites:
        offline-smoke: Tests/workbench/offline.robot
    allowed_operations: [list, run]
```

Merge this entry with existing tools.
Resource IDs must remain unique.
On Windows, set `python` to `.venv/Scripts/python.exe`.
An absolute interpreter path is also supported.

Relative interpreter and suite paths resolve from the configured repository directory.
Repository metadata overrides do not change this executable path.
Suite paths must remain inside the configured repository.

`list` returns configured suites without importing Robot or project libraries.
`run` accepts a suite name and an optional `dry_run` Boolean.
It does not accept arbitrary commands, listeners, variables, or Robot options.

The optional `variable_files` configuration accepts local YAML files for private environment inputs.
Relative variable file paths resolve from the repository directory.
Absolute variable file paths can select existing private configuration.
The provider passes file paths to Robot without reading their contents.
Do not store credential values in tool catalogs.

Granting `run` permits every suite in this resource.
Create separate resources when suites need separate execution grants.

Workspace `timeout_seconds` supports one second through 3600 seconds.
The default remains 30 seconds.
Use a separate scoped workspace for long session scenarios.
For example, a 960-second prompt check needs an explicitly configured timeout above 960 seconds.
An 1800-second timeout permits that check without changing the main workspace's timeout.

## Execute and inspect evidence

```sh
ai-sdlc --workspace PATH call ratan-test-engine list
ai-sdlc --workspace PATH call ratan-test-engine run --args '{"suite":"offline-smoke"}'
ai-sdlc --workspace PATH call ratan-test-engine run --args '{"suite":"offline-smoke","dry_run":true}'
ai-sdlc --workspace PATH runs
ai-sdlc --workspace PATH run ACTION_ID
```

Each action keeps stdout, stderr, native Robot files, and normalized test results.
The files remain inside `.workbench/runs/ACTION_ID/` with recorded hashes.
Results keep `PASS`, `FAIL`, and `SKIP` separate.
Malformed or missing Robot output fails the action.
Timeouts retain available output and fail the action.

Source identity records the local Git revision and checkout state when available.
An unknown revision remains an evidence limit.

A dry run checks Robot execution structure and can import project libraries.
It does not execute keyword assertions.
Skipped tests supply no passing assertion evidence.
Passing tests require assertion inspection before any business verification claim.
The provider does not map tests to approved requirements or authenticate execution.

Native reports can contain sensitive test data.
Keep action evidence local under the workspace retention rules.

## Ratan source checkout

This source checkout registers three Ratan resources.
Generated workspaces start with empty tool catalogs.

| Resource | Current use |
| --- | --- |
| `ratan-test-engine` | Execute the isolated framework smoke suite and retain Robot evidence. |
| `ratan-test-engine-checks` | Run package checks, inventory, `unit`, smoke parsing, and diagnostic `parse-all`. |
| `ratan-test-engine-repository` | Inspect independent Git status and diffs. |

Use the Ratan repository's `docs/WORKBENCH.md` for dependency setup and local checks.
The offline smoke suite uses BuiltIn keywords and contains no business coverage claim.
Live Ratan suites require private configuration, credentials, keys, and a selected test environment.
Their setup and execution remain separate from the offline resource.
Use the [root E2E guide](../e2e/README.md#select-and-run-tests) for Playwright fixture and application audit cases.

Use an ignored YAML variable file for required Robot bootstrap variables, including `ENV`, `SECRET`, and `LANG`.
Register that file through `config.variable_files` when you configure a separate live resource.
The `SECRET` variable identifies configuration; it does not replace credential storage.

```sh
ai-sdlc --workspace PATH call ratan-test-engine-checks run --args '{"suite":"doctor"}'
ai-sdlc --workspace PATH call ratan-test-engine-checks run --args '{"suite":"doctor-full"}'
ai-sdlc --workspace PATH call ratan-test-engine-checks run --args '{"suite":"inventory"}'
ai-sdlc --workspace PATH call ratan-test-engine-checks run --args '{"suite":"parse"}'
ai-sdlc --workspace PATH call ratan-test-engine-checks run --args '{"suite":"unit"}'
ai-sdlc --workspace PATH call ratan-test-engine-repository status
```

The `parse` check selects the isolated smoke source.
`doctor-full` checks every declared direct package version.
The diagnostic `parse-all` check selects legacy Robot sources and can fail on existing syntax defects.
Its failed action retains diagnostics for investigation.

## Run Ratan business cases directly

Use direct Robot execution for business cases absent from the registered resource.
The current `ratan-test-engine` resource exposes `offline-smoke` only.
It does not expose the hand-written session suite or generated business suites.
The provider also cannot accept arbitrary case-selection options.

Run these commands from the Workbench source root:

```sh
cd repos/testing/ratan-test-engine

# Prepare dependencies and browser assets only when needed.
uv sync --locked --python 3.13
.venv/bin/rfbrowser init

# Check packages and parse the session suite without executing business assertions.
.venv/bin/python scripts/workbench.py doctor --profile full
.venv/bin/python scripts/workbench.py parse Tests/ratan/plugin/ui/session/session_renewal.robot

# Create private session configuration once; preserve an existing configuration.
mkdir -p .workbench/session-renewal
cp -n Tests/ratan/plugin/ui/session/config.example.json .workbench/session-renewal/config.json
```

Browser initialization can download assets. Runtime startup does not install browsers.
Edit the copied configuration before execution.
Confirm target URL, selectors, full application revisions, and independently supported token lifetimes.
The example's port 8003 and 900-second access lifetime are replaceable inputs.
Supply `SESSION_E2E_USERNAME` and `SESSION_E2E_PASSWORD` through private process environment variables.
Keep credential values outside tracked files and command arguments.
Start the selected portal and authentication service separately.

Use the test repository's Python environment for the session suite:

```sh
# Execute one stable case ID.
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-001 \
  --include E2E-15 \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot

# Execute the short batch in a separate output directory.
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-002 \
  --exclude long-running --exclude diagnostic \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot

# Execute one expiry case with explicit long-running opt-in.
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/robot-run-003 \
  --include E2E-04 \
  --variable SESSION_ALLOW_LONG_RUNNING:True \
  --variable SESSION_CONFIG:.workbench/session-renewal/config.json \
  Tests/ratan/plugin/ui/session/session_renewal.robot
```

Use a fresh Robot output directory and configuration `artifactDir` for each run.
The default session browser is installed Edge with a visible window.
Expiry cases wait for real time and can take hours.
Missing long-running opt-in skips gated cases. A skip supplies no passing assertion evidence.
Use `--include diagnostic` separately for diagnostic cases.

Generated business UI and API suites use private environment YAML, certificates, keys, and selected test data.
Match `ENV`, `SECRET`, and `LANG` to that configuration.
Some cases create records or change business state.
This command selects one existing HOLD case; its environment identifiers are examples:

```sh
.venv/bin/python -m robot \
  --outputdir .workbench/business-ui/run-001 \
  --variable ENV:uat2 --variable SECRET:secret --variable LANG:0 \
  --test "CN-UI-E2E-HOLD-OO1-OO1" \
  Tests/ratan/workspace/ui/CN-UI-E2E-HOLD.robot
```

Replace the suite path and test name to select another supported business case.
Omit `--test` to execute the full selected file. Use `--include TAG` for tag selection.
Executing existing suites does not require workbook generation or report-upload utilities.

Open `report.html` or `log.html` under the selected Robot output directory.
Retain `output.xml`, the command, exit code, configuration hash, application revisions, and test source hashes.
The session `artifactDir` contains case JSON and screenshots.
Save each completed case immediately under the owning task's evidence rules.
Review private data before moving local artifacts into retained task evidence.
Inspect the assertions and matching results before reporting verified behavior.

Repository guides provide the current source-specific details:

- [Session execution and case map](../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#execution).
- [Dependency setup and generated-suite workflow](../repos/testing/ratan-test-engine/docs/WORKBENCH.md).
- [Native `RW-*` browser observations](../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/README.md#execute-cases).

### Select a named session environment

The session suite accepts complete configurations under an `environments` mapping.
Each entry supplies its own target URL, credentials' environment-variable names, selectors, timing expectations, and source revisions.
The [named example](../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/config.environments.example.json) includes nonproduction and production placeholders.
Run these commands from the test repository root:

```sh
mkdir -p .workbench/session-renewal
cp -n Tests/ratan/plugin/ui/session/config.environments.example.json .workbench/session-renewal/environments.json

# Edit complete profiles before execution.
.venv/bin/python -m robot \
  --outputdir .workbench/session-renewal/nonprod-run-001 \
  --include E2E-15 \
  --variable SESSION_CONFIG:.workbench/session-renewal/environments.json \
  --variable SESSION_ENVIRONMENT:nonprod \
  Tests/ratan/plugin/ui/session/session_renewal.robot
```

Select `SESSION_ENVIRONMENT:prod` for the configured production entry.
The name does not supply an actual URL or credentials. Replace all example placeholders first.
Missing or unknown selection fails before target navigation.
Existing single-target configuration files remain supported without `SESSION_ENVIRONMENT`.
Results record the selected environment, target, and effective configuration hash.
The native runner accepts `--environment NAME` with its own named configuration file.
See [native target selection](../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/README.md) for examples and remote mode.

Generated UI and API suites continue to select private environment YAML through `ENV`, `SECRET`, and `LANG`.
Their selected YAML determines actual service URLs and environment data.
The root [deployed Playwright checks](../e2e/README.md#select-a-target-environment) use their own UI profiles and saved authentication state.

### Ask AI to execute Robot cases

Name the selected cases, target environment, configuration path, application revision, and owning task.
Use existing task authorization and prepared configuration where available.
Investigate missing inputs before asking for clarification.
Do not substitute the offline smoke suite for requested business verification.

Example request:

> Read `docs/ROBOT_TESTING.md` and the test repository's session guide.
> Run `E2E-15` against the configured portal using its private session configuration.
> Use the named task's evidence directory. Confirm the application revisions and timing profile first.
> Retain each completed case. Report assertions, failures, skips, setup blockers, and execution limits separately.

## Integration acceptance criteria

```gherkin
Scenario: Retain an offline Robot execution
  Given the registered offline suite and its Python environment exist
  When an agent runs the offline suite through Workbench
  Then the action records the Robot exit code
  And the action retains output.xml with a SHA-256 hash
  And each test keeps its PASS, FAIL, or SKIP status

Scenario: Reject an unregistered suite
  Given a testing resource grants run
  When an agent selects a suite absent from its configuration
  Then the action fails
  And no Robot process starts

Scenario: Preserve the dry-run evidence limit
  Given the registered suite exists
  When an agent requests dry_run true
  Then the result identifies dry-run execution
  And the result states that assertions were not executed
```
