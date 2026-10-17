# @sc-node-mcp/unified

Unified MCP Server combining Azure DevOps, Confluence, SC Wiki, Messaging, Nexus IQ, SonarQube, and Context Management functionality for comprehensive SCB automation.

## Overview

This package provides a single MCP server that registers all tools from `@sc-node-mcp/ado`, `@sc-node-mcp/ado-upload-app`, `@sc-node-mcp/confluence`, `@sc-node-mcp/scwiki`, `@sc-node-mcp/messaging`, `@sc-node-mcp/nexus`, `@sc-node-mcp/sonar`, and the built-in context management tools.

**Includes:**
- **86 Azure DevOps tools**: Work items (29), repositories/branches/PRs (20), pipelines (14), PR review (4), search (2), sprint & capacity (8), test plans (9), core identity (1)
- **2 ADO Upload App tools**: Interactive file upload UI panel (`wit_upload_attachment_ui`, `wit_upload_attachment`)
- **15 Confluence tools**: Create, update, read, search, get page ID, list pages, manage spaces, comments, and labels
- **14 SC Wiki tools**: Create, update, delete, search, read, list spaces/children, manage comments/tags/history/attachments (pages addressed by dotted reference, e.g. `Sandbox.S2B NG.WebHome`)
- **2 Messaging tools**: Send emails via Outlook automation and messages via Teams
- **2 Nexus IQ tools**: npm vulnerability scanning (`nexus_scan_vulnerabilities`) and automated remediation (`nexus_fix_vulnerabilities`)
- **6 SonarQube tools**: Project search, branches, quality gate, issues, hotspots, measures
- **4 Context Management tools**: Named workspace contexts auto-fill project/team/repo across all tools
- **Prompts**: Predefined prompts for guided workflows

> **Web tools** (`web_search`, `web_fetch`, `web_crawl`, `web_crawl_browser`) are available as a standalone experimental package: `@sc-node-mcp/web`

**Total: 129 tools (max — Confluence, SC Wiki, Nexus, SonarQube only register when credentials are provided)**

## Installation

> 📘 **Complete Setup Guide:** See [Installation Guide](../../docs/INSTALLATION.md) for detailed instructions, SCB artifactory authentication, and troubleshooting.

### Quick Install Methods

```bash
# Option 1: NPX (no installation, always latest version) - RECOMMENDED
npx -y @sc-node-mcp/unified \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "your-confluence-pat"

# Option 2: Global installation
yarn global add @sc-node-mcp/unified

# Then run using binary command
sc-node-mcp \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "your-confluence-pat"

# Option 3: Local package dependency (for programmatic use)
yarn add @sc-node-mcp/unified
```

### Installation Parameters

| Position | Parameter | Required | Example |
|----------|-----------|----------|---------|
| 1 | ADO PAT | ✅ Yes | `your-ado-pat-token` |
| 2 | Proxy URL | ⚠️ Optional | `http://10.239.9.190:443` |
| 3 | Confluence PAT | ⚠️ Optional | `your-confluence-pat` |
| 4 | Nexus User Code | ⚠️ Optional | `nexus-username` |
| 5 | Nexus Pass Code | ⚠️ Optional | `nexus-password` |
| 6 | SonarQube Token | ⚠️ Optional | `your-sonar-token` |
| 7 | SC Wiki Token | ⚠️ Optional | `your-scwiki-bearer-token` |

> **💡 Tip:** Use empty strings `""` for optional parameters you want to skip.  
> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`), Confluence Base URL (`https://confluence.global.standardchartered.com`), Nexus URL, and SonarQube URL are hardcoded — do not pass them as arguments. SC Wiki Base URL defaults to `https://scwiki.global.standardchartered.com` but can be overridden via the `SCWIKI_URL` environment variable.

## Usage

### NPX Direct Execution (Recommended)

```bash
# Run directly without installation
npx -y @sc-node-mcp/unified \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "" "" ""  # Skip Confluence, Nexus parameters
```

### Global Installation

```bash
# After global install
sc-node-mcp \
  "your-ado-pat-token" \
  "http://10.239.9.190:443" \
  "" "" ""  # Skip optional parameters
```

### VS Code MCP Extension

Add to `.vscode/mcp.json`:

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
      ],
      "env": {
        "CODE_REVIEW_GUIDE_FILE": "${input:code_review_guide}"
      }
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
      "description": "Confluence PAT (optional, press Enter to skip)",
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
    },
    {
      "id": "code_review_guide",
      "type": "promptString",
      "description": "CODE_REVIEW_GUIDE.md file full path (optional, press Enter to skip)"
    }
  ]
}
```

### One-Click Install for VS Code

Click this button to install with VS Code's one-click installer:

<!-- ONE-CLICK-INSTALL-START -->
[![Pipeline](https://dev.azure.com/sc-ado/DDCPQPR/_apis/build/status/46487?branchName=main&style=flat-square&label=Pipeline)](https://dev.azure.com/sc-ado/DDCPQPR/_build?definitionId=46487&_a=summary)

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SC_NODE_MCP/UNIFIED-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%2C%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

[![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SC_NODE_MCP/UNIFIED-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%2C%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

[![Teams Channel](https://img.shields.io/badge/Teams-SC_Node_MCP_Channel-6264A7?style=flat-square&logo=microsoftteams&logoColor=white)](https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e)
<!-- ONE-CLICK-INSTALL-END -->

## Configuration

### CLI Arguments (Recommended for npm packages)

Pass credentials as command-line arguments (shown in usage examples above).

### Environment Variables

```bash
export AZURE_DEVOPS_PAT="your-pat-token"
export HTTPS_PROXY="http://10.239.9.190:443"
export CONFLUENCE_PAT="your-confluence-bearer-token"

# Then run without arguments
npx -y @sc-node-mcp/unified
```

### config.json (Local development only)

Create `config.json` in project root:

```json
{
  "AZURE_DEVOPS_PAT": "your-personal-access-token",
  "HTTPS_PROXY": "http://proxy:443",
  "CONFLUENCE_PAT": "your-confluence-bearer-token",
  "NEXUS_USER_CODE": "your-nexus-username",
  "NEXUS_PASS_CODE": "your-nexus-password",
  "SONAR_TOKEN": "your-sonarqube-token"
}
```

> **Note:** Azure DevOps Org URL (`https://dev.azure.com/sc-ado`), Confluence Base URL (`https://confluence.global.standardchartered.com`), Nexus URL, and SonarQube URL are all hardcoded. All credentials except ADO PAT are optional — tools for each service register only when the corresponding credential is provided.

## Features

- **81 Azure DevOps tools**: Work items, repositories, branches, PRs, pipelines, automated review
- **2 ADO Upload App tools**: Interactive file upload panel (`wit_upload_attachment_ui`, `wit_upload_attachment`)
- **15 Confluence tools**: Page management, search, create, update, read, get page ID, spaces, comments, and labels
- **2 Messaging tools**: Send emails via Outlook automation and messages via Teams
- **2 Nexus IQ tools**: Vulnerability scanning and multi-phase automated remediation
- **6 SonarQube tools**: Project search, branches, quality gate, issues, hotspots, measures
- **4 Context Management tools**: Named workspace contexts; auto-fill project/team/repo across all tools
- **112 Prompts**: Predefined prompts for guided workflows

## Dependencies

- `@sc-node-mcp/core` - Core MCP infrastructure
- `@sc-node-mcp/ado` - Azure DevOps tools
- `@sc-node-mcp/ado-upload-app` - ADO upload UI tools
- `@sc-node-mcp/confluence` - Confluence tools
- `@sc-node-mcp/messaging` - Messaging tools (Outlook email + Teams)
- `@sc-node-mcp/nexus` - Nexus IQ vulnerability scanning
- `@sc-node-mcp/sonar` - SonarQube code quality analysis
