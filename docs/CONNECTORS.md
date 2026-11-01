---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# External system connectors

Use the [connectors skill](../.agents/skills/connectors/SKILL.md) for agent setup, usage, and access diagnostics.

AI agents use external systems through the existing Workbench CLI and MCP interface.
The `connector.mcp` provider invokes the imported connector tools through a Node bridge.
Workbench checks operation grants and exact tool names before it starts the bridge.
Each action retains its result through the existing evidence store.

[Release reporting](RELEASE_REPORT.md) adds structured ADO and Sonar readers with exact grants.
Report collection uses one transient session per source and retains large responses in hashed files.
Other connector operations keep their existing process and response contracts.

The Python runtime remains the core application.
Node is an optional dependency for external connectors.
Connector packages remain under `core/connectors/packages/` in this source checkout.
The Workbench bridge uses their tool modules without their original startup programs.
Native startup sends no telemetry and does not search for organization proxy servers.

## Install from the project root

Use Node 22 or newer and the installed Workbench command.
Run these commands from the standalone source checkout.

```sh
python -m pip install .
npm ci --ignore-scripts --no-audit --no-fund
```

The root `package.json` manages package links and dependencies.
The root `package-lock.json` records dependency versions.
The imported Yarn release configuration does not control this installation.
No connector build is required for the native bridge.

## Maintain variables at the workspace root

Use [the root variable template](../.env.example) to create an ignored `.env` file.
This source checkout already has an empty private `.env` template.
Keep endpoints, credentials, and optional network settings in that file.
Process environment values take precedence, including empty values.
The bridge reads only the selected workspace's `.env` file.
Nested package files and the user's home configuration do not supply native connector variables.

| System | Required variables for calls |
| --- | --- |
| Azure DevOps | `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT` |
| Confluence | `CONFLUENCE_BASE_URL`, `CONFLUENCE_PAT` |
| XWiki | `SCWIKI_URL`, `SCWIKI_TOKEN`; optional `SCWIKI_WIKI` |
| Nexus IQ | `NEXUS_BASE_URL`, `NEXUS_USER_CODE`, `NEXUS_PASS_CODE` |
| SonarQube | `SONAR_BASE_URL`, `SONAR_TOKEN` |
| Kibana log analysis | `KIBANA_BASE_URL`, `KIBANA_ALLOWED_INDICES`, and `KIBANA_API_KEY` or `KIBANA_USERNAME` with `KIBANA_PASSWORD` |
| PostgreSQL analysis | `WORKBENCH_PG_HOST`, `WORKBENCH_PG_DATABASE`, `WORKBENCH_PG_USER`, `WORKBENCH_PG_PASSWORD` |
| Web | No service credentials; optional network settings |
| Messaging | Logged-in Outlook or Teams session and platform dependencies |

Configure only the systems you use.
Discovery does not require service credentials or contact external systems.
Calls validate configuration for the selected system.
One system does not require another system's credentials.

Set optional `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` at the root.
Set `NODE_EXTRA_CA_CERTS` in root `.env` when a private certificate authority is required.
Relative certificate paths resolve from the workspace root.
The bridge starts a child process when Node requires the certificate at startup.
The bridge preserves TLS certificate validation.
`CODE_REVIEW_GUIDE_FILE` resolves from the workspace root.
Optional connector context resolves under `.workbench/connectors/` in the selected workspace.

## Discover and invoke tools

This source checkout registers nine connector resources in `registry/tools.yaml`.
Initial grants permit selected reads for Azure DevOps, Confluence, XWiki, SonarQube, and web access.
Nexus and messaging initially permit discovery only.
Use discovery to inspect each tool's complete input schema and `allowed` status.

```sh
ai-sdlc --workspace . status
ai-sdlc --workspace . call external-confluence list
ai-sdlc --workspace . call external-confluence call --args '{"tool":"confluence_get_page","arguments":{"pageId":"123"}}'
ai-sdlc --workspace . runs
```

Agents use the same resources through `workbench_status` and `workbench_call`.
Start the existing MCP adapter with the selected workspace's absolute path.

```sh
ai-sdlc --workspace /absolute/path/to/workspace mcp
```

Grant `call` in `allowed_operations` and exact tool names in `config.allowed_tools` for each resource.
An absent or empty `allowed_tools` list denies every tool call.
Wildcards do not grant other tool names.
Resource grants do not replace the user's authorization for an external write or message.
Keep Confluence source access read-only as required by the source catalog contract.

## Analyze Elasticsearch logs through Kibana

The Kibana connector supports read-only log analysis through Console proxy access.
Configure the Kibana URL, including its base path and space path when required.
Supply an encoded API key or a username and password in the selected workspace's ignored `.env`.
Use credentials restricted to log reads and mapping inspection for the selected indices.
Enable Kibana Dev Tools Console for that identity.
No Elasticsearch URL is configured or contacted directly.

Set `KIBANA_ALLOWED_INDICES` to comma-separated, exact permitted index expressions.
For example, `application-logs-*` permits that expression, including its wildcard.
It does not permit a caller to substitute another expression.
Keep tenant-specific expressions in private project configuration.
`KIBANA_MAX_RANGE_HOURS` defaults to 24 hours. Its maximum is 168 hours.

Inspect the tool schemas and actual field types before searching:

```sh
ai-sdlc --workspace PATH call external-kibana list
ai-sdlc --workspace PATH call external-kibana call --args '{"tool":"kibana_get_field_mapping","arguments":{"index":"application-logs-*"}}'
```

`kibana_search_logs` requires an index, KQL expression, start time, end time, and explained field mapping.
The mapping must identify the timestamp and message fields.
Optional mappings identify the level, service, and correlation identity.
Each extra returned field also requires an explanation.
Use actual indexed field names and describe their meaning for the selected application.
The connector checks mapped field names and types against live mapping responses.

The following arguments illustrate a bounded search. Replace the times and field meanings with inspected project values.

```json
{
  "tool": "kibana_search_logs",
  "arguments": {
    "index": "application-logs-*",
    "kql": "log.level: error AND service.name: api",
    "start": "2026-11-01T00:00:00Z",
    "end": "2026-11-01T01:00:00Z",
    "fieldMapping": {
      "timestamp": {"field": "@timestamp", "explanation": "UTC event timestamp"},
      "message": {"field": "message", "explanation": "Application log message"},
      "level": {"field": "log.level", "explanation": "Application severity label"},
      "service": {"field": "service.name", "explanation": "Emitting service name"}
    },
    "size": 100
  }
}
```

KQL uses a bounded compiler in this connector. Kibana Console accepts Elasticsearch DSL, so raw KQL cannot be forwarded unchanged.
Supported expressions include field comparisons, `AND`, `OR`, `NOT`, parentheses, phrases, and field existence.
Wildcard support is limited to supported field types.
Unsupported KQL syntax or unknown field types fail explicitly.
This implementation does not claim compatibility with every Kibana KQL feature.
Inspect the discovered tool description for the supported grammar.

The connector sends only mapping reads and generated searches through `/api/console/proxy`.
Callers cannot supply Console paths, request methods, raw DSL, or scripts.
Search results explain the fields, KQL, generated query, time range, and completeness limits.
Check truncation, shard failures, and timeouts before drawing conclusions.
A bounded result cannot establish the absence of all matching events.

Console proxy compatibility depends on the installed Kibana version, authentication method, and configured privileges.
Local fixtures verify the request contract. They do not establish compatibility with the company's Kibana deployment.

## Analyze PostgreSQL data

Use a dedicated database identity with SELECT privileges for the required schemas and tables.
Do not use application write credentials or an administrator identity.
The connector rejects elevated role attributes and uses `BEGIN READ ONLY` for each operation.
It always rolls back and exposes no write, commit, DDL, or arbitrary command tool.

The database administrator must restrict role memberships, object ownership, and function execution grants.
PostgreSQL read-only transactions protect persistent database data. They do not sandbox functions with external side effects.
Do not grant this identity access to such functions or unsafe extensions.
Metadata reads describe accessible tables and their columns. They do not infer business meanings from column names.

```sh
ai-sdlc --workspace PATH call external-postgresql list
ai-sdlc --workspace PATH call external-postgresql call --args '{"tool":"postgresql_list_tables","arguments":{"schema":"public"}}'
ai-sdlc --workspace PATH call external-postgresql call --args '{"tool":"postgresql_describe_table","arguments":{"schema":"public","table":"events"}}'
ai-sdlc --workspace PATH call external-postgresql call --args '{"tool":"postgresql_query","arguments":{"sql":"SELECT status, count(*) AS total FROM public.events WHERE created_at >= $1 GROUP BY status","parameters":["2026-11-01T00:00:00Z"],"maxRows":100}}'
```

Use inspected table names and parameter placeholders for values.
Analysis accepts a single bounded `SELECT` or read-only `WITH` query.
Transaction escape attempts and mutation statements fail.
Queries return column metadata, rows, truncation status, and enforced limits.
Keep query conclusions separate from business intent and complete population claims.

`WORKBENCH_PG_PORT` defaults to `5432`.
`WORKBENCH_PG_MAX_ROWS` defaults to `1000` and cannot exceed `10000`.
`WORKBENCH_PG_STATEMENT_TIMEOUT_MS` defaults to `15000`.
Use the tool schema to inspect lower per-call row limits.
PostgreSQL uses its native TCP connection. HTTP proxy settings do not route database traffic.

TLS uses `WORKBENCH_PG_SSL_MODE=verify-full` by default.
Set `WORKBENCH_PG_CA_FILE` for a private certificate authority when required.
Relative certificate paths resolve from the selected workspace root.
An explicit `disable` setting supports an approved local environment. It provides no transport encryption.
No TLS mode disables certificate verification while claiming encrypted, verified access.

The pure JavaScript `pg` driver is installed from the root lockfile.
No local PostgreSQL server, `psql`, compiler, or native database extension is required for connector use.
The company database must remain reachable through approved routing.

## Use a generated workspace

Generated workspaces receive this guide and `.env.example`.
Their tool catalogs remain empty.
They do not receive connector source or Node dependencies.
The Python wheel installs the provider; the optional Node tools require this separate source checkout.

Use [the connector registry example](../registry/examples/connectors.yaml) to configure a generated workspace.
Merge selected entries into its tool catalog and replace each bridge path with the source checkout's absolute path.
Create `.env` at the generated workspace root.
The provider passes that root to the bridge, regardless of the connector source location.
Never put credentials into catalogs or call arguments.

## Limits and evidence

Calls start a separate process and use the workspace timeout.
Parsed responses have a four MiB limit.
The provider suppresses raw startup diagnostics because they can contain credentials.
Configure dependencies and variables before investigating a fixed connector failure message.

External content can appear in retained action results.
These results do not create raw snapshots or provenance manifest entries.
Use the ingestion procedure to preserve source bytes and source identities.
Successful tool execution does not establish approved intent or verified business behavior.

Messaging uses platform automation and can require Python packages or operating system permissions.
Web search can require Python dependencies from the imported web package guide.
Browser crawling requires an installed supported browser.
The stateful application bridge and upload application are outside this native interface.
Their original entrypoints are not configured by this integration.

## Acceptance criteria

```gherkin
Scenario: Read variables from the selected workspace
  Given the selected workspace has a root .env file
  And the connector package has a different .env file
  When an agent invokes a configured connector tool
  Then the bridge uses the root file's variables
  And process environment values override matching root values

Scenario: Deny an ungranted external tool
  Given a connector resource grants call
  And its allowed_tools list excludes the requested tool
  When an agent requests that tool
  Then the action fails with TOOL_NOT_GRANTED
  And zero connector processes start

Scenario: Discover tools without external access
  Given no external service credentials are configured
  When an agent lists a supported connector's tools
  Then the result contains tool names and input schemas
  And zero external service requests occur

Scenario: Retain a successful external read
  Given a local fixture supplies a configured service endpoint
  And the resource grants the requested read tool
  When an agent invokes the read tool
  Then the action contains the fixture response
  And retained result evidence includes a SHA-256 hash
```

### Kibana Console log analysis

```gherkin
Scenario: Search logs through Kibana with explained fields
  Given the index expression is explicitly allowed
  And the timestamp and message fields have verified types and semantic explanations
  And the query uses the supported KQL subset within the configured time limit
  When the agent requests log analysis
  Then all remote requests use the Kibana Console proxy
  And the result includes generated DSL, field explanations, and completeness limits
  And zero direct Elasticsearch requests occur
```

### Kibana query rejection

```gherkin
Scenario: Reject unsafe or unexplained log searches
  Given a log request has unsupported KQL or a missing field explanation
  When the agent requests log analysis
  Then no log search request occurs
  And the action reports an error
```

### PostgreSQL bounded analysis

```gherkin
Scenario: Protect PostgreSQL data during analysis
  Given a restricted PostgreSQL role can read the selected table
  When the agent requests bounded parameterized analysis
  Then the query executes inside a read-only transaction
  And the connector returns no more than the configured row limit
  And the transaction rolls back before the connection closes
```

### PostgreSQL mutation rejection

```gherkin
Scenario: Reject PostgreSQL mutation and transaction escape
  Given an isolated PostgreSQL fixture contains a known row
  When the agent attempts DML, DDL, or a transaction escape through the analysis tool
  Then the request fails
  And the known row and table remain unchanged
```
