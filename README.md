# AI SDLC Workbench

A local workbench gives AI agents shared engineering context, relationships, evidence, and executable capabilities.
Existing repositories, documents, and test engines stay in their original locations.

[PRINCIPLE.md](PRINCIPLE.md) records the nine project principles.
[ARCHITECTURE.md](ARCHITECTURE.md) defines the three layers, six core capabilities, workflow, and evolution phases.
These documents supersede the earlier MVP construction proposal.
[The workspace design](docs/WORKSPACE_DESIGN.md) applies the owner's [approved v2 plan](https://chatgpt.com/c/6acda433-95e4-83e9-933d-4f7b458ff7bf).

Status: Phase 1 foundation with workspace catalogs, portable knowledge contracts, and deterministic validation.
Automatic source ingestion, AI governance, complete relationship validation, and behavior verification remain planned.
Each retained item needs a current consumer, observable benefit, and supporting evidence.

The source checkout's `docs/INITIAL_CONSTRUCTION.md` records historical foundation gaps.
Generated workspaces do not include that earlier assessment.
The approved v2 plan controls the current folder and knowledge contracts.

## Install the standalone project

Run installation commands from the source checkout with Python 3.10 or newer.
Generated workspaces contain project records and guides.
They do not include package source, `pyproject.toml`, or runtime tests.
Use the installed `ai-sdlc` command to operate a generated workspace.
The package declares one Python runtime dependency: `PyYAML==6.0.2`.
Specific providers and external tools can require Git or their own environments.

```sh
python -m pip install .
ai-sdlc --workspace . status
ai-sdlc --workspace . skills
ai-sdlc --workspace . validate
```

## Create a workspace

Choose an empty directory and replace `PATH` with its location.
The initializer creates configuration, catalogs, knowledge schemas and templates, shared skills, and decision documents.
It does not require Git or create sample business assets.
New workspaces receive empty catalogs and provenance, without this project's source snapshots, candidates, findings, or audit history.

```sh
ai-sdlc init PATH
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH skills analyze-requirement
ai-sdlc --workspace PATH validate
```

The project structure separates these responsibilities:

| Location | Responsibility |
| --- | --- |
| `workspace.yaml` | Workspace identity, settings, and registry references. |
| `workspace.local.yaml` | Optional ignored repository path overrides for this machine. |
| `repos/` | Optional ignored independent clones. |
| `registry/` | Separate repository, service, capability, contract, source, and executable tool declarations. |
| `knowledge/raw/` | Unchanged source snapshots and their provenance manifest. |
| `knowledge/candidates/`, `knowledge/findings/` | Draft knowledge and unresolved evidence gaps. |
| `knowledge/requirements/`, `architecture/`, `decisions/` | Reviewed and published engineering knowledge. |
| `knowledge/schemas/`, `templates/`, `audit/` | Record contracts, starting records, and immutable event files. |
| `relationships/` | Requirement-to-code, code-to-test, and service dependency references. |
| `skills/` | Shared ingestion, governance, analysis, verification, and gap detection procedures. |
| `core/` | Single Python runtime and responsibility guides; installed as `ai_sdlc_workbench`. |
| `adapters/` | Claude Code, Copilot, and MCP integration guidance. |
| `registry/examples/` | Illustrative records checked against supported catalog contracts. |
| `tests/` | Checks for supported behavior, consequential boundaries, and confirmed defects. |

## Register existing assets

Read the [registry guide](registry/README.md).
Edit repository, service, capability, contract, and source catalogs to describe existing assets.
Edit `registry/tools.yaml` to grant specific operations through providers.
Repository and capability declarations do not grant execution by themselves.
Several repositories can support one service or capability.
One repository can support several services or capabilities.

Candidate contracts retain missing documentation as an explicit gap.

Absolute resource paths can reference assets outside the workspace.
Relative resource paths resolve against the workspace directory.
Keep repository Git histories and existing engineering layouts intact.
Local clones inside the workspace remain an optional arrangement.
Use ignored `repos/` for optional clones.

Copy [workspace.local.example.yaml](workspace.local.example.yaml) to ignored `workspace.local.yaml` for machine paths.
Its `repository_paths` mapping uses registered repository IDs as keys.
Local overrides change metadata locations in memory.
They do not rewrite provider configuration or grant operations.

`workspace.yaml` takes precedence when both workspace configuration formats exist.
Invalid YAML does not fall back to a legacy file.
Existing `workspace.json` configurations remain supported when YAML is absent.
The runtime merges tool registry records with inline `resources` and rejects duplicate IDs.
Restart CLI or MCP processes after configuration changes.

## Preserve and govern knowledge

Use Markdown with YAML frontmatter for portable knowledge documents.
The contracts follow [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) with Workbench SDLC constraints.
Use the [knowledge guide](knowledge/README.md), shipped schemas, and templates for actual records.
Keep original source bytes, source locators, revisions, retrieval times, and hashes in the raw evidence layer.
Create candidates and findings before publishing derived knowledge.

Use `governance_state` for candidate → investigated → verified → published.
Use contested, stale, or superseded when evidence requires them.
Keep this lifecycle separate from OKF `status` and test outcomes.
Important requirements and decisions need recorded human review before publication.
Never invent approval or reviewer identities.

Requirements use measurable Gherkin acceptance criteria.
Each criterion states conditions, an action, an observable result, and a measurable expectation.
Record each governance change in a new YAML event under `knowledge/audit/`.
Preserve earlier snapshots, events, and Git history.

```sh
ai-sdlc --workspace PATH validate
```

The deterministic validator reports `VALID` or `INVALID`, counts, and findings.
It checks saved contracts and provenance.
It does not establish business correctness, authenticate a reviewer, or prove passing execution.
Read [the workspace design](docs/WORKSPACE_DESIGN.md) for folder flow, traceability, and implementation limits.

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
| `graph.snapshot` | `coverage`, `relationships`, `services`, `search`, `neighborhood` |
| `testing.command` | `list`, `run` |
| `logs.file` | `search` |
| `database.sqlite` | `tables`, `query` |
| `discovery.eureka` | `instances` |

Knowledge operations retain exact file paths and hashes.
Search uses literal matching; it does not supply automatic ingestion or AI governance.
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
Use `ingest-knowledge` to review materials or produce classified, source-linked knowledge candidates.
Use `govern-knowledge` for investigation and publication.
Use [service-dependencies-graph](skills/service-dependencies-graph/SKILL.md) to build and query static dependency evidence.
Run `ai-sdlc --workspace PATH graph build`, then read the generated coverage and viewer.
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

## Provider plugins and limits

Use the [plugin contract](PLUGIN_CONTRACT.md) for provider interfaces and execution limits.
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
AI governance, external source adapters, assertion mapping, durable workflows, and platform orchestration require later implementation.

## Validate and distribute

Run tests and wheel builds from the standalone source checkout after installation.
Run `validate` against the selected source checkout or generated workspace.

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace . validate
```

The build includes runtime code, project guidance, configuration, knowledge contracts, shared skills, and adapter guides.
Workspace initialization copies responsibility guides without runtime code.
`scaffold.json` defines the shipped workspace files.
Source checkout and wheel initialization use those same canonical files.
Automated prose checks do not certify complete ASD-STE100 compliance.
