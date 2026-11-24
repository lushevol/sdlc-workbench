# Test engine execution documentation change

No critical conclusions require user attention or action.

The [documentation request](documentation-update-user-input.txt) authorizes these guide changes.
The affected scope is two guides in the independent test engine repository.
Qualitative risk is low. Runtime source, test definitions, configuration, and dependencies remain unchanged.

The [session guide](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#execution) now defines operator and AI execution steps.
It covers private preparation, short and long selectors, fresh output paths, and immediate case evidence retention.
It separates actual assertions from parsing, discovery, skipped cases, and observations.
Canonical links target the current case catalog. Execution navigation targets the current evidence index.

The [repository guide](../../../../repos/testing/ratan-test-engine/docs/WORKBENCH.md#select-the-execution-entry-point) now identifies each supported runner.
It adds generated UI and API examples with their private environment selectors.
It explains browser initialization and the offline smoke wrapper's scope.

## Checks and source identity

The [retained check result](test-engine-documentation-checks.json) records 73 resolved links and 15 shell syntax checks.
It also records nine Robot option checks and nine source-based selector checks.
All checks passed. They did not execute test cases or launch browsers.
`git diff --check` passed. The documentation diff was reviewed before staging.
The source before this documentation commit was `78141a4eec8040dd0d1ac8a6579b20f612fca0f0`.
The documentation commit is `46df3a8717f66336ce8b41ab5a3596e8d22c0c50`.
Only `docs/WORKBENCH.md` and `Tests/ratan/plugin/ui/session/README.md` entered that commit.

Existing `CLAUDE.md`, supplemental review drivers, and `playwright-log.txt` changes were preserved outside this stage.
No business execution or deployment claim follows from these documentation checks.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
