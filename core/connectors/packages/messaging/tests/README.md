# Messaging MCP Server Tests

This directory contains unit tests for the Messaging MCP server package.

## Test Files

- **send.test.js** - Tests for email_send tool
- **teams.test.js** - Tests for teams_send_message tool
- **connection.test.js** - Tests for Python bridge connection providers

## Running Tests

```bash
# From package directory
yarn test

# From root
yarn test --scope @sc-node-mcp/messaging

# Watch mode
yarn test:watch

# Coverage
yarn test:coverage
```

## Test Patterns

### Mocking Python Bridge

```javascript
const mockBridge = {
  sendEmail: vi.fn().mockResolvedValue({ status: 'success' })
};
const getMockBridge = vi.fn().mockResolvedValue(mockBridge);
```

### Testing Tools

```javascript
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

const mockServer = createMockServer();
configureEmailTools(mockServer, getMockBridge);
const response = await mockServer.invokeTool('email_send', params);
```

## Coverage Requirements

- **90% threshold** for lines, functions, branches, and statements (enforced by vitest.config.js)
- Test both success and error paths
- Validate Zod schema enforcement
