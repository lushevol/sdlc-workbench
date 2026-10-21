---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native Windows execution remains untested.
---

# Isolated browser investigations

Use this optional environment for browser observations that need screenshots, traces, snapshots, or controlled tabs.
Keep approved business test suites in their independent test repository.
Generated workspaces include this guide. Run browser commands from a separate source checkout or prepared browser installation.

Keep browser evidence under its business task only when it supports that task's claims or investigation limits.
Use the [task priorities](../tasks/README.md#evidence-priorities-and-cleanup) to remove unrelated setup bulk and redundant outputs.
Label screenshots as business reproduction, synthetic tooling, or actual test output.
Browser access alone does not establish that a unit test ran or produced screenshots.
Record each retained image's run, capture time, phase, method, hash, claim, and limits.
Mark unknown capture details explicitly. Do not present setup screenshots as business reproduction evidence.

## Retain key screenshots

For UI end-to-end verification, capture screenshots at these checkpoints:

- The starting state before the scenario action.
- Key interaction outcomes and decisive intermediate states.
- The final result, including visible errors when the scenario fails.

Save captures under the corresponding task's `evidence/` directory, grouped by run, before temporary output cleanup.
Follow [case evidence checkpoints](../tasks/README.md#save-case-evidence-and-resume-checkpoints) for immediate retention, volatile state, and interrupted investigations.
Embed key images in the investigation document with captions. Link their original files from its evidence index.
Link each image to its scenario step or asserted outcome. Keep the capture metadata and hashes described above.

For natural background investigations, capture immediately before departure and after return. Do not foreground the hidden tab for screenshots.
If capture fails, retain the error and mark the affected visual evidence incomplete.
Accessibility snapshots and traces supplement key screenshots. They do not replace the required images.
Screenshots establish visible state only. Retain assertions, logs, and traces for timing, requests, and causal claims.

## Investigate session timing

Use the [timing and deployment checks](../.agents/skills/verify-implementation/references/browser-investigation.md#verify-timing-inputs-and-deployment-settings) for missing expiry dialogs and related session failures.
Trace issued lifetimes, effective overrides, clocks, and scheduled delays before attributing the failure to browser inactivity.
Use actual configured issuance and disclosed shortened expiry controls for their separate claims.
Record unresolved deployment settings beside local passing results. A local browser pass does not establish UAT configuration parity.

## Install explicitly

Use approved Node `>=22.12.0` and npm.
Run these commands from the standalone source checkout:

```sh
npm --prefix adapters/browser ci --ignore-scripts --no-audit --no-fund
```

On macOS, provision Chromium explicitly:

```sh
PLAYWRIGHT_BROWSERS_PATH="$PWD/adapters/browser/.browsers" node adapters/browser/node_modules/playwright/cli.js install chromium --no-shell
```

On Windows PowerShell, use:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) 'adapters/browser/.browsers'
node adapters/browser/node_modules/playwright/cli.js install chromium --no-shell
```

This command also provisions Playwright's FFmpeg asset.
It omits the separate Chromium headless shell.
Use the company-approved Edge installation when available.
Do not run `playwright install msedge` over an existing managed installation.
The helper checks standard macOS and Windows Edge locations.
It does not install Edge or access a personal profile.

```sh
node adapters/browser/browser.mjs doctor
```

`READY` identifies package and executable presence only.
Run the selected smoke to establish actual launch evidence.
Missing packages or browsers require explicit installation; startup supplies no automatic download.

## Launch a disposable investigation

Open a dedicated Edge browser:

```sh
node adapters/browser/browser.mjs open --browser msedge --url about:blank
```

Select `--browser chromium` for the pinned Chromium asset.
Replace `about:blank` only with an authorized investigation URL.
Keep the launcher terminal open.
Press Ctrl+C there to close its process and remove its temporary profile.
No account sign-in or personal profile is required for setup checks.

The launcher creates its own loopback debugging endpoint and profile.
Playwright connects to that endpoint with `noDefaults: true`.
This option avoids Playwright focus emulation in the existing default context.
The launcher never connects to an existing personal browser endpoint.

The native launch arguments suppress first-run prompts, sync, browser background networking, and updater startup.
Edge also disables forced browser sign-in and LaunchServices version updates.
The launch does not disable browser sandboxing or certificate validation.
These settings still differ from a personal browser.
Record the configuration with each investigation.

In another terminal, use the bundled agent CLI:

```sh
node adapters/browser/browser.mjs agent-native msedge open
node adapters/browser/browser.mjs agent-native msedge snapshot
node adapters/browser/browser.mjs agent-native msedge tab-list
node adapters/browser/browser.mjs agent-native msedge tab-new about:blank
node adapters/browser/browser.mjs agent-native msedge tab-select 0
node adapters/browser/browser.mjs agent-native msedge screenshot
node adapters/browser/browser.mjs agent-native msedge close
```

The wrapper selects a named session and its launcher-created configuration.
Native agent commands pass that configuration on every command.
It excludes personal-profile, extension, and arbitrary endpoint options.
It ignores inherited Playwright MCP configuration and the home CLI configuration.
Outputs use ignored `adapters/browser/evidence/`.
Review retained artifacts before copying them into a shared evidence directory.
Traces and network responses can contain application secrets.

For standard automation, the wrapper can launch an independent disposable session directly:

```sh
node adapters/browser/browser.mjs agent msedge open about:blank
node adapters/browser/browser.mjs agent msedge snapshot
node adapters/browser/browser.mjs agent msedge close
```

Standard automation retains Playwright focus emulation.
Do not use its visibility result as natural background evidence.
It removes three specific launch defaults that disable background throttling and renderer backgrounding.
The native launcher avoids those defaults and uses `noDefaults` for the connection.

The installed package also exposes `mcp`, `codegen`, `show-trace`, and `trace` commands.
The agent CLI was exercised in this setup.
The MCP entry point was inspected through help; client registration and MCP browser control remain untested.
No MCP server starts automatically.

## Run and retain the controlled smoke

```sh
node adapters/browser/browser.mjs smoke --browser chromium --output /absolute/new/evidence-directory
node adapters/browser/browser.mjs smoke --browser msedge --output /absolute/another/new/evidence-directory
```

Each smoke serves a credential-free fixture on an ephemeral loopback port.
It clicks a role locator and checks the resulting status text.
It switches tabs, waits two seconds with a native browser timer, and returns.
It checks actual `visibilitychange` observations and a background interval of at least 2,000 ms.
It preserves timestamps, runtime versions, source hashes, screenshot, ARIA snapshot, trace, and artifact hashes.
Existing output directories remain protected.
Trace and cleanup errors remain in failed results. Later cleanup steps still run, and partial artifacts retain hashes.
Native launchers reserve their session directory before launch. Only the owning launcher releases it.

The smoke uses no fake clock, shortened access expiry, forced freeze, or business login.
It does not reproduce the portal's 30-minute incident.
For actual long investigations, retain natural lifecycle events and the real elapsed interval.
Avoid polling a hidden page while testing natural freezing.
Record unknown policies and environment differences beside the findings.

The source checkout registers these fixed checks through `testing.command`:

```sh
.venv/bin/ai-sdlc --workspace . call browser-investigation-checks list
.venv/bin/ai-sdlc --workspace . call browser-investigation-checks run --args '{"suite":"doctor"}'
.venv/bin/ai-sdlc --workspace . call browser-investigation-checks run --args '{"suite":"edge-smoke"}'
.venv/bin/ai-sdlc --workspace . call browser-investigation-checks run --args '{"suite":"chromium-smoke"}'
```

On Windows, use `.venv\Scripts\ai-sdlc.exe`.
Generated workspaces have empty catalogs.
Configure their resource path to this optional environment without copying runtime source.
Command actions retain stdout, stderr, and the helper's evidence path.
Preserve the referenced browser artifacts separately before sharing an action record.
Use a scoped workspace timeout for long investigations.

Inspect a retained trace locally:

```sh
node adapters/browser/node_modules/playwright/cli.js show-trace /absolute/path/trace.zip
node adapters/browser/node_modules/playwright/cli.js trace open /absolute/path/trace.zip
node adapters/browser/node_modules/playwright/cli.js trace actions
node adapters/browser/node_modules/playwright/cli.js trace close
```

## Prepare and install without package access

Use a staging computer with the target OS, CPU architecture, and Node major version.
The core offline bundle excludes this optional environment.
Install the locked packages on the staging computer first.
Then prepare a separate bundle explicitly:

```sh
node adapters/browser/bundle.mjs prepare --output /absolute/new/browser-bundle
```

Preparation reuses local `.browsers` assets when available.
It runs the explicit Chromium installer to supply missing pinned assets.
It downloads both locked npm tarballs and verifies their integrity.
It retains browser files, safe internal framework links, source files, and a content-only npm cache.
It excludes package-manager configuration, request metadata, logs, credentials, and profiles.

Transfer the unchanged optional source and complete bundle through the approved process.
Install into a new directory whose parent already exists:

```sh
node adapters/browser/bundle.mjs install --bundle /absolute/browser-bundle --destination /absolute/new/browser-tools
node /absolute/new/browser-tools/browser.mjs doctor
node /absolute/new/browser-tools/browser.mjs smoke --browser chromium --output /absolute/new/offline-smoke
```

Use quoted native Windows paths for the equivalent Node commands.
The installer rejects mismatched targets, changed source, changed files, unsafe links, and existing destinations.
It uses offline npm, empty npm configuration, and a temporary cache copy.
It has no online fallback and runs no package lifecycle scripts.
It does not install Node, npm, or Edge.
Source changes require a new prepared bundle.
Hashes identify bytes; they do not establish company approval or authenticate a publisher.

## Tooling acceptance criteria

```gherkin
Scenario: Observe an isolated browser tab switch
  Given the selected browser and pinned Playwright package are installed
  When the controlled smoke switches tabs and returns after a native two-second wait
  Then the fixture records hidden and visible events at least 2000 milliseconds apart
  And the output retains a screenshot, trace, source hashes, and runtime versions

Scenario: Install from a prepared bundle
  Given the bundle matches the target and source hashes
  And the destination does not exist
  When the operator runs the offline installer
  Then npm installs the locked packages with offline mode enabled
  And the Chromium smoke can launch without a browser download

Scenario: Preserve an existing installation
  Given the requested destination exists
  When the operator runs the offline installer
  Then installation fails before changing that destination
```

These criteria describe tooling assertions.
They establish no approved business requirement or PROD behavior.
