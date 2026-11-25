# Progressive graph viewer

Open `relationships/service-dependencies/generated/relationship-viewer.html`.
Keep its sibling `relationship-viewer.data/` folder beside it.
Both belong to the same checksum-backed snapshot.
The viewer uses local files and needs no server or external asset service.
Use a current browser with `DecompressionStream` support for gzip data.

## One graph

The initial map contains every repository, including disconnected inventory roots.
Repository links aggregate canonical relationships by endpoints, family, scope, and evidence status.
These links retain separate provider matching and investigation assessments.
They do not establish deployment or runtime calls.

Click a repository to expand its dependency groups inside the graph.
Click an API, data, shared-code, configuration, package, or ownership group to load its first batch.
Click individual services or declarations to expand their direct neighborhoods.
Use **Load more** to append another batch to the existing graph.
Previously loaded branches remain visible. Duplicate nodes and edges share one identity.
Click an expanded node to collapse its branch. Shared nodes remain when another branch references them.
Use **Collapse all** to restore the repository map.

Groups describe navigation only. They add no canonical service or relationship.
Group records are explicitly separate from canonical source declarations.
Source-only repositories remain inventory identities without inferred runtime providers.

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
A node selected from the index can expand its neighborhood in the same graph.
Isolated canonical nodes remain available through the index and repository groups.

Resolved means consumer and provider evidence matched.
Declared only means a declaration exists without a separate provider match.
Unresolved means a provider could not be matched. It does not mean broken.
Ambiguous means several providers match. Candidate means the relationship is inferred.
Solid lines show resolved or declared relationships. Dashed lines show unresolved or ambiguous links.
Dotted lines identify candidates. Colors identify relationship families.
The inspector retains exact statuses and investigated assessments.

## Evidence and traces

Select a relationship to inspect its source and target, family, provider status, and assessment.
Expand source edges from an aggregate link to inspect its individual declarations.
Open **Source details** to load canonical fields and attached source evidence.
Secret-bearing properties and configuration values remain redacted in the inspector.
Source links retain exact recorded paths and independent revisions when available.
Original architecture context remains available under **Architecture evidence**.
Its layers and source details are collapsible.

Select **Trace** on a recorded API or client to append its bounded dependency trace to this graph.
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
Neighborhoods append at most twelve entries per action.
Canonical records, evidence, and declaration summaries are stored once in the viewer data.
Neighborhoods contain references to those records.
Trace generation writes each trace as it completes, without retaining the complete trace set in the renderer.

The HTML size follows repository summary size rather than full source evidence size.
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
