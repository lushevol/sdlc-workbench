# Viewer hierarchy, legend, and filters

The skill owns the viewer template, presentation model, renderer, and regressions.
Keep enhancements under this skill's assets, tools, references, and tests.
Workbench adapters query canonical evidence and do not own presentation rules.

## Presentation levels

| Level | Content | Evidence boundary |
| --- | --- | --- |
| Highest | Confirmed, resolved API, data, and shared-module links between known repositories. | Static matching does not establish deployment or criticality. |
| Medium | APIs, data access, module imports, handler mappings, and uncertain boundaries. | Complete function reuse and execution are not extracted. |
| Lowest | Package and build-tool declarations. | Build dependency does not establish runtime invocation. |

The highest view includes repository cards with interface, configuration, data, code, and unresolved boundary counts.
Card controls open the corresponding repository details without adding canonical relationships.
The connection diagram aggregates canonical links by repository roots, family, direction, and status.
Aggregation retains all canonical edge IDs and source evidence.
Unmatched repositories can remain visible without implying independence.

Ownership and navigation edges remain optional context within the medium view.
The Components view enables ownership context by default.
Inferred containment describes grouping. It does not establish runtime calls.

## Repository exploration

Select a repository and choose Provided APIs, Outbound APIs, Messages, Storage, Configuration, or Components.
The All view retains every owned node within the selected dimension.
The node index includes isolated nodes and supports exact-name search.
Select Runtime, Business, or both dimensions independently from presentation priority.
The Business dimension enables structural context.

Dependency scope selects Production, Testing, or both.
Production is the initial scope. Selecting a testing repository enables its testing declarations.
Testing nodes and relationships retain a `TESTING` label.
Selecting both scopes retains every matching canonical declaration in the indexes.
Testing declarations do not establish execution or passing behavior.

Storage includes extracted entities, tables, columns, access, and mapping relationships.
Configuration includes declared keys, references, bindings, and supported topic configuration.
Component dependencies retain their exact recorded relationship and assertion status.
Imports, injection, mappings, and calls remain distinct.
An empty view can reflect unsupported extraction. Check coverage before claiming absent behavior.

## Legend and uncertainty

Line color identifies API, data, shared code, package, or ownership relationships.
Card markers identify UI, service/library, infrastructure, data, and external/unknown roles.
Arrows follow the recorded relationship.
Calls point toward providers; reads point toward data sources.

Solid lines show resolved or declared-only relationships.
Dashed lines show unresolved or ambiguous relationships.
Dotted lines show inferred candidates.
Inspect badges and canonical fields to distinguish states sharing a line style.

`Resolved` means consumer and provider evidence matched.
`Declared only` means a source relationship exists without a separate provider match.
`Unresolved` means the extractor cannot establish a provider from available evidence.
`Ambiguous` means more than one provider matches.
`Candidate` means the relationship is inferred.

Unknown configuration, missing source, and dynamic expressions can prevent resolution.
Unresolved does not mean broken.
External or unknown targets do not prove third-party ownership.
Declaration confirmation and provider resolution remain separate fields.

## Filters and inspection

Filter by repository, relationship family, provider status, boundary, exact relationship, or search text.
Search covers names, paths, operations, and attached source evidence.
Sort by connection count, name, family, or provider status.
Highest view contains resolved system links; inspect uncertainty in the medium view.

Each diagram page limits nodes and edges for legibility.
Additional pages retain every filtered relationship and indexed node.
No degree ranking can remove a matching item from the complete page sequence.
The node and relationship indexes retain all filtered results across pages.
Select any indexed node to focus its neighborhood, including an isolated node.
Use the return control to restore the complete diagram sequence.

Rendered counts and indexed counts remain separate.
The overview summarizes unresolved, ambiguous, candidate, and declared boundaries outside resolved system links.
Select a relationship to inspect direction, canonical edges, resolution rule, evidence, and IDs.
Node inspection includes kind, dimensions, assertion status, descriptions, source paths, properties, and evidence.
Relationship inspection retains all canonical properties.

## API and client traces

Select an API or client in the trace selector, or use its inspector trace control.
The trace projection retains canonical edge IDs, evidence, selected callsites, and explicit stops.
Exact caller methods restrict API paths to their supported callsites.
Unique local helper calls can continue within the same class.
Deferred callbacks remain declaration context; they cannot become direct method-path steps.

The initial trace hides type, import, and injection context to keep the selected path readable.
Select `Include type/import context` to restore every retained trace node and relationship.
Visible and retained counts remain separate.
The complete canonical indexes remain available when you leave the trace.

`method_path` identifies supported caller-method links.
`implementation_context` shows declared implementation alternatives without selecting runtime dispatch.
`declaration_context` includes type dependencies, imports, and ORM mappings.
`class_context` identifies unscoped class dependencies and legacy calls.
Identity context requires unique repository, qualified type, and concrete source-path evidence.
It does not add a canonical invocation edge.

Missing method evidence, ambiguous declarations, unknown providers, and unselected implementations retain explicit trace breaks.
Each trace permits six hops, 160 nodes, and 240 relationships.
Limit records retain omitted canonical edge IDs.
Canonical indexes remain available beyond the trace limits.
Trace counts measure navigation entries; they do not measure complete behavior coverage.

The diagram wraps complete names and separates APIs, handlers, interfaces, implementations, data access, and external targets.
Configuration, storage, and messages have separate columns.
Directed routes retain relationship labels, including relationships within one role column.
Diagram pagination preserves the complete matching node and relationship indexes.

Inspectors redact secret-bearing property fields and configuration values.
Additional evidence records remain available through an expandable section.
Source evidence limits remain visible when an independent Git revision is unavailable.

Do not merge different protocols, methods, or provider statuses through matching labels.
Keep package boundaries distinct from API targets.
Preserve API, data, and shared-code boundaries even when their providers remain unknown.

## Validation limits

Use skill regressions to check hierarchy, filters, pagination, evidence retention, and safe source embedding.
Check that diagram pages cover every indexed item across API-heavy and mixed-family fixtures.
Check storage, messaging, configuration, component, and business views separately.
DOM logic checks do not establish visual layout quality.
Record visual review separately from syntax and interaction checks.
If browser access blocks observation, state that visual review remains incomplete.
