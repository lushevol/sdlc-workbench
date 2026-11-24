# @sc-node-mcp/confluence

Confluence MCP Server for page management.

## ✅ Current Status: Functional

Confluence integration is fully operational. Use this package standalone or as part of **@sc-node-mcp/unified** for a combined ADO + Confluence experience.

## Overview

This package provides Confluence integration through the Model Context Protocol. 

**Tools (15):**
- `confluence_list_my_pages` - List Confluence pages created by the authenticated user
- `confluence_search` - Search Confluence content using CQL (Confluence Query Language)
- `confluence_get_page_id` - Look up a Confluence page ID and metadata from its URL
- `confluence_update_page` - Update the content of an existing Confluence page
- `confluence_create_page` - Create a new Confluence page under a parent page
- `confluence_read_page` - Read the full content of a Confluence page from its URL (Cloud and Server-style URLs supported)
- `confluence_get_page` - Get a Confluence page by its numeric ID (view, storage, and export_view formats)
- `confluence_find_page` - Find a Confluence page by space key and exact title
- `confluence_get_page_children` - List the child pages of a Confluence page by its ID
- `confluence_list_spaces` - List Confluence spaces (global spaces by default)
- `confluence_get_space` - Get details of a Confluence space by its key
- `confluence_delete_page` - Delete a Confluence page by ID (title confirmation required)
- `confluence_add_comment` - Add a page-level comment to a Confluence page
- `confluence_get_labels` - Get all labels on a Confluence page
- `confluence_add_label` - Add a label to a Confluence page

**Confluence Base URL is hardcoded:** `https://confluence.global.standardchartered.com`

## Installation

```bash
yarn add @sc-node-mcp/confluence
```

## Configuration

Requires a Confluence PAT (Personal Access Token / Bearer Token):

```json
{
  "CONFLUENCE_PAT": "your-confluence-bearer-token"
}
```

Or via environment variable:
```bash
export CONFLUENCE_PAT="your-confluence-bearer-token"
```

## Use with Unified Package

For all available tools including Azure DevOps and Nexus IQ, use the unified package:

```bash
npx -y @sc-node-mcp/unified \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "your-confluence-pat"
```

See [Installation Guide](../../docs/INSTALLATION.md) for complete setup instructions.

## Prompts

The `@sc-node-mcp/confluence` package ships 15 MCP prompts for guided Confluence workflows:

- `confluence-create-page` — Create a new Confluence page under a parent
- `confluence-update-page` — Update the content of an existing page
- `confluence-search` — Search Confluence content using CQL
- `confluence-read-page` — Read the full content of a page
- `confluence-list-my-pages` — List pages created by the authenticated user
- `confluence-get-page-id` — Look up a page ID from its URL

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## Dependencies

- `@sc-node-mcp/core` - Core MCP infrastructure
- `axios` - HTTP client for Confluence REST API
