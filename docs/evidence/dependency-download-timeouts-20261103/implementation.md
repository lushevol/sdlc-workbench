# Dependency download timeout implementation

**Download commands now stop at their configured deadline and provide manual recovery instructions.**

Owner: Workbench maintainer.
Next action: run setup with the required deadline, then diagnose remaining prerequisites.
Native Windows and live company download access remain untested.

Status: COMPLETE.

## User reference

The [user request](user-input.md#exact-user-input) defines this maintenance scope.
Downloads need bounded timeouts and manual recovery instructions when network access fails.

## Scope and risk

Inspected callers include both setup launchers, bootstrap installation, offline preparation, browser provisioning, and their tests.
Affected interfaces include online command execution and the three preparation command parsers.
No package dependency was added.
Unrelated checkout changes remain outside this stage.
Risk is moderate because interrupted installers can leave incomplete dependencies.
Stage failures therefore retain `INCOMPLETE` status or stop preparation before bundle publication.

## Result and commands

The default deadline is 120 seconds per network command.
The argument accepts whole seconds from 1 to 86400.
Each complete package operation has its own deadline; installation can contain several operations.
Local checks and offline installation retain their separate limits.
Windows process-tree termination can require up to five additional seconds.

| Action | macOS or Python command | Windows PowerShell |
| --- | --- | --- |
| Install with a 60-second command deadline | `./setup.command --download-timeout 60` | `.\setup.cmd --download-timeout 60` |
| Prepare a core bundle | `python3 core/offline.py prepare --output offline-bundle --core-only --download-timeout 120` | `py -3 core\offline.py prepare --output offline-bundle --core-only --download-timeout 120` |
| Prepare browser assets | `node adapters/browser/bundle.mjs prepare --output NEW_PATH --download-timeout 120` | Same command with a native path. |
| Diagnose remaining prerequisites | `./setup.command --check` | `.\setup.cmd --check` |

Pip requests use at most 15 seconds, with automatic retries disabled.
Npm fetches use the same request limit and no automatic retries.
Browser tarball deadlines cover headers and the complete response body.
Playwright has a whole-command deadline, including its internal retries.
Timeout cleanup stops downloader descendants.
Browser interruption also stops descendants and removes the incomplete bundle.

Warnings exclude subprocess diagnostics and private registry settings.
They identify approved mirrors, matching-platform bundles, transfer steps, and the [manual recovery guide](../../../docs/SETUP.md#blocked-downloads-and-manual-recovery).
Missing Python and Node messages identify manual runtime download sources.
The [maintenance rule](../../../AGENTS.md#dependency-maintenance) requires these controls for future scripted dependency acquisitions.

## Controlled baseline comparison

### Setup and steps

1. Start a controlled downloader with a child process that writes a delayed completion marker.
2. Apply a one-second command timeout to the committed baseline and candidate helpers.
3. Check the marker after its scheduled write time.
4. Check the failure message for manual recovery instructions.

### Intended result

Stop the downloader and its descendants.
Warn the user and identify manual recovery steps.

### Old result

The parent stopped, but its child continued and wrote the completion marker.
The message gave no manual bundle instructions.
Evidence: [baseline result](baseline-timeout.json), bound to commit `b98215fdbb6053e9e5d7c42ea2fb00051cf9102a`.

### New result

The descendant stopped and did not write its completion marker.
The warning identified matching-platform preparation and `--offline-bundle PATH`.
Evidence: [candidate result](candidate-timeout.json) and the [repeatable probe](probe-timeouts.py).
This controlled process proves local cancellation only; it does not prove company download access.

## Acceptance criteria and test cases

### AC1 and TC1: Bound stalled downloads

```gherkin
Scenario: Stop a stalled dependency download
  Given an online dependency command exceeds its configured deadline
  When the deadline expires
  Then setup stops the command and its downloader descendants
  And the operation does not report success
```

Assertions: [Python process tests](../../../tests/test_download_timeouts.py) and [browser transfer tests](../../../adapters/browser/bundle.test.mjs).
Execution: [Python suite](unit-tests.log), [browser suite](browser-tests.log), and [candidate probe](candidate-timeout.json).

### AC2 and TC2: Guide manual recovery

```gherkin
Scenario: Explain a failed dependency acquisition
  Given an online dependency command fails or times out
  When setup reports the failure
  Then the warning identifies the component and manual recovery steps
  And it excludes private subprocess diagnostics
```

Assertions: [bootstrap redaction test](../../../tests/test_bootstrap.py) and [warning tests](../../../tests/test_download_timeouts.py).
Browser assertions include private proxy response redaction and sanitized command failures.
Execution: [Python suite](unit-tests.log) and [browser suite](browser-tests.log).

### AC3 and TC3: Preserve diagnosis and offline boundaries

```gherkin
Scenario: Retain a usable offline installation path
  Given the user supplies a validated matching offline bundle
  When setup installs the bundle
  Then it uses local package assets without online fallback
  And diagnostics remain available without downloading packages
```

Assertions: [offline regressions](../../../tests/test_offline.py), [bootstrap regressions](../../../tests/test_bootstrap.py), and [browser bundle tests](../../../adapters/browser/bundle.test.mjs).
Execution: [Python suite](unit-tests.log), [browser suite](browser-tests.log), and [local diagnosis](core-check.json).

## Traceability

| Criterion | Test assertions | Changed implementation | Retained execution |
| --- | --- | --- | --- |
| [AC1](#ac1-and-tc1-bound-stalled-downloads) | [Python timeout tests](../../../tests/test_download_timeouts.py), [browser tests](../../../adapters/browser/bundle.test.mjs) | [bootstrap command](../../../core/bootstrap.py), [offline preparation](../../../core/offline.py), [browser preparation](../../../adapters/browser/bundle.mjs) | [Python](unit-tests.log), [browser](browser-tests.log), [probe](candidate-timeout.json) |
| [AC2](#ac2-and-tc2-guide-manual-recovery) | [bootstrap tests](../../../tests/test_bootstrap.py), [warning tests](../../../tests/test_download_timeouts.py), [browser tests](../../../adapters/browser/bundle.test.mjs) | [bootstrap warnings](../../../core/bootstrap.py), [macOS launcher](../../../setup.command), [Windows launcher](../../../setup.cmd), [browser warnings](../../../adapters/browser/bundle.mjs) | [Python](unit-tests.log), [browser](browser-tests.log) |
| [AC3](#ac3-and-tc3-preserve-diagnosis-and-offline-boundaries) | [offline tests](../../../tests/test_offline.py), [bootstrap tests](../../../tests/test_bootstrap.py), [browser tests](../../../adapters/browser/bundle.test.mjs) | [online/offline routing](../../../core/bootstrap.py), [bundle preparation](../../../core/offline.py), [browser routing](../../../adapters/browser/bundle.mjs) | [Python](unit-tests.log), [browser](browser-tests.log), [diagnosis](core-check.json) |

The three maintenance criteria have test assertions and changed-code links: 3/3 in each matrix.
The three changed runtime modules have direct assertion links: 3/3.
Two launcher message changes have static checks; native Windows launchers remain untested.
These counts describe traceability; they do not prove business conformance or platform parity.

## Validation

The [full Python suite](unit-tests.log) passed 852 tests with zero failures, errors, or skips.
The [browser suite](browser-tests.log) passed 20 tests with zero failures, cancellations, or skips.
An independent review found and confirmed the browser interruption issue before correction.
The added cancellation cases cover SIGINT, SIGTERM, descendant cleanup, and partial bundle removal.

The [wheel build](wheel-build.log), [installed-wheel smoke](wheel-smoke.json), and [workspace validation](workspace-validation.json) passed.
The wheel smoke initializes an external workspace and checks the shipped guides, rules, runtime, and 16 skills.
It reuses prepared local dependencies and performs no public package download.
The [verification summary](verification-summary.json) records scoped source hashes and document checks.
The full suite includes concurrent unrelated checkout changes; the source hashes identify this maintenance scope.

No complete fresh company installation or public download was performed.
Native Windows process cleanup remains unverified by execution.
Browser request tests use loopback fixtures; the cancellation probe uses controlled local processes.
Package readiness remains separate from live service access and business verification.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
