# Dependency graph skill ownership correction

Date: 15 October 2026.
Scope: Make the manually imported skill own the complete dependency graph capability.
Consumer: Engineers and agents that build, inspect, or change repository dependency graphs.

## Ownership and risk

The project owner imported the original skill in commit `0cb621f8725b3defafed0afb62ab8f6037bcabde`.
Its imported launchers still required the parent harness.
The earlier Workbench implementation also placed enhancements outside the imported skill.

The [canonical skill](../../.agents/skills/service-dependencies-graph/SKILL.md) now owns extraction, resolution, queries, schema, validation, viewer assets, references, and regressions.
The standalone runner requires installed third-party dependencies but does not require Workbench or the parent harness.
Workbench build and query adapters invoke the local skill helpers.
The installed package supplies a fallback skill for workspaces without a local copy.

This stage removes the retired core engine and duplicate procedure tree.
Discovery links expose the canonical skill through `skills/` and `.claude/skills/`.
Initialization creates forwarding documents when a platform denies directory links.
Packaging ships one physical skill implementation.

Affected interfaces include CLI builds, MCP queries, provider schemas, skill discovery, initialization, and packaging.
Callers and imports were inspected directly because this checkout has no usable code index.
Qualitative risk is medium because incorrect delegation can select stale code or omit shipped files.
Regression checks cover local precedence, independent execution, evidence retention, and package contents.

## Graph behavior

The viewer retains hierarchy, legends, arrows, search, filtering, sorting, inspection, and complete result pagination.
Highest priority shows confirmed, resolved static interactions between repositories.
Medium priority shows API calls, data access, shared modules, handlers, and uncertain boundaries.
Lowest priority shows package and build-tool declarations.

These priorities control presentation depth.
They do not establish business criticality.
Unresolved means that available static evidence cannot identify a provider.
It does not establish a broken dependency.

The actual repository graph was regenerated through the standalone skill command.
It contains 961 nodes, 1413 edges, and 1452 evidence records.
Coverage inventories nine repositories and exposes eight analysis roots.
The overview retains three resolved repository links.
Eleven GraphQL calls remain unresolved, and 374 package declarations remain available.
The source freshness query returned `CURRENT` within the recorded inventory exclusions.

## Evidence and findings

[Registered raw archives](../../knowledge/raw/service-dependencies-graph/) retain exact imported and previous procedure bytes.
The raw manifest retains their exact source commit and archive hashes.
A [new audit event](../../knowledge/audit/AUD-20261015-SKL-service-dependencies-graph-v4.yaml) registers procedure version 3 as a candidate.
Prior audit events remain unchanged.
This event does not claim human knowledge approval.

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Imported launchers required the parent harness. | Original blobs in the manual-import archive. | The imported skill could not run independently. | Workbench maintainer. | Use the standalone runner and keep enhancements inside the skill. |
| Reused build output retained the retired engine. | Wheel inspection and the new packaging regression. | An installation could include duplicate graph implementations. | Workbench maintainer. | Clear only package staging before each build. The regression now checks this boundary. |
| Some static providers remain unknown. | Generated coverage and unresolved boundary records. | The graph cannot establish those provider relationships. | Unknown. | Inspect cited source and environment identities before resolving them. |
| Visual browser inspection remains incomplete. | The earlier browser policy rejected the local viewer URL. | Automated interaction checks do not establish rendered layout quality. | Unknown. | Inspect the regenerated viewer manually. |
| Windows execution remains untested. | Validation ran on macOS; directory-link denial was simulated. | Platform execution has a remaining evidence limit. | Workbench maintainer. | Run installed-workspace checks on Windows when that environment is available. |

## Acceptance checks

```gherkin
Scenario: Execute the copied skill independently
  Given a copied skill and three local fixture repositories
  And imports of Workbench and the parent harness are denied
  When the standalone runner builds and queries the graph
  Then all commands succeed
  And the graph retains a resolved API link with source evidence
  And every generated artifact matches its manifest checksum

Scenario: Apply a local skill enhancement through Workbench
  Given an installed Workbench and an initialized workspace
  And the workspace skill viewer contains a local marker
  When the installed graph build adapter runs
  Then the generated viewer contains that marker
  And query schema discovery uses the workspace skill

Scenario: Ship one graph implementation
  Given stale files from the retired graph engine exist in package staging
  When the package build runs
  Then the wheel contains one canonical skill implementation
  And the retired core engine is absent
  And initialization creates discovery links to the canonical skill

Scenario: Return a structured invalid snapshot result
  Given a graph manifest has no generated_at field
  When the standalone query command reads the snapshot
  Then it returns ERROR with code INVALID_SNAPSHOT
  And it emits no traceback
```

## Validation

The full runtime suite passed 115 tests.
The skill validator and automated writing checks passed.
Workspace validation returned `VALID` with no findings.
Direct graph generation, checksum verification, validation, and freshness comparison passed.

The wheel built with locally installed build dependencies after isolated dependency retrieval failed.
An external installation initialized and validated a workspace.
Its standalone skill build, query, local viewer enhancement, adapter build, and retained query action passed.
Shipped guides, schemas, templates, and skill files remained available.
The source distribution also built a wheel with one canonical skill and no retired engine.

The [validation receipt](../evidence/graph-skill-ownership.json) records checks and snapshot identity.
Retained outputs include [tests](../evidence/graph-skill-ownership-tests.txt), [generation](../evidence/graph-skill-ownership-build.txt), and [wheel construction](../evidence/graph-skill-ownership-wheel.txt).
Unrelated template changes remain outside this stage.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
