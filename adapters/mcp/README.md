# MCP adapter

The MCP adapter exposes Workbench core capabilities through standard input and output.
Install this standalone project before starting the `ai-sdlc` command.
Select the workspace that contains `workspace.yaml`.

```text
ai-sdlc --workspace PATH mcp
```

In an MCP client, use command `ai-sdlc` with arguments `--workspace`, the absolute workspace path, and `mcp`.
Follow that client's supported configuration mechanism.
This directory does not install or configure a client connection.

Add `--connectors` to expose each external connector tool whose catalog grant is true:

```text
ai-sdlc --workspace PATH mcp --connectors
```

Startup calls each connector's `list` operation and retains its action record.
Calls use the existing connector `call` operation.
Catalog grants, `.env` isolation, timeouts, response limits, and result evidence stay in force.
An unavailable or ungranted connector is omitted; server startup continues.

This source checkout registers the server and enables it by default for Claude Code, the VS Code Copilot harness, Codex, and OpenCode.
Client trust and per-tool approval remain client decisions.

| Tool | Purpose | Arguments |
| --- | --- | --- |
| `workbench_status` | Discover resources, operations, and schemas. | `{}` |
| `workbench_call` | Invoke a resource operation and retain its action record. | `resource_id`, `operation`, optional `arguments` |
| `workbench_runs` | List actions or read one action record. | Optional `limit` or `run_id` |
| `workbench_skills` | List canonical skills or read one procedure. | Optional `skill_id` |

With `--connectors`, the server also lists each granted connector tool as its own MCP tool.
The name is the connector's native tool name.
Discovery and calls use the existing connector provider and action records.

Call `workbench_status` before selecting resource IDs and operations.
Read each operation schema before invoking it.

Use `connector.mcp` resources for [external system access](../../docs/CONNECTORS.md).
Their `list` operation returns tool schemas and exact tool grants.
Their `call` operation requires a granted tool name and its arguments.
Variables come from `.env` at the selected workspace root.

Use `workbench_call` with a registered `graph.snapshot` resource to query static dependency evidence.
Read `coverage` before `relationships`, `services`, `search`, or `neighborhood`.
Graph operations retain snapshot checksums and use existing action records and grants.
The provider delegates to the [canonical graph skill](../../.agents/skills/service-dependencies-graph/SKILL.md).
Keep graph extraction, queries, validation, and viewer changes inside that skill.

Use `workbench_skills` to consume [canonical skills](../../.agents/skills/).
CLI skill discovery uses the same `.agents/skills/` location.
Keep reasoning in the agent and context, evidence, relationships, and execution management in the core.

Phase 1 supports configured local operations and retained action records.
Complete automated knowledge governance and behavior verification remain future core capabilities.
An action status does not establish `VERIFIED` behavior.
Preserve the user's task scope and existing authorization when invoking operations.
