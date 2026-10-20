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

# Set up and run the supplied Ratan projects

Use this project-specific guide with the complete Workbench source checkout.
New empty workspaces receive the reusable [repository guide](README.md), without this project inventory.
Install Workbench through [the platform setup guide](../docs/SETUP.md).
Keep the existing project catalogs, knowledge, evidence, relationships, and tasks together when moving this workspace.

## Application start sequence

This procedure runs the four frontends and Single UI BFF locally.
It retains approved company services for database, identity, entitlements, and omitted Ratan backends.
The example ports are local setup choices; change all matching settings when a port is occupied.

| Component | Example local address |
| --- | --- |
| Portal root | `http://localhost:8000` |
| Base module | `http://localhost:8002/base.js` |
| Ratan container | `http://localhost:8003/ratan_container.js` |
| Cashflow blotter | `http://localhost:8015/ratan_cashflow_blotter.js` |
| Single UI BFF | `http://127.0.0.1:8088` |

1. Restore source and Workbench records through the following sections.
2. [Install frontend dependencies](#install-frontend-dependencies).
3. [Create frontend configuration](#create-frontend-configuration).
4. [Configure and start Single UI BFF](#configure-and-start-single-ui-bff).
5. [Route frontend APIs to the local BFF](#route-frontend-apis-to-the-local-bff).
6. [Start the frontends and check connections](#start-the-frontends-and-check-connections).

These commands require the private development inputs listed below.
The procedure has source and syntax checks; full application startup remains unverified.

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

## Install frontend dependencies

Read each frontend's `package.json` and `webpack.config.js` before installing dependencies.
The supplied frontend manifests declare no Node engine version.
Their project roots have no npm lockfiles; nested server lockfiles cover separate packages.
Obtain the supported Node version and approved package registry settings from the frontend maintainer.
Base requires private package access, including `@sctoolkit/webkit`.
Check the selected tools from the Workbench root:

```sh
node --version
npm --version
```

Each root has a `preinstall` script that invokes `npx npm-force-resolutions`.
This script can download the helper and modify the npm lockfile.
The supplied container and cashflow copies also run `husky install` during `prepare`.
Without child `.git` metadata, that command can find Workbench Git and then fail.
For those copies, merge this guarded `prepare` value into each `package.json` before installation:

```json
{
  "scripts": {
    "prepare": "node -e \"if (require('fs').existsSync('.git')) require('husky').install()\""
  }
}
```

Preserve all other scripts, including `preinstall`.
The guard installs hooks only when the package has its own Git metadata.
Do not create replacement Git history merely to satisfy hook installation.

Generate the initial lockfile without lifecycle scripts, then run the normal installation.
The following commands install development tools required by Webpack:

```sh
npm --prefix repos/ui/mfe-root-config install --package-lock-only --ignore-scripts --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-root-config install --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-base install --package-lock-only --ignore-scripts --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-base install --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-ratan-container install --package-lock-only --ignore-scripts --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-ratan-container install --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-cashflow-blotter install --package-lock-only --ignore-scripts --include=dev --no-audit --no-fund
npm --prefix repos/ui/mfe-cashflow-blotter install --include=dev --no-audit --no-fund
```

These options follow [npm installation behavior](https://docs.npmjs.com/cli/v10/commands/npm-install/).
Inspect installation failures before changing dependency versions or adding peer-dependency bypass flags.
The manifests contain the version placeholder `PACKAGE_VERSION`; use the repository's versioning procedure if npm rejects it.
Review and preserve resulting lockfiles through each repository's process.
Use [npm ci](https://docs.npmjs.com/cli/v10/commands/npm-ci/) on later computers only after a matching lockfile exists.

## Create frontend configuration

Each frontend's `start` script reads `.env.local` from that repository.
Only root-config supplied that file during inspection.
Create or update the files below within their owning checkouts.
Keep local settings outside business source commits unless the repository explicitly tracks them.

Set `repos/ui/mfe-root-config/.env.local`:

```dotenv
port=8000
mode=development
orgName=fm
devtool=source-map
isLocal=true
publicUrl=http://localhost:8000
importmap=/importmaplocal.json
```

Set `repos/ui/mfe-base/.env.local`:

```dotenv
port=8002
mode=development
orgName=fm
devtool=source-map
```

Use the same four keys for container and cashflow, with ports `8003` and `8015` respectively.
Base also reads `cduplatform` for its Module Federation remote.
Set the maintainer's confirmed `name@URL` value when using the CDU integration.
The supplied Webpack configuration always declares that remote, including when the environment value is missing.
If CDU is outside this local setup, update only its `ModuleFederationPlugin.remotes` setting in base's `webpack.config.js`:

```javascript
remotes: cduplatform ? { cduplatform } : {},
```

Keep the other plugin settings.
This conditional configuration omits an unset CDU remote; CDU features still require the confirmed remote.

Each React module also loads `.env.mfe` through `dotenv-webpack`.
Set `repos/ui/mfe-base/.env.mfe`:

```dotenv
orgName=fm
MFE_APP_PREFIX_STYLE=MicroWebUI_Base
```

Create container and cashflow `.env.mfe` files with the following values:

| Repository | `orgName` | `MFE_APP_PREFIX_STYLE` |
| --- | --- | --- |
| Container | `fm` | `MicroWebUI_ratan_container` |
| Cashflow | `fm` | `MicroWebUI` |

These examples retain class names referenced by [base styles](ui/mfe-base/src/components/Dialog/common/style.ts).
They also match [cashflow selectors](ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CustomSearchView/style.ts) with [container classes](ui/mfe-ratan-container/src/ratancomponents/ViewSelector/common/ViewSelectorStyle.ts).
Confirm styling in the browser after startup.
The base browser code reads `orgName` through this separate environment loader.

Update the existing `repos/ui/mfe-root-config/public/importmaplocal.json`.
Merge these four entries into its `imports` object and preserve the other required shared entries:

```json
{
  "imports": {
    "@fm/root-config": "/config.js",
    "@fm/base": "http://localhost:8002/base.js",
    "@fm/ratan_container": "http://localhost:8003/ratan_container.js",
    "@fm/ratan_cashflow_blotter": "http://localhost:8015/ratan_cashflow_blotter.js"
  }
}
```

The [HTML template](ui/mfe-root-config/src/index.ejs) loads this map and runtime scripts from the root server.
Its existing `public/js/external/` directory supplies the shared React, single-spa, and SystemJS files.
The [copy helper](ui/mfe-root-config/scripts/copy.js) copies `public/` into the served `dist/` directory.
Leave `BUILD_PATH` unset for this procedure.
The supplied helper uses that variable for both source and destination.

For direct module loading, merge this setting into each React module's existing `devServer` object:

```javascript
headers: {
  "Access-Control-Allow-Origin": "http://localhost:8000",
},
```

Keep its existing `port` setting.
Each module's `output.publicPath` already uses its configured localhost port for chunks.
Restart the development server after changing Webpack or environment files.

## Configure and start Single UI BFF

The BFF runs separately from the frontend development servers.
Run the following commands inside `repos/services/single-ui-bff`.
Use JDK 17 for this BFF and Maven configured for its approved artifact repositories:

```sh
java -version
mvn -version
mvn --settings "MAVEN_SETTINGS_XML" clean install
```

Replace `MAVEN_SETTINGS_XML` with the absolute path to your private Maven settings file.
Omit that option if Maven already loads the correct user settings.
`clean install` resolves dependencies, builds the application, and runs the configured tests.
The [BFF guide](services/single-ui-bff/AGENTS.md) documents this build and the Spring Boot start command.
Do not use its npm build wrapper; that wrapper references an unavailable parent script.

The [POM](services/single-ui-bff/pom.xml) also runs source formatting and an Ansible download during its lifecycle.
It replaces `ado-playbooks` while extracting that download.
Review the resulting child repository diff and preserve existing local changes before building.
Private starter artifacts and the Ansible download require approved company artifact access.

Create a private `.local/application-local.yml` inside the BFF checkout.
Add `/.local/` to that checkout's `.git/info/exclude` before saving private configuration.
The following overlay uses an existing, pre-migrated development database:

```yaml
server:
  address: 127.0.0.1
  port: 8088
  servlet:
    context-path: /

spring:
  application:
    name: single-ui-bff
  datasource:
    url: ${BFF_JDBC_URL}
    username: ${BFF_DB_USERNAME}
    password: ${BFF_DB_PASSWORD}
    driver-class-name: org.postgresql.Driver
  flyway:
    enabled: false
    baseline-on-migrate: false
  ldap:
    urls: ${BFF_OUD_URL}

jwt:
  prv: ${JWT_PRIVATE_KEY}
  pub: ${JWT_PUBLIC_KEY}

ratanone:
  open-apis:
    auto-startup: false

management:
  endpoints:
    web:
      exposure:
        include: [health, info]
  endpoint:
    health:
      show-details: never
      probes:
        enabled: true
```

Supply the referenced environment variables before starting Maven.
Spring does not automatically load the Workbench root `.env` file.
Use the terminal's private environment or your approved secret-loading process.
The overlay disables automatic database migrations and gateway registration during this local startup.
For a new database, use the approved migration procedure before starting with this example.

This overlay supplements `application-dev.yml`; it does not define all private starter settings.
Resolve these remaining inputs against the selected development environment:

| Configuration area | Required inputs or review |
| --- | --- |
| Database | `BFF_JDBC_URL`, `BFF_DB_USERNAME`, `BFF_DB_PASSWORD`, schema, and approved migrations. |
| LDAP | `BFF_OUD_URL`, `auth.oud.*`, certificates, and approved authentication configuration. |
| Signing keys | `JWT_PRIVATE_KEY` and `JWT_PUBLIC_KEY` as Base64-encoded PKCS#8 private and X.509 public RSA bytes. |
| Entitlements | `scb.ems2.*`, including endpoint templates and the required admin entity. |
| Analytics | `auth.elastic.*` endpoint and authentication settings when analytics is used. |
| MFA and Entra | Selected `scb.mfa.*` or `scb.entra.*` endpoints, client settings, certificates, redirect URIs, and proxy. |
| Other inherited inputs | `RATAN_CIPHER_KEY`, `API_GATEWAY_URL`, `API_GATEWAY_TOKEN`, and applicable FMAA settings. |
| Private starters | Approved HashiCorp, discovery, logging, trust, and external configuration settings. |

Use nonproduction credentials and a matching signing key pair.
Keep approved authentication and session policies; do not add whitelist entries to bypass failed login.
The development profile enables creation features and contains inherited endpoint settings that require review.
Helm-generated bootstrap configuration does not automatically apply to a Maven start.

Start the BFF in its own terminal:

```sh
mvn --settings "MAVEN_SETTINGS_XML" spring-boot:run "-Dspring-boot.run.profiles=dev,local" "-Dspring-boot.run.arguments=--spring.config.additional-location=file:./.local/application-local.yml --server.address=127.0.0.1 --server.port=8088"
```

The command explicitly selects the profile, local configuration file, bind address, and port.
Its options follow the [Spring Boot Maven plugin](https://docs.spring.io/spring-boot/3.3/maven-plugin/run.html).
The additional file follows [Spring configuration precedence](https://docs.spring.io/spring-boot/3.3/reference/features/external-config.html).
Review existing process environment and external profile files for overrides before startup.
Keep the terminal open and check its startup errors before starting the portal.

Check the local process from another terminal:

```sh
curl --fail http://127.0.0.1:8088/actuator/health
curl --fail http://127.0.0.1:8088/actuator/health/liveness
curl --fail http://127.0.0.1:8088/actuator/health/readiness
```

On Windows PowerShell, use `curl.exe` for these commands.
An exposed healthy endpoint checks application health contributors; it does not prove login or entitlements work.
If approved security settings protect these endpoints, use their configured health check procedure.

## Route frontend APIs to the local BFF

Edit `repos/ui/mfe-root-config/webpack.config.js` for this local setup.
Add the following entry first in its existing `devServer.proxy` array:

```javascript
{
  context: ["/api/auth/", "/api/analytics/"],
  target: "http://127.0.0.1:8088",
  pathRewrite: {
    "^/api/auth": "",
    "^/api/analytics": "",
  },
  changeOrigin: true,
},
```

Remove `/api/auth/` and `/api/analytics/` from the broad corporate proxy entry below it.
Remove the obsolete `/api/au_th/` entry; its context does not match the application's normal authentication requests.
Keep the remaining corporate proxy entries for services that still run remotely.

| Browser request through the root server | Request received by the local BFF |
| --- | --- |
| `/api/auth/v2/sso/login` | `/v2/sso/login` |
| `/api/auth/v3/sso/login` | `/v3/sso/login` |
| `/api/auth/v1/fmo/admin/importmap/active` | `/v1/fmo/admin/importmap/active` |
| `/api/analytics/v1/fmo/print` | `/v1/fmo/print` |

The [BFF controllers](services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller) declare these unprefixed application routes.
Keep authentication headers and request bodies unchanged.
The browser uses the root server's origin for API requests, while Webpack forwards them to the BFF.

Keep `/api/ratan/` and `/api/ratan/bff/` on the confirmed Ratan gateway.
They are not supplied Single UI BFF routes.
For Ratan socket use, enable `ws: true` on that gateway's proxy or add a specific socket rule first.
The authentication proxy does not supply Ratan WebSocket services.

## Start the frontends and check connections

From the Workbench root, copy the existing public assets before opening the browser:

```sh
npm --prefix repos/ui/mfe-root-config run copy
```

Start each module in a separate terminal:

```sh
npm --prefix repos/ui/mfe-base start
npm --prefix repos/ui/mfe-ratan-container start
npm --prefix repos/ui/mfe-cashflow-blotter start
npm --prefix repos/ui/mfe-root-config start
```

Open `http://localhost:8000` after all required servers report readiness.
Use `localhost` for the browser URL.
The base [environment selector](ui/mfe-base/src/utils/common.ts) maps `localhost` to `LOCAL`; unknown hosts select `PROD`.
The root `start` script also copies public assets while starting Webpack.

| Check | Expected observation |
| --- | --- |
| Root assets | `/importmaplocal.json` and `/js/external/system.min.js` load from port `8000`. |
| Frontend bundles | The four addresses in the start sequence return JavaScript. |
| Dynamic chunks | Browser requests use the owning module's configured localhost port. |
| BFF destination | Browser `/api/auth/` requests reach local BFF logs with the prefix removed. |
| Login and entitlements | Approved test credentials succeed against the configured identity and EMS2 services. |
| Ratan features | Required remote APIs and WebSocket upgrades reach their separately configured gateway. |

Use browser network tools and the BFF terminal to check the destination and response.
Stop each foreground server with `Ctrl+C` when finished.
Treat failed private artifact access, configuration, database, key parsing, or external login as distinct setup failures.
Retained session fixture results used synthetic adapters; they do not validate this full BFF startup procedure.

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
| Frontend root manifests omit engines and root lockfiles. | Dependency installation can differ between computers. | Frontend maintainer; identity unknown. | Confirm supported Node and dependency versions. |
| The root copy helper imports `fs-extra` without a direct manifest dependency. | Public asset copying can fail after a fresh installation. | Frontend maintainer; identity unknown. | Declare an approved direct dependency if installation does not supply it. |
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
