# Graph viewer hierarchy

Date: 15 October 2026.
Scope: Organize existing graph evidence by presentation depth.
Consumer: Engineers who inspect repository dependencies through the generated viewer.

## Change and risk

The prior overview mixed system connections with package boundaries.
It also omitted some external API boundaries.
The new viewer separates system connections, interaction details, and package declarations.
The default view shows resolved API, data, and shared-module links between repositories.
The graph retains uncertain relationships in the detail view.

Affected paths include the renderer, presentation model, packaged HTML template, generated viewer, and relationship guide.
The build command calls the renderer before bundle validation and publication.
The CLI and MCP providers continue to query canonical graph evidence.
Qualitative risk is medium because presentation can hide evidence or imply unsupported certainty.
Focused regressions check evidence retention, status separation, filters, and safe source embedding.

The hierarchy controls navigation depth.
It does not establish business criticality or approved business intent.
Canonical nodes, edges, and evidence retain their existing meanings.

## Controls and meanings

| Priority | View | Content |
| --- | --- | --- |
| Highest | System connections | Confirmed, resolved API, data, and shared-module links between repositories. |
| Medium | Interfaces, data, and shared code | API calls, storage access, module imports, handler invocations, and uncertain boundaries. |
| Lowest | Package dependencies | Declared libraries and build tools. |

The legend separates relationship colors, node roles, arrow direction, and provider status.
Filters select repositories, families, provider status, boundaries, exact relationships, and search text.
Sorting changes display order by connection count, name, family, or provider status.
The diagram limits displayed detail to preserve legibility.
The paginated relationship list retains every filtered match.

`Unresolved` means that the extractor could not match a declaration to its provider.
Missing source, configuration, and dynamic expressions can prevent provider matching.
`Ambiguous` means that multiple providers match.
`Candidate` means that a relationship is inferred.
`Declared only` does not establish a provider match.
These states do not establish broken dependencies.

## Findings and limits

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Local browser inspection is blocked. | Browser policy rejects the viewer's `file:` URL. | Visual review remains incomplete. | Unknown. | Review the refreshed viewer manually. |
| Static extraction has coverage limits. | Coverage records unresolved providers and unsupported source layouts. | Presentation cannot establish missing relationships or runtime execution. | Unknown. | Inspect cited source and relevant environment configuration. |
| Complete function reuse is not extracted. | Existing graph edges contain module imports and handler invocations. | Ownership grouping cannot prove function reuse. | Workbench maintainer. | Use source inspection when function-level impact requires evidence. |

## Acceptance checks

```gherkin
Scenario: Start with system connections
  Given a graph contains resolved repository links and package declarations
  When the viewer opens
  Then the selected priority is highest
  And each displayed link has resolved consumer and provider evidence
  And no displayed link is a package dependency

Scenario: Inspect an unresolved API boundary
  Given a GraphQL declaration has no matched provider
  When the user selects interaction details and unresolved provider status
  Then the GraphQL relationship remains available
  And the inspector explains the missing provider match

Scenario: Keep filtered results accessible
  Given more relationships match than the diagram limit permits
  When the user opens the relationship list
  Then every matching relationship remains accessible across pages
  And every listed relationship retains canonical edge IDs and source evidence
```

## Validation

The runtime suite passed 109 tests, including seven viewer regressions.
The wheel build passed.
An external workspace loaded the packaged template and presentation model.
Its initialization, graph build, coverage query, and workspace validation passed.
Shipped guides, schemas, templates, and shared skills remain available.

The regenerated graph contains 961 nodes, 1413 edges, and 1452 evidence records.
Its overview contains eight repository cards and three resolved system links.
All bundle artifact checksums passed.
Source freshness returned `CURRENT`.
Workspace validation returned `VALID`.

The isolated JavaScript check used a DOM substitute.
It checked default priorities, directed labels, repository filters, boundary filters, and family filters.
It also checked unresolved search, package separation, and complete pagination.
All eleven unresolved GraphQL calls remain searchable in the actual graph.
Auth-server Redis declarations remain visible.
The package list exposes 374 declarations across fifteen pages.

These checks do not establish rendered layout quality.
Browser visual inspection remains incomplete because the URL policy blocks local HTML inspection.
The [receipt](../evidence/graph-viewer-hierarchy.json) retains snapshot identity, packaging evidence, and check results.
Retained command outputs include [tests](../evidence/graph-viewer-tests.txt), [graph generation](../evidence/graph-viewer-build.txt), and [wheel construction](../evidence/graph-viewer-wheel-build.txt).

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
