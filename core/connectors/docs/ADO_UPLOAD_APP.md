# ADO Work Item File Upload MCP App

## Overview

`@sc-node-mcp/ado-upload-app` is an **MCP App** — a Model Context Protocol server that
embeds a custom interactive UI panel directly inside VS Code Copilot Chat. It lets you
upload one or more files to an Azure DevOps work item as attachments without leaving your
editor. The AI can optionally pre-fill the Project and Work Item ID fields when it invokes
the tool.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  VS Code Copilot Chat (host)                        │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  MCP App UI Panel (iframe / webview)        │   │
│  │                                             │   │
│  │  [Project: ________] [WI ID: _____]        │   │
│  │  [📎 Drop files here or browse]            │   │
│  │  [file1.png ×] [log.txt ×]                 │   │
│  │  [         Upload Files         ]           │   │
│  │                                             │   │
│  │  app.callServerTool("wit_upload_attachment")│   │
│  └───────────────┬─────────────────────────────┘   │
│                  │ PostMessage proxy                │
└──────────────────┼──────────────────────────────────┘
                   │ MCP stdio transport
   ┌───────────────▼─────────────────────────────┐
   │  ado-upload-app server (Node.js stdio)      │
   │                                             │
   │  wit_upload_attachment_ui  →  serves UI    │
   │  wit_upload_attachment     →  ADO API      │
   │                                             │
   │  witApi.createAttachment() × N files        │
   │  witApi.updateWorkItem()   (patch relations)│
   └─────────────────────────────────────────────┘
```

### Two-Tool Design

| Tool | Type | Role |
|------|------|------|
| `wit_upload_attachment_ui` | App Tool (has UI) | Opens the panel; optionally accepts `project` and `wiId` args for pre-fill |
| `wit_upload_attachment` | Plain MCP Tool | Receives `{ project, wiId, files[] }`, calls ADO API, returns JSON result |

The UI calls `wit_upload_attachment` via `app.callServerTool()`. The AI agent can also
invoke `wit_upload_attachment` directly (without opening the panel) by passing the full
payload as tool arguments.

---

## Package Structure

```
packages/ado-upload-app/
├── package.json           # ESM package, dependencies
├── vite.config.js         # Bundles src/app/ into a single HTML file (dist/)
├── vitest.config.js       # Test configuration (coverage ≥ 90%)
├── src/
│   ├── app/
│   │   ├── index.html     # UI form — project, WI ID, file picker, result area
│   │   ├── mcp-app.js     # App SDK wiring — ontoolinput, upload click handler
│   │   └── utils.js       # readFileAsBase64, validateForm, formatUploadResult, …
│   └── server/
│       └── server.js      # MCP server — registerAppTool + wit_upload_attachment + resource
├── tests/
│   ├── server.test.js     # Server-side tool handler unit tests
│   ├── utils.test.js      # Pure utility function tests
│   ├── mcp-app.test.js    # UI logic tests (jsdom + mocked SDK)
│   └── integration.test.js# End-to-end flow simulation
└── dist/                  # Generated — Vite build output (not committed)
```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Node.js ≥ 18 | ESM support required |
| Azure DevOps PAT | Needs `Work Items (Read & Write)` scope |
| VS Code with GitHub Copilot | For the embedded UI panel |
| HTTPS Proxy (optional) | Required in corporate networks |

---

## Setup

### 1. Install dependencies (from monorepo root)

```bash
yarn install
```

### 2. Build the UI

```bash
cd packages/ado-upload-app
yarn build
```

This bundles `src/app/index.html` (with all JS inlined as a single file) into
`dist/src/app/index.html`. The server reads this file and serves it as the UI resource.

> **Note:** The build step must run before starting the server. The server reads
> `dist/src/app/index.html` at runtime.

### 3. Run the server

```bash
node packages/ado-upload-app/src/server/server.js <ADO_PAT> [HTTPS_PROXY]
```

The server reads credentials using the same 3-tier priority as all other packages
(`getConfig()` from `@sc-node-mcp/core`):
1. **CLI args** — `node server.js <PAT> [PROXY]`
2. **Environment variable** — `AZURE_DEVOPS_PAT`
3. **config.json** — root-level file (local dev only, gitignored)

---

## VS Code MCP Configuration

Add to your `.vscode/mcp.json` (not committed to the repo):

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

---

## How It Works

### Using the Prompt (Recommended)

The easiest way to trigger the upload panel is via the built-in prompt:

```
upload-attachment-ui
```

Or just ask Copilot Chat naturally:

```
Upload a file to work item 12345 in project MyProject
```

Both will invoke `wit_upload_attachment_ui` with Project and WI ID pre-filled and open the panel inside Copilot Chat.

**Available prompt arguments (all optional):**
| Argument | Description |
|----------|-------------|
| `project` | Pre-fills the project name field in the UI |
| `wiId` | Pre-fills the work item ID field in the UI |

> See [PROMPTS.md](PROMPTS.md#37-upload-attachment-ui) for the full prompt reference.

---

### Opening the UI

Simply ask Copilot Chat to invoke the tool:

```
Upload a file to work item 12345 in project MyProject
```

Copilot will call `wit_upload_attachment_ui` (pre-filling Project and WI ID), and the
panel opens inside Copilot Chat.

### UI Walkthrough

1. **Project** — type the Azure DevOps project name (e.g. `TBQPR`)
2. **Work Item ID** — enter the numeric WI ID (e.g. `12345`)
3. **Files** — click "Click to browse" or drag & drop one or more files
4. Click **Upload Files**
5. A success banner appears with the names of all uploaded attachments

### Direct Tool Invocation (No UI)

The AI can also call `wit_upload_attachment` directly with encoded files:

```json
{
  "project": "MyProject",
  "wiId": 12345,
  "files": [
    { "name": "screenshot.png", "base64": "<base64-encoded-content>" }
  ]
}
```

---

## Tool Reference

### `wit_upload_attachment_ui`

Opens the file upload panel.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project` | string | No | Pre-fill the project name |
| `wiId` | number | No | Pre-fill the work item ID |

**Response:** JSON `{ project, wiId, message }` — the host renders the UI panel.

---

### `wit_upload_attachment`

Uploads files programmatically without opening the UI.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project` | string | Yes | Azure DevOps project name |
| `wiId` | number | Yes | Work item ID (positive integer) |
| `files` | array | Yes | Array of `{ name: string, base64: string }` objects (min 1) |

**`files` item fields:**
- `name` — filename including extension (e.g. `screenshot.png`)
- `base64` — raw base64-encoded file content (no `data:` URI prefix)

**Success response:**
```json
{
  "success": true,
  "workItemId": 12345,
  "project": "MyProject",
  "uploaded": [
    { "name": "screenshot.png", "attachmentId": "abc123-def456" }
  ]
}
```

**Error response:** `isError: true` with the ADO API error message.

---

## Testing

```bash
# Run all tests once
cd packages/ado-upload-app
yarn test

# Run with coverage (enforces ≥ 90% thresholds)
yarn test:coverage

# Watch mode
yarn test:watch
```

### Test Coverage Strategy

| File | What is tested |
|------|----------------|
| `tests/server.test.js` | `wit_upload_attachment` handler — single file, multi-file, createAttachment failures, updateWorkItem failures; `wit_upload_attachment_ui` metadata |
| `tests/utils.test.js` | All utility functions — readFileAsBase64 (prefix stripping, errors), validateForm (all branches), formatUploadResult (success/error/plural), formatError, formatFileSize |
| `tests/mcp-app.test.js` | ontoolinput pre-fill, upload payload shape, button re-enable, validation error path, server error path, exception path |
| `tests/integration.test.js` | Full flow: pre-fill → file select → submit; manual fill flow; validation failure blocks callServerTool; isError result displayed; button always re-enabled |

---

## Build & Distribution

The package is published via the ADO pipeline (`azure-pipelines-npm.yml`) to the
Standard Chartered Artifactory. Do **not** run `lerna publish` locally.

The `dist/` directory is included in the published package (`"files"` in `package.json`)
so consumers can run the server directly without a separate build step.

```bash
# Verify package contents before publish
npm pack --dry-run | grep dist/
# Should show: npm notice ...kB  dist/src/app/index.html
```
