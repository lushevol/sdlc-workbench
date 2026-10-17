# @sc-node-mcp/ado-review

MCP server providing Azure DevOps pull request review tools.

## Tools

| Tool | Description |
|------|-------------|
| `post_pr_comment` | Post a review comment on a specific file and line in a pull request |
| `delete_all_pr_review_comments` | Delete all AI-generated review comments from a pull request |
| `repo_review_pr` | Perform an automated code review of a pull request and post comments |
| `repo_pr_diff` | Retrieve the diff for a pull request |

## Installation

Configure in your MCP client (e.g. VS Code `mcp.json`):

```json
{
  "servers": {
    "ado-review": {
      "command": "node",
      "args": ["packages/ado-review/src/index.js", "<ADO_PAT>"]
    }
  }
}
```

## Configuration

| Parameter | CLI Arg | Env Var | Description |
|-----------|---------|---------|-------------|
| ADO PAT | 1st arg | `AZURE_DEVOPS_PAT` | Azure DevOps Personal Access Token |
| Proxy | 2nd arg | `HTTPS_PROXY` | Corporate HTTPS proxy URL |
| Code review guide | — | `CODE_REVIEW_GUIDE_FILE` | Path to markdown file with review guidelines |

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
