# @sc-node-mcp/ado

Azure DevOps MCP Server providing 86 tools for work items, repositories, branches, pull requests, pipelines, and automated PR review.

## Overview

This package provides comprehensive Azure DevOps integration through the Model Context Protocol:

- **Work Items (29 tools)**: Create, update, query, link work items; manage iterations, backlogs, and sprints
- **Repositories (20 tools)**: Manage repos, branches, pull requests, and commits
- **Pipelines (14 tools)**: Trigger, monitor, cancel, and list pipeline runs and build definitions
- **PR Review (4 tools)**: Automated code review with AI-powered suggestions posted as PR comments; delete AI review comments
- **Search (2 tools)**: Full-text code and work item search across repositories and projects
- **Sprint & Capacity (8 tools)**: Manage iterations, assign sprints to teams, get and update team capacity
- **Test Plans (9 tools)**: Create and manage test plans, suites, and test cases
- **Core (1 tool)**: Identity resolution for reviewer assignment and capacity tools

## Installation

> 📘 **Complete Setup Guide:** See [Installation Guide](../../docs/INSTALLATION.md) for detailed instructions, SCB artifactory authentication, and troubleshooting.

### Quick Install Methods

```bash
# Option 1: NPX (no installation, always latest version)
npx -y @sc-node-mcp/ado \
  "your-ado-pat-token" \
  "http://10.239.9.190:443"

# Option 2: Global installation
yarn global add @sc-node-mcp/ado

# Then run using binary command
sc-node-mcp-ado \
  "your-ado-pat-token" \
  "http://10.239.9.190:443"

# Option 3: Local package dependency (for programmatic use)
yarn add @sc-node-mcp/ado
```

### Installation Parameters

| Position | Parameter | Required | Example |
|----------|-----------|----------|---------|
| 1 | ADO PAT | ✅ Yes | `your-pat-token` |
| 2 | Proxy URL | ⚠️ Optional | `http://10.239.9.190:443` |

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`) is hardcoded.

## Usage

### NPX Direct Execution (Recommended)

```bash
# Run directly without installation
npx -y @sc-node-mcp/ado \
  "your-ado-pat-token" \
  "http://10.239.9.190:443"
```

### Global Installation

```bash
# After global install
sc-node-mcp-ado \
  "your-ado-pat-token" \
  "http://10.239.9.190:443"
```

### VS Code MCP Extension

Add to `.vscode/mcp.json`:

```jsonc
{
  "mcpServers": {
    "ado-server": {
      "command": "npx",
      "args": [
        "-y",
        "@sc-node-mcp/ado",
        "${input:ado_pat}",
        "${input:https_proxy}"
      ]
    }
  },
  "inputs": [
    {
      "id": "ado_pat",
      "type": "promptString",
      "description": "Azure DevOps Personal Access Token",
      "password": true
    },
    {
      "id": "https_proxy",
      "type": "promptString",
      "description": "HTTPS Proxy URL (optional, press Enter to skip)"
    }
  ]
}
```

### Programmatic Usage

```javascript
import { configureAdoTools, getADOConnection } from '@sc-node-mcp/ado';
import { createMcpServer } from '@sc-node-mcp/core';

const server = createMcpServer('my-ado-server', '1.0.0');
configureAdoTools(server, getADOConnection);
```

## Configuration

Configuration is loaded with the following priority order: **CLI arguments** → **environment variables** → **config.json**.

> **CLI args take the highest priority**, overriding environment variables and config.json. This is the recommended approach for npm packages (npx, global install).

For CLI arguments and environment variables, see the [Installation Guide](../../docs/INSTALLATION.md). For local development, create `config.json` in the workspace root:

```json
{
  "AZURE_DEVOPS_PAT": "your-personal-access-token",
  "HTTPS_PROXY": "http://proxy:443" // Optional
}
```

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`) is hardcoded in the server configuration.

## Prompts

The `@sc-node-mcp/ado` package ships ~82 MCP prompts for guided ADO workflows, covering work items, pull requests, branches, pipelines, sprints, test plans, and more.

**Context auto-fill:** If a `~/.sc-node-mcp-context.json` file is present (created via the unified server's `set-context` tool or written manually), standalone ADO installs will automatically populate the `project`, `team`, and `repository` arguments for prompts that accept them.

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## Documentation

- [Work Items Guide](../../docs/guide/WORKITEMS_TOOLS_GUIDE.md) - Complete guide to work item tools
- [Repositories Guide](../../docs/guide/REPOSITORIES_TOOLS_GUIDE.md) - Complete guide to repo, branch, PR, and commit tools
- [PR Review](../../docs/PR_REVIEW.md) - Automated PR review system documentation

## Key Features

### Automated PR Review
The `repo_review_pr` tool analyzes PR diffs and posts AI-generated code review comments directly on the corresponding lines. Review guidelines are loaded from the file path set in `CODE_REVIEW_GUIDE_FILE` when configured. All changed file types in the PR are reviewed.

### Work Item Management
Comprehensive work item operations including querying, batch updates, linking, and integration with Azure DevOps projects and teams.

### Repository Operations
Full lifecycle management of repositories, branches, pull requests, reviewers, and commit history.

## Dependencies

- `@sc-node-mcp/core` - Core MCP infrastructure
- `azure-devops-node-api` - Azure DevOps API client
