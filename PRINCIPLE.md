# AI SDLC Workbench principles

Decision date: 14 October 2026.
Authority: The project owner's [approved workspace plan](https://chatgpt.com/c/6acda433-95e4-83e9-933d-4f7b458ff7bf) and supplied principles.
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
Keep optional clones under ignored `repos/` and machine paths in ignored `workspace.local.yaml`.

### 2. Workspace as a unified context

Connect requirements, business capabilities, architecture, code, tests, and runtime behavior through one consistent workspace model.
Keep each asset's identity, location, owner, and revision available where the source provides them.
Use references and relationships to connect assets that have separate owners and storage locations.
Keep repository, service, capability, contract, source, and executable tool identities separate.
One repository can serve several services or capabilities.
One service or capability can depend on several repositories.

### 3. Evidence over assumptions

Give each significant relationship and conclusion supporting evidence.
Retain source locators and revision identities with evidence links.
State facts, AI inferences, and unresolved questions separately.
Treat a missing source as an evidence limit.
Do not infer a future business rule from implementation alone.

Preserve raw source snapshots and their provenance before deriving knowledge.
Keep AI candidates and findings separate from approved knowledge.

### 4. Knowledge quality first

Check source reliability, freshness, consistency, and completeness before treating information as authoritative.
Identify missing, outdated, conflicting, and ambiguous information.
Record the owner decision needed when available evidence cannot establish the rule.
Keep approved intent separate from observed implementation behavior.
Resolve material ambiguity before changing knowledge meaning.
After completed clarification, update affected knowledge with its answer source, scope, version, and evidence before handoff.
Do not leave resolved knowledge changes only in conversations or task notes.

Use measurable Gherkin acceptance criteria for requirements.
Require recorded human review for important requirements and decisions before publication.
Never fabricate a reviewer, approval, or source authority.
Preserve each governance event in a new audit YAML file and retain its Git history.

### 5. Agent-agnostic by design

Keep core capabilities independent of Claude Code, GitHub Copilot, and any specific AI model.
Put client integration in adapters.
Share the same workspace contracts, executable operations, and evidence records across clients.
Do not make a client's conversation history the only source of project decisions.

### 6. Executable engineering capabilities

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

Update [dependency analysis](docs/DEPENDENCIES.md) whenever a change adds, removes, or changes a runtime or build dependency.
Update installation scripts, diagnostics, manifests, and offline bundle preparation in the same change.
Record the dependency's purpose, version constraints, supported platforms, download sources, and required runtime endpoints.
Distinguish downloadable packages from live services that require network access during use.
Check affected installation paths before completing the change.
Keep this maintenance rule for future project changes.

### 8. Incremental evolution

Start with integration into existing AI coding agents.
Add governed knowledge, traceability, and verification in later stages.
Use OKF v0.2 for portable knowledge documents and Workbench schemas for SDLC constraints.
Keep deterministic validation separate from future AI governance and source adapters.
Evolve toward an independent SDLC platform without replacing the core architecture.
Introduce a dedicated interface and agent orchestration in Phase 3.

### 9. Keep only demonstrated current value

Retain an item only when a current use establishes its value.
Name its current consumer, observable benefit, and supporting evidence.
Possible future usefulness does not justify implementation, examples, dependencies, or tests.
Remove unsupported items instead of preserving speculative capability.
Keep examples beside the contract they explain.
Keep tests that check supported behavior, consequential boundaries, or confirmed defects.

Uncertainty can itself have current evidence value.
Preserve raw snapshots, candidate knowledge, unresolved findings, and immutable audit history under their existing retention rules.
Do not confuse an unresolved claim with a useless evidence record.
Require current evidence before implementing any later phase.

## Ownership boundary

The workbench owns engineering context, relationships, evidence, and executable capabilities.
AI agents consume those capabilities to reason, plan, implement, and verify.
Existing repositories and engineering tools retain their own implementation and execution responsibilities.

Task intake and domain knowledge updates serve business behavior requirements and defects in those repositories.
Harness configuration, upgrades, tools, and Workbench maintenance require no task or business knowledge record.
Maintain harness code, guides, applicable checks, and Git commits directly.
For mixed requests, retain the business scope in its task and handle harness support as maintenance.

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
Read [the workspace design](docs/WORKSPACE_DESIGN.md) for the approved folder, lifecycle, and provenance contracts.

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
