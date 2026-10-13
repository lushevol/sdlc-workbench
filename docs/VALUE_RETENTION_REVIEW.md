---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Value retention review

Review date: 14 October 2026.
Source baseline: `4400994`.
Scope: Project principles, runtime layout, registry examples, test selection, and standalone distribution.

The user directed this change in the [retained message](../knowledge/raw/value-principle-request-2026-10-14.txt).
[Principle 9](../PRINCIPLE.md) requires a current consumer, observable benefit, and supporting evidence.
Possible future usefulness alone cannot justify retained implementation.
Raw sources, unresolved knowledge, findings, and audit history retain their existing evidence value.

## Retention decisions

| Item | Current consumer and evidence | Decision and consequence |
| --- | --- | --- |
| Python runtime | Agent clients use initialization, validation, CLI, and MCP. Retained regressions check these interfaces. | Merge into `core/`. Preserve the installed package name `ai_sdlc_workbench`. |
| Catalog examples | Registry readers use linked examples. Catalog tests check schemas, classifications, and references. | Move into `registry/examples/`. Default catalogs remain separate and empty. |
| Public calculator demonstration | Integration tests required fixtures, but no current engineering workflow required a public calculator. | Remove `--demo`. Keep minimal provider fixtures inside `tests/support.py`. |
| Dashboard | The current phase uses agent interfaces. No current consumer justified the separate dashboard. | Remove `serve`, HTTP code, static assets, and two dashboard tests. |
| Sample plugin and resource list | The plugin contract supplies the interface. The sample plugin had no execution checks. The resource list had no callers. | Remove the examples. Keep the implemented provider contract and its behavior checks. |
| Duplicate tests | Broader catalog and initialization checks retain the same useful assertions. | Consolidate three tests. Remove two demonstration tests with their feature. |
| Weak test fixtures | Unrelated validation errors could satisfy two assertions. | Use valid surrounding fixtures before changing the field under test. |

The suite contains 76 tests after seven removals or consolidations.
[The test contract](../tests/README.md) identifies current consumers and observable checks.
These regressions establish bounded Workbench behavior only.
They do not establish business-system verification or complete requirement coverage.

## Scope and risk

Caller inspection covered package imports, configuration loading, initialization, CLI dispatch, MCP, provider fixtures, and build configuration.
Packaging maps `core/` to `ai_sdlc_workbench` without a second runtime.
Catalog loading now uses `ai_sdlc_workbench.context`.
Knowledge validation now uses `ai_sdlc_workbench.governance`.
Generated workspaces receive core guides without Python source.

Qualitative risk is moderate because package paths and shipped commands change.
The removed `serve` and `--demo` commands require users to use the supported agent interfaces.
Historical review reports retain their original execution claims and source limits.

Owner: Workbench maintainer. The named owner is unknown.
Next action: apply the value rule before adding implementation, examples, dependencies, or tests.

## Stage acceptance

```gherkin
Scenario: Install the runtime independently
  Given the built wheel is installed outside the source checkout
  When the installed ai-sdlc command creates and validates a workspace
  Then the validation status is VALID
  And all six primary shared skills are available
  And the workspace contains zero Python runtime files under core

Scenario: Keep catalog examples separate
  Given a newly initialized workspace
  When the catalog tests validate the shipped declarations
  Then all six default catalogs contain zero entries
  And registry/examples declarations satisfy the supported catalog contracts

Scenario: Retain useful regression checks
  Given the retained standalone regression suite
  When the suite runs with access to its local mock service
  Then all 76 tests pass
  And the required-field and identifier tests first establish valid baseline fixtures
```

## Validation evidence

| Check | Result | Retained evidence and limits |
| --- | --- | --- |
| Runtime regressions | PASSED: 76 tests | [Execution output](evidence/value-retention-tests.txt). Assertions cover the supported Workbench interfaces and boundaries. |
| Wheel build and independent installation | PASSED | [Installation and workspace checks](evidence/value-retention-wheel.txt). Checks include resource bytes, shared skills, and excluded runtime copies. |
| Source workspace validation | VALID | Configuration, catalog, source snapshot, and audit checks report zero findings. |
| Documentation and diff checks | PASSED | Local links, changed prose limits, package contents, and whitespace checks passed. |

The first sandbox run blocked the mock service's loopback socket.
The retained successful run allowed that local test server.
Execution used macOS and Python 3.14.5.
Windows execution remains unchecked.
ASD writing review remains pending.

## Governance record

[The new audit event](../knowledge/audit/2026-10-14-value-retention.yaml) records this user-directed change.
Its evidence refers to the unchanged user-message snapshot and its manifest hash.
The event records an agent-authored candidate without claiming authenticated human review.
The user supplied no formal reviewer identity.
