# @sc-node-mcp/core

Core infrastructure for sc-node-mcp MCP servers.

> **Note:** This is an **internal infrastructure package** — it is not intended to be installed directly by consumers. It is used as a shared dependency by `@sc-node-mcp/ado`, `@sc-node-mcp/confluence`, `@sc-node-mcp/messaging`, `@sc-node-mcp/nexus`, and `@sc-node-mcp/unified`.

## Overview

This package provides shared functionality for all sc-node-mcp packages:
- Configuration loading from `config.json`
- MCP server factory and initialization
- Common utilities (proxy setup, environment configuration)

## Usage

```javascript
import { getConfig, createMcpServer, startMcpServer } from '@sc-node-mcp/core';

const config = getConfig();
const server = createMcpServer('my-server', '1.0.0');
await startMcpServer(server);
```

## Exports

- `getConfig()` - Load configuration with 3-tier priority: CLI arguments → environment variables → `config.json`
- `createMcpServer(name, version)` - Create a new MCP server instance
- `startMcpServer(server)` - Start the MCP server on stdio transport
- `resetConfigCache()` - Reset memoized config (test use only)

### Supported Configuration Keys

| CLI Position | Environment Variable | Description |
|---|---|---|
| 1 | `AZURE_DEVOPS_PAT` | Azure DevOps Personal Access Token (required) |
| 2 | `HTTPS_PROXY` | Corporate proxy URL (optional) |
| 3 | `CONFLUENCE_PAT` | Confluence Bearer Token (optional — enables Confluence tools) |
| 4 | `NEXUS_USER_CODE` | Nexus IQ username (optional — enables Nexus tools) |
| 5 | `NEXUS_PASS_CODE` | Nexus IQ password (optional — enables Nexus tools) |
| 6 | `SONAR_TOKEN` | SonarQube Bearer Token (optional — enables SonarQube tools) |
| env only | `CODE_REVIEW_GUIDE_FILE` | Full path to a custom PR review guidelines file (optional) |

## Dependencies

- `@modelcontextprotocol/sdk` - MCP protocol implementation
- `zod` - Schema validation
- `https-proxy-agent` - Proxy support
- `node-fetch` - HTTP client
