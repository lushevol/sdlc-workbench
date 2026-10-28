# Test engine environment test evidence

The [user request](user-input.md) defines this harness capability scope.
The added tests cover environment resolution, target paths, failure evidence, and private-value exclusion.
The tests use fake pages and a missing native browser executable.
They perform no target requests or live browser execution.

## Completed checks

Command, from `repos/testing/ratan-test-engine`:

```sh
node --test Tests/ratan/plugin/ui/session/offline/environment.test.cjs Tests/ratan/plugin/ui/session/real-world/offline/environment.test.cjs
```

The final command passed 18 tests with zero failures, skips, or cancellations.
Its exit code was zero. Its reported duration was `4604.677125` milliseconds.
The [retained output](test-engine-targeted-tests.txt) records each result.
An earlier run passed 17 tests before the additional compatibility assertions.
These results concern the two added offline test files.
They do not establish application behavior on any configured URL.

| Assertion scope | Result |
| --- | --- |
| Existing direct configurations with no selected environment | PASSED |
| Complete named profile selection without input mutation | PASSED |
| Missing, unknown, inherited, and malformed environment selection | PASSED |
| HTTP and HTTPS targets with ports and portal paths | PASSED |
| Unsupported schemes, embedded credentials, query values, and fragments | PASSED |
| Session setup and case evidence bind the selected environment, path, and effective configuration hash | PASSED |
| Native configuration failures occur before browser startup | PASSED |
| Native snapshots retain only the selected sanitized configuration | PASSED |
| Unselected profile contents and private values remain outside retained artifacts | PASSED |
| Local fixtures remain restricted to loopback targets | PASSED |
| The exported Robot facade forwards the selected environment into session setup | PASSED |
| Native direct configuration preserves its target with an explicit null environment | PASSED |

Both test files also passed `node --check`.
No files outside the two assigned test files and this evidence record were changed by the test worker.
The implementation owner will run the complete applicable harness suite before committing the stage.

## Runtime review

No actionable defect was found in the selected runtime changes against HEAD.
The [review source manifest](test-engine-review-sources.json) records the exact inspected bytes and baseline.
The review included the resolver, session setup, facade, Robot wiring, secondary contexts, native runner, and stack supervisor.

Installed Browser 19.1.2 discovers extension parameters from function source.
It injects reserved `page` arguments by name and supports default argument values.
The new facade uses `configFile, environment, page`.
The existing exported function preserves its required configuration argument and optional environment selection.
Both secondary-context cases forward the selected environment.
Native source retention includes the shared environment resolver.

The automated review scan identified two synthetic credential strings in privacy tests.
Context inspection confirmed test sentinels. It found no real credential among those matches.
The added assertions check public configuration results, navigation targets, and retained evidence.
They do not assert implementation source structure.

This reviewer authored the added tests and reviewed another worker's runtime implementation.
Browser extension integration was inspected in source. It was not executed through an actual Browser runtime.
Long secondary-context cases and remote connectivity remain unexecuted.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
