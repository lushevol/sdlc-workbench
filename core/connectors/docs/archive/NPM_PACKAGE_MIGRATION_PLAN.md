> **⚠️ ARCHIVED** — This document captures the original migration plan. The migration is complete. See [SETUP.md](../SETUP.md) for current configuration documentation.

# NPM Package Migration Plan - Command-Line Arguments Approach

## Overview

This document outlines the plan to migrate the node-mcp-server from local config.json to command-line arguments, enabling NPM package distribution with VS Code one-click install buttons.

**Target State:** Match Azure DevOps MCP Server architecture and user experience exactly.

**Distribution:** Private NPM registry (SCB internal) - package will be available only to Standard Chartered Bank users.

## Current State vs Target State

### Current (Local Development)
```json
// config.json
{
  "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/sc-ado",
  "AZURE_DEVOPS_PAT": "abc123token",
  "HTTPS_PROXY": "http://10.239.9.190:443",
  "CONFLUENCE_BASE_URL": "https://confluence.example.com",
  "CONFLUENCE_USERNAME": "user@example.com",
  "CONFLUENCE_API_TOKEN": "token123"
}
```

### Target (NPM Package)
```bash
npx your-package-name \
  "https://dev.azure.com/sc-ado" \
  "abc123token" \
  "http://10.239.9.190:443" \
  "https://confluence.example.com" \
  "user@example.com" \
  "token123"
```

---

## Implementation Steps

### Step 1: Update `src/index.js` - Config Loading

**Current Code:**
```javascript
function getConfig() {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const configPath = path.resolve(__dirname, "../config.json");
  let config;
  try {
    config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  } catch (err) {
    throw new Error(`Failed to load config.json: ${err.message}`);
  }

  const { AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT, CONFLUENCE_BASE_URL = '', 
    CONFLUENCE_USERNAME = '', CONFLUENCE_API_TOKEN = '', HTTPS_PROXY= '' } = config || {};

  if (!AZURE_DEVOPS_ORG_URL || !AZURE_DEVOPS_PAT) {
    throw new Error('AZURE_DEVOPS_ORG_URL and AZURE_DEVOPS_PAT must be defined in config.json');
  }

  const confluenceConfig = {
    baseUrl: CONFLUENCE_BASE_URL,
    username: CONFLUENCE_USERNAME,
    apiToken: CONFLUENCE_API_TOKEN
  };

  return { AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT, confluenceConfig, HTTPS_PROXY };
}
```

**New Code:**
```javascript
function getConfig() {
  const args = process.argv.slice(2); // Skip 'node' and script path
  
  // Command-line arguments take precedence, fallback to environment variables
  const AZURE_DEVOPS_ORG_URL = args[0] || process.env.AZURE_DEVOPS_ORG_URL;
  const AZURE_DEVOPS_PAT = args[1] || process.env.AZURE_DEVOPS_PAT;
  const HTTPS_PROXY = args[2] || process.env.HTTPS_PROXY || '';
  const CONFLUENCE_BASE_URL = args[3] || process.env.CONFLUENCE_BASE_URL || '';
  const CONFLUENCE_USERNAME = args[4] || process.env.CONFLUENCE_USERNAME || '';
  const CONFLUENCE_API_TOKEN = args[5] || process.env.CONFLUENCE_API_TOKEN || '';

  // Validation
  if (!AZURE_DEVOPS_ORG_URL || !AZURE_DEVOPS_PAT) {
    throw new Error(
      'Azure DevOps configuration missing. Provide:\n' +
      '  - As arguments: node index.js <ORG_URL> <PAT> [PROXY] [CONF_URL] [CONF_USER] [CONF_TOKEN]\n' +
      '  - As env vars: AZURE_DEVOPS_ORG_URL and AZURE_DEVOPS_PAT\n'
    );
  }

  const confluenceConfig = {
    baseUrl: CONFLUENCE_BASE_URL,
    username: CONFLUENCE_USERNAME,
    apiToken: CONFLUENCE_API_TOKEN
  };

  // Log configuration (mask sensitive data)
  console.error('MCP Server Configuration:');
  console.error(`  Azure DevOps Org: ${AZURE_DEVOPS_ORG_URL}`);
  console.error(`  Azure DevOps PAT: ${AZURE_DEVOPS_PAT ? '***' + AZURE_DEVOPS_PAT.slice(-4) : 'Not set'}`);
  console.error(`  HTTPS Proxy: ${HTTPS_PROXY || 'Not set'}`);
  console.error(`  Confluence URL: ${CONFLUENCE_BASE_URL || 'Not set'}`);

  return { AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT, confluenceConfig, HTTPS_PROXY };
}
```

**Benefits:**
- ✅ Supports both command-line args and environment variables
- ✅ Better error messages
- ✅ Logs configuration for debugging (masks sensitive data)
- ✅ Backwards compatible with environment variables

---

### Step 2: Update `package.json` for NPM Publishing

**Add/Update these fields:**
```json
{
  "name": "@sc-ado/mcp-server",
  "version": "1.0.0",
  "description": "Standard Chartered Azure DevOps and Confluence MCP Server",
  "main": "src/index.js",
  "type": "module",
  "bin": {
    "sc-ado-mcp": "./src/index.js"
  },
  "files": [
    "src/**/*",
    "README.md",
    "LICENSE"
  ],
  "keywords": [
    "mcp",
    "model-context-protocol",
    "azure-devops",
    "confluence",
    "vscode",
    "standard-chartered"
  ],
  "author": "Saravanan R (1540326), Shiyamkumar U (2002918)",
  "license": "MIT",
  "publishConfig": {
    "registry": "https://your-scb-npm-registry.com"
  },
  "repository": {
    "type": "git",
    "url": "your-scb-repo-url"
  },
  "scripts": {
    "prepublishOnly": "node scripts/validate-package.js"
  }
}
```

**Key Fields Explained:**
- `bin`: Makes package executable via `npx` as `sc-ado-mcp`
- `files`: Only publish source code, not config.json
- `publishConfig.registry`: Points to SCB private NPM registry
- `prepublishOnly`: Run validation before publishing

**Note:** Update `publishConfig.registry` with actual SCB NPM registry URL before publishing.

---

### Understanding Package Name vs Binary Name

**`@sc-ado/mcp-server`** - NPM Package Name (Full Identifier)
- **What:** The complete package identifier in NPM registry
- **Format:** `@scope/package-name` where `@sc-ado` is the organization scope
- **Used for:**
  - Installing: `npx @sc-ado/mcp-server`
  - package.json: `"name": "@sc-ado/mcp-server"`
  - VS Code MCP config args: `["@sc-ado/mcp-server", ...]`
  - Importing: `import from '@sc-ado/mcp-server'`

**`sc-ado-mcp`** - Binary Command Name (Executable)
- **What:** The command name users run after installation
- **Format:** Simple command name (no @ or /)
- **Used for:**
  - Running directly: `sc-ado-mcp "https://dev.azure.com/sc-ado" "token"`
  - package.json: `"bin": { "sc-ado-mcp": "./src/index.js" }`
  - After global install: `npm install -g @sc-ado/mcp-server` → then just `sc-ado-mcp`

**Example Flow:**
```bash
# User runs with full package name
npx @sc-ado/mcp-server "org-url" "token"
      ↓
# NPM downloads package: @sc-ado/mcp-server
      ↓
# NPM creates binary command: sc-ado-mcp
      ↓
# NPX executes: sc-ado-mcp "org-url" "token"
```

**Comparison with Azure DevOps MCP:**
- **Their setup:** `@azure-devops/mcp` package → runs as `ado-mcp` (binary)
- **Your setup:** `@sc-ado/mcp-server` package → runs as `sc-ado-mcp` (binary)

**Note:** You can change the binary name independently of the package name by modifying the `bin` field in package.json.

---

### Step 3: Add Shebang to `src/index.js`

**Add at the very first line:**
```javascript
#!/usr/bin/env node
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
// ... rest of the code
```

This allows the script to be executed directly with `npx`.

---

### Step 4: Create VS Code MCP Configuration

**Full configuration with inputs:**
```json
{
  "inputs": [
    {
      "id": "ado_pat",
      "type": "promptString",
      "description": "Azure DevOps Personal Access Token",
      "password": true
    },
    {
      "id": "https_proxy",
      "type": "promptString",
      "description": "HTTPS Proxy URL (optional, press Enter to skip)"
    },
    {
      "id": "confluence_pat",
      "type": "promptString",
      "description": "Confluence API Token (optional, press Enter to skip)",
      "password": true
    }
  ],
  "sc-ado-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@sc-ado/"
      "-y",
      "@your-org/node-mcp-server",
      "${input:ado_pat}",
      "${input:https_proxy}",
      "${input:confluence_pat}"
    ]
  }
}
```

---

### Step 5: Create Install Button URL

**Tool to encode the configuration:**

```javascript
// scripts/create-install-url.js
const config = {
  "inputs": [
    {
      "id": "ado_pat",
      "type": "promptString",
      "description": "Azure DevOps Personal Access Token",
      "password": true
    },
    {
      "id": "https_proxy",
      "type": "promptString",
      "description": "HTTPS Proxy URL (optional, press Enter to skip)"
    }
  ]
};

const serverConfig = {
  "type": "stdio",
  "command": "npx",
  "argsc-ado/
    "-y",
    "@your-org/node-mcp-server",
    "${input:ado_pat}",
    "${input:https_proxy}"
  ]
};

// Encode configuration
const encodedConfig = encodeURIComponent(JSON.stringify(serverConfig));
const encodedInputs = encodeURIComponent(JSON.stringify(config.inputs));

// Create URLs
const stableUrl = `https://insiders.vscode.dev/redirect/mcp/install?name=sc-ado-mcp&config=${encodedConfig}&inputs=${encodedInputs}`;
const insidersUrl = `https://insiders.vscode.dev/redirect/mcp/install?name=sc-ado-mcp&quality=insiders&config=${encodedConfig}&inputs=${encodedInputs}`;

console.log('VS Code Stable URL:');
console.log(stableUrl);
console.log('\nVS Code Insiders URL:');
console.log(insidersUrl);

// Markdown badges
console.log('\n\nMarkdown Badges:');
console.log(`[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SCB_ADO_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](${stableUrl})`);
console.log(`[![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SCB_ADO_MCP_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](${insidersUrl})`);
```

**Run to generate URLs:**
```bash
node scripts/create-install-url.js
```

---

### Step 6: Update README.md

**Replace Quick Start section with:**
```markdown
## Quick Start

### ✨ One-Click Install (Recommended)

Click the button below to install the MCP server from SCB NPM registry:

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SCB_ADO_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](GENERATED_STABLE_URL_HERE)
[![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SCB_ADO_MCP_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](GENERATED_INSIDERS_URL_HERE)

**What happens when you click:**
1. VS Code prompts you for Azure DevOps credentials
2. NPM automatically downloads the latest version from SCB registry
3. Server is configured and ready to use
4. No manual installation required!

**You'll be prompted for:**
- Azure DevOps Organization URL (e.g., `https://dev.azure.com/sc-ado`)
- Azure DevOps Personal Access Token
- HTTPS Proxy (optional, e.g., `http://10.239.9.190:443`)
- Confluence credentials (optional)

> **Note:** This package is available only on Standard Chartered's private NPM registry.

### Manual Setup

For local development or if you prefer manual configuration:

1. **Install from SCB NPM registry:**
   ```bash
   npx @sc-ado/mcp-server \
     "https://dev.azure.com/sc-ado" \
     "your-pat-token" \
     "http://10.239.9.190:443"
   ```

2. **Or clone for development:**
   ```bash
   git clone <scb-repo-url>
   cd 23966-node-mcp-server
   npm install
   node src/index.js "https://dev.azure.com/sc-ado" "your-pat-token" "http://10.239.9.190:443"
   ```
```

---

### Step 7: Testing Plan

**Test Local Execution:**
```bash
# Test with command-line arguments
node src/index.js \
  "https://dev.azure.com/sc-ado" \
  "your-pat-token" \
  "http://10.239.9.190:443"

# Test with environment variables
export AZURE_DEVOPS_ORG_URL="https://dev.azure.com/sc-ado"
export AZURE_DEVOPS_PAT="your-pat-token"
node src/index.js

# Test error handling (missing required args)
node src/index.js
```

**Test NPM Local Package:**
```bash
# Create local NPM link
npm link

# Test as if installed from NPM
npx sc-ado-mcp "https://dev.azure.com/sc-ado" "your-pat-token" "http://10.239.9.190:443"

# Or test with full package name
npx @sc-ado/mcp-server "https://dev.azure.com/sc-ado" "your-pat-token"

# Unlink when done
npm unlink
```

**Test VS Code Integration:**
1. Update `.vscode/mcp.json` with new configuration
2. Restart MCP server in VS Code
3. Test tool execution in Copilot Chat
4. Verify authentication works
5. Test error scenarios

---

### Step 8: NPM Publishing Steps (SCB Private Registry)

**Prerequisites:**
1. Configure NPM to use SCB registry: `npm config set registry https://your-scb-npm-registry.com`
2. Login to SCB NPM registry: `npm login --registry=https://your-scb-npm-registry.com`
3. Verify authentication: `npm whoami --registry=https://your-scb-npm-registry.com`
4. Verify package name is available: `npm view @sc-ado/mcp-server`

**Publishing Process:**

```bash
# 1. Ensure package.json is correct with SCB registry
npm pack --dry-run

# 2. Check what will be published
npm pack
tar -tzf sc-ado-mcp-server-1.0.0.tgz

# 3. Publish to SCB NPM registry (first time)
npm publish --registry=https://your-scb-npm-registry.com

# 4. Publish updates
npm version patch  # or minor/major
npm publish --registry=https://your-scb-npm-registry.com

# 5. Test installation from SCB registry
npx @sc-ado/mcp-server@latest \
  "https://dev.azure.com/sc-ado" \
  "test-token" \
  --registry=https://your-scb-npm-registry.com
```

**Important Notes:**
- Replace `https://your-scb-npm-registry.com` with actual SCB NPM registry URL
- Ensure you have publishing permissions on SCB registry
- Package will only be accessible to SCB users with registry access

**Version Management:**
- `npm version patch` - Bug fixes (1.0.0 → 1.0.1)
- `npm version minor` - New features (1.0.0 → 1.1.0)
- `npm version major` - Breaking changes (1.0.0 → 2.0.0)

---

### Step 9: Backwards Compatibility

**Support Both Approaches During Transition:**

```javascript
function getConfig() {
  const args = process.argv.slice(2);
  
  // Try command-line arguments first
  if (args.length > 0) {
    return getConfigFromArgs(args);
  }
  
  // Fallback to environment variables
  if (process.env.AZURE_DEVOPS_ORG_URL) {
    return getConfigFromEnv();
  }
  
  // Finally, try config.json (for local development)
  try {
    return getConfigFromFile();
  } catch (err) {
    throw new Error(
      'Configuration not found. Provide via:\n' +
      '  1. Command-line args: node index.js <ORG_URL> <PAT>\n' +
      '  2. Environment variables: AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT\n' +
      '  3. config.json file (local development only)'
    );
  }
}
```

---

## Benefits Summary

### For End Users
✅ **No cloning required** - Install directly from NPM  
✅ **Guided setup** - VS Code prompts for all config values  
✅ **Secure** - Credentials stored in VS Code settings, not files  
✅ **Auto-updates** - Use `@latest` to always get newest version  
✅ **One-click install** - Single button in README

### For Developers
✅ **Easy distribution** - Publish to NPM registry  
✅ **Version control** - Semantic versioning with NPM  
✅ **No config file conflicts** - No more gitignored config.json  
✅ **Better debugging** - Clear error messages with config logging  
✅ **Professional** - Matches industry standard (Azure DevOps MCP)

---

## Migration Checklist

- [ ] Update `src/index.js` - Replace `getConfig()` function
- [ ] Add shebang `#!/usr/bin/env node` to `src/index.js`
- [ ] Update `package.json` - Add `bin`, `files`, `publishConfig`
- [ ] Create `scripts/create-install-url.js` - URL generator
- [ ] Test local execution with command-line args
- [ ] Test with `npm link` locally
- [ ] Generate install button URLs
- [ ] Update README.md with new install buttons
- [ ] Confirm SCB NPM registry URL
- [ ] Configure NPM CLI for SCB registry
- [ ] Login to SCB NPM registry: `npm login --registry=<SCB_REGISTRY_URL>`
- [ ] Verify publishing permissions
- [ ] Publish to SCB registry: `npm publish --registry=<SCB_REGISTRY_URL>`
- [ ] Test installation from SCB registry: `npx @sc-ado/mcp-server`
- [ ] Test VS Code integration with new config
- [ ] Update documentation (SETUP.md, etc.)
- [ ] Announce to users and provide migration guide

---

## Rollback Plan

If issues occur after migration:
sc-ado/mcp-server@1.0.0 --registry=<SCB_REGISTRY_URL>
1. **Keep config.json support** - Add backwards compatibility
2. **Document both methods** - Allow users to choose
3. **Unpublish if critical** - `npm unpublish @your-org/node-mcp-server@1.0.0`
4. **Fix and republish** - Increment version and fix issues

---

## Questions to Resolve Before Implementation

1. **SCB NPM Registry URL:** What is the exact URL of SCB's private NPM registry?
   - Need: Registry URL for `publishConfig` in package.json
   - Need: Authentication instructions for SCB users

2. **Package Name:** Confirm final package name
   - Proposed: `@sc-ado/mcp-server`
   - Alternative: `@standardchartered/ado-mcp-server`

3. **Confluence Config:** Should Confluence remain optional or required?
   - ✅ Decided: Optional (user can skip during prompts)

4. **Proxy Handling:** Should proxy be auto-detected or always prompted?
   - ✅ Decided: Always prompt, optional skip (common at SCB)

5. **Publishing Permissions:** Who has access to publish to SCB NPM registry?
   - Need: Verify your accounts (1540326, 2002918) have publishing rights

---

## Timeline Estimate

- **Code changes:** 2-3 hours
- **Testing:** 2-3 hours  
- **NPM setup & publishing:** 1 hour
- **Documentation updates:** 1-2 hours
- **Total:** 6-9 hours

---

## References

- [Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp) - Reference implementation
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/chat/mcp)
- [NPM Publishing Guide](https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)

---

*Last Updated: January 31, 2026*
*Authors: Saravanan R (1540326), Shiyamkumar U (2002918)*
