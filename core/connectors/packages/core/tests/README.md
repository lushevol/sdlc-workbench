# Core Package Tests

This directory contains comprehensive tests for the core infrastructure package.

## Test Structure

### Test Files

- **config.test.js** - Tests for configuration loading and validation (9 tests)
- **server.test.js** - Tests for MCP server creation and startup (7 tests)
- **index.test.js** - Tests for module exports (5 tests)

## Running Tests

```bash
# Run all tests
yarn test

# Run tests in watch mode
yarn test:watch

# Generate coverage report (from root)
yarn test:coverage
```

## Test Results (Latest)

- **Total Tests:** 21
- **Passing:** 21 (100%)
- **Code Coverage:** High (config and server modules)

### Coverage Breakdown

- `config.js`: Configuration loading, validation, error handling
- `server.js`: MCP server creation and transport setup
- `index.js`: Module exports and environment setup

## Test Categories

### Configuration Tests (9 tests)
- Load valid config.json
- Handle minimal required fields
- Validate Azure DevOps credentials
- Handle Confluence configuration
- Error handling for missing/invalid config
- Partial configuration support
- JSON parsing errors
- Warning on incomplete Confluence config

### Server Tests (7 tests)
- Create MCP server with name and version
- Configure server capabilities
- Create stdio transport
- Connect server to transport
- Handle connection errors
- Return connected server instance
- Integration test for create + start

### Index Tests (5 tests)
- Export getConfig function
- Export createMcpServer function
- Export startMcpServer function
- Verify all exports
- TLS rejection disabled

## Test Helpers

Tests use Vitest mocking:
- `vi.mock('fs')` - Mock file system operations
- `vi.mock('@modelcontextprotocol/sdk/server/mcp.js')` - Mock MCP server
- `vi.mock('@modelcontextprotocol/sdk/server/stdio.js')` - Mock transport

## Test Patterns

### Config Test Example
```javascript
it('should load and parse config.json successfully', () => {
  const mockConfig = {
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/org',
    AZURE_DEVOPS_PAT: 'token'
  };
  
  vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
  
  const config = getConfig();
  
  expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/org');
});
```

### Server Test Example
```javascript
it('should create MCP server', () => {
  const server = createMcpServer('test-server', '1.0.0');
  
  expect(McpServer).toHaveBeenCalledWith({
    name: 'test-server',
    version: '1.0.0',
    capabilities: expect.any(Object)
  });
});
```

## Notes

- All tests use Vitest framework
- File system operations are mocked to avoid dependencies
- MCP SDK modules are mocked for isolated testing
- Configuration validation is thoroughly tested
- Error scenarios are covered

## Core Package Responsibilities

The core package provides:
1. **Configuration Management** - Load and validate config.json
2. **Server Factory** - Create MCP server instances
3. **Transport Setup** - Configure stdio transport for VS Code
4. **Common Exports** - Shared utilities for all packages
