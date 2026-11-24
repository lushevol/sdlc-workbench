# @sc-node-mcp/ado-pipelines

MCP server providing Azure DevOps pipeline and build tools.

## Tools

| Tool | Description |
|------|-------------|
| `pipelines_get_build_definitions` | List pipeline definitions in a project |
| `pipelines_run_pipeline` | Trigger a pipeline run |
| `pipelines_list_runs` | List pipeline runs (with or without pipeline filter) |
| `pipelines_get_run` | Get details of a specific pipeline run |
| `pipelines_get_build_status` | Get the status of a specific build |
| `pipelines_get_builds` | Get builds with filtering by definition, branch, status, result |
| `pipelines_cancel_run` | Cancel a running build |
| `pipelines_retry_stage` | Retry a failed stage in a pipeline run |
| `pipelines_list_work_item_pipelines` | Find all builds linked to a specific work item |
| `pipelines_get_build_log` | Retrieve logs for a specific build |
| `pipelines_get_build_changes` | List code changes associated with a build |
| `pipelines_list_artifacts` | List artifacts produced by a build |
| `pipelines_list_variable_groups` | List variable groups (Library) for a project |
| `pipelines_get_variable_group` | Get a specific variable group (Library) by ID |

## Installation

Configure in your MCP client (e.g. VS Code `mcp.json`):

```json
{
  "servers": {
    "ado-pipelines": {
      "command": "node",
      "args": ["packages/ado-pipelines/src/index.js", "<ADO_PAT>"]
    }
  }
}
```

## Configuration

| Parameter | CLI Arg | Env Var | Description |
|-----------|---------|---------|-------------|
| ADO PAT | 1st arg | `AZURE_DEVOPS_PAT` | Azure DevOps Personal Access Token |
| Proxy | 2nd arg | `HTTPS_PROXY` | Corporate HTTPS proxy URL |

## Development

```bash
yarn test           # Run tests
yarn test:watch     # Watch mode
```

## Dependencies

- `@sc-node-mcp/core` — MCP server factory and configuration
- `@sc-node-mcp/ado-core` — Shared Azure DevOps connection provider
- `azure-devops-node-api` — Azure DevOps REST API client
- `zod` — Parameter validation
