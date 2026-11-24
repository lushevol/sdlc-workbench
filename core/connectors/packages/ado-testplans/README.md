# @sc-node-mcp/ado-testplans

MCP server providing Azure DevOps test plan management tools.

## Tools

| Tool | Description |
|------|-------------|
| `testplan_list_test_plans` | List test plans in a project, with optional active-only filter |
| `testplan_create_test_plan` | Create a new test plan |
| `testplan_list_test_suites` | List test suites within a test plan |
| `testplan_create_test_suite` | Create a new test suite in a test plan |
| `testplan_add_test_cases_to_suite` | Add existing test cases to a test suite |
| `testplan_list_test_cases` | List test cases in a test suite (includes child suites by default) |
| `testplan_create_test_case` | Create a new test case work item with optional steps |
| `testplan_update_test_case_steps` | Update the steps of an existing test case |
| `testplan_show_test_results_from_build_id` | Show test results associated with a build |

## Installation

Configure in your MCP client (e.g. VS Code `mcp.json`):

```json
{
  "servers": {
    "ado-testplans": {
      "command": "node",
      "args": ["packages/ado-testplans/src/index.js", "<ADO_PAT>"]
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
