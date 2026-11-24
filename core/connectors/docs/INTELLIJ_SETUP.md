# IntelliJ IDEA Setup Guide

Complete guide for installing and configuring the SC Node MCP Server in **IntelliJ IDEA** (and other JetBrains IDEs) using the GitHub Copilot plugin.

---

## 📋 Prerequisites

Before setting up, ensure you have:

- **IntelliJ IDEA 2024.1 or later** (any edition: Community, Ultimate, etc.)  
  Also works with: PyCharm, WebStorm, GoLand, Rider, and other JetBrains IDEs 2024.1+
- **GitHub Copilot plugin** installed and signed in (see [Installing the Plugin](#1️⃣-install-the-github-copilot-plugin))
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

## ⚠️ Key Difference vs VS Code

IntelliJ's MCP config uses a **different format** than VS Code:

| Aspect | VS Code | IntelliJ |
|--------|---------|----------|
| Config file location | `.vscode/mcp.json` (per workspace) | `%LOCALAPPDATA%\github-copilot\intellij\mcp.json` (global, all projects) |
| Root JSON key | `"mcpServers"` | `"servers"` |
| `"type"` field | Not required | **Required:** `"type": "stdio"` |
| Input prompts | `${input:variable}` supported | ❌ Not supported — use `env` instead |
| Config scope | Per workspace | Global across all projects |

> **Important:** IntelliJ does **not** support `${input:...}` variable prompts in the config file. Credentials must be provided via the `env` block or as direct values in `args`.

---

## 🎯 Quick Start (3-Minute Setup)

1. **Install the GitHub Copilot plugin** in IntelliJ (see below)
2. **Create/edit** `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`
3. **Add your server config** with credentials in the `env` block
4. **Restart IntelliJ** and open Copilot Chat — tools are ready!

---

## 1️⃣ Install the GitHub Copilot Plugin

1. Open IntelliJ IDEA
2. Go to **File → Settings** (Windows/Linux) or **IntelliJ IDEA → Preferences** (macOS)
3. Navigate to **Plugins → Marketplace**
4. Search for **"GitHub Copilot"**
5. Click **Install** → **Restart IDE**
6. After restart, sign in: **Tools → GitHub Copilot → Sign in to GitHub**

> **Note:** You need an active GitHub Copilot subscription. Check with your team lead or IT if unsure.

---

## 2️⃣ Locate the MCP Config File

The IntelliJ MCP configuration file is stored **globally** (applies to all projects):

**Windows:**
```
%LOCALAPPDATA%\github-copilot\intellij\mcp.json
```
Which resolves to:
```
C:\Users\<YourUsername>\AppData\Local\github-copilot\intellij\mcp.json
```

**macOS:**
```
~/Library/Application Support/github-copilot/intellij/mcp.json
```

**Linux:**
```
~/.config/github-copilot/intellij/mcp.json
```

> **Tip:** If the file or directory doesn't exist, create it manually. The `intellij` folder may need to be created too.

---

## 3️⃣ Configuration Methods

Choose the method that best fits your use case:

| Method | Best For | Security |
|--------|----------|----------|
| **NPX via env vars** | Quick setup, always latest version | ✅ Credentials in env block |
| **Global Installation** | Fast startup, regular use | ✅ Credentials in env block |
| **Local Development** | Contributors, code changes | ✅ Reads from `config.json` |

---

### Method A: NPX Execution (Recommended for most users)

Runs the latest package directly without a separate install step.

**Edit `mcp.json`:**

```json
{
  "servers": {
    "sc-node-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@sc-node-mcp/unified",
        "${env:AZURE_DEVOPS_PAT}",
        "${env:HTTPS_PROXY}",
        "${env:CONFLUENCE_PAT}",
        "${env:NEXUS_USER_CODE}",
        "${env:NEXUS_PASS_CODE}",
        "${env:SONAR_TOKEN}"
      ],
      "env": {
        "AZURE_DEVOPS_PAT": "your-ado-pat-here",
        "HTTPS_PROXY": "http://gateway.zscloud.net:443",
        "no_proxy": "127.0.0.1,localhost,.standardchartered.com,.sc.com",
        "NO_PROXY": "127.0.0.1,localhost,.standardchartered.com,.sc.com",
        "NODE_TLS_REJECT_UNAUTHORIZED": "0",
        "CONFLUENCE_PAT": "your-confluence-pat-here",
        "NEXUS_USER_CODE": "your-nexus-username",
        "NEXUS_PASS_CODE": "your-nexus-password",
        "SONAR_TOKEN": "your-sonarqube-token"}
    }
  }
}
```

> **Minimum config** (ADO only, Confluence/Nexus/SonarQube optional):
> ```json
> {
>   "servers": {
>     "sc-node-mcp": {
>       "type": "stdio",
>       "command": "npx",
>       "args": ["-y", "@sc-node-mcp/unified", "your-ado-pat", "http://your-proxy:443"],
>       "env": {
>         "NODE_TLS_REJECT_UNAUTHORIZED": "0"
>       }
>     }
>   }
> }
> ```

---

### Method B: Global Installation (Recommended for regular use)

Install once, start instantly every time — no download delay.

#### Step 1: Install the package globally

```bash
# Configure SCB registry first (one-time setup)
npm config set @sc-node-mcp:registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/

# Install globally
yarn global add @sc-node-mcp/unified
```

#### Step 2: Configure `mcp.json`

**Windows** (use full path to the binary):
```json
{
  "servers": {
    "sc-node-mcp": {
      "type": "stdio",
      "command": "sc-node-mcp",
      "args": [
        "your-ado-pat-here",
        "http://gateway.zscloud.net:443",
        "your-confluence-pat",
        "your-nexus-user",
        "your-nexus-pass",
        "your-sonar-token"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "0",
        "NO_PROXY": "127.0.0.1,localhost,.standardchartered.com,.sc.com"
      }
    }
  }
}
```

> **Tip:** If `sc-node-mcp` isn't in PATH, use the full binary path:  
> `"command": "C:\\Users\\YourUsername\\AppData\\Local\\Yarn\\bin\\sc-node-mcp"`

#### Step 3: Verify installation

```bash
# Windows
where sc-node-mcp

# Should print something like:
# C:\Users\YourUsername\AppData\Local\Yarn\bin\sc-node-mcp
```

---

### Method C: Local Development (Git Clone)

For contributors or developers who need to modify the source code.

#### Step 1: Clone and install

```bash
git clone <repository-url>
cd sc-node-mcp
yarn install
```

#### Step 2: Create `config.json` in the project root

```json
{
  "AZURE_DEVOPS_PAT": "your-personal-access-token-here",
  "HTTPS_PROXY": "http://gateway.zscloud.net:443",
  "CONFLUENCE_PAT": "your-confluence-bearer-token",
  "NEXUS_USER_CODE": "your-nexus-username",
  "NEXUS_PASS_CODE": "your-nexus-password",
  "SONAR_TOKEN": "your-sonarqube-token"
}
```

> ⚠️ **Security:** `config.json` is in `.gitignore`. Never commit credentials!

#### Step 3: Configure `mcp.json` for local development

```json
{
  "servers": {
    "sc-node-mcp": {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "C:\\path\\to\\sc-node-mcp\\packages\\unified\\src\\index.js"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "0"
      }
    }
  }
}
```

> **Note:** Use the full absolute path to both `node.exe` and `index.js`. Avoid relative paths in IntelliJ's global config.

---

## 4️⃣ Complete mcp.json Reference

Full example with all available options and both servers (SC Node MCP + SonarQube):

```json
{
  "servers": {
    "sc-node-mcp": {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "C:\\path\\to\\packages\\unified\\src\\index.js"
      ],
      "env": {
        "AZURE_DEVOPS_PAT": "your-ado-pat",
        "HTTPS_PROXY": "http://gateway.zscloud.net:443",
        "no_proxy": "127.0.0.1,localhost,.standardchartered.com,.standardchartered.net,.sc.com,.sc.net,.dev.net",
        "NO_PROXY": "127.0.0.1,localhost,.standardchartered.com,.standardchartered.net,.sc.com,.sc.net,.dev.net",
        "NODE_TLS_REJECT_UNAUTHORIZED": "0",
        "NODE_EXTRA_CA_CERTS": "C:\\Users\\YourUsername\\Downloads\\cacert.pem",
        "CONFLUENCE_BASE_URL": "https://confluence.global.standardchartered.com",
        "CONFLUENCE_PAT": "your-confluence-pat",
        "CONFLUENCE_USERNAME": "FirstName.LastName@sc.com",
        "CONFLUENCE_API_TOKEN": "your-confluence-api-token",
        "SONAR_URL": "https://sonarqube.vx.standardchartered.com",
        "SONAR_TOKEN": "your-sonarqube-token"
      }
    }
  }
}
```

### Environment Variable Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_DEVOPS_PAT` | ✅ Yes | Azure DevOps Personal Access Token |
| `HTTPS_PROXY` | ⚠️ SCB required | Corporate proxy URL (e.g., `http://gateway.zscloud.net:443`) |
| `NO_PROXY` / `no_proxy` | ⚠️ SCB required | Comma-separated list of no-proxy hosts |
| `NODE_TLS_REJECT_UNAUTHORIZED` | ⚠️ SCB required | Set to `"0"` for corporate SSL inspection |
| `NODE_EXTRA_CA_CERTS` | Optional | Path to custom CA certificate `.pem` file |
| `CONFLUENCE_PAT` | Optional | Enables Confluence tools (15 tools) |
| `CONFLUENCE_USERNAME` | Optional | Your Confluence/SCB email |
| `CONFLUENCE_API_TOKEN` | Optional | Same as `CONFLUENCE_PAT` |
| `SONAR_TOKEN` | Optional | Enables SonarQube tools (6 tools) |
| `SONAR_URL` | Optional | SonarQube instance URL |
| `NEXUS_USER_CODE` | Optional | Nexus IQ username — enables Nexus tools |
| `NEXUS_PASS_CODE` | Optional | Nexus IQ password — enables Nexus tools |

---

## 5️⃣ Azure DevOps Personal Access Token (PAT)

### Creating a PAT

1. Go to: `https://dev.azure.com/sc-ado`
2. Click on **User Settings** (top-right avatar) → **Personal Access Tokens**
3. Click **+ New Token**
4. Configure:
   - **Name:** `"IntelliJ MCP Token"`
   - **Organization:** Select your organization
   - **Expiration:** 30–90 days recommended
   - **Scopes:**
     - ✅ **Code:** Read & Write
     - ✅ **Work Items:** Read & Write
     - ✅ **Project and Team:** Read
     - ✅ **Build:** Read & Execute *(for pipeline tools)*
     - ✅ **Test Management:** Read & Write *(for test plan tools)*
5. Click **Create** — copy the token immediately (shown only once!)

### PAT Security Best Practices

- ✅ Set expiration dates (30–90 days)
- ✅ Revoke and rotate tokens regularly
- ❌ Never paste PATs in chat, emails, or code comments
- ❌ Never commit `mcp.json` with credentials to version control

---

## 6️⃣ Proxy Configuration (SCB Corporate Network)

Standard Chartered's corporate network requires proxy configuration for external connectivity.

### Common SCB Proxy Servers

```bash
# Try in this order
http://gateway.zscloud.net:443
http://10.239.9.190:443
http://10.239.9.188:443
http://10.192.116.73:443
```

### In mcp.json

```json
"env": {
  "HTTPS_PROXY": "http://gateway.zscloud.net:443",
  "HTTP_PROXY": "http://gateway.zscloud.net:443",
  "no_proxy": "127.0.0.1,localhost,.standardchartered.com,.standardchartered.net,.sc.com,.sc.net,.dev.net",
  "NO_PROXY": "127.0.0.1,localhost,.standardchartered.com,.standardchartered.net,.sc.com,.sc.net,.dev.net",
  "NODE_TLS_REJECT_UNAUTHORIZED": "0"
}
```

> **Note:** Both `no_proxy` (lowercase) and `NO_PROXY` (uppercase) are set — different tools read different variants.

---

## 7️⃣ SCB Artifactory Authentication (for NPX/Global Install)

Before running `npx @sc-node-mcp/unified` or `yarn global add`, authenticate with SCB's npm registry.

### One-Time Registry Setup

```bash
# Set SCB registry for @sc-node-mcp scope
npm config set @sc-node-mcp:registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/

# Or set as global default registry
npm config set registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/ --global
```

### Authentication via .npmrc

Create/edit `C:\Users\<YourUsername>\.npmrc`:

```ini
@sc-node-mcp:registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/
//artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/:_auth=<BASE64_CREDENTIALS>
//artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/:always-auth=true
```

**Generate Base64 credentials (Windows PowerShell):**
```powershell
[Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("username:password"))
```

---

## 8️⃣ Testing Your Setup

### Step 1: Verify Server Starts

Open a terminal and run:

```bash
# Using npx
npx -y @sc-node-mcp/unified "your-pat" "http://your-proxy:443"

# Using global install
sc-node-mcp "your-pat" "http://your-proxy:443"
```

You should see: `SC Node MCP Server started successfully`  
Press `Ctrl+C` to stop.

### Step 2: Verify in IntelliJ

1. Restart IntelliJ after editing `mcp.json`
2. Open **Copilot Chat** (View → Tool Windows → GitHub Copilot Chat, or the chat icon)
3. Try a test query:
   ```
   List all projects in Azure DevOps
   ```
4. You should see a list of projects from your organization

### Step 3: Test Specific Tools

Try these queries in IntelliJ Copilot Chat:

```
# Work Items
Show me work item #12345
Create a new task with title 'Test MCP in IntelliJ'

# Repositories
List all repositories in project MYPROJECT
Show me open pull requests in repository myrepo

# Confluence (if configured)
List my recent Confluence pages

# SonarQube (if configured)
Show SonarQube quality metrics for project my-project-key
```

---

## 🔧 Troubleshooting

### MCP Tools Not Appearing in Copilot Chat

**Symptoms:** Copilot Chat works but no MCP tools are invoked

**Solutions:**
1. **Verify plugin version:** GitHub Copilot plugin must be v1.5.0.6751 or later
   - `File → Settings → Plugins → GitHub Copilot → check version`
2. **Check `mcp.json` syntax:** Must be valid JSON — use a JSON validator
3. **Verify file location:** Confirm the file is at `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`
4. **Restart IntelliJ completely** (not just reload) after editing `mcp.json`
5. **Check IntelliJ logs:**
   - `Help → Show Log in Explorer` → look for MCP-related errors in `idea.log`

### Server Won't Start

**Symptoms:** MCP server process crashes on startup

**Solutions:**
```bash
# 1. Verify Node.js version (must be 20+)
node --version

# 2. Test server manually with your credentials
node "C:\path\to\packages\unified\src\index.js"
# Should print startup message, not crash

# 3. Check for PATH issues — IntelliJ may not inherit system PATH
# Use full absolute paths in mcp.json for command and args
```

**Use full path to node.exe:**
```json
"command": "C:\\Program Files\\nodejs\\node.exe"
```

### "401 Unauthorized" Errors

**Symptoms:** Tools fail with authentication errors

**Solutions:**
- ✅ Verify PAT is valid and not expired
- ✅ Ensure PAT has correct scopes (Code, Work Items, Project and Team)
- ✅ Test PAT manually:
  ```bash
  curl -u :YOUR_PAT https://dev.azure.com/sc-ado/_apis/projects?api-version=7.0
  ```

### "Cannot Find Package" on NPX

**Symptoms:** `npm ERR! 404 Not Found - GET https://registry.npmjs.org/@sc-node-mcp%2funified`

**Solutions:**
```bash
# Set SCB registry
npm config set @sc-node-mcp:registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/

# Verify
npm config get @sc-node-mcp:registry
```

### Proxy / Network Errors

**Symptoms:** `ECONNREFUSED`, `ETIMEDOUT`, or connection timeout errors

**Solutions:**
```bash
# Test proxy
curl -x http://gateway.zscloud.net:443 https://dev.azure.com

# Try alternative proxy
# Update HTTPS_PROXY in mcp.json env block to:
# http://10.239.9.190:443  or  http://10.239.9.188:443
```

### TLS / SSL Certificate Errors

**Symptoms:** `UNABLE_TO_VERIFY_LEAF_SIGNATURE` or similar SSL errors

**Solutions:**
Add to your `mcp.json` env block:
```json
"NODE_TLS_REJECT_UNAUTHORIZED": "0",
"NODE_EXTRA_CA_CERTS": "C:\\Users\\YourUsername\\Downloads\\cacert.pem"
```

> **Note:** `NODE_TLS_REJECT_UNAUTHORIZED: "0"` is already handled internally by the server entry point, but setting it in `env` ensures it's applied before the process starts.

### IntelliJ Doesn't Pick Up mcp.json Changes

**Solutions:**
1. Close IntelliJ completely (not just the project)
2. Wait 5 seconds
3. Reopen IntelliJ — the plugin re-reads `mcp.json` on startup

---

## 📦 Available Packages

| Package | Tools | Use When | Command |
|---------|-------|----------|---------|
| **@sc-node-mcp/unified** | ADO (81) + Confluence (15) + Messaging (2) + Nexus (2) + SonarQube (6) + Context (4) (112 max) | You want everything | `sc-node-mcp` |
| **@sc-node-mcp/ado** | ADO only (81 tools) | ADO tools only | `sc-node-mcp-ado` |
| **@sc-node-mcp/confluence** | Confluence only (15 tools) | Confluence-focused | `sc-node-mcp-confluence` |
| **@sc-node-mcp/nexus** | Nexus IQ (2 tools) | Vulnerability scanning | `sc-node-mcp-nexus` |
| **@sc-node-mcp/messaging** | Email + Teams (2 tools) | Messaging automation | `sc-node-mcp-messaging` |

> 💡 **Recommendation:** Use `@sc-node-mcp/unified` unless you have a specific reason to use a focused package.

---

## 📚 Additional Resources

### Setup & Configuration
- [Installation Guide](INSTALLATION.md) - Detailed installation options and SCB artifactory auth
- [MCP Guide](guide/MCP_GUIDE.md) - Understanding Model Context Protocol

### Using the Tools
- [Tools Reference](TOOLS_REFERENCE.md) - Complete list of all 112 available MCP tools
- [Work Items Guide](guide/WORKITEMS_TOOLS_GUIDE.md) - Work item tool examples
- [Repositories Guide](guide/REPOSITORIES_TOOLS_GUIDE.md) - Repository and PR tool examples
- [Pipeline Tools Guide](guide/PIPELINES_TOOLS_GUIDE.md) - CI/CD pipeline management
- [PR Review Guide](PR_REVIEW.md) - Automated code review with `CODE_REVIEW_GUIDE_FILE`
- [Context Management Guide](guide/CONTEXT_MANAGEMENT_GUIDE.md) - Workspace context setup

### Package-Specific Guides
- [Messaging (Email + Teams)](../packages/messaging/README.md)
- [Confluence](../packages/confluence/README.md)
- [Nexus IQ Scanning](../packages/nexus/README.md)
- [SonarQube](guide/SONARQUBE_TOOLS_GUIDE.md)
- [App Bridge (Browser Automation)](guide/APP_BRIDGE_TOOLS_GUIDE.md)

### Support
- **Report issues:** https://confluence.global.standardchartered.com/display/CC/SC+Node+MCP
- Include: IntelliJ version, GitHub Copilot plugin version, Node.js version, error message

---

*Last Updated: May 2026*
