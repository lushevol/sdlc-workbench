# Web Package Guide (`@sc-node-mcp/web`)

> **Package:** `packages/web`
> **Version:** 1.2.0
> **Registered in:** `@sc-node-mcp/unified` (primary distribution)

---

## What Is It?

The `web` package gives AI assistants access to live web content — no API key required. It registers **4 MCP tools** and **4 MCP prompts** on the server.

---

## Tools Reference

### `web_search`
Search the web via DuckDuckGo Lite. Returns up to 10 results with title, URL, and snippet.

**Why Python?**
DuckDuckGo uses JA3 TLS fingerprinting to detect bots. Node.js OpenSSL generates a fingerprint that DDG blocks (returns HTTP 202 CAPTCHA). Python's `ssl` module generates a different fingerprint that passes. The bundled `scripts/search-ddg.py` handles this using only Python standard library — no `pip install` required.

```
Node.js MCP tool
    └── spawn(python3, [search-ddg.py])
            ├── stdin:  { "query": "...", "proxy": "http://..." }
            └── stdout: { "results": [{ title, url, snippet }] }
```

**Requirement:** Python 3.x on PATH.

**Best for:** Current events, documentation lookup, any information query.

---

### `web_fetch`
Fetch and strip the plain-text content of any HTTPS URL (max 15,000 chars).

Uses Node.js `https` directly — no Python needed. Follows up to 3 redirects. Respects `HTTPS_PROXY`.

**Best for:** Reading a specific page after `web_search` returns its URL. Works well on server-rendered pages, REST API responses, JSON endpoints, documentation sites.

---

### `web_crawl`
BFS-crawl a website from a seed URL, staying within the same domain. Uses `cheerio` for HTML parsing.

**Output modes:**

| Mode | What It Returns |
|---|---|
| `urls` | List of all discovered URLs (default) |
| `summary` | URL + page title + first 500 chars of text |
| `full` | URL + page title + full stripped text |
| `links` | URL + all outbound same-domain links (link graph) |

**Parameters:**

| Param | Default | Max |
|---|---|---|
| `maxDepth` | 3 | 10 |
| `maxPages` | 50 | 200 |
| `delayMs` | 500ms | 5000ms |

**Best for:** Traditional websites, documentation portals, news sites, any server-rendered or SSR (Next.js/Nuxt) site.

---

### `web_crawl_browser`
BFS-crawl a website using the system-installed Chrome or Edge browser (`--headless=new --dump-dom --virtual-time-budget=10000`).

**Parameters:**

| Param | Default | Max |
|---|---|---|
| `maxDepth` | 3 | 10 |
| `maxPages` | 50 | 200 |
| `delayMs` | 1000ms | 10000ms |

**Requirement:** Google Chrome or Microsoft Edge installed. Auto-detects executable on macOS, Windows, Linux.

---

## ⚠️ Honest Limitation of `web_crawl_browser`

This is the most important thing to understand before using this tool.

### What it does
Spawns Chrome with these flags:
```
--headless=new
--dump-dom
--virtual-time-budget=10000
--no-sandbox
--disable-gpu
```

`--dump-dom` captures the DOM after a **virtual time budget** of 10 seconds. This handles:
- ✅ Synchronous JavaScript
- ✅ `setTimeout`/`setInterval` that fires within the budget
- ✅ Light client-side rendering where data is embedded in the page

### What it cannot do
- ❌ **Async `fetch()` / XHR API calls** — the virtual time budget does not wait for network responses
- ❌ **Shadow DOM web components** — `--dump-dom` sees the outer shell; `shadowRoot` content is not included in the serialised HTML
- ❌ **React/Vue/Angular SPAs that fetch data on mount** — the component tree renders but all `useEffect(() => fetch(...))` calls never resolve
- ❌ **Auth-gated content** — no session/cookie support

### Real-world example
The [FactSet Portfolio Analytics SPA](https://developer.factset.com/widgets/Portfolio-Analytics-SPA/1532562) uses Vue 3 with FactSet Design System web components (`fds-pa-*`). Every widget renders inside a Shadow DOM. `web_crawl_browser` returned only:

```
Showcase: Portfolio Analytics Widgets
Portfolio International Equity Fund ...
Composition Performance Holdings Breakdown Attribution
```

— which is the outer Vue app shell. All widget content (tables, charts, data) is inside shadow roots and was invisible to `--dump-dom`.

### When to use `web_crawl_browser` vs Playwright

| Scenario | Use |
|---|---|
| Server-rendered HTML site | `web_crawl` (faster, no browser overhead) |
| SSR Next.js / Nuxt site | `web_crawl` or `web_crawl_browser` |
| Light client-side JS, no API calls on mount | `web_crawl_browser` ✅ |
| SPA with async data fetching (React, Vue, Angular) | **Playwright** (`open_browser_page` + `run_playwright_code`) |
| Web components / Shadow DOM | **Playwright** — pierce shadow roots via `el.shadowRoot.querySelectorAll()` |
| Need to click buttons, switch tabs, fill forms | **Playwright** |
| Bulk URL discovery across 50+ pages | `web_crawl_browser` ✅ (BFS is built-in) |

---

## Do You Need This Package?

| Tool | Keep? | Reasoning |
|---|---|---|
| `web_search` | ✅ Yes | Unique value — DuckDuckGo without an API key, Python TLS bridge is genuinely clever |
| `web_fetch` | ✅ Yes | Simple, fast, useful for reading any URL |
| `web_crawl` | ✅ Yes | Practical for traditional/SSR sites, documentation crawling |
| `web_crawl_browser` | ⚠️ Keep with caveats | Works for light JS sites; misleading for heavy SPAs. The tool description says "React/Angular/Vue SPAs" but it cannot handle async data-fetching SPAs or Shadow DOM |

**The package as a whole: keep it.** `web_search` alone justifies the package — there's no good Node.js alternative to DuckDuckGo search without a paid API key, and the Python bridge pattern is well-tested and already established in the codebase.

---

## Architecture

```
packages/web/
├── src/
│   ├── index.js          # MCP server entry point
│   ├── tools.js          # Registers all 4 tools
│   ├── prompts.js        # Registers all 4 prompts
│   └── tools/
│       ├── websearch.js  # web_search (Python bridge) + web_fetch (Node https)
│       ├── webcrawl.js   # web_crawl (cheerio BFS)
│       └── webcrawlbrowser.js  # web_crawl_browser (Chrome --dump-dom BFS)
├── scripts/
│   └── search-ddg.py     # Bundled Python script (stdlib only, no pip)
└── tests/
    ├── websearch.test.js
    ├── webcrawl.test.js
    ├── webcrawlbrowser.test.js
    ├── tools.test.js
    └── prompts.test.js
```

---

## Configuration

No credentials required. Optional proxy support:

```bash
# Via CLI argument (2nd arg)
npx @sc-node-mcp/web "" "http://proxy:8080"

# Via environment variable
HTTPS_PROXY=http://proxy:8080 npx @sc-node-mcp/web
```

The proxy is forwarded to both the Python bridge (`search-ddg.py`) and Node.js HTTP requests.

---

## Running Tests

```bash
cd packages/web
yarn test
```

Tests mock `child_process.spawn` and `execSync` (Python/browser detection) and `node:https` — no real network calls are made. Use `clearPythonCache()` and `clearBrowserCache()` between tests to reset detection state.

---

## Potential Improvements

| Improvement | Priority |
|---|---|
| Update `web_crawl_browser` description to accurately state Shadow DOM / async fetch limitations | High |
| Add a `--wait-for-selector` or `--wait-for-network-idle` mechanism for true SPA rendering | Medium — would require switching from `--dump-dom` to a CDP-based approach |
| Expose `web_crawl_browser` only when Chrome/Edge is detected, with a graceful fallback message | Low |
