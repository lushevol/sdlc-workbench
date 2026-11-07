# System workspace isolation proposal

Date: 2026-11-07 (Asia/Singapore).
Status: Design recommendation. Runtime changes and asset migration are not implemented.
Authority: [Exact user request](evidence/system-workspace-isolation-20261107/user-input.md#exact-user-input).

**Use one independent workspace per system. Share the installed Workbench runtime and explicitly selected foundation sources.**

The current initializer supports this arrangement.
The main improvement is to separate framework development instructions from generated system instructions.
Folder separation provides context and data organization. Confidential systems also require access controls outside Workbench.

## Scope and ownership

A system workspace contains the engineering context for one system with coherent ownership and access requirements.
One system can contain many repositories, services, and capabilities.
Separate frontend and backend repositories do not require separate workspaces when they serve the same system.

The recommendation follows the existing [adoption boundary](WORKSPACE_DESIGN.md#brownfield-adoption-boundary) and [runtime ownership](../ARCHITECTURE.md#core-implementation-ownership).
It preserves the single Python runtime and the installed `ai_sdlc_workbench` package.
No additional server, database service, framework runtime, or foundation loader is required.

## Recommended construction

The following tree describes deployment ownership. It does not change the current source tree.
Each system directory is an independent workspace and can have its own Git repository.
The parent directory supplies navigation only. Keep system instructions, credentials, and configuration in their owning workspace.

```text
sdlc/
├── workbench-framework/             # Framework source, runtime, schemas, adapters, generic skills.
├── organization-foundations/        # Optional existing standards source; separately owned and versioned.
└── systems/
    ├── system-a/                   # Independent workspace and agent project.
    │   ├── AGENTS.md               # This system's operating instructions.
    │   ├── workspace.yaml          # Identity, catalog references, configured resources.
    │   ├── workspace.local.yaml    # Ignored machine-specific repository locations.
    │   ├── .env                    # Ignored system connection settings and credentials.
    │   ├── docs/                   # System adoption notes and engineering foundations.
    │   ├── registry/               # Repositories, services, capabilities, contracts, sources, tools.
    │   ├── knowledge/              # Intended domain behavior and target architecture.
    │   ├── repos/                  # Optional independent business Git checkouts.
    │   ├── tasks/                  # Business intake, investigation, gaps, and case evidence.
    │   ├── evidence/knowledge/     # Source snapshots, provenance, findings, immutable audits.
    │   ├── relationships/          # This system's traceability and generated dependency graphs.
    │   ├── .agents/skills/         # Distributed procedures and explicit local adaptations.
    │   ├── core/                   # Shipped guides, schemas, templates; no runtime Python source.
    │   └── .workbench/             # Local actions, caches, and execution state.
    └── system-b/                   # The same construction with independent content and settings.
```

The installed framework operates either workspace through its absolute path.
Application dependencies and builds remain owned by their business repositories.
Use separate framework environments when systems require different Workbench versions.

## Put each foundation with its owner

Here, foundation can mean procedures, engineering policy, domain architecture, or shared implementation.
Keep those responsibilities distinct through existing catalogs and source references.

| Foundation or asset | Recommended owner and location | Sharing rule |
| --- | --- | --- |
| Runtime, record schemas, generic skills | Framework distribution | Install a recorded version; review upgrades. |
| Organization engineering standards | Existing organization repository or document source | Register selected sources at exact revisions; record applicability. |
| System engineering principles and conventions | System workspace `docs/` and `AGENTS.md` | Apply only within that system's scope. |
| Intended business rules and target architecture | System workspace `knowledge/` | Preserve provenance, lifecycle, and required publication review. |
| Shared SDK, UI shell, platform library, or test engine | Independent registered repository | Preserve ownership; use separate working checkouts when either system edits. |
| System-specific skills or fixtures | Owning system workspace or business repository | Distribute only after evidence supports general reuse. |
| Credentials, endpoints, and execution grants | System `.env`, tool catalog, and scoped process environment | Configure separately for each system and environment. |
| Graphs, wiki, reports, and action evidence | Owning system workspace | Derive from that system's selected sources. |

Engineering policy can remain in `docs/` or an external registered source.
Domain target architecture belongs in `knowledge/architecture/` under the existing governance contract.
A foundation library remains a repository; its interfaces can use existing service and contract records.
No new mandatory `foundations/` catalog is needed.

Shared policy updates require an applicability review before a system adopts them.
Keep conflicting instructions visible and apply the owning repository's rules to its implementation.
Record the adopted framework revision, distribution hash, and selected source revisions in system adoption notes.

## Isolation rules

1. Give each system its own workspace root, workspace identity, Git history, and agent project.
2. Start CLI and MCP sessions with an explicit absolute workspace path.
3. Keep each system's catalogs, knowledge, source manifest, audit history, tasks, wiki, and graph inputs local to that workspace.
4. Keep secrets and endpoint bindings local. Start tools without another system's exported credentials or endpoint variables.
5. Keep operation grants explicit. Reading a shared foundation does not grant execution or transfer publication approval.
6. Preserve each business checkout's Git ownership. Use separate clones or worktrees for concurrent mutable work.
7. Scope agent retrieval and saved context to the selected system. Reference other systems only for an explicit task need.
8. Identify cross-system references with the owning workspace ID, asset ID, and exact revision or hash.

The final rule describes reference discipline. It does not introduce automatic federation or a new schema field.
Use existing registered source and contract records where their current contracts apply.
Keep cross-system contract facts in their owning sources and record consumer applicability locally.

For confidential or untrusted systems, use separate operating-system identities or execution environments with scoped filesystem and credentials.
Apply matching access restrictions to agent tools and external service accounts.
Workspace folders and operation grants cannot confine arbitrary trusted plugins or configured commands.

## What exists and what needs improvement

Source baseline: `538ad16abb1c699ed7c88f10b1222941daf660b2`.
The following claims concern inspected local implementation and the retained initialization check.

| Claim | Evidence class and confidence | Evidence and limit |
| --- | --- | --- |
| Independent roots already work. | Inspected implementation and observed execution; `HIGH`. | [Initializer](../core/workspace.py#L77-L130) creates fresh IDs, empty catalogs, and empty provenance. [Two-workspace check](evidence/system-workspace-isolation-20261107/workspace-check.json) passed local assertions. |
| Action state belongs to the selected root. | Inspected implementation; `HIGH`. | [Store](../core/store.py#L17-L32) uses root-local state. [Runtime](../core/runtime.py#L74-L86) records workspace identity. This does not restrict unrelated agent tools. |
| Generated instructions still contain framework history. | Inspected implementation and observed execution; `HIGH`. | [Scaffold list](../scaffold.json#L3-L9) copies root guides. The [check](evidence/system-workspace-isolation-20261107/workspace-check.json) confirmed identical guide bytes and an absent linked evidence file. |
| Process configuration can cross folder boundaries. | Inspected implementation; `HIGH`. | [Connector configuration](../core/connectors/workbench/config.js#L10-L16) gives process variables precedence over the workspace file. [Path resolution](../core/models.py#L43-L47) permits external paths. |
| Automatic foundation inheritance is not supported by this configuration contract. | Inspected implementation; `HIGH`. | [Workspace schema](../core/schemas/workspace.schema.json#L5-L22) rejects unknown fields and defines no foundation imports. Explicit source references remain available. |
| Separate system workspaces fit the current design. | Architectural inference; `MEDIUM`. | Existing initialization and ownership boundaries support the proposal. No second real system has completed adoption in this investigation. |

## Recommended next change

Owner: Workbench maintainer. Qualitative risk: low for this proposal; moderate for later scaffolding or relocation changes.
No application code, credentials, catalogs, or retained historical evidence were changed.

1. Create generic generated-workspace guides, separate from framework development guides.
   Include a system-owned instruction area and references to shared procedures.
   Update `scaffold.json`, packaging, initialization checks, and generated-guide link checks together.
2. Keep new systems outside the framework checkout and initialize their empty workspaces independently.
   Register their existing sources and repositories without copying framework-project content.
3. Plan the current Ratan workspace separation as a distinct migration.
   Preserve snapshot bytes, source identities, audits, and old-to-new locator manifests before moving assets.
   Update active references and keep business checkout histories independent.
4. Verify two populated workspaces before declaring adoption complete.
   Check that each system retrieves only its configured records and retains actions in its own store.
   Check explicit shared sources, independent grants, conflicting process variables, and installed-wheel behavior.

Foundation overlays, global search, and a workspace manager are unnecessary for the requested construction.
Add those capabilities only when a concrete cross-system workflow establishes their need.
This proposal does not authorize relocation or establish confidentiality between tenants.

## Use the current initializer

Run these commands after installing Workbench and placing its executable on `PATH`.
Use new, empty target directories.
Replace the example absolute paths with local paths.

```sh
ai-sdlc init /absolute/path/systems/system-a --name "System A"
ai-sdlc init /absolute/path/systems/system-b --name "System B"
ai-sdlc --workspace /absolute/path/systems/system-a validate
ai-sdlc --workspace /absolute/path/systems/system-b validate
```

The current initializer does not create Git repositories or clone business repositories.
Review generated instructions before adopting them for another system.
Use [the setup guide](SETUP.md#source-checkouts-and-generated-workspaces) and [connector guide](CONNECTORS.md#use-a-generated-workspace) for optional tools.

## Validation and limits

Two temporary workspaces passed initialization assertions and deterministic validation through the source checkout's existing Python environment.
The same check confirmed the copied-guide issue. [Canonical result](evidence/system-workspace-isolation-20261107/workspace-check.json).
Temporary workspaces were removed after the check.
The plain `ai-sdlc` command was unavailable on the current shell's `PATH`; `.venv/bin/ai-sdlc` worked.

Document checks cover local link targets, source line locators, command syntax, and whitespace.
No new wheel, Windows execution, external connector call, security boundary test, or real system migration was performed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
