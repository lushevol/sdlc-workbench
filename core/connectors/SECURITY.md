# Security Policy

This is an internal Standard Chartered tool. Please do not open a public issue for
security reports — the guidance below is for reporting privately to the maintainers.

## Reporting a Vulnerability

- Report suspected vulnerabilities privately via the [SC Node MCP Teams channel](https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e), or contact a project maintainer directly.
- Include the affected package(s)/version(s), a description of the issue, and reproduction steps if possible.
- Do not include real credentials, tokens, or production data in a report.

We aim to acknowledge reports promptly and will coordinate a fix and, where relevant, a
coordinated disclosure timeline with the reporter.

## Supported Versions

Packages in this monorepo are versioned independently (see [lerna.json](lerna.json)).
Only the latest published version of each `@sc-node-mcp/*` package receives security fixes.
Pin to a specific version in production and upgrade regularly rather than relying on old releases.

## Credential Handling

- Never commit credentials, tokens, or secrets. `config.json` is gitignored — keep it that way.
- If a credential (ADO PAT, Confluence PAT, Nexus/SonarQube token) is accidentally exposed,
  rotate it immediately in the source system and notify a maintainer.
- Prefer environment variables or `config.json` (local dev only) over command-line arguments
  for supplying credentials, since CLI args can be visible in shell history and process lists.

## Known Accepted Risks

A few design tradeoffs are documented here rather than treated as open findings:

- Entry points set `NODE_TLS_REJECT_UNAUTHORIZED=0` to work behind corporate TLS-inspecting
  proxies. This disables certificate validation for the whole process. Only run these servers
  on trusted networks.
- `web_fetch`/`web_search` will fetch any URL requested by the connected AI client, including
  internal hosts reachable from the machine running the server. Treat fetched content as
  untrusted input.
