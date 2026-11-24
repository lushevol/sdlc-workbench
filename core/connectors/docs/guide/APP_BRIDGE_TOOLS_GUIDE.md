# App Bridge Tools Guide

Complete usage guide for all 48 browser automation tools in the SC Node MCP Server's `@sc-node-mcp/app-bridge` package.

> **Prerequisites:** Google Chrome and/or Microsoft Edge installed. A matching `chromedriver`/`msedgedriver` executable downloaded locally and configured via `--chromedriver-path`/`--edgedriver-path` CLI flags (or `CHROMEDRIVER_PATH`/`EDGEDRIVER_PATH` env vars) — drivers are **never** auto-downloaded. Standalone package only — not part of `@sc-node-mcp/unified`.

---

## Table of Contents

- [Test Environment Setup](#test-environment-setup)
- [The Locator Object](#the-locator-object)
- [Tool Reference](#tool-reference)
  - [Session & Navigation](#session--navigation)
  - [Element Location & Waiting](#element-location--waiting)
  - [Element Interaction & Forms](#element-interaction--forms)
  - [Mouse, Keyboard, Alerts & Cookies](#mouse-keyboard-alerts--cookies)
  - [Windows, Frames & Screenshots](#windows-frames--screenshots)
  - [Test Code Generation](#test-code-generation)
  - [Network Inspection](#network-inspection)
  - [Console Inspection](#console-inspection)
  - [Emulation](#emulation)
  - [Performance Tracing](#performance-tracing)
- [Common Workflows](#common-workflows)

---

## Test Environment Setup

Configure at least one driver path before starting the server:

```bash
# Via environment variables
export CHROMEDRIVER_PATH="/path/to/chromedriver"
export EDGEDRIVER_PATH="/path/to/msedgedriver"

# Via CLI flags
node packages/app-bridge/src/index.js \
  --chromedriver-path "/path/to/chromedriver" \
  --edgedriver-path "/path/to/msedgedriver"
```

Both are optional individually — configure only the browser(s) you use. `browser_start` returns a
clear error if you request a browser whose driver path was never configured.

---

## The Locator Object

Every tool that targets an element accepts the **same locator object shape**, used consistently
across all 38 tools:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `using` | string | Yes | One of: `id`, `css`, `xpath`, `name`, `className`, `tagName`, `linkText`, `partialLinkText`, `relative` |
| `value` | string | Yes | Locator value. For `relative`, the base tag name or CSS selector of the elements being searched for |
| `index` | number | No | 0-based index to disambiguate when the locator matches multiple elements (default: `0`) |
| `relativeStrategy` | string | No | `css` (default) or `tagName` — how to interpret `value` when `using` is `relative` |
| `relation` | string | Only when `using: "relative"` | One of: `above`, `below`, `toLeftOf`, `toRightOf`, `straightAbove`, `straightBelow`, `straightToLeftOf`, `straightToRightOf`, `near` |
| `anchor` | object | Only when `using: "relative"` | A simple (non-relative) locator: `{ using, value }` |

**Simple locator example:**
```json
{ "using": "css", "value": "button[type=submit]" }
```

**Relative locator example** (find a text input below the "Email" label):
```json
{
  "using": "relative",
  "value": "input",
  "relation": "below",
  "anchor": { "using": "xpath", "value": "//label[text()='Email']" }
}
```

---

## Tool Reference

### Session & Navigation

#### 1. `browser_start`

Launch a new Chrome or Edge browser session, replacing any existing session. Visible (headed) by default.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `browser` | string | ✅ Yes | — | `chrome` or `edge` |
| `headless` | boolean | ⚠️ Optional | `false` | Run without a visible window |
| `windowWidth` | number | ⚠️ Optional | `1280` | Initial window width in pixels |
| `windowHeight` | number | ⚠️ Optional | `800` | Initial window height in pixels |
| `extraArgs` | string[] | ⚠️ Optional | `[]` | Additional raw Chrome/Edge command-line switches |

**Test Query:** `Start a visible Chrome browser`

**JSON Invocation:** `{ "browser": "chrome", "headless": false }`

#### 2. `browser_close`

Close the active browser session, if any. No parameters.

**Test Query:** `Close the browser`

#### 3. `browser_set_timeouts`

Set implicit wait, page load, and script execution timeouts for the active session.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `implicitMs` | number | ⚠️ Optional | Implicit element-find wait, in ms |
| `pageLoadMs` | number | ⚠️ Optional | Page load timeout, in ms |
| `scriptMs` | number | ⚠️ Optional | Script execution timeout, in ms |

**Test Query:** `Set a 15 second implicit wait`

**JSON Invocation:** `{ "implicitMs": 15000 }`

#### 4. `browser_navigate`

Navigate the active browser session to a URL.

**Parameters:** `url` (string, required)

**Test Query:** `Go to https://example.com`

#### 5. `browser_navigate_back` / 6. `browser_navigate_forward` / 7. `browser_refresh`

No parameters. Go back/forward in history, or reload the current page.

#### 8. `browser_get_page_info`

Get the current URL and page title. No parameters.

#### 9. `browser_get_page_source`

Get the full HTML source of the current page (truncated to 15,000 characters). No parameters.

#### 10. `browser_wait_for_text`

Wait for any of the given text strings to appear anywhere on the page. Unlike `element_wait_for`,
this is not scoped to a single element/locator — it checks the whole page body text.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string[] | ✅ Yes | — | Non-empty list of text values. Resolves as soon as any one appears on the page. |
| `timeout` | number | ⚠️ Optional | `10000` | Max wait time in ms |

**Test Query:** `Wait for the text "Order confirmed" to appear`

**JSON Invocation:** `{ "text": ["Order confirmed"] }`

---

### Element Location & Waiting

#### 1. `element_find`

Find one element matching a locator (supports relative locators). Returns a summary
(`tag`, `text`, `id`, `class`) of the resolved match plus the total match count. By default also
outlines the matched element in the browser (`2px solid red`) for visual confirmation.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `locator` | object | ✅ Yes | See [The Locator Object](#the-locator-object) |
| `highlight` | boolean | ⚠️ Optional | Outline the matched element (`2px solid red`) for visual confirmation (default: `true`). Best-effort — a failed highlight never fails the tool call; check the returned `highlighted` field to confirm it was applied. |

**Test Query:** `Find the Submit button`

**JSON Invocation:** `{ "locator": { "using": "css", "value": "button[type=submit]" } }`

#### 2. `element_find_all`

Find all elements matching a locator. Returns up to 50 element summaries for disambiguation
(use the array index with other tools' `locator.index`).

**Test Query:** `List all links on the page`

**JSON Invocation:** `{ "locator": { "using": "tagName", "value": "a" } }`

#### 3. `element_wait_for`

Wait until an element reaches a condition.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `locator` | object | ✅ Yes | — |
| `condition` | string | ✅ Yes | `present`, `visible`, `invisible`, `clickable`, or `text_contains` |
| `text` | string | Only for `text_contains` | Text the element must contain |
| `timeoutMs` | number | ⚠️ Optional | Max wait in ms (default `10000`) |

**Test Query:** `Wait until the loading spinner disappears`

**JSON Invocation:** `{ "locator": { "using": "css", "value": ".spinner" }, "condition": "invisible" }`

---

### Element Interaction & Forms

#### 1. `element_click`

Click an element matching a locator.

#### 2. `element_send_keys`

Type text into an element. Clears the field first by default.

**Parameters:** `locator` (required), `text` (string, required), `clearFirst` (boolean, optional, default `true`)

#### 3. `element_clear`

Clear the value of an input/textarea element.

#### 4. `element_get_text` / 5. `element_get_attribute` / 6. `element_get_css_value`

Read the visible text, an attribute/property (`attribute` param), or a computed CSS property (`property` param).

#### 7. `element_get_rect`

Get `{ x, y, width, height }` for an element.

#### 8. `element_get_state`

Get `{ displayed, enabled, selected }` booleans for an element.

#### 9. `element_upload_file`

Send an absolute file path to a `<input type="file">` element via `filePath` param.

#### 10. `select_get_options`

List `<select>` options with `{ text, value, selected }` for each.

#### 11. `select_option`

Select/deselect/deselect-all options of a `<select>` element.

**Parameters:** `locator` (required), `action` (`select` | `deselect` | `deselect_all`, default `select`), `by` (`value` | `label` | `index`), `value` (string)

**Test Query:** `Select "United Kingdom" from the country dropdown`

**JSON Invocation:** `{ "locator": { "using": "id", "value": "country" }, "by": "label", "value": "United Kingdom" }`

#### 12. `script_execute`

Execute JavaScript in the browser (sync or async).

**Parameters:** `script` (string, required), `args` (array, optional), `async` (boolean, optional, default `false`)

**Test Query:** `Scroll to the bottom of the page`

**JSON Invocation:** `{ "script": "window.scrollTo(0, document.body.scrollHeight);", "args": [] }`

---

### Mouse, Keyboard, Alerts & Cookies

#### 1. `mouse_hover` / 2. `mouse_double_click` / 3. `mouse_right_click`

Hover, double-click, or right-click an element via `locator`.

#### 4. `mouse_drag_and_drop`

Drag `sourceLocator` and drop onto `targetLocator`.

#### 5. `keyboard_press_key`

Send a special key (`ENTER`, `TAB`, `ESCAPE`, `ARROW_DOWN`, etc. — any `selenium-webdriver` `Key`
enum name) or literal text, to a `locator` if given or the currently focused element.

**Test Query:** `Press Enter to submit the search`

**JSON Invocation:** `{ "key": "ENTER" }`

#### 6. `alert_handle`

Accept, dismiss, read, or type into the current alert/confirm/prompt dialog.

**Parameters:** `action` (`accept` | `dismiss` | `get_text` | `send_text`, required), `text` (required for `send_text`), `timeoutMs` (optional, default `5000`)

#### 7. `cookie_add` / 8. `cookie_get` / 9. `cookie_delete`

Add, read (all or by `name`), or delete (all or by `name`) cookies for the current domain.

---

### Windows, Frames & Screenshots

#### 1. `window_manage`

Manage browser windows/tabs.

**Parameters:** `action` (`list` | `switch` | `open` | `close` | `resize`, required), `handle` (required for `switch`), `type` (`tab` | `window`, for `open`, default `tab`), `width`/`height`/`maximize` (for `resize`)

#### 2. `frame_manage`

Switch focus between frames.

**Parameters:** `action` (`switch` | `default` | `parent`, required), `locator` or `index` (for `switch`)

#### 3. `screenshot_capture`

Take a screenshot of the viewport (default) or a single element (when `locator` is given). Returns
the image inline as an MCP `image` content block; optionally also saves it to disk via `outputPath`.

**Test Query:** `Take a screenshot of the page`

**JSON Invocation:** `{ "outputPath": "C:\\temp\\screenshot.png" }`

---

### Test Code Generation

#### 1. `element_scan_page`

Scan the entire current page for interactive elements (links, buttons, inputs, selects, textareas,
and elements with `role=button`/`onclick`/`contenteditable`/`tabindex`) and suggest candidate
locators for each — independent of any specific locator query. Runs a script in the page via
`executeScript`, no extra dependency needed. Useful for discovering real, working locators before
writing automation code, or as a broader alternative to `element_find_all` when you don't already
know what to search for. By default also outlines the first 10 returned elements in the browser
(`2px solid red`) for visual confirmation.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `maxElements` | number | ⚠️ Optional | `50` | Max number of elements to return |
| `highlight` | boolean | ⚠️ Optional | `true` | Outline up to the first 10 returned elements (`2px solid red`) for visual confirmation. Best-effort — a failed highlight never fails the tool call; check the returned `highlightedCount` field to confirm how many were applied. |

**Test Query:** `Scan the page and show me all the interactive elements with their locators`

**JSON Invocation:** `{ "maxElements": 25 }`

#### 2. `codegen_generate_test`

Generate raw Selenium test code (including working locators) for a natural-language test scenario.
This tool does **not** execute anything itself and does not track a session history — it returns a
workflow of instructions telling the LLM to drive the real browser tools for each step first (so
accurate locators/results naturally appear in the conversation), and only afterward author a bare,
sequential Selenium script (no `describe`/`it`, no `@Test`, no pytest fixtures) from what actually
happened. This mirrors how `appium/appium-mcp`'s `appium_generate_tests` tool works.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `steps` | string[] | ✅ Yes | — | Natural-language steps describing the test scenario, in order |
| `language` | string | ⚠️ Optional | `javascript` | Target Selenium language binding: `javascript`, `java`, `python`, or `csharp` |

**Test Query:** `Generate a Selenium test in Python for: open the login page, type "admin" into the username field, click Submit`

**JSON Invocation:**
```json
{
  "steps": ["Open the login page", "Type \"admin\" into the username field", "Click the Submit button"],
  "language": "python"
}
```

---

### Network Inspection

Implemented via Chrome DevTools Protocol (`selenium-webdriver`'s own `driver.createCDPConnection()`
support — no new dependency). Capture starts lazily the first time any of these tools is called
(not at `browser_start`) and accumulates into a **single running buffer for the whole session** —
it is **not** reset on navigation. Use `network_clear_requests` to reset manually.

#### 1. `network_list_requests`

List network requests captured since capture started (or since last cleared).

**Parameters:** `resourceTypes` (string[], optional — e.g. `"Document"`, `"XHR"`, `"Fetch"`, `"Script"`, `"Image"`), `pageIdx` (number, optional, default `0`), `pageSize` (number, optional — omit for all)

**Test Query:** `List all XHR requests made by the page`

**JSON Invocation:** `{ "resourceTypes": ["XHR"] }`

#### 2. `network_get_request`

Get full detail (headers, status, request/response bodies) for one request by `reqid` from
`network_list_requests`.

**Parameters:** `reqid` (number, required), `requestFilePath` / `responseFilePath` (string, optional — save the body to disk instead of inlining it)

**Test Query:** `Show me the response body of request 3`

**JSON Invocation:** `{ "reqid": 3 }`

#### 3. `network_clear_requests`

Manually clear the captured network requests buffer. No parameters.

---

### Console Inspection

Implemented the same way as Network Inspection above — CDP-based, lazy-started, single running
buffer for the whole session (not reset per navigation). Use `console_clear_messages` to reset
manually.

#### 1. `console_list_messages`

List console messages (`console.*` API calls and browser Log entries) captured since capture
started (or since last cleared).

**Parameters:** `types` (string[], optional — e.g. `"log"`, `"warning"`, `"error"`, `"info"`, `"debug"`), `pageIdx` (number, optional, default `0`), `pageSize` (number, optional — omit for all)

**Test Query:** `Show me any console errors`

**JSON Invocation:** `{ "types": ["error"] }`

#### 2. `console_get_message`

Get full detail (including stack trace, when available) for one message by `msgid` from
`console_list_messages`.

**Parameters:** `msgid` (number, required)

#### 3. `console_clear_messages`

Manually clear the captured console messages buffer. No parameters.

---

### Emulation

#### 1. `browser_emulate`

Consolidated device/network/environment emulation via CDP. Each parameter is applied
independently — omit a parameter to leave that setting unchanged; pass its documented "clear"
value to reset it to default.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `colorScheme` | string | ⚠️ Optional | `dark`, `light`, or `auto` (clears the override) |
| `cpuThrottlingRate` | number | ⚠️ Optional | CPU slowdown factor; `1` disables throttling |
| `networkConditions` | string | ⚠️ Optional | `Online` (disables throttling), `Offline`, `Slow 3G`, `Fast 3G`, `Slow 4G`, `Fast 4G` (approximate presets) |
| `geolocation` | string | ⚠️ Optional | `"<latitude>,<longitude>"`; empty string clears the override |
| `userAgent` | string | ⚠️ Optional | User agent to emulate; empty string resets to the browser's real user agent |
| `extraHttpHeaders` | string | ⚠️ Optional | Extra HTTP headers as a JSON object string; empty string clears all extra headers |
| `viewport` | string | ⚠️ Optional | `"<width>x<height>x<devicePixelRatio>[,mobile][,touch][,landscape]"` |

**Test Query:** `Emulate a mobile device in dark mode with Slow 3G network`

**JSON Invocation:** `{ "colorScheme": "dark", "networkConditions": "Slow 3G", "viewport": "375x667x2,mobile,touch" }`

---

### Performance Tracing

Raw CDP `Tracing.start`/`Tracing.end` capture, implemented without any new dependency. Returns
basic, self-computed stats only (event count, duration, category counts) — **not** Core Web
Vitals/LCP/CLS "Insights" analysis (that requires bundling Chrome DevTools' own internal
trace-processing engine, deliberately out of scope; see `performance_stop_trace`'s output for the
raw trace data instead, or open it in `chrome://tracing` / DevTools' own Performance panel).

#### 1. `performance_start_trace`

Start a raw CDP performance trace recording on the active page.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `reload` | boolean | ⚠️ Optional | `true` | Navigate to `about:blank` then back to the current URL around starting the trace, to clear prior state |
| `autoStop` | boolean | ⚠️ Optional | `true` | Automatically stop the trace a few seconds after (re)load |
| `filePath` | string | ⚠️ Optional | — | Save the raw trace JSON to this path (`.json` or `.json.gz`) |

**Test Query:** `Record a performance trace of this page load`

**JSON Invocation:** `{ "reload": true, "autoStop": true }`

#### 2. `performance_stop_trace`

Stop the active trace started by `performance_start_trace` (only needed when `autoStop: false`
was used).

**Parameters:** `filePath` (string, optional — save the raw trace JSON to this path)

---

## Common Workflows

**Open a page and confirm what loaded:**
1. `browser_start` (`{ "browser": "chrome" }`)
2. `browser_navigate` (`{ "url": "https://example.com" }`)
3. `browser_get_page_info` to confirm the title/URL
4. `screenshot_capture` to see the result

**Fill in and submit a form:**
1. `element_find_all` to locate each field and disambiguate by index if needed
2. `element_send_keys` for text inputs, `select_option` for dropdowns
3. `element_click` on the submit button
4. `element_wait_for` (`condition: "visible"`) on a post-submit success element

**Find an element relative to another (Selenium 4 relative locators):**
1. `element_find` with a `relative` locator anchored to a known element (e.g. a label) to confirm
   the match before acting on it
2. `element_click` / `element_send_keys` with the same relative locator once confirmed

**Generate a raw Selenium test script from a scenario:**
1. `codegen_generate_test` with your `steps` and desired `language` — returns instructions, not code
2. Follow those instructions: perform each step for real with `browser_start`, `browser_navigate`,
   `element_find`/`element_find_all` (or `element_scan_page` for a broader locator snapshot),
   `element_click`/`element_send_keys`/etc., and `element_wait_for` instead of fixed sleeps
3. Once every step has actually been run, write the bare sequential script based on what happened
   in this conversation (accurate locators included) — no test-framework wrapper

**Debug a page load (network, console, and a raw performance trace):**
1. `browser_navigate` to the target URL
2. `network_list_requests` to see what loaded (filter by `resourceTypes` if needed);
   `network_get_request` for the full detail of a specific request
3. `console_list_messages` (filter `types: ["error"]`) to check for JS errors
4. `performance_start_trace` (`{ "reload": true, "autoStop": true }`) for a raw trace of the load
