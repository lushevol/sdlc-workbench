---
name: connectors
description: Set up Workbench external connectors, maintain root variables, discover tool schemas, invoke scoped operations, and diagnose connector access.
---

# Connector setup and usage

Use this procedure for native external system access through Workbench CLI or MCP.
Supported connectors are `ado`, `confluence`, `scwiki`, `sonar`, `nexus`, `messaging`, and `web`.
Read the [connector guide](../../../docs/CONNECTORS.md) for system variables, platform dependencies, and integration limits.
For an existing installation, inspect its configuration and continue with the requested operation.

## Select and install

Select the target workspace before changing variables or catalogs.
Distinguish the Workbench source checkout from a generated workspace.
The source checkout contains `pyproject.toml`, root `package.json`, and `core/connectors/workbench/bridge.js`.
Generated workspaces contain guides and skills without connector source or Node dependencies.

Use Node 22 or newer.
Reuse the Python environment that runs Workbench.
Run these commands from the standalone source checkout when installation is needed:

```sh
python -m pip install .
npm ci --ignore-scripts --no-audit --no-fund
```

Use `python3` when that is the selected environment's command.
The native bridge requires no connector build.
Do not run `pip install .` or `npm ci` inside a generated workspace.
Install Workbench from its supplied wheel there, and keep a separate connector source checkout.

The source checkout registers seven connector resources.
Generated workspace catalogs start empty.

Use the [registry example](../../../registry/examples/connectors.yaml) for the selected resources.
Merge entries into the tool catalog selected by `workspace.yaml`, and preserve existing records.
Set each generated workspace's bridge command to the source checkout's absolute bridge path.
Keep `command` as an argument array, including paths that contain spaces.
The provider passes the selected workspace root to the bridge.

## Maintain root variables

Use the selected workspace's [root template](../../../.env.example).
Create `.env` only when it does not exist.
Merge missing settings into an existing file and preserve its values, including Release Clinic settings.
Keep credentials in ignored root `.env` or the process environment.
Do not put credentials into catalogs, tool arguments, reports, or diagnostic output.

Configure only the chosen system's variables from the connector guide.
Process values override root values, including explicit empty values.
Nested package files and home configuration do not supply native connector variables.
For generated workspaces, variables come from that workspace, regardless of the connector source location.

Configure optional `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` at the root.
Use `NODE_EXTRA_CA_CERTS` for a required private certificate authority.
Its relative path resolves from the selected workspace root.
Keep TLS certificate validation enabled.
`CODE_REVIEW_GUIDE_FILE` also resolves from the selected workspace root.

## Discover and use tools

Replace `PATH` with the selected workspace directory and quote paths that contain spaces.
Discover actual resource IDs before selecting a connector.

```sh
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH call external-confluence list
```

Resource `list` returns tool names, complete input schemas, and each tool's `allowed` status.
Discovery requires no service credentials and makes no external service requests.
Inspect the requested tool's schema before constructing arguments.
Use the user's actual source identity and requested scope.
For example, replace `PAGE_ID` before this read:

```sh
ai-sdlc --workspace PATH call external-confluence call --args '{"tool":"confluence_get_page","arguments":{"pageId":"PAGE_ID"}}'
ai-sdlc --workspace PATH runs
ai-sdlc --workspace PATH run ACTION_ID
```

Replace `ACTION_ID` with the returned action identity.
For MCP, start `ai-sdlc --workspace /absolute/path/to/workspace mcp` through the configured client adapter.
Use `workbench_status`, then `workbench_call` with `resource_id`, `operation`, and optional `arguments`.
For a tool call, `arguments` contains `tool` and the tool's own `arguments` object.
Use `workbench_runs` to inspect retained actions.
Read the [MCP adapter guide](../../../adapters/mcp/README.md) when configuring a client.

Calls require `call` in `allowed_operations` and exact names in `config.allowed_tools`.
Grant `list` for discovery.
An absent or empty `allowed_tools` list denies every tool call.
Wildcards do not grant other tool names.

Source defaults permit selected reads; Nexus and messaging initially permit discovery only.
Do not broaden grants to resolve a denial unless the requested task authorizes that configuration change.
Keep Confluence source access read-only under the source catalog contract.
Resource grants do not authorize an external write or message beyond the user's request.
For setup verification, use discovery or an authorized read against a supplied source.

## Diagnose access

| Observed result | Next action |
| --- | --- |
| `ai-sdlc` is unavailable. | Activate its Python environment or use that environment's command path. |
| Resource is absent from `status`. | Inspect the selected workspace and merge the required catalog entry. |
| `CONNECTOR_UNAVAILABLE` | Check Node availability and the configured bridge command. |
| `INVALID_CONFIGURATION` | Compare the resource with the registry example. |
| `DENIED` or `TOOL_NOT_GRANTED` | Inspect operation grants and exact tool names against the requested scope. |
| `CONNECTOR_FAILURE` | Check Node dependencies, required root variables, and empty shell overrides without printing secrets. |
| Certificate or proxy access fails. | Check root network settings and certificate paths; retain TLS validation. |
| `CONNECTOR_TIMEOUT` | Check endpoint access and workspace timeout before repeating the requested operation. |
| `RESPONSE_TOO_LARGE` | Reduce the requested scope; parsed responses have a four MiB limit. |

Restart MCP after catalog changes because its workspace configuration is loaded at startup.
Raw startup diagnostics are suppressed because they can contain credentials.
Use the guide's dependency notes for messaging automation, web search, and browser crawling.
The stateful application bridge and upload application are outside this native interface.
Native startup excludes upstream telemetry.

## Retain results and limits

Record selected workspace, resource, tool, source identity, action identity, result, and evidence limits.
Calls retain action results and evidence hashes.
They do not create raw snapshots, provenance manifests, or approved knowledge.
Use the ingestion procedure when the task requires preserved source bytes and candidate knowledge.
Successful execution does not establish approved intent or verified business behavior.

Keep facts, inferences, and unknowns separate.
Give saved findings evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.

For saved reports, keep automated checks separate from writing review.
Set `automated_check` from checks actually performed and leave human review pending:

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
