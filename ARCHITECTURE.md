# AI SDLC Workbench architecture

Decision date: 13 October 2026.
Authority: The project owner's supplied architecture discussion and [PRINCIPLE.md](PRINCIPLE.md).
Status: Accepted target architecture. The foundation implementation does not complete all target capabilities.

## Architectural boundary

The workbench owns engineering context, relationships, evidence, and executable capabilities.
AI agents use these capabilities to reason, plan, implement, and verify existing business systems.
Existing SDLC assets retain their original locations and ownership.
The workbench maintains references, relationships, and derived context.

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

The current dashboard provides a resource-operation prototype.
It does not establish completion of the future independent platform.
All interfaces must use the same core contracts and execution grants.

## Six core capabilities

| Capability | Target responsibility | Foundation and remaining work |
| --- | --- | --- |
| Context Registry | Discover domains, capabilities, repositories, services, and tools. | Workspace configuration and four catalogs establish resource identities. Automated discovery remains incremental. |
| Knowledge Governance | Assess source reliability, consistency, freshness, and completeness. | Source references support inspection. Automated governance remains planned. |
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
├── workspace.yaml
├── registry/
│   ├── repositories.yaml
│   ├── services.yaml
│   ├── capabilities.yaml
│   └── tools.yaml
├── knowledge/
│   ├── requirements/
│   ├── architecture/
│   └── decisions/
├── relationships/
│   ├── requirement-code/
│   ├── code-test/
│   └── service-dependencies/
├── skills/
│   ├── analyze-requirement/
│   ├── impact-analysis/
│   ├── verify-implementation/
│   └── detect-gaps/
├── core/
│   ├── context/
│   ├── relationships/
│   ├── evidence/
│   └── execution/
├── adapters/
│   ├── claude-code/
│   ├── copilot/
│   └── mcp/
├── src/ai_sdlc_workbench/
├── tests/
├── examples/
└── pyproject.toml
```

The six responsibility roots are `registry/`, `knowledge/`, `relationships/`, `skills/`, `core/`, and `adapters/`.
The tree defines the project construction and ownership boundaries.
It does not assert that every target engine already exists.
Local checkouts and generated evidence can use configured paths inside or outside this root.

### Workspace and registry

`workspace.yaml` defines workspace identity, settings, and catalog references.
`registry/repositories.yaml` records repository identifiers, names, and locations.
`registry/services.yaml` records service identifiers, names, and locations.
`registry/capabilities.yaml` records capability identifiers, names, and locations.
These catalogs describe existing assets without moving them.

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

`knowledge/` records expected behavior, business context, and its rationale.
Its requirements, architecture, and decisions directories hold project-authored records or references to existing sources.
Domain knowledge can remain in registered external sources.
Do not relocate authoritative source documents solely to match this directory tree.

Record source ownership, revision, and approval state when available.
Assess missing, conflicting, ambiguous, and outdated information before using it as intent.
Automatic governance requires later implementation and its own acceptance checks.

### Relationships

`relationships/requirement-code/` owns mappings from requirements to implementation.
`relationships/code-test/` owns mappings from implementation to test assertions.
`relationships/service-dependencies/` owns dependency relationships and references to generated graph evidence.
Keep consumer and provider evidence for confirmed service links.
Keep uncertain boundaries unresolved or identified as inferences.

Target relationship records identify their endpoints, source locators, revisions, evidence, and analysis scope.
Generated graphs must retain source identities, freshness information, and coverage limits.
Static declarations do not prove runtime execution.
The foundation does not yet generate or validate the complete relationship contract.

### Core implementation ownership

`core/` documents capability ownership.
The single Python runtime remains under `src/ai_sdlc_workbench/`.
Do not maintain a second runtime implementation under the top-level ownership directories.

| Ownership area | Current implementation | Target extension |
| --- | --- | --- |
| `core/context/` | Workspace loading, catalog loading, models, and provider registry. | Governed discovery and source context. |
| `core/relationships/` | Relationship ownership and stored references. | Evidence-backed mapping and relationship validation. |
| `core/evidence/` | Retained resource action records and result hashes in `store.py`. | Shared source, relationship, baseline, and verification evidence contracts. |
| `core/execution/` | Operation dispatch in `runtime.py` and existing provider implementations. | Coordinated workflows and integrated verification tools. |

The current runtime retains resource action evidence only.
It does not yet maintain a complete requirement-to-code-to-test verification baseline.

### Skills and adapters

`skills/` owns shared engineering procedures.
The four primary procedures analyze requirements, assess impact, verify implementation, and detect gaps.
Their inputs, outputs, evidence requirements, and limits must remain independent of the AI client.
Procedure execution can require an external agent and registered tools.

`adapters/claude-code/` exposes the shared procedures to Claude Code.
`adapters/copilot/` exposes the same procedures to GitHub Copilot.
`adapters/mcp/` defines access through the existing MCP runtime.
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
The `--demo` option supplies the earlier resource demonstration separately.
The demonstration's calculator and unit tests remain prototype fixtures.

## Validation and unresolved inputs

Validate YAML configuration, catalog identities, executable grants, shared skill access, and retained operation evidence.
Check CLI and MCP behavior against the same runtime.
Install the package outside the parent checkout and check that shipped resources remain available.
Target macOS and Windows portability. Record the platforms actually tested.

Business source locations, repository identities, engine configuration, and approved verification environments remain project-specific inputs.
Missing inputs must produce explicit limits or unresolved states.
Do not invent remotes, deployment identities, business rules, or passing E2E results.

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
