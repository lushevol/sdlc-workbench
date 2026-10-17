# @sc-node-mcp/nexus

Nexus IQ MCP Server for vulnerability scanning and automated remediation of Node.js (npm/yarn) projects registered in Standard Chartered's Sonatype Nexus IQ instance.

> **Scope:** Currently supports **Node.js (npm/yarn) projects only** — reads `package.json` and `node_modules`. Other ecosystems (Maven, pip, NuGet, etc.) are not currently supported.

## Overview

This package provides Nexus IQ integration through the Model Context Protocol. It reads `package.json` and `node_modules` from the local filesystem, submits all npm dependencies to Nexus IQ for policy evaluation, generates multi-format reports, and can automatically remediate vulnerabilities — all without requiring Azure DevOps access.

**Node.js (npm/yarn) projects only.** The tool requires a `package.json` and populated `node_modules` directory at the target path.

**Tools:**
- `nexus_scan_vulnerabilities` — Scan local npm dependencies for security vulnerabilities using Nexus IQ
- `nexus_fix_vulnerabilities` — Automatically remediate vulnerabilities found by a previous scan

## How It Works

### Scan Flow

1. Reads `package.json` from the specified `projectPath` (defaults to current working directory)
2. Auto-installs dependencies (`yarn install --frozen-lockfile` / `npm ci` / `npm install`)
3. Resolves the internal Nexus IQ application ID using the public ID
4. Parses local `node_modules` to build an accurate component list
5. Evaluates components against Nexus IQ policy (polls up to 60 seconds)
6. Generates JSON, Markdown, and HTML reports in `nexus-report/` and opens the HTML report in the default browser
7. Returns a structured text summary with per-severity counts and CVE detail

### Fix Flow

1. Reads the existing `nexus-report/nexus-vulnerability-report.json` from the project directory
2. **Phase A** — Bumps direct dependency versions in `package.json` and runs install
3. **Phase B1** — Runs `yarn upgrade` / `npm install` to resolve transitive deps via `^` range
4. **Phase B2** — Identifies and optionally upgrades parent direct deps (requires `approveParentUpgrades=true`)
5. **Phase B3** — Force-pins remaining transitive deps via `resolutions`/`overrides` (requires `approveResolutions=true`)
6. **Phase C** — Appends a fix summary to the existing scan reports

## Tool Reference

### `nexus_scan_vulnerabilities`

Scan local npm dependencies for security vulnerabilities using Nexus IQ.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `applicationId` | string | ✅ Yes | — | Nexus IQ public application ID. Format: `ITAM__ENV__REPO_NAME` (e.g. `51855__DCDAQPR__51855-ui-platform`) |
| `projectPath` | string | ⚠️ Optional | `process.cwd()` | Absolute path to the project directory containing `package.json` |
| `deepMode` | boolean | ⚠️ Optional | `false` | `true` for exhaustive scan (all deps including devDependencies, no filtering). Default pipeline-aligned mode scans production deps only and excludes sonatype-* IDs and CVSS < 4.0 |

**Scan modes:**

| Prompt keyword | `deepMode` | Behaviour |
|---|---|---|
| `"Scan"` (default) | `false` | Production dependencies only; sonatype-* IDs and CVSS < 4.0 excluded — matches ADO pipeline |
| `"Deep Scan"`, `"full scan"`, `"include dev dependencies"` | `true` | All deps including devDependencies; every CVE and sonatype-* finding reported with no filtering |

**Example response:**

```json
{
  "applicationId": "51855__DCDAQPR__51855-ui-platform",
  "repoName": "51855-ui-platform",
  "totalComponentsScanned": 142,
  "scanMode": "pipeline",
  "summary": {
    "Critical": 1,
    "High": 4,
    "Medium": 12,
    "Low": 3,
    "total": 20
  },
  "vulnerabilities": [
    {
      "component": "lodash",
      "version": "4.17.15",
      "vulnId": "CVE-2021-23337",
      "severity": "High",
      "cvss": "7.2",
      "description": "Command Injection",
      "dependency": "direct",
      "fixVersion": "4.17.21"
    }
  ],
  "reportDir": "/path/to/project/nexus-report"
}
```

**Severity thresholds (CVSS score):**

| Severity | CVSS Score |
|----------|-----------|
| Critical | ≥ 9.0 |
| High | ≥ 7.0 |
| Medium | ≥ 4.0 |
| Low | > 0 |

---

### `nexus_fix_vulnerabilities`

Automatically remediate vulnerabilities found by `nexus_scan_vulnerabilities`. Reads the existing `nexus-report/nexus-vulnerability-report.json` from the current working directory.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `applicationId` | string | ✅ Yes | — | Nexus IQ public application ID that was previously scanned (used for display only) |
| `approveParentUpgrades` | boolean | ⚠️ Optional | `false` | Set `true` to approve and apply Phase B2 — upgrading parent direct dependencies of transitive vulnerabilities |
| `approveResolutions` | boolean | ⚠️ Optional | `false` | Set `true` to approve and apply Phase B3 — adding `resolutions`/`overrides` in `package.json` for remaining transitive vulnerabilities |

**Recommended workflow:**

```
1. Run nexus_scan_vulnerabilities to generate the report
2. Run nexus_fix_vulnerabilities (no approval flags) to see the proposed fix plan
3. Re-run with approveParentUpgrades=true to apply parent upgrades
4. Re-run with approveResolutions=true to apply resolutions/overrides
```

**Example output snippet:**
```
🔧 Starting vulnerability fix workflow for 51855__DCDAQPR__51855-ui-platform
Package manager: yarn

📦 Phase A — Fixing 2 direct dependency vulnerability/ies...
  ✅ Fixed 2 direct dependency/ies via package.json update
     lodash: 4.17.15 → 4.17.21 (CVE-2021-23337)
     axios: 0.21.1 → 1.6.0 (CVE-2023-45857)

🔄 Phase B1 — Running yarn upgrade for transitive vulnerabilities...
  ✅ yarn upgrade completed.
  ...
```

## Installation

> 📘 **Complete Setup Guide:** See [Installation Guide](../../docs/INSTALLATION.md) for detailed instructions and troubleshooting.

```bash
# Option 1: NPX (no installation required)
npx -y @sc-node-mcp/nexus \
  "" \
  "http://10.239.9.190:443" \
  "" \
  "your-nexus-user-code" \
  "your-nexus-pass-code"

# Option 2: Global installation
yarn global add @sc-node-mcp/nexus
sc-node-mcp-nexus \
  "" \
  "http://10.239.9.190:443" \
  "" \
  "your-nexus-user-code" \
  "your-nexus-pass-code"
```

### CLI Parameters

| Position | Parameter | Required | Description |
|----------|-----------|----------|-------------|
| 1 | ADO PAT | — | Not required for standalone nexus use; pass empty string `""` |
| 2 | Proxy URL | ⚠️ Optional | Corporate proxy (e.g. `http://10.239.9.190:443`) |
| 3 | Confluence credentials | — | Pass empty string `""` |
| 4 | `NEXUS_USER_CODE` | ✅ Yes | Nexus IQ username / user code |
| 5 | `NEXUS_PASS_CODE` | ✅ Yes | Nexus IQ password / pass code |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXUS_USER_CODE` | ✅ Yes | Nexus IQ username |
| `NEXUS_PASS_CODE` | ✅ Yes | Nexus IQ password |
| `HTTPS_PROXY` | ⚠️ Optional | Corporate proxy URL |

### `config.json` (local dev)

```json
{
  "HTTPS_PROXY": "http://10.239.9.190:443",
  "NEXUS_USER_CODE": "your-nexus-username",
  "NEXUS_PASS_CODE": "your-nexus-password"
}
```

> **Note:** `config.json` is gitignored. Never commit credentials.

## VS Code MCP Extension

Add to `.vscode/mcp.json`:

```jsonc
{
  "mcpServers": {
    "nexus-server": {
      "command": "npx",
      "args": [
        "-y",
        "@sc-node-mcp/nexus",
        "",
        "${input:https_proxy}",
        "",
        "${input:nexus_user_code}",
        "${input:nexus_pass_code}"
      ]
    }
  },
  "inputs": [
    {
      "id": "https_proxy",
      "type": "promptString",
      "description": "HTTPS Proxy URL (optional, press Enter to skip)"
    },
    {
      "id": "nexus_user_code",
      "type": "promptString",
      "description": "Nexus IQ Username"
    },
    {
      "id": "nexus_pass_code",
      "type": "promptString",
      "description": "Nexus IQ Password",
      "password": true
    }
  ]
}
```

## Programmatic Usage

```javascript
import { configureNexusTools, getNexusConnection } from '@sc-node-mcp/nexus';
import { createMcpServer } from '@sc-node-mcp/core';

const server = createMcpServer('my-nexus-server', '1.0.0');

const nexusConnectionProvider = () => getNexusConnection('user', 'pass');
configureNexusTools(server, nexusConnectionProvider);
```

## Use with Unified Package

The `@sc-node-mcp/unified` package includes Nexus IQ scanning alongside ADO and Confluence tools:

```bash
npx -y @sc-node-mcp/unified \
  "your-ado-pat" \
  "http://10.239.9.190:443" \
  "" \
  "your-nexus-user-code" \
  "your-nexus-pass-code"
```

## Prompts

The `@sc-node-mcp/nexus` package ships 1 MCP prompt for guided vulnerability scanning:

- `nexus-vulnerability-scan` — Scan local npm dependencies for security vulnerabilities using Nexus IQ and optionally apply automated remediations

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## Dependencies

- `@sc-node-mcp/core` — Core MCP server infrastructure
- `zod` — Parameter schema validation
