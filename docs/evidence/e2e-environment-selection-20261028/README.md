# E2E environment selection maintenance

**Configure actual URLs and authentication before deployed execution. The operator owns this setup. No deployed environment was contacted.**

The [user request](user-input.md) defines this runner capability change.
Scope: Configure test targets without changing business behavior or expected assertions.
Affected scope: Root POM CLI, Playwright configuration, target profiles, deployed UI checks, and independent session runners.
Existing consumers include fixture specifications, local audit suites, POM page objects, and native session scripts.

## Result and execution guides

The [root E2E guide](../../../e2e/README.md#select-a-target-environment) defines profiles, saved authentication, commands, and evidence.
The [Robot guide](../../ROBOT_TESTING.md#select-a-named-session-environment) defines test-engine selection and native-runner references.
The [setup guide](../../SETUP.md#root-playwright-pom-harness) links both installation and execution.

Named profiles supply explicit targets and optional saved Playwright authentication state.
The root CLI preserves direct URL selection. Its existing default area remains `portal`.
Named profiles default to `login`. Operators can select `portal` or `category`.
Unknown names and ambiguous target overrides fail before browser startup.
Local fixture suites reject named deployment selection before target requests.
Existing local audit helpers use synthetic credentials, replaced responses, and fixture endpoints.
Those cases remain bound to their isolated local configuration.

Root deployed checks assert actual HTTP success, the selected origin, and existing POM predicates.
They recheck the origin after UI assertions to reject asynchronous cross-origin redirects.
Source snapshots exclude the selected profile and authentication-state file.
Retained target summaries omit URL query values, fragments, and authentication-state contents.
The root resolver normalizes hexadecimal fingerprints and rejects non-string UI areas.

The [test-engine implementation record](test-engine-implementation.md) describes selection across Robot, secondary contexts, native execution, and stack supervision.
Its independent commit is `9f83897e8e71f8afa524b260ffa3e809b281a2f0`.
No dependency was added. Existing application assertions remain in their original runners.

## Verification evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Root TypeScript | Passed | `npm run e2e:typecheck` |
| Root resolver unit suite | 21 passed; zero failures or skips | [Final output](environment-unit-final.txt) |
| Controlled browser integration | One test passed; four target executions and CLI checks | [Output](integration-privacy-stdout.txt), [nonprod](integration-privacy/nonprod/run-result.json), [prod](integration-privacy/prod/run-result.json) |
| Negative browser assertions | Wrong prefix and asynchronous cross-origin redirect both failed as required | [Wrong prefix](integration-privacy/wrong/case-result.json), [redirect](integration-privacy/redirect/case-result.json) |
| Fixture regression | 46 passed; zero failures | [Output](fixture-regression-tests.txt) |
| Workbench runtime suite | 658 discovered; zero failures; two optional skips | [Full execution](workbench-runtime-tests-local-access.txt) |
| Optional connector suite | 14 passed, including both previously skipped cases | [Output](optional-connector-tests.txt) |
| Test-engine offline suite | 43 passed; zero failures or skips | [Execution](test-engine-offline-execution.json), [output](test-engine-offline-tests.tap) |
| Test-engine adapter and Robot parser | Eight Python tests passed; static Robot parse passed | [Results](test-engine-local-check-results.json) |
| Test-engine static checks | 122 passed | [Results](test-engine-static-checks.json) |
| Wheel build | Passed with the installed backend and no build isolation | [Output](wheel-build-offline.txt) |
| Documentation and syntax | Local links, shell blocks, and JSON examples checked | [Results](static-checks.json) |

The full runtime run and optional run overlap. Do not add their counts as unique tests.
All default-inventory cases have passing execution across those two runs.
The controlled integration uses synthetic localhost services and synthetic credentials.
Its `nonprod` and `prod` names do not represent deployed environments.
It checks distinct paths, prefixes, saved-cookie use, metadata redaction, and snapshot exclusion.
It also checks configured CLI validation and fixture rejection before HTTP access.
The [source manifest](source-manifest.json) identifies the completed implementation bytes.
Earlier execution metadata retains its own inspected source hashes.

Initial sandbox executions could not bind local ports.
Their [runtime output](workbench-runtime-tests.txt) and [integration failure](integration-sandbox-failure.json) remain retained.
Approved local-access reruns passed. No failed application assertion was suppressed.
The [isolated wheel attempt](wheel-build.txt) failed while obtaining build dependencies through the restricted proxy.
The successful build used installed tooling without changing dependencies.
The retained pip output contains two whitespace-only progress lines. Diff checks preserve those raw lines and check authored files separately.

## Risk and remaining limits

Risk is moderate. Incorrect target selection can execute session actions against the wrong service.
Explicit selection, early rejection, saved target identity, and independent profiles reduce accidental selection.
Operators must provide correct URLs, state, source revisions, and case-specific timing expectations.
These checks do not establish real deployment connectivity, valid production credentials, or passing canonical business cases.
The Robot Browser extension and long session cases were not executed against deployed services.

**Existing source-contract drift blocks `e2e:check`. The binding maintainer must compare the cited Timeout revision before updating its contract.**

The [static validator](static-source-validation.txt) reports changed bytes in `src/components/Timeout/index.tsx`.
Its cited revision is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Traceability validation passed. Source-contract validation failed independently of environment selection.
This stage preserves that failure and makes no current-source business-verification claim.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
