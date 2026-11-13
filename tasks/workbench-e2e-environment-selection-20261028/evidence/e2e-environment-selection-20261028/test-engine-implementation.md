# Test engine environment selection

The [user request](user-input.md) authorizes target selection for existing test scripts.
This stage changes the independent test engine's configuration selection and evidence metadata.
It does not change business assertions or execute business cases.

## Scope and risk

The source baseline is `5bb3d5ef73f16938a0a8864c9fd94a95a5de7ca9`.
The existing direct configuration already accepted remote portal URLs.
The new named wrapper selects complete configurations through `SESSION_ENVIRONMENT` or native `--environment`.
Selection requires an explicit known name. It cannot fall back to another environment.
Direct configuration remains supported without a named selection.

Affected consumers are the Robot facade, session setup, two secondary browser contexts, native runner, and local stack supervisor.
The shared resolver validates HTTP and HTTPS targets with deployment paths.
Existing restrictions on target credentials, queries, and fragments remain.
The separate `loginUrl` option retains its existing navigation behavior.
The native fixture mode still permits loopback targets only.

Qualitative risk is moderate. Incorrect target configuration can direct existing test actions to another environment.
Explicit selection, independent complete profiles, and target evidence reduce accidental selection.
The [examples](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/config.environments.example.json) contain placeholder URLs and environment-specific account variable names.
Operators must configure actual targets, source revisions, selectors, and lifetimes before execution.

## Evidence and tests

Results retain the selected environment, sanitized `targetUrl`, and effective configuration SHA-256.
The original configuration hash still binds the complete input file.
Native configuration snapshots retain only the selected entry and apply existing private-value redaction.
The source manifests include the new resolver.

```gherkin
Scenario: Select one configured target
  Given separate nonprod and prod configurations
  When the runner selects nonprod
  Then navigation uses the complete nonprod portal URL and path
  And retained results contain the nonprod name and selected configuration hash
  And retained evidence excludes the unused production configuration

Scenario: Reject an ambiguous target
  Given a named configuration file
  When the runner receives no environment name or an unknown name
  Then configuration fails before target navigation
  And the native runner starts no browser

Scenario: Preserve direct configuration
  Given an existing single target configuration
  When the runner receives no environment selection
  Then it uses the existing target URL and path
  And retained results identify no named environment
```

The [session tests](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/offline/environment.test.cjs) assert resolver boundaries and facade-to-evidence behavior.
They use a fake page and synthetic tokens. They make no target requests.
The [native tests](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/offline/environment.test.cjs) assert selection, privacy, and direct-configuration compatibility.
They use configuration rejection or an unavailable browser executable. They launch no actual browser.
The [independent review](test-engine-test-notes.md) found no actionable defect within its inspected scope.

The [complete offline suite](test-engine-offline-execution.json) passed 43 tests with zero failures, skips, or cancellations.
Its [execution output](test-engine-offline-tests.tap) retains individual outcomes and runner counts.
The [adapter and parser results](test-engine-local-check-results.json) record eight passing Python tests and one successful static Robot parse.
The [static checks](test-engine-static-checks.json) passed 122 link, shell, JSON example, and source syntax checks.
`git diff --check` passed before staging.

## Delivery state and limits

The independent repository commit is `9f83897e8e71f8afa524b260ffa3e809b281a2f0`.
The commit contains 15 scoped runtime, test, example, and guide files.
Existing `CLAUDE.md` and `playwright-log.txt` changes remain outside this stage.
No dependency, registry, service deployment, or business behavior changed.
Offline results establish configuration routing within the inspected boundaries.
They do not establish target connectivity, deployed identity, valid credentials, or passing business cases on any environment.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
