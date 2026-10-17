# @sc-node-mcp/shared-tests

Shared test utilities for the sc-node-mcp monorepo. This is an **internal package** — it is not published for consumer use. All other `@sc-node-mcp/*` packages use it as a dev dependency.

## Exported Helpers

Import helpers using the package path:

```javascript
import { createMockConnection } from '@sc-node-mcp/shared-tests/helpers/mockConnection';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
```

### `helpers/mockConnection.js`

| Export | Description |
|--------|-------------|
| `createMockConnection()` | Returns a mock Azure DevOps connection object with jest/vitest mock functions for all API methods (`getWorkItemTrackingApi`, `getGitApi`, `getBuildApi`, etc.) |

### `helpers/mockServer.js`

| Export | Description |
|--------|-------------|
| `createMockServer()` | Creates a mock MCP server that captures `server.tool()` registrations and exposes `invokeTool(name, params)` for testing |
| `isValidToolResponse(response)` | Returns `true` if the response has the expected MCP tool response shape: `{ content: [{ type: "text", text: string }] }` |
| `isValidErrorResponse(response)` | Returns `true` if the response has `isError: true` in addition to a valid content shape |

## Usage Pattern

```javascript
import { describe, it, expect, vi } from 'vitest';
import { createMockConnection } from '@sc-node-mcp/shared-tests/helpers/mockConnection';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { configureWorkItemTools } from '../src/tools/workItems.js';

const mockConnection = createMockConnection();
const mockServer = createMockServer();
configureWorkItemTools(mockServer, vi.fn().mockResolvedValue(mockConnection));

const response = await mockServer.invokeTool('wit_get_work_item', { id: 123 });
expect(isValidToolResponse(response)).toBe(true);
```
