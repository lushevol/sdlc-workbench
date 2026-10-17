# Telemetry Dashboard

Live usage analytics for the `sc-node-mcp` MCP server. Tracks startup sessions recorded to the `telemetry/usage-log` ADO branch.

## Quick Start

```bash
yarn telemetry
```

This single command:
1. Fetches the latest `usage.log` from the `DDCPQPR/23966-sc-node-mcp` ADO repo (`telemetry/usage-log` branch)
2. Saves it locally to `docs/telemetry/data/usage.log` (gitignored)
3. Starts a local HTTP server on `http://localhost:4000`
4. Opens the dashboard in your browser automatically

## Prerequisites

An Azure DevOps PAT with **read** access to the `23966-sc-node-mcp` repository. Set it via:

```bash
export AZURE_DEVOPS_PAT=your_pat_here
```

Or add it to `config.json` at the repo root:

```json
{
  "AZURE_DEVOPS_PAT": "your_pat_here"
}
```

## Port Override

```bash
TELEMETRY_PORT=5000 yarn telemetry
```

## Opt-Out of Telemetry Recording

Users who do not want their sessions recorded can set:

```bash
export DISABLE_TELEMETRY=1
```

## Periodic Refresh (Cron)

To automatically refresh the local data file on a schedule, add a cron job:

```bash
# Refresh data every 6 hours (macOS/Linux)
crontab -e
```

```
0 */6 * * * cd /path/to/repo && AZURE_DEVOPS_PAT=your_pat node scripts/telemetry.js --pull-only 2>&1 >> /tmp/telemetry-pull.log
```

## Dashboard Features

| Section | Description |
|---|---|
| **KPI Cards** | Total sessions, unique users, latest version, active this week |
| **Daily Sessions** | Bar chart of server starts per day |
| **Version Distribution** | Donut chart showing sessions per package version |
| **Platform Breakdown** | Donut chart showing macOS / Windows / Linux split |
| **Tool Enablement** | Horizontal bar chart showing how many sessions had each integration active |
| **Top Users** | Table of most active users with last seen date and latest version |

Use the **7d / 30d / 90d / All** time-range filter to scope all charts. Toggle dark mode with the 🌙 button.

## Data Format

Each line in `usage.log` is a JSON object (NDJSON):

```json
{
  "timestamp": "2026-05-14T08:30:00.000Z",
  "user": "Jane Doe",
  "version": "2.1.0",
  "toolsEnabled": ["ado", "confluence"],
  "platform": "darwin",
  "nodeVersion": "v22.0.0",
  "vsCodeVersion": "1.99.0",
  "hostname": "a3f8b1c2d4e5f607"
}
```

> **Privacy note:** `hostname` is a 16-character SHA-256 prefix — the actual hostname is never stored.
