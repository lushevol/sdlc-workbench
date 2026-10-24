# Release report scope and recorded answers

Date updated: 2026-10-24 (Asia/Singapore).
Status: Resolved for implementation from the latest clarification and supplied source.

The [latest design request](evidence/release-report-intake-20261024/api-render-performance-20261024/user-input.md#exact-input) defines API separation and performance concerns.
The [scope clarification](evidence/release-report-intake-20261024/clarification-20261024/user-input.md#exact-input) defines report inputs and Clinic separation.
The [returned question document](evidence/release-report-intake-20261024/clarification-20261024/returned-questions.md) preserves the existing answer and earlier unanswered fields.
The [preparation report](RELEASE_REPORT_REPRODUCTION.md) defines the resulting scope.
No further questionnaire is required for these decisions.
The [API design](RELEASE_REPORT_API_DESIGN.md) records connector reuse, SonarQube handling, renderer isolation, and query scheduling.

## Q1: Target release identity

Recorded answer, preserved exactly:

> only release workitem id is enough, because you can get all other information from query api

Answer source: [returned local answer](evidence/release-report-intake-20261024/clarification-20261024/returned-questions.md#q1-target-release-identity), observed on 2026-10-24.
The [latest chat clarification](evidence/release-report-intake-20261024/clarification-20261024/user-input.md#exact-input) confirms source-derived information retrieval.

Use only the Release work item ID as the report input.
Read project and related identities from query results using existing workspace connection settings.
The [service entry](../core/release-report/release-report.service.ts#L38-L81) derives builds and work items from that release.
The [release query](../core/release-report/ado-api/release.ts#L11-L76) returns fields, build references, and relation IDs.

Resolution: Use the source's Release work item path.
Separate build IDs, stream choices, and baseline selections are not required per-report user inputs.
An actual release ID is execution data, not an unresolved design question.

## Q2: Production baseline

Resolution type: Source-derived behavior, accepted as the implementation baseline under the latest clarification.
This records observed code behavior; it does not invent a new release policy.

Use the supplied production selection conditions:

- The stage named `prod` has numeric result `0`.
- The stage named `rollback_prod` is absent or has numeric result `4`.
- Qualifying candidates are ordered by production stage finish time.
- The first candidate supplies the production branch and commit.
- Compare the release build with its branch tip, `main`, and that production commit.

Evidence: [stage conditions and sorting](../core/release-report/ado-api/pipeline.ts#L80-L162), [baseline selection](../core/release-report/ado-api/git.ts#L123-L145), and [comparisons](../core/release-report/ado-api/git.ts#L287-L429).

Paginate query results and preserve the selected build, stage, time, and commit as evidence.
If the evidence is unavailable, show the comparison as unavailable and retain its reason.
Do not ask the user to supply a substitute baseline merely because collection failed.

## Q3: Compliance scope

Resolution type: Explicit user clarification, dated 2026-10-24.
Source: [latest message](evidence/release-report-intake-20261024/clarification-20261024/user-input.md#exact-input).

Keep the release report and Release Clinic separate.
Release Clinic retains its existing generation procedure, rules, repository, and HTML output.
The release report links its compliance section directly to the matching Clinic HTML.
Do not copy compliance rules, parse Clinic HTML, merge findings, or regenerate verdicts inside the release report.

Preserve the release work item's attachment relations and display matching Clinic HTML attachment names and original URLs.
The [Clinic audit](../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda_audit/run_tda_audit.py#L242-L302) already identifies these attachment names.
The [snippet](../core/release-report/ado-api/release.ts#L11-L19) already requests expanded release relations.
Existing local Clinic output can also supply a direct link when its filename identifies the same release.
See [Clinic output naming](../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/gen_tda_report.py#L1976-L1999).

If no matching HTML exists, display `Release Clinic report unavailable` and continue the release report.
Missing copied compliance modules no longer block this design.

## Q4: Delivery and feature scope

Resolution type: Explicit report purpose with source-derived data scope and a local presentation choice.
Source: [latest message](evidence/release-report-intake-20261024/clarification-20261024/user-input.md#exact-input).

Generate the release report with all information available through its source-defined relationships.
Collect release details, builds, repositories, commits, comparisons, coverage, work items, tests, defects, and relationship evidence.
Include related SonarQube quality data through the [separate source adapter](RELEASE_REPORT_API_DESIGN.md#sonarqube-integration-decision).
Retain complete query results instead of only the original page's selected fields.
Render a standalone report with retained JSON and local HTML as the Workbench implementation choice.
Keep the compliance document separate through direct links.

The [report contract](../core/release-report/release/data/interfaces.ts#L38-L90) supplies the existing report sections.
The [graph contract](../core/release-report/release/data/release-graph.ts#L1-L70) supplies relationship types.
The [complete collection plan](RELEASE_REPORT_REPRODUCTION.md#complete-release-information) identifies richer returned records and attachment contents.
The supplied report path does not upload generated reports to ADO.
Publication and external writes are outside this preparation scope.

No scope answer remains open.
Technical gaps and unavailable execution evidence remain visible in the preparation report.

## Review status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source-derived behavior remains distinct from explicit user statements and execution evidence.
```
