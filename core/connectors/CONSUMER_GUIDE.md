# SC Node MCP — Consumer Guide

> **SC Node MCP** is an MCP (Model Context Protocol) server that connects VS Code Copilot Chat directly to Azure DevOps, Confluence, SC Wiki, Outlook, Microsoft Teams, Nexus IQ, and SonarQube — no browser switching, no copy-pasting. Just ask Copilot in plain English and let the server execute.
Repo: https://dev.azure.com/sc-ado/DDCPQPR/_git/23966-sc-node-mcp
Teams Channel: [SC Node MCP — Microsoft Teams Support Channel](https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e)


<!-- ONE-CLICK-INSTALL-START -->
[![Pipeline](https://dev.azure.com/sc-ado/DDCPQPR/_apis/build/status/46487?branchName=main&style=flat-square&label=Pipeline)](https://dev.azure.com/sc-ado/DDCPQPR/_build?definitionId=46487&_a=summary)

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-Install_SC_NODE_MCP/UNIFIED-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%2C%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

[![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SC_NODE_MCP/UNIFIED-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Funified%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%2C%22%24%7Binput%3Asonar_token%7D%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22CODE_REVIEW_GUIDE_FILE%22%3A%22%24%7Binput%3Acode_review_guide%7D%22%2C%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D)

[![Teams Channel](https://img.shields.io/badge/Teams-SC_Node_MCP_Channel-6264A7?style=flat-square&logo=microsoftteams&logoColor=white)](https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e)
<!-- ONE-CLICK-INSTALL-END -->

> ⚠️ **Important — GHCP has transitioned to AI Credits** (from Premium Request Units). AI usage is now billed directly by tokens at $0.01 per credit. Previously free/lightweight models are now billed, and usage stops entirely when your budget runs out (no fallback model). Keep prompts focused and use `ctx_set` to avoid repeating context.
> See: [Copilot Token Usage Guidelines](https://confluence.global.standardchartered.com/display/CC/Copilot+Token+Usage+Guidelines)

> 💡 **Need only specific tools?** Jump to [Granular Package Install](#granular-package-install) to install individual packages.

---

## Table of Contents

- [What is SC Node MCP?](#what-is-sc-node-mcp)
- [Features at a Glance](#features-at-a-glance)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [One-Click Install](#1-one-click-install)
  - [Manual Install](#2-manual-install)
  - [Verify Installation](#3-verify-installation)
  - [Update MCP Config](#4-update-mcp-config)
- [Granular Package Install](#granular-package-install)
- [Confluence Integration](#confluence-integration)
  - [Create a Confluence PAT](#1-create-a-confluence-pat)
  - [Confluence in Action](#2-confluence-in-action)
- [SC Wiki Integration](#sc-wiki-integration)
  - [Create an SC Wiki Token](#1-create-an-sc-wiki-token)
  - [SC Wiki in Action](#2-sc-wiki-in-action)
- [Web Search Integration](#web-search-integration)
- [Using with Copilot Chat](#using-with-copilot-chat)
- [Available Tools](#available-tools)
- [Usage Analytics](#usage-analytics)
- [Support](#support)

---

## What is SC Node MCP?

SC Node MCP is a locally-running [Model Context Protocol](https://modelcontextprotocol.io) server built for Standard Chartered developers. It exposes **128 tools** across Azure DevOps, Confluence, SC Wiki, Outlook, Microsoft Teams, Web Search, Nexus IQ, and SonarQube directly inside VS Code Copilot Chat — no browser, no ticket juggling, no manual API calls.

Ask Copilot to create a work item, review a PR, search Confluence pages, or send a Teams message — the MCP server handles authentication, API calls, and formatting on your behalf.

> Built and maintained by the CIB S2B Trade&FM Engineering team. Source: [SC Node MCP on Azure DevOps](https://dev.azure.com/sc-ado/DDCPQPR/_git/23966-sc-node-mcp).

---

## Features at a Glance

| Integration | Tools | What you can do |
|---|:---:|---|
| **Azure DevOps — Work Items** | 26 | Query, create, update, link, batch-update, comment, manage attachments & history |
| **Azure DevOps — Repositories** | 20 | List repos & branches, create/update PRs, manage reviewers, search commits |
| **Azure DevOps — Pipelines** | 12 | Trigger, monitor, cancel, retry, and manage builds and release pipelines |
| **Azure DevOps — PR Review** | 4 | AI-driven code review with comments posted directly to PR diff lines |
| **Azure DevOps — Sprint & Capacity** | 8 | Manage iterations, assign sprints to teams, get and update team capacity |
| **Azure DevOps — Test Plans** | 9 | Create and manage test plans, suites, test cases, and build test results |
| **Azure DevOps — Search** | 2 | Full-text search across code repositories and work items |
| **Azure DevOps — Core** | 1 | Resolve user identity IDs by display name or email |
| **ADO Upload App** | 2 | Upload files to work items via an embedded VS Code panel UI |
| **Confluence** | 15 | Create, read, update, search, and manage Confluence pages, spaces, comments, and labels |
| **SC Wiki** | 14 | Create, read, update, delete, search, and manage SC Wiki (XWiki) pages, spaces, comments, tags, history, and attachments |
| **Messaging (Outlook + Teams)** | 2 | Send emails via Outlook and messages via Microsoft Teams desktop app |
| **Web Search & Fetch** | 4 | Search DuckDuckGo (no API key) and fetch any URL as plain text; crawl websites (static or JS-rendered); uses Python subprocess to bypass TLS fingerprinting |
| **Nexus IQ Scanning** | 2 | Scan npm dependencies in local Node.js (npm/yarn) project directories for vulnerabilities; automated multi-phase remediation of direct and transitive CVEs |
| **SonarQube** | 6 | Query code quality, security hotspots, issues, and metrics from SonarQube |
| **Context Management** | 4 | Named workspace contexts auto-fill project/team/repo across all tools; stored in `~/.sc-node-mcp-context.json` |

---

## Prerequisites

Before installing, make sure you have:

| Requirement | Notes |
|---|---|
| **Node.js 20+** | Install from **Company Portal** (recommended) or [nodejs.org](https://nodejs.org/) |
| **NPM registry configured for SCB** | Run:<br> <code>npm config set registry https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release/ --global</code><br>This sets the default registry for all npm operations. |
| **VS Code** with **GitHub Copilot Chat** extension | MCP tools are invoked from Copilot Chat |
| **Azure DevOps PAT** | Scopes: `Code: Read & Write`, `Work Items: Read & Write`, `Project and Team: Read` |
| **SCB Artifactory access** | Required to pull the `@sc-node-mcp` npm package |
| **Confluence PAT** *(optional)* | Required only if you want Confluence tools — see [Confluence Integration](#confluence-integration) |
| **SC Wiki Token** *(optional)* | Required only if you want SC Wiki tools — see [SC Wiki Integration](#sc-wiki-integration) |
| **Python 3.x** *(optional)* | Required for Outlook/Teams messaging tools and `web_search` (DuckDuckGo). Auto-detected. |
| **Corporate proxy** *(optional)* | Common proxies: `http://10.239.9.190:443`, `http://10.239.9.188:443` |

---

## Setup

### 1. One-Click Install

The fastest way to get started. Click the badge at the top of this page (or the README), enter your credentials when prompted, and VS Code configures the MCP server automatically.

![One-Click Install demo](/docs/assets/images/one-click-install-demo.gif)

> You will be prompted for:
> - **ADO PAT** — your Azure DevOps Personal Access Token
> - **HTTPS Proxy** — optional, press Enter to skip
> - **Confluence PAT** — optional, press Enter to skip
> - **Nexus IQ User Code** — optional, press Enter to skip
> - **Nexus IQ Pass Code** — optional, press Enter to skip
> - **SonarQube Token** — optional, press Enter to skip
> - **SC Wiki Token** — optional, press Enter to skip
> - **Code Review Guide file path** — optional, full path to your `CODE_REVIEW_GUIDE.md` (enables PR review guidelines)

---

### 2. Manual Install

Prefer full control over your config? Add the server manually to your VS Code `mcp.json`.

![Manual Install demo](/docs/assets/images/manual-install-demo.gif)

**Steps:**

1. Open VS Code and go to **Settings → MCP** (or press `Cmd+Shift+P` → `Open MCP Settings`)
2. Add the following block to your `mcp.json`:

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
        "${input:sonar_token}",
        "${input:scwiki_token}"
      ],
      "env": {
        "CODE_REVIEW_GUIDE_FILE": "${input:code_review_guide}",
        "npm_config_registry": "https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release"
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
    },
    {
      "id": "scwiki_token",
      "type": "promptString",
      "description": "SC Wiki (XWiki) Bearer Token (optional, press Enter to skip)",
      "password": true
    },
    {
      "id": "code_review_guide",
      "type": "promptString",
      "description": "Your CODE_REVIEW_GUIDE.md file full path (optional, press Enter to skip)"
    }
  ]
}
```

3. Save the file — VS Code will detect the new server automatically.

---

### 3. Verify Installation

After installing, confirm the MCP server is running and all tools are registered.

![List installed MCP servers](/docs/assets/images/list-installed-mcp.gif)

**How to check:**

- Open Copilot Chat (`Cmd+Shift+I`)
- Click the **Tools** icon (🔧) in the chat toolbar
- You should see **sc-node-mcp** listed with all registered tools

If the server is not listed, check the Output panel (`View → Output → MCP`) for error messages.

---

### 4. Update MCP Config

Need to rotate your PAT, add a proxy, or add your Confluence credentials after initial setup? Update your MCP config without reinstalling.

![Update MCP config](/docs/assets/images/update-mcp-config.gif)

**Common updates:**

| Change | What to update |
|---|---|
| Rotate PAT | Update `ado_pat` input value in mcp.json |
| Add proxy | Add `https_proxy` input value (e.g. `http://10.239.9.190:443`) |
| Enable Confluence | Add `confluence_pat` input value |
| Enable SC Wiki | Add `scwiki_token` input value |
| Enable PR review guidelines | Set `code_review_guide` input value to the full path of your `CODE_REVIEW_GUIDE.md` |
| Switch to env vars | Set `AZURE_DEVOPS_PAT`, `CONFLUENCE_PAT`, `SCWIKI_TOKEN`, and `CODE_REVIEW_GUIDE_FILE` as environment variables instead |

---

## Granular Package Install

Install only the tools you need — each package is independently installable via one-click:

> **Recommended for most users:** Install `@sc-node-mcp/unified` (see [Setup](#setup)) — it includes all tools in a single server. Use individual packages only when you want a lighter footprint or to run multiple scoped MCP servers side-by-side.

<!-- GRANULAR-INSTALL-START -->
| Package | Install |
|---------|---------|
| All ADO tools (meta-package) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Work Items — Read (17 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_WORKITEMS_READ-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-workitems-read&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-workitems-read%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_WORKITEMS_READ-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-workitems-read&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-workitems-read%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Work Items — Write (9 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_WORKITEMS_WRITE-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-workitems-write&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-workitems-write%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_WORKITEMS_WRITE-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-workitems-write&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-workitems-write%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Repos — Read (12 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_REPOS_READ-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-repos-read&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-repos-read%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_REPOS_READ-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-repos-read&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-repos-read%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Repos — Write (9 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_REPOS_WRITE-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-repos-write&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-repos-write%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_REPOS_WRITE-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-repos-write&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-repos-write%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO PR Review (4 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_REVIEW-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-review&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-review%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_REVIEW-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-review&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-review%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22code_review_guide%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Your%20CODE_REVIEW_GUIDE.md%20file%20full%20path%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Pipelines (12 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_PIPELINES-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-pipelines&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-pipelines%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_PIPELINES-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-pipelines&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-pipelines%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Test Plans (9 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_TESTPLANS-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-testplans&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-testplans%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_TESTPLANS-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-testplans&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-testplans%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Sprints & Capacity (8 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_SPRINTS-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-sprints&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-sprints%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_SPRINTS-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-sprints&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-sprints%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| ADO Search — Code & Work Items (2 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_SEARCH-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-search&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-search%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_SEARCH-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-search&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-search%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| Confluence (15 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_CONFLUENCE-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-confluence&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fconfluence%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_CONFLUENCE-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-confluence&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fconfluence%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%24%7Binput%3Aconfluence_pat%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22confluence_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Confluence%20PAT%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) |
| SC Wiki (14 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_SCWIKI-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-scwiki&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fscwiki%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SCWIKI-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-scwiki&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fscwiki%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%24%7Binput%3Ascwiki_token%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22scwiki_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SC%20Wiki%20(XWiki)%20Bearer%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) |
| Messaging — Outlook + Teams | [![VS Code](https://img.shields.io/badge/VS_Code-Install_MESSAGING-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-messaging&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fmessaging%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MESSAGING-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-messaging&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fmessaging%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| Nexus IQ Scanning (2 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_NEXUS-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-nexus&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fnexus%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_NEXUS-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-nexus&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fnexus%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%24%7Binput%3Anexus_user%7D%22%2C%22%24%7Binput%3Anexus_pass%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_user%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20User%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22nexus_pass%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Nexus%20IQ%20Pass%20Code%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) |
| SonarQube (6 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_SONAR-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-sonar&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fsonar%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%22%2C%22%22%2C%22%24%7Binput%3Asonar_token%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SONAR-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-sonar&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fsonar%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%2C%22%22%2C%22%22%2C%22%22%2C%22%24%7Binput%3Asonar_token%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22sonar_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22SonarQube%20Token%20(optional%2C%20press%20Enter%20to%20skip)%22%2C%22password%22%3Atrue%7D%5D) |
| ADO Upload App (file attachments UI) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_ADO_UPLOAD_APP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-upload-app&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-upload-app%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_ADO_UPLOAD_APP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-ado-upload-app&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fado-upload-app%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| Web Search & Crawl (4 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_WEB-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-web&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fweb%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_WEB-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-web&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fweb%22%2C%22%24%7Binput%3Aado_pat%7D%22%2C%22%24%7Binput%3Ahttps_proxy%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22ado_pat%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22https_proxy%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22HTTPS%20Proxy%20URL%20(optional%2C%20e.g.%2C%20http%3A%2F%2F10.239.9.190%3A443%20-%20press%20Enter%20to%20skip)%22%7D%5D) |
| Browser Automation — Selenium WebDriver (48 tools) | [![VS Code](https://img.shields.io/badge/VS_Code-Install_APP_BRIDGE-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-app-bridge&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fapp-bridge%22%2C%22--chromedriver-path%22%2C%22%24%7Binput%3Achromedriver_path%7D%22%2C%22--edgedriver-path%22%2C%22%24%7Binput%3Aedgedriver_path%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22chromedriver_path%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Absolute%20path%20to%20chromedriver%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22edgedriver_path%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Absolute%20path%20to%20msedgedriver%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) [![VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_APP_BRIDGE-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=sc-node-mcp-app-bridge&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40sc-node-mcp%2Fapp-bridge%22%2C%22--chromedriver-path%22%2C%22%24%7Binput%3Achromedriver_path%7D%22%2C%22--edgedriver-path%22%2C%22%24%7Binput%3Aedgedriver_path%7D%22%5D%2C%22env%22%3A%7B%22npm_config_registry%22%3A%22https%3A%2F%2Fartifactory.global.standardchartered.com%2Fartifactory%2Fapi%2Fnpm%2Fnpm-release%22%7D%7D&inputs=%5B%7B%22id%22%3A%22chromedriver_path%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Absolute%20path%20to%20chromedriver%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%2C%7B%22id%22%3A%22edgedriver_path%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Absolute%20path%20to%20msedgedriver%20(optional%2C%20press%20Enter%20to%20skip)%22%7D%5D) |
<!-- GRANULAR-INSTALL-END -->

### Manual mcp.json Configuration

Each package accepts `<ADO_PAT>` and optionally `<HTTPS_PROXY>` as CLI arguments. Add one or more entries to your `.vscode/mcp.json`:

```jsonc
{
  "mcpServers": {
    "sc-node-mcp-pipelines": {
      "command": "npx",
      "args": ["-y", "@sc-node-mcp/ado-pipelines", "${input:ado_pat}"],
      "env": {
        "npm_config_registry": "https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release"
      }
    },
    "sc-node-mcp-workitems-read": {
      "command": "npx",
      "args": ["-y", "@sc-node-mcp/ado-workitems-read", "${input:ado_pat}"],
      "env": {
        "npm_config_registry": "https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release"
      }
    }
  },
  "inputs": [
    {
      "id": "ado_pat",
      "type": "promptString",
      "description": "Azure DevOps Personal Access Token",
      "password": true
    }
  ]
}
```

> **Proxy:** Add `"${input:https_proxy}"` as a second arg to any package if you need a corporate proxy.

> **PR Review guide:** The `@sc-node-mcp/ado-review` package also reads the `CODE_REVIEW_GUIDE_FILE` environment variable for review guidelines.

---

## Confluence Integration

Confluence tools are **optional** — they only activate when a valid Confluence PAT is provided. ADO tools always work regardless.

### 1. Create a Confluence PAT

Generate a Personal Access Token from your Confluence profile settings.

![Create Confluence PAT](/docs/assets/images/conf-create-pat.gif)

**Steps:**

1. Log in to [Confluence](https://confluence.global.standardchartered.com)
2. Click your **profile avatar** → **Personal Access Tokens**
3. Click **Create token**, give it a name and expiry date
4. Copy the token — you will only see it once
5. Paste it as the `confluence_pat` input when prompted during install (or update your `mcp.json`)

---

### 2. Confluence in Action

Once the PAT is configured, Confluence tools are available directly in Copilot Chat.

![Confluence list recent pages](/docs/assets/images/conf-list-my-recent.gif)

**Example prompts:**

```
List my recently updated Confluence pages
```
```
Search Confluence for "API integration" in the CC space
```
```
Create a Confluence page titled "Sprint 42 Notes" under the CC space
```
```
Update the Confluence page ID 123456 with this content: ...
```

---

## SC Wiki Integration

SC Wiki tools are **optional** — they only activate when a valid SC Wiki Bearer token is provided. ADO tools always work regardless.

### 1. Create an SC Wiki Token

Generate a Bearer token via XWiki's Token Authenticator extension.

![Create SC Wiki token](/docs/assets/images/SCWiki_Token.gif)

**Steps:**

1. Log in to [SC Wiki](https://scwiki.global.standardchartered.com)
2. Open your **user profile** → **Token Authenticator** (or the administration section, depending on your instance)
3. Generate a new Bearer token and copy it — you will only see it once
4. Paste it as the `scwiki_token` input when prompted during install (or update your `mcp.json`)

> Pages are addressed by a dotted reference (e.g. `Sandbox.S2B NG.WebHome`), not a numeric ID. The wiki base URL defaults to `https://scwiki.global.standardchartered.com` but can be overridden via the `SCWIKI_URL` environment variable.

---

### 2. SC Wiki in Action

Once the token is configured, SC Wiki tools are available directly in Copilot Chat.

![SC Wiki list recent pages](/docs/assets/images/SCWiki_Action.gif)

**Example prompts:**

```
List my recently created SC Wiki pages
```
```
Search SC Wiki for "onboarding checklist"
```
```
Create an SC Wiki page at "Sandbox.S2B NG.Sprint 42 Notes" with this content: ...
```
```
Get the version history of the SC Wiki page "Space.PageName"
```

---

## Web Search Integration

Web Search tools are **always available** — no credentials or configuration required. They activate automatically when the server starts.

> **Standalone install:** Use the **Web Search & Crawl** row in the [granular install table](#granular-install) above.

**Available tools:**

| Tool | Description |
|---|---|
| `web_search` | Search DuckDuckGo Lite and return up to 10 results. Uses a Python subprocess bridge to bypass TLS fingerprinting. |
| `web_fetch` | Fetch and return the plain-text content of any HTTPS URL (max 15,000 chars). |
| `web_crawl` | Crawl a website from a seed URL, following same-domain links (BFS). Modes: `urls`, `summary`, `full`, `links`. |
| `web_crawl_browser` | Crawl a JavaScript-rendered (SPA) website using the system Chrome or Edge browser. Use when `web_crawl` returns empty results. |

**Requirements:**
- **Python 3.x** must be on `PATH` for `web_search` (auto-detects `python3` / `python` / `py`)
- **Chrome or Edge** installed for `web_crawl_browser`

**Example prompts:**

```
Search the web for "SonarQube quality gate configuration"
```
```
Fetch the content from https://confluence.global.standardchartered.com/display/CC/API+Guidelines
```
```
Crawl https://example.com and give me a summary of all pages
```

> **Tip:** Use `web_fetch` to read public documentation or internal Confluence pages by URL when you already know the URL. Use `web_search` when you need to discover relevant links first.

---

## Browser Automation (app-bridge)

`@sc-node-mcp/app-bridge` is a **standalone-only** package (not included in `unified`) that drives a real Chrome or Edge browser via Selenium WebDriver 4.x, so Copilot Chat can navigate pages, fill forms, click elements, take screenshots, inspect network requests/console messages, emulate devices/network/geolocation, and record raw performance traces on your behalf — the network/console/emulation/performance tools are implemented via Chrome DevTools Protocol (CDP) through `selenium-webdriver`'s own connection support, with no extra dependency.

> **Requirements:** Google Chrome and/or Microsoft Edge installed, plus a matching `chromedriver`/`msedgedriver` executable already downloaded locally (this package never auto-downloads drivers — useful behind a proxy that blocks driver downloads).

### Manual mcp.json Configuration

Unlike other packages, app-bridge uses **named CLI flags** instead of positional PAT/proxy arguments, since it has no ADO/Confluence concept:

```jsonc
{
  "servers": {
    "app-bridge": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/absolute/path/to/packages/app-bridge/dist/index.js",
        "--chromedriver-path",
        "${input:chromedriver_path}",
        "--edgedriver-path",
        "${input:edgedriver_path}"
      ]
    }
  },
  "inputs": [
    { "id": "chromedriver_path", "type": "promptString", "description": "Absolute path to chromedriver" },
    { "id": "edgedriver_path", "type": "promptString", "description": "Absolute path to msedgedriver" }
  ]
}
```

Both driver paths are optional individually — configure only the browser(s) you use. A proxy is auto-detected the same way as every other package, then applied as a `--proxy-server=` browser launch argument (Node's `HTTPS_PROXY` has no effect on the browser's own network stack). Override auto-detection with `--proxy <url>` if needed.

For the full list of tools (browser lifecycle, navigation, element location including relative locators, interaction, forms, mouse/keyboard, alerts, cookies, windows/frames, screenshots, network/console inspection, emulation, and performance tracing), see [docs/guide/APP_BRIDGE_TOOLS_GUIDE.md](docs/guide/APP_BRIDGE_TOOLS_GUIDE.md).

**Example prompts:**

```
Start a Chrome browser and go to https://www.selenium.dev/selenium/web/web-form.html
```
```
Find the text input labeled "Text input" and type "hello world" into it
```
```
Take a screenshot of the current page
```
```
List any console errors and show me the network requests that failed
```

---

## Using with Copilot Chat

Once SC Node MCP is running, all tools are automatically available in VS Code Copilot Chat. No special commands — just ask in natural language.

![Copilot Chat with SC Node MCP](/docs/assets/images/chat-custom.gif)

**Example prompts to try:**

```
Show me all open work items assigned to me in the current sprint
```
```
Create a work item titled "Fix login timeout" in the Payments project
```
```
List all open PRs in the platform-api repository
```
```
Trigger the build pipeline for the auth-service feature branch
```
```
Send an email to john.doe@sc.com with subject "Sprint recap" and a summary of today's work
```
```
Send a Teams message to Jane Smith: "The deployment is complete"
```
```
Search the web for "Azure DevOps best practices 2025"
```
```
Fetch the content from https://docs.microsoft.com/en-us/rest/api/azure/devops
```

> **Tip:** Enable **agent mode** in Copilot Chat for multi-step workflows — for example, creating a work item, linking a PR, and posting a comment all in one prompt.

---

## Available Tools

SC Node MCP exposes **114 tools** (max, when all credentials provided) across all integrations. Below is a high-level summary.

<details>
<summary>Azure DevOps — Work Items (26 tools)</summary>

| Tool | Description |
|---|---|
| `wit_list_projects` | List all projects in the Azure DevOps organization |
| `wit_get_work_item` | Retrieve details of a specific work item by ID |
| `wit_my_work_items` | List work items assigned to the current user |
| `wit_list_backlogs` | List available backlogs for a team |
| `wit_list_backlog_work_items` | List work items in a specific backlog |
| `wit_get_work_items_batch_by_ids` | Get multiple work items by IDs |
| `wit_create_work_item` | Create a new work item |
| `wit_update_work_item` | Update fields on a work item |
| `wit_update_work_items_batch` | Update multiple work items in a batch |
| `wit_add_work_item_comment` | Add a comment to a work item |
| `wit_update_work_item_comment` | Edit the text of an existing comment |
| `wit_list_work_item_comments` | List all comments on a work item |
| `wit_get_work_items_for_iteration` | Get work items for a specific iteration |
| `wit_add_child_work_items` | Add child work items to a parent |
| `wit_get_work_item_type` | Get work item type details |
| `wit_get_query` | Get a work item query by ID |
| `wit_get_query_results_by_id` | Execute a query and get results |
| `wit_work_items_link` | Create a link between two work items |
| `wit_work_item_unlink` | Remove links from a work item |
| `wit_link_work_item_to_pull_request` | Link a work item to an existing pull request |
| `wit_list_work_item_pull_requests` | List all pull requests linked to a work item |
| `wit_list_work_item_commits` | List all commits linked to a work item |
| `wit_list_work_item_revisions` | Get the full revision history of a work item |
| `wit_get_work_item_attachment` | Download a work item attachment as base64 |
| `wit_list_teams` | List all teams in a project |
| `wit_list_iterations` | List all iterations for a project and team |

</details>

<details>
<summary>Azure DevOps — Repositories & PRs (20 tools)</summary>

| Tool | Description |
|---|---|
| `repo_list_repos_by_project` | List all repositories in a project |
| `repo_get_repo_by_name_or_id` | Get repository details by name or ID |
| `repo_list_branches_by_repo` | List all branches in a repository |
| `repo_list_my_branches_by_repo` | List branches created by the current user |
| `repo_get_branch_by_name` | Get branch details by name |
| `repo_create_branch` | Create a new branch in a repository |
| `repo_get_file_content` | Get the content of a file from a repository |
| `repo_list_directory` | List files and folders in a repository directory |
| `repo_search_commits` | Search commits by message or author |
| `repo_list_pull_requests_by_repo_or_project` | List pull requests with optional filters |
| `repo_get_pull_request_by_id` | Get pull request details by ID |
| `repo_create_pull_request` | Create a new pull request |
| `repo_update_pull_request` | Update PR title, description, or status |
| `repo_update_pull_request_reviewers` | Add or remove reviewers from a pull request |
| `repo_get_pull_request_changes` | Get the list of file changes in a PR |
| `repo_vote_pull_request` | Approve, reject, or reset your vote on a PR |
| `repo_list_pull_request_threads` | List all comment threads on a pull request |
| `repo_create_pull_request_thread` | Create a new comment thread on a PR |
| `repo_update_pull_request_thread` | Update the status of a PR comment thread |
| `repo_reply_to_comment` | Reply to an existing PR comment thread |

</details>

<details>
<summary>Azure DevOps — Pipelines (12 tools)</summary>

| Tool | Description |
|---|---|
| `pipelines_get_build_definitions` | List all pipeline definitions in a project |
| `pipelines_run_pipeline` | Trigger a new pipeline run |
| `pipelines_list_runs` | List pipeline runs with optional filters |
| `pipelines_get_run` | Get details of a specific pipeline run |
| `pipelines_get_build_status` | Get the status of a build by ID |
| `pipelines_get_builds` | Get builds with various filters |
| `pipelines_cancel_run` | Cancel a running pipeline/build |
| `pipelines_retry_stage` | Retry a specific stage in a pipeline run |
| `pipelines_list_work_item_pipelines` | Find all pipeline runs linked to a work item |
| `pipelines_get_build_log` | Retrieve the combined log output for a build |
| `pipelines_get_build_changes` | Get the work items and commits for a build |
| `pipelines_list_artifacts` | List artifacts produced by a build |

</details>

<details>
<summary>Azure DevOps — PR Review (4 tools)</summary>

| Tool | Description |
|---|---|
| `repo_review_pr` | AI-driven review of a PR; posts comments on specific diff lines |
| `repo_pr_diff` | Get the complete diff of a pull request |
| `post_pr_comment` | Post a comment on a specific PR diff line |
| `delete_all_pr_review_comments` | Delete all AI-generated review comments from a PR |

</details>

<details>
<summary>Azure DevOps — Sprint & Capacity (8 tools)</summary>

| Tool | Description |
|---|---|
| `work_list_iterations` | List all iterations (sprints) in a project |
| `work_create_iterations` | Create new sprint iterations in a project |
| `work_list_team_iterations` | List iterations assigned to a specific team |
| `work_assign_iterations` | Assign existing iterations to a team |
| `work_get_iteration_capacities` | Get capacity breakdown for all teams in an iteration |
| `work_get_team_capacity` | Get capacity for a specific team in a sprint |
| `work_update_team_capacity` | Update a team member's capacity for a sprint |
| `work_get_team_settings` | Get team settings including default iteration and area path |

</details>

<details>
<summary>Azure DevOps — Test Plans (9 tools)</summary>

| Tool | Description |
|---|---|
| `testplan_list_test_plans` | List all test plans in a project |
| `testplan_create_test_plan` | Create a new test plan |
| `testplan_list_test_suites` | List all test suites in a test plan |
| `testplan_create_test_suite` | Create a new test suite inside a test plan |
| `testplan_add_test_cases_to_suite` | Add test case work items to a test suite |
| `testplan_list_test_cases` | List all test cases in a test suite (includes child suites by default) |
| `testplan_create_test_case` | Create a new test case work item |
| `testplan_update_test_case_steps` | Update the steps of an existing test case |
| `testplan_show_test_results_from_build_id` | Get test pass/fail results for a specific build |

</details>

<details>
<summary>Azure DevOps — Search (2 tools)</summary>

| Tool | Description |
|---|---|
| `search_code` | Full-text search across Azure DevOps repositories |
| `search_workitem` | Search work items by free text with optional filters |

</details>

<details>
<summary>Azure DevOps — Core (1 tool)</summary>

| Tool | Description |
|---|---|
| `core_get_identity_ids` | Resolve user identity IDs by display name or email |

</details>

<details>
<summary>ADO Upload App (2 tools)</summary>

| Tool | Description |
|---|---|
| `wit_upload_attachment_ui` | Upload files to a work item via an embedded VS Code panel UI |
| `wit_upload_attachment` | Upload a file attachment to a work item directly |

> These tools are provided by the separate `@sc-node-mcp/ado-upload-app` package. See [ADO Upload App](docs/ADO_UPLOAD_APP.md) for details.

</details>

<details>
<summary>Confluence (15 tools)</summary>

| Tool | Description |
|---|---|
| `confluence_create_page` | Create a new Confluence page under a parent page |
| `confluence_update_page` | Update the content of an existing Confluence page |
| `confluence_read_page` | Read the full content of a Confluence page by URL |
| `confluence_get_page_id` | Look up a page ID and metadata from its URL |
| `confluence_search` | Search Confluence content using a CQL query |
| `confluence_list_my_pages` | List Confluence pages created by the current user |
| `confluence_get_page` | Get a Confluence page by its numeric ID |
| `confluence_find_page` | Find a Confluence page by space key and exact title |
| `confluence_get_page_children` | List the child pages of a Confluence page by its ID |
| `confluence_list_spaces` | List Confluence spaces |
| `confluence_get_space` | Get details of a Confluence space by its key |
| `confluence_delete_page` | Delete a Confluence page by ID (title confirmation required) |
| `confluence_add_comment` | Add a page-level comment to a Confluence page |
| `confluence_get_labels` | Get all labels on a Confluence page |
| `confluence_add_label` | Add a label to a Confluence page |

</details>

<details>
<summary>SC Wiki (14 tools)</summary>

| Tool | Description |
|---|---|
| `scwiki_create_page` | Create a new SC Wiki page at the given dotted reference (upsert — overwrites an existing page) |
| `scwiki_update_page` | Update the title and/or content of an existing SC Wiki page |
| `scwiki_get_page` | Get an SC Wiki page's metadata and content by its dotted reference |
| `scwiki_find_page` | Look up an SC Wiki page from its browser URL and return its metadata and content |
| `scwiki_search` | Search SC Wiki pages by keyword across title, content, and page name |
| `scwiki_list_my_pages` | List SC Wiki pages created by the authenticated user |
| `scwiki_get_page_children` | List the direct child pages of an SC Wiki page |
| `scwiki_list_spaces` | List the top-level spaces in the configured SC Wiki instance |
| `scwiki_delete_page` | Delete an SC Wiki page by its dotted reference (title confirmation required — moved to recycle bin) |
| `scwiki_add_comment` | Add a comment to an SC Wiki page |
| `scwiki_get_labels` | Get all tags on an SC Wiki page |
| `scwiki_add_label` | Add a tag to an SC Wiki page |
| `scwiki_get_page_history` | Get the version history of an SC Wiki page |
| `scwiki_list_attachments` | List the attachments on an SC Wiki page (metadata only) |

</details>

<details>
<summary>Web Search & Fetch (4 tools)</summary>

| Tool | Description |
|---|---|
| `web_search` | Search DuckDuckGo Lite and return up to 10 results (title, URL, snippet). Uses a Python subprocess bridge to bypass TLS fingerprinting. No API key required. |
| `web_fetch` | Fetch and return the plain-text content of any HTTPS URL (max 15,000 chars). |
| `web_crawl` | Crawl a website from a seed URL, following same-domain links (BFS). Returns URLs, summaries, full text, or link graphs. Configurable depth and page count. |
| `web_crawl_browser` | Crawl a JavaScript-rendered (SPA) website using the system Chrome or Edge browser. Use when `web_crawl` returns empty results. Requires Chrome or Edge installed. |

</details>

<details>
<summary>Messaging — Outlook & Teams (2 tools)</summary>

| Tool | Description |
|---|---|
| `email_send` | Send an email via the Outlook desktop app |
| `teams_send_message` | Send a message via Microsoft Teams desktop app |

</details>

<details>
<summary>Nexus IQ Scanning (2 tools)</summary>

| Tool | Description |
|---|---|
| `nexus_scan_vulnerabilities` | Scan npm dependencies in a local Node.js (npm/yarn) project directory for vulnerabilities |
| `nexus_fix_vulnerabilities` | Automatically remediate vulnerabilities found by the scan (multi-phase: direct deps, transitive upgrades, resolutions). Node.js (npm/yarn) projects only. |

</details>

<details>
<summary>SonarQube (6 tools)</summary>

| Tool | Description |
|---|---|
| `sonar_search_projects` | Search or list SonarQube projects by name or key |
| `sonar_get_branches` | List all analysed branches for a SonarQube project |
| `sonar_get_quality_gate_status` | Check quality gate pass/fail status for a branch or pull request |
| `sonar_get_issues` | Search for bugs, vulnerabilities, and code smells |
| `sonar_get_hotspots` | List security hotspots requiring manual review |
| `sonar_get_measures` | Retrieve code quality metrics (coverage, bugs, tech debt, ratings) |

</details>

For the complete tool list with parameters and examples, see the [Tools Reference](docs/TOOLS_REFERENCE.md).

---

## Usage Analytics

> **Privacy notice:** Each time the unified MCP server starts, it records a single entry for **usage counting purposes only**. The sole purpose is to understand how many people are using the tool. No usage behaviour, queries, or content is ever recorded.

### What is collected

```json
{"timestamp": "2026-05-08T09:12:34.567Z", "user": "Jane Doe", "version": "2.7.3", "toolsEnabled": ["ado", "confluence"]}
```

| What IS recorded | What is NOT recorded |
|---|---|
| ADO display name (resolved from your PAT at startup) | Your PAT or any credential |
| Server version | Prompts, queries, or chat messages |
| Timestamp of startup | Work item IDs, repo names, or any ADO data |
| Which integrations are active (e.g. confluence, nexus) | Any content you create, read, or update |

### Where it goes

Data is appended to the `telemetry/usage-log` branch of this repository (`DDCPQPR/23966-sc-node-mcp`) inside SC's own Azure DevOps. **No data leaves Standard Chartered infrastructure.** The write is fire-and-forget — if it fails, a message is logged to stderr and the server continues normally.

### How to opt out

Set the `DISABLE_TELEMETRY=1` environment variable before starting the server. The server will skip the recording entirely and log `[Telemetry] Disabled via DISABLE_TELEMETRY=1`.

**In `.vscode/mcp.json`:**

```jsonc
{
  "servers": {
    "sc-node-mcp": {
      "command": "npx",
      "args": ["..."],
      "env": {
        "DISABLE_TELEMETRY": "1"
      }
    }
  }
}
```

**Or in your shell:**

```bash
export DISABLE_TELEMETRY=1
```

### Legal basis

This data collection is conducted under **legitimate interest** — tracking adoption of an internal developer tool built and operated by CIB S2B Trade&FM Engineering team. If you have concerns, raise them via the [Support](#support) page or contact Author(1540326@zone1.scb.net).

---

## Support

**Report issues or request features:** [SC Node MCP — Microsoft Teams Support Channel](https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e)

---

*SC Node MCP — Protocol-driven automation for Azure DevOps, Confluence, Messaging, and Web Search inside VS Code.*
