# GitHub Copilot adapter

GitHub Copilot consumes the canonical skills under [`.agents/skills/`](../../.agents/skills/).
CLI and MCP skill discovery use that canonical location.
Keep workflow logic only in the canonical skills.
Avoid copies that can develop different behavior.

Install this standalone project before using its `ai-sdlc` command.
Select the workspace that contains `workspace.yaml`.

```text
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH skills
ai-sdlc --workspace PATH skills impact-analysis
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Replace placeholders with discovered resource IDs, operation names, and schema arguments.
The CLI exposes the Workbench core; Copilot supplies reasoning and task execution.
Existing assets stay at their registered locations.

For stdio MCP access, use the [shared MCP adapter](../mcp/README.md).
The four tools expose status, operations, action records, and canonical skills.

Native skill discovery depends on the Copilot client, version, and project configuration.
Expose canonical files through the supported client mechanism, or read them through CLI or MCP.
This directory supplies integration guidance.
It does not install or configure a Copilot connection.
Preserve the user's task scope and existing authorization when invoking operations.

## Optional Workbench hooks

The [shared hook runtime](../../docs/HOOKS.md) supplies bounded session context and scoped completion checks.
Install its Copilot registration explicitly:

```text
ai-sdlc --workspace . hooks install --client copilot
ai-sdlc --workspace . hooks status
```

The adapter uses `.github/hooks/workbench.json` with `sessionStart` and `agentStop` events.
Run the hook commands from the workspace root and make installed `ai-sdlc` available on the agent's `PATH` before launching Copilot.
Native events discover the nearest owning Workbench workspace from their working directory; registrations contain no machine paths.
Copilot CLI and the VS Code Copilot harness share this format.
The VS Code hooks experience is preview; the deprecated Local harness has a separate schema.
`sessionEnd` means session termination and does not replace turn completion.
Workbench keeps Claude hooks in a separate settings file selected explicitly by the Claude launcher.
That file avoids duplicate Workbench handlers from Copilot's ordinary Claude-settings discovery.
Bind the active living record to the exact client session before expecting task-specific checks.
Configuration validity does not establish successful hook execution in the installed client or cloud environment.
