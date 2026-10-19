---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - macOS arm64 is the only platform with launch evidence in this review.
  - No PROD, STAGING, UAT, or DEV browser session was used.
---

# Browser investigation setup review

## Decision

Use the optional Playwright environment for future local browser investigations.
Use its branded Edge path when a declared Edge installation exists.
Keep the Robot test engine for independent business suites.
Do not add Playwright to mandatory Workbench Python or root Node installation.

The setup supplies a disposable profile, direct Edge selection, Chromium provisioning, agent CLI control, screenshots, traces, and timestamps.
It records runtime and source identities with each controlled smoke.
It provides a separate prepared bundle for disconnected installation.

This decision concerns tooling capability.
It does not prove portal behavior, browser policy, or PROD parity.

## Facts

The Workbench checkout was `621096a7aa0d09f4239a02c09af0b59e866e7832` at task start.
The final scoped changes use later commits because other authorized changes landed during this shared checkout.
The unrelated untracked `TODO` was preserved.

The registered resource `ratan-test-engine` uses `testing.robot`.
The resource points to `repos/testing/ratan-test-engine` and its `offline-smoke` suite.
The registered command resource exposes doctor, inventory, parse, and unit checks.
Workbench action records retain operation results and evidence hashes.

The test engine revision is `a639c6a92b2f125e2e99a0ca282ad7178e8c2c40`.
Its working tree has an unrelated modified `CLAUDE.md`.
The engine declares Robot Framework `7.2.2` and Robot Browser `19.1.2`.
Its Browser wrapper lock selects Playwright `1.49.1`.
Its wrapper `node_modules` was absent during inspection.
Its shared launch keyword passes a browser type and does not pass the Edge channel.
Its Python environment has no Selenium package or SeleniumLibrary.

The optional environment pins Playwright `1.64.1` in [package.json](../../adapters/browser/package.json) and [package-lock.json](../../adapters/browser/package-lock.json).
The npm stable tag resolved to `1.64.1` on `2026-10-19`.
The package requires Node `>=20`; this setup declares Node `>=22.12.0`.
The tested runtime was Node `24.16.0` on macOS `26.5` arm64.

The installed Edge executable was `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`.
Its version was `155.0.4283.62`.
The earlier incident evidence recorded `.60`.
The version difference limits direct browser-version comparison.

Playwright revision `1248` supplied Chrome for Testing `156.0.8078.4`.
The source installation also downloaded FFmpeg revision `1013`.
The optional browser folder is ignored and remains local.

The helper starts a browser process with a new temporary profile.
It binds a loopback debugging endpoint on an ephemeral port.
It connects with Playwright `noDefaults: true`.
It never connects to an existing browser endpoint.
It removes the profile after the smoke or launcher closes.

The helper starts Edge with updater and sync startup controls.
It disables background network startup and component update startup.
It preserves the browser sandbox and certificate validation.
It removes three Playwright defaults that suppress native background lifecycle behavior.
The helper records these settings in each result.

## Evidence

The source inspection record is [test-engine-inspection.json](../evidence/browser-setup-20261019/test-engine-inspection.json).
It records exact source revisions, installed package metadata, source hashes, action identities, and evidence limits.

The Edge controlled smoke is [edge-passed/result.json](../evidence/browser-setup-20261019/edge-passed/result.json).
It recorded Edge `155.0.4283.62` and Playwright `1.64.1`.
It recorded a hidden interval of `2012.3` milliseconds.
It retained a screenshot, ARIA snapshot, trace, and artifact manifest.

The Chromium controlled smoke is [chromium/result.json](../evidence/browser-setup-20261019/chromium/result.json).
It recorded Chrome for Testing `156.0.8078.4` and a hidden interval of `2039.8` milliseconds.
It retained the same evidence classes.

The registered Edge action is [registered-edge-action.json](../evidence/browser-setup-20261019/registered-edge-action.json).
Its action ID is `eb3b28fe9ae141699ad91496f192e4ae`.
It completed with `SUCCEEDED` and the nested browser smoke completed with `PASSED`.
An additional un-escalated rerun is [registered-edge-action-latest.json](../evidence/browser-setup-20261019/registered-edge-action-latest.json).
It failed before launch with `listen EPERM` while the sandbox denied the loopback socket.
The automatic approval reviewer rejected one escalated retry because its review service disconnected.
The earlier escalated action remains the registered Workbench success evidence.

The agent CLI smoke is [agent-cli.json](../evidence/browser-setup-20261019/agent-cli.json).
It ran ten fixed commands.
It exercised heading lookup, snapshot, tabs, screenshot, and close operations.
The native sequence attached to the launcher-created Edge process.

The prepared bundle manifest is [prepared-manifest.json](../evidence/browser-setup-20261019/prepared-manifest.json).
Its target was macOS arm64 and Node major `24`.
Its manifest hash was `5aa56608ab50cbcbf0d7997b61558be7ef0a466a9c81de5cb2a482ee2c8da71a`.
The clean installation retained an `INSTALLED` result in [offline-install.txt](../evidence/browser-setup-20261019/offline-install.txt).
Its package installation used offline npm and did not download a browser.

The clean installation launched Chromium and passed the role-locator assertion.
Two early visibility runs failed because the first page stayed hidden after the native tab action.
The failures are retained under `offline-chromium` and `offline-chromium-retry`.
The focused retry passed with a `2039.8` millisecond hidden interval.
Its result is retained under `offline-chromium-focused`.
The repeated desktop result limits confidence in an unattended clean-bundle smoke.
The source installation passed Edge and Chromium visibility checks.

The Workbench runtime suite ran `480` tests with `2` skips and `0` failures.
The wheel build passed with `--no-build-isolation`.
Workspace validation passed.
The focused bundle suite passed `6` tests.

## Inferences

The existing test engine can support branded Edge through Robot Browser's `channel` argument.
Its current shared keyword does not expose that argument.
A dedicated engine suite would need an independent source change and its own browser initialization.

The optional Playwright environment supplies a more current browser backend and direct agent operations.
It is useful for investigation evidence because it retains a trace and browser-native visibility timestamps.

The clean-bundle visibility failures may reflect native desktop foreground state or Chromium startup behavior.
They do not invalidate offline package integrity or browser launch evidence.
They prevent a claim that every clean-bundle desktop smoke has passed.

The short smoke cannot establish that a tab remains frozen naturally for thirty minutes.
It cannot establish access-token renewal, logout policy, or portal behavior.

## Unknowns and next actions

No approved browser policy was available for PROD, STAGING, UAT, or DEV.
The owner is unknown.
Obtain a permitted environment and record its browser version and policy before live verification.

The user's original browser profile and extension state are unknown.
The owner is unknown.
Use the native isolated launcher for future controlled comparisons.

The test engine's Browser wrapper installation remains incomplete.
The owner is the Ratan test-engine maintainer.
Initialize its own Browser node dependencies only when an approved Robot suite needs them.

Native Windows launch, bundle preparation, and clean installation remain untested.
The owner is unknown.
Repeat the doctor, smoke, and offline bundle checks on a matching Windows computer.

MCP client registration remains untested.
The owner is Workbench maintainers.
Register an MCP operation only after a client test retains tool output and access limits.

## Evidence limits

The fixture uses no account, token, business endpoint, or external message.
The smoke is a tooling check and has no business coverage.
The local portal services were not restarted or modified.
The earlier portal incident report remains the source for its long interval and local root cause.
This review does not change that report or establish PROD parity.

The evidence records use exact source hashes and action paths.
Hashes support change detection.
They do not authenticate a publisher or establish human approval.

Human review is pending for this report.
