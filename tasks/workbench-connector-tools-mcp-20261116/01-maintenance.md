---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - No live external connector call was made.
---

# Core Connector tools as project MCP

> **Critical conclusion: the granted connector tools are now one project MCP server.**
>
> `ai-sdlc mcp --connectors` lists the four Workbench tools and 61 granted connector tools.
> Calls use the existing connector provider, so catalog grants, `.env` isolation, and action evidence stay in force.
> The project registers the server in `.mcp.json`, `.claude/settings.json`, `.codex/config.toml`, and `opencode.json`.
> Evidence: [user input](evidence/user-input.md).

## Request and scope

- Date: 16 November 2026 (Asia/Singapore).
- Exact user input: [user request](evidence/user-input.md#exact-user-input).
- Authorized scope: harness maintenance only.
- Business behavior, connector credentials, and deployment authorization remain outside this scope.

## Outcome

The user selected direct, grant-filtered tools and four clients.
`ai-sdlc mcp --connectors` keeps the four built-in Workbench tools and adds each connector tool whose catalog grant is true.

Discovery uses the existing `list` operation and retains its action record.
Calls use the existing `call` operation.
`TOOL_NOT_GRANTED`, environment isolation, timeouts, response limits, and result evidence stay unchanged.
An unavailable or ungranted connector is omitted and does not stop server startup.

Project files register the server and enable it by default:

| Client | File | Enablement |
| --- | --- | --- |
| Claude Code and the VS Code Copilot harness | `.mcp.json` | Portable `mcpServers` entry. |
| Claude Code | `.claude/settings.json` | Project approval through `enabledMcpjsonServers`. |
| Codex | `.codex/config.toml` | `enabled = true` for trusted projects. |
| OpenCode | `opencode.json` | Local server, enabled unless `disabled` is true. |

Client trust and per-tool approval remain client decisions.
No credentials enter tracked files.

## Affect, consumers, and risk

- Affected source: `core/mcp.py`, `core/cli.py`, four client configuration files, and connector documentation.
- Existing consumers: `ai-sdlc mcp` without `--connectors`, `workbench_call`, and retained action records.
- Qualitative risk: moderate.
- Startup performs one discovery action per connector.
- Mitigation: discovery is read-only, uses the workspace timeout, and skips failures.
- The default `ai-sdlc mcp` tool list does not change.

## Checks and results

- `.venv/bin/python -m unittest discover -s tests`: 1073 tests passed, 2 skipped.
- `.venv/bin/ai-sdlc --workspace . validate`: `VALID`, 119 documents, zero findings.
- Exact server command with `initialize` and `tools/list`: 65 tools, including 61 connector tools.
- Forbidden write tools absent: `wit_create_work_item`, `repo_create_pull_request`, `confluence_create_page`, `postgresql_execute`.
- Server stderr was empty during discovery in the configured checkout.
- JSON parsed for `.mcp.json`, `.claude/settings.json`, and `opencode.json`.
- TOML parsed for `.codex/config.toml`.
- `codex mcp list`: `workbench` is enabled with the configured command.
- `opencode mcp list`: `workbench` connected.
- Discovered grants: ADO 24 reads plus 14 report readers, Confluence 8, SC Wiki 8, SonarQube 11, Web 3, Kibana 2, PostgreSQL 3.
- Nexus and messaging expose no tool call grant, so they add no tools.

Limits:

- No live external connector call ran; credentials and service access were not used.
- Client trust dialogs, tool approvals, and Copilot runtime startup were not exercised in this session.
- Discovery adds one action record per connector at client startup.
- Relative `.venv/bin/python` and `--workspace .` assume the client starts the server at the checkout root.

## Documentation reconciliation

Updated sections:

- [Connector guide](../../docs/CONNECTORS.md#expose-granted-connector-tools-as-mcp-tools): new server section and client table.
- [MCP adapter](../../adapters/mcp/README.md): `--connectors` behavior and current registrations.
- [Claude Code adapter](../../adapters/claude-code/README.md): current MCP surface.
- [Copilot adapter](../../adapters/copilot/README.md): workspace `.mcp.json` and connector tools.
- [Root README](../../README.md#connect-external-systems): current command and project registration.

The existing connector grants, provider contracts, and action evidence rules did not change.
