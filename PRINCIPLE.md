# AI SDLC Workbench principles

Decision date: 13 October 2026.
Authority: The project owner's supplied principles and architecture discussion.
Status: Accepted project direction. Implementation follows the phases in [ARCHITECTURE.md](ARCHITECTURE.md).

## Problem and goal

Requirements, design documents, source repositories, and test engines often have separate locations and owners.
Missing relationships limit an AI agent's understanding of business rules, change impact, and implementation evidence.

Create one evidence-driven SDLC workspace for existing business systems.
Enable agents to understand, analyze, implement, and verify those systems through shared context and executable tools.

## Project principles

### 1. Reuse, do not replace

Integrate existing repositories, documents, and engineering tools.
Keep existing assets in their original locations.
Do not require source migration or repository restructuring.
Support separate Git clones inside the workspace when the project owner chooses that arrangement.

### 2. Workspace as a unified context

Connect requirements, business capabilities, architecture, code, tests, and runtime behavior through one consistent workspace model.
Keep each asset's identity, location, owner, and revision available where the source provides them.
Use references and relationships to connect assets that have separate owners and storage locations.

### 3. Evidence over assumptions

Give each significant relationship and conclusion supporting evidence.
Retain source locators and revision identities with evidence links.
State facts, AI inferences, and unresolved questions separately.
Treat a missing source as an evidence limit.
Do not infer a future business rule from implementation alone.

### 4. Knowledge quality first

Check source reliability, freshness, consistency, and completeness before treating information as authoritative.
Identify missing, outdated, conflicting, and ambiguous information.
Record the owner decision needed when available evidence cannot establish the rule.
Keep approved intent separate from observed implementation behavior.

### 5. Agent-agnostic by design

Keep core capabilities independent of Claude Code, GitHub Copilot, and any specific AI model.
Put client integration in adapters.
Share the same workspace contracts, executable operations, and evidence records across clients.
Do not make a client's conversation history the only source of project decisions.

### 6. Executable, not just searchable

Let agents invoke existing analysis, build, testing, and verification tools.
Register each tool's operations and execution grants.
Retain execution inputs, results, and evidence limits.
Distinguish successful command execution from verified requirement behavior.

### 7. Local-first, minimal dependencies

Target local operation on macOS and Windows.
Require no dedicated server, database service, or cloud infrastructure for the core workspace.
Declare the runtime dependencies that shipped commands require.
Keep credentials outside tracked workspace configuration.
External tools can have their own declared dependencies and access requirements.

### 8. Incremental evolution

Start with integration into existing AI coding agents.
Add governed knowledge, traceability, and verification in later stages.
Evolve toward an independent SDLC platform without replacing the core architecture.
Introduce a dedicated interface and agent orchestration in Phase 3.

## Ownership boundary

The workbench owns engineering context, relationships, evidence, and executable capabilities.
AI agents consume those capabilities to reason, plan, implement, and verify.
Existing repositories and engineering tools retain their own implementation and execution responsibilities.

The standalone distribution must run without its parent analysis harness.
Ship reusable runtime code, configuration, schemas, and procedures within the workbench or through declared dependencies.
This packaging boundary does not require an independent model runtime or user interface in Phase 1.

## Seven SDLC concerns

The workspace covers domain knowledge, requirements, system design, source repositories, service dependencies, E2E verification, and SDLC skills.
These concerns connect through the architecture's registries, knowledge references, relationship records, core capabilities, and adapters.
They do not require seven mandatory asset copies inside the project.

Domain knowledge supplies terms, rules, and business context.
Requirements and system design supply versioned intent and design decisions.
Repositories supply implementation evidence at exact revisions.
Service dependencies identify relationships with source evidence and coverage limits.
E2E tools supply case assertions and actual execution observations.
Skills coordinate these sources through repeatable engineering procedures.

## Decision use

Use these principles and [ARCHITECTURE.md](ARCHITECTURE.md) when deciding project structure or implementation scope.
The earlier MVP layout no longer requires asset relocation, mandatory local clones, or client-specific skill ownership.
Keep implemented capabilities, planned capabilities, and unresolved project inputs distinct.
Record verification evidence before declaring a requirement behavior verified.

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
