---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# External system connectors

AI agents use external systems through the existing Workbench CLI and MCP interface.
The `connector.mcp` provider invokes the imported connector tools through a Node bridge.
Workbench checks operation grants and exact tool names before it starts the bridge.
Each action retains its result through the existing evidence store.

The Python runtime remains the core application.
Node is an optional dependency for external connectors.
Connector packages remain under `core/connectors/packages/` in this source checkout.
The Workbench bridge uses their tool modules without their original startup programs.
Native startup sends no telemetry and does not search for organization proxy servers.

## Install from the project root

Use Node 22 or newer and the installed Workbench command.
Run these commands from the standalone source checkout.

```sh
python -m pip install .
npm ci --ignore-scripts --no-audit --no-fund
```

The root `package.json` manages package links and dependencies.
The root `package-lock.json` records dependency versions.
The imported Yarn release configuration does not control this installation.
No connector build is required for the native bridge.

## Maintain variables at the workspace root

Use [the root variable template](../.env.example) to create an ignored `.env` file.
This source checkout already has an empty private `.env` template.
Keep endpoints, credentials, and optional network settings in that file.
Process environment values take precedence, including empty values.
The bridge reads only the selected workspace's `.env` file.
Nested package files and the user's home configuration do not supply native connector variables.

| System | Required variables for calls |
| --- | --- |
| Azure DevOps | `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT` |
| Confluence | `CONFLUENCE_BASE_URL`, `CONFLUENCE_PAT` |
| XWiki | `SCWIKI_URL`, `SCWIKI_TOKEN`; optional `SCWIKI_WIKI` |
| Nexus IQ | `NEXUS_BASE_URL`, `NEXUS_USER_CODE`, `NEXUS_PASS_CODE` |
| SonarQube | `SONAR_BASE_URL`, `SONAR_TOKEN` |
| Web | No service credentials; optional network settings |
| Messaging | Logged-in Outlook or Teams session and platform dependencies |

Configure only the systems you use.
Discovery does not require service credentials or contact external systems.
Calls validate configuration for the selected system.
One system does not require another system's credentials.

Set optional `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` at the root.
Set `NODE_EXTRA_CA_CERTS` in root `.env` when a private certificate authority is required.
Relative certificate paths resolve from the workspace root.
The bridge starts a child process when Node requires the certificate at startup.
The bridge preserves TLS certificate validation.
`CODE_REVIEW_GUIDE_FILE` resolves from the workspace root.
Optional connector context resolves under `.workbench/connectors/` in the selected workspace.

## Discover and invoke tools

This source checkout registers seven connector resources in `registry/tools.yaml`.
Initial grants permit selected reads for Azure DevOps, Confluence, XWiki, SonarQube, and web access.
Nexus and messaging initially permit discovery only.
Use discovery to inspect each tool's complete input schema and `allowed` status.

```sh
ai-sdlc --workspace . status
ai-sdlc --workspace . call external-confluence list
ai-sdlc --workspace . call external-confluence call --args '{"tool":"confluence_get_page","arguments":{"pageId":"123"}}'
ai-sdlc --workspace . runs
```

Agents use the same resources through `workbench_status` and `workbench_call`.
Start the existing MCP adapter with the selected workspace's absolute path.

```sh
ai-sdlc --workspace /absolute/path/to/workspace mcp
```

Grant `call` in `allowed_operations` and exact tool names in `config.allowed_tools` for each resource.
An absent or empty `allowed_tools` list denies every tool call.
Wildcards do not grant other tool names.
Resource grants do not replace the user's authorization for an external write or message.
Keep Confluence source access read-only as required by the source catalog contract.

## Use a generated workspace

Generated workspaces receive this guide and `.env.example`.
Their tool catalogs remain empty.
They do not receive connector source or Node dependencies.
The Python wheel installs the provider; the optional Node tools require this separate source checkout.

Use [the connector registry example](../registry/examples/connectors.yaml) to configure a generated workspace.
Merge selected entries into its tool catalog and replace each bridge path with the source checkout's absolute path.
Create `.env` at the generated workspace root.
The provider passes that root to the bridge, regardless of the connector source location.
Never put credentials into catalogs or call arguments.

## Limits and evidence

Calls start a separate process and use the workspace timeout.
Parsed responses have a four MiB limit.
The provider suppresses raw startup diagnostics because they can contain credentials.
Configure dependencies and variables before investigating a fixed connector failure message.

External content can appear in retained action results.
These results do not create raw snapshots or provenance manifest entries.
Use the ingestion procedure to preserve source bytes and source identities.
Successful tool execution does not establish approved intent or verified business behavior.

Messaging uses platform automation and can require Python packages or operating system permissions.
Web search can require Python dependencies from the imported web package guide.
Browser crawling requires an installed supported browser.
The stateful application bridge and upload application are outside this native interface.
Their original entrypoints are not configured by this integration.

## Acceptance criteria

```gherkin
Scenario: Read variables from the selected workspace
  Given the selected workspace has a root .env file
  And the connector package has a different .env file
  When an agent invokes a configured connector tool
  Then the bridge uses the root file's variables
  And process environment values override matching root values

Scenario: Deny an ungranted external tool
  Given a connector resource grants call
  And its allowed_tools list excludes the requested tool
  When an agent requests that tool
  Then the action fails with TOOL_NOT_GRANTED
  And zero connector processes start

Scenario: Discover tools without external access
  Given no external service credentials are configured
  When an agent lists a supported connector's tools
  Then the result contains tool names and input schemas
  And zero external service requests occur

Scenario: Retain a successful external read
  Given a local fixture supplies a configured service endpoint
  And the resource grants the requested read tool
  When an agent invokes the read tool
  Then the action contains the fixture response
  And retained result evidence includes a SHA-256 hash
```
