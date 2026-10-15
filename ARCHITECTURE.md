# AI SDLC Workbench architecture

Decision date: 14 October 2026.
Authority: The owner's [approved v2 plan](https://chatgpt.com/c/6acda433-95e4-83e9-933d-4f7b458ff7bf) and [PRINCIPLE.md](PRINCIPLE.md).
Status: Accepted target architecture with deterministic workspace and knowledge validation.
Automatic ingestion, AI governance, and complete behavior verification remain planned.

## Architectural boundary

The workbench owns engineering context, relationships, evidence, and executable capabilities.
AI agents use these capabilities to reason, plan, implement, and verify existing business systems.
Existing SDLC assets retain their original locations and ownership.
The workbench maintains references, relationships, and derived context.
It preserves raw sources before interpretation and separates candidates, findings, and published knowledge.

The standalone package must run without the parent analysis harness.
Its runtime code must not import the parent harness or require parent-relative command paths.
Existing agents provide reasoning in Phase 1.
A dedicated interface and agent orchestration belong to Phase 3.

## Three layers

| Layer | Responsibility | Interfaces or assets |
| --- | --- | --- |
| 1. AI interface | Give agents access to shared workbench capabilities. | Claude Code, GitHub Copilot, shared skills, CLI, and MCP adapters. |
| 2. SDLC Workbench core | Manage context, knowledge quality, relationships, verification, workflows, and executable tools. | The six core capabilities below. |
| 3. Existing SDLC assets | Supply source intent, implementation, test definitions, and observations. | Requirements, acceptance criteria, decisions, design, repositories, test engines, CI/CD, and runtime observations. |

All interfaces must use the same core contracts and execution grants.

## Six core capabilities

| Capability | Target responsibility | Foundation and remaining work |
| --- | --- | --- |
| Context Registry | Discover capabilities, repositories, services, contracts, sources, and tools. | Six catalogs establish separate identities and references. Automatic discovery remains incremental. |
| Knowledge Governance | Assess source reliability, consistency, freshness, and completeness. | Schemas, templates, provenance checks, and audit records support agent procedures. AI governance remains planned. |
| Relationship Engine | Connect requirements, architecture, implementation, and tests through evidence links. | Relationship directories establish ownership. Automated mapping and validation remain planned. |
| Verification Engine | Identify gaps and compare expected behavior with implementation and observations. | Tool execution retains action evidence. Complete behavior verification remains planned. |
| Workflow Engine | Coordinate reusable engineering operations through shared skills. | Skills provide procedures for external agents. A durable workflow runner remains planned. |
| Tool Registry | Discover and invoke existing engineering and verification tools. | Registered resource operations use existing providers, operation grants, and retained action records. |

Catalog records establish declared resources and locations.
They do not prove an execution path, deployed service, or complete discovery coverage.
An action record establishes the retained operation result within its stated limits.
It does not establish requirement coverage or approved business intent.

## Project construction

The standalone project root is the current `workbench/` directory.

```text
workbench/
├── PRINCIPLE.md
├── ARCHITECTURE.md
├── README.md
├── AGENTS.md
├── workspace.yaml
├── workspace.local.example.yaml
├── workspace.local.yaml              # Ignored machine paths; optional.
├── repos/                            # Ignored independent clones; optional.
├── registry/
│   ├── repositories.yaml
│   ├── services.yaml
│   ├── capabilities.yaml
│   ├── contracts.yaml
│   ├── sources.yaml
│   ├── tools.yaml
│   └── examples/                    # Catalog examples checked against registry contracts.
├── knowledge/
│   ├── raw/
│   ├── candidates/
│   ├── findings/
│   ├── requirements/
│   ├── architecture/
│   ├── decisions/
│   ├── repository-profiles/
│   ├── audit/
│   ├── schemas/
│   └── templates/
├── relationships/
│   ├── requirement-code/
│   ├── code-test/
│   └── service-dependencies/
├── .agents/
│   └── skills/
│       └── service-dependencies-graph/ # Canonical graph implementation, guides, and tests.
├── skills/
│   ├── analyze-requirement/
│   ├── ingest-knowledge/
│   ├── govern-knowledge/
│   ├── impact-analysis/
│   ├── verify-implementation/
│   └── detect-gaps/
├── core/                           # Single Python runtime and responsibility guides.
│   ├── __init__.py
│   ├── cli.py
│   ├── runtime.py
│   ├── workspace.py
│   ├── providers/
│   ├── context/
│   ├── ingestion/
│   ├── understanding/
│   ├── governance/
│   ├── relationships/
│   ├── evidence/
│   └── execution/
├── adapters/
│   ├── sources/
│   ├── claude-code/
│   ├── copilot/
│   └── mcp/
├── tests/
├── docs/
└── pyproject.toml
```

The six responsibility roots are `registry/`, `knowledge/`, `relationships/`, `skills/`, `core/`, and `adapters/`.
The tree defines the project construction and ownership boundaries.
It does not assert that every target engine already exists.
Local checkouts and generated evidence can use configured paths inside or outside this root.
Read [the workspace design](docs/WORKSPACE_DESIGN.md) for each folder's role, data flow, and traceability diagrams.

### Workspace and registry

`workspace.yaml` defines workspace identity, settings, and catalog references.
`registry/repositories.yaml` records repository identifiers, names, and locations.
`registry/services.yaml` records service identifiers, names, and locations.
`registry/capabilities.yaml` records capability identifiers, names, and locations.
`registry/contracts.yaml` records documented or candidate component interfaces with exact source locators.
`registry/sources.yaml` records technical or context sources and their access mode.

These catalogs describe existing assets without moving them.
Keep repository, service, and capability identities separate.
Services and capabilities can reference several repositories.
Repositories can support several services or capabilities.

Optional `workspace.local.yaml` maps registered repository IDs through `repository_paths`.
The file uses `schema_version: 1` and remains ignored by Git.
Relative local paths resolve against the workspace directory.
Overrides replace metadata locations in memory and leave executable provider paths and grants unchanged.
Optional independent clones belong under ignored `repos/`.

`registry/tools.yaml` stores executable resource records.
Each executable record selects a provider, environment, configuration, and permitted operations.
The runtime resolves these records through its existing provider registry.
An empty operation grant denies execution for that resource.

Keep the metadata catalogs separate from executable resource configuration.
A repository metadata record alone does not grant Git operations.
A test-engine metadata record alone does not grant test execution.
Legacy `workspace.json` supports existing prototype workspaces during migration.
Use `workspace.yaml` for new workspaces.

### Knowledge

`knowledge/` records source evidence, expected behavior, business context, and rationale.
Its raw layer retains unchanged source snapshots with revisions, locators, retrieval times, and hashes.
Its candidates and findings layers retain unreviewed claims, conflicts, missing evidence, and open questions.
Its requirements, architecture, and decisions directories hold published knowledge or references to existing sources.
Domain knowledge can remain in registered external sources.
Do not relocate authoritative source documents solely to match this directory tree.

`KnowledgeTopic` records connect background, domain terms, workflows, and historical explanations across sources.
Classified drafts live under `knowledge/candidates/<classification>/` with a project-specific `index.md`.
The ingestion skill supplies review and ingestion modes for agent-assisted operation.
Classification does not establish approved intent or source authority.

Use [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) and the shipped Workbench schemas and templates.
Record source ownership, revision, and approval state when available.
Assess missing, conflicting, ambiguous, and outdated information before using it as intent.
Use measurable Gherkin acceptance criteria for requirements.
Track candidate → investigated → verified → published through `governance_state`.
Keep contested, stale, and superseded knowledge visible.

Important requirements and decisions require recorded human review before publication.
Keep OKF `status` and `verified` separate from Workbench lifecycle and business execution results.
Do not fabricate approvals or reviewer identities.

Retain each governance event in a new YAML file under `knowledge/audit/`.
Preserve earlier events and Git history.
An event binds the item version, content hash, actor, and supporting evidence.
Deterministic validation checks saved records and provenance.
It does not authenticate a reviewer or decide business correctness.
Automatic source adapters and AI governance require later implementation.

### Relationships

`relationships/requirement-code/` owns mappings from requirements to implementation.
`relationships/code-test/` owns mappings from implementation to test assertions.
`relationships/service-dependencies/` owns dependency relationships and references to generated graph evidence.
Keep consumer and provider evidence for confirmed service links.
Keep uncertain boundaries unresolved or identified as inferences.

Target relationship records identify their endpoints, source locators, revisions, evidence, and analysis scope.
Generated graphs must retain source identities, freshness information, and coverage limits.
Static declarations do not prove runtime execution.

The [canonical graph skill](.agents/skills/service-dependencies-graph/SKILL.md) owns extraction, resolution, validation, queries, and visualization.
Keep graph enhancements inside that skill.
Its helpers require no parent harness.
The installed `graph build` command delegates to the skill through a thin adapter.
The `graph.snapshot` provider delegates checksum-validated queries through existing CLI and MCP resource grants.
Requirement-to-code and code-to-test relationship validation remain planned.

### Core implementation ownership

`core/` contains the single Python runtime and its responsibility guides.
Packaging maps this directory to the installed `ai_sdlc_workbench` package.
`core/context/` owns catalog loading, and `core/governance/` owns deterministic knowledge validation.
Shared CLI, MCP, dispatch, models, and providers remain in this runtime.
Do not maintain a duplicate runtime under `src/`.

Generated workspaces receive core responsibility guides without core runtime source.
Initialization also copies the canonical graph skill, including its executable helpers, schema, viewer, references, and tests.
Initialization creates empty catalogs and provenance without copying live project configuration or knowledge records.

| Ownership area | Current implementation | Target extension |
| --- | --- | --- |
| `core/context/` | Catalog loading, supported by shared workspace loading, models, and provider registration. | Governed discovery and source context. |
| `core/ingestion/` | Source contracts and the ingestion procedure. | External source adapters and automatic snapshot collection. |
| `core/understanding/` | Candidate templates and agent interpretation procedures. | Automatic extraction and evidence-backed synthesis. |
| `core/governance/` | Deterministic knowledge validation and audit contracts. | AI governance and durable review workflows. |
| `core/relationships/` | Relationship ownership, stored references, and thin graph skill loading. | Evidence-backed mapping and relationship validation. |
| `core/evidence/` | Retained resource action records and result hashes in `store.py`. | Shared source, relationship, baseline, and verification evidence contracts. |
| `core/execution/` | Operation dispatch in `runtime.py` and existing provider implementations. | Coordinated workflows and integrated verification tools. |

The current runtime retains resource action evidence only.
It does not yet maintain a complete requirement-to-code-to-test verification baseline.

### Skills and adapters

`skills/` owns shared engineering procedures.
The shared procedures ingest knowledge, govern knowledge, analyze requirements, assess impact, verify implementation, and detect gaps.
Their inputs, outputs, evidence requirements, and limits must remain independent of the AI client.
Procedure execution can require an external agent and registered tools.

`.agents/skills/service-dependencies-graph/` owns the imported dependency graph capability.
Its scripts and tools support direct execution.
Its packaged helpers supply the same implementation to Workbench adapters.
CLI and MCP skill discovery include both canonical locations.
Discovery aliases under `skills/` and `.claude/skills/` point to the canonical graph directory.
Initialization creates forwarding `SKILL.md` files when the platform denies directory links.

`adapters/claude-code/` exposes the shared procedures to Claude Code.
`adapters/copilot/` exposes the same procedures to GitHub Copilot.
`adapters/mcp/` defines access through the existing MCP runtime.
`adapters/sources/` defines the future source integration boundary.
Adapters must reuse core dispatch and retained evidence.
They must not create separate business rules, grants, or verification claims.

## Core workflow

**Discover → Understand → Relate → Analyze → Execute → Verify**

1. Discover relevant capabilities, repositories, services, sources, and tools.
2. Understand reliable requirements, design decisions, and existing behavior.
3. Relate expected behaviors to affected services, code, and tests through evidence links.
4. Analyze change impact, inconsistent information, implementation gaps, and test gaps.
5. Execute registered tools or agent-directed implementation within the owning repositories.
6. Verify expected, implemented, and observed behavior. Retain evidence and unresolved gaps.

Preserve raw source evidence before drafting candidates.
Investigate findings and obtain required human review before publication.
Record governance changes through append-only audit event files and Git history.

Use exact repository revisions when analyzing code changes.
Read the cited source before treating retrieved text as authoritative evidence.
Inspect assertions before claiming test coverage.
Retain execution identities before claiming observed behavior.
Keep facts, inferences, and unresolved questions separate throughout the workflow.

## Seven concerns within the architecture

| SDLC concern | Workspace representation |
| --- | --- |
| Domain knowledge | Capability context, registered sources, knowledge references, and governance checks. |
| Requirements | `knowledge/requirements/` and requirement-to-code relationships. |
| System design | `knowledge/architecture/`, `knowledge/decisions/`, and service context. |
| Source repositories | `registry/repositories.yaml` and registered Git tools. Local clones remain optional. |
| Service Dependencies Graph | `relationships/service-dependencies/` and registered graph-generation or query tools. |
| E2E engine | Registered existing test engine, case references, execution tools, and retained observations. |
| SDLC skills | Shared procedures in `skills/`, exposed through adapters. |

An E2E engine can remain a separate checkout at its existing location.
The current command provider can run configured suites and retain their output.
Assertion mapping and complete E2E behavior verification require further implementation.
Demonstration fixtures do not establish business-system verification.

## Evolution phases

| Phase | Delivery scope | Completion evidence |
| --- | --- | --- |
| 1. Agent-Integrated Workbench | Local workspace, structured context, relationship records, shared skills, Claude Code, and Copilot integration. | Agents discover registered assets and invoke existing tools through shared interfaces with retained evidence. |
| 2. Governed SDLC Workbench | Automated knowledge maintenance, cross-repository traceability, evidence validation, and integrated verification workflows. | One versioned requirement maps through code and assertions to retained execution evidence. Governance checks expose unresolved gaps. |
| 3. Independent AI SDLC Platform | Dedicated interface, agent orchestration, managed workspaces, workflow automation, and enterprise governance. | The platform operates these capabilities through its own interface while retaining the same core contracts. |

The foundation stage creates the Phase 1 construction and preserves existing resource operations.
It does not complete all Phase 1 acceptance evidence or the later phases.
Clean initialization creates workspace configuration and responsibility directories.

Registry examples live under `registry/examples/` and illustrate validated catalog contracts.
Tests retain private fixtures only when they check supported behavior or consequential boundaries.
The project removes the public calculator demonstration and dashboard because they have no established current consumer.
Later phases describe possible direction and do not authorize speculative implementation.

## Validation and unresolved inputs

Validate YAML configuration, catalog identities, references, local mappings, knowledge contracts, and source provenance.
Use `ai-sdlc --workspace PATH validate` for deterministic checks.
Check executable grants, shared skill access, and retained operation evidence through relevant regressions.
Check CLI and MCP behavior against the same runtime.
Install the package outside the parent checkout and check that shipped resources remain available.

Target macOS and Windows portability. Record the platforms actually tested.

Business source locations, repository identities, engine configuration, and approved verification environments remain project-specific inputs.
Missing inputs must produce explicit limits or unresolved states.
Do not invent remotes, deployment identities, business rules, or passing E2E results.

## Implementation scope and risk

This stage merges runtime ownership, relocates catalog examples, and removes the public demonstration and dashboard.
CLI and MCP continue to share the same core runtime and grants.
Qualitative risk is moderate because package mapping, initialization, and imports affect CLI, MCP, providers, and distributed workspace files.
This standalone project has no GitNexus index.
Review callers, imports, configuration paths, tests, and package initialization directly.
Do not substitute an unrelated repository index or invent a numerical risk score.

## Output review

```json
{
  "asd_review": "PENDING",
  "automated_check": "PASSED",
  "findings": [],
  "limitations": [
    "Automated checks do not check the complete approved dictionary or grammar rules."
  ],
  "reviewed_at": null,
  "reviewer": null,
  "standard": "ASD-STE100"
}
```
