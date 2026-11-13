# Claude Code adapter

Claude Code consumes the canonical skills under [`.agents/skills/`](../../.agents/skills/).
Links under `.claude/skills/` provide native Claude Code discovery.
Initialization creates forwarding files when the platform denies directory links.
Keep workflow logic only in the canonical skills.
Avoid copies that can develop different behavior.

Install this standalone project before using its `ai-sdlc` command.
Select the workspace that contains `workspace.yaml`.

```text
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH skills
ai-sdlc --workspace PATH skills analyze-requirement
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Replace placeholders with discovered resource IDs, operation names, and schema arguments.
The CLI exposes the Workbench core; Claude Code supplies reasoning and task execution.
Existing assets stay at their registered locations.

For stdio MCP access, use the [shared MCP adapter](../mcp/README.md).
The four tools expose status, operations, action records, and canonical skills.

Native skill discovery depends on the Claude Code version and project configuration.
Use `.claude/skills/` for native discovery, or read canonical skills through CLI or MCP.
This directory supplies integration guidance.
It does not install or configure a Claude Code connection.
Preserve the user's task scope and existing authorization when invoking operations.

## Optional Workbench hooks

The [shared hook runtime](../../docs/HOOKS.md) supplies bounded session context and scoped completion checks.
Install its Claude Code registration explicitly:

```text
ai-sdlc --workspace . hooks install --client claude
ai-sdlc --workspace . hooks status
```

The adapter maps native `SessionStart` and `Stop` events through isolated `.claude/workbench-hooks.json`.
**From the workspace root, launch Claude Code with `claude --settings .claude/workbench-hooks.json`.**
Make installed `ai-sdlc` available on the agent's `PATH` before launching Claude Code.
Native events discover the nearest owning Workbench workspace from their working directory; registrations contain no machine paths.
Bare `claude` does not activate this isolated registration.
Ordinary `.claude/settings.json` and `.claude/settings.local.json` remain untouched.
The isolated file prevents Copilot from inheriting the installed Claude Workbench handlers.
Native workspace trust remains a client responsibility.
Bind the active living record to the exact client session before expecting task-specific checks.
The hooks provide advisory evidence checks; they do not replace semantic workflows or grant publication approval.
