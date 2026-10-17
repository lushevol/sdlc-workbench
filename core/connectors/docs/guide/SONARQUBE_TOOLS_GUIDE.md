# SonarQube Tools Guide

Complete usage guide for all 6 SonarQube tools in the SC Node MCP Server.

> **Prerequisites:** SonarQube tools are enabled when `SONAR_TOKEN` is provided (as a CLI argument, environment variable, or in `config.json`).  
> **SonarQube URL:** `https://sonarqube.vx.standardchartered.com` (hardcoded)

---

## Table of Contents

- [Test Environment Setup](#test-environment-setup)
- [Tool Reference](#tool-reference)
  1. [sonar_search_projects](#1-sonar_search_projects)
  2. [sonar_get_branches](#2-sonar_get_branches)
  3. [sonar_get_quality_gate_status](#3-sonar_get_quality_gate_status)
  4. [sonar_get_issues](#4-sonar_get_issues)
  5. [sonar_get_hotspots](#5-sonar_get_hotspots)
  6. [sonar_get_measures](#6-sonar_get_measures)
- [Common Workflows](#common-workflows)

---

## Test Environment Setup

Ensure your SonarQube token is configured before running any SonarQube tools:

```bash
# Via environment variable
export SONAR_TOKEN="squ_your_sonarqube_token"

# Via CLI argument (position 6)
npx -y @sc-node-mcp/unified \
  "your-ado-pat" \
  "" "" "" "" \
  "squ_your_sonarqube_token"
```

---

## Tool Reference

### 1. `sonar_search_projects`

Search or list SonarQube projects by name or key.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ⚠️ Optional | — | Filter text — project name or key substring |
| `page` | number | ⚠️ Optional | `1` | Page number for pagination |
| `pageSize` | number | ⚠️ Optional | `50` | Results per page (max 500) |

**Test Query:**
```
Find SonarQube projects matching "my-service"
```

**JSON Invocation:**
```json
{
  "query": "my-service",
  "page": 1,
  "pageSize": 20
}
```

**Example Response:**
```json
{
  "paging": { "pageIndex": 1, "pageSize": 20, "total": 3 },
  "components": [
    {
      "key": "your-project_my-service",
      "name": "my-service",
      "qualifier": "TRK",
      "lastAnalysisDate": "2026-04-28T10:23:00+0000"
    }
  ]
}
```

**Alternative Prompts:**
- `List all SonarQube projects`
- `Search SonarQube for projects in the payments domain`

---

### 2. `sonar_get_branches`

List all analysed branches for a SonarQube project.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectKey` | string | ✅ Yes | SonarQube project key |

**Test Query:**
```
List all analysed branches for SonarQube project "your-project_my-service"
```

**JSON Invocation:**
```json
{
  "projectKey": "your-project_my-service"
}
```

**Example Response:**
```json
[
  {
    "name": "main",
    "isMain": true,
    "type": "LONG",
    "status": { "qualityGateStatus": "OK" },
    "analysisDate": "2026-04-28T10:23:00+0000"
  },
  {
    "name": "develop",
    "isMain": false,
    "type": "LONG",
    "status": { "qualityGateStatus": "ERROR" },
    "analysisDate": "2026-04-27T14:11:00+0000"
  }
]
```

**Alternative Prompts:**
- `Show me all branches analysed by SonarQube for my-service`
- `Which branches are tracked in SonarQube for project X?`

---

### 3. `sonar_get_quality_gate_status`

Check quality gate pass/fail status for a project branch or pull request.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectKey` | string | ✅ Yes | SonarQube project key |
| `branch` | string | ⚠️ Optional | Branch name (mutually exclusive with `pullRequest`) |
| `pullRequest` | string | ⚠️ Optional | Pull request ID (mutually exclusive with `branch`) |

**Test Query:**
```
Check the quality gate status for project "your-project_my-service" on the main branch
```

**JSON Invocation:**
```json
{
  "projectKey": "your-project_my-service",
  "branch": "main"
}
```

**Example Response:**
```json
{
  "projectStatus": {
    "status": "OK",
    "conditions": [
      { "status": "OK", "metricKey": "new_coverage", "comparator": "LT", "errorThreshold": "80", "actualValue": "85.2" },
      { "status": "OK", "metricKey": "new_duplicated_lines_density", "comparator": "GT", "errorThreshold": "3", "actualValue": "1.1" }
    ],
    "periods": [{ "index": 1, "mode": "PREVIOUS_VERSION", "date": "2026-04-01T00:00:00+0000" }]
  }
}
```

**Alternative Prompts:**
- `Does my-service pass the quality gate on the develop branch?`
- `Check quality gate for PR #42 in SonarQube`

---

### 4. `sonar_get_issues`

Search for bugs, vulnerabilities, and code smells in a SonarQube project.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `projectKey` | string | ✅ Yes | — | SonarQube project key |
| `types` | string | ⚠️ Optional | all | Comma-separated: `BUG`, `VULNERABILITY`, `CODE_SMELL` |
| `severities` | string | ⚠️ Optional | all | Comma-separated: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `statuses` | string | ⚠️ Optional | `OPEN` | Comma-separated statuses |
| `branch` | string | ⚠️ Optional | — | Branch name |
| `page` | number | ⚠️ Optional | `1` | Page number |
| `pageSize` | number | ⚠️ Optional | `100` | Results per page (max 500) |

**Test Query:**
```
Show all critical bugs in SonarQube project "your-project_my-service" on the main branch
```

**JSON Invocation:**
```json
{
  "projectKey": "your-project_my-service",
  "types": "BUG",
  "severities": "BLOCKER,CRITICAL",
  "branch": "main",
  "pageSize": 50
}
```

**Example Response:**
```json
{
  "total": 2,
  "issues": [
    {
      "key": "AX123abc",
      "rule": "java:S2259",
      "severity": "CRITICAL",
      "component": "your-project_my-service:src/main/java/Service.java",
      "line": 42,
      "message": "A \"NullPointerException\" could be thrown.",
      "type": "BUG",
      "status": "OPEN"
    }
  ]
}
```

**Alternative Prompts:**
- `List all open vulnerabilities in my-service`
- `Show BLOCKER code smells in project X on the develop branch`

---

### 5. `sonar_get_hotspots`

List security hotspots in a project that require manual review.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `projectKey` | string | ✅ Yes | — | SonarQube project key |
| `branch` | string | ⚠️ Optional | — | Branch name |
| `status` | string | ⚠️ Optional | `TO_REVIEW` | `TO_REVIEW` or `REVIEWED` |
| `page` | number | ⚠️ Optional | `1` | Page number |
| `pageSize` | number | ⚠️ Optional | `100` | Results per page (max 500) |

**Test Query:**
```
Show unreviewed security hotspots for project "your-project_my-service" on main
```

**JSON Invocation:**
```json
{
  "projectKey": "your-project_my-service",
  "branch": "main",
  "status": "TO_REVIEW"
}
```

**Example Response:**
```json
{
  "paging": { "pageIndex": 1, "pageSize": 100, "total": 1 },
  "hotspots": [
    {
      "key": "AY456def",
      "component": "your-project_my-service:src/main/java/AuthController.java",
      "securityCategory": "sql-injection",
      "vulnerabilityProbability": "HIGH",
      "status": "TO_REVIEW",
      "line": 88,
      "message": "Make sure using this SQL query is safe here."
    }
  ]
}
```

**Alternative Prompts:**
- `Are there any security hotspots I need to review in my-service?`
- `List already-reviewed security hotspots for project X`

---

### 6. `sonar_get_measures`

Retrieve code quality metrics for a project.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `component` | string | ✅ Yes | — | SonarQube project key |
| `metricKeys` | string | ⚠️ Optional | default set | Comma-separated metric keys |
| `branch` | string | ⚠️ Optional | — | Branch name |

**Default metrics returned when `metricKeys` is omitted:**  
`bugs`, `vulnerabilities`, `code_smells`, `coverage`, `duplicated_lines_density`, `ncloc`, `sqale_index`, `reliability_rating`, `security_rating`, `sqale_rating`

**Test Query:**
```
Get code quality metrics for project "your-project_my-service" on the main branch
```

**JSON Invocation:**
```json
{
  "component": "your-project_my-service",
  "branch": "main"
}
```

**Example Response:**
```json
{
  "component": {
    "key": "your-project_my-service",
    "name": "my-service",
    "measures": [
      { "metric": "bugs", "value": "3" },
      { "metric": "vulnerabilities", "value": "1" },
      { "metric": "code_smells", "value": "47" },
      { "metric": "coverage", "value": "84.5" },
      { "metric": "duplicated_lines_density", "value": "2.3" },
      { "metric": "ncloc", "value": "12540" },
      { "metric": "sqale_index", "value": "720" },
      { "metric": "reliability_rating", "value": "3.0" },
      { "metric": "security_rating", "value": "2.0" },
      { "metric": "sqale_rating", "value": "1.0" }
    ]
  }
}
```

**Alternative Prompts:**
- `What is the code coverage for my-service on the develop branch?`
- `Get only the bugs and vulnerability count for project X`

---

## Common Workflows

### Check Project Health Before Release

```
1. Get quality gate status on main
2. List any open BLOCKER/CRITICAL bugs
3. Show unreviewed security hotspots
4. Get overall code metrics
```

**Combined example:**
```
Run a full health check on SonarQube project "your-project_my-service" on main — quality gate, critical issues, hotspots, and coverage
```

### Security Review Workflow

```
1. List all open vulnerabilities (type=VULNERABILITY, severity=BLOCKER,CRITICAL)
2. List all security hotspots with status=TO_REVIEW
3. Compare against the security_rating metric
```

**Example prompt:**
```
Show me all security vulnerabilities and hotspots in "your-project_my-service" that need review
```

### Monitor Multiple Branches

```
1. Use sonar_get_branches to see all tracked branches
2. Check quality gate per branch using sonar_get_quality_gate_status
3. Compare metrics across branches using sonar_get_measures
```

---

## Related Documentation

- [Tools Reference — SonarQube section](../TOOLS_REFERENCE.md#sonarqube)
- [Prompts Reference — SonarQube section](../PROMPTS.md#sonarqube)
- [Setup Guide — SonarQube token configuration](../SETUP.md)
- [SonarQube Package README](../../packages/sonar/README.md)
