---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Instructions derive from local catalogs, Git metadata, manifests, and source inspected on 2026-10-20.
  - No business application startup, external connection, or native Windows setup was checked for this guide.
---

# Restore the supplied Ratan projects

Use this project-specific guide with the complete Workbench source checkout.
New empty workspaces receive the reusable [repository guide](README.md), without this project inventory.
Install Workbench through [the platform setup guide](../docs/SETUP.md).
Keep the existing project catalogs, knowledge, evidence, relationships, and tasks together when moving this workspace.

## Restore source into the registered paths

The [repository catalog](../registry/repositories.yaml) registers these nine projects.
The five independent Git checkouts had no configured remotes during inspection.
The other four directories had no independent `.git` metadata.
Confirmed upstream URLs and original upstream revisions remain unavailable.

| Repository ID | Restore location from the workspace root | Available source form |
| --- | --- | --- |
| `mfe-root-config` | `repos/ui/mfe-root-config` | Independent Git checkout. |
| `mfe-base` | `repos/ui/mfe-base` | Independent Git checkout. |
| `mfe-ratan-container` | `repos/ui/mfe-ratan-container` | Supplied filesystem copy. |
| `mfe-cashflow-blotter` | `repos/ui/mfe-cashflow-blotter` | Supplied filesystem copy. |
| `single-ui-bff` | `repos/services/single-ui-bff` | Independent Git checkout. |
| `ratan-auth-server` | `repos/services/ratan-auth-server` | Supplied filesystem copy. |
| `single-ui-auth-sdk` | `repos/libraries/single-ui-sdk-starter` | Independent Git checkout. |
| `nginx` | `repos/infra/nginx` | Supplied filesystem copy. |
| `ratan-test-engine` | `repos/testing/ratan-test-engine` | Independent Git checkout. |

Obtain confirmed upstream URLs from the source owners when available.
Clone each upstream into its table location and select the required revision.
Otherwise, follow [Git bundle transfer](README.md#transfer-a-git-checkout-without-an-upstream) for each independent checkout.
Follow [filesystem transfer](README.md#transfer-a-filesystem-copy) for each supplied copy.
Keep the checkout names unchanged; the SDK repository ID differs from its directory name.

Record current commit IDs before transfer.
The inspected local commits were:

| Repository ID | Local `HEAD` on 2026-10-20 |
| --- | --- |
| `single-ui-bff` | `85d7cc03eb12710d6facf581987fd4ae24fc9844` |
| `mfe-base` | `4cddb38dc0e3117708fea00bdbb886f7b4b3d5c5` |
| `mfe-root-config` | `83091d85beff5306ca0cd643955d8ea6ed0a2d93` |
| `single-ui-auth-sdk` | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` |
| `ratan-test-engine` | `7a504c13a8d51bb52af5cc89bd4af88d1988da94` |

These commits identify local history; they do not establish original upstream identity.
Existing [source records](../registry/sources.yaml) retain earlier evidence baselines.
Preserve those historical revisions when restoring current checkouts.
The inspected base checkout also contained modified and untracked files.
The test checkout contained a modified `CLAUDE.md` and an untracked log.
Review and preserve required uncommitted files separately; bundles exclude them.

## Reconnect Workbench

Restore the tracked project workspace through its Git repository or approved transfer process.
Do not run initialization over the restored workspace.
Its six catalogs already declare repository, service, capability, contract, source, and tool IDs.
Retain their cross references when restoring this project.

The [service catalog](../registry/services.yaml) groups root-config and base under `single-ui-web`.
It groups BFF under `single-ui-bff-api`.
The [capability catalog](../registry/capabilities.yaml) connects the relevant implementation and test repositories.
The [contract catalog](../registry/contracts.yaml) retains candidate interfaces and exact source locators.
These records describe relationships; they do not start applications or configure endpoint URLs.

Keep the listed paths to reuse the existing [tool configuration](../registry/tools.yaml).
For alternate paths, update both catalog overrides and affected tool paths through [the repository guide](README.md#configure-executable-tools).
Recreate the workspace root `.env` from [.env.example](../.env.example) for required connector features.
Follow [connector setup](../docs/CONNECTORS.md) for source installation and exact tool grants.

Run these commands with the Workbench environment active:

```sh
ai-sdlc --workspace "PATH" doctor --profile core
ai-sdlc --workspace "PATH" validate
ai-sdlc --workspace "PATH" status
ai-sdlc --workspace "PATH" call ratan-test-engine-repository status
```

Replace `PATH` with the restored workspace directory.
Core validation does not check each application's dependencies or network access.

## Prepare frontend modules

Read each frontend's `package.json` and `webpack.config.js` before installing dependencies.
The supplied frontend manifests declare no Node engine version.
The inspected frontend copies had no package lockfiles.
Obtain the supported Node version and dependency installation procedure from the project maintainer.
Inspect lifecycle scripts before installation; some invoke additional package tools.

Each frontend's `start` script reads `.env.local` from that repository.
Only root-config supplied that file during inspection.
Obtain approved local settings for base, container, and cashflow.
Keep local environment files private within their owning repository.

| Repository | Required configuration from inspected Webpack source |
| --- | --- |
| Root-config | `port`, `mode`, `orgName`, `devtool`, `isLocal`, `publicUrl`, and `importmap`. |
| Base | `port`, `mode`, `orgName`, `devtool`, `cduplatform`, and values loaded through `.env.mfe`. |
| Container and cashflow | `port`, `mode`, `orgName`, `devtool`, and values loaded through `.env.mfe`. |

Select a distinct development port for each module.
Keep `orgName` consistent with the import-map module names.
The root [HTML template](ui/mfe-root-config/src/index.ejs) loads its SystemJS import map from `publicUrl + importmap`.
It also loads shared runtime assets from `publicUrl`.
Obtain the approved import map and required runtime assets before starting the shell.

Configure these entries in a local import-map copy or supported local overrides:

| Module ID | URL to use after selecting development ports |
| --- | --- |
| `@fm/root-config` | `http://localhost:ROOT_PORT/config.js` |
| `@fm/base` | `http://localhost:BASE_PORT/base.js` |
| `@fm/ratan_container` | `http://localhost:CONTAINER_PORT/ratan_container.js` |
| `@fm/ratan_cashflow_blotter` | `http://localhost:CASHFLOW_PORT/ratan_cashflow_blotter.js` |

Replace the port placeholders with the configured values.
Preserve other required shared module entries in the approved import map.
The [container imports base](ui/mfe-ratan-container/src/Root/import/index.ts).
Cashflow imports [base](ui/mfe-cashflow-blotter/src/Root/import/index.ts) and [container components](ui/mfe-cashflow-blotter/src/Root/import/ratancomponents/index.ts).

After dependencies and settings are ready, start each module in a separate terminal from the Workbench root:

```sh
npm --prefix repos/ui/mfe-base start
npm --prefix repos/ui/mfe-ratan-container start
npm --prefix repos/ui/mfe-cashflow-blotter start
npm --prefix repos/ui/mfe-root-config start
```

Check each configured module URL, then open the root-config development URL.
Use the browser's network tools to check resolved module URLs and API destinations.
Root-config's [proxy configuration](ui/mfe-root-config/webpack.config.js) targets corporate gateways for several API routes.
Confirm approved proxy targets and authentication configuration before checking business flows.
Local frontend startup alone does not establish backend connectivity.

## Prepare backend projects and infrastructure

Read the BFF [onboarding guide](services/single-ui-bff/docs/onboarding/README.md).
Use its [configuration guide](services/single-ui-bff/docs/onboarding/configuration-and-secrets.md) for environment requirements.
Use its [build guide](services/single-ui-bff/docs/onboarding/build-delivery-and-operations.md) for repository-owned build procedures.
Read the auth server's [agent guide](services/ratan-auth-server/AGENTS.md) before changes or execution.

| Project source | Declared Java level | Declared Spring Boot version |
| --- | --- | --- |
| BFF [POM](services/single-ui-bff/pom.xml) | `17` | `3.3.4` |
| SDK [parent POM](libraries/single-ui-sdk-starter/pom.xml) | `17` | `4.0.6` |
| Auth server [POM](services/ratan-auth-server/pom.xml) | `21` | `4.0.6` |

These declarations do not establish a compatible or passing target build.
Have the maintainer confirm each project's JDK and Maven setup.
Configure approved artifact access and private service settings before the documented build or startup command.

The auth server requests `com.scb.fmoportal:fmoportal-auth-sdk:1.1.1`.
The supplied SDK parent declares `2.0.0-SNAPSHOT`.
Installing the supplied SDK locally does not satisfy the requested version automatically.
Confirm the intended SDK artifact before connecting these projects.
The BFF and auth package build scripts reference unavailable parent scripts.
Use their repository-owned Maven procedures after resolving prerequisites.

The [Nginx entry](infra/nginx/nginx_ratan.conf.j2) includes rendered configuration files.
The [server template](infra/nginx/ratan_servers.conf.j2) routes authentication and Ratan requests through gateway configuration.
Obtain the deployment renderer, environment variables, certificates, gateways, and backend services from the infrastructure maintainer.
The nine supplied projects do not provide every required gateway or backend.
Do not start a raw Jinja template as an Nginx configuration.

## Prepare the independent test engine

Follow the test repository's [canonical Workbench setup](testing/ratan-test-engine/docs/WORKBENCH.md).
Its full profile uses Python 3.13 and its retained uv lockfile.
Run these commands inside `repos/testing/ratan-test-engine`:

```sh
uv venv --python 3.13 .venv
uv sync --locked --python 3.13
```

The existing tool records use `.venv/bin/python` for macOS.
On Windows, set the native Robot resource's `config.python` to `.venv/Scripts/python.exe`.
That provider resolves the interpreter relative to the test repository.

For `ratan-test-engine-checks`, replace every suite array's first item with the test interpreter's absolute path.
For example, use `C:/Work/workbench/repos/testing/ratan-test-engine/.venv/Scripts/python.exe` for that checkout location.
Keep script arguments relative to the test repository; the command provider uses that directory as its working directory.
`{python}` selects the Workbench interpreter and does not automatically select the test environment.

List the registered smoke suite from the Workbench environment:

```sh
ai-sdlc --workspace "PATH" call ratan-test-engine list
```

Use the canonical test guide for local checks and authorized suite execution.
The framework smoke checks Robot execution only.
Business suites need approved environment files, credentials, endpoints, and task-specific execution scope.

## Resolve setup limits

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Five checkouts have no configured remotes. | Upstream cloning cannot reproduce the local commits yet. | Unknown source owners. | Confirm upstream URLs or transfer independent Git bundles. |
| Four supplied directories have no independent Git metadata. | Their original revision identities remain unknown. | Unknown source owners. | Transfer source archives and confirm upstream provenance. |
| Frontend manifests omit engines and retained lockfiles. | Dependency installation can differ between computers. | Frontend maintainer; identity unknown. | Confirm supported Node and dependency versions. |
| Auth requests SDK `1.1.1`; supplied SDK declares `2.0.0-SNAPSHOT`. | Local SDK installation does not resolve the declared dependency. | Authentication maintainer; identity unknown. | Confirm the required artifact and approved artifact source. |
| Proxy and Nginx sources depend on external gateways and services. | These projects cannot establish a complete local business environment alone. | Infrastructure maintainer; identity unknown. | Supply approved routes and missing environment dependencies. |

## Filesystem evidence identities

The Git commit table identifies inspected committed sources for the five independent checkouts.
These SHA-256 values identify selected filesystem sources used for this guide:

| File | SHA-256 on 2026-10-20 |
| --- | --- |
| `repos/ui/mfe-ratan-container/webpack.config.js` | `9dcac6860a554eadf9de1a54f2f5f8abab18ffdde18c35d9abaa10b415acf00c` |
| `repos/ui/mfe-cashflow-blotter/webpack.config.js` | `9f8a41dad944eeeae349435ab43c93f291e681879b54827b2322b535e34ce7e5` |
| `repos/services/ratan-auth-server/pom.xml` | `b4c36b73a946502da3632b1daec392ef5ea377487ea4daad2d866b556ea660ce` |
| `repos/infra/nginx/ratan_servers.conf.j2` | `9c7fb1c11567d92d68eee67c4e56e06315ce6e55b7c2663e7857542becb9c2f5` |
