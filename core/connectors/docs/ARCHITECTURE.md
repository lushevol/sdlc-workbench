# Architecture and Development

## Project Structure

```
SC_Node_MCP (Lerna Monorepo)
├── packages/
│   ├── core/              # Core MCP infrastructure
│   │   └── src/
│   │       ├── config.js  # Configuration loading
│   │       ├── server.js  # MCP server factory
│   │       └── index.js   # Exports
│   ├── ado-core/          # Shared Azure DevOps connection factory
│   │   └── src/
│   │       └── index.js   # getADOConnection provider
│   ├── ado/               # Azure DevOps meta-package (all ADO tools)
│   │   ├── src/
│   │   │   ├── index.js   # MCP server entry point
│   │   │   ├── connection.js # Azure DevOps connection
│   │   │   ├── tools.js   # Registers all tools
│   │   │   └── tools/
│   │   │       ├── workItems.js  # Work item tools
│   │   │       ├── repos.js      # Repository tools
│   │   │       ├── pipelines.js  # Pipeline tools
│   │   │       ├── review.js     # PR review tools
│   │   │       ├── search.js     # Code & work item search tools
│   │   │       ├── testPlans.js  # Test plan & suite tools
│   │   │       └── work.js       # Sprint, iteration & capacity tools
│   │   └── tests/         # ADO package tests
│   ├── ado-workitems-read/  # Standalone: work item read tools
│   ├── ado-workitems-write/ # Standalone: work item write tools
│   ├── ado-repos-read/      # Standalone: repository read tools
│   ├── ado-repos-write/     # Standalone: repository write tools
│   ├── ado-pipelines/       # Standalone: pipeline tools
│   ├── ado-review/          # Standalone: PR review tools
│   ├── ado-sprints/         # Standalone: sprint & capacity tools
│   ├── ado-testplans/       # Standalone: test plan tools
│   ├── ado-search/          # Standalone: code & work item search tools
│   ├── confluence/        # Confluence package
│   │   └── src/
│   │       ├── index.js
│   │       ├── tools.js
│   │       └── tools/
│   ├── scwiki/            # SC Wiki (XWiki) package
│   │   └── src/
│   │       ├── index.js
│   │       ├── tools.js
│   │       └── tools/
│   ├── nexus/             # Nexus IQ vulnerability scanning package
│   │   └── src/
│   │       ├── index.js
│   │       ├── connection.js
│   │       ├── tools.js
│   │       └── tools/
│   │           ├── scan.js                # nexus_scan_vulnerabilities tool
│   │           ├── fix-vulnerabilities.js # nexus_fix_vulnerabilities tool
│   │           ├── generate-reports.js    # shared report utilities
│   │           └── enrich-fix-versions.js # Nexus Remediation API
│   ├── messaging/         # Messaging package (Outlook email + Microsoft Teams)
│   │   ├── src/
│   │   │   ├── index.js
│   │   │   ├── connection.js # Python bridge providers
│   │   │   ├── tools.js
│   │   │   └── tools/
│   │   │       ├── send.js   # Email send tool
│   │   │       └── teams.js  # Teams messaging tool
│   │   ├── scripts/
│   │   └── tests/
│   ├── web/               # Web search & fetch package (Python bridge for DuckDuckGo)
│   │   ├── src/
│   │   │   ├── index.js
│   │   │   ├── tools.js
│   │   │   └── tools/
│   │   │       └── websearch.js  # web_search (Python bridge) + web_fetch tools
│   │   ├── scripts/
│   │   │   └── search-ddg.py    # Bundled Python script — DDG search via urllib
│   │   └── tests/
│   ├── unified/           # Combined server — all packages (primary distribution)
│   │   └── src/
│   │       ├── index.js
│   │       ├── prompts.js   # Unified-only prompt definitions (set-context, switch-context, list-contexts, upload-attachment-ui); delegates to per-package configurators
│   │       ├── telemetry.js # Startup usage telemetry: one NDJSON entry per user+version on telemetry/usage-log branch (opt-out via DISABLE_TELEMETRY=1)
│   │       └── tools/
│   │           └── context.js  # ctx_set, ctx_get, ctx_switch, ctx_list tools
│   ├── ado-upload-app/    # Interactive file upload UI tools
│   ├── app-bridge/        # Browser automation via Selenium WebDriver 4.x (standalone, Chrome & Edge)
│   │   └── src/
│   │       ├── index.js
│   │       ├── config.js   # --chromedriver-path/--edgedriver-path CLI flag parsing
│   │       ├── driver.js   # Browser session singleton + proxy-arg injection
│   │       ├── cdp.js      # Lazy CDP connection + network/console capture buffers + trace state
│   │       ├── locators.js # Shared locator schema (incl. relative locators) + resolver
│   │       ├── errors.js   # Shared formatError() helper
│   │       ├── tools.js
│   │       └── tools/      # 48 tools across session/navigation/elements/interaction/
│   │                       # select/script/mouseKeyboard/alerts/cookies/windows/screenshot/codegen/
│   │                       # network/console/emulation/performance (CDP-based, no new dependency)
│   ├── sonar/             # SonarQube code quality and security analysis package
│   │   └── src/
│   │       ├── index.js
│   │       ├── connection.js
│   │       ├── tools.js
│   │       └── tools/
│   │           └── sonar.js     # 6 SonarQube tools
│   └── shared-tests/      # Shared test utilities
│       └── helpers/       # Test mocks and utilities
├── docs/                  # Root-level documentation
├── package.json           # Monorepo root package config
├── lerna.json             # Lerna monorepo configuration
├── config.json            # Azure DevOps credentials (required, gitignored)
├── jsconfig.json          # JS project config
└── azure-pipelines-npm.yml# Azure DevOps pipeline config
```

## How This MCP Server Was Created

This project implements a Lerna-managed monorepo with modular MCP servers for Azure DevOps, Confluence, SC Wiki, Email, and Nexus IQ:

- **Unified MCP Server** (`packages/unified/src/index.js`): Exposes all MCP tools across ADO, Confluence, SC Wiki, Messaging, Nexus IQ, SonarQube, and Context Management in a single server.
- **ADO Meta-Package** (`packages/ado/src/index.js`): All Azure DevOps tools in one server (81 tools)
- **ADO Work Items Read** (`packages/ado-workitems-read/src/index.js`): Work item read tools only
- **ADO Work Items Write** (`packages/ado-workitems-write/src/index.js`): Work item write/mutation tools only
- **ADO Repos Read** (`packages/ado-repos-read/src/index.js`): Repository and PR read tools (12 tools)
- **ADO Repos Write** (`packages/ado-repos-write/src/index.js`): Repository and PR write tools (9 tools)
- **ADO Pipelines** (`packages/ado-pipelines/src/index.js`): Pipeline and build tools (12 tools)
- **ADO PR Review** (`packages/ado-review/src/index.js`): AI-driven PR review tools (4 tools)
- **ADO Sprints** (`packages/ado-sprints/src/index.js`): Sprint, iteration, and capacity tools (8 tools)
- **ADO Test Plans** (`packages/ado-testplans/src/index.js`): Test plan management tools (9 tools)
- **ADO Search** (`packages/ado-search/src/index.js`): Code and work item search tools (2 tools)
- **Confluence-Only Server** (`packages/confluence/src/index.js`): Confluence tools only (15 tools)
- **SC Wiki-Only Server** (`packages/scwiki/src/index.js`): SC Wiki (XWiki) tools only (14 tools) — Bearer token auth via XWiki's Token Authenticator extension
- **Messaging Server** (`packages/messaging/src/index.js`): Email sending via Outlook automation and Microsoft Teams messaging
- **Nexus IQ Server** (`packages/nexus/src/index.js`): Vulnerability scanning and automated remediation via Sonatype Nexus IQ (2 tools) — Node.js (npm/yarn) projects only
- **SonarQube Server** (`packages/sonar/src/index.js`): Code quality and security analysis via SonarQube (6 tools)
- **App Bridge** (`packages/app-bridge/src/index.js`): Browser automation via Selenium WebDriver 4.x — Chrome and Edge only (48 tools, including Selenium test-code generation and CDP-based network/console inspection, device/network emulation, and raw performance tracing via `selenium-webdriver`'s own `driver.createCDPConnection()` — no new dependency). Standalone-only, like `web` — not included in `unified`. Driver paths are configured via `--chromedriver-path`/`--edgedriver-path` CLI flags (or `CHROMEDRIVER_PATH`/`EDGEDRIVER_PATH` env vars) rather than the positional ADO-style args, since it has no ADO/Confluence concept.

> **Shared connection factory:** All standalone `ado-*` packages depend on `@sc-node-mcp/ado-core` for the Azure DevOps connection provider, avoiding duplication across packages.

All tool registration is handled in package-specific `tools.js` files, which import and register tools from modular tool files:
- `packages/ado/src/tools/workItems.js` - 26 work item management tools
- `packages/ado/src/tools/repos.js` - 20 repository, branch, and PR management tools
- `packages/ado/src/tools/pipelines.js` - 12 pipeline and build management tools
- `packages/ado/src/tools/review.js` - 4 automated PR review tools
- `packages/ado/src/tools/search.js` - 2 code and work item search tools
- `packages/ado/src/tools/work.js` - 8 sprint, iteration, and capacity tools
- `packages/ado/src/tools/testPlans.js` - 9 test plan and test suite management tools
- `packages/confluence/src/tools/confluence.js` - 15 Confluence integration tools
- `packages/scwiki/src/tools/scwiki.js` - 14 SC Wiki (XWiki) integration tools
- `packages/messaging/src/tools/send.js` - Email send tool
- `packages/messaging/src/tools/teams.js` - Microsoft Teams messaging tool
- `packages/nexus/src/tools/scan.js` - `nexus_scan_vulnerabilities` — local dependency scan with HTML/JSON/Markdown report generation
- `packages/nexus/src/tools/fix-vulnerabilities.js` - `nexus_fix_vulnerabilities` — multi-phase automated vulnerability remediation
- `packages/nexus/src/tools/generate-reports.js` - shared report-building utilities
- `packages/nexus/src/tools/enrich-fix-versions.js` - Nexus IQ Remediation API integration for fix version resolution
- `packages/unified/src/tools/context.js` - 4 workspace context management tools (`ctx_set`, `ctx_get`, `ctx_switch`, `ctx_list`)
- `packages/unified/src/telemetry.js` - Startup usage telemetry: records display name + timestamp to `telemetry/usage-log` branch on first connection

The server uses:
- Node.js with modern JavaScript (ES2020+) and ESM modules
- `@modelcontextprotocol/sdk` package for MCP protocol implementation
- `azure-devops-node-api` library for Azure DevOps REST API interaction
- Lerna for monorepo management with independent package versioning

Tools are discoverable and callable by any MCP-compatible client. The server is configured to run via `.vscode/mcp.json`, allowing easy integration with the VS Code MCP extension or other MCP clients.

## Features

- **MCP tools** across Azure DevOps (81), ado-upload-app (2), Confluence (15), SC Wiki (14), Messaging (2), Nexus IQ (2), SonarQube (6), and Context Management (4) — **129 max** when all credentials are provided
- **Monorepo Architecture:** Modular packages with independent versioning using Lerna
- **Multiple Server Options:** Use ADO-only, individual ADO sub-packages (workitems-read, repos-read, pipelines, etc.), Confluence-only, SC Wiki-only, Messaging-only, Nexus-only, SonarQube-only, or the unified server
- **Distributed Prompts:** Each package ships its own prompts via a `configureXxxPrompts()` function. The unified server delegates to all per-package configurators and adds 4 unified-only prompts (`set-context`, `switch-context`, `list-contexts`, `upload-attachment-ui`). Context auto-fill (`~/.sc-node-mcp-context.json`) is provided by `@sc-node-mcp/core` and works in standalone package installs too.
- **Work Item Management (26 tools):** Create, update, query, link, batch-update; manage iterations, backlogs, sprints
- **Repository & PR Management (20 tools):** List repos, branches, PRs; create/update PRs; manage reviewers; search commits
- **Automated PR Review (4 tools):** AI-driven review posting comments to specific diff lines; cleanup via delete tool
- **Messaging Integration (2 tools):** Messaging integration via Outlook email automation and Microsoft Teams (native app)
- **Confluence Integration (15 tools):** Create, update, search, read, get page ID, list pages, manage spaces, comments, and labels
- **SC Wiki Integration (14 tools):** Create, update, delete, search, read, list spaces/children, manage comments/tags/history/attachments — pages addressed by dotted reference (e.g. `Sandbox.S2B NG.WebHome`), Bearer token auth via XWiki's Token Authenticator extension
- **Nexus IQ Scanning (2 tools):** Read local `package.json` and `node_modules`, submit to Nexus IQ, generate HTML/JSON/Markdown reports, auto-open in browser; automated multi-phase remediation of direct and transitive vulnerabilities. **Node.js (npm/yarn) projects only.**
- **Context Management (4 tools):** Named workspace contexts stored in `~/.sc-node-mcp-context.json`; auto-fill project/team/repo across all tools; auto-activate by workspace path
- **Conditional tool registration:** Confluence, SC Wiki, and Nexus tools only register when credentials are present
- Customizable PR review guidelines via a single `CODE_REVIEW_GUIDE.md` file; set `CODE_REVIEW_GUIDE_FILE` to its full path
- **Shared Test Infrastructure:** Reusable mocks and helpers across packages

## Development

- Code is written in modern JavaScript (ES2020+), using ESM modules
- Test framework: Vitest (native ESM support, Jest-compatible API)
- Test coverage target: 90% minimum (lines, functions, branches, statements)
- Linting and formatting are not enforced by default
- All tools are modular and can be extended independently

### Build System

Each package has a `build` script that stages files into `dist/` — only `dist/` is included in the published npm package:

| Package | Build command | Output |
|---------|--------------|--------|
| `core`, `ado-core`, `confluence`, `scwiki`, `ado`, `ado-workitems-read`, `ado-workitems-write`, `ado-repos-read`, `ado-repos-write`, `ado-pipelines`, `ado-review`, `ado-sprints`, `ado-testplans`, `ado-search`, `messaging`, `nexus`, `unified`, `web`, `app-bridge` | `rm -rf dist && cp -r src dist` | Plain copy of `src/` into `dist/` |
| `ado` (extra step) | `+ rm -rf dist/tempRepos` | Strips the runtime scratch dir from the artefact |
| `ado-upload-app` | `vite build` | Vite bundles `src/app/` into a single self-contained `dist/` file; `src/server/` ships as-is alongside `dist/` |

```bash
# Build all packages
yarn build

# Build a single package
cd packages/ado && yarn build
```

The ADO publish pipeline runs `build` before packaging so only compiled artefacts are pushed to Artifactory.  
`dist/` is gitignored — it is never committed; it is produced fresh in CI.

### Running Tests

```bash
# Run all tests across all packages
yarn test

# Run tests in watch mode
yarn test:watch

# Run tests with UI
yarn test:ui

# Run tests with coverage
yarn test:coverage

# Run tests for specific package
cd packages/ado && yarn test
cd packages/core && yarn test
```

### Testing Strategy

- **Unit Tests** - Test individual tool modules in isolation
  - Configuration loading and validation (packages/core)
  - Tool parameter validation (Zod schemas)
  - Azure DevOps API mocking
  - Error handling patterns

- **Integration Tests** - Test full MCP server lifecycle
  - Tool registration across all modules
  - Multi-tool workflows
  - End-to-end error handling

- **Shared Test Infrastructure** - Reusable test utilities
  - Mock Azure DevOps connections (packages/shared-tests/helpers)
  - Mock MCP server instances
  - Shared test fixtures and data

- **Test Helpers** - Reusable mocking utilities
  - `mockConnection.js` - Azure DevOps API mocks
  - `mockServer.js` - MCP server mocks and response validators

For detailed testing documentation, see the `README.md` in each package's `tests/` directory (e.g., [packages/ado/tests/README.md](../packages/ado/tests/README.md)).

## MCP Tools Organization

### Work Items & Repos
- List, get, create, update work items
- List backlogs and backlog items
- Add comments, link to pull requests, batch operations
- List repositories, branches, pull requests
- Get repo/branch/PR details
- Manage PR comments, threads
- Search commits, link PRs to commits

### PR Review Tools
- Automated PR analysis and review
- Post comments directly on PR lines
- Get PR diffs for analysis

### Confluence Integration
- List and manage Confluence pages

### Nexus IQ Vulnerability Scanning
- Fetch `package.json` from ADO repositories via Git API
- Submit npm dependencies to Nexus IQ for policy evaluation
- Poll and return structured vulnerability reports (Critical/High/Medium/Low)

See the code in `packages/ado/src/tools/workItems.js`, `packages/ado/src/tools/repos.js`, `packages/ado/src/tools/pipelines.js`, `packages/ado/src/tools/review.js`, `packages/confluence/src/tools/confluence.js`, and `packages/nexus/src/tools/scan.js` for full tool definitions and parameters.

## Extending the Server

To add new tools:

1. Create a new tool file in `src/tools/`
2. Export your tools from the file
3. Import and register them in `src/tools.js`
4. Update documentation as needed

The modular architecture makes it easy to add new capabilities while maintaining clean separation of concerns.
