# @sc-node-mcp/web

MCP server for web search, URL fetching, and website crawling — no API key required.

## Overview

This package exposes four tools that give AI assistants access to live web content:

- **`web_search`** — Search the web via DuckDuckGo Lite and return structured results (title, URL, snippet)
- **`web_fetch`** — Fetch and strip the plain-text content of any HTTPS URL
- **`web_crawl`** — Crawl a website from a seed URL, following same-domain links (BFS). Returns URLs, summaries, full text, or link graphs
- **`web_crawl_browser`** — Crawl a JavaScript-rendered (SPA) website using the system Chrome or Edge browser. Use when `web_crawl` returns empty results because the site uses React, Angular, or Vue

### How `web_search` Works (Python Bridge)

DuckDuckGo uses TLS fingerprinting (JA3) to detect bots. Node.js's OpenSSL generates a fingerprint that DDG flags, returning a 202 CAPTCHA. Python's `ssl` module generates a different fingerprint that passes DDG's checks.

To work around this, `web_search` uses a **Python subprocess bridge** — the same pattern as the `@sc-node-mcp/messaging` package:

```
Node.js MCP tool
    └── spawn(python3, [search-ddg.py])
            ├── stdin:  JSON { "query": "...", "proxy": "http://..." }
            └── stdout: JSON { "results": [{ title, url, snippet }] }
                     or JSON { "error": "..." }
```

The Python script (`scripts/search-ddg.py`) is bundled inside the npm package and uses only Python standard library modules (`urllib`, `ssl`, `html`, `re`) — no `pip install` required.

**Requirement:** Python 3.x must be installed and on `PATH`. The server auto-detects `python3`, `python`, or `py` (Windows).

## Included Tools

| Tool | Description |
|------|-------------|
| `web_search` | Search DuckDuckGo Lite. Returns up to 10 results with title, URL, and snippet. |
| `web_fetch` | Fetch any HTTPS URL and return stripped plain-text content (max 15,000 chars). |
| `web_crawl` | Crawl a website via plain HTTP (BFS). Modes: `urls`, `summary`, `full`, `links`. |
| `web_crawl_browser` | Crawl a JS-rendered site via headless Chrome/Edge. Same modes as `web_crawl`. Requires Chrome or Edge installed. |

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Node.js | 18+ |
| Python 3.x | Required for `web_search`. Tries `python3` → `python` → `py`. |
| Chrome or Edge | Required for `web_crawl_browser`. Auto-detected from standard install paths. |
| Network | Proxy auto-detected via `detectProxyFor('html.duckduckgo.com')`. |

## Installation

> 📘 **Complete Setup Guide:** See [Installation Guide](../../docs/INSTALLATION.md).

```bash
# Option 1: NPX (recommended)
npx -y @sc-node-mcp/web "" "http://10.239.9.190:443"
# Arg 1: leave empty (ADO PAT not used by this package)
# Arg 2: HTTPS proxy (optional — auto-detected if omitted)

# Option 2: Global install
yarn global add @sc-node-mcp/web
sc-node-mcp-web "" "http://10.239.9.190:443"
```

## Configuration

The proxy for DuckDuckGo is auto-detected separately from the ADO proxy. If the auto-detected proxy isn't working, pass it explicitly as the second argument.

| Config | Source | Description |
|--------|--------|-------------|
| `HTTPS_PROXY` / arg 2 | CLI arg or env var | Proxy for external internet access (optional) |

## VS Code MCP Config (`mcp.json`)

```jsonc
"sc-node-mcp-web": {
    "command": "node",
    "args": [
        "${workspaceFolder}/packages/web/src/index.js",
        "",
        "${input:https_proxy}"
    ]
}
```

## Package Structure

```
packages/web/
├── src/
│   ├── index.js                 # MCP server entry point
│   ├── tools.js                 # Registers all 4 web tools
│   ├── tools/
│   │   ├── websearch.js         # web_search (Python bridge) + web_fetch
│   │   ├── webcrawl.js          # web_crawl (plain HTTP BFS crawler)
│   │   └── webcrawlbrowser.js   # web_crawl_browser (headless Chrome/Edge crawler)
│   └── prompts.js               # MCP prompts for all 4 tools
├── scripts/
│   └── search-ddg.py            # Bundled Python script for DDG search
└── tests/
    ├── websearch.test.js        # web_search / web_fetch unit tests
    ├── webcrawl.test.js         # web_crawl unit tests
    ├── webcrawlbrowser.test.js  # web_crawl_browser unit tests
    ├── prompts.test.js          # Prompt registration tests
    └── tools.test.js            # configureWebTools() registration tests
```

## Architecture Notes

### Python Bridge

The `search-ddg.py` script is bundled in `scripts/` and shipped with the npm package (listed in `files` in `package.json`). It is invoked at runtime via `child_process.spawn` using an auto-detected Python 3.x executable.

```javascript
// Auto-detect Python 3.x (cached after first call)
const pythonCmd = findPython3Command();  // tries python3 / python / py
const proc = spawn(pythonCmd, [scriptPath], { stdio: ['pipe', 'pipe', 'pipe'] });
proc.stdin.write(JSON.stringify({ query, proxy }));
```

### Proxy Detection

On startup, `detectProxyFor('html.duckduckgo.com')` probes known corporate proxy candidates (including `127.0.0.1:9000` SSH tunnel) and picks the first that responds with HTTP < 500. The detected proxy is passed to the Python script via stdin JSON.

### `web_fetch`

Uses Node.js `https` module directly (not Python). Follows up to 3 redirects, strips HTML tags, and truncates to 15,000 characters.

### `web_crawl`

Uses Node.js `https` directly for plain-HTTP BFS crawling. Stays within the same origin. Supports four output modes: `urls` (URL list), `summary` (URL + title + 500-char snippet), `full` (URL + title + full text), `links` (URL + outbound same-domain links).

### `web_crawl_browser` (Headless Chrome/Edge)

Spawns the system-installed Chrome or Edge in headless mode (`--headless=new --dump-dom`) to fetch JS-rendered pages before crawling. Uses `--virtual-time-budget=10000` to allow SPAs up to 10 seconds of virtual time to execute before the DOM is captured.

**Browser detection:** Tries platform-specific paths in order (e.g. `/Applications/Google Chrome.app/...` on macOS, `C:\Program Files\Google\Chrome\...` on Windows) and falls back to bare command names (`google-chrome`, `chromium`). Detection result is cached after the first successful call.

```
web_crawl_browser
    └── spawn(chrome/edge, ['--headless=new', '--dump-dom', url])
            └── stdout: full rendered HTML
```

**Note:** `web_crawl_browser` is slower than `web_crawl` (browser startup + JS execution per page). Use a lower `maxPages` and `maxDepth` and keep the default `delayMs: 1000`.

## Testing

```bash
cd packages/web
yarn test          # run tests once
yarn test:watch    # watch mode
```

Tests use `vi.mock('node:child_process', ...)` to mock `spawn` and `execSync` for `web_search` and `web_crawl_browser`, and `vi.mock('node:https')` for `web_fetch` and `web_crawl`. Coverage target: 90%.
