# MVP assessment and minimum initial construction

Assessment date: 13 October 2026.
Source revision: `df34b47c2497c9a0eb9fd30843fdf2107ff4d09c`.
Scope: The checked-out Workbench foundation and selected parent components.
Status: Historical assessment of the source revision above.

Its behavior descriptions, gaps, and execution results describe that revision only.
Current source links follow the merged `core/` layout.
Use [the workspace design](WORKSPACE_DESIGN.md) for current contracts and [the principles](../PRINCIPLE.md) for scope decisions.

## Assessment

The current folder provides a useful standalone foundation for brownfield SDLC work.
Keep its six responsibility roots and single Python runtime.
The next stage must connect registered sources to one saved engineering review.

“One place” means one context and evidence workspace.
Repositories, documents, graph bundles, and test engines can retain their existing locations.
The Workbench connects their identities, source references, relationships, and executable tools.
This construction follows [PRINCIPLE.md](../PRINCIPLE.md) and [ARCHITECTURE.md](../ARCHITECTURE.md).

The current implementation retains resource actions.
It does not yet validate a complete requirement-to-code-to-test evidence chain.
The architecture already states this limit.

## Confirmed foundation

| Component | Inspected evidence | Current behavior |
| --- | --- | --- |
| Workspace construction | [workspace.py](../core/workspace.py), `initialize_workspace`; [scaffold.json](../scaffold.json). | Creates configuration, catalogs, ownership folders, shared skills, and adapter guides. |
| Context declarations | [catalogs.py](../core/context/catalogs.py), `load_catalogs`. | Loads four catalogs. Checks identities and selected service references. |
| Source access | [knowledge.py](../core/providers/knowledge.py), `LocalKnowledgeProvider`. | Lists, searches, and reads Markdown/text sources. Retains paths, content, and hashes for reads. |
| Repository operations | [repository.py](../core/providers/repository.py), `GitRepositoryProvider`. | Inspects independent checkouts, compares refs, and creates branches. |
| Tool execution | [runtime.py](../core/runtime.py), `Workbench.call`; [testing.py](../core/providers/testing.py). | Checks grants, invokes providers, and retains test command output and exit codes. |
| Action evidence | [store.py](../core/store.py), `Store.retain`. | Saves action records and evidence file hashes. |
| Shared agent access | [cli.py](../core/cli.py); [mcp.py](../core/mcp.py); [skills](../skills/). | Exposes shared operations, action history, and four primary SDLC procedures. |
| Standalone boundary | [pyproject.toml](../pyproject.toml); [setup.py](../setup.py); [interface tests](../tests/test_interfaces.py). | Declares the runtime dependency and builds the workspace scaffold. Tests CLI access without parent runtime imports. |

These facts support continued use of the current structure.
They do not establish business coverage, complete agent integration, or verified business behavior.

## Material gaps

Owners below identify proposed responsibilities. Named project owners remain unresolved.

| ID | Evidence and gap | Consequence | Owner and next action |
| --- | --- | --- | --- |
| G1 | `Workbench.describe` returns catalog counts and IDs. CLI and MCP provide no catalog record reader. | Agents cannot retrieve registered asset locations or service links through the shared interface. | Workbench maintainer: add catalog list/read operations. Expose source metadata separately from tool connection configuration. |
| G2 | `load_catalogs` permits ID-only metadata records. It has no shared source authority or freshness contract. | A declaration can lack a usable locator. Agents must reconstruct source roles and authority during each review. | Workbench maintainer: define validated source records. Represent unknown ownership, location, approval, and revision explicitly. |
| G3 | `GitRepositoryProvider` retains ref arguments and diff text. It provides no exact-ref file read or resolved comparison commits. | Mutable refs and omitted surrounding source limit later reconstruction of a code review. | Workbench maintainer: retain resolved commit IDs and exact-ref source reads. Record dirty source when execution uses a worktree. |
| G4 | Relationship folders contain guidance. Shared skills describe reports without a common saved review schema or template. | Reviews have no checked contract for behavior, implementation, assertion, and finding links. | Workbench maintainer: add one versioned review contract and template. Validate references and evidence limits. |
| G5 | `CommandTestingProvider` records commands and output. It does not bind results to code revisions, assertions, or target runtime identity. | A passing action cannot establish which business behavior the implementation satisfied. | Verification maintainer: bind observations to code, tests, configuration, data, and environment evidence. Preserve missing bindings as unresolved. |
| G6 | `Store.run` returns saved records without checking current evidence hashes. | Missing or changed evidence can remain undisclosed during a later review. | Workbench maintainer: add evidence integrity checks. Keep action outcome and current evidence integrity separate. |
| G7 | The scaffold lacks a brownfield onboarding example, operating guide, and standalone SDLC output standard. | Users receive empty catalogs and procedures without a complete first-review setup. | Workbench maintainer: ship onboarding guidance, operating instructions, the output standard, and one review example. |

G1–G3 use [runtime.py](../core/runtime.py), [catalogs.py](../core/context/catalogs.py), and [repository.py](../core/providers/repository.py).
G4 uses the [relationship guides](../relationships/) and [verification procedure](../skills/verify-implementation/SKILL.md).
G5–G7 use [testing.py](../core/providers/testing.py), [store.py](../core/store.py), and [scaffold.json](../scaffold.json).

These gaps concern initial usability and evidence retention.
They do not demonstrate defects in any business repository.

## Minimum initial construction

Keep the existing ownership boundaries:

| Location | Minimum completed responsibility |
| --- | --- |
| `registry/` | Identify capabilities, services, repositories, sources, and tools. Expose inspectable source records and explicit operation grants. |
| `knowledge/` | Reference domain rules, requirements, design, and decisions. Record source authority and unresolved conflicts. |
| `relationships/` | Retain requirement-to-code, code-to-assertion, and relevant service dependency links with evidence. |
| `skills/` | Run one repeatable requirement, code, and test gap review through the existing shared procedures. |
| `core/` | Own source access, relationship validation, evidence checks, review records, and dispatch. The current implementation now lives under `core/`. |
| `adapters/` | Expose the same contracts through CLI/MCP and one proven coding-agent integration. |

Use small records with explicit identities:

| Record | Minimum fields or relationships |
| --- | --- |
| Source | ID, role, locator, owner, revision/hash, authority state, freshness result, and access tool reference. |
| Behavior | ID, source IDs, exact source locators, condition, expected result, and unresolved intent. |
| Evidence link | ID, endpoint IDs, relationship kind, revision, locator, evidence reference, analysis scope, and evidence grade. |
| Review | ID, selected capability, source versions, repository comparison commits, behavior matrix, findings, and evidence limits. |
| Observation | Action ID, assertion/predicate reference, implementation and test identities, environment, time, result, and evidence references. |
| Finding | ID, behavior/link reference, evidence, consequence, owner, and next action. |

Add source records through one shared contract across document, graph, and test-source roles.
The current configuration recognizes four catalogs only.
Any additional source catalog needs schema, loader, interface, and initialization changes together.
Do not document a planned catalog as a supported configuration.

A reviewed file can remain external while the Workbench retains the bytes used as evidence.
Record the original locator and version with the retained copy.
Evidence copies do not replace the authoritative source or its ownership.

For the first review, agents can author behavior mappings and findings.
The core must validate identities, links, retained hashes, and required fields.
Automated mapping and complete knowledge governance can follow later.

## Extract or integrate parent components

The parent project supplies reference implementations and evidence contracts.
The standalone runtime must work without that checkout.
An external tool integration can use a separately configured installation.

| Parent source | Initial reuse | Adaptation or limit |
| --- | --- | --- |
| [Evidence schema](../../config/evidence-contract.schema.json), [baseline schema](../../config/behavior-baseline.schema.json), and [assurance.py](../../ratan_harness/assurance.py). | Extract the minimum source, behavior, link, finding, and review contracts with selected validation logic and fixtures. | Parent assurance uses parent-relative schemas, contained artifact paths, and additional dependencies. Adapt resource locators and package the required schemas. |
| [Output standard](../../docs/SDLC_OUTPUT_STANDARD.md) and [output_standard.py](../../ratan_harness/output_standard.py). | Ship the writing standard and reusable prose checks with report generation. | Keep automated checks and ASD review separate. Package the implementation without parent imports. |
| [OpenKB MCP](../../ratan_harness/mcp/openkb.py) and [knowledge.py](../../ratan_harness/knowledge.py). | Integrate an existing configured knowledge service when local Markdown/text access cannot serve the pilot. | Search requires exact cited reads. Preserve source roles, citations, and freshness. Keep optional model-backed synthesis optional. |
| [GitNexus launcher](../../.claude/tools/gitnexus-repos-mcp.py). | Integrate a separately configured repository-scoped code index when the pilot requires indexed callers or impact. | The launcher filters direct children of parent `repos/`. Adapt catalog locations. Check index revision against review scope. |
| [Graph skill](../../.claude/skills/service-dependencies-graph/SKILL.md). | Build and query local static dependency snapshots. | Grouped discovery reads registered locations. External registered paths remain explicit coverage limits. |
| [Execution importer](../../ratan_harness/assurance_execution.py) and [execution bindings](../../config/assurance-execution-bindings.schema.json). | Adapt observation bindings for normalized retained reports that follow the evidence contract. | Native formats need a translator. The importer does not authenticate execution. Inspect the real test engine first. Retain exact test/code/environment identities. Do not infer coverage from exit status. |
| [SDLC skills](../../.claude/skills/verify-story-change-test/SKILL.md) and [assurance handoff](../../.claude/skills/references/assurance-handoff.md). | Adapt source selection, behavior mapping, gap categories, and report procedures into the four shared Workbench skills. | Remove fixed Ratan paths and tool assumptions. Keep evidence rules and verification limits. |

Copying parent wrappers alone does not supply standalone capabilities.
Each extraction needs its implementation, schemas, fixtures, declared dependencies, and configurable paths.
Keep business clones, credentials, indexes, and knowledge databases outside the distribution.

## Delivery stages and checks

| Stage | Work | Completion evidence |
| --- | --- | --- |
| 1. Inspectable sources | Complete G1–G3. Add source metadata, public discovery, and exact code access. | CLI and MCP return the same source identities. Recorded commits and retained source bytes reproduce inspected content after refs move. |
| 2. Saved review | Complete G4 and G6. Add the review schema, report template, and integrity checks. | A review links one requirement, implementation, and inspected assertion. Changed evidence and broken references produce explicit findings. |
| 3. First brownfield workflow | Complete G7 and the required G5 bindings. Configure one capability and demonstrate agent use. | Save one real gap review. Retain execution bindings when available. An independent reviewer checks one mapping and one finding. |

Each stage must preserve external asset locations and unrelated changes.
Before editing harness symbols, inspect callers and affected CLI/MCP paths.
Add regressions for demonstrated behavioral defects.
Run relevant tests, review the staged scope, and commit each completed stage.

The first workflow needs one versioned requirement, relevant domain/design sources, repository comparison commits, and inspectable test assertions.
Use a graph snapshot when the reviewed behavior crosses service boundaries.
If graph evidence is unavailable, record the affected architecture scope as unresolved.
If execution evidence is unavailable, complete the gap review and record an observation gap.
Use `VERIFIED` only when passing actual execution supports the mapped predicates and their retained identities.

Defer a dedicated interface, agent orchestration, durable workflow scheduling, automated mapping, and broad connector coverage.
Add these capabilities after the first workflow supplies useful review evidence.

## Unresolved project inputs

| Input | Decision owner | Next action |
| --- | --- | --- |
| First business capability and requirement revision. | Business owner. | Select one bounded behavior and its authoritative sources. |
| Source locations, document formats, owners, and approval states. | Source owners. | Supply usable locators and identify missing authority information. |
| Repository identities and base/head commits. | Engineering owner. | Select the exact comparison and its implementation scope. |
| Test engine, assertion source, native reports, and verification environment. | Test owner. | Provide accessible definitions and available actual execution evidence. |
| Coding agent and required operating systems. | Workbench owner. | Select the first integration and the required portability checks. |

This assessment does not require these inputs to define the construction.
The first business workflow requires them or explicit unresolved states.

## Historical validation record

These results belong to the assessed revision and are not current validation evidence.

The standalone test suite passed all 47 tests on macOS.
The initial sandbox run blocked three loopback socket tests.
The rerun with local socket access passed all tests.

The recorded command belongs to the assessed revision:

```text
PYTHONPATH=src ../.venv/bin/python -m unittest discover -s tests -v
```

Run current checks from the standalone source checkout:

```sh
python -m unittest discover -s tests -v
```

The historical command used the parent virtual environment only as the Python executable.
The interface regression checks CLI operation without parent runtime imports.
This assessment did not test Windows, wheel installation, external agent configuration, or actual business E2E execution.
No business repositories, indexes, or generated graph bundles changed.

The harness has no root GitNexus index.
This documentation stage changes the assessment and its README link only.
Its qualitative implementation risk is low.
Documentation validation covers local links, command examples, prose checks, and the staged diff.

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
