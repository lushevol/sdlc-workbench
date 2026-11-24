# Setup Guide

Quick start guide for configuring and using the SC Node MCP Server with VS Code and other MCP-compatible clients.

> 📘 **Need detailed installation instructions?** See [Installation Guide](INSTALLATION.md) for complete setup steps, troubleshooting, and SCB artifactory authentication.

> 🧠 **Using IntelliJ IDEA or another JetBrains IDE?** See the dedicated [IntelliJ Setup Guide](INTELLIJ_SETUP.md).

---

## 🎯 Quick Start

### Prerequisites

- **Node.js 20+** ([download](https://nodejs.org/))
- **Azure DevOps Personal Access Token** with Code & Work Items permissions
- **VS Code with MCP Extension** (recommended) or any MCP-compatible client
- **SCB Artifactory Access** (for npm package installation)

### 3-Minute Setup

1. **Click the One-Click Install button** in the [README](../README.md)
2. **Enter your credentials** when prompted (PAT, proxy, optional Confluence credentials)
3. **Start using tools** in VS Code Copilot Chat!

That's it! The server is installed and ready to use.

---

## ⚙️ Configuration Methods

The MCP server supports three configuration methods. Choose based on your installation type:

| Method | Best For | Priority |
|--------|----------|----------|
| **CLI Arguments** | NPM packages (npx, global install) | 🥇 Recommended for npm packages |
| **Environment Variables** | CI/CD pipelines, Docker containers | 🥈 Good for automation |
| **config.json File** | Local development, git clone setup | 🥉 Development only |

> 💡 **Tip:** Configuration methods are checked in order: CLI args → Environment variables → config.json

---

## 1️⃣ Configuration via CLI Arguments

**Used with:** npx, global installation, one-click install

Pass credentials as command-line arguments when starting the server:

```bash
# Unified server (all optional parameters)
npx -y @sc-node-mcp/unified \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "your-confluence-pat" \
  "nexus-username" \
  "nexus-password" \
  "your-sonarqube-token"

# ADO only
npx -y @sc-node-mcp/ado \
  "your-ado-pat-token" \
  "http://10.239.9.190:443"
```

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`), Confluence Base URL, Nexus URL, and SonarQube URL are all hardcoded in the server. Do not pass them as arguments.

### Parameter Details

**For @sc-node-mcp/unified (6 parameters):**
1. Azure DevOps PAT (required)
2. HTTPS Proxy URL (optional - use empty string `""` to skip)
3. Confluence PAT / Bearer Token (optional - enables Confluence tools when provided)
4. Nexus IQ Username (optional - enables Nexus tools when provided with password)
5. Nexus IQ Password (optional - enables Nexus tools when provided with username)
6. SonarQube Token (optional - enables SonarQube tools when provided)

**For @sc-node-mcp/ado (2 parameters):**
1. Azure DevOps PAT (required)
2. HTTPS Proxy URL (optional - use empty string `""` to skip)

### VS Code MCP Extension Configuration

Edit `.vscode/mcp.json` for npx or global installation:

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
        "${input:confluence_pat}",
        "${input:nexus_user}",
        "${input:nexus_pass}",
        "${input:sonar_token}"
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
      "description": "Confluence PAT / Bearer Token (optional, press Enter to skip)",
      "password": true
    },
    {
      "id": "nexus_user",
      "type": "promptString",
      "description": "Nexus IQ User Code (optional, press Enter to skip)"
    },
    {
      "id": "nexus_pass",
      "type": "promptString",
      "description": "Nexus IQ Pass Code (optional, press Enter to skip)",
      "password": true
    },
    {
      "id": "sonar_token",
      "type": "promptString",
      "description": "SonarQube Token (optional, press Enter to skip)",
      "password": true
    }
  ]
}
```

**For global installation**, replace `"command": "npx"` with `"command": "sc-node-mcp"` and remove `-y`, `@sc-node-mcp/unified` from args.

---

## 2️⃣ Configuration via Environment Variables

**Used with:** CI/CD pipelines, Docker, automation scripts

Set environment variables before running the server:

```bash
# Required
export AZURE_DEVOPS_PAT="your-pat-token"

# Optional
export HTTPS_PROXY="http://10.239.9.190:443"
export CONFLUENCE_PAT="your-confluence-bearer-token"
export NEXUS_USER_CODE="your-nexus-username"
export NEXUS_PASS_CODE="your-nexus-password"
export SONAR_TOKEN="your-sonarqube-token"

# Run server (no arguments needed)
npx -y @sc-node-mcp/unified
```

### Docker Example

```dockerfile
FROM node:20-alpine

ENV AZURE_DEVOPS_PAT="your-pat-token"
ENV HTTPS_PROXY="http://10.239.9.190:443"

RUN yarn global add @sc-node-mcp/unified

CMD ["sc-node-mcp"]
```

### CI/CD Pipeline Example

```yaml
# GitHub Actions
- name: Run MCP Server
  env:
    AZURE_DEVOPS_PAT: ${{ secrets.ADO_PAT }}
    HTTPS_PROXY: "http://10.239.9.190:443"
  run: |
    npx -y @sc-node-mcp/unified
```

---

## 3️⃣ Configuration via config.json

**Used with:** Local development (git clone setup)

Create `config.json` in the project root:

```json
{
  "AZURE_DEVOPS_PAT": "your-personal-access-token",
  "HTTPS_PROXY": "http://10.239.9.190:443",
  "CONFLUENCE_PAT": "your-confluence-bearer-token",
  "NEXUS_USER_CODE": "your-nexus-username",
  "NEXUS_PASS_CODE": "your-nexus-password",
  "SONAR_TOKEN": "your-sonarqube-token"
}
```

> ⚠️ **Security:** `config.json` is in `.gitignore`. Never commit credentials to version control!

### VS Code Configuration for Local Development

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

**Server Options:**
- **Unified:** `packages/unified/src/index.js` - All ADO + Confluence tools
- **ADO Only:** `packages/ado/src/index.js` - Azure DevOps tools only
- **Confluence Only:** `packages/confluence/src/index.js` - Confluence tools only
- **App Bridge (Browser Automation):** `packages/app-bridge/src/index.js` - standalone-only, not part of unified; see below

### App Bridge (Browser Automation) Local Setup

`@sc-node-mcp/app-bridge` uses **named CLI flags** instead of the positional `<PAT> [PROXY] ...` args used by every other package, since it has no ADO/Confluence concept — only local Selenium driver paths:

```jsonc
{
  "servers": {
    "app-bridge": {
      "type": "stdio",
      "command": "node",
      "args": [
        "${workspaceFolder}/packages/app-bridge/src/index.js",
        "--chromedriver-path",
        "${input:chromedriver_path}",
        "--edgedriver-path",
        "${input:edgedriver_path}"
      ]
    }
  }
}
```

Both driver paths are optional individually — configure only the browser(s) you use. Chrome/Edge browser *binaries* are expected in their standard OS install locations; if not, override with `--chrome-binary-path`/`--edge-binary-path`. Proxy is auto-detected the same way as every other package (`--proxy <url>` to override), then applied as a `--proxy-server=` browser launch argument rather than via `HTTPS_PROXY`, since the browser's own network stack doesn't read Node environment variables. See [docs/guide/APP_BRIDGE_TOOLS_GUIDE.md](guide/APP_BRIDGE_TOOLS_GUIDE.md) for the full tool reference.

---

## 🔑 Azure DevOps Personal Access Token (PAT)

### Creating a PAT

1. Go to Azure DevOps: `https://dev.azure.com/{your-org}`
2. Click on **User Settings** (top right) → **Personal Access Tokens**
3. Click **+ New Token**
4. Configure:
   - **Name:** "MCP Server Token"
   - **Organization:** Select your organization
   - **Expiration:** Choose validity period
   - **Scopes:** Select these permissions:
     - ✅ **Code:** Read & Write
     - ✅ **Work Items:** Read & Write
     - ✅ **Project and Team:** Read
5. Click **Create** and copy the token immediately (it won't be shown again!)

### PAT Security Best Practices

- ✅ Use different PATs for different applications
- ✅ Set reasonable expiration dates (30-90 days)
- ✅ Regenerate tokens regularly
- ✅ Revoke compromised tokens immediately
- ❌ Never commit PATs to version control
- ❌ Never share PATs via email or chat
- ❌ Never use Full Access scope unless absolutely necessary

---

## 🌐 Proxy Configuration

If you're behind Standard Chartered's corporate firewall, you need proxy configuration.

### Common SCB Proxy Servers

```bash
# Known working proxies (try in this order)
http://10.239.9.190:443
http://10.239.9.188:443
http://10.192.116.73:443
http://10.239.9.190:443
```

---

## 📦 Choosing the Right Package

Five packages are available on SCB artifactory:

| Package | Tools Included | Use When | Binary Command |
|---------|---------------|----------|----------------|
| **@sc-node-mcp/unified** | ADO (81 tools) + ado-upload-app (2 tools) + Confluence (15 tools) + Messaging (2 tools) + Nexus (2 tools) + SonarQube (6 tools) + Context Management (4 tools) (112 max) | You want all features | `sc-node-mcp` |
| **@sc-node-mcp/ado** | ADO only (81 tools) | You only need Azure DevOps | `sc-node-mcp-ado` |
| **@sc-node-mcp/confluence** | Confluence only (15 tools) | For Confluence-focused setups | `sc-node-mcp-confluence` |
| **@sc-node-mcp/messaging** | Messaging only (2 tools) | For email/Teams automation only | `sc-node-mcp-messaging` |
| **@sc-node-mcp/nexus** | Nexus IQ (2 tools) | For vulnerability scanning and remediation only | `sc-node-mcp-nexus` |

> 💡 **Recommendation:** Use `@sc-node-mcp/unified` unless you have a specific reason to use a single-service package.

For detailed package information, see [NPM Packages Guide](archive/NPM_PACKAGE_MIGRATION_PLAN.md).

---

## 🧪 Testing Your Setup

After configuration, verify everything works:

### 1. Test Server Startup

```bash
# If using npx
npx -y @sc-node-mcp/unified \
  "your-pat" \
  "http://10.239.9.190:443" \
  "" ""

# Should see: "SC Node MCP Server started successfully"
```

### 2. Test in VS Code

1. Open VS Code with MCP extension installed
2. Open Copilot Chat
3. Try a simple query: `"List all projects in Azure DevOps"`
4. Should see list of projects from your organization

### 3. Test Specific Tools

Try these test queries in VS Code Copilot Chat:

```
# Work Items
"Show me work item #12345"
"Create a new task with title 'Test MCP Server'"

# Repositories
"List all repositories in project MYPROJECT"
"Show me pull requests in repository myrepo"

# Branches
"List all branches in repository myrepo"
```

---

## 🔧 Troubleshooting

### Server Won't Start

**Symptoms:** Server exits immediately or shows "Configuration error"

**Solutions:**
```bash
# 1. Verify Node.js version
node --version  # Should be v20+

# 2. Check credentials are provided
echo $AZURE_DEVOPS_PAT  # Should not be empty
```

### "401 Unauthorized" Errors

**Symptoms:** Tools fail with authentication errors

**Solutions:**
- ✅ Verify PAT is valid and not expired
- ✅ Check PAT has correct scopes (Code, Work Items)
- ✅ Ensure organization URL is correct (no trailing slash)
- ✅ Test PAT manually:
  ```bash
  curl -u :YOUR_PAT https://dev.azure.com/sc-ado/_apis/projects?api-version=7.0
  ```

### "Cannot Find Package" Errors

**Symptoms:** `npm ERR! 404 Not Found - GET https://registry.npmjs.org/@sc-node-mcp%2funified`

**Solutions:**
```bash
# 1. Configure SCB registry
npm config set @sc-node-mcp:registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/

# 2. Authenticate with registry (see Installation Guide)

# 3. Verify registry access
npm view @sc-node-mcp/unified
```

### "Cannot find module ...@modelcontextprotocol/sdk/server/mcp.js" (ERR_MODULE_NOT_FOUND)

**Symptoms:** Server crashes on startup with `Error [ERR_MODULE_NOT_FOUND]` pointing at a file under `_npx\<hash>\node_modules\@modelcontextprotocol\sdk\...`

**Cause:** A previous `npx` invocation was interrupted (network drop, antivirus quarantine, disk full) and left a corrupted/incomplete install cached under npx's hash-keyed cache directory. `npx` reuses that broken cached install on every subsequent run — it never repairs itself.

**Solutions:**
```bash
# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx"
npm cache clean --force

# macOS / Linux
rm -rf ~/.npm/_npx
npm cache clean --force
```
Then restart the MCP server (VS Code will re-run `npx` and perform a fresh install). See [Installation Guide](INSTALLATION.md#-troubleshooting) for more detail.

### VS Code MCP Extension Issues

**Symptoms:** Server doesn't appear in MCP extension or fails to start

**Solutions:**
1. **Check MCP extension logs:**
   - VS Code → Output panel → Select "MCP" from dropdown
2. **Verify `.vscode/mcp.json` syntax:**
   - Must be valid JSON (no trailing commas, correct quotes)
3. **Restart MCP server:**
   - Command Palette (Cmd/Ctrl+Shift+P) → "MCP: Restart Server"
4. **Reinstall MCP extension:**
   - Extensions → Search "MCP" → Uninstall → Install

### Proxy Connection Issues

**Symptoms:** `ECONNREFUSED`, `ETIMEDOUT`, or "Cannot connect to Azure DevOps"

**Solutions:**
```bash
# 1. Test proxy connection
curl -x http://10.239.9.190:443 https://dev.azure.com

# 2. Try different proxy servers
export HTTPS_PROXY=http://10.239.9.188:443
export HTTPS_PROXY=http://10.192.116.73:443

# 3. Verify proxy environment variables
env | grep -i proxy
```

---

## 📚 Additional Resources

### Configuration
- [Installation Guide](INSTALLATION.md) - Detailed installation options and SCB artifactory auth
- [IntelliJ Setup Guide](INTELLIJ_SETUP.md) - Setup for IntelliJ IDEA and other JetBrains IDEs
- [NPM Packages Guide](archive/NPM_PACKAGE_MIGRATION_PLAN.md) - Package selection and registry setup

### Using the Server
 - [Tools Reference](TOOLS_REFERENCE.md) - Complete list of all tools
 - [Work Items Guide](guide/WORKITEMS_TOOLS_GUIDE.md) - Work item tool examples
 - [Repositories Guide](guide/REPOSITORIES_TOOLS_GUIDE.md) - Repository tool examples
 - [PR Review Guide](PR_REVIEW.md) - Automated code review

### Development
 - [Architecture Guide](ARCHITECTURE.md) - Project structure for contributors
 - [MCP Guide](guide/MCP_GUIDE.md) - Understanding Model Context Protocol

---

## Confluence Configuration

Confluence integration is fully functional. Provide your Confluence credentials when setting up the server to enable the `confluence_list_my_pages` tool.

**Configuration:** Pass Confluence username and API token as parameters, or use empty strings `""` to skip them if you only need Azure DevOps tools.

---

## 📊 Startup Telemetry

The unified server automatically records a usage entry each time it starts, appending a single JSON line to `usage.log` on the `telemetry/usage-log` branch of this repository (`DDCPQPR/23966-sc-node-mcp`). No configuration is required.

Each record contains: `timestamp`, `user` (ADO display name — the PAT is **never stored**), `version`, and `toolsEnabled` (which of ADO / Confluence / Nexus / SonarQube are active for that session).

This is fire-and-forget — if the write fails for any reason, a message is logged to stderr and the server continues normally.

---
