# Dependency setup maintenance

**Setup now diagnoses missing dependencies before installation. Run the existing setup launcher to install them.**

Owner: Workbench maintainer.
Next action: use the [setup commands](#commands), then configure only selected optional integrations.
The [full suite](unit-tests.log) passed 831 tests with zero failures, errors, or skips.
The [verification summary](verification-summary.json) records candidate source hashes and retained checks.
Native Windows and live service access remain unverified.

## Scope and authority

[The preserved user input](user-input.md) defines this maintenance scope.
The baseline execution records its exact Git revision in [the original result](fresh-checkout-baseline.json).
Unrelated README, task assets, and untracked source changes remain outside this stage.
No package dependency was added.

The inspected callers are setup launchers, bootstrap check/install branches, offline setup, and bootstrap regression tests.
The affected symbols are [bootstrap diagnosis](../../../core/bootstrap.py#L94-L143) and [argument handling](../../../core/bootstrap.py#L278-L310).
Both check and post-install paths call diagnosis.
Change risk is moderate because fallback could otherwise mistake launcher packages for completed project installation.
Fallback therefore forces project readiness to `INCOMPLETE`.

## Commands

Run these commands from the source checkout.

| Action | macOS | Windows PowerShell |
| --- | --- | --- |
| Install full dependencies and report remaining prerequisites | `./setup.command` | `.\setup.cmd` |
| Install Python core only | `./setup.command --core-only` | `.\setup.cmd --core-only` |
| List missing prerequisites without installation | `./setup.command --check` | `.\setup.cmd --check` |
| Return structured diagnostics | `./setup.command --check --json` | `.\setup.cmd --check --json` |
| Check core prerequisites only | `./setup.command --check --core-only` | `.\setup.cmd --check --core-only` |

Python can also invoke the shared implementation: `python3 core/bootstrap.py --check --json`.
Use an approved Python `>=3.10` interpreter.
The [setup guide](../../../docs/SETUP.md#start-setup) covers matching offline bundles and external workspace selection.
Generated workspaces use an installed runtime and a separate source checkout for setup.

## Behavior change and retained comparison

### Setup

Use a fresh source fixture and an isolated launcher Python without third-party packages.
Keep `.venv`, `.env`, and `.workbench` absent.
Source paths include spaces.

### Steps

1. Run `core/bootstrap.py --check --core-only` through the isolated launcher.
2. Inspect its exit status, missing package output, and setup state.
3. Repeat with `--json`, then with the full diagnostic profile.
4. Create an empty project virtual environment and repeat diagnosis before installing Workbench.

### Intended result

List missing prerequisites, required versions, and next actions.
Exit nonzero while installation is incomplete.
Keep credential values out of output and create no setup state.

### Old result

Diagnosis stopped at the missing project environment.
It did not list missing Python packages.
Evidence: [baseline execution](fresh-checkout-baseline.json).

### New result

Diagnosis lists all five missing core packages and their required versions.
JSON identifies source fallback and its diagnostic interpreter.
The project remains `INCOMPLETE`, including when launcher packages are available.
The probe also checks an existing virtual environment without an installed Workbench.
Evidence: [text result](fresh-checkout-candidate.json), [core JSON](fresh-checkout-json.json), [full JSON](fresh-checkout-all-json.json), and [missing runtime](missing-installed-runtime.json).
[The probe](probe-setup.py) saves each completed case and asserts unchanged source files and absent setup state.

## Maintenance acceptance and canonical cases

These criteria define this harness change. They do not represent business acceptance or live integration approval.

### AC1 and TC1: Diagnose an incomplete project installation

```gherkin
Scenario Outline: Diagnose missing project installation prerequisites
  Given the source checkout has <condition>
  When the user runs setup with --check
  Then the output lists missing prerequisites and concrete next actions
  And the project readiness is INCOMPLETE
  And the exit status is 1

  Examples:
    | condition                              |
    | no project virtual environment         |
    | no Workbench in the project environment |
    | an unusable project Python             |
```

### AC2 and TC2: Return structured checks without installation

```gherkin
Scenario: Diagnose a fresh checkout through JSON
  Given a fresh checkout and a launcher without third-party packages
  When the user runs setup with --check --json
  Then stdout contains a JSON object with feature checks and next actions
  And each missing core package has a required version
  And no environment, configuration, or setup state is created
  And credential values are absent from stdout and stderr

Scenario: Reject JSON installation mode
  When the user runs setup with --json without --check
  Then the exit status is 2
  And no installer runs
```

### AC3 and TC3: Keep dependency setup and diagnosis current

```gherkin
Scenario: Validate diagnostic coverage for declared runtime dependencies
  Given the core, Release Clinic, and root Node dependency declarations
  When the maintenance regression runs
  Then diagnostic Python names and constraints match the declared core and Clinic requirements
  And every root Node runtime dependency has a diagnostic presence check
```

The [project rule](../../../AGENTS.md#dependency-maintenance) also covers component-specific tools, services, platforms, manifests, locks, offline preparation, and tests.
The [principle](../../../PRINCIPLE.md#7-local-first-minimal-dependencies) retains this obligation for future changes.
New components still require source inspection for prerequisites outside the tracked package groups.

## Traceability

The denominators cover three derived maintenance criteria and three changed verification units.
The units are bootstrap diagnosis, check argument handling, and declaration coverage regression.
Installation commands and offline preparation are required unchanged behavior.
Rules and documentation are supporting maintenance.
Link completeness does not establish universal setup compatibility.

### AC-to-test coverage

| Criterion | Canonical case and inspected assertions | Execution |
| --- | --- | --- |
| [AC1](#ac1-and-tc1-diagnose-an-incomplete-project-installation) | [TC1](#ac1-and-tc1-diagnose-an-incomplete-project-installation); [fallback assertions](../../../tests/test_bootstrap.py#L518-L565) | [Passing suite](unit-tests.log); [retained probe](missing-installed-runtime.json) |
| [AC2](#ac2-and-tc2-return-structured-checks-without-installation) | [TC2](#ac2-and-tc2-return-structured-checks-without-installation); [read-only JSON assertions](../../../tests/test_bootstrap.py#L567-L599) | [Passing suite](unit-tests.log); [retained JSON probe](fresh-checkout-json.json) |
| [AC3](#ac3-and-tc3-keep-dependency-setup-and-diagnosis-current) | [TC3](#ac3-and-tc3-keep-dependency-setup-and-diagnosis-current); [declaration assertions](../../../tests/test_doctor.py#L22-L43) | [Passing suite](unit-tests.log) |

Definition and inspected-assertion links: 3 of 3 criteria.
Passing execution covers the declared local assertions. Live installation conformance remains outside this denominator.

### AC-to-code-change coverage

| Criterion | Changed unit or supporting rule | Scope |
| --- | --- | --- |
| [AC1](#ac1-and-tc1-diagnose-an-incomplete-project-installation) | [Bootstrap diagnosis](../../../core/bootstrap.py#L94-L143) | Source fallback and forced incomplete target status. |
| [AC2](#ac2-and-tc2-return-structured-checks-without-installation) | [Check argument handling](../../../core/bootstrap.py#L278-L310) | JSON output and rejection before installation. |
| [AC3](#ac3-and-tc3-keep-dependency-setup-and-diagnosis-current) | [Declaration regression](../../../tests/test_doctor.py#L22-L43); [maintenance rule](../../../AGENTS.md#dependency-maintenance) | Current declaration checks and future maintenance obligations. |

Source mappings: 3 of 3 criteria.
This mapping does not count unchanged installer stages as new implementation.

### Code-change-to-test coverage

| Changed verification unit | Direct assertions | Evidence |
| --- | --- | --- |
| [Bootstrap diagnosis](../../../core/bootstrap.py#L94-L143) | [Fallback boundaries](../../../tests/test_bootstrap.py#L518-L565) | [Passing suite](unit-tests.log) |
| [Check argument handling](../../../core/bootstrap.py#L278-L310) | [JSON and no-write boundaries](../../../tests/test_bootstrap.py#L567-L599) | [Passing suite](unit-tests.log); [fresh probe](fresh-checkout-json.json) |
| [Declaration coverage regression](../../../tests/test_doctor.py#L22-L43) | Inspects both Python requirement maps and root Node runtime declarations. | [Passing suite](unit-tests.log) |

Inspected assertion paths: 3 of 3 changed verification units.
The test-only declaration unit enforces maintenance coverage. It implements no additional product behavior.

## Verification and limits

| Check | Actual result | Evidence |
| --- | --- | --- |
| Complete Python suite with native connector integration enabled | 831 passed; zero failures, errors, or skips | [Execution](unit-tests.log) |
| Initial targeted bootstrap and doctor suites | 28 and 21 passed before the final fallback regression | [Bootstrap](bootstrap-tests.log); [doctor](doctor-tests.log) |
| Existing macOS launcher, core profile | READY; JSON parsed successfully | [Launcher result](launcher-core-check.json) |
| Current all-feature diagnostics | Core READY; optional feature readiness INCOMPLETE | [Full result](current-all-check.json) |
| Workspace validation | VALID | [Result](workspace-validation.json) |
| Wheel build and local installation | Passed with prepared dependencies | [Build](wheel-build.log); [install](wheel-install.log) |
| Installed-wheel initialization and validation | Passed; new rules and setup instructions shipped; catalogs empty | [Result](wheel-smoke.json) |
| Document checks | Local links passed; no whitespace or report sentence-length findings | [Result](document-checks.json) |

The full suite includes unchanged online-command and offline fixture installation boundaries.
No new package download or complete company-target installation ran during this stage.
The wheel probe reused prepared local dependencies.
Native Windows, company proxy routing, live services, and business E2E remain unverified.
Optional credentials and grants still require their owners.
Check mode does not install Python, Node, browsers, or business applications.
No remaining blocker prevents use of the completed script changes within the verified local scope.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
