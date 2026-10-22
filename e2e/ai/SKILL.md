---
name: portal-pom
description: Discover and execute the root Playwright POM for portal, login, session, and Category UI investigations.
---

# Portal POM operations

Use the root [E2E guide](../README.md) for setup and execution limits.
Run commands from the Workbench source root.
The POM remains separate from the registered business test engine.

Discover operations and check static source freshness:

```sh
npm run e2e:ai -- actions list
npm run e2e:ai -- validate
```

Inspect the current state before choosing a named action.
Use `--fixture` for isolated harness checks.
Use an explicitly authorized `--url` and actual `--prefix` for application investigations.
`--allow-session-change` enables the registered session operations within that invocation.
It records execution intent; it does not grant external-system authorization.

```sh
npm run e2e:ai -- inspect --fixture --area portal
npm run e2e:ai -- sequence --fixture --allow-session-change --steps-file e2e/ai/session-extension.sequence.json
```

Use `sequence` for dependent actions.
Separate invocations create isolated browser contexts.
The dispatcher accepts named operations only.
It accepts no caller JavaScript, selector fallback, or arbitrary endpoint.

If a target is absent, duplicated, hidden, or disabled, retain the mismatch and inspect its source contract.
Do not replace the locator with a guessed control.
Component methods describe clicks and UI observations.
Only the session flow independently checks installed credentials and authentication validation.
That predicate establishes neither token lifetime nor downstream authorization.

Treat fixture results as harness evidence.
Keep canonical business cases `NOT_RUN` until actual application execution supports their assertions.
Use the [binding manifest](../traceability/bindings.json) and [case inventory](../traceability/cases.json) for remaining gaps.

Fixture commands save structured summaries and traces under ignored `e2e/results/`.
Application commands save summaries without traces or authentication state.
Use `--capture-ui` only when the authorized investigation permits application text capture.
Accessibility snapshots can contain displayed data.
Keep captured application evidence under its owning task and inspect it before sharing.
