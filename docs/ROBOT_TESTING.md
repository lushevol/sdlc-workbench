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
