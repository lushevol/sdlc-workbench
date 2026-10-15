# Relationship responsibility

The relationship layer connects requirements, architecture, code, tests, and observations through supporting evidence.
Use the three directories under `relationships/` for references and derived context.

The [canonical graph skill](../../.agents/skills/service-dependencies-graph/SKILL.md) owns graph extraction, resolution, validation, queries, and visualization.
Keep graph enhancements inside that skill.
The `skill.py` loader connects installed Workbench adapters to the workspace skill or its packaged fallback.
The installed CLI delegates builds and publishes snapshots under `relationships/service-dependencies/generated/` by default.
The `graph.snapshot` provider delegates read operations through existing CLI and MCP grants.

Generated workspaces receive this guide without core runtime source or project snapshots.
Initialization also copies the graph skill, including its executable helpers, schema, viewer, references, and tests.
Complete requirement-to-code and code-to-test validation requires further implementation.
This directory records the boundary within the single `core/` runtime.
