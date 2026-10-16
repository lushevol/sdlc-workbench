---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Ratan native integration validation

Ratan now uses native Workbench Robot execution and registered offline checks.
The engine keeps its independent repository and Python environment.
The integration commit is `a639c6a92b2f125e2e99a0ca282ad7178e8c2c40`.
Read [the baseline assessment](assessment.md) for source findings and dependency limits.
Read [the action results](integration-results.json) for retained execution identities and file hashes.

## Completed scope

The `testing.robot` provider uses explicit suite grants and a separate interpreter.
It retains native reports, source hashes, and separate `PASS`, `FAIL`, and `SKIP` results.
It rejects unregistered suites, escaping paths, and malformed reports.
Dry runs retain an explicit assertion-execution limit.
Timeouts terminate process groups or request Windows process-tree termination.
Unconfirmed termination remains an explicit result limitation.

The engine uses Python 3.13.14 and 138 installed packages.
Its repaired lock preserves all 144 package identities.
Only NumPy changed version, from `2.4.0` to `2.4.1`.
All 751 shared artifact hashes matched the previous lock.
The manifest now declares its direct pandas and FastMCP dependencies.
The canonical lock uses public PyPI artifacts.

## Actual checks

| Check | Result | Scope and limit |
| --- | --- | --- |
| Workbench runtime tests | PASSED: 325 tests | Includes 13 native Robot regressions and existing runtime boundaries. |
| Engine adapter tests | PASSED: 8 tests | Covers private paths, parser imports, dependency checks, and syntax failures. |
| Full package doctor | PASSED: 32 checks | Checks installed package metadata without importing business libraries. |
| Dependency consistency | PASSED: 138 packages | Checks installed dependency requirements. |
| Native Robot execution | PASSED: 3 tests | Executes BuiltIn-only framework assertions through Workbench. |
| Native dry run | SUCCEEDED: 3 reported tests | Assertions were not executed. |
| Scoped static parsing | PASSED | Parses the isolated smoke source without project-library imports. |
| Metadata inventory | PASSED | Reports selected code paths and sizes without source excerpts. |
| Legacy static parsing | FAILED | Reports 567 diagnostics across 19 of 312 selected files. |
| Workspace validation | VALID | Checks catalog and saved knowledge contracts. |
| Wheel and external initialization | PASSED | Initializes and validates a workspace outside the source checkout. |
| Shipped assets | PASSED | Provider, guides, schemas, templates, and shared skills remain available. |
| Windows process-tree cleanup | PASSED with mocks | Actual Windows execution was unavailable. |

Runtime tests required loopback access for their local mock HTTP server.
The final wheel check used the required isolated build command.
The independent wheel environment imported the installed package outside this checkout.
Generated workspaces contain responsibility guides without runtime source or runtime tests.

## Remaining findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Retained `parse-all` action and baseline assessment | Legacy syntax diagnostics prevent a clean all-source parse. | unknown | Review each diagnostic before enabling its business suite. |
| Private variable imports in the baseline assessment | Business execution still needs environment inputs, credentials, and keys. | unknown | Supply approved private inputs and select a permitted test environment. |
| Browser dependency installation | UI execution still needs browser binaries. | unknown | Install the required browser assets before selected UI tests. |
| Windows cleanup mock tests | Windows process-tree behavior lacks local execution evidence. | Workbench runtime maintainer | Run the provider checks on Windows before deployment there. |

No business suite, workbook generator, MCP server, or upload utility ran during setup.
Framework execution does not establish approved business coverage or verified business behavior.
The original onboarding report remains pinned to its earlier baseline.
Its exact-byte check passed before implementation changes.

An unrelated `CLAUDE.md` deletion remains unstaged in the engine repository.
Its actor is unknown.
The Workbench's unrelated `TODO` file remains untracked.
Neither file is part of these integration commits.
