# SC Wiki Package Tests

This directory contains comprehensive tests for the SC Wiki (XWiki) MCP server package.

## Test Structure

### Test Files

- **scwiki.test.js** - Tests for SC Wiki tool functionality, the page-reference parser, and the browser-URL parser
- **tools.test.js** - Tests for tools module configuration
- **prompts.test.js** - Tests for prompt registration

## Running Tests

```bash
# Run all tests
yarn test

# Run tests in watch mode
yarn test:watch

# Generate coverage report
yarn test:coverage
```

## Test Categories

### SC Wiki Tool Tests
Each of the 14 tools has a success-path test (mocked axios response) and an error-path test
(mocked axios rejection): `scwiki_search`, `scwiki_get_page`, `scwiki_find_page`,
`scwiki_create_page`, `scwiki_update_page`, `scwiki_delete_page`, `scwiki_get_page_children`,
`scwiki_list_spaces`, `scwiki_list_my_pages`, `scwiki_add_comment`, `scwiki_get_labels`,
`scwiki_add_label`, `scwiki_get_page_history`, `scwiki_list_attachments`.

### Reference/URL Parser Tests
- `parsePageReference` — simple, nested-space, escaped-dot, and `wiki:`-prefixed references;
  invalid references throw.
- `buildPagePath` — REST path construction, including URL-encoding of space names with spaces.
- `parseViewUrl` — resolves a `/bin/view/...` browser URL to a dotted reference, including the
  confirmed `WebHome`-default-on-trailing-slash behavior.
