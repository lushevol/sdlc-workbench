> **⚠️ ARCHIVED** — See [SETUP.md](../SETUP.md) for current configuration documentation.

# MCP Configuration Guide

This guide explains the different MCP configuration files and when to use each one.

## 📁 Configuration Files

### 1. `mcp.json.template`
**Purpose:** Master template with all configuration options documented  
**Use:** Reference for understanding all available options  
**Contains:** Production setup (active) + Local development options (commented)

### 2. `mcp.json.production`
**Purpose:** Production-ready configuration for end users  
**Use:** Share this with users for one-click install  
**Setup:** Uses `npx` to install from artifactory registry  
**Requires:** 
- NPM registry access to artifactory
- Or `.npmrc` file with registry configuration

### 3. `mcp.json.local`
**Purpose:** Local development configuration  
**Use:** Copy to `.vscode/mcp.json` for local development  
**Setup:** Runs directly from source with `node`  
**Best for:** Active development and debugging

## 🚀 Quick Start

### For Local Development
```bash
# Copy local config
cp mcp.json.local .vscode/mcp.json

# Restart MCP server in VS Code
# Cmd+Shift+P → "MCP: Restart Server"
```

### For Production Testing (with yarn link)
```bash
# Link all packages
cd packages/core && yarn link
cd ../ado && yarn link
cd ../confluence && yarn link
cd ../unified && yarn link
cd ../unified && yarn link "@sc-node-mcp/core" "@sc-node-mcp/ado" "@sc-node-mcp/confluence"

# Use npx in mcp.json (it will use linked version)
cp mcp.json.production .vscode/mcp.json
# Edit to remove --registry flag since you're using yarn link

# Restart MCP server
```

### For End Users (Production)
```bash
# Option 1: Create .npmrc file
echo '@sc-node-mcp:registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release' > ~/.npmrc

# Option 2: Or use --registry flag in mcp.json (already included in mcp.json.production)
cp mcp.json.production .vscode/mcp.json
```

## 🔧 Configuration Differences

| Feature | Local | Production |
|---------|-------|-----------|
| Command | `node` | `npx` |
| Install Required | ❌ No | ✅ Yes (or yarn link) |
| Registry Access | ❌ Not needed | ✅ Required |
| Live Reload | ✅ Instant | ⚠️ Needs republish |
| Speed | ⚡ Fastest | 🐢 Slower (first run) |
| Use Case | Development | Distribution |

## 📝 Environment Variables

All configurations use the same environment variables for security:
- `AZURE_DEVOPS_PAT` - Azure DevOps Personal Access Token (required)
- `HTTPS_PROXY` - Corporate proxy URL (optional)
- `CONFLUENCE_USERNAME` - Confluence username (optional)
- `CONFLUENCE_API_TOKEN` - Confluence API token (optional)
- `NODE_TLS_REJECT_UNAUTHORIZED=0` - Disable TLS verification (corporate proxy)

## 🔍 Troubleshooting

### Server stops immediately
- Check that `import.meta.url` check is removed from index.js
- Ensure all dependencies are installed (`npm install` or `yarn install`)
- Verify yarn link is set up correctly if using npx

### Cannot find package
- Verify `.npmrc` exists with correct registry
- Or use `--registry` flag in args
- Check package is published: `npm view @sc-node-mcp/unified`

### Wrong version running
- Clear npx cache: `npx clear-npx-cache`
- Unlink and relink: `yarn unlink && yarn link`
- Restart VS Code

## 📦 Publishing Checklist

Before publishing to production:
1. ✅ Commit all changes
2. ✅ Update version: `npm version patch`
3. ✅ Test with yarn link
4. ✅ Publish: `npx lerna publish from-package --yes`
5. ✅ Test with clean npx install
6. ✅ Update one-click install URL if needed
