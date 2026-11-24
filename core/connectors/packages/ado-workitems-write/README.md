# @sc-node-mcp/ado-workitems-write

Azure DevOps work item **write** tools MCP server — create, update, link, and comment on work items.

## Tools

| Tool | Description |
|------|-------------|
| `wit_add_work_item_comment` | Add a comment to a work item |
| `wit_update_work_item` | Update a work item via JSON patch document |
| `wit_create_work_item` | Create a new work item via JSON patch |
| `wit_add_child_work_items` | Add child work items to a parent using a hierarchy link |
| `wit_work_items_link` | Create a link between two work items |
| `wit_update_work_items_batch` | Update multiple work items in a loop |
| `wit_work_item_unlink` | Remove links from a work item |
| `wit_link_work_item_to_pull_request` | Link a work item to a pull request as an artifact link |
| `wit_update_work_item_comment` | Update the text of an existing work item comment |

## Usage

```bash
npx @sc-node-mcp/ado-workitems-write <AZURE_DEVOPS_PAT> [HTTPS_PROXY]
```

## Configuration

| Source | Variable |
|--------|----------|
| CLI arg 1 | `AZURE_DEVOPS_PAT` |
| CLI arg 2 | `HTTPS_PROXY` (optional) |
| Env var | `AZURE_DEVOPS_PAT` |
| Env var | `HTTPS_PROXY` (optional) |
