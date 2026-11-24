# MCP Tools Reference

All tools below are available in the `@sc-node-mcp/unified` package. For a lighter footprint, each tool group is also available as a standalone package — see [CONSUMER_GUIDE.md](../CONSUMER_GUIDE.md#modular-install-individual-packages).

> **Note:** Confluence, SC Wiki, Nexus IQ, and SonarQube tools only register when their credentials are provided at startup. The maximum available tool count is **129** (all credentials supplied). ADO, Messaging, Context, and Upload App tools always register. Web tools are available as a standalone experimental package (`@sc-node-mcp/web`) and are **not** included in unified. Browser automation tools are available as a standalone package (`@sc-node-mcp/app-bridge`) and are also **not** included in unified.

## Package → Tool Group Mapping

| Package | Tool Group | Tools |
|---------|-----------|-------|
| `@sc-node-mcp/unified` | All tools | 129 tools (max) |
| `@sc-node-mcp/web` | Web Search & Fetch (standalone, experimental) | `web_search`, `web_fetch`, `web_crawl`, `web_crawl_browser` |
| `@sc-node-mcp/app-bridge` | Browser Automation via Selenium WebDriver (standalone) | 48 tools — see [Browser Automation Tools](#browser-automation-tools-app-bridge) below |
| `@sc-node-mcp/ado` | All ADO tools | 86 tools |
| `@sc-node-mcp/ado-workitems-read` | Work Items (read) | `wit_list_projects`, `wit_get_work_item`, `wit_my_work_items`, `wit_list_backlogs`, `wit_list_backlog_work_items`, `wit_get_work_items_batch_by_ids`, `wit_get_work_items_for_iteration`, `wit_get_work_item_type`, `wit_get_query`, `wit_get_query_results_by_id`, `wit_query_by_url`, `wit_get_dashboard_work_items`, `wit_get_work_item_links`, `wit_list_teams`, `wit_list_iterations`, `wit_list_work_item_comments`, `wit_list_work_item_pull_requests`, `wit_list_work_item_commits`, `wit_list_work_item_revisions`, `wit_get_work_item_attachment` |
| `@sc-node-mcp/ado-workitems-write` | Work Items (write) | `wit_create_work_item`, `wit_update_work_item`, `wit_update_work_items_batch`, `wit_add_work_item_comment`, `wit_update_work_item_comment`, `wit_add_child_work_items`, `wit_work_items_link`, `wit_work_item_unlink`, `wit_link_work_item_to_pull_request` |
| `@sc-node-mcp/ado-repos-read` | Repositories (read) | `repo_list_repos_by_project`, `repo_get_repo_by_name_or_id`, `repo_list_branches_by_repo`, `repo_list_my_branches_by_repo`, `repo_get_branch_by_name`, `repo_get_file_content`, `repo_list_directory`, `repo_search_commits`, `repo_list_pull_requests_by_repo_or_project`, `repo_get_pull_request_by_id`, `repo_list_pull_request_threads`, `repo_get_pull_request_changes` |
| `@sc-node-mcp/ado-repos-write` | Repositories (write) | `repo_create_branch`, `repo_create_pull_request`, `repo_update_pull_request`, `repo_update_pull_request_reviewers`, `repo_vote_pull_request`, `repo_update_pull_request_thread`, `repo_reply_to_comment`, `repo_create_pull_request_thread`, `core_get_identity_ids` |
| `@sc-node-mcp/ado-pipelines` | Pipelines | All `pipelines_*` tools (14) |
| `@sc-node-mcp/ado-review` | PR Review | `repo_review_pr`, `repo_pr_diff`, `post_pr_comment`, `delete_all_pr_review_comments` |
| `@sc-node-mcp/ado-sprints` | Sprint & Capacity | All `work_*` tools (8) |
| `@sc-node-mcp/ado-testplans` | Test Plans | All `testplan_*` tools (9) |
| `@sc-node-mcp/ado-search` | Search | `search_code`, `search_workitem` |
| `@sc-node-mcp/confluence` | Confluence | All `confluence_*` tools (15) |
| `@sc-node-mcp/scwiki` | SC Wiki (XWiki) | All `scwiki_*` tools (14) |
| `@sc-node-mcp/messaging` | Messaging | `email_send`, `teams_send_message` |
| `@sc-node-mcp/nexus` | Nexus IQ | `nexus_scan_vulnerabilities`, `nexus_fix_vulnerabilities` |
| `@sc-node-mcp/sonar` | SonarQube | All `sonar_*` tools (6) |
| `@sc-node-mcp/ado-upload-app` | ADO Upload | `wit_upload_attachment_ui`, `wit_upload_attachment` |

---

## Web Search Tools

> **Requires Python 3.x** on `PATH` for `web_search`. `web_fetch` and `web_crawl` use Node.js directly. `web_crawl_browser` requires **Google Chrome or Microsoft Edge** installed on the system.

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|-------------- |
| 1 | web_search | Search the web using DuckDuckGo Lite (no API key required). Uses a Python subprocess bridge to bypass TLS fingerprinting. Returns up to 10 results with title, URL, and snippet. | Search the web for the latest news on a topic | `/web-search query: <query>` | `{ "query": "site:python.org" }` |
| 2 | web_fetch | Fetch and read the plain-text content of a specific HTTPS URL. Use after web_search to read a result page in full (max 15,000 chars returned). | Fetch and summarise the content of a URL | `/web-fetch url: <url>` | `{ "url": "https://docs.python.org/3/" }` |
| 3 | web_crawl | Crawl a website from a seed URL, following links within the same domain (BFS). Returns results in one of four modes: `urls` (URL list only), `summary` (URL + title + 500-char snippet), `full` (URL + title + full text), `links` (URL + outbound link graph). Configurable depth, page count, and request delay. | Crawl a website and discover all pages | `/web-crawl url: <url>` | `{ "url": "https://example.com", "mode": "summary", "maxDepth": 2, "maxPages": 20 }` |
| 4 | web_crawl_browser | Crawl a JavaScript-rendered (SPA) website using the system Chrome or Edge browser. Works on React/Angular/Vue sites that `web_crawl` cannot handle. Same four output modes as `web_crawl`. Requires Chrome or Edge installed. | Crawl a React SPA and summarise its pages | `/web-crawl-browser url: <url>` | `{ "url": "https://spa.example.com", "mode": "summary", "maxDepth": 2, "maxPages": 10 }` |

---

## Browser Automation Tools (app-bridge)

> **Standalone-only** — `@sc-node-mcp/app-bridge` is not included in `unified` (same precedent as `@sc-node-mcp/web`). **Requires** Google Chrome and/or Microsoft Edge installed, plus a matching `chromedriver`/`msedgedriver` executable configured via `--chromedriver-path`/`--edgedriver-path` CLI flags or `CHROMEDRIVER_PATH`/`EDGEDRIVER_PATH` env vars (drivers are never auto-downloaded). See [docs/guide/APP_BRIDGE_TOOLS_GUIDE.md](guide/APP_BRIDGE_TOOLS_GUIDE.md) for full parameter details and [CONSUMER_GUIDE.md](../CONSUMER_GUIDE.md#browser-automation-app-bridge) for setup. Only 3 guided prompts are registered (`open-and-screenshot`, `find-and-click`, `fill-a-form`) rather than one per tool, given the size of this tool set — most tools have no dedicated slash command.

### Session & Navigation

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | browser_start | Launch a new Chrome or Edge browser session, replacing any existing session. Visible (headed) by default. | Start a visible Chrome browser session | `/open-and-screenshot url: <url> browser: <chrome\|edge>` | `{ "browser": "chrome", "headless": false, "windowWidth": 1280, "windowHeight": 800 }` |
| 2 | browser_close | Close the active browser session, if any. | Close the browser session | — | `{}` |
| 3 | browser_set_timeouts | Set implicit wait, page load, and script execution timeouts for the active session. | Set a 15 second implicit wait | — | `{ "implicitMs": 15000 }` |
| 4 | browser_navigate | Navigate the active browser session to a URL. | Navigate to a URL | `/open-and-screenshot url: <url>` | `{ "url": "https://example.com" }` |
| 5 | browser_navigate_back | Go back one entry in the browser history. | Go back | — | `{}` |
| 6 | browser_navigate_forward | Go forward one entry in the browser history. | Go forward | — | `{}` |
| 7 | browser_refresh | Reload the current page. | Refresh the page | — | `{}` |
| 8 | browser_get_page_info | Get the current URL and page title. | Get the current page title and URL | — | `{}` |
| 9 | browser_get_page_source | Get the full HTML source of the current page (truncated to 15,000 characters). | Get the page HTML source | — | `{}` |
| 10 | browser_wait_for_text | Wait for any of the given text strings to appear anywhere on the page (not scoped to a single element/locator). | Wait for the text "Order confirmed" to appear | — | `{ "text": ["Order confirmed"] }` |

### Element Location & Waiting

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | element_find | Find one element matching a locator (supports all Selenium locator strategies plus relative locators). Returns a summary and the total match count. By default also outlines the matched element (`2px solid red`, best-effort) for visual confirmation — set `highlight: false` to skip. | Find the Submit button | `/find-and-click description: <description>` | `{ "locator": { "using": "css", "value": "button[type=submit]" } }` |
| 2 | element_find_all | Find all elements matching a locator. Returns up to 50 element summaries for disambiguation. | List all links on the page | — | `{ "locator": { "using": "tagName", "value": "a" } }` |
| 3 | element_wait_for | Wait until an element reaches a condition: present, visible, invisible, clickable, or text_contains. | Wait until the loading spinner disappears | — | `{ "locator": { "using": "css", "value": ".spinner" }, "condition": "invisible", "timeoutMs": 10000 }` |

### Element Interaction & Forms

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | element_click | Click an element matching a locator. | Click the Submit button | `/find-and-click description: <description>` | `{ "locator": { "using": "id", "value": "submit-btn" } }` |
| 2 | element_send_keys | Type text into an element matching a locator (clears the field first by default). | Type "hello world" into the search box | `/fill-a-form fields: <fields>` | `{ "locator": { "using": "name", "value": "q" }, "text": "hello world" }` |
| 3 | element_clear | Clear the value of an input or textarea element. | Clear the search box | — | `{ "locator": { "using": "name", "value": "q" } }` |
| 4 | element_get_text | Get the visible text of an element. | Get the text of the page heading | — | `{ "locator": { "using": "css", "value": "h1" } }` |
| 5 | element_get_attribute | Get an attribute or property value from an element (e.g. href, value, class). | Get the href of the first link | — | `{ "locator": { "using": "tagName", "value": "a" }, "attribute": "href" }` |
| 6 | element_get_css_value | Get a computed CSS property value from an element. | Get the background color of the header | — | `{ "locator": { "using": "css", "value": "header" }, "property": "background-color" }` |
| 7 | element_get_rect | Get the location and size of an element. | Get the bounding box of the logo | — | `{ "locator": { "using": "id", "value": "logo" } }` |
| 8 | element_get_state | Get whether an element is displayed, enabled, and selected. | Check if the submit button is enabled | — | `{ "locator": { "using": "id", "value": "submit-btn" } }` |
| 9 | element_upload_file | Upload a file by sending its absolute path to a file input element. | Upload a file to the file input | — | `{ "locator": { "using": "css", "value": "input[type=file]" }, "filePath": "C:\\\\temp\\\\report.pdf" }` |
| 10 | select_get_options | List the options of a `<select>` element, including which are currently selected. | List the options of the country dropdown | — | `{ "locator": { "using": "id", "value": "country" } }` |
| 11 | select_option | Select, deselect, or deselect-all options of a `<select>` element by value, label, or index. | Select "United Kingdom" from the country dropdown | `/fill-a-form fields: <fields>` | `{ "locator": { "using": "id", "value": "country" }, "by": "label", "value": "United Kingdom" }` |
| 12 | script_execute | Execute JavaScript in the browser (sync or async), for advanced interactions not covered by other tools. | Scroll to the bottom of the page | — | `{ "script": "window.scrollTo(0, document.body.scrollHeight);", "args": [] }` |

### Mouse, Keyboard, Alerts & Cookies

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | mouse_hover | Move the mouse over an element (hover). | Hover over the dropdown menu | — | `{ "locator": { "using": "id", "value": "menu" } }` |
| 2 | mouse_double_click | Double-click an element. | Double-click the file icon | — | `{ "locator": { "using": "css", "value": ".file-icon" } }` |
| 3 | mouse_right_click | Right-click (context-click) an element. | Right-click the image | — | `{ "locator": { "using": "tagName", "value": "img" } }` |
| 4 | mouse_drag_and_drop | Drag an element and drop it onto another element. | Drag the task card into the "Done" column | — | `{ "sourceLocator": { "using": "id", "value": "task-1" }, "targetLocator": { "using": "id", "value": "done-column" } }` |
| 5 | keyboard_press_key | Send a keyboard key (special key name or literal text) to an element or the focused element. | Press Enter to submit the search | — | `{ "key": "ENTER" }` |
| 6 | alert_handle | Accept, dismiss, read, or type into the current alert/confirm/prompt dialog. | Accept the confirmation dialog | — | `{ "action": "accept" }` |
| 7 | cookie_add | Add a cookie for the current domain. | Add a session cookie | — | `{ "name": "session", "value": "abc123" }` |
| 8 | cookie_get | Get all cookies, or a specific one by name. | Get all cookies | — | `{}` |
| 9 | cookie_delete | Delete all cookies, or a specific one by name. | Delete the session cookie | — | `{ "name": "session" }` |

### Windows, Frames & Screenshots

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | window_manage | List, switch, open, close, or resize/maximize browser windows and tabs. | List all open tabs | — | `{ "action": "list" }` |
| 2 | frame_manage | Switch into a frame by locator/index, or reset to default content or the parent frame. | Switch into the payment iframe | — | `{ "action": "switch", "locator": { "using": "id", "value": "payment-frame" } }` |
| 3 | screenshot_capture | Take a screenshot of the viewport or a single element, returned inline as an image (optionally also saved to disk). | Take a screenshot of the page | `/open-and-screenshot url: <url>` | `{ "outputPath": "C:\\\\temp\\\\screenshot.png" }` |

### Test Code Generation

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | element_scan_page | Scan the entire current page for interactive elements and suggest candidate locators for each, independent of any specific locator query. By default also outlines the first 10 returned elements (`2px solid red`, best-effort) — set `highlight: false` to skip. | Scan the page and show me all the interactive elements with their locators | — | `{ "maxElements": 25 }` |
| 2 | codegen_generate_test | Generate raw Selenium test code (including working locators) for a natural-language scenario. Returns instructions to drive the real tools step-by-step first, then author a bare script from what happened — does not execute anything itself. | Generate a Selenium test in Python for: open the login page, type "admin" into the username field, click Submit | — | `{ "steps": ["Open the login page", "Click the Submit button"], "language": "python" }` |

### Network Inspection

> Implemented via Chrome DevTools Protocol (`selenium-webdriver`'s own `driver.createCDPConnection()` support — no new dependency). Capture starts lazily on first use (not at `browser_start`) and accumulates into a single running buffer for the whole session, not reset per navigation; use `network_clear_requests` to reset manually.

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | network_list_requests | List network requests captured since capture started (or since last cleared), optionally filtered by resource type. | List all XHR requests made by the page | — | `{ "resourceTypes": ["XHR"] }` |
| 2 | network_get_request | Get full detail (headers, status, request/response bodies) for one request by reqid. | Show me the response body of request 3 | — | `{ "reqid": 3 }` |
| 3 | network_clear_requests | Manually clear the captured network requests buffer. | Clear the captured network requests | — | `{}` |

### Console Inspection

> Same CDP-based, lazy-started, single-running-buffer design as Network Inspection above. Use `console_clear_messages` to reset manually.

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | console_list_messages | List console messages (console.* API calls and browser Log entries) captured since capture started, optionally filtered by type. | Show me any console errors | — | `{ "types": ["error"] }` |
| 2 | console_get_message | Get full detail (including stack trace, when available) for one message by msgid. | Get the stack trace for console message 5 | — | `{ "msgid": 5 }` |
| 3 | console_clear_messages | Manually clear the captured console messages buffer. | Clear the captured console messages | — | `{}` |

### Emulation

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | browser_emulate | Consolidated device/network/environment emulation via CDP (color scheme, CPU/network throttling, geolocation, user agent, extra HTTP headers, viewport). Each parameter is applied independently. | Emulate a mobile device in dark mode with Slow 3G network | — | `{ "colorScheme": "dark", "networkConditions": "Slow 3G", "viewport": "375x667x2,mobile,touch" }` |

### Performance Tracing

> Raw CDP `Tracing.start`/`Tracing.end` capture, no new dependency. Returns basic self-computed stats only (event count, duration, category counts) — not Core Web Vitals/LCP/CLS "Insights" analysis (would require bundling Chrome DevTools' own internal trace-processing engine; deliberately out of scope).

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | performance_start_trace | Start a raw CDP performance trace recording on the active page. | Record a performance trace of this page load | — | `{ "reload": true, "autoStop": true }` |
| 2 | performance_stop_trace | Stop the active trace started by performance_start_trace (only needed when autoStop: false was used). | Stop the running performance trace | — | `{}` |

---

## Messaging Tools

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | email_send | Send an email via Outlook automation. Works on macOS and Windows using your logged-in Outlook session. Supports To, CC, BCC recipients and HTML/plain text body. No SMTP configuration needed. | Send an email via Outlook with recipients, subject, and body | `/send-email to: <emails> subject: <subject> body: <body>` | `{ "to": ["john@example.com"], "cc": ["manager@example.com"], "subject": "Meeting Update", "body": "The meeting is rescheduled to 3 PM." }` |
| 2 | teams_send_message | Send a message to one or more people on Microsoft Teams using the installed Teams desktop app. Uses your logged-in Teams session — no webhook URL or API setup required. Supports direct messages (1 recipient) and group chats (multiple recipients). macOS requires Accessibility permission. | Send a direct message or group chat via Microsoft Teams using the native Teams desktop app (no webhook required) | `/teams-send-message to: <emails> message: <message>` | `{ "to": ["john@example.com"], "message": "Call in 5 minutes", "title": "Reminder" }` |

## PR Review Tools

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | post_pr_comment | Post a comment on a PR line as a new thread or reply to an existing thread (when threadId is provided). All AI review comments are prefixed with `🤖 Co-pilot Assisted Review:`. | Post a review comment or reply on a pull request | `/post-pr-comment prUrl: <url> filePath: <path> line: <n> comment: <text>` | `{ "prUrl": "https://dev.azure.com/org/proj/_git/repo/pullrequest/123", "filePath": "src/index.js", "line": 42, "commentText": "Refactor suggestion", "threadId": 1 }` |
| 2 | repo_review_pr | Automated PR review. Clones repo, diffs source vs target branch, loads review guidelines from the file path set in `CODE_REVIEW_GUIDE_FILE` (all file types), and the AI posts comments directly on changed lines via `post_pr_comment`. | Review a pull request with automated code quality checks | `/review-pr prUrl: <url>` | `{ "prUrl": "https://dev.azure.com/org/proj/_git/repo/pullrequest/123" }` |
| 3 | repo_pr_diff | Get the full diff of a pull request by cloning and comparing branches. | Analyze PR changes and suggest improvements | `/analyze-pr-diff prUrl: <url>` | `{ "prUrl": "https://dev.azure.com/org/proj/_git/repo/pullrequest/123" }` |
| 4 | delete_all_pr_review_comments | Delete all AI-generated review comments (`🤖 Co-pilot Assisted Review:` prefix) from a PR. Useful for re-running reviews with updated guidelines. Manual comments are not affected. | Delete all AI-generated Co-pilot review comments from a pull request | `/delete-pr-review-comments prUrl: <url>` | `{ "prUrl": "https://dev.azure.com/org/proj/_git/repo/pullrequest/123" }` |

## Search

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | search_code | Search for code text across Azure DevOps repositories. Supports filtering by project, repository, branch, and file path. | Search for code text across Azure DevOps repositories | `/search-code searchText: <text>` | `{ "searchText": "getUser", "project": "YOUR_PROJECT", "repository": "MyRepo", "branch": "main", "top": 25 }` |
| 2 | search_workitem | Search Azure DevOps work items by free text with optional filters for project, type, state, and assignee. | Search Azure DevOps work items by free text with optional filters | `/search-work-item searchText: <text>` | `{ "searchText": "login bug", "project": "YOUR_PROJECT", "workItemType": "Bug", "assignedTo": "john@example.com", "top": 25 }` |

## Work Items

| S.No | Tool Name | Description | Prompt Example (Test Query) | MCP Prompt | JSON Example |
|------|-----------|-------------|-----------------------------|----------|--------------|
| 1 | wit_list_projects | List all projects in the Azure DevOps organization | List all projects in the Azure DevOps organization | `/list-all-projects` | `{}` |
| 2 | wit_get_work_item | Retrieve details of a specific Azure DevOps work item by its ID | Get full details of a single work item by ID | `/get-work-item id: <id>` | `{ "id": 12345 }` |
| 3 | wit_my_work_items | List work items assigned to the current user | Show all work items assigned to me | `/my-work` | `{ "top": 10 }` |
| 4 | wit_get_work_items_batch_by_ids | Get multiple work items by IDs | Get details of multiple work items by IDs | `/get-multiple-work-items workItemIds: <ids>` | `{ "ids": [12345, 12346, 12347] }` |
| 5 | wit_list_work_item_comments | List comments for a work item | View all comments on a work item | `/view-work-item-comments workItemId: <id>` | `{ "id": 12345 }` |
| 6 | wit_get_work_item_type | Get field definitions and metadata for a specific work item type (e.g., Bug, Task, User Story) in an Azure DevOps project. | Get the schema and field definitions for a work item type | `/get-work-item-type project: <project> type: <type>` | `{ "project": "YOUR_PROJECT", "type": "Task" }` |
| 7 | wit_list_backlogs | List all backlog levels (e.g., Epics, Features, Stories) available to a specific team in an Azure DevOps project. | List available backlog levels for a team to support sprint planning | `/sprint-planning project: <project> team: <team>` | `{ "project": "YOUR_PROJECT", "team": "Your Team" }` |
| 8 | wit_list_backlog_work_items | List all work items in a named team backlog level (identified by backlogId, e.g. 'Microsoft.RequirementCategory') in an Azure DevOps project. | View backlog items for a team | `/view-backlog project: <project> team: <team>` | `{ "backlogId": "Microsoft.RequirementCategory", "project": "YOUR_PROJECT", "team": "Your Team" }` |
| 9 | wit_list_teams | List all teams in an Azure DevOps project | List all teams in a project | `/list-project-teams project: <project>` | `{ "project": "YOUR_PROJECT" }` |
| 10 | wit_list_iterations | List all iterations for a project and team | List all iterations for a team | `/list-team-iterations project: <project> team: <team>` | `{ "project": "YOUR_PROJECT", "team": "Your Team" }` |
| 11 | wit_get_work_items_for_iteration | Get work items for a specific iteration | Find all work items in a specific iteration | `/find-work-items-by-iteration project: <project> team: <team> iteration: <path>` | `{ "iterationPath": "YOUR_PROJECT\\Your Team\\Your Sprint B", "project": "YOUR_PROJECT", "team": "Your Team" }` |
| 12 | wit_get_query | Get a work item query by ID | Get query metadata (name, WIQL, path) without executing it | `/get-query project: <project> queryId: <id>` | `{ "project": "YOUR_PROJECT", "queryId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }` |
| 13 | wit_get_query_results_by_id | Execute a query and get results by query ID | Execute a saved work item query by ID | `/run-work-item-query project: <project> queryId: <id>` | `{ "project": "YOUR_PROJECT", "queryId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }` |
| 14 | wit_list_work_item_pull_requests | List all pull requests linked to a work item | List all pull requests linked to a work item | `/list-work-item-pull-requests project: <project> workItemId: <id>` | `{ "id": 12345 }` |
| 15 | wit_list_work_item_commits | List all commits linked to a work item | List all commits associated with a work item | `/list-work-item-commits project: <project> workItemId: <id>` | `{ "id": 12345 }` |
| 16 | wit_add_work_item_comment | Add a comment to a work item | Add a comment to a work item | `/add-work-item-comment workItemId: <id> comment: <text>` | `{ "id": 12345, "text": "Testing comment from MCP" }` |
| 17 | wit_update_work_item | Update a work item by applying a JSON patch document (array of {op, path, value} operations) to the specified work item ID. | Update a field on a single work item | `/update-work-item id: <id> field: <field> value: <value>` | `{ "id": 12345, "patch": [{ "op": "add", "path": "/fields/System.Tags", "value": "MCP-Test" }] }` |
| 18 | wit_create_work_item | Create a new work item of a given type in an Azure DevOps project using a JSON patch document to set fields such as title, description, and area path. | Create a new work item (User Story, Bug, Task, Feature, or any type) | `/create-work-item project: <project> title: <title>` | `{ "project": "YOUR_PROJECT", "type": "Task", "patch": [{ "op": "add", "path": "/fields/System.Title", "value": "Test Task from MCP Tool" }, { "op": "add", "path": "/fields/System.Description", "value": "This is a test task created via MCP tool" }] }` |
| 19 | wit_add_child_work_items | Add child work items to a parent work item | Add child work items to a parent work item | `/add-child-items parentId: <id> childIds: <ids>` | `{ "parentId": 12025714, "childIds": [12025719] }` |
| 20 | wit_work_items_link | Create a link between two work items with a specified relation type | Create a relationship between work items | `/link-related-work-items sourceId: <id> targetId: <id>` | `{ "sourceId": 12025719, "targetId": 12025714, "linkType": "System.LinkTypes.Related" }` |
| 21 | wit_update_work_items_batch | Update multiple work items in batch | Update multiple work items in a single batch operation | `/update-multiple-work-items workItemIds: <ids> updateType: <type> value: <value>` | `{ "updates": [ { "id": 12025719, "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}] }, { "id": 12025714, "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}] } ] }` |
| 22 | wit_work_item_unlink | Remove one or more relation links from a work item by URL or all links of a given type. | Remove one or more relation links from a work item | `/unlink-work-item workItemId: <id> relationUrls: <urls>` | `{ "id": 12345, "relationUrls": ["https://dev.azure.com/sc-ado/.../_apis/wit/workItems/6789"] }` |
| 23 | wit_link_work_item_to_pull_request | Link a work item to a pull request as an artifact link. | Link a work item to a pull request as an artifact link | `/link-work-item-to-pr workItemId: <id> pullRequestId: <id> repositoryId: <repo> projectId: <project>` | `{ "workItemId": 12345, "pullRequestId": 99, "repositoryId": "MyRepo", "projectId": "YOUR_PROJECT" }` |
| 24 | wit_update_work_item_comment | Update the text of an existing comment on a work item. | Update the text of an existing comment on a work item | `/update-work-item-comment project: <project> workItemId: <id> commentId: <id> text: <text>` | `{ "project": "YOUR_PROJECT", "workItemId": 12345, "commentId": 5, "text": "Updated comment text" }` |
| 25 | wit_list_work_item_revisions | List all revision history for a work item. | List the full revision history of a work item | `/list-work-item-revisions workItemId: <id>` | `{ "project": "YOUR_PROJECT", "id": 12345, "top": 20 }` |
| 26 | wit_get_work_item_attachment | Download a work item attachment and return its content as base64. | Download a work item attachment and return its content as base64 | `/get-work-item-attachment project: <project> attachmentId: <guid>` | `{ "project": "YOUR_PROJECT", "attachmentId": "abc123-def456" }` |
| 27 | wit_upload_attachment_ui | Opens an interactive UI panel to upload one or more files to a work item as attachments. AI can pre-fill project and WI ID via optional args. Available in the `@sc-node-mcp/ado-upload-app` package. | Open the interactive file upload panel to attach files to an Azure DevOps work item | `/upload-attachment-ui` | `{ "project": "YOUR_PROJECT", "wiId": 12345 }` |
| 28 | wit_upload_attachment | Upload one or more base64-encoded files to a work item as AttachedFile relations. Called directly by the AI or from the UI via callServerTool. Available in the `@sc-node-mcp/ado-upload-app` package. | — | — | `{ "project": "YOUR_PROJECT", "wiId": 12345, "files": [{ "name": "screenshot.png", "base64": "<base64>" }] }` |
| 29 | wit_get_work_item_links | Get work items linked to a given work item, grouped by relation type (parent, child, related). | Get parent, child, and related work items linked to a work item | `/get-work-item-links id: <id>` | `{ "id": 12345 }` |
| 30 | wit_query_by_url | Get work items from a saved Azure DevOps query, given its URL or project+queryId. | Get work items from a saved query URL or project+queryId | `/query-by-url url: <url>` | `{ "url": "https://dev.azure.com/sc-ado/YOUR_PROJECT/_queries/query/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }` |
| 31 | wit_get_dashboard_work_items | Get work items from all query-backed widgets on an Azure DevOps dashboard, given its URL or project+dashboardId. | Get work items from query-backed widgets on a dashboard | `/get-dashboard-work-items url: <url>` | `{ "url": "https://dev.azure.com/sc-ado/YOUR_PROJECT/_dashboards/dashboard/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }` |

## Projects and Repositories

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | repo_list_repos_by_project | List all repositories in a given Azure DevOps project with optional filtering | List all repositories in a project | `/list-project-repositories project: <project>` | `{ "project": "MyProject", "repoNameFilter": "web", "skip": 0, "top": 10 }` |
| 2 | repo_get_repo_by_name_or_id | Get repository details by name or ID | Get detailed information about a repository | `/get-repository-details project: <project> repository: <name>` | `{ "project": "MyProject", "repositoryNameOrId": "RepoName" }` |
| 3 | repo_get_file_content | Get the content of a specific file from an Azure DevOps repository. | Get the content of a specific file from an Azure DevOps repository | `/get-file-content repository: <name> path: <path>` | `{ "repositoryId": "MyRepo", "path": "/src/index.js", "version": "main", "versionType": "branch" }` |
| 4 | repo_list_directory | List files and folders at a given path in a repository. | List files and folders at a given path in a repository | `/list-repo-directory repository: <name>` | `{ "repositoryId": "MyRepo", "path": "/src", "version": "main", "versionType": "branch", "recursive": false }` |

## Branches

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | repo_list_branches_by_repo | List all branches in a repository with optional filtering | List all branches in a repository | `/list-all-branches repository: <name>` | `{ "repositoryId": "MyRepo", "filterContains": "feature", "top": 20 }` |
| 2 | repo_list_my_branches_by_repo | List branches in a repository created by current user | List branches I created in a repository | `/list-my-branches repository: <name>` | `{ "repositoryId": "MyRepo", "filterContains": "", "top": 10 }` |
| 3 | repo_get_branch_by_name | Get branch details by name | Get detailed information about a specific branch | `/get-branch-details repository: <name> branchName: <branch>` | `{ "repositoryId": "MyRepo", "branchName": "main" }` |
| 4 | repo_create_branch | Create a new branch from a source branch or commit | Create a new feature or bugfix branch | `/create-branch repository: <name> branchName: <name> sourceBranch: <branch>` | `{ "repositoryId": "MyRepo", "branchName": "feature/new", "sourceBranchName": "main" }` |

## Pull Requests

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | repo_list_pull_requests_by_repo_or_project | List pull requests for a repository or project with comprehensive filters | Show all pull requests I created or need to review | `/my-prs` | `{ "repositoryId": "MyRepo", "status": "active", "i_am_reviewer": true, "top": 10 }` |
| 2 | repo_get_pull_request_by_id | Get pull request details by ID with optional work item refs | Get full details of a pull request by ID | `/get-pull-request repositoryId: <repo> pullRequestId: <id>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "includeWorkItemRefs": true }` |
| 3 | repo_create_pull_request | Create a new pull request from a source branch to a target branch in an Azure DevOps repository, with optional title, description, draft mode, labels, and linked work items. | Create a new pull request with description and reviewers | `/create-pr repository: <name> sourceBranch: <branch> targetBranch: <branch> title: <title>` | `{ "repositoryId": "MyRepo", "sourceRefName": "feature", "targetRefName": "main", "title": "New Feature", "description": "Feature description", "isDraft": false, "labels": ["enhancement"], "workItems": [123] }` |
| 4 | repo_update_pull_request | Update pull request properties including status, title, description, and completion options | Update pull request status, merge settings, or complete/abandon it | `/update-pull-request prUrl: <url> action: <action>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "status": "completed", "autoComplete": true, "deleteSourceBranch": true, "mergeStrategy": "squash" }` |
| 5 | repo_update_pull_request_reviewers | Add or remove reviewers from a pull request. Accepts employee IDs (converted to `ID@zone1.scb.net`), email addresses, or display names (fuzzy-matched via IdentityPicker, including "Surname, Firstname" order). | Add or remove reviewers on a pull request | `/manage-pr-reviewers prUrl: <url> action: <add|remove> reviewers: <emails; semicolon-separated>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "reviewerIdentifiers": ["user1-id", "user2-id"], "action": "add" }` |
| 6 | repo_get_pull_request_changes | Get all file changes in a pull request across all iterations. | Get all file changes in a pull request across all iterations | `/get-pr-file-changes repository: <name> pullRequestId: <id>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123 }` |
| 7 | repo_vote_pull_request | Cast a vote on a pull request (approve, approveWithSuggestions, waitForAuthor, reject, or reset). | Cast a vote on a pull request (approve, approveWithSuggestions, waitForAuthor, reject, or reset) | `/vote-pull-request repository: <name> pullRequestId: <id> vote: <vote>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "vote": "approve" }` |
| 8 | repo_update_pull_request_thread | Update the status of a PR comment thread (active, fixed, wontFix, closed, byDesign, pending). | Update the status of a PR comment thread | `/update-pr-thread-status repository: <name> pullRequestId: <id> threadId: <id> status: <status>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "threadId": 5, "status": "closed" }` |
| 9 | repo_reply_to_comment | Post a reply comment to an existing PR thread. | Post a reply to an existing PR comment thread | `/reply-to-pr-comment repository: <name> pullRequestId: <id> threadId: <id> content: <text>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "threadId": 5, "content": "Fixed in latest commit" }` |

## Pull Request Comments and Threads

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | repo_list_pull_request_threads | List all comment threads for a pull request with optional filters | View all comment threads in a pull request | `/view-pr-threads prUrl: <url>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "project": "YOUR_PROJECT", "top": 50 }` |
| 2 | repo_create_pull_request_thread | Create a new comment thread on a pull request (general or line-specific) | Create a new comment thread in a pull request | `/create-pr-thread prUrl: <url> filePath: <path> line: <n> comment: <text>` | `{ "repositoryId": "MyRepo", "pullRequestId": 123, "content": "Please review this change", "filePath": "/src/index.js", "rightFileStartLine": 42, "status": "active" }` |

## Commits

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | repo_search_commits | Search commits in a repository with comprehensive filtering (author, date, text, branch, etc.) | Search for commits in a repository with filters | `/search-commits repository: <name>` | `{ "project": "YOUR_PROJECT", "repository": "MyRepo", "searchText": "bug fix", "authorEmail": "john@example.com", "version": "main", "versionType": "branch", "top": 10, "includeWorkItems": true }` |

## Pipelines

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | pipelines_get_build_definitions | Retrieves a list of build/pipeline definitions for a given project | List pipeline/build definitions for a project with optional filters | `/list-build-definitions project: <project>` | `{ "project": "YOUR_PROJECT", "repositoryId": "MyRepo", "top": 20 }` |
| 2 | pipelines_run_pipeline | Trigger/queue a new pipeline run with optional branch, variables, and parameters | Trigger a pipeline run with optional branch, variables, and parameters | `/run-pipeline project: <project> pipelineId: <id>` | `{ "project": "YOUR_PROJECT", "pipelineId": 123, "branchName": "feature/new-branch", "variables": { "env": { "value": "prod" } } }` |
| 3 | pipelines_list_runs | List pipeline runs for a specific pipeline or project with filters for branch and status | List pipeline runs with optional filters for branch and status | `/list-pipeline-runs project: <project>` | `{ "project": "YOUR_PROJECT", "pipelineId": 123, "branchName": "main", "statusFilter": "completed" }` |
| 4 | pipelines_get_run | Get details of a specific pipeline run | Get details of a specific pipeline run by pipeline ID and run ID | `/get-pipeline-run project: <project> pipelineId: <id> runId: <id>` | `{ "project": "YOUR_PROJECT", "pipelineId": 123, "runId": 789 }` |
| 5 | pipelines_get_build_status | Get the status of a specific build/pipeline run using build ID | Get the status of a specific build/pipeline run by build ID | `/get-pipeline-status project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 456 }` |
| 6 | pipelines_get_builds | Get builds/pipeline runs with various filters including branch, status, and definition | Get builds with filters for branch, status, result, and definition | `/get-builds project: <project>` | `{ "project": "YOUR_PROJECT", "definitions": [123], "branchName": "develop", "resultFilter": "failed", "top": 10 }` |
| 7 | pipelines_cancel_run | Cancel a running pipeline/build | Cancel a running pipeline or build | `/cancel-pipeline project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 789 }` |
| 8 | pipelines_retry_stage | Retry/restart a specific stage in a pipeline run | Retry a failed stage in a pipeline build | `/retry-pipeline-stage project: <project> buildId: <id> stageName: <name>` | `{ "project": "YOUR_PROJECT", "buildId": 789, "stageName": "Deploy", "forceRetryAllJobs": true }` |
| 9 | pipelines_list_work_item_pipelines | Find all pipeline runs linked to a specific work item (useful for release work items) | Find all pipeline runs linked to a specific work item | `/list-work-item-pipelines project: <project> workItemId: <id>` | `{ "project": "YOUR_PROJECT", "workItemId": 12345, "top": 50 }` |
| 10 | pipelines_get_build_log | Retrieve the combined log output for all steps of a specific build. | Retrieve all log lines for a build | `/get-build-logs project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 789 }` |
| 11 | pipelines_get_build_changes | List commits/changesets associated with a pipeline build. | List commits and changesets associated with a pipeline build | `/get-build-changes project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 789, "top": 20 }` |
| 12 | pipelines_list_artifacts | List published artifacts from a build. | List published artifacts from a build | `/list-build-artifacts project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 789 }` |
| 13 | pipelines_list_variable_groups | List variable groups (Library) for a project, optionally filtered by name. | List variable groups (Library) for a project | `/list-variable-groups project: <project>` | `{ "project": "YOUR_PROJECT", "groupName": "Common Vars" }` |
| 14 | pipelines_get_variable_group | Get a specific variable group (Library) by ID, including its variables. | Get a specific variable group (Library) by ID | `/get-variable-group project: <project> groupId: <id>` | `{ "project": "YOUR_PROJECT", "groupId": 7 }` |

## Sprint & Capacity

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | work_list_iterations | List all iterations (sprints) defined in an Azure DevOps project. | List all sprint iterations defined in an Azure DevOps project | `/list-project-sprints project: <project>` | `{ "project": "YOUR_PROJECT", "depth": 2 }` |
| 2 | work_create_iterations | Create new sprint iterations in an Azure DevOps project. | Create one or more new sprint iterations in a project | `/create-sprints project: <project> name: <name>` | `{ "project": "YOUR_PROJECT", "iterations": [{ "name": "Sprint 42", "startDate": "2026-04-21", "finishDate": "2026-05-04" }] }` |
| 3 | work_list_team_iterations | List sprint iterations assigned to a specific team in a project. | List sprint iterations assigned to a specific team | `/list-team-sprint-iterations project: <project> team: <team>` | `{ "project": "YOUR_PROJECT", "team": "Your Team", "timeframe": "current" }` |
| 4 | work_assign_iterations | Assign one or more existing project iterations to a team. | Assign an existing project iteration to a team | `/assign-sprint-to-team project: <project> team: <team> iterationId: <guid>` | `{ "project": "YOUR_PROJECT", "team": "Your Team", "iterations": [{"id": "abc123-def456"}] }` |
| 5 | work_get_iteration_capacities | Get capacity breakdown for all teams in a project iteration. | Get capacity for all teams in a sprint iteration | `/get-sprint-capacities project: <project> iterationId: <guid>` | `{ "project": "YOUR_PROJECT", "iterationId": "abc123-def456" }` |
| 6 | work_get_team_capacity | Get the total team capacity summary (activity totals, days off) for an iteration. | Get the total team capacity summary (activity totals, days off) for a sprint | `/get-team-capacity project: <project> team: <team> iterationId: <guid>` | `{ "project": "YOUR_PROJECT", "team": "Your Team", "iterationId": "abc123-def456" }` |
| 7 | work_update_team_capacity | Update a team member's capacity (activity and daily hours) for a sprint. | Update a team member's daily capacity hours and activities for a sprint | `/update-team-capacity project: <project> team: <team> iterationId: <guid> teamMemberId: <guid> activityName: <name> hoursPerDay: <hours>` | `{ "project": "YOUR_PROJECT", "team": "Your Team", "iterationId": "abc123-def456", "teamMemberId": "member-guid", "activities": [{ "name": "Development", "capacityPerDay": 6 }] }` |
| 8 | work_get_team_settings | Get team settings including sprint cadence, working days, and bug behaviour. | Get team settings including sprint cadence and working days | `/get-team-settings project: <project> team: <team>` | `{ "project": "YOUR_PROJECT", "team": "Your Team" }` |

## Test Plans

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | testplan_list_test_plans | List all test plans in an Azure DevOps project. | List all test plans in an Azure DevOps project | `/list-test-plans project: <project>` | `{ "project": "YOUR_PROJECT", "filterActivePlans": true, "top": 20 }` |
| 2 | testplan_create_test_plan | Create a new test plan in an Azure DevOps project. | Create a new test plan in an Azure DevOps project | `/create-test-plan project: <project> name: <name> iteration: <path>` | `{ "project": "YOUR_PROJECT", "name": "Release 2.0", "iteration": "YOUR_PROJECT/Sprint 42", "startDate": "2026-04-21", "endDate": "2026-05-04" }` |
| 3 | testplan_list_test_suites | List all test suites in a test plan in a hierarchical structure. | List all test suites in a test plan | `/list-test-suites project: <project> planId: <id>` | `{ "project": "YOUR_PROJECT", "planId": 10, "top": 50 }` |
| 4 | testplan_create_test_suite | Create a new test suite inside a test plan. | Create a new test suite inside a test plan | `/create-test-suite project: <project> planId: <id> parentSuiteId: <id> name: <name>` | `{ "project": "YOUR_PROJECT", "planId": 10, "parentSuiteId": 11, "name": "Login Tests", "suiteType": "staticTestSuite" }` |
| 5 | testplan_add_test_cases_to_suite | Add existing test case work items to a test suite. | Add existing test case work items to a test suite | `/add-test-cases-to-suite project: <project> planId: <id> suiteId: <id> testCaseIds: <ids>` | `{ "project": "YOUR_PROJECT", "planId": 10, "suiteId": 12, "testCaseIds": [1001, 1002] }` |
| 6 | testplan_list_test_cases | List all test cases in a test suite (recursively includes child suites by default). | List all test cases in a test suite | `/list-test-cases project: <project> planId: <id> suiteId: <id>` | `{ "project": "YOUR_PROJECT", "planId": 10, "suiteId": 12, "includeChildSuites": true, "top": 100 }` |
| 7 | testplan_create_test_case | Create a new test case work item with optional steps. | Create a new test case work item with optional steps | `/create-test-case project: <project> title: <title>` | `{ "project": "YOUR_PROJECT", "title": "Verify login", "priority": 2, "steps": [{ "action": "Navigate to login page", "expectedResult": "Login page is displayed" }, { "action": "Enter credentials", "expectedResult": "User is logged in" }] }` |
| 8 | testplan_update_test_case_steps | Replace all test steps on an existing test case work item. | Replace all test steps on an existing test case | `/update-test-case-steps project: <project> testCaseId: <id> steps: <text>` | `{ "project": "YOUR_PROJECT", "testCaseId": 1001, "steps": [{ "action": "Open app", "expectedResult": "App loads" }] }` |
| 9 | testplan_show_test_results_from_build_id | Show all test run results associated with a specific build. | Show all test run results associated with a specific build | `/show-build-test-results project: <project> buildId: <id>` | `{ "project": "YOUR_PROJECT", "buildId": 789 }` |

## Core

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | core_get_identity_ids | Resolve Azure DevOps user identities (names, emails, or usernames) to their ADO identity IDs via the IdentityPicker API (fuzzy-matched, including "Surname, Firstname" order). Accepts a single search term. Useful for finding team member IDs needed by capacity and reviewer tools. | Look up Azure DevOps identity GUIDs for one or more users by email or display name | `/get-identity-ids identifiers: <emails; semicolon-separated>` | `{ "searchFilter": "john@example.com" }` |

## Confluence

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | confluence_list_my_pages | List Confluence pages created by the authenticated user | List my recent Confluence pages | `/my-confluence-pages` | `{ "limit": 5, "spaceKey": "CITGOLD" }` |
| 2 | confluence_search | Search Confluence content using CQL (Confluence Query Language) | Search Confluence pages using CQL | `/search-confluence cql: <query>` | `{ "cql": "type=page AND space.key=\"CITGOLD\" AND text~\"trade finance\"", "limit": 10 }` |
| 3 | confluence_get_page_id | Look up a Confluence page ID and metadata from its URL | Look up a Confluence page ID from its URL | `/get-confluence-page-id pageUrl: <url>` | `{ "pageUrl": "https://confluence.global.standardchartered.com/display/CC/MyPage" }` |
| 4 | confluence_update_page | Update the content of an existing Confluence page (Confluence Storage Format XHTML) | Update the content of a Confluence page | `/update-confluence-page pageId: <id> body: <content>` | `{ "pageId": "12345678", "title": "Updated Title", "body": "<p>New content</p>" }` |
| 5 | confluence_create_page | Create a new Confluence page under a parent page | Create a new Confluence page under a parent page | `/create-confluence-page parentPageUrl: <url> title: <title>` | `{ "parentPageUrl": "https://confluence.global.standardchartered.com/display/CC/Sprints", "title": "Sprint 42 Notes", "body": "<p>Notes here</p>" }` |
| 6 | confluence_read_page | Read the full content of a Confluence page from its URL. Supports both Cloud-style (/wiki/spaces/SPACE/pages/{id}/Title) and Server-style (/display/SPACE/Title) URLs. Returns `body.export_view` to capture tab content. | Read the full content of a Confluence page from its URL | `/read-confluence-page pageUrl: <url>` | `{ "pageUrl": "https://confluence.global.standardchartered.com/display/CC/Architecture" }` |
| 7 | confluence_get_page | Get a Confluence page by its numeric ID. Returns view, storage, and export_view body formats (export_view captures rendered tab content). | Get a Confluence page by ID | `/get-confluence-page pageId: <id>` | `{ "pageId": "123456789" }` |
| 8 | confluence_find_page | Find a Confluence page by space key and exact title. Returns page metadata including ID. | Find a Confluence page by space key and title | `/find-confluence-page spaceKey: <key> title: <title>` | `{ "spaceKey": "TEAM", "title": "Architecture Overview" }` |
| 9 | confluence_get_page_children | List the child pages of a Confluence page by its ID. | List children of a Confluence page | `/get-confluence-page-children pageId: <id>` | `{ "pageId": "123456789", "limit": 25 }` |
| 10 | confluence_list_spaces | List Confluence spaces (global spaces by default). | List all Confluence spaces | `/list-confluence-spaces` | `{ "limit": 50 }` |
| 11 | confluence_get_space | Get details of a Confluence space by its key. | Get details of a Confluence space | `/get-confluence-space spaceKey: <key>` | `{ "spaceKey": "TEAM" }` |
| 12 | confluence_delete_page | Delete a Confluence page by ID. Requires the page title to be provided for confirmation — title must match exactly or deletion is cancelled. | Delete a Confluence page | `/delete-confluence-page pageId: <id> title: <title>` | `{ "pageId": "123456789", "title": "Old Sprint Notes" }` |
| 13 | confluence_add_comment | Add a page-level comment to a Confluence page. Body must be in Confluence Storage Format (XHTML). | Add a comment to a Confluence page | `/add-confluence-comment pageId: <id> body: <xhtml>` | `{ "pageId": "123456789", "body": "<p>Great work!</p>" }` |
| 14 | confluence_get_labels | Get all labels on a Confluence page. | Get labels on a Confluence page | `/get-confluence-labels pageId: <id>` | `{ "pageId": "123456789" }` |
| 15 | confluence_add_label | Add a label to a Confluence page. | Add a label to a Confluence page | `/add-confluence-label pageId: <id> label: <name>` | `{ "pageId": "123456789", "label": "architecture" }` |

## SC Wiki

> SC Wiki is the internal XWiki instance replacing Confluence. Pages are addressed by a dotted reference (e.g. `Sandbox.S2B NG.WebHome`) rather than a numeric ID — nested spaces are chained with dots, and the final segment is the page name.

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | scwiki_search | Search SC Wiki pages by keyword across title, content, and page name. | Search SC Wiki pages by keyword | `/search-scwiki query: <query>` | `{ "query": "trade finance", "limit": 10 }` |
| 2 | scwiki_get_page | Get an SC Wiki page's metadata and content by its dotted reference. | Get an SC Wiki page by reference | `/get-scwiki-page pageReference: <ref>` | `{ "pageReference": "Sandbox.S2B NG.WebHome" }` |
| 3 | scwiki_find_page | Look up an SC Wiki page from its browser URL and return its metadata and content. | Find an SC Wiki page from its URL | `/find-scwiki-page pageUrl: <url>` | `{ "pageUrl": "https://scwiki.global.standardchartered.com/bin/view/Sandbox/S2B%20NG/" }` |
| 4 | scwiki_create_page | Create a new SC Wiki page at the given dotted reference (upsert). | Create a new SC Wiki page | `/create-scwiki-page pageReference: <ref> title: <title>` | `{ "pageReference": "Sandbox.NewPage", "title": "New Page", "content": "Hello" }` |
| 5 | scwiki_update_page | Update the title and/or content of an existing SC Wiki page. | Update an SC Wiki page | `/update-scwiki-page pageReference: <ref> content: <content>` | `{ "pageReference": "Sandbox.WebHome", "content": "Updated content" }` |
| 6 | scwiki_delete_page | Delete an SC Wiki page by its dotted reference. Requires the page title for confirmation — moved to the recycle bin, not permanently deleted. | Delete an SC Wiki page | `/delete-scwiki-page pageReference: <ref> title: <title>` | `{ "pageReference": "Sandbox.OldPage", "title": "Old Page" }` |
| 7 | scwiki_get_page_children | List the direct child pages of an SC Wiki page. | List children of an SC Wiki page | `/get-scwiki-page-children pageReference: <ref>` | `{ "pageReference": "Sandbox.WebHome", "limit": 25 }` |
| 8 | scwiki_list_spaces | List the top-level spaces in the configured SC Wiki instance. | List all SC Wiki spaces | `/list-scwiki-spaces` | `{ "limit": 50 }` |
| 9 | scwiki_list_my_pages | List SC Wiki pages created by the authenticated user. | List my recent SC Wiki pages | `/list-my-scwiki-pages` | `{ "limit": 10 }` |
| 10 | scwiki_add_comment | Add a comment to an SC Wiki page. | Add a comment to an SC Wiki page | `/add-scwiki-comment pageReference: <ref> text: <text>` | `{ "pageReference": "Sandbox.WebHome", "text": "Great work!" }` |
| 11 | scwiki_get_labels | Get all tags on an SC Wiki page. | Get tags on an SC Wiki page | `/get-scwiki-labels pageReference: <ref>` | `{ "pageReference": "Sandbox.WebHome" }` |
| 12 | scwiki_add_label | Add a tag to an SC Wiki page. | Add a tag to an SC Wiki page | `/add-scwiki-label pageReference: <ref> tag: <name>` | `{ "pageReference": "Sandbox.WebHome", "tag": "architecture" }` |
| 13 | scwiki_get_page_history | Get the version history of an SC Wiki page. | Get version history of an SC Wiki page | `/get-scwiki-page-history pageReference: <ref>` | `{ "pageReference": "Sandbox.WebHome", "limit": 25 }` |
| 14 | scwiki_list_attachments | List the attachments on an SC Wiki page (metadata only). | List attachments on an SC Wiki page | `/list-scwiki-attachments pageReference: <ref>` | `{ "pageReference": "Sandbox.WebHome" }` |

## Nexus IQ

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | nexus_scan_vulnerabilities | Scan local npm dependencies for security vulnerabilities using Nexus IQ. Reads local `package.json` and `node_modules`, auto-installs deps, submits components for policy evaluation, generates JSON/Markdown/HTML reports in `nexus-report/`, and opens the HTML report in the browser. Supports `deepMode` for exhaustive scans including devDependencies. **Node.js (npm/yarn) projects only.** | Scan local npm dependencies for security vulnerabilities using Nexus IQ. Supports 4 patterns: scan, scan-fix, deep-scan, deep-scan-fix via the pattern argument. | `/nexus-vulnerability-scan applicationId: <id>` | `{ "applicationId": "ITAM__YOUR_PROJECT__your-service", "projectPath": "/path/to/project", "deepMode": false }` |
| 2 | nexus_fix_vulnerabilities | Automatically remediate vulnerabilities found by `nexus_scan_vulnerabilities`. Reads `nexus-report/nexus-vulnerability-report.json`. Phase A: fixes direct deps; Phase B1: runs yarn/npm upgrade for transitive deps; Phase B2: upgrades parent direct deps (requires `approveParentUpgrades=true`); Phase B3: adds resolutions/overrides (requires `approveResolutions=true`). **Node.js (npm/yarn) projects only.** | — | — | `{ "applicationId": "ITAM__YOUR_PROJECT__your-service", "approveParentUpgrades": false, "approveResolutions": false }` |

## SonarQube

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | sonar_search_projects | Search or list SonarQube projects by name or key | Search or list SonarQube projects by name or key | `/sonar-search-projects` | `{ "query": "my-service" }` |
| 2 | sonar_get_branches | List all analysed branches for a SonarQube project | List all analysed branches for a SonarQube project | `/sonar-get-branches project: <key>` | `{ "project": "my-service" }` |
| 3 | sonar_get_quality_gate_status | Check the quality gate pass/fail status for a project branch or pull request | Check the quality gate pass/fail status for a SonarQube project branch or pull request | `/sonar-get-quality-gate projectKey: <key>` | `{ "projectKey": "my-service", "branch": "main" }` |
| 4 | sonar_get_issues | Search for bugs, vulnerabilities, and code smells in a SonarQube project | Search for bugs, vulnerabilities, and code smells in a SonarQube project | `/sonar-get-issues componentKeys: <key>` | `{ "componentKeys": "my-service", "types": "BUG", "severities": "BLOCKER,CRITICAL" }` |
| 5 | sonar_get_hotspots | List security hotspots in a SonarQube project that require manual review | List security hotspots in a SonarQube project that require manual review | `/sonar-get-hotspots projectKey: <key>` | `{ "projectKey": "my-service", "status": "TO_REVIEW" }` |
| 6 | sonar_get_measures | Retrieve code quality metrics (coverage, bugs, vulnerabilities, code smells, tech debt) for a project | Retrieve code quality metrics (coverage, bugs, vulnerabilities, code smells, tech debt) for a SonarQube project | `/sonar-get-measures component: <key>` | `{ "component": "my-service", "branch": "main" }` |

## Context Management

Tools for managing named workspace contexts. Contexts store ADO project, team, default branch, area/iteration paths, repository list, Nexus app IDs, and Confluence space key in `~/.sc-node-mcp-context.json`. The active context auto-fills arguments in other tools so you don't have to repeat project/team/repo details in every call.

| S.No | Tool Name | Description | Prompt Example | MCP Prompt | JSON Example |
|------|-----------|-------------|----------------|----------|--------------|
| 1 | ctx_set | Create or update a named workspace context and set it as the active context. Stores ADO project, team, default branch, area/iteration paths, repository list, Nexus app IDs, and Confluence space key in `~/.sc-node-mcp-context.json`. Auto-activates when the current working directory matches a `workspacePaths` entry. | Guided workflow to set up the active workspace context (project, team, default repo, Nexus app ID, Confluence space key) | `/set-context name: <name>` | `{ "name": "my-service", "project": "YOUR_PROJECT", "team": "Your Team", "defaultBranch": "develop", "confluenceSpaceKey": "PLAT" }` |
| 2 | ctx_get | Get the current active context as JSON. Auto-detects the active context by matching `workspacePaths` against the current working directory. Returns all stored fields (project, team, repos, Nexus app IDs, Confluence space). | — | — | `{}` |
| 3 | ctx_switch | Switch the active context to a different stored context by name. | Switch the active workspace context to a previously saved context by name | `/switch-context name: <name>` | `{ "name": "payments-service" }` |
| 4 | ctx_list | List all stored context names with their descriptions and workspace paths. | List all saved workspace contexts with their project, team, and workspace path details | `/list-contexts` | `{}` |
