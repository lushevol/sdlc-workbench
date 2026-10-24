# Supplied release report UI analysis

The [preserved request](user-input.md#exact-input) defines this preparation scope.
The supplied files are reference evidence, not an installed Workbench feature.
This review inspected source and assertions only.
It did not execute the UI, its tests, or ADO requests.

## Observed views and contracts

| Area | Observed behavior | Source |
| --- | --- | --- |
| Release board | Select dates, move seven days, and open release details. Default dates span today through seven days later. | [Board queries](../../../core/release-report/release/board.tsx#L59-L81), [navigation](../../../core/release-report/release/board.tsx#L95-L183). |
| Board approvals | Show PO, TSO, and TSUO approvals. Security Champion approval is commented out. | [Approval fields](../../../core/release-report/release/board.tsx#L23-L57), [approval display](../../../core/release-report/release/board.tsx#L196-L205). |
| Detail header | Show release title, ID, planned date, state, release approach, and nature of change. | [Header](../../../core/release-report/release/details.tsx#L95-L189). |
| Work items | Show ID, title, type, state, test execution counts, and defect status counts. | [Work-item table](../../../core/release-report/release/details.tsx#L195-L339). |
| Build cards | Show repository, branch, comparison controls, and available ADO line and branch coverage. | [Build cards](../../../core/release-report/release/details.tsx#L351-L451). |
| Coverage | Hide cards when both current coverage values are unavailable. Show percentage differences only when both values exist. | [Coverage guards](../../../core/release-report/release/details.tsx#L480-L504). |
| Compliance | Show backend overall status, summary counts, expandable checks, gaps, and correction guidance. | [Compliance component](../../../core/release-report/release/components/ReleaseComplianceAudit.tsx#L33-L131). |
| Report API | Fetch `/api/oct/release-report-api/:id` with a three-minute timeout and ten-second stale time. | [Report query](../../../core/release-report/release/api/queryRelease.ts#L8-L25). |
| Board API | Query release IDs and release fields through `/api/oct/graphql`. | [List query](../../../core/release-report/release/api/queryRelease.ts#L27-L50), [release query](../../../core/release-report/release/api/queryRelease.ts#L125-L142). |

Board approval values use an exact `Yes` comparison.
Performance Testing indicates declared scope, not a passing test result.
See [board status logic](../../../core/release-report/release/board.tsx#L196-L209).
The detail page sorts five named infrastructure repositories last; it does not hide them.
See [repository list](../../../core/release-report/release/details.tsx#L14-L20) and [sort](../../../core/release-report/release/details.tsx#L364-L373).

## Optional release graph

The [feature flag](../../../core/release-report/release/details.tsx#L30-L32) controls whether the graph section appears.
The graph query starts after the operator expands the section.
Collapsing disables the query and clears the selection.
See [query and state logic](../../../core/release-report/release/components/ReleaseGraphSection.tsx#L40-L66).

The graph has repository, commit, file, story, and test-case nodes.
Edges hold optional file paths and changed line ranges.
See [graph contract](../../../core/release-report/release/data/release-graph.ts#L1-L70).
The [mapper](../../../core/release-report/release/components/release-graph-mapper.ts#L84-L110) passes nodes and edges to ECharts.
The [canvas](../../../core/release-report/release/components/ReleaseGraphCanvas.tsx#L84-L144) uses a force layout with pan and zoom.
The [detail panel](../../../core/release-report/release/components/ReleaseGraphDetails.tsx#L24-L105) displays selected node fields or edge line ranges.

The graph request uses a separate `/api/oct/release-graph-api/:id` endpoint.
See [graph query](../../../core/release-report/release/api/queryReleaseGraph.ts#L6-L24).
The supplied files contain its consumer and data contract.
They do not contain its controller or graph producer.
Reproducing graph collection needs additional source or a new implementation.

## Compliance presentation

The UI maps fourteen named backend checks to five gate groups.
Five check types become critical only when their status is `FAIL`.
Missing mapped checks become `INFO`.
See [check metadata](../../../core/release-report/release/data/compliance-audit.ts#L118-L152) and [card construction](../../../core/release-report/release/data/compliance-audit.ts#L287-L308).

Additional backend checks contribute to failure, warning, and pass totals.
The UI displays only their count, not their individual detail.
See [overview](../../../core/release-report/release/data/compliance-audit.ts#L250-L284) and [additional signals](../../../core/release-report/release/components/ReleaseComplianceAudit.tsx#L121-L130).
The backend determines overall compliance.
This UI does not establish human deployment authorization.

## Reproduction findings

### UI-1: Host application files are missing

Fact: The page imports routes, layouts, UI controls, generated GraphQL types, and credential helpers outside the supplied tree.
See [detail imports](../../../core/release-report/release/details.tsx#L1-L12), [board imports](../../../core/release-report/release/board.tsx#L1-L21), and [query imports](../../../core/release-report/release/api/queryRelease.ts#L1-L6).
No `package.json`, frontend entry point, route implementation, or API controller exists in the supplied tree.
The exact host package versions and aliases are unknown.

Consequence: The supplied UI cannot run as a standalone project.
Owner: Workbench maintainer; individual unknown.
Next action: Reproduce report data first, then select a local report renderer within Workbench boundaries.

### UI-2: The specification differs from the current page

Fact: The [supplied specification](../../../core/release-report/release/docs/RELEASE_REPORT_PAGE_SPEC.md#L10-L47) requests breadcrumbs, deployment status, build timestamps, and Sonar issue details.
The [current page](../../../core/release-report/release/details.tsx#L95-L451) lacks these sections or fields.
It includes compliance cards, work-item counts, branch comparisons, and ADO coverage instead.
The available report type carries build metadata but no Sonar issue collection.
See [report contract](../../../core/release-report/release/data/interfaces.ts#L38-L78).

Consequence: Copying the old specification would misstate source feature parity.
Owner: Workbench maintainer; individual unknown.
Next action: Separate observed parity from optional additions in the implementation plan.
Unknown: Whether the original application had other report pages or export functions.

### UI-3: Graph incompleteness is hidden

Fact: The [graph response](../../../core/release-report/release/data/release-graph.ts#L58-L69) includes warnings, unresolved story IDs, and unlinked commits.
The [mapper](../../../core/release-report/release/components/release-graph-mapper.ts#L84-L110) excludes all metadata.
The [section](../../../core/release-report/release/components/ReleaseGraphSection.tsx#L109-L143) displays the graph without these warnings.

Consequence: A partial relationship graph can appear complete.
Owner: Workbench maintainer; individual unknown.
Next action: Keep counts, warnings, unresolved IDs, and unlinked commits visible in the new report contract and renderer.

### UI-4: Comparison results lack a consistent unavailable state

Fact: [Latest commit logic](../../../core/release-report/release/components/BuildDiffStatus.tsx#L56-L70) treats absent counts as an issue.
[Main comparison logic](../../../core/release-report/release/components/BuildDiffStatus.tsx#L72-L92) passes an empty non-null comparison.
[PROD logic](../../../core/release-report/release/components/BuildDiffStatus.tsx#L94-L145) can pass unavailable change counts.
This follows the inspected JavaScript conversion and default branches.
No execution evidence confirms how often collectors produce these inputs.

Consequence: Missing evidence can become a success or a misleading mismatch.
Owner: Workbench maintainer; individual unknown.
Next action: Represent unavailable, failed, excluded, and evaluated comparisons separately.

### UI-5: Source URLs and credential handling are host-specific

Fact: [Detail links](../../../core/release-report/release/details.tsx#L113-L118) and [build links](../../../core/release-report/release/details.tsx#L380-L397) hardcode one ADO organization and project.
The [query](../../../core/release-report/release/api/queryRelease.ts#L16-L18) sends a browser credential or `VITE_ADO_TOKEN` fallback.
The credential helper implementation is absent.

Consequence: Direct reuse can select incorrect links and require browser-held credentials.
Owner: Workbench maintainer; individual unknown.
Next action: Derive links from selected workspace configuration and reuse Workbench server-side credential boundaries.

### UI-6: Some compliance evidence text does not expose its deciding field

Fact: [Evidence construction](../../../core/release-report/release/data/compliance-audit.ts#L326-L369) uses deployment counts for rollback documentation.
It uses release state for signed control documents and security status.
It uses planned release date for assessment validity.
The displayed result itself comes from backend checks.

Consequence: The operator cannot inspect the decisive value through these evidence strings.
Owner: Workbench maintainer; individual unknown.
Next action: Include exact deciding fields and source locators with evaluated checks.

## Inspected assertion coverage

The supplied [test file](../../../core/release-report/release/components/ReleaseGraphSection.test.tsx#L300-L539) defines twelve tests.
These assertions cover the following items:

- Graph query key, timeout, token selection, disabled default, stale time, and returned data.
- Graph edge mapping for source, target, and line ranges.
- The empty selection message.
- Disabled query before expansion and enabled query after expansion.
- Disabled query after collapse and the retry callback.
- Commit selection details and edge path with line ranges.
- Graph feature flag visibility.
- Hidden coverage cards when current coverage is absent.

The query test names token fallback, but it asserts only the local-token path.
See [query assertions](../../../core/release-report/release/components/ReleaseGraphSection.test.tsx#L300-L332).
The suite mocks React Query and ECharts.
See [chart mock](../../../core/release-report/release/components/ReleaseGraphSection.test.tsx#L35-L88) and [query mock](../../../core/release-report/release/components/ReleaseGraphSection.test.tsx#L90-L99).
It does not establish network fetching, cancellation, chart layout, or ADO response parity.
The detail suite mocks build comparisons and compliance presentation.
See [component mocks](../../../core/release-report/release/components/ReleaseGraphSection.test.tsx#L145-L151).

No supplied assertions verify compliance rules, branch comparison classifications, board errors, responsive layout, or keyboard access to graph selections.
No test execution result was supplied or produced in this review.
The absent host manifest and imported host files prevent a supported standalone test command.

## Verification and review

The automated inspection counted test declarations and checked linked source locations.
The check does not execute TypeScript or validate rendered behavior.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Static source inspection does not establish runtime behavior or passing UI tests.
```
