# Context Management Guide

Complete usage guide for the 4 context management tools in the SC Node MCP Server.

Context management allows you to save named workspace configurations — project, team, repositories, branch defaults, Nexus app IDs, Confluence space — and switch between them instantly. Once a context is active, other tools (work items, repos, pipelines, etc.) can read the active context to auto-fill their default parameters.

---

## Table of Contents

- [How Context Works](#how-context-works)
- [Stored Fields](#stored-fields)
- [MCP Resource: `context://active`](#mcp-resource-contextactive)
- [Tool Reference](#tool-reference)
  1. [ctx_set](#1-ctx_set)
  2. [ctx_get](#2-ctx_get)
  3. [ctx_switch](#3-ctx_switch)
  4. [ctx_list](#4-ctx_list)
- [Common Workflows](#common-workflows)

---

## How Context Works

Contexts are stored in `~/.sc-node-mcp-context.json` — a JSON file in your home directory that persists across sessions. The file contains:

- A map of named contexts (each with project, team, repos, etc.)
- An `activeContext` field pointing to the currently active context name

**Auto-detection:** If a context has `workspacePaths` defined, the server automatically activates that context when the current working directory (`cwd`) matches one of those paths. This means switching to a repository in your terminal can automatically switch your MCP context.

**Storage format:**
```json
{
  "activeContext": "my-service",
  "contexts": {
    "my-service": {
      "project": "YOUR_PROJECT",
      "team": "Your Team",
      "defaultBranch": "develop",
      "repositories": ["my-service-api", "my-service-ui"],
      "nexusAppIds": ["ITAM__YOUR_PROJECT__my-service"],
      "confluenceSpaceKey": "PLAT",
      "workspacePaths": ["/Users/you/repos/my-service"]
    }
  }
}
```

---

## Stored Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Unique context identifier (used for switching) |
| `description` | string | Human-readable description |
| `project` | string | Default ADO project name |
| `team` | string | Default ADO team name |
| `defaultBranch` | string | Default branch for repo operations |
| `areaPath` | string | Default work item area path |
| `iterationPath` | string | Default work item iteration path |
| `repositories` | string[] | List of relevant repository names |
| `nexusAppIds` | string[] | Nexus IQ application IDs for vulnerability scanning |
| `confluenceSpaceKey` | string | Default Confluence space key |
| `workspacePaths` | string[] | Local directory paths — trigger auto-activation on `cwd` match |

All fields except `name` are optional.

---

## MCP Resource: `context://active`

In addition to the `ctx_get` tool, the active context is also exposed as an **MCP resource** at `context://active`. MCP-compatible clients can passively read this resource between tool calls without invoking a tool explicitly. This allows AI clients to always have the current context available as background knowledge.

---

## Tool Reference

### 1. `ctx_set`

Create or update a named workspace context. Sets it as the active context immediately upon creation.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | ✅ Yes | Unique context name |
| `description` | string | ⚠️ Optional | Human-readable description |
| `project` | string | ⚠️ Optional | Default ADO project |
| `team` | string | ⚠️ Optional | Default ADO team |
| `defaultBranch` | string | ⚠️ Optional | Default branch for operations |
| `areaPath` | string | ⚠️ Optional | Default area path for work items |
| `iterationPath` | string | ⚠️ Optional | Default iteration path |
| `repositories` | string[] | ⚠️ Optional | List of related repository names |
| `nexusAppIds` | string[] | ⚠️ Optional | Nexus IQ application IDs |
| `confluenceSpaceKey` | string | ⚠️ Optional | Confluence space key |
| `workspacePaths` | string[] | ⚠️ Optional | Local directory paths for auto-activation |

**Test Query:**
```
Set context "my-service" for ADO project YOUR_PROJECT, team "Your Team", branch develop, repos ["my-service-api", "my-service-ui"]
```

**JSON Invocation:**
```json
{
  "name": "my-service",
  "description": "My Service development context",
  "project": "YOUR_PROJECT",
  "team": "Your Team",
  "defaultBranch": "develop",
  "repositories": ["my-service-api", "my-service-ui"],
  "nexusAppIds": ["ITAM__YOUR_PROJECT__my-service"],
  "confluenceSpaceKey": "PLAT",
  "workspacePaths": ["/Users/you/repos/my-service"]
}
```

**Example Response:**
```json
{
  "message": "Context 'my-service' created and set as active.",
  "context": {
    "name": "my-service",
    "project": "YOUR_PROJECT",
    "team": "Your Team",
    "defaultBranch": "develop"
  }
}
```

**Alternative Prompts:**
- `Create a context for the payments project called "payments-service"`
- `Update my current context to use the feature/new-api branch as default`

---

### 2. `ctx_get`

Get the currently active context. Auto-detects the context by matching `workspacePaths` against the server's current working directory; falls back to the `activeContext` field.

**Parameters:** None

**Test Query:**
```
What is my current MCP context?
```

**JSON Invocation:**
```json
{}
```

**Example Response:**
```json
{
  "activeContext": "my-service",
  "context": {
    "name": "my-service",
    "project": "YOUR_PROJECT",
    "team": "Your Team",
    "defaultBranch": "develop",
    "repositories": ["my-service-api", "my-service-ui"],
    "nexusAppIds": ["ITAM__YOUR_PROJECT__my-service"],
    "confluenceSpaceKey": "PLAT"
  }
}
```

**Alternative Prompts:**
- `Show me my current context`
- `What project and team is currently active?`

---

### 3. `ctx_switch`

Switch the active context to a different stored context by name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | ✅ Yes | The context name to switch to (use `ctx_list` to see available names) |

**Test Query:**
```
Switch context to "payments-service"
```

**JSON Invocation:**
```json
{
  "name": "payments-service"
}
```

**Example Response:**
```json
{
  "message": "Switched active context to 'payments-service'.",
  "context": {
    "name": "payments-service",
    "project": "PAYMENTS_PROJECT",
    "team": "Payments Team"
  }
}
```

**Alternative Prompts:**
- `Change my context to the auth-service project`
- `Switch to the platform team context`

---

### 4. `ctx_list`

List all stored context names with their descriptions, workspace paths, project, and team.

**Parameters:** None

**Test Query:**
```
List all my saved MCP contexts
```

**JSON Invocation:**
```json
{}
```

**Example Response:**
```json
{
  "activeContext": "my-service",
  "contexts": [
    {
      "name": "my-service",
      "description": "My Service development context",
      "project": "YOUR_PROJECT",
      "team": "Your Team",
      "workspacePaths": ["/Users/you/repos/my-service"]
    },
    {
      "name": "payments-service",
      "description": "Payments domain services",
      "project": "PAYMENTS_PROJECT",
      "team": "Payments Team",
      "workspacePaths": ["/Users/you/repos/payments"]
    }
  ]
}
```

**Alternative Prompts:**
- `What contexts do I have saved?`
- `Show me all my workspace contexts`

---

## Common Workflows

### First-Time Setup (New Developer)

```
1. List projects in ADO: "List all projects in my Azure DevOps org"
2. Find your team: "List teams in project YOUR_PROJECT"
3. Create a context: "Set context 'my-service' with project YOUR_PROJECT, team 'Your Team'"
4. Confirm: "What is my current context?"
```

### Working Across Multiple Projects

If you work on multiple repositories in different ADO projects, create a context for each:

```
Set context "service-a" with project PROJECT_A, team "Team A", repos ["service-a-api"]
Set context "service-b" with project PROJECT_B, team "Team B", repos ["service-b-ui"]
```

Then switch between them:
```
Switch context to "service-a"
# ... do work items, PRs for Project A ...

Switch context to "service-b"
# ... do work items, PRs for Project B ...
```

### Auto-Activation with Workspace Paths

If you set `workspacePaths` when creating your context, the server automatically activates your context when VS Code is opened in that folder. No manual switching needed.

```
Set context "my-service" with workspacePaths ["/Users/you/repos/my-service"]
```

Now whenever you open `/Users/you/repos/my-service` in VS Code, the `my-service` context activates automatically, pre-filling the project and team for all your tools.

### Using Context in Nexus Scans

If you set `nexusAppIds` in your context, Nexus IQ vulnerability scanning can pick up the application ID automatically:

```
Set context "my-service" with nexusAppIds ["ITAM__YOUR_PROJECT__my-service"]
# Then scan:
Scan the current project for vulnerabilities using Nexus IQ
```

---

## Related Documentation

- [Tools Reference — Context Management section](../TOOLS_REFERENCE.md#context-management)
- [Prompts Reference — Context Management section](../PROMPTS.md#context-management)
- [Setup Guide](../SETUP.md)
