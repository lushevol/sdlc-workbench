# Service graph viewer

Open `relationships/service-dependencies/generated/relationship-viewer.html`.
Keep its sibling `relationship-viewer.data/` folder beside it.
Both belong to the same checksum-backed snapshot.
The viewer uses local files and needs no server or external asset service.
Use a current browser with `DecompressionStream` support for gzip data.

## One graph

The initial map contains service and UI module identities from the saved source graph.
UI modules, gateways, and services have separate layout lanes.
Each directed service pair has one connection line, even when many declarations connect it.
The inspector retains each declaration's protocol, matching status, assessment, and evidence.
Arrows point from the caller or consumer to its dependency.
These static relationships do not establish deployment or runtime execution.

Click a service to focus its callers and dependencies within the same canvas.
Use **Inbound callers**, **Outbound dependencies**, or both directions.
Select one, two, or three hops to inspect upstream and downstream relationships.
Click neighboring services to extend the connected graph progressively.
Use **Load connections** to increase a service's neighborhood in batches of twelve.
Large hubs start with bounded neighborhoods, including when their local peers already appear in the overview.
Use **Focus here** to move the focus to another service. **Overview** restores the complete service map.

Components, methods, individual API operations, tables, configuration keys, and package declarations add no canvas nodes.
Internal and infrastructure declarations remain in service cards and complete declaration indexes.
The collapsed repository inventory includes testing and source-only repositories without inventing runtime service identities.
Multiple explicit services within one repository retain separate identities.
Unowned or ambiguous implementation declarations cannot select the repository's first service.
Unavailable service and UI providers appear as external boundaries when loaded.
Unknown API destinations can share a display group by caller, protocol, and explicit authority.
These groups establish no common provider identity. Their individual destinations remain in the inspector.

Use the wheel to zoom and drag the background to pan.
Use **Fit graph** to fit the current expanded graph.
The desktop workspace fits the viewport. The inspector scrolls independently when details require space.
Small phone screens stack the inspector below the graph.
The architecture inventory, legend, evidence, and extra filters start collapsed.

## Filters and complete indexes

Filter visible declarations by repository, relationship family, provider status, dependency scope, dimension, and assessment.
Search names and recorded paths in the loaded graph.
Use **Browse all declarations** to inspect the complete node or relationship index in bounded batches.
Filters apply within the current index batch. Continue through remaining batches before claiming absence.
A declaration selected from the index opens its source details in the inspector.
It does not add implementation nodes to the canvas.
Isolated canonical nodes remain available through the complete index.

Resolved means consumer and provider evidence matched.
Declared only means a declaration exists without a separate provider match.
Unresolved means a provider could not be matched. It does not mean broken.
Ambiguous means several providers match. Candidate means the relationship is inferred.
Solid lines show resolved or declared relationships. Dashed lines show unresolved or ambiguous links.
Dotted lines identify candidates. Colors identify relationship families.
The inspector retains exact statuses and investigated assessments.
An aggregate containing several statuses retains mixed evidence and a dashed line.
Combined filters must match the same underlying declaration.

## Evidence and traces

Select a relationship to inspect its source and target, family, provider status, and assessment.
Use **Inspect declarations** on a connection to inspect its individual source relationships in bounded batches.
Open **Source details** to load canonical fields and attached source evidence.
Secret-bearing properties and configuration values remain redacted in the inspector.
Source links retain exact recorded paths and independent revisions when available.
Original architecture context remains available under **Architecture evidence**.
Its layers and source details are collapsible.

Select **Trace** on a recorded API or client to inspect its bounded trace and evidence stops.
Traces do not append implementation nodes to the service canvas.
Trace records preserve canonical IDs, selected callsites, method scopes, implementation alternatives, and explicit stops.
Source identity bridges supply declaration context. They do not create canonical call edges.
Type dependencies, unselected implementations, and callbacks do not establish executed API paths.
Each recorded trace retains its existing six-hop, 160-node, and 240-edge bounds.
Open the trace evidence stops and source details before interpreting a complete path.

## Size and performance

The HTML contains the application and repository summary, without canonical evidence or expanded trace bodies.
Local data buckets use deterministic gzip compression through the Python standard library.
The browser loads a bucket only when its content is requested and caches at most eight decoded buckets.
Repeated concurrent requests share one promise. Failed requests clear their loading state and can retry.
Neighborhoods append at most twelve service relationships per action.
Canonical records, evidence, and declaration summaries are stored once in the viewer data.
Neighborhoods contain references to those records.
Trace generation writes each trace as it completes, without retaining the complete trace set in the renderer.

The HTML size follows the service overview size rather than full source evidence size.
The complete data bundle still grows with canonical records, links, and trace evidence.
Compression and lazy loading do not make arbitrary graph sizes constant or prove a memory limit.
One unusually large canonical record can exceed the ordinary 192 KiB logical batch target.
Keep the complete manifest and bundle for CLI queries and checksum verification.

## Validation

Skill regressions check complete navigation, uncertainty, evidence retention, escaping, retries, and compressed data recovery.
The interaction harness executes the shipped JavaScript with a DOM substitute.
Browser verification is separate:

```sh
node .agents/skills/service-dependencies-graph/tests/viewer_browser.cjs PATH_TO_HTML TASK_LOG_DIRECTORY
```

Use `WORKBENCH_GRAPH_BROWSER` to select an already installed browser executable when necessary.
The command uses the existing optional Playwright tooling. It downloads nothing.
It checks viewport overflow, lazy startup, expansion, evidence inspection, and collapse in local Chromium.
Record the actual browser version and platform. Unchecked browsers remain explicit limits.
