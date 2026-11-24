> **⚠️ ARCHIVED** — One-click install links are in [README.md](../../README.md). Install URLs can be generated with `node scripts/create-install-url.js`.

# One-Click Install Mechanism Explained

## Overview

This document explains how the one-click install badge works for MCP servers, using the Azure DevOps MCP Server as a reference example.

---

## The Install Badge

```markdown
[![Install with NPX in VS Code](badge-image-url)](install-link-url)
```

### Example from Azure DevOps MCP:
```markdown
[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_AzureDevops_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=ado&config=%7B%20%22type%22%3A%20%22stdio%22%2C%20%22command%22%3A%20%22npx%22%2C%20%22args%22%3A%20%5B%22-y%22%2C%20%22%40azure-devops%2Fmcp%22%2C%20%22%24%7Binput%3Aado_org%7D%22%5D%7D&inputs=%5B%7B%22id%22%3A%20%22ado_org%22%2C%20%22type%22%3A%20%22promptString%22%2C%20%22description%22%3A%20%22Azure%20DevOps%20organization%20name%22%7D%5D)
```

---

## URL Structure Breakdown

### The Complete URL:
```
https://insiders.vscode.dev/redirect/mcp/install
  ?name=ado
  &config=<URL_ENCODED_JSON>
  &inputs=<URL_ENCODED_JSON>
  &quality=insiders (optional, for VS Code Insiders)
```

### URL Parameters:

**1. `name=ado`**
- Display name for the MCP server
- Shows in VS Code as "Install MCP Server 'ado'?"

**2. `config=<encoded>`** - Server Configuration

Decoded JSON:
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@azure-devops/mcp", "${input:ado_org}"]
}
```

**3. `inputs=<encoded>`** - User Input Prompts

Decoded JSON:
```json
[{
  "id": "ado_org",
  "type": "promptString",
  "description": "Azure DevOps organization name (e.g. 'contoso')"
}]
```

---

## Complete Installation Flow

### Step-by-Step Process:

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: User clicks badge in README                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Browser opens URL                                  │
│ https://insiders.vscode.dev/redirect/mcp/install?...       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: VS Code web service redirects to desktop app       │
│ Protocol: vscode://redirect/mcp/install                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Desktop VS Code receives deep link                 │
│ MCP extension intercepts the URL                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: VS Code shows confirmation dialog                  │
│ "Install MCP Server 'ado'?"                                │
│ [Shows decoded config for review]                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: User clicks "Install"                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 7: VS Code prompts for inputs                         │
│ "Azure DevOps organization name (e.g. 'contoso')"          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 8: User enters value                                  │
│ Example: "sc-ado"                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 9: VS Code creates/updates .vscode/mcp.json          │
│ {                                                          │
│   "servers": {                                             │
│     "ado": {                                               │
│       "type": "stdio",                                     │
│       "command": "npx",                                    │
│       "args": ["-y", "@azure-devops/mcp", "sc-ado"]       │
│     }                                                      │
│   }                                                        │
│ }                                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 10: MCP extension starts the server                   │
│ Runs: npx -y @azure-devops/mcp sc-ado                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 11: NPX checks cache                                  │
│ Location: ~/.npm/_npx/                                     │
│ Is @azure-devops/mcp cached? No                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 12: NPX downloads package from NPM registry           │
│ npm info @azure-devops/mcp                                 │
│ npm http fetch GET @azure-devops/mcp                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 13: NPX caches package                                │
│ ~/.npm/_npx/<hash>/node_modules/@azure-devops/mcp/         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 14: NPX reads package.json bin field                  │
│ "bin": { "ado-mcp": "./dist/index.js" }                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 15: NPX executes the binary                           │
│ node ./dist/index.js sc-ado                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 16: MCP server starts                                 │
│ - Reads command-line arg: "sc-ado"                        │
│ - Builds URL: https://dev.azure.com/sc-ado                │
│ - Connects to Azure DevOps                                │
│ - Registers tools with VS Code via stdio                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 17: Tools available in Copilot Chat ✅                │
│ User can now use: "List my ADO work items"                │
└─────────────────────────────────────────────────────────────┘
```

---

## How NPX Works

### What is NPX?

**NPX** (Node Package Execute) is a tool that comes bundled with NPM (Node Package Manager).

**Key Features:**
1. Downloads and executes NPM packages without global installation
2. Caches packages in `~/.npm/_npx/` for reuse
3. Always uses the latest version (or specified version)
4. Cleans up temporary packages automatically

### NPX Command Breakdown:

```bash
npx -y @azure-devops/mcp sc-ado
```

**`npx`** - The NPM package executor
**`-y`** - Automatically confirm installation (no prompt)
**`@azure-devops/mcp`** - Package name to download/execute
**`sc-ado`** - Argument passed to the package binary

### What NPX Does Internally:

1. **Check cache:** Is `@azure-devops/mcp` already downloaded?
2. **Download (if needed):** `npm install @azure-devops/mcp` to temp cache
3. **Locate binary:** Read `package.json` → find `bin` field → get executable path
4. **Execute:** Run `node <executable-path> sc-ado`
5. **Keep cache:** Package stays in cache for next time

---

## File Locations

### Where Everything Lives:

```
User's Workspace:
/Users/username/myproject/
  ├── .vscode/
  │   └── mcp.json              ← Created by VS Code MCP extension
  └── (user's project files)

NPX Cache Directory:
/Users/username/.npm/_npx/
  └── <random-hash>/
      └── node_modules/
          └── @azure-devops/
              └── mcp/            ← Downloaded NPM package
                  ├── package.json
                  ├── dist/
                  │   └── index.js
                  └── node_modules/

VS Code Settings:
/Users/username/Library/Application Support/Code/User/
  └── settings.json             ← Global VS Code settings (if configured)
```

---

## Prerequisites: Node.js Required! ⚠️

### Critical Requirement:

**Node.js MUST be installed on the user's machine for this to work.**

### Why Node.js is Required:

1. **NPX requires Node.js** - NPX is part of the NPM package that comes with Node.js
2. **MCP servers run on Node.js** - They are Node.js applications
3. **VS Code doesn't bundle Node.js for user scripts** - VS Code has internal Node.js for its own operation, but doesn't expose it for running user packages

### What Happens Without Node.js:

```
User clicks install button
  ↓
VS Code tries to run: npx -y @azure-devops/mcp
  ↓
System error: "npx: command not found" ❌
  ↓
MCP server fails to start
  ↓
User sees error in VS Code MCP extension logs
```

### Minimum Requirements:

- **Node.js:** Version 20+ (as specified by Azure DevOps MCP)
- **NPM:** Comes bundled with Node.js (usually 10+)
- **VS Code:** Latest version or Insiders build
- **VS Code MCP Extension:** Installed and enabled

### Installation Instructions for Users:

**If Node.js is NOT installed:**

1. **Download Node.js:**
   - Visit: https://nodejs.org/
   - Download LTS version (Long Term Support)
   - Install for your operating system

2. **Verify installation:**
   ```bash
   node --version   # Should show: v20.x.x or higher
   npm --version    # Should show: 10.x.x or higher
   npx --version    # Should show: 10.x.x or higher
   ```

3. **Restart VS Code** (important - to pick up new PATH)

4. **Then click the install button**

---

## Security Considerations

### What VS Code Does to Protect Users:

1. **Review Before Execute:**
   - Shows decoded configuration before installing
   - User can see exact command that will run
   - User must explicitly confirm

2. **Trusted Sources:**
   - URL must come from known VS Code domains
   - Configuration is validated by MCP extension

3. **No Auto-Execution:**
   - Nothing runs without user confirmation
   - Each prompt must be answered

### Example Security Dialog:

```
┌────────────────────────────────────────────────────┐
│ Install MCP Server?                                │
│                                                    │
│ Name: ado                                          │
│                                                    │
│ Configuration:                                     │
│   Command: npx                                     │
│   Args: -y @azure-devops/mcp ${input:ado_org}     │
│                                                    │
│ This will run a command from the following        │
│ package on npm:                                    │
│   @azure-devops/mcp                                │
│                                                    │
│ [Cancel]  [Install]                                │
└────────────────────────────────────────────────────┘
```

---

## Advantages of This Approach

### For End Users:

✅ **No manual configuration** - VS Code does it all
✅ **No cloning repositories** - Package downloaded automatically
✅ **No running npm install** - NPX handles it
✅ **Guided setup** - Prompts for required values
✅ **Always latest version** - NPX fetches newest by default
✅ **Clean workspace** - No MCP server files in project
✅ **Cross-platform** - Works on Windows, Mac, Linux

### For Developers:

✅ **Easy distribution** - Publish once to NPM
✅ **Easy updates** - Users get new versions automatically
✅ **Professional UX** - Matches industry standards
✅ **Reduces support burden** - Less "how to install" questions
✅ **Analytics** - NPM tracks download counts
✅ **Versioning** - Semantic versioning with NPM

---

## Comparison: Manual vs One-Click Install

### Traditional Manual Installation:

```bash
# User does all of this:
1. git clone https://github.com/org/mcp-server
2. cd mcp-server
3. npm install
4. Create .vscode/mcp.json manually
5. Edit mcp.json with correct paths
6. Add config.json with credentials
7. Restart VS Code
8. Hope it works

Time: 10-15 minutes
Error-prone: High
User frustration: High
```

### One-Click Installation:

```bash
# User does:
1. Click button
2. Enter organization name
3. Done

Time: 30 seconds
Error-prone: Low
User frustration: Very low
```

---

## For Your Project: @sc-ado/mcp-server

### What You Need to Do:

1. **Publish to SCB NPM Registry:**
   ```bash
   npm publish --registry=https://your-scb-npm-registry.com
   ```

2. **Create Install URL** (see NPM_PACKAGE_MIGRATION_PLAN.md):
   - Generate encoded config with inputs
   - Create badges for VS Code and VS Code Insiders
   - Add to README.md

3. **Test Installation:**
   ```bash
   # From SCB NPM registry
   npx @sc-ado/mcp-server "https://dev.azure.com/sc-ado" "token"
   ```

4. **Document Prerequisites:**
   - Add "Node.js 20+ required" to README
   - Link to Node.js download page
   - Provide verification commands

### Your Install Badge Will Look Like:

```markdown
[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SCB_ADO_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=sc-ado-mcp&config=...&inputs=...)
```

---

## Troubleshooting

### Common Issues:

**1. "npx: command not found"**
- **Cause:** Node.js not installed or not in PATH
- **Solution:** Install Node.js from https://nodejs.org/ and restart terminal/VS Code

**2. "Package not found: @sc-ado/mcp-server"**
- **Cause:** Package not published to NPM registry, or user not authenticated
- **Solution:** Verify package is published: `npm view @sc-ado/mcp-server --registry=<SCB_REGISTRY>`

**3. "Unable to connect to Azure DevOps"**
- **Cause:** Invalid credentials or network issues
- **Solution:** Check PAT token, verify proxy settings, check network connectivity

**4. "MCP server failed to start"**
- **Cause:** Missing dependencies, wrong Node.js version
- **Solution:** Clear NPX cache: `rm -rf ~/.npm/_npx`, verify Node.js version: `node --version`

**5. "VS Code doesn't show install dialog"**
- **Cause:** MCP extension not installed, VS Code version too old
- **Solution:** Update VS Code, install MCP extension from marketplace

---

## References

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/chat/mcp)
- [NPX Documentation](https://docs.npmjs.com/cli/v10/commands/npx)
- [Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [Node.js Download](https://nodejs.org/)

---

*Last Updated: January 31, 2026*
*Authors: Saravanan R (1540326), Shiyamkumar U (2002918)*
