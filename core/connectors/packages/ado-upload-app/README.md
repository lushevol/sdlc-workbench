# @sc-node-mcp/ado-upload-app

An MCP App that embeds an interactive file upload panel inside VS Code Copilot Chat. Upload one or more files to an Azure DevOps work item as attachments — without leaving your editor.

## Features

- Interactive UI panel with drag-and-drop file selection
- Multi-file upload in a single operation
- AI pre-fill of Project and Work Item ID
- Headless `wit_upload_attachment` tool for direct AI invocation
- Proxy-aware (corporate network support)

## Prerequisites

- Node.js ≥ 18
- Azure DevOps PAT with **Work Items (Read & Write)** scope
- VS Code with GitHub Copilot Chat (for the UI panel)

## Build

```bash
# From the monorepo root
yarn install

# Build the UI (required before running the server)
cd packages/ado-upload-app
yarn build
```

## Run

```bash
node src/server/server.js <ADO_PAT> [HTTPS_PROXY]
```

Credentials are read in priority order: CLI args → `AZURE_DEVOPS_PAT` env var → `config.json`.

## VS Code Configuration

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "ado-upload-app": {
      "type": "stdio",
      "command": "node",
      "args": [
        "${workspaceFolder}/packages/ado-upload-app/src/server/server.js",
        "${input:ado_pat}",
        "${input:https_proxy}"
      ]
    }
  },
  "inputs": [
    { "id": "ado_pat", "type": "promptString", "description": "Azure DevOps PAT", "password": true },
    { "id": "https_proxy", "type": "promptString", "description": "HTTPS Proxy URL (optional)" }
  ]
}
```

Then say in Copilot Chat:

> "Upload a file to work item 12345 in project MyProject"

## Tools

| Tool | Description |
|------|-------------|
| `wit_upload_attachment_ui` | Opens the upload panel; optionally pre-fills `project` and `wiId` |
| `wit_upload_attachment` | Headless upload — accepts `{ project, wiId, files: [{name, base64}] }` |

## Test

```bash
yarn test              # Single run
yarn test:coverage     # With coverage report (≥ 90% required)
yarn test:watch        # Watch mode
```

## Full Documentation

See [docs/ADO_UPLOAD_APP.md](../../docs/ADO_UPLOAD_APP.md) for the complete guide including architecture, tool reference, and build/deploy instructions.
