# Relationship responsibility

The relationship layer connects requirements, architecture, code, tests, and observations through supporting evidence.
Use the three directories under `relationships/` for references and derived context.
The `graph/` package builds and validates static cross-repository dependency snapshots.
It reuses the imported Service Dependencies Graph extractors and resolver.
The installed CLI publishes snapshots under `relationships/service-dependencies/generated/` by default.
The `graph.snapshot` provider exposes read operations through existing CLI and MCP grants.
Generated workspaces receive this guide without runtime source or project snapshots.
Complete requirement-to-code and code-to-test validation requires further implementation.
This directory records the boundary within the single `core/` runtime.
