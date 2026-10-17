# @sc-node-mcp/app-bridge

MCP server for browser automation via Selenium WebDriver 4.x — Chrome and Edge only.

## Overview

`app-bridge` gives AI assistants direct control of a real Chrome or Edge browser through the official
[`selenium-webdriver`](https://www.npmjs.com/package/selenium-webdriver) Node bindings, so Copilot Chat
can navigate pages, locate elements (including Selenium 4 relative locators), interact with forms,
handle alerts/cookies/windows/frames, run JavaScript, capture screenshots, and inspect network
requests/console messages, emulate devices/network/geolocation, and record raw performance traces
via the Chrome DevTools Protocol (CDP).

- **Standalone-only** — not included in `@sc-node-mcp/unified` (same precedent as `@sc-node-mcp/web`),
  since it uses named CLI flags rather than the positional ADO-style config every other package shares.
- **Chrome + Edge only.** No Firefox/Safari, no Selenium Grid/remote WebDriver.
- **Driver paths are always explicit.** This package never auto-downloads `chromedriver`/`msedgedriver`
  — useful behind a corporate proxy that blocks driver downloads. Supply the absolute path to each
  driver executable you plan to use.
- **Single global browser session** at a time — `browser_start` replaces any existing session.
- **Visible (headed) by default** — a real window opens so you can watch the AI interact with the page;
  pass `headless: true` to `browser_start` to run without a visible window.
- **Stateless locators** — every tool takes a locator object and re-finds the element on each call
  (an optional `index` disambiguates multiple matches). No element-handle cache to manage.
- **Selenium test-code generation** — `codegen_generate_test` returns a workflow for driving the
  real browser tools step-by-step and then authoring a raw JavaScript/Java/Python/C# Selenium
  script from what actually happened; `element_scan_page` scans the whole page for interactive
  elements and suggests locators for each. Mirrors `appium/appium-mcp`'s `appium_generate_tests`.
- **CDP-based inspection/emulation, no new dependency.** Network/console capture, device/network/
  geolocation emulation, and raw performance tracing are implemented via `selenium-webdriver`'s own
  `driver.createCDPConnection()` support — no puppeteer or chrome-remote-interface dependency was
  added. Network/console capture is a single running buffer for the whole session (not reset per
  navigation); use `network_clear_requests`/`console_clear_messages` to reset manually. Performance
  tracing returns raw trace data plus basic self-computed stats only — it does not include Core Web
  Vitals/LCP/CLS "Insights" analysis (that requires bundling Chrome DevTools' own internal trace
  engine, deliberately out of scope).

See [docs/guide/APP_BRIDGE_TOOLS_GUIDE.md](../../docs/guide/APP_BRIDGE_TOOLS_GUIDE.md) for the full
48-tool reference with parameters and examples.

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Node.js | 18+ |
| Google Chrome and/or Microsoft Edge | Installed in the standard OS location, or override via `--chrome-binary-path`/`--edge-binary-path` |
| `chromedriver` / `msedgedriver` | A version matching your installed browser, downloaded locally. Supply its absolute path — never auto-downloaded. |

## Installation

```bash
# Option 1: NPX
npx -y @sc-node-mcp/app-bridge --chromedriver-path "/path/to/chromedriver" --edgedriver-path "/path/to/msedgedriver"

# Option 2: Global install
yarn global add @sc-node-mcp/app-bridge
sc-node-mcp-app-bridge --chromedriver-path "/path/to/chromedriver" --edgedriver-path "/path/to/msedgedriver"
```

Both driver paths are optional individually — configure only the browser(s) you plan to use.

## Configuration

Unlike other packages, app-bridge uses **named CLI flags** (not positional args), since it has no
ADO/Confluence/Nexus/Sonar concept to position around.

| Flag | Env var fallback | Description |
|------|-------------------|-------------|
| `--chromedriver-path` | `CHROMEDRIVER_PATH` | Absolute path to the chromedriver executable |
| `--edgedriver-path` | `EDGEDRIVER_PATH` | Absolute path to the msedgedriver executable |
| `--proxy` | `HTTPS_PROXY` | Override auto-detected proxy (applied as a browser `--proxy-server=` launch arg, not a Node env var — the browser's own network stack doesn't read `HTTPS_PROXY`) |
| `--chrome-binary-path` | `CHROME_BINARY_PATH` | Override the Chrome binary location |
| `--edge-binary-path` | `EDGE_BINARY_PATH` | Override the Edge binary location |

Priority: CLI flags > environment variables. Neither driver path is required at startup — `browser_start`
returns a clear error if the requested browser's driver path was never configured.

## VS Code MCP Config (`mcp.json`)

```jsonc
"app-bridge": {
    "type": "stdio",
    "command": "node",
    "args": [
        "${workspaceFolder}/packages/app-bridge/dist/index.js",
        "--chromedriver-path",
        "${input:chromedriver_path}",
        "--edgedriver-path",
        "${input:edgedriver_path}"
    ]
}
```

## Tools

All 48 tools, grouped by category. Each entry includes a sample chat prompt you can use as-is.
See [docs/guide/APP_BRIDGE_TOOLS_GUIDE.md](../../docs/guide/APP_BRIDGE_TOOLS_GUIDE.md) for full
parameter tables and JSON invocation examples.

### Session & Navigation

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `browser_start` | Launch a new Chrome or Edge session (replaces any existing session) | "Start a visible Chrome browser" |
| `browser_close` | Close the active browser session | "Close the browser" |
| `browser_set_timeouts` | Set implicit wait, page load, and script timeouts | "Set a 15 second implicit wait" |
| `browser_navigate` | Navigate to a URL | "Go to https://example.com" |
| `browser_navigate_back` | Go back in browser history | "Go back to the previous page" |
| `browser_navigate_forward` | Go forward in browser history | "Go forward to the next page" |
| `browser_refresh` | Reload the current page | "Refresh the page" |
| `browser_get_page_info` | Get the current URL and page title | "What page am I currently on?" |
| `browser_get_page_source` | Get the full HTML source (truncated to 15,000 chars) | "Show me the HTML source of this page" |
| `browser_wait_for_text` | Wait for given text to appear anywhere on the page | "Wait for the text \"Order confirmed\" to appear" |

### Element Location & Waiting

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `element_find` | Find one element matching a locator (highlights it in the browser) | "Find the Submit button" |
| `element_find_all` | Find all elements matching a locator, up to 50 | "List all links on the page" |
| `element_wait_for` | Wait until an element is present, visible, invisible, clickable, or contains text | "Wait until the loading spinner disappears" |

### Element Interaction & Forms

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `element_click` | Click an element | "Click the Submit button" |
| `element_send_keys` | Type text into an element (clears first by default) | "Type \"admin\" into the username field" |
| `element_clear` | Clear the value of an input/textarea | "Clear the search box" |
| `element_get_text` | Read an element's visible text | "What text is shown in the error message?" |
| `element_get_attribute` | Read an element's attribute/property | "What is the href of the first link?" |
| `element_get_css_value` | Read a computed CSS property of an element | "What is the background color of the header?" |
| `element_get_rect` | Get an element's position and size | "What are the dimensions of the logo image?" |
| `element_get_state` | Get whether an element is displayed, enabled, and selected | "Is the checkout button enabled?" |
| `element_upload_file` | Send a file path to a `<input type="file">` element | "Upload C:\\temp\\invoice.pdf to the file input" |
| `select_get_options` | List `<select>` options with text/value/selected state | "List the options in the country dropdown" |
| `select_option` | Select/deselect option(s) of a `<select>` element | "Select \"United Kingdom\" from the country dropdown" |
| `script_execute` | Execute JavaScript in the browser (sync or async) | "Scroll to the bottom of the page" |

### Mouse, Keyboard, Alerts & Cookies

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `mouse_hover` | Hover over an element | "Hover over the profile menu icon" |
| `mouse_double_click` | Double-click an element | "Double-click the file to open it" |
| `mouse_right_click` | Right-click an element | "Right-click the image to open its context menu" |
| `mouse_drag_and_drop` | Drag one element and drop it onto another | "Drag the first task card into the \"Done\" column" |
| `keyboard_press_key` | Send a special key or literal text to an element or the focused element | "Press Enter to submit the search" |
| `alert_handle` | Accept, dismiss, read, or type into the current alert/confirm/prompt dialog | "Accept the confirmation dialog" |
| `cookie_add` | Add a cookie for the current domain | "Add a cookie named \"theme\" with value \"dark\"" |
| `cookie_get` | Read all cookies, or one by name | "Show me all cookies for this site" |
| `cookie_delete` | Delete all cookies, or one by name | "Delete the \"session\" cookie" |

### Windows, Frames & Screenshots

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `window_manage` | List, switch, open, close, or resize browser windows/tabs | "Open a new tab" |
| `frame_manage` | Switch focus between iframes, or back to the default/parent frame | "Switch into the payment iframe" |
| `screenshot_capture` | Take a screenshot of the viewport or a single element | "Take a screenshot of the page" |

### Test Code Generation

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `element_scan_page` | Scan the whole page for interactive elements and suggest locators | "Scan the page and show me all the interactive elements with their locators" |
| `codegen_generate_test` | Generate raw Selenium test code from a natural-language scenario | "Generate a Selenium test in Python for: open the login page, type \"admin\" into the username field, click Submit" |

### Network Inspection

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `network_list_requests` | List captured network requests since capture started (or last cleared) | "List all XHR requests made by the page" |
| `network_get_request` | Get full detail (headers, status, bodies) for one request by id | "Show me the response body of request 3" |
| `network_clear_requests` | Clear the captured network requests buffer | "Clear the captured network requests" |

### Console Inspection

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `console_list_messages` | List captured console messages since capture started (or last cleared) | "Show me any console errors" |
| `console_get_message` | Get full detail (including stack trace) for one message by id | "Show me the full stack trace of console message 2" |
| `console_clear_messages` | Clear the captured console messages buffer | "Clear the captured console messages" |

### Emulation

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `browser_emulate` | Emulate device/network/color-scheme/geolocation/user-agent/headers via CDP | "Emulate a mobile device in dark mode with Slow 3G network" |

### Performance Tracing

| Tool | Description | Sample Prompt |
|------|--------------|----------------|
| `performance_start_trace` | Start a raw CDP performance trace recording on the active page | "Record a performance trace of this page load" |
| `performance_stop_trace` | Stop the active trace (only needed when `autoStop: false` was used) | "Stop the performance trace and save it to disk" |

## Development

```bash
cd packages/app-bridge
yarn test            # Run tests
yarn test:coverage    # Run tests with coverage (90% statements/branches, 81% functions, 90% lines)
yarn build            # Stage src/ into dist/
```
