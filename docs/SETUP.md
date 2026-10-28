---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native Windows and macOS setup require checks on the target company computer.
---

# Set up Workbench on Windows 11 or macOS

Use this guide with the complete standalone source checkout.
Python and Node must already be installed through your approved company process.
Setup installs project packages into the checkout's `.venv` and `node_modules` directories.
It does not install Python, Node, browsers, drivers, or business applications.

Setup preserves existing `.env`, catalogs, and repository path settings.
It does not clone business repositories or configure service credentials.
New workspaces include `repos/README.md` for independent ADO checkout setup and registration.
Use [repository setup](../repos/README.md) after initialization.
It covers grouped checkouts, linked catalogs, executable tools, application configuration, and transfer without an upstream.
An installed dependency does not grant an operation or establish access to an external system.

The [code review skill](../.agents/skills/code-review/SKILL.md) uses existing Python and Git installations for its local helpers.
Its helpers require no additional packages, service accounts, or runtime downloads.
The packaged skill includes optional structured report validation and conditional language-specific review guidance.

## Start setup

Keep the checkout in a local directory where your account can write.
Preserve the complete checkout, including `core/connectors`, `package-lock.json`, and shared skills.
Paths with spaces are supported when quoted in commands.

Use a fresh source checkout on each operating system.
Do not copy `.venv` or `node_modules` between computers.
Set the target computer's repository paths in ignored `workspace.local.yaml` where supported.

| Step | Windows 11 | macOS |
| --- | --- | --- |
| Run setup | Double-click `setup.cmd`, or run `.\setup.cmd` in PowerShell. | Double-click `setup.command`, or run `./setup.command` in Terminal. |
| Check setup | `.\setup.cmd --check` | `./setup.command --check` |
| Install core only | `.\setup.cmd --core-only` | `./setup.command --core-only` |
| Select another workspace | `.\setup.cmd --workspace "C:\Work\team-workspace"` | `./setup.command --workspace "/Users/you/Work/team-workspace"` |

Run terminal commands from the source checkout.
If macOS blocks direct execution, run `bash setup.command` from that directory.
Keep company application controls enabled and use their approved exception process when required.

Default setup installs the core, Release Clinic, `.msg` parsing, and Node connector dependencies.
Windows setup also installs `pywin32` for Outlook automation.
Core-only setup omits Release Clinic, desktop Python extras, and Node package installation.

[Release reporting](RELEASE_REPORT.md) uses the existing Node connector dependencies for collection.
Offline rendering requires only the Python core and a complete saved report bundle.
Generated workspaces require explicit connector resources that point to a separately installed source checkout.

Use `--check` for diagnostics without package installation.
Check mode uses the installed `.venv` when available.
It reports missing installation prerequisites when that environment is absent.
It writes no setup report and returns nonzero when the selected readiness checks are incomplete.

`--workspace PATH` selects the workspace used for diagnostics and configuration.
Setup initializes that location only when it is missing or empty.
It refuses an existing nonempty directory without workspace configuration.
It keeps the Python environment and Node packages in the source checkout.

Online setup needs access to your configured Python package index and npm registry.
Company certificates, proxy settings, and package permissions must already permit those downloads.
Setup uses `npm ci --ignore-scripts --no-audit --no-fund` with the root lockfile.
It does not run imported package startup programs or build the excluded application integrations.

For restricted computers, use [offline installation](#install-without-package-registry-access).
See [the dependency analysis](DEPENDENCIES.md) for package hosts, runtime APIs, browser assets, and evidence limits.

After installation stages complete, setup prints readiness and saves JSON and Markdown reports under source `.workbench/setup/`.
The reports identify the run and feature prerequisites.
Review optional feature findings even when package installation succeeds.
Installation returns zero only when package installation completes and core readiness passes.
Optional features can still report `INCOMPLETE`.
If Node is missing, full setup installs Python packages and reports connector installation incomplete with a nonzero result.

Setup suppresses package manager output because index and proxy addresses can contain private values.
Installation failures identify the failed stage and recovery action.
Early failures print guidance without a setup report.
Inspect private package manager configuration locally when the fixed diagnostic cannot resolve the failure.

## Install without package registry access

Prepare an offline bundle on a connected staging computer.
The staging computer must match the target operating system, CPU architecture, approved Python minor version, and interpreter implementation.
The bundle also records bitness, Python ABI, and platform identity.
Do not prepare a Windows bundle on macOS or Linux.
Use a complete source checkout and approved package access during preparation.

Run these commands from the source checkout with the approved interpreter selected.
On Windows, `py -3` must select the same Python minor version as target setup.
Use an explicit approved Python executable when multiple installations need selection.

Native wheels, such as `tree-sitter` and `cryptography`, contain machine code for specific platforms.
The wrong operating system, Python minor version, CPU architecture, or bitness can prevent installation or import.
Online pip selects compatible packages automatically.
Offline preparation needs the matching staging computer and interpreter.

Print target details without package downloads or configuration changes:

| Read target identity | Windows 11 | macOS |
| --- | --- | --- |
| Selected launcher interpreter | `py -3 core\offline.py target` | `python3 core/offline.py target` |

Compare this output between the target and staging computers.
The offline setup validator also rejects a target mismatch.

| Preparation | Windows staging computer | macOS staging computer |
| --- | --- | --- |
| Full bundle | `py -3 core\offline.py prepare --output offline-bundle` | `python3 core/offline.py prepare --output offline-bundle` |
| Core bundle | `py -3 core\offline.py prepare --output offline-bundle --core-only` | `python3 core/offline.py prepare --output offline-bundle --core-only` |

Preparation builds the Workbench wheel and downloads binary dependency wheels for the selected staging interpreter.
After download, preparation resolves Python dependencies again from local wheels with isolated offline package settings.
This check rejects incomplete or incompatible wheel sets, including those caused by inherited resolver overrides.

The full bundle also caches every tarball in the root npm lockfile.
It includes optional npm platform packages and checks their recorded integrity hashes.
The bundle retains cache content without index metadata, logs, or package-manager configuration.

Preparation stops when approved binary wheels or locked tarballs are unavailable.
It preserves any existing output directory.
Select a new output directory for another bundle.

Transfer the complete unchanged source checkout and bundle through your approved company process.
Do not transfer `.venv`, `node_modules`, `.env`, or private package-manager settings.
The default `offline-bundle` directory is ignored by Git.
Keep it inside the transferred checkout for automatic setup selection.
Then double-click the platform setup launcher or use the commands below.

| Installation | Windows 11 | macOS |
| --- | --- | --- |
| Automatic bundle selection | `.\setup.cmd` | `./setup.command` |
| Bundle elsewhere | `.\setup.cmd --offline-bundle "C:\Work\offline-bundle"` | `./setup.command --offline-bundle "/Users/you/Work/offline-bundle"` |
| Core bundle | `.\setup.cmd --core-only` | `./setup.command --core-only` |

The bundle profile must match the selected setup profile.
A full bundle needs full setup; a core bundle needs `--core-only`.
Use `--offline-bundle PATH` with `--core-only` when a core bundle is elsewhere.
Setup rejects changed bundle files, mismatched source inputs, or a different target identity before environment creation.
Hashes detect changed bytes; they do not authenticate the publisher or establish company approval.

Offline setup uses pip without indexes and npm with `--offline`.
It does not retry through online registries.
It excludes inherited package-manager environment overrides.
Pip disables configuration files; npm uses empty user and global configuration files.

It preserves the bundle while npm uses a temporary cache copy.
An incomplete cache requires a new preparation run on the staging computer.
Use fresh environment directories to check the complete bundle.

The bundle supplies project packages only.
Install approved Python, Node, Git, browsers, desktop applications, and required business toolchains separately.
Independent test repositories and Nexus targets need their own dependency caches.
Fresh collection still requires access to selected internal services and valid credentials.
FastAPI browser documentation currently uses public assets; its local `/openapi.json` endpoint avoids that documentation UI.
See [runtime access and assets](DEPENDENCIES.md#runtime-api-access) before internal hosting.

No native Windows bundle was produced during this source audit.
Run setup, doctor, validation, and selected authorized operations on the target company computer.

## Use the installed commands

Activate `.venv` before using `ai-sdlc` or starting an agent's MCP process.
Activation also puts the selected Python first on `PATH` for connector helper scripts.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
ai-sdlc --workspace . doctor
ai-sdlc --workspace . status
ai-sdlc --workspace . validate
```

If company policy blocks activation, use the executable paths directly.
Do not change the execution policy only to run Workbench.
Put the environment scripts first on `PATH` for connector helpers.

```powershell
$env:Path = (Resolve-Path '.\.venv\Scripts').Path + [IO.Path]::PathSeparator + $env:Path
.\.venv\Scripts\ai-sdlc.exe --workspace . doctor
.\.venv\Scripts\ai-sdlc.exe --workspace . validate
```

macOS:

```sh
source .venv/bin/activate
ai-sdlc --workspace . doctor
ai-sdlc --workspace . status
ai-sdlc --workspace . validate
```

The doctor checks local feature prerequisites.
Its default profile includes optional integrations.
Use `ai-sdlc --workspace . doctor --profile core` after a core-only installation.
If CLI dependencies cannot load, use the standalone diagnostic module:

```powershell
.\.venv\Scripts\python.exe -m ai_sdlc_workbench.doctor --workspace . --profile core
```

On macOS, use `.venv/bin/python -m ai_sdlc_workbench.doctor --workspace . --profile core`.

| Status | Meaning | Required action |
| --- | --- | --- |
| `READY` | The checked local prerequisites are present. | Check the selected operation's business inputs and external access separately. |
| `INCOMPLETE` | A checked prerequisite is missing or invalid. | Follow the reported recovery action and run doctor again. |
| `NOT_CONFIGURED` | The feature has no selected resource or configuration. | Configure it only when required for your work. |
| `UNSUPPORTED` | The checked integration is outside the supported interface or platform. | Use the supported alternative described in the finding. |

The default profile includes two unsupported application integrations.
Its aggregate result remains `INCOMPLETE` while these interfaces remain unsupported.
Read each feature and `core_status` to identify usable functionality.

Doctor does not contact service endpoints or validate tokens.
It cannot establish browser interaction, desktop permissions, business test results, or company approval.
Python package checks inspect distribution metadata; they do not import every native extension.
Browser and desktop checks inspect local prerequisites without opening applications.
An optional feature can remain incomplete while core operations are usable.
`validate` checks workspace records and contracts; it does not replace doctor.

## Restore independent projects on another computer

Restore the tracked project workspace before restoring its independent repositories.
Use `ai-sdlc init "PATH"` only for a new empty workspace.
Initialization supplies reusable guides and empty catalogs; it does not recover an existing project's registrations.

Follow [the repository sequence](../repos/README.md#quick-setup-on-another-computer) for a new or existing project.
Keep the same relative paths under `repos/` to reuse portable catalog and tool settings.
Use [Git bundles or filesystem transfer](../repos/README.md#preserve-a-project-for-another-computer) when confirmed upstreams are unavailable.
Recreate private credentials and business dependency environments on the target computer.

Check both catalog locations and executable tool paths when checkout locations differ.
`workspace.local.yaml` changes repository metadata only.
It does not update `registry/tools.yaml`, interpreter paths, or connector bridge paths.
Run doctor, workspace validation, and selected local tool checks after restoration.

## Runtime dependencies

The package manifests define the installed versions.
The tables distinguish shared dependencies from optional business environments.
Setup does not install each business repository's toolchain.

| Component | Windows 11 | macOS | Purpose and installation |
| --- | --- | --- | --- |
| Python | Approved Python >=3.10 with `venv` and `pip` | Approved Python >=3.10 with `venv` and `pip` | Required core runtime; installed before setup. |
| Node and npm | Approved Node 24 LTS; alternatively Node 22.12+ | Same | Full setup and connector tools; Node 23 is outside the locked toolchain range. |
| Git | Approved Git on `PATH` | Approved Git on `PATH` | Repository operations and source identity; optional for local records. |
| Target package manager | Target-compatible npm or Yarn on `PATH` | Same | Nexus scans and fixes of npm/Yarn business projects; separate from Workbench's root npm installation. |
| Maven and Java | Maven on `PATH` plus a compatible JDK | Same | Nexus Maven target scans and fixes; versions follow the target repository. |
| SQLite | Python standard library | Python standard library | Local action history; no database server installation. |
| Shell | Windows command processor; PowerShell for examples | Bash for setup launcher | Native launchers; WSL is not required for supported core operations. |
| Company package access | Configured pip and npm indexes | Configured pip and npm indexes | Required during package installation. |
| C/C++ or Rust build tools | Conditional | Conditional | Needed only when selected native packages lack compatible approved wheels. |

Prefer approved binary wheels for the target Python version and CPU architecture.
The project does not promise wheels for every future Python release.
Python installation compatibility does not establish compatibility for every business test repository.

Static source graph extraction uses the Python parsers and does not require Java or Maven.
Nexus target scanning can install or resolve target dependencies.
Nexus fixes can change target manifests and lockfiles.
Obtain authorization for those changes and follow the owning repository's instructions.

| Core Python distribution | Version | Runtime use |
| --- | --- | --- |
| `PyYAML` | `6.0.2` | Workspace, catalogs, and YAML configuration. |
| `tree-sitter` | `0.25.2` | Source parsing. |
| `tree-sitter-java` | `0.23.5` | Java source grammar. |
| `tree-sitter-typescript` | `0.23.2` | TypeScript and TSX source grammars. |
| `jsonschema` | `4.25.1` | Document and catalog contracts. |

These versions come from the source checkout's `pyproject.toml`.
`setuptools>=68` is a package build dependency.
It is not a separate application service.

| Release Clinic Python distribution | Minimum version | Runtime use |
| --- | --- | --- |
| `requests` | `2.31.0` | External HTTP APIs. |
| `urllib3` | `2.0.0` | HTTP retries and transport. |
| `beautifulsoup4` | `4.12.0` | HTML extraction. |
| `lxml` | `5.0.0` | Preferred HTML parser. |
| `atlassian-python-api` | `3.41.0` | Confluence API client. |
| `python-sonarqube-api` | `2.0.4` | SonarQube API client. |
| `cryptography` | `42.0.0` | ServiceNow secret decryption. |
| `rapidfuzz` | `3.0.0` | Fuzzy matching. |
| `fastapi` | `0.111.0` | Optional hosted service. |
| `uvicorn` | `0.29.0` | Optional hosted service server. |
| `pydantic` | `2.7.0` | Service request and response models. |
| `extract-msg` | `0.45.0` | Outlook `.msg` attachment parsing; included by the extra and full setup. |

The `release-clinic` extra supplies the collection and service packages.
The extra also supplies `extract-msg` for attachment parsing.
Missing `extract-msg` leaves `.msg` attachments detected but unparsed.
`.eml` parsing uses the Python standard library.
Local report generation, offline audit extraction, and portfolio aggregation use standard library modules.

Historical requirements also list `pandas`, `tabulate`, `python-docx`, `fuzzywuzzy`, and `python-Levenshtein`.
The supported current collector uses `rapidfuzz` and does not require those legacy additions.
Read [Release Clinic](RELEASE_CLINIC.md) before selecting collector or service configuration.

| Node dependency group | Packages | Installation and scope |
| --- | --- | --- |
| Native connector bridge | `@modelcontextprotocol/sdk`, `axios`, `azure-devops-node-api`, `dotenv`, `https-proxy-agent`, `node-fetch`, `zod` | Root `npm ci`; exact resolved versions come from `package-lock.json`. |
| Web extraction | `cheerio` | Installed through the linked web workspace. |
| Imported application packages | `selenium-webdriver`, `@modelcontextprotocol/ext-apps` | Installed packages do not enable the excluded application bridge or upload application. |
| Connector development checks | `vitest` and workspace development dependencies | Installed by root `npm ci`; required for corresponding test commands. |
| Root UI POM harness | `@playwright/test==1.64.1`, `typescript==5.9.3`, `tsx==4.20.6` | Installed by root `npm ci`; separate explicit browser provisioning is required. |

Use the source checkout's root `package.json` and `package-lock.json`.
Do not run imported Yarn, Lerna, or package build procedures for native connector setup.
The Node bridge reads package source directly.

## Configure company services and grants

Copy [.env.example](../.env.example) to `.env` only when `.env` does not exist.
Merge missing variable names into an existing file and preserve its values.
Keep credentials in the selected workspace's ignored `.env` or approved process environment.
Process environment values override file values, including explicit empty values.
Never place credentials in catalogs or tool call arguments.

| Feature | Endpoint and authentication | Additional condition |
| --- | --- | --- |
| Azure DevOps connector | `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT` | Token permissions must cover the selected granted tool. |
| Confluence connector | `CONFLUENCE_BASE_URL`, `CONFLUENCE_PAT` | Retain read-only source access. |
| XWiki connector | `SCWIKI_URL`, `SCWIKI_TOKEN`; optional `SCWIKI_WIKI` | API key and page access. |
| Nexus IQ connector | `NEXUS_BASE_URL`, `NEXUS_USER_CODE`, `NEXUS_PASS_CODE` | Initial catalog grants discovery only. |
| Nexus target scanning and fixes | Existing npm/Yarn or Maven project plus Nexus access | Requires the target's package manager, package registry access, and separate operation authorization. |
| SonarQube connector | `SONAR_BASE_URL`, `SONAR_TOKEN` | Project read access. |
| Release Clinic | ADO settings plus `ADO_PROJECT`, Confluence, Sonar, and Genie settings | Also requires release/build identities and a valid stream. |
| Release Clinic Confluence | Connector aliases plus `USER_EMAIL`, optional `CONFLUENCE_SPACE_KEY` | The local collector doctor does not check every authentication condition. |
| Release Clinic Genie | `GENIE_REPORT_LINK`, `GENIE_TOKEN` | Reachable reporting API. |
| Release Clinic ServiceNow | `SN_INSTANCE`, `SNOW_API_PATH`, `CLIENT_ID`, `FERNET_KEY`, `SNOW_BLADE_KEY` | Required when the selected stream enables ServiceNow. |
| Release Clinic service | `VAULT_ADDR`, `VAULT_NAMESPACE`, `HC_ROLE_ID`, `HC_SECRET_ID`, `HC_VAULT_AUTH_PATH`, `HC_VAULT_SECRET_PATH` | Direct Vault access and AppRole policy. |
| Local service development | `VAULT_DEV_MODE=true` and required environment credentials | Development mode only; does not grant production hosting approval. |
| Eureka discovery | Configured registry URL and required service access | The business deployment must supply its registry. |
| Business tests and databases | Test repository dependencies, private configuration, credentials, and reachable services | Owned by the selected business environment. |

Set `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` when required by company routing.
Set `NODE_EXTRA_CA_CERTS` for private certificate authorities used by the native Node bridge.
Configure installation certificates through approved pip and npm settings before setup.
Release Clinic and imported browser helpers have separate TLS limitations listed below.

Release Clinic skips the optional canonical skill update check by default.
Set `TDA_CHECK_SKILL_UPDATES=true` only when that cloud ADO check is required and authorized.
The setting does not disable configured service access for fresh collection.

Discover the selected workspace's resources before invoking tools:

```sh
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH call external-confluence list
```

Replace `PATH` with the selected workspace directory.
Replace the resource ID when using a different configured resource.
Inspect each tool's argument schema and `allowed` value.
Grant `call` through `allowed_operations` and exact tool names through `config.allowed_tools` only for authorized work.
Installation does not expand existing grants.
See [the connector guide](CONNECTORS.md) for detailed variables and generated workspace configuration.

## Browsers, desktop applications, and test environments

| Function | Windows 11 | macOS | Setup boundary |
| --- | --- | --- | --- |
| HTML report viewing | Approved browser | Approved browser | Open retained HTML locally; setup does not install a browser. |
| Web search | Python helper and network access to DuckDuckGo | Same | Uses standard library modules; external search can remain blocked by company policy. |
| `web_crawl_browser` | Chrome or Edge in a supported installation path | Chrome or Edge in a supported installation path | Starts the browser directly; no WebDriver required. |
| Outlook messaging | Logged-in COM-compatible Outlook; `pywin32>=305` | Logged-in Outlook; permitted AppleScript automation | Full setup installs `pywin32` on Windows; app compatibility remains a target-PC check. |
| Teams messaging | Logged-in Teams desktop app and `msteams://` handler | Logged-in Teams plus Accessibility and Automation permissions | Uses desktop automation; it can affect the foreground session. |
| Robot tests | Selected repository's Python, Robot, libraries, and browser assets | Same | Install inside the test repository environment. |
| Selenium business tests | Required browser plus matching driver when the test project requires it | Same | Follow the owning repository's instructions. |
| Stateful application bridge | Outside the native Workbench interface | Outside the native Workbench interface | Imported Selenium package and browser drivers do not enable this interface. |
| Embedded ADO upload application | Outside the native Workbench interface | Outside the native Workbench interface | Requires separate application integration; setup does not configure it. |

Messaging discovery and package installation do not send messages.
Send a message only after explicit user authorization and the required tool grants.
Do not use a message send as a setup test.

Repository Git operations require Git and an existing independent checkout.
ADO PR review also clones and fetches repositories through Git.
Configure company-approved Git authentication for those repository URLs before review.
An API PAT variable does not automatically configure Git clone credentials.

Record machine locations in ignored `workspace.local.yaml` where supported.
Configure executable provider paths separately in `registry/tools.yaml`.
Metadata path overrides do not rewrite executable paths.
On Windows, Robot's configured Python commonly uses `.venv/Scripts/python.exe` inside the test repository.
See [Robot testing](ROBOT_TESTING.md) for suite grants and evidence limits.

## Optional browser investigations

Use [the browser guide](BROWSER_INVESTIGATIONS.md) for isolated Playwright tooling and dedicated Edge sessions.
This environment uses `adapters/browser/package.json` and its own lockfile.
It remains separate from root npm installation, Python installation, and independent Robot environments.

Run these commands from the source checkout:

```sh
npm --prefix adapters/browser ci --ignore-scripts --no-audit --no-fund
```

Provision Chromium explicitly with the platform commands in the browser guide.
Install approved Edge separately when its declared installation is absent.
The browser helper never downloads missing software during startup.

The core offline bundle excludes this optional environment.
Prepare and install its separate bundle with `adapters/browser/bundle.mjs`.
The browser guide defines matching-platform checks, readiness commands, and evidence limits.

## Root Playwright POM harness

The [root E2E guide](../e2e/README.md) describes the AI action catalog, page objects, fixtures, and evidence.
Use its [test commands](../e2e/README.md#select-and-run-tests) and [AI execution requests](../e2e/README.md#ask-ai-to-execute-cases) after setup.
This source harness remains outside the Python package and the existing business test engines.
It uses root npm dependencies and shares the adapter's exact Playwright browser version.

Install root packages through the normal setup command, or run this command from the source checkout:

```sh
npm ci --ignore-scripts --no-audit --no-fund
```

Use existing Chromium assets in `adapters/browser/.browsers` when available.
Otherwise, provision Chromium explicitly with the matching platform command below.
These commands download browser assets; test and runner startup never download software.

macOS:

```sh
PLAYWRIGHT_BROWSERS_PATH="$PWD/adapters/browser/.browsers" node node_modules/@playwright/test/cli.js install chromium --no-shell
```

Windows PowerShell:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) "adapters/browser/.browsers"
node node_modules/@playwright/test/cli.js install chromium --no-shell
```

Alternatively, set `E2E_BROWSER=msedge` in the process environment to use approved installed Edge.
Set `E2E_HEADED=1` for a visible browser.
An explicit `PLAYWRIGHT_BROWSERS_PATH` overrides the shared default.
Use the npm scripts so browser configuration loads before Playwright initializes.

The application compatibility audit also supports explicitly provisioned Firefox and WebKit automation builds.
Install their assets before running those cases:

```sh
PLAYWRIGHT_BROWSERS_PATH="$PWD/adapters/browser/.browsers" node node_modules/@playwright/test/cli.js install firefox webkit
```

On PowerShell, set `PLAYWRIGHT_BROWSERS_PATH` as shown above, then run the same Node installation command.
Set `E2E_COMPAT_BROWSER=firefox` or `E2E_COMPAT_BROWSER=webkit` for `e2e/audit-specs/browser-compatibility.spec.ts`.
This selection affects that application audit only.
The default POM checks and browser adapter still use Chromium or installed Edge.
WebKit results apply to the recorded automation build; they do not establish installed Safari compatibility.

Run the read-only static checks first:

```sh
npm run e2e:typecheck
npm run e2e:ai -- validate
npm run e2e:test -- --list
```

Run the complete harness check when the selected browser is available:

```sh
npm run e2e:check
```

The supplied specs use local fixtures.
Their results establish POM harness behavior; they do not execute the canonical business UI cases.
The existing Workbench doctor does not assess this optional root harness.
The browser tests establish browser launch and fixture interaction for the selected platform only.
Native Windows execution remains untested.

The [full offline bundle](#install-without-package-registry-access) includes all new root npm tarballs.
Prepare a new bundle after the package files change.
Transfer the matching complete checkout, including `e2e/`.
The full bundle excludes browser assets and live services.
Use the separate [browser bundle](BROWSER_INVESTIGATIONS.md) for Chromium, or provision approved Edge separately.
Install optional Firefox and WebKit assets before preparing a bundle that must include those engines.
The existing browser bundle copies and hashes the complete installed browser cache.
Its offline installer needs no browser download.
The [retained runtime checks](../tasks/ui-test-coverage-20261022/evidence/step-audit-20261022/browser-runtime-feasibility/README.md) verify both engines after connected and prepared-bundle installation.
These checks cover macOS 26.5 arm64; other platforms remain untested.
See [dependency analysis](DEPENDENCIES.md#root-playwright-pom-harness) for versions, download hosts, and runtime network limits.

## Source checkouts and generated workspaces

The Python wheel contains the Workbench runtime and Release Clinic assets.
It does not contain the Node connector source or `node_modules`.
Keep the source checkout available when using connectors from an installed wheel.
Generated workspaces contain records and guides, with empty tool catalogs.
They do not contain source, package manifests, runtime tests, or copied Node dependencies.

Use the installed command to create a workspace:

```sh
ai-sdlc init PATH
ai-sdlc --workspace PATH doctor
ai-sdlc --workspace PATH validate
```

Configure generated workspace connectors from [the registry example](../registry/examples/connectors.yaml).
Set each bridge path to the source checkout's absolute location.
Use the generated workspace's root `.env` for its private settings.
Do not run source setup or `pip install .` inside a generated workspace.

## Remaining gaps and recovery actions

These findings describe setup limits and known source conditions.
They do not establish failing business behavior on your computer.
Owner identities remain unknown until your team assigns them.
Source paths below refer to the complete source checkout, including when this guide appears in a generated workspace.

| Finding and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Credentials and endpoint access are outside local doctor checks. See [connectors](CONNECTORS.md) and [Release Clinic](RELEASE_CLINIC.md). | `READY` cannot establish service access. | unknown | Obtain scoped credentials, configure routing, and perform an authorized read against each required service. |
| Tool grants and generated catalogs require project configuration. See [the registry guide](../registry/README.md). | Installed tools can remain unavailable or denied. | unknown | Register selected resources and grant only authorized operations and exact tools. |
| Independent repositories retain separate environments. See [Robot testing](ROBOT_TESTING.md). | Framework installation cannot run every business test. | unknown | Supply repository paths, dependency environments, private variables, and selected business endpoints. |
| Nexus target tools run npm, Yarn, or Maven. See `core/connectors/packages/nexus/src/tools/scan.js:459` and `core/connectors/packages/nexus/src/tools/fix-vulnerabilities.js:325`. | Missing target tools or registry access can block scans and fixes; operations can change target files. | unknown | Install the target-compatible package manager or Maven and Java, then authorize the selected operation. |
| ADO PR review clones through Git. See `core/connectors/packages/ado-review/src/tools/review.js:297`. | API token presence cannot establish authenticated Git cloning. | unknown | Configure company-approved Git credentials and check authorized clone access before PR review. |
| Browser and desktop checks require real applications and permissions. See the platform table above. | Package presence cannot establish automation compatibility. | unknown | Check approved browser paths, matching test drivers, Outlook COM, Teams login, and macOS permissions. |
| The wheel excludes Node source. See [connector distribution](CONNECTORS.md#use-a-generated-workspace). | Wheel-only installation cannot supply connector tools. | unknown | Keep this source checkout and point connector resources to its absolute bridge path. |
| Application bridge and upload entrypoints are outside the native interface. See [connector limits](CONNECTORS.md#limits-and-evidence). | Installing their packages does not enable these applications. | unknown | Use supported native tools or scope a separate integration. |
| Native Windows and macOS execution need target-PC evidence. See `docs/IMPLEMENTATION_REVIEW.md`. | Static checks and mocked platform tests cannot establish target-PC readiness. | unknown | Run setup, doctor, validation, and selected authorized operations on each target platform. |
| Release Clinic clients disable TLS checks. See `core/release-clinic/plugins/test/dtp-tda-service/service/vault_client.py:75` and `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/integrations/confluence.py:24`. | Certificate validation does not protect those current paths. | unknown | Review company requirements before use and implement verified certificate handling when required. |
| Web helpers disable certificate checks. See `core/connectors/packages/web/scripts/search-ddg.py:36` and `core/connectors/packages/web/src/tools/webcrawlbrowser.js:95`. | The affected requests do not validate server certificates; crawling also passes `--no-sandbox`. | unknown | Review these settings before enabling affected tools in the company environment. |
| Vault ignores environment proxies; ADO changes `HTTPS_PROXY`. See `core/release-clinic/plugins/test/dtp-tda-service/service/vault_client.py:75` and `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/http_client.py:178`. | A single root proxy setting cannot establish routing for every integration. | unknown | Check direct Vault access and each collector's effective routing in the company network. |
| Generic command timeouts kill the direct Windows process. See `core/providers/testing.py`. | Descendant processes can remain after a timeout. | unknown | Inspect and stop the selected process tree; require Windows cleanup evidence before unattended execution. |
| Package installation uses current approved registries and compatible wheels. See `pyproject.toml` and `package-lock.json`. | Restricted registries or missing wheels can block installation. | unknown | Request approved package availability or use a supported Python version with compatible binary packages. |

For Release Clinic setup, also run its existing operation-specific check:

```sh
ai-sdlc --workspace PATH release-clinic doctor
ai-sdlc --workspace PATH release-clinic collect --help
```

Use an interactive terminal for collection because build selection can require operator decisions.
Start the hosted service only for an authorized hosting task.
Its default listener is `127.0.0.1:8080`.
Preserve collected JSON, attachments, configuration identity, and execution details under the applicable evidence rules.

## Setup acceptance criteria

The scenarios define acceptance checks.
Their presence does not establish completed execution on either platform.

```gherkin
Scenario: Install into the source checkout
  Given approved Python 3.10 or newer and Node 24 LTS are installed
  And the configured package indexes are reachable
  When the operator runs the platform setup launcher
  Then the checkout has a .venv with the installed Workbench runtime
  And the checkout has Node dependencies installed from the root lockfile
  And zero operating system runtimes are downloaded

Scenario: Preserve private configuration
  Given .env, registry/tools.yaml, and workspace.local.yaml already exist
  And their initial SHA-256 hashes are recorded
  When setup completes
  Then each existing file has its initial SHA-256 hash
  And setup grants zero additional resource operations

Scenario: Check without package installation
  Given the source checkout exists
  When the operator runs the setup launcher with --check
  Then setup reports its observed prerequisites
  And zero package installation commands run

Scenario: Install the core profile
  Given approved Python 3.10 or newer is installed
  When the operator runs the setup launcher with --core-only
  Then the checkout has the installed Workbench core
  And zero Node package installation commands run
  And Release Clinic installation is not required for the core profile

Scenario: Keep local readiness separate from external access
  Given a selected workspace has configured external service variables
  When the operator runs ai-sdlc doctor
  Then each checked feature has a readiness status
  And zero external service requests occur
  And the result does not claim token validity or verified business behavior

Scenario: Preserve unsupported integration status
  Given the imported application packages are installed
  When the operator reads doctor results for excluded application integrations
  Then the results identify their unsupported native interface
  And package presence does not change those results to READY

Scenario: Install project packages from an offline bundle
  Given a matching source checkout and complete matching-target bundle exist
  And approved Python and Node are installed
  And .venv and node_modules are absent
  And package registry access is unavailable
  When the operator runs setup with the matching offline bundle profile
  Then Python packages install from the wheelhouse without indexes
  And Node packages install from the cache with offline mode
  And zero online package fallback commands run

Scenario: Reject an incompatible offline bundle
  Given an offline bundle differs in source fingerprint, target identity, profile, or retained file hashes
  And the initial .venv and node_modules state is recorded
  When the operator selects that bundle for setup
  Then setup reports the bundle mismatch
  And .venv and node_modules retain their initial state
```
