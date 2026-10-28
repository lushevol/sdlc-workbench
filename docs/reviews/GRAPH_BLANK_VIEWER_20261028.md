# Blank graph viewer

**Action: open the generated relationship graph. The current tab points to its template. Owner: user.**

High-priority intent: [exact user input](../evidence/graph-blank-viewer-20261028/user-input.txt), 28 October 2026.

## Cause and fix

The browser context identifies `.agents/skills/service-dependencies-graph/tools/viewer.html` as the current page.
That file is the reusable template. It contains placeholders instead of graph data.
Its previous startup code passed `__GRAPH__` into `JSON.parse`, then stopped without showing recovery instructions.
The [independent reproduction](../evidence/graph-blank-viewer-20261028/independent-reproduction.json) records this failure and successful initialization of the generated page.

The template now shows a clear notice and a link to the default generated graph.
Invalid embedded JSON also shows recovery instructions instead of an empty diagram.
The workspace and priority controls stay hidden when startup fails.
The skill owns the fix, regression, and viewer guide.
Risk is low. Only startup error handling and its related guidance changed.

Open [the generated graph](../../relationships/service-dependencies/generated/relationship-viewer.html) to inspect the repository relationships.
Its script initializes 6,507 nodes and 17,818 edges.
The first diagram renders 16 nodes and 20 edges, from 24 indexed system relationships.
Pagination retains the remaining indexed relationships.
The [final receipt](../evidence/graph-blank-viewer-20261028/final-verification.json) binds these results to exact viewer and snapshot hashes.
Source and context freshness are `CURRENT`.

## Validation and limits

The [skill suite](../evidence/graph-blank-viewer-20261028/skill-tests.log) passes all 164 tests.
The [Workbench suite](../evidence/graph-blank-viewer-20261028/workbench-tests.log) executes 661 tests with zero failures or errors.
Two optional native connector checks remain skipped.
Regressions check template recovery, malformed JSON recovery, and normal viewer initialization.
The [generated-page probe](../evidence/graph-blank-viewer-20261028/generated-check.log) checks actual generated SVG and startup state.
The [template probe](../evidence/graph-blank-viewer-20261028/template-recovery.log) checks the recovery notice and link.

The [build](../evidence/graph-blank-viewer-20261028/build.log) passes graph and projection validation.
The [wheel build](../evidence/graph-blank-viewer-20261028/wheel-build.log) uses installed dependencies without downloads.
The [isolated wheel smoke](../evidence/graph-blank-viewer-20261028/wheel-smoke.json) passes 13 shipped viewer tests in a fresh workspace.
Only macOS with existing Python dependencies was tested.

The [browser policy](../evidence/graph-blank-viewer-20261028/browser-policy.txt) blocks access to local file URLs.
No alternate browser route or local server was used.
Script checks establish initialization and SVG generation. They do not establish visual layout quality.
The user must select the generated page through the supplied link.

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
