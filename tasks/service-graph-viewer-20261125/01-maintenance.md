# Service graph viewer and bundle size

Date: 25 November 2026. Source: current Codex chat, session `01a2134f-8a1e-7332-a4ab-3d0d409e0e1a`.

> **Current conclusion:** The progressive viewer is implemented and verified. The scoped change is ready for handoff.
> Owner: Codex for implementation. Human acceptance remains pending.

## Exact user input

```text
The Service Dependency Graph HTML output isn't great. First, there are way too many titles and subtitles. Delete all the unnecessary subtitles, and use layout and UI to convey the functionality instead. Ideally, the entire layout should fit on a single screen without needing to scroll. The second thing I'm really unhappy with is the graph for the Shenzhen services. You've split it up into way too many pieces. If you want to do lazy loading, here's how you should handle it:\
\
1\. For the top-level view, show an overall relationship map of all the reports.\
2\. When you click into a specific repo or service, it should expand to show its dependencies on other services.\
3\. Then let users click to expand further and load things progressively as needed.\
\
I don't want to switch between different diagram. I want everything displayed within a single graph. You'll just need to figure out a way to handle the performance side of it.

3\. The Inspect Unresolved feature: I couldn't see what it does, and clicking it just freezes and becomes unresponsive. If it's not useful, let's remove it.\
4\. The extra descriptions: These aren't really necessary. You can hide them so they aren't displayed all the time; this kind of legend doesn't need to stay on screen.\
5\. The architecture overview: This is too abstract, and the diagram doesn't fit on the screen properly with all the services listed out. Can we make those collapsible?

Please think carefully about how to improve these things: first walk me through your plan, and then implement it. Finally, we need to consider a new issue.\
\
The HTML we're currently generating, if there are too many reports, could reach several hundred megabytes or even a gigabyte. That's way too big.
```

## Scope and starting state

Workbench harness maintenance only. Existing business graph facts keep their canonical meaning.
Starting revision: `82d943adc`. Branch: `feature/knowledge-layout-consolidation`.
The worktree was clean. A successful elevated `git fetch --all` followed an initial sandbox denial.
Compared with `origin/feature/knowledge-layout-consolidation`, HEAD is six commits ahead and zero behind.
These unpublished commits concern learning, freshness, diagrams, and agent settings. They remain outside this task.

Consumers include graph build, standalone renderer, snapshot validation, CLI/provider queries, and installed skill assets.
The viewer currently embeds the full graph, presentation metadata, precomputed traces, and architecture context.
Its diagram pagination and extensive permanent descriptions conflict with the requested interaction.
Risk is moderate: navigation and artifact packaging change together. Evidence, uncertainty, filters, and source escaping require preservation.

## Plan shared before implementation

1. Use one viewport-height workspace, compact controls, and an on-demand inspector.
2. Expand dependencies progressively in one graph. Preserve the repository map and collapse expanded branches.
3. Collapse architecture inventory and optional explanatory content.
4. Remove the freezing unresolved shortcut. Keep uncertainty through normal filtering and inspection.
5. Keep a small HTML entry point with sibling data loaded only when requested.
6. Verify graph interaction, payload growth, artifact integrity, and installed distribution behavior.

The plan interprets “reports” as all repositories within the generated graph snapshot.
No Shenzhen-specific names or topology will enter the reusable renderer.
No learning promotion, new external dependency, business publication, or deployment is requested.

## Implemented result

The viewer uses one graph and a compact desktop workspace.
Every repository remains in the initial map, including disconnected inventory roots.
Repository clicks reveal dependency groups. Further clicks load direct neighborhoods in that graph.
Each action appends at most twelve entries. Duplicate identities share one node or relationship.
Collapse removes branches while retaining nodes referenced elsewhere.
The graph supports pan, zoom, fit, and viewport culling.

Removed diagram pagination, repeated page subtitles, and the unresolved shortcut.
The architecture inventory, legend, detailed filters, and source fields start collapsed.
Provider uncertainty remains available through filters, indexes, source edges, and the inspector.
Navigation groups explicitly add no canonical relationship or runtime call.

The HTML contains the application and repository summary.
Compressed local buckets hold shared declaration summaries, canonical records, evidence, and trace records.
Neighborhoods reference shared summaries instead of copying them.
The browser caches eight decoded buckets and shares concurrent requests.
Failed loads can retry. Failed rendering preserves the prior viewer and its data.
No external package or server was added.

## Size evidence

The [verification receipt](evidence/verification.json) binds sizes, sources, commands, browser results, and file hashes.
Sizes below use decimal bytes. They describe viewer files, excluding the canonical query bundle.

| Saved snapshot | Previous HTML | New HTML | Compressed viewer data |
| --- | ---: | ---: | ---: |
| 11 repositories; 8,548 nodes; 22,142 edges | 35,666,309 | 65,600 | 12,621,208 |
| 13 repositories; 2,456 nodes; 4,259 edges | 5,244,378 | 73,915 | 2,775,612 |

The default viewer and its manifest were replaced from the saved snapshot.
All 65 prior canonical artifacts retained their bytes.
The canonical graph SHA-256 remains `5e279be68c412718731268b29c436d0f9773972412e0cd7314e6397afe82b1fc`.
The settlement-service snapshot has a task-local preview. Its original external bundle remains unchanged.

Keep the HTML beside its `.data/` directory.
The complete viewer data still grows with evidence. No gigabyte-scale performance result is claimed.

## Verification and recoveries

The final complete suite passed 1,177 tests without failures, errors, skips, or expected failures.
Command: `WORKBENCH_CONNECTOR_INTEGRATION=1 PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python -m unittest discover -s tests -v`.
The final focused viewer suite passed all 18 tests.
The broader graph suite passed 245 tests before the final data normalization.
The final complete suite includes those graph regressions.

Chromium `151.0.7922.34` passed both saved-snapshot browser cases.
The desktop layouts fit 1024×768, 1366×768, and 1440×900 without page overflow.
Each startup made zero data-script requests.
Cases checked expansion, additional batches, unique identities, retained roots, evidence inspection, and collapse.
[Service overview](evidence/service-overview.png) and [repository expansion](evidence/repository-expanded.png) retain the visual result.

The wheel built successfully with `--no-deps --no-build-isolation`.
Its critical source assets matched the checked worktree bytes.
An isolated installation initialized a workspace and generated a checksum-verified graph bundle.
Its services query succeeded. Workspace validation returned `VALID`.
The source workspace also passed validation for 119 documents.
Documentation checks found no broken local targets across 152 links. Diff whitespace checks passed.

The first full run hit local socket restrictions. The unrestricted mock-server run passed.
Two initial viewer harness assumptions were corrected using identity and real select behavior.
The first wheel probe incorrectly rejected generated responsibility guides under `core/`.
The corrected probe checks absent runtime source, package manifests, and runtime tests.
An initial refresh candidate copied its old manifest and failed its self-checksum.
A fresh candidate excluded that old manifest. All checks passed before the local replacement.
The receipt and compressed original logs preserve these failures and their corrections.

## Current documentation and ownership

Updated the canonical graph skill and its existing viewer guide.
Updated `docs/DEPENDENCIES.md`, `docs/SETUP.md`, and the graph section in `docs/WORKSPACE_DESIGN.md`.
Updated `relationships/service-dependencies/README.md`.
The canonical graph schema and CLI/provider query contracts remain unchanged.

Unrelated Requirement Grill work appeared during execution and was committed separately as `91e9a3273`.
Those files remain outside this task. Final verification uses that existing base commit.
The latest fetched comparison showed one unrelated local commit ahead and zero incoming commits.
No pull, merge, rebase, or reset was performed.

Capability retrieval found no matching registry entry.
The task reused existing graph, trace, manifest, and publication controls.
No registry rule, global preference, experience packet, or business knowledge was promoted.
Direct implementation follows the user's explicit request.

## Limits and handoff

The generated views describe saved static snapshots. Business sources were not refreshed or runtime-verified.
Safari, Firefox, Windows, and phone layouts remain unverified.
A single large canonical record can exceed the ordinary logical batch target.
Human visual acceptance remains separate from passing automated checks.
Effective settings remain automatic commits, per-stage granularity, plain messages, and full Ponytail mode.
Next: use the updated viewer. Human visual acceptance remains pending.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
