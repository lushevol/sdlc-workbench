# Confluence Package Tests

This directory contains comprehensive tests for the Confluence MCP server package.

## Test Structure

### Test Files

- **confluence.test.js** - Tests for Confluence tool functionality (14 tests)
- **tools.test.js** - Tests for tools module configuration (6 tests)

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

- **Total Tests:** 20
- **Passing:** 20 (100%)
- **Code Coverage:** Good (confluence tools module)

### Coverage Breakdown

- `tools/confluence.js`: Confluence API integration, authentication, filtering
- `tools.js`: Tool registration wrapper

## Test Categories

### Confluence Tool Tests (14 tests)
- List pages created by current user
- Filter pages by creator
- Respect limit parameter
- Use default limit
- Filter by space key
- Basic authentication
- Handle missing config
- Handle incomplete config
- Handle API errors
- Handle empty results
- URL construction with parameters
- Handle pages without history
- Handle 401 unauthorized
- Configuration validation

### Tools Module Tests (6 tests)
- Function existence check
- Parameter acceptance
- Tool registration
- Null config handling
- Undefined config handling
- Tool naming verification

## Test Helpers

Tests use shared utilities from `@sc-node-mcp/shared-tests`:
- `createMockServer()` - Mock MCP server for tool registration
- `isValidToolResponse()` - Validate response format
- `isValidErrorResponse()` - Validate error response format

Tests also mock axios for HTTP requests:
- `vi.mock('axios')` - Mock HTTP client

## Test Patterns

### Confluence Tool Test
```javascript
it('should list pages created by current user', async () => {
  const mockPages = {
    data: {
      results: [
        {
          id: '123',
          title: 'Test Page',
          history: {
            createdBy: { email: 'user@example.com' }
          }
        }
      ]
    }
  };
  
  axios.get.mockResolvedValue(mockPages);
  
  const response = await mockServer.invokeTool('confluence_list_my_pages', {});
  
  expect(isValidToolResponse(response)).toBe(true);
});
```

### Configuration Test
```javascript
it('should handle missing config', async () => {
  configureConfluenceTools(mockServer, null);
  
  const response = await mockServer.invokeTool('confluence_list_my_pages', {});
  
  expect(isValidErrorResponse(response)).toBe(true);
});
```

## Notes

- All tests use Vitest framework
- Axios HTTP client is mocked to avoid external dependencies
- Confluence API responses are mocked
- Authentication and filtering logic is thoroughly tested
- Error scenarios are covered
- Confluence integration is fully operational in production

## Confluence Tool Features

### confluence_list_my_pages

Lists Confluence pages created by the authenticated user.

**Parameters:**
- `limit` (optional): Max number of pages (default: 10)
- `spaceKey` (optional): Filter by space key

**Features Tested:**
- Basic authentication with API token
- Filter pages by creator email
- Pagination with limit
- Space key filtering
- URL construction
- Error handling
- Empty result handling

## Known Limitations

- Currently only supports Basic auth
- Only implements list_my_pages tool
- No page creation/update/delete tools yet
- No attachment handling
- No comment functionality

## Future Improvements

- [ ] Add tests for additional Confluence tools (when implemented)
- [ ] Add integration tests with real Confluence sandbox
- [ ] Test OAuth authentication flow (when enabled)
- [ ] Add tests for page CRUD operations
- [ ] Add tests for search functionality
- [ ] Mock response pagination
