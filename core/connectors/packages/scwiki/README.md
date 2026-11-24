# @sc-node-mcp/scwiki

SC Wiki (XWiki) MCP Server for page management — Bearer token auth.

## ✅ Current Status: Functional

SC Wiki integration is fully operational. Use this package standalone or as part of **@sc-node-mcp/unified** for a combined ADO + SC Wiki experience.

## Overview

This package provides SC Wiki (XWiki) integration through the Model Context Protocol. Pages are
addressed by a dotted reference (e.g. `Sandbox.S2B NG.WebHome`) rather than a numeric ID — nested
spaces are chained with dots, and the final segment is the page name.

**Tools (14):**
- `scwiki_search` - Search SC Wiki pages by keyword across title, content, and page name
- `scwiki_get_page` - Get an SC Wiki page's metadata and content by its dotted reference
- `scwiki_find_page` - Look up an SC Wiki page from its browser URL
- `scwiki_create_page` - Create a new SC Wiki page at the given dotted reference (upsert)
- `scwiki_update_page` - Update the title and/or content of an existing SC Wiki page
- `scwiki_delete_page` - Delete an SC Wiki page by its dotted reference (title confirmation required — moved to recycle bin, not permanently deleted)
- `scwiki_get_page_children` - List the direct child pages of an SC Wiki page
- `scwiki_list_spaces` - List the top-level spaces in the configured SC Wiki instance
- `scwiki_list_my_pages` - List SC Wiki pages created by the authenticated user
- `scwiki_add_comment` - Add a comment to an SC Wiki page
- `scwiki_get_labels` - Get all tags on an SC Wiki page
- `scwiki_add_label` - Add a tag to an SC Wiki page
- `scwiki_get_page_history` - Get the version history of an SC Wiki page
- `scwiki_list_attachments` - List the attachments on an SC Wiki page (metadata only)

**SC Wiki Base URL defaults to** `https://scwiki.global.standardchartered.com` but can be
overridden via the `SCWIKI_URL` environment variable — the one exception among this repo's
services where the base URL is not fully hardcoded.

## Installation

```bash
yarn add @sc-node-mcp/scwiki
```

## Configuration

Requires an SC Wiki Bearer token, issued via XWiki's **Token Authenticator** extension:

```json
{
  "SCWIKI_TOKEN": "your-scwiki-bearer-token"
}
```

Or via environment variable:
```bash
export SCWIKI_TOKEN="your-scwiki-bearer-token"
```

To override the default SC Wiki URL (e.g. for a different environment):
```bash
export SCWIKI_URL="https://your-scwiki-instance.example.com"
```

## Use with Unified Package

For all available tools including Azure DevOps and Confluence, use the unified package:

```bash
npx -y @sc-node-mcp/unified \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "" "" "" "" \
  "your-scwiki-bearer-token"
```

See [Installation Guide](../../docs/INSTALLATION.md) for complete setup instructions.

## Prompts

The `@sc-node-mcp/scwiki` package ships 14 MCP prompts for guided SC Wiki workflows, including
`search-scwiki`, `get-scwiki-page`, `find-scwiki-page`, `create-scwiki-page`, `update-scwiki-page`,
and `delete-scwiki-page`.

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## Dependencies

- `@sc-node-mcp/core` - Core MCP infrastructure
- `axios` - HTTP client for the XWiki REST API
