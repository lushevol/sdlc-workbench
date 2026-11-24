# ADO Package Tests

This directory contains comprehensive tests for the Azure DevOps MCP server package.

## Test Structure

### Test Files

- **connection.test.js** - Tests for Azure DevOps connection setup and authentication
- **tools.test.js** - Tests for tool registration and configuration
- **workItems.test.js** - Tests for work item management tools
- **repos.test.js** - Tests for repository, branch, and PR management tools
- **review.test.js** - Tests for PR review and commenting tools

## Running Tests

```bash
# Run all tests
yarn test

# Run tests in watch mode
yarn test:watch

# Generate coverage report
yarn test:coverage
```

## Coverage Requirement

**90% threshold** for lines, functions, branches, and statements — enforced by `vitest.config.js`.

## Test Categories

### Connection Tests (3 tests)
- PAT authentication setup
- Proxy configuration
- Connection creation

### Tools Configuration Tests (5 tests)
- Tool registration verification
- Work item tools registration
- Repository tools registration
- Review tools registration
- Connection provider passing

### Work Item Tests (13 tests)
- Get work item by ID
- List work items assigned to current user
- Create work item
- Update work item
- List projects
- Add work item comment
- Link work items
- Get work items in batch
- List backlogs

### Repository Tests (15 tests)
- List repositories
- Filter repositories by name
- List pull requests
- Filter PRs by status
- List branches
- Filter branches
- Auto-discover project
- Create branch
- Create pull request
- Get PR by ID
- Update PR
- Search commits
- List PR threads

### Review Tests (12 tests)
- Post PR comment (new thread)
- Reply to existing thread
- Handle invalid PR URL
- PR URL parsing
- Get PR diff
- Review PR
- Error handling

## Test Helpers

Tests use shared utilities from `@sc-node-mcp/shared-tests`:

- `createMockServer()` - Mock MCP server for tool registration
- `createMockConnection()` - Mock Azure DevOps connection
- `createMockWitApi()` - Mock Work Item Tracking API
- `createMockGitApi()` - Mock Git API
- `createMockCoreApi()` - Mock Core API
- `isValidToolResponse()` - Validate response format
- `isValidErrorResponse()` - Validate error response format

## Test Patterns

### Basic Tool Test
```javascript
it('should perform action', async () => {
  // Setup mocks
  mockApi.method.mockResolvedValue(mockData);
  
  // Invoke tool
  const response = await mockServer.invokeTool('tool_name', params);
  
  // Assertions
  expect(isValidToolResponse(response)).toBe(true);
  expect(mockApi.method).toHaveBeenCalledWith(expectedArgs);
});
```

### Error Handling Test
```javascript
it('should handle errors gracefully', async () => {
  mockApi.method.mockRejectedValue(new Error('API Error'));
  
  const response = await mockServer.invokeTool('tool_name', params);
  
  expect(isValidErrorResponse(response)).toBe(true);
  expect(response.content[0].text).toContain('API Error');
});
```

## Notes

- All tests use Vitest framework
- Tests mock Azure DevOps API responses to avoid external dependencies
- PR review tests that attempt git cloning are expected to fail in test environment (handled gracefully)
- Coverage target: 70%+ (current: 61%)

## Future Improvements

- [ ] Increase coverage for repos.js (currently 55%)
- [ ] Increase coverage for workItems.js (currently 60%)
- [ ] Add integration tests with real Azure DevOps sandbox
- [ ] Add performance benchmarks for tool execution
- [ ] Add tests for edge cases in PR URL parsing
- [ ] Mock git operations in review tool tests
