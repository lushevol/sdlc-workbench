# Installation Guide

Complete guide for installing and setting up the SC Node MCP Server across different environments and use cases.

## 📋 Prerequisites

Before installing, ensure you have:

- **Node.js 20+** installed ([download here](https://nodejs.org/))
- **Azure DevOps Personal Access Token (PAT)** with permissions:
  - Code: Read & Write
  - Work Items: Read & Write
  - Project and Team: Read
- **Access to Standard Chartered's NPM Registry** (artifactory.global.standardchartered.com)
- **Corporate proxy configuration** (if behind SCB firewall)

### Verify Node.js Installation

```bash
node --version  # Should show v20.x.x or higher
```

---

## 🎯 Installation Methods

Choose the installation method that best fits your use case:

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **One-Click Install** | VS Code users | ✅ Easiest setup<br>✅ Automatic configuration<br>✅ No terminal commands | ⚠️ VS Code only |
| **NPX Direct Execution** | Quick testing, CI/CD | ✅ No installation needed<br>✅ Always latest version<br>✅ Great for scripts | ⚠️ Slower startup<br>⚠️ Downloads each time |
| **Global Installation** | Regular use across projects | ✅ Fast startup<br>✅ Available everywhere<br>✅ Binary commands | ⚠️ Manual updates needed |
| **Local Development** | Contributing to project | ✅ Full control<br>✅ Can modify code<br>✅ Run tests | ⚠️ Most complex setup |

---

## 1️⃣ One-Click Install (Recommended for VS Code)

### Quick Installation

Click one of these buttons to install directly in VS Code:

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SC_NODE_MCP/UNIFIED-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

[![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SC_NODE_MCP/UNIFIED-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

### What Happens When You Click?

1. **VS Code opens** and shows an install confirmation dialog
2. **You're prompted for up to 7 configuration values:**
   - Azure DevOps Personal Access Token (masked, required)
   - HTTPS Proxy URL (optional, e.g., `http://10.239.9.190:443`)
   - Confluence PAT / Bearer Token (optional, enables Confluence tools)
   - Nexus IQ User Code (optional, enables Nexus tools)
   - Nexus IQ Pass Code (optional, enables Nexus tools)
   - SonarQube Token (optional, enables SonarQube tools)
   - CODE_REVIEW_GUIDE.md file path (optional, enables custom PR review guidelines)
3. **NPM automatically downloads** the latest version from SCB artifactory
4. **Server starts immediately** and tools are available in Copilot Chat!

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`), Confluence Base URL (`https://confluence.global.standardchartered.com`), Nexus URL, and SonarQube URL are all hardcoded in the server configuration.

### Configuration Location

After installation, your configuration is stored in one of these places:
- **Workspace setup:** `.vscode/mcp.json`
- **One-click install:** Managed by the VS Code MCP extension in user settings

---

## 2️⃣ NPX Direct Execution

Run the MCP server directly without installing it. Perfect for testing, CI/CD pipelines, or one-off usage.

### Unified Server (All Tools)

```bash
npx -y @sc-node-mcp/unified \
  "your-pat-token-here" \
  "http://10.239.9.190:443" \
  "your-confluence-pat-bearer-token"
```

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`) and Confluence URL (`https://confluence.global.standardchartered.com`) are hardcoded.

### ADO Tools Only

```bash
npx -y @sc-node-mcp/ado \
  "your-pat-token-here" \
  "http://10.239.9.190:443"
```

### Nexus IQ Tools

```bash
npx -y @sc-node-mcp/nexus \
  "" \
  "http://10.239.9.190:443" \
  "" \
  "your-nexus-user-code" \
  "your-nexus-pass-code"
```

### Parameter Breakdown

| Position | Parameter | Required | Example | Description |
|----------|-----------|----------|---------|-------------|
| 1 | ADO PAT | ✅ Yes | `your-pat-token` | Personal Access Token with Code & Work Items permissions |
| 2 | Proxy URL | ⚠️ Optional | `http://10.239.9.190:443` | HTTPS proxy if behind corporate firewall |
| 3 | Confluence PAT | ⚠️ Optional | `your-confluence-pat` | Confluence Bearer token — enables Confluence tools when provided |
| 4 | Nexus User Code | ⚠️ Optional | `nexus-user` | Nexus IQ username — enables Nexus tools when provided with password |
| 5 | Nexus Pass Code | ⚠️ Optional | `nexus-pass` | Nexus IQ password — enables Nexus tools when provided with username |
| 6 | SonarQube Token | ⚠️ Optional | `your-sonar-token` | SonarQube Bearer token — enables SonarQube tools when provided |

> **💡 Tip:** Pass `CODE_REVIEW_GUIDE_FILE` as an environment variable (or via the `code_review_guide` input in the one-click installer) to enable custom PR review guidelines.

### Use Cases

**✅ Perfect for:**
- Quick testing without installation
- CI/CD pipeline scripts
- One-time operations
- Always using the latest version

**❌ Not ideal for:**
- Regular daily use (slower startup)
- Offline environments (requires download)
- Bandwidth-constrained networks

---

## 3️⃣ Global Installation

Install the MCP server globally to use it across all your projects with fast startup times.

### Installation Commands

```bash
# Install unified server (recommended)
yarn global add @sc-node-mcp/unified

# Or install specific packages
yarn global add @sc-node-mcp/ado        # ADO tools only
yarn global add @sc-node-mcp/confluence  # Confluence tools only
yarn global add @sc-node-mcp/nexus       # Nexus IQ vulnerability scanning
```

### Running After Installation

After global installation, use the binary commands:

```bash
# Unified server binary
sc-node-mcp \
  "your-pat-token" \
  "http://10.239.9.190:443" \
  "your-confluence-pat"

# ADO-only binary
sc-node-mcp-ado \
  "your-pat-token" \
  "http://10.239.9.190:443"

# Nexus IQ binary
sc-node-mcp-nexus \
  "" \
  "http://10.239.9.190:443" \
  "" \
  "your-nexus-user-code" \
  "your-nexus-pass-code"
```

> **Note:** URLs are hardcoded: Azure DevOps (`https://dev.azure.com/sc-ado`), Confluence (`https://confluence.global.standardchartered.com`)

### Checking Installation

```bash
# Verify installation
yarn global list | grep sc-node-mcp
which sc-node-mcp  # Unix/macOS
where sc-node-mcp  # Windows
```

### Updating

```bash
# Update to latest version
yarn global upgrade @sc-node-mcp/unified

# Or reinstall
yarn global remove @sc-node-mcp/unified
yarn global add @sc-node-mcp/unified
```

---

## 4️⃣ Local Development Setup

For developers contributing to this project or needing local modifications.

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd sc-node-mcp
```

#### 2. Install Dependencies

```bash
yarn install
```

This installs dependencies for all packages in the monorepo using Lerna.

#### 3. Build All Packages

```bash
yarn build
```

#### 4. Configure Credentials

Create `config.json` in the project root:

```json
{
  "AZURE_DEVOPS_PAT": "your-personal-access-token-here",
  "HTTPS_PROXY": "http://10.239.9.190:443",
  "CONFLUENCE_PAT": "your-confluence-bearer-token",
  "NEXUS_USER_CODE": "your-nexus-username",
  "NEXUS_PASS_CODE": "your-nexus-password"
}
```

> **⚠️ Security:** `config.json` is in `.gitignore`. Never commit credentials!  
> **Note:** Azure DevOps Org URL and Confluence Base URL are hardcoded in the application.

#### 5. Configure VS Code MCP Extension

Edit `.vscode/mcp.json`:

```jsonc
{
  "mcpServers": {
    "sc-node-mcp": {
      "command": "node",
      "args": ["${workspaceFolder}/packages/unified/src/index.js"]
    }
  }
}
```

#### 6. Run the Server

```bash
# Unified server (ADO + Confluence)
node packages/unified/src/index.js

# ADO server only
node packages/ado/src/index.js

# Confluence server only
node packages/confluence/src/index.js

# Nexus IQ server only
node packages/nexus/src/index.js
```

#### 7. Run Tests

```bash
# Run all tests
yarn test

# Run tests for specific package
cd packages/ado
yarn test

# Watch mode
yarn test:watch

# With coverage
yarn test:coverage
```

### Development Workflow

```bash
# Make changes to code
vim packages/ado/src/tools/workItems.js

# Run tests
yarn test

# Build packages
yarn build

# Test in VS Code
# Restart MCP server from VS Code MCP extension
```

---

## 🔐 SCB Artifactory Authentication

The npm packages are published to Standard Chartered's private NPM registry. You need to authenticate before installation.


### Configure NPM Registry Access

> **Tip:**
> To set the SCB Artifactory registry as the default for all npm packages (not just @sc-node-mcp), run:
> ```bash
> npm config set registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/ --global
> ```
> This is optional, but may simplify setup if you only use SCB's registry.

#### Option 1: .npmrc File (Recommended)

Create or edit `~/.npmrc`:

```ini
# SCB Artifactory Registry
@sc-node-mcp:registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/

# Authentication (use your SCB credentials)
//artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/:_auth=<BASE64_ENCODED_CREDENTIALS>
//artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/:always-auth=true

# Or use auth token (if available)
//artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/:_authToken=<YOUR_AUTH_TOKEN>

# Proxy configuration (if needed)
proxy=http://10.239.9.190:443
https-proxy=http://10.239.9.190:443
```

#### Option 2: NPM Login (Interactive)

```bash
npm login --registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/ --scope=@sc-node-mcp
```

#### Generating Base64 Credentials

```bash
# Unix/macOS
echo -n "username:password" | base64

# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("username:password"))
```

### Verifying Registry Access

```bash
# Check registry configuration
npm config get @sc-node-mcp:registry

# Test package access
npm view @sc-node-mcp/unified

# Search for packages
npm search @sc-node-mcp
```

---

## 🌐 Proxy Configuration

If you're behind Standard Chartered's corporate firewall, configure proxy settings.

### NPM Proxy Configuration

```bash
# Set proxy for npm
npm config set proxy http://10.239.9.190:443
npm config set https-proxy http://10.239.9.190:443

# Verify proxy settings
npm config get proxy
npm config get https-proxy
```

### Verify Proxy Connection

```bash
# Test connection through proxy
curl -x http://10.239.9.190:443 https://artifactory.global.standardchartered.com

# Test npm registry access
npm ping --registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/
```

---

## 🔧 VS Code MCP Extension Configuration

### For NPX Installation

Edit `.vscode/mcp.json` (or workspace settings):

```jsonc
{
  "mcpServers": {
    "sc-node-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@sc-node-mcp/unified",
        "${input:ado_pat}",
        "${input:https_proxy}",
        "${input:confluence_pat}"
      ]
    }
  },
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
  ]
}
```

> **Note:** Azure DevOps Org URL and Confluence Base URL are hardcoded in the server.

### For Global Installation

```jsonc
{
  "mcpServers": {
    "sc-node-mcp": {
      "command": "sc-node-mcp",
      "args": [
        "${input:ado_pat}",
        "${input:https_proxy}",
        "${input:confluence_pat}"
      ]
    }
  },
  "inputs": [
    // ... same inputs as above
  ]
}
```

### For Local Development

```jsonc
{
  "mcpServers": {
    "sc-node-mcp": {
      "command": "node",
      "args": ["${workspaceFolder}/packages/unified/src/index.js"]
    }
  }
}
```

> **Note:** Local development reads credentials from `config.json`, so no inputs needed.

---

## ❓ Troubleshooting

### Common Issues

#### 1. "Cannot find package '@sc-node-mcp/unified'"

**Cause:** Not authenticated with SCB artifactory.

**Solution:**
```bash
# Configure registry authentication (see SCB Artifactory Authentication section)
npm config set @sc-node-mcp:registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/
```

#### 2. "ECONNREFUSED" or "ETIMEDOUT"

**Cause:** Proxy configuration issue.

**Solution:**
```bash
# Set proxy
npm config set proxy http://10.239.9.190:443
npm config set https-proxy http://10.239.9.190:443

# Or use environment variables
export HTTPS_PROXY=http://10.239.9.190:443
export HTTP_PROXY=http://10.239.9.190:443
```

#### 3. "401 Unauthorized" When Installing

**Cause:** Invalid or expired credentials.

**Solution:**
```bash
# Re-authenticate
npm logout --registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/
npm login --registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/ --scope=@sc-node-mcp

# Or regenerate Base64 credentials
echo -n "username:password" | base64
```

#### 4. "npx -y @sc-node-mcp/unified" Downloads Every Time

**Cause:** npx doesn't cache packages with `-y` flag in some configurations.

**Solution:** Use global installation instead:
```bash
yarn global add @sc-node-mcp/unified
sc-node-mcp <args...>
```

#### 5. "Cannot find module ...@modelcontextprotocol/sdk/server/mcp.js" (ERR_MODULE_NOT_FOUND)

**Cause:** A previous `npx` run for this package was interrupted (network drop, antivirus quarantine, disk full, etc.) and left a corrupted/incomplete install cached under npx's hash-keyed cache directory. Because `npx` reuses that cached install on subsequent runs, the same broken copy keeps getting reused until the cache is cleared manually — it does not repair itself.

**Solution:** Clear the npx cache and let it re-download a clean copy:
```bash
# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx"
npm cache clean --force

# macOS / Linux
rm -rf ~/.npm/_npx
npm cache clean --force
```
Then restart VS Code (or re-run the `npx` command) so it performs a fresh install.

#### 6. VS Code MCP Extension Doesn't Start Server

**Cause:** VS Code can't find the command or incorrect `.vscode/mcp.json`.

**Solution:**
```bash
# Verify installation
which sc-node-mcp  # Should show path
node --version     # Should be 20+

# Check VS Code MCP extension logs
# VS Code > Output > Select "MCP" from dropdown
```

#### 7. "TLS certificate verification failed"

**Cause:** Corporate proxy with SSL inspection.

**Solution:** This is handled automatically in the code (`NODE_TLS_REJECT_UNAUTHORIZED=0`), but if you see this error:
```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0
yarn global add @sc-node-mcp/unified
```

### Getting Help

If you're still stuck:

1. **Check logs:**
   - VS Code: Output panel > Select "MCP"
   - Terminal: stderr output from server

2. **Verify prerequisites:**
   ```bash
   node --version  # v20+
   npm --version   # v10+
   npm config get @sc-node-mcp:registry  # Should show SCB artifactory
   ```

3. **Report issue:**
   - Confluence: https://confluence.global.standardchartered.com/display/CC/SC+Node+MCP
   - Teams: https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e (SC Node MCP channel)
   - Include: Node version, npm version, error message, installation method

---

## 📚 Next Steps

After installation:

1. **Configure credentials** - See [Configuration Guide](CONFIGURATION.md)
2. **Choose your package** - See [NPM Packages Guide](archive/NPM_PACKAGE_MIGRATION_PLAN.md)
3. **Learn the tools** - See [Tools Reference](TOOLS_REFERENCE.md)
4. **Start using** - Try asking Copilot: "List all work items in project TBQPR"

---

**Last Updated:** February 2, 2026
