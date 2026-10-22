---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source inspection does not establish successful execution on the target company computer.
  - Third-party SDK internals and company endpoint redirects were not exhaustively inspected.
---

# Runtime and network dependencies

This document records the dependency analysis for Windows 11 and macOS.
Use [setup](SETUP.md) for installation commands and local readiness checks.
Keep this analysis current when manifests, connectors, service clients, or browser assets change.

The supported core can run on Windows 11 with approved Python and its installed packages.
Full setup also requires Node and npm for native connectors.
Business tests, desktop automation, and external services have separate prerequisites.
The excluded application bridge and upload application remain outside the native Workbench interface.

## Evidence boundary

The inspection date is `2026-10-18`.
The initial source baseline is commit `746698a836f2336331630b020c86893e04be8741`.
The accompanying offline setup and optional update-check changes extend that baseline.
The root Playwright POM dependency addition was inspected on `2026-10-22`.
The tables describe inspected implementation and declared dependencies.
They do not establish company approval, token validity, endpoint access, or passing business behavior.

Inspection covered package manifests, launchers, providers, connectors, Release Clinic clients, packaged schemas, and local report assets.
Local workspace status supplied registered resource identities.
No external endpoint was contacted for this analysis.
No company credentials, application sessions, or native Windows installation were tested.

## Platform requirements

| Dependency | Windows 11 | macOS | Required function and evidence |
| --- | --- | --- | --- |
| Python | Approved Python >=3.10 with `venv` and `pip` | Same | Core runtime; [E1](#evidence-locators). |
| Node and npm | Approved Node 24 LTS, or Node 22.12+ | Same | Full connector setup; Node 23 is outside the locked toolchain range; [E2](#evidence-locators). |
| Git | Approved Git on `PATH` | Same | Local repository operations and ADO PR cloning; [E3](#evidence-locators). |
| Browser | Approved Chrome, Edge, or HTML browser | Same | Local HTML viewing; browser crawling requires supported Chrome or Edge paths; [E4](#evidence-locators). |
| Outlook | Logged-in COM-compatible Outlook and `pywin32>=305` | Logged-in Outlook and AppleScript permission | Authorized Outlook messaging; [E4](#evidence-locators). |
| Teams | Logged-in Teams and the `msteams://` handler | Same, plus Automation and Accessibility permission | Authorized desktop messaging; [E4](#evidence-locators). |
| Test environment | Target repository's Python, Robot libraries, browser assets, and private configuration | Same | Selected business tests; [E5](#evidence-locators). |
| Target package manager | Target-compatible npm or Yarn | Same | Nexus npm/Yarn scans and fixes; [E6](#evidence-locators). |
| Maven and JDK | Target-compatible Maven and Java | Same | Nexus Maven scans and fixes; [E6](#evidence-locators). |
| Native build tools | Conditional C/C++ or Rust tools | Same | Only when approved compatible binary wheels are unavailable. |
| SQLite | Included with Python | Same | Local action history; no separate database server. |

Static source graph extraction uses Python parsers.
It does not require Java or Maven.
No Docker, Kubernetes, database server, or WSL installation is required for the supported core.
Selected business environments can require these tools independently.

The [code review helpers](../.agents/skills/code-review/references/helpers.md) consume existing Python 3.10+ and installed Git.
They provide comparison identities and redacted pattern candidates without additional packages or runtime network calls.
The structured review validator uses the same standard library and optionally recollects local Git context.
Git must support the documented revision and index comparison options.

Use fresh `.venv` and `node_modules` directories on each computer.
Do not transfer these directories between Windows and macOS.
Select the same operating system, CPU architecture, and Python minor version when preparing an offline bundle.
An installed package does not establish native extension compatibility.

Native wheels, such as `tree-sitter` and `cryptography`, contain platform-specific machine code.
Their compatibility depends on the operating system, Python minor version, CPU architecture, and bitness.
An incompatible wheel can fail installation or import.
Online pip selects compatible wheels automatically.
Offline preparation must use a matching staging interpreter and computer.
Run the read-only `python core/offline.py target` command with the selected interpreter to print its target identity.

## Python and Node packages

| Package group | Declared distributions | Version policy and function |
| --- | --- | --- |
| Core Python | `PyYAML==6.0.2`, `tree-sitter==0.25.2`, `tree-sitter-java==0.23.5`, `tree-sitter-typescript==0.23.2`, `jsonschema==4.25.1` | Exact direct versions; configuration, source parsing, and contracts; [E1](#evidence-locators). |
| Python build | `setuptools>=68` | Build-system dependency; source installation requires its availability; [E1](#evidence-locators). |
| Release Clinic HTTP and parsing | `requests>=2.31.0`, `urllib3>=2.0.0`, `beautifulsoup4>=4.12.0`, `lxml>=5.0.0` | Optional `release-clinic` extra; [E1](#evidence-locators). |
| Release Clinic APIs and matching | `atlassian-python-api>=3.41.0`, `python-sonarqube-api>=2.0.4`, `cryptography>=42.0.0`, `rapidfuzz>=3.0.0` | Confluence, Sonar, ServiceNow credentials, and matching; [E1](#evidence-locators). |
| Release Clinic service | `fastapi>=0.111.0`, `uvicorn>=0.29.0`, `pydantic>=2.7.0` | Optional hosted service; [E1](#evidence-locators). |
| Outlook attachment parsing | `extract-msg>=0.45.0` | Included in the extra; parses retained `.msg` attachments. |
| Windows desktop automation | `pywin32>=305` | Full Windows setup installs this package; [E2](#evidence-locators). |
| Native Node bridge | `@modelcontextprotocol/sdk`, `axios`, `azure-devops-node-api`, `dotenv`, `https-proxy-agent`, `node-fetch`, `zod` | Root manifest and lockfile define resolved versions; [E7](#evidence-locators). |
| Linked Node workspaces | `cheerio`, `selenium-webdriver`, `@modelcontextprotocol/ext-apps`, and development dependencies | Root npm installation includes these packages; installation does not enable excluded interfaces; [E7](#evidence-locators). |
| Root UI test harness | `@playwright/test==1.64.1`, `typescript==5.9.3`, `tsx==4.20.6` | Exact development dependencies for [the POM harness](../e2e/README.md); [E17](#evidence-locators). |

The Python extra uses minimum versions and has no complete checked-in transitive lockfile.
Core transitive Python dependencies also depend on package resolution.
The offline preparation process retains the resolved wheel set for its selected target.
Preserve that bundle and its manifest to reproduce the selected package versions.

The root npm lockfile pins the connector and source UI test dependency graph.
Its inspected resolved entries contain 376 tarball URLs, all under `registry.npmjs.org`.
These entries resolve to 372 unique tarball URLs.
No GitHub-hosted dependency appears in those resolved entries.
This count describes the inspected lockfile; regenerate the inventory after lockfile changes.

Historical requirements also list `pandas`, `tabulate`, `python-docx`, `fuzzywuzzy`, and `python-Levenshtein`.
The supported collector uses `rapidfuzz` and does not require those legacy additions.
Standard-library report generation, audit extraction, and portfolio aggregation have separate local execution paths.
See [E8](#evidence-locators) and [Release Clinic](RELEASE_CLINIC.md).

## Installation downloads

These hosts supply software packages.
They do not supply current release observations or business API results.

| Download class | Public default or inspected host | Trigger | Internal alternative |
| --- | --- | --- | --- |
| Python packages | Usually `pypi.org` and `files.pythonhosted.org` | Online pip resolution and installation | Approved Python mirror or prepared wheel bundle. |
| Node packages | `registry.npmjs.org` in the inspected root lockfile | Root `npm ci` | Approved compatible mirror or prepared npm cache. |
| Operating system runtimes | Company software distribution | Python, Node, Git, browser, JDK, or Maven installation | Company-approved installers. |
| Target project dependencies | Selected project's npm, Yarn, Maven, or other configured registries | Target scans, fixes, or test preparation | Separate approved target dependency caches and mirrors. |
| Browser drivers | Selected business test project's configured source | Driver installation or that project's automatic driver management | Approved matching local drivers and browser assets. |
| Optional Playwright packages | `registry.npmjs.org` | Explicit installation under `adapters/browser`; exact separate lockfile. | Separate prepared browser bundle. |
| Root POM development packages | `registry.npmjs.org` | Root `npm ci`; exact root lockfile. | Full Workbench bundle's npm cache. |
| Optional Chromium assets | `cdn.playwright.dev`; redirects include `storage.googleapis.com`; fallback hosts include `playwright.download.prss.microsoft.com` | Explicit Playwright Chromium installation or browser bundle preparation. | Separate matching-platform browser bundle. |

Pip uses its effective index configuration.
The project does not hardcode the public Python package hosts.
Private indexes, proxies, and certificates must be configured outside credentials-bearing catalog arguments.
Never store credentials inside a shared bundle or its manifest.

Setup runs `npm ci --ignore-scripts --no-audit --no-fund`.
It skips package lifecycle scripts and npm audit calls.
The native bridge reads local package source and needs no GitHub download during normal startup.
The excluded Selenium application bridge requires a supplied local driver path.
It does not establish browser-driver readiness for independent business tests.

## Optional browser investigation environment

The current consumer is the portal session investigation workflow.
Its observable benefit is isolated browser control with timestamped visibility observations, screenshots, and traces.
The source checkout retains [Edge smoke evidence](../tasks/portal-background-session-20261019/evidence/browser-final/edge/result.json).
Its [screenshot](../tasks/portal-background-session-20261019/evidence/browser-final/edge/returned.png) and trace demonstrate tooling capability only.

| Component | Constraint or identity | Scope |
| --- | --- | --- |
| Playwright and playwright-core | `1.64.1`, pinned in `adapters/browser/package-lock.json` | Optional JavaScript API, agent CLI, and MCP implementation. |
| Node | `>=22.12.0`; tested `24.16.0` | Separate optional environment; npm is required for installation. |
| Chromium | Playwright revision `1248`, Chrome for Testing `156.0.8078.4` | Explicit provisioning into local `.browsers`; no driver package. |
| Microsoft Edge | Approved installed branded browser; tested `155.0.4283.62` | Native executable or standard `channel: msedge`; never installed automatically. |
| Platform | macOS and Windows installation commands | macOS `26.5` arm64 tested; native Windows remains untested. |

The npm stable tag resolved to `1.64.1` on `2026-10-19`.
The retained registry response identifies package hashes and the resolved tarball.
The separate lockfile pins two tarballs under `registry.npmjs.org`.
Root npm installation and mandatory Python dependencies remain independent.

Connected preparation explicitly downloads packages and browser assets.
The browser bundle checks OS, architecture, Node major, source hashes, package integrity, and browser file hashes.
Offline installation uses fresh directories, local cache content, empty npm configuration, and no online fallback.
The bundle excludes Edge, Node, npm, credentials, profiles, and business services.
Hashes detect changed bytes; they do not authenticate the publisher.

The controlled smoke serves a local fixture on an ephemeral `127.0.0.1` port.
Browser pages can request configured investigation URLs, redirects, and subresources during later authorized investigations.
Branded browsers can contact vendor services under their own policies.
The helper performs no startup package download or update check.
Playwright suppresses some browser background networking and updater activity by default.
These automation defaults do not establish the user's original browser configuration.

The agent CLI supplies snapshots, element references, tabs, screenshots, and tracing.
The MCP entry point is present; its client integration remains untested in this change.
No optional MCP service starts automatically.
See [the browser guide](BROWSER_INVESTIGATIONS.md) for commands and visibility constraints.

## Root Playwright POM harness

The current consumer is the [refined UI case catalog](../tasks/ui-test-coverage-20261022/test-cases.md).
The [source harness](../e2e/README.md) provides typed UI operations, semantic actions, controlled execution, and fixture checks.
It remains outside the Python wheel and independent business test engines.
Fixture results establish harness behavior only.
They do not establish passing business cases or deployed UI compatibility.

| Component | Constraint or identity | Current use |
| --- | --- | --- |
| `@playwright/test`, `playwright`, `playwright-core` | Exact `1.64.1` in the root lockfile | POM locators, assertions, traces, browser control, and fixture tests. |
| TypeScript | Exact `5.9.3` | Strict static checking through `npm run e2e:typecheck`. |
| tsx | Exact `4.20.6` | Runner execution through Node's import loader, including supported Node 22.12. |
| tsx transitive esbuild | Locked `0.25.12`, with platform optional binary packages | TypeScript loading without runtime downloads; lifecycle scripts remain disabled during installation. |
| Node type declarations | Locked `@types/node==22.20.5` through existing connector development dependencies | Node imports in the strict TypeScript configuration. |
| Node and npm | Approved Node 22.12+ or Node 24+; Node 23 excluded | Same toolchain policy as root installation; Node 24.16.0 was tested. |
| Chromium or Edge | Same Playwright version and browser constraints as the optional adapter | Default Chromium assets use `adapters/browser/.browsers`; `E2E_BROWSER=msedge` selects installed Edge. |

The npm scripts preload [browser configuration](../e2e/browser-config.ts) before Playwright reads its browser cache location.
An explicit `PLAYWRIGHT_BROWSERS_PATH` takes precedence over the default.
The harness uses full Chromium through `channel: chromium`; it does not require the separate headless shell.
Missing packages or browser files cause failure; startup performs no download or update check.
Browser installation remains an explicit operation in [setup](SETUP.md#root-playwright-pom-harness).

The full offline preparation already caches every root lockfile tarball and checks each recorded integrity digest.
The changed root package files invalidate older bundle source fingerprints.
Prepare a fresh matching bundle and transfer the complete checkout, including `e2e/`.
The npm cache excludes browser assets, Edge, credentials, profiles, and live business services.
Provision Chromium through the separate browser bundle, or install approved Edge independently.

Catalog validation and TypeScript checking need no runtime network access.
Browser execution can request configured application URLs and subresources.
Authorized live targets need their own endpoint access and credentials.
The local fixture checks do not contact business systems.
Native Windows execution remains untested.

## Runtime API access

Live collection and connectors need the configured business services.
An offline software bundle cannot replace those services or their access grants.
Some APIs return additional download URLs or redirects.
Use authorized target-environment observations to complete the endpoint list.

| Consumer | Endpoint or host | Trigger and data | Evidence |
| --- | --- | --- | --- |
| ADO connectors and collector | `AZURE_DEVOPS_ORG_URL` or collector `ADO_ORG_URL`; cloud default `dev.azure.com` | Selected work-item, repository, pipeline, test, wiki, or release operations. | [E3](#evidence-locators), [E9](#evidence-locators). |
| ADO search connector | `almsearch.dev.azure.com` | Cloud code or work-item search. | [E3](#evidence-locators). |
| ADO identity lookup | `vssps.dev.azure.com` | Selected identity lookup during repository writes. | [E3](#evidence-locators). |
| ADO artifact download | Service-returned `resource.downloadUrl` | Build artifact and retained evidence downloads; host depends on the response. | [E10](#evidence-locators). |
| Confluence | `CONFLUENCE_BASE_URL`; collector alias `CONFLUENCE_URL` | Page reads and report collection; short links can redirect. | [E9](#evidence-locators). |
| SonarQube | `SONAR_BASE_URL`; collector alias `SONAR_URL` | Project quality and analysis reads. | [E9](#evidence-locators). |
| XWiki | `SCWIKI_URL` | Selected REST page reads. | [E9](#evidence-locators). |
| Nexus IQ | `NEXUS_BASE_URL` | Selected policy scans and vulnerability operations. | [E6](#evidence-locators). |
| Genie | `GENIE_REPORT_LINK`; `GENIE_TEST_MANAGEMENT_URL_TEMPLATE` | Release or latest test results; default test-management host `report.genie.cloud.sc.net`. | [E9](#evidence-locators). |
| Artifactory | `ARTIFACTORY_BASE_URL` | Optional build metadata discovery; default `artifactory.global.standardchartered.com`. | [E10](#evidence-locators). |
| ServiceNow | `SN_INSTANCE` and `SNOW_API_PATH` | OAuth token and change records when enabled; default host `scbnow01.service-now.com`. | [E9](#evidence-locators). |
| Vault | `VAULT_ADDR` | Service startup authentication and later credential reads; default `https://vault-dev.sc.net:8200`. | [E11](#evidence-locators). |
| Eureka | Discovery resource's configured HTTP/S URL | Explicit `instances` operation appends `/apps`. | [E12](#evidence-locators). |
| Web search | `lite.duckduckgo.com/lite/` | Explicit web search operation. | [E4](#evidence-locators). |
| Web crawl | Authorized URL and its redirects or browser subresources | Explicit crawl operation. | [E4](#evidence-locators). |
| Business tests | Selected test environment's endpoints | Registered test command or Robot suite. | [E5](#evidence-locators). |

Artifactory discovery requires the stream setting `artifactory_build_discovery_enabled: true`.
It reads build properties through the storage API.
This operation does not install Workbench packages.
ServiceNow also depends on the selected stream's enabled state.

The collector's optional canonical skill check uses `dev.azure.com`.
Set `TDA_CHECK_SKILL_UPDATES=true` only when that check is required and authorized.
The default collector path skips this remote check.
The check reports version information; it does not download or install an update.
Its helper retains a cloud ADO URL, independent of the configured collector host.

The explicit eSDLC refresh script also uses cloud ADO.
It reads curated files from `ESDM/ESDM.wiki` under `dev.azure.com`.
It does not run during ordinary local report generation.
The package already contains raw wiki snapshots, their manifest, and the derived control registry.
Preserve those bytes and add new snapshots when sources change.

## Browser assets and documentation

The graph viewer embeds its CSS, JavaScript, and graph data.
The initial TDA HTML report also uses local generated content.
Their inspected renderers contain no external script or stylesheet dependency.
Following report hyperlinks still requires the linked business service.
See [E8](#evidence-locators) and [E13](#evidence-locators).

The optional FastAPI service has a separate documentation dependency.
Its constructor leaves the default `/docs` and `/redoc` routes enabled.
Inspection of installed FastAPI `0.143.3` found these browser asset URLs:

| Documentation route | Browser request | Purpose |
| --- | --- | --- |
| `/docs` | `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js` | Swagger UI JavaScript. |
| `/docs` | `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css` | Swagger UI stylesheet. |
| `/docs` and `/redoc` | `https://fastapi.tiangolo.com/img/favicon.png` | Browser tab icon. |
| `/redoc` | `https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js` | ReDoc JavaScript. |
| `/redoc` | `https://fonts.googleapis.com/css?family=Montserrat:300,400,700\|Roboto:300,400,700` | Font stylesheet; `with_google_fonts` defaults to `True`. |

These requests start when a browser opens the documentation.
They are separate from service API calls and local package installation.
Returned stylesheets or JavaScript can request additional assets.
Those downstream requests were not observed during this source inspection.

The current service does not configure self-hosted documentation assets.
An internal deployment can vendor approved assets and override or disable the default documentation routes.
Keep the local OpenAPI endpoint available when the selected API workflow requires it.
See [E14](#evidence-locators) and the official documentation links below.

## Schemas and retained local data

The inspected schema inventory contained 18 files and 326 schema references.
All inspected `$ref`, `$dynamicRef`, and `$recursiveRef` values started with `#`.
No external schema reference appeared in that inventory.
The `$schema` URLs identify JSON Schema versions; current validation does not download them.
This result applies to the shipped inventory, not future externally referenced schemas.

Workbench reads packaged schemas from local paths.
Its bounded operation validator rejects unsupported schema keywords, including `$ref`.
Artifact, assurance, and graph checks use local schemas with `Draft202012Validator`.
Governance validation does not fetch declared external resource names.
See [E15](#evidence-locators).

| Operation | Offline condition | Limit |
| --- | --- | --- |
| Local records, validation, action history, and local Git inspection | Installed runtime and available local inputs | No current external observation is created. |
| Static source graph and embedded viewer | Installed parsers and available repositories | Graph evidence covers inspected local revisions. |
| TDA HTML report | Retained collector JSON and installed report assets | Report content remains limited by retained input evidence. |
| Portfolio aggregation | Retained JSONL or report inputs | No service refresh occurs. |
| Audit extraction | Retained HTML and `--skip-download` | New ADO work-item discovery and downloads are omitted. |
| eSDLC reference consultation | Shipped raw snapshots and manifest | Snapshot freshness remains limited by its recorded revision. |
| Fresh collection, search, discovery, and remote tests | Required service unavailable | Offline software cannot supply current remote results. |

Collector `--rwi-only` still contacts ADO.
Collector `--use-yaml` replaces build discovery inputs only.
Neither option makes fresh collection fully offline.
An OKF `verified` state does not establish successful business execution.

## Offline installation boundary

The offline bundle caches Python wheels and the root connector npm dependencies.
Prepare it on a connected computer that matches the target operating system, CPU, and Python minor version.
Use approved company registries during preparation.
Preserve the complete source checkout separately.
The Python wheel does not contain native Node connector source.

Run `python core/offline.py prepare --output offline-bundle` with the approved matching interpreter.
Use `--core-only` when the target needs only the core profile.
Preparation builds the Workbench wheel and downloads binary dependency wheels for the staging interpreter.
It also caches every locked npm tarball for the full profile.
Preparation fails when a compatible required wheel or locked tarball is unavailable.

After download, preparation resolves Python dependencies again from local wheels with isolated offline package settings.
This check rejects incomplete or incompatible wheel sets, including those caused by inherited resolver overrides.

Transfer the unchanged source checkout and complete bundle.
Setup detects the checkout's `offline-bundle` directory automatically.
Use `--offline-bundle PATH` when the bundle is elsewhere.
The bundle and setup profiles must match.
No prepared Windows bundle was produced during this audit.

Validation compares source fingerprints, file hashes, operating system, CPU architecture, interpreter implementation, Python minor version, bitness, and ABI.
It also compares the Python platform identifier.
These checks run before setup creates or changes the Python environment.
Hashes detect changed bytes; they do not authenticate the publisher or establish company approval.

Offline pip and npm commands have no online fallback.
Offline pip uses `--force-reinstall` for bundled Python packages.
This replaces installed Workbench code when source changes keep the same package version.
Offline setup excludes inherited package-manager environment overrides.
Pip disables configuration files; npm uses empty user and global configuration files.

Setup copies the npm cache temporarily to preserve bundle bytes.
See [E16](#evidence-locators) for the preparation and validation implementation.

The npm bundle retains cached content bytes only.
It excludes cache index metadata, npm logs, and package-manager configuration.
Keep private credentials outside all shared installation assets.

The bundle does not include Python, Node, Git, browsers, drivers, Outlook, Teams, Maven, or a JDK.
It does not include independent repository dependencies, private credentials, business datasets, or external services.
Use the target repository's separate cache procedure for its package managers and browser assets.
Do not transfer a macOS cache as proof of Windows readiness.

Validate offline installation with network access unavailable and fresh `.venv` and `node_modules` directories.
Run setup, doctor, and workspace validation on the target computer.
Then run only authorized operations against required internal services.
Local readiness checks do not validate credentials or grants.
See [setup](SETUP.md) for the supported offline commands.

## Findings and next actions

| Finding and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Native Windows execution was not observed. Source and local checks are the current evidence. | Target-PC readiness remains unconfirmed. | unknown | Run setup, doctor, validation, and selected authorized operations on the company Windows 11 computer. |
| Python extras have minimum versions; [E1](#evidence-locators). | Fresh online resolution can select different transitive versions. | unknown | Retain the approved offline wheel set and manifest; consider a maintained target-specific lock policy. |
| npm lock URLs use the public registry; [E7](#evidence-locators). | Restricted installation can fail without package availability. | unknown | Prepare the supported bundle or validate an approved compatible internal mirror. |
| API hosts and download URLs depend on configuration and responses; [E3](#evidence-locators), [E10](#evidence-locators). | Literal source hosts cannot establish a complete endpoint list. | unknown | Record authorized requests and redirects for selected company operations. |
| Default FastAPI documentation uses public browser assets; [E14](#evidence-locators). | `/docs` or `/redoc` can fail on restricted computers. | unknown | Vendor approved assets or disable unused documentation routes before internal hosting. |
| Cloud-only optional refresh helpers remain; [E10](#evidence-locators). | Internal ADO Server settings cannot redirect every helper. | unknown | Keep optional probes disabled; adapt explicit refresh tools only when required. |
| Release Clinic and web helpers disable some TLS checks; [setup findings](SETUP.md#remaining-gaps-and-recovery-actions). | Affected requests do not validate the server certificate. | unknown | Review company requirements and implement verified certificate handling where required. |
| Vault ignores environment proxies; [E11](#evidence-locators). | A shared proxy setting cannot establish service startup access. | unknown | Check approved direct Vault routing or implement the required proxy support. |
| Business repositories retain separate dependency environments; [E5](#evidence-locators), [E6](#evidence-locators). | Workbench installation cannot enable every business test or scan. | unknown | Inventory each selected repository's tools, packages, endpoints, and execution permissions. |
| Desktop interfaces require real applications; [E4](#evidence-locators). | Package checks cannot establish Outlook or Teams automation. | unknown | Check application compatibility and permissions without sending setup messages. |

## Evidence locators

Paths below refer to the complete source checkout.
Generated workspaces omit the cited runtime and manifest files.
Use the complete source checkout to inspect those code locators.
Locators identify inspected functions or line positions in the audit baseline.
Later edits can change line positions.

| ID | Source and locator | Support and limit |
| --- | --- | --- |
| E1 | `pyproject.toml`, `build-system`, `requires-python`, dependency groups | Declared direct Python requirements; no target execution evidence. |
| E2 | `core/bootstrap.py`, `npm_command`, `install` | Runtime checks, pip/npm installation, Windows extra; command construction only. |
| E3 | `core/connectors/packages/ado-core/src/connection.js`; `core/connectors/packages/ado-search/src/tools/search.js`, lines 38 and 82; `core/connectors/packages/ado-repos-write/src/tools/repos-write.js`, lines 4 and 42; `core/connectors/packages/ado-review/src/tools/review.js`, line 297 | Configured ADO clients, auxiliary cloud hosts, and Git cloning. |
| E4 | `core/connectors/packages/web/scripts/search-ddg.py`, line 48; `core/connectors/packages/web/src/tools/webcrawlbrowser.js`; `core/connectors/packages/messaging/scripts`; [setup](SETUP.md#browsers-desktop-applications-and-test-environments) | Native browser and desktop prerequisites; application sessions untested. |
| E5 | `core/providers/testing.py`; `core/providers/robot.py`; [Robot guide](ROBOT_TESTING.md) | Selected executable environments remain independent. |
| E6 | `core/connectors/packages/nexus/src/tools/scan.js`, lines 481, 489, and 636; `core/connectors/packages/nexus/src/tools/fix-vulnerabilities.js`, lines 325, 358, and 706 | Target npm, Yarn, Maven commands; registry settings belong to the target. |
| E7 | `package.json`; `package-lock.json`, representative tarball at line 253 | Node declared and resolved dependencies; host count covers this lockfile. |
| E8 | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/gen_tda_report.py`, lines 1949 and 2025; `core/release-clinic/plugins/test/dtp-tda-service/scripts/aggregate_portfolio.py`, lines 34 and 58; `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda_audit/run_tda_audit.py`, lines 854 and 880 | Local inputs, output generation, and audit download branch. |
| E9 | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/config.py`, lines 358–455; `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/integrations`; `core/release-clinic/release_clinic_env.py` | Configured service hosts and API clients; effective company values untested. |
| E10 | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/http_client.py`, `get_remote_skill_version`, `download_build_artifact_zip`, `get_artifactory_build_info`; `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/version_check.py`, `check_skill_staleness`; `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/build_resolver.py`, line 705; `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/esdlc_kb/fetch_esdlc_kb.py`, lines 77–148 | Optional cloud probe, service-returned downloads, metadata reads, explicit refresh. |
| E11 | `core/release-clinic/plugins/test/dtp-tda-service/service/main.py`, `lifespan`; `core/release-clinic/plugins/test/dtp-tda-service/service/vault_client.py`, lines 65–147 | Startup authentication, routing settings, and credential reads. |
| E12 | `core/providers/discovery.py`, lines 31–57 | Configured HTTP/S registry access on explicit invocation. |
| E13 | [graph renderer](../.agents/skills/service-dependencies-graph/tools/render_graph.py), lines 14–41; [viewer](../.agents/skills/service-dependencies-graph/tools/viewer.html) | Embedded CSS, JavaScript, and graph data; no external asset call observed in these files. |
| E14 | `core/release-clinic/plugins/test/dtp-tda-service/service/main.py`, lines 136–145; installed FastAPI `0.143.3`, `fastapi/openapi/docs.py`, lines 79, 92, 100, 236, 244, 252, and 277 | Default documentation assets from the inspected installed version; other permitted versions need reinspection. |
| E15 | `core/models.py`, lines 69–111; `core/artifact_lint.py`, lines 46 and 323; `core/assurance.py`, lines 29 and 153; `core/governance/validation.py`, line 149; [graph validator](../.agents/skills/service-dependencies-graph/tools/validate_graph.py), lines 18–35 | Local schema loaders and bounded validation; inventory covered `core/schemas`, `registry`, `core/knowledge/schemas`, and graph schemas. |
| E16 | `core/offline.py`, `prepare`, `target`, `validate_bundle`; `core/bootstrap.py`, `install`, `main` | Matching-target bundles, source and file checks, offline package commands, and automatic bundle selection. |
| E17 | [root manifest](../package.json), [root lockfile](../package-lock.json), [POM configuration](../e2e/playwright.config.ts), [TypeScript configuration](../e2e/tsconfig.json) | Exact harness dependencies, browser selection, local checks, and retained output locations. |

## Official documentation links

These are documentation references, not required runtime endpoints.
Their presence does not mean Workbench downloads them.
The audit did not fetch these pages.

| Topic | Official documentation |
| --- | --- |
| Python on Windows | [Using Python on Windows](https://docs.python.org/3/using/windows.html) |
| Python environments | [venv](https://docs.python.org/3/library/venv.html) |
| Offline pip installation | [pip install options](https://pip.pypa.io/en/stable/cli/pip_install/#install-no-index) |
| Wheel download preparation | [pip download](https://pip.pypa.io/en/stable/cli/pip_download/) |
| Node releases | [Node.js releases](https://nodejs.org/en/about/previous-releases) |
| npm installation and cache behavior | [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci), [npm cache](https://docs.npmjs.com/cli/v11/commands/npm-cache), [npm offline option](https://docs.npmjs.com/cli/v11/using-npm/config#offline) |
| FastAPI local documentation assets | [Custom Docs UI Static Assets](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) |
| JSON Schema identifiers and references | [JSON Schema structuring](https://json-schema.org/understanding-json-schema/structuring) |

## Automated document checks

Checks covered local link targets, heading anchors, code fences, prose line lengths, paragraph lengths, and whitespace differences.
The static inventory counted schema references and npm resolved URL hosts.
The read-only target command printed the current macOS interpreter identity.
No native Windows installation or external endpoint test ran.
The complete ASD-STE100 writing review remains pending.
