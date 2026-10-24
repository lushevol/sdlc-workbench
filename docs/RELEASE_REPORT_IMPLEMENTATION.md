# Release report implementation

Date: 2026-10-24 (Asia/Singapore).
Status: Complete for the authorized implementation and mock verification scope.

**Collection, retained report data, and offline HTML rendering are implemented. No implementation blocker remains within the authorized mock scope.**

Live ADO, SonarQube, and native Windows compatibility remain untested.
The [implementation request](evidence/release-report-implementation-20261024/user-input.md#exact-input) requires mock data.
The [continuation request](evidence/release-report-implementation-20261024/continuation-user-input.md#exact-input) resumes the prior chat's authorized work.
Use the [current guide](RELEASE_REPORT.md) for setup, commands, configuration, and evidence limits.
Open the [redesigned report](evidence/release-report-implementation-20261024/ui-redesign/release-501.html) to inspect the output.
Its service links identify an expired local fixture.

The [UI redesign request](evidence/release-report-implementation-20261024/ui-redesign-user-input.md#exact-input) defines the completed presentation change.

## Report presentation

The redesign follows the supplied [release details page](../core/release-report/release/details.tsx#L95-L205).
The header shows essential release fields. Optional empty metadata stays hidden.
A compact attention panel highlights failed checks and their recorded reasons.
Build cards show execution outcomes, branch alignment, coverage, and production deltas.
Work item tables, comparisons, and raw evidence use closed disclosures.

The [source review](evidence/release-report-implementation-20261024/ui-redesign/reference-review.json) records the reused layout and source check semantics.
The [UI cases](../tests/test_release_report_render.py) define and assert the presentation boundaries.
The [check cases](../tests/test_release_report_checks.py) define and assert failure explanations and unavailable evidence.
The [report execution](evidence/release-report-implementation-20261024/ui-redesign/report-validation.json) retains their actual execution with collection integration.
The [browser checks](evidence/release-report-implementation-20261024/ui-redesign/failure-visual-validation.json) inspect desktop, mobile, and expandable details.
The [UI review](evidence/release-report-implementation-20261024/ui-redesign/review.json) records corrected Sonar association and unavailable-count defects.
The [redesigned report](evidence/release-report-implementation-20261024/ui-redesign/release-501.html) uses the prior mock snapshot unchanged.
The [failure preview](evidence/release-report-implementation-20261024/ui-redesign/failure-preview.html) adds explicitly synthetic build, gate, and denied-read failures.

The affected scope is the offline renderer and its pure presentation checks.
Qualitative risk is medium because failure labels affect interpretation of retained evidence.
Sonar cards retain each build association and identify partial counts as retained records.
The [final validation](evidence/release-report-implementation-20261024/ui-redesign/final-validation.json) records runtime, package, and workspace checks.

## Evidence index

| Evidence | Result and purpose |
| --- | --- |
| [Document checks](evidence/release-report-implementation-20261024/document-validation.json) | Local links and new prose sentence limits passed. Full ASD review remains pending. |
| [Runtime validation](evidence/release-report-implementation-20261024/runtime-validation.json) | 645 tests ran. The suite passed with two optional connector checks skipped. |
| [Optional connector checks](evidence/release-report-implementation-20261024/native-connector-validation.json) | Both skipped checks passed in a separate enabled run. |
| [Connector validation](evidence/release-report-implementation-20261024/connector-validation.json) | All 25 Node tests passed. |
| [Integration validation](evidence/release-report-implementation-20261024/integration-validation.json) | All 19 report integration cases passed against loopback services. |
| [Per-case execution](evidence/release-report-implementation-20261024/integration-cases.json) | Each completed integration case has retained execution and source identities. |
| [Assertion map](evidence/release-report-implementation-20261024/integration-case-map.json) | Exact assertion locations, source hashes, canonical cases, and coverage limits. |
| [Renderer validation](evidence/release-report-implementation-20261024/renderer-validation.json) | All 14 renderer and contract cases passed. |
| [Configuration regression](evidence/release-report-implementation-20261024/local-config-validation.json) | An empty process value overrides the root Clinic output setting. |
| [Synthetic comparison](evidence/release-report-implementation-20261024/synthetic-benchmark.json) | Serial and scheduled collection retained equivalent data and 36 HTTP attempts. |
| [Wheel build](evidence/release-report-implementation-20261024/wheel-validation.json) | The wheel built with existing dependencies and package-index access disabled. |
| [Installed wheel checks](evidence/release-report-implementation-20261024/installed-wheel-final-validation.json) | An external temporary workspace passed collection, verification, and deterministic rendering. |
| [Visual checks](evidence/release-report-implementation-20261024/visual-validation.json) | Desktop and mobile pages had no page overflow or network attempts. |
| [Independent review](evidence/release-report-implementation-20261024/final-review.json) | No actionable defects remained in the inspected Python and interface scope. |
| [Mock manifest](evidence/release-report-implementation-20261024/mock-report/manifest.json) | Retained snapshot and request evidence with byte counts and SHA-256 values. |

## Scope and risk

This change maintains Workbench tooling. It requires no business task or domain knowledge publication.
Affected interfaces include the report provider, CLI, connector readers, session transport, snapshot contract, renderer, catalogs, and installed guides.
Qualitative risk is medium because collection crosses permission, process, concurrency, and evidence boundaries.
The [review](evidence/release-report-implementation-20261024/final-review.json) records inspected consumers and exact source hashes.
The original supplied source remains unchanged and untracked under `core/release-report/`.
Release Clinic implementation files remain unchanged.

## Implemented behavior

One Release work item ID derives builds, supported related work items, tests, defects, coverage, comparisons, commits, and files.
The collector preserves returned fields and failed identities.
Commit-discovered work items also expand their supported child and test links.
Failed Sonar pages retain completed pages and mark that section partial.
Test counts remain separate for each build because no aggregation rule is configured.

The Python collection API dispatches through the registered `release.report` provider.
CLI and MCP use the same grants and retained action contract.
The renderer reads saved evidence and makes no external requests.
It rejects modified artifacts, contradictory identities, unsafe links, and attempts to replace Clinic content.
The HTML records the input snapshot hash.

ADO and Sonar readers reuse native connector configuration, credentials, proxy handling, and declared Node dependencies.
Each required source has one transient session, HTTP client, and connection pool set.
Raw REST readers permit limits on actual HTTP attempts.
Existing SDK-based tools retain their contracts.
This refines the earlier [API design](RELEASE_REPORT_API_DESIGN.md#implemented-refinements) without adding a package dependency.

Collection batches unique work item IDs and shares duplicate requests.
It follows pages, applies deadlines, respects throttling delays, and reduces concurrency after throttling.
Large responses stream into hashed evidence files.
A prior manifest can trigger fresh collection and revision comparison through `--resume`.
Mutable responses are not reused between collections.

## Verification boundaries

The [assertion map](evidence/release-report-implementation-20261024/integration-case-map.json) distinguishes exact case coverage from related boundary checks.
The cases retain their canonical definitions:
[RR-1](RELEASE_REPORT_REPRODUCTION.md#rr-1-preserve-a-failed-build),
[RR-2](RELEASE_REPORT_REPRODUCTION.md#rr-2-preserve-an-unknown-production-baseline),
[RR-3](RELEASE_REPORT_REPRODUCTION.md#rr-3-keep-duplicate-requirement-evidence),
[RR-4](RELEASE_REPORT_REPRODUCTION.md#rr-4-replay-retained-evidence),
[RR-5](RELEASE_REPORT_REPRODUCTION.md#rr-5-preserve-graph-limits),
[RR-6](RELEASE_REPORT_REPRODUCTION.md#rr-6-derive-report-identities),
[RR-7](RELEASE_REPORT_REPRODUCTION.md#rr-7-link-separate-compliance-content), and
[RR-8](RELEASE_REPORT_REPRODUCTION.md#rr-8-continue-without-a-compliance-document).
Performance boundaries retain separate definitions:
[RR-P1](RELEASE_REPORT_API_DESIGN.md#rr-p1-batch-unique-work-item-identities),
[RR-P2](RELEASE_REPORT_API_DESIGN.md#rr-p2-bound-actual-requests-and-reuse-sessions),
[RR-P3](RELEASE_REPORT_API_DESIGN.md#rr-p3-respect-a-delay-on-a-successful-response),
[RR-P4](RELEASE_REPORT_API_DESIGN.md#rr-p4-apply-grants-before-cached-data-access),
[RR-P5](RELEASE_REPORT_API_DESIGN.md#rr-p5-retain-evidence-larger-than-one-tool-response), and
[RR-P6](RELEASE_REPORT_API_DESIGN.md#rr-p6-resume-without-concealing-changed-sources).

The synthetic comparison used the same fixture and response coverage in both schedules.
The [measurement record](evidence/release-report-implementation-20261024/synthetic-benchmark.json) retains synthetic durations for both schedules.
Each run made 36 HTTP attempts and shared 20 duplicate requests.
Observed ADO concurrency changed from one to six.
Sonar requests coalesced, so the comparison did not saturate its two-request limit.
Separate connector tests exercised that bound.

The installed wheel initialized a workspace outside this checkout.
The workspace received guides, schemas, templates, skills, and empty catalogs.
It received no runtime source or `pyproject.toml`.
The installed command collected the fixture release and verified every declared evidence artifact.
Two renders produced identical HTML hashes and zero additional HTTP requests.

## Resolved defects

| Evidence | Consequence before correction | Owner | Completed action |
| --- | --- | --- | --- |
| [Initial change-page failure](evidence/release-report-implementation-20261024/mock-capped-pages-initial.json) | File records could disappear from capped server pages. | Workbench maintainer; individual unknown. | Retained all change pages and exact-commit file reads. |
| [Traversal and page regressions](evidence/release-report-implementation-20261024/integration-regressions.json) | Commit-linked tests could be omitted. A failed Sonar page could leave a complete section. | Workbench maintainer; individual unknown. | Expanded discovered links and propagated partial pagination states. |
| [Renderer regressions](evidence/release-report-implementation-20261024/renderer-validation.json) | Conflicting identities and parser limits could bypass the expected report error boundary. | Workbench maintainer; individual unknown. | Rejected identity conflicts and normalized parser failures. |
| [Transport regressions](evidence/release-report-implementation-20261024/connector-validation.json) | Proxy trust, local write retries, throttling, and inline response limits could fail their contracts. | Workbench maintainer; individual unknown. | Preserved CA trust, restricted retries, reduced concurrency, and bounded MCP responses. |

## Remaining evidence limits

Mock execution does not establish deployed ADO contribution APIs, tenant fields, attachment formats, or Sonar version compatibility.
Coverage normalization supports numeric summary fields and line or branch covered/total statistics.
Other coverage formats retain raw evidence with unavailable summary values.
Sonar enrichment requires published build properties and preserves uncertain build association.
Production selection follows the supplied source and does not establish deployment approval.

The code has no known blocker within the authorized mock scope.
The deployment owner is unknown.
An authorized target-environment comparison remains the next action before claiming company endpoint compatibility.
The wheel reused installed dependencies. It did not test a new Windows installation or prepare another offline dependency bundle.

## Review status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Mock checks do not establish deployed service compatibility or production readiness.
```
