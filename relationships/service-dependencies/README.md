# Service dependency relationships

Build a static dependency graph from local repositories with the installed runtime:

```sh
ai-sdlc --workspace PATH graph build
```

The default bundle is `relationships/service-dependencies/generated/`.
The default output directory is ignored by Git.
Keep the complete bundle and matching manifest together.
Use `--open` to display its interactive viewer.
Use `--repos` to select a repository directory within the workspace.
Use `--out` to select a separate output directory.

Read `analysis-coverage.json` before interpreting the graph.
Record snapshot identity, source freshness, independent Git revisions, dirty states, and source fingerprints.
Filesystem source copies can have fingerprints without Git revisions.
Static declarations do not prove runtime invocation, deployment, or approved business intent.
Dynamic nginx templates cannot establish concrete upstream identities without supported bindings.

Registered `graph.snapshot` tools query the same validated bundle through CLI `call` or MCP `workbench_call`.
The project resource `service-dependencies` grants `coverage`, `relationships`, `services`, `search`, and `neighborhood`.
Generated workspaces use their installed runtime and configured tool grants.
Initialization copies this responsibility guide and leaves live graph output behind.

Read the shared `service-dependencies-graph` skill for build, query, evidence, and source audit procedures.
