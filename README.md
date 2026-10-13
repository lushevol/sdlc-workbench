# AI SDLC Workbench

A local workbench gives AI agents shared engineering context, relationships, evidence, and executable capabilities.
Existing repositories, documents, and test engines stay in their original locations.

[PRINCIPLE.md](PRINCIPLE.md) records the eight project principles.
[ARCHITECTURE.md](ARCHITECTURE.md) defines the three layers, six core capabilities, workflow, and evolution phases.
These documents supersede the earlier MVP construction proposal.

Status: Phase 1 foundation implemented.
Complete knowledge governance, relationship validation, and behavior verification remain planned.
The existing dashboard remains an optional resource-operation prototype.

The [MVP assessment and initial construction plan](docs/INITIAL_CONSTRUCTION.md) defines the next minimum delivery stages.
It records current evidence, source access gaps, parent reuse, and first-workflow completion checks.

## Install the standalone project

Run from this directory with Python 3.10 or newer.
The package declares one Python runtime dependency: `PyYAML==6.0.2`.
Specific providers and external tools can require Git or their own environments.

```sh
python -m pip install .
ai-sdlc --workspace . status
ai-sdlc --workspace . skills
```

## Create a workspace

Choose an empty directory and replace `PATH` with its location.
The initializer creates the configured project structure, shared skills, and decision documents.
It does not require Git or create sample business assets.

```sh
ai-sdlc init PATH
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH skills analyze-requirement
```

The project structure separates these responsibilities:

| Location | Responsibility |
| --- | --- |
| `workspace.yaml` | Workspace identity, settings, and registry references. |
| `registry/` | Repository, service, capability, and executable tool declarations. |
| `knowledge/` | Requirement, architecture, and decision references or derived context. |
| `relationships/` | Requirement-to-code, code-to-test, and service dependency references. |
| `skills/` | Shared procedures for requirement analysis, impact analysis, implementation verification, and gap detection. |
| `core/` | Capability ownership and implementation boundaries. |
| `adapters/` | Claude Code, Copilot, and MCP integration guidance. |
| `src/ai_sdlc_workbench/` | The single Python runtime implementation. |
| `tests/` | Workbench regressions, separate from business E2E tests. |

## Register existing assets

Read the [registry guide](registry/README.md).
Edit `registry/repositories.yaml`, `services.yaml`, and `capabilities.yaml` to describe existing assets.
Edit `registry/tools.yaml` to grant specific operations through providers.
Repository and capability declarations do not grant execution by themselves.

Absolute resource paths can reference assets outside the workspace.
Relative resource paths resolve against the workspace directory.
Keep repository Git histories and existing engineering layouts intact.
Local clones inside the workspace remain an optional arrangement.

`workspace.yaml` takes precedence when both workspace configuration formats exist.
Invalid YAML does not fall back to a legacy file.
Existing `workspace.json` configurations remain supported when YAML is absent.
The runtime merges tool registry records with inline `resources` and rejects duplicate IDs.
Restart CLI, dashboard, or MCP processes after configuration changes.

## Run operations and read evidence

Discover resource IDs, grants, and argument schemas through `status`.
Replace placeholders with the selected resource, operation, and JSON arguments.

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
ai-sdlc --workspace PATH run ACTION_ID
```

| Provider | Operations |
| --- | --- |
| `knowledge.local` | `list`, `search`, `read`, `ingest` |
| `repository.git` | `status`, `diff`, `branch` |
| `testing.command` | `list`, `run` |
| `logs.file` | `search` |
| `database.sqlite` | `tables`, `query` |
| `discovery.eureka` | `instances` |

Knowledge operations retain exact file paths and hashes.
Search uses literal matching; it does not supply automatic knowledge governance.
Repository operations use the registered independent checkout.
Test execution uses named command arrays from resource configuration and runs without a shell.
The test provider retains command output and exit codes without parsing assertion-level coverage.

Resource operations require explicit grants.
Actions use statuses `RUNNING`, `SUCCEEDED`, `FAILED`, and `DENIED`.
Provider failures can report `ERROR` or `TIMEOUT` within a failed action.
The workspace retains records in `.workbench/actions.sqlite3` and evidence files under `.workbench/runs/`.
A process interruption can leave an action at `RUNNING`; this foundation does not resume it.

Hashes identify retained bytes, not execution authenticity or approved intent.
A successful action does not establish `VERIFIED` behavior.

## Shared skills and agent adapters

The canonical procedures live in `skills/<skill-id>/SKILL.md`.
CLI and MCP expose the same files.
Workspace procedures override bundled procedures with the same ID.
The two original prototype procedures remain available for compatibility.

Use the [Claude Code](adapters/claude-code/README.md), [Copilot](adapters/copilot/README.md), and [MCP](adapters/mcp/README.md) guides.
These guides describe integration; they do not change the user's client configuration.
Native client discovery depends on that client's supported mechanisms.
The core does not depend on a specific agent, model, or conversation history.

The stdio MCP interface exposes four tools:

| Tool | Purpose |
| --- | --- |
| `workbench_status` | Read catalogs, resources, operations, and grants. |
| `workbench_call` | Invoke one permitted operation and retain evidence. |
| `workbench_runs` | Read action history or one action record. |
| `workbench_skills` | List or read shared procedures. |

## Optional resource demonstration

Use a different empty directory for sample assets.
The demonstration's independent calculator checkout requires Git.

```text
ai-sdlc init PATH --demo
ai-sdlc --workspace PATH call tests run --args '{"suite":"unit"}'
ai-sdlc --workspace PATH serve
```

The demonstration creates a requirement, calculator code, unit tests, logs, and a SQLite database.
Its `workspace.json` remains compatible with the resource prototype.
Its fixtures do not establish business-system behavior or E2E verification.
The dashboard binds to loopback and checks origin and session tokens for write requests.

## Provider plugins and limits

Use the [plugin contract](PLUGIN_CONTRACT.md) and [example plugin](examples/hello-plugin/hello_provider.py).
Installed plugins load only when the workspace enables their entry point names.
Plugins execute trusted Python code in the workbench process.
Operation grants control dispatch; they do not sandbox plugins or configured commands.

This foundation requires no dedicated server, database service, or cloud infrastructure.
SQLite stores local action history through the Python standard library.
External providers can require network access, credentials, or their own infrastructure.
Keep credentials outside tracked configuration.

Knowledge and query results have content bounds.
Test and Git output can consume disk space until timeout.
Action history has no automatic retention cleanup.
Full governance, graph integration, assertion mapping, durable workflows, and platform orchestration require later implementation.

## Validate and distribute

Run from the standalone project directory after installation:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
```

The build includes decision documents, configuration, responsibility folders, shared skills, and adapter guides.
`scaffold.json` defines the shipped workspace files.
Source checkout and wheel initialization use those same canonical files.
Automated prose checks do not certify complete ASD-STE100 compliance.
