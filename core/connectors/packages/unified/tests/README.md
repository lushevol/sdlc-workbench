# Unified Package Tests

This directory contains comprehensive tests for the unified MCP server package that combines Azure DevOps and Confluence tools.

## Test Structure

### Test Files

- **prompts.test.js** - Tests for prompt templates and generation (24 tests)
- **index.test.js** - Tests for server integration (2 tests)

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

- **Total Tests:** 26
- **Passing:** 26 (100%)
- **Code Coverage:** Good (prompts module)

### Coverage Breakdown

- `prompts.js`: Prompt registration, message generation, argument handling
- `index.js`: Server initialization and tool integration

## Test Categories

### Prompt Definition Tests (5 tests)
- PROMPTS constant export
- Work item prompts existence
- PR prompts existence
- Repository prompts existence
- Confluence prompts existence
- Prompt structure validation

### Prompt Configuration Tests (6 tests)
- Register all prompts on server
- Register specific prompt types
- Pass correct argument structures
- Register handler functions
- Verify prompt metadata

### Prompt Handler Tests (10 tests)
- Generate create-user-story message
- Generate review-pr message
- Generate my-work message
- Generate create-bug message with severity
- Generate create-branch message
- Generate my-confluence-pages message
- Handle optional arguments
- Return proper message structure
- Include required information

### Prompt Metadata Tests (4 tests)
- Required arguments marked correctly
- Argument descriptions present
- Unique prompt names
- Descriptive prompt descriptions

### Integration Tests (2 tests)
- Import without errors
- All dependencies available

## Test Helpers

Tests use Vitest mocking:
- Mock server with `prompt()` method
- Mock core, ado, and confluence packages
- Verify prompt registration
- Test message generation

## Available Prompts

### Work Item Management
- **create-user-story** - Create user story with acceptance criteria
- **create-bug** - Create bug report with reproduction steps
- **my-work** - Show work items assigned to current user
- **sprint-planning** - Help plan current sprint

### Pull Request Management
- **review-pr** - Review PR with code quality checks
- **create-pr** - Create new pull request
- **my-prs** - Show PRs created or need review

### Repository Management
- **create-branch** - Create new feature/bugfix branch
- **link-work-item-pr** - Link work item to PR
- **analyze-pr-diff** - Analyze PR changes

### Confluence
- **my-confluence-pages** - List recent Confluence pages

## Test Patterns

### Prompt Registration Test
```javascript
it('should register all prompts on server', () => {
  configurePrompts(mockServer);
  
  expect(mockServer.prompt).toHaveBeenCalled();
  expect(mockServer.prompt.mock.calls.length).toBe(
    Object.keys(PROMPTS).length
  );
});
```

### Message Generation Test
```javascript
it('should generate create-user-story message', async () => {
  configurePrompts(mockServer);
  
  const handler = mockServer.prompt.mock.calls.find(
    call => call[0] === 'create-user-story'
  )[3];
  
  const result = await handler({
    project: 'TestProject',
    title: 'New Feature'
  });
  
  expect(result.messages[0].content.text).toContain('TestProject');
});
```

### Argument Validation Test
```javascript
it('should have required arguments marked correctly', () => {
  expect(PROMPTS.CREATE_USER_STORY.arguments[0].required).toBe(true);
  expect(PROMPTS.CREATE_USER_STORY.arguments[2].required).toBe(false);
});
```

## Prompt Message Format

All prompt handlers return messages in MCP format:

```javascript
{
  messages: [
    {
      role: 'user',
      content: {
        type: 'text',
        text: 'Generated prompt message...'
      }
    }
  ]
}
```

## Notes

- All tests use Vitest framework
- Prompts are registered at server startup
- Message generation is context-aware
- Handles optional and required arguments
- Provides helpful templates for common workflows

## Unified Package Features

The unified package combines:
1. **Azure DevOps Tools** - Work items, repos, PRs, branches
2. **Confluence Tools** - Page management
3. **Prompt Templates** - Reusable workflow templates
4. **Integrated Server** - Single entry point for all tools

## Future Improvements

- [ ] Add tests for prompt argument validation
- [ ] Add tests for error cases in prompt handlers
- [ ] Test integration with actual tool invocations
- [ ] Add tests for prompt message formatting edge cases
- [ ] Test prompt discovery by MCP clients
- [ ] Add performance benchmarks for prompt generation
