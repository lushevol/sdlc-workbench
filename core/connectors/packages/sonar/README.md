# @sc-node-mcp/sonar

SonarQube MCP Server providing code quality and security analysis tools for Standard Chartered's SonarQube instance.

## Overview

This package provides SonarQube integration through the Model Context Protocol. It enables AI assistants to query project health, quality gate status, issues, security hotspots, and code metrics from SonarQube — all through 6 standardised tools.

**Tools:**
- `sonar_search_projects` — Search or list SonarQube projects
- `sonar_get_branches` — List all analysed branches for a project
- `sonar_get_quality_gate_status` — Check quality gate pass/fail status
- `sonar_get_issues` — Search for bugs, vulnerabilities, and code smells
- `sonar_get_hotspots` — List security hotspots requiring review
- `sonar_get_measures` — Retrieve code quality metrics

## Tool Reference

### `sonar_search_projects`

Search or list SonarQube projects by name or key.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ⚠️ Optional | — | Filter text — project name or key substring |
| `page` | number | ⚠️ Optional | `1` | Page number for pagination |
| `pageSize` | number | ⚠️ Optional | `50` | Results per page (max 500) |

---

### `sonar_get_branches`

List all analysed branches for a SonarQube project.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project` | string | ✅ Yes | — | SonarQube project key |

---

### `sonar_get_quality_gate_status`

Check quality gate pass/fail status for a project branch or pull request.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `projectKey` | string | ✅ Yes | — | SonarQube project key |
| `branch` | string | ⚠️ Optional | — | Branch name (mutually exclusive with `pullRequest`) |
| `pullRequest` | string | ⚠️ Optional | — | Pull request ID (mutually exclusive with `branch`) |

---

### `sonar_get_issues`

Search for bugs, vulnerabilities, and code smells in a project.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `componentKeys` | string | ✅ Yes | — | Comma-separated SonarQube project keys to search issues in |
| `types` | string | ⚠️ Optional | all | Comma-separated: `BUG`, `VULNERABILITY`, `CODE_SMELL` |
| `severities` | string | ⚠️ Optional | all | Comma-separated: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `statuses` | string | ⚠️ Optional | `OPEN` | Comma-separated statuses |
| `branch` | string | ⚠️ Optional | — | Branch name |
| `page` | number | ⚠️ Optional | `1` | Page number |
| `pageSize` | number | ⚠️ Optional | `100` | Results per page (max 500) |

---

### `sonar_get_hotspots`

List security hotspots in a project that require manual review.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `projectKey` | string | ✅ Yes | — | SonarQube project key |
| `branch` | string | ⚠️ Optional | — | Branch name |
| `status` | string | ⚠️ Optional | `TO_REVIEW` | `TO_REVIEW` or `REVIEWED` |
| `page` | number | ⚠️ Optional | `1` | Page number |
| `pageSize` | number | ⚠️ Optional | `100` | Results per page (max 500) |

---

### `sonar_get_measures`

Retrieve code quality metrics for a project.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `component` | string | ✅ Yes | — | SonarQube project key (component key) |
| `metricKeys` | string | ⚠️ Optional | standard set | Comma-separated metric keys |
| `branch` | string | ⚠️ Optional | — | Branch name |

**Default metrics:** `bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,ncloc,sqale_index,reliability_rating,security_rating,sqale_rating`

## Installation

> 📘 **Complete Setup Guide:** See [Installation Guide](../../docs/INSTALLATION.md) for detailed instructions and troubleshooting.

```bash
# Option 1: NPX (no installation required)
npx -y @sc-node-mcp/sonar \
  "your-ado-pat" \
  "http://10.239.9.190:443" \
  "" \
  "" \
  "" \
  "your-sonar-token"

# Option 2: Global installation
yarn global add @sc-node-mcp/sonar
sc-node-mcp-sonar \
  "your-ado-pat" \
  "http://10.239.9.190:443" \
  "" \
  "" \
  "" \
  "your-sonar-token"
```

### CLI Parameters

| Position | Parameter | Required | Description |
|----------|-----------|----------|-------------|
| 1 | ADO PAT | ✅ Yes | Azure DevOps Personal Access Token |
| 2 | Proxy URL | ⚠️ Optional | Corporate proxy (e.g. `http://10.239.9.190:443`) |
| 3 | Confluence PAT | ⚠️ Optional | Leave empty `""` if not needed |
| 4 | Nexus User Code | ⚠️ Optional | Leave empty `""` if not needed |
| 5 | Nexus Pass Code | ⚠️ Optional | Leave empty `""` if not needed |
| 6 | SonarQube Token | ✅ Yes | SonarQube user token (`squ_...`) |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_DEVOPS_PAT` | Azure DevOps Personal Access Token |
| `HTTPS_PROXY` | Corporate proxy URL |
| `SONAR_TOKEN` | SonarQube authentication token |

### VS Code MCP Configuration

```json
{
  "servers": {
    "sonar-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@sc-node-mcp/sonar",
        "your-ado-pat",
        "http://10.239.9.190:443",
        "",
        "",
        "",
        "your-sonar-token"
      ]
    }
  }
}
```

## SonarQube Instance

This package is pre-configured for Standard Chartered's SonarQube instance:

- **URL:** `https://sonarqube.vx.standardchartered.com`

## Prerequisites

- Node.js 18+
- A valid SonarQube user token (generate at **My Account → Security → Generate Tokens** in SonarQube)
- Access to Standard Chartered's SonarQube instance

## Prompts

The `@sc-node-mcp/sonar` package ships 8 MCP prompts for guided SonarQube workflows:

- `sonar-search-projects` — Search or list SonarQube projects
- `sonar-get-branches` — List all analysed branches for a project
- `sonar-quality-gate` — Check quality gate pass/fail status for a branch or PR
- `sonar-get-issues` — Search for bugs, vulnerabilities, and code smells
- `sonar-get-hotspots` — List security hotspots requiring review
- `sonar-get-measures` — Retrieve code quality metrics for a project
- `sonar-project-health` — Summary health check across quality gate, issues, and metrics
- `sonar-pr-analysis` — Quality analysis for a pull request branch

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## CHANGELOG

See [CHANGELOG.md](./CHANGELOG.md) for version history.
